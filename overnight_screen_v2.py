#!/usr/bin/env python3
"""
一夜持股法 - A股超短线选股筛选脚本 (最终版)
日期: 2026-06-17
使用mootdx进行K线分析，腾讯API获取行情数据
"""

import urllib.request
import json
import time
import requests

# ============================================================
# 腾讯财经API - 获取全量行情数据
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
        except Exception as e:
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
# mootdx K线分析
# ============================================================

def mootdx_kline_analysis(code):
    """用mootdx获取日K线, 计算MA5/MA10/MA20, 检查涨停, 检查量能"""
    try:
        from mootdx.quotes import Quotes
        client = Quotes.factory(market='std')
        market = 1 if code.startswith("6") else 0
        klines = client.bars(symbol=code, category=4, offset=30, market=market)
        if klines is None or len(klines) == 0:
            return {"ma_bullish": False, "limit_up_20d": False, "vol_increasing": False,
                    "ma5": 0, "ma10": 0, "ma20": 0, "limit_up_count": 0}

        import pandas as pd
        df = klines.copy()

        # 计算均线
        df['ma5'] = df['close'].rolling(window=5).mean()
        df['ma10'] = df['close'].rolling(window=10).mean()
        df['ma20'] = df['close'].rolling(window=20).mean()

        # 取最新一根K线的均线值
        latest = df.iloc[-1]
        ma5 = latest.get('ma5', 0)
        ma10 = latest.get('ma10', 0)
        ma20 = latest.get('ma20', 0)

        # 均线多头: MA5 > MA10 > MA20 > 0
        ma_bullish = False
        if pd.notna(ma5) and pd.notna(ma10) and pd.notna(ma20):
            ma_bullish = ma5 > ma10 > ma20 > 0

        # 检查20天涨停
        limit_up_count = 0
        for _, row in df.tail(20).iterrows():
            close = row['close']
            last_close = row.get('last_close', 0)
            if last_close > 0:
                pct = (close - last_close) / last_close * 100
                if code.startswith("3") or code.startswith("68"):
                    if pct >= 19.5:
                        limit_up_count += 1
                else:
                    if pct >= 9.5:
                        limit_up_count += 1

        # 检查量能放大 (最近3-5天量能递增)
        vol_increasing = False
        if len(df) >= 3:
            recent_vols = df['vol'].tail(3).values
            increasing = sum(1 for i in range(1, len(recent_vols)) if recent_vols[i] > recent_vols[i-1])
            vol_increasing = increasing >= 2

        return {
            "ma_bullish": ma_bullish,
            "ma5": round(ma5, 2) if pd.notna(ma5) else 0,
            "ma10": round(ma10, 2) if pd.notna(ma10) else 0,
            "ma20": round(ma20, 2) if pd.notna(ma20) else 0,
            "limit_up_20d": limit_up_count > 0,
            "limit_up_count": limit_up_count,
            "vol_increasing": vol_increasing,
        }
    except Exception as e:
        return {"ma_bullish": False, "limit_up_20d": False, "vol_increasing": False,
                "ma5": 0, "ma10": 0, "ma20": 0, "limit_up_count": 0, "error": str(e)}


def mootdx_vwap_check(code):
    """用mootdx检查分时站均价线上方"""
    try:
        from mootdx.quotes import Quotes
        client = Quotes.factory(market='std')
        market = 1 if code.startswith("6") else 0
        klines = client.bars(symbol=code, category=7, offset=240, market=market)
        if klines is None or len(klines) == 0:
            return None, None

        total_amount = 0
        total_vol = 0
        above_count = 0
        total_count = 0

        for _, row in klines.iterrows():
            close = row.get('close', 0)
            vol = row.get('vol', 0)
            amount = row.get('amount', 0)
            if vol > 0:
                total_amount += amount
                total_vol += vol
                vwap = total_amount / total_vol / 100
                if close >= vwap:
                    above_count += 1
                total_count += 1

        if total_count == 0:
            return None, None
        ratio = above_count / total_count
        return ratio >= 0.7, round(ratio * 100, 1)
    except Exception as e:
        return None, None


# ============================================================
# 生成全A股代码池
# ============================================================

def generate_stock_codes():
    """生成A股代码池(排除北交所)"""
    codes = []

    # 沪市主板: 600000-605999, 609999
    for i in range(600000, 606000):
        codes.append(str(i))

    # 科创板: 688000-688999
    for i in range(688000, 689000):
        codes.append(str(i))

    # 深市主板: 000001-004999
    for i in range(1, 5000):
        codes.append(str(i).zfill(6))

    # 创业板: 300001-301999
    for i in range(300001, 302000):
        codes.append(str(i))

    return codes


