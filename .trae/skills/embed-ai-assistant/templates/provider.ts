// src/lib/llm/provider.ts
// OpenAI 兼容 Provider，支持流式、Abort、超时、CORS 兜底
import type { ChatOptions, LLMConfig, ModelInfo } from './types';

export class OpenAICompatibleProvider {
  constructor(private config: LLMConfig) {}

  private get url() {
    const base = (this.config.proxyURL && this.config.mode === 'proxy')
      ? this.config.proxyURL.replace(/\/+$/, '')
      : this.config.baseURL.replace(/\/+$/, '');
    return `${base}/chat/completions`;
  }

  private get headers() {
    return {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${this.config.apiKey}`,
    };
  }

  async chat(opts: ChatOptions): Promise<string> {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), this.config.timeoutSec * 1000);

    // 串联外部 signal
    if (opts.signal) {
      if (opts.signal.aborted) controller.abort();
      opts.signal.addEventListener('abort', () => controller.abort());
    }

    try {
      const res = await fetch(this.url, {
        method: 'POST',
        headers: this.headers,
        body: JSON.stringify({
          model: this.config.model,
          messages: opts.messages,
          temperature: this.config.temperature,
          stream: true,
        }),
        signal: controller.signal,
      });

      if (!res.ok || !res.body) {
        const text = await res.text().catch(() => '');
        throw new Error(`HTTP ${res.status} ${res.statusText}: ${text.slice(0, 200)}`);
      }

      return await parseSSE(res.body, {
        onToken: opts.onToken,
        onDone: opts.onDone,
        onError: opts.onError,
        signal: controller.signal,
      });
    } catch (e: any) {
      if (e.name === 'AbortError') {
        opts.onError?.(new Error('请求已停止'));
      } else {
        opts.onError?.(e);
      }
      throw e;
    } finally {
      clearTimeout(timeout);
    }
  }

  async listModels(): Promise<ModelInfo[]> {
    const base = (this.config.proxyURL && this.config.mode === 'proxy')
      ? this.config.proxyURL.replace(/\/+$/, '')
      : this.config.baseURL.replace(/\/+$/, '');
    const res = await fetch(`${base}/models`, {
      headers: { Authorization: `Bearer ${this.config.apiKey}` },
    });
    if (!res.ok) throw new Error(`HTTP ${res.status} ${res.statusText}`);
    const data = await res.json();
    return data.data ?? [];
  }
}

// SSE 解析：把 ReadableStream 切成一个个 token 回调
export async function parseSSE(
  body: ReadableStream<Uint8Array>,
  cb: {
    onToken?: (delta: string, full: string) => void;
    onDone?: (full: string) => void;
    onError?: (e: Error) => void;
    signal: AbortSignal;
  }
): Promise<string> {
  const reader = body.getReader();
  const decoder = new TextDecoder('utf-8');
  let buffer = '';
  let full = '';

  try {
    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });

      let sepIdx: number;
      while ((sepIdx = buffer.indexOf('\n\n')) !== -1) {
        const event = buffer.slice(0, sepIdx);
        buffer = buffer.slice(sepIdx + 2);

        for (const line of event.split('\n')) {
          const trimmed = line.trim();
          if (!trimmed.startsWith('data:')) continue;
          const payload = trimmed.slice(5).trim();
          if (payload === '[DONE]') {
            cb.onDone?.(full);
            return full;
          }
          try {
            const json = JSON.parse(payload);
            const delta = json.choices?.[0]?.delta?.content ?? '';
            if (delta) {
              full += delta;
              cb.onToken?.(delta, full);
            }
          } catch {
            // 忽略坏行
          }
        }
      }
    }
    cb.onDone?.(full);
    return full;
  } catch (e: any) {
    if (e.name !== 'AbortError') cb.onError?.(e);
    throw e;
  } finally {
    try { reader.releaseLock(); } catch {}
  }
}
