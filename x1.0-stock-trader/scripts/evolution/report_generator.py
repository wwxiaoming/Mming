"""
report_generator.py — 自进化报告生成

输出 Markdown 格式的多维度分析报告,7 大章节:
  1. 执行摘要(命中率/平均收益/超额收益/最佳/最差)
  2. 策略有效性分析(9 策略评级表)
  3. 最佳持有周期(T+1~T+20)
  4. 评分体系有效性(高分是否优于低分)
  5. 错误分析(TOP 10 亏损标的)
  6. 权重优化建议(新旧对比)
  7. 行动建议(自动生成的改进措施)

用法:
  python3 scripts/evolution/report_generator.py
"""
from __future__ import annotations
import sys, json
from pathlib import Path
from datetime import datetime

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))
from _common import log, DAILY_DIR

EVOLUTION_DIR = DAILY_DIR / "_evolution"
TRACK_DIR = DAILY_DIR / "_tracking"


# ── 加载最新产物 ──
def _load_latest(dir_path: Path, prefix: str) -> dict | list:
    """加载 _evolution 或 _tracking 目录下最新文件"""
    files = sorted(dir_path.glob(f"{prefix}_*.json"), reverse=True)
    if not files:
        return {}
    try:
        return json.loads(files[0].read_text(encoding="utf-8"))
    except Exception as e:
        log(f"  ⚠ 加载 {prefix} 失败: {e}")
        return {}


def load_analysis() -> dict:
    return _load_latest(EVOLUTION_DIR, "analysis") or {}


def load_evaluation() -> dict:
    return _load_latest(EVOLUTION_DIR, "evaluation") or {}


def load_weights() -> dict:
    return _load_latest(EVOLUTION_DIR, "weights") or {}


def load_tracking() -> list:
    return _load_latest(TRACK_DIR, "tracking") or []


# ── 格式化辅助 ──
def _fmt_pct(v, sign: bool = True) -> str:
    if v is None:
        return "—"
    try:
        return f"{v:+.2f}%" if sign else f"{v:.2f}%"
    except (TypeError, ValueError):
        return "—"


def _fmt_num(v, digits: int = 2) -> str:
    if v is None:
        return "—"
    try:
        return f"{float(v):.{digits}f}"
    except (TypeError, ValueError):
        return "—"


# ── 7 大章节构建 ──
def section_header(title: str, emoji: str = "") -> str:
    return f"\n## {emoji} {title}\n" if emoji else f"\n## {title}\n"


def build_executive_summary(tracking: list, analysis: dict) -> str:
    """章节 1: 执行摘要"""
    md = [section_header("一、执行摘要", "📊")]

    if not tracking:
        md.append("> ⚠ 无追踪数据,无法生成摘要。\n")
        return "".join(md)

    total = len(tracking)
    # T+5 收益率(主指标)
    t5 = [r["returns"]["T+5"] for r in tracking
          if "returns" in r and "T+5" in r["returns"]]
    t1 = [r["returns"]["T+1"] for r in tracking
          if "returns" in r and "T+1" in r["returns"]]
    excess = [r["excess_t5"] for r in tracking if r.get("excess_t5") is not None]

    md.append(f"- **分析样本**: {total} 条选股记录\n")

    if t5:
        wins = [r for r in t5 if r > 0]
        losses = [r for r in t5 if r < 0]
        avg_win = sum(wins) / len(wins) if wins else 0
        avg_loss = abs(sum(losses) / len(losses)) if losses else 0
        pl_ratio = avg_win / avg_loss if avg_loss > 0 else float("inf")
        md.append(f"- **T+5 命中率**: {len(wins)/len(t5)*100:.1f}%({len(wins)}/{len(t5)})\n")
        md.append(f"- **T+5 平均收益**: {sum(t5)/len(t5):+.2f}%\n")
        md.append(f"- **T+5 平均超额收益(vs 沪深300)**: "
                  f"{sum(excess)/len(excess):+.2f}%\n" if excess else "")
        md.append(f"- **T+5 最佳表现**: {max(t5):+.2f}%\n")
        md.append(f"- **T+5 最差表现**: {min(t5):+.2f}%\n")
        md.append(f"- **盈亏比**: {pl_ratio:.2f}(均盈 {avg_win:+.2f}% / 均亏 {avg_loss:+.2f}%)\n")

    if t1:
        wins_t1 = sum(1 for r in t1 if r > 0)
        md.append(f"- **T+1 次日命中率**: {wins_t1/len(t1)*100:.1f}%({wins_t1}/{len(t1)})\n")

    # 评级分布(来自 evaluation)
    md.append("\n### 整体评级\n")
    md.append("> 评级基于 T+5 命中率与超额收益,详见下文章节二。\n")

    return "".join(md)


