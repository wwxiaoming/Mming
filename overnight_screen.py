import os
import urllib.request
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time

def fetch_kline_tencent(code, start_date, end_date):
    """通过腾讯财经API获取前复权日K线数据"""
    # 确定市场前缀
    if code.startswith('6') or code.startswith('9'):
        prefix = 'sh'
    elif code.startswith('8'):
        prefix = 'bj'
    else:
        prefix = 'sz'
    
    symbol = f"{prefix}{code}"
    url = f"https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param={symbol},day,{start_date},{end_date},30,qfq"
    
    try:
        req = urllib.request.Request(url)
        req.add_header("User-Agent", "Mozilla/5.0")
        resp = urllib.request.urlopen(req, timeout=15)
        data = json.loads(resp.read().decode('utf-8'))
        
        if data.get('code') != 0:
            return pd.DataFrame()
        
        # 数据在 data.{symbol}.qfqday 下，如果没有复权数据则用day
        stock_data = data.get('data', {}).get(symbol, {})
        klines = stock_data.get('qfqday', [])
        if not klines:
            klines = stock_data.get('day', [])

        if not klines:
            return pd.DataFrame()
        
        rows = []
        for k in klines:
            # 腾讯格式: [日期, 开盘, 收盘, 最高, 最低, 成交量]
            rows.append({
                '日期': k[0],
                '开盘': float(k[1]),
                '收盘': float(k[2]),
                '最高': float(k[3]),
                '最低': float(k[4]),
                '成交量': float(k[5]),
            })
        
        return pd.DataFrame(rows)
    except Exception as e:
        print(f"  腾讯API获取数据失败: {e}")
        return pd.DataFrame()

def fetch_kline_eastmoney(code, start_date, end_date):
    """通过东方财富API获取日K线数据（备用）"""
    import requests
    if code.startswith('68') or code.startswith('60'):
        secid = f"1.{code}"
    else:
        secid = f"0.{code}"
    
    url = "https://push2his.eastmoney.com/api/qt/stock/kline/get"
    params = {
        'fields1': 'f1,f2,f3,f4,f5,f6',
        'fields2': 'f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f116',
        'ut': '7eea3edcaed734bea9cbfc24409ed989',
        'klt': '101', 'fqt': '1',
        'secid': secid,
        'beg': start_date, 'end': end_date,
    }
    proxies = {
        'http': os.environ.get('http_proxy', os.environ.get('HTTP_PROXY', '')),
        'https': os.environ.get('https_proxy', os.environ.get('HTTPS_PROXY', '')),
    }
    try:
        r = requests.get(url, params=params, timeout=15, proxies=proxies)
        data = r.json()
        if data.get('data') is None or data['data'].get('klines') is None:
            return pd.DataFrame()
        klines = data['data']['klines']
        rows = []
        for line in klines:
            parts = line.split(',')
            rows.append({
                '日期': parts[0],
                '开盘': float(parts[1]),
                '收盘': float(parts[2]),
                '最高': float(parts[3]),
                '最低': float(parts[4]),
                '成交量': float(parts[5]),
                '成交额': float(parts[6]),
                '振幅': float(parts[7]),
                '涨跌幅': float(parts[8]),
                '涨跌额': float(parts[9]),
                '换手率': float(parts[10]),
            })
        return pd.DataFrame(rows)
    except Exception as e:
        print(f"  东方财富API获取数据失败: {e}")
        return pd.DataFrame()

def fetch_kline(code, start_date, end_date):
    """获取K线数据，优先腾讯，备用东方财富"""
    df = fetch_kline_tencent(code, start_date, end_date)
    if df.empty or len(df) < 5:
        # 尝试东方财富
        df2 = fetch_kline_eastmoney(code, start_date, end_date)
        if not df2.empty and len(df2) >= 5:
            return df2
        return df
    
    # 腾讯数据没有涨跌幅和成交额，需要计算
    df['涨跌幅'] = df['收盘'].pct_change() * 100
    df['涨跌额'] = df['收盘'].diff()
    # 成交额近似 = 成交量 * (开盘+收盘)/2 (手 * 元/股)
    df['成交额'] = df['成交量'] * (df['开盘'] + df['收盘']) / 2 * 100
    df['振幅'] = (df['最高'] - df['最低']) / df['收盘'].shift(1) * 100
    df['换手率'] = 0  # 腾讯日K不提供换手率
    
    return df

candidates = [
    ("301392", "汇成真空"), ("300401", "花园生物"), ("601083", "锦江航运"),
    ("002083", "孚日股份"), ("002915", "中欣氟材"), ("600576", "祥源文旅"),
    ("300307", "慈星股份"), ("301528", "多浦乐"), ("000751", "锌业股份"),
    ("002617", "露笑科技"), ("600531", "豫光金铅"), ("688721", "龙图光罩"),
    ("301667", "纳百川"), ("300774", "倍杰特"),
]

results = {}

end_date = datetime.now().strftime("%Y-%m-%d")
start_date = (datetime.now() - timedelta(days=40)).strftime("%Y-%m-%d")

