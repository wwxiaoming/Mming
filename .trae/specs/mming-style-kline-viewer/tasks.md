# Tasks — QuantDinger IDE K 线优化 v3

按顺序执行；标 ⭐ 的为关键里程碑。

## Phase 1：环境准备（Codespace 30 分钟）

- [ ] **Task 1：Codespace 仓库准备**
  - [ ] SubTask 1.1：在 GitHub 新建空仓库 `quantdinger-custom`
  - [ ] SubTask 1.2：开启 Codespace（4-core / 16GB）
  - [ ] SubTask 1.3：终端执行 `git clone https://github.com/brokermr810/QuantDinger.git .`
  - [ ] SubTask 1.4：执行 `git clone https://github.com/brokermr810/QuantDinger-Vue.git`
  - [ ] SubTask 1.5：在 `QuantDinger-Vue/Dockerfile` 顶部加 `RUN npm config set registry https://registry.npmmirror.com`
  - [ ] SubTask 1.6：Codespace 设置 idle timeout = 240 分钟

- [ ] **Task 2：后端配置**
  - [ ] SubTask 2.1：`cp backend_api_python/env.example backend_api_python/.env`
  - [ ] SubTask 2.2：生成 SECRET_KEY 并写入 `backend_api_python/.env`
  - [ ] SubTask 2.3：`backend_api_python/.env` 设 `ENABLED_MARKETS=Crypto,USStock,CNStock,HKStock,Forex,Futures,MOEX`
  - [ ] SubTask 2.4：根目录 `.env` 加 `IMAGE_PREFIX=docker.m.daocloud.io/library/` 和 `TZ=Asia/Shanghai`

## Phase 2：探索 + Demo（1 小时）⭐

- [ ] **Task 3：摸清 IDE 页面结构**
  - [ ] SubTask 3.1：`cd QuantDinger-Vue && cat package.json` 确认 klinecharts / vue / ant-design-vue 版本
  - [ ] SubTask 3.2：`find src/views -iname "*ide*"` 找 IDE 页面路径
  - [ ] SubTask 3.3：`grep -rl "klinecharts" src/` 列所有用 KLineCharts 的文件
  - [ ] SubTask 3.4：阅读 IDE 主页面的 `<template>` + `<script>`，识别图表初始化 / 主题 / 周期切换代码位置
  - [ ] SubTask 3.5：把关键文件路径写到 `quantdinger-ide-files.md`

- [ ] **Task 4：本地最小 demo 验证**
  - [ ] SubTask 4.1：建 `src/views/KDemo/index.vue` 测试页
  - [ ] SubTask 4.2：路由加 `/k-demo`
  - [ ] SubTask 4.3：写 4 pane KLineCharts（K线+MA / VOL / MACD / NET_INFLOW）用 mock 数据
  - [ ] SubTask 4.4：`docker compose -f docker-compose.yml -f docker-compose.build.yml up -d --build`（⭐ 首次 build）
  - [ ] SubTask 4.5：浏览器登录 → "K Demo" → 验证 4 pane + 中文 tooltip + 主题切换正常
  - [ ] SubTask 4.6：截屏 `screenshots/k-demo-light.png` 和 `k-demo-dark.png`

## Phase 3：实现核心功能（2 小时）⭐

- [ ] **Task 5：实现 `netInflow.js` 自定义指标**
  - [ ] SubTask 5.1：建 `src/charts/indicators/netInflow.js`
  - [ ] SubTask 5.2：`registerIndicator('NET_INFLOW', { calc, figures, ... })`
  - [ ] SubTask 5.3：`calc` 函数：`(volume * (close - open)) / (high - low)`，0 除法返回 0
  - [ ] SubTask 5.4：figures 配柱子（type: 'bar'），baseValue: 0
  - [ ] SubTask 5.5：tooltip 数值格式化为 "X.X亿"（除以 1e8 + toFixed(1)）

- [ ] **Task 6：实现 `zh-CN.js` 中文文案**
  - [ ] SubTask 6.1：建 `src/charts/i18n/zh-CN.js`
  - [ ] SubTask 6.2：覆盖 Open/High/Low/Close/Volume → 开盘/最高/最低/收盘/成交量
  - [ ] SubTask 6.3：覆盖 1m/5m/15m/30m/1H/4H/1D/1W → 1分/5分/15分/30分/1时/4时/1日/1周
  - [ ] SubTask 6.4：在 `main.js` 调用 `loadLocales('zh-CN', customZhCN)`

- [ ] **Task 7：实现 `ThemeSwitcher.vue`**
  - [ ] SubTask 7.1：建 `src/components/ThemeSwitcher.vue`（右上角 Switch 组件）
  - [ ] SubTask 7.2：用 Vuex / Pinia 存全局 `theme` 状态
  - [ ] SubTask 7.3：切换时调 3 个 API：
    - 全局 CSS 变量：`document.documentElement.style.setProperty('--bg', ...)`
    - Ant Design Vue：`ConfigProvider` 主题切换
    - KLineCharts 实例：`chart.setStyles({...})`
  - [ ] SubTask 7.4：写入 `localStorage.theme`，`created()` 时读回
  - [ ] SubTask 7.5：把 `ThemeSwitcher` 挂到 `App.vue` 顶部全局位置

