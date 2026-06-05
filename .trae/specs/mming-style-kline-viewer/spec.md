# QuantDinger IDE K 线 — Spec v4（精简）

## 现状（已查源码确认）

`QuantDinger-Vue` 仓库 main 分支，**v3.0.28**：

| 功能 | 是否存在 | 文件位置 |
|---|---|---|
| 主题切换（亮/暗） | ✅ 已有 | `src/views/indicator-ide/index.vue` 顶部 `<div class="indicator-ide" :class="{ 'theme-dark': isDarkTheme }">` |
| 多语言 i18n | ✅ 已有 | `src/locales/{index.js,lang/zh-CN.js}`，默认 `en-US` |
| KLineCharts 多 pane | ✅ 已有 | `src/views/indicator-analysis/components/KlineChart.vue` 已用 `createIndicator` 创建 VOL/MACD/MA 等 |
| 自定义指标 | ✅ 支持 | `KlineChart.vue` 第 3384-3736 行有 `createIndicator(customIndicatorName, ...)` 模式 |
| 股票搜索 | ⚠️ 部分 | 现有 `searchSymbols()` API 在 `@/api/market`，**但 UI 只在"加入自选"弹窗里用**，IDE 顶部下拉仍只显示已加自选的 |
| "主力净流入" 指标 | ❌ 缺 | 完全没注册 |
| 中文界面 | ⚠️ 翻译齐了但默认 en-US | 用户需在右上角切语言，或在 `.env` / store 改默认 |

## Why

用户（iPad + GitHub Codespace）想：
1. 指标 IDE 里加一个 **"主力净流入"** 自定义指标（与 Mming 量化 / jzhu-quant 一致）
2. IDE 顶部股票选择器能**搜索全市场**（不只自选股）并直接切股票
3. IDE 页面默认显示**中文**（避免每次手动切语言）

## What Changes

- **新增** `src/charts/indicators/netInflow.js` 注册 NET_INFLOW 指标
- **修改** `src/views/indicator-analysis/components/KlineChart.vue`
  - 引入 netInflow.js
  - 在 indicatorButtons 列表加 `NET_INFLOW` 按钮
- **修改** `src/views/indicator-ide/index.vue`
  - 顶部股票选择器改用 `searchSymbols()` 替代只看 watchlist
  - 默认 `i18n.locale = 'zh-CN'`（在 `mounted()` 强制设）
- **新增** `REPLACE-GUIDE.md` — Codespace 部署 + 容器替换手册
- **新增** `dev-rebuild.sh` 增量 build 脚本

> **BREAKING**：无。所有改动不破坏现有功能，主题切换器、自选股流程、其它指标均不变。

## Impact

- 新增 1 个文件、修改 2 个文件、新增 1 个文档、1 个脚本
- 不需要新建 demo 页 / 主题切换组件 / 搜索弹窗（用现有的）
- 不修改背景色 / 主题逻辑（按用户要求"不强调背景色"）

## ADDED Requirements

### Requirement: 主力净流入自定义指标
`src/charts/indicators/netInflow.js` SHALL 注册名为 `NET_INFLOW` 的 KLineCharts 指标，公式 `volume * (close - open) / (high - low)`，渲染为柱状图（baseValue=0），tooltip 数值格式化为 "X.X亿"。

#### Scenario: 在指标 IDE 工具栏出现
- **WHEN** 用户打开指标 IDE
- **THEN** 工具栏新增一个按钮「主力净流入」（或在已展开指标列表里能选到）
- **AND** 点击后图表下方新增一个 pane 显示柱状图

#### Scenario: 平盘 0 涨跌
- **WHEN** `high === low`（一字板）
- **THEN** 返回 0，不抛 NaN

### Requirement: IDE 顶部股票选择支持全市场搜索
`indicator-ide/index.vue` 顶部 Select 组件 SHALL 改用 `a-select` 的 `show-search` + `filter-option` 调后端 `searchSymbols()`，**跨 market 搜索**（默认搜 CNStock + USStock + Crypto + HKStock），选中后直接调用 `setSymbol` 切图。

#### Scenario: 输入"600519"
- **WHEN** 在 IDE 顶部选择器输入「600519」
- **THEN** 弹出下拉建议包含「贵州茅台 sh600519 — CNStock」
- **AND** 选中后图表自动切到 sh600519，无需先加入自选

#### Scenario: 输入"TSLA"
- **WHEN** 输入「TSLA」
- **THEN** 弹出「Tesla TSLA — USStock」
- **AND** 选中后切到 TSLA

#### Scenario: 不在自选股里也能搜
- **WHEN** 用户没添加 sh600519 到自选，但搜索了 600519
- **THEN** 仍能选到（不限自选股）

### Requirement: 默认中文界面
`indicator-ide/index.vue` 的 `mounted()` SHALL 调 `this.$i18n.locale = 'zh-CN'`（覆盖默认 en-US）。

#### Scenario: 首次进入
- **WHEN** 用户登录 IDE 页面
- **THEN** 顶部菜单、按钮、tooltip、统计文字都是中文

#### Scenario: 切换语言保留
- **WHEN** 用户在右上角切到 English
- **THEN** 整站切到英文（已存在功能不被破坏）

## MODIFIED Requirements

无。

## REMOVED Requirements

无。

## 文件改动清单

```
新增：
  QuantDinger-Vue/src/charts/indicators/netInflow.js    (~80 行)
  REPLACE-GUIDE.md                                       (~150 行)
  dev-rebuild.sh                                          (~10 行)

修改：
  QuantDinger-Vue/src/views/indicator-analysis/components/KlineChart.vue
    - import './charts/indicators/netInflow'
    - indicatorButtons 列表加 { id: 'NET_INFLOW', name: '主力净流入', shortName: '主力净流入' }
  QuantDinger-Vue/src/views/indicator-ide/index.vue
    - mounted() 设 this.$i18n.locale = 'zh-CN'
    - 顶部自选 Select 改为 show-search + searchSymbols 远程搜索
```

## 不做（用户明确说"不强调"）

- ❌ 不加主题切换器（已有）
- ❌ 不改背景色
- ❌ 不新建主题切换组件
- ❌ 不新建搜索弹窗（复用现有的 searchSymbols API）
- ❌ 不新建 demo 页面
- ❌ 不改 KLineCharts 默认样式

## 三种"换进"的方法（详见 REPLACE-GUIDE.md）

| 方法 | 适用 | 难度 |
|---|---|---|
| A：Codespace commit + `./dev-rebuild.sh` | Codespace 部署 | ⭐ |
| B：本地 build dist/ 覆盖挂载 | 自建服务器 | ⭐⭐ |
| C：导出 git format-patch 包 | 分享给他人 | ⭐⭐⭐ |
