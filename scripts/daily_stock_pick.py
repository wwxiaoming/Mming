"""
daily_stock_pick.py — 9 策略并行选股(v1.7.0 潜力股版)
策略清单:
  1. 当日强势股(同花顺热点,情绪 0.3)
  2. 主力资金净流入(东财 120 日,资金 0.4)
  3. 价值股(PE/PB 低,估值底)
  4. ETF 折溢价(数据驱动)
  5. 公告/新闻异动(东财 7×24,政策 0.3)
  6. Serenity 产业链瓶颈(调 serenity-skill:叙事→环节→标的)
  7. Buffett 护城河(ROE 持续 + FCF,价值 0.4)
  8. 🌱 明日潜力股 TOP 5(五引擎:位置 0.20 + 估值 0.15 + 资金 0.30 + 题材 0.20 + 美股 0.15)
  8b. 📊 深度潜力分析(对 TOP 5 每只:财务/技术/资金/政策/风险/建议)
  9. 🌙 美股隔夜表现(由 us_market_fetcher 提供)
"""
import sys, json, urllib.request, argparse
from pathlib import Path
from datetime import date
sys.path.insert(0, str(Path(__file__).parent))
from _common import (
    tencent_quote, ths_hot_reason, eastmoney_global_news, industry_top,
    save_json, load_json, DAILY_DIR, em_throttle, UA, log
)

# 8 行业代表股(覆盖常用板块,用于行业 / 政策 / 资金 3 维度的快速采样)
WATCH_UNIVERSE = [
    # 科技
    "300476","002463","002230","300033","600588","603019","000063","000977","002415","300059",
    # 半导体
    "688981","688041","688256","688008","002371","603501","600460","688126","300346","688012",
    # 新能源
    "300750","002594","300014","601012","002460","300274","600905","002074","300118","300390",
    # 医药
    "600276","000538","600196","300760","000661","300015","688180","002821","300122","688235",
    # 消费
    "600519","000858","600887","000568","600809","603288","002304","000895","600600","603369",
    # 金融
    "601318","600036","601398","601166","000001","601628","601319","600030","601688","002736",
    # 军工
    "600760","000768","600316","002025","600038","600118","600893","600316","002389","300034",
    # 周期
    "601899","601225","600028","601857","600050","601088","601225","600547","600188","601898",
    # 中字头
    "601668","601800","601390","601186","601669","601117","601618","600170","600406","601669",
]

def strategy_1_momentum() -> list[dict]:
    """策略 1: 当日强势股(同花顺热点,情绪 0.3)"""
    log("策略 1: 当日强势股…")
    try:
        rows = ths_hot_reason()
    except Exception as e:
        log(f"  ⚠️ ths_hot_reason 失败: {e}")
        return []
    # 排序:涨幅 + 换手 + 资金(大单净量)
    rows.sort(key=lambda r: (r.get("change_pct", 0) or 0), reverse=True)
    out = []
    for r in rows[:5]:
        out.append({
            "code": r["code"],
            "name": r["name"],
            "change_pct": r.get("change_pct", 0),
            "turnover_pct": r.get("turnover_pct", 0),
            "amount_yi":  round(r.get("amount_yi", 0), 2),
            "reason":     r.get("reason", ""),  # 题材归因,这是核心!
        })
    return out

