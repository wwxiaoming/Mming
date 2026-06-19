#!/usr/bin/env python3
"""一夜持股法 - 使用可用API获取分时数据
可用API: 腾讯实时行情(qt.gtimg.cn), 腾讯分时(web.ifzq.gtimg.cn), 
         东财slist板块, 同花顺热点, 新浪行情
不可用: 东财push2/push2his(代理限制), 腾讯1minK线(SSL)
"""

import time
import random
import requests
import urllib.request
import json
import pandas as pd

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"

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

def get_prefix(code):
    if code.startswith(("6", "9")):
        return "sh"
    elif code.startswith("8"):
        return "bj"
    else:
        return "sz"

# ============ 腾讯分时数据 ============
def tencent_minute_data(code):
    """获取腾讯分时数据"""
    prefix = get_prefix(code)
    url = f"https://web.ifzq.gtimg.cn/appstock/app/minute/query?_var=min_data&code={prefix}{code}"
    req = urllib.request.Request(url)
    req.add_header("User-Agent", UA)
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        text = resp.read().decode("gbk")
        json_str = text.split("=", 1)[1].strip() if "=" in text else text
        data = json.loads(json_str)
        return data
    except Exception as e:
        print(f"  [FAIL] 腾讯分时 {code}: {e}")
        return None

def parse_tencent_minute(data, code):
    """解析腾讯分时数据
    返回: (站均价线比例%, 尾盘5分钟拉升%, 量能持续性比)
    """
    if not data:
        return None, None, None
    
    stock_data = data.get("data", {}).get("data", {})
    
    mx_str = None
    avg_price = 0
    pre_close = 0
    
    # 遍历找到分时数据
    for key, val in stock_data.items():
        if isinstance(val, dict):
            if "mx" in val:
                mx_str = val["mx"]
            if "av" in val and val["av"]:
                avg_price = float(val["av"])
            if "pre" in val and val["pre"]:
                pre_close = float(val["pre"])
    
    if not mx_str:
        return None, None, None
    
    # 解析分时点: time price vol;time price vol;...
    points = []
    for item in mx_str.split(";"):
        item = item.strip()
        if not item:
            continue
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
    
    if not points:
        return None, None, None
    
    # 计算均价（如果API没给）
    if avg_price <= 0:
        cum_amount = sum(p["price"] * p["vol"] for p in points)
        cum_vol = sum(p["vol"] for p in points)
        avg_price = cum_amount / cum_vol if cum_vol > 0 else 0
    
    # 1. 站均价线比例
    above_count = sum(1 for p in points if p["price"] >= avg_price)
    above_ratio = above_count / len(points) * 100
    
    # 2. 尾盘5分钟拉升 (14:55-15:00)
    price_1455 = None
    price_1500 = None
    for p in points:
        t = p["time"]
        if t.startswith("1455"):
            price_1455 = p["price"]
        if t.startswith("1500"):
            price_1500 = p["price"]
    
    tail_surge = 0
    if price_1455 and price_1500 and price_1455 > 0:
        tail_surge = (price_1500 - price_1455) / price_1455 * 100
    
    # 3. 量能持续性: 上午vs下午成交量
    morning_vol = sum(p["vol"] for p in points if p["time"] < "1300")
    afternoon_vol = sum(p["vol"] for p in points if p["time"] >= "1300")
    vol_ratio = afternoon_vol / morning_vol if morning_vol > 0 else 0
    
    return above_ratio, tail_surge, vol_ratio

# ============ 腾讯实时行情 ============
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

# ============ 东财板块 ============
def eastmoney_concept_blocks(code):
    market_code = 1 if code.startswith("6") else 0
    params = {
        "fltt": "2", "invt": "2",
        "secid": f"{market_code}.{code}",
        "spt": "3", "pi": "0", "pz": "200", "po": "1",
        "fields": "f12,f14,f3,f128",
    }
    headers = {"User-Agent": UA, "Referer": "https://quote.eastmoney.com/"}
    try:
        r = requests.get("https://push2.eastmoney.com/api/qt/slist/get",
                        params=params, headers=headers, timeout=15)
        d = r.json()
        diff = (d.get("data") or {}).get("diff") or {}
        items = diff.values() if isinstance(diff, dict) else diff
        tags = [it.get("f14", "") for it in items]
        return tags
    except:
        return []

# ============ 同花顺热点 ============
def ths_hot_reason(date="2026-06-18"):
    url = (
        f"http://zx.10jqka.com.cn/event/api/getharden/"
        f"date/{date}/orderby/date/orderway/desc/charset/GBK/"
    )
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/117.0.0.0 Safari/537.36"}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        data = r.json()
        return data.get("data") or []
    except:
        return []

