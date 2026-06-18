#!/usr/bin/env python3
"""Comprehensive fix: restore from _repos/ and re-translate with proper handling.

The previous scripts had a bug with multi-line folded scalars (`>`): they only
matched the first indented line, leaving trailing lines as orphan content.

This script:
  1. Restores each skill from _repos/ to a clean state
  2. Translates the WHOLE description (multi-line `|` and `>`) into a single
     Chinese string
  3. Writes `description: "..."` (single-line quoted) for max parser compat
"""
import re
import shutil
import zipfile
from pathlib import Path

# Paths
REPOS = Path("/workspace/skills_pack/_repos")
SKILLS = Path("/workspace/skills_pack/_skills")
ZIPS = Path("/workspace/skills_pack/zips")

# Skill mapping (must match pick_top10.py / restore.py)
JOBS = [
    ('01_company-valuation_himself65',        'finance-skills',   'plugins/market-analysis/skills/company-valuation'),
    ('02_longbridge-value-investing',         'longbridge-skills', 'skills/longbridge-value-investing'),
    ('03_longbridge-market-data',             'longbridge-skills', 'skills/longbridge-market-data'),
    ('04_earnings-preview_himself65',         'finance-skills',   'plugins/market-analysis/skills/earnings-preview'),
    ('05_longbridge-earnings',                'longbridge-skills', 'skills/longbridge-earnings'),
    ('06_earnings-preview_anthropics',        'anthropics-fsp',   'plugins/vertical-plugins/equity-research/skills/earnings-preview'),
    ('07_institutional-flow-tracker',         'tradermonty-cts',  'skills/institutional-flow-tracker'),
    ('08_longbridge-watchlist',               'longbridge-skills', 'skills/longbridge-watchlist'),
    ('09_longbridge-portfolio',               'longbridge-skills', 'skills/longbridge-portfolio'),
    ('10_longbridge-fundamentals',            'longbridge-skills', 'skills/longbridge-fundamentals'),
    ('11_longbridge-research',                'longbridge-skills', 'skills/longbridge-research'),
    ('12_sector-analyst_tradermonty',         'tradermonty-cts',  'skills/sector-analyst'),
    ('13_longbridge-intel',                   'longbridge-skills', 'skills/longbridge-intel'),
    ('14_longbridge-content',                 'longbridge-skills', 'skills/longbridge-content'),
    ('15_macro-rates-monitor_anthropics',     'anthropics-fsp',   'plugins/partner-built/lseg/skills/macro-rates-monitor'),
    ('16_fred-macro_gauss314',                'gauss314-skills',   'skills/fred-macro'),
    ('17_macro-calendar_termix',              'termix-cryptoclaw', 'skills/macro-calendar'),
    ('18_akshare_succ985',                    'succ985-akshare',  None),
    ('19_hk-stock-analysis_nicepkg',          'nicepkg-aw',       'workflows/stock-trader-workflow/.claude/skills/hk-stock-analysis'),
    ('20_us-stock-analysis_tradermonty',      'tradermonty-cts',  'skills/us-stock-analysis'),
    ('21_market-breadth-analyzer',            'tradermonty-cts',  'skills/market-breadth-analyzer'),
    ('22_market-top-detector',                'tradermonty-cts',  'skills/market-top-detector'),
    ('23_market-news-analyst_nicepkg',        'nicepkg-aw',       'workflows/stock-trader-workflow/.claude/skills/market-news-analyst'),
    ('24_commodities-quote_octagonai',        'octagonai-skills', 'skills/commodities-quote'),
]

