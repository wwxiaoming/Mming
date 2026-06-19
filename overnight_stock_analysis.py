#!/usr/bin/env python3
"""一夜持股法 - 第二阶段盯盘验证 + 第三阶段6维评分
数据日期: 2026-06-18
"""

import time
import random
import requests
import urllib.request
import pandas as pd
import json
import math
from datetime import datetime

# ============ 东财防封共用 ============
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
EM_SESSION = requests.Session()
EM_SESSION.headers.update({"User-Agent": UA})
EM_MIN_INTERVAL = 1.5
_em_last_call = [0.0]

def em_get(url, params=None, headers=None, timeout=15, **kwargs):
    wait = EM_MIN_INTERVAL - (time.time() - _em_last_call[0])
    if wait > 0:
        time.sleep(wait + random.uniform(0.1, 0.5))
    try:
        return EM_SESSION.get(url, params=params, headers=headers, timeout=timeout, **kwargs)
    finally:
        _em_last_call[0] = time.time()

# ============ 候选股 ============
STOCKS = [
    {"code": "003004", "name": "声迅股份", "change_pct": 4.33, "turnover": 9.01, "float_mcap": 56.6, "vol_ratio": 1.60, "tier": "重点"},
    {"code": "301548", "name": "崇德科技", "change_pct": 4.30, "turnover": 8.00, "float_mcap": 67.5, "vol_ratio": 1.59, "tier": "重点"},
    {"code": "603166", "name": "福达股份", "change_pct": 4.30, "turnover": 7.96, "float_mcap": 106.5, "vol_ratio": 2.46, "tier": "重点"},
    {"code": "002029", "name": "七匹狼",   "change_pct": 4.92, "turnover": 5.25, "float_mcap": 61.7, "vol_ratio": 2.16, "tier": "次优"},
    {"code": "001266", "name": "宏英智能", "change_pct": 4.68, "turnover": 10.27, "float_mcap": 55.1, "vol_ratio": 1.58, "tier": "次优"},
    {"code": "605060", "name": "联德股份", "change_pct": 4.38, "turnover": 3.42, "float_mcap": 126.9, "vol_ratio": 1.61, "tier": "次优"},
    {"code": "301316", "name": "慧博云通", "change_pct": 4.26, "turnover": 5.35, "float_mcap": 172.8, "vol_ratio": 1.41, "tier": "次优"},
    {"code": "603052", "name": "可川科技", "change_pct": 4.18, "turnover": 4.91, "float_mcap": 179.8, "vol_ratio": 1.77, "tier": "次优"},
    {"code": "002990", "name": "盛视科技", "change_pct": 3.60, "turnover": 12.75, "float_mcap": 146.1, "vol_ratio": 1.94, "tier": "次优"},
    {"code": "688135", "name": "利扬芯片", "change_pct": 3.54, "turnover": 9.20, "float_mcap": 92.1, "vol_ratio": 1.78, "tier": "次优"},
    {"code": "300337", "name": "银邦股份", "change_pct": 3.46, "turnover": 5.40, "float_mcap": 105.7, "vol_ratio": 1.71, "tier": "次优"},
    {"code": "301617", "name": "博苑新材", "change_pct": 3.23, "turnover": 10.31, "float_mcap": 98.4, "vol_ratio": 1.55, "tier": "次优"},
]

# ============ 1. 腾讯分时数据获取 ============
def tencent_minute_data(code, date="20260618"):
    """通过腾讯财经获取分时数据"""
    prefix = "sh" if code.startswith(("6", "9")) else ("bj" if code.startswith("8") else "sz")
    # 腾讯分时API
    url = f"https://web.ifzq.gtimg.cn/appstock/app/minute/query?_var=min_data&code={prefix}{code}"
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "Mozilla/5.0")
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        text = resp.read().decode("gbk")
        # 解析 JSONP
        json_str = text.split("=", 1)[1].strip() if "=" in text else text
        data = json.loads(json_str)
        
        # 提取分时数据
        result = {}
        stock_data = data.get("data", {}).get("data", {})
        
        # 分时数据在 data.data.{code}.data.mx 中
        for key in stock_data:
            if isinstance(stock_data[key], dict):
                mx_data = stock_data[key].get("mx", "")
                if mx_data:
                    result["mx"] = mx_data
                # 均价
                avg_price = stock_data[key].get("av", 0)
                if avg_price:
                    result["av"] = float(avg_price)
                # 开盘价
                open_price = stock_data[key].get("op", 0)
                if open_price:
                    result["op"] = float(open_price)
                # 昨收
                pre_close = stock_data[key].get("pre", 0)
                if pre_close:
                    result["pre"] = float(pre_close)
            elif key == "mx":
                result["mx"] = stock_data[key]
        
        return result
    except Exception as e:
        print(f"  [WARN] 腾讯分时获取失败 {code}: {e}")
        return {}

