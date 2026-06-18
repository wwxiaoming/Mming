#!/usr/bin/env python3
"""
A股候选股深度盯盘验证脚本 - 使用多数据源
优先使用新浪/腾讯接口，备用akshare
"""

import pandas as pd
import requests
import json
import time
import re
from datetime import datetime, timedelta

# 候选股列表
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
    """获取新浪市场前缀"""
    if code.startswith('6'):
        return 'sh'
    else:
        return 'sz'

def get_daily_data_sina(code):
    """使用新浪接口获取日K线数据"""
    try:
        market = get_sina_market(code)
        # 新浪日K线接口
        url = f"https://quotes.sina.cn/cn/api/jsonp_v2.php/var%20_{market}{code}_dklr=/CN_MarketDataService.getKLineData?symbol={market}{code}&scale=240&ma=no&datalen=40"
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code == 200:
            text = resp.text
            # 解析JSONP
            match = re.search(r'\((.*)\)', text, re.DOTALL)
            if match:
                data = json.loads(match.group(1))
                if data and len(data) > 0:
                    df = pd.DataFrame(data)
                    # 转换数据类型
                    for col in ['open', 'high', 'low', 'close', 'volume']:
                        if col in df.columns:
                            df[col] = pd.to_numeric(df[col], errors='coerce')
                    if 'ma_volume5' in df.columns:
                        df['ma_volume5'] = pd.to_numeric(df['ma_volume5'], errors='coerce')
                    return df
    except Exception as e:
        print(f"  [新浪日K] 失败: {e}")
    return None

def get_daily_data_tencent(code):
    """使用腾讯接口获取日K线"""
    try:
        market = get_sina_market(code)
        url = f"https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param={market}{code},day,,,40,qfq"
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            # 提取数据
            stock_data = data.get('data', {}).get('data', {})
            for key in stock_data:
                day_data = stock_data[key].get('day', stock_data[key].get('qfqday', []))
                if day_data and len(day_data) > 0:
                    df = pd.DataFrame(day_data, columns=['date', 'open', 'close', 'high', 'low', 'volume'])
                    for col in ['open', 'close', 'high', 'low', 'volume']:
                        df[col] = pd.to_numeric(df[col], errors='coerce')
                    return df
    except Exception as e:
        print(f"  [腾讯日K] 失败: {e}")
    return None

def get_daily_data_akshare(code):
    """使用akshare获取日K线"""
    try:
        import akshare as ak
        end_date = datetime.now().strftime('%Y%m%d')
        start_date = (datetime.now() - timedelta(days=60)).strftime('%Y%m%d')
        df = ak.stock_zh_a_hist(symbol=code, period="daily", start_date=start_date, end_date=end_date, adjust="qfq")
        if df is not None and len(df) > 0:
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
            for col in ['close', 'open', 'high', 'low', 'volume']:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            return df
    except Exception as e:
        print(f"  [akshare日K] 失败: {e}")
    return None

def get_daily_data(code):
    """多源获取日K线数据"""
    # 尝试新浪
    df = get_daily_data_sina(code)
    if df is not None and len(df) >= 20:
        print(f"  日K线(新浪): {len(df)}条")
        return df

    # 尝试腾讯
    df = get_daily_data_tencent(code)
    if df is not None and len(df) >= 20:
        print(f"  日K线(腾讯): {len(df)}条")
        return df

    # 尝试akshare
    df = get_daily_data_akshare(code)
    if df is not None and len(df) >= 20:
        print(f"  日K线(akshare): {len(df)}条")
        return df

    # 返回任何可用的数据
    if df is not None and len(df) > 0:
        print(f"  日K线(部分): {len(df)}条")
        return df

    print("  日K线: 所有源均失败")
    return None