# Chinese translations
TRANSLATIONS = {
    "01_company-valuation_himself65":
        "用 DCF、相对估值（同行倍数）和 SOTP（分部加总）三种方法估算上市公司的内在价值，综合得到隐含股价并对比当前市价计算上行/下行空间。适用场景：用户问'AAPL 值多少'、'NVDA 估值'、'TSLA 公允价值'、'MSFT DCF'、'建个 DCF'、'折现现金流'、'WACC'、'终值'、'隐含股价'、'相对公允的上行空间'、'X 是否高估/低估'、'相对估值'、'同业对比估值'、'EV/EBITDA 目标'、'SOTP'、'分部加总'、'这公司值多少钱'、'基本面驱动的目标价'，或任何在计算内在/相对估值语境下的股票代码。默认同时运行三种方法（DCF + 相对 + SOTP-如适用），输出混合隐含价 + 敏感性表。不要凭记忆回答估值问题——始终运行完整工作流。",
    "02_longbridge-value-investing":
        "价值投资分析，基于格雷厄姆（NCAV/净流动资产/防御型投资者）与巴菲特（经济护城河/ROE/FCF）方法论。覆盖单股诊断与批量筛选，兼容格雷厄姆烟蒂与巴菲特优质复利两类标准，评分前先做跨报表对账。数据源优先 Longbridge CLI，失败回退 MCP，仍有缺口时方用 WebSearch。触发词：格雷厄姆、巴菲特、捡烟蒂、烟蒂股、NCAV、净流动资产、护城河、价值投资、安全边际、深度价值、Graham、Buffett、cigar butt、net-net、NCAV screen、moat、value investing、margin of safety、deep value、quality compounder。",
    "03_longbridge-market-data":
        "实时行情、K线、盘口、逐笔成交、盘中资金流、市场情绪温度、交易时段、证券列表、汇率、IPO 日历（港/美/A/新），基于 Longbridge。也覆盖 ADR 溢价与外汇套息框架。触发词：股价、行情、K线、走势、盘口、资金流、市场温度、汇率、IPO、打新、隔夜股、ADR溢价、外汇套息、现在多少钱、stock price、quote、kline、chart、depth、orderbook、capital flow、market sentiment、exchange rate、IPO calendar、security list、ADR premium、fx carry、market open、trading hours、开市、溢价。",
    "04_earnings-preview_himself65":
        "用 Yahoo Finance 数据为任意股票生成财报前简报。用户想为即将发布的财报做准备、了解分析师预期、回顾公司 beat/miss 记录，或在业绩电话会前快速概览时使用。触发词：AAPL 财报前瞻、TSLA 财报预期什么、MSFT 下周披露、earnings preview、pre-earnings analysis、NVDA 分析师预期、earnings estimates、GOOGL 能否 beat 预期、beat/miss 历史、upcoming earnings、before earnings、earnings setup、consensus estimates、earnings whisper、EPS expectations、what's the street expecting、earnings season preview，或任何涉及财报前预期梳理的请求。",
    "05_longbridge-earnings":
        "财报分析——业绩前瞻 + 业绩回顾。前瞻：复盘上季度指引、追踪近期事件、梳理上次电话会 Q&A，并给出本期'关注要点'框架。回顾分两层：快速聊天摘要卡（默认）与完整 Markdown 研究报告（按需生成）。覆盖 beat/miss、分部、利润率、指引、预测、估值，适用美/港/A 股。响应语言匹配用户输入（简中/繁中/英文）。触发词：earnings update、quarterly results、Q1/Q2/Q3/Q4 results、earnings report、post-earnings analysis、beat/miss、guidance update、earnings preview、pre-earnings、what to watch this earnings、before earnings、财报分析、业绩更新、季度业绩、季报、年报、盈利分析、财报点评、财报前瞻、业绩前瞻、财报预览。",
    "06_earnings-preview_anthropics":
        "构建财报前分析：估值模型、情景框架、关键观察指标。在公司季报披露前用于：准备头寸备忘、搭建多/空情景、识别股价驱动因素。触发词：earnings preview、what to watch for [公司] earnings、pre-earnings、earnings setup、preview Q[X] for [公司]。",
    "07_institutional-flow-tracker":
        "用 13F 申报数据跟踪机构投资者持仓变化与组合资金流。分析对冲基金、共同基金及其他机构持有人，识别出现显著 smart money 累积或派发的股票。跟随老练投资者的资金部署方向，可在重大行情前发现先机。",
    "08_longbridge-watchlist":
        "自选股分组管理（列/创建/重命名/删除/添加/移除标的）、价格提醒（列/添加/删除）、社区股票清单（sharelist：列/详情/创建/删除/管理），通过 Longbridge。变更操作需用户明确确认（dry-run 协议）。触发词：自选股、添加自选、删除自选、创建分组、价格提醒、股票清单、watchlist、add to watchlist、create group、rename group、price alert、sharelist、community list。",
    "09_longbridge-portfolio":
        "账户资产、股票/基金持仓、盈亏、现金流记录、对账单、保证金率、购买力估算、订单管理、定投（DCA），通过 Longbridge（多数需 Trade 权限）。框架：组合诊断、再平衡、资产配置、风险分析（VaR/CVaR）、绩效归因、税损收割。触发词：持仓、账户、盈亏、资产、对账单、下单、买入、卖出、撤单、定投、组合诊断、再平衡、资产配置、风险分析、绩效归因、税损收割、positions、portfolio、P&L、order、buy、sell、DCA、statement。",
    "10_longbridge-fundamentals":
        "财务报表、业务分部、分红、估值倍数（PE/PB/PS）、行业对比、经营数据、公司行为、公司与高管资料、跨股对比、估值排名，通过 Longbridge。另含 DCF 模型、价值投资筛选（低 PE/PB、安全边际）、行为金融分析框架。触发词：财报、三表、利润表、资产负债、现金流、估值、PE、PB、分红、公司信息、高管、行业估值、并购、DCF、内在价值、低估值、安全边际、行为金融、financial report、income statement、balance sheet、valuation、dividend、DCF、value screen、behavioral finance。",
    "11_longbridge-research":
        "机构评级、一致目标价、EPS/营收预测、财报日历、股东数据、基金持仓、内部人交易（SEC Form 4）、空头持仓、行业排名、同业组分析，通过 Longbridge。框架：投资提案、首次覆盖、股票研究、竞争分析、财务规划、DeFi/链上分析。触发词：机构评级、目标价、一致预期、EPS预测、内部人交易、空头、行业排名、投资提案、首次覆盖、竞争格局、财务规划、DeFi收益、链上数据、analyst rating、price target、consensus、insider trades、short interest、coverage initiation、DeFi yield、on-chain、财报日历、FOMC、非农。",
    "12_sector-analyst_tradermonty":
        "用于分析板块轮动模式与市场周期定位。从 CSV 抓取板块上涨趋势数据（无需 API key），可选接收图表作为辅助分析。触发词：板块轮动分析、周期 vs 防御评估、超买/超卖识别、市场周期阶段判断。所有分析与输出以中文呈现。",
    "13_longbridge-intel":
        "市场情报：策略筛选器、热度排行、异动+新闻关联、行情异常、指数/ETF 成分股、早晨简报、自选股催化剂监控、事件驱动策略、ETF 资金流、板块轮动、市场微观结构、产业链分析、行业概览、ARK 式颠覆式创新分析。触发词：筛选、策略筛选、排行、热度、异动、成分股、晨报、早报、催化剂、事件驱动、ETF资金流、板块轮动、产业链、行业概览、ARK、颠覆式创新、screener、rank、anomaly、constituent、morning brief、catalyst、event strategy、ETF flow、sector rotation、supply chain。",
    "14_longbridge-content":
        "最新新闻文章、监管申报、上市公司社区讨论话题、SEC EDGAR 申报分析（10-K/10-Q/8-K/委托书/Form 4），通过 Longbridge。触发词：新闻、公告、资讯、话题、社区讨论、SEC、10-K、10-Q、8-K、Form 4、news、filing、announcement、community、SEC filing、annual report、quarterly report、proxy、insider filing、监管规则、涨跌停、T+1、熔断、circuit breaker、保证金。",
    "15_macro-rates-monitor_anthropics":
        "构建宏观经济与利率仪表盘：综合宏观指标、收益率曲线、通胀盈亏平衡、掉期利率。用于监控宏观环境、分析收益率曲线形态、拆分实际 vs 名义利率、评估政策利率预期、判断金融条件。",
    "16_fred-macro_gauss314":
        "美联储免费 API (FRED)：840K+ 宏观数据序列（GDP、CPI、利率、就业、M2、VIX、美债）。",
    "17_macro-calendar_termix":
        "跟踪影响加密货币的宏观经济事件、美联储利率、CPI、经济指标。",
    "18_akshare_succ985":
        "通过 AkShare 库获取中文金融数据。提供 A 股、港股、美股、期货、基金的实时与历史数据，及宏观经济指标。当用户请求中国市场数据、股价、市场分析或中国交易所金融信息时使用。支持股票行情、历史数据、期货行情、基金信息、宏观指标、实时市场动态。",
    "19_hk-stock-analysis_nicepkg":
        "全面的港股分析，覆盖 H 股、红筹、本地港股、AH 折溢价、互联互通资金流向，以及港股特征（T+0、无涨跌幅限制、做空机制）。当用户询问'港股分析'、香港上市股票、H 股，或需要考虑港股特性的分析时使用。",
    "20_us-stock-analysis_tradermonty":
        "全面的美股分析：基本面（财务指标、商业质量、估值）、技术面（指标、形态、支撑/阻力）、股票对比、投资报告生成。当用户要求分析美股代码（如'分析 AAPL'、'TSLA 对比 NVDA'、'给我一份微软的报告'），或评估美股财务指标、图表技术分析、投资建议时使用。",
    "21_market-breadth-analyzer":
        "用 TraderMonty 公开 CSV 数据量化市场广度健康度。生成 0-100 综合分（100=健康），6 个分项组成，无需 API key。当用户询问市场广度、参与率、涨跌家数健康度、行情是否普涨，或一般市场健康评估时使用。",
    "22_market-top-detector":
        "用 O'Neil Distribution Days、Minervini Leading Stock Deterioration、Monty Defensive Sector Rotation 三种方法检测市场见顶概率。生成 0-100 综合分 + 风险区分类。当用户询问市场见顶风险、分发日、防御板块轮动、龙头股恶化、是否减仓时使用。专注 2-8 周战术择时信号，针对 10-20% 调整。",
    "23_market-news-analyst_nicepkg":
        "用于分析近期市场驱动新闻事件及其对股市与大宗商品的影响。当用户请求分析过去 10 天重大财经新闻、想理解市场对货币政策（FOMC、ECB、BOJ）的反应、评估地缘事件对大宗商品影响、或需全面回顾大盘股业绩公告时使用。自动通过 WebSearch/WebFetch 收集新闻并产出按影响力排序的分析报告。所有分析思考与输出以中文呈现。",
    "24_commodities-quote_octagonai":
        "通过 Octagon MCP 实时获取大宗商品行情报价。用于查询当前大宗商品价格、分析日内区间、与均线对比、跟踪贵金属、能源、农产品价格。",
}


