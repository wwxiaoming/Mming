"""
auto_publish.py — 6 通道自动写出
1. /workspace/daily_picks/YYYY-MM-DD/{md, summary.txt, console.txt, state.json}  (本地完整)
2. /workspace/latest.md  软链(已在 post_report.py 里做了)
3. /workspace/POSITIONS.md  持仓表(自动更新 159941 行)
4. /workspace/DAILY_LOG.md  日志(在 ## YYYY-MM-DD 区块下追加)
5. /workspace/STOCK_CONTEXT.md  上下文(顶部 snapshot)
6. 飞书 Webhook 推送(可选,环境变量 FEISHU_WEBHOOK 启用)
"""
from __future__ import annotations
import os, sys, json, re
from pathlib import Path
from datetime import datetime, date
sys.path.insert(0, str(Path(__file__).parent))
from _common import load_json, save_json, DAILY_DIR, log, WORKSPACE

# ── 路径 ──
POSITIONS_MD  = WORKSPACE / "POSITIONS.md"
DAILY_LOG_MD  = WORKSPACE / "DAILY_LOG.md"
CONTEXT_MD    = WORKSPACE / "STOCK_CONTEXT.md"
FEISHU_ENV    = "FEISHU_WEBHOOK"

# ── 工具 ──
def now_iso() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def fmt_money(n: float, sign: bool = False) -> str:
    if n is None:
        return "—"
    s = f"{n:+.2f}" if sign else f"{n:.2f}"
    return s

def fmt_pct(n: float, sign: bool = True) -> str:
    if n is None:
        return "—"
    return f"{n:+.2f}%" if sign else f"{n:.2f}%"

# ── 1. 写 summary.txt(控制台友好的简版)─
def write_summary(today: str, us: dict, picks: dict, t159: dict) -> str:
    """生成简短摘要(可粘到 IM / 短信)"""
    lines = []
    lines.append(f"📊 每日选股摘要 — {today}")
    lines.append("")

    # 美股
    if us and us.get("summary"):
        s = us["summary"]
        ndx = s.get("NDX", 0)
        sox = s.get("SOX", 0)
        lines.append("🌙 美股隔夜:")
        lines.append(f"  NDX {ndx:+.2f}%  SPX {s.get('SPX',0):+.2f}%  DJI {s.get('DJI',0):+.2f}%  SOX {sox:+.2f}%")
        lines.append("")

    # 159941
    if t159:
        h = t159["holdings"]
        q = t159["quote"]
        cum_pct = h.get("cum_pnl_pct", 0)
        cum = h.get("cum_pnl", 0)
        emoji = "🟢" if cum > 0 else "🔴" if cum < 0 else "⚪"
        lines.append("📈 159941 持仓:")
        lines.append(f"  现价 {q['price']:.3f} ({q['change_pct']:+.2f}%)")
        lines.append(f"  {h['shares']}股 × 成本{h['cost']:.3f}")
        lines.append(f"  当日 {h['daily_pnl']:+.2f}元  累计 {cum_pct:+.2f}% ({cum:+.2f}元) {emoji}")
        lines.append("")

    # 9 策略 TOP
    sections = [
        ("1️⃣ 当日强势股", "1_momentum", ["name","code","change_pct","reason"]),
        ("2️⃣ 主力资金",   "2_fund_flow", ["name","code","change_pct","main_net_5d_yi"]),
        ("3️⃣ 价值股",     "3_value",     ["name","code","pe_ttm","pb"]),
        ("4️⃣ ETF 活跃",   "4_etf_premium",["name","code","change_pct","turnover_pct"]),
        ("6️⃣ 产业链瓶颈", "6_serenity_chain", ["theme","hits"]),
        ("7️⃣ 护城河",     "7_buffett_moat",  ["name","code","roe_est","pe_ttm"]),
        ("8️⃣ 🔮 最佳 5 选","8_best5",    ["name","code","score","change_pct"]),
    ]
    for title, key, fields in sections:
        rows = picks.get(key, [])[:5]
        if not rows:
            continue
        lines.append(title)
        for i, r in enumerate(rows, 1):
            parts = []
            for f in fields[:3]:  # 只列前 3 个字段
                v = r.get(f)
                if isinstance(v, float):
                    parts.append(f"{f}={v:+.2f}")
                else:
                    parts.append(f"{f}={v}")
            lines.append(f"  {i}. " + " ".join(parts))
        lines.append("")

    lines.append("📁 详细报告: /workspace/daily_picks/{}/".format(today))
    return "\n".join(lines)

