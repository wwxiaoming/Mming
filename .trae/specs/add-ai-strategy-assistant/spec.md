# 小宇量化 · AI 策略助手 Spec

## Why

jzhu-trading（小宇量化）当前已有完整的 K线/指标/资金流/回测/策略编辑能力（Groovy 脚本策略、TimescaleDB 存储、Docker 一键部署），但**写策略的门槛卡在"懂 Groovy 语法"**、**解读行情的门槛卡在"看得懂 MACD/资金流背离"**。本次改造把这两件事交给大模型（DeepSeek / 兼容 OpenAI 协议）：用户用自然语言写策略，AI 出 Groovy 代码；K线+指标+资金流一键让 AI 解读。

## What Changes

- **新增 AI 配置页**：在系统设置里配置 AI Provider（DeepSeek / OpenAI / 自定义）、Base URL、API Key、模型名，存到 `system_config` 表（已有结构）
- **新增 AI 服务进程（Python FastAPI）**：端口 8282，3 个端点 `/ai/nl-to-strategy`、`/ai/analyze-kline`、`/ai/optimize-strategy`；流式响应（SSE）；后端数据由 Java 后端 8180 提供
- **改 Java 后端**：新增 `system_config` 增删改查接口（API key 加密入库）；新增 `/api/plugin/ai/*` 反向代理到 Python AI 服务（解决 SSE 流式跨域）；把"AI 解读"快捷按钮植入策略详情页与 K线详情页
- **改 web-app 前端**：
  - 策略编辑器右侧加 AI 聊天面板（输入自然语言 → 流式生成 Groovy → 一键填入编辑器 → 跑回测）
  - 策略详情页加 "AI 优化" 按钮（把回测结果 + 策略代码一起喂给 LLM，让它给出修改建议）
  - K线/资金流页面加 "AI 解读" 按钮（把最近 N 日 K线 + MA + MACD + 资金流喂给 LLM）
- **Mming量化（单文件 index.html）**：同步加 "AI 解读当前走势" 入口（共用 AI 服务）

## Impact

- Affected specs: 无
- Affected code:
  - 新增 `ai-service/`（Python FastAPI）
  - 改 `compose.yml` / `compose-lite.yml`：增加 `ai-service` 容器
  - 改 Java 后端（加 controller / 增改 system_config 端点 / SSE 代理）
  - 改 web-app（策略编辑器、策略详情、K线详情）
  - 改 `Mming量化/index.html`（加 AI 入口 + SSE 客户端）
  - 改 `db-init/04_init_system_config.sql`：预置 AI 配置默认值
  - 改 `README.txt` / `CODESPACES.md`：增加 AI 配置说明
- **BREAKING**：无。完全增量，老用户不配 AI Key 也能用原功能。

## ADDED Requirements

### Requirement: AI Provider 配置
系统 SHALL 在 `system_config` 表中支持以下 4 个键（用户可在设置页改）：
- `ai.provider`：默认 `deepseek`，可选 `openai` / `custom`
- `ai.base_url`：默认 `https://api.deepseek.com`
- `ai.api_key`：用户填入，前端展示时脱敏（`sk-***1234`）
- `ai.model`：默认 `deepseek-chat`

#### Scenario: 首次进入设置页
- **WHEN** 用户访问 `/settings/ai`
- **THEN** 页面读取 4 个配置项，api_key 字段脱敏显示，保存按钮启用

#### Scenario: 保存 AI 配置
- **WHEN** 用户填入 API Key 并点保存
- **THEN** 后端 AES-256 加密后写入 `system_config`，前端收到 `ok:true`

### Requirement: AI 服务（Python FastAPI 容器）
独立容器 `ai-service`（端口 8282）暴露 3 个端点，**必须流式响应**（SSE）：

#### Scenario: 自然语言转 Groovy 策略
- **WHEN** 前端 POST `/ai/nl-to-strategy` body=`{buy_text, sell_text, symbol?}`
- **THEN** 流式返回 `{chunk: "..."}` 形式的 Groovy 代码片段，前端拼接填入编辑器；最后一行返回 `{done: true, code: "完整代码"}`

#### Scenario: K线 AI 解读
- **WHEN** 前端 POST `/ai/analyze-kline` body=`{symbol, days: 60}`
- **THEN** 服务端**先调 8180** 拉 K线/MA/MACD/资金流，组织成结构化 prompt，发给 LLM；流式返回中文解读

#### Scenario: 策略 AI 优化
- **WHEN** 前端 POST `/ai/optimize-strategy` body=`{strategy_script, backtest_result}`
- **THEN** LLM 基于回测指标（胜率/夏普/最大回撤）给出 3 条可执行修改建议（参数调整 / 过滤条件 / 仓位管理），流式返回

