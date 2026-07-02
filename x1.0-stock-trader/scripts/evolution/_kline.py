"""
_kline.py — 腾讯日 K 线拉取(前复权)

供 backtest_tracker 使用,拉取指定股票的日 K 线数据。
API: https://web.ifzq.gtimg.cn/appstock/app/fqkline/get
"""
from __future__ import annotations
import json, urllib.request, time
from pathlib import Path

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"


def tencent_daily_kline(
    code: str,
    start_date: str | None = None,
    end_date: str | None = None,
    count: int = 40,
    adjust: str = "qfq",
) -> list[dict]:
    """拉取日 K 线(前复权)

    Args:
        code:       6 位 A 股代码,如 "000001" / "600519"
        start_date: 起始日期 "YYYY-MM-DD"(可选)
        end_date:   截止日期 "YYYY-MM-DD"(可选)
        count:      拉取根数(当不指定日期时使用)
        adjust:     "qfq" 前复权 / "hfq" 后复权 / "" 不复权

    Returns:
        [{"date": "2026-06-20", "open": 10.5, "close": 10.8,
          "high": 10.9, "low": 10.3, "volume": 123456, "amount": 1300000}, ...]
    """
    # 构建腾讯代码前缀
    if code.startswith(("sh", "sz", "bj")):
        prefixed = code
    elif code.startswith(("6", "9")):
        prefixed = f"sh{code}"
    elif code.startswith("8"):
        prefixed = f"bj{code}"
    else:
        prefixed = f"sz{code}"

    # 构建日期参数: API 要求 6 段 param=code,day,start,end,count,adjust
    # (start/end 可为空,但占位必须保留,否则会返回 "param error")
    if start_date and end_date:
        date_param = f"{start_date},{end_date},{count}"
    else:
        date_param = f",,{count}"

    url = (
        f"https://web.ifzq.gtimg.cn/appstock/app/fqkline/get"
        f"?param={prefixed},day,{date_param},{adjust}"
    )
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        resp = urllib.request.urlopen(req, timeout=15)
        raw = json.loads(resp.read())
    except Exception as e:
        print(f"  ⚠ kline fetch failed for {code}: {e}")
        return []

    # 解析: data.{prefixed}.qfqday 或 data.{prefixed}.day
    # 注意: 无数据时 API 返回 data: [](list),有数据时返回 data: {prefixed: {...}}(dict)
    data_field = raw.get("data", {})
    if isinstance(data_field, list) or not isinstance(data_field, dict):
        # API 返回空 list(无数据) — 直接返回空
        return []
    stock_data = data_field.get(prefixed, {})
    if not isinstance(stock_data, dict):
        return []
    klines = stock_data.get(f"{adjust}day") or stock_data.get("day") or []

    out = []
    for k in klines:
        # 标准格式: ["2026-06-20", "10.50", "10.80", "10.90", "10.30", "123456"]
        # 部分股票会多一个 amount 字段(数字)或 dict 元数据,需稳健解析
        if len(k) < 6:
            continue
        try:
            date  = k[0]
            open_  = float(k[1])
            close = float(k[2])
            high  = float(k[3])
            low   = float(k[4])
            vol   = float(k[5]) if k[5] else 0
            # amount 字段可能缺失、为字符串、或为 dict(部分新版 API)
            amt = 0.0
            if len(k) >= 7 and isinstance(k[6], (int, float, str)):
                try:
                    amt = float(k[6])
                except (ValueError, TypeError):
                    amt = 0.0
            out.append({
                "date":   date,
                "open":   open_,
                "close":  close,
                "high":   high,
                "low":    low,
                "volume": vol,
                "amount": amt,
            })
        except (ValueError, IndexError, TypeError):
            continue
    return out


def fetch_index_kline(index_code: str = "sh000300", count: int = 40) -> list[dict]:
    """拉取指数日 K 线(用于计算沪深 300 基准收益)"""
    return tencent_daily_kline(index_code, count=count, adjust="")


# ── 自测 ──
if __name__ == "__main__":
    print("=== 测试 tencent_daily_kline ===")
    klines = tencent_daily_kline("000001", count=5)
    for k in klines:
        print(f"  {k['date']} O={k['open']:.2f} C={k['close']:.2f} H={k['high']:.2f} L={k['low']:.2f}")

    print("\n=== 测试 fetch_index_kline (沪深300) ===")
    idx = fetch_index_kline("sh000300", count=5)
    for k in idx:
        print(f"  {k['date']} C={k['close']:.2f}")
