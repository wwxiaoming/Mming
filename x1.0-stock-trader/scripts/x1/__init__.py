"""x1.0 融合版工程包。

提供 N1.0 方法论纪律 → v1.7.0 量化打分的双向桥梁：
- environment_gate:  S/A/B/C/D 五级环境评级
- exclusion_filter:   10 条排除规则脚本化
- conclusion_mapper:  评分 → 4 选 1 结论映射
"""
from .environment_gate import evaluate, grade_to_position
from .exclusion_filter import filter_excluded, EXCLUSION_REASONS
from .conclusion_mapper import map_conclusion, EDGE_LOW, EDGE_HIGH

__all__ = [
    "evaluate",
    "grade_to_position",
    "filter_excluded",
    "EXCLUSION_REASONS",
    "map_conclusion",
    "EDGE_LOW",
    "EDGE_HIGH",
]
