import os
os.environ['http_proxy'] = 'http://127.0.0.1:18080'
os.environ['https_proxy'] = 'http://127.0.0.1:18080'

import akshare as ak
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
import time
warnings.filterwarnings('ignore')

# ===== 第一步：获取A股实时行情数据（腾讯源）=====
print("=== 获取A股实时行情（腾讯源）===")
df = ak.stock_zh_a_spot()
print(f"获取到 {len(df)} 只股票")

# ===== 数据预处理 =====
col_code = '代码'
col_name = '名称'
col_price = '最新价'
col_change = '涨跌幅'
col_volume = '成交量'
col_amount = '成交额'

for c in [col_price, col_change, col_volume, col_amount]:
    df[c] = pd.to_numeric(df[c], errors='coerce')

# 排除ST、退市、北交所、科创板
df = df[~df[col_name].str.contains('ST|退|N|C|U|W', na=False)]
df = df[~df[col_code].str.startswith(('bj', '8', '4', '9'))]
# 排除科创板（688开头）- 代码格式是 sh688xxx
df = df[~df[col_code].str.contains('688|689')]
# 排除停牌
df = df[df[col_volume] > 0]
print(f"排除ST/退市/北交所/科创板/停牌后: {len(df)} 只")

# ===== 筛选1：涨幅 3%-5% =====
mask1 = (df[col_change] >= 3.0) & (df[col_change] <= 5.0)
step1 = df[mask1].copy()
print(f"\n筛选1（涨幅3-5%）: {len(step1)} 只")

if len(step1) == 0:
    print("⚠️ 涨幅3-5%无结果，放宽到2-6%")
    mask1 = (df[col_change] >= 2.0) & (df[col_change] <= 6.0)
    step1 = df[mask1].copy()
    print(f"放宽后: {len(step1)} 只")

# ===== 筛选2-4：用新浪历史数据获取换手率、流通市值、计算量比 =====
print(f"\n=== 逐只获取补充数据（检查全部{len(step1)}只）===")

candidates_list = []
checked = 0
total = len(step1)
error_count = 0

for idx, row in step1.iterrows():
    code = row[col_code]
    name = row[col_name]
    checked += 1
    
    if checked % 50 == 0:
        print(f"  已检查 {checked}/{total}...")
    
    try:
        end_date = datetime.now().strftime("%Y%m%d")
        start_date = (datetime.now() - timedelta(days=30)).strftime("%Y%m%d")
        
        hist = ak.stock_zh_a_daily(symbol=code, start_date=start_date, end_date=end_date, adjust='qfq')
        
        if len(hist) < 5:
            continue
        
        time.sleep(0.08)  # 限流
        
        # 最新交易日数据（最后一行）
        today_data = hist.iloc[-1]
        today_vol = float(today_data['volume'])
        today_turnover = float(today_data['turnover'])  # 换手率（小数格式）
        outstanding_share = float(today_data['outstanding_share'])  # 流通股本
        
        # 计算流通市值 = 流通股本 * 当前股价
        circ_mv = outstanding_share * row[col_price]
        circ_mv_yi = circ_mv / 1e8  # 亿
        
        # 计算量比 = 今日成交量 / 近5日平均成交量
        recent_6 = hist.tail(6)
        if len(recent_6) < 2:
            continue
        prev_5 = recent_6.head(5)
        avg_vol_5 = prev_5['volume'].mean()
        
        if avg_vol_5 == 0:
            continue
        volume_ratio = today_vol / avg_vol_5
        
        # 换手率转为百分比
        turnover_pct = today_turnover * 100
        
        # 筛选2：量比 > 1.5（稍微放宽）
        if volume_ratio <= 1.5:
            continue
        
        # 筛选3：换手率 4%-12%（放宽）
        if turnover_pct < 4.0 or turnover_pct > 12.0:
            continue
        
        # 筛选4：流通市值 40-250亿（放宽）
        if circ_mv_yi < 40 or circ_mv_yi > 250:
            continue
        
        candidates_list.append({
            '代码': code,
            '名称': name,
            '涨跌幅': row[col_change],
            '最新价': row[col_price],
            '量比': round(volume_ratio, 2),
            '换手率': round(turnover_pct, 2),
            '流通市值(亿)': round(circ_mv_yi, 2),
            '成交额': row[col_amount],
            '成交量': today_vol,
        })
        
        print(f"  ✅ {code} {name} 涨幅={row[col_change]:.2f}% 量比={volume_ratio:.2f} 换手={turnover_pct:.2f}% 流通市值={circ_mv_yi:.1f}亿")
        
    except Exception as e:
        error_count += 1
        if error_count <= 3:
            print(f"  ⚠️ {code} {name} 失败: {e}")
        continue

