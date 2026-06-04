# 上下文管理

## 1. 三层上下文模型

```
┌────────────────────────────────────────────┐
│  ① System Prompt（永久）                  │
│     - 用户自定义，或默认提示词             │
│     - 包含免责声明指令                     │
├────────────────────────────────────────────┤
│  ② 附加上下文（仅本轮）                    │
│     - K 线摘要、自选股、策略代码…          │
│     - 序列化为 system 消息，置于本轮末尾   │
│     - 不进入持久化 messages                │
├────────────────────────────────────────────┤
│  ③ 历史消息（按 N 轮裁剪）                 │
│     - 最近 N 轮 user/assistant             │
│     - 超出 N 轮的丢弃                       │
└────────────────────────────────────────────┘
```

最终请求 payload：

```json
{
  "messages": [
    {"role": "system", "content": "<①>"},
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."},
    ...裁剪到 N 轮,
    {"role": "system", "content": "<②附加上下文>"},
    {"role": "user", "content": "<本轮用户输入>"}
  ]
}
```

## 2. 上下文包（ContextPayload）设计

```ts
type ContextPayload = {
  stock?: {
    code: string,
    name: string,
    price: number,
    changePct: number,
  },
  klineSummary?: string,      // 序列化为表格/Markdown
  watchlist?: { code: string, name: string }[],
  strategy?: {
    name: string,
    buyRule: string,           // 自然语言
    sellRule: string,
  },
  custom?: Record<string, string>, // 用户自定义键值
  extra?: string,             // 自由文本
}
```

## 3. 序列化模板

```ts
export function serializeContext(ctx: ContextPayload): string {
  const parts: string[] = ['[本轮附加上下文]'];
  if (ctx.stock) parts.push(`当前股票：${ctx.stock.code} ${ctx.stock.name}，最新价 ${ctx.stock.price}（${ctx.stock.changePct >= 0 ? '+' : ''}${ctx.stock.changePct}%）`);
  if (ctx.klineSummary) parts.push(`K 线摘要：\n${ctx.klineSummary}`);
  if (ctx.watchlist?.length) parts.push(`自选股：${ctx.watchlist.map(s => `${s.code} ${s.name}`).join('、')}`);
  if (ctx.strategy) parts.push(`当前策略「${ctx.strategy.name}」：\n- 买入：${ctx.strategy.buyRule}\n- 卖出：${ctx.strategy.sellRule}`);
  if (ctx.extra) parts.push(`附加信息：\n${ctx.extra}`);
  return parts.join('\n\n');
}
```

## 4. 业务页面主动注入示例

```tsx
// 行情页
import { useAssistantStore } from '@/lib/ai-assistant/store';

function StockPage({ stock, klineSummary }) {
  const openWithContext = useAssistantStore(s => s.openWithContext);
  
  return (
    <button onClick={() => openWithContext(
      { stock, klineSummary },
      '请帮我分析这只股票的近期走势'
    )}>
      🤖 AI 分析
    </button>
  );
}
```

## 5. 注意点

- **不要把附加上下文写进 system prompt**（会污染所有未来对话）
- **不要把用户输入和附加上下文合并**（会丢失"用户原话"信息）
- **超过 ~3000 字符的上下文要截断**，避免 token 超限
- **永远不要把 apiKey 写进上下文**（万一 echo 到前端就是泄露）
- **图片/PDF 上下文** 走 vision 模型的 `image_url` 字段（v2 再加）
