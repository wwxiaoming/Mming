"""
multi_dimension_analysis.py — 7 维度分析引擎

对追踪结果进行 7 维度分析:
  dim1 策略有效性  dim2 板块题材  dim3 时间窗口
  dim4 市值区间    dim5 美股影响  dim6 评分分位
  dim7 错误分析

用法:
  python3 scripts/evolution/multi_dimension_analysis.py --days=30
"""
from __future__ import annotations
import sys, json, argparse
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
from statistics import mean, median

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))
from _common import log, DAILY_DIR

TRACK_DIR = DAILY_DIR / "_tracking"
EVOLUTION_DIR = DAILY_DIR / "_evolution"

# 板块关键词映射(用于 dim2 板块分析)
SECTOR_KEYWORDS = {
    "半导体":   ["芯片", "半导体", "光刻", "存储", "hbm", "先进封装", "碳化硅", "sic", "封测"],
    "AI/算力":  ["算力", "gpu", "ai", "大模型", "智能", "数据中心", "光模块"],
    "新能源":   ["锂电", "固态电池", "光伏", "风电", "储能", "新能源", "充电"],
    "医药":     ["医药", "医疗", "生物", "创新药", "疫苗", "中药"],
    "消费":     ["消费", "食品", "白酒", "啤酒", "零售", "家电"],
    "金融":     ["银行", "证券", "保险", "金融", "券商"],
    "军工":     ["军工", "航天", "航空", "国防", "导弹"],
    "机器人":   ["机器人", "减速器", "丝杠", "传感器", "自动化"],
    "通信":     ["通信", "5g", "6g", "卫星", "光通信"],
    "材料":     ["材料", "化工", "稀土", "磁性", "涂料", "电子化学品"],
}


def _safe_mean(lst: list[float]) -> float:
    return round(mean(lst), 2) if lst else 0.0


def _win_rate(returns: list[float]) -> float:
    if not returns:
        return 0.0
    wins = sum(1 for r in returns if r > 0)
    return round(wins / len(returns) * 100, 1)


def _profit_loss_ratio(returns: list[float]) -> float:
    """盈亏比 = 平均盈利 / 平均亏损"""
    wins = [r for r in returns if r > 0]
    losses = [abs(r) for r in returns if r < 0]
    if not wins or not losses:
        return float("inf") if wins else 0.0
    return round(mean(wins) / mean(losses), 2)


# ── dim1: 策略有效性 ──
def analyze_by_strategy(results: list[dict]) -> list[dict]:
    by_strategy = defaultdict(list)
    for r in results:
        by_strategy[r.get("strategy", "unknown")].append(r)

    output = []
    for strategy, items in by_strategy.items():
        t5 = [i["returns"]["T+5"] for i in items if "returns" in i and "T+5" in i["returns"]]
        if not t5:
            continue
        excess = [i["excess_t5"] for i in items if i.get("excess_t5") is not None]
        output.append({
            "strategy":       strategy,
            "count":          len(items),
            "hit_rate":       _win_rate(t5),
            "avg_return_t5":  _safe_mean(t5),
            "avg_excess_t5":  _safe_mean(excess) if excess else None,
            "win_rate":       _win_rate(t5),
            "profit_loss_ratio": _profit_loss_ratio(t5),
            "best":           round(max(t5), 2),
            "worst":          round(min(t5), 2),
        })
    return sorted(output, key=lambda x: x["avg_return_t5"], reverse=True)


# ── dim2: 板块/题材 ──
def analyze_by_sector(results: list[dict]) -> list[dict]:
    by_sector = defaultdict(list)
    for r in results:
        reason = r.get("reason", "")
        name = r.get("name", "")
        matched = "其他"
        for sector, keywords in SECTOR_KEYWORDS.items():
            text = (reason + name).lower()
            if any(kw.lower() in text for kw in keywords):
                matched = sector
                break
        by_sector[matched].append(r)

    output = []
    for sector, items in by_sector.items():
        t5 = [i["returns"]["T+5"] for i in items if "returns" in i and "T+5" in i["returns"]]
        if not t5:
            continue
        output.append({
            "sector":        sector,
            "count":         len(items),
            "hit_rate":      _win_rate(t5),
            "avg_return_t5": _safe_mean(t5),
            "best":          round(max(t5), 2),
            "worst":         round(min(t5), 2),
        })
    return sorted(output, key=lambda x: x["avg_return_t5"], reverse=True)


