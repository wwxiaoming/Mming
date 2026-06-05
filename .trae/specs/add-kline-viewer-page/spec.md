# QuantDinger K线查看器 (A 股) Spec

## Why

QuantDinger 默认前端是私有 Vue 仓库（`QuantDinger-Vue`），无法直接修改源码。但其 Flask 后端暴露了完整的 K 线/行情/自选股 REST API。我们要在不修改 Vue 源码的前提下，新增一个「K 线 + 资金流向 + 买卖点回测 + 自选股」综合页面，复用 jzhu-quant 中已经验证过的多 Panel K 线布局，挂在 QuantDinger 同一域名下，作为「量化系统 · A 股视图」入口。

## What Changes

- **新增文件**：
  - `backend_api_python/app/static/kline_viewer/index.html` — 单文件 SPA，4 个 Tab（K线 / 资金流向 / 买卖点回测 / 自选股）
  - `backend_api_python/app/routes/kline_viewer.py` — 把 `/kline-viewer/*` 静态路径交给 Flask
  - `kline_viewer_proxy.py` — 独立启动脚本（开发用，Codespaces 可直接 `python3 kline_viewer_proxy.py` 跑在 8000 端口，做 CORS 代理）
- **修改文件**：
  - `backend_api_python/app/__init__.py` — 注册 kline_viewer 蓝图
  - `backend_api_python/run.py` — 让 gunicorn 也能 serve 静态文件
  - `docker-compose.ghcr.yml` — 添加一个 `kline-viewer` 服务（8000 端口），挂载静态目录
  - `docker-compose.yml` — 同上
  - `backend_api_python/env.example` — 添加 K线查看器相关配置（`KLINE_VIEWER_ENABLED`、`KLINE_VIEWER_PORT`）

- **不修改** Vue 前端源码（不可访问）。集成通过以下 2 种方式实现：
  1. **同源挂载**：Flask 直接 serve `/kline-viewer/`，前端通过 nginx 反代访问 `http://<host>/kline-viewer/`
  2. **独立端口 + 链接跳转**：在 QuantDinger 登录页 dashboard 通过 `BRAND_*` env 注入一个 banner 链接（QuantDinger 已支持 brand-config 动态化）

- **核心功能**（参考 `/workspace/jzhu-quant/index.html` 实现）：
  - **Tab 1 - K线图**：4 Panel 联动 K线（K线+MA5/10/20 / 成交量 / MACD / 主力净流入），支持缩放/拖动/双击还原
  - **Tab 2 - 资金流向**：日度资金流向明细表格 + 饼图（特大单/大单/中单/小单 买入/卖出构成）
  - **Tab 3 - 买卖点回测**：基于「主力净流入 N 日均线 > 0 看多」规则回测，K线叠加买卖点 marker
  - **Tab 4 - 自选股**：股票搜索 + 添加/移除自选股 + 自选股列表 + 一键跳到 K线 Tab

- **数据源**（复用 QuantDinger 后端 API）：
  - K线：`GET /api/kline?market=CNStock&symbol=sh600519&timeframe=1D&limit=300`
  - 行情搜索：`GET /api/market/symbols/search?keyword=...&market=CNStock`
  - 热门股票：`GET /api/market/symbols/hot?market=CNStock&limit=20`
  - 自选股：`GET/POST /api/market/watchlist/{get|add|remove}`
  - 自选股价格：`GET /api/market/watchlist/prices`
  - 资金流向：通过 `/api/global-market/...` 或后端补充接口（如果后端没有直接的「A 股日度资金流」接口，需新增一个 `GET /api/market/cn-moneyflow?symbol=...`）

- **进入方式**（集成到 QuantDinger）：
  - **方式 A（推荐）**：在 QuantDinger dashboard 顶部加一个 banner 链接 "🆕 打开 A 股 K 线查看器"（用 `BRAND_LOGIN_BANNER_HTML` env 注入）
  - **方式 B**：在 AI 智能分析 / 自选股页面加外链（需要 Vue 源码，不可行 → 用方法 A 替代）
  - **方式 C**：登录后跳转默认页时附带一个弹窗（最小侵入）
  - **方式 D**：在 QuantDinger 左侧菜单底部加一行 "更多工具 · A 股 K 线"（同 A）

- **A 股特化**：
  - 默认显示沪深京 A 股（`market=CNStock`）
  - 在 AI 智能分析 / 及时分析的 6 个板块（涨跌幅榜、成交量榜、资金流入榜、热门股、AI 信号、组合监控）加入 CNStock 板块的开关（需在 `app/utils/market_visibility.py` 暴露 `SHOW_CN_*` 类目 env，本次不动它）
  - 股票代码格式：`sh600519` / `sz000001` / `bj833000`

