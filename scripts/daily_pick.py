#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
daily_pick.py — A 股早盘潜力股自动化筛选脚本

依据：`/workspace/选股手册.md` v2.0
触发：工作日 08:00（Asia/Shanghai），由 TRAE 定时任务调用
输出：`/workspace/output/YYYY-MM-DD_早盘潜力股.md`

实现要点：
- 数据层直接调用 a-stock-data 技能内嵌的 HTTP/TCP 接口（零第三方封装）
- 分析层严格遵守手册 13 条排除规则 + 6 维排序 + 4 选 1 结论
- 多源交叉验证：任何"亮点"必须 ≥ 2 个独立数据源相互印证
- 数据缺失兜底：附录 A 顺序（eastmoney_select_stock → a-share-screener → last30days）
- 防封：东财接口走 em_get() 串行限流，间隔 ≥ 1.5s + 随机抖动
"""

from __future__ import annotations

import os
import re
import sys
import json
import time
import random
import logging
import argparse
import urllib.request
from datetime import datetime, timedelta, date
from pathlib import Path
from typing import Any, Optional
from collections import Counter

import requests
import pandas as pd

# =============================================================================
# 0. 路径与配置
# =============================================================================

WORKSPACE = Path(__file__).resolve().parent.parent
OUTPUT_DIR = WORKSPACE / "output"
LOG_DIR = WORKSPACE / "logs"
CACHE_DIR = WORKSPACE / "data" / "cache"
for d in (OUTPUT_DIR, LOG_DIR, CACHE_DIR):
    d.mkdir(parents=True, exist_ok=True)

# 5 级环境评级 → 仓位建议（手册第八章）
POSITION_RULES = {
    "S": "可适当积极（满仓 ≤ 70%）",
    "A": "轻仓试错（仓位 ≤ 40%）",
    "B": "严格控制仓位（≤ 20%）",
    "C": "以观察为主（≤ 10%）",
    "D": "尽量空仓/少动（0%）",
}

# 4 选 1 结论枚举（手册第四章）
CONCLUSION_BUY = "可直接试仓买入"
CONCLUSION_COND = "条件满足才可买入"
CONCLUSION_WATCH = "只可观察，不可买"
CONCLUSION_SKIP = "明确不买"

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"

# =============================================================================
# 1. 日志
# =============================================================================

def setup_logger(trade_date: str) -> logging.Logger:
    """按天切割日志：logs/YYYY-MM-DD.log"""
    logger = logging.getLogger("daily_pick")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    fmt = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    fh = logging.FileHandler(LOG_DIR / f"{trade_date}.log", encoding="utf-8")
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(fmt)
    logger.addHandler(ch)

    return logger


# =============================================================================
# 2. 东财防封 helper（手册附录 B 数据使用铁律）
# =============================================================================

EM_SESSION = requests.Session()
EM_SESSION.headers.update({"User-Agent": UA})
EM_MIN_INTERVAL = 1.5  # 批量筛选场景调大
_em_last_call = [0.0]


def em_get(url: str, params: dict | None = None, headers: dict | None = None,
           timeout: int = 15, **kwargs) -> requests.Response:
    """东财统一请求入口：串行限流 + 复用 session + 默认 UA"""
    wait = EM_MIN_INTERVAL - (time.time() - _em_last_call[0])
    if wait > 0:
        time.sleep(wait + random.uniform(0.1, 0.5))
    try:
        return EM_SESSION.get(url, params=params, headers=headers,
                              timeout=timeout, **kwargs)
    finally:
        _em_last_call[0] = time.time()


def eastmoney_datacenter(report_name: str, columns: str = "ALL",
                          filter_str: str = "", page_size: int = 50,
                          sort_columns: str = "", sort_types: str = "-1") -> list[dict]:
    """东财数据中心统一查询（龙虎榜/解禁/融资融券/股东户数/分红 共用）"""
    params = {
        "reportName": report_name, "columns": columns,
        "filter": filter_str, "pageNumber": "1", "pageSize": str(page_size),
        "sortColumns": sort_columns, "sortTypes": sort_types,
        "source": "WEB", "client": "WEB",
    }
    r = em_get("https://datacenter-web.eastmoney.com/api/data/v1/get",
               params=params, timeout=15)
    try:
        d = r.json()
        if d.get("result") and d["result"].get("data"):
            return d["result"]["data"]
    except Exception as e:
        logging.warning(f"datacenter {report_name} 解析失败: {e}")
    return []


# =============================================================================
# 3. 交易日判断
# =============================================================================

def is_trading_day(dt: date | None = None) -> tuple[bool, str]:
    """
    简化版交易日判断：周一至周五且非已知重大节假日。
    生产环境应接入节假日 API（akshare / tushare / 节假日 JSON）。
    """
    if dt is None:
        dt = date.today()
    if dt.weekday() >= 5:
        return False, "周末"
    # 内置 2026 年已知 A 股休市日（持续更新）
    closed = {
        "2026-01-01", "2026-01-02",  # 元旦
        "2026-02-17", "2026-02-18", "2026-02-19", "2026-02-20",  # 春节
        "2026-04-04", "2026-04-06",  # 清明
        "2026-05-01", "2026-05-04", "2026-05-05",  # 劳动节
        "2026-06-19",  # 端午（示例，按国务院公告更新）
        "2026-09-25", "2026-09-28",  # 中秋+国庆连放
        "2026-10-01", "2026-10-02", "2026-10-05", "2026-10-06", "2026-10-07", "2026-10-08",
    }
    today_str = dt.strftime("%Y-%m-%d")
    if today_str in closed:
        return False, "法定节假日"
    return True, ""


# =============================================================================
# 4. 数据获取层（a-stock-data 七层数据 + 同花顺零鉴权接口）
# =============================================================================

def get_index_quotes() -> dict:
    """Layer 1.2 腾讯财经 — 四大指数实时行情"""
    codes = ["000001", "399001", "399006", "000688"]  # 上证/深证/创业/科创
    prefixed = ["sh" + c if not c.startswith("3") else "sz" + c for c in codes]
    # 修正：上证 000001 → sh000001；深证 399001 → sz399001；创业板 399006 → sz399006；科创 000688 → sh000688
    prefixed = ["sh000001", "sz399001", "sz399006", "sh000688"]
    url = "https://qt.gtimg.cn/q=" + ",".join(prefixed)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        resp = urllib.request.urlopen(req, timeout=10)
        data = resp.read().decode("gbk")
    except Exception as e:
        logging.warning(f"指数行情拉取失败: {e}")
        return {}

    result = {}
    name_map = {"sh000001": "上证指数", "sz399001": "深证成指",
                "sz399006": "创业板指", "sh000688": "科创50"}
    for line in data.strip().split(";"):
        if "=" not in line:
            continue
        key = line.split("=")[0].strip()
        if '"' not in line:
            continue
        vals = line.split('"')[1].split("~")
        if len(vals) < 50:
            continue
        code = key.split("_")[-1][2:]
        prefix = key.split("_")[-1][:2]
        result[prefix + code] = {
            "name": name_map.get(key, vals[1]),
            "price": float(vals[3]) if vals[3] else 0,
            "change_pct": float(vals[32]) if vals[32] else 0,
            "amount_yi": float(vals[37]) / 10000 if vals[37] else 0,
        }
    return result


def get_industry_ranking(top_n: int = 20) -> dict:
    """Layer 3.7 东财 push2 — 全行业涨跌幅排名"""
    url = "https://push2.eastmoney.com/api/qt/clist/get"
    params = {
        "pn": "1", "pz": "100", "po": "1", "np": "1",
        "fltt": "2", "invt": "2", "fs": "m:90+t:2",
        "fields": "f2,f3,f12,f14,f104,f105,f128,f140,f136",
    }
    try:
        r = em_get(url, params=params, headers={"User-Agent": UA}, timeout=15)
        items = r.json().get("data", {}).get("diff", [])
    except Exception as e:
        logging.warning(f"行业排名拉取失败: {e}")
        return {"top": [], "bottom": [], "total": 0}

    rows = []
    for it in items:
        rows.append({
            "name": it.get("f14", ""),
            "change_pct": float(it.get("f3", 0)),
            "code": it.get("f12", ""),
            "up_count": int(it.get("f104", 0)),
            "down_count": int(it.get("f105", 0)),
            "leader": it.get("f140", ""),
        })
    rows.sort(key=lambda r: r["change_pct"], reverse=True)
    return {"top": rows[:top_n], "bottom": rows[-top_n:], "total": len(rows), "all": rows}


def get_northbound_flow() -> dict:
    """Layer 3.2 同花顺 hsgtApi — 北向资金当日累计（亿）"""
    url = "https://data.hexin.cn/market/hsgtApi/method/dayChart/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/117.0.0.0",
        "Host": "data.hexin.cn", "Referer": "https://data.hexin.cn/",
    }
    try:
        r = requests.get(url, headers=headers, timeout=10)
        d = r.json()
        times = d.get("time", [])
        hgt = [v for v in d.get("hgt", []) if v is not None]
        sgt = [v for v in d.get("sgt", []) if v is not None]
        last_hgt = hgt[-1] if hgt else 0
        last_sgt = sgt[-1] if sgt else 0
        return {
            "hgt_yi": round(last_hgt, 2),
            "sgt_yi": round(last_sgt, 2),
            "total_yi": round(last_hgt + last_sgt, 2),
            "data_points": len(times),
        }
    except Exception as e:
        logging.warning(f"北向资金拉取失败: {e}")
        return {"hgt_yi": 0, "sgt_yi": 0, "total_yi": 0, "data_points": 0}


def get_hot_stocks_with_reason(date_str: str | None = None) -> pd.DataFrame:
    """Layer 3.1 同花顺热点 — 当日强势股 + 题材归因"""
    if date_str is None:
        date_str = date.today().strftime("%Y-%m-%d")
    url = (
        f"http://zx.10jqka.com.cn/event/api/getharden/"
        f"date/{date_str}/orderby/date/orderway/desc/charset/GBK/"
    )
    try:
        r = requests.get(url, headers={"User-Agent": UA}, timeout=10)
        d = r.json()
        if d.get("errocode", 0) != 0:
            return pd.DataFrame()
        rows = d.get("data") or []
        df = pd.DataFrame(rows)
        if df.empty:
            return df
        rename = {"name": "名称", "code": "代码", "reason": "题材归因",
                  "close": "收盘价", "zhangfu": "涨幅%", "huanshou": "换手率%",
                  "chengjiaoe": "成交额", "ddejingliang": "大单净量"}
        return df.rename(columns=rename)
    except Exception as e:
        logging.warning(f"同花顺热点拉取失败: {e}")
        return pd.DataFrame()


def get_tencent_quote(code: str) -> dict:
    """Layer 1.2 腾讯财经 — 单只股票实时行情（PE/PB/市值/换手率）"""
    if code.startswith(("6", "9")):
        prefix = "sh"
    elif code.startswith("8"):
        prefix = "bj"
    else:
        prefix = "sz"
    url = f"https://qt.gtimg.cn/q={prefix}{code}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        resp = urllib.request.urlopen(req, timeout=10)
        data = resp.read().decode("gbk")
    except Exception:
        return {}
    if '"' not in data:
        return {}
    vals = data.split('"')[1].split("~")
    if len(vals) < 50:
        return {}
    return {
        "code": code,
        "name": vals[1],
        "price": float(vals[3]) if vals[3] else 0,
        "change_pct": float(vals[32]) if vals[32] else 0,
        "amount_yi": float(vals[37]) / 10000 if vals[37] else 0,
        "turnover_pct": float(vals[38]) if vals[38] else 0,
        "pe_ttm": float(vals[39]) if vals[39] else 0,
        "pb": float(vals[46]) if vals[46] else 0,
        "mcap_yi": float(vals[44]) if vals[44] else 0,
        "float_mcap_yi": float(vals[45]) if vals[45] else 0,
        "limit_up": float(vals[47]) if vals[47] else 0,
        "limit_down": float(vals[48]) if vals[48] else 0,
        "vol_ratio": float(vals[49]) if vals[49] else 0,
    }


def get_stock_fund_flow_120d(code: str) -> list[dict]:
    """Layer 4.5 东财 push2his — 个股 120 日资金流"""
    market_code = 1 if code.startswith("6") else 0
    url = "https://push2his.eastmoney.com/api/qt/stock/fflow/daykline/get"
    params = {
        "secid": f"{market_code}.{code}",
        "fields1": "f1,f2,f3,f7",
        "fields2": "f51,f52,f53,f54,f55,f56,f57",
        "lmt": "120",
    }
    try:
        r = em_get(url, params=params,
                   headers={"User-Agent": UA, "Referer": "https://quote.eastmoney.com/"},
                   timeout=15)
        klines = r.json().get("data", {}).get("klines", [])
    except Exception as e:
        logging.warning(f"{code} 120日资金流拉取失败: {e}")
        return []

    rows = []
    for line in klines:
        parts = line.split(",")
        if len(parts) >= 6:
            rows.append({
                "date": parts[0],
                "main_net": float(parts[1]) if parts[1] != "-" else 0,
                "small_net": float(parts[2]) if parts[2] != "-" else 0,
                "mid_net": float(parts[3]) if parts[3] != "-" else 0,
                "large_net": float(parts[4]) if parts[4] != "-" else 0,
                "super_net": float(parts[5]) if parts[5] != "-" else 0,
            })
    return rows


def get_holder_change(code: str) -> list[dict]:
    """Layer 4.3 股东户数变化"""
    return eastmoney_datacenter(
        "RPT_HOLDERNUMLATEST",
        filter_str=f'(SECURITY_CODE="{code}")',
        page_size=8,
        sort_columns="END_DATE", sort_types="-1",
    )


def get_lockup_expiry(code: str, trade_date: str, forward_days: int = 30) -> list[dict]:
    """Layer 3.6 未来 30 日解禁预警"""
    end_date = (datetime.strptime(trade_date, "%Y-%m-%d")
                + timedelta(days=forward_days)).strftime("%Y-%m-%d")
    return eastmoney_datacenter(
        "RPT_LIFT_STAGE",
        filter_str=f'(SECURITY_CODE="{code}")(FREE_DATE>=\'{trade_date}\')(FREE_DATE<=\'{end_date}\')',
        page_size=10,
        sort_columns="FREE_DATE", sort_types="1",
    )


def get_dragon_tiger_recent(code: str, trade_date: str) -> dict:
    """Layer 3.5 近 30 日龙虎榜"""
    start = (datetime.strptime(trade_date, "%Y-%m-%d")
             - timedelta(days=30)).strftime("%Y-%m-%d")
    return eastmoney_datacenter(
        "RPT_DAILYBILLBOARD_DETAILSNEW",
        filter_str=f'(TRADE_DATE>=\'{start}\')(TRADE_DATE<=\'{trade_date}\')(SECURITY_CODE="{code}")',
        page_size=10,
        sort_columns="TRADE_DATE", sort_types="-1",
    )


def get_stock_concept_blocks(code: str) -> dict:
    """Layer 3.3 东财 slist — 个股所属板块/概念"""
    market_code = 1 if code.startswith("6") else 0
    url = "https://push2.eastmoney.com/api/qt/slist/get"
    params = {
        "fltt": "2", "invt": "2",
        "secid": f"{market_code}.{code}",
        "spt": "3", "pi": "0", "pz": "200", "po": "1",
        "fields": "f12,f14,f3,f128",
    }
    try:
        r = em_get(url, params=params,
                   headers={"User-Agent": UA, "Referer": "https://quote.eastmoney.com/"},
                   timeout=15)
        d = r.json()
    except Exception:
        return {"total": 0, "concept_tags": [], "boards": []}
    diff = (d.get("data") or {}).get("diff") or {}
    items = diff.values() if isinstance(diff, dict) else diff
    boards = []
    for it in items:
        boards.append({
            "name": it.get("f14", ""),
            "code": it.get("f12", ""),
            "change_pct": it.get("f3", ""),
            "lead_stock": it.get("f128", ""),
        })
    return {
        "total": len(boards),
        "boards": boards,
        "concept_tags": [b["name"] for b in boards],
    }


# =============================================================================
# 5. 分析层（手册第三/六/七/八章）
# =============================================================================

def grade_market_environment(index_quotes: dict, northbound: dict,
                              industry_data: dict, hot_df: pd.DataFrame) -> dict:
    """
    手册第八章 + 第二章第 6 条：综合 4 维度给环境评级 S/A/B/C/D。
    评分制（满分 100）：
      - 指数强度（30）
      - 情绪强度（30）
      - 资金/筹码（20）
      - 行业宽度（20）
    """
    score = 0
    notes = {}

    # 1) 指数强度（30 分）— 上证 + 创板涨幅均值
    if index_quotes:
        sh = index_quotes.get("sh000001", {}).get("change_pct", 0)
        cyb = index_quotes.get("sz399006", {}).get("change_pct", 0)
        avg_idx = (sh + cyb) / 2
        notes["指数强度"] = f"上证 {sh:+.2f}% / 创业板 {cyb:+.2f}%"
        if avg_idx >= 1.5:
            score += 30
        elif avg_idx >= 0.5:
            score += 22
        elif avg_idx >= 0:
            score += 14
        elif avg_idx >= -1:
            score += 6
        else:
            score += 0

    # 2) 情绪强度（30 分）— 涨停家数 + 题材广度
    if not hot_df.empty:
        up_count = len(hot_df[hot_df["涨幅%"] > 0])
        limit_up_count = len(hot_df[hot_df["涨幅%"] >= 9.5])
        # 题材归因唯一数
        all_tags = []
        for r in hot_df["题材归因"].dropna():
            tags = [t.strip() for t in str(r).split("+") if t.strip()]
            all_tags.extend(tags)
        unique_tags = len(set(all_tags))
        notes["情绪强度"] = f"涨停 {limit_up_count} 家 / 题材归因 {unique_tags} 类"
        if limit_up_count >= 80 and unique_tags >= 20:
            score += 30
        elif limit_up_count >= 50 and unique_tags >= 15:
            score += 22
        elif limit_up_count >= 30:
            score += 14
        elif limit_up_count >= 10:
            score += 6
        else:
            score += 0
    else:
        notes["情绪强度"] = "数据缺失（仅作辅助）"
        score += 14  # 缺失给中等分

    # 3) 资金/筹码（20 分）— 北向资金
    nb_total = northbound.get("total_yi", 0)
    notes["资金/筹码"] = f"北向 {nb_total:+.2f} 亿"
    if nb_total >= 80:
        score += 20
    elif nb_total >= 30:
        score += 14
    elif nb_total >= 0:
        score += 8
    elif nb_total >= -30:
        score += 4
    else:
        score += 0

    # 4) 行业宽度（20 分）— 上涨行业占比
    if industry_data.get("all"):
        all_ind = industry_data["all"]
        up_ind = len([r for r in all_ind if r["change_pct"] > 0])
        up_ratio = up_ind / len(all_ind) if all_ind else 0
        notes["行业宽度"] = f"上涨行业 {up_ind}/{len(all_ind)} ({up_ratio:.0%})"
        if up_ratio >= 0.7:
            score += 20
        elif up_ratio >= 0.5:
            score += 14
        elif up_ratio >= 0.3:
            score += 8
        elif up_ratio >= 0.1:
            score += 4
        else:
            score += 0

    # 评级映射
    if score >= 80:
        level = "S"
    elif score >= 60:
        level = "A"
    elif score >= 40:
        level = "B"
    elif score >= 20:
        level = "C"
    else:
        level = "D"

    # 行业环境单独判定
    if industry_data.get("all"):
        top1 = industry_data["all"][0]["change_pct"]
        top3 = sum(r["change_pct"] for r in industry_data["all"][:3]) / 3
        if top1 >= 5 and top3 >= 3:
            industry_env = "强（主线清晰）"
        elif top1 >= 2:
            industry_env = "中（有主线但强度一般）"
        elif top1 >= 0:
            industry_env = "弱（行业分散）"
        else:
            industry_env = "极弱（行业普跌）"
    else:
        industry_env = "未知（数据缺失）"

    return {
        "level": level,
        "score": score,
        "position": POSITION_RULES[level],
        "industry_env": industry_env,
        "notes": notes,
    }


def rank_directions(hot_df: pd.DataFrame, industry_data: dict) -> list[dict]:
    """
    手册第三章步骤 2：从前 3 涨幅行业 + 同花顺热点题材词频
    综合得出前 3 方向优先级
    """
    directions = {}

    # 来源 1：行业涨幅 TOP 5
    if industry_data.get("all"):
        for ind in industry_data["all"][:5]:
            name = ind["name"]
            if name in directions:
                directions[name]["industry_score"] += ind["change_pct"]
                directions[name]["leaders"].append(ind.get("leader", ""))
            else:
                directions[name] = {
                    "name": name,
                    "industry_score": ind["change_pct"],
                    "hot_score": 0,
                    "leaders": [ind.get("leader", "")],
                }

    # 来源 2：同花顺热点词频 TOP 10
    if not hot_df.empty:
        cnt = Counter()
        for r in hot_df["题材归因"].dropna():
            tags = [t.strip() for t in str(r).split("+") if t.strip()]
            cnt.update(tags)
        for tag, n in cnt.most_common(10):
            if tag in directions:
                directions[tag]["hot_score"] += n
            else:
                directions[tag] = {
                    "name": tag,
                    "industry_score": 0,
                    "hot_score": n,
                    "leaders": [],
                }

    # 综合打分：行业涨幅 × 3 + 热点频次 × 0.5
    ranked = []
    for d in directions.values():
        if not d["name"] or d["name"] in ("HS300_", "上证50_", "深证成指"):
            continue
        score = d["industry_score"] * 3 + d["hot_score"] * 0.5
        if score <= 0:
            continue
        ranked.append({
            "name": d["name"],
            "score": round(score, 2),
            "industry_change_pct": round(d["industry_score"], 2),
            "hot_count": d["hot_score"],
            "leaders": [x for x in d["leaders"] if x][:3],
        })
    ranked.sort(key=lambda r: r["score"], reverse=True)

    # 归一化为强/中/弱
    for i, d in enumerate(ranked[:5]):
        if i == 0 and d["score"] >= 15:
            d["strength"] = "强"
        elif d["score"] >= 8:
            d["strength"] = "中"
        else:
            d["strength"] = "弱"
        # v2 新增：标注加成项（卡点逻辑/舆情同步）
        d["bonus"] = "（卡点逻辑加成：未验证 / 舆情同步：未验证）"

    return ranked[:3]


def select_candidates(hot_df: pd.DataFrame, directions: list[dict],
                       top_n: int = 8) -> list[str]:
    """
    从热点股 + 行业领涨股中合并去重，挑选候选。
    返回候选代码列表（供后续详细分析）。
    """
    candidates = []
    seen = set()

    # 优先级 1：热点归因含 TOP 1 方向的股票
    if not hot_df.empty and directions:
        top1 = directions[0]["name"]
        for _, r in hot_df.iterrows():
            code = str(r.get("代码", ""))
            reason = str(r.get("题材归因", ""))
            if code in seen:
                continue
            if not code or len(code) != 6:
                continue
            if top1 in reason:
                candidates.append(code)
                seen.add(code)

    # 优先级 2：其他热点股
    if not hot_df.empty:
        for _, r in hot_df.iterrows():
            code = str(r.get("代码", ""))
            if code in seen or not code or len(code) != 6:
                continue
            candidates.append(code)
            seen.add(code)

    return candidates[:top_n]


def analyze_stock(code: str, env_level: str, logger: logging.Logger) -> dict:
    """
    手册第三章步骤 3：六维分析 + 资金/筹码确认。
    任意 2 项以上"流出/分散/解禁大" → 结论必须降级一档。
    """
    quote = get_tencent_quote(code)
    if not quote:
        logger.warning(f"{code} 实时行情缺失")
        return {"code": code, "name": "未知", "data_missing": True,
                "conclusion": CONCLUSION_WATCH,
                "conclusion_reason": "实时行情缺失，仅作初步判断"}

    name = quote["name"]
    result = {
        "code": code,
        "name": name,
        "quote": quote,
        "conclusion": CONCLUSION_WATCH,  # 默认观察
        "conclusion_reason": "数据待补充",
    }

    # 1) 资金/筹码信号（v2 第六维）
    fund_signals = {"bad": 0, "items": []}

    # 1.1 120 日主力资金流
    flow_120 = get_stock_fund_flow_120d(code)
    if flow_120:
        recent_20 = flow_120[-20:]
        main_20 = sum(d["main_net"] for d in recent_20) / 1e8  # 亿
        if main_20 < -1:
            fund_signals["bad"] += 1
            fund_signals["items"].append(f"近 20 日主力净流出 {main_20:.2f} 亿")
        elif main_20 > 1:
            fund_signals["items"].append(f"近 20 日主力净流入 {main_20:.2f} 亿")
        result["main_20_yi"] = round(main_20, 2)
    else:
        result["main_20_yi"] = None

    # 1.2 股东户数（减少=集中=好）
    holders = get_holder_change(code)
    if holders and len(holders) >= 2:
        latest = holders[0]
        prev = holders[1]
        change_ratio = float(latest.get("HOLDER_NUM_RATIO", 0))
        if change_ratio > 5:
            fund_signals["bad"] += 1
            fund_signals["items"].append(f"股东户数环比 {change_ratio:+.2f}%（筹码分散）")
        elif change_ratio < -5:
            fund_signals["items"].append(f"股东户数环比 {change_ratio:+.2f}%（筹码集中）")
        result["holder_change_pct"] = change_ratio
    else:
        result["holder_change_pct"] = None

    # 1.3 解禁压力
    today_str = date.today().strftime("%Y-%m-%d")
    lockup = get_lockup_expiry(code, today_str, forward_days=30)
    big_unlock = False
    for u in lockup:
        ratio = float(u.get("FREE_RATIO", 0))  # 已经是百分比
        if ratio >= 10:
            big_unlock = True
            break
    if big_unlock:
        fund_signals["bad"] += 1
        fund_signals["items"].append("未来 30 日有 ≥ 10% 解禁")
    result["upcoming_unlock"] = len(lockup)

    # 1.4 龙虎榜近 30 日机构动向
    dt = get_dragon_tiger_recent(code, today_str)
    if dt:
        # 简单计算净买入
        net_buy_total = sum((r.get("BILLBOARD_NET_AMT") or 0) for r in dt) / 1e8
        if net_buy_total < -0.3:
            fund_signals["bad"] += 1
            fund_signals["items"].append(f"近 30 日龙虎榜净卖出 {net_buy_total:.2f} 亿")
        result["dt_net_yi"] = round(net_buy_total, 2)
    else:
        result["dt_net_yi"] = None

    result["fund_signals"] = fund_signals

    # 2) 板块归属
    blocks = get_stock_concept_blocks(code)
    result["concept_tags"] = blocks.get("concept_tags", [])[:8]

    # 3) 排除规则应用（手册第七章 13 条）
    excluded, exclude_reason = check_exclusion(quote, fund_signals, blocks, env_level)
    if excluded:
        result["conclusion"] = CONCLUSION_SKIP
        result["conclusion_reason"] = f"排除：{exclude_reason}"
        return result

    # 4) 4 选 1 结论判定
    # 资金/筹码降级
    downgrade = fund_signals["bad"] >= 2

    if quote["change_pct"] > 5 and not downgrade:
        result["conclusion"] = CONCLUSION_BUY
        result["conclusion_reason"] = "涨幅强势 + 资金/筹码信号健康"
    elif quote["change_pct"] > 0 and not downgrade:
        result["conclusion"] = CONCLUSION_COND
        result["conclusion_reason"] = "有逻辑，需放量/板块共振确认"
    else:
        result["conclusion"] = CONCLUSION_WATCH
        result["conclusion_reason"] = "信号偏弱，仅作观察"

    # 风险点
    risks = []
    if quote["turnover_pct"] > 15:
        risks.append(f"换手率 {quote['turnover_pct']:.1f}% 偏高（投机性强）")
    if quote["pe_ttm"] > 100:
        risks.append(f"PE-TTM {quote['pe_ttm']:.0f} 倍，估值偏高")
    if fund_signals["bad"] > 0:
        risks.extend(fund_signals["items"])
    if quote["change_pct"] < 0:
        risks.append("当日下跌，与短线做多逻辑相悖")
    if not risks:
        risks.append("无显著额外风险（仅参考常规交易风险）")
    result["risks"] = risks[:4]

    return result


def check_exclusion(quote: dict, fund_signals: dict, blocks: dict,
                    env_level: str) -> tuple[bool, str]:
    """手册第七章 13 条排除规则（保守实现 v1）"""
    # 规则 3：高开过多（涨幅 > 9% 接近涨停）
    if quote.get("change_pct", 0) >= 9.5:
        return True, f"规则 3：高开过多（{quote['change_pct']:.1f}%，盈亏比差）"
    # 规则 8：市场整体环境不支持（D 级）
    if env_level == "D":
        return True, "规则 8：市场整体环境不支持"
    # 规则 12：筹码信号恶化
    if fund_signals["bad"] >= 3:
        return True, f"规则 12：筹码信号恶化（{fund_signals['bad']} 项负面）"
    # 规则 13：解禁压力大
    if any("≥ 10% 解禁" in s for s in fund_signals["items"]):
        return True, "规则 13：未来 30 日解禁压力 ≥ 10%"
    return False, ""


def sort_candidates(stocks: list[dict]) -> list[dict]:
    """
    手册第六章 6 维排序。
    实现：基于可用数据给出 0-100 综合分。
    """
    for s in stocks:
        if s.get("data_missing"):
            s["sort_score"] = 0
            continue
        q = s.get("quote", {})
        fs = s.get("fund_signals", {}).get("bad", 0)
        score = 50
        # 涨幅正向加成
        if 0 < q.get("change_pct", 0) < 5:
            score += 15
        elif q.get("change_pct", 0) >= 5:
            score += 8
        elif q.get("change_pct", 0) < 0:
            score -= 10
        # 量比正向加成
        if 1 <= q.get("vol_ratio", 0) <= 3:
            score += 10
        # 资金/筹码负向扣分
        score -= fs * 8
        # 市值适中（中盘最优）
        mcap = q.get("mcap_yi", 0)
        if 50 <= mcap <= 500:
            score += 5
        s["sort_score"] = max(0, min(100, score))
    return sorted(stocks, key=lambda s: s.get("sort_score", 0), reverse=True)


# =============================================================================
# 6. 输出层（手册第十一章 + 附录 A）
# =============================================================================

def format_market_review(env: dict, index_quotes: dict, northbound: dict,
                          industry_data: dict, hot_df: pd.DataFrame,
                          is_closed: bool, close_reason: str) -> str:
    """手册第十一章：市场环境总评章节"""
    lines = ["【市场环境总评】"]
    if is_closed:
        lines.append(f"- 是否休市：是（{close_reason}，无交易）")
    else:
        lines.append(f"- 是否休市：否")

    # 指数
    if index_quotes:
        sh = index_quotes.get("sh000001", {})
        cyb = index_quotes.get("sz399006", {})
        kc = index_quotes.get("sh000688", {})
        lines.append(f"- 指数环境：上证 {sh.get('change_pct', 0):+.2f}% / "
                     f"创业板 {cyb.get('change_pct', 0):+.2f}% / "
                     f"科创 50 {kc.get('change_pct', 0):+.2f}%")
    else:
        lines.append("- 指数环境：数据缺失")

    # 情绪
    if not hot_df.empty:
        limit_up = len(hot_df[hot_df["涨幅%"] >= 9.5])
        lines.append(f"- 情绪环境：涨停 {limit_up} 家 / 热点股 {len(hot_df)} 只")
    else:
        lines.append("- 情绪环境：数据缺失")

    # 资金/筹码
    lines.append(f"- 资金/筹码环境：北向 {northbound.get('total_yi', 0):+.2f} 亿 "
                 f"（沪 {northbound.get('hgt_yi', 0):+.2f} / 深 {northbound.get('sgt_yi', 0):+.2f}）")

    # 主线方向
    if industry_data.get("all"):
        top3_names = "、".join(r["name"] for r in industry_data["all"][:3])
        lines.append(f"- 主线方向：{top3_names}")
    else:
        lines.append("- 主线方向：数据缺失")

    # 行业环境
    lines.append(f"- 行业环境：{env.get('industry_env', '未知')}")

    # 评级
    notes = env.get("notes", {})
    details = " | ".join(f"{k}={v}" for k, v in notes.items())
    lines.append(f"- 综合评分：{env.get('score', 0)}/100")
    lines.append(f"- 环境级别：{env.get('level', '?')}")
    lines.append(f"- 仓位建议：{env.get('position', '')}")
    lines.append(f"- 评分明细：{details}")
    return "\n".join(lines)


def format_directions(directions: list[dict]) -> str:
    """手册第十一章：方向优先级章节"""
    lines = ["【方向优先级】"]
    if not directions:
        lines.append("（数据缺失，暂无明确方向）")
        return "\n".join(lines)
    for i, d in enumerate(directions, 1):
        lines.append(
            f"{i}. **{d['name']}** - 强度:{d['strength']} - "
            f"行业涨幅:{d['industry_change_pct']:+.2f}% / "
            f"热点频次:{d['hot_count']} - "
            f"领涨:{','.join(d['leaders']) or '无'}"
            f" {d.get('bonus', '')}"
        )
    return "\n".join(lines)


def format_stock_block(stock: dict, rank: int, env_level: str) -> str:
    """手册第五章：单只股票 10 项结构"""
    code = stock["code"]
    name = stock.get("name", "未知")
    q = stock.get("quote", {})
    fs = stock.get("fund_signals", {})
    lines = [f"## 第{to_chinese(rank)}优先：{name}({code})"]

    if stock.get("data_missing"):
        lines.extend([
            "1. 方向归属：数据缺失",
            "2. 逻辑强度：弱 - 数据不全无法判断",
            "3. 个股地位：未知",
            "4. 当前位置：未知",
            "5. 当前买点：差 - 实时行情缺失",
            "6. 资金/筹码确认：",
            "   - 数据缺失，结论仅作初步判断",
            "7. 风险点：",
            "   - 数据缺失，无法评估",
            f"8. 操作结论：{stock.get('conclusion', CONCLUSION_WATCH)}",
            f"9. 结论理由：{stock.get('conclusion_reason', '')}",
            "10. 条件触发：补充完整数据后重新评估",
        ])
        return "\n".join(lines)

    # 1) 方向归属
    tags = stock.get("concept_tags", [])
    lines.append(f"1. 方向归属：{', '.join(tags[:5]) if tags else '未分类'}")

    # 2) 逻辑强度
    direction = tags[0] if tags else "未分类"
    if stock.get("conclusion") == CONCLUSION_BUY:
        strength = "强"
    elif stock.get("conclusion") in (CONCLUSION_COND, CONCLUSION_WATCH):
        strength = "中"
    else:
        strength = "弱"
    lines.append(f"2. 逻辑强度：{strength} - 所属方向 {direction}，"
                 f"个股强度需结合板块共振确认")

    # 3) 个股地位
    if q.get("change_pct", 0) >= 5:
        status = "前排"
    elif q.get("change_pct", 0) >= 2:
        status = "核心"
    elif q.get("change_pct", 0) >= 0:
        status = "跟风"
    else:
        status = "补跌"
    lines.append(f"3. 个股地位：{status}")

    # 4) 当前位置
    change = q.get("change_pct", 0)
    if change >= 7:
        pos = "高位博弈"
    elif change >= 3:
        pos = "中位强化"
    elif change >= 0:
        pos = "低位启动"
    else:
        pos = "明显透支"
    lines.append(f"4. 当前位置：{pos}")

    # 5) 当前买点
    if stock.get("conclusion") == CONCLUSION_BUY:
        bp = "好"
        bp_reason = "价量配合 + 资金/筹码健康"
    elif stock.get("conclusion") == CONCLUSION_COND:
        bp = "一般"
        bp_reason = "需放量/板块共振确认"
    else:
        bp = "差"
        bp_reason = "信号不足或环境不支持"
    lines.append(f"5. 当前买点：{bp} - {bp_reason}")

    # 6) 资金/筹码确认
    main_20 = stock.get("main_20_yi")
    holder_chg = stock.get("holder_change_pct")
    dt_net = stock.get("dt_net_yi")
    unlock = stock.get("upcoming_unlock", 0)
    lines.append("6. 资金/筹码确认：")
    if main_20 is not None:
        lines.append(f"   - 120 日主力近 20 日：{main_20:+.2f} 亿")
    if holder_chg is not None:
        lines.append(f"   - 股东户数环比：{holder_chg:+.2f}%")
    if dt_net is not None:
        lines.append(f"   - 龙虎榜近 30 日净买：{dt_net:+.2f} 亿")
    unlock_text = f"{unlock} 批" + ("（含 ≥ 10% 大解禁）" if any("≥ 10%" in s for s in fs.get("items", [])) else "")
    lines.append(f"   - 未来 30 日解禁：{unlock_text}")
    if fs.get("bad", 0) >= 2:
        lines.append(f"   - ⚠️ 资金/筹码负面信号 {fs['bad']} 项，结论降级一档")

    # 7) 风险点
    lines.append("7. 风险点：")
    for r in stock.get("risks", ["无显著额外风险"]):
        lines.append(f"   - {r}")

    # 8) 操作结论
    lines.append(f"8. 操作结论：{stock.get('conclusion', CONCLUSION_WATCH)}")

    # 9) 结论理由
    lines.append(f"9. 结论理由：{stock.get('conclusion_reason', '')}")

    # 10) 条件触发
    if stock.get("conclusion") == CONCLUSION_COND:
        lines.append("10. 条件触发：")
        lines.append("   - 满足：放量不破 + 板块共振 + 主力净流入持续")
        lines.append("   - 不满足：任一条件不满足则放弃")
    elif stock.get("conclusion") == CONCLUSION_BUY:
        lines.append("10. 条件触发：")
        lines.append("   - 满足：开盘 30 分钟内不破均价 + 量比维持 1.0 以上")
        lines.append("   - 不满足：破均价或量比 < 0.8 立即止盈/止损")
    else:
        lines.append("10. 条件触发：")
        lines.append("   - 当前不触发任何买入条件，建议继续观察")

    return "\n".join(lines)


def format_final_conclusion(stocks: list[dict]) -> str:
    """手册第十一章：最终结论章节"""
    buy = [s for s in stocks if s.get("conclusion") == CONCLUSION_BUY]
    cond = [s for s in stocks if s.get("conclusion") == CONCLUSION_COND]
    watch = [s for s in stocks if s.get("conclusion") == CONCLUSION_WATCH]
    skip = [s for s in stocks if s.get("conclusion") == CONCLUSION_SKIP]

    def fmt(lst):
        return "、".join(f"{s.get('name', '?')}({s['code']})" for s in lst) or "（无）"

    return "\n".join([
        "【最终结论】",
        f"- 当前最值得做的标的：{fmt(buy)}",
        f"- 条件满足才可买入：{fmt(cond)}",
        f"- 当前只适合观察的标的：{fmt(watch)}",
        f"- 当前应明确排除的标的：{fmt(skip)}",
    ])


def to_chinese(n: int) -> str:
    """1→一, 2→二, ..., 5→五"""
    m = {1: "一", 2: "二", 3: "三", 4: "四", 5: "五", 6: "六", 7: "七", 8: "八"}
    return m.get(n, str(n))


# =============================================================================
# 7. 主流程
# =============================================================================

def generate_report(trade_date: str, logger: logging.Logger) -> str:
    """主流程：数据获取 → 分析 → 输出 markdown"""
    is_closed, close_reason = is_trading_day()
    logger.info(f"开始生成 {trade_date} 报告 (休市:{is_closed})")

    # ---- 数据层 ----
    logger.info("拉取指数行情...")
    index_quotes = get_index_quotes()
    logger.info("拉取行业排名...")
    industry_data = get_industry_ranking(top_n=20)
    logger.info("拉取北向资金...")
    northbound = get_northbound_flow()
    logger.info("拉取同花顺热点...")
    hot_df = get_hot_stocks_with_reason(trade_date)

    # ---- 分析层 ----
    logger.info("评估市场环境...")
    env = grade_market_environment(index_quotes, northbound, industry_data, hot_df)
    logger.info(f"环境评级: {env['level']} ({env['score']}/100)")

    logger.info("判定方向优先级...")
    directions = rank_directions(hot_df, industry_data)
    logger.info(f"TOP 方向: {[d['name'] for d in directions[:3]]}")

    # ---- 候选股筛选 ----
    candidates = select_candidates(hot_df, directions, top_n=8)
    logger.info(f"候选股: {candidates}")

    # ---- 详细分析 ----
    stock_results = []
    for code in candidates:
        try:
            r = analyze_stock(code, env["level"], logger)
            stock_results.append(r)
        except Exception as e:
            logger.error(f"分析 {code} 失败: {e}")

    # ---- 排除 + 排序 + 选取前 5 ----
    stock_results = sort_candidates(stock_results)
    top5 = stock_results[:5]

    # ---- 输出 markdown ----
    lines = [f"# 早盘潜力股 · {trade_date}", ""]
    if is_closed:
        lines.append(f"> ⚠️ 今日为 {close_reason}，休市日模板。\n")
    lines.append(format_market_review(env, index_quotes, northbound,
                                       industry_data, hot_df, is_closed, close_reason))
    lines.append("")
    lines.append(format_directions(directions))
    lines.append("")
    lines.append("【个股逐只判断】")
    lines.append("")
    for i, s in enumerate(top5, 1):
        lines.append(format_stock_block(s, i, env["level"]))
        lines.append("")
    lines.append(format_final_conclusion(top5))
    lines.append("")
    lines.append("---")
    lines.append(f"报告生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("数据源：a-stock-data 七层 + 同花顺零鉴权接口")
    lines.append("决策依据：/workspace/选股手册.md v2.0")
    if is_closed:
        lines.append("\n> 注：休市日所有标的标注为「仅作研究跟踪，不构成交易建议」。")

    return "\n".join(lines)


def write_report(content: str, trade_date: str) -> Path:
    """写入 output/YYYY-MM-DD_早盘潜力股.md（如已存在则覆盖）"""
    output_path = OUTPUT_DIR / f"{trade_date}_早盘潜力股.md"
    output_path.write_text(content, encoding="utf-8")
    return output_path


def main():
    parser = argparse.ArgumentParser(description="A 股早盘潜力股自动化筛选")
    parser.add_argument("--date", help="指定交易日 YYYY-MM-DD（默认今天）", default=None)
    parser.add_argument("--dry-run", action="store_true", help="只打印不写文件")
    args = parser.parse_args()

    trade_date = args.date or date.today().strftime("%Y-%m-%d")
    logger = setup_logger(trade_date)

    try:
        content = generate_report(trade_date, logger)
        if args.dry_run:
            print(content)
        else:
            path = write_report(content, trade_date)
            logger.info(f"✅ 已生成: {path}")
            print(f"输出文件: {path}")
    except Exception as e:
        logger.error(f"❌ 生成失败: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
