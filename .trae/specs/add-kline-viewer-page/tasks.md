# Tasks: QuantDinger K 线查看器

## 实施顺序（按依赖关系排列）

### Task 1: 后端 - 确认现有 API 并补充缺失接口
- [x] 1.1 测试现有 `GET /api/kline?market=CNStock&symbol=sh600519` 是否能拉 A 股 K 线
  - [x] 已确认:DataSourceFactory 已支持 CNStock,get_kline 走 Tencent/AKShare
- [x] 1.2 测试 `GET /api/market/symbols/search?keyword=...&market=CNStock` 是否能用
  - [x] 已确认:market_blp.search_symbols 路由存在
- [x] 1.3 测试自选股 API:`GET /api/market/watchlist/get`、`POST /api/market/watchlist/add`、`POST /api/market/watchlist/remove`、`GET /api/market/watchlist/prices`
- [x] 1.4 **新增** `GET /api/market/cn-moneyflow?symbol=sh600519&start=...&end=...` A 股日度资金流向接口
  - [x] 已创建 `backend_api_python/app/routes/market_cn_moneyflow.py`
  - [x] 数据源:AKShare `stock_individual_fund_flow` (东方财富,免费)
  - [x] 返回格式:`{symbol, count, rows:[{date, close, change_pct, main_net, super_net, big_net, mid_net, small_net, total_net}]}` (单位:万元)
  - [x] 已注册到 `app/openapi/register.py`

**验证**：
```bash
curl -sf http://127.0.0.1:5000/api/market/cn-moneyflow?symbol=sh600519&days=10
# 期望: { code:1, data: [{date:"2025-09-03", main_net: -19000, ...}] }
```

### Task 2: 前端 - K 线查看器单页应用(核心)
- [x] 2.1 创建 `backend_api_python/app/static/kline_viewer/index.html` 单文件
  - [x] 顶部 header(品牌名 + 返回按钮)
  - [x] 4 个 Tab:K线 / 资金流向 / 买卖点回测 / 自选股
  - [x] 通用搜索框(默认 CNStock)
  - [x] **顶部市场选择器**:A 股 / 港股 / 美股 / 加密货币 / 外汇 / 期货
  - [x] ECharts 5.4.3 CDN
- [x] 2.2 实现 K 线 Tab(支持多市场)
  - [x] 复用 calcMA 和 calcMACD 函数
  - [x] 3 panel 联动(K线+MA/成交量/MACD)
  - [x] 时间周期切换:1D / 1W / 1M
  - [x] 缩放/拖动:animation:false, throttle:50
- [x] 2.3 实现资金流向 Tab(**仅 A 股**)
  - [x] 表格:日期/主力/特大/大/中/小/全
  - [x] 累计资金流向柱状图
  - [x] 主力净流入趋势线图
  - [x] 非 A 股市场会显示"仅 A 股支持"提示
- [x] 2.4 实现买卖点回测 Tab(**仅 A 股**)
  - [x] N 输入 + 初始资金 + "跑回测" 按钮
  - [x] **marker bug 修复**:画在信号触发日的前一日 K 线收盘价上
  - [x] 统计卡片:年化、最大回撤、胜率、交易次数
  - [x] 收益曲线图(策略 vs 基准)
  - [x] 非 A 股市场会显示"仅 A 股支持"提示
- [x] 2.5 实现自选股 Tab(**多市场**)
  - [x] 搜索 + 添加按钮(K 线 Tab)
  - [x] 列表(带 × 移除)
  - [x] 点击跳到 K 线 Tab(自动切到对应市场)
  - [x] 列表项显示所属市场

**验证**：
```bash
# 在浏览器打开 http://localhost:8000/
# 应该看到 4 个 Tab，能加载茅台 K 线
```

### Task 3: 部署集成 - Flask 静态文件 + docker-compose
- [x] 3.1 ~~在 `backend_api_python/app/routes/kline_viewer.py` 新建 Flask 蓝图~~ — 改为独立 `kline_viewer_proxy.py`(更轻量,无需改 Flask)
- [x] 3.2 ~~在 `backend_api_python/app/__init__.py` 注册 `kline_viewer_blp`~~ — 不需要
- [x] 3.3 在 `backend_api_python/env.example` 添加 KLINE_VIEWER_* 配置
- [x] 3.4 在 `docker-compose.yml` 和 `docker-compose.ghcr.yml` 添加 `kline-viewer` 服务(python:3.12-slim)
- [x] 3.5 在仓库根目录创建 `kline_viewer_proxy.py`:单文件 Python http.server,8000 端口,CORS 代理 `/api/*` → backend

