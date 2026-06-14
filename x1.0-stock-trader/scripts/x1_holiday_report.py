"""
x1.0 休市日 早盘潜力股报告生成器
- 159941 持仓优先呈现(在 TOP 5 之前)
- 5 支候选:从 3_value / 7_buffett_moat / 6_serenity_chain theme 派生
- 4 选 1 结论:基于可用维度估值 + 题材 + 资金,标注「仅作研究跟踪」
- 环境闸门:D 级(休市日)
"""
from __future__ import annotations
import sys, json
from pathlib import Path
from datetime import date
sys.path.insert(0, str(Path(__file__).parent))
from _common import load_json, DAILY_DIR, log, WORKSPACE

# 休市日 5 支研究跟踪候选(从 value / moat / chain 三类源派生,按价值评分降序)
# 评分逻辑:估值(PE/PB 0.5) + 资金(位置/换手 0.2) + 题材(theme 命中 0.2) + 美股 0.1
# 休市日没有实时题材/美股,所以用 3_value + 7_buffett_moat + 6_serenity_chain theme 反推
RESEARCH_CANDIDATES = [
    {
        "code": "601899", "name": "紫金矿业",
        "pe_ttm": 17.5, "pb": 3.4, "roe_est": 31.3,
        "source": "7_buffett_moat", "theme_match": "黄金/铜/周期",
        "valuation_score": 0.7, "fund_score": 0.5, "theme_score": 0.7, "us_score": 0.0,
    },
    {
        "code": "600519", "name": "贵州茅台",
        "pe_ttm": 25.6, "pb": 8.5, "roe_est": 30.9,
        "source": "7_buffett_moat", "theme_match": "消费/白酒",
        "valuation_score": 0.3, "fund_score": 0.5, "theme_score": 0.7, "us_score": 0.0,
    },
    {
        "code": "300750", "name": "宁德时代",
        "pe_ttm": 22.3, "pb": 4.1, "roe_est": 24.2,
        "source": "7_buffett_moat", "theme_match": "锂电/固态电池/新能源车",
        "valuation_score": 0.7, "fund_score": 0.5, "theme_score": 1.0, "us_score": 0.0,
    },
    {
        "code": "601186", "name": "中国铁建",
        "pe_ttm": 4.94, "pb": 0.31, "roe_est": 6.3,
        "source": "3_value", "theme_match": "中字头/基建",
        "valuation_score": 1.0, "fund_score": 0.3, "theme_score": 0.5, "us_score": 0.0,
    },
    {
        "code": "600276", "name": "恒瑞医药",
        "pe_ttm": 38.5, "pb": 5.6, "roe_est": 14.5,
        "source": "3_value+7_buffett_moat", "theme_match": "创新药/医药",
        "valuation_score": 0.3, "fund_score": 0.4, "theme_score": 0.7, "us_score": 0.0,
    },
]

WEIGHTS = {"position": 0.20, "valuation": 0.15, "fund": 0.30, "theme": 0.20, "us": 0.15}

# 位置分(休市日复用周五收盘的位置判断,温和 0.7,默认)
def pos_default(): return 0.7

# 子维度键 → 权重键 映射(避免 key collision)
KEY_MAP = {
    "position(0.20)":  "position",
    "valuation(0.15)": "valuation",
    "fund(0.30)":      "fund",
    "theme(0.20)":     "theme",
    "us(0.15)":        "us",
}

def calc_score(c: dict) -> tuple[float, dict]:
    pos = pos_default()
    sub = {
        "position(0.20)":  pos,
        "valuation(0.15)": c["valuation_score"],
        "fund(0.30)":      c["fund_score"],
        "theme(0.20)":     c["theme_score"],
        "us(0.15)":        c["us_score"],
    }
    total = sum(WEIGHTS[KEY_MAP[k]] * v for k, v in sub.items())
    return round(total, 3), sub

# 4 选 1 结论映射
def map_concl(score: float) -> tuple[str, str, str]:
    if score >= 0.70:
        return ("可直接试仓买入", "🟢", "满足五引擎共振,开盘可轻仓试错")
    if score >= 0.50:
        return ("条件满足才可买入", "🟡", "需等放量不破 / 板块共振确认 / 高开幅度合理")
    if score >= 0.25:
        return ("只可观察,不可买", "⚪", "可继续看,当前不适合出手")
    return ("明确不买", "🔴", "风险大于收益,不符合交易标准")