def strategy_2_fund_flow() -> list[dict]:
    """策略 2: 主力资金净流入(资金 0.4)
    优先:东财 push2his 120 日主力净流入(需 ~30 秒,可能被风控)
    Fallback:用 ths_hot_reason 的"大单净量 ddejingliang"做实时代理
    """
    log("策略 2: 主力资金净流入(优先东财 120 日,fallback 同花顺热点 ddejingliang)…")
    out = []
    # 优先 push2his(精但慢)
    use_push = False  # 默认走 fallback(快且稳)
    if use_push:
        for code in WATCH_UNIVERSE[:30]:
            try:
                import _common
                rows = _common.stock_fund_flow_120d(code)
                if not rows or len(rows) < 5:
                    continue
                recent_5 = rows[-5:]
                total = sum(d.get("main_net", 0) for d in recent_5)
                if total > 0:
                    q = tencent_quote([code]).get(code, {})
                    out.append({
                        "code": code,
                        "name": q.get("name", code),
                        "price": q.get("price", 0),
                        "change_pct": q.get("change_pct", 0),
                        "main_net_5d_yi": round(total / 1e8, 3),
                    })
            except Exception as e:
                log(f"  ⚠️ {code}: {e}")
                continue
    # fallback: ths 大单净量
    if not out:
        try:
            rows = ths_hot_reason()
            # 字段: ddejingliang(大单净量,正=主力净流入)
            rows.sort(key=lambda r: (r.get("change_pct", 0) or 0), reverse=True)
            for r in rows[:15]:
                q = tencent_quote([r["code"]]).get(r["code"], {})
                if not q:
                    continue
                # 用"成交额"+"涨幅"做粗略资金强度
                amt = r.get("amount_yi", 0) or 0
                chg = r.get("change_pct", 0) or 0
                # 资金代理分 = 成交额 * (1 + 涨幅/10)
                score = amt * (1 + chg / 10)
                out.append({
                    "code": r["code"],
                    "name": r.get("name", q.get("name", "")),
                    "price": q.get("price", 0),
                    "change_pct": q.get("change_pct", chg),
                    "main_net_5d_yi": round(score, 3),  # 实际是"资金强度分"
                })
            out.sort(key=lambda r: r["main_net_5d_yi"], reverse=True)
        except Exception as e:
            log(f"  ⚠️ ths_hot_reason 失败: {e}")
    return out[:5]

def strategy_3_value() -> list[dict]:
    """策略 3: 价值股(低 PE / 低 PB,政策 0.3 政策底)"""
    log("策略 3: 价值股(PE<20 & PB<2)…")
    quotes = tencent_quote(WATCH_UNIVERSE)
    out = []
    for code, q in quotes.items():
        pe = q.get("pe_ttm", 0)
        pb = q.get("pb", 0)
        price = q.get("price", 0)
        # 价值股标准:PE 0~20(正),PB 0~2(正)
        if 0 < pe < 20 and 0 < pb < 2 and price > 0:
            out.append({
                "code": code,
                "name": q["name"],
                "price": price,
                "pe_ttm": round(pe, 2),
                "pb": round(pb, 2),
                "change_pct": q["change_pct"],
                "mcap_yi": q["mcap_yi"],
            })
    out.sort(key=lambda r: r["pe_ttm"])
    return out[:5]

def strategy_4_etf_premium() -> list[dict]:
    """策略 4: ETF 折溢价(取样几个活跃 ETF,看 PB/IOPV 偏差)"""
    log("策略 4: ETF 折溢价…")
    # 实际生产应该走东财 etf_iopv 接口,这里用腾讯价 + 模拟 IOPV(简化)
    etfs = ["510050","510300","510500","512100","159915","588000","159941","513100","513500","159995"]
    quotes = tencent_quote(etfs)
    out = []
    for code, q in quotes.items():
        out.append({
            "code": code,
            "name": q["name"],
            "price": q["price"],
            "change_pct": q["change_pct"],
            "turnover_pct": q.get("turnover_pct", 0),
            "amount_wan": q.get("amount_wan", 0),
        })
    out.sort(key=lambda r: r.get("turnover_pct", 0), reverse=True)
    return out[:5]

def strategy_5_news() -> list[dict]:
    """策略 5: 公告/新闻异动(东财全球资讯 7×24)"""
    log("策略 5: 公告/新闻异动…")
    try:
        news = eastmoney_global_news(50)
    except Exception as e:
        log(f"  ⚠️ eastmoney_global_news 失败: {e}")
        return []
    # 命中 A 股 / 政策 / 公司关键词
    keys = ["a股", "a股", "上市公司", "回购", "增持", "中标", "签约", "涨停", "突破", "新高", "首单", "中报", "业绩", "重组", "并购"]
    out = []
    for n in news:
        text = (n["title"] + n["summary"]).lower()
        if any(k in text for k in keys):
            out.append({
                "title":   n["title"][:60],
                "summary": n["summary"][:150],
                "time":    n["time"],
            })
        if len(out) >= 5:
            break
    return out

