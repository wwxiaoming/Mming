# Mming 风格 K 线查看器 — Spec

## Why

QuantDinger 指标 IDE 页面的 K 线组件是闭源 Vue SPA（GHCR 镜像分发的 `QuantDinger-Vue` 仓库），无法直接修改源码。用户在 Codespace 里跑 QuantDinger 后发现：IDE 页面只有 K 线 + 成交量两栏、Light 主题、英文标签（Open/High/Low/Close/Volume），没有 4 联动面板（K线 / MA / 成交量 / MACD / 主力净流入），也没有"开盘/收盘/最高/最低"中文 tooltip，体感远不如已经调好的 `/workspace/jzhu-quant/index.html` 资金流向 tab 的 K 线图。需要让 QuantDinger 的指标能复用 Mming 量化的暗色 4 面板中文 K 线渲染。

## What Changes

- **新增** `/workspace/jzhu-quant/qd-kline.html`（独立单页，与现有 `index.html` 平级），从 URL query string 读取 `symbol` 和 `market`，调用 QuantDinger 后端的 `/api/kline` 拉 K 线，按 Mming 量化风格渲染暗色 4 联动面板
- **新增** `/workspace/jzhu-quant/qd-kline.js` 渲染模块，封装"取数据 → 算 MA / MACD / 主力净流入 → setOption"流程，可被 `index.html` 复用
- **修改** `/workspace/jzhu-quant/index.html` 资金流向 tab：在"加载 K 线"按钮旁加"用 QuantDinger 数据"开关，切到 QD 数据源时跳转到 `qd-kline.html?symbol=...&market=CNStock`
- **修改** `server.py` CORS 代理：把 `/qd-api/*` 也代理到 `localhost:5000`（QuantDinger 后端），新增 `QD_API_BASE` 配置项
- **修改** `start-all.sh`：在启动 jzhu-quant 之前询问"是否同时跑 QuantDinger"，如跑，则启动 jzhu-quant 容器（端口 5000）后代理到它

> 标记 `**BREAKING**` 的改动：无。所有改动均向后兼容，原 `index.html` 不动默认行为。

## Impact

- **Affected specs**：
  - `learn-sillytavern-character-cards` — 无影响
- **Affected code**：
  - `/workspace/jzhu-quant/index.html`（资金流向 tab 增加 1 个按钮 + 1 个 if 分支）
  - `/workspace/jzhu-quant/server.py`（新增 1 个路由前缀转发）
  - `/workspace/jzhu-quant/start-all.sh`（可选启 QuantDinger 容器）
- **Affected deployments**：
  - Codespace 端口表新增 5000 端口（QuantDinger 后端，转发到 jzhu-quant 代理时使用）
  - iPad Safari 浏览器：现有访问方式不变，新功能通过按钮进入

## ADDED Requirements

### Requirement: 独立 Mming 风格 K 线查看器

系统 SHALL 在 `/workspace/jzhu-quant/qd-kline.html` 提供单页 K 线查看器，URL 形如 `qd-kline.html?market=CNStock&symbol=sh600519&tf=1D&limit=300`，拉取 QuantDinger 后端 K 线数据后按 Mming 量化 4 面板风格渲染。

#### Scenario: A 股日 K 线正常渲染

- **WHEN** 用户访问 `qd-kline.html?market=CNStock&symbol=sh600519&tf=1D&limit=120`
- **THEN** 页面调用 `GET /qd-api/kline?market=CNStock&symbol=sh600519&timeframe=1D&limit=120` 拿到 120 根 K 线 OHLCV，渲染出：① 顶部 K线 + MA5/MA10/MA20 ② 成交量（红涨绿跌反转，色与 Mming 一致）③ MACD（DIF/DEA/柱）④ 主力净流入（基于成交量近似计算：净流入 ≈ volume × (close-open)/(high-low)）
- **AND** tooltip 显示「时间 / 开盘 / 收盘 / 最高 / 最低 / 成交量 / 涨跌幅 / MA5 / MA10 / MA20 / DIF / DEA / MACD / 主力净流入」，全部中文
- **AND** dataZoom 默认显示最近 60 根，4 个 panel 联动缩放
- **AND** 图表背景 `#0d1117`，主网格 `#1f2937`，文字 `#d1d5db`