for code, name in candidates:
    print(f"\n{'='*60}")
    print(f"分析: {name}({code})")
    print(f"{'='*60}")
    
    try:
        df = fetch_kline(code, start_date, end_date)
        
        if df.empty or len(df) < 5:
            print(f"  K线数据不足，跳过")
            continue
        
        print(f"  获取到{len(df)}根日K线")
        
        # === 第2步: 20天内有涨停 ===
        recent_20 = df.tail(20)
        limit_up_days = 0
        limit_up_dates = []
        for _, row in recent_20.iterrows():
            chg = row.get('涨跌幅', 0)
            if pd.isna(chg):
                continue
            if chg >= 9.8:  # 考虑科创板20%涨跌停
                limit_up_days += 1
                limit_up_dates.append(str(row['日期'])[:10])
            elif code.startswith('68') and chg >= 19.5:
                limit_up_days += 1
                limit_up_dates.append(str(row['日期'])[:10])
        
        step2_pass = limit_up_days > 0
        print(f"  第2步-20天涨停: {'✅通过' if step2_pass else '❌淘汰'} (涨停{limit_up_days}次: {limit_up_dates})")
        
        # === 第6步: 成交量连续温和放大 ===
        recent_5 = df.tail(5)
        vols = recent_5['成交量'].values
        vol_increasing = True
        vol_change_rates = []
        for i in range(1, len(vols)):
            if vols[i-1] > 0:
                change_rate = (vols[i] - vols[i-1]) / vols[i-1]
                vol_change_rates.append(change_rate)
                if change_rate < 0:
                    vol_increasing = False
        
        mild_increase = False
        if len(vol_change_rates) >= 2:
            avg_change = np.mean(vol_change_rates)
            positive_count = sum(1 for r in vol_change_rates if r > 0)
            mild_increase = positive_count >= len(vol_change_rates) * 0.5 and avg_change > 0
        
        step6_pass = mild_increase
        print(f"  第6步-量能温和放大: {'✅通过' if step6_pass else '❌淘汰'} (量能变化率: {[f'{r*100:.1f}%' for r in vol_change_rates]})")
        
        # === 第7步: K线均线多头向上 ===
        if len(df) >= 20:
            df_calc = df.copy()
            df_calc['MA5'] = df_calc['收盘'].rolling(5).mean()
            df_calc['MA10'] = df_calc['收盘'].rolling(10).mean()
            df_calc['MA20'] = df_calc['收盘'].rolling(20).mean()
            
            last = df_calc.iloc[-1]
            prev = df_calc.iloc[-2]
            
            bullish_alignment = (last['MA5'] > last['MA10'] > last['MA20'])
            ma5_rising = last['MA5'] > prev['MA5']
            ma10_rising = last['MA10'] > prev['MA10']
            
            step7_pass = bullish_alignment and ma5_rising
            print(f"  第7步-均线多头: {'✅通过' if step7_pass else '❌淘汰'} (MA5={last['MA5']:.2f} MA10={last['MA10']:.2f} MA20={last['MA20']:.2f} 多头={bullish_alignment} MA5上升={ma5_rising})")
        else:
            step7_pass = False
            print(f"  第7步-均线多头: ❌数据不足")
        
        # === 第8步: 分时站均价线上方 (用日K近似) ===
        last_row = df.iloc[-1]
        if last_row['成交量'] > 0 and '成交额' in df.columns:
            avg_price = last_row['成交额'] / last_row['成交量'] / 100
            above_avg = last_row['收盘'] >= avg_price
        else:
            # 用(最高+最低+收盘)/3近似均价
            avg_price = (last_row['最高'] + last_row['最低'] + last_row['收盘']) / 3
            above_avg = last_row['收盘'] >= avg_price
        
        step8_pass = above_avg
        print(f"  第8步-站均价线上方: {'✅通过' if step8_pass else '❌淘汰'} (收盘={last_row['收盘']:.2f} 均价≈{avg_price:.2f})")
        
        # === 基本面排雷 ===
        is_st = 'ST' in name or '*ST' in name
        
        # 综合结果
        all_pass = step2_pass and step6_pass and step7_pass and step8_pass and not is_st
        passed_steps = sum([step2_pass, step6_pass, step7_pass, step8_pass])
        
        print(f"\n  === 综合结果: {'✅通过全部8步' if all_pass else f'❌未通过(通过{passed_steps}/4步)'} ===")
        
        results[code] = {
            "name": name,
            "step2_pass": step2_pass,
            "step2_detail": f"20天涨停{limit_up_days}次",
            "step6_pass": step6_pass,
            "step6_detail": f"量能变化{[f'{r*100:.1f}%' for r in vol_change_rates]}",
            "step7_pass": step7_pass,
            "step7_detail": f"MA5={last['MA5']:.2f} MA10={last['MA10']:.2f} MA20={last['MA20']:.2f}",
            "step8_pass": step8_pass,
            "step8_detail": f"收盘{last_row['收盘']:.2f} vs 均价{avg_price:.2f}",
            "all_pass": all_pass,
            "passed_steps": passed_steps,
            "limit_up_count": limit_up_days,
            "close": last_row['收盘'],
            "change_pct": last_row.get('涨跌幅', 0),
        }
        
        time.sleep(0.3)
        
    except Exception as e:
        print(f"  ❌分析失败: {e}")
        results[code] = {"name": name, "error": str(e), "all_pass": False}

# === 汇总 ===
print(f"\n\n{'='*80}")
print(f"8步筛选汇总")
print(f"{'='*80}")

passed_all = [code for code, r in results.items() if r.get("all_pass", False)]
failed = [code for code, r in results.items() if not r.get("all_pass", False)]

print(f"\n通过全部8步的标的: {len(passed_all)} 只")
for code in passed_all:
    r = results[code]
    print(f"  ✅ {r['name']}({code})")

print(f"\n未通过全部8步的标的: {len(failed)} 只")
for code in failed:
    r = results[code]
    if "error" in r:
        print(f"  ❌ {r['name']}({code}): 数据异常")
    else:
        fails = []
        if not r.get("step2_pass"): fails.append("20天无涨停")
        if not r.get("step6_pass"): fails.append("量能未温和放大")
        if not r.get("step7_pass"): fails.append("均线非多头")
        if not r.get("step8_pass"): fails.append("未站均价线上方")
        print(f"  ❌ {r['name']}({code}): {', '.join(fails)}")
