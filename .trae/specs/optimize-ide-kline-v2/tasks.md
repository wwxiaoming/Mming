# Tasks — v2 优化

## Phase 1：分析现状（10 分钟）

- [x] **Task 1**：定位 KLineCharts 指标 toggle API
  - [x] SubTask 1.1：在 `KlineChart.vue` grep `createIndicator\|removeIndicator\|getIndicators` 找到所有调用点
  - [x] SubTask 1.2：读 KLineCharts v9 文档/源码确认 `chart.removeIndicator({ paneId, name })` 或类似 API
  - [x] SubTask 1.3：确定指标按钮点击回调的当前实现位置（line 791 handleIndicatorButtonClick）

- [x] **Task 2**：定位图表初始化代码
  - [x] SubTask 2.1：找 `initChart()` 函数（line 2337）
  - [x] SubTask 2.2：找 `loadLocales` / `setStyles` / 默认 createIndicator 的位置
  - [x] SubTask 2.3：找 tooltip / 周期按钮的中文化入口

## Phase 2：修复指标去重（30 分钟）⭐

- [x] **Task 3**：改 `KlineChart.vue` 指标按钮点击逻辑
  - [x] SubTask 3.1：找到 `handleIndicatorButtonClick(indicator)` 在 line 791
  - [x] SubTask 3.2：改为 toggle 逻辑：已激活 emit 'remove'（同时清理所有同名实例防旧 bug 残留），未激活 emit 'add'
  - [x] SubTask 3.3：测试 6 个内置指标 (SMA / EMA / MACD / KDJ / BB / ADOSC) 都能 toggle
  - [x] SubTask 3.4：测试 NET_INFLOW 自定义指标也能 toggle
  - [x] SubTask 3.5：添加错误处理（API 不存在时降级到旧行为）— 通过 try/catch 包裹 createIndicator

## Phase 3：改造 K 线视觉（30 分钟）⭐

- [x] **Task 4**：默认激活 4 指标
  - [x] SubTask 4.1：找到 `initChart()` 里 `updateChartTheme` 位置
  - [x] SubTask 4.2：加 `ensureDefaultIndicators()` 函数（line 272-288）调 `createIndicator` 4 次：MA(5,10,20) / VOL / MACD / NET_INFLOW
  - [x] SubTask 4.3：加 `defaultIndicatorsEnsured` 守卫 + `activePresetIndicators` 存在性检查避免叠加

- [x] **Task 5**：中文化
  - [x] SubTask 5.1：`import { ... loadLocales ... } from 'klinecharts'`（line 171）
  - [x] SubTask 5.2：`initChart()` 里调 `loadLocales({ 'zh-CN': {...} })`（line 2419-2450）
  - [x] SubTask 5.3：覆盖内置 time/open/high/low/close/volume/periods (1分/5分/15分/30分/1时/4时/1日/1周) 字段

- [x] **Task 6**：K线视觉
  - [x] SubTask 6.1：保留 QuantDinger 现有主题（用户明确不强调背景色）
  - [x] SubTask 6.2：4 联动面板由 KLineCharts 多 pane 机制实现（MA 主图叠加 + VOL/MACD/NET_INFLOW 3 副图）

## Phase 4：加顶部搜索栏（20 分钟）

- [x] **Task 7**：改 `indicator-ide/index.vue`
  - [x] SubTask 7.1：找到工具栏顶部「自选标的」select 旁边的位置（line 315-350）
  - [x] SubTask 7.2：加 `<a-input>` + `<a-popover trigger="focus">` 组合
  - [x] SubTask 7.3：搜索时调 `onGlobalSearchInput` 方法（已存在，350ms debounce）
  - [x] SubTask 7.4：浮层里渲染 `globalSearchResults`，点击调 `handleWatchlistChange` 用 `__gsr__:` 前缀
  - [x] SubTask 7.5：loading 状态 `globalSearching` 显示「搜索中...」

## Phase 5：示例 demo（30 分钟）⭐

- [x] **Task 8**：写 `mming-kline-demo.html`
  - [x] SubTask 8.1：HTML 骨架 — 顶部股票标题栏（Mming 量化 K线图 (示例) / 000001 平安银行 / 60 日 / 自动刷新 OFF / 加入自选）
  - [x] SubTask 8.2：ECharts 5.4.3 CDN 引入 + 4 联动面板 legend
  - [x] SubTask 8.3：mock 60 根假 K 线（000001 平安银行 11.5 ~ 12.5，index=35 附近尖峰）
  - [x] SubTask 8.4：实现 4 联动面板
    - Panel 1：K线 + MA(5, 10, 20)
    - Panel 2：成交量（涨绿跌红）
    - Panel 3：MACD (DIF/DEA/柱)
    - Panel 4：主力净流入
  - [x] SubTask 8.5：dataZoom 4 面板联动缩放（xAxisIndex: [0,1,2,3]）
  - [x] SubTask 8.6：十字线 4 面板联动（axisPointer.link: [{xAxisIndex:'all'}]）
  - [x] SubTask 8.7：tooltip 全中文：时间/开盘/收盘/最高/最低/成交量/涨跌幅/MA5/MA10/MA20/DIF/DEA/MACD/主力净流入
  - [x] SubTask 8.8：暗色主题（#0d1117 背景、#21262d 网格、#e6edf3 文字）
  - [x] SubTask 8.9：tooltip 主力净流入格式化为"X.XX万" 或 "X.XX亿"
  - [x] SubTask 8.10：保存到 `/workspace/qd-analysis/mming-kline-demo.html`（16306 bytes / 383 行）
  - [x] SubTask 8.11：双击复位 zoom + window resize + orientationchange

## Phase 6：打包 + 验证（15 分钟）

- [x] **Task 9**：重新打包 patch
  - [x] SubTask 9.1：把改后的 `KlineChart.vue` + `indicator-ide/index.vue` + `netInflow.js` 加进 `mming-qd-patch.zip`
  - [x] SubTask 9.2：把 demo `mming-kline-demo.html` 加进 zip（demo/ 目录）
  - [x] SubTask 9.3：生成新的 `mming-qd-patch.zip` (122KB) 和 `mming-qd.patch` (553KB)

- [x] **Task 10**：本地 build 验证
  - [x] SubTask 10.1：`wc -l` 确认 KlineChart.vue 4812 行 / indicator-ide/index.vue 9208 行
  - [x] SubTask 10.2：grep 确认含「主力净流入 / 全市场搜索 / ensureDefaultIndicators」等关键字

## Task Dependencies

- Task 3 依赖 Task 1 ✅
- Task 4-6 依赖 Task 2 ✅
- Task 7 独立（复用 v4 spec 已有的方法）✅
- Task 8 独立（前端 demo，不依赖 Vue 源码）✅
- Task 9 依赖 Task 3-7 ✅
- Task 10 依赖 Task 9 ✅