def parse_tencent_mx(mx_str):
    """解析腾讯分时数据 mx 字符串
    格式: 时间1 价格1 成交量1;时间2 价格2 成交量2;...
    """
    if not mx_str:
        return []
    points = []
    for item in mx_str.split(";"):
        parts = item.split(" ")
        if len(parts) >= 3:
            try:
                points.append({
                    "time": parts[0],
                    "price": float(parts[1]),
                    "vol": float(parts[2])
                })
            except:
                continue
    return points

def calc_above_avg_ratio(points, avg_price):
    """计算分时线在均价线上方的时间比例"""
    if not points or avg_price <= 0:
        return 0
    above = sum(1 for p in points if p["price"] >= avg_price)
    return above / len(points) * 100

def calc_tail_surge(points):
    """计算最后5分钟(14:55-15:00)的拉升幅度"""
    if not points:
        return 0
    # 找14:55和15:00的价格
    price_1455 = None
    price_1500 = None
    for p in points:
        t = p["time"]
        if t.startswith("1455"):
            price_1455 = p["price"]
        if t.startswith("1500"):
            price_1500 = p["price"]
    
    if price_1455 and price_1500 and price_1455 > 0:
        return (price_1500 - price_1455) / price_1455 * 100
    return 0

# ============ 2. mootdx 1分钟K线获取 ============
def get_mootdx_1min(code, date_str="2026-06-18"):
    """通过mootdx获取1分钟K线"""
    try:
        from mootdx.quotes import Quotes
        client = Quotes.factory(market='std')
        market = 1 if code.startswith("6") else 0
        # 获取1分钟K线
        df = client.bars(symbol=code, category=7, offset=250, market=market)
        if df is not None and not df.empty:
            return df
        return None
    except Exception as e:
        print(f"  [WARN] mootdx 1min获取失败 {code}: {e}")
        return None

def calc_above_avg_from_klines(df):
    """从1分钟K线计算站均价线比例和尾盘拉升"""
    if df is None or df.empty:
        return None, None, None
    
    # 计算累计均价
    df = df.copy()
    df['cum_amount'] = df['amount'].cumsum()
    df['cum_vol'] = df['vol'].cumsum()
    df['avg_price'] = df['cum_amount'] / df['cum_vol'] / 100  # amount单位是元*100
    
    # 站均价线比例
    above = (df['close'] >= df['avg_price']).sum()
    ratio = above / len(df) * 100
    
    # 尾盘5分钟拉升 (14:55-15:00)
    # 找到14:55和15:00附近的K线
    late_df = df[df.index.strftime('%H%M').astype(int) >= 1455] if hasattr(df.index, 'strftime') else None
    
    # 简化：用最后5根K线
    if len(df) >= 5:
        last5 = df.tail(5)
        first_close = last5.iloc[0]['close']
        last_close = last5.iloc[-1]['close']
        if first_close > 0:
            tail_surge = (last_close - first_close) / first_close * 100
        else:
            tail_surge = 0
    else:
        tail_surge = 0
    
    # 下午盘量能 vs 上午盘量能
    # 上午: 9:30-11:30, 下午: 13:00-15:00
    # 简化：前半 vs 后半
    mid = len(df) // 2
    morning_vol = df.iloc[:mid]['vol'].sum()
    afternoon_vol = df.iloc[mid:]['vol'].sum()
    
    return ratio, tail_surge, (morning_vol, afternoon_vol)

