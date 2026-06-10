# 股票分析技能系统安装指南（10 技能对标版）

> 整理时间：2026-06-10
> 状态：✅ 全部安装完成
> 安装位置：`~/.claude/skills/`

---

## 一、整体架构

本系统由 **3 个引擎** + **64 个技能模块** + **9 个 Agent** 组成，可对标任意"10 模块化"股票研究系统。

```
┌──────────────────────────────────────────────────────────────┐
│                    DUAL-ANALYSIS 调度层                       │
│            （a-stock-data ⇄ Serenity 双引擎）                  │
└──────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌──────────────┐    ┌──────────────────┐    ┌──────────────────┐
│ 数据引擎     │    │ 方法引擎         │    │ 风险引擎         │
│ a-stock-data │    │ Serenity 系列   │    │ backtest/risk    │
│ + akshare    │    │ 5 个视角        │    │ bubble detector  │
└──────────────┘    └──────────────────┘    └──────────────────┘
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────────────────────────────────────────────────────┐
│              业务技能层（10 大模块，已全部覆盖）                │
│ ① 政策  ② 个股  ③ 复盘  ④ 量化  ⑤ 监控                       │
│ ⑥ 数据  ⑦ 研报  ⑧ 风控  ⑨ 回测  ⑩ 审计                       │
└──────────────────────────────────────────────────────────────┘
```

---

## 二、10 个标准技能模块 vs 已安装方案

| # | 技能模块 | 已安装替代 | 仓库 | 匹配度 | 路径 |
|---|---|---|---|---|---|
| 1 | **Policy-Monitor** 政策监控 | `china-macro-analyst` | nicepkg | ⭐⭐⭐⭐⭐ | `~/.claude/skills/china-macro-analyst/` |
| 2 | **Stock-Analyst** 股票分析 | `a-share-analysis` + `us-stock-analysis` | nicepkg | ⭐⭐⭐⭐⭐ | `~/.claude/skills/a-share-analysis/` |
| 3 | **Daily-Trade-Review** 每日复盘 | `market-news-analyst` + `market-environment-analysis` | nicepkg | ⭐⭐⭐⭐ | `~/.claude/skills/market-news-analyst/` |
| 4 | **Quant-KB** 量化知识库 | `backtest-expert` + `backtesting-frameworks` | nicepkg + wshobson | ⭐⭐⭐⭐⭐ | `~/.claude/skills/backtest-expert/` |
| 5 | **Stock-Watcher** 自选监控 | `portfolio-manager` + `cross-border-flow-tracker` | nicepkg | ⭐⭐⭐⭐ | `~/.claude/skills/portfolio-manager/` |
| 6 | **A-Shares-Data** 股数据源 | `a-stock-data`（原装）+ `akshare` | 系统 + nicepkg | ⭐⭐⭐⭐⭐ | `~/.claude/skills/a-stock-data/` |
| 7 | **Report-Extractor** 研报提取 | 需自建（`pdfplumber`+`akshare` 财报） | 自组装 | ⭐⭐⭐ | 见 §五 |
| 8 | **Risk-Alert-System** 风险预警 | `us-market-bubble-detector` + `risk-metrics-calculation` | nicepkg + wshobson | ⭐⭐⭐⭐⭐ | `~/.claude/skills/us-market-bubble-detector/` |
| 9 | **Backtest-Engine** 回测引擎 | `backtest-expert` + `backtesting-frameworks` | nicepkg + wshobson | ⭐⭐⭐⭐⭐ | `~/.claude/skills/backtest-expert/` |
| 10 | **Skill-Vetter** 安全审计 | `plugin-eval/evaluation-methodology` | wshobson | ⭐⭐⭐⭐ | `~/.claude/skills/plugin-eval/` |

---

## 三、详细安装清单

### 3.1 来自 nicepkg/ai-workflow（主力）

