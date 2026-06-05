# Mming 风格 K 线页 — Spec（重写版：直接改后端源码挂新页面）

## Why

QuantDinger 仓库（`QuantDinger-main.zip`）只有 Python 后端源码，**前端 Vue SPA 是闭源**（`QuantDinger-Vue` 私有仓库，编译后通过 GHCR 镜像分发）。所以"指标 IDE 页面"那个 K 线组件**没法直接改源码**。但是 Python 后端是 Flask，可以加新的 blueprint route，让同一个后端同时 serve 一份自定义 HTML 页面（用 ECharts 画 Mming 风格的 4 面板中文 K 线），数据继续走后端既有的 `/api/kline` 端点。这样就能在不改前端 SPA 的情况下，从浏览器访问 `http://<codespace>-5000.app.github.dev/custom-kline/?symbol=sh600519` 看到 Mming 风格图表。

## What Changes

- **修改** `/workspace/qd-analysis/QuantDinger-main/backend_api_python/app/routes/__init__.py`：注册新 blueprint `custom_kline_bp`
- **新增** `/workspace/qd-analysis/QuantDinger-main/backend_api_python/app/routes/custom_kline.py`：Flask blueprint，路由：
  - `GET /custom-kline/` → 返回静态 HTML 页面（带查询参数透传 `?market=&symbol=&tf=&limit=`）
  - `GET /custom-kline/static/<file>` → 返回 CSS / JS 静态文件
- **新增** `/workspace/qd-analysis/QuantDinger-main/backend_api_python/app/static_custom/kline.html`：主页面（含 ECharts 5.4.3 CDN）
- **新增** `/workspace/qd-analysis/QuantDinger-main/backend_api_python/app/static_custom/kline.js`：4 面板 K 线渲染逻辑
- **新增** `/workspace/qd-analysis/QuantDinger-main/backend_api_python/app/static_custom/kline.css`：暗色配色常量
- **修改** `/workspace/qd-analysis/QuantDinger-main/docker-compose.ghcr.yml`（或新建 `docker-compose.local-dev.yml`）：挂载整个 `backend_api_python` 源码到容器 `/app`，让代码改动**热生效**（Flask 调试模式 + volume mount）

> 标记 `**BREAKING**` 的改动：无。新增路由不影响 QuantDinger 原 SPA（前端 SPA 调用 `/api/*`，新页面调用 `/api/*` 同源，互不干扰）。

## Impact

- **Affected specs**：
  - `learn-sillytavern-character-cards` — 无影响
- **Affected code**：
  - `backend_api_python/app/routes/__init__.py`（+1 行 register）
  - `backend_api_python/app/routes/custom_kline.py`（新文件）
  - `backend_api_python/app/static_custom/`（新目录，4 个文件）
- **Affected deployments**：
  - **关键约束**：必须用源码挂载方式跑后端（不能直接用 GHCR 镜像），否则代码改了不生效
  - iPad Safari 浏览器：访问端口 5000（新页面），端口 8888（QuantDinger 原 SPA）继续可用

## ADDED Requirements

### Requirement: 自定义 K 线页 Blueprint

系统 SHALL 在 QuantDinger Python 后端注册名为 `custom_kline_bp` 的 Flask blueprint，提供：
- `GET /custom-kline/` 返回 HTML 主页面（带 market/symbol/tf/limit query 参数透传）
- `GET /custom-kline/static/<path>` 返回 `static_custom/` 目录下的 CSS/JS 文件
- blueprint 必须用 `url_prefix='/custom-kline'` 注册

#### Scenario: 启动后无 404

- **WHEN** 用户启动 Codespace 中的 QuantDinger 后端（端口 5000）
- **THEN** `curl -I http://localhost:5000/custom-kline/` 返回 200 + `text/html`
- **AND** `curl -I http://localhost:5000/custom-kline/static/kline.js` 返回 200 + `application/javascript`
- **AND** `curl http://localhost:5000/api/health` 仍然 200（原有路由未受影响）

#### Scenario: 查询参数透传

- **WHEN** 用户访问 `/custom-kline/?market=CNStock&symbol=sh600519&tf=1D&limit=180`
- **THEN** HTML 中有 `<input id="symbol" value="sh600519">`、`data-tf="1D"`、`data-limit="180"` 等预填字段
- **AND** JS 自动 fetch `/api/kline?market=CNStock&symbol=sh600519&timeframe=1D&limit=180` 加载数据

### Requirement: 暗色 4 面板 K 线渲染

`static_custom/kline.js` SHALL 用 ECharts 5.4.3 渲染 4 联动面板，**全部中文 tooltip**，与 `/workspace/jzhu-quant/index.html` 风格一致。

