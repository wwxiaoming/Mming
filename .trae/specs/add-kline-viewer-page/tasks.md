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
  - [x] ECharts 5.4.3 CDN
- [x] 2.2 实现 K 线 Tab
  - [x] 复用 calcMA 和 calcMACD 函数
  - [x] 3 panel 联动(K线+MA/成交量/MACD)
  - [x] 时间周期切换:1D / 1W / 1M
  - [x] 缩放/拖动:animation:false, throttle:50
- [x] 2.3 实现资金流向 Tab
  - [x] 表格:日期/主力/特大/大/中/小/全
  - [x] 累计资金流向柱状图
  - [x] 主力净流入趋势线图
- [x] 2.4 实现买卖点回测 Tab
  - [x] N 输入 + 初始资金 + "跑回测" 按钮
  - [x] **marker bug 修复**:画在信号触发日的前一日 K 线收盘价上
  - [x] 统计卡片:年化、最大回撤、胜率、交易次数
  - [x] 收益曲线图(策略 vs 基准)
- [x] 2.5 实现自选股 Tab
  - [x] 搜索 + 添加按钮(K 线 Tab)
  - [x] 列表(带 × 移除)
  - [x] 点击跳到 K 线 Tab

**验证**：
```bash
# 在浏览器打开 http://localhost:8000/
# 应该看到 4 个 Tab，能加载茅台 K 线
```

### Task 3: 部署集成 - Flask 静态文件 + docker-compose
- [ ] 3.1 在 `backend_api_python/app/routes/kline_viewer.py` 新建 Flask 蓝图，把 `/kline-viewer/` 路径 serve 静态文件
- [ ] 3.2 在 `backend_api_python/app/__init__.py` 注册 `kline_viewer_blp`
- [ ] 3.3 在 `backend_api_python/env.example` 添加：
  ```bash
  KLINE_VIEWER_ENABLED=true
  KLINE_VIEWER_PORT=8000
  KLINE_VIEWER_TITLE=量化系统 · A 股视图
  ```
- [ ] 3.4 在 `docker-compose.yml` 和 `docker-compose.ghcr.yml` 添加 `kline-viewer` 服务：
  ```yaml
  kline-viewer:
    image: python:3.12-slim
    container_name: quantdinger-kline-viewer
    restart: unless-stopped
    ports:
      - "8000:8000"
    volumes:
      - ./kline_viewer_proxy.py:/app/proxy.py:ro
      - ./backend_api_python/app/static/kline_viewer:/app/static:ro
    working_dir: /app
    command: ["python3", "proxy.py"]
    networks:
      - quantdinger-network
  ```
- [ ] 3.5 在仓库根目录创建 `kline_viewer_proxy.py`：单文件 Python http.server，8000 端口，CORS 代理 `/api/*` → `http://backend:5000`

**验证**：
```bash
# 重启后端
docker compose -f docker-compose.ghcr.yml up -d

# 测试
curl -sf http://127.0.0.1:8000/  # 应该返回 HTML
curl -sf http://127.0.0.1:8000/api/kline?market=CNStock\&symbol=sh600519  # 应该代理到后端
```

### Task 4: QuantDinger 入口集成（不修改 Vue 源码）
- [ ] 4.1 在 `backend_api_python/app/routes/dashboard.py`（或 Flask 入口）找到首页 HTML 返回位置
- [ ] 4.2 在返回的 HTML 中**字符串注入**一个 banner 链接（顶部）：
  ```html
  <div style="position:fixed;top:0;left:0;right:0;background:linear-gradient(90deg,#1e88e5,#7e57c2);color:#fff;padding:8px 16px;text-align:center;z-index:9999;font-family:sans-serif;">
    🆕 <b>量化系统 · A 股 K 线查看器</b> →
    <a href="/kline-viewer/" style="color:#ffeb3b;text-decoration:underline">立即打开</a>
  </div>
  ```
- [ ] 4.3 通过 env `KLINE_VIEWER_BANNER_HTML` 控制是否注入
- [ ] 4.4 同时在 README 添加使用说明

**验证**：
```bash
# 登录 QuantDinger 后，dashboard 顶部应该看到蓝色 banner
# 点击 → 跳到 /kline-viewer/
```

### Task 5: AI 智能分析页加入 A 股板块
- [ ] 5.1 验证 `app/utils/market_visibility.py` 已支持 `ENABLED_MARKETS` 白名单
- [ ] 5.2 在 `env.example` 添加推荐配置：
  ```bash
  ENABLED_MARKETS=Crypto,USStock,CNStock,HKStock,Forex,Futures,MOEX
  ```
- [ ] 5.3 测试 `GET /api/global-market/opportunities` 返回的板块中是否包含 CNStock
- [ ] 5.4 如果不包含：在 `app/services/global_market/opportunities.py` 找代码并扩展
- [ ] 5.5 在 dashboard 顶部 banner 旁边再加一个"打开 A 股板块"链接（指向 `/global-market/opportunities?market=CNStock`）

**验证**：
```bash
curl -sf http://127.0.0.1:5000/api/global-market/opportunities | jq '.data[] | {market: .market, count: (.items | length)}'
# 期望: CNStock 的 count > 0
```

### Task 6: 文档和验证
- [ ] 6.1 创建 `docs/CN_README_KLINE_VIEWER.md`：使用说明（截图占位）
- [ ] 6.2 在主 `README.md` 添加一行 "**新功能**：A 股 K 线查看器"
- [ ] 6.3 在 iPad Safari 跑通完整流程（K线 → 资金流 → 回测 → 自选股 → 跳回 QuantDinger）

## Task Dependencies

- Task 1（后端 API 补充）必须先完成 → Task 2（前端）才能拿到真实数据
- Task 2（前端）可以与 Task 3（部署）并行做（用 mock 数据）
- Task 4（QuantDinger 集成）依赖 Task 3（kline-viewer 服务能跑）
- Task 5（AI 智能分析 A 股）独立，可与 1-4 并行
- Task 6（文档）依赖所有前置任务

## 并行建议

- **可并行**：Task 1（后端 A）、Task 2.1-2.2（前端 K 线）、Task 5（AI A 股）
- **串行**：Task 2.3-2.5（前端依赖 K 线框架）→ Task 3（部署）→ Task 4（集成）
