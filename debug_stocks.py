# -*- coding: utf-8 -*-
"""
A股尾盘候选池筛选 - 2026-06-23
8步标准筛选 + 抗跌筛选（大盘跌-1.76%） - 调试版
"""
import requests
import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta
import time
import warnings
warnings.filterwarnings('ignore')

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://quote.eastmoney.com/',
    'Accept': '*/*',
}

print("=" * 80)
print("  候选股技术面逐项校验")
print("=" * 80)

def clean_code(c):
    c = str(c)
    for p in ['sh', 'sz', 'bj']:
        if c.startswith(p):
            return c[2:]
    return c

def get_daily_kline(code_raw, days=80):
    if code_raw.startswith(('6', '9')):
        secid = f'1.{code_raw}'
    elif code_raw.startswith(('0', '3', '2')):
        secid = f'0.{code_raw}'
    else:
        secid = f'0.{code_raw}'

    start_date = (datetime(2026, 6, 23) - timedelta(days=days*2)).strftime('%Y%m%d')
    kline_url = 'https://push2his.eastmoney.com/api/qt/stock/kline/get'
    params = {
        'secid': secid,
        'ut': 'fa5fd1943c7b386f172d6893dbfba10b',
        'fields1': 'f1,f2,f3,f4,f5,f6',
        'fields2': 'f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61',
        'klt': 101, 'fqt': 1, 'beg': start_date, 'end': '20260623',
    }
    try:
        r = requests.get(kline_url, params=params, headers=HEADERS, timeout=10)
        if r.status_code == 200 and r.text:
            data = r.json()
            if data.get('data') and data['data'].get('klines'):
                klines = []
                for line in data['data']['klines']:
                    parts = line.split(',')
                    if len(parts) >= 11:
                        klines.append({
                            '日期': parts[0], '开盘': float(parts[1]),
                            '收盘': float(parts[2]), '最高': float(parts[3]),
                            '最低': float(parts[4]), '成交量': float(parts[5]),
                            '成交额': float(parts[6]), '振幅': float(parts[7]),
                            '涨跌幅': float(parts[8]), '涨跌额': float(parts[9]),
                            '换手率': float(parts[10]),
                        })
                return pd.DataFrame(klines)
    except Exception as e:
        print(f'    K线请求失败: {e}')
    return None

def get_minute_kline(code_raw):
    if code_raw.startswith(('6', '9')):
        secid = f'1.{code_raw}'
    elif code_raw.startswith(('0', '3', '2')):
        secid = f'0.{code_raw}'
    else:
        secid = f'0.{code_raw}'

    minute_url = 'https://push2his.eastmoney.com/api/qt/stock/trends2/get'
    params = {
        'secid': secid,
        'ut': 'fa5fd1943c7b386f172d6893dbfba10b',
        'fields1': 'f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13',
        'fields2': 'f51,f52,f53,f54,f55,f56,f57,f58',
        'iscr': 0, 'ndays': 1,
    }
    try:
        r = requests.get(minute_url, params=params, headers=HEADERS, timeout=10)
        if r.status_code == 200 and r.text:
            data = r.json()
            if data.get('data') and data['data'].get('trends'):
                trends = data['data']['trends']
                rows = []
                for t in trends:
                    parts = t.split(',')
                    if len(parts) >= 8:
                        rows.append({
                            '时间': parts[0], '开盘': float(parts[1]),
                            '收盘': float(parts[2]), '最高': float(parts[3]),
                            '最低': float(parts[4]), '成交量': float(parts[5]),
                            '成交额': float(parts[6]), '均价': float(parts[7]),
                        })
                return pd.DataFrame(rows)
    except Exception as e:
        print(f'    分时请求失败: {e}')
    return None

# 5只基础候选
candidates_data = [
    ('sh603341', '龙旗科技', 4.34, 1.72, 5.62, 102.4),
    ('sz002546', '新联电子', 3.66, 3.78, 7.98, 61.2),
    ('sz002312', '川发龙蟒', 3.46, 3.21, 5.63, 180.5),
    ('sz301053', '远信工业', 3.36, 2.37, 6.03, 53.5),
    ('sh605178', '时空科技', 3.35, 1.72, 5.14, 72.1),
]

for code_full, name, pct, vr, to, mcap in candidates_data:
    code_raw = clean_code(code_full)
    print(f"\n--- {code_full} {name} (涨幅{pct}%, 量比{vr}, 换手{to}%, 流通{mcap}亿) ---")

    # 获取日K
    hist = get_daily_kline(code_raw, days=80)
    if hist is None or len(hist) < 25:
        print(f"  K线数据不足 ({len(hist) if hist is not None else 0}行)")
        continue
    print(f"  K线: {len(hist)}行, 最新日期: {hist['日期'].iloc[-1]}")
    hist = hist.sort_values('日期').reset_index(drop=True)

    # 均线
    closes = hist['收盘'].astype(float)
    ma5 = closes.rolling(5).mean()
    ma10 = closes.rolling(10).mean()
    ma20 = closes.rolling(20).mean()
    ma5_l, ma10_l, ma20_l = ma5.iloc[-1], ma10.iloc[-1], ma20.iloc[-1]
    ma5_p, ma10_p, ma20_p = ma5.iloc[-2], ma10.iloc[-2], ma20.iloc[-2]
    print(f"  均线: MA5={ma5_l:.2f}({ma5_p:.2f}) MA10={ma10_l:.2f}({ma10_p:.2f}) MA20={ma20_l:.2f}({ma20_p:.2f})")
    ma_bullish = (ma5_l > ma10_l > ma20_l) and (ma5_l > ma5_p) and (ma10_l > ma10_p) and (ma20_l > ma20_p)
    print(f"  5>10>20: {ma5_l > ma10_l > ma20_l} | 三线向上: {ma5_l > ma5_p} {ma10_l > ma10_p} {ma20_l > ma20_p}")
    print(f"  ✓ 多头排列: {ma_bullish}")

    # 涨停
    last_20 = hist.tail(20)
    limit_ups = (last_20['涨跌幅'] >= 9.5).sum()
    print(f"  20日内涨停: {limit_ups}次, 涨停日: {last_20[last_20['涨跌幅']>=9.5]['日期'].tolist()}")
    if limit_ups == 0:
        print("  ✗ 20日无涨停 → 失败")

    # 量能
    volumes = hist['成交量'].astype(float).tail(5).values
    print(f"  5日量: {volumes.tolist()}")
    volumes_3d = volumes[-3:]
    vol_inc_3d = all(volumes_3d[i] < volumes_3d[i+1] for i in range(2))
    vol_ratio = volumes[-1] / volumes[0] if volumes[0] > 0 else 0
    print(f"  3日递增: {vol_inc_3d} | 5日量比: {vol_ratio:.2f}")
    if not (vol_inc_3d and 1.15 <= vol_ratio <= 4.0):
        print("  ✗ 量能不达标 → 失败")

    # 分时
    minute = get_minute_kline(code_raw)
    if minute is None or len(minute) < 30:
        print(f"  分时数据不足")
        continue
    above_avg = (minute['收盘'] > minute['均价']).sum() / len(minute)
    print(f"  分时数据: {len(minute)}条, 站均价线: {above_avg*100:.1f}%")
    if above_avg < 0.70:
        print("  ✗ 分时站均线<70% → 失败")

    print(f"  >>> 综合: {'通过' if (ma_bullish and limit_ups>=1 and vol_inc_3d and 1.15<=vol_ratio<=4.0 and above_avg>=0.70) else '不通过'} <<<")