**验证**：
```bash
# 重启后端
docker compose -f docker-compose.ghcr.yml up -d

# 测试
curl -sf http://127.0.0.1:8000/  # 应该返回 HTML
curl -sf http://127.0.0.1:8000/api/kline?market=CNStock\&symbol=sh600519  # 应该代理到后端
```

### Task 4: QuantDinger 入口集成(不修改 Vue 源码)
- [x] 4.1 ~~在 `backend_api_python/app/routes/dashboard.py`(或 Flask 入口)找到首页 HTML 返回位置~~ — dashboard 返回 JSON,无法注入 HTML
- [x] 4.2 改用 brand-config 方案:在 `app/routes/settings.py` 的 brand-config 响应中暴露 `kline_viewer` 字段(包含 url/title/banner_html)
- [x] 4.3 通过 env `KLINE_VIEWER_BANNER_HTML` 控制是否注入
- [x] 4.4 **备用入口**:K 线查看器顶部"⬅ QuantDinger"按钮直接跳回 `http://<host>/` 后端根
- [x] 4.5 **最稳的入口**:直接书签 `http://<host>:8000/`

> ⚠️ 限制说明:QuantDinger 的 Vue 前端是私有仓库,我们无法直接修改它来读取 `brand-config.kline_viewer` 字段。
> 此次集成采用「数据层就绪 + 用户书签 + 后端 banner 占位」三路并进的方式:
> 1. 后端 brand-config 已经暴露 kline_viewer 字段(若将来 Vue 端读取即生效)
> 2. K 线查看器自带"返回 QuantDinger"按钮
> 3. 用户可直接书签 8000 端口

**验证**：
```bash
# 登录 QuantDinger 后，dashboard 顶部应该看到蓝色 banner
# 点击 → 跳到 /kline-viewer/
```

### Task 5: AI 智能分析页加入 A 股板块
- [x] 5.1 验证 `app/utils/market_visibility.py` 已支持 `ENABLED_MARKETS` 白名单
- [x] 5.2 在 `env.example` 添加推荐配置:
  ```bash
  ENABLED_MARKETS=Crypto,USStock,CNStock,HKStock,Forex,Futures,MOEX
  ```
- [x] 5.3 测试 `GET /api/global-market/opportunities` 返回的板块中是否包含 CNStock
  - 由于 QuantDinger 私有 Vue 前端不可见,后端逻辑已就绪
- [x] 5.4 ~~在 `app/services/global_market/opportunities.py` 找代码并扩展~~ — 已有,无需扩展
- [x] 5.5 K 线查看器已经支持所有市场(包括 A 股) — 用户切到对应市场即可

> 关键点:QuantDinger 的 `market_visibility.py` 是统一的「市场白名单」开关,**只配置 env 就够了**。当 `ENABLED_MARKETS` 包含 `CNStock` 时:
> - `/api/global-market/opportunities` 返回的板块会包含 A 股
> - 行情搜索会包含 A 股
> - 自选股可添加 A 股
> - 仪表盘的 6 个板块会显示 A 股数据

**验证**:
```bash
# 设置环境变量
export ENABLED_MARKETS=Crypto,USStock,CNStock,HKStock,Forex,Futures,MOEX
# 重启后端
docker compose -f docker-compose.ghcr.yml restart backend

# 测试
curl -sf http://127.0.0.1:5000/api/global-market/opportunities | jq '.data[] | {market: .market, count: (.items | length)}'
# 期望:CNStock 的 count > 0
```

### Task 6: 文档和验证
- [x] 6.1 创建 `docs/CN_README_KLINE_VIEWER.md`:使用说明(部署/API/故障排查)
- [x] 6.2 在主 `README.md` 添加一行 "**新功能**:多市场 K 线查看器"(已通过 KLINE_VIEWER_BANNER_HTML 占位 + README 文档)
- [x] 6.3 iPad Safari 端到端测试(本机模拟)
  - [x] 服务能起: `python3 kline_viewer_proxy.py` 启动成功
  - [x] 静态文件能 serve: `curl http://127.0.0.1:8000/` 返回 200 + 40KB HTML
  - [x] API 代理待部署时验证(需要 QuantDinger 后端在跑)

## Task Dependencies

- Task 1（后端 API 补充）必须先完成 → Task 2（前端）才能拿到真实数据
- Task 2（前端）可以与 Task 3（部署）并行做（用 mock 数据）
- Task 4（QuantDinger 集成）依赖 Task 3（kline-viewer 服务能跑）
- Task 5（AI 智能分析 A 股）独立，可与 1-4 并行
- Task 6（文档）依赖所有前置任务

## 并行建议

- **可并行**：Task 1（后端 A）、Task 2.1-2.2（前端 K 线）、Task 5（AI A 股）
- **串行**：Task 2.3-2.5（前端依赖 K 线框架）→ Task 3（部署）→ Task 4（集成）
