"""
strategy_holdings_tracker.py — 159941(广发纳指100ETF)持仓跟踪
计算:现价 / 涨跌 / 当日盈亏 / 累计盈亏(对比成本) / 对比美股隔夜
写入: /workspace/daily_picks/YYYY-MM-DD/159941-tracker.json
"""
import sys, json, argparse
from pathlib import Path
from datetime import date
sys.path.insert(0, str(Path(__file__).parent))
from _common import tencent_quote, save_json, load_json, DAILY_DIR, log

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--code", default="159941")
    parser.add_argument("--shares", type=int, required=True, help="持仓股数")
    parser.add_argument("--cost",  type=float, required=True, help="平均成本价")
    parser.add_argument("--date",  default=None, help="日期(默认今天)")
    args = parser.parse_args()

    today = args.date or date.today().strftime("%Y-%m-%d")
    out_dir = DAILY_DIR / today
    out_dir.mkdir(parents=True, exist_ok=True)

    log(f"拉 {args.code} 实时行情 + 持仓计算(shares={args.shares} cost={args.cost})…")
    q = tencent_quote([args.code]).get(args.code)
    if not q:
        log(f"❌ 拉不到 {args.code} 行情")
        sys.exit(1)

    # 持仓计算
    price = q["price"]
    last_close = q["last_close"]
    cost = args.cost
    shares = args.shares
    market_value = price * shares
    cost_total = cost * shares
    cum_pnl = (price - cost) * shares
    cum_pnl_pct = (price / cost - 1) * 100 if cost else 0
    daily_pnl = (price - last_close) * shares
    daily_pnl_pct = (price / last_close - 1) * 100 if last_close else 0

    # 美股隔夜关联(读上一步的 us_market.json)
    us_data = load_json(out_dir / "us_market.json")
    ndx_change = us_data["summary"]["NDX"] if us_data else None
    sox_change = us_data["summary"]["SOX"] if us_data else None

    data = {
        "date": today,
        "code": args.code,
        "name": q["name"],
        "quote": {
            "price":       price,
            "open":        q["open"],
            "high":        q["high"],
            "low":         q["low"],
            "last_close":  last_close,
            "change_amt":  q["change_amt"],
            "change_pct":  q["change_pct"],
            "turnover_pct":q["turnover_pct"],
            "amount_wan":  q["amount_wan"],
            "pe_ttm":      q["pe_ttm"],
            "pb":          q["pb"],
            "mcap_yi":     q["mcap_yi"],
        },
        "holdings": {
            "shares":          shares,
            "cost":            cost,
            "market_value":    round(market_value, 2),
            "cost_total":      round(cost_total, 2),
            "daily_pnl":       round(daily_pnl, 2),
            "daily_pnl_pct":   round(daily_pnl_pct, 2),
            "cum_pnl":         round(cum_pnl, 2),
            "cum_pnl_pct":     round(cum_pnl_pct, 2),
        },
        "us_overnight": {
            "NDX_change_pct": ndx_change,
            "SOX_change_pct": sox_change,
            "narrative": (
                f"美股纳指隔夜 {ndx_change:+.2f}%,费半 {sox_change:+.2f}%;"
                f"今日 ETF 跟涨/跌 {q['change_pct']:+.2f}%,关联度观察中"
                if ndx_change is not None else "无美股数据"
            )
        },
    }

    out = out_dir / "159941-tracker.json"
    save_json(out, data)
    log(f"✅ 写入 {out}")
    print(json.dumps(data, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