def generate_common_codes():
    """生成常见活跃A股代码池(缩小范围加速)"""
    codes = []

    # 沪市主板活跃股
    for prefix in [600, 601, 603, 605]:
        for i in range(0, 1000):
            codes.append(f"{prefix}{str(i).zfill(3)}")

    # 科创板
    for i in range(0, 1000):
        codes.append(f"688{str(i).zfill(3)}")

    # 深市主板
    for prefix in [0, 1, 2]:
        for i in range(0, 1000):
            codes.append(f"{prefix}{str(i).zfill(3)}" if prefix > 0 else str(i).zfill(6))
    # 000xxx
    for i in range(0, 1000):
        codes.append(f"000{str(i).zfill(3)}")
    # 001xxx
    for i in range(0, 1000):
        codes.append(f"001{str(i).zfill(3)}")
    # 002xxx
    for i in range(0, 1000):
        codes.append(f"002{str(i).zfill(3)}")
    # 003xxx
    for i in range(0, 1000):
        codes.append(f"003{str(i).zfill(3)}")

    # 创业板
    for prefix in [300, 301]:
        for i in range(0, 1000):
            codes.append(f"{prefix}{str(i).zfill(3)}")

    # 去重
    seen = set()
    unique = []
    for c in codes:
        if c not in seen and len(c) == 6:
            seen.add(c)
            unique.append(c)

    return unique


# ============================================================
# 主流程
# ============================================================

def main():
    print("=" * 80)
    print("一夜持股法 - A股超短线选股筛选")
    print("日期: 2026-06-17")
    print("=" * 80)

    # Step 1: 用腾讯API批量获取全市场行情数据
    print("\n[Step 1] 生成A股代码池...")
    all_codes = generate_common_codes()
    print(f"  代码池: {len(all_codes)} 只")

    # 分批获取腾讯行情
    print(f"\n[Step 2] 腾讯API批量获取行情数据(分批,每批50只)...")
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

        # 每100批暂停一下避免被限流
        if batch_num % 100 == 0:
            time.sleep(0.5)

    print(f"  获取到 {len(all_tq)} 只股票行情数据")

    # Step 3: 筛选条件1+3+4+5: 涨幅3-5% + 量比>1.4 + 换手5-10% + 流通市值50-200亿
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
        print("[WARN] 无候选股票,尝试放宽条件...")
        # 放宽量比到>1.0
        for code, q in all_tq.items():
            name = q.get("name", "")
            change_pct = q.get("change_pct", 0)
            turnover = q.get("turnover_pct", 0)
            float_mcap = q.get("float_mcap_yi", 0)
            vol_ratio = q.get("vol_ratio", 0)
            pe = q.get("pe_ttm", 0)
            pb = q.get("pb", 0)
            price = q.get("price", 0)

            if "ST" in name or "st" in name or "退" in name:
                continue
            if code.startswith("8") or code.startswith("4"):
                continue
            if change_pct < 3 or change_pct > 5:
                continue
            if vol_ratio < 1.0:
                continue
            if turnover < 5 or turnover > 10:
                continue
            if float_mcap < 50 or float_mcap > 200:
                continue

            # 检查是否已在candidates中
            if any(c["code"] == code for c in candidates):
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
                "relaxed": True,
            })

        print(f"  放宽后: {len(candidates)} 只")
        for s in candidates:
            print(f"    {s['code']} {s['name']}: 涨幅{s['change_pct']:.2f}% 换手{s['turnover_pct']:.2f}% 量比{s['vol_ratio']:.2f} 流通市值{s['float_mcap_yi']:.1f}亿")

    if not candidates:
        print("[ERROR] 仍无候选股票")
        return

    # Step 4: mootdx深度检查
    print(f"\n[Step 4] mootdx深度检查: 20天涨停 + 均线多头 + 量能放大 + 分时VWAP...")

    # 先初始化mootdx
    try:
        from mootdx.quotes import Quotes
        # 先运行bestip
        import subprocess
        subprocess.run(["python", "-m", "mootdx", "bestip"], capture_output=True, timeout=30)
    except:
        pass

    final = []
    for s in candidates:
        code = s["code"]
        name = s["name"]
        print(f"\n  检查 {code} {name}...")

        # K线分析
        kline_result = mootdx_kline_analysis(code)
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
        above_vwap, vwap_pct = mootdx_vwap_check(code)
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

        time.sleep(0.5)

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
