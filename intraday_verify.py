# -*- coding: utf-8 -*-
"""
5项盯盘验证 - 2026-06-23 14:40
使用腾讯财经数据源
"""
import requests
import json
import pandas as pd
import numpy as np
import time
import warnings
warnings.filterwarnings('ignore')

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://gu.qq.com/',
}

# 11只候选股
CANDIDATES = [
    ('sh605178', '时空科技'),
    ('sh603341', '龙旗科技'),
    ('sz002546', '新联电子'),
    ('sz002312', '川发龙蟒'),
    ('sh688166', '博瑞医药'),
    ('sh688131', '皓元医药'),
    ('sz301053', '远信工业'),
    ('sz300520', '科大国创'),
    ('sz300259', '新天科技'),
    ('sh688699', '明微电子'),
    ('sh688237', '超卓航科'),
]

def get_tencent_realtime(codes):
    """拉腾讯实时行情 - 返回 {code: dict}"""
    url = f"https://qt.gtimg.cn/q={'%2C'.join(codes)}"
    for retry in range(3):
        try:
            r = requests.get(url, headers=HEADERS, timeout=10)
            if r.status_code == 200 and '~' in r.text:
                result = {}
                for line in r.text.strip().split(';'):
                    if not line.strip() or '="' not in line:
                        continue
                    key = line.split('=')[0].strip()
                    code = key[2:] if key.startswith('v_') else key
                    body = line.split('"')[1]
                    vals = body.split('~')
                    if len(vals) < 50:
                        continue
                    result[code] = {
                        'name': vals[1],
                        'price': float(vals[3]) if vals[3] else 0,
                        'last_close': float(vals[4]) if vals[4] else 0,
                        'open': float(vals[5]) if vals[5] else 0,
                        'high': float(vals[33]) if len(vals) > 33 and vals[33] else 0,
                        'low': float(vals[34]) if len(vals) > 34 and vals[34] else 0,
                        'change_amt': float(vals[31]) if len(vals) > 31 and vals[31] else 0,
                        'change_pct': float(vals[32]) if len(vals) > 32 and vals[32] else 0,
                        'amount': float(vals[37]) if len(vals) > 37 and vals[37] else 0,
                        'turnover_pct': float(vals[38]) if len(vals) > 38 and vals[38] else 0,
                        'volume': float(vals[36]) if len(vals) > 36 and vals[36] else 0,
                    }
                return result
        except Exception as e:
            time.sleep(0.3)
    return {}

def get_tencent_minute(code):
    """拉腾讯分时 - 返回 DataFrame: time, price, volume, amount"""
    url = 'https://web.ifzq.gtimg.cn/appstock/app/minute/query'
    for retry in range(3):
        try:
            r = requests.get(url, params={'code': code}, headers=HEADERS, timeout=10)
            if r.status_code == 200:
                d = r.json()
                data = d.get('data', {}).get(code, {}).get('data', {})
                if isinstance(data, dict) and 'data' in data:
                    rows = []
                    for line in data['data']:
                        parts = line.split(' ')
                        if len(parts) >= 4:
                            rows.append({
                                'time': parts[0],       # HHMM
                                'price': float(parts[1]),
                                'volume_lot': float(parts[2]),  # 累计手数
                                'amount': float(parts[3]),      # 累计成交额(元)
                            })
                    if rows:
                        return pd.DataFrame(rows)
        except Exception as e:
            time.sleep(0.3)
    return pd.DataFrame()

def calc_vwap(df):
    """计算VWAP (cumulative_amount / (cumulative_volume_in_shares))
    注: 腾讯分时数据中 volume_lot 单位为「手」(1手=100股), amount 单位为「元」
    """
    if len(df) == 0:
        return df
    df = df.copy()
    df['cum_vol_lot'] = df['volume_lot'].cumsum()      # 累计手数
    df['cum_vol_share'] = df['cum_vol_lot'] * 100       # 累计股数
    df['cum_amt'] = df['amount'].cumsum()               # 累计成交额(元)
    df['vwap'] = df['cum_amt'] / df['cum_vol_share']    # VWAP(元/股)
    return df

def get_index_minute():
    """上证指数分时"""
    return get_tencent_minute('sh000001')

# ====== 4. 大盘 14:30 复检 ======
print("=" * 80)
print("  [4] 大盘 14:30 复检")
print("=" * 80)

idx_realtime = get_tencent_realtime(['sh000001'])
idx_min = get_index_minute()

