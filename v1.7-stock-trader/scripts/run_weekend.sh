#!/usr/bin/env bash
# run_weekend.sh — v1.7.0 周末模式(周日晚 22:00 跑,选周一开盘潜力股)
# 流程:
#   1. 美股周五收盘(us_market_fetcher)
#   2. 周末选股(daily_stock_pick.py --mode=weekend)
#   3. 拼周末报告(post_report_weekend.py)
#   4. 6 通道写出(auto_publish.py)
set -e
cd /workspace

# ── 用户配置(与 run_daily.sh 保持一致)──
HOLDINGS_CODE="159941"
HOLDINGS_SHARES="700"
HOLDINGS_COST="1.623"

echo "═══════════════════════════════════════════════"
echo "  v1.7.0 周末展望 — $(date '+%Y-%m-%d %H:%M:%S')"
echo "═══════════════════════════════════════════════"
echo "  持仓: ${HOLDINGS_CODE} × ${HOLDINGS_SHARES}股 @ ${HOLDINGS_COST}"
echo "  模式: 🌙 周一潜力股 TOP 5(行业+资金+美股周五+7×24 资讯)"
echo

# ── 1. 美股周五收盘 ──
echo "[1/4] 拉美股周五收盘…"
python3 scripts/us_market_fetcher.py

# ── 2. 159941 持仓跟踪(虽然周末没行情,但记录周五收盘)──
echo
echo "[2/4] 跟踪 ${HOLDINGS_CODE} 持仓…"
python3 scripts/strategy_holdings_tracker.py \
  --code="${HOLDINGS_CODE}" \
  --shares="${HOLDINGS_SHARES}" \
  --cost="${HOLDINGS_COST}"

# ── 3. 周末选股(行业+资金+美股+资讯)──
echo
echo "[3/4] 周末选股(周一潜力股 TOP 5)…"
python3 scripts/daily_stock_pick.py --mode=weekend

# ── 4. 拼周末报告 ──
echo
echo "[4/4] 生成周末报告 + 6 通道写出…"
python3 scripts/post_report_weekend.py
python3 scripts/auto_publish.py

echo
echo "═══════════════════════════════════════════════"
echo "  ✅ 周末展望完成"
echo "  📊 报告:  /workspace/daily_picks/$(date '+%Y-%m-%d')/weekend_preview.md"
echo "  📋 摘要:  /workspace/daily_picks/$(date '+%Y-%m-%d')/summary.txt"
echo "  📈 持仓:  /workspace/POSITIONS.md"
echo "  📝 日志:  /workspace/DAILY_LOG.md"
echo "═══════════════════════════════════════════════"