def build_strategy_evaluation(analysis: dict, evaluation: dict) -> str:
    """章节 2: 策略有效性分析(9 策略评级表)"""
    md = [section_header("二、策略有效性分析", "🧠")]

    evals = evaluation.get("evaluations", [])
    summary = evaluation.get("summary", {})

    if not evals:
        md.append("> ⚠ 无策略评估数据。\n")
        return "".join(md)

    md.append(f"- 优秀 ⭐⭐⭐: {summary.get('excellent_count', 0)} 个\n")
    md.append(f"- 合格 ⭐⭐:   {summary.get('pass_count', 0)} 个\n")
    md.append(f"- 不及格 ⭐:   {summary.get('fail_count', 0)} 个\n")
    md.append(f"- 总计:        {summary.get('total_strategies', 0)} 个策略\n")

    md.append("\n| 策略 | 样本数 | 命中率 | 平均收益(T+5) | 超额收益 | 盈亏比 | 评级 | 动作 |\n")
    md.append("|------|-------|-------|---------------|---------|--------|------|------|\n")
    for e in evals:
        pl = e.get("profit_loss_ratio", 0)
        pl_str = f"{pl:.2f}" if pl != float("inf") else "∞"
        excess = e.get("avg_excess_t5")
        excess_str = _fmt_pct(excess) if excess is not None else "—"
        md.append(
            f"| {e.get('name_cn', e['strategy'])} | {e.get('count', 0)} | "
            f"{e.get('hit_rate', 0)}% | {_fmt_pct(e.get('avg_return_t5', 0))} | "
            f"{excess_str} | {pl_str} | {e['rating']} | {e['action']} |\n"
        )

    # 评级明细
    md.append("\n### 评级标准\n")
    md.append("- ⭐⭐⭐ 优秀: 命中率 > 60% 且超额收益 > 2%\n")
    md.append("- ⭐⭐ 合格: 命中率 50-60% 或超额收益 0-2%\n")
    md.append("- ⭐ 不及格: 命中率 < 50% 或超额收益 < 0%\n")

    return "".join(md)


def build_best_holding_period(analysis: dict) -> str:
    """章节 3: 最佳持有周期"""
    md = [section_header("三、最佳持有周期", "⏱️")]

    timeframes = analysis.get("dim3_timeframe", [])
    if not timeframes:
        md.append("> ⚠ 无时间窗口分析数据。\n")
        return "".join(md)

    md.append("\n| 持有天数 | 样本数 | 平均收益 | 胜率 | 最佳 | 最差 |\n")
    md.append("|---------|---------|---------|------|------|------|\n")
    for tf in timeframes:
        md.append(
            f"| {tf['timeframe']} | {tf['count']} | {_fmt_pct(tf['avg_return'])} | "
            f"{tf['win_rate']}% | {_fmt_pct(tf['best'])} | {_fmt_pct(tf['worst'])} |\n"
        )

    # 找最佳持有周期
    best = max(timeframes, key=lambda x: x["avg_return"])
    md.append(f"\n**结论**: 最佳持有周期为 **{best['timeframe']}**"
              f"(平均收益 {best['avg_return']:+.2f}%,胜率 {best['win_rate']}%)。\n")

    return "".join(md)


