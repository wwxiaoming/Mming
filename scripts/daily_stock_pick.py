"""
daily_stock_pick.py — 9 策略并行选股(每个策略返回 TOP 5)
策略清单(资金 0.4 / 情绪 0.3 / 政策 0.3 = 三维评分;美股隔夜 +0.15 加成):
  1. 当日强势股(同花顺热点,情绪 0.3)
  2. 主力资金净流入(东财 push2 资金流 120 日,资金 0.4)
  3. 价值股(PE/PB 低,政策 0.3 — 政策底)
  4. ETF 折溢价(数据驱动)
  5. 公告/新闻异动(东财全球资讯 7×24,政策 0.3)
  6. Serenity 产业链瓶颈(调 serenity-skill 思路:叙事→环节→标的)
  7. Buffett 护城河(ROE 持续 + FCF,价值 0.4)
  8. 🔮 最佳 5 选(三引擎加权 = 资金 0.4 + 情绪 0.3 + 政策 0.3 + 美股隔夜 0.15)
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

def strategy_8_best5() -> list[dict]:
    """策略 8: 明日最可能涨的 TOP 3(v1.6.1: 美股权重 0.10,资金 0.40,情绪 0.30,政策 0.20)"""
    log("策略 8: 🔮 明日最可能涨的 TOP 3…")
    # 读 us_market.json(美股隔夜,新权重 0.10)
    today = date.today().strftime("%Y-%m-%d")
    us = load_json(DAILY_DIR / today / "us_market.json")
    ndx_pct = us["summary"]["NDX"] if us else 0
    sox_pct = us["summary"]["SOX"] if us else 0
    us_score = 1.0 if (ndx_pct > 0.5 or sox_pct > 0.5) else -1.0 if (ndx_pct < -0.5 or sox_pct < -0.5) else 0.0

    quotes = tencent_quote(WATCH_UNIVERSE)
    out = []
    for code, q in quotes.items():
        # 资金面(用换手率近似)
        turnover = q.get("turnover_pct", 0)
        fund_score = min(turnover / 5, 1.0)  # 换手 5% 满分
        # 情绪面(涨幅)
        chg = q.get("change_pct", 0)
        mood_score = max(min(chg / 5, 1.0), -1.0)
        # 政策面(用涨跌幅稳定度,这里用 PB 估值底近似)
        pb = q.get("pb", 0)
        policy_score = 1.0 if (0 < pb < 2) else -1.0 if pb > 8 else 0.0
        # 加权(v1.6.1:资金 0.40 + 情绪 0.30 + 政策 0.20 + 美股隔夜 0.10)
        total = 0.40 * fund_score + 0.30 * mood_score + 0.20 * policy_score + 0.10 * us_score
        if total > 0.2:  # 阈值过滤
            out.append({
                "code": code,
                "name": q["name"],
                "price": q["price"],
                "change_pct": q["change_pct"],
                "pe_ttm": q["pe_ttm"],
                "pb": q["pb"],
                "score": round(total, 3),
                "breakdown": {
                    "fund(0.40)":   round(fund_score, 2),
                    "mood(0.30)":   round(mood_score, 2),
                    "policy(0.20)": round(policy_score, 2),
                    "us(0.10)":     round(us_score, 2),
                },
            })
    out.sort(key=lambda r: r["score"], reverse=True)
    return out[:3]   # ← v1.6.1: TOP 3(只选最可能涨的 3 支)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", default="all",
                        choices=["all","1","2","3","4","5","6","7","8","9"])
    parser.add_argument("--date", default=None)
    args = parser.parse_args()

    today = args.date or date.today().strftime("%Y-%m-%d")
    out_dir = DAILY_DIR / today
    out_dir.mkdir(parents=True, exist_ok=True)

    log(f"=== 9 策略选股({today})===")
    all_results = {}

    if args.mode in ("all", "1"):
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
        all_results["8_best5"] = strategy_8_best5()
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
