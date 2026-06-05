# Tasks: QuantDinger K 线查看器 (多市场) — 重写版

## 实施顺序

### Task 1: 后端 - 确认现有 API + 新增 cn-moneyflow
- [x] 1.1 测试现有 `GET /api/kline?market=CNStock&symbol=sh600519&timeframe=1m|5m|15m|30m|1H|4H|1D|1W` 能拉数据
  - [x] 已确认:DataSourceFactory 已支持 CNStock,catch_quote/fetch_kline 调用 Tencent API
  - [x] 已确认:cn_stock.py 支持 1m/5m/15m/30m/1H/4H（短周期）+ 1D/1W/1M（长周期）
- [x] 1.2 测试 `GET /api/market/symbols/search?market=...&keyword=...` 能用
- [x] 1.3 测试 `GET /api/market/symbols/hot?market=...&limit=10` 能用
- [x] 1.4 测试自选股 API:watchlist/get、add、remove
- [x] 1.5 **新增** A 股日度资金流向 `GET /api/market/cn-moneyflow`
  - [x] 文件 `backend_api_python/app/routes/market_cn_moneyflow.py`（167 行）
  - [x] 数据源:AKShare `stock_individual_fund_flow`(东方财富,免费)
  - [x] 字段:date/close/change_pct/main_net/super_net/big_net/mid_net/small_net/total_net(单位:万元)
  - [x] 30 分钟缓存
  - [x] 已注册到 `app/openapi/register.py`

**验证**:
```bash
curl -sf http://127.0.0.1:5000/api/market/cn-moneyflow?symbol=sh600519\&days=10
```

### Task 2: 后端 - K 线查看器 Flask 蓝图
- [x] 2.1 创建 `backend_api_python/app/routes/kline_viewer.py`(71 行)
  - [x] 蓝图路由:`/kline-viewer/` 返回 `index.html`
  - [x] 静态文件路由:`/kline-viewer/<path>` 返回静态文件
  - [x] `KLINE_VIEWER_ENABLED=false` 时返回 404
  - [x] 路径安全检查(防止跳出 kline_viewer 目录)
- [x] 2.2 注册蓝图到 `app/openapi/register.py`
- [x] 2.3 brand-config 暴露 `kline_viewer` 字段
  - [x] enabled/url/title/banner_html
  - [x] supported_markets:6 个
  - [x] supported_timeframes:8 个

**验证**:
```bash
# 重启后端
docker compose -f docker-compose.ghcr.yml restart backend
curl -sf http://127.0.0.1:5000/kline-viewer/  # 应该返回 HTML
```

### Task 3: 前端 - K 线查看器单页应用 (1198 行)
- [x] 3.1 顶部品牌栏
  - [x] Logo + 标题
  - [x] 6 个市场 tab(默认 CNStock 选中)
  - [x] 搜索框 + 联想结果
  - [x] 返回 QuantDinger 按钮
- [x] 3.2 当前标的信息卡
  - [x] 名称 + 代码 + 市场
  - [x] 最新价 + 涨跌幅
  - [x] ⭐ 加自选按钮
- [x] 3.3 K 线图工具栏
  - [x] 8 个时间周期按钮(1m/5m/15m/30m/1H/4H/1D/1W)
  - [x] 主图指标下拉(MA/EMA/BOLL/无)
  - [x] 副图指标下拉(VOL+MACD/VOL+RSI/仅 MACD/仅 VOL)
  - [x] 全屏按钮 + 刷新按钮
- [x] 3.4 K 线图渲染
  - [x] 动态 1-3 个 panel
  - [x] 跨 panel dataZoom 联动
  - [x] 十字光标联动
  - [x] 丝滑缩放(throttle 50ms)
  - [x] 双击还原
- [x] 3.5 底部 4 个 Tab
  - [x] **图表与交易**:自选标的快速切换 + 图表设置开关
  - [x] **回测与结果**:N/初始资金/跑回测 + 统计卡 + 收益曲线
  - [x] **资金流向**(仅 A 股):表格 + 趋势线
  - [x] **自选股**:完整列表