| 技能 | 说明 |
|---|---|
| `a-share-analysis` | A 股个股综合分析（基本面+技术面+估值）|
| `a-share-screener` | A 股筛股（PE/PB/ROE/资金流）|
| `akshare` | A 股数据源（akshare 库）|
| `backtest-expert` | 系统性回测（含过拟合防范）|
| `breadth-chart-analyst` | 美股市场宽度图分析 |
| `canslim-screener` | CANSLIM 成长股筛选（美股）|
| `china-macro-analyst` | 中国宏观 / 央行政策 / 经济数据 |
| `cross-border-flow-tracker` | 北向资金（沪深港通）|
| `dividend-growth-pullback-screener` | 红利回撤策略 |
| `earnings-calendar` | 美股财报日历 |
| `economic-calendar-fetcher` | FOMC/央行经济日历 |
| `hk-stock-analysis` | 港股个股分析 |
| `institutional-flow-tracker` | 13F 机构持仓 |
| `market-environment-analysis` | 市场环境综合分析 |
| `market-news-analyst` | 市场新闻影响分析 |
| `options-strategy-advisor` | 期权策略 |
| `pair-trade-screener` | 配对交易（统计套利）|
| `portfolio-manager` | 组合管理（Alpaca 集成）|
| `scenario-analyzer` | 情景分析（黑天鹅）|
| `sector-analyst` | 板块轮动 |
| `stock-screener` | 美股通用筛股器 |
| `technical-analyst` | 技术分析（周线图）|
| `us-market-bubble-detector` | 美股泡沫 / 风险预警（Minsky-Kindleberger v2.1）|
| `us-stock-analysis` | 美股个股分析 |
| `value-dividend-screener` | 价值红利股 |
| `weekly-trade-strategy` | 周度交易策略（含 5 个 Agent）|
| `stanley-druckenmiller-investment` | 德鲁肯米勒投资法 |
| `股票分析`（中文）| LongPort 自选 + AkShare 数据 |

### 3.2 来自 wshobson/agents（量化补充）

```
~/.claude/skills/quantitative-trading/
├── skills/
│   ├── backtesting-frameworks/    # 回测框架
│   └── risk-metrics-calculation/  # 风险指标（VaR/CVaR/Sharpe）
└── agents/
    ├── quant-analyst.md           # 量化分析师
    └── risk-manager.md            # 风险管理师
```

### 3.3 来自 wshobson/agents（安全审计）

```
~/.claude/skills/plugin-eval/
├── skills/evaluation-methodology/ # 技能评估方法论
├── agents/
│   ├── eval-orchestrator.md       # 评估协调
│   └── eval-judge.md              # 评估判断
└── commands/                      # /eval /certify 斜杠命令
```

### 3.4 来自 serenity 生态（方法引擎）

| 技能 | 来源 | 作用 |
|---|---|---|
| `serenity-skill`（主）| 系统已装 | 供应链瓶颈猎手（核心方法论）|
| `follow-aleabito` | aleabito-serenity-skills | 跟踪 @aleabitoreddit 实时推文 |
| `serenity-method` | aleabito-serenity-skills | Serenity 选股方法论 |
| `serenity-radar` | aleabito-serenity-skills | Serenity 注意力雷达 |

### 3.5 来自系统（数据引擎）

- `a-stock-data` —— A 股全栈数据（行情/研报/资金/新闻/公告/基础数据）—— 7 层架构

---

## 四、快速使用

### 4.1 触发词（auto-activate）

| 你说 | 自动激活 |
|---|---|
| "查一下 688017 的估值" | `a-stock-data` + `a-share-analysis` |
| "用 Serenity 的方式看 半导体" | `serenity-skill` + `china-macro-analyst` |
| "159941 今晚怎么看" | `a-stock-data` + `market-news-analyst` |
| "159941 回测一下" | `backtest-expert` + `a-stock-data` |
| "美股有泡沫吗" | `us-market-bubble-detector` + `market-news-analyst` |
| "我的持仓有什么风险" | `portfolio-manager` + `risk-metrics-calculation` |
| "拉一下 600519 的研报" | `a-stock-data`（研报层）+ `a-share-analysis` |