result = pd.DataFrame(candidates_list)
print(f"\n=== 基础4步筛选结果 ===")
print(f"筛选出 {len(result)} 只股票 (错误数: {error_count})")

if len(result) == 0:
    print("⚠️ 基础4步筛选无结果，大幅放宽条件重试...")
    print("放宽：量比>1.2，换手3-15%，流通市值30-300亿")
    candidates_list2 = []
    for idx, row in step1.iterrows():
        code = row[col_code]
        name = row[col_name]
        try:
            end_date = datetime.now().strftime("%Y%m%d")
            start_date = (datetime.now() - timedelta(days=30)).strftime("%Y%m%d")
            hist = ak.stock_zh_a_daily(symbol=code, start_date=start_date, end_date=end_date, adjust='qfq')
            if len(hist) < 5:
                continue
            time.sleep(0.08)
            
            today_data = hist.iloc[-1]
            today_vol = float(today_data['volume'])
            today_turnover = float(today_data['turnover'])
            outstanding_share = float(today_data['outstanding_share'])
            circ_mv = outstanding_share * row[col_price]
            circ_mv_yi = circ_mv / 1e8
            
            recent_6 = hist.tail(6)
            if len(recent_6) < 2:
                continue
            prev_5 = recent_6.head(5)
            avg_vol_5 = prev_5['volume'].mean()
            if avg_vol_5 == 0:
                continue
            volume_ratio = today_vol / avg_vol_5
            
            turnover_pct = today_turnover * 100
            
            if volume_ratio <= 1.2:
                continue
            if turnover_pct < 3.0 or turnover_pct > 15.0:
                continue
            if circ_mv_yi < 30 or circ_mv_yi > 300:
                continue
            
            candidates_list2.append({
                '代码': code,
                '名称': name,
                '涨跌幅': row[col_change],
                '最新价': row[col_price],
                '量比': round(volume_ratio, 2),
                '换手率': round(turnover_pct, 2),
                '流通市值(亿)': round(circ_mv_yi, 2),
                '成交额': row[col_amount],
            })
            print(f"  ✅ {code} {name} 涨幅={row[col_change]:.2f}% 量比={volume_ratio:.2f} 换手={turnover_pct:.2f}% 流通市值={circ_mv_yi:.1f}亿")
        except:
            continue
    
    result = pd.DataFrame(candidates_list2)
    print(f"\n放宽条件后筛选出 {len(result)} 只股票")

if len(result) == 0:
    print("⚠️ 仍无候选，退出")
    exit()

result = result.sort_values('涨跌幅', ascending=False)
print(result[['代码', '名称', '涨跌幅', '量比', '换手率', '流通市值(亿)', '最新价']].to_string(index=False))

# ===== 第五步：成交量连续温和放大 =====
print("\n\n=== 第五步：检查成交量连续放大 ===")
valid_codes = []
for _, row in result.iterrows():
    code = row['代码']
    name = row['名称']
    try:
        end_date = datetime.now().strftime("%Y%m%d")
        start_date = (datetime.now() - timedelta(days=30)).strftime("%Y%m%d")
        hist = ak.stock_zh_a_daily(symbol=code, start_date=start_date, end_date=end_date, adjust='qfq')
        if len(hist) < 5:
            continue
        time.sleep(0.08)
        
        recent_5 = hist.tail(5)
        volumes = recent_5['volume'].values.astype(float)
        
        # 近3日成交量递增
        is_increasing_3 = False
        if len(volumes) >= 3:
            vol_last3 = volumes[-3:]
            is_increasing_3 = all(vol_last3[i] <= vol_last3[i+1] for i in range(len(vol_last3)-1))
        
        # 近5日成交量递增
        is_increasing_5 = all(volumes[i] <= volumes[i+1] for i in range(len(volumes)-1))
        
        # 放宽：近3日中2日递增也算
        vol_last3 = volumes[-3:]
        increasing_count = sum(1 for i in range(len(vol_last3)-1) if vol_last3[i] <= vol_last3[i+1])
        
        if is_increasing_3 or is_increasing_5 or increasing_count >= 1:
            valid_codes.append(code)
            print(f"  ✅ {code} {name} 近5日递增={is_increasing_5}, 近3日递增={is_increasing_3}")
        else:
            print(f"  ❌ {code} {name} 成交量未递增")
    except Exception as e:
        print(f"  ⚠️ {code} {name} 失败: {e}")
        continue

