"""
_common.py — 公共基础: a-stock-data 工具函数 + 输出目录
所有 daily 脚本都从这里 import。
"""
from __future__ import annotations
import json, sys, time, random, urllib.request
from pathlib import Path
from datetime import datetime, date

# ── 路径 ──
WORKSPACE = Path("/workspace")
SCRIPTS_DIR = WORKSPACE / "scripts"
DAILY_DIR = WORKSPACE / "daily_picks"
DAILY_DIR.mkdir(parents=True, exist_ok=True)

# ── 用户 UA(避免被东财风控)─
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"

# ── 东财防封:全局节流 + Keep-Alive ──
EM_SESSION_HEADERS = {"User-Agent": UA}
EM_MIN_INTERVAL = 1.0
_em_last_call = [0.0]

def em_throttle():
    """东财请求前 sleep(最少 1s + 随机抖动)"""
    wait = EM_MIN_INTERVAL - (time.time() - _em_last_call[0])
    if wait > 0:
        time.sleep(wait + random.uniform(0.1, 0.5))

# ── 腾讯财经(不封IP)─
def tencent_quote(codes: list[str]) -> dict[str, dict]:
    """批量拉腾讯财经行情(A 股 / 指数 / ETF / 美股)
    返回 {code: {name, price, last_close, open, change_pct, change_amt,
                  high, low, turnover_pct, pe_ttm, pb, mcap_yi}}
    """
    if isinstance(codes, str):
        codes = [codes]
    prefixed = []
    for c in codes:
        c = c.strip()
        if not c:
            continue
        low = c.lower()
        if low.startswith("us") or low.startswith("us."):
            # 美股(腾讯要求无点号: usNDX / usAAPL)
            prefixed.append(low.replace("us.", "us").lower())
        elif c.startswith(("6", "9")):
            prefixed.append(f"sh{c}")
        elif c.startswith("8"):
            prefixed.append(f"bj{c}")
        else:
            prefixed.append(f"sz{c}")
    if not prefixed:
        return {}
    url = "https://qt.gtimg.cn/q=" + ",".join(prefixed)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    resp = urllib.request.urlopen(req, timeout=10)
    data = resp.read().decode("gbk")

    out = {}
    for line in data.strip().split(";"):
        if "=" not in line or '"' not in line:
            continue
        key = line.split("=")[0].split("_")[-1]
        vals = line.split('"')[1].split("~")
        if len(vals) < 50:
            continue
        # 提取 6 位代码(去掉 sh/sz/bj 前缀,us 保持原样)
        code = key[2:] if key[:2] in ("sh", "sz", "bj") else key
        out[code] = {
            "name":         vals[1],
            "price":        float(vals[3])  if vals[3]  else 0,
            "last_close":   float(vals[4])  if vals[4]  else 0,
            "open":         float(vals[5])  if vals[5]  else 0,
            "change_amt":   float(vals[31]) if vals[31] else 0,
            "change_pct":   float(vals[32]) if vals[32] else 0,
            "high":         float(vals[33]) if vals[33] else 0,
            "low":          float(vals[34]) if vals[34] else 0,
            "amount_wan":   float(vals[37]) if vals[37] else 0,
            "turnover_pct": float(vals[38]) if vals[38] else 0,
            "pe_ttm":       float(vals[39]) if vals[39] else 0,
            "amplitude_pct":float(vals[43]) if vals[43] else 0,
            "mcap_yi":      float(vals[44]) if vals[44] else 0,
            "float_mcap_yi":float(vals[45]) if vals[45] else 0,
            "pb":           float(vals[46]) if vals[46] else 0,
            "limit_up":     float(vals[47]) if vals[47] else 0,
            "limit_down":   float(vals[48]) if vals[48] else 0,
            "vol_ratio":    float(vals[49]) if vals[49] else 0,
        }
    return out

