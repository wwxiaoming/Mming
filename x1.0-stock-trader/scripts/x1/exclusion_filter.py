"""
exclusion_filter.py — x1.0 排除规则过滤器

把 N1.0 第 7 章的 10 条排除规则脚本化，作为 v1.7.0 评分前的硬过滤。
每条规则对应一个 reason code，被排除的标的带原因返回。
"""
from __future__ import annotations
from typing import Any

EXCLUSION_REASONS = {
    "E_HIGH_RISE":   "① 高位加速：当日涨幅 > 6% 已透支",
    "E_LOW_VOL":     "② 缩量硬质：换手 < 1.5% 且 vol_ratio < 0.8，承接不明",
    "E_HIGH_GAP":    "③ 高开过多：开盘涨幅 > 5%，盈亏比差",
    "E_NO_THEME":    "④ 逻辑不清：题材 reason 为空，情绪冲动",
    "E_THEME_DIFF":  "⑤ 题材发散：单一题材占比 > 50%，核心不明确",
    "E_NOT_FRONT":   "⑥ 非前排：不在板块 TOP 3 名单",
    "E_SECTOR_WEAK": "⑦ 板块持续性存疑：5 日板块涨跌 < -2%",
    "E_BAD_ENV":     "⑧ 环境不支持：环境闸门评级 D",
    "E_HISTORY_DUMP":"⑨ 冲高回落历史：最近 5 日 K 线 3 根上影线 > 5%",
    "E_MODE_MISMATCH":"⑩ 模式不匹配：持仓周期 > 短线",
}


def _high_rise(s: dict) -> bool:
    """① 高位加速后接：当日涨幅 > 6%"""
    return float(s.get("change_pct", 0) or 0) > 6.0


def _low_volume(s: dict) -> bool:
    """② 缩量硬质：换手 < 1.5% 且 vol_ratio < 0.8"""
    t = float(s.get("turnover_pct", 0) or 0)
    v = float(s.get("vol_ratio", 1.0) or 1.0)
    return t < 1.5 and v < 0.8


def _high_gap(s: dict) -> bool:
    """③ 高开过多：开盘涨幅 > 5%"""
    o = float(s.get("open", 0) or 0)
    lc = float(s.get("last_close", 0) or 0)
    if lc <= 0:
        return False
    gap = (o / lc - 1) * 100
    return gap > 5.0


def _no_theme(s: dict) -> bool:
    """④ 逻辑不清：reason 为空"""
    return not (s.get("reason") or "").strip()


def _theme_diffuse(s: dict) -> bool:
    """⑤ 题材发散：单一题材占比 > 50%"""
    pct = float(s.get("theme_concentration", 0) or 0)
    return pct > 50.0


def _not_front(s: dict) -> bool:
    """⑥ 非前排：板块内排名 > 3"""
    rank = int(s.get("sector_rank", 99) or 99)
    return rank > 3


def _sector_weak(s: dict) -> bool:
    """⑦ 板块持续性存疑：5 日板块涨跌 < -2%"""
    return float(s.get("sector_chg_5d", 0) or 0) < -2.0


def _history_dump(s: dict) -> bool:
    """⑨ 冲高回落历史：最近 5 日 K 线 3 根上影线 > 5%"""
    upper_shadows = s.get("upper_shadow_count_5d", 0)
    return int(upper_shadows) >= 3


def _mode_mismatch(s: dict) -> bool:
    """⑩ 模式不匹配：用户持仓周期不匹配短线"""
    cycle = s.get("holding_cycle", "short")
    return cycle not in ("short", "day", "overnight")


RULES = [
    ("E_HIGH_RISE",     _high_rise),
    ("E_LOW_VOL",       _low_volume),
    ("E_HIGH_GAP",      _high_gap),
    ("E_NO_THEME",      _no_theme),
    ("E_THEME_DIFF",    _theme_diffuse),
    ("E_NOT_FRONT",     _not_front),
    ("E_SECTOR_WEAK",   _sector_weak),
    ("E_HISTORY_DUMP",  _history_dump),
    ("E_MODE_MISMATCH", _mode_mismatch),
]


def filter_excluded(
    stock_list: list[dict],
    market: dict[str, Any] | None = None,
) -> tuple[list[dict], list[dict]]:
    """
    输入：stock_list = [{code, name, change_pct, ...}, ...]
         market     = 环境闸门结果（用于 E_BAD_ENV）
    输出：(passed, excluded_with_reason)
          passed  = 保留的标的
          excluded = [{code, name, reason_code, reason_text}, ...]
    """
    passed: list[dict] = []
    excluded: list[dict] = []

    # 环境闸门：如果是 D 级，所有股都被排除
    env_skip = bool(market and market.get("skip_stock_pick"))

    for s in stock_list:
        if env_skip:
            excluded.append({
                "code": s.get("code", ""),
                "name": s.get("name", ""),
                "reason_code": "E_BAD_ENV",
                "reason_text": EXCLUSION_REASONS["E_BAD_ENV"],
            })
            continue

        # 顺序检查所有规则，第一条命中即排除
        hit = None
        for code, fn in RULES:
            try:
                if fn(s):
                    hit = code
                    break
            except Exception:
                # 数据缺失时静默跳过该条规则
                continue

        if hit:
            excluded.append({
                "code": s.get("code", ""),
                "name": s.get("name", ""),
                "reason_code": hit,
                "reason_text": EXCLUSION_REASONS[hit],
            })
        else:
            passed.append(s)

    return passed, excluded


# ── 自测 ──
if __name__ == "__main__":
    sample = [
        {"code": "300750", "name": "宁德时代", "change_pct": 7.5, "turnover_pct": 2.0, "vol_ratio": 1.2, "reason": "固态电池"},
        {"code": "000001", "name": "平安银行", "change_pct": 0.5, "turnover_pct": 0.5, "vol_ratio": 0.6, "reason": ""},
        {"code": "002594", "name": "比亚迪",   "change_pct": 1.0, "turnover_pct": 3.0, "vol_ratio": 1.5, "reason": "新能源车", "sector_rank": 1},
        {"code": "300059", "name": "东方财富", "change_pct": 2.0, "turnover_pct": 4.0, "vol_ratio": 1.3, "reason": "券商"},
    ]
    passed, excl = filter_excluded(sample)
    print(f"  通过 {len(passed)} / 排除 {len(excl)}")
    for p in passed:
        print(f"    ✅ {p['code']} {p['name']}")
    for e in excl:
        print(f"    ❌ {e['code']} {e['name']} → {e['reason_text']}")
