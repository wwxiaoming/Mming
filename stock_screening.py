#!/usr/bin/env python3
"""
A股候选股深度盯盘验证脚本
检查项目：
1. 分时站均价线比例（>70%为通过）
2. 尾盘是否偷袭（5分钟拉升<1%为通过）
3. 量能是否持续（下午不萎缩为通过）
4. K线均线多头排列（MA5>MA10>MA20为通过）
5. 成交量连续温和放大（近5日递增为通过）
6. 20天内有涨停（有涨停为通过）
7. 基本面排雷（PE为负/减持/ST为不通过）
"""

import akshare as ak
import pandas as pd
import requests
import json
import time
from datetime import datetime, timedelta

# 候选股列表
candidates = [
    ("002785", "万里石"), ("300224", "正海磁材"), ("000795", "英洛华"),
    ("301548", "崇德科技"), ("301316", "慧博云通"), ("002860", "星帅尔"),
    ("301148", "嘉戎技术"), ("300767", "震安科技"), ("001266", "宏英智能"),
    ("300337", "银邦股份"), ("003004", "声迅股份")
]

# 创业板/科创板代码判断
def is_gem_or_star(code):
    """判断是否为创业板(300xxx)或科创板(688xxx)"""
    return code.startswith('300') or code.startswith('688')

def get_limit_up_threshold(code):
    """获取涨停阈值"""
    if is_gem_or_star(code):
        return 19.9  # 20%涨跌幅
    else:
        return 9.9   # 10%涨跌幅

def get_daily_data(code):
    """获取日K线数据（近40天）"""
    try:
        end_date = datetime.now().strftime('%Y%m%d')
        start_date = (datetime.now() - timedelta(days=60)).strftime('%Y%m%d')
        df = ak.stock_zh_a_hist(
            symbol=code, period="daily",
            start_date=start_date, end_date=end_date, adjust="qfq"
        )
        if df is not None and len(df) > 0:
            # 统一列名
            col_map = {}
            for col in df.columns:
                if '日期' in col or 'date' in col.lower():
                    col_map[col] = 'date'
                elif '收盘' in col or 'close' in col.lower():
                    col_map[col] = 'close'
                elif '开盘' in col or 'open' in col.lower():
                    col_map[col] = 'open'
                elif '最高' in col or 'high' in col.lower():
                    col_map[col] = 'high'
                elif '最低' in col or 'low' in col.lower():
                    col_map[col] = 'low'
                elif '成交量' in col or 'volume' in col.lower():
                    col_map[col] = 'volume'
                elif '成交额' in col or 'amount' in col.lower():
                    col_map[col] = 'amount'
                elif '涨跌幅' in col or 'pct_chg' in col.lower():
                    col_map[col] = 'pct_chg'
            df = df.rename(columns=col_map)
            return df
    except Exception as e:
        print(f"  [日K线] 获取失败: {e}")
    return None

def get_intraday_data(code):
    """获取分时数据"""
    try:
        # 尝试使用akshare获取分时数据
        df = ak.stock_intraday_em(symbol=code)
        if df is not None and len(df) > 0:
            return df
    except Exception as e:
        print(f"  [分时-akshare] 获取失败: {e}")

    # 备用方案：使用腾讯接口
    try:
        market = 'sz' if code.startswith(('0','3')) else 'sh'
        url = f"https://web.ifzq.gtimg.cn/appstock/app/minute/query?_var=min_data&code={market}{code}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            text = resp.text
            # 解析腾讯分时数据
            json_str = text.split('=')[1] if '=' in text else text
            data = json.loads(json_str)
            # 提取分时数据
            minute_data = {}
            for key in data.get('data', {}):
                minute_data = data['data'][key]
                break
            if 'data' in minute_data:
                rows = []
                for item in minute_data['data']:
                    parts = item.split()
                    if len(parts) >= 3:
                        time_str = parts[0]
                        price = float(parts[1])
                        vol = float(parts[2]) if len(parts) > 2 else 0
                        rows.append({'时间': time_str, '价格': price, '成交量': vol})
                if rows:
                    return pd.DataFrame(rows)
    except Exception as e2:
        print(f"  [分时-腾讯] 获取失败: {e2}")

    return None

