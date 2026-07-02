"""
backtest_tracker.py — 拉取选股后实际行情

读取过去 N 天的 daily_picks.json,对每只股票拉取选股日之后的日 K 线,
以次日开盘价为基准计算 T+1/T+3/T+5/T+10/T+20 收益率。

用法:
  python3 scripts/evolution/backtest_tracker.py --days=30
"""
from __future__ import annotations
import sys, json, argparse
from pathlib import Path
from datetime import datetime, timedelta
from collections import OrderedDict

# 确保能 import 父级 _common 和 evolution._kline
SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import log, DAILY_DIR
from _kline import tencent_daily_kline, fetch_index_kline

TRACK_DIR = DAILY_DIR / "_tracking"

# 9 大策略 → 中文标签
STRATEGY_LABELS = OrderedDict([
    ("1_momentum",     "策略1-强势股"),
    ("2_fund_flow",    "策略2-主力资金"),
    ("3_value",        "策略3-价值股"),
    ("4_etf_premium",  "策略4-ETF活跃"),
    ("6_serenity_chain","策略6-产业链"),
    ("7_buffett_moat", "策略7-护城河"),
    ("8_potential5",   "策略8-五引擎潜力"),
])

# 哪些策略包含可追踪的个股(有 code 字段)
TRACKABLE_STRATEGIES = list(STRATEGY_LABELS.keys())


def load_historical_picks(days: int = 30) -> list[dict]:
    """读取过去 N 天的选股记录

    Returns:
        [{"date": "2026-06-20", "strategy": "1_momentum",
          "code": "300665", "name": "飞鹿股份",
          "score": 0.0, "price_at_pick": 11.76,
          "reason": "...", "mcap_yi": 0}, ...]
    """
    cutoff = datetime.now() - timedelta(days=days)
    records = []

    for d in sorted(DAILY_DIR.iterdir()):
        if not d.is_dir() or d.name.startswith("_"):
            continue
        try:
            dt = datetime.strptime(d.name, "%Y-%m-%d")
        except ValueError:
            continue
        if dt < cutoff:
            continue

        picks_file = d / "daily_picks.json"
        if not picks_file.exists():
            continue

        try:
            data = json.loads(picks_file.read_text(encoding="utf-8"))
        except Exception:
            continue

        pick_date = d.name
        for strat_key, strat_label in STRATEGY_LABELS.items():
            items = data.get(strat_key, [])
            if not isinstance(items, list):
                continue
            for item in items:
                code = item.get("code", "")
                if not code or len(code) != 6:
                    continue
                # ETF(15/16/51/52 开头)跳过,不追踪
                if code.startswith(("15", "16", "51", "52")):
                    continue
                records.append({
                    "date":          pick_date,
                    "strategy":      strat_key,
                    "strategy_label": strat_label,
                    "code":          code,
                    "name":          item.get("name", ""),
                    "score":         item.get("score", 0),
                    "price_at_pick": item.get("price", 0),
                    "reason":        item.get("reason", ""),
                    "pe_ttm":        item.get("pe_ttm", 0),
                    "mcap_yi":       item.get("mcap_yi", 0),
                    "change_pct":    item.get("change_pct", 0),
                })

    print(f"读取 {len(records)} 条历史选股记录(近 {days} 天)")
    return records


def fetch_post_pick_performance(code: str, pick_date: str, max_days: int = 25) -> dict:
    """拉取选股后 N 天的实际表现

    以选股日**次日开盘价**为基准(T+1 制度),计算 T+1/T+3/T+5/T+10/T+20 收益率。

    Returns:
        {"code": code, "base_price": 10.5, "base_date": "2026-06-21",
         "returns": {"T+1": 1.2, "T+3": 3.5, ...},
         "max_return": 8.5, "min_return": -2.3, "kline_count": 20}
    """
    # 拉取选股日前后各加 buffer 的 K 线
    start = (datetime.strptime(pick_date, "%Y-%m-%d") - timedelta(days=5)).strftime("%Y-%m-%d")
    end = (datetime.strptime(pick_date, "%Y-%m-%d") + timedelta(days=max_days + 15)).strftime("%Y-%m-%d")

    klines = tencent_daily_kline(code, start_date=start, end_date=end)
    if len(klines) < 2:
        return {"code": code, "error": "K线数据不足", "kline_count": len(klines)}

    # 找到选股日之后的 K 线(严格大于 pick_date)
    post_klines = [k for k in klines if k["date"] > pick_date]
    if not post_klines:
        return {"code": code, "error": "无选股后数据", "kline_count": len(klines)}

    base_price = post_klines[0]["open"]  # 次日开盘价
    base_date = post_klines[0]["date"]
    if base_price <= 0:
        # fallback: 用前一日收盘
        pre_klines = [k for k in klines if k["date"] <= pick_date]
        if pre_klines:
            base_price = pre_klines[-1]["close"]
        if base_price <= 0:
            return {"code": code, "error": "基准价异常", "kline_count": len(klines)}

    returns = {}
    for d in [1, 3, 5, 10, 20]:
        if d <= len(post_klines):
            close = post_klines[d - 1]["close"]
            returns[f"T+{d}"] = round((close / base_price - 1) * 100, 2)

    # 区间最高/最低
    highs = [k["high"] for k in post_klines]
    lows = [k["low"] for k in post_klines]
    max_ret = round((max(highs) / base_price - 1) * 100, 2) if highs else 0
    min_ret = round((min(lows) / base_price - 1) * 100, 2) if lows else 0

    return {
        "code":        code,
        "base_price":  round(base_price, 3),
        "base_date":   base_date,
        "returns":     returns,
        "max_return":  max_ret,
        "min_return":  min_ret,
        "kline_count": len(post_klines),
    }