- [ ] **Task 8：实现 `StockSearchBox.vue`**
  - [ ] SubTask 8.1：建 `src/components/StockSearchBox.vue`
  - [ ] SubTask 8.2：弹窗用 Ant Design Vue `Modal` + `Input.Search`
  - [ ] SubTask 8.3：建 `src/data/market-symbols.json` 静态列表（CNStock 5000+, USStock 10000+, Crypto 500+, HKStock 2500+）
  - [ ] SubTask 8.4：用 `fuse.js` 模糊匹配（npm install fuse.js）
  - [ ] SubTask 8.5：键盘事件：`↓↑` 选，`Enter` 确认，`Esc` 关闭
  - [ ] SubTask 8.6：全局快捷键 `Ctrl+K` / `Cmd+K` 唤起
  - [ ] SubTask 8.7：选中后 emit `select` 事件，IDE 页面监听后切换股票
  - [ ] SubTask 8.8：在 IDE 页面顶部放「🔍 搜索股票」按钮 + 挂全局监听

- [ ] **Task 9：改造 IDE 主页面**
  - [ ] SubTask 9.1：在 `IndicatorIDE/index.vue` 顶部加：股票选择器 + 搜索按钮 + 主题切换按钮
  - [ ] SubTask 9.2：图表区加 KLineCharts 实例，调用 `setStyles()` 应用当前主题
  - [ ] SubTask 9.3：图表高度调到 700px
  - [ ] SubTask 9.4：用 `createIndicator('MA', ..., { calcParams: [5,10,20] })` 主图叠加 MA
  - [ ] SubTask 9.5：用 `createIndicator('VOL')` 副图 1
  - [ ] SubTask 9.6：用 `createIndicator('MACD')` 副图 2
  - [ ] SubTask 9.7：用 `createIndicator('NET_INFLOW')` 副图 3
  - [ ] SubTask 9.8：调 `setPaneOptions({ height: ... })` 调 pane 高度
  - [ ] SubTask 9.9：监听 `StockSearchBox` 的 `select` 事件，切股票重画
  - [ ] SubTask 9.10：监听主题变化事件，重新调 `setStyles()`

## Phase 4：构建 & 验证（30 分钟）⭐

- [ ] **Task 10：构建脚本**
  - [ ] SubTask 10.1：写 `dev-rebuild.sh`：
    ```bash
    #!/bin/bash
    cd "$(dirname "$0")"
    docker compose -f docker-compose.yml -f docker-compose.build.yml build frontend && \
    docker compose -f docker-compose.yml -f docker-compose.build.yml up -d frontend
    ```
  - [ ] SubTask 10.2：写 `start-qd.sh`：
    ```bash
    #!/bin/bash
    cd "$(dirname "$0")"
    cd QuantDinger-Vue && npm install --registry https://registry.npmmirror.com
    cd .. && docker compose -f docker-compose.yml -f docker-compose.build.yml up -d --build
    ```
  - [ ] SubTask 10.3：`chmod +x dev-rebuild.sh start-qd.sh`

- [ ] **Task 11：端到端验证**
  - [ ] SubTask 11.1：`./dev-rebuild.sh` 重建前端
  - [ ] SubTask 11.2：浏览器登录 → 指标 IDE
  - [ ] SubTask 11.3：默认主题是 Light（亮色），截图 `ide-light.png`
  - [ ] SubTask 11.4：点主题切换 → 暗色，截图 `ide-dark.png`
  - [ ] SubTask 11.5：点搜索按钮 → 输入「600519」→ 选「贵州茅台」→ 图表切换，截图 `search-result.png`
  - [ ] SubTask 11.6：键盘 `Ctrl+K` → 全局搜索 → 输入「TSLA」→ 选 → 切到美股，截图 `search-us.png`
  - [ ] SubTask 11.7：切换到「1时」按钮 → 验证周期切换 + 中文
  - [ ] SubTask 11.8：刷新页面，验证主题和搜索框状态保留

## Phase 5：写"换进"操作手册（30 分钟）⭐

- [ ] **Task 12：写 `REPLACE-GUIDE.md`**
  - [ ] SubTask 12.1：方法 A — Codespace 仓库直接 commit + 重启容器（推荐）
    - 步骤：`git add -A && git commit -m "..." && git push`
    - 重启：`./dev-rebuild.sh` 或 `docker compose restart frontend`
  - [ ] SubTask 12.2：方法 B — 本地 build 静态文件覆盖挂载
    - `cd QuantDinger-Vue && npm run build`
    - `cp -r dist/* /path/to/host/quantdinger-frontend/`
    - 重启容器
  - [ ] SubTask 12.3：方法 C — 导出 patch 包
    - `git format-patch HEAD~5 --output=/tmp/patches/`
    - 复制到目标机器
    - `git am /tmp/patches/*.patch`
  - [ ] SubTask 12.4：每种方法配 iPad 截屏
  - [ ] SubTask 12.5：加 FAQ（"重启后白屏怎么办" / "改坏了怎么回滚" / "如何加环境变量"）

## Task Dependencies

- Task 2 依赖 Task 1
- Task 3 依赖 Task 2
- Task 4 依赖 Task 3
- Task 5, 6 依赖 Task 4
- Task 7, 8 依赖 Task 4
- Task 9 依赖 Task 5, 6, 7, 8
- Task 10 依赖 Task 9
- Task 11 依赖 Task 10
- Task 12 依赖 Task 11
