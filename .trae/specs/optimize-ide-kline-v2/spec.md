# QuantDinger 指标 IDE K 线优化 v2 — Spec

## Why

用户在 QuantDinger 指标 IDE 页面点击「主力净流入」按钮时，**每次点击都新建一个独立的指标实例**，没有去重逻辑，导致 9 个「主力净流入」面板 + 4 个 KDJ + 5 个 ADOSC 全部堆叠显示（见用户截屏）。同时用户希望整个 IDE 页面的 K 线图视觉对齐 Mming 量化风格（jzhu-quant）：**暗色主题 + 4 联动面板（K线/MA / 成交量 / MACD / 主力净流入）+ 中文 tooltip**。还缺一个全 IDE 页面的股票搜索栏（不止顶部自选股下拉）。

参考文件：
- `/workspace/jzhu-quant/index.html` — Mming 量化 K 线图实际代码
- `/workspace/jzhu-quant/Mming量化K线图拆解.txt` — 拆解文档

## What Changes

### A. 修复重复指标 bug
- **修改** `QuantDinger-Vue/src/views/indicator-analysis/components/KlineChart.vue`
  - 在指标按钮点击事件里增加**去重逻辑**：已激活的指标再点就移除（toggle），不创建新实例
  - 在 `addIndicator` / `createIndicator` 调用前判断是否同名实例已存在，存在就 `removeIndicator`
  - KLineCharts 实际 API 用 `chart.removeIndicator({ name: 'NET_INFLOW' })` 或类似方法
  - 验证：KDJ / ADOSC / 主力净流入 三个按钮都修

### B. 顶部加全局搜索栏
- **修改** `QuantDinger-Vue/src/views/indicator-ide/index.vue`
  - 在工具栏顶部「自选标的」下拉框旁边加一个独立的「🔍 股票搜索」输入框
  - 支持跨 market 搜索（复用 v4 spec 里已加的 `onGlobalSearchInput` + `doGlobalSearch` 跨 4 市场并发）
  - 搜索结果弹浮层（用 `a-popover` 或 `a-tooltip` trigger），不挤占下拉框
  - 选中后调用 `setSymbol` 切图

### C. 改造 K 线图视觉对齐 Mming 风格
- **修改** `KlineChart.vue`：
  - 默认 KLineCharts 主题切到**暗色**（`chart.setStyles({ ...darkStyles })`）
  - 默认激活 4 个指标：MA / VOL / MACD / NET_INFLOW（再点 toggle off）
  - tooltip 走 KLineCharts 的 `loadLocales('zh-CN')` 让内置字段变中文
  - 周期按钮中文：1分 / 5分 / 15分 / 30分 / 1时 / 4时 / 1日 / 1周
  - K 线配色：亮色=绿涨红跌（默认），不强调暗色背景（保留原 QuantDinger Light 主题作为默认）

> ⚠️ **不做的事**（用户明确要求）：
> - ❌ 不加全局主题切换器
> - ❌ 不改 background 色为强制暗色（KLineCharts 默认 Light 主题保持）
> - ❌ 不重建示例 demo 文件（用 jzhu-quant 已有的 `index.html` 作参考就行）

### D. 给出可预览的样例网页
- **新增** `/workspace/qd-analysis/mming-kline-demo.html` — 单文件 demo
  - 不依赖 QuantDinger-Vue build
  - 用 ECharts 5.4.3（CDN） + 模拟数据（60 根假 K 线，模拟 000001 平安银行 2025-06 走势）
  - 实现 4 联动面板（K线/MA / 成交量 / MACD / 主力净流入）
  - 暗色主题（仿 Mming 量化风格）
  - 中文 tooltip / 周期按钮
  - 用户在 iPad Safari 打开 file:///workspace/qd-analysis/mming-kline-demo.html 直接看效果

## Impact

| 改动 | 涉及文件 | 用户感知 |
|---|---|---|
| 修复指标去重 | KlineChart.vue | 重复点同按钮不创建新实例 |
| 加搜索栏 | indicator-ide/index.vue | IDE 工具栏顶部多一个搜索框 |
| K线视觉改造 | KlineChart.vue | 暗色 + 4 指标默认显示 + 中文 |
| 示例网页 | mming-kline-demo.html（新增）| 离线可预览新样式 |

## ADDED Requirements

### Requirement: 指标按钮去重（toggle 行为）

`KlineChart.vue` 的指标按钮 SHALL 实现 toggle 行为：
- 点击未激活的指标 → 创建新指标实例
- 点击已激活的指标 → 移除该指标实例
- 绝不允许同名指标在 KLineCharts 全局出现 ≥ 2 次

#### Scenario: 第一次点「主力净流入」
- **WHEN** 用户点击「主力净流入」按钮（图表当前无该指标）
- **THEN** 创建 1 个 NET_INFLOW 指标 pane
- **AND** 按钮高亮状态切换为「已激活」

#### Scenario: 再点「主力净流入」
- **WHEN** 用户再次点击「主力净流入」按钮（图表已有该指标）
- **THEN** 移除已存在的 NET_INFLOW 指标
- **AND** 按钮高亮状态切回「未激活」
- **AND** 图表中**只 0 或 1 个** NET_INFLOW pane（不能是 2 个或更多）

#### Scenario: 多次点不同按钮混合
- **WHEN** 用户依次点 主力净流入 → KDJ → 主力净流入 → 主力净流入 → ADOSC
- **THEN** 最终图表里：NET_INFLOW = 0, KDJ = 1, ADOSC = 1
- **AND** KLineCharts 全局 NET_INFLOW 实例数 = 0
- **AND** KLineCharts 全局 KDJ 实例数 = 1
- **AND** KLineCharts 全局 ADOSC 实例数 = 1

