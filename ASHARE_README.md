# A 股增强包（6 个 Skill）

> 对应 best_10 中 6 个美股 skill 的 A 股替代
> 版本：v1.0 / 2026-06-13
> 总包：[`ashare_bundle.zip`](ashare_bundle.zip) (76.5 KB)

## 为什么需要这个包？

`best_10/` 中的 6 个 skill（#4/#5/#6/#7/#9/#10）是美股向工具（yfinance 美股 / S&P 500 / SEC 13F / LSEG 美债），用于 A 股研究时受限：

| 局限 | 表现 |
|------|------|
| 数据源是美股 | A 股代码无法直接用，需找 A/H/US 三市版本 |
| 指标是美股概念 | 涨跌停、T+1、北向、申万/中证等 A 股特色无覆盖 |
| 风险指标错位 | 美股用 Put/Call + VIX，A 股用涨停/炸板率/股权质押 |

**A 股增强包**对每个美股 skill 精选 1 个 A 股原生替代，6 个均独立可装。

## 一对一对应对照

| # | A 股 Skill | 替代的 best_10 # | 用途 | 安装量 | 来源 |
|---|-----------|----------------|------|-------|------|
| A01 | `a-share-analysis` | 04 `company-valuation` | A 股估值分析（DCF/同业/SOTP，含 T+1、涨跌停、北向） | 123 | nicepkg/ai-workflow |
| A02 | `sector-rotation-detector` | 05 `sector-analyst` | 申万/中证板块轮动检测 | 33 | yuping322/finskills |
| A03 | `china-macro-analyst` | 06 `macro-rates-monitor` | 中国 GDP/CPI/PPI/PMI/社融/LPR | 79 | nicepkg/ai-workflow |
| A04 | `limit-up-pool-analyzer` | 07 `market-breadth-analyzer` | 涨停池+连板梯队+炸板率+市场广度 | 85 | yuping322/finskills |
| A05 | `equity-pledge-risk-monitor` | 09 `market-top-detector` | 股权质押比例+平仓线+见顶预警 | 24 | yuping322/finskills |
| A06 | `fund-screener` | 10 `institutional-flow-tracker` | 公募基金筛选+smart money 异动 | 193 | sososun/mutual-fund-skills |

**总社区安装量**：123 + 33 + 79 + 85 + 24 + 193 = **537**

## 安装

```bash
# 方式 A：整包一键安装（推荐）
unzip /workspace/skills_pack/best_10/ashare_bundle.zip -d ~/.claude/skills/

# 方式 B：单独安装
cd /workspace/skills_pack/best_10/zips_ashare
for z in *.zip; do unzip -o "$z" -d ~/.claude/skills/; done

# 方式 C：只装某一个
unzip /workspace/skills_pack/best_10/zips_ashare/A04_limit-up-pool-analyzer.zip -d ~/.claude/skills/
```

## 与 best_10 的取舍建议

| 你的研究目标 | 用 best_10 还是本包 |
|------------|------------------|
| **A 股为主**（沪深主板/创业板/科创板/北交所） | ✅ **本包**（A 股原生） |
| **H 股 / 美股 / 全球联动** | 用 best_10 中港美向 skill（longbridge-*/akshare/commodities-quote） |
| **A+H+US 三市对照** | 并用：宏观走 china-macro + 估值走 a-share-analysis + 财报走 longbridge-earnings |
| **A 股短线打板/题材** | 本包 A04 涨停池 + A02 板块轮动 |
| **A 股机构资金/公募调仓** | 本包 A06 fund-screener |

## 6 个 Skill 速查

