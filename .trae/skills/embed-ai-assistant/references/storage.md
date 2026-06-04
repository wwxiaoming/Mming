# 本地存储

## 1. localStorage Key 约定

| Key | 内容 | 大小预估 |
|---|---|---|
| `ai-assistant.config` | LLMConfig | < 1KB |
| `ai-assistant.messages` | LLMMessage[] | 取决于 N，建议截断到最近 50 轮 |
| `ai-assistant.quickActions` | PromptTemplate[] | < 2KB |
| `ai-assistant.drawerOpen` | boolean | < 0.1KB |
| `ai-assistant.disclaimerAck` | boolean | < 0.1KB |

## 2. API Key 的处理

- **至少 base64 编码一次**：防 `view-source:` 一眼看到原文
- **不要存 cookie**：会被服务端日志记录
- **不要用 sessionStorage**：刷新即丢，体验差
- **v2 升级方向**：用 Web Crypto + 用户密码派生密钥加密，但用户每次要输密码解锁

```ts
// 写入
const encoded = btoa(unescape(encodeURIComponent(apiKey)));
localStorage.setItem('ai-assistant.config', JSON.stringify({ ...rest, apiKey: encoded }));

// 读取
const { apiKey } = JSON.parse(localStorage.getItem('ai-assistant.config')!);
const decoded = decodeURIComponent(escape(atob(apiKey)));
```

## 3. 持久化封装（Zustand persist）

```ts
import { persist, createJSONStorage } from 'zustand/middleware';

export const useAssistantStore = create(
  persist(
    (set, get) => ({ ... }),
    {
      name: 'ai-assistant',
      storage: createJSONStorage(() => localStorage),
      partialize: (state) => ({
        config: state.config,
        messages: state.messages.slice(-100),  // 截断
        quickActions: state.quickActions,
        drawerOpen: state.drawerOpen,
      }),
      onRehydrateStorage: () => (state) => {
        // 恢复后清空运行时态
        state?.setLoading(false);
        state?.setAbortCtl(null);
      },
    }
  )
);
```

## 4. 多 tab 同步（可选）

```ts
window.addEventListener('storage', (e) => {
  if (e.key === 'ai-assistant.config') {
    useAssistantStore.getState().refreshConfig();
  }
});
```

## 5. 错误处理

- `localStorage` 满了（5MB）：捕获 `QuotaExceededError`，提示用户清理历史
- 用户开了"无痕模式"：写入失败时降级到内存，仅本次会话可用
- JSON.parse 异常：清掉这个 key，给默认值
