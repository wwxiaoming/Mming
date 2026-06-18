#!/usr/bin/env python3
"""
A股候选股深度盯盘验证脚本 V4 - 修复腾讯分时数据解析
"""

import pandas as pd
import requests
import json
import re
import time
from datetime import datetime, timedelta

candidates = [
    ("002785", "万里石"), ("300224", "正海磁材"), ("000795", "英洛华"),
    ("301548", "崇德科技"), ("301316", "慧博云通"), ("002860", "星帅尔"),
    ("301148", "嘉戎技术"), ("300767", "震安科技"), ("001266", "宏英智能"),
    ("300337", "银邦股份"), ("003004", "声迅股份")
]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://finance.sina.com.cn'
}

def is_gem_or_star(code):
    return code.startswith('300') or code.startswith('688')

def get_limit_up_threshold(code):
    return 19.9 if is_gem_or_star(code) else 9.9

def get_sina_market(code):
    if code.startswith('6'):
        return 'sh'
    return 'sz'

# ============ 数据获取 ============

def get_daily_data_sina(code):
    """新浪日K线"""
    try:
        market = get_sina_market(code)
        url = f"https://quotes.sina.cn/cn/api/jsonp_v2.php/var%20_{market}{code}_dklr=/CN_MarketDataService.getKLineData?symbol={market}{code}&scale=240&ma=no&datalen=40"
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code == 200:
            match = re.search(r'\((.*)\)', resp.text, re.DOTALL)
            if match:
                data = json.loads(match.group(1))
                if data and len(data) > 0:
                    df = pd.DataFrame(data)
                    for col in ['open', 'high', 'low', 'close', 'volume']:
                        if col in df.columns:
                            df[col] = pd.to_numeric(df[col], errors='coerce')
                    return df
    except Exception as e:
        print(f"  [新浪日K] 失败: {e}")
    return None

def get_intraday_tencent(code):
    """腾讯分时数据 - 修复版"""
    try:
        market = get_sina_market(code)
        url = f"https://web.ifzq.gtimg.cn/appstock/app/minute/query?_var=min_data&code={market}{code}"
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code == 200:
            text = resp.text
            json_str = text.split('=')[1].strip(';') if '=' in text else text
            data = json.loads(json_str)

            # 正确的路径: data['data'][key]['data']['data']
            stock_data = data.get('data', {})
            for key in stock_data:
                inner = stock_data[key]
                if isinstance(inner, dict) and 'data' in inner:
                    minute_inner = inner['data']
                    if isinstance(minute_inner, dict) and 'data' in minute_inner:
                        raw_list = minute_inner['data']
                        if raw_list and len(raw_list) > 0:
                            rows = []
                            for item in raw_list:
                                parts = item.split()
                                if len(parts) >= 4:
                                    rows.append({
                                        'time': parts[0],
                                        'price': float(parts[1]),
                                        'cum_volume': float(parts[2]),
                                        'cum_amount': float(parts[3]),
                                    })
                            if rows:
                                df = pd.DataFrame(rows)
                                df['volume'] = df['cum_volume'].diff().fillna(df['cum_volume'])
                                df['amount'] = df['cum_amount'].diff().fillna(df['cum_amount'])
                                return df
                break
    except Exception as e:
        print(f"  [腾讯分时] 失败: {e}")
    return None

def get_pe_from_eastmoney(code):
    """东方财富PE"""
    try:
        market = '0' if code.startswith(('0','3')) else '1'
        url = f"https://push2.eastmoney.com/api/qt/stock/get?secid={market}.{code}&fields=f57,f58,f162,f167"
        resp = requests.get(url, headers=HEADERS, timeout=10)
        if resp.status_code == 200:
            data = resp.json().get('data', {})
            return data
    except:
        pass
    return None

# ============ 检查函数 ============

