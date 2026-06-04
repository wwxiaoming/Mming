# Mming量化 · AI 增强 + 文件夹分离 Spec

## Why

`jzhu-trading05` 项目里同时混着两套东西：
1. **小宇量化主项目**（Java + Docker，8180 + 18080）— 完整策略市场/AI 编辑器/回测系统
2. **Mming量化**（单文件 HTML + Python 代理，8000 端口）— 极简的资金流向 / K线 / 回测小工具

本次要做的：
- **A. 文件夹分离**：把 Mming量化 相关文件挪到独立的 `/workspace/Mming量化/` 目录，便于单独维护
- **B. AI 增强**：在 Mming量化的 `index.html` 里加 4 个 AI 能力（对应你给的 4 张截图）：
  1. 策略市场（带收益率/胜率/夏普的卡片墙）
  2. 策略详情（买入/卖出逻辑 + K线 + 买卖点）
  3. AI 策略编辑器（DeepSeek 模型选择 + 自然语言生成 Groovy/Python 策略）
  4. K线 AI 解读（流式显示趋势/信号/建议）

## What Changes

### 文件夹分离
- 新建 `/workspace/Mming量化/` 目录
- 从 `/workspace/jzhu-trading05/` 移入：`index.html` / `server.py` / `start-all.sh` / `compose-lite.yml` / `compose.yml` / `db-init/` / `start.sh` / `stop.sh` / `restart.sh` / `icon.ico` / `README.txt` / `CODESPACES.md` / `API.html` / `prompt-1~5.txt`
- `/workspace/jzhu-trading05/` 保留主项目文件不变

### Mming量化 AI 增强
- **`server.py` 加 AI 代理端点**：`/ai/chat` `/ai/test` `/ai/usage` 3 个端点，流式 SSE，调 DeepSeek/OpenAI 兼容 API
- **`config.json` 新增**：AI 配置（provider / base_url / api_key / model），首次启动自动生成模板
- **`index.html` 加 3 个新 Tab**：
  - `🤖 AI 助手`：聊天面板，4 个快捷指令（写策略 / 优化 / 验证 / 分析走势）+ 模型下拉
  - `📚 策略市场`：策略卡片墙（11+ 个内置策略，含收益率/胜率/夏普/最大回撤/Alpha/已导入次数）
  - `📊 策略详情`：点卡片进入，K线 + 买卖点 + 资金曲线 + 买入/卖出逻辑说明
- **`index.html` K线页加 🤖 解读按钮**：点击流式弹右侧抽屉

### Docker 镜像
- 不引入新容器，复用现有 8180 (Java app) 跑数据查询；AI 走 server.py 内置代理
- server.py 新增 `pip install openai httpx sse-starlette` 依赖（在 requirements.txt 里加）

## Impact

- Affected specs: 无
- Affected code:
  - 移动文件（15 个文件）到新目录
  - 改 `Mming量化/server.py`（+150 行：AI 代理 / 配置管理 / 限流）
  - 改 `Mming量化/index.html`（+800 行：3 个新 tab + AI 抽屉 + CSS）
  - 新增 `Mming量化/config.json`（AI 配置持久化）
  - 新增 `Mming量化/requirements.txt`（依赖）
- **BREAKING**：无。原有的 4 个 Tab（数据查询 / 资金图表 / 择时回测 / 明细弹窗）完全保留。

## ADDED Requirements

### Requirement: 文件夹分离
项目 SHALL 把 Mming量化 独立到 `/workspace/Mming量化/` 目录。

#### Scenario: 移动完成
- **WHEN** 执行移动脚本后
- **THEN** `/workspace/Mming量化/` 含全部 15 个文件，`/workspace/jzhu-trading05/` 不再有这些文件
- **AND** `server.py` 里的相对路径（`./db-init/` 等）仍可工作

### Requirement: AI 配置管理
`config.json` SHALL 存储 AI 配置，server.py 启动时加载，文件不存在则生成默认模板。

#### Scenario: 首次启动
- **WHEN** 第一次跑 `python3 server.py`
- **THEN** 自动生成 `config.json` 含默认值（`provider=deepseek`, `base_url=https://api.deepseek.com`, `model=deepseek-chat`, `api_key=""`）
- **AND** 控制台提示"⚠️ 请在 config.json 填入 api_key 后重启"

#### Scenario: 缺 api_key
- **WHEN** 任何 AI 接口被调用但 api_key 为空
- **THEN** 返回 `{ok:false, error:"AI 未配置,请编辑 config.json 后重启"}`，HTTP 503

### Requirement: AI 代理端点
server.py SHALL 暴露 3 个端点，**SSE 流式**：

#### Scenario: AI 对话
- **WHEN** 前端 `POST /ai/chat` body=`{model, messages: [{role, content}, ...]}`
- **THEN** 流式返回 `data: {"chunk": "..."}\n\n`，最后一行 `data: {"done": true, usage: {...}}`

#### Scenario: 测试连接
- **WHEN** 前端 `POST /ai/test` body=`{}`
- **THEN** 调一次 `chat.completions` 用最少 token 验证连通性，返回 `{ok, model, latency_ms}` 或 `{ok:false, error}`

#### Scenario: 用量统计
- **WHEN** 每次 AI 调用结束
- **THEN** 累加到内存计数器（重启清空），`GET /ai/usage` 返回 `{total_calls, total_tokens, total_cost_yuan, by_model: {...}}`