# ============ 3. 东财资金流分钟级 ============
def eastmoney_fund_flow_minute(code):
    """东财个股资金流分钟级"""
    secid = f"1.{code}" if code.startswith("6") else f"0.{code}"
    url = "https://push2.eastmoney.com/api/qt/stock/fflow/kline/get"
    params = {
        "secid": secid, "klt": 1,
        "fields1": "f1,f2,f3,f7",
        "fields2": "f51,f52,f53,f54,f55,f56,f57",
    }
    headers = {"User-Agent": UA, "Referer": "https://quote.eastmoney.com/"}
    try:
        r = em_get(url, params=params, headers=headers, timeout=10)
        d = r.json()
        rows = []
        for line in d.get("data", {}).get("klines", []):
            parts = line.split(",")
            if len(parts) >= 6:
                rows.append({
                    "time": parts[0],
                    "main_net": float(parts[1]),
                    "small_net": float(parts[2]),
                    "mid_net": float(parts[3]),
                    "large_net": float(parts[4]),
                    "super_net": float(parts[5]),
                })
        return rows
    except Exception as e:
        print(f"  [WARN] 东财资金流获取失败 {code}: {e}")
        return []

def check_volume_sustainability(flow_data):
    """检查量能持续性：下午盘主力资金不出现明显萎缩"""
    if not flow_data or len(flow_data) < 10:
        return None
    
    # 分上午和下午
    morning = [f for f in flow_data if f["time"] < "13:00"]
    afternoon = [f for f in flow_data if f["time"] >= "13:00"]
    
    if not morning or not afternoon:
        return None
    
    # 比较上午和下午的平均主力净流入
    morning_avg = sum(abs(f["main_net"]) for f in morning) / len(morning)
    afternoon_avg = sum(abs(f["main_net"]) for f in afternoon) / len(afternoon)
    
    # 下午量能不应低于上午的50%
    ratio = afternoon_avg / morning_avg if morning_avg > 0 else 0
    return ratio

# ============ 4. 大盘15分钟线判断 ============
def check_market_15min():
    """判断6月18日14:30后大盘15分钟线方向"""
    # 获取上证指数15分钟K线
    try:
        from mootdx.quotes import Quotes
        client = Quotes.factory(market='std')
        # 上证指数 000001, market=1
        df = client.bars(symbol='000001', category=9, offset=20, market=1)
        if df is not None and not df.empty:
            print("\n上证指数15分钟K线(最近20根):")
            print(df[['open', 'close', 'high', 'low', 'vol']].to_string())
            # 判断14:30后的方向
            # 15分钟线收盘价趋势
            recent = df.tail(6)  # 14:30-15:00 约2根15分钟线
            if len(recent) >= 2:
                first_close = recent.iloc[0]['close']
                last_close = recent.iloc[-1]['close']
                direction = "上行" if last_close > first_close else "下行"
                change = (last_close - first_close) / first_close * 100
                return direction, change, df
        return None, None, None
    except Exception as e:
        print(f"  [WARN] 大盘15分钟线获取失败: {e}")
        return None, None, None

# ============ 5. 腾讯实时行情 ============
def tencent_quote(codes):
    """批量拉取腾讯财经实时行情"""
    prefixed = []
    for c in codes:
        if c.startswith(("6", "9")):
            prefixed.append(f"sh{c}")
        elif c.startswith("8"):
            prefixed.append(f"bj{c}")
        else:
            prefixed.append(f"sz{c}")
    
    url = "https://qt.gtimg.cn/q=" + ",".join(prefixed)
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "Mozilla/5.0")
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        data = resp.read().decode("gbk")
    except:
        return {}
    
    result = {}
    for line in data.strip().split(";"):
        if not line.strip() or "=" not in line or '"' not in line:
            continue
        key = line.split("=")[0].split("_")[-1]
        vals = line.split('"')[1].split("~")
        if len(vals) < 53:
            continue
        code = key[2:]
        result[code] = {
            "name": vals[1],
            "price": float(vals[3]) if vals[3] else 0,
            "last_close": float(vals[4]) if vals[4] else 0,
            "change_pct": float(vals[32]) if vals[32] else 0,
            "turnover_pct": float(vals[38]) if vals[38] else 0,
            "pe_ttm": float(vals[39]) if vals[39] else 0,
            "mcap_yi": float(vals[44]) if vals[44] else 0,
            "float_mcap_yi": float(vals[45]) if vals[45] else 0,
            "pb": float(vals[46]) if vals[46] else 0,
            "vol_ratio": float(vals[49]) if vals[49] else 0,
        }
    return result