def fetch_hs300_benchmark(pick_date: str, max_days: int = 25) -> dict:
    """拉取沪深 300 在同一时间窗口的收益(作为超额收益基准)"""
    start = (datetime.strptime(pick_date, "%Y-%m-%d") - timedelta(days=5)).strftime("%Y-%m-%d")
    end = (datetime.strptime(pick_date, "%Y-%m-%d") + timedelta(days=max_days + 15)).strftime("%Y-%m-%d")

    klines = tencent_daily_kline("sh000300", start_date=start, end_date=end, adjust="")
    post = [k for k in klines if k["date"] > pick_date]
    if not post:
        return {}

    base = post[0]["open"]
    if base <= 0:
        return {}

    returns = {}
    for d in [1, 3, 5, 10, 20]:
        if d <= len(post):
            close = post[d - 1]["close"]
            returns[f"T+{d}"] = round((close / base - 1) * 100, 2)
    return returns


def run_tracking(days: int = 30) -> list[dict]:
    """执行全量追踪"""
    TRACK_DIR.mkdir(parents=True, exist_ok=True)
    picks = load_historical_picks(days)
    if not picks:
        print("⚠ 无历史选股记录,跳过追踪")
        return []

    # 去重:同一 code+date 只追踪一次
    seen = set()
    unique_picks = []
    for p in picks:
        key = (p["code"], p["date"])
        if key not in seen:
            seen.add(key)
            unique_picks.append(p)
    print(f"去重后 {len(unique_picks)} 条唯一选股记录")

    # 拉取沪深 300 基准(按 pick_date 缓存)
    hs300_cache: dict[str, dict] = {}
    pick_dates = sorted(set(p["date"] for p in unique_picks))

    results = []
    total = len(unique_picks)
    for i, p in enumerate(unique_picks):
        # 拉个股表现
        perf = fetch_post_pick_performance(p["code"], p["date"])
        if "error" in perf:
            continue

        # 拉沪深 300 基准
        if p["date"] not in hs300_cache:
            hs300_cache[p["date"]] = fetch_hs300_benchmark(p["date"])
        hs300_ret = hs300_cache.get(p["date"], {})

        # 计算超额收益(T+5)
        t5_stock = perf["returns"].get("T+5")
        t5_hs300 = hs300_ret.get("T+5")
        excess_t5 = round(t5_stock - t5_hs300, 2) if t5_stock is not None and t5_hs300 is not None else None

        results.append({
            **p,
            **perf,
            "hs300_returns": hs300_ret,
            "excess_t5": excess_t5,
        })

        if (i + 1) % 10 == 0 or (i + 1) == total:
            print(f"  进度: {i+1}/{total} (有效 {len(results)})")
        # 避免请求过快
        if (i + 1) % 5 == 0:
            import time
            time.sleep(0.5)

    # 保存
    out = TRACK_DIR / f"tracking_{datetime.now().strftime('%Y%m%d')}.json"
    out.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ 追踪完成: {len(results)} 条有效记录 → {out}")
    return results


# ── CLI ──
def main():
    parser = argparse.ArgumentParser(description="选股后表现追踪")
    parser.add_argument("--days", type=int, default=30, help="回溯天数(默认 30)")
    args = parser.parse_args()
    run_tracking(args.days)


if __name__ == "__main__":
    main()