print(f"\n成交量递增的候选: {len(valid_codes)} 只")

# ===== 第六步：K线均线多头向上 =====
print("\n\n=== 第六步：检查K线均线多头排列 ===")
ma_valid_codes = []
ma_partial_codes = []  # 部分满足（MA5>MA10但MA10不一定>MA20）
for code in valid_codes:
    name_row = result[result['代码'] == code]
    name = name_row['名称'].values[0] if len(name_row) > 0 else ''
    try:
        end_date = datetime.now().strftime("%Y%m%d")
        start_date = (datetime.now() - timedelta(days=60)).strftime("%Y%m%d")
        hist = ak.stock_zh_a_daily(symbol=code, start_date=start_date, end_date=end_date, adjust='qfq')
        if len(hist) < 20:
            continue
        time.sleep(0.08)
        
        hist['MA5'] = hist['close'].rolling(5).mean()
        hist['MA10'] = hist['close'].rolling(10).mean()
        hist['MA20'] = hist['close'].rolling(20).mean()
        
        latest = hist.iloc[-1]
        prev = hist.iloc[-2]
        
        # 严格多头：MA5 > MA10 > MA20 且 MA5上升
        is_bullish = latest['MA5'] > latest['MA10'] > latest['MA20']
        ma5_rising = latest['MA5'] > prev['MA5']
        
        # 部分多头：MA5 > MA10 且 MA5上升
        is_partial = latest['MA5'] > latest['MA10'] and ma5_rising
        
        if is_bullish and ma5_rising:
            ma_valid_codes.append(code)
            print(f"  ✅ {code} {name} MA5={latest['MA5']:.2f} > MA10={latest['MA10']:.2f} > MA20={latest['MA20']:.2f}, MA5上升")
        elif is_partial:
            ma_partial_codes.append(code)
            print(f"  🔶 {code} {name} MA5={latest['MA5']:.2f} > MA10={latest['MA10']:.2f}, MA20={latest['MA20']:.2f} (部分多头)")
        else:
            print(f"  ❌ {code} {name} MA5={latest['MA5']:.2f} MA10={latest['MA10']:.2f} MA20={latest['MA20']:.2f}")
    except Exception as e:
        print(f"  ⚠️ {code} {name} 失败: {e}")
        continue

print(f"\n均线严格多头的候选: {len(ma_valid_codes)} 只")
print(f"均线部分多头的候选: {len(ma_partial_codes)} 只")

# 合并严格和部分多头
all_ma_codes = ma_valid_codes + ma_partial_codes

# ===== 第七步：20天内有涨停 =====
print("\n\n=== 第七步：检查20天内有涨停 ===")
limit_up_codes = []
for code in all_ma_codes:
    name_row = result[result['代码'] == code]
    name = name_row['名称'].values[0] if len(name_row) > 0 else ''
    try:
        end_date = datetime.now().strftime("%Y%m%d")
        start_date = (datetime.now() - timedelta(days=30)).strftime("%Y%m%d")
        hist = ak.stock_zh_a_daily(symbol=code, start_date=start_date, end_date=end_date, adjust='qfq')
        if len(hist) < 2:
            continue
        time.sleep(0.08)
        
        recent_20 = hist.tail(20).copy()
        recent_20['pct_change'] = recent_20['close'].pct_change() * 100
        has_limit_up = (recent_20['pct_change'] >= 9.8).any()
        
        if has_limit_up:
            limit_up_dates = recent_20[recent_20['pct_change'] >= 9.8]['date'].tolist()
            limit_up_codes.append(code)
            print(f"  ✅ {code} {name} 20天内有涨停: {limit_up_dates}")
        else:
            print(f"  ❌ {code} {name} 20天内无涨停")
    except Exception as e:
        print(f"  ⚠️ {code} {name} 失败: {e}")
        continue