def escape_yaml_quoted(s: str) -> str:
    """Escape a string for use inside YAML double-quoted scalar."""
    s = s.replace('\\', '\\\\').replace('"', '\\"')
    return s


# Match either:
#  - description: | or description: > (block scalar with multiple indented lines)
#  - description: "..." (quoted single line)
#  - description: bare (unquoted single line)
# Greedy matching for block scalars to capture ALL indented lines.
BLOCK_RE = re.compile(
    r'(^|\n)description:\s*[|>][+-]?\s*\n((?:[ \t]+[^\n]*\n?)+)',
    re.MULTILINE
)
QUOTED_RE = re.compile(r'(^|\n)description:\s*"([^"]*)"\s*$', re.MULTILINE | re.DOTALL)
BARE_RE = re.compile(r'(^|\n)description:\s*(.+?)\s*$', re.MULTILINE)

FM_RE = re.compile(r'^---\n(.*)\n---\n(.*)$', re.DOTALL)


def replace_description(content: str, new_desc: str) -> str:
    """Replace the description with a single-line quoted string, robustly handling all formats."""
    m = FM_RE.match(content)
    if not m:
        raise RuntimeError("No YAML frontmatter found")
    fm, body = m.group(1), m.group(2)

    quoted = f'description: "{escape_yaml_quoted(new_desc)}"'

    # Try block scalar first (| or >)
    new_fm, n = BLOCK_RE.subn(lambda _: '\n' + quoted + '\n', fm, count=1)
    if n:
        return '---\n' + new_fm + '\n---\n' + body

    # Try quoted single line
    new_fm, n = QUOTED_RE.subn(lambda _: '\n' + quoted + '\n', fm, count=1)
    if n:
        return '---\n' + new_fm + '\n---\n' + body

    # Try bare single line
    new_fm, n = BARE_RE.subn(lambda _: '\n' + quoted + '\n', fm, count=1)
    if n:
        return '---\n' + new_fm + '\n---\n' + body

    raise RuntimeError("description field not found")