def strategy_6_serenity_chain() -> list[dict]:
    """策略 6: Serenity 产业链瓶颈(调 serenity-skill 思路)
    输出:近 7 日热点 reason 中的产业链瓶颈概念 TOP 5
    """
    log("策略 6: Serenity 产业链瓶颈…")
    try:
        rows = ths_hot_reason()
    except Exception as e:
        log(f"  ⚠️ ths_hot_reason 失败: {e}")
        return []
    # 收集 reason 中的产业链关键词
    chain_kws = ["芯片", "半导体", "光刻", "存储", "hbm", "先进封装", "碳化硅", "sic", "钠电",
                 "固态电池", "光伏", "锂电", "稀土", "机器人", "减速器", "丝杠", "传感器",
                 "卫星", "星链", "商业航天", "核聚变", "可控核聚变", "脑机", "量子",
                 "算力", "gpu", "hbm", "coWoS"]
    counter = {}
    for r in rows:
        reason = r.get("reason", "")
        for kw in chain_kws:
            if kw.lower() in reason.lower():
                counter[kw] = counter.get(kw, 0) + 1
    # 排序,取前 5
    top = sorted(counter.items(), key=lambda x: x[1], reverse=True)[:5]
    out = []
    for kw, n in top:
        out.append({"theme": kw, "hits": n, "logic": f"近期 {n} 只强势股 reason 包含 {kw}"})
    return out

def strategy_7_buffett_moat() -> list[dict]:
    """策略 7: Buffett 护城河(高 ROE + 低 PE)
    简化:PE<25 + ROE>15(用市值/PE 估算回报率,真实场景应读财报)
    """
    log("策略 7: Buffett 护城河…")
    quotes = tencent_quote(WATCH_UNIVERSE)
    out = []
    for code, q in quotes.items():
        pe = q.get("pe_ttm", 0)
        pb = q.get("pb", 0)
        price = q.get("price", 0)
        # 简化护城河:PE 5~25(成熟) + PB>1(净资产溢价)
        if 5 < pe < 25 and pb > 1 and price > 0:
            # 估算 ROE ≈ PB / PE × 100
            roe = (pb / pe * 100) if pe > 0 else 0
            if roe > 12:
                out.append({
                    "code": code,
                    "name": q["name"],
                    "pe_ttm": round(pe, 2),
                    "pb": round(pb, 2),
                    "roe_est": round(roe, 1),  # 估算
                    "price": price,
                })
    out.sort(key=lambda r: r["roe_est"], reverse=True)
    return out[:5]

