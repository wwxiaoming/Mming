"""
post_report.py — v1.6.1 极简报告(只输出明日预测 TOP 3 + 关联信息)
章节:
  1. 🎯 明日预测 TOP 3(主菜:策略 8 加权评分结果)
  2. 🌙 美股隔夜(5 指数 + 7 巨头)
  3. 📈 159941 持仓跟踪(实时行情 + 盈亏 + 美股隔夜联动)
  4. ⚠️ 风险点(美股 + 累计盈亏 + 当日异动)

v1.6 时代的 14+1 章节排名已全部去掉,只留用户最关心的"明日最可能涨的 3 支股票"。
"""
import sys, json
from pathlib import Path
from datetime import date
sys.path.insert(0, str(Path(__file__).parent))
from _common import load_json, save_json, DAILY_DIR, log

def fmt_emoji(pct: float) -> str:
    if pct > 0.5: return "🟢"
    if pct < -0.5: return "🔴"
    return "⚪"

def section_top3(picks: dict) -> str:
    """🎯 明日预测 TOP 3 — 主菜"""
    rows = picks.get("8_best5", [])
    if not rows:
        return "### 🎯 明日预测 TOP 3\n(无候选股 — 阈值过滤后无符合标的)\n"
    out = ["### 🎯 明日预测 TOP 3(资金 0.40 + 情绪 0.30 + 政策 0.20 + 美股 0.10)\n"]
    out.append("| # | 代码 | 名称 | 现价 | 涨跌% | PE | PB | **总分** | 资金 | 情绪 | 政策 | 美股 |")
    out.append("|---|------|------|------|-------|-----|----|----------|------|------|------|------|")
    for i, r in enumerate(rows, 1):
        b = r["breakdown"]
        # 兼容旧字段名
        fund   = b.get("fund(0.40)",   b.get("fund(0.4)",   0))
        mood   = b.get("mood(0.30)",   b.get("mood(0.3)",   0))
        policy = b.get("policy(0.20)", b.get("policy(0.3)", 0))
        us     = b.get("us(0.10)",     b.get("us(0.15)",    0))
        out.append(f"| {i} | {r['code']} | {r['name']} | {r['price']:.2f} | {r['change_pct']:+.2f} | {r['pe_ttm']:.2f} | {r['pb']:.2f} | **{r['score']}** | {fund} | {mood} | {policy} | {us} |")
    out.append("\n> **评分公式** = `0.40×资金换手 + 0.30×情绪涨幅 + 0.20×政策估值底 + 0.10×美股隔夜`\n")
    return "\n".join(out)

def section_us(us: dict) -> str:
    """🌙 美股隔夜"""
    if not us:
        return "### 🌙 美股隔夜\n(无数据)\n"
    s = us["summary"]
    out = [f"### 🌙 美股隔夜({us['date']})\n"]
    out.append("**5 大指数**\n")
    out.append("| 指数 | 涨跌% | 状态 |")
    out.append("|------|-------|------|")
    for k, label in [("NDX", "纳斯达克100"), ("IXIC", "纳斯达克综合"),
                     ("SPX", "标普500"), ("DJI", "道琼斯"), ("SOX", "费城半导体")]:
        v = s.get(k, 0)
        out.append(f"| {label} | {v:+.2f} | {fmt_emoji(v)} |")
    out.append("")
    mag7 = us.get("magnificent7", [])
    if mag7:
        out.append("**七巨头**\n")
        out.append("| 名称 | 现价 | 涨跌% |")
        out.append("|------|------|-------|")
        for r in mag7:
            out.append(f"| {r.get('name','?')[:8]} | {r.get('price',0):.2f} | {r.get('change_pct',0):+.2f} |")
        out.append("")
    return "\n".join(out)