### Requirement: IDE 顶部全局搜索栏

`indicator-ide/index.vue` 工具栏 SHALL 在自选股下拉框旁显示一个独立的「🔍 股票搜索」输入框，复用 `onGlobalSearchInput` + `doGlobalSearch` 跨 4 市场并发搜索。

#### Scenario: 输入「600519」
- **WHEN** 用户在搜索栏输入「600519」并等待 0.5 秒
- **THEN** 下方浮层显示「贵州茅台 sh600519 — CNStock」
- **AND** 浮层标头有「全市场搜索」字样区分
- **AND** 点击/回车选中后图表切到 sh600519

#### Scenario: 输入「TSLA」
- **WHEN** 输入「TSLA」
- **THEN** 浮层显示「Tesla TSLA — USStock」
- **AND** 选中后切到 TSLA

### Requirement: K 线图默认 4 指标配置

`KlineChart.vue` 创建图表实例时 SHALL 默认调 `createIndicator` 4 次：
- 主图：MA(5, 10, 20) 叠加
- 副图 1：VOL
- 副图 2：MACD (12, 26, 9)
- 副图 3：NET_INFLOW

#### Scenario: 打开 IDE 页面
- **WHEN** 用户进入指标 IDE
- **THEN** 图表一加载就有 4 个指标在位（MA + VOL + MACD + NET_INFLOW）
- **AND** 这 4 个按钮都高亮成「已激活」状态

#### Scenario: 移除默认指标
- **WHEN** 用户点击「MACD」按钮（toggle off）
- **THEN** 图表的 MACD pane 消失
- **AND** 其他 3 个指标保留

### Requirement: 中文 KLineCharts locale

`KlineChart.vue` SHALL 在 `initChart` 内调 `klinecharts.loadLocales('zh-CN')`，覆盖内置字段：
- 周期按钮：1分 / 5分 / 15分 / 30分 / 1时 / 4时 / 1日 / 1周
- tooltip：开盘 / 收盘 / 最高 / 最低 / 成交量
- 指标名（NET_INFLOW 自定义显示为「主力净流入」）

#### Scenario: 鼠标悬停 K 线
- **WHEN** 鼠标悬停图表十字线
- **THEN** tooltip 显示「时间 / 开盘 / 收盘 / 最高 / 最低 / 成交量」全中文

#### Scenario: 周期切换按钮
- **WHEN** 用户看周期按钮组
- **THEN** 显示「1分 / 5分 / 15分 / 30分 / 1时 / 4时 / 1日 / 1周」

### Requirement: 离线示例 demo 网页

`mming-kline-demo.html` SHALL 是单文件 HTML，无任何外部依赖（除 ECharts CDN），用 60 根模拟 K 线数据渲染 4 联动面板。

#### Scenario: iPad Safari 打开
- **WHEN** 用户在 iPad Safari 打开 `file:///workspace/qd-analysis/mming-kline-demo.html`
- **THEN** 页面正常显示 4 联动面板的 K 线图
- **AND** 暗色主题（#0d1117 背景）
- **AND** tooltip 全中文
- **AND** 缩放/拖动/十字线联动正常

## MODIFIED Requirements

无。

## REMOVED Requirements

无。

## 文件改动清单

```
新增：
  /workspace/qd-analysis/mming-kline-demo.html   (示例 demo,~300 行)
  
修改：
  QuantDinger-Vue/src/views/indicator-analysis/components/KlineChart.vue
    - 指标按钮点击加 toggle / 去重逻辑
    - 默认创建 4 指标 (MA / VOL / MACD / NET_INFLOW)
    - initChart() 调 loadLocales('zh-CN')
    - 周期 / tooltip 中文覆盖
  QuantDinger-Vue/src/views/indicator-ide/index.vue
    - 工具栏顶部加全局搜索 input
    - 复用 onGlobalSearchInput / doGlobalSearch
```

## 风险 & 缓解

| 风险 | 缓解 |
|---|---|
| KLineCharts API 不同版本差异 | 用 v9.8.0 已验证的 API (`createIndicator` / `removeIndicator` / `loadLocales`) |
| 周期按钮 / tooltip 改不了（KLineCharts 内置字符串硬编码） | 用 `loadLocales('zh-CN')` 走官方翻译；不行就降级为用 `custom-` 字段覆盖 |
| 指标按钮 toggle 改坏了影响正常用户 | 测试全部内置指标 (SMA / EMA / MACD / KDJ / BB / ADOSC / 主力净流入) 都能 toggle |
| 搜索栏并发请求 4 个 market 卡 UI | 已有 350ms debounce；加 loading 状态 |

## 不做

- ❌ 全局主题切换器
- ❌ 强制暗色背景（保留默认 Light）
- ❌ 重建测试 demo 页面
- ❌ 改后端 API
- ❌ 改 IDE 页面其它子功能（代码编辑区、AI 生成等）

## 完成验证

- [ ] 用户在自己 Codespace 重新 build，IDE 页面里点「主力净流入」N 次，图表里始终 ≤ 1 个 NET_INFLOW
- [ ] IDE 工具栏顶部新搜索栏能搜「600519」/「TSLA」
- [ ] 周期按钮 + tooltip 是中文
- [ ] 离线示例 `mming-kline-demo.html` 能用浏览器打开看效果