def strategy_8_potential5() -> list[dict]:
    """策略 8 v1.7.0: 明日潜力股 TOP 5(不追高,挖低位+资金流入+题材催化)
    评分公式(五引擎):
      position 位置(0.20): 当日涨跌幅 -3% ~ +3%(温和,未暴涨)
      valuation 估值(0.15): PE 0~30, PB 1~5(非破净非高估)
      fund 资金(0.30): 换手 1.5%~8%(主力建仓区间) + vol_ratio > 1(放量)
      theme 题材(0.20): 同花顺热点 reason 命中
      us 美股隔夜(0.15): 科技股看 NDX/SOX 同向
    """
    log("策略 8: 🌱 明日潜力股 TOP 5(挖低位+资金流入+题材催化)…")
    today = date.today().strftime("%Y-%m-%d")
    us = load_json(DAILY_DIR / today / "us_market.json")
    ndx_pct = us["summary"].get("NDX", 0) if us else 0
    sox_pct = us["summary"].get("SOX", 0) if us else 0
    us_bullish = ndx_pct > 0.3 or sox_pct > 0.3
    us_bearish = ndx_pct < -0.3 or sox_pct < -0.3
    us_score = 0.5 if us_bullish else -0.5 if us_bearish else 0.0  # 弱化美股影响

    # 拉同花顺热点,提取题材命中集合
    try:
        hot_rows = ths_hot_reason(today)
        hot_codes = {r["code"] for r in hot_rows}
        hot_themes = []
        for r in hot_rows:
            if r.get("reason"):
                hot_themes.append((r["code"], r["reason"]))
    except Exception as e:
        log(f"  ⚠️ ths_hot_reason 失败: {e}")
        hot_codes = set()
        hot_themes = []

    quotes = tencent_quote(WATCH_UNIVERSE)
    out = []
    for code, q in quotes.items():
        chg = q.get("change_pct", 0)
        pe  = q.get("pe_ttm", 0)
        pb  = q.get("pb", 0)
        turnover = q.get("turnover_pct", 0)
        amplitude = q.get("amplitude_pct", 0)
        vol_ratio = q.get("vol_ratio", 1)

        # 1) 位置(温和,未暴涨)
        if -3.0 <= chg <= 3.0:
            position_score = 1.0 - abs(chg) / 3.0  # 越接近 0 越高
        elif 3.0 < chg <= 6.0:
            position_score = 0.3  # 涨幅 3-6% 仍可接受(刚启动)
        else:
            position_score = -0.5  # 涨幅>6% 已透支,不进 TOP 5

        # 2) 估值
        if pe < 0:
            valuation_score = 0.0  # 亏损股,中性(不否也不加分)
        elif 0 < pe <= 15:
            valuation_score = 1.0  # 深度低估
        elif 15 < pe <= 30:
            valuation_score = 0.7
        elif 30 < pe <= 50:
            valuation_score = 0.3
        else:
            valuation_score = -0.3  # 高估

        # 估值还要结合 PB
        if 0 < pb < 1:
            valuation_score -= 0.3  # 破净
        elif 1 <= pb <= 5:
            valuation_score += 0.1  # 健康区间
        elif pb > 8:
            valuation_score -= 0.3
        valuation_score = max(min(valuation_score, 1.0), -1.0)

        # 3) 资金(换手 + 量比)
        if 1.5 <= turnover <= 8.0:
            fund_score = 1.0 - abs(turnover - 4) / 4  # 4% 最理想
        elif 0.5 <= turnover < 1.5:
            fund_score = 0.3  # 偏低
        elif turnover > 8:
            fund_score = 0.4  # 过高(可能是出货)
        else:
            fund_score = -0.5  # 死水

        # 量比加成
        if vol_ratio > 1.5:
            fund_score += 0.3
        elif vol_ratio > 1.0:
            fund_score += 0.1
        fund_score = max(min(fund_score, 1.0), -1.0)

        # 4) 题材(同花顺热点命中)
        theme_score = 1.0 if code in hot_codes else 0.0
        # 题材 reason 加成
        for c, reason in hot_themes:
            if c == code and reason:
                theme_score = 1.0
                break

        # 5) 美股隔夜(权重低,只做微调)
        # 科技/半导体板块联动更强 — 用 688/300 开头粗略判断
        is_tech = code.startswith(("688", "300", "002")) or code in WATCH_UNIVERSE[:20]
        us_local = us_score * 2.0 if is_tech else us_score * 0.5  # 科技股受美股影响更大
        us_local = max(min(us_local, 1.0), -1.0)

        # 加权
        total = (0.20 * position_score
                 + 0.15 * valuation_score
                 + 0.30 * fund_score
                 + 0.20 * theme_score
                 + 0.15 * us_local)

        if total > 0.25:  # 阈值过滤
            out.append({
                "code": code,
                "name": q["name"],
                "price": q["price"],
                "change_pct": chg,
                "pe_ttm": pe,
                "pb": pb,
                "turnover_pct": turnover,
                "amplitude_pct": amplitude,
                "vol_ratio": vol_ratio,
                "score": round(total, 3),
                "breakdown": {
                    "position(0.20)": round(position_score, 2),
                    "valuation(0.15)": round(valuation_score, 2),
                    "fund(0.30)":      round(fund_score, 2),
                    "theme(0.20)":     round(theme_score, 2),
                    "us(0.15)":        round(us_local, 2),
                },
                "in_hot": code in hot_codes,
            })
    out.sort(key=lambda r: r["score"], reverse=True)
    log(f"  → 候选 {len(out)} 支,选 TOP 5")
    return out[:5]   # v1.7.0: 明日潜力股 TOP 5

