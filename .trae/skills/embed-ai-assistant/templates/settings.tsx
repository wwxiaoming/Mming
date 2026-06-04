// src/pages/settings/AISettings.tsx
// 设置页：配置 LLM + 快捷指令管理
import { useState } from 'react';
import { useAssistantStore } from '@/lib/ai-assistant/store';

export function AISettings() {
  const config = useAssistantStore(s => s.config);
  const updateConfig = useAssistantStore(s => s.updateConfig);
  const refreshModels = useAssistantStore(s => s.refreshModels);
  const models = useAssistantStore(s => s.models);
  const error = useAssistantStore(s => s.error);
  const quickActions = useAssistantStore(s => s.quickActions);
  const setQuickActions = useAssistantStore(s => s.setQuickActions);

  const [showKey, setShowKey] = useState(false);

  return (
    <div className="max-w-2xl mx-auto p-6 space-y-6 text-slate-100">
      <h1 className="text-xl font-semibold">AI 助手设置</h1>
      <p className="text-sm text-slate-400">所有信息仅保存在你的浏览器本地，不会上传到任何服务器。</p>

      <Field label="Base URL">
        <input
          className="w-full bg-slate-800 px-3 py-2 rounded"
          value={config.baseURL}
          onChange={e => updateConfig({ baseURL: e.target.value })}
          placeholder="https://api.deepseek.com/v1"
        />
      </Field>

      <Field label="API Key">
        <div className="flex gap-2">
          <input
            type={showKey ? 'text' : 'password'}
            className="flex-1 bg-slate-800 px-3 py-2 rounded"
            value={config.apiKey}
            onChange={e => updateConfig({ apiKey: e.target.value })}
            placeholder="sk-..."
          />
          <button onClick={() => setShowKey(s => !s)} className="px-3 py-2 bg-slate-700 rounded">
            {showKey ? '隐藏' : '显示'}
          </button>
        </div>
      </Field>

      <Field label="模型">
        <input
          className="w-full bg-slate-800 px-3 py-2 rounded"
          list="model-list"
          value={config.model}
          onChange={e => updateConfig({ model: e.target.value })}
        />
        <datalist id="model-list">
          {models.map(m => <option key={m} value={m} />)}
        </datalist>
      </Field>

      <Field label={`Temperature: ${config.temperature}`}>
        <input
          type="range" min={0} max={2} step={0.1}
          value={config.temperature}
          onChange={e => updateConfig({ temperature: Number(e.target.value) })}
        />
      </Field>

      <Field label="最大上下文轮数 N">
        <input
          type="number" min={1} max={50}
          className="w-24 bg-slate-800 px-3 py-2 rounded"
          value={config.maxHistoryRounds}
          onChange={e => updateConfig({ maxHistoryRounds: Number(e.target.value) })}
        />
      </Field>

      <Field label="请求超时(秒)">
        <input
          type="number" min={5} max={300}
          className="w-24 bg-slate-800 px-3 py-2 rounded"
          value={config.timeoutSec}
          onChange={e => updateConfig({ timeoutSec: Number(e.target.value) })}
        />
      </Field>

      <Field label="请求模式">
        <div className="flex gap-4 text-sm">
          <label><input type="radio" checked={config.mode === 'direct'} onChange={() => updateConfig({ mode: 'direct' })} /> 浏览器直连</label>
          <label><input type="radio" checked={config.mode === 'proxy'} onChange={() => updateConfig({ mode: 'proxy' })} /> 经本站代理（CORS 兜底）</label>
        </div>
        {config.mode === 'proxy' && (
          <input
            className="w-full mt-2 bg-slate-800 px-3 py-2 rounded"
            placeholder="/api/llm"
            value={config.proxyURL ?? ''}
            onChange={e => updateConfig({ proxyURL: e.target.value })}
          />
        )}
      </Field>

      <Field label="自定义系统提示词">
        <textarea
          rows={6}
          className="w-full bg-slate-800 px-3 py-2 rounded text-sm"
          value={config.systemPrompt}
          onChange={e => updateConfig({ systemPrompt: e.target.value })}
        />
        <p className="text-xs text-slate-500 mt-1">覆盖默认提示词。客户端会强制在每条消息末尾追加免责声明。</p>
      </Field>

      <div className="flex items-center gap-3">
        <button
          onClick={refreshModels}
          className="px-4 py-2 bg-blue-500 text-white rounded"
        >
          测试连接
        </button>
        {models.length > 0 && <span className="text-sm text-green-400">连接成功，检测到 {models.length} 个模型</span>}
        {error && <span className="text-sm text-red-400">{error}</span>}
      </div>

      <hr className="border-slate-700" />

      <h2 className="text-lg font-semibold">快捷指令</h2>
      <div className="space-y-2">
        {quickActions.map((qa, i) => (
          <div key={qa.id} className="bg-slate-800 p-3 rounded space-y-2">
            <input
              className="w-full bg-slate-900 px-2 py-1 rounded"
              value={qa.title}
              onChange={e => {
                const next = [...quickActions];
                next[i] = { ...qa, title: e.target.value };
                setQuickActions(next);
              }}
            />
            <textarea
              rows={2}
              className="w-full bg-slate-900 px-2 py-1 rounded text-sm"
              value={qa.prompt}
              onChange={e => {
                const next = [...quickActions];
                next[i] = { ...qa, prompt: e.target.value };
                setQuickActions(next);
              }}
            />
            <button
              onClick={() => setQuickActions(quickActions.filter((_, j) => j !== i))}
              className="text-xs text-red-400"
            >
              删除
            </button>
          </div>
        ))}
        <button
          onClick={() => setQuickActions([...quickActions, { id: String(Date.now()), title: '新指令', prompt: '' }])}
          className="px-3 py-1 bg-slate-700 rounded text-sm"
        >
          + 新增快捷指令
        </button>
      </div>
    </div>
  );
}

function Field({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <label className="block space-y-1">
      <span className="text-sm text-slate-300">{label}</span>
      {children}
    </label>
  );
}