def get_intraday_data_sina(code):
    """使用新浪接口获取分时数据"""
    try:
        market = get_sina_market(code)
        url = f"https://quotes.sina.cn/cn/api/jsonp_v2.php/var%20_{market}{code}_lc=/CN_MarketDataService.getKLineData?symbol={market}{code}&scale=5&ma=no&datalen=48"
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code == 200:
            text = resp.text
            match = re.search(r'\((.*)\)', text, re.DOTALL)
            if match:
                data = json.loads(match.group(1))
                if data and len(data) > 0:
                    return pd.DataFrame(data)
    except Exception as e:
        print(f"  [新浪分时] 失败: {e}")
    return None

def get_intraday_data_tencent(code):
    """使用腾讯接口获取分时数据"""
    try:
        market = get_sina_market(code)
        url = f"https://web.ifzq.gtimg.cn/appstock/app/minute/query?_var=min_data&code={market}{code}"
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code == 200:
            text = resp.text
            # 解析
            json_str = text.split('=')[1].strip(';') if '=' in text else text
            data = json.loads(json_str)
            for key in data.get('data', {}):
                minute_data = data['data'][key]
                break
            else:
                return None

            if 'data' in minute_data:
                rows = []
                for item in minute_data['data']:
                    parts = item.split()
                    if len(parts) >= 3:
                        rows.append({
                            'day': parts[0],
                            'price': float(parts[1]),
                            'volume': float(parts[2]) if len(parts) > 2 else 0
                        })
                if rows:
                    return pd.DataFrame(rows)
    except Exception as e:
        print(f"  [腾讯分时] 失败: {e}")
    return None

def get_intraday_data(code):
    """多源获取分时数据"""
    df = get_intraday_data_tencent(code)
    if df is not None and len(df) > 0:
        print(f"  分时数据(腾讯): {len(df)}条")
        return df

    df = get_intraday_data_sina(code)
    if df is not None and len(df) > 0:
        print(f"  分时数据(新浪5分钟): {len(df)}条")
        return df

    print("  分时数据: 所有源均失败")
    return None

def get_realtime_sina(code):
    """获取新浪实时行情"""
    try:
        market = get_sina_market(code)
        url = f"https://hq.sinajs.cn/list={market}{code}"
        headers = HEADERS.copy()
        headers['Referer'] = 'https://finance.sina.com.cn'
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            text = resp.text
            match = re.search(r'="(.*)"', text)
            if match:
                parts = match.group(1).split(',')
                if len(parts) >= 32:
                    return {
                        'name': parts[0],
                        'open': float(parts[1]) if parts[1] else 0,
                        'prev_close': float(parts[2]) if parts[2] else 0,
                        'price': float(parts[3]) if parts[3] else 0,
                        'high': float(parts[4]) if parts[4] else 0,
                        'low': float(parts[5]) if parts[5] else 0,
                        'volume': float(parts[8]) if parts[8] else 0,
                        'amount': float(parts[9]) if parts[9] else 0,
                        'date': parts[30] if len(parts) > 30 else '',
                        'time': parts[31] if len(parts) > 31 else '',
                    }
    except Exception as e:
        print(f"  [新浪实时] 失败: {e}")
    return None

def get_pe_from_eastmoney(code):
    """从东方财富获取PE数据"""
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

