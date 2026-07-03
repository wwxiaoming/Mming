#!/usr/bin/env python3
"""A股板块轮动检测器 - 数据获取与分析脚本 v3（使用可用接口）"""

import akshare as ak
import pandas as pd
import warnings
import traceback
from datetime import datetime, timedelta

warnings.filterwarnings('ignore')

# ============================================================
# 1. 申万一级行业实时行情
# ============================================================
print("=" * 80)
print("【1】申万一级行业实时行情（index_realtime_sw）")
print("=" * 80)

df_realtime = pd.DataFrame()
try:
    df_realtime = ak.index_realtime_sw(symbol="一级行业")
    print(f"获取到 {len(df_realtime)} 个申万一级行业实时数据")
    # 计算涨跌幅 = (最新价 - 昨收盘) / 昨收盘 * 100
    df_realtime['涨跌幅%'] = ((df_realtime['最新价'] / df_realtime['昨收盘'] - 1) * 100).round(2)
    df_realtime = df_realtime.sort_values('涨跌幅%', ascending=False)
    print(df_realtime[['指数代码', '指数名称', '最新价', '昨收盘', '涨跌幅%', '成交额']].to_string())
except Exception as e:
    print(f"申万一级行业实时行情获取失败: {e}")
    traceback.print_exc()

print()

# ============================================================
# 2. 申万行业指数历史数据（逐个获取近60日）
# ============================================================
print("=" * 80)
print("【2】申万行业指数历史涨跌幅")
print("=" * 80)

industry_hist_data = {}
if not df_realtime.empty:
    for _, row in df_realtime.iterrows():
        code = str(row['指数代码'])
        name = str(row['指数名称'])
        try:
            df_hist = ak.index_hist_sw(symbol=code, period="day")
            if df_hist is not None and not df_hist.empty and len(df_hist) > 1:
                # 找收盘价列
                close_col = None
                for col in df_hist.columns:
                    if '收盘' in str(col) or 'close' in str(col).lower():
                        close_col = col
                        break
                if close_col is None:
                    close_col = df_hist.columns[-1]
                
                latest = float(df_hist.iloc[-1][close_col])
                
                # 5日涨跌幅
                if len(df_hist) >= 5:
                    price_5d = float(df_hist.iloc[-5][close_col])
                    chg_5d = (latest / price_5d - 1) * 100
                else:
                    chg_5d = None
                
                # 20日涨跌幅
                if len(df_hist) >= 20:
                    price_20d = float(df_hist.iloc[-20][close_col])
                    chg_20d = (latest / price_20d - 1) * 100
                else:
                    chg_20d = None
                
                # 60日涨跌幅
                if len(df_hist) >= 60:
                    price_60d = float(df_hist.iloc[-60][close_col])
                    chg_60d = (latest / price_60d - 1) * 100
                else:
                    first = float(df_hist.iloc[0][close_col])
                    chg_60d = (latest / first - 1) * 100
                
                industry_hist_data[name] = {
                    '指数代码': code,
                    '5日涨跌幅%': round(chg_5d, 2) if chg_5d is not None else None,
                    '20日涨跌幅%': round(chg_20d, 2) if chg_20d is not None else None,
                    '60日涨跌幅%': round(chg_60d, 2) if chg_60d is not None else None,
                    '当日涨跌幅%': round((latest / float(row['昨收盘']) - 1) * 100, 2) if float(row['昨收盘']) > 0 else None,
                    '最新价': round(latest, 2)
                }
                print(f"  {name}({code}): 5日={chg_5d:.2f}%" if chg_5d else f"  {name}({code}): 5日=N/A", end="")
                print(f", 20日={chg_20d:.2f}%" if chg_20d else ", 20日=N/A", end="")
                print(f", 60日={chg_60d:.2f}%" if chg_60d else ", 60日=N/A")
        except Exception as e2:
            print(f"  {name}({code}) 历史数据获取失败: {e2}")
            continue

print()

# ============================================================
# 3. 宏观经济数据
# ============================================================
print("=" * 80)
print("【3】宏观经济数据")
print("=" * 80)

# 3a. LPR
print("--- LPR利率 ---")
try:
    df_lpr = ak.macro_china_lpr()
    print("LPR利率(最近6期):")
    print(df_lpr.tail(6).to_string())
except Exception as e:
    print(f"LPR获取失败: {e}")

print()

# 3b. GDP
print("--- GDP ---")
try:
    df_gdp = ak.macro_china_gdp()
    print("GDP(最近4期):")
    print(df_gdp.head(4).to_string())
except Exception as e:
    print(f"GDP获取失败: {e}")

print()

