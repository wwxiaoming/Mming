# Tasks — Mming 风格 K 线查看器

## 总览

按顺序执行；标 ⭐ 的为里程碑。

- [ ] **Task 1**：抽出 Mming 量化 K 线渲染核心代码到独立模块
  - [ ] SubTask 1.1：从 `/workspace/jzhu-quant/index.html` 复制 `loadKlineChart()` 函数、MA / MACD 计算函数（`calcMA`、`calcMACD`）、tooltip 格式化函数到 `/workspace/jzhu-quant/qd-kline.js` 顶部
  - [ ] SubTask 1.2：把 `loadKlineChart()` 内的 `klineChart.setOption({...})` 完整 4 面板配置抽成函数 `renderKlinePanel(domEl, ohlc, volArr, macdData, netInflowArr, dates, opts)`，接收数据返回 chart 实例
  - [ ] SubTask 1.3：抽 tooltip 拼装为 `buildKlineTooltip(params, dates)`，输出中文

- [ ] **Task 2**：实现 `/workspace/jzhu-quant/qd-kline.html` 单页查看器
  - [ ] SubTask 2.1：HTML 骨架 — 顶部股票标题栏（代码 + 名称 + 周期切换 1D/1W/1m/5m 等）、`<div id="qdChart">` 容器（高 600px）、错误条 `<div id="errBox" class="hidden">`、重试按钮
  - [ ] SubTask 2.2：JS 入口 `init()` — 解析 URL query（market, symbol, tf, limit）→ fetch `/qd-api/kline?...` → 转成 `[date, o, c, l, h, v]` 格式 → 计算 MA/MACD/主力净流入 → 调 `renderKlinePanel()` → 启用 dataZoom 联动
  - [ ] SubTask 2.3：实现周期切换按钮 — 点击修改 URL 并 `init()` 重渲染
  - [ ] SubTask 2.4：错误处理 — `fetch` 失败 / 502 / 超时（>15s）时显示 errBox，按钮触发重试
  - [ ] SubTask 2.5：配色常量集中到 CSS 变量（`--bg: #0d1117; --red: #ef4444; --green: #10b981;`）便于暗色统一

- [ ] **Task 3**：扩展 `/workspace/jzhu-quant/server.py` 代理
  - [ ] SubTask 3.1：增加 `QD_API_BASE` 类属性（默认 `http://localhost:5000`），从环境变量 `QD_API_BASE` 读取
  - [ ] SubTask 3.2：在 `do_GET` 中增加分支：`if self.path.startswith("/qd-api/")` → 转发到 `QD_API_BASE + path.replace('/qd-api', '/api')`
  - [ ] SubTask 3.3：502 处理 — 后端连不上时返回 `{"error":"QuantDinger backend not reachable on port 5000"}` + 502 状态码
  - [ ] SubTask 3.4：保留原 `/api/*` 行为不变（jzhu-quant 8180 后端）

- [ ] **Task 4**：在 Mming 量化资金流向 tab 集成入口
  - [ ] SubTask 4.1：在 `index.html` 的 `#klineArea` 顶部"加载 K 线"按钮旁边加新按钮 `<button id="openMmingKlineBtn">🎨 Mming 风格 (QD数据)</button>`
  - [ ] SubTask 4.2：JS 中加监听 — 点击时 `window.open('qd-kline.html?market=CNStock&symbol=' + addPrefix($('stockCode').value) + '&tf=1D&limit=180', '_blank')`
  - [ ] SubTask 4.3：自动加前缀 — 输入 `600519` 自动补成 `sh600519`，输入 `000001` 补成 `sz000001`（6开头→sh，0/3开头→sz）
  - [ ] SubTask 4.4：在按钮旁加 tooltip：「用 QuantDinger 真实数据 + Mming 暗色 4 面板渲染」

- [ ] **Task 5**：本地验证（jzhu-quant 不依赖 QuantDinger 也能跑通）
  - [ ] SubTask 5.1：模拟 QD 响应 — 写一个 `/workspace/jzhu-quant/mock-qd-server.py` 用 `http.server` 监听 5000，收到 `/api/kline` 返回 60 根假 K 线（随机游走 + 趋势）
  - [ ] SubTask 5.2：浏览器打开 `qd-kline.html?market=CNStock&symbol=sh600519&tf=1D&limit=60`，目视检查：4 面板完整、中文 tooltip、配色暗色、缩放联动
  - [ ] SubTask 5.3：kill mock server 后刷新页面，验证错误条 + 重试按钮
  - [ ] SubTask 5.4：浏览器打开 `index.html`，资金流向 tab 查一只股票（如 600519），点击新按钮，验证新窗口打开 qd-kline.html 且 symbol 自动填好

- [ ] **Task 6**：QuantDinger 实数据联调（用户在 Codespace）
  - [ ] SubTask 6.1：在 `.env` 加 `QD_API_BASE=http://quantdinger-backend:5000`（docker 网络内）或 `http://localhost:5000`（宿主机跑）
  - [ ] SubTask 6.2：Codespace 端口转发 5000 后，`curl http://localhost:5000/api/kline?market=CNStock&symbol=sh600519&timeframe=1D&limit=10` 验证返回
  - [ ] SubTask 6.3：浏览器访问 qd-kline.html，确认拿到真 A 股数据，图表正常显示

## Task Dependencies

- Task 2 依赖 Task 1（要先抽出渲染函数）
- Task 3 独立（可与 Task 1/2 并行）
- Task 4 依赖 Task 2（按钮跳转的页面要先存在）
- Task 5 依赖 Task 1, 2, 3, 4（全部完成后才能端到端测）
- Task 6 依赖 Task 5（本地 mock 测通后再上真数据）