### Requirement: Java 后端代理 SSE
Java 后端（8180）新增 `/api/plugin/ai/*` 路由，**原样转发**到 Python AI 服务 8282。**不读 body 不缓存**，必须支持 chunked streaming。

#### Scenario: 前端通过 Java 后端调用 AI
- **WHEN** 前端 `fetch('/api/plugin/ai/nl-to-strategy', ...)`
- **THEN** Java 收到后用 WebClient / HttpClient 流式转发到 8282，SSE 头完整透传

### Requirement: 策略编辑器 AI 助手
策略编辑页（`/strategy/edit/:id`）右侧浮动面板，宽度 380px，可折叠。

#### Scenario: 用户输入策略描述
- **WHEN** 用户在 AI 面板输入"5日均线上穿20日均线买入,跌破10日均线卖出" 点发送
- **THEN** 面板流式显示 AI 生成的 Groovy 代码，含 5 个快捷指令（一键帮我写 / 我有代码想回测 / 验证可行性 / 帮我优化 / 分析走势）

#### Scenario: 一键应用生成的代码
- **WHEN** AI 流式输出结束，底部"应用"按钮亮起
- **THEN** 点击后把 Groovy 代码填入主编辑器，点"跑回测"自动运行

#### Scenario: 校验 AI 理解
- **WHEN** 用户勾选"自动检查 AI 是否听懂"
- **THEN** AI 收到自然语言后先复述一遍（≤50 字），用户点"继续"才生成代码

### Requirement: K线 AI 解读按钮
策略详情页 + K线详情页 + Mming量化 主页 都加"🤖 AI 解读"按钮（位置：K线图右上角）。

#### Scenario: 点 AI 解读
- **WHEN** 用户点 K线右上角"AI 解读"
- **THEN** 弹出右侧抽屉（420px 宽），流式显示 3 段内容：①近 N 日趋势（涨/跌/震荡）②关键信号（MACD 背离/资金异动）③操作建议（仅供参考，加红字警示）

#### Scenario: AI 未配置
- **WHEN** 用户没配 API Key
- **THEN** 弹窗提示"请先在设置页配置 AI"，附跳转链接

### Requirement: 策略详情页 AI 优化
回测结果卡片下方加"AI 优化建议"折叠面板（默认折叠）。

#### Scenario: 点 AI 优化
- **WHEN** 用户点"AI 优化"
- **THEN** 喂给 LLM：策略代码 + 回测指标 + 最近一笔亏损交易；返回 3 条结构化建议（带 diff 片段）

### Requirement: Mming量化 AI 入口
单文件 `index.html`（8000 端口）底部 Tab 加"🤖 AI 解读"。

#### Scenario: 在 Mming 量化页调 AI
- **WHEN** 用户点 AI 解读 tab
- **THEN** 复用已查询的股票代码/日期，POST `/api/plugin/ai/analyze-kline`，流式显示

### Requirement: 沙箱与安全
LLM 生成的 Groovy 代码**必须**经过校验才能填入编辑器。

#### Scenario: 危险 API 调用拦截
- **WHEN** LLM 输出包含 `Runtime.exec` / `System.exit` / `new File` / `new URL` / `ProcessBuilder` / `Class.forName`
- **THEN** Java 后端拒绝保存（403），前端弹"AI 生成的代码包含危险调用"

#### Scenario: 代码长度限制
- **WHEN** LLM 输出 Groovy 代码 > 5000 字符
- **THEN** 截断并提示"代码过长，请简化"

### Requirement: 成本控制与限流

#### Scenario: 单用户限流
- **WHEN** 同一用户 1 分钟内调 AI 接口 > 10 次
- **THEN** 429 拒绝，提示"调用过快，60 秒后再试"

#### Scenario: Token 用量统计
- **WHEN** 每次 AI 调用结束
- **THEN** 写入 `ai_usage` 表（新增）记录：user_id、model、prompt_tokens、completion_tokens、cost_estimate、created_at

## MODIFIED Requirements

无（完全增量）。

## REMOVED Requirements

无。

## 部署 & 兼容性

- 镜像：`crpi-3glujemjfb279758.cn-shanghai.personal.cr.aliyuncs.com/jzhu-trading/ai-service:latest`
- 端口：8282（容器内 8282 → 主机 8282，可改）
- 内存：~200MB，比 Java app 轻
- **环境变量**：`AI_DEFAULT_BASE_URL` / `AI_DEFAULT_MODEL`（启动时灌入默认配置）
- 升级：用户跑 `restart.sh` / `restart.bat` 自动拉新镜像
- 兼容：Java 后端、Postgres、Mming量化、老 web-app 全部不动；不配 AI Key 完全等价于老版本