# ── 2. 写 state.json(给前端 / 监控消费)─
def write_state_json(today: str, us: dict, picks: dict, t159: dict):
    state = {
        "date": today,
        "generated_at": now_iso(),
        "us_overnight": us.get("summary") if us else {},
        "holdings_159941": {
            "name": t159.get("name"),
            "price": t159["quote"]["price"],
            "change_pct": t159["quote"]["change_pct"],
            "shares": t159["holdings"]["shares"],
            "cost": t159["holdings"]["cost"],
            "daily_pnl": t159["holdings"]["daily_pnl"],
            "cum_pnl": t159["holdings"]["cum_pnl"],
            "cum_pnl_pct": t159["holdings"]["cum_pnl_pct"],
        } if t159 else {},
        "top_picks": {
            "momentum": picks.get("1_momentum", [])[:5],
            "fund_flow": picks.get("2_fund_flow", [])[:5],
            "value": picks.get("3_value", [])[:5],
            "best5": picks.get("8_best5", [])[:5],
            "serenity_chain": picks.get("6_serenity_chain", [])[:5],
            "buffett_moat": picks.get("7_buffett_moat", [])[:5],
        },
        "news": picks.get("5_news", [])[:5],
        "etf_active": picks.get("4_etf_premium", [])[:5],
    }
    out = DAILY_DIR / today / "state.json"
    save_json(out, state)
    return out

# ── 3. 更新 POSITIONS.md ──
def update_positions(t159: dict):
    """找到 159941 行,更新现价 / 当日盈亏 / 累计盈亏 / 成本价(若仍为"待补")"""
    if not t159:
        log("  ⏭ POSITIONS.md: 无 159941 数据,跳过")
        return
    h = t159["holdings"]
    q = t159["quote"]
    cum = h.get("cum_pnl", 0)
    cum_pct = h.get("cum_pnl_pct", 0)
    cum_emoji = "🟢" if cum > 0 else "🔴" if cum < 0 else "⚪"

    if not POSITIONS_MD.exists():
        log("  ⚠ POSITIONS.md 不存在,跳过")
        return

    text = POSITIONS_MD.read_text(encoding="utf-8")
    # 找 159941 行(基于表头识别)
    # 表头: 代码 | 名称 | 数量(股) | 成本价(元) | 现价(元) | 当日盈亏(元) | 累计盈亏(元) | 备注
    # 数据行: 159941 | 广发纳指100ETF | 700 | 待补 | (自动) | (自动) | (自动) | ...
    # 我们用更简单的:找包含 159941 的行
    new_line = (
        f"| 159941 | 广发纳指100ETF | {h['shares']} | "
        f"{h['cost']:.3f} | {q['price']:.3f} | "
        f"{h['daily_pnl']:+.2f} | {cum:+.2f} {cum_emoji} | "
        f"换手 {q['turnover_pct']:.2f}% |"
    )

    # 替换:用整行匹配
    pattern = r"\| 159941 \|[^\n]*"
    new_text, n = re.subn(pattern, new_line, text)
    if n == 0:
        # 没找到 → append 一行
        log("  ⚠ POSITIONS.md 没找到 159941 行,append")
        new_text = text.rstrip() + "\n" + new_line + "\n"
    else:
        log(f"  ✅ POSITIONS.md 更新 159941 行(替换 {n} 处)")

    # 在文件顶部加更新时间
    if "# 持仓表" in new_text:
        new_text = re.sub(
            r"(# 持仓表\(Positions\)\n\n> 每次 `run_daily\.sh` 自动更新。\n\n)",
            r"\1> 最近一次更新:" + now_iso() + "\n\n",
            new_text
        )
    POSITIONS_MD.write_text(new_text, encoding="utf-8")

