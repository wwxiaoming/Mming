"""
post_report_weekend.py — x1.0 融合版周末展望报告
  0. 🚦 环境闸门（基于行业+资金+美股周五的 5 级评级）
  1. 🌙 美股周五收盘(5 指数 + 7 巨头)
  2. 🎯 周一潜力股 TOP 5(行业 0.30 + 估值 0.15 + 资金 0.30 + 美股 0.15 + 资讯 0.10)
     + 4 选 1 结论映射（x1.0 第 17 章）
  3. 📰 周末 7×24 资讯摘要(题材归因)
  4. 📈 159941 持仓跟踪
  5. ⚠️ 风险点(周一开盘)
"""
import sys, json
from pathlib import Path
from datetime import date
sys.path.insert(0, str(Path(__file__).parent))
from _common import load_json, save_json, DAILY_DIR, log, eastmoney_global_news, WORKSPACE

def fmt_emoji(pct: float) -> str:
    if pct > 0.5: return "🟢"
    if pct < -0.5: return "🔴"
    return "⚪"

# ── 1. 美股周五收盘 ──
def section_us(us: dict) -> str:
    if not us:
        return "### 🌙 美股周五收盘\n(无数据)\n"
    s = us["summary"]
    out = [f"### 🌙 美股周五收盘({us['date']})\n"]
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

# ── 2. 周一潜力股 TOP 5 ──
def section_monday_pick(picks: dict) -> str:
    rows = picks.get("weekend_pick", [])
    if not rows:
        return "### 🎯 周一潜力股 TOP 5\n(无候选股 — 周末选股未通过阈值)\n"
    out = ["### 🎯 周一潜力股 TOP 5(行业 0.30 + 估值 0.15 + 资金 0.30 + 美股 0.15 + 资讯 0.10)\n"]
    out.append("| # | 代码 | 名称 | 现价 | PE | PB | **总分** | **4 选 1 结论** | 行业 | 估值 | 资金 | 美股 | 资讯 | 5日净流入(亿) | 20日净流入(亿) |")
    out.append("|---|------|------|------|-----|----|----------|----------------|------|------|------|------|------|--------------|---------------|")
    for i, r in enumerate(rows, 1):
        b = r.get("breakdown", {})
        conc = r.get("conclusion", "")
        emoji = r.get("conclusion_emoji", "")
        conc_short = f"{emoji} {conc[:6]}"
        out.append(
            f"| {i} | {r['code']} | {r['name']} | {r['price']:.2f} | {r['pe_ttm']:.2f} | {r['pb']:.2f} "
            f"| **{r['score']}** "
            f"| {conc_short} "
            f"| {b.get('industry(0.30)',0)} | {b.get('valuation(0.15)',0)} | {b.get('fund(0.30)',0)} "
            f"| {b.get('us(0.15)',0)} | {b.get('news(0.10)',0)} "
            f"| {r.get('flow_5d',0):+.3f} | {r.get('flow_20d',0):+.3f} |"
        )
    out.append("\n> **核心思路**: 周末 A 股没开盘，改用 7×24 资讯+行业板块+5/20日资金流+美股周五收盘 4 引擎，预测周一开盘潜力股 + 4 选 1 结论映射（x1.0 第 17 章）。\n")
    return "\n".join(out)

# ── 3. 周末 7×24 资讯摘要 ──
def section_weekend_news(top_n: int = 20) -> str:
    out = ["### 📰 周末 7×24 全球资讯(影响周一开盘)\n"]
    try:
        news = eastmoney_global_news(top_n)
    except Exception as e:
        log(f"  ⚠️ eastmoney_global_news 失败: {e}")
        news = []
    if not news:
        out.append("(无数据)\n")
        return "\n".join(out)
    for i, n in enumerate(news, 1):
        out.append(f"**{i}. [{n.get('time','')}] {n.get('title','')}**")
        if n.get("summary"):
            out.append(f"  > {n['summary'][:200]}")
    out.append("")
    return "\n".join(out)

# ── 4. 159941 持仓跟踪 ──
def section_159941(t159: dict) -> str:
    if not t159:
        return "### 📈 159941 持仓跟踪\n(无数据)\n"
    h = t159["holdings"]
    q = t159["quote"]
    out = [f"### 📈 159941({t159['name']}) 持仓跟踪\n"]
    out.append("**周五收盘行情**\n")
    out.append(f"- 现价 **{q['price']:.3f}**  涨跌 **{q['change_pct']:+.2f}%**")
    out.append(f"- 持仓 **{h['shares']} 股** × 成本 **{h['cost']:.3f}**")
    out.append(f"- 累计盈亏 **{h['cum_pnl']:+.2f} 元**({h['cum_pnl_pct']:+.2f}%)\n")
    out.append(f"**美股周五联动展望**\n> {t159['us_overnight'].get('narrative','')}\n")
    return "\n".join(out)

