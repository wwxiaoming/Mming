# 我的 K 线优化需求 — 3 个改过的文件

## 文件清单

1. **01-netInflow.js** — 主力净流入自定义指标
   - 路径：src/charts/indicators/netInflow.js
   - 公式：volume * (close - open) / (high - low) （0 除法保护）
   - 注册名：NET_INFLOW

2. **02-KlineChart.vue** — 核心 K 线图组件（3 处改动）
   - 路径：src/views/indicator-analysis/components/KlineChart.vue
   - 改动 A: handleIndicatorButtonClick 加 toggle 去重（line ~773）
   - 改动 B: initChart 加 loadLocales('zh-CN') 中文化（line ~2419）
   - 改动 C: ensureDefaultIndicators 默认激活 4 指标（MA / VOL / MACD / NET_INFLOW）

3. **03-indicator-ide-index.vue** — 指标 IDE 主页面
   - 路径：src/views/indicator-ide/index.vue
   - 改动: 工具栏顶部 watchlist 旁边加全市场搜索栏（line ~315-350）

## 部署位置

把上面 3 个文件覆盖到 QuantDinger-Vue 仓库对应路径：

```
QuantDinger-Vue/
├── src/
│   ├── charts/indicators/
│   │   └── netInflow.js          ← 01
│   └── views/
│       ├── indicator-analysis/components/
│       │   └── KlineChart.vue    ← 02
│       └── indicator-ide/
│           └── index.vue         ← 03
```

## 离线 demo（验证用）

demo HTML 不需要上面 3 个文件，单文件就能跑：
- /workspace/qd-analysis/mming-kline-demo.html
- /workspace/deliver-full/demo/mming-kline-demo.html

iPad Safari 直接 file:// 打开，看 4 联动面板效果。

## 验证清单

改完后看：
- [ ] 反复点「主力净流入」按钮 → 不会叠加
- [ ] 工具栏顶部有 🔍 全市场搜索 600519 / TSLA 输入框
- [ ] K 线区默认就有 4 面板：K线+MA / 成交量 / MACD / 主力净流入
- [ ] 鼠标悬停 K 线 → tooltip 显示「时间/开盘/收盘/最高/最低/成交量」中文
- [ ] 周期按钮显示「1分/5分/1时/1日/1周」中文
