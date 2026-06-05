# QuantDinger 指标 IDE K 线优化 — Spec v3

## Why

QuantDinger 前端是 **Vue 2 + Ant Design Vue + KLineCharts**（不是 ECharts），源码在公开仓库 `https://github.com/brokermr810/QuantDinger-Vue`（Apache-2.0，可自由修改）。`QuantDinger` 主仓库的 `docker-compose.yml` 注释里**官方明确支持本地 build 前端**：

```yaml
# Local iteration: clone QuantDinger-Vue into `./QuantDinger-Vue/`
# (gitignored) and layer the build override on top:
#   docker compose -f docker-compose.yml -f docker-compose.build.yml up --build
```

用户想在 Codespace 里直接改 IDE 页面（指标 IDE 主页面 + 全局）：
1. K 线显示升级：4 联动面板（K线+MA / 成交量 / MACD / 主力净流入），跟 Mming 量化（jzhu-quant）一致
2. 英文 tooltip 全部改中文
3. **不强调背景色**（默认保持原 Ant Design Vue 的 Light 主题）
4. **加全局主题切换**（亮色 / 暗色 两套，IDE 页面右上角放开关）
5. **加股票搜索框**（全市场搜索，不仅限自选股）
6. 提供详细的"如何把修改后的代码换进现有部署"操作手册

## What Changes

- **新增** Codespace 仓库根目录 `./QuantDinger-Vue/` 子目录（从 GitHub 克隆）
- **修改** `./QuantDinger-Vue/src/views/IndicatorIDE/index.vue`（指标 IDE 主页面）
  - 注册"主力净流入"(NET_INFLOW) 自定义指标
  - 在 4 个 pane 里分别画：① 主图 K线 + MA5/MA10/MA20 ② 成交量 ③ MACD ④ 主力净流入柱
  - 把图表高度从默认调到 700px
  - 集成主题切换按钮（亮 / 暗）
  - 集成全市场股票搜索框
- **新增** `./QuantDinger-Vue/src/charts/indicators/netInflow.js` 自定义指标文件
  - 计算公式：`netInflow = volume × (close - open) / (high - low)`
  - 配色跟 IDE 主题联动：亮色模式绿涨红跌（A 股默认） / 暗色模式红涨绿跌（亚洲习惯）
- **新增** `./QuantDinger-Vue/src/charts/i18n/zh-CN.js` 自定义 tooltip 文案
  - 「Open → 开盘 / High → 最高 / Low → 最低 / Close → 收盘 / Volume → 成交量」
  - 周期按钮「1m → 1分 / 5m → 5分 / 1H → 1时 / 1D → 1日 / 1W → 1周」
- **新增** `./QuantDinger-Vue/src/components/ThemeSwitcher.vue` 全局主题切换组件
  - 右上角浮窗开关，2 档：「亮色（默认）」 / 「暗色」
  - 用 Vuex / Pinia 存全局 `theme` 状态
  - 切换时同步更新 KLineCharts 的 `setStyles({...})` + 全局 CSS 变量
- **新增** `./QuantDinger-Vue/src/components/StockSearchBox.vue` 全局股票搜索组件
  - 弹窗式输入框（按 `Ctrl+K` / 顶部按钮触发）
  - **不限制** 自选股（默认查全市场，支持 CNStock / USStock / Crypto / HKStock / Forex / Futures）
  - 后端走 `GET /api/market/search?keyword=...`（如无此端点则前端本地 mock）
  - 支持模糊搜索、键盘上下键选、回车跳转
- **修改** `./QuantDinger-Vue/src/main.js` / `App.vue`
  - 引入 `loadLocales('zh-CN')` 全局中文
  - 引入并挂载 `ThemeSwitcher` + `StockSearchBox`
  - 应用启动时读 `localStorage.theme` 恢复上次主题
- **新增** Codespace 仓库根目录 `start-qd.sh` 一键启动脚本
- **新增** Codespace 仓库根目录 `dev-rebuild.sh` 增量重建脚本
- **新增** `REPLACE-GUIDE.md` — **详细图文操作手册**，教用户 3 种把改好的代码"换进"已有部署的方法：
  - 方法 A：Codespace 仓库直接 commit + 重启容器（推荐）
  - 方法 B：本地 build 出 dist/ 静态文件，覆盖挂载到容器
  - 方法 C：导出 patch 包，在另一台机器应用

> **BREAKING**：无；纯属视觉/功能优化，原 API、其它页面、其它指标不受影响。默认主题仍为 Light，保持原观感。

## Impact

- **Affected specs**：
  - `learn-sillytavern-character-cards` — 无影响