# 3c. M2
print("--- M2 ---")
try:
    df_m2 = ak.macro_china_money_supply()
    print("M2(最近6期):")
    print(df_m2.head(6).to_string())
except Exception as e:
    print(f"M2获取失败: {e}")

print()

# 3d. CPI/PPI 年率
print("--- CPI年率 ---")
try:
    df_cpi = ak.macro_china_cpi_yearly()
    print("CPI年率(最近6期):")
    print(df_cpi.head(6).to_string())
except Exception as e:
    print(f"CPI年率获取失败: {e}")

print()

print("--- PPI年率 ---")
try:
    df_ppi = ak.macro_china_ppi_yearly()
    print("PPI年率(最近6期):")
    print(df_ppi.head(6).to_string())
except Exception as e:
    print(f"PPI年率获取失败: {e}")

print()

# 3e. PMI
print("--- 官方PMI ---")
try:
    df_pmi = ak.macro_china_pmi()
    print("官方PMI(最近6期):")
    print(df_pmi.head(6).to_string())
except Exception as e:
    print(f"官方PMI获取失败: {e}")

print()

# 3f. 财新PMI
print("--- 财新PMI ---")
try:
    df_cx = ak.macro_china_cx_pmi_yearly()
    print("财新PMI(最近6期):")
    print(df_cx.head(6).to_string())
except Exception as e:
    print(f"财新PMI获取失败: {e}")

print()

# 3g. 社会消费品零售
print("--- 社零 ---")
try:
    df_retail = ak.macro_china_consumer_goods_retail()
    print("社零(最近4期):")
    print(df_retail.head(4).to_string())
except Exception as e:
    print(f"社零获取失败: {e}")

print()

# 3h. 固定资产投资
print("--- 固定资产投资 ---")
try:
    df_fai = ak.macro_china_fixed_asset_invest()
    print("固定资产投资(最近4期):")
    print(df_fai.head(4).to_string())
except Exception as e:
    print(f"固定资产投资获取失败: {e}")

print()

# ============================================================
# 4. 申万一级行业估值数据
# ============================================================
print("=" * 80)
print("【4】申万一级行业估值数据")
print("=" * 80)

try:
    df_sw_info = ak.sw_index_first_info()
    print(f"获取到 {len(df_sw_info)} 个行业估值数据")
    print(df_sw_info.to_string())
except Exception as e:
    print(f"行业估值获取失败: {e}")

print()

# ============================================================
# 5. 北向资金历史数据
# ============================================================
print("=" * 80)
print("【5】北向资金历史数据")
print("=" * 80)

try:
    df_north = ak.stock_hsgt_hist_em(symbol="北向资金")
    print(f"获取到 {len(df_north)} 条北向资金数据")
    print("最近20日:")
    print(df_north.tail(20)[['日期', '当日成交净买额', '当日资金流入', '沪深300', '沪深300-涨跌幅']].to_string())
    
    # 计算近5日/20日净买入
    recent_5 = df_north.tail(5)
    recent_20 = df_north.tail(20)
    net_5d = recent_5['当日成交净买额'].sum() if recent_5['当日成交净买额'].notna().any() else 'N/A'
    net_20d = recent_20['当日成交净买额'].sum() if recent_20['当日成交净买额'].notna().any() else 'N/A'
    print(f"\n近5日北向净买入合计: {net_5d}")
    print(f"近20日北向净买入合计: {net_20d}")
except Exception as e:
    print(f"北向资金获取失败: {e}")

print()

# ============================================================
# 6. 汇总：相对强弱排名 & 周期vs防御对比
# ============================================================
print("=" * 80)
print("【6】汇总：相对强弱排名 & 周期vs防御轮动判断")
print("=" * 80)

