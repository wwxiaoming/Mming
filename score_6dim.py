import akshare as ak
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time

candidates = [
    ("301392", "汇成真空", 172.14, 4.86, 9.83, 1.65, 172.14),
    ("300401", "花园生物", 14.56, 4.75, 8.25, 2.97, 79.16),
    ("601083", "锦江航运", 11.57, 4.71, 5.43, 2.51, 149.73),
    ("002083", "孚日股份", 10.09, 4.67, 5.17, 3.08, 95.52),
    ("002915", "中欣氟材", 22.60, 4.44, 8.73, 2.30, 75.77),
    ("600576", "祥源文旅", 6.44, 4.21, 6.26, 4.17, 67.91),
    ("300307", "慈星股份", 8.54, 4.15, 7.59, 2.03, 68.37),
    ("301528", "多浦乐", 92.30, 3.85, 8.63, 1.48, 57.13),
    ("000751", "锌业股份", 5.28, 3.73, 7.28, 2.93, 85.31),
    ("002617", "露笑科技", 8.81, 3.65, 9.07, 1.71, 168.20),
    ("600531", "豫光金铅", 13.53, 3.36, 7.02, 3.11, 163.61),
    ("688721", "龙图光罩", 50.51, 3.27, 9.83, 1.72, 67.43),
    ("301667", "纳百川", 78.78, 3.24, 9.38, 1.60, 87.97),
    ("300774", "倍杰特", 13.65, 3.10, 5.92, 1.42, 55.80),
]

scores = {}

for code, name, price, change_pct, turnover, vol_ratio, float_mcap in candidates:
    print(f"\n{'='*60}")
    print(f"6维评分: {name}({code})")
    print(f"{'='*60}")

    try:
        # 获取K线数据
        end_date = datetime.now().strftime("%Y%m%d")
        start_date = (datetime.now() - timedelta(days=60)).strftime("%Y%m%d")

        df = ak.stock_zh_a_hist(symbol=code, period="daily", start_date=start_date, end_date=end_date, adjust="qfq")

        if df.empty or len(df) < 10:
            print(f"  数据不足，跳过")
            continue

        # === 维度1: 分时强度 (1-5分) ===
        last_row = df.iloc[-1]
        if last_row['成交量'] > 0:
            avg_price = last_row['成交额'] / last_row['成交量'] / 100
            price_vs_avg = (last_row['收盘'] - avg_price) / avg_price * 100
        else:
            price_vs_avg = 0

        if price_vs_avg > 1.5 and change_pct >= 4:
            score1 = 5
        elif price_vs_avg > 0.5 and change_pct >= 3.5:
            score1 = 4
        elif price_vs_avg > 0 and change_pct >= 3:
            score1 = 3
        elif price_vs_avg > -0.5:
            score1 = 2
        else:
            score1 = 1
        print(f"  维度1-分时强度: {score1}分 (收盘vs均价: {price_vs_avg:.2f}%)")

        # === 维度2: 量价配合 (1-5分) ===
        recent_5 = df.tail(5)
        vols = recent_5['成交量'].values
        vol_trend = "递增" if all(vols[i] >= vols[i-1]*0.8 for i in range(1, len(vols))) else "波动"

        if vol_ratio >= 3.0 and vol_trend == "递增":
            score2 = 5
        elif vol_ratio >= 2.5:
            score2 = 4
        elif vol_ratio >= 2.0:
            score2 = 3
        elif vol_ratio >= 1.5:
            score2 = 2
        else:
            score2 = 1
        print(f"  维度2-量价配合: {score2}分 (量比={vol_ratio:.2f} 量能趋势={vol_trend})")

        # === 维度3: K线形态 (1-5分) ===
        if len(df) >= 20:
            df_calc = df.copy()
            df_calc['MA5'] = df_calc['收盘'].rolling(5).mean()
            df_calc['MA10'] = df_calc['收盘'].rolling(10).mean()
            df_calc['MA20'] = df_calc['收盘'].rolling(20).mean()

            last = df_calc.iloc[-1]
            bullish = last['MA5'] > last['MA10'] > last['MA20']
            ma5_rising = df_calc.iloc[-1]['MA5'] > df_calc.iloc[-2]['MA5']

            high_20 = df_calc['最高'].tail(20).max()
            distance_to_high = (high_20 - last['收盘']) / last['收盘'] * 100

            if bullish and ma5_rising and distance_to_high < 2:
                score3 = 5
            elif bullish and ma5_rising:
                score3 = 4
            elif bullish:
                score3 = 3
            elif last['收盘'] > last['MA5']:
                score3 = 2
            else:
                score3 = 1
            print(f"  维度3-K线形态: {score3}分 (多头={bullish} MA5升={ma5_rising} 距高点={distance_to_high:.1f}%)")
        else:
            score3 = 2
            print(f"  维度3-K线形态: {score3}分 (数据不足)")

        # === 维度4: 股性活跃度 (1-5分) ===
        recent_20 = df.tail(20)
        limit_up_count = 0
        for _, row in recent_20.iterrows():
            threshold = 19.5 if code.startswith('68') else 9.8
            if row['涨跌幅'] >= threshold:
                limit_up_count += 1

        if limit_up_count >= 3:
            score4 = 5
        elif limit_up_count >= 2:
            score4 = 4
        elif limit_up_count >= 1:
            score4 = 3
        elif turnover >= 8:
            score4 = 2
        else:
            score4 = 1
        print(f"  维度4-股性活跃度: {score4}分 (20天涨停{limit_up_count}次 换手={turnover}%)")

        # === 维度5: 基本面安全度 (1-5分) ===
        is_st = 'ST' in name

        if is_st:
            score5 = 1
        elif float_mcap >= 100 and change_pct <= 4.5:
            score5 = 5
        elif float_mcap >= 80:
            score5 = 4
        elif float_mcap >= 60:
            score5 = 3
        elif float_mcap >= 50:
            score5 = 2
        else:
            score5 = 1
        print(f"  维度5-基本面安全度: {score5}分 (流通市值={float_mcap}亿 ST={is_st})")

        # === 维度6: 次日溢价预期 (1-5分) ===
        golden_range = 1 - abs(change_pct - 4) / 2
        vol_score = min(vol_ratio / 3, 1)

        premium = golden_range * 0.4 + vol_score * 0.3 + (score4 / 5) * 0.3

        if premium >= 0.8:
            score6 = 5
        elif premium >= 0.65:
            score6 = 4
        elif premium >= 0.5:
            score6 = 3
        elif premium >= 0.35:
            score6 = 2
        else:
            score6 = 1
        print(f"  维度6-次日溢价预期: {score6}分 (黄金区间得分={golden_range:.2f} 量比得分={vol_score:.2f} 活跃度得分={score4/5:.2f})")

        total_score = score1 + score2 + score3 + score4 + score5 + score6
        print(f"\n  ★ 总分: {total_score}/30")

        scores[code] = {
            "name": name,
            "price": price,
            "change_pct": change_pct,
            "turnover": turnover,
            "vol_ratio": vol_ratio,
            "float_mcap": float_mcap,
            "score1": score1,
            "score2": score2,
            "score3": score3,
            "score4": score4,
            "score5": score5,
            "score6": score6,
            "total_score": total_score,
            "limit_up_count": limit_up_count,
        }

        time.sleep(0.5)

    except Exception as e:
        print(f"  ❌评分失败: {e}")
        scores[code] = {"name": name, "error": str(e), "total_score": 0}