def build_score_validity(analysis: dict) -> str:
    """章节 4: 评分体系有效性"""
    md = [section_header("四、评分体系有效性", "🎯")]

    scores = analysis.get("dim6_score", [])
    if not scores:
        md.append("> ⚠ 无评分分位分析数据(可能样本中无策略8 potential5 标的)。\n")
        return "".join(md)

    md.append("\n| 评分区间 | 样本数 | T+5 平均收益 | 胜率 |\n")
    md.append("|---------|---------|--------------|-------|\n")
    for s in scores:
        md.append(
            f"| {s['score_band']} | {s['count']} | "
            f"{_fmt_pct(s['avg_return_t5'])} | {s['win_rate']}% |\n"
        )

    # 结论:高分是否优于低分
    if len(scores) >= 2:
        # 按平均收益排序,看是否高分在前
        sorted_by_band = sorted(scores, key=lambda x: x["avg_return_t5"], reverse=True)
        high_band = next((s for s in scores if "高分" in s["score_band"]), None)
        low_band = next((s for s in scores if "低分" in s["score_band"]), None)
        if high_band and low_band:
            if high_band["avg_return_t5"] > low_band["avg_return_t5"]:
                diff = high_band["avg_return_t5"] - low_band["avg_return_t5"]
                md.append(f"\n**结论**: ✅ 评分体系有效 — 高分标的 T+5 平均收益 "
                          f"({high_band['avg_return_t5']:+.2f}%) 显著高于低分标的 "
                          f"({low_band['avg_return_t5']:+.2f}%),差距 {diff:+.2f}%。\n")
            else:
                md.append(f"\n**结论**: ⚠️ 评分体系失效 — 高分标的收益未优于低分标的,"
                          f"需要重新校准五引擎权重或评分维度。\n")

    return "".join(md)


def build_error_analysis(analysis: dict) -> str:
    """章节 5: 错误分析(TOP 10 亏损标的)"""
    md = [section_header("五、错误分析", "⚠️")]

    errors = analysis.get("dim7_errors", [])
    if not errors:
        md.append("> ✅ 近期无 T+5 亏损超过 5% 的标的。\n")
        return "".join(md)

    md.append(f"\n> 共 {len(errors)} 条 T+5 亏损 > 5% 的记录,TOP 10 如下:\n\n")
    md.append("| 排名 | 代码 | 名称 | 选股日 | 策略 | T+5 收益 | 区间最高 | 区间最低 | 错误类型 |\n")
    md.append("|------|------|------|--------|------|---------|---------|---------|----------|\n")
    for i, e in enumerate(errors[:10], 1):
        md.append(
            f"| {i} | {e['code']} | {e.get('name', '')} | {e['date']} | "
            f"{e.get('strategy', '')} | {_fmt_pct(e['return_t5'])} | "
            f"{_fmt_pct(e.get('max_return', 0))} | {_fmt_pct(e.get('min_return', 0))} | "
            f"{e['error_type']} |\n"
        )

    # 错误类型分布
    md.append("\n### 错误类型分布\n")
    type_count: dict[str, int] = {}
    for e in errors:
        type_count[e["error_type"]] = type_count.get(e["error_type"], 0) + 1
    md.append("| 错误类型 | 次数 | 占比 |\n")
    md.append("|---------|------|------|\n")
    total = len(errors)
    for et, cnt in sorted(type_count.items(), key=lambda x: -x[1]):
        md.append(f"| {et} | {cnt} | {cnt/total*100:.1f}% |\n")

    return "".join(md)


