"""
us_market_fetcher.py — 拉美股 5 指数隔夜 + 7 巨头 + 半导体 + 中概
写入: /workspace/daily_picks/YYYY-MM-DD/us_market.json
"""
import sys, json
from pathlib import Path
from datetime import date
sys.path.insert(0, str(Path(__file__).parent))
from _common import tencent_quote, save_json, DAILY_DIR, log

# 美股 5 指数 + 7 巨头 + 半导体 + 中概
US_TICKERS = [
    # 5 大指数
    ("usNDX",  "纳斯达克100"),
    ("usIXIC", "纳斯达克综合"),
    ("usINX",  "标普500"),
    ("usDJI",  "道琼斯"),
    ("usSOX",  "费城半导体"),
    # 七巨头
    ("usAAPL", "苹果"),
    ("usMSFT", "微软"),
    ("usNVDA", "英伟达"),
    ("usGOOG", "谷歌"),
    ("usAMZN", "亚马逊"),
    ("usMETA", "Meta"),
    ("usTSLA", "特斯拉"),
    # 半导体
    ("usAMD",  "AMD"),
    ("usAVGO", "博通"),
    ("usTSM",  "台积电"),
    ("usMU",   "美光"),
    ("usASML", "阿斯麦"),
    # 中概
    ("usBABA", "阿里巴巴"),
    ("usPDD",  "拼多多"),
    ("usJD",   "京东"),
    ("usBIDU", "百度"),
    ("usNIO",  "蔚来"),
    ("usXPEV", "小鹏"),
    ("usLI",   "理想"),
    # VIX / 美元
    ("usVIX",  "VIX恐慌指数"),
    ("usDXY",  "美元指数"),
    ("usTNX",  "美10年债"),
]

def main():
    today = date.today().strftime("%Y-%m-%d")
    out_dir = DAILY_DIR / today
    out_dir.mkdir(parents=True, exist_ok=True)

    log(f"拉 {len(US_TICKERS)} 个美股代码(隔夜数据)…")
    codes = [c for c, _ in US_TICKERS]
    quotes = tencent_quote(codes)

    rows = []
    for code, name in US_TICKERS:
        q = quotes.get(code)
        if not q:
            rows.append({"code": code, "name": name, "err": "no_data"})
            continue
        rows.append({
            "code": code,
            "name": q["name"] or name,
            "price": q["price"],
            "change_pct": q["change_pct"],
            "change_amt": q["change_amt"],
            "open": q["open"],
            "high": q["high"],
            "low": q["low"],
        })

    # 拆分类
    def section(rows, code):
        return [r for r in rows if r.get("code") == code]

    ndx  = next((r for r in rows if r.get("code") == "usNDX"), {})
    ixic = next((r for r in rows if r.get("code") == "usIXIC"), {})
    spx  = next((r for r in rows if r.get("code") == "usINX"), {})
    dji  = next((r for r in rows if r.get("code") == "usDJI"), {})
    sox  = next((r for r in rows if r.get("code") == "usSOX"), {})

    data = {
        "date": today,
        "summary": {
            "NDX":  ndx.get("change_pct", 0),
            "IXIC": ixic.get("change_pct", 0),
            "SPX":  spx.get("change_pct", 0),
            "DJI":  dji.get("change_pct", 0),
            "SOX":  sox.get("change_pct", 0),
        },
        "indices":   rows[:5],   # 5 大指数
        "magnificent7": [r for r in rows if r.get("code") in
                         ["usAAPL","usMSFT","usNVDA","usGOOG","usAMZN","usMETA","usTSLA"]],
        "semis":     [r for r in rows if r.get("code") in
                      ["usAMD","usAVGO","usTSM","usMU","usASML","usNVDA"]],
        "china_concept": [r for r in rows if r.get("code") in
                          ["usBABA","usPDD","usJD","usBIDU","usNIO","usXPEV","usLI"]],
        "all":       rows,
    }

    out = out_dir / "us_market.json"
    save_json(out, data)
    log(f"✅ 写入 {out}")
    print(json.dumps(data["summary"], ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
