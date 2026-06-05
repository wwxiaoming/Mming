# Tasks — QuantDinger IDE K 线优化 v2

按顺序执行；标 ⭐ 的为关键里程碑。

## Phase 1：环境准备（Codespace 30 分钟）

- [ ] **Task 1：Codespace 仓库准备**
  - [ ] SubTask 1.1：在 GitHub 新建空仓库 `quantdinger-custom`（或复用上次 `quantdinger`）
  - [ ] SubTask 1.2：开启 Codespace（4-core / 16GB）
  - [ ] SubTask 1.3：终端执行 `git clone https://github.com/brokermr810/QuantDinger.git .`（注意有点 `.`）拉主仓库源码
  - [ ] SubTask 1.4：执行 `git clone https://github.com/brokermr810/QuantDinger-Vue.git` 拉前端源码到 `./QuantDinger-Vue/`
  - [ ] SubTask 1.5：在 `QuantDinger-Vue/Dockerfile` 顶部加 `RUN npm config set registry https://registry.npmmirror.com`（加速国内网络）

- [ ] **Task 2：后端配置（A 股 + 安全）**
  - [ ] SubTask 2.1：复制 `cp backend_api_python/env.example backend_api_python/.env`
  - [ ] SubTask 2.2：生成 SECRET_KEY：`python3 -c "import secrets; print(secrets.token_hex(32))"` 写入 `backend_api_python/.env`
  - [ ] SubTask 2.3：在 `backend_api_python/.env` 设 `ENABLED_MARKETS=Crypto,USStock,CNStock,HKStock,Forex,Futures,MOEX`
  - [ ] SubTask 2.4：根目录建 `.env` 文件：`IMAGE_PREFIX=docker.m.daocloud.io/library/`

## Phase 2：探索（45 分钟）⭐

- [ ] **Task 3：摸清 IDE 页面结构**
  - [ ] SubTask 3.1：`cd QuantDinger-Vue && cat package.json` — 确认 klinecharts 版本、vue 版本、构建工具
  - [ ] SubTask 3.2：`find src/views -iname "*ide*"` 找指标 IDE 页面路径（可能叫 `IndicatorIDE.vue` / `ide/index.vue` 等）
  - [ ] SubTask 3.3：`find src -name "*.vue" | xargs grep -l "klinecharts"` — 找所有用 KLineCharts 的文件
  - [ ] SubTask 3.4：阅读 IDE 主页面的 `<template>` + `<script>` 段，识别：① 图表初始化函数 ② setStyles 主题调用 ③ 周期切换按钮事件 ④ 数据加载函数
  - [ ] SubTask 3.5：把找到的 3-5 个关键文件路径写到 `quantdinger-ide-files.md` 备忘

- [ ] **Task 4：本地最小 demo 验证 KLineCharts 多 pane**
  - [ ] SubTask 4.1：在 `QuantDinger-Vue/src/views/` 下新建一个 `KDemo/index.vue` 测试页
  - [ ] SubTask 4.2：在路由 `src/router/index.js` 加一条 `/k-demo` 路由指向这个测试页
  - [ ] SubTask 4.3：测试页里写 4 pane（K线 + MA / VOL / MACD / 主力净流入），用 mock 数据（写死 100 根假 K 线）
  - [ ] SubTask 4.4：在 IDE 主页面的菜单里加临时菜单项 "K Demo" 跳到 `/k-demo`
  - [ ] SubTask 4.5：启动 `docker compose -f docker-compose.yml -f docker-compose.build.yml up -d --build`（⭐ 第一次 build）
  - [ ] SubTask 4.6：Codespace 端口转发 8888，浏览器登录 → 菜单 → "K Demo" → 验证 4 pane + 中文 tooltip + 暗色都正常
  - [ ] SubTask 4.7：截屏保存到 `/workspace/.trae/specs/mming-style-kline-viewer/screenshots/k-demo.png`

## Phase 3：正式改 IDE 页面（1.5 小时）⭐

- [ ] **Task 5：注入中文 i18n**
  - [ ] SubTask 5.1：在 IDE 主页面 `<script>` 顶部加 `import { loadLocales } from 'klinecharts'`
  - [ ] SubTask 5.2：在 `created()` / `mounted()` 里执行 `loadLocales('zh-CN')`
  - [ ] SubTask 5.3：把内置未翻译的字段（Open/High/Low/Close/Volume）写一个 `tooltipOverride` 函数覆盖
  - [ ] SubTask 5.4：周期切换按钮文案「1m / 5m / 15m / 30m / 1H / 4H / 1D / 1W」改为「1分 / 5分 / 15分 / 30分 / 1时 / 4时 / 1日 / 1周」