def section_159941(t159: dict) -> str:
    """📈 159941 持仓跟踪"""
    if not t159:
        return "### 📈 159941 持仓跟踪\n(无数据)\n"
    h = t159["holdings"]
    q = t159["quote"]
    out = [f"### 📈 159941({t159['name']}) 持仓跟踪\n"]
    out.append("**实时行情**\n")
    out.append(f"- 现价 **{q['price']:.3f}**  涨跌 **{q['change_pct']:+.2f}%**  成交额 **{q['amount_wan']/1e4:.2f} 亿**")
    out.append(f"- 今开 {q['open']:.3f}  最高 {q['high']:.3f}  最低 {q['low']:.3f}  昨收 {q['last_close']:.3f}")
    out.append(f"- 换手 {q['turnover_pct']:.2f}%  PE {q['pe_ttm']:.2f}  PB {q['pb']:.2f}  市值 {q['mcap_yi']:.0f}亿")
    out.append("")
    out.append("**持仓盈亏**\n")
    out.append(f"- 持仓 **{h['shares']} 股** × 成本 **{h['cost']:.3f}**")
    out.append(f"- 持仓市值 **{h['market_value']:.2f} 元**(成本 {h['cost_total']:.2f})")
    out.append(f"- 当日盈亏 **{h['daily_pnl']:+.2f} 元**({h['daily_pnl_pct']:+.2f}%)")
    out.append(f"- 累计盈亏 **{h['cum_pnl']:+.2f} 元**({h['cum_pnl_pct']:+.2f}%)\n")
    out.append(f"**美股隔夜联动**\n> {t159['us_overnight'].get('narrative','')}\n")
    return "\n".join(out)

def section_risks(picks: dict, us: dict, t159: dict) -> str:
    """⚠️ 风险点"""
    risks = []
    if us:
        ndx = us["summary"].get("NDX", 0)
        sox = us["summary"].get("SOX", 0)
        if ndx < -1.5:
            risks.append(f"🔴 美股纳指隔夜大跌 {ndx:.2f}%,A 股开盘承压(美股权重 0.10,影响有限但需警惕)")
        elif ndx > 2:
            risks.append(f"🟢 美股大涨 {ndx:.2f}%,A 股有跟涨动力(注意高开低走)")
        if sox < -2:
            risks.append(f"🔴 费城半导体隔夜大跌 {sox:.2f}%,科技股承压")
    if t159:
        cum = t159["holdings"]["cum_pnl_pct"]
        if cum < -10:
            risks.append(f"🔴 159941 累计亏损 {cum:.1f}%,建议补仓前评估")
        elif cum > 20:
            risks.append(f"🟢 159941 累计盈利 {cum:.1f}%,建议分批止盈")
    if not risks:
        risks.append("⚪ 暂无显著风险信号")
    out = ["### ⚠️ 风险点\n"]
    for r in risks:
        out.append(f"- {r}")
    out.append("")
    return "\n".join(out)

def main():
    today = date.today().strftime("%Y-%m-%d")
    out_dir = DAILY_DIR / today
    if not out_dir.exists():
        log(f"❌ {out_dir} 不存在,先跑 run_daily.sh")
        sys.exit(1)

    log("读 JSON 数据并拼 Markdown(极简版 4 章节)…")
    us      = load_json(out_dir / "us_market.json")
    picks   = load_json(out_dir / "daily_picks.json")
    t159    = load_json(out_dir / "159941-tracker.json")

    md = []
    md.append(f"# 📊 每日选股报告 — {today}\n")
    md.append("> 由 stock-trader-agent v1.6.1 自动化生成(资金 0.40 + 情绪 0.30 + 政策 0.20 + 美股 0.10)")
    md.append(f"> 数据时间: {today} 07:00(A 股开盘前 2.5 小时)")
    md.append("> 核心: **明日最可能涨的 3 支股票** + 美股隔夜 + 159941 持仓\n")

    md.append("---\n")
    md.append(section_top3(picks))
    md.append("---\n")
    md.append(section_us(us))
    md.append(section_159941(t159))
    md.append(section_risks(picks, us, t159))

    md.append("---\n")
    md.append("> ⚠️ **风险声明**:本报告仅供参考,不构成投资建议。市场有风险,投资需谨慎。")
    md.append(f"> 报告生成时间: {date.today().strftime('%Y-%m-%d %H:%M:%S')}")

    out_md = out_dir / f"{today}.md"
    out_md.write_text("\n".join(md), encoding="utf-8")
    log(f"✅ 写入 {out_md} ({out_md.stat().st_size} 字节)")

    # 同时复制一份最新
    latest = DAILY_DIR / "latest.md"
    latest.write_text("\n".join(md), encoding="utf-8")
    log(f"✅ 复制到 {latest}")

if __name__ == "__main__":
    main()