# ── 5. 风险点 ──
def section_risks(us: dict, t159: dict) -> str:
    risks = []
    if us:
        ndx = us["summary"].get("NDX", 0)
        sox = us["summary"].get("SOX", 0)
        if ndx < -1.5:
            risks.append(f"🔴 美股纳指周五跌 {ndx:.2f}%,周一 A 股科技股开盘承压")
        elif ndx > 2:
            risks.append(f"🟢 美股纳指周五涨 {ndx:.2f}%,周一 A 股科技股有跟涨动能")
        if sox < -2:
            risks.append(f"🔴 费城半导体周五跌 {sox:.2f}%,半导体板块开盘压力")
    if t159:
        cum = t159["holdings"]["cum_pnl_pct"]
        if cum < -10:
            risks.append(f"🔴 159941 累计亏损 {cum:.1f}%,周一开盘可考虑加仓或止损")
        elif cum > 20:
            risks.append(f"🟢 159941 累计盈利 {cum:.1f}%,可分批止盈")
    if not risks:
        risks.append("⚪ 暂无显著风险信号")
    out = ["### ⚠️ 风险点(周一开盘)\n"]
    for r in risks:
        out.append(f"- {r}")
    out.append("")
    return "\n".join(out)

def main():
    today = date.today().strftime("%Y-%m-%d")
    out_dir = DAILY_DIR / today
    if not out_dir.exists():
        log(f"❌ {out_dir} 不存在,先跑 run_weekend.sh")
        sys.exit(1)

    log("读 JSON 数据并拼 Markdown(x1.0 周末展望版)…")
    us      = load_json(out_dir / "us_market.json")
    picks   = load_json(out_dir / "daily_picks.json")
    t159    = load_json(out_dir / "159941-tracker.json")

    md = []
    md.append(f"# 🌙 周末展望 · x1.0 — 周一潜力股({today})\n")
    md.append("> 由 stock-trader-agent **x1.0** 融合版周末模式自动化生成(闸门 + 4 引擎 + 4 选 1 结论)")
    md.append("> 融合基线: N1.0 v1.0 + v1.7.0 + x1.0 第 17/18 章")
    md.append(f"> 数据时间: {today} 22:00(周末晚 22:00 跑,预测周一开盘)")
    md.append("> 评分公式: 行业 0.30 + 估值 0.15 + 资金 0.30 + 美股 0.15 + 资讯 0.10")
    md.append("> 4 选 1 结论映射: ≥0.70 试仓 / 0.50-0.70 等条件 / 0.25-0.50 观察 / <0.25 不买")
    md.append("> 方法学: a-share-analysis + consulting-analysis + 7×24 资讯归因 + x1.0 三框架\n")

    md.append("---\n")
    md.append(section_us(us))
    md.append("---\n")
    md.append(section_monday_pick(picks))
    md.append("---\n")
    md.append(section_weekend_news(20))
    md.append(section_159941(t159))
    md.append(section_risks(us, t159))

    md.append("\n---\n")
    md.append("> ⚠️ **风险声明**:本报告仅供参考,不构成投资建议。市场有风险,投资需谨慎。")
    md.append(f"> 报告生成时间: {date.today().strftime('%Y-%m-%d %H:%M:%S')}")

    text = "\n".join(md)

    # v1.7.0 原位置
    out_md = out_dir / "weekend_preview.md"
    out_md.write_text(text, encoding="utf-8")
    log(f"✅ 写入 {out_md} ({out_md.stat().st_size} 字节)")

    # x1.0 新位置
    x1_output = WORKSPACE / "output" / f"{today}_周末展望_x1.0.md"
    x1_output.parent.mkdir(parents=True, exist_ok=True)
    x1_output.write_text(text, encoding="utf-8")
    log(f"✅ 写入 x1.0 周末报告 {x1_output} ({x1_output.stat().st_size} 字节)")

    latest = DAILY_DIR / "latest_weekend.md"
    latest.write_text("\n".join(md), encoding="utf-8")
    log(f"✅ 复制到 {latest}")

if __name__ == "__main__":
    main()