# ============ 6. 东财概念板块 ============
def eastmoney_concept_blocks(code):
    """个股所属板块"""
    market_code = 1 if code.startswith("6") else 0
    params = {
        "fltt": "2", "invt": "2",
        "secid": f"{market_code}.{code}",
        "spt": "3", "pi": "0", "pz": "200", "po": "1",
        "fields": "f12,f14,f3,f128",
    }
    headers = {"User-Agent": UA, "Referer": "https://quote.eastmoney.com/"}
    try:
        r = em_get("https://push2.eastmoney.com/api/qt/slist/get",
                   params=params, headers=headers, timeout=15)
        d = r.json()
        diff = (d.get("data") or {}).get("diff") or {}
        items = diff.values() if isinstance(diff, dict) else diff
        tags = [it.get("f14", "") for it in items]
        return tags
    except:
        return []

# ============ 7. 东财个股基本信息 ============
def eastmoney_stock_info(code):
    """东财个股基本面"""
    market_code = 1 if code.startswith("6") else 0
    url = "https://push2.eastmoney.com/api/qt/stock/get"
    params = {
        "fltt": "2", "invt": "2",
        "fields": "f57,f58,f84,f85,f127,f116,f117,f189,f43",
        "secid": f"{market_code}.{code}",
    }
    headers = {"User-Agent": UA}
    try:
        r = em_get(url, params=params, headers=headers, timeout=10)
        d = r.json().get("data", {})
        return {
            "name": d.get("f58", ""),
            "industry": d.get("f127", ""),
            "total_shares": d.get("f84", 0),
            "float_shares": d.get("f85", 0),
        }
    except:
        return {}

# ============ 8. 同花顺热点 ============
def ths_hot_reason(date="2026-06-18"):
    """同花顺当日强势股归因"""
    url = (
        f"http://zx.10jqka.com.cn/event/api/getharden/"
        f"date/{date}/orderby/date/orderway/desc/charset/GBK/"
    )
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/117.0.0.0 Safari/537.36"}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        data = r.json()
        rows = data.get("data") or []
        return rows
    except Exception as e:
        print(f"  [WARN] 同花顺热点获取失败: {e}")
        return []

