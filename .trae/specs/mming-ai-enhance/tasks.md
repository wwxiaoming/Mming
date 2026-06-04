# Tasks

- [x] Task 1: 文件夹分离
  - [x] SubTask 1.1: 创建 `/workspace/Mming量化/` 目录
  - [x] SubTask 1.2: 移动 21 个文件到新目录
  - [x] SubTask 1.3: 验证文件结构正确
  - [x] SubTask 1.4: 删除原目录 Mming 量化相关文件

- [x] Task 2: AI 依赖与配置
  - [x] SubTask 2.1: 创建 `Mming量化/requirements.txt`：openai / httpx / flask
  - [x] SubTask 2.2: 写 `Mming量化/config_manager.py`：load_config / save_config / 默认模板生成
  - [x] SubTask 2.3: 创建 `Mming量化/config.json` 模板（api_key="" 占位）
  - [x] SubTask 2.4: 3 个单元测试全过（自动生成 / 不覆盖 / load_config / is_configured）

- [x] Task 3: server.py 加 AI 代理
  - [x] SubTask 3.1: 重构 server.py 用 Flask 替代 SimpleHTTPRequestHandler
  - [x] SubTask 3.2: 实现 `/ai/chat` 端点（SSE 流式）
  - [x] SubTask 3.3: 实现 `/ai/test` 端点
  - [x] SubTask 3.4: 实现 `/ai/usage` 端点
  - [x] SubTask 3.5: 限流中间件（同 IP 1 分钟 10 次）
  - [x] SubTask 3.6: prompt token 截断（>8000 token 截断）
  - [x] SubTask 3.7: 危险词过滤（6+ 类注入 pattern）

- [x] Task 4-7: 改 index.html (策略市场/详情/AI助手/K线解读)
  - [x] 6 个 nav-tab 按钮（数据查询/资金图表/择时回测/策略市场/策略详情/AI助手）
  - [x] 6 个 section DOM
  - [x] STRATEGY_TEMPLATES 11 个策略常量
  - [x] renderMarket() / importStrategy() / showStrategyDetail() / renderDetailCharts()
  - [x] 14 列统计卡 + ECharts K线图 + 资金曲线对比图
  - [x] AI 助手聊天面板 + SSE 客户端 + 4 个快捷指令
  - [x] AI 模型下拉（5 选项 + 自定义）
  - [x] "应用到回测" 按钮
  - [x] K线 🤖 解读按钮 + 右侧抽屉 + 流式 3 段渲染
  - [x] 关闭逻辑（× / Esc / 遮罩）
  - [x] AI 配置侧栏 + 保存 + 测试
  - [x] AI 用量统计显示
  - [x] 全套 CSS（含策略市场卡片 / 详情卡 / AI 助手 / 抽屉）
  - [x] 集成 switchTab 覆盖原版（合并 6 个 tab + ECharts resize）
  - [x] _lastTableData hook（让 AI 抽屉能读到表格数据）

- [x] Task 8: 回归测试
  - [x] SubTask 8.1: 原 4 Tab 静态结构验证 ✓
  - [x] SubTask 8.2: 新 3 Tab 静态结构验证 ✓
  - [x] SubTask 8.3: K线 🤖 按钮位置 ✓
  - [x] SubTask 8.4: API 代理 + 5 个 AI 端点 HTTP 状态全部正确
  - [x] SubTask 8.5: 无 api_key 时返回 503 + 友好提示
  - [x] SubTask 8.6: 端到端冒烟（保存/读取/恢复 config.json）

- [x] Task 9: 文档
  - [x] SubTask 9.1: README.txt 加 AI 配置章节
  - [x] SubTask 9.2: CODESPACES.md 加 config.json + AI 端点说明
  - [x] SubTask 9.3: 启动横幅显示"AI 未配置"提示
