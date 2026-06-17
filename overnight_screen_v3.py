#!/usr/bin/env python3
"""
一夜持股法 - A股超短线选股筛选脚本 (最终版v3)
日期: 2026-06-17
使用腾讯行情API + 腾讯K线API(计算MA/涨停/量能)
"""

import urllib.request
import json
import time

# ============================================================
# 腾讯财经API - 行情数据
# ============================================================

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

    all_results = {}
    for i in range(0, len(prefixed), 50):
        batch = prefixed[i:i+50]
        url = "https://qt.gtimg.cn/q=" + ",".join(batch)
        req = urllib.request.Request(url)
        req.add_header("User-Agent", "Mozilla/5.0")
        try:
            resp = urllib.request.urlopen(req, timeout=10)
            data = resp.read().decode("gbk")
        except:
            continue

        for line in data.strip().split(";"):
            if not line.strip() or "=" not in line or '"' not in line:
                continue
            key = line.split("=")[0].split("_")[-1]
            vals = line.split('"')[1].split("~")
            if len(vals) < 53:
                continue
            code = key[2:]
            try:
                all_results[code] = {
                    "name": vals[1],
                    "price": float(vals[3]) if vals[3] else 0,
                    "last_close": float(vals[4]) if vals[4] else 0,
                    "change_pct": float(vals[32]) if vals[32] else 0,
                    "turnover_pct": float(vals[38]) if vals[38] else 0,
                    "pe_ttm": float(vals[39]) if vals[39] else 0,
                    "mcap_yi": float(vals[44]) if vals[44] else 0,
                    "float_mcap_yi": float(vals[45]) if vals[45] else 0,
                    "pb": float(vals[46]) if vals[46] else 0,
                    "limit_up": float(vals[47]) if vals[47] else 0,
                    "vol_ratio": float(vals[49]) if vals[49] else 0,
                }
            except (ValueError, IndexError):
                continue

    return all_results


# ============================================================
# 腾讯K线API - 获取日K线数据
# ============================================================

def tencent_kline(code, count=30):
    """获取腾讯前复权日K线"""
    if code.startswith(("6", "9")):
        prefix = "sh"
    elif code.startswith("8"):
        prefix = "bj"
    else:
        prefix = "sz"

    url = f"https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?_var=kline_dayqfq&param={prefix}{code},day,,,{count},qfq"
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "Mozilla/5.0")
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        data = resp.read().decode("utf-8")
    except:
        return []

    # 解析: kline_dayqfq={"code":0,...}
    var_name = "kline_dayqfq="
    idx = data.find(var_name)
    if idx < 0:
        return []
    json_str = data[idx + len(var_name):]
    try:
        d = json.loads(json_str)
    except:
        return []

    # 提取K线数据
    stock_data = d.get("data", {}).get(f"{prefix}{code}", {})
    klines = stock_data.get("qfqday", [])
    if not klines:
        klines = stock_data.get("day", [])

    # 格式: [日期, 开, 收, 高, 低, 成交量(手)]
    result = []
    for k in klines:
        try:
            result.append({
                "date": k[0],
                "open": float(k[1]),
                "close": float(k[2]),
                "high": float(k[3]),
                "low": float(k[4]),
                "vol": float(k[5]),  # 手
            })
        except (ValueError, IndexError):
            continue

    return result


