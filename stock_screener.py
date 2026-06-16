#!/usr/bin/env python3
"""A股实时行情筛选脚本 - 腾讯财经API (requests版)"""

import json
import time
import requests
import os

# 清除代理设置
for k in ['http_proxy', 'https_proxy', 'HTTP_PROXY', 'HTTPS_PROXY']:
    os.environ.pop(k, None)

# 设置tcp_tw_reuse以避免端口耗尽
os.system('sysctl -w net.ipv4.tcp_tw_reuse=1 2>/dev/null')

def log(msg):
    print(msg, flush=True)

def generate_codes():
    """生成A股代码列表"""
    codes = []
    for i in range(600000, 606000):
        codes.append(f"sh{i}")
    for i in range(1, 5000):
        codes.append(f"sz{i:06d}")
    for i in range(300001, 302000):
        codes.append(f"sz{i}")
    return codes

def is_excluded(code):
    """排除北交所"""
    num = code[2:]
    if num.startswith('8') or num.startswith('4'):
        return True
    return False

def fetch_batch(batch_codes):
    """用requests批量查询腾讯API"""
    query = ','.join(batch_codes)
    url = f"https://qt.gtimg.cn/q={query}"
    try:
        resp = requests.get(url, timeout=15, headers={'User-Agent': 'Mozilla/5.0'})
        if resp.status_code != 200:
            return []
        text = resp.content.decode('gbk', errors='ignore')
    except Exception as e:
        return []

    results = []
    for line in text.strip().split(';'):
        line = line.strip()
        if not line or '=' not in line:
            continue
        try:
            _, data = line.split('=', 1)
            data = data.strip().strip('"')
            if not data:
                continue
            fields = data.split('~')
            if len(fields) < 50:
                continue
            results.append(fields)
        except Exception:
            continue
    return results

def apply_filters(fields):
    """应用4个硬条件筛选"""
    try:
        name = fields[1]
        code_raw = fields[2]
        price = fields[3]
        change_pct = fields[32]
        turnover = fields[38]
        circ_mv = fields[45]
        vol_ratio = fields[49]
        amount = fields[37]
        pe = fields[39]
        pb = fields[46]
    except IndexError:
        return None

    if not name or 'ST' in name or 'st' in name or '退' in name:
        return None

    if not price or not change_pct or not turnover or not circ_mv or not vol_ratio:
        return None

    try:
        change_pct_f = float(change_pct)
        vol_ratio_f = float(vol_ratio)
        turnover_f = float(turnover)
        circ_mv_f = float(circ_mv)
        price_f = float(price)
    except (ValueError, TypeError):
        return None

    if change_pct_f < 3 or change_pct_f > 5:
        return None
    if vol_ratio_f <= 1.4:
        return None
    if turnover_f < 5 or turnover_f > 10:
        return None
    if circ_mv_f < 50 or circ_mv_f > 200:
        return None

    if code_raw.startswith('6'):
        prefix = 'sh'
    else:
        prefix = 'sz'

    return {
        'code': f"{prefix}{code_raw}",
        'name': name,
        'price': price_f,
        'change_pct': round(change_pct_f, 2),
        'turnover_rate': round(turnover_f, 2),
        'circ_market_cap': round(circ_mv_f, 2),
        'vol_ratio': round(vol_ratio_f, 2),
        'amount_wan': amount,
        'pe_ttm': pe,
        'pb': pb,
    }

def main():
    all_codes = generate_codes()
    filtered_codes = [c for c in all_codes if not is_excluded(c)]
    log(f"总代码数: {len(all_codes)}, 排除后: {len(filtered_codes)}")

    filtered_codes = filtered_codes[:10000]
    log(f"本次查询: {len(filtered_codes)} 只股票")

    candidates = []
    batch_size = 50
    total_batches = (len(filtered_codes) + batch_size - 1) // batch_size
    total_fetched = 0

    for i in range(0, len(filtered_codes), batch_size):
        batch = filtered_codes[i:i+batch_size]
        batch_num = i // batch_size + 1

        fields_list = fetch_batch(batch)
        total_fetched += len(fields_list)

        for fields in fields_list:
            result = apply_filters(fields)
            if result:
                candidates.append(result)
                log(f"    ★ 命中: {result['code']} {result['name']} "
                      f"涨幅={result['change_pct']}% 量比={result['vol_ratio']} "
                      f"换手={result['turnover_rate']}% 流通市值={result['circ_market_cap']}亿")

        if batch_num % 20 == 0 or batch_num == 1:
            log(f"  批次 {batch_num}/{total_batches}, 已获取{total_fetched}条, 命中{len(candidates)}只")

        time.sleep(0.3)

    candidates.sort(key=lambda x: x['change_pct'], reverse=True)

    log(f"\n筛选完成! 共获取{total_fetched}条数据, 命中 {len(candidates)} 只股票")
    with open('/workspace/candidates.json', 'w', encoding='utf-8') as f:
        json.dump(candidates, f, ensure_ascii=False, indent=2)
    log(f"结果已保存到 /workspace/candidates.json")

    if candidates:
        log("\n--- 候选股票列表 ---")
        for s in candidates:
            log(f"  {s['code']} {s['name']:8s} | 现价:{s['price']:7.2f} | "
                  f"涨幅:{s['change_pct']:5.2f}% | 量比:{s['vol_ratio']:5.2f} | "
                  f"换手:{s['turnover_rate']:5.2f}% | 流通市值:{s['circ_market_cap']:7.2f}亿 | "
                  f"PE:{s['pe_ttm']} PB:{s['pb']}")

if __name__ == '__main__':
    main()
