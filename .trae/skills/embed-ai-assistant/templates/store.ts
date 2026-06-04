// src/lib/ai-assistant/store.ts
// Zustand store + persist，封装抽屉状态、消息历史、配置、上下文注入
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import { OpenAICompatibleProvider } from '@/lib/llm/provider';
import { serializeContext } from './context';
import { DEFAULT_SYSTEM_PROMPT, DEFAULT_QUICK_ACTIONS } from './prompts';
import type { ContextPayload, LLMConfig, LLMMessage, PromptTemplate } from '@/lib/llm/types';

type State = {
  isOpen: boolean;
  config: LLMConfig;
  messages: LLMMessage[];
  loading: boolean;
  abortCtl: AbortController | null;
  draftContext: ContextPayload | null;
  quickActions: PromptTemplate[];
  models: string[];        // listModels 缓存
  error: string | null;

  // actions
  open: () => void;
  close: () => void;
  toggle: () => void;
  openWithContext: (ctx: ContextPayload, prefilled?: string) => void;
  setDraftContext: (ctx: ContextPayload | null) => void;
  send: (text: string) => Promise<void>;
  stop: () => void;
  reset: () => void;
  updateConfig: (patch: Partial<LLMConfig>) => void;
  setQuickActions: (qas: PromptTemplate[]) => void;
  refreshModels: () => Promise<void>;
};

const DEFAULT_CONFIG: LLMConfig = {
  baseURL: 'https://api.deepseek.com/v1',
  apiKey: '',
  model: 'deepseek-chat',
  temperature: 0.7,
  maxHistoryRounds: 10,
  timeoutSec: 60,
  systemPrompt: DEFAULT_SYSTEM_PROMPT,
  mode: 'direct',
};

export const useAssistantStore = create<State>()(
  persist(
    (set, get) => ({
      isOpen: false,
      config: DEFAULT_CONFIG,
      messages: [],
      loading: false,
      abortCtl: null,
      draftContext: null,
      quickActions: DEFAULT_QUICK_ACTIONS,
      models: [],
      error: null,

      open: () => set({ isOpen: true }),
      close: () => set({ isOpen: false }),
      toggle: () => set(s => ({ isOpen: !s.isOpen })),

      openWithContext: (ctx, prefilled) => {
        set({ isOpen: true, draftContext: ctx });
        if (prefilled) {
          // 让 UI 拿到一个"待发送"标记，自己决定是否自动 send
          // 简化：直接 send
          get().send(prefilled);
        }
      },

      setDraftContext: (ctx) => set({ draftContext: ctx }),

      send: async (text) => {
        const { config, messages, draftContext, maxHistoryRounds } = get();
        if (!config.apiKey) {
          set({ error: '请先在设置中配置 API Key' });
          get().open();
          return;
        }
        set({ error: null, loading: true });

        const abortCtl = new AbortController();
        set({ abortCtl });

        // 构造最终 messages
        const sysMsg: LLMMessage = { role: 'system', content: config.systemPrompt };
        const recent = messages.slice(-maxHistoryRounds * 2);
        const ctxMsg: LLMMessage | null = draftContext
          ? { role: 'system', content: serializeContext(draftContext) }
          : null;
        const userMsg: LLMMessage = { role: 'user', content: text };

        const finalMessages = [sysMsg, ...recent, ...(ctxMsg ? [ctxMsg] : []), userMsg];

        // 立即把 user 消息推入历史
        set(s => ({ messages: [...s.messages, userMsg] }));

        // 推一个空的 assistant 占位
        const assistantMsg: LLMMessage = { role: 'assistant', content: '' };
        set(s => ({ messages: [...s.messages, assistantMsg] }));

        const provider = new OpenAICompatibleProvider(config);
        try {
          await provider.chat({
            messages: finalMessages,
            signal: abortCtl.signal,
            onToken: (_delta, full) => {
              set(s => ({
                messages: s.messages.map((m, i) =>
                  i === s.messages.length - 1 ? { ...m, content: full } : m
                ),
              }));
            },
          });
        } catch (e: any) {
          set({ error: e?.message ?? '请求失败' });
        } finally {
          set({ loading: false, abortCtl: null, draftContext: null });
        }
      },

      stop: () => {
        get().abortCtl?.abort();
        set({ loading: false, abortCtl: null });
      },

      reset: () => set({ messages: [], draftContext: null, error: null }),

      updateConfig: (patch) => set(s => ({ config: { ...s.config, ...patch } })),

      setQuickActions: (qas) => set({ quickActions: qas }),

      refreshModels: async () => {
        const { config } = get();
        if (!config.apiKey) {
          set({ models: [], error: '请先填 API Key' });
          return;
        }
        try {
          const list = await new OpenAICompatibleProvider(config).listModels();
          set({ models: list.map(m => m.id), error: null });
        } catch (e: any) {
          set({ error: e?.message ?? '获取模型失败' });
        }
      },
    }),
    {
      name: 'ai-assistant',
      storage: createJSONStorage(() => localStorage),
      partialize: (s) => ({
        isOpen: s.isOpen,
        config: s.config,
        messages: s.messages.slice(-100), // 截断持久化
        quickActions: s.quickActions,
      }),
      onRehydrateStorage: () => (s) => {
        s?.setDraftContext(null);
        s?.stop();
      },
    }
  )
);