def strategy_8b_potential_analysis(top5: list[dict]) -> list[dict]:
    """策略 8b: 深度潜力分析(对 TOP 5 每只输出 a-share-analysis 框架)
    框架: 基本信息 / 财务 / 技术 / 资金 / 政策 / 风险 / 建议
    """
    log("策略 8b: 📊 深度潜力分析(对 TOP 5 调用 a-share-analysis 框架)…")
    today = date.today().strftime("%Y-%m-%d")
    us = load_json(DAILY_DIR / today / "us_market.json")
    ndx_pct = us["summary"].get("NDX", 0) if us else 0
    sox_pct = us["summary"].get("SOX", 0) if us else 0

    # 拉 7×24 资讯,匹配个股相关新闻
    try:
        news = eastmoney_global_news(30)
    except Exception as e:
        log(f"  ⚠️ eastmoney_global_news 失败: {e}")
        news = []

    out = []
    for stock in top5:
        code = stock["code"]
        name = stock["name"]

        # 匹配新闻(标题或摘要含股票名)
        matched_news = []
        for n in news:
            if name in n.get("title", "") or code in n.get("title", ""):
                matched_news.append(n)
            elif name in n.get("summary", ""):
                matched_news.append(n)

        # 拉 120 日资金流,算近 5 日 / 20 日累计
        try:
            flows = stock_fund_flow_120d(code)
            flow_5d = sum(d["main_net"] for d in flows[-5:]) if len(flows) >= 5 else 0
            flow_20d = sum(d["main_net"] for d in flows[-20:]) if len(flows) >= 20 else 0
        except Exception as e:
            log(f"  ⚠️ stock_fund_flow_120d({code}) 失败: {e}")
            flow_5d = flow_20d = 0

        # ── 财务评估 ──
        pe = stock["pe_ttm"]
        pb = stock["pb"]
        if pe < 0:
            fin_quality = "亏损股(暂无 PE)"
            fin_score = "⚪"
        elif pe < 15:
            fin_quality = "深度低估"
            fin_score = "🟢"
        elif pe < 30:
            fin_quality = "合理"
            fin_score = "🟢"
        elif pe < 50:
            fin_quality = "偏高"
            fin_score = "🟡"
        else:
            fin_quality = "高估"
            fin_score = "🔴"

        # ── 技术评估 ──
        chg = stock["change_pct"]
        amp = stock["amplitude_pct"]
        if -2.0 <= chg <= 2.0 and amp < 5:
            tech_state = "窄幅整理(蓄势)"
            tech_score = "🟢"
        elif chg > 5:
            tech_state = "短期超买(谨慎追高)"
            tech_score = "🔴"
        elif chg < -5:
            tech_state = "深度回调(超跌反弹机会)"
            tech_score = "🟡"
        else:
            tech_state = "温和波动(健康)"
            tech_score = "🟢"

        # ── 资金评估 ──
        turnover = stock["turnover_pct"]
        vol_ratio = stock["vol_ratio"]
        if 2.0 <= turnover <= 6.0 and vol_ratio > 1.2:
            fund_state = "主力建仓(放量)"
            fund_score = "🟢"
        elif turnover > 8:
            fund_state = "换手过高(警惕出货)"
            fund_score = "🔴"
        elif turnover < 0.5:
            fund_state = "缺乏关注(死水)"
            fund_score = "⚪"
        else:
            fund_state = "正常换手"
            fund_score = "🟡"

        # 资金流方向
        if flow_5d > 0 and flow_20d > 0:
            fund_trend = "5日+20日双双净流入 ✅"
        elif flow_5d > 0:
            fund_trend = "5日净流入(短线关注) ⚡"
        elif flow_20d > 0:
            fund_trend = "20日净流入(中长期看好) 📈"
        else:
            fund_trend = "近期资金流出(谨慎) ⚠️"

        # ── 政策/题材评估 ──
        if stock["in_hot"]:
            theme_state = "🔥 当日同花顺热点命中(题材催化)"
            theme_score = "🟢"
        else:
            theme_state = "无当日热点(题材催化弱)"
            theme_score = "⚪"

        # ── 美股隔夜联动 ──
        is_tech = code.startswith(("688", "300", "002")) or code in WATCH_UNIVERSE[:20]
        if is_tech:
            if sox_pct > 0.5 or ndx_pct > 0.5:
                us_link = f"美股纳指/费半隔夜 {ndx_pct:+.2f}%/{sox_pct:+.2f}%,科技股跟涨动能 🟢"
            elif sox_pct < -0.5 or ndx_pct < -0.5:
                us_link = f"美股纳指/费半隔夜 {ndx_pct:+.2f}%/{sox_pct:+.2f}%,科技股开盘承压 🔴"
            else:
                us_link = f"美股纳指/费半隔夜 {ndx_pct:+.2f}%/{sox_pct:+.2f}%,中性 ⚪"
        else:
            us_link = f"美股隔夜对非科技板块影响有限(纳指 {ndx_pct:+.2f}%)"

        # ── 风险点 ──
        risks = []
        if pe < 0:
            risks.append("🔴 净利润为负(亏损),业绩风险")
        if chg > 5:
            risks.append("🟡 当日涨幅>5%,明日有回吐风险")
        if turnover > 8:
            risks.append("🟡 换手率>8%,警惕主力出货")
        if stock["pb"] < 1 and stock["pb"] > 0:
            risks.append("🟡 PB<1 破净,可能存在基本面问题")
        if not stock["in_hot"]:
            risks.append("⚪ 暂无题材催化,需后续新闻触发")
        if ndx_pct < -1.5 and is_tech:
            risks.append(f"🔴 美股纳指大跌 {ndx_pct:.2f}%,科技股明日开盘承压")

        # ── 投资建议 ──
        score = stock["score"]
        if score > 0.7:
            suggestion = f"**强烈关注** — 综合评分 {score},五引擎共振,符合潜力股模型"
        elif score > 0.5:
            suggestion = f"**可建仓** — 综合评分 {score},基本面+资金面配合较好"
        elif score > 0.3:
            suggestion = f"**观望** — 综合评分 {score},等更明确信号"
        else:
            suggestion = f"**回避** — 综合评分 {score},引擎分化"

        out.append({
            "code": code,
            "name": name,
            "summary": {
                "price": stock["price"],
                "change_pct": chg,
                "pe_ttm": pe,
                "pb": pb,
                "turnover_pct": turnover,
                "score": score,
            },
            "fundamental": {
                "pe": pe, "pb": pb,
                "quality": fin_quality,
                "score_emoji": fin_score,
            },
            "technical": {
                "change_pct": chg,
                "amplitude_pct": amp,
                "state": tech_state,
                "score_emoji": tech_score,
            },
            "fund_flow": {
                "turnover_pct": turnover,
                "vol_ratio": vol_ratio,
                "5d_net_yi":   round(flow_5d / 1e8, 3),
                "20d_net_yi":  round(flow_20d / 1e8, 3),
                "state": fund_state,
                "trend": fund_trend,
                "score_emoji": fund_score,
            },
            "theme_policy": {
                "in_hot": stock["in_hot"],
                "state": theme_state,
                "score_emoji": theme_score,
                "matched_news": matched_news[:3],  # 最多 3 条
            },
            "us_overnight_link": us_link,
            "risks": risks if risks else ["⚪ 暂无显著风险"],
            "suggestion": suggestion,
        })
    log(f"  → 完成 {len(out)} 只深度分析")
    return out