## Impact

- **Affected specs**：无
- **Affected code**：
  - 新增 `backend_api_python/app/static/kline_viewer/`（静态文件目录）
  - 新增 `backend_api_python/app/routes/kline_viewer.py`（Flask 蓝图）
  - 新增 `backend_api_python/app/routes/market_cn_moneyflow.py`（A 股资金流向 API 适配，**如果后端没有**）
  - 新增 `kline_viewer_proxy.py`（开发用 CORS 代理）
  - 修改 `backend_api_python/app/__init__.py`（注册蓝图）
  - 修改 `backend_api_python/env.example`（添加配置项）
  - 修改 `docker-compose.ghcr.yml` 和 `docker-compose.yml`（添加 kline-viewer 服务）
  - 修改 `docs/CN_README.md`（添加使用说明）

- **环境依赖**：纯前端 ECharts 5.4.3（CDN）+ 后端 Flask（已有）。不引入新的 npm/pip 依赖。

## ADDED Requirements

### Requirement: A 股 K 线查看器主页

系统 SHALL 提供一个单文件 HTML 页面 `/kline-viewer/`，通过 Flask serve 静态文件提供访问。

#### Scenario: 通过同源访问
- **WHEN** 用户访问 `http://<quantdinger-host>/kline-viewer/`
- **THEN** 返回完整的 K 线查看器 SPA
- **AND** 所有 `/api/*` 请求同源发到 QuantDinger 后端（端口 5000），无 CORS 问题

#### Scenario: 通过独立端口访问
- **WHEN** 用户访问 `http://<quantdinger-host>:8000/`
- **THEN** 返回 K 线查看器（`kline_viewer_proxy.py` 模式，Codespaces 开发用）
- **AND** 内置 CORS 代理把 `/api/*` 转到 5000 端口

### Requirement: 4 Panel 联动 K 线图

系统 SHALL 提供一个 4 panel ECharts 联动图，包含：K线+MA5/10/20（panel 1）、成交量（panel 2）、MACD（panel 3）、主力净流入（panel 4）。

#### Scenario: 加载股票 K 线
- **WHEN** 用户在自选股/搜索框点击一只 A 股
- **THEN** 自动切到 K线 Tab
- **AND** 调用 `GET /api/kline?market=CNStock&symbol=sh600519&timeframe=1D&limit=300` 拉数据
- **AND** 渲染 4 panel 联动图，支持：丝滑缩放（throttle 50ms）、拖动、双击还原、自动同步十字光标

#### Scenario: 切换时间周期
- **WHEN** 用户点 1D / 1W / 1M 按钮
- **THEN** 重新请求对应 timeframe 数据并重绘图表
- **AND** 切换时显示 loading 状态

### Requirement: 资金流向 Tab

系统 SHALL 提供 A 股日度资金流向明细表格 + 饼图。

#### Scenario: 加载资金流向
- **WHEN** 用户在 K 线 Tab 点 "查看资金流向" 按钮
- **THEN** 切到资金流向 Tab
- **AND** 调用 `GET /api/market/cn-moneyflow?symbol=sh600519&start=...&end=...` 拉数据
- **AND** 显示表格（日期 / 主力 / 特大单 / 大单 / 中单 / 小单 / 全单）+ 买入/卖出饼图

> **注意**：QuantDinger 后端可能没有 A 股日度资金流向接口。需在本次实现中**新增**这个接口（调用 Tencent/AKShare），与 `app/data_sources/cn_stock.py` 集成。

### Requirement: 买卖点回测 Tab

系统 SHALL 提供基于「主力净流入 N 日均线 > 0 看多」规则的资金流择时回测，回测结果叠加在 K 线上。

#### Scenario: 跑回测
- **WHEN** 用户在买卖点回测 Tab 设置 N（默认 5）并点 "跑回测"
- **THEN** 计算 N 日主力均线，生成每日仓位（0/1）
- **AND** 计算策略收益曲线 vs 基准（持有不动）
- **AND** 在 K 线上画买卖点 marker（▲ 买在次日开盘前一日收盘，▼ 卖同理）
- **AND** 显示统计指标：年化、最大回撤、夏普、胜率

> **关键 bug 修复**：marker 必须画在「信号触发日的 K 线 i-1」上，价格 = `kmap[dates[i-1]].close`，**而非** `dates[i]` 的 k.low（参考 jzhu-quant 中已修复的版本）。

### Requirement: 自选股管理 Tab