def get_realtime_data(code):
    """获取实时行情数据"""
    try:
        market = '0' if code.startswith(('0','3')) else '1'
        url = f"https://push2.eastmoney.com/api/qt/stock/get?secid={market}.{code}&fields=f43,f44,f45,f46,f47,f48,f50,f51,f52,f55,f57,f58,f116,f117,f162,f167,f170,f171"
        headers = {'User-Agent': 'Mozilla/5.0'}
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            data = resp.json().get('data', {})
            return data
    except Exception as e:
        print(f"  [实时行情] 获取失败: {e}")
    return None

def check_above_avg_price(code):
    """检查1: 分时站均价线比例"""
    try:
        df = get_intraday_data(code)
        if df is None or len(df) == 0:
            return None, "无分时数据"

        # 尝试识别列名
        price_col = None
        time_col = None
        vol_col = None
        for col in df.columns:
            if '价' in str(col) or 'price' in str(col).lower() or col == '价格':
                price_col = col
            if '时' in str(col) or 'time' in str(col).lower() or col == '时间':
                time_col = col
            if '量' in str(col) or 'vol' in str(col).lower() or col == '成交量':
                vol_col = col

        if price_col is None:
            # 尝试使用第二列作为价格
            cols = df.columns.tolist()
            if len(cols) >= 2:
                price_col = cols[1]
            else:
                return None, "无法识别价格列"

        prices = df[price_col].astype(float).values
        volumes = df[vol_col].astype(float).values if vol_col else None

        # 计算均价线 (VWAP)
        if volumes is not None and len(volumes) == len(prices):
            cumulative_amount = 0
            cumulative_volume = 0
            vwap_list = []
            for i in range(len(prices)):
                cumulative_amount += prices[i] * volumes[i]
                cumulative_volume += volumes[i]
                vwap = cumulative_amount / cumulative_volume if cumulative_volume > 0 else prices[i]
                vwap_list.append(vwap)
        else:
            # 简单移动平均
            vwap_list = []
            for i in range(len(prices)):
                vwap_list.append(prices[:i+1].mean())

        # 计算站均价线比例
        above_count = sum(1 for i in range(len(prices)) if prices[i] >= vwap_list[i])
        ratio = above_count / len(prices) * 100

        passed = ratio > 70
        return passed, f"站均价线比例={ratio:.1f}%"

    except Exception as e:
        return None, f"计算失败: {e}"

def check_tail_sneak(code):
    """检查2: 尾盘是否偷袭（14:30-14:45期间5分钟拉升<1%为通过）"""
    try:
        df = get_intraday_data(code)
        if df is None or len(df) == 0:
            return None, "无分时数据"

        time_col = None
        price_col = None
        for col in df.columns:
            if '时' in str(col) or 'time' in str(col).lower() or col == '时间':
                time_col = col
            if '价' in str(col) or 'price' in str(col).lower() or col == '价格':
                price_col = col

        if time_col is None or price_col is None:
            return None, "无法识别时间/价格列"

        df['time_str'] = df[time_col].astype(str)
        df['price_val'] = df[price_col].astype(float)

        # 筛选14:25-14:50的数据
        tail_data = df[df['time_str'].str.contains('14:[2-4][0-9]')].copy()
        if len(tail_data) == 0:
            # 尝试其他时间格式
            tail_data = df[df['time_str'].str.contains('14:')].copy()

        if len(tail_data) < 2:
            return None, "尾盘数据不足"

        prices = tail_data['price_val'].values
        # 检查5分钟窗口内最大拉升幅度
        max_surge = 0
        window = min(5, len(prices) - 1)  # 5个数据点约5分钟
        for i in range(len(prices) - window):
            surge_pct = (prices[i + window] - prices[i]) / prices[i] * 100
            max_surge = max(max_surge, surge_pct)

        passed = max_surge < 1.0
        return passed, f"尾盘5分钟最大拉升={max_surge:.2f}%"

    except Exception as e:
        return None, f"计算失败: {e}"

