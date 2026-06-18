import os
# 清除代理设置，避免连接东方财富API失败
for key in ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy']:
    os.environ.pop(key, None)

import akshare as ak
import pandas as pd
from datetime import datetime, timedelta

# 候选股票列表（需要检查20天涨停历史的）
# 先获取今日涨幅3-5%的股票列表，然后逐一检查
candidates = []

# 获取全市场行情
try:
    df = ak.stock_zh_a_spot_em()
    # 筛选涨幅3-5%, 量比>1.2, 换手3-15%, 市值30-300亿, 非ST
    mask = (
        (df['涨跌幅'] >= 3) & (df['涨跌幅'] <= 5) &
        (df['量比'] > 1.2) &
        (df['换手率'] >= 3) & (df['换手率'] <= 15) &
        (df['流通市值'] >= 30e8) & (df['流通市值'] <= 300e8) &
        (~df['名称'].str.contains('ST', case=False))
    )
    candidates_df = df[mask]
    candidate_codes = candidates_df['代码'].tolist()
    candidate_names = candidates_df['名称'].tolist()
    print(f"共{len(candidate_codes)}只候选股需要检查20天涨停历史")
except Exception as e:
    print(f"获取行情失败: {e}")
    # 使用东方财富API替代
    import requests
    url = "https://push2.eastmoney.com/api/qt/clist/get"
    params = {
        "pn": 1, "pz": 6000, "po": 1, "np": 1,
        "fltt": 2, "invt": 2, "fid": "f3",
        "fs": "m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23,m:0+t:81+s:2048",
        "fields": "f2,f3,f5,f6,f8,f10,f12,f14,f20,f21"
    }
    headers = {"User-Agent": "Mozilla/5.0"}
    # 不使用代理
    session = requests.Session()
    session.trust_env = False
    resp = session.get(url, params=params, headers=headers, timeout=30)
    data = resp.json()
    items = data.get("data", {}).get("diff", [])
    rdf = pd.DataFrame(items)
    rdf = rdf.rename(columns={"f3": "涨跌幅", "f8": "换手率", "f10": "量比", "f12": "代码", "f14": "名称", "f21": "流通市值"})
    for col in ['涨跌幅', '换手率', '量比', '流通市值']:
        rdf[col] = pd.to_numeric(rdf[col], errors='coerce')
    mask = (
        (rdf['涨跌幅'] >= 3) & (rdf['涨跌幅'] <= 5) &
        (rdf['量比'] > 1.2) &
        (rdf['换手率'] >= 3) & (rdf['换手率'] <= 15) &
        (rdf['流通市值'] >= 30e8) & (rdf['流通市值'] <= 300e8) &
        (~rdf['名称'].str.contains('ST', case=False))
    )
    candidates_df = rdf[mask]
    candidate_codes = candidates_df['代码'].tolist()
    candidate_names = candidates_df['名称'].tolist()
    print(f"共{len(candidate_codes)}只候选股需要检查20天涨停历史")

# 检查20天涨停历史 - 使用涨停板数据
# 方法：获取近20天的涨停股票列表，看候选股是否在其中
try:
    # 获取近期涨停数据
    end_date = datetime.now().strftime('%Y%m%d')
    start_date = (datetime.now() - timedelta(days=30)).strftime('%Y%m%d')

    limit_up_stocks = set()
    limit_up_detail = {}  # code -> [dates]
    # 逐日获取涨停数据
    for i in range(25):  # 多查几天确保覆盖20个交易日
        check_date = (datetime.now() - timedelta(days=i)).strftime('%Y%m%d')
        try:
            # 尝试获取每日涨停数据
            zt_df = ak.stock_zt_pool_em(date=check_date)
            if zt_df is not None and len(zt_df) > 0:
                codes = zt_df['代码'].tolist() if '代码' in zt_df.columns else []
                limit_up_stocks.update(codes)
                for code in codes:
                    if code not in limit_up_detail:
                        limit_up_detail[code] = []
                    limit_up_detail[code].append(check_date)
                print(f"  {check_date}: {len(codes)}只涨停")
            else:
                print(f"  {check_date}: 无数据（可能非交易日）")
        except Exception as e2:
            print(f"  {check_date}: 获取失败 - {str(e2)[:80]}")

    # 检查候选股是否在涨停列表中
    print(f"\n过去20天涨停股票总数: {len(limit_up_stocks)}")
    has_limit_up = []
    for code, name in zip(candidate_codes, candidate_names):
        if code in limit_up_stocks:
            dates = limit_up_detail.get(code, [])
            has_limit_up.append((code, name, dates))

    print(f"\n候选股中有20天涨停记录的: {len(has_limit_up)}只")
    print("=" * 70)
    for code, name, dates in has_limit_up:
        dates_str = ", ".join(dates)
        print(f"  {code} {name}  涨停日期: {dates_str}")

    print(f"\n候选股中无20天涨停记录的: {len(candidate_codes) - len(has_limit_up)}只")
    no_limit_up = []
    for code, name in zip(candidate_codes, candidate_names):
        if code not in limit_up_stocks:
            no_limit_up.append((code, name))
    for code, name in no_limit_up:
        print(f"  {code} {name}")

except Exception as e:
    print(f"获取涨停数据失败: {e}")
    print("使用替代方法：检查近20日涨幅是否曾达到9.9%以上")

    # 替代方法：逐个获取候选股历史数据
    has_limit_up = []
    no_limit_up = []
    end_date = datetime.now().strftime('%Y%m%d')
    start_date = (datetime.now() - timedelta(days=30)).strftime('%Y%m%d')

    for idx, (code, name) in enumerate(zip(candidate_codes, candidate_names)):
        try:
            hist = ak.stock_zh_a_hist(symbol=code, period="daily", start_date=start_date, end_date=end_date, adjust="qfq")
            if hist is not None and len(hist) > 0:
                # 检查是否有涨幅>=9.9%的记录（考虑科创板20%涨停）
                if '涨跌幅' in hist.columns:
                    # 判断是否科创板(688开头)或创业板(300开头，注册制后20%)
                    threshold = 19.5 if code.startswith('688') or code.startswith('30') else 9.5
                    limit_up_days = hist[hist['涨跌幅'] >= threshold]
                    if len(limit_up_days) > 0:
                        dates = limit_up_days['日期'].tolist()
                        has_limit_up.append((code, name, dates))
                        print(f"  [{idx+1}/{len(candidate_codes)}] {code} {name} 有涨停记录: {dates}")
                    else:
                        no_limit_up.append((code, name))
                else:
                    no_limit_up.append((code, name))
            else:
                no_limit_up.append((code, name))
        except Exception as e3:
            print(f"  [{idx+1}/{len(candidate_codes)}] {code} {name} 获取历史失败: {str(e3)[:80]}")
            no_limit_up.append((code, name))

        # 控制请求频率
        import time
        time.sleep(0.3)

    print(f"\n候选股中有20天涨停记录的: {len(has_limit_up)}只")
    print("=" * 70)
    for code, name, dates in has_limit_up:
        dates_str = ", ".join([str(d) for d in dates])
        print(f"  {code} {name}  涨停日期: {dates_str}")

    print(f"\n候选股中无20天涨停记录的: {len(no_limit_up)}只")
    for code, name in no_limit_up:
        print(f"  {code} {name}")