# ── 4. 追加 DAILY_LOG.md ──
def append_daily_log(today: str, us: dict, picks: dict, t159: dict):
    """在 ## YYYY-MM-DD 区块下追加;若该区块已存在,合并"""
    if not DAILY_LOG_MD.exists():
        log("  ⚠ DAILY_LOG.md 不存在,跳过")
        return

    text = DAILY_LOG_MD.read_text(encoding="utf-8")

    # 生成新条目
    new_section = build_log_section(today, us, picks, t159)

    # 找 ## YYYY-MM-DD 区块
    pattern = re.compile(
        rf"## {re.escape(today)}\n.*?(?=\n## \d{{4}}-\d{{2}}-\d{{2}}|\Z)",
        re.DOTALL,
    )
    if pattern.search(text):
        # 已存在 → 删除旧块,插入新块(放最前)
        text = pattern.sub("", text).rstrip() + "\n\n" + new_section
        log(f"  ✅ DAILY_LOG.md 替换 {today} 区块")
    else:
        # 不存在 → 插到文件最前(在 # 标题之后)
        if "# 每日盘后日志" in text:
            text = re.sub(
                r"(# 每日盘后日志\(Daily Log\)\n\n>.*?\n\n)",
                r"\1" + new_section + "\n",
                text,
                count=1,
                flags=re.DOTALL,
            )
        else:
            text = text + "\n" + new_section
        log(f"  ✅ DAILY_LOG.md 追加 {today} 区块")

    DAILY_LOG_MD.write_text(text, encoding="utf-8")

def build_log_section(today: str, us: dict, picks: dict, t159: dict) -> str:
    """生成 ## YYYY-MM-DD 区块内容"""
    lines = [f"## {today}\n"]
    lines.append(f"**生成时间**:{now_iso()}\n")

    # 1. 美股隔夜
    if us and us.get("summary"):
        s = us["summary"]
        lines.append("### 🌙 美股隔夜")
        lines.append(f"- NDX **{s.get('NDX',0):+.2f}%**  SPX {s.get('SPX',0):+.2f}%  DJI {s.get('DJI',0):+.2f}%  SOX {s.get('SOX',0):+.2f}%")
        if us.get("magnificent7"):
            lines.append("- 七巨头: " + "  ".join(
                f"{r.get('name','?')[:4]}{r.get('change_pct',0):+.2f}%" for r in us["magnificent7"]
            ))
        lines.append("")

    # 2. 159941 持仓
    if t159:
        h = t159["holdings"]
        q = t159["quote"]
        cum_pct = h.get("cum_pnl_pct", 0)
        cum = h.get("cum_pnl", 0)
        emoji = "🟢" if cum > 0 else "🔴" if cum < 0 else "⚪"
        lines.append("### 📈 159941 持仓")
        lines.append(f"- 现价 **{q['price']:.3f}** ({q['change_pct']:+.2f}%)  换手 {q['turnover_pct']:.2f}%")
        lines.append(f"- 持仓 {h['shares']}股 × 成本 {h['cost']:.3f} → 市值 {h['market_value']:.2f}元")
        lines.append(f"- 当日盈亏 **{h['daily_pnl']:+.2f}元** ({h['daily_pnl_pct']:+.2f}%)")
        lines.append(f"- 累计盈亏 **{cum:+.2f}元** ({cum_pct:+.2f}%) {emoji}")
        lines.append("")

    # 3. 9 策略精华
    lines.append("### 🧠 9 策略精华")
    for title, key, fmt in [
        ("1️⃣ 强势股", "1_momentum", "{name}({code}) {change_pct:+.2f}% {reason}"),
        ("2️⃣ 资金",   "2_fund_flow","{name}({code}) {main_net_5d_yi:+.3f}分"),
        ("3️⃣ 价值",   "3_value",    "{name}({code}) PE{pe_ttm:.2f} PB{pb:.2f}"),
        ("4️⃣ ETF",    "4_etf_premium","{name}({code}) {change_pct:+.2f}% 换手{turnover_pct:.2f}%"),
        ("6️⃣ 产业链", "6_serenity_chain","{theme} ×{hits}"),
        ("7️⃣ 护城河", "7_buffett_moat", "{name}({code}) ROE估算{roe_est:.1f}% PE{pe_ttm:.2f}"),
        ("8️⃣ 最佳 5 选","8_best5",  "{name}({code}) {score}分 {change_pct:+.2f}%"),
    ]:
        rows = picks.get(key, [])[:5]
        if not rows:
            continue
        lines.append(f"- **{title}**")
        for r in rows:
            try:
                lines.append(f"  - " + fmt.format(**r))
            except (KeyError, IndexError):
                lines.append(f"  - " + str(r)[:80])
    lines.append("")

    # 4. 新闻
    news = picks.get("5_news", [])[:3]
    if news:
        lines.append("### 📰 今日新闻 TOP 3")
        for n in news:
            lines.append(f"- {n.get('time','')[:16]} **{n.get('title','')[:60]}**")
        lines.append("")

    # 5. 风险
    risks = []
    if us and us["summary"].get("NDX", 0) < -1.5:
        risks.append(f"🔴 美股纳指大跌 {us['summary']['NDX']:.2f}%")
    if t159 and t159["holdings"].get("cum_pnl_pct", 0) < -10:
        risks.append("🔴 159941 累计亏损 >10%")
    if not risks:
        risks.append("⚪ 暂无显著风险")
    lines.append(f"### ⚠️ 风险\n- " + "\n- ".join(risks))
    lines.append("")

    return "\n".join(lines)

