---
name: embed-ai-assistant
description: 在任意 Web 网站中嵌入"侧边抽屉式 AI 助手"——既能自由聊天，又能结合当前页面上下文（K 线/自选股/策略代码等）做 AI 分析；API 完全由用户在"设置"中自由配置（Base URL、API Key、模型名），兼容任何 OpenAI Chat Completions 协议的服务（DeepSeek、OpenAI、Moonshot、智谱、Together、Groq、Ollama、vLLM 等）。当用户说"在网站里塞入 AI 聊天/助手/分析"、"想接入自己的 API Key"、"让用户自己设置 LLM"、"做一个 AI 侧边栏"、"GPT 聊天抽屉"、"网站 AI 助手"等场景时使用。
---

# Embed AI Assistant

## 一句话定位

给你的网站加一个**像 ChatGPT 一样能聊天、又能"看见"当前页面并做 AI 分析**的侧边抽屉，**API 完全由最终用户在"设置"里自己填**，零成本、零后端、可换源。

## 何时使用本 skill

触发关键词（命中任一即应优先加载本 skill）：

- "在网站里塞入/嵌入 AI 聊天"、"做一个 AI 助手/AI 侧边栏/AI 抽屉"
- "用户能在设置里自由配置 API/Key/模型/Base URL"
- "兼容 OpenAI/DeepSeek/通义/智谱/...的聊天 API"
- "AI 分析当前页内容/数据（K 线、策略代码、表格…）"
- "做一个 Quant/Copilot 助手"

**不要**用于：纯后端 LLM 微调、模型训练、Prompt Engineering 学术研究、与"在网站里嵌入"无关的纯 LLM 脚本。

## 核心架构（30 秒看完）

```
┌─────────────────────────────────────────────────────────────┐
│  Browser                                                     │
│  ┌──────────────┐  ┌──────────────────┐  ┌──────────────┐  │
│  │ 业务页面     │──│  AI Assistant    │──│ Settings     │  │
│  │ (K线/策略…)  │  │ Drawer (全局)    │  │ Modal/路由   │  │
│  └──────────────┘  └────┬─────────────┘  └──────┬───────┘  │
│        │  inject ctx     │                       │          │
│        ▼                 ▼                       ▼          │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  useAssistantStore  (Zustand + persist → localStorage)│  │
│  │  - messages / model / loading / abortController      │  │
│  └────────────────────────┬─────────────────────────────┘  │
│                           ▼                                │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  OpenAICompatibleProvider                            │  │
│  │  - chat({messages, stream, signal})                  │  │
│  │  - listModels()                                      │  │
│  │  - 模式: direct / proxy (CORS 兜底)                  │  │
│  └────────────────────────┬─────────────────────────────┘  │
└───────────────────────────┼─────────────────────────────────┘
                            │ HTTPS
                            ▼
                  ┌──────────────────────┐
                  │ 用户配置的 LLM 服务   │
                  │ (DeepSeek / OpenAI…) │
                  └──────────────────────┘
```

**关键决策：**

1. **不内置 Key、不托管后端**：让用户填自己的 Key，从浏览器直发（或可选自建代理），避免泄露和服务商合规问题。
2. **OpenAI 兼容协议**作为唯一接口：DeepSeek、Moonshot、智谱、Together、Groq、OpenRouter、Ollama (`/v1`)、vLLM、LM Studio 默认就支持这一套，写一次 Provider 就能跑通所有源。
3. **流式 (SSE) 是标配**：用 `fetch` + `ReadableStream` 逐 token 渲染，体验才能"打字机"。
4. **上下文分两层**：系统提示（永久）+ 附加上下文（仅本轮）+ 历史消息（按 N 轮裁剪）。
5. **localStorage 持久化**：配置、快捷指令、历史都放本地；多会话可后续扩展。

## 目录结构