def check_above_avg_price(intraday_df):
    """检查1: 分时站均价线比例（>70%为通过）"""
    try:
        if intraday_df is None or len(intraday_df) == 0:
            return None, "无分时数据"

        prices = intraday_df['price'].values
        volumes = intraday_df['volume'].values

        # 计算VWAP
        cum_amount = 0
        cum_vol = 0
        vwap_list = []
        for i in range(len(prices)):
            cum_amount += prices[i] * volumes[i]
            cum_vol += volumes[i]
            vwap = cum_amount / cum_vol if cum_vol > 0 else prices[i]
            vwap_list.append(vwap)

        above_count = sum(1 for i in range(len(prices)) if prices[i] >= vwap_list[i])
        ratio = above_count / len(prices) * 100

        passed = ratio > 70
        return passed, f"站均价线比例={ratio:.1f}%"
    except Exception as e:
        return None, f"计算失败: {e}"

def check_tail_sneak(intraday_df):
    """检查2: 尾盘是否偷袭（14:30-14:45期间5分钟拉升<1%为通过）"""
    try:
        if intraday_df is None or len(intraday_df) == 0:
            return None, "无分时数据"

        # 筛选14:25-14:50的数据
        tail_data = intraday_df[
            intraday_df['time'].astype(str).str.match(r'^14[2-4]\d')
        ].copy()

        if len(tail_data) < 5:
            tail_data = intraday_df[
                intraday_df['time'].astype(str).str.match(r'^14\d\d')
            ].copy()

        if len(tail_data) < 5:
            return None, "尾盘数据不足"

        prices = tail_data['price'].values
        max_surge = 0
        window = min(5, len(prices) - 1)
        for i in range(len(prices) - window):
            if prices[i] > 0:
                surge_pct = (prices[i + window] - prices[i]) / prices[i] * 100
                max_surge = max(max_surge, surge_pct)

        passed = max_surge < 1.0
        return passed, f"尾盘5分钟最大拉升={max_surge:.2f}%"
    except Exception as e:
        return None, f"计算失败: {e}"

def check_volume_sustained(intraday_df):
    """检查3: 量能是否持续（上午vs下午成交额对比）"""
    try:
        if intraday_df is None or len(intraday_df) == 0:
            return None, "无分时数据"

        morning = intraday_df[intraday_df['time'].astype(str).str.match(r'^(09|10|11)\d\d')]
        afternoon = intraday_df[intraday_df['time'].astype(str).str.match(r'^(13|14|15)\d\d')]

        if len(morning) == 0 or len(afternoon) == 0:
            return None, "上午/下午数据不足"

        morning_amount = morning['amount'].sum()
        afternoon_amount = afternoon['amount'].sum()

        if morning_amount == 0:
            return None, "上午成交额为0"

        ratio = afternoon_amount / morning_amount
        passed = ratio >= 0.5
        return passed, f"下午/上午成交额比={ratio:.2f}（>0.5为持续）"
    except Exception as e:
        return None, f"计算失败: {e}"

def check_ma_bullish(df_daily):
    """检查4: 均线多头排列（MA5>MA10>MA20）"""
    try:
        if df_daily is None or len(df_daily) < 20:
            return None, "数据不足20天"

        close_col = 'close' if 'close' in df_daily.columns else None
        if close_col is None:
            return None, "无收盘价列"

        df = df_daily.copy()
        df['MA5'] = df[close_col].rolling(5).mean()
        df['MA10'] = df[close_col].rolling(10).mean()
        df['MA20'] = df[close_col].rolling(20).mean()

        latest = df.iloc[-1]
        ma5, ma10, ma20 = latest['MA5'], latest['MA10'], latest['MA20']

        if pd.isna(ma5) or pd.isna(ma10) or pd.isna(ma20):
            return None, "均线数据缺失"

        passed = ma5 > ma10 > ma20
        return passed, f"MA5={ma5:.2f}, MA10={ma10:.2f}, MA20={ma20:.2f}"
    except Exception as e:
        return None, f"计算失败: {e}"

def check_volume_increasing(df_daily):
    """检查5: 成交量连续温和放大（近5日递增）"""
    try:
        if df_daily is None or len(df_daily) < 5:
            return None, "数据不足5天"

        recent_5 = df_daily.tail(5)
        vol_col = 'volume' if 'volume' in recent_5.columns else None
        if vol_col is None:
            return None, "无成交量列"

        vols = recent_5[vol_col].astype(float).values
        increasing_count = sum(1 for i in range(len(vols)-1) if vols[i] < vols[i+1])
        overall_up = vols[-1] > vols[0]
        passed = increasing_count >= 3 and overall_up

        return passed, f"5日量能递增天数={increasing_count}/4, 整体放量={overall_up}"
    except Exception as e:
        return None, f"计算失败: {e}"