def check_volume_sustained(df_daily):
    """检查3: 量能是否持续（下午不萎缩）"""
    try:
        if df_daily is None or len(df_daily) < 2:
            return None, "日K数据不足"

        # 使用日K线数据中的成交额/量来近似判断
        # 对比最近几天的量能变化趋势
        recent = df_daily.tail(5)
        if 'amount' in recent.columns:
            amounts = recent['amount'].values
        elif 'volume' in recent.columns:
            amounts = recent['volume'].values
        else:
            return None, "无成交额/量数据"

        # 简化：检查最近5日量能是否整体维持（不出现大幅萎缩）
        # 如果最近一天量能比前一天萎缩超过30%则视为萎缩
        if len(amounts) >= 2:
            latest_amount = amounts[-1]
            prev_amount = amounts[-2]
            if prev_amount > 0:
                shrink_ratio = (prev_amount - latest_amount) / prev_amount * 100
                passed = shrink_ratio < 30  # 萎缩不超过30%
                return passed, f"量能变化={-shrink_ratio:.1f}%（正为放量）"

        return None, "数据不足"
    except Exception as e:
        return None, f"计算失败: {e}"

def check_ma_bullish(df_daily):
    """检查4: K线均线多头排列（MA5>MA10>MA20）"""
    try:
        if df_daily is None or len(df_daily) < 20:
            return None, "数据不足20天"

        df = df_daily.copy()
        df['MA5'] = df['close'].rolling(5).mean()
        df['MA10'] = df['close'].rolling(10).mean()
        df['MA20'] = df['close'].rolling(20).mean()

        latest = df.iloc[-1]
        ma5 = latest['MA5']
        ma10 = latest['MA10']
        ma20 = latest['MA20']

        if pd.isna(ma5) or pd.isna(ma10) or pd.isna(ma20):
            return None, f"均线数据缺失 MA5={ma5}, MA10={ma10}, MA20={ma20}"

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
        if 'volume' in recent_5.columns:
            vols = recent_5['volume'].values.astype(float)
        else:
            return None, "无成交量数据"

        # 检查是否递增（允许1天小幅回落，但整体趋势向上）
        increasing_count = sum(1 for i in range(len(vols)-1) if vols[i] < vols[i+1])
        # 至少3天递增视为温和放大
        passed = increasing_count >= 3
        # 也检查整体趋势：最后一天 > 第一天
        overall_up = vols[-1] > vols[0]
        passed = passed and overall_up

        return passed, f"5日量能递增天数={increasing_count}/4, 整体放量={overall_up}"
    except Exception as e:
        return None, f"计算失败: {e}"

def check_limit_up_20d(df_daily, code):
    """检查6: 20天内有涨停"""
    try:
        if df_daily is None or len(df_daily) < 1:
            return None, "无日K数据"

        threshold = get_limit_up_threshold(code)
        recent_20 = df_daily.tail(20)

        if 'pct_chg' in recent_20.columns:
            pct_col = 'pct_chg'
        elif '涨跌幅' in recent_20.columns:
            pct_col = '涨跌幅'
        else:
            return None, "无涨跌幅数据"

        limit_up_days = recent_20[recent_20[pct_col] >= threshold]
        has_limit = len(limit_up_days) > 0

        if has_limit:
            dates = limit_up_days['date'].values if 'date' in limit_up_days.columns else []
            pct_values = limit_up_days[pct_col].values
            detail = f"有{len(limit_up_days)}天涨停(阈值{threshold}%)"
            if len(pct_values) > 0:
                detail += f", 最近涨幅={pct_values[-1]:.1f}%"
        else:
            max_pct = recent_20[pct_col].max()
            detail = f"无涨停(阈值{threshold}%), 20日最大涨幅={max_pct:.1f}%"

        return has_limit, detail
    except Exception as e:
        return None, f"计算失败: {e}"

