"""
environment_gate.py — x1.0 环境闸门

按 N1.0 第 8 章「S/A/B/C/D 五级环境评级」实现为可执行函数。
输入：市场数据 dict（指数 / 情绪 / 连板 / 量能 / 催化 5 维度）
输出：{grade, position_size, skip_stock_pick, reasoning}
"""
from __future__ import annotations
from typing import Any

GRADE_S = "S"
GRADE_A = "A"
GRADE_B = "B"
GRADE_C = "C"
GRADE_D = "D"

GRADE_TO_POSITION = {
    GRADE_S: ("可适当积极", 0.7, 1.0),
    GRADE_A: ("轻仓试错", 0.4, 0.7),
    GRADE_B: ("严格控制仓位", 0.2, 0.4),
    GRADE_C: ("以观察为主", 0.0, 0.2),
    GRADE_D: ("尽量空仓/少动", 0.0, 0.0),
}


def grade_to_position(grade: str) -> tuple[str, float, float]:
    """根据评级取 (仓位描述, 仓位下限, 仓位上限)"""
    return GRADE_TO_POSITION.get(grade, GRADE_TO_POSITION[GRADE_C])


def evaluate(market: dict[str, Any] | None) -> dict[str, Any]:
    """
    输入示例：
    {
        "index_chg":   1.2,        # 上证/沪深300 当日涨跌幅 %
        "sentiment":   "high",     # high / mid / low
        "limit_up":    50,         # 涨停家数
        "limit_down":  5,          # 跌停家数
        "volume_vs5d": 1.3,        # 当日成交额 / 5日均量
        "leaders":     ["算力","固态电池"],  # 主线方向列表
        "is_trading_day": True,    # 是否交易日
    }
    """
    if not market or not market.get("is_trading_day", True):
        return {
            "grade": GRADE_D,
            "position_desc": "休市日，无交易",
            "position_low": 0.0,
            "position_high": 0.0,
            "skip_stock_pick": True,
            "reasoning": "休市日或数据缺失，跳过选股",
        }

    score = 0
    reasons = []

    # 1) 指数环境（±30）
    chg = float(market.get("index_chg", 0) or 0)
    if chg >= 1.0:
        score += 30; reasons.append(f"指数 +{chg:.2f}% 强势")
    elif chg >= 0.3:
        score += 20; reasons.append(f"指数 +{chg:.2f}% 偏强")
    elif chg >= -0.3:
        score += 10; reasons.append(f"指数 {chg:+.2f}% 震荡")
    elif chg >= -1.0:
        score += 0;  reasons.append(f"指数 {chg:+.2f}% 偏弱")
    else:
        score -= 20; reasons.append(f"指数 {chg:+.2f}% 弱势")

    # 2) 情绪环境（±25）
    sent = (market.get("sentiment") or "").lower()
    if sent == "high":
        score += 25; reasons.append("情绪高")
    elif sent == "mid":
        score += 10; reasons.append("情绪中")
    elif sent == "low":
        score -= 15; reasons.append("情绪低")
    else:
        score += 5;  reasons.append("情绪未知，按中性")

    # 3) 连板梯队（±20）
    lu = int(market.get("limit_up", 0) or 0)
    ld = int(market.get("limit_down", 0) or 0)
    if lu >= 60 and ld <= 10:
        score += 20; reasons.append(f"涨停 {lu} / 跌停 {ld} 梯队健康")
    elif lu >= 30:
        score += 10; reasons.append(f"涨停 {lu} 中等")
    elif lu < 15 and ld > 30:
        score -= 20; reasons.append(f"涨停 {lu} 跌停 {ld} 退潮")
    else:
        score += 0;  reasons.append(f"涨停 {lu} 跌停 {ld} 一般")

    # 4) 量能（±15）
    vol = float(market.get("volume_vs5d", 1.0) or 1.0)
    if vol >= 1.3:
        score += 15; reasons.append(f"量能 {vol:.2f}x 放量")
    elif vol >= 0.9:
        score += 5;  reasons.append(f"量能 {vol:.2f}x 正常")
    elif vol >= 0.7:
        score -= 5; reasons.append(f"量能 {vol:.2f}x 缩量")
    else:
        score -= 15; reasons.append(f"量能 {vol:.2f}x 严重缩量")

    # 5) 主线催化（±10）
    leaders = market.get("leaders") or []
    if len(leaders) >= 2:
        score += 10; reasons.append(f"主线 {','.join(leaders[:3])} 清晰")
    elif len(leaders) == 1:
        score += 5;  reasons.append(f"主线 {leaders[0]} 单点")
    else:
        score -= 5; reasons.append("无清晰主线")

    # 评级映射
    if score >= 70:
        grade = GRADE_S
    elif score >= 50:
        grade = GRADE_A
    elif score >= 30:
        grade = GRADE_B
    elif score >= 10:
        grade = GRADE_C
    else:
        grade = GRADE_D

    pos_desc, pos_low, pos_high = grade_to_position(grade)
    skip = grade == GRADE_D

    return {
        "grade": grade,
        "position_desc": pos_desc,
        "position_low": pos_low,
        "position_high": pos_high,
        "skip_stock_pick": skip,
        "raw_score": score,
        "reasoning": " | ".join(reasons),
    }


# ── 自测 ──
if __name__ == "__main__":
    samples = [
        ("强势环境", {"index_chg": 1.5, "sentiment": "high", "limit_up": 80, "limit_down": 5, "volume_vs5d": 1.4, "leaders": ["算力", "固态电池"]}),
        ("一般环境", {"index_chg": 0.0, "sentiment": "mid", "limit_up": 30, "limit_down": 15, "volume_vs5d": 1.0, "leaders": ["AI"]}),
        ("弱势环境", {"index_chg": -1.5, "sentiment": "low", "limit_up": 10, "limit_down": 40, "volume_vs5d": 0.6, "leaders": []}),
        ("休市日",   {"is_trading_day": False}),
    ]
    for name, m in samples:
        r = evaluate(m)
        print(f"  {name}: grade={r['grade']} pos={r['position_desc']} skip={r['skip_stock_pick']}")
        print(f"    reasoning: {r['reasoning']}")
