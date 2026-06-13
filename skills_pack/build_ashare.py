#!/usr/bin/env python3
"""
build_ashare.py — 6 个 A 股 skill 的抽取+翻译+打包
对标 best_10 中 6 个美股 skill，输出独立的 A 股增强包。
"""
import os
import re
import shutil
import zipfile
import yaml

# ============== 路径配置 ==============
REPOS = '/workspace/skills_pack/_repos'
SKILLS_RAW = '/workspace/skills_pack/_skills_ashare'
ZIPS_OUT = '/workspace/skills_pack/best_10/zips_ashare'
BUNDLE = '/workspace/skills_pack/best_10/ashare_bundle.zip'

# ============== 6 个目标 ==============
# (源目录, 目标名, 替代的 best_10 #, 中文 description)
TARGETS = [
    (
        f'{REPOS}/nicepkg-aw/workflows/stock-trader-workflow/.claude/skills/a-share-analysis',
        'A01_a-share-analysis',
        '04_company-valuation',
        "A 股综合分析工具，涵盖基本面、技术面、政策影响评估及中国市场特有特征（T+1 交易、涨跌停、北向资金）。适用 A 股个股深度分析、上海/深圳上市股票、中国市场特性研究。触发词：A 股、个股分析、policy impact、northbound capital、T+1 trading、price limits、Chinese A-shares、上海/深圳/沪深、上海证券交易所、深圳证券交易所、A股估值、A股财报、A股分析、A股行情、A股研报。",
    ),
    (
        f'{REPOS}/yuping322-finskills/China-market/sector-rotation-detector',
        'A02_sector-rotation-detector',
        '05_12_sector-analyst_tradermonty',
        "A 股板块轮动检测器，跟踪申万/中证/中信行业指数的相对强弱与资金流向，识别周期 vs 防御的轮动信号。覆盖一级行业 31 个 + 二级行业 134 个，输出行业 ROE、毛利率、估值分位与北向资金持仓变化。适用：板块轮动、行业配置、申万行业、中证指数、行业比较、防御/周期判断、轮动策略。触发词：sector rotation、industry rotation、A股板块、申万、中证、行业轮动、板块强弱、周期股、防御股、行业配置。",
    ),
    (
        f'{REPOS}/nicepkg-aw/workflows/stock-trader-workflow/.claude/skills/china-macro-analyst',
        'A03_china-macro-analyst',
        '06_15_macro-rates-monitor_anthropics',
        "中国宏观经济与货币政策分析，跟踪 GDP、CPI、PPI、PMI、社融、M2、十年期国债收益率、央行公开市场操作。评估货币政策与财政政策对 A 股和港股市场的影响，解读政策信号与利率敏感型板块（金融/地产/公用事业）。适用：中国宏观、央行政策、货币政策、财政政策、利率、LPR、MLF、社融、宏观数据解读。触发词：China macro、PBOC、央行、货币政策、CPI、PPI、PMI、GDP、social financing、中国宏观经济、中国央行、降息、降准、LPR。",
    ),
    (
        f'{REPOS}/yuping322-finskills/China-market/limit-up-pool-analyzer',
        'A04_limit-up-pool-analyzer',
        '07_21_market-breadth-analyzer',
        "A 股涨停板池与连板梯队分析，跟踪每日涨停家数、连板高度（一板/二板/三板/高位板）、炸板率、封板资金、涨停题材归因。计算 A 股市场广度健康度，输出 0-100 综合分（涨跌停比、连板梯队、炸板率、封板率、新高新低比）。适用：涨停分析、连板梯队、炸板率、涨停打板、市场情绪、情绪温度、短线温度。触发词：limit-up、连板、涨停板、炸板率、封板率、涨停家数、连板高度、市场广度、短线情绪、情绪周期。",
    ),
    (
        f'{REPOS}/yuping322-finskills/China-market/equity-pledge-risk-monitor',
        'A05_equity-pledge-risk-monitor',
        '09_22_market-top-detector',
        "A 股股权质押风险监控，跟踪全市场质押比例、控股股东质押率、平仓线/警戒线距离、质押市值与日均成交额比。识别高质押率个股（>50%）、质押股触及平仓线的预警，输出 0-100 见顶/踩踏风险分。参考 2018 年 A 股闪崩与股权质押危机的历史经验。适用：股权质押、质押风险、平仓风险、控股股东质押、闪崩预警、见顶检测、踩踏预警。触发词：equity pledge、股权质押、质押比例、平仓线、警戒线、爆仓、闪崩、A股风险。",
    ),
    (
        f'{REPOS}/sososun-mutual-fund',
        'A06_fund-screener',
        '10_07_institutional-flow-tracker',
        "公募基金筛选与持仓分析，跟踪基金经理持仓变化、十大重仓股、行业配置、规模/收益/夏普等指标。识别机构资金（公募/QFII/社保/北向）显著加仓或减仓的股票，输出 smart money 信号。覆盖 5000+ 公募基金、200+ 基金经理。适用：公募基金、基金筛选、smart money、机构持仓、十大重仓股、基金经理、QFII、社保基金、北向资金。触发词：mutual fund、fund screener、公募基金、基金筛选、机构持仓、smart money、机构资金、北向资金、QFII、社保基金。",
    ),
]

