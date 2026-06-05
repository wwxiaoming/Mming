# Checklist — QuantDinger IDE K 线优化 v2

按以下检查点逐项验证，全部 ✅ 才算完成。

## Phase 1：环境

- [ ] Codespace 4-core / 16GB 启动
- [ ] `QuantDinger` 主仓库源码在 `./`
- [ ] `QuantDinger-Vue` 源码在 `./QuantDinger-Vue/`
- [ ] `QuantDinger-Vue/package.json` 含 klinecharts 依赖
- [ ] `backend_api_python/.env` 有 SECRET_KEY 且不是默认值
- [ ] `backend_api_python/.env` 有 `ENABLED_MARKETS=...CNStock...`
- [ ] 根目录 `.env` 有 `IMAGE_PREFIX=docker.m.daocloud.io/library/`
- [ ] `QuantDinger-Vue/Dockerfile` 加了 npmmirror registry

## Phase 2：Demo 验证

- [ ] `src/views/KDemo/index.vue` 文件存在
- [ ] `src/router/index.js` 含 `/k-demo` 路由
- [ ] IDE 主菜单里有 "K Demo" 菜单项
- [ ] `docker compose ... up -d --build` 成功（首次 build 5-10 分钟）
- [ ] 浏览器能登录到 QuantDinger
- [ ] "K Demo" 页能正常显示 4 个联动面板
- [ ] K 线配色：红涨绿跌
- [ ] tooltip 显示中文「时间/开盘/收盘/最高/最低/成交量/MA5/MA10/MA20/DIF/DEA/MACD/主力净流入」
- [ ] 截屏保存到 `screenshots/k-demo.png`

## Phase 3：IDE 主页面改造

- [ ] IDE 主页面加载时执行 `loadLocales('zh-CN')`
- [ ] 自定义 `tooltipOverride` 覆盖了 Open/High/Low/Close/Volume 字段
- [ ] 周期按钮文案：1分/5分/15分/30分/1时/4时/1日/1周
- [ ] `src/charts/indicators/netInflow.js` 文件存在
- [ ] `NET_INFLOW` 指标已注册到 KLineCharts 全局
- [ ] 主图：K线 + MA(5, 10, 20) 三条线
- [ ] 副图 1：VOL（成交量）
- [ ] 副图 2：MACD (12, 26, 9)
- [ ] 副图 3：NET_INFLOW（主力净流入）
- [ ] 4 个 pane 高度比 ≈ 50% : 16% : 16% : 18%
- [ ] 整体背景 `#0d1117`、网格 `#1f2937`、文字 `#d1d5db`
- [ ] K 线 `upColor: #ef4444, downColor: #10b981`（红涨绿跌）

## Phase 4：构建 & 部署

- [ ] `dev-rebuild.sh` 脚本存在且可执行
- [ ] `start-qd.sh` 脚本存在且可执行
- [ ] 第二次 build 耗时 < 5 分钟（增量）
- [ ] `docker ps` 显示 4 个容器都 Running
- [ ] `docker logs quantdinger-frontend` 无 ERROR
- [ ] Codespace 端口 8888 转发正常
- [ ] iPad Safari 能正常访问

## Phase 5：端到端验证

- [ ] IDE 页面能选 A 股「CNStock / sh600519」
- [ ] 5 秒内 K 线加载完成
- [ ] 鼠标悬停 K 线 tooltip 全中文
- [ ] 4 个 pane 鼠标十字线同步
- [ ] 切周期按钮响应 < 5s
- [ ] 缩放 / 拖动丝滑
- [ ] 主力净流入数字格式化正确（如 -1.9亿）
- [ ] MA5/MA10/MA20 数值与 K 线收盘价匹配
- [ ] 截屏 `screenshots/ide-after.png` 与 Mming 量化 jzhu-quant K 线视觉对齐

## 健壮性

- [ ] 选 A 股无数据时不崩（显示"暂无数据"）
- [ ] 网络断开时 IDE 页面有错误条
- [ ] 切到加密货币 / 美股时图表正常切换数据源
- [ ] 登录失效跳回登录页
- [ ] 30 分钟不操作 Codespace 不会 kill 容器（idle timeout 调 240min）

## 文件清单（完成后应有）

- [ ] `./QuantDinger-Vue/src/views/KDemo/index.vue`
- [ ] `./QuantDinger-Vue/src/views/IndicatorIDE/index.vue`（已改）
- [ ] `./QuantDinger-Vue/src/charts/indicators/netInflow.js`
- [ ] `./QuantDinger-Vue/src/router/index.js`（加了路由）
- [ ] `./QuantDinger-Vue/Dockerfile`（加了 npmmirror）
- [ ] `./dev-rebuild.sh`
- [ ] `./start-qd.sh`
- [ ] `./backend_api_python/.env`
- [ ] `./.env`（IMAGE_PREFIX）
- [ ] `./.trae/specs/mming-style-kline-viewer/spec.md`（已存在）
- [ ] `./.trae/specs/mming-style-kline-viewer/tasks.md`（已存在）
- [ ] `./.trae/specs/mming-style-kline-viewer/checklist.md`（本文件）
- [ ] `./.trae/specs/mming-style-kline-viewer/quantdinger-ide-files.md`（备忘）
- [ ] `./.trae/specs/mming-style-kline-viewer/screenshots/k-demo.png`
- [ ] `./.trae/specs/mming-style-kline-viewer/screenshots/ide-after.png`

## 回滚

- [ ] 每个 Phase 完成后 `git add -A && git commit -m "phase X 完成"` 做版本快照
- [ ] 改坏后能 `git reset --hard HEAD~1` 快速回滚
- [ ] IDE 主页面是"装饰性"改动，不影响后端 API
- [ ] 旧 QuantDinger 镜像标签 `ghcr.io/brokermr810/quantdinger-frontend:v3.0.20` 可在 docker-compose.yml 改 `FRONTEND_TAG` 一键回退官方版