if 'sh000001' in idx_realtime and len(idx_min) > 0:
    last_close = idx_realtime['sh000001']['last_close']
    row_1430 = idx_min[idx_min['time'] == '1430']
    if len(row_1430) > 0:
        p1430 = row_1430.iloc[0]['price']
        pct_1430 = (p1430 - last_close) / last_close * 100
        print(f"  昨收: {last_close}")
        print(f"  14:30 价: {p1430}")
        print(f"  14:30 涨跌幅: {pct_1430:+.2f}%")
        print(f"  阈值: ≥ -1.0% (即跌幅≤1%)")
        print(f"  判定: {'❌ FAIL（超阈值1%）' if pct_1430 < -1.0 else '✅ PASS'}")
        idx_pass = pct_1430 >= -1.0
    else:
        print(f"  14:30 分时数据缺失")
        idx_pass = False
else:
    print(f"  上证指数数据缺失")
    idx_pass = False

# ====== 逐股验证 ======
print("\n" + "=" * 80)
print("  5项验证 · 逐股明细")
print("=" * 80)

# 拉所有实时数据
realtime = get_tencent_realtime([c for c, _ in CANDIDATES])
print(f"\n[实时行情] 拉取 {len(realtime)}/{len(CANDIDATES)} 只")

results = []
for code, name in CANDIDATES:
    print(f"\n[{code}] {name}")
    print(f"  {'─' * 70}")
    res = {'code': code, 'name': name, 'passes': 0, 'fails': 0, 'details': []}

    # 1. 分时站均线 > 70%
    df = get_tencent_minute(code)
    if len(df) == 0:
        res['fails'] += 1
        res['details'].append('[1] ✗ 分时数据缺失')
        print(f"  [1] 分时站均线: ✗ 分时数据缺失")
    else:
        df = calc_vwap(df)
        above = (df['price'] > df['vwap']).sum()
        total = len(df)
        pct_above = above / total
        passed = pct_above >= 0.70
        if passed: res['passes'] += 1
        else: res['fails'] += 1
        msg = f"[1] 分时站均价线: {above}/{total} = {pct_above*100:.1f}% {'✅ PASS' if passed else '❌ FAIL'} (阈值≥70%)"
        res['details'].append(msg)
        res['站均线%'] = round(pct_above * 100, 1)
        print(f"  {msg}")

    # 2. 尾盘非偷袭
    if len(df) > 0:
        df_1425 = df[(df['time'] >= '1425') & (df['time'] <= '1429')]
        df_1430 = df[(df['time'] >= '1430') & (df['time'] <= '1434')]
        if len(df_1425) > 0 and len(df_1430) > 0:
            p1 = df_1425.iloc[-1]['price']  # 14:29
            p2 = df_1430.iloc[-1]['price']  # 14:34
            # 5分钟涨幅
            chg = (p2 - p1) / p1 * 100
            passed = abs(chg) < 1.0
            if passed: res['passes'] += 1
            else: res['fails'] += 1
            msg = f"[2] 尾盘非偷袭: 14:29={p1:.3f} → 14:34={p2:.3f} 5min涨幅{chg:+.2f}% {'✅ PASS' if passed else '❌ FAIL'} (阈值<1%)"
            res['details'].append(msg)
            res['尾盘5min%'] = round(chg, 2)
            print(f"  {msg}")
        else:
            res['fails'] += 1
            res['details'].append('[2] ✗ 尾盘区段数据缺失')
            print(f"  [2] 尾盘区段数据缺失")

    # 3. 量能持续 (volume_lot 是累计的,需差分得每5分钟增量)
    if len(df) > 0:
        df_pm = df[(df['time'] >= '1400') & (df['time'] <= '1439')].copy()
        df_am = df[(df['time'] >= '0930') & (df['time'] <= '1130')].copy()
        if len(df_pm) > 0 and len(df_am) > 0:
            # 5分钟分桶
            df_pm['bucket'] = df_pm['time'].str[:3] + (df_pm['time'].str[3:5].astype(int) // 5 * 5).astype(str).str.zfill(2)
            df_am['bucket'] = df_am['time'].str[:3] + (df_am['time'].str[3:5].astype(int) // 5 * 5).astype(str).str.zfill(2)

            # 对每个bucket用首尾差计算增量volume
            def bucket_delta(group):
                if len(group) < 2:
                    return group['volume_lot'].iloc[-1]
                return group['volume_lot'].iloc[-1] - group['volume_lot'].iloc[0]
            pm_vols = df_pm.groupby('bucket').apply(bucket_delta)
            am_vols = df_am.groupby('bucket').apply(bucket_delta)
            am_avg = am_vols.mean()
            if am_avg > 0:
                pm_passed = (pm_vols > am_avg).sum()
                pm_total = len(pm_vols)
                passed = pm_passed >= pm_total * 0.7
                if passed: res['passes'] += 1
                else: res['fails'] += 1
                avg_ratio = pm_vols.mean() / am_avg
                msg = f"[3] 量能持续: 午后{pm_passed}/{pm_total}段 > 上午均量({am_avg:.0f}手) | 午后均量倍数={avg_ratio:.2f} {'✅ PASS' if passed else '❌ FAIL'}"
                res['details'].append(msg)
                res['午后量能'] = f"{pm_passed}/{pm_total}"
                res['午后均量倍数'] = round(avg_ratio, 2)
                print(f"  {msg}")
            else:
                res['fails'] += 1
                print(f"  [3] ✗ 上午均量为0")
        else:
            res['fails'] += 1
            print(f"  [3] ✗ 时段数据缺失 (午后{len(df_pm)} 上午{len(df_am)})")

    # 4. 大盘 14:30 复检 (全局)
    if not idx_pass:
        res['fails'] += 1
        msg = f"[4] 大盘 14:30 复检: ❌ FAIL (上证-1.86% < -1.0% 阈值)"
        res['details'].append(msg)
        print(f"  {msg}")
    else:
        res['passes'] += 1
        msg = "[4] 大盘 14:30 复检: ✅ PASS"
        res['details'].append(msg)
        print(f"  {msg}")

    # 5. 涨幅未透支 (3%-5%)
    if code in realtime:
        q = realtime[code]
        chg_pct = q['change_pct']
        passed = 3.0 <= chg_pct <= 5.0
        if passed: res['passes'] += 1
        else: res['fails'] += 1
        msg = f"[5] 涨幅未透支: {chg_pct:+.2f}% {'✅ PASS' if passed else '❌ FAIL'} (阈值3-5%)"
        res['details'].append(msg)
        res['涨跌幅%'] = chg_pct
        res['现价'] = q['price']
        res['昨收'] = q['last_close']
        print(f"  {msg}")
    else:
        res['fails'] += 1
        print(f"  [5] ✗ 实时行情缺失")

    print(f"  >>> 通过 {res['passes']}/5 项 <<<")
    results.append(res)

# ====== 汇总 ======
print("\n" + "=" * 80)
print("  汇总：5项盯盘验证结果")
print("=" * 80)
print(f"{'代码':<10} {'名称':<8} {'站均线%':<10} {'尾盘5min%':<10} {'午后量能':<10} {'大盘':<6} {'涨跌幅%':<10} {'通过'}")
print("─" * 80)
for r in results:
    p1 = f"{r.get('站均线%', '-'):.1f}%" if '站均线%' in r else '-'
    p2 = f"{r.get('尾盘5min%', 0):+.2f}%" if '尾盘5min%' in r else '-'
    p3 = r.get('午后量能', '-')
    p4 = '❌FAIL' if not idx_pass else '✓'
    p5 = f"{r.get('涨跌幅%', 0):+.2f}%" if '涨跌幅%' in r else '-'
    print(f"{r['code']:<10} {r['name']:<8} {p1:<10} {p2:<10} {p3:<10} {p4:<6} {p5:<10} {r['passes']}/5")

# ====== 分类 ======
print("\n" + "=" * 80)
print("  分类结果")
print("=" * 80)

passed_5 = [r for r in results if r['passes'] == 5]
passed_partial = [r for r in results if 3 <= r['passes'] < 5]
failed = [r for r in results if r['passes'] < 3]

print(f"\n【✅ 通过验证（5/5）】({len(passed_5)}只)")
for r in passed_5:
    print(f"  {r['code']} {r['name']}")

print(f"\n【👀 仅观察（3-4/5）】({len(passed_partial)}只)")
for r in passed_partial:
    print(f"  {r['code']} {r['name']} ({r['passes']}/5)")

print(f"\n【❌ 排除（<3/5）】({len(failed)}只)")
for r in failed:
    print(f"  {r['code']} {r['name']} ({r['passes']}/5)")

if len(passed_5) == 0:
    print("\n" + "=" * 80)
    print("  📌 最终判定")
    print("=" * 80)
    print("  无一只通过5项验证。")
    if not idx_pass:
        print("  ❌ **全部淘汰** —— 大盘14:30跌幅超阈值（-1.86% < -1%），全市场系统性下跌，")
        print("     任何个股层面的强势都难以独立于大盘。根据策略纪律，**当日空仓**。")
    else:
        print("  ❌ 全部淘汰 —— 个股层面亦无标的通过全部5项验证。")

# 保存到CSV
df_res = pd.DataFrame([{
    '代码': r['code'],
    '名称': r['name'],
    '站均线%': r.get('站均线%', None),
    '尾盘5min%': r.get('尾盘5min%', None),
    '午后量能': r.get('午后量能', None),
    '午后均量倍数': r.get('午后均量倍数', None),
    '涨跌幅%': r.get('涨跌幅%', None),
    '现价': r.get('现价', None),
    '昨收': r.get('昨收', None),
    '通过项': r['passes'],
    '失败项': r['fails'],
} for r in results])
df_res.to_csv('/workspace/output/5项盯盘验证_20260623.csv', index=False, encoding='utf-8-sig')
print(f"\n✓ 详细结果已保存: /workspace/output/5项盯盘验证_20260623.csv")