- **Affected code**：
  - Codespace 仓库根目录（新增 `QuantDinger-Vue/`、`start-qd.sh`、`dev-rebuild.sh`、`REPLACE-GUIDE.md`）
  - `QuantDinger-Vue/src/main.js` / `App.vue`
  - `QuantDinger-Vue/src/views/IndicatorIDE/index.vue`
  - `QuantDinger-Vue/src/charts/indicators/netInflow.js`
  - `QuantDinger-Vue/src/charts/i18n/zh-CN.js`
  - `QuantDinger-Vue/src/components/ThemeSwitcher.vue`（新）
  - `QuantDinger-Vue/src/components/StockSearchBox.vue`（新）
- **Affected deployments**：
  - 第一次 build 前端约 5-10 分钟（npm install + webpack build）
  - 后续修改增量 build 1-3 分钟
  - iPad Safari 访问方式不变

## ADDED Requirements

### Requirement: 4 联动面板 + 自定义指标

`QuantDinger-Vue/src/views/IndicatorIDE/index.vue` SHALL 渲染 KLineCharts 时使用 4 个联动 pane：
- 主图：K线 + 叠加 MA(5, 10, 20) 三条线
- 副图 1：成交量柱
- 副图 2：MACD (12, 26, 9)
- 副图 3：主力净流入柱（自定义 NET_INFLOW 指标）

#### Scenario: 打开 IDE 页面默认布局

- **WHEN** 用户在 QuantDinger 系统里点击"指标 IDE" 菜单
- **THEN** 右侧图表区显示 4 个联动面板，K线主图占 50% 高度，3 个副图各占 ~16%
- **AND** 鼠标悬停 K 线时，4 个 pane 十字线同步，tooltip 全中文

### Requirement: 主题切换器（亮 / 暗）

`ThemeSwitcher.vue` SHALL 提供亮色 / 暗色两档主题切换，挂在 IDE 页面右上角。

#### Scenario: 切换到暗色

- **WHEN** 用户点击主题切换按钮选「暗色」
- **THEN** KLineCharts 调用 `chart.setStyles({...})` 应用暗色样式：背景 `#0d1117`、网格 `#1f2937`、文字 `#d1d5db`、K线 红涨绿跌
- **AND** 全局 CSS 变量 `--bg-primary / --text-primary` 切换
- **AND** 选择写入 `localStorage.theme = 'dark'`，下次打开自动恢复
- **AND** 图表配色 K 线 `upColor: #ef4444, downColor: #10b981`

#### Scenario: 切换到亮色（默认）

- **WHEN** 用户点击主题切换按钮选「亮色」（或首次进入）
- **THEN** 恢复 Ant Design Vue 默认 Light 主题
- **AND** KLineCharts K 线 `upColor: #10b981, downColor: #ef4444`（绿涨红跌，国内 A 股默认）
- **AND** 写入 `localStorage.theme = 'light'`

#### Scenario: 主题切换不影响其它页面

- **WHEN** 用户从 IDE 切到"AI 智能分析"页面
- **THEN** 主题保持用户选定的（不重置）

### Requirement: 全局股票搜索（不限自选股）

`StockSearchBox.vue` SHALL 提供全市场股票搜索，不限制自选股。

#### Scenario: 顶部按钮触发搜索

- **WHEN** 用户点击 IDE 页面顶部「🔍 搜索股票」按钮
- **THEN** 弹出模态框，输入框自动 focus
- **AND** 输入关键字 ≥ 1 个字符时实时显示搜索建议列表
- **AND** 列表项显示：代码 + 名称 + 市场标签（CNStock / USStock / Crypto 等）
- **AND** 点击 / 回车选中后跳转到该股票图表

#### Scenario: 全市场搜索（不是只搜自选股）

- **WHEN** 用户输入「600519」
- **THEN** 返回 `贵州茅台 (sh600519) - CNStock` 在结果中（即使未加入自选股）
- **AND** 用户输入「TSLA」返回 `Tesla (TSLA) - USStock`
- **AND** 用户输入「BTC」返回 `BTC/USDT` 等加密货币
- **AND** 用户输入「00700」返回 `腾讯控股 (hk00700) - HKStock`

#### Scenario: 键盘操作

- **WHEN** 搜索结果列表打开
- **THEN** 键盘 `↓` / `↑` 可上下选择项，`Enter` 确认，`Esc` 关闭
- **AND** 选中的项高亮背景

#### Scenario: 全局快捷键

- **WHEN** 用户按 `Ctrl+K`（Mac 按 `Cmd+K`）
- **THEN** 全局唤起搜索框（任意页面都可用）
- **AND** 再按 `Esc` 关闭

### Requirement: 中文 tooltip

#### Scenario: 鼠标悬停 K 线

- **WHEN** 鼠标悬停图表十字线位置
- **THEN** tooltip 显示：「时间 2026-06-01 / 开盘 427.49 / 最高 433.60 / 最低 413.65 / 收盘 418.45 / 成交量 161.273M / 涨跌幅 -2.11% / MA5 419.32 / MA10 421.07 / MA20 425.88 / DIF -0.110 / DEA -0.074 / MACD -0.073 / 主力净流入 -1.9亿」全部中文

