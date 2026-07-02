"""
weight_optimizer.py — 权重自动优化

基于策略有效性评估,自动调整 x1.0 五引擎权重。
当前权重: 位置 0.20 / 估值 0.15 / 资金 0.30 / 题材 0.20 / 美股 0.15

约束:
  - 每次调整幅度 ≤ 30%(防过拟合)
  - 归一化保持总和 = 1.0
  - 单项权重范围 [0.05, 0.50]

用法:
  python3 scripts/evolution/weight_optimizer.py
"""
from __future__ import annotations
import sys, json
from pathlib import Path
from datetime import datetime

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))
from _common import DAILY_DIR

EVOLUTION_DIR = DAILY_DIR / "_evolution"

# x1.0 当前五引擎权重(选股手册_x1.0.md 第 17.1 节)
CURRENT_WEIGHTS = {
    "position":    0.20,  # 位置
    "valuation":   0.15,  # 估值
    "fund":        0.30,  # 资金
    "theme":       0.20,  # 题材
    "us":          0.15,  # 美股
}

# 策略 → 影响的引擎维度映射
# (策略有效性如何反映到引擎权重上)
STRATEGY_TO_ENGINE = {
    "1_momentum":      ["theme", "position"],       # 强势股 → 题材+位置
    "2_fund_flow":     ["fund"],                     # 主力资金 → 资金
    "3_value":         ["valuation"],                 # 价值股 → 估值
    "7_buffett_moat":  ["valuation"],                 # 护城河 → 估值
    "8_potential5":    ["position", "valuation", "fund", "theme", "us"],  # 五引擎综合
}

MAX_ADJUST = 0.30  # 单次最大调整幅度 30%
MIN_WEIGHT = 0.05
MAX_WEIGHT = 0.50


def optimize_weights(evaluation: dict) -> dict:
    """根据策略评估结果优化权重

    Returns:
        {"old_weights": {...}, "new_weights": {...},
         "changes": {...}, "rationale": "...", "adjustments": [...]}
    """
    evaluations = evaluation.get("evaluations", [])
    if not evaluations:
        return {
            "old_weights": CURRENT_WEIGHTS,
            "new_weights": CURRENT_WEIGHTS,
            "changes": {},
            "rationale": "无策略评估数据,保持当前权重",
            "adjustments": [],
        }

    # 计算每个引擎维度的调整信号
    engine_signals: dict[str, float] = {}  # engine → 调整方向(+/-)

    for e in evaluations:
        strategy = e["strategy"]
        rating = e["rating"]
        hit_rate = e.get("hit_rate", 50)
        avg_return = e.get("avg_return_t5", 0)
        count = e.get("count", 0)

        # 样本太少不参考
        if count < 3:
            continue

        # 调整强度: 命中率偏离 50% 的幅度 × 收益方向
        signal = (hit_rate - 50) / 50 * 0.5 + (avg_return / 10) * 0.5
        signal = max(min(signal, 1.0), -1.0)

        engines = STRATEGY_TO_ENGINE.get(strategy, [])
        for engine in engines:
            if engine not in engine_signals:
                engine_signals[engine] = []
            engine_signals[engine].append(signal)

    # 平均每个引擎的信号
    engine_avg: dict[str, float] = {}
    for engine, signals in engine_signals.items():
        engine_avg[engine] = sum(signals) / len(signals) if signals else 0

    # 计算新权重
    new_weights = dict(CURRENT_WEIGHTS)
    adjustments = []

    for engine, old_w in CURRENT_WEIGHTS.items():
        signal = engine_avg.get(engine, 0)
        if signal == 0:
            continue

        # 调整量 = 信号 × 最大调整幅度 × 当前权重
        delta = signal * MAX_ADJUST * old_w
        new_w = old_w + delta

        # 约束范围
        new_w = max(MIN_WEIGHT, min(MAX_WEIGHT, new_w))
        new_weights[engine] = round(new_w, 3)

        actual_delta = round(new_w - old_w, 3)
        if abs(actual_delta) > 0.001:
            direction = "↑" if actual_delta > 0 else "↓"
            adjustments.append(
                f"{direction} {engine}: {old_w:.3f} → {new_w:.3f} (Δ {actual_delta:+.3f}, 信号 {signal:+.2f})"
            )

    # 归一化(确保总和 = 1.0)
    total = sum(new_weights.values())
    if total > 0:
        for k in new_weights:
            new_weights[k] = round(new_weights[k] / total, 3)

    changes = {k: round(new_weights[k] - CURRENT_WEIGHTS.get(k, 0), 3) for k in new_weights}

    return {
        "old_weights": CURRENT_WEIGHTS,
        "new_weights": new_weights,
        "changes": changes,
        "rationale": "基于策略命中率与平均收益自动优化,单次调整 ≤ 30%",
        "adjustments": adjustments,
        "engine_signals": {k: round(v, 3) for k, v in engine_avg.items()},
    }


def load_latest_evaluation() -> dict:
    """加载最新的策略评估"""
    files = sorted(EVOLUTION_DIR.glob("evaluation_*.json"), reverse=True)
    if not files:
        return {}
    return json.loads(files[0].read_text(encoding="utf-8"))


def main():
    evaluation = load_latest_evaluation()
    if not evaluation:
        print("⚠ 无评估数据,请先运行 strategy_evaluator.py")
        sys.exit(1)

    result = optimize_weights(evaluation)

    out = EVOLUTION_DIR / f"weights_{datetime.now().strftime('%Y%m%d')}.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ 权重优化完成 → {out}")

    print(f"\n旧权重: {result['old_weights']}")
    print(f"新权重: {result['new_weights']}")
    print(f"\n调整明细:")
    for a in result["adjustments"]:
        print(f"  {a}")


if __name__ == "__main__":
    main()