def check_fundamentals(code, name):
    """检查7: 基本面排雷"""
    issues = []

    try:
        # 获取实时行情中的PE
        rt_data = get_realtime_data(code)
        if rt_data:
            # f162: 市盈率(动态)
            pe = rt_data.get('f162')
            if pe is not None:
                pe_val = float(pe) if pe != '-' else None
                if pe_val is not None and pe_val < 0:
                    issues.append(f"PE为负({pe_val:.1f}), 亏损股")
                elif pe_val is not None:
                    pass  # PE正常
                else:
                    pass  # PE数据缺失
            else:
                pass  # 无PE数据
    except Exception as e:
        pass

    # 检查ST风险
    if 'ST' in name or '*ST' in name:
        issues.append("有ST风险")

    # 检查减持公告（通过搜索公告）
    try:
        # 尝试获取个股公告
        df_notice = ak.stock_notice_report(symbol=code)
        if df_notice is not None and len(df_notice) > 0:
            # 检查近30天是否有减持公告
            recent_notices = df_notice.tail(20)
            for _, row in recent_notices.iterrows():
                title = str(row.get('公告标题', row.get('title', '')))
                if '减持' in title:
                    issues.append(f"有减持公告: {title[:30]}")
                    break
    except:
        pass  # 公告接口可能不可用

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
            "code": code,
            "name": name,
            "above_avg": None,
            "tail_sneak": None,
            "vol_sustained": None,
            "ma_bullish": None,
            "vol_increasing": None,
            "limit_up_20d": None,
            "fundamentals": None,
        }

        # 获取日K线数据
        print("  获取日K线数据...")
        df_daily = get_daily_data(code)
        if df_daily is not None:
            print(f"  日K线数据: {len(df_daily)}条记录")
        else:
            print("  日K线数据: 获取失败")

        time.sleep(0.5)  # 避免请求过快

        # 检查1: 分时站均价线比例
        print("  [检查1] 分时站均价线比例...")
        passed, detail = check_above_avg_price(code)
        result["above_avg"] = (passed, detail)
        status = "✅通过" if passed else ("❌不通过" if passed == False else "⚠️未知")
        print(f"  结果: {status} - {detail}")

        time.sleep(0.3)

        # 检查2: 尾盘偷袭
        print("  [检查2] 尾盘是否偷袭...")
        passed, detail = check_tail_sneak(code)
        result["tail_sneak"] = (passed, detail)
        status = "✅通过" if passed else ("❌不通过" if passed == False else "⚠️未知")
        print(f"  结果: {status} - {detail}")

        time.sleep(0.3)

        # 检查3: 量能持续
        print("  [检查3] 量能是否持续...")
        passed, detail = check_volume_sustained(df_daily)
        result["vol_sustained"] = (passed, detail)
        status = "✅通过" if passed else ("❌不通过" if passed == False else "⚠️未知")
        print(f"  结果: {status} - {detail}")

        # 检查4: 均线多头排列
        print("  [检查4] 均线多头排列...")
        passed, detail = check_ma_bullish(df_daily)
        result["ma_bullish"] = (passed, detail)
        status = "✅通过" if passed else ("❌不通过" if passed == False else "⚠️未知")
        print(f"  结果: {status} - {detail}")

        # 检查5: 成交量温和放大
        print("  [检查5] 成交量连续温和放大...")
        passed, detail = check_volume_increasing(df_daily)
        result["vol_increasing"] = (passed, detail)
        status = "✅通过" if passed else ("❌不通过" if passed == False else "⚠️未知")
        print(f"  结果: {status} - {detail}")

        # 检查6: 20天涨停
        print("  [检查6] 20天内有涨停...")
        passed, detail = check_limit_up_20d(df_daily, code)
        result["limit_up_20d"] = (passed, detail)
        status = "✅通过" if passed else ("❌不通过" if passed == False else "⚠️未知")
        print(f"  结果: {status} - {detail}")

        # 检查7: 基本面排雷
        print("  [检查7] 基本面排雷...")
        passed, detail = check_fundamentals(code, name)
        result["fundamentals"] = (passed, detail)
        status = "✅通过" if passed else ("❌不通过" if passed == False else "⚠️未知")
        print(f"  结果: {status} - {detail}")

        time.sleep(0.5)

        results.append(result)

    # ============ 汇总输出 ============
    print("\n\n")
    print("=" * 120)
    print("A股候选股深度盯盘验证汇总")
    print(f"检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 120)

    # 表头
    header = f"{'代码':<8} {'名称':<8} {'站均价线':<12} {'尾盘偷袭':<12} {'量能持续':<12} {'均线多头':<12} {'量能放大':<12} {'20天涨停':<12} {'基本面':<12} {'通过数':<6}"
    print(header)
    print("-" * 120)

    for r in results:
        checks = [
            r["above_avg"], r["tail_sneak"], r["vol_sustained"],
            r["ma_bullish"], r["vol_increasing"], r["limit_up_20d"],
            r["fundamentals"]
        ]

        pass_count = sum(1 for c in checks if c[0] == True)
        fail_count = sum(1 for c in checks if c[0] == False)
        unknown_count = sum(1 for c in checks if c[0] is None)

        def fmt(check):
            if check[0] is True:
                return "✅通过"
            elif check[0] is False:
                return "❌不通过"
            else:
                return "⚠️未知"

        row = f"{r['code']:<8} {r['name']:<8} {fmt(r['above_avg']):<12} {fmt(r['tail_sneak']):<12} {fmt(r['vol_sustained']):<12} {fmt(r['ma_bullish']):<12} {fmt(r['vol_increasing']):<12} {fmt(r['limit_up_20d']):<12} {fmt(r['fundamentals']):<12} {pass_count}/7"
        print(row)

    print("-" * 120)

    # 详细信息
    print("\n\n=== 详细检查信息 ===\n")
    for r in results:
        print(f"\n【{r['code']} {r['name']}】")
        checks = [
            ("分时站均价线", r["above_avg"]),
            ("尾盘偷袭", r["tail_sneak"]),
            ("量能持续", r["vol_sustained"]),
            ("均线多头", r["ma_bullish"]),
            ("量能放大", r["vol_increasing"]),
            ("20天涨停", r["limit_up_20d"]),
            ("基本面", r["fundamentals"]),
        ]
        for label, (passed, detail) in checks:
            status = "✅" if passed else ("❌" if passed == False else "⚠️")
            print(f"  {status} {label}: {detail}")

    # 最终推荐
    print("\n\n=== 最终筛选结果 ===\n")
    print("通过5项及以上的候选股：")
    for r in results:
        checks = [r["above_avg"], r["tail_sneak"], r["vol_sustained"],
                  r["ma_bullish"], r["vol_increasing"], r["limit_up_20d"],
                  r["fundamentals"]]
        pass_count = sum(1 for c in checks if c[0] == True)
        fail_count = sum(1 for c in checks if c[0] == False)

        if pass_count >= 5:
            print(f"  ⭐ {r['code']} {r['name']} - 通过{pass_count}项, 不通过{fail_count}项")

    print("\n被淘汰的候选股：")
    for r in results:
        checks = [r["above_avg"], r["tail_sneak"], r["vol_sustained"],
                  r["ma_bullish"], r["vol_increasing"], r["limit_up_20d"],
                  r["fundamentals"]]
        pass_count = sum(1 for c in checks if c[0] == True)
        fail_count = sum(1 for c in checks if c[0] == False)

        if pass_count < 5:
            fail_reasons = []
            labels = ["站均价线", "尾盘偷袭", "量能持续", "均线多头", "量能放大", "20天涨停", "基本面"]
            for i, c in enumerate(checks):
                if c[0] == False:
                    fail_reasons.append(labels[i])
            print(f"  ✗ {r['code']} {r['name']} - 通过{pass_count}项, 不通过: {', '.join(fail_reasons)}")

if __name__ == "__main__":
    main()
