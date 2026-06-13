# v1.6 每日选股自动化

> 📅 工作日 07:00 跑(A 股开盘前 2.5 小时,可消化美股隔夜)
> 📊 9 数据策略 + 美股隔夜 + 159941 持仓跟踪 + 4 咨询章节 + 1 图
> 🎯 核心哲学: A 股买"筹码"不是买公司 — 三维信号(资金 0.4 + 情绪 0.3 + 政策 0.3) + 美股隔夜 0.15

## 一键运行

```bash
cd /workspace
./scripts/run_daily.sh
```

或分步:
```bash
python3 scripts/us_market_fetcher.py
python3 scripts/strategy_holdings_tracker.py --code=159941 --shares=700 --cost=1.55
python3 scripts/daily_stock_pick.py --mode=all
python3 scripts/post_report.py
```

## 文件结构

```
/workspace/
├── scripts/
│   ├── _common.py                     # 公共:腾讯/东财/同花顺/news + 限流
│   ├── us_market_fetcher.py           # 美股 5 指数 + 7 巨头 + 半导体 + 中概
│   ├── strategy_holdings_tracker.py   # 159941 持仓跟踪(参数: --shares --cost)
│   ├── daily_stock_pick.py            # 9 策略选股(--mode=1~9 或 all)
│   ├── post_report.py                 # 拼 Markdown 14+1 章节
│   └── run_daily.sh                   # 主调度
└── daily_picks/
    ├── latest.md                       # 最新报告(符号链接外的复制)
    └── YYYY-MM-DD/
        ├── us_market.json              # 美股数据
        ├── 159941-tracker.json         # 持仓快照
        ├── daily_picks.json            # 9 策略结果
        └── YYYY-MM-DD.md               # 最终报告
```

## 9 策略说明

| # | 策略 | 数据源 | 权重维度 | 实现位置 |
|---|---|---|---|---|
| 1 | 当日强势股 TOP 5 | 同花顺热点 reason | 情绪 0.3 | `strategy_1_momentum` |
| 2 | 主力资金净流入 TOP 5 | 东财 push2 120 日 | 资金 0.4 | `strategy_2_fund_flow` |
| 3 | 价值股 TOP 5 | 腾讯 PE/PB | 政策 0.3 | `strategy_3_value` |
| 4 | ETF 折溢价 TOP 5 | 腾讯 ETF 行情 | 流动性 | `strategy_4_etf_premium` |
| 5 | 公告/新闻异动 TOP 5 | 东财 7×24 资讯 | 政策 0.3 | `strategy_5_news` |
| 6 | Serenity 产业链瓶颈 | 同花顺热点 reason 词频 | 方法引擎 | `strategy_6_serenity_chain` |
| 7 | Buffett 护城河 | PE/PB 估算 ROE | 价值 0.4 | `strategy_7_buffett_moat` |
| 8 | 🔮 最佳 5 选 | 三维加权 | 0.4+0.3+0.3+0.15 | `strategy_8_best5` |
| 9 | 🌙 美股隔夜 | 腾讯美股(usNDX 等) | 隔夜 0.15 | `us_market_fetcher` |

## 14+1 报告章节

1️⃣ 当日强势股 TOP 5
2️⃣ 主力资金净流入 TOP 5
3️⃣ 价值股 TOP 5
4️⃣ ETF 折溢价 TOP 5
5️⃣ 公告/新闻异动 TOP 5
6️⃣ Serenity 产业链瓶颈 TOP 5
7️⃣ Buffett 护城河 TOP 5
8️⃣ 🔮 最佳 5 选
9️⃣ 🌙 美股隔夜
🔟 📈 159941 持仓跟踪
1️⃣1️⃣ 行业地位
1️⃣2️⃣ 竞争格局
1️⃣3️⃣ 财务亮点
1️⃣4️⃣ ⚠️ 风险点
📊 对比图
📈 159941 K 线

## 数据源(已实测)

| 数据 | API | 是否封 IP | 频率限制 |
|---|---|---|---|
| 腾讯行情(沪深/美/ETF) | `qt.gtimg.cn` | **不封** | 无 |
| 同花顺热点 | `zx.10jqka.com.cn` | **不封** | 无(73ms 拿全) |
| 东财 7×24 资讯 | `np-weblist.eastmoney.com` | 间歇 | 已加 em_throttle |
| 东财 push2 资金流 | `push2his.eastmoney.com` | 间歇 | 已加 em_throttle(≥1s) |

## 挂 cron

```bash
# 编辑 crontab
crontab -e

# 加一行(工作日 07:00)
0 7 * * 1-5 /workspace/scripts/run_daily.sh >> /workspace/daily_picks/cron.log 2>&1
```

## 调参

修改 `scripts/daily_stock_pick.py` 里的 `WATCH_UNIVERSE` 调整采样股池。
修改 `scripts/strategy_holdings_tracker.py` 的 `--shares=700 --cost=1.55` 改为你的真实持仓。
修改 `run_daily.sh` 的 STEP 2 参数对齐。

## 已知限制

- `ths_hot_reason` 周末/节假日返回空(预期行为,工作日才跑就行)
- 东财 push2 住宅 IP 间歇抽风,代码已加重试;遇空时用腾讯降级
- `strategy_2_fund_flow` 一次最多扫 30 只(防东财封),如需全市场用 `a-share-screener` 替代
- `strategy_4_etf_premium` 是简化版(只用换手率),生产应接东财 etf_iopv 实时折溢价接口
- Buffett 护城河的 ROE 是 PB/PE 估算,正式版应读年报 F10

## 升级到 v2.0 的方向

- 接 `chart-visualization` 生成 PNG 对比图
- 接 `consulting-analysis` 出 50 页研报
- 接 `serenity-stock-choke` 替换 `strategy_6` 的简化版词频
- 接 `data-analysis` 把 daily_picks 沉淀到 SQLite
- 加 `agent-browser` 推送摘要到企业微信/钉钉