- [ ] **Task 6：注册"主力净流入"自定义指标**
  - [ ] SubTask 6.1：新建 `QuantDinger-Vue/src/charts/indicators/netInflow.js`
  - [ ] SubTask 6.2：用 `klinecharts.registerIndicator('NET_INFLOW', { calc, figures, ... })` 注册
  - [ ] SubTask 6.3：`calc` 函数计算 `volume * (close - open) / (high - low)`，遇 0 除法返回 0
  - [ ] SubTask 6.4：figures 配置为柱子（type: 'bar'），基线 0，baseValue: 0
  - [ ] SubTask 6.5：styles 配红涨绿跌 + tooltip 数值格式化为"X.X亿"

- [ ] **Task 7：改造 IDE 主页面的图表区**
  - [ ] SubTask 7.1：找到现有 KLineCharts 实例，调 `chart.setStyles({...})` 切换到暗色 + 改 K 线配色为红涨绿跌
  - [ ] SubTask 7.2：把图表容器高度从 500px 改 700px
  - [ ] SubTask 7.3：用 `createIndicator('MA', ..., { calcParams: [5,10,20] })` 在主图叠加 MA 三条线
  - [ ] SubTask 7.4：用 `createIndicator('VOL')` 创建成交量副图（KLineCharts 内置）
  - [ ] SubTask 7.5：用 `createIndicator('MACD')` 创建 MACD 副图
  - [ ] SubTask 7.6：用 `createIndicator('NET_INFLOW')` 创建主力净流入副图
  - [ ] SubTask 7.7：调 `setPaneOptions({ height: 200 })` 等调 pane 高度比例

- [ ] **Task 8：容器化与构建**
  - [ ] SubTask 8.1：写 `dev-rebuild.sh` 脚本（增量 build）：
    ```bash
    #!/bin/bash
    cd QuantDinger-Vue && \
      docker compose -f ../docker-compose.yml -f ../docker-compose.build.yml build frontend && \
      docker compose -f ../docker-compose.yml -f ../docker-compose.build.yml up -d frontend
    ```
  - [ ] SubTask 8.2：`chmod +x dev-rebuild.sh`
  - [ ] SubTask 8.3：写 `start-qd.sh` 脚本（首次启动全 build）：
    ```bash
    #!/bin/bash
    cd QuantDinger-Vue && \
      npm install --registry https://registry.npmmirror.com
    cd .. && \
      docker compose -f docker-compose.yml -f docker-compose.build.yml up -d --build
    ```

## Phase 4：验证（30 分钟）⭐

- [ ] **Task 9：浏览器端到端验证**
  - [ ] SubTask 9.1：访问 `https://<codespace>-8888.app.github.dev/`
  - [ ] SubTask 9.2：登录（quantdinger / 123456，改密码）
  - [ ] SubTask 9.3：菜单 → 指标 IDE
  - [ ] SubTask 9.4：股票选择器选「CNStock / 600519 贵州茅台」
  - [ ] SubTask 9.5：周期切到「1日」，验证 4 pane 出现
  - [ ] SubTask 9.6：鼠标悬停 K 线，验证 tooltip 全中文
  - [ ] SubTask 9.7：截屏保存到 `screenshots/ide-after.png`，对比 `k-demo.png`

- [ ] **Task 10：iPad Safari 兼容性**
  - [ ] SubTask 10.1：iPad Safari 登录，访问 IDE 页面
  - [ ] SubTask 10.2：横屏 / 竖屏切换，验证图表响应式正常
  - [ ] SubTask 10.3：双指缩放 / 拖动，验证联动正常
  - [ ] SubTask 10.4：切周期按钮，验证响应 < 5s

## Task Dependencies

- Task 2 依赖 Task 1
- Task 3, 4 依赖 Task 2
- Task 5, 6, 7 依赖 Task 4（demo 跑通后才改主页面）
- Task 8 依赖 Task 5, 6, 7
- Task 9 依赖 Task 8
- Task 10 依赖 Task 9