#### Scenario: 美股 TSLA 周 K 线

- **WHEN** 用户访问 `qd-kline.html?market=USStock&symbol=TSLA&tf=1W&limit=200`
- **THEN** 同样渲染 4 面板，K 线配色红涨绿跌（美股惯例），tooltip 全中文

#### Scenario: 主力净流入字段缺失

- **WHEN** QuantDinger 返回的 K 线数据中无 `net_inflow` 字段
- **THEN** 系统用「(close-open)/(high-low) × volume」公式估算主力净流入，并在第 4 panel 标题后追加「(估算)」二字
- **AND** tooltip 中"主力净流入"行的值后加 "(估)"

#### Scenario: API 拉取失败

- **WHEN** 拉取 `/qd-api/kline` 返回非 200 或超时（>15s）
- **THEN** 页面显示红色错误条 "加载 K 线失败: <status> <msg>，请确认 QuantDinger 已启动 (端口 5000)"
- **AND** 保留一个「重试」按钮，点击重新拉取

### Requirement: 资金流向 tab 集成入口

`/workspace/jzhu-quant/index.html` 资金流向 tab SHALL 在 K 线区域顶部新增一个按钮「🎨 用 Mming 风格打开 (QuantDinger 数据)」，点击后在新窗口打开 `qd-kline.html?market=CNStock&symbol=<当前输入框代码>&tf=1D&limit=180`。

#### Scenario: 按钮存在且可点击

- **WHEN** 用户在资金流向 tab 加载完一次数据后
- **THEN** 上述按钮出现在"加载 K 线"按钮右侧
- **AND** 点击后用 `window.open()` 打开新 tab，URL 含当前代码（自动加 `sh`/`sz` 前缀）
- **AND** 当前 jzhu-quant 自带的 K 线图继续工作不受影响

### Requirement: CORS 代理扩展

`server.py` SHALL 增加 `/qd-api/*` 路径前缀转发到 `localhost:5000`（QuantDinger 后端），`QD_API_BASE` 通过环境变量可配置。

#### Scenario: 浏览器调用被代理

- **WHEN** 浏览器 fetch `/qd-api/kline?market=CNStock&symbol=sh600519`
- **THEN** server.py 转发到 `http://localhost:5000/api/kline?market=CNStock&symbol=sh600519`（注意补上 `/api` 段）
- **AND** 响应头加上 `Access-Control-Allow-Origin: *`

#### Scenario: QuantDinger 未启动

- **WHEN** `localhost:5000` 连接被拒
- **THEN** 代理返回 502 Bad Gateway + JSON `{"error":"QuantDinger backend not reachable on port 5000"}`
- **AND** 前端在 qd-kline.html 显示出对应错误信息

## MODIFIED Requirements

无（属于纯新增，不修改现有需求行为）。

## REMOVED Requirements

无。

## 实现关键点

1. **数据格式对齐**：QuantDinger `/api/kline` 返回 `{time, open, close, high, low, volume}`，与 Mming 量化 K 线预期的 `[date, open, close, low, high]` 数组基本兼容，只需做字段名映射
2. **指标复用**：MA / MACD 计算函数从 `index.html` 抽出放到 `qd-kline.js` 顶部，避免重复
3. **配色统一**：暗色 `#0d1117` 背景、`#ef4444` 红、`#10b981` 绿、MA 颜色 `#fbbf24/#60a5fa/#a78bfa`、网格 `#1f2937`，与 Mming 量化完全一致
4. **响应式布局**：iPad Safari 横向时 4 panel 总高度 600px，竖向时 700px
5. **可降级**：若 QuantDinger 未启动，qd-kline.html 给出明确提示，不崩溃