```
src/
├── components/
│   └── ai-assistant/
│       ├── Drawer.tsx              # 容器：右侧滑出
│       ├── Header.tsx              # 标题/模型下拉/新建/关闭/设置
│       ├── MessageList.tsx         # 消息流
│       ├── MessageItem.tsx         # 单条消息（Markdown + 免责声明）
│       ├── InputBar.tsx            # 输入框 + 字数 + 停止
│       ├── QuickActions.tsx        # 空状态欢迎语 + 快捷气泡
│       ├── ContextPicker.tsx       # "+" 弹出的上下文选择
│       └── Disclaimer.tsx          # 免责声明组件
├── lib/
│   ├── llm/
│   │   ├── types.ts                # LLMConfig / LLMMessage
│   │   ├── provider.ts             # OpenAICompatibleProvider
│   │   ├── sse.ts                  # 流式解析
│   │   └── storage.ts              # 配置/历史的 localStorage 封装
│   └── ai-assistant/
│       ├── store.ts                # Zustand store
│       ├── prompts.ts              # 默认系统提示词 + 预置快捷指令
│       └── context.ts              # 上下文裁剪逻辑
├── pages/
│   └── settings/
│       └── AISettings.tsx          # 设置页/弹层
└── App.tsx                         # 挂载 <AssistantDrawer /> + <AISettings />
```

## 必读子文档

| 文件 | 何时读 |
|---|---|
| [references/architecture.md](references/architecture.md) | 想了解整体设计决策与扩展点 |
| [references/provider.md](references/provider.md) | 写 LLM Provider / 流式 / CORS 兜底时 |
| [references/ui.md](references/ui.md) | 写抽屉 / 设置 / 消息 UI 时 |
| [references/context.md](references/context.md) | 处理"附加上下文"与历史裁剪时 |
| [references/storage.md](references/storage.md) | 处理 localStorage 持久化时 |
| [references/prompts.md](references/prompts.md) | 调整系统提示词 / 快捷指令文案时 |

## 必拷代码模板

| 模板 | 用途 |
|---|---|
| [templates/provider.ts](templates/provider.ts) | OpenAI 兼容 Provider 完整实现 |
| [templates/store.ts](templates/store.ts) | Zustand store + 持久化 |
| [templates/drawer.tsx](templates/drawer.tsx) | 抽屉 + Header + InputBar 一体 |
| [templates/settings.tsx](templates/settings.tsx) | 设置面板 |
| [templates/types.ts](templates/types.ts) | 类型定义 |

## 落地清单（最小可用版本 MVP）

1. 复制 `templates/types.ts` → `src/lib/llm/types.ts`
2. 复制 `templates/provider.ts` → `src/lib/llm/provider.ts`
3. 复制 `templates/store.ts` → `src/lib/ai-assistant/store.ts`
4. 复制 `templates/drawer.tsx` → `src/components/ai-assistant/Drawer.tsx`
5. 复制 `templates/settings.tsx` → `src/pages/settings/AISettings.tsx`
6. 在 `App.tsx` 挂载 `<AssistantDrawer />` 和 `<AISettingsTrigger />`
7. 在你想接入的业务页面调用 `useAssistantStore.getState().openWithContext({...})`

完成后用 [references/provider.md §3 自检清单](references/provider.md) 与 [references/ui.md §4 自检清单](references/ui.md) 逐条核对。

## 反模式（不要这样做）

- ❌ 在前端代码里 hardcode 任何人的 API Key
- ❌ 用 `axios` 走非流式（体验差、容易超时）
- ❌ 把聊天历史存到自家后端（合规风险）
- ❌ 自创协议（必须 OpenAI 兼容，否则每加一个源要重写）
- ❌ 把"附加上下文"写进系统提示词（会污染所有未来对话）
- ❌ 在生产中明文把 Key 放到 localStorage 而不提示用户

## 扩展方向（v2 再考虑）

- 多会话（侧边栏会话列表 + 命名）
- 图片/文件上传（Vision 模型）
- 工具调用 / Function Calling（让助手能调业务接口）
- 服务端代理模式（解决 CORS 同时隐藏 Key）
- 团队共享预设（管理员下发快捷指令）
