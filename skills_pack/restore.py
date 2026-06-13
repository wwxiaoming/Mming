#!/usr/bin/env python3
"""Restore all 24 skills from _repos/ to _skills/ (clean state)."""
import shutil
from pathlib import Path

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

repos = Path('/workspace/skills_pack/_repos')
skills = Path('/workspace/skills_pack/_skills')
skills.mkdir(parents=True, exist_ok=True)

for name, repo, sub in JOBS:
    src = repos / repo / sub if sub else repos / repo
    dst = skills / name
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
print(f'Restored {len(JOBS)} skills')