# ── dim3: 时间窗口 ──
def analyze_by_timeframe(results: list[dict]) -> list[dict]:
    timeframes = ["T+1", "T+3", "T+5", "T+10", "T+20"]
    output = []
    for tf in timeframes:
        returns = [r["returns"][tf] for r in results if "returns" in r and tf in r["returns"]]
        if not returns:
            continue
        output.append({
            "timeframe":   tf,
            "count":       len(returns),
            "avg_return":  _safe_mean(returns),
            "win_rate":    _win_rate(returns),
            "best":        round(max(returns), 2),
            "worst":       round(min(returns), 2),
        })
    return output


# ── dim4: 市值区间 ──
def analyze_by_mcap(results: list[dict]) -> list[dict]:
    bands = [
        ("<50亿", 0, 50),
        ("50-100亿", 50, 100),
        ("100-300亿", 100, 300),
        ("300-1000亿", 300, 1000),
        (">1000亿", 1000, float("inf")),
    ]
    output = []
    for label, lo, hi in bands:
        items = [r for r in results if lo <= r.get("mcap_yi", 0) < hi
                 and "returns" in r and "T+5" in r["returns"]]
        if not items:
            continue
        t5 = [i["returns"]["T+5"] for i in items]
        output.append({
            "mcap_band":    label,
            "count":        len(items),
            "avg_return_t5": _safe_mean(t5),
            "win_rate":     _win_rate(t5),
        })
    return output


# ── dim5: 美股隔夜影响 ──
def analyze_us_market_impact(results: list[dict]) -> list[dict]:
    """分析美股隔夜涨跌对选股次日表现的影响"""
    # 需要读取每日的 us_market.json
    us_cache: dict[str, dict] = {}
    for r in results:
        d = r.get("date", "")
        if d not in us_cache:
            us_file = DAILY_DIR / d / "us_market.json"
            if us_file.exists():
                try:
                    us_cache[d] = json.loads(us_file.read_text(encoding="utf-8")).get("summary", {})
                except Exception:
                    us_cache[d] = {}

    # 分组: 美股大涨(NDX>1%) / 小涨(0~1%) / 小跌(-1~0%) / 大跌(NDX<-1%)
    groups = {"美股大涨(>1%)": [], "美股小涨(0~1%)": [], "美股小跌(-1~0%)": [], "美股大跌(<-1%)": []}
    for r in results:
        us = us_cache.get(r.get("date", ""), {})
        ndx = us.get("NDX", 0)
        t1 = r.get("returns", {}).get("T+1")
        if t1 is None:
            continue
        if ndx > 1:
            groups["美股大涨(>1%)"].append(t1)
        elif ndx > 0:
            groups["美股小涨(0~1%)"].append(t1)
        elif ndx > -1:
            groups["美股小跌(-1~0%)"].append(t1)
        else:
            groups["美股大跌(<-1%)"].append(t1)

    output = []
    for label, t1_list in groups.items():
        if not t1_list:
            continue
        output.append({
            "us_signal":    label,
            "count":        len(t1_list),
            "avg_t1_return": _safe_mean(t1_list),
            "win_rate":     _win_rate(t1_list),
        })
    return output


