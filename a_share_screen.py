import requests
import json
import os
import time
import pandas as pd

# 确保代理设置正确
proxy = os.environ.get('https_proxy', os.environ.get('HTTPS_PROXY', ''))
proxies = {"http": proxy, "https": proxy} if proxy else None
print(f"使用代理: {proxy}")

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

# ===== 步骤1: 获取三大指数 =====
def tencent_quote(prefixed_codes):
    url = "https://qt.gtimg.cn/q=" + ",".join(prefixed_codes)
    resp = requests.get(url, headers=headers, timeout=10, proxies=proxies)
    data = resp.content.decode("gbk")
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
            "change_amt": float(vals[31]) if vals[31] else 0,
            "change_pct": float(vals[32]) if vals[32] else 0,
            "high": float(vals[33]) if vals[33] else 0,
            "low": float(vals[34]) if vals[34] else 0,
            "amount_wan": float(vals[37]) if vals[37] else 0,
            "turnover_pct": float(vals[38]) if vals[38] else 0,
            "amplitude_pct": float(vals[43]) if vals[43] else 0,
            "mcap_yi": float(vals[44]) if vals[44] else 0,
            "float_mcap_yi": float(vals[45]) if vals[45] else 0,
        }
    return result

index_quotes = tencent_quote(["sh000001", "sz399001", "sz399006"])
print("=== 大盘指数行情 ===")
for code, q in index_quotes.items():
    print(f"{q['name']}({code}): 现价={q['price']} 涨跌幅={q['change_pct']}% 振幅={q['amplitude_pct']}%")

# ===== 步骤2: 获取A股代码列表 =====
print("\n正在获取A股代码列表...")
all_codes = []
page = 1
while True:
    url = f"https://datacenter-web.eastmoney.com/api/data/v1/get?sortColumns=SECURITY_CODE&sortTypes=1&pageSize=2000&pageNumber={page}&reportName=RPT_LICO_FN_CPD&columns=SECURITY_CODE,SECURITY_NAME_ABBR,TRADE_MARKET&source=WEB&client=WEB&filter=(SECURITY_TYPE_CODE=%22058001001%22)(ISNEW=%221%22)"
    try:
        r = requests.get(url, headers=headers, timeout=15, proxies=proxies)
        d = r.json()
        if not d.get('result') or not d['result'].get('data'):
            break
        data = d['result']['data']
        all_codes.extend([(row['SECURITY_CODE'], row['SECURITY_NAME_ABBR'], row['TRADE_MARKET']) for row in data])
        total = d['result'].get('count', 0)
        print(f"  第{page}页: 获取 {len(data)} 只, 累计 {len(all_codes)}/{total}")
        if len(all_codes) >= total:
            break
        page += 1
        time.sleep(0.2)
    except Exception as e:
        print(f"  第{page}页失败: {e}")
        break

print(f"共获取 {len(all_codes)} 只A股代码")

# ===== 步骤3: 批量获取腾讯行情 =====
print("\n正在批量获取行情数据...")

def code_to_prefix(code):
    """将股票代码转为腾讯前缀格式"""
    if code.startswith("6") or code.startswith("9"):
        return f"sh{code}"
    elif code.startswith("8"):
        return f"bj{code}"
    else:
        return f"sz{code}"

def batch_tencent_quote(code_list, batch_size=50):
    """批量获取腾讯行情"""
    all_results = []
    total_batches = (len(code_list) + batch_size - 1) // batch_size

    for i in range(0, len(code_list), batch_size):
        batch = code_list[i:i+batch_size]
        prefixed = [code_to_prefix(c) for c in batch]
        url = "https://qt.gtimg.cn/q=" + ",".join(prefixed)
        try:
            resp = requests.get(url, headers=headers, timeout=15, proxies=proxies)
            data = resp.content.decode("gbk")
            for line in data.strip().split(";"):
                if not line.strip() or "=" not in line or '"' not in line:
                    continue
                key = line.split("=")[0].split("_")[-1]
                vals = line.split('"')[1].split("~")
                if len(vals) < 53:
                    continue
                code = key[2:]
                try:
                    all_results.append({
                        "代码": code,
                        "名称": vals[1],
                        "最新价": float(vals[3]) if vals[3] else 0,
                        "昨收": float(vals[4]) if vals[4] else 0,
                        "涨跌额": float(vals[31]) if vals[31] else 0,
                        "涨跌幅": float(vals[32]) if vals[32] else 0,
                        "最高": float(vals[33]) if vals[33] else 0,
                        "最低": float(vals[34]) if vals[34] else 0,
                        "成交额万": float(vals[37]) if vals[37] else 0,
                        "换手率": float(vals[38]) if vals[38] else 0,
                        "振幅": float(vals[43]) if vals[43] else 0,
                        "总市值亿": float(vals[44]) if vals[44] else 0,
                        "流通市值亿": float(vals[45]) if vals[45] else 0,
                        "量比": float(vals[49]) if vals[49] else 0,
                        "市盈率": float(vals[39]) if vals[39] else 0,
                    })
                except (ValueError, IndexError):
                    continue
        except Exception as e:
            print(f"  批次 {i//batch_size + 1} 失败: {e}")

        batch_num = i // batch_size + 1
        if batch_num % 10 == 0:
            print(f"  已处理 {batch_num}/{total_batches} 批, 获取 {len(all_results)} 只行情")
        time.sleep(0.15)

    return all_results

codes = [c[0] for c in all_codes]
quote_data = batch_tencent_quote(codes, batch_size=50)

df = pd.DataFrame(quote_data)
print(f"\n全市场A股行情数量: {len(df)}")
print("列名:", df.columns.tolist())

# ===== 步骤4: 筛选 =====
# 排除停牌
df = df[df['最新价'] > 0]
print(f"排除停牌后: {len(df)} 只")

# 涨幅 3%-5%
df_filtered = df[(df['涨跌幅'] >= 3) & (df['涨跌幅'] <= 5)].copy()
print(f"涨幅3%-5%: {len(df_filtered)} 只")

# 量比 > 1.4
df_filtered = df_filtered[df_filtered['量比'] > 1.4]
print(f"量比>1.4: {len(df_filtered)} 只")

# 换手率 5%-10%
df_filtered = df_filtered[(df_filtered['换手率'] >= 5) & (df_filtered['换手率'] <= 10)]
print(f"换手率5%-10%: {len(df_filtered)} 只")

# 流通市值 50-200亿
df_filtered = df_filtered[(df_filtered['流通市值亿'] >= 50) & (df_filtered['流通市值亿'] <= 200)]
print(f"流通市值50-200亿: {len(df_filtered)} 只")

# 排除ST
df_filtered = df_filtered[~df_filtered['名称'].str.contains('ST|\\*ST', na=False)]
print(f"排除ST: {len(df_filtered)} 只")

print(f"\n=== 初筛结果: {len(df_filtered)} 只 ===")
cols_to_show = ['代码', '名称', '最新价', '涨跌幅', '换手率', '量比', '流通市值亿']
available_cols = [c for c in cols_to_show if c in df_filtered.columns]
df_filtered_display = df_filtered[available_cols].sort_values('涨跌幅', ascending=False)
print(df_filtered_display.to_string(index=False))