print(f"\n20天内有涨停的候选: {len(limit_up_codes)} 只")

# ===== 最终候选池 =====
print("\n\n" + "="*60)
print("=== 最终候选池 ===")
print("="*60)

# 优先级1：8步全部通过
final_candidates = result[result['代码'].isin(limit_up_codes)]
if len(final_candidates) > 0:
    print("\n🏆 8步全部通过的标的：")
    print(final_candidates[['代码', '名称', '涨跌幅', '量比', '换手率', '流通市值(亿)', '最新价']].to_string(index=False))

# 优先级2：基础4步+均线多头（无涨停要求）
relaxed_ma = result[result['代码'].isin(all_ma_codes)]
if len(relaxed_ma) > 0:
    print("\n🥈 基础4步+均线多头（无涨停要求）：")
    print(relaxed_ma[['代码', '名称', '涨跌幅', '量比', '换手率', '流通市值(亿)', '最新价']].to_string(index=False))

# 优先级3：仅基础4步
if len(result) > 0:
    print("\n🥉 仅通过基础4步筛选：")
    print(result[['代码', '名称', '涨跌幅', '量比', '换手率', '流通市值(亿)', '最新价']].to_string(index=False))

# ===== 第八步：综合评分排序 =====
print("\n\n=== 第八步：综合评分排序 ===")

# 合并所有候选，去重
if len(final_candidates) > 0:
    score_df = final_candidates.copy()
    print("（8步全部通过）")
elif len(relaxed_ma) > 0:
    score_df = relaxed_ma.copy()
    print("（基础4步+均线多头）")
else:
    score_df = result.copy()
    print("（仅基础4步筛选）")

if len(score_df) > 0:
    score_df['涨幅分'] = 100 - abs(score_df['涨跌幅'] - 4.0) * 20
    score_df['量比分'] = np.minimum(score_df['量比'] / 3.0 * 100, 100)
    score_df['换手分'] = 100 - abs(score_df['换手率'] - 7.0) * 10
    score_df['市值分'] = 100 - abs(score_df['流通市值(亿)'] - 100) / 100 * 50
    
    # 加分项
    score_df['涨停加分'] = score_df['代码'].apply(lambda x: 10 if x in limit_up_codes else 0)
    score_df['严格多头加分'] = score_df['代码'].apply(lambda x: 10 if x in ma_valid_codes else (5 if x in ma_partial_codes else 0))
    
    score_df['综合分'] = (score_df['涨幅分'] * 0.2 + score_df['量比分'] * 0.2 + 
                          score_df['换手分'] * 0.15 + score_df['市值分'] * 0.15 +
                          score_df['涨停加分'] * 0.15 + score_df['严格多头加分'] * 0.15)
    score_df = score_df.sort_values('综合分', ascending=False)
    
    print(score_df[['代码', '名称', '涨跌幅', '量比', '换手率', '流通市值(亿)', '最新价', '综合分']].to_string(index=False))
    
    print("\n\n" + "="*60)
    print("=== 最终推荐标的（一夜持股法）===")
    print("="*60)
    top = score_df.head(15)
    for i, (_, r) in enumerate(top.iterrows(), 1):
        tag = ""
        if r['代码'] in limit_up_codes:
            tag = " [8步全通]"
        elif r['代码'] in ma_valid_codes:
            tag = " [7步通]"
        elif r['代码'] in ma_partial_codes:
            tag = " [6步通]"
        print(f"  {i:2d}. {r['代码']} {r['名称']} | 涨幅{r['涨跌幅']:.2f}% | 量比{r['量比']:.2f} | 换手{r['换手率']:.2f}% | 流通市值{r['流通市值(亿)']:.1f}亿 | 综合分{r['综合分']:.1f}{tag}")