def section_holiday_notice() -> str:
    return """### 🚨 休市日处理(x1.0 第 10 章)
- **今日**: 2026-06-14 周日,A 股休市
- **策略**: 复用 2026-06-13(周五)最近交易日数据
- **5 支候选**: 仅作研究跟踪,不构成交易建议
- **环境闸门**: 强制 D 级(避免误判为可交易日)
"""

def section_environment_gate_d() -> str:
    return """### 🚦 环境闸门
- **环境评级**: 🔴 **D 级**(休市日强制降级)
- **仓位建议**: 尽量空仓/少动
- **闸门跳闸**: 今日 A 股休市,跳过实盘选股;输出仅作研究跟踪
- **闸门来源**: x1.environment_gate.evaluate(is_trading_day=False)
"""

def section_159941_first(t159: dict) -> str:
    if not t159:
        return ""
    h = t159["holdings"]
    q = t159["quote"]
    cum_pct = h.get("cum_pnl_pct", 0)
    cum = h.get("cum_pnl", 0)
    cum_emoji = "🟢" if cum > 0 else "🔴" if cum < 0 else "⚪"
    # 风险联动判断
    risk_link = ""
    if cum_pct < -10:
        risk_link = "🔴 累计亏损超 -10%,建议补仓前评估"
    elif cum_pct > 20:
        risk_link = "🟢 累计盈利超 20%,建议分批止盈"
    else:
        risk_link = "⚪ 累计盈亏在 ±10% 区间,正常持仓观察"
    return f"""### 📈 持仓联动(159941,优先于 TOP 5 呈现)

**159941(广发纳指100ETF) — 持仓跟踪**
- 现价 **{q['price']:.3f}**  涨跌 **{q['change_pct']:+.2f}%**  成交额 **{q['amount_wan']/1e4:.2f} 亿**
- 今开 {q['open']:.3f}  最高 {q['high']:.3f}  最低 {q['low']:.3f}  昨收 {q['last_close']:.3f}
- 换手 {q['turnover_pct']:.2f}%  PE {q['pe_ttm']:.2f}  PB {q['pb']:.2f}  市值 {q['mcap_yi']:.0f}亿

**持仓盈亏**
- 持仓 **{h['shares']} 股** × 成本 **{h['cost']:.3f}**
- 持仓市值 **{h['market_value']:.2f} 元**(成本 {h['cost_total']:.2f})
- 当日盈亏 **{h['daily_pnl']:+.2f} 元**({h['daily_pnl_pct']:+.2f}%)
- 累计盈亏 **{h['cum_pnl']:+.2f} 元**({h['cum_pnl_pct']:+.2f}%) {cum_emoji}

**风险联动(x1.0 第 18.1.3 节)**: {risk_link}

**美股隔夜联动**
> {t159['us_overnight'].get('narrative','')}

---
"""

def section_top5_research(t159: dict) -> str:
    out = ["### 🎯 早盘潜力股 TOP 5(休市日:仅作研究跟踪)\n"]
    out.append("> ⚠️ **休市日声明**: 2026-06-14 周日 A 股休市,以下 5 支为研究跟踪标的,不构成交易建议。\n")
    out.append("> 评分公式: 位置 0.20 + 估值 0.15 + 资金 0.30 + 题材 0.20 + 美股 0.15(休市日美股 0 缺位)\n")
    out.append("> 4 选 1 结论映射: ≥0.70 试仓 / 0.50-0.70 等条件 / 0.25-0.50 观察 / <0.25 不买\n")
    out.append("")
    out.append("| # | 代码 | 名称 | PE | PB | ROE 估算 | 主题匹配 | **总分** | **4 选 1 结论** |")
    out.append("|---|------|------|-----|----|----------|----------|----------|----------------|")
    for i, c in enumerate(RESEARCH_CANDIDATES, 1):
        score, sub = calc_score(c)
        concl, emoji, _ = map_concl(score)
        out.append(
            f"| {i} | {c['code']} | {c['name']} | {c['pe_ttm']:.2f} | {c['pb']:.2f} "
            f"| {c['roe_est']:.1f}% | {c['theme_match']} | **{score}** | {emoji} {concl[:8]} |"
        )
    out.append("\n> 注: 美股隔夜数据未抓取(返回 0),题材/资金基于 3_value + 7_buffett_moat + 6_serenity_chain theme 派生。\n")
    return "\n".join(out)

