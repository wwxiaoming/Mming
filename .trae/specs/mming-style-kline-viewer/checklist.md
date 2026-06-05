# Checklist — QuantDinger IDE K 线优化 v3

按以下检查点逐项验证，全部 ✅ 才算完成。

## Phase 1：环境

- [ ] Codespace 4-core / 16GB 启动
- [ ] 仓库 `quantdinger-custom` 已创建
- [ ] `QuantDinger` 主仓库源码在 `./`
- [ ] `QuantDinger-Vue` 源码在 `./QuantDinger-Vue/`
- [ ] `QuantDinger-Vue/package.json` 含 klinecharts 依赖
- [ ] `QuantDinger-Vue/Dockerfile` 加了 npmmirror registry
- [ ] `backend_api_python/.env` 有合法 SECRET_KEY
- [ ] `backend_api_python/.env` 有 `ENABLED_MARKETS=...CNStock...`
- [ ] 根目录 `.env` 有 `IMAGE_PREFIX=...` 和 `TZ=Asia/Shanghai`
- [ ] Codespace idle timeout = 240min

## Phase 2：Demo 验证

- [ ] `quantdinger-ide-files.md` 备忘文件已写
- [ ] `src/views/KDemo/index.vue` 文件存在
- [ ] `src/router/index.js` 含 `/k-demo` 路由
- [ ] `docker compose ... up -d --build` 成功
- [ ] 浏览器能登录 QuantDinger
- [ ] "K Demo" 页能显示 4 个联动面板
- [ ] K 线亮色模式：绿涨红跌
- [ ] K 线暗色模式：红涨绿跌
- [ ] tooltip 全中文
- [ ] 截屏 `screenshots/k-demo-light.png` 和 `k-demo-dark.png`

## Phase 3：核心功能

### 自定义指标

- [ ] `src/charts/indicators/netInflow.js` 文件存在
- [ ] `NET_INFLOW` 指标已注册到 KLineCharts 全局
- [ ] 计算公式 `volume * (close - open) / (high - low)` 正确
- [ ] 0 除法时返回 0
- [ ] tooltip 数值格式化为 "X.X亿"

### 中文 i18n

- [ ] `src/charts/i18n/zh-CN.js` 文件存在
- [ ] `main.js` 调用 `loadLocales('zh-CN', customZhCN)`
- [ ] Open/High/Low/Close/Volume → 开盘/最高/最低/收盘/成交量
- [ ] 周期按钮：1分/5分/15分/30分/1时/4时/1日/1周

### 主题切换器

- [ ] `src/components/ThemeSwitcher.vue` 文件存在
- [ ] 右上角 Switch 按钮可见
- [ ] 默认主题是 Light（保持原观感，不强调背景色）
- [ ] 切换到暗色：背景 `#0d1117`、网格 `#1f2937`、K线 红涨绿跌
- [ ] 切换到亮色：恢复 Ant Design Vue 默认、K线 绿涨红跌
- [ ] 主题状态写入 `localStorage.theme`
- [ ] 刷新页面后主题保持
- [ ] 切到其它页面主题不变

### 全局股票搜索

- [ ] `src/components/StockSearchBox.vue` 文件存在
- [ ] `src/data/market-symbols.json` 含 CNStock 5000+ / USStock 10000+ / Crypto 500+ / HKStock 2500+ 条
- [ ] `fuse.js` 已安装
- [ ] IDE 页面顶部有「🔍 搜索股票」按钮
- [ ] 点击按钮弹出搜索 Modal
- [ ] 输入"600519"返回贵州茅台
- [ ] 输入"TSLA"返回 Tesla（美股）
- [ ] 输入"BTC"返回 BTC/USDT
- [ ] 输入"00700"返回腾讯控股（港股）
- [ ] **不是只搜自选股**（全市场）
- [ ] 键盘 `↓↑` 选，`Enter` 确认，`Esc` 关闭
- [ ] 全局 `Ctrl+K` / `Cmd+K` 快捷键唤起
- [ ] 选中后 IDE 页面切换股票图表

### IDE 主页面改造

- [ ] `IndicatorIDE/index.vue` 顶部加：股票选择器 + 搜索按钮 + 主题切换按钮
- [ ] KLineCharts 实例初始化（应用当前主题）
- [ ] 图表高度 = 700px
- [ ] 主图：K线 + MA(5, 10, 20)
- [ ] 副图 1：VOL
- [ ] 副图 2：MACD (12, 26, 9)
- [ ] 副图 3：NET_INFLOW
- [ ] 4 个 pane 联动（鼠标十字线同步）
- [ ] 监听 `StockSearchBox` 的 select 事件
- [ ] 监听主题变化重新 `setStyles()`