# === 排序输出 ===
print(f"\n\n{'='*80}")
print(f"6维评分排名（按总分降序）")
print(f"{'='*80}")

sorted_scores = sorted(scores.items(), key=lambda x: x[1].get("total_score", 0), reverse=True)

print(f"\n{'排名':<4} {'代码':<8} {'名称':<8} {'分时':<4} {'量价':<4} {'K线':<4} {'股性':<4} {'基本面':<4} {'溢价':<4} {'总分':<6} {'建议'}")
print("-" * 80)

for i, (code, s) in enumerate(sorted_scores, 1):
    if "error" in s:
        print(f"{i:<4} {code:<8} {s['name']:<8} 数据异常")
        continue

    if s["total_score"] >= 24:
        suggestion = "★推荐买入"
    elif s["total_score"] >= 18:
        suggestion = "○仅观察"
    else:
        suggestion = "✕排除"

    print(f"{i:<4} {code:<8} {s['name']:<8} {s['score1']:<4} {s['score2']:<4} {s['score3']:<4} {s['score4']:<4} {s['score5']:<4} {s['score6']:<4} {s['total_score']:<6} {suggestion}")

# 分类输出
print(f"\n\n=== 推荐买入标的（总分≥24）===")
for code, s in sorted_scores:
    if s.get("total_score", 0) >= 24:
        print(f"  ★ {s['name']}({code}): {s['total_score']}分")

print(f"\n=== 仅观察标的（总分18-23）===")
for code, s in sorted_scores:
    if 18 <= s.get("total_score", 0) < 24:
        print(f"  ○ {s['name']}({code}): {s['total_score']}分")

print(f"\n=== 排除标的（总分<18）===")
for code, s in sorted_scores:
    if s.get("total_score", 0) < 18:
        reason = []
        if s.get("score4", 0) <= 2: reason.append("股性不活跃")
        if s.get("score3", 0) <= 2: reason.append("K线形态差")
        if s.get("score2", 0) <= 2: reason.append("量价配合弱")
        print(f"  ✕ {s['name']}({code}): {s.get('total_score',0)}分 - {', '.join(reason)}")