def check_kline_conditions(code):
    """综合检查: 均线多头 + 20天涨停 + 量能放大"""
    klines = tencent_kline(code, count=30)

    result = {
        "ma_bullish": False,
        "ma5": 0, "ma10": 0, "ma20": 0,
        "limit_up_20d": False,
        "limit_up_count": 0,
        "vol_increasing": False,
    }

    if len(klines) < 20:
        return result

    # 计算MA
    closes = [k["close"] for k in klines]
    vols = [k["vol"] for k in klines]

    # MA5/MA10/MA20
    if len(closes) >= 5:
        result["ma5"] = round(sum(closes[-5:]) / 5, 2)
    if len(closes) >= 10:
        result["ma10"] = round(sum(closes[-10:]) / 10, 2)
    if len(closes) >= 20:
        result["ma20"] = round(sum(closes[-20:]) / 20, 2)

    # 均线多头: MA5 > MA10 > MA20
    if result["ma5"] > result["ma10"] > result["ma20"] > 0:
        result["ma_bullish"] = True

    # 检查20天涨停
    limit_up_count = 0
    for i in range(max(0, len(klines) - 20), len(klines)):
        k = klines[i]
        if i > 0:
            prev_close = klines[i-1]["close"]
            if prev_close > 0:
                pct = (k["close"] - prev_close) / prev_close * 100
                if code.startswith("3") or code.startswith("68"):
                    if pct >= 19.5:
                        limit_up_count += 1
                else:
                    if pct >= 9.5:
                        limit_up_count += 1

    result["limit_up_count"] = limit_up_count
    result["limit_up_20d"] = limit_up_count > 0

    # 量能放大: 最近3-5天量能递增
    if len(vols) >= 3:
        recent_vols = vols[-3:]
        increasing = sum(1 for i in range(1, len(recent_vols)) if recent_vols[i] > recent_vols[i-1])
        result["vol_increasing"] = increasing >= 2

    return result


def check_vwap(code):
    """用腾讯分时数据检查站均价线上方"""
    if code.startswith(("6", "9")):
        prefix = "sh"
    elif code.startswith("8"):
        prefix = "bj"
    else:
        prefix = "sz"

    url = f"https://web.ifzq.gtimg.cn/appstock/app/minute/query?_var=min_data&code={prefix}{code}"
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "Mozilla/5.0")
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        data = resp.read().decode("utf-8")
    except:
        return None, None

    var_name = "min_data="
    idx = data.find(var_name)
    if idx < 0:
        return None, None
    json_str = data[idx + len(var_name):]
    try:
        d = json.loads(json_str)
    except:
        return None, None

    # 提取分时数据
    stock_data = d.get("data", {}).get(f"{prefix}{code}", {})
    minute_data = stock_data.get("data", [])

    if not minute_data:
        return None, None

    total_amount = 0
    total_vol = 0
    above_count = 0
    total_count = 0

    for item in minute_data:
        try:
            # 格式: [时间, 价格, 均价, 成交量]
            if len(item) >= 4:
                price = float(item[1])
                vol = float(item[3])
                # 用累计计算VWAP
                total_amount += price * vol
                total_vol += vol
                if total_vol > 0:
                    vwap = total_amount / total_vol
                    if price >= vwap:
                        above_count += 1
                    total_count += 1
        except (ValueError, IndexError):
            continue

    if total_count == 0:
        return None, None
    ratio = above_count / total_count
    return ratio >= 0.7, round(ratio * 100, 1)


# ============================================================
# 主流程
# ============================================================

