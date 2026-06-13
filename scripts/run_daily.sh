#!/usr/bin/env bash
# run_daily.sh — v1.6 每日选股主调度(集成 auto_publish)
# 用法: ./run_daily.sh
# 时间: 工作日 07:00(可挂 cron: 0 7 * * 1-5 /workspace/scripts/run_daily.sh)
set -e
cd /workspace

# ── 用户配置 ──
HOLDINGS_CODE="159941"
HOLDINGS_SHARES="700"
HOLDINGS_COST="1.55"     # 改成你的真实平均成本

echo "═══════════════════════════════════════════════"
echo "  v1.6 每日选股 — $(date '+%Y-%m-%d %H:%M:%S')"
echo "═══════════════════════════════════════════════"
echo "  持仓: ${HOLDINGS_CODE} × ${HOLDINGS_SHARES}股 @ ${HOLDINGS_COST}"
echo

# ── 1. 美股隔夜 ──
echo "[1/5] 拉美股隔夜数据…"
python3 scripts/us_market_fetcher.py

# ── 2. 持仓跟踪 ──
echo
echo "[2/5] 跟踪 ${HOLDINGS_CODE} 持仓…"
python3 scripts/strategy_holdings_tracker.py \
  --code="${HOLDINGS_CODE}" \
  --shares="${HOLDINGS_SHARES}" \
  --cost="${HOLDINGS_COST}"

# ── 3. 9 策略并行 ──
echo
echo "[3/5] 9 策略并行选股…"
python3 scripts/daily_stock_pick.py --mode=all

# ── 4. 拼 Markdown 报告 ──
echo
echo "[4/5] 生成 Markdown 报告…"
python3 scripts/post_report.py

# ── 5. 自动写出 6 通道 ──
echo
echo "[5/5] 自动写出 6 通道…"
python3 scripts/auto_publish.py

echo
echo "═══════════════════════════════════════════════"
echo "  ✅ 全部完成"
echo "  📊 报告:  /workspace/daily_picks/$(date '+%Y-%m-%d').md"
echo "  📋 摘要:  /workspace/daily_picks/$(date '+%Y-%m-%d')/summary.txt"
echo "  📈 持仓:  /workspace/POSITIONS.md"
echo "  📝 日志:  /workspace/DAILY_LOG.md"
echo "  📚 上下文:/workspace/STOCK_CONTEXT.md"
echo "═══════════════════════════════════════════════"
