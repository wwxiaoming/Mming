// src/lib/ai-assistant/context.ts
// 上下文序列化：把 ContextPayload 打包成一段 system 消息文本
import type { ContextPayload } from '@/lib/llm/types';

export function serializeContext(ctx: ContextPayload): string {
  const parts: string[] = ['[本轮附加上下文]'];
  if (ctx.stock) {
    const sign = ctx.stock.changePct >= 0 ? '+' : '';
    parts.push(
      `当前股票：${ctx.stock.code} ${ctx.stock.name}，最新价 ${ctx.stock.price}（${sign}${ctx.stock.changePct}%）`
    );
  }
  if (ctx.klineSummary) {
    parts.push(`K 线摘要：\n${ctx.klineSummary}`);
  }
  if (ctx.watchlist?.length) {
    parts.push(`自选股：${ctx.watchlist.map(s => `${s.code} ${s.name}`).join('、')}`);
  }
  if (ctx.strategy) {
    parts.push(
      `当前策略「${ctx.strategy.name}」：\n- 买入：${ctx.strategy.buyRule}\n- 卖出：${ctx.strategy.sellRule}`
    );
  }
  if (ctx.custom) {
    const lines = Object.entries(ctx.custom).map(([k, v]) => `- ${k}：${v}`).join('\n');
    if (lines) parts.push(`附加字段：\n${lines}`);
  }
  if (ctx.extra) parts.push(`附加信息：\n${ctx.extra}`);

  // 防御性截断
  const text = parts.join('\n\n');
  return text.length > 3000 ? text.slice(0, 3000) + '\n...(已截断)' : text;
}

export function fillTemplate(tpl: string, vars: Record<string, string>): string {
  return tpl.replace(/\{\{(\w+)\}\}/g, (_, k) => vars[k] ?? `{{${k}}}`);
}