def check_above_avg_price(code, intraday_df):
    """检查1: 分时站均价线比例"""
    try:
        if intraday_df is None or len(intraday_df) == 0:
            return None, "无分时数据"

        # 识别价格和成交量列
        price_col = None
        vol_col = None
        time_col = None

        for col in intraday_df.columns:
            cl = str(col).lower()
            if 'price' in cl or '价' in str(col):
                price_col = col
            if 'volume' in cl or '量' in str(col):
                vol_col = col
            if 'day' in cl or 'time' in cl or '时' in str(col) or 'date' in cl:
                time_col = col

        if price_col is None:
            # 尝试第二列
            cols = intraday_df.columns.tolist()
            if len(cols) >= 2:
                price_col = cols[1]

        if price_col is None:
            return None, "无法识别价格列"

        prices = intraday_df[price_col].astype(float).values

        if vol_col and vol_col in intraday_df.columns:
            volumes = intraday_df[vol_col].astype(float).values
        else:
            volumes = None

        # 计算VWAP
        if volumes is not None and len(volumes) == len(prices) and volumes.sum() > 0:
            cumulative_amount = 0
            cumulative_volume = 0
            vwap_list = []
            for i in range(len(prices)):
                cumulative_amount += prices[i] * volumes[i]
                cumulative_volume += volumes[i]
                vwap = cumulative_amount / cumulative_volume if cumulative_volume > 0 else prices[i]
                vwap_list.append(vwap)
        else:
            # 简单累计平均
            vwap_list = []
            for i in range(len(prices)):
                vwap_list.append(prices[:i+1].mean())

        above_count = sum(1 for i in range(len(prices)) if prices[i] >= vwap_list[i])
        ratio = above_count / len(prices) * 100

        passed = ratio > 70
        return passed, f"站均价线比例={ratio:.1f}%"

    except Exception as e:
        return None, f"计算失败: {e}"

def check_tail_sneak(code, intraday_df):
    """检查2: 尾盘是否偷袭"""
    try:
        if intraday_df is None or len(intraday_df) == 0:
            return None, "无分时数据"

        time_col = None
        price_col = None
        for col in intraday_df.columns:
            cl = str(col).lower()
            if 'day' in cl or 'time' in cl or '时' in str(col) or 'date' in cl:
                time_col = col
            if 'price' in cl or '价' in str(col):
                price_col = col

        if time_col is None or price_col is None:
            return None, "无法识别时间/价格列"

        df = intraday_df.copy()
        df['time_str'] = df[time_col].astype(str)
        df['price_val'] = df[price_col].astype(float)

        # 筛选14:25之后的数据
        tail_data = df[df['time_str'].str.contains('14:[2-4]')].copy()
        if len(tail_data) == 0:
            tail_data = df[df['time_str'].str.contains('14:')].copy()

        if len(tail_data) < 2:
            return None, "尾盘数据不足"

        prices = tail_data['price_val'].values
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

def check_volume_sustained(df_daily):
    """检查3: 量能是否持续"""
    try:
        if df_daily is None or len(df_daily) < 2:
            return None, "日K数据不足"

        recent = df_daily.tail(5)
        vol_col = 'volume' if 'volume' in recent.columns else None
        if vol_col is None:
            for col in recent.columns:
                if 'volume' in str(col).lower() or '量' in str(col):
                    vol_col = col
                    break

        if vol_col is None:
            return None, "无成交量数据"

        vols = recent[vol_col].astype(float).values
        if len(vols) >= 2 and vols[-2] > 0:
            shrink_ratio = (vols[-2] - vols[-1]) / vols[-2] * 100
            passed = shrink_ratio < 30
            return passed, f"量能变化={-shrink_ratio:.1f}%（正为放量）"

        return None, "数据不足"
    except Exception as e:
        return None, f"计算失败: {e}"

def check_ma_bullish(df_daily):
    """检查4: 均线多头排列"""
    try:
        if df_daily is None or len(df_daily) < 20:
            return None, "数据不足20天"

        df = df_daily.copy()
        close_col = 'close' if 'close' in df.columns else None
        if close_col is None:
            for col in df.columns:
                if 'close' in str(col).lower() or '收盘' in str(col):
                    close_col = col
                    break

        if close_col is None:
            return None, "无收盘价数据"

        df['MA5'] = df[close_col].rolling(5).mean()
        df['MA10'] = df[close_col].rolling(10).mean()
        df['MA20'] = df[close_col].rolling(20).mean()

        latest = df.iloc[-1]
        ma5, ma10, ma20 = latest['MA5'], latest['MA10'], latest['MA20']

        if pd.isna(ma5) or pd.isna(ma10) or pd.isna(ma20):
            return None, f"均线数据缺失"

        passed = ma5 > ma10 > ma20
        return passed, f"MA5={ma5:.2f}, MA10={ma10:.2f}, MA20={ma20:.2f}"
    except Exception as e:
        return None, f"计算失败: {e}"

