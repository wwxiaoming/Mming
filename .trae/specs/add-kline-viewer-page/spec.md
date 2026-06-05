# QuantDinger K 线查看器 (多市场) Spec — 重写版

## Why

QuantDinger 默认前端是私有 Vue 仓库（`QuantDinger-Vue`），无法直接修改源码。但其 Flask 后端暴露了完整的 K 线/行情/自选股 REST API，覆盖 CNStock/HKStock/USStock/Crypto/Forex/Futures 等多个市场，且 K 线数据源（Tencent/AKShare）已支持 8 个时间周期（1m/5m/15m/30m/1H/4H/1D/1W）。

我们要在不修改 Vue 源码的前提下，在 QuantDinger **后端内部**新增一个「多市场 K 线 + 资金流向 + 买卖点回测 + 自选股」综合页面：
- 通过 Flask 蓝图在 `/kline-viewer/` 路径 serve
- 复用 jzhu-quant 中已经验证过的多 Panel K 线布局
- 复用 QuantDinger 已有的 `/api/kline` 接口
- 不再单独跑 Python 代理服务器（Flask 自身 serve 静态文件即可）

## What Changes

- **新增文件**：
  - `backend_api_python/app/routes/kline_viewer.py` — Flask 蓝图（71 行），在 `/kline-viewer/` serve 静态 HTML
  - `backend_api_python/app/routes/market_cn_moneyflow.py` — A 股日度资金流向 API（167 行，AKShare 数据源）
  - `backend_api_python/app/static/kline_viewer/index.html` — 单文件 SPA（1198 行），4 个 Tab + 多市场
- **修改文件**：
  - `backend_api_python/app/openapi/register.py` — 注册 `kline_viewer_blp` + `moneyflow_blp`
  - `backend_api_python/app/routes/settings.py` — brand-config 响应中暴露 `kline_viewer` 字段
  - `backend_api_python/env.example` — 添加 `KLINE_VIEWER_ENABLED` / `KLINE_VIEWER_BANNER_HTML` / `ENABLED_MARKETS` / `SHOW_CN_STOCK`

- **多市场支持**（核心）：
  - 顶部 6 个市场 tab：🇨🇳 A 股 / 🇭🇰 港股 / 🇺🇸 美股 / ₿ 加密 / 💱 外汇 / 📊 期货
  - 默认 A 股（CNStock），可一键切换
  - 切换后：搜索、K 线、自选股全部基于新市场
  - 资金流向和买卖点回测**仅 A 股**支持（其他市场数据源不提供资金流明细）

- **8 个时间周期**（按 QuantDinger 截图 1:1 复刻）：
  - 1m / 5m / 15m / 30m / 1H / 4H / 1D / 1W
  - 默认选中 1D（与 QuantDinger dashboard 默认一致）
  - 1m / 5m 数据量大，limit 限制为 500；其他周期 300

- **核心功能**（参考 `/workspace/jzhu-quant/index.html` + QuantDinger 截图 2）：
  - **顶部品牌栏**：Logo / 市场 tab / 搜索 / 返回 QuantDinger
  - **当前标的信息卡**：名称 / 代码 / 最新价 / 涨跌幅 / 加自选
  - **K 线图区**：
    - 工具栏：周期 8 个按钮 + 主图指标下拉（MA/EMA/BOLL/无）+ 副图指标下拉（VOL+MACD/VOL+RSI/仅 MACD/仅 VOL）+ 全屏 + 刷新
    - K 线图：根据指标选择动态渲染 1-3 个 panel，支持缩放/拖动/双击还原/十字光标联动
  - **底部 4 个 Tab**（按 QuantDinger 截图 2 的 "图表与交易 / 回测与结果" 风格）：
    - **图表与交易**：自选标的快速切换 + 图表设置（显示成交量/MACD/十字光标联动开关）
    - **回测与结果**：N 周期 + 初始资金 + 跑回测 + 统计卡（年化/回撤/胜率/交易次数）+ 收益曲线
    - **资金流向**（仅 A 股）：表格 + 趋势线（5 日均线 + 主力净流入）
    - **自选股**：完整自选股列表
  - **右侧栏**：
    - 我的自选股（点击跳到 K 线）
    - 热门标的（按当前市场自动筛选）

- **数据源**（复用 QuantDinger 现有 API + 1 个新增）：
  - K线：`GET /api/kline?market=...&symbol=...&timeframe=1m|5m|15m|30m|1H|4H|1D|1W&limit=...`
  - 行情搜索：`GET /api/market/symbols/search?market=...&keyword=...`
  - 热门标的：`GET /api/market/symbols/hot?market=...&limit=10`
  - 实时价：`GET /api/market/price?market=...&symbol=...`
  - 自选股：`GET/POST /api/market/watchlist/{get|add|remove}`
  - **新增** A股资金流向：`GET /api/market/cn-moneyflow?symbol=sh600519&days=60`（AKShare 东方财富）

- **部署路径**（与旧版不同）：
  - **不再使用** `kline_viewer_proxy.py` 独立代理服务器
  - **不再使用** 单独的 `kline-viewer` docker 服务
  - 访问路径：`http://<quantdinger-host>/kline-viewer/`（同源，无 CORS 问题）
  - 由 Flask 蓝图直接 serve，nginx（quantdinger-frontend 容器）反代时自动透传

## Impact

- **Affected specs**：无（新增功能）
- **Affected code**：
  - 新增 3 个文件（kline_viewer.py、market_cn_moneyflow.py、index.html）
  - 修改 3 个文件（register.py、settings.py、env.example）
  - **不影响** docker-compose.yml / docker-compose.ghcr.yml（无需新服务）
  - **不影响** 现有 4 个服务（postgres/redis/backend/frontend）