- [x] 3.6 右侧栏
  - [x] 我的自选股(点击跳到 K 线)
  - [x] 热门标的(按当前市场自动筛选)

**验证**:
```bash
# 浏览器打开
http://<host>/kline-viewer/

# 应该看到:
# - 顶部 6 个市场 tab
# - 8 个时间周期按钮
# - 当前显示 "-- 请搜索标的 --"
# - 右侧"暂无自选"占位
# - 底部 4 个 Tab
```

### Task 4: AI 智能分析页加入 A 股板块
- [x] 4.1 验证 `app/utils/market_visibility.py` 已支持 `ENABLED_MARKETS` 白名单
- [x] 4.2 在 `env.example` 添加推荐配置:
  ```bash
  ENABLED_MARKETS=Crypto,USStock,CNStock,HKStock,Forex,Futures,MOEX
  SHOW_CN_STOCK=true
  ```

### Task 5: 部署验证
- [ ] 5.1 在 Codespace 重启 backend 容器
  ```bash
  docker compose -f docker-compose.ghcr.yml restart backend
  ```
- [ ] 5.2 测试 K 线查看器能访问
  ```bash
  curl -sf http://localhost:5000/kline-viewer/
  ```
- [ ] 5.3 测试 A 股资金流向 API
  ```bash
  curl -sf "http://localhost:5000/api/market/cn-moneyflow?symbol=sh600519&days=5"
  ```
- [ ] 5.4 在 iPad Safari 打开 K 线查看器
  - [ ] 顶部市场 tab 切换正常
  - [ ] 搜索 600519 / AAPL / BTCUSDT 都有结果
  - [ ] K 线加载成功
  - [ ] 8 个周期按钮都能切换
  - [ ] 主图/副图指标切换都重绘
  - [ ] 加自选 / 移自选 成功
  - [ ] 回测 Tab 能跑(仅 A 股)
  - [ ] 资金流向 Tab 显示数据(仅 A 股)

### Task 6: 清理旧文件
- [x] 6.1 删除旧的 `kline_viewer_proxy.py`(独立代理服务器)
- [x] 6.2 删除旧的 `kline-viewer` docker 服务(从 docker-compose.yml 移除)
- [x] 6.3 删除 `KLINE_VIEWER_PORT` / `KLINE_VIEWER_URL` / `KLINE_VIEWER_TITLE` 配置项

## Task Dependencies

- Task 1 必须先完成 → Task 2 才能注册蓝图
- Task 2 完成 → Task 3 才能被 Flask serve
- Task 4 独立,可与 1-3 并行
- Task 5 依赖所有前置任务(实际部署验证)
- Task 6 独立(清理工作)

## 与上一版的关键差异

| 项目 | 旧版(已删除) | 新版 |
|---|---|---|
| 部署方式 | 独立 `kline_viewer_proxy.py` + 单独 docker 服务(端口 8000) | Flask 蓝图同源挂载(无 CORS) |
| 访问路径 | `http://host:8000/`(独立端口) | `http://host/kline-viewer/`(同源) |
| 时间周期 | 3 个(1D/1W/1M) | **8 个**(1m/5m/15m/30m/1H/4H/1D/1W) |
| 主图指标 | 仅 MA | MA / EMA / BOLL / 无 |
| 副图指标 | 固定 VOL+MACD | VOL+MACD / VOL+RSI / 仅 MACD / 仅 VOL |
| 底部 Tab | K线/资金流/回测/自选(中文) | 图表与交易/回测与结果/资金流/自选(**与 QuantDinger 截图一致**) |
| 视觉风格 | 自定义深色 | **仿 QuantDinger** dashboard(蓝色 #2d7ff9) |
| 配置文件 | 需要 KLINE_VIEWER_* 3 个 | 只需 KLINE_VIEWER_ENABLED 1 个开关 |
| docker-compose | 新增 1 个服务 | **零修改** |
