#!/usr/bin/env python3
"""Copy each skill into _skills/<name>/ and zip to zips/<name>.zip.

Mapping: (output_name, source_repo_dir, source_skill_subpath_or_None)
- If source_skill_subpath is None, the whole repo is treated as the skill
  (used for succ985/akshare which is a top-level SKILL.md).
"""
import shutil
import zipfile
from pathlib import Path

REPOS = Path("/workspace/skills_pack/_repos")
SKILLS = Path("/workspace/skills_pack/_skills")
ZIPS = Path("/workspace/skills_pack/zips")
SKILLS.mkdir(parents=True, exist_ok=True)
ZIPS.mkdir(parents=True, exist_ok=True)

# (output_name, repo_dir, subpath_within_repo or None for whole repo)
JOBS = [
    # #1 历史估值带 (3)
    ("01_company-valuation_himself65",        "finance-skills",   "plugins/market-analysis/skills/company-valuation"),
    ("02_longbridge-value-investing",         "longbridge-skills", "skills/longbridge-value-investing"),
    ("03_longbridge-market-data",             "longbridge-skills", "skills/longbridge-market-data"),
    # #2 业绩预告 (3)
    ("04_earnings-preview_himself65",         "finance-skills",   "plugins/market-analysis/skills/earnings-preview"),
    ("05_longbridge-earnings",                "longbridge-skills", "skills/longbridge-earnings"),
    ("06_earnings-preview_anthropics",        "anthropics-fsp",   "plugins/vertical-plugins/equity-research/skills/earnings-preview"),
    # #3 十大股东+机构持仓 (3)
    ("07_institutional-flow-tracker",         "tradermonty-cts",  "skills/institutional-flow-tracker"),
    ("08_longbridge-watchlist",               "longbridge-skills", "skills/longbridge-watchlist"),
    ("09_longbridge-portfolio",               "longbridge-skills", "skills/longbridge-portfolio"),
    # #4 分析师评级/目标价 (2 - longbridge renamed)
    ("10_longbridge-fundamentals",            "longbridge-skills", "skills/longbridge-fundamentals"),
    ("11_longbridge-research",                "longbridge-skills", "skills/longbridge-research"),
    # #5 行业指数 (3)
    ("12_sector-analyst_tradermonty",         "tradermonty-cts",  "skills/sector-analyst"),
    ("13_longbridge-intel",                   "longbridge-skills", "skills/longbridge-intel"),
    ("14_longbridge-content",                 "longbridge-skills", "skills/longbridge-content"),
    # #7 宏观环境 (3)
    ("15_macro-rates-monitor_anthropics",     "anthropics-fsp",   "plugins/partner-built/lseg/skills/macro-rates-monitor"),
    ("16_fred-macro_gauss314",                "gauss314-skills",   "skills/fred-macro"),
    ("17_macro-calendar_termix",              "termix-cryptoclaw", "skills/macro-calendar"),
    # #8 海外联动 (3)
    ("18_akshare_succ985",                    "succ985-akshare",  None),  # whole repo
    ("19_hk-stock-analysis_nicepkg",          "nicepkg-aw",       "workflows/stock-trader-workflow/.claude/skills/hk-stock-analysis"),
    ("20_us-stock-analysis_tradermonty",      "tradermonty-cts",  "skills/us-stock-analysis"),
    # #9 市场情绪 (3)
    ("21_market-breadth-analyzer",            "tradermonty-cts",  "skills/market-breadth-analyzer"),
    ("22_market-top-detector",                "tradermonty-cts",  "skills/market-top-detector"),
    ("23_market-news-analyst_nicepkg",        "nicepkg-aw",       "workflows/stock-trader-workflow/.claude/skills/market-news-analyst"),
    # #10 大宗商品 (1 - octagonai)
    ("24_commodities-quote_octagonai",        "octagonai-skills", "skills/commodities-quote"),
]

ok, skipped = [], []

for name, repo, sub in JOBS:
    src_base = REPOS / repo
    if not src_base.exists():
        skipped.append((name, f"repo missing: {repo}"))
        continue

    src = src_base / sub if sub else src_base
    if not src.exists():
        skipped.append((name, f"path missing: {src}"))
        continue

    # Verify SKILL.md presence (unless whole repo, which has top-level SKILL.md)
    if sub and not (src / "SKILL.md").exists():
        skipped.append((name, f"no SKILL.md in {src}"))
        continue

    dst = SKILLS / name
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)

    # Zip it (top-level dir inside zip = name)
    zip_path = ZIPS / f"{name}.zip"
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in dst.rglob("*"):
            if p.is_file():
                zf.write(p, arcname=f"{name}/{p.relative_to(dst)}")
    ok.append((name, zip_path.stat().st_size))

print(f"=== SUCCESS ({len(ok)}) ===")
for n, sz in ok:
    print(f"  {n:50s} {sz:>10,} bytes")
print(f"\n=== SKIPPED ({len(skipped)}) ===")
for n, why in skipped:
    print(f"  {n:50s} -> {why}")
print(f"\nTotal zips: {len(ok)}/{len(JOBS)}")