## Phase 4：构建 & 部署

- [ ] `dev-rebuild.sh` 脚本存在且可执行
- [ ] `start-qd.sh` 脚本存在且可执行
- [ ] 第二次 build 耗时 < 5 分钟
- [ ] `docker ps` 4 个容器都 Running
- [ ] `docker logs quantdinger-frontend` 无 ERROR
- [ ] Codespace 端口 8888 转发正常
- [ ] iPad Safari 能正常访问

## Phase 5：端到端验证

- [ ] IDE 页面能选 A 股「CNStock / 600519」
- [ ] 5 秒内 K 线加载
- [ ] 鼠标悬停 K 线 tooltip 全中文
- [ ] 4 个 pane 鼠标十字线同步
- [ ] 切周期按钮响应 < 5s
- [ ] 缩放 / 拖动丝滑
- [ ] 主题切换器点击后立即生效
- [ ] 默认 Light 主题看起来跟原版差不多（**不强调背景色**）
- [ ] 搜索按钮点击 → Modal 弹出
- [ ] 全局 `Ctrl+K` 唤起搜索
- [ ] 截屏 `screenshots/ide-light.png` `ide-dark.png` `search-result.png` `search-us.png`

## 健壮性

- [ ] 选 A 股无数据时不崩（"暂无数据"占位）
- [ ] 网络断开时 IDE 页面有错误条
- [ ] 切到加密货币 / 美股时图表正常切换
- [ ] 登录失效跳回登录页
- [ ] 30 分钟不操作 Codespace 不杀容器
- [ ] 搜索框输入空字符串不报错
- [ ] 搜索框输入特殊字符（"*" "." 等）不崩
- [ ] 主题切换不影响 tooltip 中文

## 文件清单（完成后应有）

### 新增
- [ ] `./QuantDinger-Vue/src/views/KDemo/index.vue`
- [ ] `./QuantDinger-Vue/src/charts/indicators/netInflow.js`
- [ ] `./QuantDinger-Vue/src/charts/i18n/zh-CN.js`
- [ ] `./QuantDinger-Vue/src/components/ThemeSwitcher.vue`
- [ ] `./QuantDinger-Vue/src/components/StockSearchBox.vue`
- [ ] `./QuantDinger-Vue/src/data/market-symbols.json`
- [ ] `./start-qd.sh`
- [ ] `./dev-rebuild.sh`
- [ ] `./REPLACE-GUIDE.md`

### 修改
- [ ] `./QuantDinger-Vue/Dockerfile`（npmmirror）
- [ ] `./QuantDinger-Vue/src/main.js`（loadLocales）
- [ ] `./QuantDinger-Vue/src/App.vue`（挂全局组件）
- [ ] `./QuantDinger-Vue/src/router/index.js`（路由）
- [ ] `./QuantDinger-Vue/src/views/IndicatorIDE/index.vue`（核心改造）
- [ ] `./backend_api_python/.env`（已存在）
- [ ] `./.env`（已存在）

### 文档
- [ ] `./.trae/specs/mming-style-kline-viewer/spec.md`（本文件）
- [ ] `./.trae/specs/mming-style-kline-viewer/tasks.md`
- [ ] `./.trae/specs/mming-style-kline-viewer/checklist.md`
- [ ] `./.trae/specs/mming-style-kline-viewer/quantdinger-ide-files.md`
- [ ] `./.trae/specs/mming-style-kline-viewer/screenshots/k-demo-light.png`
- [ ] `./.trae/specs/mming-style-kline-viewer/screenshots/k-demo-dark.png`
- [ ] `./.trae/specs/mming-style-kline-viewer/screenshots/ide-light.png`
- [ ] `./.trae/specs/mming-style-kline-viewer/screenshots/ide-dark.png`
- [ ] `./.trae/specs/mming-style-kline-viewer/screenshots/search-result.png`
- [ ] `./.trae/specs/mming-style-kline-viewer/screenshots/search-us.png`

## 回滚

- [ ] 每个 Phase 完成后 `git add -A && git commit -m "phase X 完成"`
- [ ] 改坏后 `git reset --hard HEAD~1` 快速回滚
- [ ] 改 `docker-compose.yml` 的 `FRONTEND_IMAGE` 改回 `ghcr.io/...` 标签可一键回退官方版
- [ ] `localStorage.theme` 改回 `light` 立即恢复亮色