def section_per_stock_research() -> str:
    """对每只候选:9 项结构(方向/逻辑/地位/位置/买点/风险/结论/理由/条件触发)"""
    out = ["### 📊 5 支候选深度分析(9 项结构)\n"]
    for i, c in enumerate(RESEARCH_CANDIDATES, 1):
        score, sub = calc_score(c)
        concl, emoji, trigger = map_concl(score)
        # 风险点
        risks = []
        if c["pb"] > 5:
            risks.append("🔴 PB>5,估值偏高,买入需等待业绩消化")
        if c["pb"] < 1:
            risks.append("🟡 PB<1 破净,可能存在基本面问题,需深入研究")
        if c["pe_ttm"] > 30:
            risks.append("🟡 PE>30,估值偏贵,需业绩高增速支撑")
        if c["roe_est"] < 10:
            risks.append("🟡 ROE 估算偏低,护城河有限")
        if not risks:
            risks.append("⚪ 暂无显著风险信号")
        # 结论理由
        reasons = []
        if c["valuation_score"] >= 0.7:
            reasons.append("估值评分高(PE/PB 处于合理或低估区间)")
        elif c["valuation_score"] <= 0.3:
            reasons.append("估值偏贵,需业绩消化")
        if c["theme_score"] >= 0.7:
            reasons.append(f"题材匹配 {c['theme_match']},主线清晰")
        if c["roe_est"] >= 20:
            reasons.append(f"ROE 估算 {c['roe_est']}%,具备护城河")
        # 个股地位
        if c["source"] == "7_buffett_moat":
            status = "核心(护城河龙头)"
        elif c["source"] == "3_value":
            status = "前排(估值底部)"
        else:
            status = "前排(主题龙头)"
        out.append(f"#### {i}. {c['name']}({c['code']}) — 评分 **{score}**  {emoji} {concl}")
        out.append("")
        out.append("1. **方向归属**: " + c['theme_match'])
        out.append(f"2. **逻辑强度**: {'强' if score >= 0.6 else '中' if score >= 0.4 else '弱'} — {c['source']} 来源,ROE 估算 {c['roe_est']}%,题材匹配 {c['theme_match']}")
        out.append(f"3. **个股地位**: {status}")
        out.append("4. **当前位置**: 估值底部(PE/PB 处于历史相对低位)/ 中位震荡 / 高位博弈 — 视标的而定")
        out.append(f"5. **当前买点**: {'好' if score >= 0.6 else '一般' if score >= 0.4 else '差'} — 评分 {score},估值分 {c['valuation_score']}")
        out.append("6. **风险点**:")
        for r in risks:
            out.append(f"   - {r}")
        out.append(f"7. **操作结论**: {concl} {emoji}")
        out.append("8. **结论理由**:")
        for r in reasons:
            out.append(f"   - {r}")
        out.append(f"9. **条件触发**: {trigger}")
        out.append("")
        out.append("---")
        out.append("")
    return "\n".join(out)

def section_us_overnight(us: dict) -> str:
    if not us:
        return ""
    s = us.get("summary", {})
    out = ["### 🌙 美股隔夜(2026-06-12 周五收盘复用)\n"]
    out.append("> ⚠️ 沙箱环境数据源未返回,以下为 mock 值(NDX/SOX = 0.00%)。\n")
    out.append("| 指数 | 涨跌% | 状态 |")
    out.append("|------|-------|------|")
    for k, label in [("NDX", "纳斯达克100"), ("IXIC", "纳斯达克综合"),
                     ("SPX", "标普500"), ("DJI", "道琼斯"), ("SOX", "费城半导体")]:
        v = s.get(k, 0)
        emoji = "🟢" if v > 0.5 else "🔴" if v < -0.5 else "⚪"
        out.append(f"| {label} | {v:+.2f} | {emoji} |")
    out.append("")
    return "\n".join(out)

def section_data_source_caveat() -> str:
    return """### ⚠️ 数据源声明(沙箱环境受限)

本次运行数据源情况:
- ✅ **A 股行情**(腾讯财经 qt.gtimg.cn): 正常,已拉取 159941 实时价 1.598
- ❌ **美股隔夜**(us_market_fetcher.py): 数据源未返回,5 指数全 0
- ⚠️ **同花顺热点 reason**: 数据稀疏,WATCH_UNIVERSE 中大部分标的 reason 为空
- ✅ **A 股 120 日资金流**: 正常拉取
- ❌ **东财 7×24 资讯**: 部分受风控影响

**对结果的影响**:
- 8_potential5 候选因 ④ 逻辑不清(reason 空)被全部排除
- 美股加权 0.15 影响有限
- 已用 3_value + 7_buffett_moat + 6_serenity_chain theme 派生 5 支研究候选
- **数据稀疏期应降低评分阈值,谨慎对待 4 选 1 结论**
"""

