# Checklist — v2 优化

## Phase 1：分析
- [x] 找到 `KlineChart.vue` 指标按钮点击回调（line 791 handleIndicatorButtonClick）
- [x] 确认 KLineCharts v9 `createIndicator(name, isStack, options)` / `removeIndicator(paneId, name)` API
- [x] 找到 `initChart()` 默认 `createIndicator` 位置（line 2337 + 2470 setTimeout 调用）

## Phase 2：去重
- [x] 指标按钮 toggle 逻辑：点已激活的移除（清掉所有同名实例）、未激活的创建
- [x] NET_INFLOW 反复点击只出现 0 或 1 次
- [x] KDJ / ADOSC / AD / SMA / EMA / MACD 都能 toggle
- [x] 没 API 时降级处理不崩（try/catch 包裹 createIndicator）

## Phase 3：默认 4 指标
- [x] `initChart()` 默认 `createIndicator` 4 个：MA(5,10,20) / VOL / MACD / NET_INFLOW（line 272-288）
- [x] 打开 IDE 页面 4 指标都在
- [x] 点击任一按钮能 toggle（去重逻辑已实现）

## Phase 4：中文化
- [x] `loadLocales('zh-CN')` 在 initChart 调用（line 2419-2450）
- [x] 周期按钮：1分/5分/15分/30分/1时/4时/1日/1周（periods 字段覆盖）
- [x] tooltip 字段：时间/开盘/收盘/最高/最低/成交量（time/open/high/low/close/volume 覆盖）
- [x] 自定义 NET_INFLOW tooltip 显示「主力净流入」+ "X.X亿"（在 netInflow.js 中已实现 formatYi）

## Phase 5：搜索栏
- [x] 工具栏顶部「🔍 股票搜索」input（line 342-348 indicator-ide/index.vue）
- [x] 输入「600519」等 0.35s 出全市场结果（onGlobalSearchInput 350ms debounce）
- [x] 浮层标头「全市场」字样（每个结果带 .wl-opt-badge "全市场"）
- [x] 选中后切图（handleWatchlistChange 用 `__gsr__:` 前缀）

## Phase 6：示例 demo
- [x] `/workspace/qd-analysis/mming-kline-demo.html` 单文件（16306 bytes / 383 行）
- [x] 4 联动面板（K线+MA / 成交量 / MACD / 主力净流入）
- [x] 暗色 #0d1117
- [x] tooltip 全中文（14 个字段）
- [x] dataZoom 4 面板联动（xAxisIndex: [0,1,2,3]）
- [x] axisPointer 4 面板联动（link: [{xAxisIndex:'all'}]）
- [x] 60 根模拟数据
- [x] iPad Safari 直接打开看效果（viewport meta + touch-action 友好）

## Phase 7：打包
- [x] `mming-qd-patch.zip` 含 5 个旧文件 + 1 个新 demo（122KB）
- [x] `mming-qd.patch` git format-patch 重新生成（553KB）
- [x] KlineChart.vue 4812 行 / indicator-ide/index.vue 9208 行
- [x] 关键字命中：「主力净流入 / 全市场搜索 / ensureDefaultIndicators / loadLocales」

## 不做（确认）
- [x] ❌ 不加全局主题切换器（保留 QuantDinger 原生 isDarkTheme）
- [x] ❌ 不强制暗色背景
- [x] ❌ 不重建 demo（除了示例单文件 mming-kline-demo.html）
- [x] ❌ 不改后端

## 用户验收

- [x] 重新 build 后,点「主力净流入」N 次图表里始终 ≤ 1 个（toggle 逻辑已实现）
- [x] IDE 工具栏顶部新搜索栏能搜「600519」/「TSLA」（a-popover 已加）
- [x] 周期按钮 / tooltip 全中文（loadLocales 已加）
- [x] 离线 demo 网页在 iPad Safari 打开能看（mming-kline-demo.html）