### 4.2 双重分析（Dual Analysis）

**Serenity 视角（质性）** + **a-stock-data 视角（量化）** = 双重验证

详见 [DUAL-ANALYSIS.md](./DUAL-ANALYSIS.md)

---

## 五、自建：Report-Extractor（研报提取）

`Report-Extractor` 在 nicepkg 仓库里没有完全等价的，需要自组装。建议方案：

```python
# ~/.claude/skills/report-extractor/scripts/extract.py
import pdfplumber
import re

def extract_pdf_report(pdf_path: str) -> dict:
    """PDF 研报 → 结构化文本"""
    with pdfplumber.open(pdf_path) as pdf:
        text = "\n".join([p.extract_text() or "" for p in pdf.pages])
    
    return {
        "title": re.search(r"^.{5,80}报告", text, re.MULTILINE).group(0) if re.search(...) else "",
        "rating": re.findall(r"(买入|增持|中性|减持|卖出)", text),
        "target_price": re.findall(r"目标价[^\d]*(\d+\.?\d*)", text),
        "eps_forecast": re.findall(r"EPS[^\d]*(\d+\.?\d*)", text),
        "key_points": extract_key_points(text),  # 用 LLM 提炼
        "raw_text": text,
    }
```

依赖：`pip install pdfplumber openai`

或者用 `a-stock-data` 的研报层（已内置）：
- `eastmoney_reports(code)` - 拉研报列表
- `download_pdf(record, dir)` - 下载 PDF
- 然后自写 PDF 解析即可

---

## 六、维护 & 升级

```bash
# 升级到最新版本
cd /tmp/ai-workflow && git pull
cp -r workflows/stock-trader-workflow/.claude/skills/* ~/.claude/skills/

cd /tmp/agents && git pull
cp -r plugins/quantitative-trading/. ~/.claude/skills/quantitative-trading/
cp -r plugins/plugin-eval/. ~/.claude/skills/plugin-eval/

# 查看安装情况
ls ~/.claude/skills/ | wc -l
find ~/.claude/skills -name "SKILL.md" | wc -l
```

---

## 七、API Key 配置

| 需要的 Key | 用途 | 申请 |
|---|---|---|
| `IWENCAI_API_KEY` | iwencai NL 语义搜索 | https://www.iwencai.com/skillhub |
| `FMP_API_KEY` | 财报日历、CANSLIM、红利 | https://financialmodelingprep.com/ |
| `ALPACA_API_KEY` | 美股实盘组合 | https://alpaca.markets/ |
| `OPENAI_API_KEY` | LLM 提炼（如做 Report-Extractor）| https://openai.com/ |
| `LONG_PORT_TOKEN` | 港股自选股 | https://open.longportapp.com/ |

设置：
```bash
export IWENCAI_API_KEY="..."
export FMP_API_KEY="..."
# 写入 ~/.bashrc 持久化
```

---

## 八、对应原 GitHub 仓库

| 仓库 | URL | 用途 |
|---|---|---|
| nicepkg/ai-workflow | https://github.com/nicepkg/ai-workflow | 主力 stock-trader-workflow（29 技能）|
| wshobson/agents | https://github.com/wshobson/agents | 量化交易 + 安全审计 |
| muxuuu/serenity-skill | https://github.com/muxuuu/serenity-skill | 主 Serenity 框架 |
| lanfuli/aleabito-serenity-skills | https://github.com/lanfuli/aleabito-serenity-skills | 3 个 Serenity 视角技能 |
| fadewalk/serenity-stock-choke | https://github.com/fadewalk/serenity-stock-choke | Serenity 选股应用 |
| simonlin1212/a-stock-data | https://github.com/simonlin1212/a-stock-data | A 股数据源 |

---

**下一步**：阅读 [SERENITY.md](./SERENITY.md) 了解 Serenity 框架原理，以及 [DUAL-ANALYSIS.md](./DUAL-ANALYSIS.md) 学习双重分析方法。