#### Scenario: 周期切换按钮

- **WHEN** 用户点击「1时」按钮
- **THEN** 图表重新拉取小时 K 线并重渲染
- **AND** 按钮文案「1分 / 5分 / 15分 / 30分 / 1时 / 4时 / 1日 / 1周」全部中文

### Requirement: 主力净流入自定义指标

`netInflow.js` SHALL 注册一个名为「主力净流入」的自定义指标：
- 计算公式 `volume * (close - open) / (high - low)`
- 亮色主题：绿涨红跌
- 暗色主题：红涨绿跌
- tooltip 数值格式化为"X.X亿"（除以 1e8）

### Requirement: A 股数据可访问

`backend_api_python/.env` SHALL 配置 `ENABLED_MARKETS=Crypto,USStock,CNStock,HKStock,Forex,Futures,MOEX`、`SHOW_CN_STOCK=true`，使 IDE 能选 A 股。

#### Scenario: 选 A 股

- **WHEN** IDE 页面顶部股票选择器选「CNStock / 600519 贵州茅台」
- **THEN** 图表 5 秒内加载 K 线数据（后端走腾讯财经 / AkShare）

## MODIFIED Requirements

无（属于纯新增，不修改现有需求行为）。

## REMOVED Requirements

无。

## 实施关键点

1. **KLineCharts 与 ECharts 差异**：
   - KLineCharts canvas 渲染，主图 1 pane，副图通过 `createIndicator('X', ..., { paneId: '...' })` 显式指定
   - 多 pane 联动：KLineCharts v9 内置联动，所有 pane 共享 xAxis
   - 自定义指标用 `klinecharts.registerIndicator(name, { calc, figures, ... })`

2. **i18n 改造**：
   - KLineCharts v9 内置 `zh-CN`：`import { loadLocales } from 'klinecharts'` → `loadLocales('zh-CN')`
   - 内置翻译只覆盖部分字段，剩余 "Open" "High" 等要自己在 indicator 的 `createTooltipDataSource` 里覆盖

3. **主题切换实现**：
   - 全局 CSS 变量：`document.documentElement.style.setProperty('--bg', '#0d1117')`
   - Ant Design Vue 主题：`ConfigProvider` 组件的 `theme` prop
   - KLineCharts：`chart.setStyles({ grid: { horizontal: { color: '#1f2937' } }, candle: { bar: { upColor, downColor } } })`
   - 切换时三个同步更新

4. **股票搜索数据源**：
   - 后端有 `GET /api/market/search?keyword=xxx`（或类似）端点时直接调
   - 后端没有时，前端预置一份静态列表 `src/data/market-symbols.json`（CNStock 5000+ / USStock 10000+ / Crypto 500+ / HKStock 2500+）做模糊匹配
   - 搜索算法：`fuse.js` 模糊匹配，按代码前缀 + 名称包含打分

5. **Docker build 性能**：
   - 第一次 build 5-10 分钟（npm install + webpack build）
   - 在 `QuantDinger-Vue/Dockerfile` 加 `npm config set registry https://registry.npmmirror.com`
   - 在根目录 `.env` 加 `IMAGE_PREFIX=docker.m.daocloud.io/library/`

6. **修改后增量 build**：
   - `dev-rebuild.sh` 脚本：`docker compose -f docker-compose.yml -f docker-compose.build.yml build frontend && docker compose up -d frontend`（~2-3 分钟）

## 风险 & 缓解

| 风险 | 缓解 |
|---|---|
| npm install 超时 | Dockerfile 加 npmmirror |
| 前端 build 内存爆 | Codespace 选 4-core / 16GB；加 `NODE_OPTIONS=--max-old-space-size=4096` |
| KLineCharts API 与 ECharts 差异 | 先在 `KDemo/index.vue` 验证多 pane 联动 |
| 改源码导致整个页面崩 | git 提交每个稳定版本 + 备份 GHCR 旧镜像标签可回退 |
| 主题切换状态丢失 | `localStorage.theme` 持久化 |
| 搜索框无后端支持 | 前端预置静态列表（CNStock 5000+，够用） |
| 误改 Vue 文件 | `git reset --hard HEAD~1` 快速回滚 |

## 三种"换进去"的方法（见 REPLACE-GUIDE.md）

| 方法 | 适用 | 难度 |
|---|---|---|
| A：Codespace 仓库直接 commit + 重启容器 | Codespace 部署 | ⭐ 最简单 |
| B：本地 build 出 dist/ 静态文件，覆盖挂载到容器 | 自建服务器 / Docker 部署 | ⭐⭐ |
| C：导出 patch 包，在另一台机器应用 | 想分享给他人 | ⭐⭐⭐ |
