# Tasks

- [ ] Task 1: 搭建项目骨架与基础依赖
  - [ ] SubTask 1.1: 初始化 React + Vite + TypeScript 项目，引入 Tailwind / shadcn 风格 UI 基础
  - [ ] SubTask 1.2: 加入状态管理（Zustand 或 Jotai）与持久化中间件（localStorage）
  - [ ] SubTask 1.3: 选定图标库（lucide-react）与 Markdown 渲染库（react-markdown + remark-gfm）

- [ ] Task 2: 实现 LLM Provider 抽象层（`src/lib/llm/`）
  - [ ] SubTask 2.1: 定义 `LLMConfig` 与 `LLMMessage` 类型
  - [ ] SubTask 2.2: 实现 `OpenAICompatibleProvider`，支持 `chat/completions` 流式与非流式请求
  - [ ] SubTask 2.3: 实现 SSE/ReadableStream 解析，逐 token 回调
  - [ ] SubTask 2.4: 实现 `listModels()` 调用 `GET /models`
  - [ ] SubTask 2.5: 实现"浏览器直连"与"经本站代理"两种请求模式（CORS 兜底）
  - [ ] SubTask 2.6: 实现超时、AbortController、重试一次的错误处理

- [ ] Task 3: 实现 AI 助手状态机与历史管理（`src/lib/ai-assistant/`）
  - [ ] SubTask 3.1: 定义 `useAssistantStore`（抽屉开关、当前会话、消息列表、加载态、模型）
  - [ ] SubTask 3.2: 实现历史裁剪：保留系统提示 + 附加上下文 + 最近 N 轮
  - [ ] SubTask 3.3: 实现 `localStorage` 持久化与多会话切换（先支持单会话，后续可扩展）
  - [ ] SubTask 3.4: 实现 `open({ context })` API 供业务页面主动调用
  - [ ] SubTask 3.5: 实现"新建对话"清空历史但保留系统提示

- [ ] Task 4: 实现 AI 助手抽屉 UI（`src/components/ai-assistant/`）
  - [ ] SubTask 4.1: `Drawer` 容器：右侧滑出、宽度 360~420px、遮罩、Esc 关闭
  - [ ] SubTask 4.2: `Header`：标题、模型下拉、新建对话、关闭、设置入口
  - [ ] SubTask 4.3: `MessageList`：用户/助手气泡区分、Markdown 渲染、代码块高亮、自动滚动到底部
  - [ ] SubTask 4.4: `InputBar`：多行 textarea、Enter 发送、Shift+Enter 换行、字符计数、停止生成按钮
  - [ ] SubTask 4.5: `QuickActions`：空状态欢迎语 + 预置快捷指令气泡
  - [ ] SubTask 4.6: `ContextPicker`："+"按钮弹出的上下文选择面板
  - [ ] SubTask 4.7: `Disclaimer` 组件：每条助手消息末尾固定追加免责小字

- [ ] Task 5: 实现 AI 设置面板
  - [ ] SubTask 5.1: 路由或 Modal 形式接入"设置 → AI 助手"
  - [ ] SubTask 5.2: 表单字段：Base URL、API Key、模型、Temperature、N、超时、自定义系统提示词、请求模式
  - [ ] SubTask 5.3: 实现"显示/隐藏 Key"、"测试连接"按钮（调 `listModels`）
  - [ ] SubTask 5.4: 实现"快捷指令管理"子面板
  - [ ] SubTask 5.5: 保存时校验必填项，提示"密钥仅保存在本机浏览器"

- [ ] Task 6: 业务页面接入示范
  - [ ] SubTask 6.1: 行情页（个股页）接入"附加 K 线"按钮
  - [ ] SubTask 6.2: 策略编辑页接入"回测个股"按钮，自动注入当前策略代码
  - [ ] SubTask 6.3: 全局 `AppShell` 挂载抽屉入口与设置入口

- [ ] Task 7: 端到端验证
  - [ ] SubTask 7.1: 用 DeepSeek 真实 API 跑通"测试连接 → 发送消息 → 流式接收 → 历史上下文"
  - [ ] SubTask 7.2: 用本地 Ollama (`http://localhost:11434/v1`) 验证自建源可用
  - [ ] SubTask 7.3: 验证"未配置 API 时发送"拦截
  - [ ] SubTask 7.4: 验证刷新页面后配置与历史均保留
  - [ ] SubTask 7.5: 验证免责声明始终出现在每条助手消息末尾

# Task Dependencies

- Task 2 依赖 Task 1
- Task 3 依赖 Task 2
- Task 4 依赖 Task 3
- Task 5 依赖 Task 3
- Task 6 依赖 Task 4 + Task 5
- Task 7 依赖 Task 6