- **环境依赖**：纯前端 ECharts 5.4.3（CDN）+ 后端 Flask + AKShare（若未安装需 `pip install akshare`）。不引入新的 docker 服务。

## ADDED Requirements

### Requirement: K 线查看器主页（同源挂载）

系统 SHALL 在 `/kline-viewer/` 路径提供 K 线查看器单页应用。

#### Scenario: 访问 K 线查看器
- **WHEN** 用户访问 `http://<quantdinger-host>/kline-viewer/`
- **THEN** 返回完整的 K 线查看器 SPA（1200 行 HTML）
- **AND** 所有 `/api/*` 请求同源发到 QuantDinger 后端（端口 5000），**无 CORS 问题**
- **AND** nginx 反代自动透传到 Flask 蓝图

#### Scenario: 禁用开关
- **WHEN** `KLINE_VIEWER_ENABLED=false`
- **THEN** 访问 `/kline-viewer/` 返回 404 + JSON 提示

### Requirement: 8 个时间周期

系统 SHALL 支持 8 个时间周期：1m / 5m / 15m / 30m / 1H / 4H / 1D / 1W（与 QuantDinger dashboard 默认顺序一致）。

#### Scenario: 切换到 1m 周期
- **WHEN** 用户点 1m 按钮
- **THEN** 重新请求 `GET /api/kline?timeframe=1m&limit=500` 拉取 1 分钟 K 线
- **AND** K 线图重绘
- **AND** 显示加载提示

#### Scenario: 切换到 1D 周期
- **WHEN** 用户点 1D 按钮（默认选中）
- **THEN** 重新请求 `GET /api/kline?timeframe=1D&limit=300` 拉取日 K 线
- **AND** K 线图重绘

### Requirement: 多市场切换

系统 SHALL 支持 6 个市场：CNStock / HKStock / USStock / Crypto / Forex / Futures。

#### Scenario: 切换到美股
- **WHEN** 用户点 "🇺🇸 美股" tab
- **THEN** 搜索结果基于 USStock 市场
- **AND** 热门标的列表基于 USStock
- **AND** 当前选中的标的清空，等待新搜索

#### Scenario: 资金流向/回测仅 A 股
- **WHEN** 当前市场不是 CNStock
- **THEN** "资金流向" 和 "回测与结果" Tab 显示"仅 A 股支持"提示
- **AND** 但 K 线 Tab 仍可正常拉数据

### Requirement: 4 个底部 Tab

#### Scenario: 图表与交易 Tab
- **WHEN** 用户点 "图表与交易" Tab
- **THEN** 显示自选标的快速下拉 + 图表设置（显示成交量/显示 MACD/十字光标联动 开关）

#### Scenario: 回测与结果 Tab
- **WHEN** 用户设置 N=5、初始资金 100000、点 "跑回测"
- **THEN** 计算 N 日主力均线，生成每日仓位（0/1）
- **AND** 计算策略收益曲线 vs 基准（持有不动）
- **AND** 显示统计：年化、最大回撤、胜率、交易次数
- **AND** **修复 marker bug**：买点画在信号触发日的前一日 K 线收盘价上

#### Scenario: 资金流向 Tab（仅 A 股）
- **WHEN** 用户点 "资金流向" Tab
- **THEN** 调用 `GET /api/market/cn-moneyflow` 拉数据
- **AND** 显示表格（日期 / 主力 / 特大 / 大 / 中 / 小 / 全）+ 趋势线

#### Scenario: 自选股 Tab
- **WHEN** 用户点 "自选股" Tab
- **THEN** 列出所有自选股（多市场）
- **AND** 点击跳到 K 线 Tab（自动切到对应市场）

### Requirement: 自选股管理

系统 SHALL 提供自选股的增删查 + 一键跳到 K 线 Tab。

#### Scenario: 添加自选
- **WHEN** 用户点 K 线区 "⭐ 加自选" 按钮
- **THEN** 调用 `POST /api/market/watchlist/add`（带 `market` + `symbol` + `name`）
- **AND** 右侧 "我的自选股" 列表立刻刷新

#### Scenario: 移除自选
- **WHEN** 用户点自选股项的 × 按钮
- **THEN** 弹确认 → 调用 `POST /api/market/watchlist/remove` → 刷新列表

### Requirement: AI 智能分析页加入 A 股板块

系统 SHALL 在 AI 智能分析 / 及时分析页的 6 个板块中支持 A 股（CNStock）数据。

#### Scenario: 涨跌幅榜包含 A 股
- **WHEN** `ENABLED_MARKETS` 包含 `CNStock`
- **THEN** `/api/global-market/opportunities` 返回的板块包含 CNStock 的数据
- **AND** 前端 dashboard 渲染时显示 A 股板块

> **实现方式**：QuantDinger 的 `app/utils/market_visibility.py` 已经支持 `ENABLED_MARKETS` 白名单。**本次不修改后端**，仅在 `env.example` 中给出推荐配置 `ENABLED_MARKETS=Crypto,USStock,CNStock,HKStock,Forex,Futures,MOEX`。

## MODIFIED Requirements

### Requirement: backend.env 增加 K 线查看器配置

`backend_api_python/env.example` SHALL 增加以下配置项：
- `KLINE_VIEWER_ENABLED=true` — 开关（默认启用）
- `KLINE_VIEWER_BANNER_HTML=` — 自定义 dashboard banner（可空）

> 已删除：旧版 `KLINE_VIEWER_PORT` / `KLINE_VIEWER_URL` / `KLINE_VIEWER_TITLE`（不再需要独立端口/URL，由 Flask 同源挂载）。

## REMOVED Requirements

无（本次为新增功能，不删除任何旧功能）。