系统 SHALL 提供自选股的增删查 + 一键跳到 K 线 Tab。

#### Scenario: 添加自选股
- **WHEN** 用户在搜索框输入"600519"或"茅台"并点 + 按钮
- **THEN** 调用 `POST /api/market/watchlist/add`（带 `market=CNStock&symbol=sh600519`）
- **AND** 列表立刻刷新
- **AND** 显示添加成功 toast

#### Scenario: 点击自选股跳到 K 线
- **WHEN** 用户点自选股列表的某一项
- **THEN** 自动切到 K 线 Tab 并加载该股票

#### Scenario: 移除自选股
- **WHEN** 用户点自选股列表某项的 × 按钮
- **THEN** 弹确认 → 调用 `POST /api/market/watchlist/remove` → 刷新列表

### Requirement: AI 智能分析页加入 A 股板块

系统 SHALL 在 AI 智能分析 / 及时分析页的 6 个板块中支持 A 股（CNStock）数据。

#### Scenario: 涨跌幅榜包含 A 股
- **WHEN** `ENABLED_MARKETS` 包含 `CNStock`
- **THEN** `/api/global-market/opportunities` 返回的板块包含 CNStock 的数据
- **AND** 前端 dashboard 渲染时显示 A 股板块

> **实现方式**：QuantDinger 的 `app/utils/market_visibility.py` 已经支持 `ENABLED_MARKETS` 白名单。**本次不修改后端**，仅在 `env.example` 中给出推荐配置 `ENABLED_MARKETS=Crypto,USStock,CNStock,HKStock,Forex,Futures,MOEX`。

### Requirement: 进入方式集成

系统 SHALL 在 QuantDinger dashboard 顶部提供一个 banner，链接到 K 线查看器。

#### Scenario: 通过 banner 进入
- **WHEN** 用户登录 QuantDinger 后看到 dashboard
- **THEN** 顶部显示一个蓝色 banner："🆕 打开 A 股 K 线查看器 →"
- **AND** 点击后在新标签页打开 `/kline-viewer/`

> **实现方式**：通过 QuantDinger 已有的 `BRAND_LOGIN_BANNER_HTML` 或类似的 brand-config 注入（如果后端没暴露这个字段，**新增**一个 `BRAND_TOP_BANNER_HTML` env，前端读 `/api/settings/brand-config` 显示）。本次为最小侵入，**直接在 QuantDinger 静态 nginx 容器挂载一个 `custom-banner.html`，通过前端 envsubst 注入 `<div>` 到 body 顶部**（需要在 frontend Dockerfile 调整 — 不可行）。

> **退而求其次**：本次**不修改** QuantDinger Vue 源码，而是：
> - 在 K 线查看器页面上提供"复制链接给 QuantDinger 用户"按钮，链接带 JWT 鉴权跳转
> - 在 QuantDinger 默认页（`http://<host>/`）的右侧**通过 nginx 反代**注入一个 iframe 或一个 `<meta http-equiv="refresh">` （不优雅，但零代码侵入）
> - **实用方案**：在 docker-compose 里把 K 线查看器服务（8000 端口）和 QuantDinger 前端（8888）都暴露，用户从 8888 顶部或 bookmark 跳到 8000

> **最终方案**（确认）：本次实现的 K 线查看器**独立运行**（Flask + 静态文件，端口 8000），通过**顶部 banner 跳转**集成到 QuantDinger dashboard。banner 实现：在 `backend_api_python/app/routes/dashboard.py`（如果存在）的首页响应中**追加 HTML 片段**（不修改 Vue 源码，仅修改后端返回的 index.html）。详细方案见 tasks.md。

## MODIFIED Requirements

### Requirement: QuantDinger docker-compose 增加 kline-viewer 服务

`docker-compose.yml` 和 `docker-compose.ghcr.yml` SHALL 增加一个 `kline-viewer` 服务。

#### Scenario: docker compose up 启动所有服务
- **WHEN** 用户运行 `docker compose -f docker-compose.ghcr.yml up -d`
- **THEN** 4 个原有服务（postgres/redis/backend/frontend）+ 1 个新增（kline-viewer）一起启动
- **AND** kline-viewer 在 8000 端口监听

### Requirement: backend.env 增加 K 线查看器配置

`backend_api_python/env.example` SHALL 增加以下配置项：
- `KLINE_VIEWER_ENABLED=true` — 开关
- `KLINE_VIEWER_PORT=8000` — 端口
- `KLINE_VIEWER_TITLE=量化系统 · A 股视图` — 页面标题

## REMOVED Requirements

无（本次为新增功能，不删除任何旧功能）。