# ── dim6: 评分分位 ──
def analyze_by_score(results: list[dict]) -> list[dict]:
    """验证评分越高是否收益越好(仅对策略8 potential5 有效)"""
    # 五引擎评分范围 0~1,转换为百分制
    # 注意: 非 potential5 策略 score=0(无评分),需与"低分"区分开,避免重叠
    bands = [
        ("高分(>0.5)", 0.5, float("inf")),
        ("中分(0.25-0.5)", 0.25, 0.5),
        ("低分(<0.25)", 0.001, 0.25),  # 排除 score=0(无评分)
        ("无评分(0)", -1, 0.001),       # score=0 的标的(其他策略无评分)
    ]
    output = []
    for label, lo, hi in bands:
        items = [r for r in results if lo <= r.get("score", 0) < hi
                 and "returns" in r and "T+5" in r["returns"]]
        if not items:
            continue
        t5 = [i["returns"]["T+5"] for i in items]
        output.append({
            "score_band":    label,
            "count":         len(items),
            "avg_return_t5": _safe_mean(t5),
            "win_rate":      _win_rate(t5),
        })
    return output


# ── dim7: 错误分析 ──
def analyze_errors(results: list[dict]) -> list[dict]:
    """分析 T+5 亏损超过 5% 的标的"""
    errors = []
    for r in results:
        returns = r.get("returns", {})
        t5 = returns.get("T+5")
        if t5 is None or t5 >= -5:
            continue
        errors.append({
            "code":       r["code"],
            "name":       r.get("name", ""),
            "date":       r["date"],
            "strategy":   r.get("strategy", ""),
            "return_t5":  t5,
            "max_return": r.get("max_return", 0),
            "min_return": r.get("min_return", 0),
            "error_type": _classify_error(r, t5),
        })
    return sorted(errors, key=lambda x: x["return_t5"])


def _classify_error(r: dict, ret: float) -> str:
    """错误分类"""
    chg = r.get("change_pct", 0)
    if chg > 6:
        return "追高被套"
    if ret < -10:
        return "大幅下跌"
    if ret < -5:
        return "持续下跌"
    return "小幅亏损"


# ── 主分析函数 ──
def analyze(results: list[dict]) -> dict:
    """执行 7 维度分析"""
    if not results:
        return {"error": "无追踪数据"}
    return {
        "dim1_strategy":   analyze_by_strategy(results),
        "dim2_sector":     analyze_by_sector(results),
        "dim3_timeframe":  analyze_by_timeframe(results),
        "dim4_mcap":       analyze_by_mcap(results),
        "dim5_us_market":  analyze_us_market_impact(results),
        "dim6_score":      analyze_by_score(results),
        "dim7_errors":     analyze_errors(results),
    }


def load_latest_tracking() -> list[dict]:
    """加载最新的追踪数据"""
    files = sorted(TRACK_DIR.glob("tracking_*.json"), reverse=True)
    if not files:
        return []
    return json.loads(files[0].read_text(encoding="utf-8"))


def main():
    parser = argparse.ArgumentParser(description="7 维度分析引擎")
    parser.add_argument("--days", type=int, default=30, help="回溯天数")
    parser.add_argument("--input", type=str, default=None, help="指定追踪数据文件")
    args = parser.parse_args()

    if args.input:
        results = json.loads(Path(args.input).read_text(encoding="utf-8"))
    else:
        results = load_latest_tracking()

    if not results:
        print("⚠ 无追踪数据,请先运行 backtest_tracker.py")
        sys.exit(1)

    print(f"分析 {len(results)} 条追踪记录…")
    analysis = analyze(results)

    EVOLUTION_DIR.mkdir(parents=True, exist_ok=True)
    out = EVOLUTION_DIR / f"analysis_{datetime.now().strftime('%Y%m%d')}.json"
    out.write_text(json.dumps(analysis, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ 分析完成 → {out}")

    # 打印摘要
    print("\n=== dim1 策略有效性 ===")
    for s in analysis.get("dim1_strategy", []):
        print(f"  {s['strategy']}: 命中率={s['hit_rate']}% 均收={s['avg_return_t5']}% 盈亏比={s['profit_loss_ratio']}")


if __name__ == "__main__":
    main()
