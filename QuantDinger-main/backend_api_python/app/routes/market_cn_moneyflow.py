"""
A 股日度资金流向 API.

数据源:
  - Tier 1: AKShare `stock_individual_fund_flow` (东方财富, 免费)
  - Tier 2: AKShare `stock_zh_a_individual_fund_flow` (新浪, 备用)

返回字段 (单位:万元):
  date          交易日期 (YYYY-MM-DD)
  close         收盘价
  change_pct    涨跌幅 (%)
  main_net      主力净流入 (超大单+大单)
  super_net     特大单净流入
  big_net       大单净流入
  mid_net       中单净流入
  small_net     小单净流入
  total_net     全单净流入 (主力+中单+小单)
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from flask import jsonify, request

from app.data_sources.tencent import normalize_cn_code
from app.openapi.blueprint import HumanBlueprint as Blueprint
from app.utils.cache import CacheManager
from app.utils.logger import get_logger

logger = get_logger(__name__)

moneyflow_blp = Blueprint("cn-moneyflow", __name__, description="A 股日度资金流向")
_cache = CacheManager()
_CACHE_TTL_SEC = 1800  # 30 分钟


def _to_wan(value: Any) -> Optional[float]:
    """AKShare 返回的金额单位是元;我们转成万元(保留 1 位小数)。"""
    if value is None:
        return None
    try:
        f = float(value)
    except (TypeError, ValueError):
        return None
    if abs(f) > 1e12:
        return None
    return round(f / 10000.0, 2)


def _to_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _strip_prefix(symbol: str) -> str:
    """把 sh600519 / 600519.SH 转成 600519(给 AKShare 用)。"""
    s = (symbol or "").strip().upper()
    for p in ("SH", "SZ", "BJ"):
        if s.startswith(p):
            s = s[len(p):]
            break
    for suf in (".SH", ".SZ", ".SS", ".BJ"):
        if s.endswith(suf):
            s = s[:-len(suf)]
            break
    return s


def _fetch_akshare_moneyflow(symbol: str, days: int) -> Optional[List[Dict[str, Any]]]:
    """调用 AKShare 拉单只股票的资金流(东方财富)。"""
    code = _strip_prefix(symbol)
    if not code.isdigit() or len(code) != 6:
        return None
    market = "sh" if code.startswith(("6", "9")) else "sz"

    try:
        import akshare as ak  # type: ignore
    except Exception as exc:
        logger.warning("akshare not installed: %s", exc)
        return None

    try:
        df = ak.stock_individual_fund_flow(stock=code, market=market)
    except Exception as exc:
        logger.warning("ak.stock_individual_fund_flow failed: %s", exc)
        return None

    if df is None or len(df) == 0:
        return None

    col_date = next((c for c in df.columns if "日期" in c), None)
    if col_date is None:
        return None

    df = df.head(days).iloc[::-1]  # 翻成正序

    out: List[Dict[str, Any]] = []
    for _, row in df.iterrows():
        main = _to_wan(row.get("主力净流入-净额"))
        mid = _to_wan(row.get("中单净流入-净额"))
        small = _to_wan(row.get("小单净流入-净额"))
        item: Dict[str, Any] = {
            "date": str(row[col_date])[:10],
            "close": _to_float(row.get("收盘价")),
            "change_pct": _to_float(row.get("涨跌幅")),
            "main_net": main,
            "super_net": _to_wan(row.get("超大单净流入-净额")),
            "big_net": _to_wan(row.get("大单净流入-净额")),
            "mid_net": mid,
            "small_net": small,
        }
        if main is not None and mid is not None and small is not None:
            item["total_net"] = round(main + mid + small, 2)
        else:
            item["total_net"] = None
        out.append(item)
    return out


@moneyflow_blp.route("/cn-moneyflow", methods=["GET"])
def get_cn_moneyflow():
    """A 股日度资金流向(主力/特大/大/中/小单)。"""
    try:
        symbol = (request.args.get("symbol") or "").strip()
        if not symbol:
            return jsonify({
                "code": 0, "msg": "Missing symbol parameter", "data": None,
            }), 400

        days = int(request.args.get("days") or 30)
        days = max(1, min(days, 365))

        code_norm = normalize_cn_code(symbol)
        cache_key = f"cn-moneyflow:{code_norm}:{days}"
        cached = _cache.get(cache_key)
        if cached:
            return jsonify({"code": 1, "msg": "success (cached)", "data": cached})

        rows = _fetch_akshare_moneyflow(code_norm, days)
        if not rows:
            return jsonify({
                "code": 0,
                "msg": "No moneyflow data found (akshare may be unavailable or symbol invalid)",
                "data": None,
            }), 404

        _cache.set(cache_key, rows, _CACHE_TTL_SEC)
        return jsonify({
            "code": 1,
            "msg": "success",
            "data": {
                "symbol": code_norm,
                "count": len(rows),
                "rows": rows,
            },
        })
    except Exception as exc:
        logger.error("cn-moneyflow failed: %s", exc, exc_info=True)
        return jsonify({
            "code": 0,
            "msg": f"Failed to fetch moneyflow: {exc}",
            "data": None,
        }), 500