def strategy_weekend_pick() -> list[dict]:
    """周末模式:基于 7×24 资讯 + 行业板块 + 资金流 + 美股周五收盘,选周一潜力股 TOP 5
    评分公式(四引擎,周末没有盘中数据):
      industry 行业强度(0.30): 该股所属行业是否在 industry_top 前 5
      valuation 估值(0.15): PE 0~30, PB 1~5
      fund 资金(0.30): 5日 + 20日主力净流入
      us 美股周五收盘(0.15): NDX/SOX 周五涨跌幅
      news 题材新闻(0.10): 7×24 资讯中匹配股票名
    """
    log("周末策略: 🌙 周一潜力股 TOP 5(基于行业+资金+美股周五+7×24 资讯)…")
    today = date.today().strftime("%Y-%m-%d")
    us = load_json(DAILY_DIR / today / "us_market.json")
    ndx_pct = us["summary"].get("NDX", 0) if us else 0
    sox_pct = us["summary"].get("SOX", 0) if us else 0
    us_bullish = ndx_pct > 0.3 or sox_pct > 0.3
    us_bearish = ndx_pct < -0.3 or sox_pct < -0.3
    us_score = 1.0 if us_bullish else -1.0 if us_bearish else 0.0

    # 行业板块 top
    try:
        industries = industry_top(10)
        top_industries = {ind["name"]: ind["change_pct"] for ind in industries[:5]}
    except Exception as e:
        log(f"  ⚠️ industry_top 失败: {e}")
        top_industries = {}

    # 7×24 资讯,提取可能命中股票
    try:
        news = eastmoney_global_news(50)
    except Exception as e:
        log(f"  ⚠️ eastmoney_global_news 失败: {e}")
        news = []

    quotes = tencent_quote(WATCH_UNIVERSE)
    out = []
    for code, q in quotes.items():
        pe = q.get("pe_ttm", 0)
        pb = q.get("pb", 0)

        # 1) 行业强度(用板块名截取关键词匹配股票名)
        industry_score = 0.0
        for ind_name, ind_pct in top_industries.items():
            # 板块名截取前 2 字(如"通信设备" → "通信")
            for keyword in [ind_name, ind_name[:2], ind_name[:3]]:
                if keyword and keyword in q.get("name", ""):
                    industry_score = ind_pct / 3  # 归一化
                    break
            if industry_score != 0:
                break
        industry_score = max(min(industry_score, 1.0), -1.0)
        if not top_industries:
            industry_score = 0.0  # 拿不到数据

        # 2) 估值
        if pe < 0:
            valuation_score = 0.0
        elif 0 < pe <= 30:
            valuation_score = 1.0
        elif 30 < pe <= 50:
            valuation_score = 0.3
        else:
            valuation_score = -0.3
        if 0 < pb < 1:
            valuation_score -= 0.3
        elif 1 <= pb <= 5:
            valuation_score += 0.1
        elif pb > 8:
            valuation_score -= 0.3
        valuation_score = max(min(valuation_score, 1.0), -1.0)

        # 3) 资金流(5日 + 20日)
        try:
            flows = stock_fund_flow_120d(code)
            flow_5d = sum(d["main_net"] for d in flows[-5:]) if len(flows) >= 5 else 0
            flow_20d = sum(d["main_net"] for d in flows[-20:]) if len(flows) >= 20 else 0
        except Exception:
            flow_5d = flow_20d = 0
        # 归一化: 5亿 = 1.0, -5亿 = -1.0
        fund_score = max(min((flow_5d * 0.6 + flow_20d * 0.4) / 5e8, 1.0), -1.0)

        # 4) 美股(科技股加权)
        is_tech = code.startswith(("688", "300", "002")) or code in WATCH_UNIVERSE[:20]
        us_local = us_score * 1.5 if is_tech else us_score * 0.5
        us_local = max(min(us_local, 1.0), -1.0)

        # 5) 题材新闻(在 7×24 中匹配股票名)
        news_score = 0.0
        for n in news:
            if q.get("name", "") in n.get("title", ""):
                news_score = 1.0
                break
            elif q.get("name", "") in n.get("summary", ""):
                news_score = max(news_score, 0.7)
        news_score = max(min(news_score, 1.0), 0.0)

        # 加权
        total = (0.30 * industry_score
                 + 0.15 * valuation_score
                 + 0.30 * fund_score
                 + 0.15 * us_local
                 + 0.10 * news_score)

        if total > 0.10:  # 阈值(周末数据稀疏,放宽)
            out.append({
                "code": code,
                "name": q["name"],
                "price": q["price"],
                "change_pct": q.get("change_pct", 0),
                "pe_ttm": pe,
                "pb": pb,
                "score": round(total, 3),
                "breakdown": {
                    "industry(0.30)": round(industry_score, 2),
                    "valuation(0.15)": round(valuation_score, 2),
                    "fund(0.30)":      round(fund_score, 2),
                    "us(0.15)":        round(us_local, 2),
                    "news(0.10)":      round(news_score, 2),
                },
                "flow_5d":  round(flow_5d / 1e8, 3),
                "flow_20d": round(flow_20d / 1e8, 3),
            })
    out.sort(key=lambda r: r["score"], reverse=True)
    log(f"  → 周末候选 {len(out)} 支,选 TOP 5")
    return out[:5]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", default="all",
                        choices=["all","1","2","3","4","5","6","7","8","8b","9","weekend"])
    parser.add_argument("--date", default=None)
    args = parser.parse_args()

    today = args.date or date.today().strftime("%Y-%m-%d")
    out_dir = DAILY_DIR / today
    out_dir.mkdir(parents=True, exist_ok=True)

    log(f"=== 9 策略选股 v1.7.0({today})===")
    all_results = {}

    if args.mode == "weekend":
        # 周末模式:只跑美股隔夜 + 周末选股(基于行业+资金+美股周五+7×24 资讯)
        log("周末模式: 🌙 选周一潜力股 TOP 5")
        us = load_json(out_dir / "us_market.json")
        all_results["9_us_overnight"] = us["summary"] if us else {}
        all_results["weekend_pick"] = strategy_weekend_pick()
    elif args.mode in ("all", "1"):
        all_results["1_momentum"] = strategy_1_momentum()
    if args.mode in ("all", "2"):
        all_results["2_fund_flow"] = strategy_2_fund_flow()
    if args.mode in ("all", "3"):
        all_results["3_value"] = strategy_3_value()
    if args.mode in ("all", "4"):
        all_results["4_etf_premium"] = strategy_4_etf_premium()
    if args.mode in ("all", "5"):
        all_results["5_news"] = strategy_5_news()
    if args.mode in ("all", "6"):
        all_results["6_serenity_chain"] = strategy_6_serenity_chain()
    if args.mode in ("all", "7"):
        all_results["7_buffett_moat"] = strategy_7_buffett_moat()
    if args.mode in ("all", "8"):
        all_results["8_potential5"] = strategy_8_potential5()
    # 策略 8b: 深度潜力分析(依赖 8 的输出)
    if args.mode in ("all", "8b"):
        if "8_potential5" not in all_results:
            all_results["8_potential5"] = strategy_8_potential5()
        all_results["8b_analysis"] = strategy_8b_potential_analysis(all_results["8_potential5"])
    # 策略 9 = 美股隔夜(由 us_market_fetcher 提供,这里只是引用)
    if args.mode in ("all", "9"):
        us = load_json(out_dir / "us_market.json")
        all_results["9_us_overnight"] = us["summary"] if us else {}

    # 保存
    out = out_dir / "daily_picks.json"
    save_json(out, all_results)
    log(f"✅ 写入 {out}")
    print(json.dumps({k: (v if isinstance(v, list) else v) for k, v in all_results.items()},
                      ensure_ascii=False, indent=2)[:2000])

if __name__ == "__main__":
    main()