if industry_hist_data:
    df_summary = pd.DataFrame(industry_hist_data).T
    # 按多种维度排序
    for col in ['20日涨跌幅%', '60日涨跌幅%', '5日涨跌幅%']:
        if col in df_summary.columns:
            df_sorted = df_summary.sort_values(col, ascending=False)
            print(f"\n=== 按{col}排名 ===")
            print(df_sorted.to_string())
            break
    
    # 周期 vs 防御分类
    cyclical = ['银行', '非银金融', '房地产', '有色金属', '煤炭', '石油石化', '钢铁', 
                '基础化工', '建筑材料', '建筑装饰', '机械设备', '汽车', '电子']
    defensive = ['食品饮料', '医药生物', '公用事业', '交通运输', '农林牧渔', 
                 '社会服务', '美容护理', '纺织服饰']
    growth = ['计算机', '通信', '电力设备', '传媒', '国防军工']
    
    for period_label, col in [('5日', '5日涨跌幅%'), ('20日', '20日涨跌幅%'), ('60日', '60日涨跌幅%')]:
        cyclical_chgs = [industry_hist_data[n][col] for n in cyclical if n in industry_hist_data and industry_hist_data[n][col] is not None]
        defensive_chgs = [industry_hist_data[n][col] for n in defensive if n in industry_hist_data and industry_hist_data[n][col] is not None]
        growth_chgs = [industry_hist_data[n][col] for n in growth if n in industry_hist_data and industry_hist_data[n][col] is not None]
        
        if cyclical_chgs and defensive_chgs:
            avg_c = sum(cyclical_chgs) / len(cyclical_chgs)
            avg_d = sum(defensive_chgs) / len(defensive_chgs)
            avg_g = sum(growth_chgs) / len(growth_chgs) if growth_chgs else 0
            
            print(f"\n=== {period_label}周期 vs 防御轮动信号 ===")
            print(f"  周期板块平均{period_label}涨跌幅: {avg_c:.2f}%  (样本: {len(cyclical_chgs)})")
            print(f"  防御板块平均{period_label}涨跌幅: {avg_d:.2f}%  (样本: {len(defensive_chgs)})")
            print(f"  成长板块平均{period_label}涨跌幅: {avg_g:.2f}%  (样本: {len(growth_chgs)})")
            print(f"  周期-防御差值: {avg_c - avg_d:.2f}%")
            if avg_c > avg_d:
                print(f"  >>> {period_label}信号: 周期 > 防御 (+{avg_c - avg_d:.2f}%)")
            else:
                print(f"  >>> {period_label}信号: 防御 > 周期 (+{avg_d - avg_c:.2f}%)")
    
    # 综合判断
    print("\n" + "=" * 60)
    print("【综合轮动判断】")
    print("=" * 60)
    
    # 使用20日数据作为主要判断依据
    cyclical_20 = [industry_hist_data[n]['20日涨跌幅%'] for n in cyclical if n in industry_hist_data and industry_hist_data[n]['20日涨跌幅%'] is not None]
    defensive_20 = [industry_hist_data[n]['20日涨跌幅%'] for n in defensive if n in industry_hist_data and industry_hist_data[n]['20日涨跌幅%'] is not None]
    
    if cyclical_20 and defensive_20:
        avg_cyclical_20 = sum(cyclical_20) / len(cyclical_20)
        avg_defensive_20 = sum(defensive_20) / len(defensive_20)
        spread = avg_cyclical_20 - avg_defensive_20
        
        if spread > 2:
            signal = "强周期占优"
            desc = "市场明显偏好周期敏感型行业，经济扩张预期强烈"
        elif spread > 0:
            signal = "弱周期占优"
            desc = "市场略微偏好周期型行业，但优势不显著"
        elif spread > -2:
            signal = "弱防御占优"
            desc = "市场略微偏好防御型行业，但优势不显著"
        else:
            signal = "强防御占优"
            desc = "市场明显偏好防御型行业，避险情绪较重"
        
        print(f"\n周期 vs 防御综合判断: {signal}")
        print(f"周期板块20日均值: {avg_cyclical_20:.2f}%, 防御板块20日均值: {avg_defensive_20:.2f}%, 差值: {spread:.2f}%")
        print(f"解读: {desc}")
        
        # 列出周期/防御中表现最强和最弱的行业
        print("\n周期板块内排名(20日):")
        for name in sorted(cyclical, key=lambda x: industry_hist_data.get(x, {}).get('20日涨跌幅%', -999) or -999, reverse=True):
            if name in industry_hist_data and industry_hist_data[name]['20日涨跌幅%'] is not None:
                print(f"  {name}: {industry_hist_data[name]['20日涨跌幅%']:.2f}%")
        
        print("\n防御板块内排名(20日):")
        for name in sorted(defensive, key=lambda x: industry_hist_data.get(x, {}).get('20日涨跌幅%', -999) or -999, reverse=True):
            if name in industry_hist_data and industry_hist_data[name]['20日涨跌幅%'] is not None:
                print(f"  {name}: {industry_hist_data[name]['20日涨跌幅%']:.2f}%")
        
        print("\n成长板块内排名(20日):")
        for name in sorted(growth, key=lambda x: industry_hist_data.get(x, {}).get('20日涨跌幅%', -999) or -999, reverse=True):
            if name in industry_hist_data and industry_hist_data[name]['20日涨跌幅%'] is not None:
                print(f"  {name}: {industry_hist_data[name]['20日涨跌幅%']:.2f}%")

print("\n数据获取完成！")
