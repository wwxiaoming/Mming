# Tasks — v4 精简 (已完成)

## Phase 1：环境（10 分钟）

- [x] **Task 1**：Codespace 仓库 + 克隆 Vue 源码
  - [x] SubTask 1.1：`git clone https://github.com/brokermr810/QuantDinger-Vue.git ./QuantDinger-Vue`

## Phase 2：实现（30 分钟）⭐

- [x] **Task 2**：写 `src/charts/indicators/netInflow.js`
  - [x] SubTask 2.1：`registerIndicator('NET_INFLOW', { name, calc, figures, ... })`
  - [x] SubTask 2.2：`calc(dataList) => dataList.map(k => volume * (close - open) / (high - low))`，0 除法 → 0
  - [x] SubTask 2.3：figures: `[{ key: 'net', type: 'bar', baseValue: 0, ... }]`
  - [x] SubTask 2.4：tooltip formatter 输出"X.X亿"

- [x] **Task 3**：改 `KlineChart.vue`
  - [x] SubTask 3.1：顶部 `import '@/charts/indicators/netInflow'`
  - [x] SubTask 3.2：在 `indicatorButtons` 数组加 `{ id: 'NET_INFLOW', name: '主力净流入', shortName: '主力净流入' }`

- [x] **Task 4**：改 `indicator-ide/index.vue`
  - [x] SubTask 4.1：`mounted()` 头部加 `if (this.$i18n) this.$i18n.locale = 'zh-CN'`
  - [x] SubTask 4.2：顶部自选股 Select 加 `show-search`，搜索时调 `searchSymbols` 远程拉
  - [x] SubTask 4.3：搜索请求跨 market：`Promise.allSettled` 并发 4 个市场 (CNStock + USStock + HKStock + Crypto)

## Phase 3：写文档 + 脚本（20 分钟）

- [x] **Task 5**：写 `dev-rebuild.sh`
  - [x] SubTask 5.1：脚本内容 (docker compose -f ... build frontend && up -d frontend)
  - [x] SubTask 5.2：`chmod +x dev-rebuild.sh`

- [x] **Task 6**：写 `REPLACE-GUIDE.md`
  - [x] SubTask 6.1：方法 A — Codespace commit + `./dev-rebuild.sh`（推荐）
  - [x] SubTask 6.2：方法 B — 本地 build dist/ 覆盖挂载
  - [x] SubTask 6.3：方法 C — git format-patch 导出
  - [x] SubTask 6.4：FAQ：白屏 / 回滚 / 环境变量 / 默认密码重置

## Phase 4：验证（10 分钟）

- [x] **Task 7**：检查
  - [x] SubTask 7.1：改动文件 = 2 个 .vue + 1 个新增 JS + 1 个新 MD + 1 个新 sh
  - [x] SubTask 7.2：`grep -n "NET_INFLOW" src/views/indicator-analysis/components/KlineChart.vue` 找到 (line 175, 505)
  - [x] SubTask 7.3：`grep -n "zh-CN" src/views/indicator-ide/index.vue` 找到 (line 2322-2328)
  - [x] SubTask 7.4：本地 `npm run build` 成功 (16.66s) + dist 含 "主力净流入" + "全市场搜索结果"

## Task Dependencies
- Task 2 独立
- Task 3 依赖 Task 2
- Task 4 独立
- Task 5, 6 独立
- Task 7 依赖 Task 3, 4