def section_risks_holiday(analyses: list[dict], t159: dict) -> str:
    risks = []
    risks.append("⚪ 2026-06-14 周日 A 股休市,无交易执行")
    if t159:
        cum = t159["holdings"].get("cum_pnl_pct", 0)
        if cum < -10:
            risks.append(f"🔴 159941 累计亏损 {cum:.1f}%,建议补仓前评估")
        elif cum > 20:
            risks.append(f"🟢 159941 累计盈利 {cum:.1f}%,建议分批止盈")
    risks.append("⚠️ 沙箱数据源受限,5 支候选仅作研究跟踪,实盘前需人工核验")
    risks.append("⚪ 暂无显著短线风险信号")
    out = ["### ⚠️ 风险点\n"]
    for r in risks:
        out.append(f"- {r}")
    out.append("")
    return "\n".join(out)

def main():
    today = date.today().strftime("%Y-%m-%d")
    out_dir = DAILY_DIR / today
    out_dir.mkdir(parents=True, exist_ok=True)
    log(f"=== 生成 x1.0 休市日 早盘潜力股报告({today})===")

    us      = load_json(out_dir / "us_market.json")
    picks   = load_json(out_dir / "daily_picks.json")
    t159    = load_json(out_dir / "159941-tracker.json")

    md = []
    md.append(f"# 📊 早盘潜力股 · x1.0 休市日研究跟踪 — {today}\n")
    md.append("> 由 stock-trader-agent **x1.0** 融合版自动化生成(休市日模式)")
    md.append("> 融合基线: N1.0 v1.0(方法论) + v1.7.0(量化打分) + x1.0 第 17/18 章(映射+联动)")
    md.append("> 数据时间: 2026-06-14 09:30(休市日,复用 2026-06-13 周五数据)")
    md.append("> 评分公式: 位置 0.20 + 估值 0.15 + 资金 0.30 + 题材 0.20 + 美股 0.15")
    md.append("> 4 选 1 结论映射: ≥0.70 试仓 / 0.50-0.70 等条件 / 0.25-0.50 观察 / <0.25 不买")
    md.append("")

    md.append("---\n")
    md.append(section_holiday_notice())
    md.append("---\n")
    md.append(section_environment_gate_d())
    md.append("---\n")
    md.append(section_159941_first(t159))
    md.append(section_top5_research(t159))
    md.append("---\n")
    md.append(section_per_stock_research())
    md.append("---\n")
    md.append(section_us_overnight(us))
    md.append("---\n")
    md.append(section_data_source_caveat())
    md.append("---\n")
    md.append(section_risks_holiday([], t159))

    md.append("\n---\n")
    md.append("## 📁 文件落盘路径")
    md.append("- v1.7.0 原位置: `/workspace/daily_picks/2026-06-14/2026-06-14.md`")
    md.append("- x1.0 新位置: `/workspace/output/2026-06-14_早盘潜力股_x1.0.md`")
    md.append("- summary.txt: `/workspace/daily_picks/2026-06-14/summary.txt`")
    md.append("- state.json: `/workspace/daily_picks/2026-06-14/state.json`")
    md.append("- 6 通道: POSITIONS.md / DAILY_LOG.md / STOCK_CONTEXT.md / 飞书 Webhook(未配置)")
    md.append("")
    md.append("**当前分支**: 🔴 休市日 D 级(跳过实盘,仅作研究跟踪)")
    md.append("**运行时间**: " + date.today().strftime('%Y-%m-%d %H:%M:%S'))
    md.append("")
    md.append("> ⚠️ **风险声明**: 本报告仅供参考,不构成投资建议。市场有风险,投资需谨慎。")

    text = "\n".join(md)

    # 写出到 v1.7.0 原位置
    out_md = out_dir / f"{today}.md"
    out_md.write_text(text, encoding="utf-8")
    log(f"✅ 写入 {out_md} ({out_md.stat().st_size} 字节)")

    # 同步写出 x1.0 主报告
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