def build_weight_optimization(weights: dict) -> str:
    """章节 6: 权重优化建议(新旧对比)"""
    md = [section_header("六、权重优化建议", "⚖️")]

    if not weights:
        md.append("> ⚠ 无权重优化数据。\n")
        return "".join(md)

    old = weights.get("old_weights", {})
    new = weights.get("new_weights", {})
    rationale = weights.get("rationale", "")
    adjustments = weights.get("adjustments", [])
    signals = weights.get("engine_signals", {})

    md.append(f"\n> **优化理由**: {rationale}\n\n")

    md.append("| 引擎 | 旧权重 | 新权重 | 变化 | 信号 |\n")
    md.append("|------|--------|--------|------|------|\n")
    # 五引擎中文名
    engine_cn = {
        "position":  "位置",
        "valuation": "估值",
        "fund":      "资金",
        "theme":     "题材",
        "us":        "美股",
    }
    for k in old:
        old_v = old.get(k, 0)
        new_v = new.get(k, 0)
        diff = new_v - old_v
        arrow = "↑" if diff > 0.001 else "↓" if diff < -0.001 else "→"
        sig = signals.get(k, 0)
        md.append(
            f"| {engine_cn.get(k, k)} | {old_v:.3f} | {new_v:.3f} | "
            f"{arrow} {diff:+.3f} | {sig:+.2f} |\n"
        )

    if adjustments:
        md.append("\n### 调整明细\n")
        for a in adjustments:
            md.append(f"- {a}\n")

    md.append("\n### 调整约束\n")
    md.append("- 单次最大调整幅度: ≤ 30%(防过拟合)\n")
    md.append("- 单项权重范围: [0.05, 0.50]\n")
    md.append("- 归一化保持总和 = 1.0\n")

    return "".join(md)


def build_action_suggestions(evaluation: dict, analysis: dict, weights: dict) -> str:
    """章节 7: 行动建议"""
    md = [section_header("七、行动建议", "✅")]

    suggestions = evaluation.get("suggestions", [])
    if not suggestions:
        md.append("> 暂无行动建议(可能样本量不足)。\n")
        return "".join(md)

    md.append("\n### 自动生成的改进措施\n")
    for i, s in enumerate(suggestions, 1):
        md.append(f"{i}. {s}\n")

    # 追加板板块建议(基于 dim2)
    sectors = analysis.get("dim2_sector", [])
    if sectors:
        md.append("\n### 板块配置建议\n")
        top_sector = sectors[0]
        worst_sector = sectors[-1]
        md.append(f"- ✅ 表现最佳板块: **{top_sector['sector']}**"
                  f"(命中率 {top_sector['hit_rate']}%,平均 T+5 {top_sector['avg_return_t5']:+.2f}%)"
                  f"— 建议继续关注\n")
        if len(sectors) > 1:
            md.append(f"- ⚠️ 表现最差板块: **{worst_sector['sector']}**"
                      f"(命中率 {worst_sector['hit_rate']}%,平均 T+5 {worst_sector['avg_return_t5']:+.2f}%)"
                      f"— 建议谨慎参与\n")

    # 市值区间建议(基于 dim4)
    mcaps = analysis.get("dim4_mcap", [])
    if mcaps:
        md.append("\n### 市值区间建议\n")
        best_mc = max(mcaps, key=lambda x: x["avg_return_t5"])
        md.append(f"- 表现最佳市值区间: **{best_mc['mcap_band']}**"
                  f"(平均 T+5 {best_mc['avg_return_t5']:+.2f}%,胜率 {best_mc['win_rate']}%)\n")

    # 美股影响建议(基于 dim5)
    us_impacts = analysis.get("dim5_us_market", [])
    if us_impacts:
        md.append("\n### 美股隔夜信号建议\n")
        for u in us_impacts:
            md.append(f"- {u['us_signal']}: 次日平均收益 {_fmt_pct(u['avg_t1_return'])},"
                      f"胜率 {u['win_rate']}%(样本 {u['count']})\n")

    return "".join(md)


