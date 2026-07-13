"""
post_report.py — x1.0 融合版报告
  1. 🚦 环境闸门（x1.0 新增，S/A/B/C/D 评级 + 仓位建议）
  2. 📈 159941 持仓跟踪（持仓联动，必须在 TOP 5 之前）
  3. 🎯 明日潜力股 TOP 5（主菜，五引擎加权 + 4 选 1 结论）
  4. 📊 每只 TOP 5 独立深度分析（财务/技术/资金/题材/美股联动/风险/建议 + 9 项结构）
  5. 🛡 排除规则摘要（x1.0 新增）
  6. 🌙 美股隔夜
  7. ⚠️ 风险点

调用方法学:
  - a-share-analysis 框架: 财务/技术/资金/政策/风险/建议 6 维
  - consulting-analysis 框架: 主题-维度-数据-洞察
  - x1.0 第 17 章: 4 选 1 结论映射
  - x1.0 第 18 章: 持仓与跨市场联动
"""
import sys, json
from pathlib import Path
from datetime import date
sys.path.insert(0, str(Path(__file__).parent))
from _common import load_json, save_json, DAILY_DIR, log, WORKSPACE, today_cst

def fmt_emoji(pct: float) -> str:
    if pct > 0.5: return "🟢"
    if pct < -0.5: return "🔴"
    return "⚪"

# ── 1. 环境闸门（x1.0 新增） ──
def section_environment_gate(meta: dict) -> str:
    grade = meta.get("environment_grade", "B")
    pos_desc = meta.get("position_desc", "严格控制仓位")
    skip = meta.get("skip_stock_pick", False)
    reasoning = meta.get("environment_reasoning", "")
    grade_emoji = {"S": "🟢", "A": "🟢", "B": "🟡", "C": "⚪", "D": "🔴"}.get(grade, "⚪")
    out = ["### 🚦 环境闸门（x1.0 第 8 章闸门脚本化）\n"]
    out.append(f"- **环境评级**: {grade_emoji} **{grade} 级**")
    out.append(f"- **仓位建议**: {pos_desc}")
    if skip:
        out.append("- **🚨 闸门跳闸**: 评级 D / 休市日，今日跳过选股，仅出持仓与美股报告")
    if reasoning:
        out.append(f"- **闸门依据**: {reasoning}")
    out.append(f"\n> 闸门由 `x1.environment_gate.evaluate()` 计算，输入：指数/情绪/连板/量能/主线 5 维度。\n")
    return "\n".join(out)

# ── 2. 明日潜力股 TOP 5 总览表 ──
def section_potential5_summary(picks: dict) -> str:
    rows = picks.get("8_potential5", [])
    x1m = picks.get("x1_meta", {})
    env_grade = x1m.get("environment_grade", "?")
    env_pos = x1m.get("position_desc", "?")
    cand_total = picks.get("8_candidates_count", "?")
    cand_passed = picks.get("8_passed_count", 0)

    if not rows:
        # 即使无候选股,也强制输出 4 选 1 结论(整体结论)
        return (
            "### 🎯 明日潜力股 TOP 5 — 评分表(位置 0.20 + 估值 0.15 + 资金 0.30 + 题材 0.20 + 美股 0.15)\n\n"
            f"**(无候选股 — 候选池 {cand_total} → 通过 {cand_passed} / 排除 {(cand_total if isinstance(cand_total,int) else '?')-cand_passed})**\n\n"
            f"- 🚦 当前闸门评级 **{env_grade} 级** → {env_pos}\n"
            f"- 🛡 排除规则把 **{cand_total}** 候选筛到 **{cand_passed}** 通过(详见下方「排除规则摘要」)\n"
            "- 🎯 **4 选 1 整体结论**: 🔴 **明确不买** — 无任何标的满足五引擎阈值(>0.25),今日放弃开仓\n"
            "- 💡 建议:耐心等板块/题材催化转暖,或下日观察是否出现低位+资金+题材共振\n\n"
        )
    out = ["### 🎯 明日潜力股 TOP 5 — 评分表(位置 0.20 + 估值 0.15 + 资金 0.30 + 题材 0.20 + 美股 0.15)\n"]
    out.append("| # | 代码 | 名称 | 现价 | 涨跌% | PE | PB | 换手% | 量比 | **总分** | **4 选 1 结论** | 位置 | 估值 | 资金 | 题材 | 美股 | 热点 |")
    out.append("|---|------|------|------|-------|-----|----|------|-----|----------|----------------|------|------|------|------|------|------|")
    for i, r in enumerate(rows, 1):
        b = r.get("breakdown", {})
        hot_mark = "🔥" if r.get("in_hot") else ""
        conc = r.get("conclusion", "")
        emoji = r.get("conclusion_emoji", "")
        conc_short = f"{emoji} {conc[:6]}"
        out.append(
            f"| {i} | {r['code']} | {r['name']} | {r['price']:.2f} | {r['change_pct']:+.2f} "
            f"| {r['pe_ttm']:.2f} | {r['pb']:.2f} | {r['turnover_pct']:.2f} | {r.get('vol_ratio',1):.2f} "
            f"| **{r['score']}** "
            f"| {conc_short} "
            f"| {b.get('position(0.20)',0)} | {b.get('valuation(0.15)',0)} | {b.get('fund(0.30)',0)} "
            f"| {b.get('theme(0.20)',0)} | {b.get('us(0.15)',0)} | {hot_mark} |"
        )
    out.append("\n> **核心思路**: 不追已涨强势股，挖**低位+资金流入+题材催化**的潜力股 + **4 选 1 结论映射**(x1.0 第 17 章)。\n")
    return "\n".join(out)

