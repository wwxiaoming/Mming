"""
strategy_evaluator.py — 策略有效性评估

基于多维度分析结果,对 9 大策略进行评级并生成改进建议。

评级标准:
  ⭐⭐⭐ 优秀: 命中率 > 60% 且超额收益 > 2%
  ⭐⭐   合格: 命中率 50-60% 或超额收益 0-2%
  ⭐     不及格: 命中率 < 50% 或超额收益 < 0%

用法:
  python3 scripts/evolution/strategy_evaluator.py
"""
from __future__ import annotations
import sys, json
from pathlib import Path
from datetime import datetime

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))
from _common import DAILY_DIR

EVOLUTION_DIR = DAILY_DIR / "_evolution"

RATING_EXCELLENT = "⭐⭐⭐"
RATING_PASS = "⭐⭐"
RATING_FAIL = "⭐"

# 策略中文名映射
STRATEGY_NAMES = {
    "1_momentum":      "策略1-强势股",
    "2_fund_flow":     "策略2-主力资金",
    "3_value":         "策略3-价值股",
    "4_etf_premium":   "策略4-ETF活跃",
    "6_serenity_chain": "策略6-产业链",
    "7_buffett_moat":  "策略7-护城河",
    "8_potential5":    "策略8-五引擎潜力",
}


def evaluate_strategy(strategy_data: dict) -> dict:
    """评估单个策略

    Returns:
        {"strategy": ..., "rating": "⭐⭐⭐", "action": "加大权重",
         "reasons": [...], "suggestions": [...]}
    """
    hit_rate = strategy_data.get("hit_rate", 0)
    avg_return = strategy_data.get("avg_return_t5", 0)
    excess = strategy_data.get("avg_excess_t5")
    pl_ratio = strategy_data.get("profit_loss_ratio", 0)
    count = strategy_data.get("count", 0)

    reasons = []
    suggestions = []

    # 评级
    if hit_rate > 60 and (excess is not None and excess > 2):
        rating = RATING_EXCELLENT
        action = "加大权重"
        reasons.append(f"命中率 {hit_rate}% > 60%,超额收益 {excess}% > 2%")
        suggestions.append(f"✅ 策略「{STRATEGY_NAMES.get(strategy_data['strategy'], strategy_data['strategy'])}」表现优秀,建议加大权重")
    elif hit_rate > 50 or (excess is not None and excess > 0):
        rating = RATING_PASS
        action = "保持权重"
        reasons.append(f"命中率 {hit_rate}%,超额收益 {excess if excess is not None else 'N/A'}%")
    else:
        rating = RATING_FAIL
        action = "降低权重" if hit_rate > 30 else "考虑暂停"
        reasons.append(f"命中率 {hit_rate}% < 50%,超额收益 {excess if excess is not None else 'N/A'}%")
        suggestions.append(f"⚠️ 策略「{STRATEGY_NAMES.get(strategy_data['strategy'], strategy_data['strategy'])}」命中率仅 {hit_rate}%,建议{action}")

    # 盈亏比分析
    if pl_ratio != float("inf") and pl_ratio < 1.0 and count >= 5:
        reasons.append(f"盈亏比 {pl_ratio} < 1.0,亏损大于盈利")
        if rating == RATING_PASS:
            rating = RATING_FAIL
            action = "降低权重"
            suggestions.append(f"⚠️ 策略「{strategy_data['strategy']}」盈亏比 {pl_ratio} 偏低,建议降低权重")

    # 样本量不足警告
    if count < 5:
        reasons.append(f"样本量仅 {count} 条,统计意义有限")
        suggestions.append(f"📊 策略「{strategy_data['strategy']}」样本量不足({count}),建议积累更多数据再评估")

    return {
        **strategy_data,
        "rating": rating,
        "action": action,
        "reasons": reasons,
        "suggestions": suggestions,
        "name_cn": STRATEGY_NAMES.get(strategy_data["strategy"], strategy_data["strategy"]),
    }


def evaluate_all(analysis: dict) -> dict:
    """评估所有策略"""
    strategy_list = analysis.get("dim1_strategy", [])
    evaluations = [evaluate_strategy(s) for s in strategy_list]

    # 全局建议
    global_suggestions = []
    excellent = [e for e in evaluations if e["rating"] == RATING_EXCELLENT]
    failing = [e for e in evaluations if e["rating"] == RATING_FAIL]

    if excellent:
        global_suggestions.append(f"✅ {len(excellent)} 个策略表现优秀: {', '.join(e['name_cn'] for e in excellent)}")
    if failing:
        global_suggestions.append(f"⚠️ {len(failing)} 个策略不及格: {', '.join(e['name_cn'] for e in failing)}")

    # 最佳持有周期建议
    timeframes = analysis.get("dim3_timeframe", [])
    if timeframes:
        best_tf = max(timeframes, key=lambda x: x["avg_return"])
        global_suggestions.append(f"📊 最佳持有周期为 {best_tf['timeframe']}(平均收益 {best_tf['avg_return']}%),建议以此周期为主")

    # 评分体系验证
    scores = analysis.get("dim6_score", [])
    if len(scores) >= 2:
        high = [s for s in scores if "高分" in s["score_band"]]
        low = [s for s in scores if "低分" in s["score_band"]]
        if high and low:
            if high[0]["avg_return_t5"] > low[0]["avg_return_t5"]:
                global_suggestions.append("✅ 评分体系有效:高分标的收益显著优于低分")
            else:
                global_suggestions.append("⚠️ 评分体系失效:高分标的收益未优于低分,需要重新校准")

    # 合并所有建议
    all_suggestions = global_suggestions
    for e in evaluations:
        all_suggestions.extend(e["suggestions"])

    return {
        "evaluations": evaluations,
        "summary": {
            "excellent_count": len(excellent),
            "pass_count": len([e for e in evaluations if e["rating"] == RATING_PASS]),
            "fail_count": len(failing),
            "total_strategies": len(evaluations),
        },
        "suggestions": all_suggestions,
    }


def load_latest_analysis() -> dict:
    """加载最新的分析结果"""
    files = sorted(EVOLUTION_DIR.glob("analysis_*.json"), reverse=True)
    if not files:
        return {}
    return json.loads(files[0].read_text(encoding="utf-8"))


def main():
    analysis = load_latest_analysis()
    if not analysis:
        print("⚠ 无分析数据,请先运行 multi_dimension_analysis.py")
        sys.exit(1)

    result = evaluate_all(analysis)

    out = EVOLUTION_DIR / f"evaluation_{datetime.now().strftime('%Y%m%d')}.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ 评估完成 → {out}")

    for e in result["evaluations"]:
        print(f"  {e['rating']} {e['name_cn']}: 命中率={e['hit_rate']}% 动作={e['action']}")

    print("\n=== 行动建议 ===")
    for s in result["suggestions"]:
        print(f"  {s}")


if __name__ == "__main__":
    main()