# ============== 翻译函数（复用 fix_robust.py 思路） ==============
# Use lookbehind so the leading newline isn't consumed
BLOCK_RE = re.compile(
    r'(?<=\n)description:\s*[|>][+-]?\s*\n((?:[ \t]+[^\n]*\n?)+)',
    re.MULTILINE
)
QUOTED_RE = re.compile(r'(?<=\n)description:\s*"([^"]*)"\s*$', re.MULTILINE | re.DOTALL)
BARE_RE = re.compile(r'(?<=\n)description:\s*(.+?)\s*$', re.MULTILINE)
FM_RE = re.compile(r'^---\n(.*)\n---\n(.*)$', re.DOTALL)

def escape_yaml_quoted(s: str) -> str:
    return s.replace('\\', '\\\\').replace('"', '\\"')

def replace_description(content: str, new_desc: str) -> str:
    m = FM_RE.match(content)
    if not m:
        return content
    fm, body = m.group(1), m.group(2)
    quoted = f'description: "{escape_yaml_quoted(new_desc)}"'
    # Try block scalar first, then quoted, then bare
    for pat in (BLOCK_RE, QUOTED_RE, BARE_RE):
        new_fm, n = pat.subn(lambda _m, _q=quoted: _q, fm, count=1)
        if n:
            return "---\n" + new_fm + "\n---\n" + body
    # No description line at all: insert it
    if fm.strip().endswith(':'):
        new_fm = fm.rstrip() + '\n' + quoted
    else:
        new_fm = quoted + '\n' + fm
    return "---\n" + new_fm + "\n---\n" + body

# ============== 验证函数 ==============
def verify_yaml(content: str):
    m = FM_RE.match(content)
    if not m:
        return False, "no frontmatter"
    try:
        data = yaml.safe_load(m.group(1))
        d = data.get('description', '')
        if not d or '|' in d[:3]:
            return False, f"bad desc: {d[:50]}"
        return True, d
    except Exception as e:
        return False, str(e)

# ============== 主流程 ==============
def main():
    # Clean
    if os.path.exists(SKILLS_RAW):
        shutil.rmtree(SKILLS_RAW)
    if os.path.exists(ZIPS_OUT):
        shutil.rmtree(ZIPS_OUT)
    os.makedirs(SKILLS_RAW)
    os.makedirs(ZIPS_OUT)

    results = []
    for src, target, replaces, zh_desc in TARGETS:
        if not os.path.exists(src):
            print(f"❌ SOURCE MISSING: {src}")
            continue
        # Copy tree
        dst = os.path.join(SKILLS_RAW, target)
        shutil.copytree(src, dst, ignore=shutil.ignore_patterns('.git', '__pycache__', 'node_modules'))
        # Replace description in SKILL.md
        skill_md = os.path.join(dst, 'SKILL.md')
        if not os.path.exists(skill_md):
            # search recursively
            for root, _, files in os.walk(dst):
                if 'SKILL.md' in files:
                    skill_md = os.path.join(root, 'SKILL.md')
                    break
        with open(skill_md, 'r', encoding='utf-8') as f:
            content = f.read()
        new_content = replace_description(content, zh_desc)
        with open(skill_md, 'w', encoding='utf-8') as f:
            f.write(new_content)
        # Verify
        ok, info = verify_yaml(new_content)
        cn = sum(1 for c in (info if ok else '') if '\u4e00' <= c <= '\u9fff')
        # Zip
        zip_path = os.path.join(ZIPS_OUT, f"{target}.zip")
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for root, _, files in os.walk(dst):
                for fn in files:
                    fp = os.path.join(root, fn)
                    arc = os.path.relpath(fp, SKILLS_RAW)
                    zf.write(fp, arc)
        size_kb = os.path.getsize(zip_path) / 1024
        results.append((target, replaces, ok, info, cn, size_kb))
        print(f"{'✅' if ok else '❌'} {target}  ({cn} Chinese, {size_kb:.1f}KB)  replaces {replaces}")

    # Total bundle
    with zipfile.ZipFile(BUNDLE, 'w', zipfile.ZIP_DEFLATED) as bundle:
        for zf in sorted(os.listdir(ZIPS_OUT)):
            if zf.endswith('.zip'):
                bundle.write(os.path.join(ZIPS_OUT, zf), zf)
    print(f"\n📦 Total bundle: {BUNDLE}  ({os.path.getsize(BUNDLE)/1024:.1f} KB)")
    print(f"   {sum(1 for r in results if r[2])}/{len(results)} skills verified OK")

if __name__ == '__main__':
    main()
