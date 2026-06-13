# 📦 v1.6.1 stock-trader 上传 Git 指南

## 一、本次更新(v1.6 → v1.6.1)

| 改动点 | 旧 | 新 |
|--------|-----|-----|
| 159941 成本价 | 1.55(占位) | **1.623**(真实平均成本,2026-06-09 早上买入) |
| 美股隔夜权重 | 0.15 | **0.10** |
| 资金面权重 | 0.40 | **0.40**(不变,主菜) |
| 情绪面权重 | 0.30 | **0.30**(不变) |
| 政策面权重 | 0.30 | **0.20** |
| 报告输出 | 14 章节排名 | **只输出明日预测 TOP 3** |
| 策略 8 输出数量 | TOP 5 | **TOP 3** |
| 报告文件大小 | ~30 KB | **2.2 KB** |

## 二、文件清单(11 个核心文件)

```
v1.6-stock-trader/
├── scripts/
│   ├── _common.py                              # 公共:腾讯/东财/同花顺/news + 限流
│   ├── us_market_fetcher.py                    # 美股 5 指数 + 7 巨头 + 半导体 + 中概
│   ├── strategy_holdings_tracker.py            # 159941 持仓跟踪
│   ├── daily_stock_pick.py                     # 9 策略并行(策略 8 输出 TOP 3)
│   ├── post_report.py                          # 拼 Markdown 报告(极简 4 章节)
│   ├── auto_publish.py                         # 6 通道自动写出
│   ├── run_daily.sh                            # 主调度(集成 5 个步骤)
│   └── README.md                               # 使用说明
├── STOCK_CONTEXT.md                            # 上下文(自动更新)
├── POSITIONS.md                                # 持仓表(自动更新)
├── DAILY_LOG.md                                # 日志(自动追加)
└── GIT_PUSH.md                                 # 本文件
```

## 三、Git 操作步骤

```bash
# 1. 解压
cd /workspace
unzip v1.6-stock-trader.zip

# 2. 进 git 仓库
cd /path/to/your-git-repo
cp -r /workspace/v1.6-stock-trader/* .

# 3. 提交
git add scripts/ STOCK_CONTEXT.md POSITIONS.md DAILY_LOG.md
git commit -m "v1.6.1: 成本价 1.623 + 美股权重 0.10 + 报告精简到 TOP 3"

# 4. 推送
git push origin main
```

## 四、Trae IDE 调度任务

- **任务 ID**: `8HBXYCBRO9_Y55`
- **频率**: `0 7 * * 1-5`(工作日 07:00)
- **时区**: `Asia/Shanghai`

## 五、验证方式

```bash
cd /workspace
bash scripts/run_daily.sh          # 跑一次验证
cat daily_picks/latest.md          # 看最新报告
cat POSITIONS.md                   # 看持仓
cat DAILY_LOG.md                   # 看日志
```

## 六、报告样例(2026-06-13)

```
# 📊 每日选股报告 — 2026-06-13

### 🎯 明日预测 TOP 3(资金 0.40 + 情绪 0.30 + 政策 0.20 + 美股 0.10)

| # | 代码 | 名称 | 现价 | 涨跌% | **总分** |
|---|------|------|------|-------|----------|
| 1 | 300118 | 东方日升 | 13.43 | +3.15 | **0.789** |
| 2 | 000661 | 长春高新 | 66.50 | +3.39 | **0.711** |
| 3 | 601688 | 华泰证券 | 19.97 | +3.53 | **0.669** |

### 📈 159941 持仓
- 现价 1.598 (+1.40%)
- 700股 × 成本 1.623
- 当日 +15.40 元  累计 -17.50 元 (-1.54%) 🔴
```
