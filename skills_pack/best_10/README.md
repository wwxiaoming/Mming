# A股研究最佳 10 技能包

按"覆盖缺口 + 零依赖 + 独立可跑 + 数据深度 + 安装量"综合评分从 24 个候选中精选而出。
完整对照表见对话历史中"完整版 24 技能包"。

## 安装方式

```bash
# 整包安装（推荐）
unzip top10_bundle.zip -d ~/.claude/skills/

# 或逐个安装
cd zips && for z in *.zip; do unzip -o "$z" -d ~/.claude/skills/; done
```

## 排行

| 排名 | Skill | 评分 | 补缺口 | 关键理由 |
|------|-------|------|--------|----------|
| 1 | `05_longbridge-earnings` | 92 | - | 业绩前瞻+回顾+电话会Q&A+关注要点，美/港/A 三市。需Longbridge |
| 2 | `18_akshare_succ985` | 90 | - | 1.6K安装量，A/H/US/期货/基金/宏观全覆盖。海外联动首选 |
| 3 | `11_longbridge-research` | 88 | - | 机构评级+目标价+一致预期+内部人+财报日历五合一。需Longbridge |
| 4 | `01_company-valuation_himself65` | 85 | - | DCF+相对估值+SOTP三方法齐全，零依赖(Yahoo Finance) |
| 5 | `12_sector-analyst_tradermonty` | 82 | - | 板块轮动+周期定位+CSV无API key |
| 6 | `15_macro-rates-monitor_anthropics` | 80 | - | 收益率曲线+通胀盈亏平衡+掉期利率，专业级宏观面板 |
| 7 | `21_market-breadth-analyzer` | 78 | - | 0-100量化广度健康分，6分项组成，零依赖CSV |
| 8 | `24_commodities-quote_octagonai` | 76 | - | 贵金属/能源/农产品实时报价+均线对比 |
| 9 | `22_market-top-detector` | 74 | - | O'Neil+Minervini+Monty三方法检测见顶，2-8周择时 |
| 10 | `07_institutional-flow-tracker` | 72 | - | 13F跟踪smart money异动(美股为主) |

## 依赖说明

- **零依赖（开箱即用）**：`01_company-valuation_himself65`、`12_sector-analyst_tradermonty`、`21_market-breadth-analyzer`、`22_market-top-detector`、`24_commodities-quote_octagonai`
- **仅需 Yahoo Finance / CSV（零成本）**：`01`、`04`
- **需 Longbridge 账号**：`05_longbridge-earnings`、`11_longbridge-research`
- **需 Python 库**：`18_akshare`（pip install akshare）
- **需 MCP**：`24_commodities-quote_octagonai`（Octagon MCP）

## 覆盖面

- 行情 + 估值：#1 DCF/SOTP
- 业绩：#2 财报前瞻+回顾
- 资金/机构：#7 13F 跟踪
- 评级：#3 分析师目标价
- 行业：#5 板块轮动
- 宏观：#6 利率曲线
- 海外：#4 akshare
- 情绪：#8/#9 广度+见顶
- 商品：#10 大宗报价

---

## ⚡ A 股增强包（6 个 A 股替代）

> 6 个 best_10 中的 skill（#4/#5/#6/#7/#9/#10）是美股向工具。本包精选 1 对 1 A 股替代。

| # | A 股 Skill | 替代 | 用途 |
|---|-----------|------|------|
| A01 | `a-share-analysis` | #4 | A 股估值（DCF/同业/SOTP，T+1/涨跌停/北向） |
| A02 | `sector-rotation-detector` | #5 | 申万/中证板块轮动 |
| A03 | `china-macro-analyst` | #6 | 中国 GDP/CPI/PPI/PMI/社融/LPR |
| A04 | `limit-up-pool-analyzer` | #7 | 涨停池+连板梯队+炸板率+广度分 |
| A05 | `equity-pledge-risk-monitor` | #9 | 股权质押+平仓线+见顶预警 |
| A06 | `fund-screener` | #10 | 公募基金筛选+smart money |

**总包**：[`ashare_bundle.zip`](ashare_bundle.zip) (76.5 KB)
**详细文档**：[`ASHARE_README.md`](ASHARE_README.md)
**独立 zip**：[`zips_ashare/`](zips_ashare/) 6 个

```bash
# 整包安装
unzip ashare_bundle.zip -d ~/.claude/skills/
```
