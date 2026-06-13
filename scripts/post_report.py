"""
post_report.py — 把 JSON 报告拼成 Markdown(14+1 章节)
章节:
  1-5  : 5 大数据策略(强势/资金/价值/ETF/新闻)
  6-7  : Serenity 产业链 + Buffett 护城河
  8    : 最佳 5 选
  9-10 : 美股隔夜 + 159941 持仓
  11-14: consulting 4 章(行业地位/竞争格局/财务亮点/风险点)
  +1   : chart-visualization 1 张对比图(ASCII 表格版)
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

def section_1_momentum(picks: dict) -> str:
    rows = picks.get("1_momentum", [])
    if not rows:
        return "### 1️⃣ 当日强势股 TOP 5\n(无数据)\n"
    out = ["### 1️⃣ 当日强势股 TOP 5(同花顺热点 + 题材归因)\n"]
    out.append("| # | 代码 | 名称 | 涨幅% | 换手% | 成交额(亿) | 题材归因 |")
    out.append("|---|------|------|-------|-------|-----------|---------|")
    for i, r in enumerate(rows, 1):
        out.append(f"| {i} | {r['code']} | {r['name']} | {r['change_pct']:+.2f} | {r['turnover_pct']:.2f} | {r['amount_yi']:.2f} | {r['reason']} |")
    out.append("")
    return "\n".join(out)

def section_2_fund(picks: dict) -> str:
    rows = picks.get("2_fund_flow", [])
    if not rows:
        return "### 2️⃣ 主力资金净流入 TOP 5\n(无数据)\n"
    out = ["### 2️⃣ 主力资金净流入 TOP 5(东财 120 日资金流)\n"]
    out.append("| # | 代码 | 名称 | 现价 | 涨跌% | 5 日主力净流入(亿) |")
    out.append("|---|------|------|------|-------|------------------|")
    for i, r in enumerate(rows, 1):
        out.append(f"| {i} | {r['code']} | {r['name']} | {r['price']:.2f} | {r['change_pct']:+.2f} | {r['main_net_5d_yi']:+.3f} |")
    out.append("")
    return "\n".join(out)

def section_3_value(picks: dict) -> str:
    rows = picks.get("3_value", [])
    if not rows:
        return "### 3️⃣ 价值股 TOP 5\n(无数据)\n"
    out = ["### 3️⃣ 价值股 TOP 5(PE<20 & PB<2)\n"]
    out.append("| # | 代码 | 名称 | 现价 | PE(TTM) | PB | 市值(亿) |")
    out.append("|---|------|------|------|--------|----|----------|")
    for i, r in enumerate(rows, 1):
        out.append(f"| {i} | {r['code']} | {r['name']} | {r['price']:.2f} | {r['pe_ttm']:.2f} | {r['pb']:.2f} | {r['mcap_yi']:.0f} |")
    out.append("")
    return "\n".join(out)

def section_4_etf(picks: dict) -> str:
    rows = picks.get("4_etf_premium", [])
    if not rows:
        return "### 4️⃣ ETF 折溢价 TOP 5\n(无数据)\n"
    out = ["### 4️⃣ ETF 折溢价 TOP 5(按换手率活跃度)\n"]
    out.append("| # | 代码 | 名称 | 现价 | 涨跌% | 换手% |")
    out.append("|---|------|------|------|-------|-------|")
    for i, r in enumerate(rows, 1):
        out.append(f"| {i} | {r['code']} | {r['name']} | {r['price']:.3f} | {r['change_pct']:+.2f} | {r.get('turnover_pct',0):.2f} |")
    out.append("")
    return "\n".join(out)

def section_5_news(picks: dict) -> str:
    rows = picks.get("5_news", [])
    if not rows:
        return "### 5️⃣ 公告/新闻异动 TOP 5\n(无数据)\n"
    out = ["### 5️⃣ 公告/新闻异动 TOP 5(东财 7×24 资讯)\n"]
    for i, r in enumerate(rows, 1):
        out.append(f"**{i}. [{r['time']}] {r['title']}**")
        if r.get("summary"):
            out.append(f"  > {r['summary']}")
    out.append("")
    return "\n".join(out)

def section_6_serenity(picks: dict) -> str:
    rows = picks.get("6_serenity_chain", [])
    if not rows:
        return "### 6️⃣ Serenity 产业链瓶颈 TOP 5\n(无数据)\n"
    out = ["### 6️⃣ Serenity 产业链瓶颈 TOP 5(同花顺热点 reason 词频)\n"]
    out.append("| # | 主题 | 命中次数 | 产业链逻辑 |")
    out.append("|---|------|---------|-----------|")
    for i, r in enumerate(rows, 1):
        out.append(f"| {i} | **{r['theme']}** | {r['hits']} | {r['logic']} |")
    out.append("\n> 完整瓶颈分析请调 serenity-skill 与 serenity-stock-choke。\n")
    return "\n".join(out)

def section_7_buffett(picks: dict) -> str:
    rows = picks.get("7_buffett_moat", [])
    if not rows:
        return "### 7️⃣ Buffett 护城河 TOP 5\n(无数据)\n"
    out = ["### 7️⃣ Buffett 护城河 TOP 5(PE 5~25 + ROE>12 估算)\n"]
    out.append("| # | 代码 | 名称 | 现价 | PE | PB | ROE 估算% |")
    out.append("|---|------|------|------|-----|----|----------|")
    for i, r in enumerate(rows, 1):
        out.append(f"| {i} | {r['code']} | {r['name']} | {r['price']:.2f} | {r['pe_ttm']:.2f} | {r['pb']:.2f} | {r['roe_est']:.1f} |")
    out.append("\n> 真实 ROE 请以年报/同花顺 F10 为准,这里 PB/PE 仅作粗略估算。\n")
    return "\n".join(out)

def section_8_best5(picks: dict) -> str:
    rows = picks.get("8_best5", [])
    if not rows:
        return "### 8️⃣ 🔮 最佳 5 选(三维加权)\n(无数据)\n"
    out = ["### 8️⃣ 🔮 最佳 5 选(资金 0.4 + 情绪 0.3 + 政策 0.3 + 美股 0.15)\n"]
    out.append("| # | 代码 | 名称 | 现价 | 涨跌% | PE | PB | **总分** | 资金 | 情绪 | 政策 | 美股 |")
    out.append("|---|------|------|------|-------|-----|----|----------|------|------|------|------|")
    for i, r in enumerate(rows, 1):
        b = r["breakdown"]
        out.append(f"| {i} | {r['code']} | {r['name']} | {r['price']:.2f} | {r['change_pct']:+.2f} | {r['pe_ttm']:.2f} | {r['pb']:.2f} | **{r['score']}** | {b['fund(0.4)']} | {b['mood(0.3)']} | {b['policy(0.3)']} | {b['us(0.15)']} |")
    out.append("\n> 综合评分 = `0.4×资金 + 0.3×情绪 + 0.3×政策 + 0.15×美股隔夜`。详见 consulting-analysis 的财务亮点章节。\n")
    return "\n".join(out)

def section_9_us(us: dict) -> str:
    if not us:
        return "### 9️⃣ 🌙 美股隔夜表现\n(无数据)\n"
    s = us["summary"]
    out = [f"### 9️⃣ 🌙 美股隔夜表现({us['date']})\n"]
    out.append("| 指数 | 涨跌% | 状态 |")
    out.append("|------|-------|------|")
    for k, label in [("NDX", "纳斯达克100"), ("IXIC", "纳斯达克综合"),
                     ("SPX", "标普500"), ("DJI", "道琼斯"), ("SOX", "费城半导体")]:
        v = s.get(k, 0)
        out.append(f"| {label} | {v:+.2f} | {fmt_emoji(v)} |")
    out.append("")
    # 七巨头
    out.append("**七巨头表现**\n")
    out.append("| 名称 | 现价 | 涨跌% |")
    out.append("|------|------|-------|")
    for r in us.get("magnificent7", []):
        out.append(f"| {r.get('name','?')[:8]} | {r.get('price',0):.2f} | {r.get('change_pct',0):+.2f} |")
    out.append("")
    return "\n".join(out)

def section_10_159941(t159: dict) -> str:
    if not t159:
        return "### 🔟 📈 159941 纳指 ETF 跟踪\n(无数据)\n"
    h = t159["holdings"]
    q = t159["quote"]
    out = [f"### 🔟 📈 159941({t159['name']}) 持仓跟踪\n"]
    out.append("**实时行情**\n")
    out.append(f"- 现价 **{q['price']:.3f}**  涨跌 **{q['change_pct']:+.2f}%**  成交额 **{q['amount_wan']/1e4:.2f} 亿**")
    out.append(f"- 今开 {q['open']:.3f}  最高 {q['high']:.3f}  最低 {q['low']:.3f}  昨收 {q['last_close']:.3f}")
    out.append(f"- 换手 {q['turnover_pct']:.2f}%  PE {q['pe_ttm']:.2f}  PB {q['pb']:.2f}  市值 {q['mcap_yi']:.0f}亿")
    out.append("")
    out.append("**持仓盈亏**\n")
    out.append(f"- 持仓 **{h['shares']} 股** × 成本 **{h['cost']:.3f}**")
    out.append(f"- 持仓市值 **{h['market_value']:.2f} 元** (成本 {h['cost_total']:.2f})")
    out.append(f"- 当日盈亏 **{h['daily_pnl']:+.2f} 元** ({h['daily_pnl_pct']:+.2f}%)")
    out.append(f"- 累计盈亏 **{h['cum_pnl']:+.2f} 元** ({h['cum_pnl_pct']:+.2f}%)")
    out.append("")
    out.append(f"**美股隔夜联动**\n> {t159['us_overnight'].get('narrative','')}\n")
    return "\n".join(out)

def section_11_to_14_consulting(picks: dict, us: dict, t159: dict) -> str:
    """consulting-analysis 4 章节(行业地位/竞争格局/财务亮点/风险点)"""
    best5 = picks.get("8_best5", [])
    serenity_top = picks.get("6_serenity_chain", [])
    out = ["## 📊 咨询级深度分析(consulting-analysis)\n"]
    # 11 行业地位
    out.append("### 1️⃣1️⃣ 行业地位 — 候选股在所属板块中的位置\n")
    if best5:
        out.append("| 标的 | 行业地位评估(基于热度+资金) |")
        out.append("|------|---------------------------|")
        for r in best5:
            score = r["score"]
            rank = "龙头" if score > 0.6 else "二线" if score > 0.4 else "尾部"
            out.append(f"| {r['name']}({r['code']}) | 三维评分 {score} → **{rank}** |")
    out.append("")
    # 12 竞争格局
    out.append("### 1️⃣2️⃣ 竞争格局 — 产业链中竞争烈度\n")
    if serenity_top:
        out.append("| 主题 | 竞争烈度 | 投资位置 |")
        out.append("|------|---------|---------|")
        for r in serenity_top:
            hits = r['hits']
            intensity = "白热化" if hits > 5 else "中等" if hits > 2 else "蓝海"
            position = "选龙头" if hits > 5 else "选第二" if hits > 2 else "选唯一"
            out.append(f"| {r['theme']} | {intensity}({hits}只) | {position} |")
    out.append("")
    # 13 财务亮点
    out.append("### 1️⃣3️⃣ 财务亮点 — 候选股财务质量\n")
    if best5:
        out.append("| 标的 | PE | PB | 财务质量 |")
        out.append("|------|-----|----|---------|")
        for r in best5:
            pe = r["pe_ttm"]
            pb = r["pb"]
            quality = "低估" if 0 < pe < 15 and pb < 2 else "合理" if 0 < pe < 30 else "高估"
            out.append(f"| {r['name']}({r['code']}) | {pe:.2f} | {pb:.2f} | {quality} |")
    out.append("")
    # 14 风险点
    out.append("### 1️⃣4️⃣ ⚠️ 风险点 — 当日最大风险\n")
    risks = []
    if us:
        ndx = us["summary"].get("NDX", 0)
        if ndx < -1.5:
            risks.append(f"🔴 美股纳指隔夜大跌 {ndx:.2f}%,A 股开盘承压")
        if ndx > 2:
            risks.append(f"🟢 美股大涨 {ndx:.2f}%,A 股有跟涨动力(注意高开低走)")
    if t159:
        cum = t159["holdings"]["cum_pnl_pct"]
        if cum < -10:
            risks.append(f"🔴 159941 累计亏损 {cum:.1f}%,建议补仓前评估")
        elif cum > 20:
            risks.append(f"🟢 159941 累计盈利 {cum:.1f}%,建议分批止盈")
    if not risks:
        risks.append("⚪ 暂无显著风险信号")
    for r in risks:
        out.append(f"- {r}")
    out.append("")
    return "\n".join(out)

def section_chart(picks: dict) -> str:
    """+1 章节:chart-visualization 对比图(ASCII 表 + 评分条)"""
    best5 = picks.get("8_best5", [])
    if not best5:
        return "### 📊 对比图\n(无数据)\n"
    out = ["### 📊 最佳 5 选对比图(chart-visualization)\n"]
    out.append("**综合评分条形图(0~1)\n**")
    out.append("```")
    for r in best5:
        score = r["score"]
        bar_len = int(score * 30)
        bar = "█" * bar_len + "░" * (30 - bar_len)
        chg = r["change_pct"]
        out.append(f"  {r['name']:8s} {r['code']} |{bar}| {score:.3f} ({chg:+.2f}%)")
    out.append("```\n")
    out.append("**评分公式**:`0.4×资金 + 0.3×情绪 + 0.3×政策 + 0.15×美股`\n")
    return "\n".join(out)

def section_159941_kline(t159: dict) -> str:
    """+1 章节:159941 简易 K 线描述(ASCII,实际生产用 chart-visualization)"""
    if not t159:
        return "### 📈 159941 K 线(简化)\n(无数据)\n"
    q = t159["quote"]
    out = ["### 📈 159941 行情(简化版,实际生产用 chart-visualization 出 PNG)\n"]
    out.append("```")
    out.append(f"  昨收 {q['last_close']:.3f}  →  今开 {q['open']:.3f}  →  最高 {q['high']:.3f}  →  最低 {q['low']:.3f}  →  收 {q['price']:.3f}")
    out.append(f"  涨跌 {q['change_amt']:+.3f} 元  涨跌幅 {q['change_pct']:+.2f}%")
    # 简易 K 线形状
    open_p = q["open"]
    close_p = q["price"]
    high_p = q["high"]
    low_p = q["low"]
    last_p = q["last_close"]
    # 极简:画一个区间
    if high_p > low_p:
        rng = high_p - low_p
        body = "█" * max(1, int(abs(close_p - open_p) / rng * 30))
        out.append(f"  ┌─── {high_p:.3f}")
        out.append(f"  │   {body} (实体)")
        out.append(f"  ├─── {max(open_p, close_p):.3f} (上沿)")
        out.append(f"  ├─── {min(open_p, close_p):.3f} (下沿)")
        out.append(f"  └─── {low_p:.3f}")
    out.append("```\n")
    return "\n".join(out)

def main():
    today = date.today().strftime("%Y-%m-%d")
    out_dir = DAILY_DIR / today
    if not out_dir.exists():
        log(f"❌ {out_dir} 不存在,先跑 run_daily.sh")
        sys.exit(1)

    log("读 JSON 数据并拼 Markdown…")
    us      = load_json(out_dir / "us_market.json")
    picks   = load_json(out_dir / "daily_picks.json")
    t159    = load_json(out_dir / "159941-tracker.json")

    md = []
    md.append(f"# 📊 每日选股报告 — {today}\n")
    md.append("> 由 stock-trader-agent v1.6 自动化生成(9 策略 + 美股隔夜 + 159941 跟踪)")
    md.append(f"> 数据时间: {today} 07:00 (A 股开盘前 2.5 小时)")
    md.append(f"> 核心哲学: A 股买「筹码」不是买公司 — 三维信号(资金 0.4 + 情绪 0.3 + 政策 0.3) + 美股隔夜 0.15\n")

    md.append("## 📈 数据驱动 TOP 5(5 个)\n")
    md.append(section_1_momentum(picks))
    md.append(section_2_fund(picks))
    md.append(section_3_value(picks))
    md.append(section_4_etf(picks))
    md.append(section_5_news(picks))

    md.append("## 🧠 方法驱动 TOP 5(2 个)\n")
    md.append(section_6_serenity(picks))
    md.append(section_7_buffett(picks))

    md.append("## 🔮 综合 + 关联(3 个)\n")
    md.append(section_8_best5(picks))
    md.append(section_9_us(us))
    md.append(section_10_159941(t159))

    md.append(section_11_to_14_consulting(picks, us, t159))

    md.append("## 📊 可视化(2 张)\n")
    md.append(section_chart(picks))
    md.append(section_159941_kline(t159))

    md.append("\n---\n")
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
