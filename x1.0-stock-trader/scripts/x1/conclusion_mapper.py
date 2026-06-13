"""
conclusion_mapper.py — x1.0 4 选 1 结论映射器

把 v1.7.0 五引擎评分映射到 N1.0 第 4 章的 4 类固定结论。
边界：EDGE_LOW=0.50, EDGE_HIGH=0.70 区间触发 LLM 二次确认。
"""
from __future__ import annotations
from typing import Any

EDGE_LOW = 0.50
EDGE_HIGH = 0.70

# 4 选 1 结论枚举（与 N1.0 第 4 章完全一致）
CONCL_BUY = "可直接试仓买入"
CONCL_WAIT = "条件满足才可买入"
CONCL_WATCH = "只可观察，不可买"
CONCL_AVOID = "明确不买"

CONCL_TO_EMOJI = {
    CONCL_BUY:   "🟢",
    CONCL_WAIT:  "🟡",
    CONCL_WATCH: "⚪",
    CONCL_AVOID: "🔴",
}

# 评分 → 结论 映射表
THRESHOLD_BUY = 0.70
THRESHOLD_WAIT = 0.50
THRESHOLD_WATCH = 0.25


def _condition_trigger(sub: dict[str, Any] | None) -> str:
    """根据子维度给出条件触发提示（仅在 WAIT 时返回）"""
    if not sub:
        return "需放量不破 / 板块共振确认 / 高开幅度合理"
    tips = []
    pos = float(sub.get("position", 0) or 0)
    fund = float(sub.get("fund", 0) or 0)
    theme = float(sub.get("theme", 0) or 0)
    if pos < 0.5:
        tips.append("等回调到位（位置分 < 0.5 提示买点未到）")
    if fund < 0.5:
        tips.append("等主力建仓信号（换手 1.5-8% + vol_ratio > 1）")
    if theme < 0.5:
        tips.append("等题材催化（同花顺热点 reason 命中）")
    if not tips:
        tips.append("等放量不破 / 板块共振确认 / 高开幅度合理")
    return " | ".join(tips)


def map_conclusion(
    score: float,
    sub_metrics: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    输入：score       = 五引擎总分（0~1）
         sub_metrics = {position, valuation, fund, theme, us}（可选）
    输出：{conclusion, emoji, condition_trigger, edge_flag, conflict_note}
    """
    if score >= THRESHOLD_BUY:
        return {
            "conclusion":       CONCL_BUY,
            "emoji":            CONCL_TO_EMOJI[CONCL_BUY],
            "condition_trigger": "",
            "edge_flag":        False,
            "conflict_note":    "",
        }
    if score >= THRESHOLD_WAIT:
        edge = EDGE_LOW <= score <= EDGE_HIGH
        return {
            "conclusion":       CONCL_WAIT,
            "emoji":            CONCL_TO_EMOJI[CONCL_WAIT],
            "condition_trigger": _condition_trigger(sub_metrics),
            "edge_flag":        edge,
            "conflict_note":    "评分边缘，需 LLM 二次确认" if edge else "",
        }
    if score >= THRESHOLD_WATCH:
        return {
            "conclusion":       CONCL_WATCH,
            "emoji":            CONCL_TO_EMOJI[CONCL_WATCH],
            "condition_trigger": "",
            "edge_flag":        False,
            "conflict_note":    "",
        }
    return {
        "conclusion":       CONCL_AVOID,
        "emoji":            CONCL_TO_EMOJI[CONCL_AVOID],
        "condition_trigger": "",
        "edge_flag":        False,
        "conflict_note":    "",
    }


# ── 自测 ──
if __name__ == "__main__":
    cases = [
        (0.85, None, "强烈建议"),
        (0.62, {"position": 0.4, "fund": 0.8, "theme": 0.6}, "边缘待确认"),
        (0.45, None, "观察"),
        (0.10, None, "明确不买"),
    ]
    for s, sub, label in cases:
        r = map_conclusion(s, sub)
        print(f"  score={s:.2f} ({label}): {r['emoji']} {r['conclusion']}"
              + (f" | edge={r['edge_flag']}" if r['edge_flag'] else "")
              + (f" | trigger={r['condition_trigger']}" if r['condition_trigger'] else ""))
