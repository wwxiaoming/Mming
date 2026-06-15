import akshare as ak
import pandas as pd
from datetime import datetime, timedelta
import time
import json

today = datetime.now().strftime("%Y%m%d")
print(f"分析日期: {today}")

# ===== 1. 涨停板数据 =====
print("=" * 60)
print("涨停板数据分析")
print("=" * 60)

try:
    # 涨停板池
    df_zt = ak.stock_zt_pool_em(date=today)
    print(f"今日涨停家数: {len(df_zt)}")
    if len(df_zt) > 0:
        print("\n涨停板详情:")
        cols = [c for c in ['代码', '名称', '涨跌幅', '封板资金', '最新价', '涨停统计', '连板数'] if c in df_zt.columns]
        for _, row in df_zt.head(30).iterrows():
            info = {c: row.get(c, 'N/A') for c in cols}
            print(f"  {row.get('代码','')} {row.get('名称','')}: 涨幅={row.get('涨跌幅','N/A')}% 连板={row.get('连板数', row.get('涨停统计','N/A'))}")

        # 连板梯队
        if '连板数' in df_zt.columns:
            print("\n连板梯队:")
            for n in sorted(df_zt['连板数'].unique(), reverse=True):
                count = len(df_zt[df_zt['连板数'] == n])
                stocks = df_zt[df_zt['连板数'] == n]['名称'].tolist()
                print(f"  {n}连板: {count}只 - {', '.join(stocks[:5])}")
except Exception as e:
    print(f"涨停板数据获取失败: {e}")

# ===== 2. 炸板率 =====
print("\n" + "=" * 60)
print("炸板率分析")
print("=" * 60)
try:
    df_zb = ak.stock_zt_pool_zbgc_em(date=today)
    print(f"今日炸板家数: {len(df_zb)}")
    if len(df_zb) > 0:
        for _, row in df_zb.head(10).iterrows():
            print(f"  {row.get('代码','')} {row.get('名称','')}: 涨幅={row.get('涨跌幅','N/A')}%")
except Exception as e:
    print(f"炸板数据获取失败: {e}")

# ===== 3. 跌停板数据 =====
print("\n" + "=" * 60)
print("跌停板数据")
print("=" * 60)
try:
    df_dt = ak.stock_zt_pool_dtgc_em(date=today)
    print(f"今日跌停家数: {len(df_dt)}")
except Exception as e:
    print(f"跌停数据获取失败: {e}")

# ===== 4. 计算市场情绪温度 =====
print("\n" + "=" * 60)
print("市场情绪温度计算")
print("=" * 60)

zt_count = 0
zb_count = 0
dt_count = 0

try:
    df_zt = ak.stock_zt_pool_em(date=today)
    zt_count = len(df_zt)
except: pass

try:
    df_zb = ak.stock_zt_pool_zbgc_em(date=today)
    zb_count = len(df_zb)
except: pass

try:
    df_dt = ak.stock_zt_pool_dtgc_em(date=today)
    dt_count = len(df_dt)
except: pass

total_zt_attempts = zt_count + zb_count
seal_rate = (zt_count / total_zt_attempts * 100) if total_zt_attempts > 0 else 0
zt_dt_ratio = (zt_count / dt_count) if dt_count > 0 else float('inf')

print(f"涨停: {zt_count}家")
print(f"炸板: {zb_count}家")
print(f"跌停: {dt_count}家")
print(f"封板率: {seal_rate:.1f}%")
print(f"涨跌停比: {zt_dt_ratio:.1f}")

# 情绪温度评分 (0-100)
score = 50  # 基准分
# 涨停加分
if zt_count > 50: score += 15
elif zt_count > 30: score += 10
elif zt_count > 15: score += 5
elif zt_count < 5: score -= 10
# 跌停减分
if dt_count > 20: score -= 15
elif dt_count > 10: score -= 10
elif dt_count > 5: score -= 5
# 封板率加分
if seal_rate > 80: score += 10
elif seal_rate > 60: score += 5
elif seal_rate < 40: score -= 10
# 炸板率减分
if zb_count > 20: score -= 10
elif zb_count > 10: score -= 5

score = max(0, min(100, score))
print(f"\n市场情绪温度: {score}/100")
print(f"情绪判断: {'过热' if score >= 80 else '偏热' if score >= 65 else '正常' if score >= 45 else '偏冷' if score >= 30 else '极冷'}")

# ===== 5. 20天涨停记录查询 =====
print("\n" + "=" * 60)
print("20天涨停记录（用于验证选股条件2）")
print("=" * 60)

# 查询最近20天的涨停记录
zt_history = {}
for i in range(20):
    d = (datetime.now() - timedelta(days=i)).strftime("%Y%m%d")
    try:
        df = ak.stock_zt_pool_em(date=d)
        if len(df) > 0:
            for _, row in df.iterrows():
                code = row.get('代码', '')
                name = row.get('名称', '')
                if code not in zt_history:
                    zt_history[code] = {'name': name, 'count': 0, 'dates': []}
                zt_history[code]['count'] += 1
                zt_history[code]['dates'].append(d)
    except:
        pass
    time.sleep(0.5)

print(f"20天内出现过涨停的股票数: {len(zt_history)}")
# 按涨停次数排序
sorted_zt = sorted(zt_history.items(), key=lambda x: x[1]['count'], reverse=True)
print("\n涨停次数TOP30:")
for code, info in sorted_zt[:30]:
    print(f"  {code} {info['name']}: {info['count']}次涨停, 日期={info['dates'][:3]}")

# 保存结果
with open('/workspace/zt_history_20d.json', 'w') as f:
    json.dump(zt_history, f, ensure_ascii=False)
print("\n20天涨停记录已保存到 /workspace/zt_history_20d.json")
