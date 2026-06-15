import os
proxy = os.environ.get('http_proxy', '') or os.environ.get('HTTP_PROXY', '')
if proxy:
    os.environ['http_proxy'] = proxy
    os.environ['https_proxy'] = proxy
    os.environ['HTTP_PROXY'] = proxy
    os.environ['HTTPS_PROXY'] = proxy

import urllib.request
import json
import time

proxy_handler = urllib.request.ProxyHandler({'http': proxy, 'https': proxy})
opener = urllib.request.build_opener(proxy_handler)

# ===== 1. 大盘指数行情 =====
print("=" * 60)
print("大盘指数行情")
print("=" * 60)

def tencent_index_quote(index_codes):
    """获取指数行情，用s_sh/s_sz前缀"""
    prefixed = []
    for c in index_codes:
        if c.startswith(("6", "9")):
            prefixed.append(f"s_sh{c}")
        else:
            prefixed.append(f"s_sz{c}")
    url = "https://qt.gtimg.cn/q=" + ",".join(prefixed)
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "Mozilla/5.0")
    resp = opener.open(req, timeout=15)
    data = resp.read().decode("gbk")
    result = {}
    for line in data.strip().split(";"):
        if not line.strip() or "=" not in line or '"' not in line:
            continue
        key = line.split("=")[0].split("_")[-1]
        vals = line.split('"')[1].split("~")
        if len(vals) < 10:
            continue
        code = key[2:]
        result[code] = {
            "name": vals[1],
            "price": float(vals[3]) if vals[3] else 0,
            "change": float(vals[4]) if vals[4] else 0,
            "change_pct": float(vals[5]) if vals[5] else 0,
        }
    return result

def tencent_stock_quote(codes):
    """获取股票详细行情（含量比等）"""
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
    resp = opener.open(req, timeout=15)
    data = resp.read().decode("gbk")
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
            "high": float(vals[33]) if vals[33] else 0,
            "low": float(vals[34]) if vals[34] else 0,
            "amount_wan": float(vals[37]) if vals[37] else 0,
            "turnover_pct": float(vals[38]) if vals[38] else 0,
            "mcap_yi": float(vals[44]) if vals[44] else 0,
            "float_mcap_yi": float(vals[45]) if vals[45] else 0,
            "vol_ratio": float(vals[49]) if vals[49] else 0,
        }
    return result

try:
    index_quotes = tencent_index_quote(["000001", "000300", "399006"])
    for code, q in index_quotes.items():
        print(f"  {q['name']}({code}): {q['price']} 涨跌={q['change']} 涨跌幅={q['change_pct']}%")
except Exception as e:
    print(f"腾讯指数接口失败: {e}")

# 获取指数详细行情（注意：sh000001在腾讯股票接口中映射为平安银行，所以指数详细行情需要单独处理）
print("\n指数详细行情:")
try:
    # 上证指数用sh000001在股票接口中会返回平安银行，需要用指数专用接口
    # 沪深300
    index_detail = tencent_stock_quote(["000300", "399006"])
    for code, q in index_detail.items():
        print(f"  {q['name']}({code}): 价格={q['price']} 涨跌幅={q['change_pct']}% 昨收={q['last_close']} 高={q['high']} 低={q['low']} 成交额={q['amount_wan']}万 换手率={q['turnover_pct']}% 总市值={q['mcap_yi']}亿 流通市值={q['float_mcap_yi']}亿 量比={q['vol_ratio']}")
    # 上证指数单独获取
    sh_detail = tencent_index_quote(["000001"])
    for code, q in sh_detail.items():
        print(f"  {q['name']}({code}): 价格={q['price']} 涨跌幅={q['change_pct']}% 涨跌额={q['change']}")
except Exception as e:
    print(f"指数详细行情获取失败: {e}")


# ===== 2. 全市场A股初筛 =====
print("\n" + "=" * 60)
print("全市场A股初筛（涨幅3%-5% + 量比>1.4 + 换手率5%-10% + 流通市值50-200亿）")
print("=" * 60)

def sina_stock_list(page=1, num=80, sort='changepercent', asc=0, node='hs_a'):
    """通过新浪接口获取A股列表"""
    url = f'https://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page={page}&num={num}&sort={sort}&asc={asc}&node={node}&symbol=&_s_r_a=auto'
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "Mozilla/5.0")
    resp = opener.open(req, timeout=15)
    data = resp.read().decode('gbk')
    return json.loads(data)

# 获取全市场数据（分页获取）
all_stocks = []
page = 1
while True:
    try:
        data = sina_stock_list(page=page, num=80)
        if not data or len(data) == 0:
            break
        all_stocks.extend(data)
        if len(data) < 80:
            break
        page += 1
        time.sleep(0.3)
    except Exception as e:
        print(f"获取第{page}页失败: {e}")
        break

print(f"全市场A股总数: {len(all_stocks)}")