def check_limit_up_20d(df_daily, code):
    """检查6: 20天内有涨停"""
    try:
        if df_daily is None or len(df_daily) < 2:
            return None, "无日K数据"

        threshold = get_limit_up_threshold(code)
        recent_20 = df_daily.tail(20)

        close_col = 'close' if 'close' in recent_20.columns else None
        if close_col is None:
            return None, "无收盘价列"

        closes = recent_20[close_col].astype(float).values
        pcts = []
        for i in range(len(closes)):
            if i == 0:
                pcts.append(0)
            else:
                if closes[i-1] > 0:
                    pcts.append((closes[i] - closes[i-1]) / closes[i-1] * 100)
                else:
                    pcts.append(0)

        limit_up_days = sum(1 for p in pcts if p >= threshold)
        has_limit = limit_up_days > 0
        max_pct = max(pcts) if pcts else 0

        if has_limit:
            detail = f"有{limit_up_days}天涨停(阈值{threshold}%), 20日最大涨幅={max_pct:.1f}%"
        else:
            detail = f"无涨停(阈值{threshold}%), 20日最大涨幅={max_pct:.1f}%"

        return has_limit, detail
    except Exception as e:
        return None, f"计算失败: {e}"

def check_fundamentals(code, name):
    """检查7: 基本面排雷"""
    issues = []

    if 'ST' in name or '*ST' in name:
        issues.append("有ST风险")

    # PE检查
    try:
        em_data = get_pe_from_eastmoney(code)
        if em_data:
            pe_raw = em_data.get('f162')
            if pe_raw is not None and pe_raw != '-':
                pe_val = float(pe_raw)
                if pe_val < 0:
                    issues.append(f"PE为负({pe_val:.1f}), 亏损股")
    except:
        pass

    # akshare补充
    if not issues:
        try:
            import akshare as ak
            df_info = ak.stock_individual_info_em(symbol=code)
            if df_info is not None and len(df_info) > 0:
                for _, row in df_info.iterrows():
                    item = str(row.iloc[0]) if len(row) > 0 else ''
                    value = str(row.iloc[1]) if len(row) > 1 else ''
                    if '市盈率' in item and '动' in item:
                        try:
                            pe_val = float(value)
                            if pe_val < 0:
                                issues.append(f"PE为负({pe_val:.1f}), 亏损股")
                        except:
                            pass
                    if 'ST' in value or '退' in value:
                        issues.append(f"有ST/退市风险: {value}")
        except:
            pass

    # 减持公告
    try:
        import akshare as ak
        df_notice = ak.stock_notice_report(symbol=code)
        if df_notice is not None and len(df_notice) > 0:
            recent = df_notice.tail(10)
            for _, row in recent.iterrows():
                title = str(row.get('公告标题', row.get('title', '')))
                if '减持' in title:
                    issues.append(f"有减持公告: {title[:30]}")
                    break
    except:
        pass

    passed = len(issues) == 0
    detail = "无风险" if passed else "; ".join(issues)
    return passed, detail