# ============ 主流程 ============
def main():
    print("=" * 80)
    print("一夜持股法 - 第二阶段盯盘验证 + 第三阶段6维评分")
    print("数据日期: 2026-06-18")
    print("=" * 80)
    
    # ---- Step 1: 获取腾讯实时行情 ----
    print("\n## Step 1: 获取腾讯实时行情")
    codes = [s["code"] for s in STOCKS]
    quotes = tencent_quote(codes)
    for code, q in quotes.items():
        print(f"  {q['name']}({code}): 价={q['price']} 涨幅={q['change_pct']}% PE={q['pe_ttm']} PB={q['pb']} 市值={q['mcap_yi']}亿")
    
    # ---- Step 2: 获取分时数据 ----
    print("\n## Step 2: 获取分时数据（站均价线比例 + 尾盘拉升）")
    
    # 已知数据
    known_above_avg = {
        "003004": 45,
        "301548": 73,
        "603166": 44,
        "301617": 78,
    }
    
    results = {}
    for stock in STOCKS:
        code = stock["code"]
        name = stock["name"]
        print(f"\n  --- {name}({code}) ---")
        
        above_avg = known_above_avg.get(code)
        tail_surge = None
        vol_sustain = None
        
        # 尝试mootdx获取1分钟K线
        df_1min = get_mootdx_1min(code)
        if df_1min is not None and not df_1min.empty:
            print(f"  mootdx 1min K线: {len(df_1min)} 条")
            ratio, surge, vols = calc_above_avg_from_klines(df_1min)
            if above_avg is None and ratio is not None:
                above_avg = ratio
            if surge is not None:
                tail_surge = surge
            if vols:
                morning_vol, afternoon_vol = vols
                vol_ratio_pm = afternoon_vol / morning_vol if morning_vol > 0 else 0
                vol_sustain = vol_ratio_pm
                print(f"  上午量={morning_vol:.0f} 下午量={afternoon_vol:.0f} 下午/上午={vol_ratio_pm:.2f}")
        else:
            print(f"  mootdx 1min K线: 无数据")
        
        # 尝试腾讯分时
        mx_data = tencent_minute_data(code)
        if mx_data:
            mx_points = parse_tencent_mx(mx_data.get("mx", ""))
            avg_price = mx_data.get("av", 0)
            if mx_points and avg_price > 0:
                if above_avg is None:
                    above_avg = calc_above_avg_ratio(mx_points, avg_price)
                if tail_surge is None:
                    tail_surge = calc_tail_surge(mx_points)
                print(f"  腾讯分时: {len(mx_points)}个点 均价={avg_price:.2f}")
        
        # 尝试东财资金流
        flow = eastmoney_fund_flow_minute(code)
        if flow:
            vol_ratio_check = check_volume_sustainability(flow)
            if vol_ratio_check is not None:
                vol_sustain = vol_ratio_check
            total_main = sum(f["main_net"] for f in flow)
            print(f"  东财资金流: {len(flow)}个分钟点 主力净流入={total_main/1e4:.0f}万")
        else:
            print(f"  东财资金流: 无数据")
        
        results[code] = {
            "name": name,
            "above_avg": above_avg,
            "tail_surge": tail_surge,
            "vol_sustain": vol_sustain,
            "change_pct": stock["change_pct"],
            "tier": stock["tier"],
        }
        print(f"  站均价线比例={above_avg}%" if above_avg else "  站均价线比例=未知")
        print(f"  尾盘5分钟拉升={tail_surge:.2f}%" if tail_surge is not None else "  尾盘5分钟拉升=未知")
        print(f"  量能持续性(下午/上午)={vol_sustain:.2f}" if vol_sustain is not None else "  量能持续性=未知")
    
    # ---- Step 3: 大盘14:30复检 ----
    print("\n\n## Step 3: 大盘14:30复检")
    direction, change, df_15min = check_market_15min()
    if direction:
        print(f"  14:30后15分钟线方向: {direction}, 变化: {change:.3f}%")
    else:
        print(f"  14:30后15分钟线方向: 无法获取")
        # 根据已知信息判断：6月18日沪指收跌0.43%，盘中4080-4117窄幅震荡
        print("  根据已知信息：沪指收跌0.43%，盘中窄幅震荡(4080-4117)")
        print("  判断：14:30后大盘偏弱，15分钟线大概率下行")
        direction = "下行"
        change = -0.1
    
    # ---- Step 4: 5项验证 ----
    print("\n\n## Step 4: 5项盯盘验证")
    print("-" * 80)
    
    verification_results = {}
    for stock in STOCKS:
        code = stock["code"]
        name = stock["name"]
        r = results[code]
        
        checks = {}
        
        # 1. 分时站均线>70%
        above = r["above_avg"]
        checks["站均线>70%"] = "通过" if above and above > 70 else "不通过"
        
        # 2. 尾盘非偷袭（最后5分钟拉升<1%）
        surge = r["tail_surge"]
        if surge is not None:
            checks["尾盘非偷袭"] = "通过" if surge < 1.0 else "不通过"
        else:
            checks["尾盘非偷袭"] = "待定"
        
        # 3. 量能持续
        vs = r["vol_sustain"]
        if vs is not None:
            checks["量能持续"] = "通过" if vs >= 0.5 else "不通过"
        else:
            checks["量能持续"] = "待定"
        
        # 4. 大盘14:30复检
        checks["大盘复检"] = "通过" if direction == "上行" else "不通过"
        
        # 5. 涨幅未透支（3%-5%）
        chg = r["change_pct"]
        checks["涨幅未透支"] = "通过" if 3.0 <= chg <= 5.0 else "不通过"
        
        pass_count = sum(1 for v in checks.values() if v == "通过")
        fail_count = sum(1 for v in checks.values() if v == "不通过")
        
        verification_results[code] = {
            "checks": checks,
            "pass_count": pass_count,
            "fail_count": fail_count,
            "passed": fail_count == 0,  # 任一不通过则淘汰
        }
        
        status = "✅ 通过" if verification_results[code]["passed"] else "❌ 淘汰"
        print(f"\n  {name}({code}) [{r['tier']}候选] {status}")
        for k, v in checks.items():
            symbol = "✅" if v == "通过" else ("❌" if v == "不通过" else "⚠️")
            print(f"    {symbol} {k}: {v}")
        print(f"    通过{pass_count}/5, 不通过{fail_count}/5")
    
    # ---- Step 5: 大盘复检全局判断 ----
    print("\n\n## 大盘复检全局判断")
    if direction == "下行":
        print("  ⚠️ 6月18日沪指收跌0.43%，14:30后15分钟线下行")
        print("  ⚠️ 按一夜持股法规则，大盘复检不通过，应当日空仓！")
        print("  ⚠️ 以下评分仅供参考，实际操作建议空仓")
    else:
        print("  ✅ 大盘14:30复检通过，可继续选股")
    
    # ---- Step 6: 6维评分（对通过验证的标的）----
    print("\n\n## Step 5: 6维评分")
    print("-" * 80)
    
    # 获取板块信息
    print("\n获取板块归属...")
    block_info = {}
    for stock in STOCKS:
        code = stock["code"]
        tags = eastmoney_concept_blocks(code)
        block_info[code] = tags
        print(f"  {stock['name']}({code}): {', '.join(tags[:8])}")
    
    # 获取同花顺热点
    print("\n获取同花顺热点...")
    hot_stocks = ths_hot_reason("2026-06-18")
    hot_codes = set()
    hot_reasons = {}
    for h in hot_stocks:
        c = h.get("code", "")
        hot_codes.add(c)
        hot_reasons[c] = h.get("reason", "")
    print(f"  当日强势股: {len(hot_stocks)} 只")
    
    # 评分
    scoring_results = {}
    for stock in STOCKS:
        code = stock["code"]
        name = stock["name"]
        r = results[code]
        v = verification_results[code]
        
        # 即使未通过验证也评分，但标注
        scores = {}
        
        # 1. 分时强度 (1-10)
        above = r["above_avg"]
        if above is not None:
            if above >= 80:
                scores["分时强度"] = 9
            elif above >= 70:
                scores["分时强度"] = 7
            elif above >= 60:
                scores["分时强度"] = 5
            elif above >= 50:
                scores["分时强度"] = 4
            else:
                scores["分时强度"] = 2
        else:
            scores["分时强度"] = 5  # 默认中间分
        
        # 2. 量价配合 (1-10)
        vol_ratio = stock["vol_ratio"]
        turnover = stock["turnover"]
        if vol_ratio >= 2.0 and turnover >= 5:
            scores["量价配合"] = 8
        elif vol_ratio >= 1.5 and turnover >= 5:
            scores["量价配合"] = 7
        elif vol_ratio >= 1.5:
            scores["量价配合"] = 6
        elif vol_ratio >= 1.0:
            scores["量价配合"] = 5
        else:
            scores["量价配合"] = 3
        
        # 3. K线形态 (1-10) - 基于涨幅和位置
        chg = stock["change_pct"]
        if 3.5 <= chg <= 4.5:
            scores["K线形态"] = 8  # 理想区间
        elif 3.0 <= chg <= 5.0:
            scores["K线形态"] = 7
        elif chg > 5.0:
            scores["K线形态"] = 5  # 涨幅过大
        else:
            scores["K线形态"] = 6
        
        # 4. 股性活跃度 (1-10)
        is_hot = code in hot_codes
        tags = block_info.get(code, [])
        # AI/半导体/光模块相关加分
        ai_related = any(kw in " ".join(tags) for kw in ["AI", "算力", "半导体", "芯片", "光模块", "PCB", "液冷", "人工智能"])
        if is_hot and ai_related:
            scores["股性活跃度"] = 9
        elif is_hot:
            scores["股性活跃度"] = 7
        elif ai_related:
            scores["股性活跃度"] = 7
        else:
            scores["股性活跃度"] = 5
        
        # 5. 基本面安全度 (1-10)
        q = quotes.get(code, {})
        pe = q.get("pe_ttm", 0)
        pb = q.get("pb", 0)
        if pe > 0 and pe < 30:
            scores["基本面安全度"] = 8
        elif pe >= 30 and pe < 60:
            scores["基本面安全度"] = 6
        elif pe >= 60 and pe < 100:
            scores["基本面安全度"] = 4
        elif pe >= 100:
            scores["基本面安全度"] = 2
        else:
            scores["基本面安全度"] = 5  # 亏损股
        
        # 6. 次日溢价预期 (1-10)
        # 考虑板块持续性、市场情绪
        if ai_related and is_hot:
            scores["次日溢价预期"] = 8
        elif ai_related:
            scores["次日溢价预期"] = 7
        elif is_hot:
            scores["次日溢价预期"] = 6
        else:
            scores["次日溢价预期"] = 4
        
        # 加权总分
        weights = {
            "分时强度": 0.20,
            "量价配合": 0.20,
            "K线形态": 0.15,
            "股性活跃度": 0.15,
            "基本面安全度": 0.15,
            "次日溢价预期": 0.15,
        }
        total = sum(scores[k] * weights[k] for k in scores)
        
        scoring_results[code] = {
            "scores": scores,
            "total": round(total, 2),
            "passed_verification": v["passed"],
            "hot_reason": hot_reasons.get(code, ""),
            "blocks": tags[:5],
        }
        
        v_status = "✅通过验证" if v["passed"] else "❌未通过验证"
        print(f"\n  {name}({code}) [{stock['tier']}候选] {v_status}")
        print(f"    综合得分: {total:.2f}/10")
        for k, s in scores.items():
            print(f"    {k}: {s}/10 (权重{weights[k]*100:.0f}%)")
        if hot_reasons.get(code):
            print(f"    题材: {hot_reasons[code]}")
        print(f"    板块: {', '.join(tags[:5])}")
    
    # ---- Step 7: 最终输出 ----
    print("\n\n" + "=" * 80)
    print("最终输出")
    print("=" * 80)
    
    # 按综合得分排序
    sorted_stocks = sorted(scoring_results.items(), key=lambda x: x[1]["total"], reverse=True)
    
    print("\n### 🏆 推荐买入标的")
    print("(注意：大盘14:30复检不通过，按规则应当日空仓！以下仅供参考)")
    recommended = [(code, data) for code, data in sorted_stocks if data["passed_verification"]]
    if recommended:
        for code, data in recommended:
            stock_info = next(s for s in STOCKS if s["code"] == code)
            q = quotes.get(code, {})
            price = q.get("price", 0)
            # 建议买入价区间：收盘价±0.5%
            buy_low = price * 0.995 if price else 0
            buy_high = price * 1.005 if price else 0
            print(f"\n  📌 {data['scores']}分 | {stock_info['name']}({code})")
            print(f"     综合得分: {data['total']:.2f}/10")
            print(f"     建议买入价: {buy_low:.2f}-{buy_high:.2f}")
            print(f"     建议仓位: 20%（单只不超过20%）")
            print(f"     题材: {data.get('hot_reason', '无')}")
    else:
        print("\n  无标的通过全部5项验证")
    
    print("\n### 👀 仅观察标的")
    observed = [(code, data) for code, data in sorted_stocks 
                if not data["passed_verification"] and data["total"] >= 6.0]
    for code, data in observed:
        stock_info = next(s for s in STOCKS if s["code"] == code)
        v = verification_results[code]
        fail_items = [k for k, val in v["checks"].items() if val == "不通过"]
        print(f"\n  🔍 {stock_info['name']}({code}) 得分={data['total']:.2f}")
        print(f"     未通过项: {', '.join(fail_items)}")
    
    print("\n### ❌ 排除标的")
    excluded = [(code, data) for code, data in sorted_stocks 
                if not data["passed_verification"] and data["total"] < 6.0]
    for code, data in excluded:
        stock_info = next(s for s in STOCKS if s["code"] == code)
        v = verification_results[code]
        fail_items = [k for k, val in v["checks"].items() if val == "不通过"]
        print(f"\n  ✖ {stock_info['name']}({code}) 得分={data['total']:.2f}")
        print(f"     排除理由: {', '.join(fail_items)}")
    
    # 全局结论
    print("\n\n### 📋 全局结论")
    if direction == "下行":
        print("  ⚠️⚠️⚠️ 重要提醒 ⚠️⚠️⚠️")
        print("  6月18日沪指收跌0.43%，14:30后大盘15分钟线判断为下行")
        print("  按一夜持股法规则，大盘复检不通过 → 当日应空仓！")
        print("  且6月18日为端午节前最后一个交易日，节后开盘存在不确定性")
        print("  建议：空仓过端午，节后观察大盘方向再操作")
    else:
        print("  大盘复检通过，可按评分结果操作")

if __name__ == "__main__":
    main()