# 初筛：涨幅3%-5% + 换手率5%-10% + 流通市值50-200亿 + 排除ST/退/北交所
filtered = []
for s in all_stocks:
    try:
        code = s.get('code', '')
        name = s.get('name', '')
        change_pct = float(s.get('changepercent', 0))
        turnover = float(s.get('turnoverratio', 0))
        mktcap = float(s.get('mktcap', 0))  # 万元
        nmc = float(s.get('nmc', 0))  # 万元(流通市值)
        trade = float(s.get('trade', 0))
        amount = float(s.get('amount', 0))
        
        # 排除北交所
        if code.startswith(('8', '4', '9')):
            continue
        # 排除ST
        if 'ST' in name or '退' in name:
            continue
        # 涨幅 3%-5%
        if change_pct < 3 or change_pct > 5:
            continue
        # 换手率 5%-10%
        if turnover < 5 or turnover > 10:
            continue
        # 流通市值 50-200亿
        nmc_yi = nmc / 10000
        if nmc_yi < 50 or nmc_yi > 200:
            continue
        
        filtered.append({
            'code': code,
            'name': name,
            'change_pct': change_pct,
            'turnover': turnover,
            'nmc_yi': nmc_yi,
            'trade': trade,
            'amount': amount,
            'mktcap_yi': mktcap / 10000,
        })
    except (ValueError, TypeError):
        continue

print(f"涨幅3%-5%: 已筛选")
print(f"换手率5%-10%: 已筛选")
print(f"流通市值50-200亿: 已筛选")
print(f"排除ST/退: 已筛选")
print(f"排除北交所: 已筛选")
print(f"新浪初筛（涨幅3%-5% + 换手率5%-10% + 流通市值50-200亿）: {len(filtered)} 只")

if filtered:
    # 批量获取腾讯行情补充量比
    codes_for_tencent = [f['code'] for f in filtered]
    vol_ratio_map = {}
    for i in range(0, len(codes_for_tencent), 50):
        batch = codes_for_tencent[i:i+50]
        try:
            tencent_data = tencent_stock_quote(batch)
            for code, q in tencent_data.items():
                vol_ratio_map[code] = q['vol_ratio']
            time.sleep(0.3)
        except Exception as e:
            print(f"获取腾讯量比失败: {e}")
    
    # 应用量比筛选
    final_filtered = []
    for f in filtered:
        vr = vol_ratio_map.get(f['code'], 0)
        f['vol_ratio'] = vr
        if vr > 1.4:
            final_filtered.append(f)
    
    print(f"量比>1.4筛选后: {len(final_filtered)} 只")
    
    print(f"\n初筛通过: {len(final_filtered)} 只")
    for f in final_filtered:
        print(f"  {f['code']} {f['name']}: 涨幅={f['change_pct']:.2f}% 换手={f['turnover']:.2f}% 量比={f['vol_ratio']:.2f} 流通市值={f['nmc_yi']:.1f}亿 价格={f['trade']} 成交额={f['amount']:.0f}")
    
    if final_filtered:
        codes = [f['code'] for f in final_filtered]
        print(f"\n初筛股票代码列表: {codes}")
else:
    print("新浪初筛无结果")


# ===== 3. 获取上证指数15分钟K线 =====
print("\n" + "=" * 60)
print("上证指数15分钟K线（14:30后趋势判断）")
print("=" * 60)

try:
    url = 'https://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol=sh000001&scale=15&ma=no&datalen=30'
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "Mozilla/5.0")
    resp = opener.open(req, timeout=15)
    kline_data = json.loads(resp.read().decode('utf-8'))
    
    print(f"获取15分钟K线: {len(kline_data)} 条")
    
    # 输出所有K线
    for k in kline_data:
        print(f"  {k['day']} O={k['open']} H={k['high']} L={k['low']} C={k['close']}")
    
    # 筛选14:30后的K线
    afternoon = [k for k in kline_data if k['day'][11:16] >= '14:30']
    print(f"\n14:30后K线数: {len(afternoon)}")
    for k in afternoon:
        print(f"  {k['day']} O={k['open']} H={k['high']} L={k['low']} C={k['close']}")
    
    if len(afternoon) >= 2:
        first_close = float(afternoon[0]['close'])
        last_close = float(afternoon[-1]['close'])
        trend = "上升" if last_close > first_close else "下降"
        print(f"14:30后趋势: {trend} (首={first_close:.2f} → 末={last_close:.2f})")
except Exception as e:
    print(f"新浪15分钟K线获取失败: {e}")

    # 尝试mootdx
    try:
        from mootdx.quotes import Quotes
        client = Quotes.factory(market='std')
        klines_15m = client.bars(symbol='000001', category=9, offset=30, market=1)
        if klines_15m is not None and len(klines_15m) > 0:
            afternoon = klines_15m[klines_15m.index.strftime('%H:%M') >= '14:30']
            print(f"14:30后15分钟K线数: {len(afternoon)}")
            for idx, row in afternoon.iterrows():
                print(f"  {idx.strftime('%H:%M')} O={row['open']:.2f} H={row['high']:.2f} L={row['low']:.2f} C={row['close']:.2f}")
            if len(afternoon) >= 2:
                first_close = afternoon.iloc[0]['close']
                last_close = afternoon.iloc[-1]['close']
                trend = "上升" if last_close > first_close else "下降"
                print(f"14:30后趋势: {trend} (首={first_close:.2f} → 末={last_close:.2f})")
        else:
            print("mootdx返回空数据")
    except Exception as e2:
        print(f"mootdx也失败: {e2}")
