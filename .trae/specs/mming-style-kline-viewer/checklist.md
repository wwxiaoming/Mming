# Checklist — v4 精简 (已完成)

## 现状确认
- [x] 已读 `src/views/indicator-ide/index.vue` (9083 行)
- [x] 已读 `src/views/indicator-analysis/components/KlineChart.vue` (4736 行)
- [x] 已确认 `isDarkTheme` 主题切换已存在
- [x] 已确认 vue-i18n 已存在，defaultLang='en-US'
- [x] 已确认 `searchSymbols()` API 已存在

## 改动
- [x] `src/charts/indicators/netInflow.js` 新增 (71 行)
  - [x] `registerIndicator('NET_INFLOW', ...)` 调用
  - [x] calc 公式：volume * (close - open) / (high - low)
  - [x] 0 除法返回 0
  - [x] baseValue: 0 柱状图
  - [x] tooltip 格式化"X.X亿"
- [x] `KlineChart.vue` 修改 (line 175, 505)
  - [x] 顶部 import netInflow
  - [x] indicatorButtons 加 NET_INFLOW
- [x] `indicator-ide/index.vue` 修改
  - [x] mounted() 设 i18n.locale = 'zh-CN' (line 2322-2328)
  - [x] 顶部 Select show-search + searchSymbols (line 269, 5117-5184)
  - [x] 数据：globalSearchResults / globalSearching / globalSearchTimer (line 1655-1657)
  - [x] 方法：onGlobalSearchInput / doGlobalSearch / isInGlobalResults / handleWatchlistChange 加 __gsr__: 前缀处理

## 部署
- [x] `dev-rebuild.sh` 存在且可执行 (1165 字节)
- [x] `REPLACE-GUIDE.md` 存在含 3 种方法 + 10 个 FAQ (5539 字节)

## 验证
- [x] `npm run build` 成功 (16.66s)
- [x] dist 包含 "主力净流入" (line 主力净流入: ✓ built)
- [x] dist 包含 "全市场搜索结果" (line 全市场搜索结果: ✓ built)
- [x] netInflow.js 语法检查通过 (node -c)
- [x] KlineChart.vue grep 找到 NET_INFLOW @ 175, 505
- [x] indicator-ide/index.vue grep 找到 zh-CN @ 2322-2328

## 不做（确认）
- ❌ 不改背景色
- ❌ 不加主题切换器（已存在）
- ❌ 不新建组件（复用现有）
- ❌ 不新建 demo 页面
- ❌ 不改 KLineCharts 默认样式