# ── 5. 更新 STOCK_CONTEXT.md(顶部 snapshot)─
def update_context(today: str, us: dict, picks: dict, t159: dict):
    if not CONTEXT_MD.exists():
        log("  ⚠ STOCK_CONTEXT.md 不存在,跳过")
        return
    text = CONTEXT_MD.read_text(encoding="utf-8")

    # 生成 snapshot
    snap = build_context_snapshot(today, us, picks, t159)
    # 替换 ## 最近一次更新 区块
    pattern = re.compile(
        r"## 最近一次更新\n.*?(?=\n---\n|\n## |\Z)",
        re.DOTALL,
    )
    if pattern.search(text):
        text = pattern.sub(snap, text)
        log(f"  ✅ STOCK_CONTEXT.md 更新 snapshot")
    else:
        # 插到最前
        text = text + "\n\n" + snap
        log(f"  ✅ STOCK_CONTEXT.md append snapshot")
    CONTEXT_MD.write_text(text, encoding="utf-8")

def build_context_snapshot(today: str, us: dict, picks: dict, t159: dict) -> str:
    ndx = us["summary"].get("NDX", 0) if us else 0
    sox = us["summary"].get("SOX", 0) if us else 0
    spx = us["summary"].get("SPX", 0) if us else 0
    cum_pct = t159["holdings"].get("cum_pnl_pct", 0) if t159 else 0
    cum = t159["holdings"].get("cum_pnl", 0) if t159 else 0
    best5 = picks.get("8_best5", [])[:3]

    lines = ["## 最近一次更新\n"]
    lines.append(f"- **时间**:{now_iso()}({today})")
    lines.append(f"- **美股隔夜**:NDX {ndx:+.2f}%  SPX {spx:+.2f}%  SOX {sox:+.2f}%")
    if t159:
        lines.append(f"- **持仓汇总**:159941 现价 {t159['quote']['price']:.3f} | 累计 {cum_pct:+.2f}% ({cum:+.2f}元)")
    if best5:
        names = "、".join(f"{r['name']}({r['code']})" for r in best5)
        lines.append(f"- **最佳 3 选**:{names}")
    lines.append(f"- **核心结论**:" + derive_conclusion(ndx, cum_pct, picks))
    return "\n".join(lines)

