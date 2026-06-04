// src/components/ai-assistant/Drawer.tsx
// 抽屉 + Header + 消息列表 + 输入框 的最小可用整合
// 用 Tailwind + lucide-react 示意，实际可换 shadcn / antd
import { useEffect, useRef, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { useAssistantStore } from '@/lib/ai-assistant/store';
import { X, Plus, Settings, RefreshCw, Square, Send, Paperclip } from 'lucide-react';

const DISCLAIMER = '⚠️ 以上分析仅供参考，不构成投资建议';

export function AssistantDrawer() {
  const isOpen = useAssistantStore(s => s.isOpen);
  const close = useAssistantStore(s => s.close);
  const messages = useAssistantStore(s => s.messages);
  const loading = useAssistantStore(s => s.loading);
  const config = useAssistantStore(s => s.config);
  const send = useAssistantStore(s => s.send);
  const stop = useAssistantStore(s => s.stop);
  const reset = useAssistantStore(s => s.reset);
  const quickActions = useAssistantStore(s => s.quickActions);
  const openWithContext = useAssistantStore(s => s.openWithContext);

  const [input, setInput] = useState('');
  const listRef = useRef<HTMLDivElement>(null);

  // 自动滚动
  useEffect(() => {
    if (listRef.current) listRef.current.scrollTop = listRef.current.scrollHeight;
  }, [messages.length, messages[messages.length - 1]?.content]);

  // Esc 关闭
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => { if (e.key === 'Escape') close(); };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [close]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-y-0 right-0 w-[400px] max-w-full z-50 bg-slate-900 text-slate-100 shadow-2xl flex flex-col border-l border-slate-700">
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-slate-700">
        <div className="flex items-center gap-2 font-medium">
          <span className="text-lg">🤖</span> AI 量化助手
        </div>
        <div className="flex items-center gap-1 text-sm">
          <span className="px-2 py-1 rounded bg-slate-800">{config.model || '未配置'}</span>
          <button onClick={reset} className="p-1 hover:bg-slate-800 rounded" title="新建对话">
            <RefreshCw size={16} />
          </button>
          <a href="/settings/ai" className="p-1 hover:bg-slate-800 rounded" title="设置">
            <Settings size={16} />
          </a>
          <button onClick={close} className="p-1 hover:bg-slate-800 rounded" title="关闭">
            <X size={16} />
          </button>
        </div>
      </div>

      {/* 消息列表 */}
      <div ref={listRef} className="flex-1 overflow-y-auto px-4 py-3 space-y-3">
        {messages.length === 0 ? (
          <div className="text-slate-300 text-sm space-y-3">
            <p>您好！我是您的 AI 量化助手 👋</p>
            <p>请选择您想做的事情：</p>
            <div className="space-y-2">
              {quickActions.map(qa => (
                <button
                  key={qa.id}
                  onClick={() => send(qa.prompt)}
                  className="w-full text-left px-3 py-2 rounded border border-slate-700 hover:border-blue-500 hover:bg-slate-800"
                >
                  {qa.title}
                </button>
              ))}
            </div>
          </div>
        ) : (
          messages.map((m, i) => (
            <div key={i} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`max-w-[85%] px-3 py-2 rounded-lg text-sm whitespace-pre-wrap break-words ${
                m.role === 'user' ? 'bg-blue-600 text-white' : 'bg-slate-800 text-slate-100'
              }`}>
                {m.role === 'assistant' ? (
                  <>
                    <ReactMarkdown remarkPlugins={[remarkGfm]}>{m.content || (loading && i === messages.length - 1 ? '...' : '')}</ReactMarkdown>
                    {m.content && <div className="mt-2 text-xs text-slate-400">{DISCLAIMER}</div>}
                  </>
                ) : m.content}
              </div>
            </div>
          ))
        )}
      </div>

      {/* 底部提示 */}
      <div className="px-4 py-1 text-xs text-slate-500 border-t border-slate-800">
        AI 会记住本次对话的上下文，点 <span className="font-bold">+</span> 开始新对话
      </div>

      {/* 输入框 */}
      <div className="p-3 border-t border-slate-700">
        <div className="flex items-end gap-2">
          <button
            onClick={() => openWithContext({}, '')}
            className="p-2 text-slate-400 hover:text-slate-100"
            title="附加上下文"
          >
            <Paperclip size={16} />
          </button>
          <textarea
            value={input}
            onChange={e => setInput(e.target.value.slice(0, 500))}
            onKeyDown={e => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                if (!loading && input.trim()) { send(input.trim()); setInput(''); }
              }
            }}
            placeholder="请输入问题... (按 Enter 发送)"
            rows={1}
            className="flex-1 resize-none bg-slate-800 text-slate-100 rounded px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-blue-500"
          />
          {loading ? (
            <button onClick={stop} className="p-2 rounded bg-orange-500 text-white" title="停止">
              <Square size={16} />
            </button>
          ) : (
            <button
              onClick={() => { if (input.trim()) { send(input.trim()); setInput(''); } }}
              disabled={!input.trim()}
              className="p-2 rounded bg-blue-500 text-white disabled:opacity-40"
              title="发送"
            >
              <Send size={16} />
            </button>
          )}
        </div>
        <div className="text-right text-xs text-slate-500 mt-1">{input.length}/500</div>
      </div>
    </div>
  );
}

// 在 App.tsx 挂载：
// import { AssistantDrawer } from '@/components/ai-assistant/Drawer';
// <AssistantDrawer />