### Requirement: 限流与安全
- 同 IP 1 分钟 > 10 次 → 429
- 单次 prompt > 8000 token → 截断
- 危险词过滤（避免 LLM 注入 system prompt）

### Requirement: 策略市场 Tab
`index.html` 加第 5 个 Tab "📚 策略市场"，含 11 个内置策略卡片。

#### Scenario: 渲染卡片墙
- **WHEN** 用户切到"策略市场" Tab
- **THEN** 看到 11 张卡片（MACD金叉量价突破 / 强势回踩突破 / RSI超卖做多 / 黄金坑做多 / 急跌首阳做多 / 逆势抢反弹做多 / 突破前高做多 / 均线多头排列 / 放量大阳线 / 缩量回踩MA20 / 资金连续3日净流入）
- **AND** 每张卡显示：标题、简介、收益率、胜率、夏普、最大回撤、交易次数、Alpha、已导入次数、"一键导入"按钮

#### Scenario: 一键导入
- **WHEN** 用户点"一键导入"
- **THEN** 把策略代码（JSON 形式，含 buy/sell 逻辑）写入 localStorage 暂存，弹 Toast"已导入,请到 AI 助手中查看"
- **AND** localStorage key = `mming_imported_strategies`（list）

#### Scenario: 点卡片进详情
- **WHEN** 用户点卡片标题或封面
- **THEN** 切到"📊 策略详情" Tab，显示该策略的完整信息（买入/卖出逻辑、统计卡、K线、买卖点、资金曲线）

### Requirement: 策略详情 Tab
复用 K线 Tab 的 ECharts 实例（节省性能）。

#### Scenario: 渲染策略详情
- **WHEN** 导入某策略或点卡片
- **THEN** 顶部显示策略名 + 简介 + "已收录进策略市场" 徽章
- **AND** 中间两栏："▲ 买入逻辑" / "▼ 卖出逻辑"（用户可复制）
- **AND** 底部 14 列统计卡（初始资金/最终资金/收益率/交易次数/胜率/平均赚/平均亏/最大回撤/最深浮亏/夏普/买入持有收益/持有回撤/ALPHA/平均持仓/最长持仓）
- **AND** 最底部 K线图（带买卖点 ▲▼）+ 资金曲线对比图

### Requirement: AI 助手 Tab
`index.html` 加第 6 个 Tab "🤖 AI 助手"，右侧浮动聊天面板（沿用截图设计）。

#### Scenario: 渲染聊天面板
- **WHEN** 用户切到"AI 助手" Tab
- **THEN** 看到欢迎语 + 4 个快捷指令（我是新手帮我跑一个 / 我有策略代码想回测 / 我有想法想验证 / 帮我分析走势）+ 模型下拉 + 输入框

#### Scenario: 模型选择
- **WHEN** 用户点模型下拉
- **THEN** 看到 `deepseek-chat` / `deepseek-coder` / `gpt-4o-mini` / `gpt-4o` / 自定义（手动填入 model 名字）

#### Scenario: 输入自然语言生成策略
- **WHEN** 用户输入"5日均线上穿20日均线买入,RSI>70卖出" 点发送
- **THEN** 面板流式显示 AI 输出（左侧用户 / 右侧 AI）
- **AND** AI 输出包含 Groovy 风格的伪代码（用 `if (MA5 > MA20) buy; else if (RSI > 70) sell;` 这种格式）
- **AND** 底部"应用到回测"按钮亮起，点击后跳到"择时回测" Tab 并自动填入策略

#### Scenario: AI 配置缺失
- **WHEN** 用户点发送但 `config.json` 没配 api_key
- **THEN** 弹"AI 未配置" 提示 + 跳到"⚙️ 设置"（如果没设置 Tab 则在控制台提示）

### Requirement: K线 AI 解读按钮
现有 K线 Tab（数据查询里的 K线 子区）右上角加 🤖 按钮。

#### Scenario: 点 AI 解读
- **WHEN** 用户点 K线图右上角"🤖 AI 解读"
- **THEN** 弹右侧抽屉（420px 宽），流式显示 3 段：
  1. 近期趋势（涨/跌/震荡 + 关键转折点）
  2. 关键信号（MACD 背离、量价异动、均线交叉）
  3. 操作建议（仅供参考，加红字警示）
- **AND** 抽屉可关闭（× 或 Esc）

#### Scenario: 无数据时点
- **WHEN** 用户没查数据就点 🤖
- **THEN** 弹 Toast"请先查询数据"

### Requirement: 已有功能完整保留
原有的 4 个 Tab（数据查询 / 资金图表 / 择时回测 / 当日明细弹窗）代码 1:1 保留，只在 K线区加 🤖 按钮。

#### Scenario: 回归测试
- **WHEN** 完成所有 AI 功能后跑回归
- **THEN** 查 600519 数据 → 看资金图表 → 跑择时回测 → 点表格行看饼图 → 所有原功能与改造前一致

## MODIFIED Requirements

无（完全增量）。

## REMOVED Requirements

无。

## 数据来源

Mming量化是单文件工具，AI 需要的数据**走 8180 现有端点**（已确认存在）：
- `GET /api/plugin/kline?ts_code=...&start_date=...&end_date=...`
- `GET /api/plugin/moneyflow?ts_code=...&start_date=...&end_date=...`
- `GET /api/plugin/health`

server.py 加 AI 代理后，AI 后端要拿 K线时**通过 server.py 自己转发**到 8180（避免 CORS 和重复鉴权）。