def derive_conclusion(ndx: float, cum_pct: float, picks: dict) -> str:
    """简单三段式结论"""
    parts = []
    if ndx > 1:
        parts.append(f"美股强({ndx:+.1f}%)")
    elif ndx < -1:
        parts.append(f"美股弱({ndx:+.1f}%)")
    else:
        parts.append("美股震荡")
    if cum_pct > 5:
        parts.append(f"159941 浮盈 {cum_pct:+.1f}%")
    elif cum_pct < -5:
        parts.append(f"159941 浮亏 {cum_pct:+.1f}%")
    else:
        parts.append("159941 持平")
    chain = picks.get("6_serenity_chain", [])
    if chain:
        parts.append(f"主线 {chain[0].get('theme','')}")
    return " | ".join(parts)

# ── 6. 飞书 Webhook 推送(可选)─
def publish_feishu(today: str, summary: str):
    webhook = os.environ.get(FEISHU_ENV)
    if not webhook:
        log("  ⏭ FEISHU_WEBHOOK 未设置,跳过飞书推送")
        return False
    try:
        import urllib.request
        # 飞书机器人 markdown 消息(免费版可用,无需签名)
        payload = {
            "msg_type": "interactive",
            "card": {
                "header": {
                    "title": {"tag": "plain_text", "content": f"📊 每日选股 {today}"},
                    "template": "blue",
                },
                "elements": [
                    {"tag": "markdown", "content": f"```\n{summary}\n```"},
                    {"tag": "note", "elements": [{"tag": "plain_text", "content": f"由 stock-trader-agent v1.6 自动生成 · {now_iso()}"}]},
                ],
            }
        }
        req = urllib.request.Request(
            webhook,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        resp = urllib.request.urlopen(req, timeout=10)
        body = resp.read().decode("utf-8")
        if "ok" in body.lower() or '"StatusCode"' in body:
            log(f"  ✅ 飞书推送成功:{body[:80]}")
            return True
        log(f"  ⚠ 飞书推送返回: {body[:200]}")
        return False
    except Exception as e:
        log(f"  ⚠ 飞书推送失败:{e}")
        return False

# ── 主入口 ──
def main():
    today = date.today().strftime("%Y-%m-%d")
    out_dir = DAILY_DIR / today
    if not out_dir.exists():
        log(f"❌ {out_dir} 不存在,先跑 run_daily.sh")
        sys.exit(1)

    log(f"=== 自动写出 6 通道({today})===")

    # 读 4 个 JSON
    us      = load_json(out_dir / "us_market.json")
    picks   = load_json(out_dir / "daily_picks.json")
    t159    = load_json(out_dir / "159941-tracker.json")
    md_file = out_dir / f"{today}.md"
    md_text = md_file.read_text(encoding="utf-8") if md_file.exists() else ""

    # 通道 1:写 summary.txt + console.txt
    summary = write_summary(today, us, picks, t159)
    (out_dir / "summary.txt").write_text(summary, encoding="utf-8")
    log(f"  ✅ 通道 1.1: {out_dir}/summary.txt")
    # console.txt = 完整 md(便于 cat)
    if md_text:
        (out_dir / "console.txt").write_text(md_text, encoding="utf-8")
        log(f"  ✅ 通道 1.2: {out_dir}/console.txt")

    # 通道 2:state.json
    state_path = write_state_json(today, us, picks, t159)
    log(f"  ✅ 通道 2: {state_path}")

    # 通道 3:POSITIONS.md
    log("  → 通道 3: POSITIONS.md")
    update_positions(t159)

    # 通道 4:DAILY_LOG.md
    log("  → 通道 4: DAILY_LOG.md")
    append_daily_log(today, us, picks, t159)

    # 通道 5:STOCK_CONTEXT.md
    log("  → 通道 5: STOCK_CONTEXT.md")
    update_context(today, us, picks, t159)

    # 通道 6:飞书 Webhook(可选)
    log("  → 通道 6: 飞书 Webhook")
    publish_feishu(today, summary)

    # 写到 console
    print("\n" + "═" * 50)
    print("  📊 6 通道写出完成")
    print("═" * 50)
    print(summary)
    print("\n" + "═" * 50)
    print("  ✅ 自动写出 6 通道完成")
    print("═" * 50)

if __name__ == "__main__":
    main()
