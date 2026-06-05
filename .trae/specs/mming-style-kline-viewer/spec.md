# QuantDinger 指标 IDE K 线优化 — Spec v2

## Why

QuantDinger 前端是 **Vue 2 + Ant Design Vue + KLineCharts**（不是 ECharts），源码在公开仓库 `https://github.com/brokermr810/QuantDinger-Vue`（Apache-2.0，可自由修改）。`QuantDinger` 主仓库的 `docker-compose.yml` 注释里**官方明确支持本地 build 前端**：

```yaml
# Local iteration: clone QuantDinger-Vue into `./QuantDinger-Vue/`
# (gitignored) and layer the build override on top:
#   docker compose -f docker-compose.yml -f docker-compose.build.yml up --build
```

用户想在 Codespace 里直接改 IDE 页面的 K 线，让它跟 Mming 量化（jzhu-quant）一样的暗色 4 联动面板（K线 + MA + 成交量 + MACD + 主力净流入），并把英文 tooltip 全部改成中文。

## What Changes

- **新增** Codespace 仓库根目录 `./QuantDinger-Vue/` 子目录（从 GitHub 克隆）
- **修改** `./QuantDinger-Vue/src/views/IndicatorIDE/index.vue`（指标 IDE 主页面）
  - 把内置的 Light 主题切换为暗色（`#0d1117` 背景）
  - 给 KLineCharts 实例设置 `i18n` 为 `zh-CN`（KLineCharts 内置多语言支持）
  - 注册自定义指标「主力净流入」(net_inflow)，用 KLineCharts 的 `registerIndicator` API
  - 在 4 个 pane 里分别画：① 主图 K线 + MA5/MA10/MA20 ② 成交量 ③ MACD ④ 主力净流入柱
  - 把图表高度从 500 → 700px
- **新增** `./QuantDinger-Vue/src/charts/indicators/netInflow.js` 自定义指标文件
  - 计算公式：`netInflow = volume × (close - open) / (high - low)`（与 Mming 量化口径一致）
  - 红色涨 / 绿色跌（与 Mming 反向配色对齐：红涨=亚洲习惯）
- **新增** `./QuantDinger-Vue/src/charts/i18n/zh-CN.js` 自定义 tooltip 文案
  - 把内置的 "Time / Open / High / Low / Close / Volume" 改为「时间 / 开盘 / 最高 / 最低 / 收盘 / 成交量」
- **新增** 仓库根目录 `Dockerfile.frontend-build`（如 QuantDinger-Vue 自带的 Dockerfile 不够用）
- **修改** `docker-compose.yml` 不变（用现成的）+ `docker-compose.build.yml` 不变（已配好本地 build 路径）
- **新增** Codespace 仓库根目录 `start-qd.sh` 启动脚本（与 jzhu-quant 的 `start-all.sh` 类似）

> **BREAKING**：无；纯属视觉/功能优化，原 API、其它页面、其它指标不受影响。

## Impact

- **Affected specs**：
  - `learn-sillytavern-character-cards` — 无影响
- **Affected code**：
  - Codespace 仓库根目录（新增 `QuantDinger-Vue/` 子目录、`start-qd.sh`）
  - `QuantDinger-Vue/src/views/IndicatorIDE/index.vue`
  - `QuantDinger-Vue/src/charts/indicators/netInflow.js`
  - `QuantDinger-Vue/src/charts/i18n/zh-CN.js`
- **Affected deployments**：
  - Codespace 第一次 build 前端约 5-10 分钟（npm install + webpack build）
  - 后续修改增量 build 1-3 分钟
  - iPad Safari 访问方式不变

## ADDED Requirements

### Requirement: QuantDinger-Vue 本地源码可访问

系统 SHALL 在 Codespace 仓库根目录下提供 `./QuantDinger-Vue/` 目录，内容与 `https://github.com/brokermr810/QuantDinger-Vue` 的 main 分支一致。

#### Scenario: 仓库克隆完成

- **WHEN** 用户在 Codespace 终端执行 `git clone https://github.com/brokermr810/QuantDinger-Vue.git`
- **THEN** 当前目录出现 `QuantDinger-Vue/` 文件夹
- **AND** `QuantDinger-Vue/package.json` 存在且声明 vue / klinecharts / ant-design-vue 等依赖
- **AND** `QuantDinger-Vue/Dockerfile` 存在（用于 docker build）

### Requirement: 指标 IDE 页面支持 4 面板暗色布局

`QuantDinger-Vue/src/views/IndicatorIDE/index.vue` SHALL 渲染 KLineCharts 时使用：
- 主题：dark（背景 `#0d1117`、网格 `#1f2937`、文字 `#d1d5db`）
- 主图：K线 + 叠加 MA(5, 10, 20) 三条线
- 副图 1：成交量柱（红涨绿跌）
- 副图 2：MACD (12, 26, 9) — DIF / DEA / 柱
- 副图 3：主力净流入柱（自定义指标）

#### Scenario: 打开 IDE 页面默认布局

- **WHEN** 用户在 QuantDinger 系统里点击"指标 IDE" 菜单
- **THEN** 页面在右侧图表区显示 4 个联动面板，K线主图占 50% 高度，3 个副图各占 ~16%
- **AND** 主图标题区显示股票代码 + 周期切换按钮 + 指标选择下拉
- **AND** 鼠标悬停 K 线时，十字线 4 个面板同步，tooltip 显示中文 OHLCV

#### Scenario: 修改源码后能 build

