#!/usr/bin/env bash
# run_daily.sh — v1.6 每日选股主调度
# 用法: ./run_daily.sh
# 时间: 工作日 07:00(可挂 cron: 0 7 * * 1-5 /workspace/scripts/run_daily.sh)
set -e
cd /workspace
echo "═══════════════════════════════════════════════"
echo "  v1.6 每日选股 — $(date '+%Y-%m-%d %H:%M:%S')"
echo "═══════════════════════════════════════════════"

# 1. 美股隔夜
echo
echo "[1/4] 拉美股隔夜数据…"
python3 scripts/us_market_fetcher.py

# 2. 159941 持仓跟踪(700 股,成本 1.55 — 需根据实际改)
echo
echo "[2/4] 跟踪 159941 持仓…"
python3 scripts/strategy_holdings_tracker.py --code=159941 --shares=700 --cost=1.55

# 3. 9 策略并行
echo
echo "[3/4] 9 策略并行选股…"
python3 scripts/daily_stock_pick.py --mode=all

# 4. 拼报告
echo
echo "[4/4] 生成 Markdown 报告…"
python3 scripts/post_report.py

echo
echo "═══════════════════════════════════════════════"
echo "  ✅ 完成 — /workspace/daily_picks/$(date '+%Y-%m-%d').md"
echo "═══════════════════════════════════════════════"