# ── 报告入口 ──
def generate(
    tracking: list,
    analysis: dict,
    evaluation: dict,
    weights: dict,
    days: int = 30,
) -> str:
    """生成完整 Markdown 报告

    Args:
        tracking:   backtest_tracker 输出
        analysis:   multi_dimension_analysis 输出
        evaluation: strategy_evaluator 输出
        weights:    weight_optimizer 输出
        days:       回溯天数(用于报告标题)
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    md = []

    # 报告头
    md.append(f"# 🧬 AI 选股自进化报告\n\n")
    md.append(f"> 生成时间: {now}\n")
    md.append(f"> 回溯周期: 近 {days} 天\n")
    md.append(f"> 分析样本: {len(tracking)} 条选股记录\n")
    md.append(f"> 系统版本: x1.0 融合版(N1.0 方法论 + v1.7.0 量化打分)\n")
    md.append(f"> 数据来源: 腾讯财经日 K 线(前复权),T+1 制度基准(次日开盘价)\n")
    md.append("---")

    # 7 大章节
    md.append(build_executive_summary(tracking, analysis))
    md.append(build_strategy_evaluation(analysis, evaluation))
    md.append(build_best_holding_period(analysis))
    md.append(build_score_validity(analysis))
    md.append(build_error_analysis(analysis))
    md.append(build_weight_optimization(weights))
    md.append(build_action_suggestions(evaluation, analysis, weights))

    # 报告尾
    md.append("\n---\n")
    md.append(f"> ⚠️ 风险声明:本报告基于历史选股数据自动生成,仅供策略优化参考,"
              f"不构成投资建议。市场有风险,投资需谨慎。\n")
    md.append(f"> 报告生成时间: {now}\n")
    md.append(f"> **当前分支**: x1.0 自进化系统\n")
    md.append(f"> **文件落盘路径**:\n")
    md.append(f"> - 追踪数据: /workspace/daily_picks/_tracking/tracking_YYYYMMDD.json\n")
    md.append(f"> - 分析结果: /workspace/daily_picks/_evolution/analysis_YYYYMMDD.json\n")
    md.append(f"> - 策略评估: /workspace/daily_picks/_evolution/evaluation_YYYYMMDD.json\n")
    md.append(f"> - 权重优化: /workspace/daily_picks/_evolution/weights_YYYYMMDD.json\n")
    md.append(f"> - 自进化报告: /workspace/daily_picks/_evolution/evolution_YYYYMMDD.md\n")

    return "".join(md)


def save_report(md: str, days: int = 30) -> Path:
    """保存报告到 _evolution 目录"""
    EVOLUTION_DIR.mkdir(parents=True, exist_ok=True)
    out = EVOLUTION_DIR / f"evolution_{datetime.now().strftime('%Y%m%d')}.md"
    out.write_text(md, encoding="utf-8")
    return out


def main():
    import argparse
    parser = argparse.ArgumentParser(description="自进化报告生成")
    parser.add_argument("--days", type=int, default=30, help="回溯天数(用于报告标题)")
    args = parser.parse_args()

    print("=== 自进化报告生成 ===")
    print("1. 加载追踪数据…")
    tracking = load_tracking()
    print(f"   追踪记录: {len(tracking)} 条")

    print("2. 加载多维度分析…")
    analysis = load_analysis()
    print(f"   维度数据: {list(analysis.keys()) if analysis else '无'}")

    print("3. 加载策略评估…")
    evaluation = load_evaluation()
    print(f"   评估策略: {evaluation.get('summary', {}).get('total_strategies', 0)} 个")

    print("4. 加载权重优化…")
    weights = load_weights()
    print(f"   新权重: {weights.get('new_weights', '无')}")

    print("5. 生成 Markdown 报告…")
    md = generate(tracking, analysis, evaluation, weights, days=args.days)
    out = save_report(md, days=args.days)
    print(f"\n✅ 报告生成完成 → {out}")
    print(f"   报告大小: {out.stat().st_size} bytes")


if __name__ == "__main__":
    main()