# ── 2. 每只股票独立深度分析 ──
def section_per_stock_analysis(analyses: list[dict]) -> str:
    if not analyses:
        return "### 📊 深度潜力分析\n(无数据)\n"
    out = ["### 📊 深度潜力分析(对 TOP 5 每只调用 a-share-analysis 框架)\n"]
    for a in analyses:
        s = a.get("summary", {})
        fund = a.get("fundamental", {})
        tech = a.get("technical", {})
        ff = a.get("fund_flow", {})
        tp = a.get("theme_policy", {})
        risks = a.get("risks", [])
        news_list = tp.get("matched_news", [])

        out.append(f"#### 🏷️ {a['name']}({a['code']}) — 综合评分 **{s.get('score',0)}**")
        out.append("")
        # 基本信息
        out.append("**基本信息**")
        out.append(f"- 现价 **{s.get('price',0):.2f}**  涨跌 **{s.get('change_pct',0):+.2f}%**  PE **{s.get('pe_ttm',0):.2f}**  PB **{s.get('pb',0):.2f}**  换手 **{s.get('turnover_pct',0):.2f}%**")
        out.append("")
        # 财务
        out.append(f"**财务评估** {fund.get('score_emoji','⚪')} — {fund.get('quality','?')}")
        out.append(f"- PE: {fund.get('pe',0):.2f} | PB: {fund.get('pb',0):.2f}")
        out.append("")
        # 技术
        out.append(f"**技术评估** {tech.get('score_emoji','⚪')} — {tech.get('state','?')}")
        out.append(f"- 涨跌 {tech.get('change_pct',0):+.2f}% | 振幅 {tech.get('amplitude_pct',0):.2f}%")
        out.append("")
        # 资金
        out.append(f"**资金评估** {ff.get('score_emoji','⚪')} — {ff.get('state','?')}")
        out.append(f"- 换手 {ff.get('turnover_pct',0):.2f}% | 量比 {ff.get('vol_ratio',0):.2f}")
        out.append(f"- 5日主力净流入 **{ff.get('5d_net_yi',0):+.3f} 亿** | 20日 **{ff.get('20d_net_yi',0):+.3f} 亿**")
        out.append(f"- 资金趋势: {ff.get('trend','?')}")
        out.append("")
        # 题材
        out.append(f"**题材/政策** {tp.get('score_emoji','⚪')} — {tp.get('state','?')}")
        if news_list:
            for n in news_list:
                out.append(f"  - 📰 [{n.get('time','')}] {n.get('title','')}")
                if n.get("summary"):
                    out.append(f"    > {n['summary'][:200]}")
        else:
            out.append("  - (暂无匹配的 7×24 资讯)")
        out.append("")
        # 美股隔夜联动
        out.append(f"**美股隔夜联动** — {a.get('us_overnight_link','?')}")
        out.append("")
        # 风险
        out.append("**风险点**")
        for r in risks:
            out.append(f"- {r}")
        out.append("")
        # 建议
        out.append(f"**投资建议** — {a.get('suggestion','?')}")
        out.append("")
        out.append("---")
        out.append("")
    return "\n".join(out)

