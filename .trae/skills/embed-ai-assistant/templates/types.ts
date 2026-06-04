// src/lib/llm/types.ts
// 全部类型集中在这里，方便 import

export type LLMMessageRole = 'system' | 'user' | 'assistant';

export interface LLMMessage {
  role: LLMMessageRole;
  content: string;
}

export type RequestMode = 'direct' | 'proxy';

export interface LLMConfig {
  baseURL: string;          // 例: https://api.deepseek.com/v1
  apiKey: string;           // base64 编码后存盘
  model: string;            // 例: deepseek-chat
  temperature: number;      // 0~2
  maxHistoryRounds: number; // 1~50
  timeoutSec: number;       // 5~300
  systemPrompt: string;     // 自定义系统提示词
  mode: RequestMode;        // direct / proxy
  proxyURL?: string;        // mode=proxy 时的代理地址
}

export interface ContextPayload {
  stock?: { code: string; name: string; price: number; changePct: number };
  klineSummary?: string;
  watchlist?: { code: string; name: string }[];
  strategy?: { name: string; buyRule: string; sellRule: string };
  custom?: Record<string, string>;
  extra?: string;
}

export interface ChatOptions {
  messages: LLMMessage[];
  signal?: AbortSignal;
  onToken?: (delta: string, full: string) => void;
  onDone?: (full: string) => void;
  onError?: (err: Error) => void;
}

export interface ModelInfo {
  id: string;
  owned_by?: string;
}