def check_volume_increasing(df_daily):
    """检查5: 成交量连续温和放大"""
    try:
        if df_daily is None or len(df_daily) < 5:
            return None, "数据不足5天"

        recent_5 = df_daily.tail(5)
        vol_col = 'volume' if 'volume' in recent_5.columns else None
        if vol_col is None:
            for col in recent_5.columns:
                if 'volume' in str(col).lower() or '量' in str(col):
                    vol_col = col
                    break

        if vol_col is None:
            return None, "无成交量数据"

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
        if df_daily is None or len(df_daily) < 1:
            return None, "无日K数据"

        threshold = get_limit_up_threshold(code)
        recent_20 = df_daily.tail(20)

        # 计算涨跌幅
        close_col = 'close' if 'close' in recent_20.columns else None
        if close_col is None:
            for col in recent_20.columns:
                if 'close' in str(col).lower() or '收盘' in str(col):
                    close_col = col
                    break

        if close_col is None:
            return None, "无收盘价数据"

        # 如果有pct_chg列直接使用
        pct_col = None
        for col in recent_20.columns:
            if 'pct_chg' in str(col).lower() or '涨跌幅' in str(col):
                pct_col = col
                break

        if pct_col:
            pcts = recent_20[pct_col].astype(float).values
        else:
            # 计算涨跌幅
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
            pcts = pd.Series(pcts)

        limit_up_days = sum(1 for p in pcts if p >= threshold)
        has_limit = limit_up_days > 0

        max_pct = max(pcts) if len(pcts) > 0 else 0
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

    # 检查ST
    if 'ST' in name or '*ST' in name:
        issues.append("有ST风险")

    # 检查PE
    try:
        em_data = get_pe_from_eastmoney(code)
        if em_data:
            pe = em_data.get('f162')
            if pe is not None and pe != '-':
                pe_val = float(pe)
                if pe_val < 0:
                    issues.append(f"PE为负({pe_val:.1f}), 亏损股")
    except:
        pass

    # 尝试通过akshare获取PE
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

    # 检查减持公告
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
        df_daily = get_daily_data(code)
        time.sleep(0.3)

        # 获取分时数据
        print("  获取分时数据...")
        intraday_df = get_intraday_data(code)
        time.sleep(0.3)

        # 检查1: 分时站均价线
        print("  [检查1] 分时站均价线比例...")
        passed, detail = check_above_avg_price(code, intraday_df)
        result["above_avg"] = (passed, detail)
        print(f"  -> {'✅通过' if passed else ('❌不通过' if passed==False else '⚠️未知')}: {detail}")

        # 检查2: 尾盘偷袭
        print("  [检查2] 尾盘是否偷袭...")
        passed, detail = check_tail_sneak(code, intraday_df)
        result["tail_sneak"] = (passed, detail)
        print(f"  -> {'✅通过' if passed else ('❌不通过' if passed==False else '⚠️未知')}: {detail}")

        # 检查3: 量能持续
        print("  [检查3] 量能是否持续...")
        passed, detail = check_volume_sustained(df_daily)
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
    print("=" * 130)
    print("A股候选股深度盯盘验证汇总")
    print(f"检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 130)

    header = f"{'代码':<8} {'名称':<8} {'站均价线':<14} {'尾盘偷袭':<14} {'量能持续':<14} {'均线多头':<14} {'量能放大':<14} {'20天涨停':<14} {'基本面':<14} {'通过/总数':<8}"
    print(header)
    print("-" * 130)

    for r in results:
        checks = [r["above_avg"], r["tail_sneak"], r["vol_sustained"],
                  r["ma_bullish"], r["vol_increasing"], r["limit_up_20d"],
                  r["fundamentals"]]

        pass_count = sum(1 for c in checks if c[0] == True)
        total_known = sum(1 for c in checks if c[0] is not None)

        def fmt(check):
            if check[0] is True: return "✅通过"
            elif check[0] is False: return "❌不通过"
            else: return "⚠️未知"

        row = f"{r['code']:<8} {r['name']:<8} {fmt(r['above_avg']):<14} {fmt(r['tail_sneak']):<14} {fmt(r['vol_sustained']):<14} {fmt(r['ma_bullish']):<14} {fmt(r['vol_increasing']):<14} {fmt(r['limit_up_20d']):<14} {fmt(r['fundamentals']):<14} {pass_count}/{total_known}"
        print(row)

    print("-" * 130)

    # 详细信息
    print("\n\n=== 详细检查信息 ===\n")
    for r in results:
        print(f"\n【{r['code']} {r['name']}】")
        checks = [
            ("分时站均价线(>70%)", r["above_avg"]),
            ("尾盘偷袭(<1%)", r["tail_sneak"]),
            ("量能持续", r["vol_sustained"]),
            ("均线多头(MA5>MA10>MA20)", r["ma_bullish"]),
            ("量能温和放大", r["vol_increasing"]),
            ("20天涨停", r["limit_up_20d"]),
            ("基本面排雷", r["fundamentals"]),
        ]
        for label, (passed, detail) in checks:
            status = "✅" if passed else ("❌" if passed == False else "⚠️")
            print(f"  {status} {label}: {detail}")

    # 最终推荐
    print("\n\n=== 最终筛选结果 ===\n")

    # 按通过数排序
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

    print("⭐ 通过4项及以上的候选股（推荐关注）：")
    for r, pc, fc, uc in ranked:
        if pc >= 4:
            fail_labels = []
            labels = ["站均价线", "尾盘偷袭", "量能持续", "均线多头", "量能放大", "20天涨停", "基本面"]
            checks = [r["above_avg"], r["tail_sneak"], r["vol_sustained"],
                      r["ma_bullish"], r["vol_increasing"], r["limit_up_20d"],
                      r["fundamentals"]]
            for i, c in enumerate(checks):
                if c[0] == False:
                    fail_labels.append(labels[i])
            fail_str = f", 不通过: {', '.join(fail_labels)}" if fail_labels else ""
            print(f"  ⭐ {r['code']} {r['name']} - 通过{pc}项{fail_str}")

    print("\n⚠️ 通过2-3项的候选股（需进一步观察）：")
    for r, pc, fc, uc in ranked:
        if 2 <= pc < 4:
            fail_labels = []
            labels = ["站均价线", "尾盘偷袭", "量能持续", "均线多头", "量能放大", "20天涨停", "基本面"]
            checks = [r["above_avg"], r["tail_sneak"], r["vol_sustained"],
                      r["ma_bullish"], r["vol_increasing"], r["limit_up_20d"],
                      r["fundamentals"]]
            for i, c in enumerate(checks):
                if c[0] == False:
                    fail_labels.append(labels[i])
            fail_str = f", 不通过: {', '.join(fail_labels)}" if fail_labels else ""
            print(f"  ⚠️ {r['code']} {r['name']} - 通过{pc}项{fail_str}")

    print("\n✗ 通过不足2项的候选股（建议淘汰）：")
    for r, pc, fc, uc in ranked:
        if pc < 2:
            fail_labels = []
            labels = ["站均价线", "尾盘偷袭", "量能持续", "均线多头", "量能放大", "20天涨停", "基本面"]
            checks = [r["above_avg"], r["tail_sneak"], r["vol_sustained"],
                      r["ma_bullish"], r["vol_increasing"], r["limit_up_20d"],
                      r["fundamentals"]]
            for i, c in enumerate(checks):
                if c[0] == False:
                    fail_labels.append(labels[i])
            fail_str = f", 不通过: {', '.join(fail_labels)}" if fail_labels else ""
            print(f"  ✗ {r['code']} {r['name']} - 通过{pc}项{fail_str}")

if __name__ == "__main__":
    main()