# ── 3. 美股隔夜 ──
def section_us(us: dict) -> str:
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

# ── 5. 排除规则摘要（x1.0 新增） ──
def section_exclusion_summary(picks: dict) -> str:
    rows = picks.get("8_excluded", [])
    if not rows:
        return ""
    # 按 reason_code 聚合统计
    from collections import Counter
    counter = Counter()
    for r in rows:
        counter[r.get("reason_code", "?")] += 1
    out = ["### 🛡 排除规则摘要（x1.0 第 7 章）\n"]
    out.append(f"- **候选池**: {picks.get('8_candidates_count', '?')} → **通过**: {picks.get('8_passed_count', 0)} / **排除**: {len(rows)}")
    out.append("")
    out.append("**按原因聚合**\n")
    out.append("| 规则 | 数量 | 说明 |")
    out.append("|------|------|------|")
    reason_text = {
        "E_HIGH_RISE":   "① 高位加速:当日涨幅 > 6% 已透支",
        "E_LOW_VOL":     "② 缩量硬质:换手 < 1.5% 且 vol_ratio < 0.8",
        "E_HIGH_GAP":    "③ 高开过多:开盘涨幅 > 5%",
        "E_NO_THEME":    "④ 逻辑不清:题材 reason 为空",
        "E_THEME_DIFF":  "⑤ 题材发散:单一题材占比 > 50%",
        "E_NOT_FRONT":   "⑥ 非前排:不在板块 TOP 3",
        "E_SECTOR_WEAK": "⑦ 板块持续性存疑:5 日板块涨跌 < -2%",
        "E_HISTORY_DUMP":"⑨ 冲高回落历史:5 日 3 根上影线 > 5%",
        "E_MODE_MISMATCH":"⑩ 模式不匹配",
        "E_BAD_ENV":     "⑧ 环境不支持:闸门 D 级",
    }
    for code, cnt in counter.most_common():
        out.append(f"| {code} | {cnt} | {reason_text.get(code, '?')} |")
    # 列出前 10 个被排除的样本
    out.append("")
    out.append("**前 10 个被排除样本**\n")
    for r in rows[:10]:
        out.append(f"- ❌ **{r.get('code','?')} {r.get('name','?')}** → {r.get('reason_text', r.get('reason_code',''))}")
    out.append("")
    return "\n".join(out)


# ── 4. 159941 持仓跟踪 ──
def section_159941(t159: dict) -> str:
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

# ── 5. 风险点 ──
def section_risks(picks: dict, us: dict, t159: dict, analyses: list[dict]) -> str:
    risks = []
    if us:
        ndx = us["summary"].get("NDX", 0)
        sox = us["summary"].get("SOX", 0)
        if ndx < -1.5:
            risks.append(f"🔴 美股纳指隔夜大跌 {ndx:.2f}%,A 股科技股开盘承压(美股权重 0.15,影响有限但需警惕)")
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
    # 来自 8b 分析的聚合风险
    high_risk_count = 0
    for a in analyses:
        if any("🔴" in r for r in a.get("risks", [])):
            high_risk_count += 1
    if high_risk_count > 0:
        risks.append(f"🟡 TOP 5 中有 {high_risk_count} 只存在 🔴 高风险信号(详见个股分析)")
    if not risks:
        risks.append("⚪ 暂无显著风险信号")
    out = ["### ⚠️ 风险点\n"]
    for r in risks:
        out.append(f"- {r}")
    out.append("")
    return "\n".join(out)

