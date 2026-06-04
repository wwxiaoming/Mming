# Architecture

## 设计目标

1. **零后端依赖**：纯前端即可工作（业务方不需要部署任何服务）。
2. **可换源**：用户换一家 LLM 服务商不需要改任何代码。
3. **可扩展**：业务页面可以"主动"把当前数据塞进对话。
4. **可观测**：配置、错误、超时、token 消耗都有日志/UI 反馈。

## 模块划分

### 1. UI 层（`components/ai-assistant/*`）

- **Drawer**：最外层容器，负责开关动画、遮罩、键盘 Esc 关闭。
- **Header**：标题、模型下拉、新建对话、设置入口、关闭。
- **MessageList / MessageItem**：消息流，区分 user/assistant 气泡，Markdown 渲染。
- **InputBar**：多行输入 + 字符计数 + 停止生成按钮。
- **QuickActions**：空状态欢迎语 + 预置快捷指令气泡。
- **ContextPicker**：点击"+"弹出的上下文选择面板（K 线、策略代码…）。
- **Disclaimer**：每条助手消息末尾固定追加的小字。

### 2. 状态层（`lib/ai-assistant/store.ts`）

基于 Zustand（推荐）或 Jotai，持有：

```ts
{
  isOpen: boolean,
  config: LLMConfig,              // 当前激活的配置
  messages: LLMMessage[],        // 当前会话历史
  loading: boolean,              // 是否正在生成
  abortCtl: AbortController | null,
  draftContext: ContextPayload | null,  // 本轮待注入的上下文
  // actions
  open(), close(), toggle(),
  openWithContext(ctx, prefilledText?),
  send(text), stop(), reset(),
  updateConfig(patch),
}
```

持久化（用 `zustand/middleware/persist`）：
- ✅ `config`、`draftContext`、`messages` 写入 localStorage
- ❌ `loading`、`abortCtl` 写入（运行时态，刷新后必须重置）

### 3. 通信层（`lib/llm/*`）

- **types.ts**：`LLMConfig`（baseURL/apiKey/model/temperature/maxHistory/systemPrompt/mode/timeout）、`LLMMessage`（role/content）、`ContextPayload`
- **provider.ts**：`OpenAICompatibleProvider` 实现 `chat()`、`listModels()`
- **sse.ts**：`parseSSE(stream, onToken, onDone, onError)` 解析 `data: {...}\n\n`
- **storage.ts**：`getConfig()` / `saveConfig()`，对 apiKey 至少 base64 编码一次

### 4. 上下文层（`lib/ai-assistant/context.ts`）

- 把"附加上下文"作为 `system` 消息插入本轮请求的**最末尾**（在历史之后）
- 永不进入持久化的 `messages`
- 历史裁剪：保留系统提示 + 最近 N 轮 user/assistant

### 5. 设置层（`pages/settings/AISettings.tsx`）

- 表单 + 校验
- "测试连接"按钮 → 调 `listModels()`
- 错误提示分类：401（Key 错）、403（额度/权限）、CORS、timeout

## 数据流（一次"用户发送消息"）

```
[User 按 Enter]
    │
    ▼
useAssistantStore.send(text)
    │
    ├── 构造 messages: [
    │     { role: 'system', content: systemPrompt },
    │     ...history.slice(-N*2),
    │     { role: 'system', content: serialize(ctx) }, // 附加上下文，仅本轮
    │     { role: 'user', content: text }
    │   ]
    │
    ▼
provider.chat({ messages, stream: true, signal: abortCtl.signal })
    │
    ▼
fetch(baseURL + '/chat/completions', { method: POST, body: { ..., stream: true } })
    │
    ▼
parseSSE(body) ──onToken──▶ store.appendToken(delta) ─▶ MessageItem 重渲染
                                                ──onDone──▶ store.finalize()
                                                ──onError──▶ store.setError()
```

## 关键决策记录（ADR 摘要）

| 决策 | 选项 | 选择 | 理由 |
|---|---|---|---|
| 协议 | OpenAI/Anthropic/自创 | **OpenAI 兼容** | 95% 服务商支持，模型最丰富 |
| 持久化 | localStorage / IndexedDB | **localStorage** | 5MB 足够存配置与近期历史，零依赖 |
| 状态库 | Redux / Zustand / Jotai | **Zustand** | API 极简、persist 中间件开箱即用 |
| 流式 | fetch+ReadableStream / EventSource | **fetch+ReadableStream** | 支持 POST、可自定义 headers、POST body |
| Key 加密 | 原文 / base64 / Web Crypto | **base64 + 提示** | 防误读，不防专业攻击；v2 可加 Web Crypto |
| Markdown | dangerouslySetInnerHTML / react-markdown | **react-markdown** | XSS 安全，可扩展 GFM、代码高亮 |
| 上下文注入 | system / user 消息 | **临时 system 消息** | 清晰区分、不污染历史 |
| 请求模式 | 直连 / 代理 | **默认直连 + 可选代理** | 直连零成本，遇到 CORS 再切代理 |

## 扩展点

- `LLMProvider` 接口已抽象，后续可加 AnthropicProvider、GeminiProvider
- `ContextPayload` 是 union type，可加 `'table' | 'chart-snapshot' | 'pdf' | 'image'` 等新类型
- 快捷指令是 `PromptTemplate[]`，可加占位符替换、版本号
- 设置页是独立组件，可整页也可改弹层