# Step 1: Restore from _repos/
print("=== Step 1: Restore from _repos/ ===")
for name, repo, sub in JOBS:
    src = REPOS / repo / sub if sub else REPOS / repo
    dst = SKILLS / name
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
print(f"  Restored {len(JOBS)} skills\n")

# Step 2: Replace descriptions
print("=== Step 2: Replace descriptions (robust, single-line quoted) ===")
ok, errors = [], []
for name, repo, sub in JOBS:
    skill_md = SKILLS / name / "SKILL.md"
    if not skill_md.exists():
        errors.append((name, "SKILL.md not found"))
        continue
    original = skill_md.read_text(encoding="utf-8")
    try:
        updated = replace_description(original, TRANSLATIONS[name])
    except Exception as e:
        errors.append((name, f"replace failed: {e}"))
        continue
    if updated == original:
        errors.append((name, "no change applied"))
        continue
    skill_md.write_text(updated, encoding="utf-8")
    ok.append(name)
print(f"  Replaced {len(ok)}/{len(JOBS)} descriptions")
for n, why in errors:
    print(f"  ! {n}: {why}")

# Step 3: Re-zip
print("\n=== Step 3: Re-zip ===")
zipped = 0
for name, repo, sub in JOBS:
    skill_dir = SKILLS / name
    zip_path = ZIPS / f"{name}.zip"
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in skill_dir.rglob("*"):
            if p.is_file():
                zf.write(p, arcname=f"{name}/{p.relative_to(skill_dir)}")
    zipped += 1
print(f"  Created {zipped} zips")