def main():
    today = today_cst()
    out_dir = DAILY_DIR / today
    if not out_dir.exists():
        # 兼容 UTC 旧日期目录:尝试 -1d 回退
        from datetime import timedelta
        prev = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
        if (DAILY_DIR / prev).exists():
            out_dir = DAILY_DIR / prev
            today = prev
            log(f"⚠️ 今天({today_cst()})目录不存在,回退到上一交易日 {today}")
        else:
            log(f"❌ {out_dir} 不存在,先跑 run_daily.sh")
            sys.exit(1)

    log("读 JSON 数据并拼 Markdown(x1.0 融合版: 闸门 + 持仓联动 + 潜力股 TOP 5 + 深度分析)…")
    us      = load_json(out_dir / "us_market.json")
    picks   = load_json(out_dir / "daily_picks.json")
    t159    = load_json(out_dir / "159941-tracker.json")
    analyses = picks.get("8b_analysis", [])

    # 休市日处理（x1.0 第 10 章）— 用 x1_meta.environment_grade / skip_stock_pick 判定
    x1_meta = picks.get("x1_meta", {})
    env_grade = x1_meta.get("environment_grade", "")
    skip_pick = x1_meta.get("skip_stock_pick", False)
    # D 级 + skip=True + 休市文案 → 休市日
    is_trading_day = not (skip_pick and env_grade == "D" and "休市" in x1_meta.get("position_desc", ""))
    if not is_trading_day:
        x1_meta = {
            "environment_grade": "D",
            "position_desc": "休市日，无交易",
            "skip_stock_pick": True,
        }

    md = []
    md.append(f"# 📊 每日选股报告 · x1.0 — {today}\n")
    md.append("> 由 stock-trader-agent **x1.0** 融合版自动化生成(闸门 + 量化 + 深度)")
    md.append("> 融合基线: N1.0 v1.0(方法论) + v1.7.0(量化打分) + x1.0 第 17/18 章(映射+联动)")
    md.append(f"> 数据时间: {today} 09:30(A 股开盘时执行,与 cron `30 9 * * 1-5` 对齐)")
    if not is_trading_day:
        md.append("> 🚨 **休市日处理**: 复用最近一个交易日数据,所有标的标注为「仅作研究跟踪,不构成交易建议」")
    md.append("> 评分公式: 位置 0.20 + 估值 0.15 + 资金 0.30 + 题材 0.20 + 美股 0.15")
    md.append("> 4 选 1 结论映射: ≥0.70 试仓 / 0.50-0.70 等条件 / 0.25-0.50 观察 / <0.25 不买")
    md.append("> 方法学: a-share-analysis + consulting-analysis + x1.0 三框架\n")

    # ── 顺序: 闸门 → 持仓联动(必须在 TOP 5 之前)→ TOP 5 → 深度分析 → 排除规则摘要 → 美股 → 风险
    md.append("---\n")
    md.append(section_environment_gate(x1_meta))
    md.append("---\n")
    md.append(section_159941(t159))  # x1.0: 持仓联动,必须在 TOP 5 之前出现
    md.append("---\n")
    md.append(section_potential5_summary(picks))
    md.append("---\n")
    md.append(section_per_stock_analysis(analyses))
    # 排除规则摘要(只展示)
    excl_section = section_exclusion_summary(picks)
    if excl_section:
        md.append("---\n")
        md.append(excl_section)
    md.append("---\n")
    md.append(section_us(us))
    md.append(section_risks(picks, us, t159, analyses))

    md.append("\n---\n")
    md.append("> ⚠️ **风险声明**:本报告仅供参考,不构成投资建议。市场有风险,投资需谨慎。")
    md.append(f"> 报告生成时间: {today_cst()}")

    text = "\n".join(md)

    # 写出到 v1.7.0 原位置(v1.7.0 daily_picks/)
    out_md = out_dir / f"{today}.md"
    out_md.write_text(text, encoding="utf-8")
    log(f"✅ 写入 {out_md} ({out_md.stat().st_size} 字节)")

    # 同步写出 x1.0 主报告(新位置 output/)
    x1_output = WORKSPACE / "output" / f"{today}_早盘潜力股_x1.0.md"
    x1_output.parent.mkdir(parents=True, exist_ok=True)
    x1_output.write_text(text, encoding="utf-8")
    log(f"✅ 写入 x1.0 主报告 {x1_output} ({x1_output.stat().st_size} 字节)")

    # latest 软链接
    latest = DAILY_DIR / "latest.md"
    latest.write_text(text, encoding="utf-8")
    log(f"✅ 复制到 {latest}")

if __name__ == "__main__":
    main()