# ── 东财全球资讯(7×24)─
def eastmoney_global_news(page_size: int = 50) -> list[dict]:
    import uuid
    url = "https://np-weblist.eastmoney.com/comm/web/getFastNewsList"
    params = (
        "?client=web&biz=web_724&fastColumn=102&sortEnd="
        f"&pageSize={page_size}&req_trace={uuid.uuid4()}"
    )
    em_throttle()
    req = urllib.request.Request(url + params, headers={
        "User-Agent": UA, "Referer": "https://kuaixun.eastmoney.com/"
    })
    import re
    d = json.loads(urllib.request.urlopen(req, timeout=10).read())
    out = []
    for it in d.get("data", {}).get("fastNewsList", []):
        out.append({
            "title": it.get("title", ""),
            "summary": re.sub(r"<[^>]+>", "", it.get("summary", ""))[:300],
            "time": it.get("showTime", ""),
        })
    return out

# ── 同花顺热点(题材归因,零鉴权 73ms)─
def ths_hot_reason(date_str: str | None = None) -> list[dict]:
    from urllib.parse import quote
    if date_str is None:
        date_str = date.today().strftime("%Y-%m-%d")
    url = (
        f"http://zx.10jqka.com.cn/event/api/getharden/"
        f"date/{date_str}/orderby/date/orderway/desc/charset/GBK/"
    )
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    d = json.loads(urllib.request.urlopen(req, timeout=10).read())
    rows = []
    for r in d.get("data") or []:
        rows.append({
            "code": r.get("code", ""),
            "name": r.get("name", ""),
            "reason": r.get("reason", ""),
            "close": r.get("close", 0),
            "change_pct": r.get("zhangfu", 0),
            "turnover_pct": r.get("huanshou", 0),
            "amount_yi": (r.get("chengjiaoe", 0) or 0) / 1e8,
        })
    return rows

# ── 个股资金流(120 日)─
def stock_fund_flow_120d(code: str) -> list[dict]:
    market = 1 if code.startswith("6") else 0
    url = "https://push2his.eastmoney.com/api/qt/stock/fflow/daykline/get"
    params = {
        "secid": f"{market}.{code}",
        "fields1": "f1,f2,f3,f7",
        "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63,f64,f65",
        "lmt": "120",
    }
    em_throttle()
    req = urllib.request.Request(url + "?" + "&".join(f"{k}={v}" for k, v in params.items()),
                                  headers={"User-Agent": UA, "Referer": "https://quote.eastmoney.com/"})
    d = json.loads(urllib.request.urlopen(req, timeout=15).read())
    rows = []
    for line in d.get("data", {}).get("klines", []):
        parts = line.split(",")
        if len(parts) >= 7:
            rows.append({
                "date": parts[0],
                "main_net": float(parts[1]) if parts[1] != "-" else 0,
            })
    return rows

# ── 行业板块排名(东财)─
def industry_top(top_n: int = 20) -> list[dict]:
    url = "https://push2.eastmoney.com/api/qt/clist/get"
    params = (
        "?pn=1&pz=100&po=1&np=1&fltt=2&invt=2&fs=m:90+t:2"
        "&fields=f2,f3,f4,f12,f13,f14,f104,f105,f128,f136,f140,f141,f207"
    )
    em_throttle()
    req = urllib.request.Request(url + params, headers={"User-Agent": UA})
    d = json.loads(urllib.request.urlopen(req, timeout=15).read())
    items = d.get("data", {}).get("diff", [])
    out = []
    for i, it in enumerate(items):
        out.append({
            "rank": i + 1,
            "name": it.get("f14", ""),
            "change_pct": it.get("f3", 0),
            "code": it.get("f12", ""),
            "up_count": it.get("f104", 0),
            "down_count": it.get("f105", 0),
            "leader": it.get("f140", ""),
        })
    return out[:top_n]

# ── 简单日志 ──
def log(msg: str):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}", file=sys.stderr, flush=True)

# ── 工具:从路径拿 json ──
def load_json(path: Path):
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))

def save_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
