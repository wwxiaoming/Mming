# Provider & LLM 通信层

## 1. 为什么选 OpenAI 兼容协议

几乎所有主流 LLM 服务商都提供 OpenAI 兼容的 `/v1/chat/completions` 接口：

| 服务 | Base URL 示例 |
|---|---|
| DeepSeek | `https://api.deepseek.com/v1` |
| OpenAI | `https://api.openai.com/v1` |
| Moonshot (Kimi) | `https://api.moonshot.cn/v1` |
| 智谱 GLM | `https://open.bigmodel.cn/api/paas/v4`（注意：有的不是 v1） |
| 阿里 DashScope（兼容模式） | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| Together | `https://api.together.xyz/v1` |
| Groq | `https://api.groq.com/openai/v1` |
| OpenRouter | `https://openrouter.ai/api/v1` |
| Ollama (本地) | `http://localhost:11434/v1` |
| LM Studio (本地) | `http://localhost:1234/v1` |
| vLLM (自部署) | `http://your-host:8000/v1` |

**注意**：智谱 GLM 走的是 `v4` 路径不是 `v1`，需要在 `chat()` 里特殊处理或允许用户在 Base URL 里写完整路径。

## 2. SSE 流式解析要点

OpenAI 兼容接口的流式响应是 `text/event-stream`：

```
data: {"id":"...","object":"chat.completion.chunk","choices":[{"delta":{"content":"你"},"index":0}]}

data: {"id":"...","object":"chat.completion.chunk","choices":[{"delta":{"content":"好"},"index":0}]}

data: [DONE]
```

注意点：

1. **每个 event 以 `\n\n` 分隔**，不是 `\n`
2. **`data: [DONE]` 是结束标志**，收到后立即 `onDone()`，不要试图 JSON.parse
3. **某些代理/CDN 会把多个 event 合并**，要用 `buf.split('\n\n')` 循环处理剩余 buffer
4. **断网/超时**：`fetch` 会抛 `TypeError`，要 catch 包装成友好错误
5. **Abort**：监听 `signal.aborted` 立即 `reader.cancel()`

## 3. 自检清单（写完 Provider 后逐条核对）

- [ ] `baseURL` 自动补全末尾斜杠、`/chat/completions` 拼接正确
- [ ] `apiKey` 空时拒绝请求并提示
- [ ] 流式 `onToken` 收到的 token 顺序与终端输出一致
- [ ] 收到 `[DONE]` 立即触发 `onDone`，不再触发 `onToken`
- [ ] `AbortController.abort()` 后流立即停止，无残留 token
- [ ] 超时（默认 60s）触发后抛出 `TimeoutError` 并 `onError`
- [ ] HTTP 401/403/429/5xx 都有友好提示
- [ ] `listModels()` 用 GET `/models`，无 Key 时也能给"未授权"提示
- [ ] "浏览器直连"遇到 CORS 错误时，UI 提示用户切换"经代理"模式

## 4. CORS 兜底

前端直连最大的坑是 CORS。两种处理：

### A. 提示用户换源
很多托管服务（OpenAI/DeepSeek/Moonshit）**不允许**浏览器直连，浏览器会报：
```
Access to fetch at '...' from origin '...' has been blocked by CORS policy
```
这种必须在设置里给提示：建议用支持 CORS 的服务（如 OpenRouter），或自建代理。

### B. 自建代理（可选）
在你自己可控的服务器上：
```ts
// /api/llm/chat  (Node)
app.post('/api/llm/chat', async (req, res) => {
  const r = await fetch(req.body.baseURL + '/chat/completions', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${req.body.apiKey}`,
    },
    body: JSON.stringify(req.body.payload),
  });
  // ... pipe stream back
});
```
然后在 Provider 里 `mode === 'proxy'` 时把请求发到 `/api/llm/chat`。

## 5. 请求体最小示例

```json
{
  "model": "deepseek-chat",
  "messages": [
    {"role": "system", "content": "你是助手"},
    {"role": "user", "content": "你好"}
  ],
  "temperature": 0.7,
  "stream": true
}
```

`stream: true` 是流式开关；非流式场景把 `onToken` 替换成一次性 `onComplete(fullText)`。