# ============ 主流程 ============
def main():
    results = []

    for code, name in candidates:
        print(f"\n{'='*60}")
        print(f"检查 {code} {name}")
        print(f"{'='*60}")

        result = {
            "code": code, "name": name,
            "above_avg": (None, ""),
            "tail_sneak": (None, ""),
            "vol_sustained": (None, ""),
            "ma_bullish": (None, ""),
            "vol_increasing": (None, ""),
            "limit_up_20d": (None, ""),
            "fundamentals": (None, ""),
        }

        # 获取日K线
        print("  获取日K线数据...")
        df_daily = get_daily_data_sina(code)
        if df_daily is not None:
            print(f"  日K线: {len(df_daily)}条")
        else:
            print("  日K线: 获取失败")
        time.sleep(0.5)

        # 获取分时数据
        print("  获取分时数据...")
        intraday_df = get_intraday_tencent(code)
        if intraday_df is not None:
            print(f"  分时数据: {len(intraday_df)}条")
        else:
            print("  分时数据: 获取失败")
        time.sleep(0.5)

        # 检查1: 分时站均价线
        print("  [检查1] 分时站均价线比例...")
        passed, detail = check_above_avg_price(intraday_df)
        result["above_avg"] = (passed, detail)
        print(f"  -> {'✅通过' if passed else ('❌不通过' if passed==False else '⚠️未知')}: {detail}")

        # 检查2: 尾盘偷袭
        print("  [检查2] 尾盘是否偷袭...")
        passed, detail = check_tail_sneak(intraday_df)
        result["tail_sneak"] = (passed, detail)
        print(f"  -> {'✅通过' if passed else ('❌不通过' if passed==False else '⚠️未知')}: {detail}")

        # 检查3: 量能持续
        print("  [检查3] 量能是否持续...")
        passed, detail = check_volume_sustained(intraday_df)
        result["vol_sustained"] = (passed, detail)
        print(f"  -> {'✅通过' if passed else ('❌不通过' if passed==False else '⚠️未知')}: {detail}")

        # 检查4: 均线多头
        print("  [检查4] 均线多头排列...")
        passed, detail = check_ma_bullish(df_daily)
        result["ma_bullish"] = (passed, detail)
        print(f"  -> {'✅通过' if passed else ('❌不通过' if passed==False else '⚠️未知')}: {detail}")

        # 检查5: 量能放大
        print("  [检查5] 成交量连续温和放大...")
        passed, detail = check_volume_increasing(df_daily)
        result["vol_increasing"] = (passed, detail)
        print(f"  -> {'✅通过' if passed else ('❌不通过' if passed==False else '⚠️未知')}: {detail}")

        # 检查6: 20天涨停
        print("  [检查6] 20天内有涨停...")
        passed, detail = check_limit_up_20d(df_daily, code)
        result["limit_up_20d"] = (passed, detail)
        print(f"  -> {'✅通过' if passed else ('❌不通过' if passed==False else '⚠️未知')}: {detail}")

        # 检查7: 基本面
        print("  [检查7] 基本面排雷...")
        passed, detail = check_fundamentals(code, name)
        result["fundamentals"] = (passed, detail)
        print(f"  -> {'✅通过' if passed else ('❌不通过' if passed==False else '⚠️未知')}: {detail}")

        time.sleep(0.5)
        results.append(result)

    # ============ 汇总 ============
    print("\n\n")
    print("=" * 140)
    print("A股候选股深度盯盘验证汇总")
    print(f"检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 140)

    header = f"{'代码':<8} {'名称':<8} {'站均价线':<16} {'尾盘偷袭':<16} {'量能持续':<16} {'均线多头':<16} {'量能放大':<16} {'20天涨停':<16} {'基本面':<16} {'通过/7':<8}"
    print(header)
    print("-" * 140)

    for r in results:
        checks = [r["above_avg"], r["tail_sneak"], r["vol_sustained"],
                  r["ma_bullish"], r["vol_increasing"], r["limit_up_20d"],
                  r["fundamentals"]]
        pass_count = sum(1 for c in checks if c[0] == True)

        def fmt(check):
            if check[0] is True: return "✅通过"
            elif check[0] is False: return "❌不通过"
            else: return "⚠️未知"

        row = (f"{r['code']:<8} {r['name']:<8} {fmt(r['above_avg']):<16} "
               f"{fmt(r['tail_sneak']):<16} {fmt(r['vol_sustained']):<16} "
               f"{fmt(r['ma_bullish']):<16} {fmt(r['vol_increasing']):<16} "
               f"{fmt(r['limit_up_20d']):<16} {fmt(r['fundamentals']):<16} {pass_count}/7")
        print(row)

    print("-" * 140)

    # 详细信息
    print("\n\n=== 详细检查信息 ===\n")
    for r in results:
        print(f"\n【{r['code']} {r['name']}】")
        checks = [
            ("1.分时站均价线(>70%)", r["above_avg"]),
            ("2.尾盘偷袭(<1%)", r["tail_sneak"]),
            ("3.量能持续(下午不萎缩)", r["vol_sustained"]),
            ("4.均线多头(MA5>MA10>MA20)", r["ma_bullish"]),
            ("5.量能温和放大(5日递增)", r["vol_increasing"]),
            ("6.20天涨停", r["limit_up_20d"]),
            ("7.基本面排雷", r["fundamentals"]),
        ]
        for label, (passed, detail) in checks:
            status = "✅" if passed else ("❌" if passed == False else "⚠️")
            print(f"  {status} {label}: {detail}")

    # 最终推荐
    print("\n\n" + "=" * 80)
    print("=== 最终筛选结果 ===")
    print("=" * 80)

    ranked = []
    for r in results:
        checks = [r["above_avg"], r["tail_sneak"], r["vol_sustained"],
                  r["ma_bullish"], r["vol_increasing"], r["limit_up_20d"],
                  r["fundamentals"]]
        pass_count = sum(1 for c in checks if c[0] == True)
        fail_count = sum(1 for c in checks if c[0] == False)
        unknown_count = sum(1 for c in checks if c[0] is None)
        ranked.append((r, pass_count, fail_count, unknown_count))

    ranked.sort(key=lambda x: (-x[1], x[2]))

    labels = ["站均价线", "尾盘偷袭", "量能持续", "均线多头", "量能放大", "20天涨停", "基本面"]

    print("\n⭐⭐⭐ 通过5项及以上（强烈推荐关注）：")
    for r, pc, fc, uc in ranked:
        if pc >= 5:
            checks = [r["above_avg"], r["tail_sneak"], r["vol_sustained"],
                      r["ma_bullish"], r["vol_increasing"], r["limit_up_20d"],
                      r["fundamentals"]]
            fail_labels = [labels[i] for i, c in enumerate(checks) if c[0] == False]
            fail_str = f", 不通过: {', '.join(fail_labels)}" if fail_labels else ""
            print(f"  ⭐ {r['code']} {r['name']} - 通过{pc}/7项{fail_str}")

    print("\n⭐⭐ 通过4项（推荐关注）：")
    for r, pc, fc, uc in ranked:
        if pc == 4:
            checks = [r["above_avg"], r["tail_sneak"], r["vol_sustained"],
                      r["ma_bullish"], r["vol_increasing"], r["limit_up_20d"],
                      r["fundamentals"]]
            fail_labels = [labels[i] for i, c in enumerate(checks) if c[0] == False]
            fail_str = f", 不通过: {', '.join(fail_labels)}" if fail_labels else ""
            print(f"  ⭐ {r['code']} {r['name']} - 通过{pc}/7项{fail_str}")

    print("\n⚠️ 通过2-3项（需进一步观察）：")
    for r, pc, fc, uc in ranked:
        if 2 <= pc < 4:
            checks = [r["above_avg"], r["tail_sneak"], r["vol_sustained"],
                      r["ma_bullish"], r["vol_increasing"], r["limit_up_20d"],
                      r["fundamentals"]]
            fail_labels = [labels[i] for i, c in enumerate(checks) if c[0] == False]
            fail_str = f", 不通过: {', '.join(fail_labels)}" if fail_labels else ""
            print(f"  ⚠️ {r['code']} {r['name']} - 通过{pc}/7项{fail_str}")

    print("\n✗ 通过不足2项（建议淘汰）：")
    for r, pc, fc, uc in ranked:
        if pc < 2:
            checks = [r["above_avg"], r["tail_sneak"], r["vol_sustained"],
                      r["ma_bullish"], r["vol_increasing"], r["limit_up_20d"],
                      r["fundamentals"]]
            fail_labels = [labels[i] for i, c in enumerate(checks) if c[0] == False]
            fail_str = f", 不通过: {', '.join(fail_labels)}" if fail_labels else ""
            print(f"  ✗ {r['code']} {r['name']} - 通过{pc}/7项{fail_str}")

if __name__ == "__main__":
    main()
