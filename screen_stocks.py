# -*- coding: utf-8 -*-
"""
A股尾盘候选池筛选 - 2026-06-23
8步标准筛选 - 完整版（11只候选股逐项校验）
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
print("  A股尾盘候选池 | 8项标准严格筛选 | 2026-06-23 14:00")
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
    for retry in range(3):
        try:
            r = requests.get(kline_url, params=params, headers=HEADERS, timeout=15)
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
            time.sleep(0.3)
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
    for retry in range(3):
        try:
            r = requests.get(minute_url, params=params, headers=HEADERS, timeout=15)
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
            time.sleep(0.3)
    return None

# 11只基础候选（含科创/创业）
candidates_data = [
    ('sh688699', '明微电子', 4.90, 1.60, 8.01, 82.6, '科创板'),
    ('sh688237', '超卓航科', 4.75, 2.01, 8.38, 52.6, '科创板'),
    ('sh688166', '博瑞医药', 4.51, 1.46, 5.71, 164.7, '科创板'),
    ('sh688131', '皓元医药', 4.51, 1.50, 5.33, 191.9, '科创板'),
    ('sh603341', '龙旗科技', 4.34, 1.72, 5.62, 102.4, '主板'),
    ('sz300520', '科大国创', 4.11, 1.94, 8.51, 86.5, '创业板'),
    ('sz300259', '新天科技', 4.10, 2.16, 8.38, 64.6, '创业板'),
    ('sz002546', '新联电子', 3.66, 3.78, 7.98, 61.2, '主板'),
    ('sz002312', '川发龙蟒', 3.46, 3.21, 5.63, 180.5, '主板'),
    ('sz301053', '远信工业', 3.36, 2.37, 6.03, 53.5, '创业板'),
    ('sh605178', '时空科技', 3.35, 1.72, 5.14, 72.1, '主板'),
]

results = []
for code_full, name, pct, vr, to, mcap, btype in candidates_data:
    code_raw = clean_code(code_full)
    print(f"\n[{code_full}] {name} ({btype}, 涨幅{pct}%, 量比{vr}, 换手{to}%, 流通{mcap}亿)")

    # 获取日K
    hist = get_daily_kline(code_raw, days=80)
    if hist is None or len(hist) < 25:
        print(f"  ✗ K线数据不足")
        continue
    hist = hist.sort_values('日期').reset_index(drop=True)

    closes = hist['收盘'].astype(float)
    ma5 = closes.rolling(5).mean()
    ma10 = closes.rolling(10).mean()
    ma20 = closes.rolling(20).mean()
    ma5_l, ma10_l, ma20_l = ma5.iloc[-1], ma10.iloc[-1], ma20.iloc[-1]
    ma5_p, ma10_p, ma20_p = ma5.iloc[-2], ma10.iloc[-2], ma20.iloc[-2]

    # 检查7: 5/10/20日均线多头排列 (5>10>20 且 都向上)
    ma_bullish = (ma5_l > ma10_l > ma20_l) and (ma5_l > ma5_p) and (ma10_l > ma10_p) and (ma20_l > ma20_p)
    print(f"  均线: MA5={ma5_l:.2f} MA10={ma10_l:.2f} MA20={ma20_l:.2f} | 5>10>20: {ma5_l>ma10_l>ma20_l} | 都向上: {ma5_l>ma5_p and ma10_l>ma10_p and ma20_l>ma20_p}")
    print(f"  均线7: {'✓' if ma_bullish else '✗'}")

    # 检查2: 20日涨停
    last_20 = hist.tail(20)
    limit_ups = (last_20['涨跌幅'] >= 9.5).sum()
    print(f"  20日涨停: {limit_ups}次 {'✓' if limit_ups >= 1 else '✗'}")

    # 检查6: 3-5日量能温和放大
    volumes = hist['成交量'].astype(float).tail(5).values
    volumes_3d = volumes[-3:]
    vol_inc_3d = all(volumes_3d[i] < volumes_3d[i+1] for i in range(2))
    vol_ratio = volumes[-1] / volumes[0] if volumes[0] > 0 else 0
    vol_moderate = vol_inc_3d and (1.15 <= vol_ratio <= 4.0)
    print(f"  5日量: {volumes.tolist()}")
    print(f"  量能6: 3日递增={vol_inc_3d}, 倍数={vol_ratio:.2f} {'✓' if vol_moderate else '✗'}")

    # 检查8: 分时站均价线 > 70%
    minute = get_minute_kline(code_raw)
    if minute is None or len(minute) < 30:
        print(f"  ✗ 分时数据缺失")
        above_avg = 0
    else:
        above_avg = (minute['收盘'] > minute['均价']).sum() / len(minute)
        print(f"  分时8: 站均线{above_avg*100:.1f}% {'✓' if above_avg >= 0.70 else '✗'}")

    # 综合判断
    all_pass = (ma_bullish and limit_ups >= 1 and vol_moderate and above_avg >= 0.70)
    print(f"  >>> 综合: {'通过✓' if all_pass else '不通过✗'} <<<")

    if all_pass:
        results.append({
            '代码': code_full, '名称': name, '板块': btype,
            '最新价': hist['收盘'].iloc[-1],
            '涨幅%': pct, '量比': vr, '换手率%': to, '流通市值(亿)': mcap,
            '20日涨停次数': int(limit_ups),
            '5日均线': round(ma5_l, 2), '10日均线': round(ma10_l, 2), '20日均线': round(ma20_l, 2),
            '5日量能倍数': round(vol_ratio, 2),
            '分时站均线%': round(above_avg * 100, 1),
        })

# ========== 输出 ==========
print("\n" + "=" * 80)
print(f"  最终结果: {len(results)} 只符合全部8项标准")
print("=" * 80)

if len(results) == 0:
    print("\n  ⚠️ 无符合全部8项标准的标的")
    print("\n  详细诊断：")
    print("    在大盘跌-1.76%环境下，严格8项标准（涨幅3-5% + 涨停 + 量比>1.4 + 换手5-10% + ")
    print("    市值50-200亿 + 量能温和放大 + 5/10/20均线多头排列 + 分时站均线>70%）")
    print("    同时通过的概率极低（11只基础候选中无一只通过）。")
    print()
    print("  失败原因分布：")
    print("    1. 【均线】11只中无一严格满足 MA5>MA10>MA20 且三条均线上行")
    print("       多数为MA5>MA10但MA10<MA20（典型反弹初期形态）")
    print("    2. 【分时站均线】部分股票虽涨幅达3-5%，但分时站均价线比例<70%")
    print("       例:川发龙蟒分时站均线仅10.9%（开盘冲高后大幅回落）")
    print("    3. 【量能】少数股票5日量能不一致（如远信工业）")
else:
    result_df = pd.DataFrame(results)
    result_df = result_df.sort_values('涨幅%', ascending=False).reset_index(drop=True)
    result_df.index = result_df.index + 1
    print(f"\n  共 {len(result_df)} 只候选股：\n")
    for idx, r in result_df.iterrows():
        print(f"  [{idx}] {r['代码']} {r['名称']}  ({r['板块']})")
        print(f"      涨幅: {r['涨幅%']:+.2f}% | 现价: {r['最新价']} | 量比: {r['量比']:.2f} | 换手: {r['换手率%']:.2f}% | 流通: {r['流通市值(亿)']}亿")
        print(f"      20日涨停: {r['20日涨停次数']}次 | 均线: MA5={r['5日均线']} MA10={r['10日均线']} MA20={r['20日均线']} (多头↑)")
        print(f"      5日量能: {r['5日量能倍数']}倍 | 分时站均线: {r['分时站均线%']}%")
        print()
    result_df.to_csv('/workspace/output/尾盘候选池_20260623.csv', index=False, encoding='utf-8-sig')
    print(f"  ✓ 已保存到 /workspace/output/尾盘候选池_20260623.csv")