- **WHEN** 用户编辑 `IndicatorIDE/index.vue` 保存
- **THEN** 在 Codespace 终端执行 `cd QuantDinger-Vue && npm install && npm run build` 能在 1-3 分钟内产出 `dist/`
- **AND** 执行 `docker compose -f docker-compose.yml -f docker-compose.build.yml build frontend` 能在 3-5 分钟内产出新镜像
- **AND** `docker compose -f docker-compose.yml -f docker-compose.build.yml up -d` 启动后浏览器刷新就能看到修改

### Requirement: 中文 tooltip 与中文周期按钮

#### Scenario: 鼠标悬停 K 线

- **WHEN** 鼠标悬停图表十字线位置
- **THEN** tooltip 显示：「时间 2026-06-01 / 开盘 427.49 / 最高 433.60 / 最低 413.65 / 收盘 418.45 / 成交量 161.273M / 涨跌幅 -2.11% / MA5 419.32 / MA10 421.07 / MA20 425.88 / DIF -0.110 / DEA -0.074 / MACD -0.073 / 主力净流入 -1.9亿」全部中文

#### Scenario: 周期切换按钮

- **WHEN** 用户点击「1时」按钮
- **THEN** 图表重新拉取小时 K 线并重渲染
- **AND** 按钮文案「1分 / 5分 / 15分 / 30分 / 1时 / 4时 / 1日 / 1周」全部中文

### Requirement: 主力净流入自定义指标

`QuantDinger-Vue/src/charts/indicators/netInflow.js` SHALL 注册一个名为「主力净流入」的自定义指标，计算公式 `volume * (close - open) / (high - low)`，渲染为柱子（红涨绿跌），与 Mming 量化配色对齐。

#### Scenario: 注册到全局

- **WHEN** 应用启动时执行 `import './charts/indicators/netInflow'`
- **THEN** KLineCharts 全局可通过 `createIndicator('NET_INFLOW', ...)` 引用
- **AND** tooltip 中显示「主力净流入 -1.9亿」（亿为单位格式化）

#### Scenario: 0 涨跌时

- **WHEN** `(close - open) / (high - low) = 0`（平盘）
- **THEN** 净流入 = 0，柱高度为 0，不画

### Requirement: A 股数据可访问

`backend_api_python/.env` SHALL 配置 `ENABLED_MARKETS=Crypto,USStock,CNStock,HKStock,Forex,Futures,MOEX`，`SHOW_CN_STOCK=true`，使指标 IDE 能选 A股。

#### Scenario: 选 A股

- **WHEN** IDE 页面顶部股票选择器选「CNStock / 600519 贵州茅台」
- **THEN** 图表 5 秒内加载 K 线数据（后端走腾讯财经 / AkShare）

## MODIFIED Requirements

无（属于纯新增，不修改现有需求行为）。

## REMOVED Requirements

无。

## 实施关键点

1. **KLineCharts 与 ECharts 差异**：
   - KLineCharts 是 canvas 渲染，自带 MA/MACD/RSI 等指标，但**主图只有 1 个 pane**，副图（成交量、MACD）要通过 `createIndicator('MA', ..., { paneId: '...' })` 显式指定 pane
   - 多 pane 联动：KLineCharts v9 内置联动（不像 ECharts 要 `dataZoom.xAxisIndex: [...]`），所有 pane 默认共享 xAxis
   - 自定义指标用 `klinecharts.registerIndicator(name, { calc, figures, ... })`

2. **i18n 改造**：
   - KLineCharts v9 内置 `zh-CN` 语言包：`import { loadLocales } from 'klinecharts'` 然后 `loadLocales('zh-CN')`
   - 但内置翻译只覆盖部分字段，**剩余 "Open" "High" 等要自己在 indicator 的 `createTooltipDataSource` 里覆盖**

3. **K 线配色**：
   - KLineCharts 默认绿涨红跌（A 股习惯相反），要覆盖 styles：
   ```js
   chart.setStyles({
     candle: {
       bar: {
         upColor: '#ef4444',     // 涨 = 红
         downColor: '#10b981',   // 跌 = 绿
         noChangeColor: '#888'
       }
     }
   })
   ```

4. **Docker build 性能**：
   - 第一次 build 前端要 npm install 几百 MB 依赖，需要 Codespace 至少 4-core 8GB
   - 在 `.env` 加 `IMAGE_PREFIX=docker.m.daocloud.io/library/` 加速基础镜像
   - 在 `QuantDinger-Vue/Dockerfile` 里改 npm registry 为 npmmirror.com（淘宝镜像）加速

5. **修改后增量 build**：
   - Vue 2 项目一般用 vue-cli-service build，Dockfile 多阶段 build
   - 修改 .vue 文件后只需 `docker compose build frontend` 增量构建（~2-3 分钟）

## 风险 & 缓解

| 风险 | 缓解 |
|---|---|
| npm install 超时 / 失败 | 在 Dockerfile 加 `npm config set registry https://registry.npmmirror.com` |
| 前端 build 内存爆（2GB 机器） | Codespace 选 4-core / 16GB；或加 `NODE_OPTIONS=--max-old-space-size=4096` |
| 改源码后忘记重启容器 | 写一个 `dev-rebuild.sh` 脚本：`docker compose build frontend && docker compose up -d frontend` |
| KLineCharts API 与 ECharts 差异大 | 写最小 demo 先验证多 pane 联动，再迁到 IDE 页面 |
| 误改 Vue 文件导致整个页面崩 | git 提交每个稳定版本，`git reset --hard HEAD~1` 快速回滚 |