def main():
    print("=" * 80)
    print("一夜持股法 - A股超短线选股筛选")
    print("日期: 2026-06-17")
    print("=" * 80)

    # Step 1: 生成代码池
    print("\n[Step 1] 生成A股代码池...")
    all_codes = []

    # 沪市主板
    for prefix in [600, 601, 603, 605]:
        for i in range(0, 1000):
            all_codes.append(f"{prefix}{str(i).zfill(3)}")

    # 科创板
    for i in range(0, 1000):
        all_codes.append(f"688{str(i).zfill(3)}")

    # 深市主板
    for prefix in ["000", "001", "002", "003"]:
        for i in range(0, 1000):
            all_codes.append(f"{prefix}{str(i).zfill(3)}")

    # 创业板
    for prefix in [300, 301]:
        for i in range(0, 1000):
            all_codes.append(f"{prefix}{str(i).zfill(3)}")

    # 去重
    all_codes = list(set(all_codes))
    print(f"  代码池: {len(all_codes)} 只")

    # Step 2: 腾讯API批量获取行情
    print(f"\n[Step 2] 腾讯API批量获取行情数据...")
    all_tq = {}
    batch_size = 50
    total_batches = (len(all_codes) + batch_size - 1) // batch_size

    for i in range(0, len(all_codes), batch_size):
        batch = all_codes[i:i+batch_size]
        batch_num = i // batch_size + 1
        if batch_num % 50 == 0:
            print(f"  进度: {batch_num}/{total_batches} 批, 已获取 {len(all_tq)} 只有效数据")

        tq = tencent_quote(batch)
        all_tq.update(tq)

    print(f"  获取到 {len(all_tq)} 只股票行情数据")

    # Step 3: 筛选条件1+3+4+5
    print(f"\n[Step 3] 筛选: 涨幅3-5% + 量比>1.4 + 换手5-10% + 流通市值50-200亿...")
    candidates = []

    for code, q in all_tq.items():
        name = q.get("name", "")
        change_pct = q.get("change_pct", 0)
        turnover = q.get("turnover_pct", 0)
        float_mcap = q.get("float_mcap_yi", 0)
        vol_ratio = q.get("vol_ratio", 0)
        pe = q.get("pe_ttm", 0)
        pb = q.get("pb", 0)
        price = q.get("price", 0)

        # 排除ST/退市/北交所
        if "ST" in name or "st" in name or "退" in name:
            continue
        if code.startswith("8") or code.startswith("4"):
            continue

        # 条件1: 涨幅3%-5%
        if change_pct < 3 or change_pct > 5:
            continue
        # 条件3: 量比>1.4
        if vol_ratio < 1.4:
            continue
        # 条件4: 换手率5%-10%
        if turnover < 5 or turnover > 10:
            continue
        # 条件5: 流通市值50-200亿
        if float_mcap < 50 or float_mcap > 200:
            continue

        candidates.append({
            "code": code,
            "name": name,
            "price": price,
            "change_pct": round(change_pct, 2),
            "turnover_pct": round(turnover, 2),
            "vol_ratio": round(vol_ratio, 2),
            "float_mcap_yi": round(float_mcap, 1),
            "pe_ttm": round(pe, 1),
            "pb": round(pb, 2),
        })

    print(f"  筛选后: {len(candidates)} 只")
    for s in candidates:
        print(f"    {s['code']} {s['name']}: 涨幅{s['change_pct']:.2f}% 换手{s['turnover_pct']:.2f}% 量比{s['vol_ratio']:.2f} 流通市值{s['float_mcap_yi']:.1f}亿 PE={s['pe_ttm']} PB={s['pb']}")

    if not candidates:
        print("[WARN] 无候选股票")
        return

    # Step 4: 腾讯K线深度检查
    print(f"\n[Step 4] 腾讯K线深度检查: 20天涨停 + 均线多头 + 量能放大 + 分时VWAP...")

    final = []
    for s in candidates:
        code = s["code"]
        name = s["name"]
        print(f"\n  检查 {code} {name}...")

        # K线分析
        kline_result = check_kline_conditions(code)
        s["ma_bullish"] = kline_result["ma_bullish"]
        s["ma5"] = kline_result["ma5"]
        s["ma10"] = kline_result["ma10"]
        s["ma20"] = kline_result["ma20"]
        s["limit_up_20d"] = kline_result["limit_up_20d"]
        s["limit_up_count"] = kline_result["limit_up_count"]
        s["vol_increasing"] = kline_result["vol_increasing"]

        print(f"    20天涨停: {'✓' if kline_result['limit_up_20d'] else '✗'} ({kline_result['limit_up_count']}次)")
        print(f"    均线多头: {'✓' if kline_result['ma_bullish'] else '✗'} MA5={kline_result['ma5']} MA10={kline_result['ma10']} MA20={kline_result['ma20']}")
        print(f"    量能放大: {'✓' if kline_result['vol_increasing'] else '✗'}")

        # 分时VWAP
        above_vwap, vwap_pct = check_vwap(code)
        s["above_vwap"] = above_vwap
        s["vwap_pct"] = vwap_pct
        if above_vwap is not None:
            print(f"    分时VWAP: {'✓' if above_vwap else '✗'} ({vwap_pct}%)")
        else:
            print(f"    分时VWAP: 数据不可用")

        # 统计通过条件数
        passed = sum([
            3 <= s["change_pct"] <= 5,
            s["limit_up_20d"],
            s["vol_ratio"] > 1.4,
            5 <= s["turnover_pct"] <= 10,
            50 <= s["float_mcap_yi"] <= 200,
            s["vol_increasing"],
            s["ma_bullish"],
            above_vwap if above_vwap is not None else True,
        ])
        s["passed_count"] = passed
        final.append(s)

        time.sleep(0.2)

    # 输出最终结果
    print("\n" + "=" * 80)
    print("最终候选池")
    print("=" * 80)

    final.sort(key=lambda x: x["passed_count"], reverse=True)

    perfect = [s for s in final if s["passed_count"] >= 7]
    good = [s for s in final if 5 <= s["passed_count"] < 7]
    partial = [s for s in final if s["passed_count"] < 5]

    def print_table(stocks, title):
        print(f"\n{title}: {len(stocks)} 只")
        print("-" * 130)
        header = f"{'代码':<8} {'名称':<10} {'现价':<8} {'涨幅%':<8} {'换手%':<8} {'量比':<6} {'流通市值':<10} {'PE':<8} {'PB':<6} {'涨停':<8} {'均线':<6} {'量能':<6} {'VWAP':<10} {'通过'}"
        print(header)
        print("-" * 130)
        for s in stocks:
            limit_str = f"✓({s['limit_up_count']})" if s.get("limit_up_20d") else "✗"
            ma_str = "✓" if s.get("ma_bullish") else "✗"
            vol_str = "✓" if s.get("vol_increasing") else "✗"
            vwap_str = f"✓({s.get('vwap_pct','-')}%)" if s.get("above_vwap") else ("✗" if s.get("above_vwap") is False else "N/A")
            print(f"{s['code']:<8} {s['name']:<10} {s.get('price',0):<8.2f} {s['change_pct']:<8.2f} {s['turnover_pct']:<8.2f} {s['vol_ratio']:<6.2f} {s['float_mcap_yi']:<10.1f} {s.get('pe_ttm',0):<8.1f} {s.get('pb',0):<6.2f} {limit_str:<8} {ma_str:<6} {vol_str:<6} {vwap_str:<10} {s['passed_count']}/8")

    print_table(perfect, "★★★ 高度符合 (≥7条)")
    print_table(good, "★★ 部分符合 (5-6条)")
    print_table(partial, "★ 待观察 (<5条)")

    # JSON输出
    print("\n\n[JSON格式候选池]")
    output = []
    for s in final:
        output.append({
            "code": s["code"],
            "name": s["name"],
            "price": s.get("price", 0),
            "change_pct": s["change_pct"],
            "turnover_pct": s["turnover_pct"],
            "vol_ratio": s.get("vol_ratio", 0),
            "float_mcap_yi": s["float_mcap_yi"],
            "pe_ttm": s.get("pe_ttm", 0),
            "pb": s.get("pb", 0),
            "limit_up_20d": s.get("limit_up_20d", False),
            "limit_up_count": s.get("limit_up_count", 0),
            "ma_bullish": s.get("ma_bullish", False),
            "ma5": s.get("ma5"),
            "ma10": s.get("ma10"),
            "ma20": s.get("ma20"),
            "vol_increasing": s.get("vol_increasing", False),
            "above_vwap": s.get("above_vwap"),
            "vwap_pct": s.get("vwap_pct"),
            "passed_count": s.get("passed_count", 0),
        })
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