# ============ 新浪行情 ============
def sina_quote(codes):
    """新浪实时行情"""
    prefixed = [f"sh{c}" if c.startswith("6") else f"sz{c}" for c in codes]
    url = "https://hq.sinajs.cn/list=" + ",".join(prefixed)
    headers = {"User-Agent": UA, "Referer": "https://finance.sina.com.cn/"}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        return r.text
    except:
        return ""

# ============ 主流程 ============
def main():
    print("=" * 80)
    print("一夜持股法 - 第二阶段盯盘验证 + 第三阶段6维评分")
    print("数据日期: 2026-06-18")
    print("=" * 80)
    
    # ---- Step 1: 腾讯实时行情 ----
    print("\n## Step 1: 腾讯实时行情")
    codes = [s["code"] for s in STOCKS]
    quotes = tencent_quote(codes)
    for code, q in quotes.items():
        print(f"  {q['name']}({code}): 价={q['price']} 涨幅={q['change_pct']}% PE={q['pe_ttm']} PB={q['pb']} 市值={q['mcap_yi']}亿 量比={q['vol_ratio']}")
    
    # ---- Step 2: 腾讯分时数据 ----
    print("\n## Step 2: 腾讯分时数据")
    
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
        
        # 腾讯分时
        data = tencent_minute_data(code)
        if data:
            ar, ts, vs = parse_tencent_minute(data, code)
            print(f"  腾讯分时解析: 站均线={ar}, 尾盘拉升={ts}, 量能比={vs}")
            if above_avg is None and ar is not None:
                above_avg = ar
            if ts is not None:
                tail_surge = ts
            if vs is not None:
                vol_sustain = vs
        else:
            print(f"  腾讯分时: 无数据")
        
        results[code] = {
            "name": name,
            "above_avg": above_avg,
            "tail_surge": tail_surge,
            "vol_sustain": vol_sustain,
            "change_pct": stock["change_pct"],
            "tier": stock["tier"],
        }
        print(f"  最终: 站均线={above_avg}%, 尾盘拉升={tail_surge}, 量能比={vol_sustain}")
    
    # ---- Step 3: 大盘14:30复检 ----
    print("\n\n## Step 3: 大盘14:30复检")
    # 获取上证指数分时数据
    idx_data = tencent_minute_data("000001")
    idx_above, idx_tail, idx_vol = parse_tencent_minute(idx_data, "000001") if idx_data else (None, None, None)
    
    # 判断14:30后方向
    # 6月18日沪指收跌0.43%，盘中4080-4117窄幅震荡
    # 收盘4090.48，跌幅0.43%
    # 如果14:30后分时在均价线下方，则判断下行
    market_direction = "下行"  # 默认判断
    
    if idx_data:
        stock_data = idx_data.get("data", {}).get("data", {})
        mx_str = None
        for key, val in stock_data.items():
            if isinstance(val, dict) and "mx" in val:
                mx_str = val["mx"]
        
        if mx_str:
            points = []
            for item in mx_str.split(";"):
                item = item.strip()
                if not item:
                    continue
                parts = item.split(" ")
                if len(parts) >= 2:
                    try:
                        points.append({"time": parts[0], "price": float(parts[1])})
                    except:
                        continue
            
            # 找14:30和15:00的价格
            price_1430 = None
            price_1500 = None
            for p in points:
                if p["time"].startswith("1430"):
                    price_1430 = p["price"]
                if p["time"].startswith("1500"):
                    price_1500 = p["price"]
            
            if price_1430 and price_1500:
                change_1430_1500 = (price_1500 - price_1430) / price_1430 * 100
                market_direction = "上行" if change_1430_1500 > 0 else "下行"
                print(f"  上证指数14:30价={price_1430}, 15:00价={price_1500}, 变化={change_1430_1500:.3f}%")
                print(f"  14:30后方向: {market_direction}")
            else:
                print(f"  无法获取14:30/15:00价格，使用默认判断: {market_direction}")
        else:
            print(f"  无分时数据，使用默认判断: {market_direction}")
    else:
        print(f"  无上证指数数据，根据已知信息(沪指收跌0.43%)判断: {market_direction}")
    
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
        if above is not None:
            checks["站均线>70%"] = "通过" if above > 70 else "不通过"
        else:
            checks["站均线>70%"] = "待定(无数据)"
        
        # 2. 尾盘非偷袭（最后5分钟拉升<1%）
        surge = r["tail_surge"]
        if surge is not None:
            checks["尾盘非偷袭"] = "通过" if surge < 1.0 else "不通过"
        else:
            checks["尾盘非偷袭"] = "待定(无数据)"
        
        # 3. 量能持续
        vs = r["vol_sustain"]
        if vs is not None:
            checks["量能持续"] = "通过" if vs >= 0.5 else "不通过"
        else:
            checks["量能持续"] = "待定(无数据)"
        
        # 4. 大盘14:30复检
        checks["大盘复检"] = "通过" if market_direction == "上行" else "不通过"
        
        # 5. 涨幅未透支（3%-5%）
        chg = r["change_pct"]
        checks["涨幅未透支"] = "通过" if 3.0 <= chg <= 5.0 else "不通过"
        
        pass_count = sum(1 for v in checks.values() if v == "通过")
        fail_count = sum(1 for v in checks.values() if v == "不通过")
        pending_count = sum(1 for v in checks.values() if "待定" in v)
        
        # 判定：任一"不通过"则淘汰；"待定"项不作为淘汰依据
        passed = fail_count == 0
        
        verification_results[code] = {
            "checks": checks,
            "pass_count": pass_count,
            "fail_count": fail_count,
            "pending_count": pending_count,
            "passed": passed,
        }
        
        status = "✅ 通过" if passed else "❌ 淘汰"
        print(f"\n  {name}({code}) [{r['tier']}候选] {status}")
        for k, v in checks.items():
            symbol = "✅" if v == "通过" else ("❌" if v == "不通过" else "⚠️")
            print(f"    {symbol} {k}: {v}")
        print(f"    通过{pass_count}/5, 不通过{fail_count}/5, 待定{pending_count}/5")
    
    # ---- Step 5: 板块和热点信息 ----
    print("\n\n## Step 5: 板块归属和热点信息")
    
    block_info = {}
    for stock in STOCKS:
        code = stock["code"]
        tags = eastmoney_concept_blocks(code)
        block_info[code] = tags
        print(f"  {stock['name']}({code}): {', '.join(tags[:8])}")
        time.sleep(0.5)
    
    hot_stocks = ths_hot_reason("2026-06-18")
    hot_codes = set()
    hot_reasons = {}
    for h in hot_stocks:
        c = h.get("code", "")
        hot_codes.add(c)
        hot_reasons[c] = h.get("reason", "")
    print(f"\n  当日强势股: {len(hot_stocks)} 只")
    
    # 检查候选股是否在强势股中
    for stock in STOCKS:
        code = stock["code"]
        if code in hot_codes:
            print(f"  🔥 {stock['name']}({code}) 在强势股中: {hot_reasons.get(code, '')}")
    
    # ---- Step 6: 6维评分 ----
    print("\n\n## Step 6: 6维评分")
    print("-" * 80)
    
    scoring_results = {}
    for stock in STOCKS:
        code = stock["code"]
        name = stock["name"]
        r = results[code]
        v = verification_results[code]
        q = quotes.get(code, {})
        
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
            scores["分时强度"] = 5
        
        # 2. 量价配合 (1-10)
        vol_ratio_val = stock["vol_ratio"]
        turnover = stock["turnover"]
        if vol_ratio_val >= 2.0 and turnover >= 5:
            scores["量价配合"] = 8
        elif vol_ratio_val >= 1.5 and turnover >= 5:
            scores["量价配合"] = 7
        elif vol_ratio_val >= 1.5:
            scores["量价配合"] = 6
        elif vol_ratio_val >= 1.0:
            scores["量价配合"] = 5
        else:
            scores["量价配合"] = 3
        
        # 3. K线形态 (1-10)
        chg = stock["change_pct"]
        if 3.5 <= chg <= 4.5:
            scores["K线形态"] = 8
        elif 3.0 <= chg <= 5.0:
            scores["K线形态"] = 7
        elif chg > 5.0:
            scores["K线形态"] = 5
        else:
            scores["K线形态"] = 6
        
        # 4. 股性活跃度 (1-10)
        is_hot = code in hot_codes
        tags = block_info.get(code, [])
        tags_str = " ".join(tags)
        ai_related = any(kw in tags_str for kw in ["AI", "算力", "半导体", "芯片", "光模块", "PCB", "液冷", "人工智能", "消费电子", "集成电路"])
        if is_hot and ai_related:
            scores["股性活跃度"] = 9
        elif is_hot:
            scores["股性活跃度"] = 7
        elif ai_related:
            scores["股性活跃度"] = 7
        else:
            scores["股性活跃度"] = 5
        
        # 5. 基本面安全度 (1-10)
        pe = q.get("pe_ttm", 0)
        if pe > 0 and pe < 30:
            scores["基本面安全度"] = 8
        elif pe >= 30 and pe < 60:
            scores["基本面安全度"] = 6
        elif pe >= 60 and pe < 100:
            scores["基本面安全度"] = 4
        elif pe >= 100:
            scores["基本面安全度"] = 2
        else:
            scores["基本面安全度"] = 3  # 亏损股
        
        # 6. 次日溢价预期 (1-10)
        if ai_related and is_hot:
            scores["次日溢价预期"] = 8
        elif ai_related:
            scores["次日溢价预期"] = 7
        elif is_hot:
            scores["次日溢价预期"] = 6
        else:
            scores["次日溢价预期"] = 4
        
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
            "fail_items": [k for k, val in v["checks"].items() if val == "不通过"],
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
    
    sorted_stocks = sorted(scoring_results.items(), key=lambda x: x[1]["total"], reverse=True)
    
    # 推荐买入
    print("\n### 🏆 推荐买入标的")
    if market_direction == "下行":
        print("  ⚠️ 大盘14:30复检不通过，按规则应当日空仓！以下仅供参考")
    
    recommended = [(code, data) for code, data in sorted_stocks if data["passed_verification"]]
    if recommended:
        for code, data in recommended:
            stock_info = next(s for s in STOCKS if s["code"] == code)
            q = quotes.get(code, {})
            price = q.get("price", 0)
            buy_low = price * 0.995 if price else 0
            buy_high = price * 1.005 if price else 0
            print(f"\n  📌 {stock_info['name']}({code}) 综合得分: {data['total']:.2f}/10")
            print(f"     建议买入价: {buy_low:.2f}-{buy_high:.2f}")
            print(f"     建议仓位: 20%（单只不超过20%）")
            print(f"     题材: {data.get('hot_reason', '无')}")
            for k, s in data["scores"].items():
                print(f"     {k}: {s}/10")
    else:
        print("\n  无标的通过全部5项验证")
    
    # 仅观察
    print("\n### 👀 仅观察标的（得分≥6.0但未通过验证）")
    observed = [(code, data) for code, data in sorted_stocks 
                if not data["passed_verification"] and data["total"] >= 6.0]
    if observed:
        for code, data in observed:
            stock_info = next(s for s in STOCKS if s["code"] == code)
            print(f"\n  🔍 {stock_info['name']}({code}) 得分={data['total']:.2f}")
            print(f"     未通过项: {', '.join(data['fail_items'])}")
            for k, s in data["scores"].items():
                print(f"     {k}: {s}/10")
    else:
        print("  无")
    
    # 排除
    print("\n### ❌ 排除标的（得分<6.0且未通过验证）")
    excluded = [(code, data) for code, data in sorted_stocks 
                if not data["passed_verification"] and data["total"] < 6.0]
    if excluded:
        for code, data in excluded:
            stock_info = next(s for s in STOCKS if s["code"] == code)
            print(f"\n  ✖ {stock_info['name']}({code}) 得分={data['total']:.2f}")
            print(f"     排除理由: {', '.join(data['fail_items'])}")
    else:
        print("  无")
    
    # 全局结论
    print("\n\n### 📋 全局结论")
    if market_direction == "下行":
        print("  ⚠️⚠️⚠️ 重要提醒 ⚠️⚠️⚠️")
        print("  6月18日沪指收跌0.43%，14:30后大盘15分钟线判断为下行")
        print("  按一夜持股法规则，大盘复检不通过 → 当日应空仓！")
        print("  且6月18日为端午节前最后一个交易日，节后开盘存在不确定性")
        print("  建议：空仓过端午，节后观察大盘方向再操作")
    else:
        print("  大盘复检通过，可按评分结果操作")
    
    # 如果忽略大盘复检，最优标的
    print("\n\n### 📊 假设忽略大盘复检，按评分排序的TOP5")
    for i, (code, data) in enumerate(sorted_stocks[:5]):
        stock_info = next(s for s in STOCKS if s["code"] == code)
        q = quotes.get(code, {})
        price = q.get("price", 0)
        print(f"  {i+1}. {stock_info['name']}({code}) 得分={data['total']:.2f} 价格={price}")
        print(f"     未通过项: {', '.join(data['fail_items']) if data['fail_items'] else '无'}")
        print(f"     分时强度={data['scores']['分时强度']} 量价配合={data['scores']['量价配合']} K线形态={data['scores']['K线形态']} 股性={data['scores']['股性活跃度']} 基本面={data['scores']['基本面安全度']} 次日溢价={data['scores']['次日溢价预期']}")

if __name__ == "__main__":
    main()