#### Scenario: A 股日 K 线正常渲染

- **WHEN** JS 拉取到 `/api/kline` 返回 120 根 OHLCV
- **THEN** 渲染出 4 个 panel（垂直堆叠）：
  1. **K 线 + MA**：candlestick + 3 条 MA 折线（MA5/MA10/MA20，颜色 `#fbbf24`/`#60a5fa`/`#a78bfa`）
  2. **成交量**：bar，红 `#ef4444` 涨、绿 `#10b981` 跌，叠加 MA5/MA10 折线
  3. **MACD**：DIF 蓝线 + DEA 黄线 + 柱状图（DIF-DEA）
  4. **主力净流入**：估算公式 `volume × (close-open)/(high-low)`，bar 颜色按正负染色
- **AND** 4 panel 共用 `dataZoom.xAxisIndex: [0,1,2,3]`，缩放联动
- **AND** 4 panel 共用 `axisPointer.link: {xAxisIndex: 'all'}`，鼠标十字线联动
- **AND** `animation: false`，缩放丝滑

#### Scenario: 中文 tooltip

- **WHEN** 鼠标悬停在任一 K 线上
- **THEN** tooltip 显示（按此顺序）：
  - 时间：2025-09-03
  - 开盘：11.744
  - 收盘：11.514
  - 最高：11.774
  - 最低：11.504
  - 涨跌幅：-1.96%
  - 成交量：1,367,232
  - MA 5:11.714 10:11.847 20:11.918
  - DIF:-0.110 DEA:-0.074 MACD:-0.073
  - 主力净流入:-1.9亿
- **AND** 全部中文，无 `Open/High/Low/Close/Volume` 英文

#### Scenario: 配色

- **WHEN** 页面加载
- **THEN** CSS 变量定义：
  ```css
  --bg:#0d1117; --grid:#1f2937; --text:#d1d5db;
  --red:#ef4444; --green:#10b981;
  --ma5:#fbbf24; --ma10:#60a5fa; --ma20:#a78bfa;
  --macd-dif:#60a5fa; --macd-dea:#fbbf24;
  ```
- **AND** ECharts 通过 `getOption` 后用 `setOption({...})` 注入这些颜色

#### Scenario: 周期切换

- **WHEN** 用户点击周期按钮（1分/5分/15分/30分/1时/4时/1日/1周）
- **THEN** URL query 中 `tf` 改变（用 `history.pushState`）
- **AND** JS 重新 fetch 对应 timeframe 的 K 线并重渲染图表（不刷新页面）

#### Scenario: API 拉取失败

- **WHEN** `fetch('/api/kline?...')` 返回非 200 或超时 15s
- **THEN** 红色错误条 `加载 K 线失败: <status>，请确认市场代码正确` 显示在图表上方
- **AND** 保留「重试」按钮，点击重新拉取

### Requirement: 源码挂载（开发模式）

部署 SHALL 使用源码 volume mount 方式跑后端容器，让代码改动**热生效**，不需要每次 `docker compose up --build`。

#### Scenario: 改 HTML 不需重建镜像

- **WHEN** 用户在 Codespace 编辑 `backend_api_python/app/static_custom/kline.html`
- **THEN** 浏览器刷新 `/custom-kline/` 立即看到改动（容器内 `/app/app/static_custom/kline.html` 同步更新）
- **AND** Python 后端进程通过 `--reload` 启动（gunicorn `--reload` 或 `flask run --debug`）

#### Scenario: 改 Python 代码自动重载

- **WHEN** 用户在 Codespace 编辑 `backend_api_python/app/routes/custom_kline.py`
- **THEN** gunicorn 检测到文件变化自动重启 worker（约 2-3 秒）
- **AND** 浏览器刷新后看到新行为

## MODIFIED Requirements

无。

## REMOVED Requirements

无。

## 实现关键点

1. **同源请求**：因为页面是从同一个 Flask 后端 serve 的（`/custom-kline/`），JS 调 `/api/kline` 是**同源**，无 CORS 问题，比之前的 `server.py` 代理方案简单 10 倍
2. **不改前端 SPA**：QuantDinger 自带的 Vue SPA 完全不变，我们只是在后端"加"了一个新页面
3. **不需要 Docker Hub 镜像**：直接 `python3 run.py` 跑 Flask debug 模式最快
4. **不需要 GHCR 镜像**：完全可以跳过 frontend 容器，只跑后端（用 Postgres 还是要的）
5. **iPad Safari 访问**：Codespace 端口转发 5000 → `xxx-5000.app.github.dev/custom-kline/`
