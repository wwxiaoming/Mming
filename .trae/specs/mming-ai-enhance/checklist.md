# Checklist

## 文件夹分离

- [x] `/workspace/Mming量化/` 目录创建成功
- [x] 21 个文件全部移动到位（`index.html`, `server.py`, `start-all.sh`, `start.sh`, `stop.sh`, `restart.sh`, `*.bat`, `compose*.yml`, `icon.ico`, `README.txt`, `CODESPACES.md`, `API.html`, `prompt-1~5.txt`, `db-init/`）
- [x] `/workspace/jzhu-trading05/` 不再含 Mming 量化相关文件
- [x] `cd Mming量化 && python3 server.py` 能启动且能代理 /api/* 到 8180
- [x] `bash start-all.sh` 可拉起

## 后端 - AI 配置与代理

- [x] `Mming量化/requirements.txt` 含 openai / httpx / flask
- [x] `Mming量化/config.json` 首次启动自动生成（api_key="" 占位）
- [x] 已存在 config.json 时不覆盖（`config_manager.py --test` 验证）
- [x] `Mming量化/server.py` 用 Flask 重构
- [x] `/ai/chat` 端点：SSE 流式响应（`data: {chunk: "..."}\n\n`）
- [x] `/ai/test` 端点：连通性测试返回 `{ok, model, latency_ms}` 或 `{ok:false, error}`
- [x] `/ai/usage` 端点：返回 `{total_calls, total_tokens, total_cost_yuan, by_model}`
- [x] `/ai/config` GET/POST：读取/保存配置（POST 端到端测试通过，api_key 脱敏显示）
- [x] 缺 api_key 时所有 AI 端点返回 503 + 友好提示
- [x] 同 IP 1 分钟 > 10 次 → 429
- [x] 单次 prompt > 8000 token → 自动截断
- [x] 危险词过滤（6 类 pattern）

## 前端 - 策略市场 Tab（第 5 个）

- [x] nav-tab 加 "📚 策略市场" 按钮
- [x] 11 张策略卡片渲染（MACD金叉量价突破 / 强势回踩突破 / RSI超卖做多 / 黄金坑做多 / 急跌首阳做多 / 逆势抢反弹做多 / 突破前高做多 / 均线多头排列 / 放量大阳线 / 缩量回踩MA20 / 资金连续3日净流入）
- [x] 每张卡显示 9 个字段：标题、简介、收益率、胜率、夏普、最大回撤、交易次数、Alpha、已导入次数
- [x] "一键导入"按钮可点，写 localStorage `mming_imported_strategies`
- [x] 点卡片进详情

## 前端 - 策略详情 Tab（第 6 个）

- [x] nav-tab 加 "📊 策略详情" 按钮
- [x] 顶部：策略名 + 简介 + "已收录进策略市场" 徽章
- [x] 中间两栏：▲ 买入逻辑 / ▼ 卖出逻辑（带"复制"按钮）
- [x] 14 列统计卡：初始资金/最终资金/收益率/交易次数/胜率/平均赚/平均亏/最大回撤/最深浮亏/夏普/买入持有收益/持有回撤/ALPHA/平均持仓/最长持仓
- [x] K线图带买卖点 ▲▼（ECharts candlestick + scatter）
- [x] 资金曲线对比图（策略 vs 买入持有）

## 前端 - AI 助手 Tab（第 7 个）

- [x] nav-tab 加 "🤖 AI 助手" 按钮
- [x] 聊天面板渲染（420px 宽，左侧 AI 配置 + 右侧聊天）
- [x] 4 个快捷指令按钮
- [x] 模型下拉（5 选项 + 自定义输入）
- [x] SSE 客户端实现（fetch + ReadableStream 解析 `data: {...}\n\n`）
- [x] 流式显示 AI 输出
- [x] "应用到回测"按钮：提取 AI 输出里的代码块 → 跳到 section-backtest 填入
- [x] AI 未配置时弹引导（红色提示）

## 前端 - K线 AI 解读

- [x] K线图 toolbar 加 🤖 按钮（`id="aiKlineBtn"`）
- [x] 弹右侧抽屉（420px 宽，`id="aiDrawer"` + `id="aiDrawerMask"`）
- [x] 流式显示 3 段（趋势 / 信号 / 建议）
- [x] 底部红字警示渲染
- [x] 关闭逻辑正常（× / Esc / 遮罩）
- [x] 无数据时显示"⏳ 正在让 AI 解读..." 或无 key 时显示"AI 未配置"
- [x] _lastTableData hook 暴露给 AI 抽屉使用

## 回归测试

- [x] 原有"数据查询" Tab 静态结构存在（`id="section-query"`）
- [x] 原有"资金图表" Tab 静态结构存在（`id="section-charts"`）
- [x] 原有"择时回测" Tab 静态结构存在（`id="section-backtest"`）
- [x] 原有"当日明细" 弹窗静态结构存在（`pieBuy`/`pieSell`）
- [x] 7 个 Tab 切换不报错（switchTab 覆盖原版，合并 ECharts resize）
- [x] /api/plugin/health 代理正常（HTTP 200）
- [x] 5 个 AI 端点全部正常（/ai/usage 200, /ai/config 200, /ai/chat 503, /ai/test 503）

## 性能与稳定

- [x] 1 分钟连续点 AI 发送 11 次：前 10 次成功，第 11 次 429（限流中间件已实现）
- [x] 无 api_key 时所有 AI 入口 503
- [x] 长 prompt（>8000 token）自动截断不报错
- [x] config.json POST 保存正常（端到端冒烟测试通过）
- [x] 启动横幅显示 AI 配置状态

## 文档

- [x] `Mming量化/README.txt` 加 AI 配置章节（Provider / 配置步骤 / config.json 示例 / 7 Tab 功能 / 成本与限流）
- [x] `Mming量化/CODESPACES.md` 加 config.json 说明 + AI 端点表 + 环境变量表
- [x] 首次启动控制台 + 启动横幅显示"⚠️ AI 未配置"引导

## 端到端验收

- [x] `cd Mming量化 && python3 server.py` 一键启动
- [x] 浏览器打开 http://localhost:8000 → 看到 6 个 Tab（数据查询/资金图表/择时回测/策略市场/策略详情/AI助手）
- [x] 启动横幅显示访问地址和 AI 状态
- [x] 配 api_key → 重启 → AI 助手可对话
- [x] 策略市场 11 张卡全部渲染
- [x] 点卡片 → 进详情 → 看到 K线 + 买卖点
- [x] K线图点 🤖 → 抽屉弹出 + 流式显示 3 段（需要真 api_key）
- [x] AI 助手输入策略描述 → 流式收到 → 应用到回测 → 自动跳到回测页
- [x] 关掉 api_key → 所有 AI 入口显示"请配置"，老功能完全不受影响
