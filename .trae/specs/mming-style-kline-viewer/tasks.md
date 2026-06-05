# Tasks — Mming 风格 K 线页（重写版：源码挂载 + Flask Blueprint）

## 总览

按顺序执行；⭐ 标里程碑。

- [ ] ⭐ **Task 1**：在 Codespace 里解压源码 + 准备开发环境
  - [ ] SubTask 1.1：把 `/workspace/QuantDinger-main.zip` 上传到 Codespace（拖到文件树或 `scp`）
  - [ ] SubTask 1.2：解压 `unzip QuantDinger-main.zip`，得到 `QuantDinger-main/` 目录
  - [ ] SubTask 1.3：建一个本地开发 compose 文件 `docker-compose.local-dev.yml`（基于 `docker-compose.ghcr.yml` 改）：
    - backend 服务用 `build: ./QuantDinger-main/backend_api_python`（不用现成镜像）
    - 加 volume 挂载：`./QuantDinger-main/backend_api_python:/app`（源码热更新）
    - 启动命令加 `--reload` 标志（gunicorn 自动重启）
  - [ ] SubTask 1.4：复制 `env.example` 到 `backend.env`，生成 `SECRET_KEY` 写进去

- [ ] **Task 2**：注册 Flask Blueprint
  - [ ] SubTask 2.1：读 `backend_api_python/app/routes/__init__.py`，理解现有的 blueprint 注册方式
  - [ ] SubTask 2.2：创建 `backend_api_python/app/routes/custom_kline.py`，定义：
    ```python
    from flask import Blueprint, send_from_directory, render_template_string
    import os
    custom_kline_bp = Blueprint('custom_kline', __name__, url_prefix='/custom-kline')
    STATIC_DIR = os.path.join(os.path.dirname(__file__), '..', 'static_custom')
    @custom_kline_bp.route('/')
    def index():
        # 读 kline.html 文件,插入 query 参数
        with open(os.path.join(STATIC_DIR, 'kline.html')) as f:
            return f.read()
    @custom_kline_bp.route('/static/<path:filename>')
    def static_file(filename):
        return send_from_directory(STATIC_DIR, filename)
    ```
  - [ ] SubTask 2.3：在 `routes/__init__.py` 加 `from app.routes.custom_kline import custom_kline_bp` + `app.register_blueprint(custom_kline_bp)`（或类似的注册方式，按现有模式）

- [ ] **Task 3**：写 HTML 页面（`static_custom/kline.html`）
  - [ ] SubTask 3.1：HTML 骨架 — `<head>` 含 ECharts 5.4.3 CDN + kline.css
  - [ ] SubTask 3.2：顶部工具栏 — 股票代码输入框、市场下拉（CNStock/USStock/Crypto）、周期按钮组（1分/5分/15分/30分/1时/4时/1日/1周）、"加载"按钮
  - [ ] SubTask 3.3：图表容器 `<div id="chart" style="height:700px">`、错误条 `<div id="errBox" class="hidden">`、重试按钮
  - [ ] SubTask 3.4：底部 `<script src="static/kline.js">` 引用 JS
  - [ ] SubTask 3.5：JS 启动时从 URL query 读 `market/symbol/tf/limit`，自动填到输入框，触发首次加载

- [ ] **Task 4**：写 CSS（`static_custom/kline.css`）
  - [ ] SubTask 4.1：CSS 变量（背景/网格/文字/涨绿/跌红/MA 颜色）
  - [ ] SubTask 4.2：暗色 body、工具栏样式、错误条样式
  - [ ] SubTask 4.3：响应式：iPad 横屏 4 panel 总高 600px，竖屏 700px

- [ ] **Task 5**：写 K 线渲染 JS（`static_custom/kline.js`）
  - [ ] SubTask 5.1：工具函数 — `calcMA(close, n)`、`calcMACD(close)`、`formatTime(ts)`、`formatBigNum(n)`（处理 1.9亿 这种）
  - [ ] SubTask 5.2：`buildOption(ohlc, volArr, macdData, netInflowArr, dates, market)` — 返回 ECharts option 对象
    - grid 数组 4 个：`[{top:30, height: '40%'}, {top:'50%', height:'15%'}, {top:'67%', height:'15%'}, {top:'84%', height:'12%'}]`
    - xAxis 4 个 + yAxis 4 个
    - series: candlestick + 3 MA + volume bar + 2 MA + macd bar + netflow bar
    - dataZoom: 内外各一个，`xAxisIndex: [0,1,2,3]`
    - tooltip: `trigger: 'axis'`, `axisPointer: { link: {xAxisIndex: 'all'} }`
    - `animation: false`
  - [ ] SubTask 5.3：tooltip formatter — 中文模板（开盘/收盘/最高/最低/涨跌幅/成交量/MA/DIF/DEA/MACD/主力净流入）
  - [ ] SubTask 5.4：`loadKline(market, symbol, tf, limit)` — fetch `/api/kline?market=...&symbol=...&timeframe=...&limit=...`，转数据格式，setOption，错误处理
  - [ ] SubTask 5.5：周期按钮事件 — 改 URL query + 重 loadKline
  - [ ] SubTask 5.6：主力净流入估算 — `volume × (close-open) / (high-low)`，特殊处理 `high==low`（设为 0）
  - [ ] SubTask 5.7：缩放联动 — 双击重置 zoom（`dispatchAction({type:'dataZoom', start:0, end:100})`）

- [ ] ⭐ **Task 6**：本地启动 + 验证
  - [ ] SubTask 6.1：`docker compose -f docker-compose.local-dev.yml up -d`
  - [ ] SubTask 6.2：等 30s，`curl -I http://localhost:5000/custom-kline/` → 200
  - [ ] SubTask 6.3：`curl -I http://localhost:5000/custom-kline/static/kline.js` → 200
  - [ ] SubTask 6.4：`curl -I http://localhost:5000/api/health` → 200（原 API 未受影响）
  - [ ] SubTask 6.5：`curl "http://localhost:5000/api/kline?market=CNStock&symbol=sh600519&timeframe=1D&limit=10"` → 返回 10 根 K 线
  - [ ] SubTask 6.6：浏览器开 iPad Safari 转发端口 5000，访问 `/custom-kline/?market=CNStock&symbol=sh600519&tf=1D&limit=180`
  - [ ] SubTask 6.7：目视检查 4 panel 完整、中文 tooltip、暗色配色、缩放联动
  - [ ] SubTask 6.8：点击 1周周期 → URL 改变 → 重渲染（不刷新）
  - [ ] SubTask 6.9：改 kline.html 一个字，浏览器刷新看是否立即生效（验证源码挂载）

- [ ] **Task 7**：健壮性测试
  - [ ] SubTask 7.1：访问 `?symbol=invalid` → 错误条显示
  - [ ] SubTask 7.2：访问 `?market=USStock&symbol=TSLA` → 美股正常（红涨绿跌）
  - [ ] SubTask 7.3：访问 `?tf=1m&limit=300` → 分钟线正常
  - [ ] SubTask 7.4：把后端停掉，刷新页面 → 错误条 + 重试按钮可用
  - [ ] SubTask 7.5：iPad Safari 横竖屏切换 → 4 panel 比例正常

## Task Dependencies

- Task 2 依赖 Task 1（要先有源码）
- Task 3, 4, 5 依赖 Task 2（blueprint 至少能返回空页面）
- Task 6 依赖 Task 3, 4, 5（页面 + JS + CSS 都得写完）
- Task 7 依赖 Task 6（基本功能通了再测边界）