### A01 — `a-share-analysis`（A 股综合分析）
- 替代 `04_company-valuation`
- 覆盖：基本面 + 技术面 + 政策影响 + T+1/涨跌停/北向
- 来源：[nicepkg/ai-workflow](https://skills.sh/nicepkg/ai-workflow/a-share-analysis)
- 触发词：A股、个股分析、policy impact、northbound capital、T+1 trading、price limits

### A02 — `sector-rotation-detector`（A 股板块轮动检测）
- 替代 `05_12_sector-analyst_tradermonty`
- 覆盖：申万/中证/中信一级 31 + 二级 134 行业
- 来源：[yuping322/finskills](https://skills.sh/yuping322/finskills/sector-rotation-detector)
- 触发词：sector rotation、industry rotation、A股板块、申万、中证、轮动策略

### A03 — `china-macro-analyst`（中国宏观分析）
- 替代 `06_15_macro-rates-monitor_anthropics`
- 覆盖：GDP / CPI / PPI / PMI / 社融 / M2 / LPR / 10Y 国债
- 来源：[nicepkg/ai-workflow](https://skills.sh/nicepkg/ai-workflow/china-macro-analyst)
- 触发词：China macro、PBOC、央行政策、CPI、PPI、社融、降息、降准

### A04 — `limit-up-pool-analyzer`（A 股涨停池与连板）
- 替代 `07_21_market-breadth-analyzer`
- 覆盖：涨停家数、连板高度、炸板率、封板资金、市场广度 0-100 分
- 来源：[yuping322/finskills](https://skills.sh/yuping322/finskills/limit-up-pool-analyzer)
- 触发词：limit-up、连板、涨停板、炸板率、市场情绪、情绪温度

### A05 — `equity-pledge-risk-monitor`（A 股股权质押风险）
- 替代 `09_22_market-top-detector`
- 覆盖：质押比例、平仓线距离、控股股东质押率、见顶/踩踏风险
- 来源：[yuping322/finskills](https://skills.sh/yuping322/finskills/equity-pledge-risk-monitor)
- 触发词：equity pledge、股权质押、平仓线、闪崩预警

### A06 — `fund-screener`（公募基金筛选与持仓）
- 替代 `10_07_institutional-flow-tracker`
- 覆盖：5000+ 公募基金、基金经理、十大重仓股、行业配置
- 来源：[sososun/mutual-fund-skills](https://skills.sh/sososun/mutual-fund-skills/fund-screener)
- 触发词：mutual fund、fund screener、公募基金、smart money、QFII、社保

## 验证

- 6/6 description 通过 `yaml.safe_load` 严格解析
- 6/6 description 通过简单 frontmatter 正则解析
- 6/6 无遗留的 `|` block scalar 字符
- 中文 107-146 字 / 条，英文触发词全部保留

## 文件结构

```
best_10/
├── zips_ashare/                       # 6 个独立 zip
│   ├── A01_a-share-analysis.zip
│   ├── A02_sector-rotation-detector.zip
│   ├── A03_china-macro-analyst.zip
│   ├── A04_limit-up-pool-analyzer.zip
│   ├── A05_equity-pledge-risk-monitor.zip
│   └── A06_fund-screener.zip
├── ashare_bundle.zip                  # 总包 76.5 KB
├── ASHARE_README.md                   # 本文档
└── ...

../_skills_ashare/                     # 解压后的源（开发参考）
├── A01_a-share-analysis/
├── A02_sector-rotation-detector/
├── A03_china-macro-analyst/
├── A04_limit-up-pool-analyzer/
├── A05_equity-pledge-risk-monitor/
└── A06_fund-screener/

../_repos/                             # 源仓库（shallow clone）
├── yuping322-finskills/               # 含 50+ China-market skill
├── sososun-mutual-fund/               # 单 skill
└── nicepkg-aw/                        # 已有
```

## 后续扩展方向

- 港股 A 股联动可加 `longbridge-northbound-flow`（551 installs）
- 链上数据可加 `yuping322/finskills@hsgt-holdings-monitor` / `industry-chain-mapper`
- 政策可加 `policy-sensitivity-brief`
- 衍生品可加 `options-strategy-advisor`（nicepkg）

## 版本

- v1.0 / 2026-06-13 — 6 个 A 股替代初版
