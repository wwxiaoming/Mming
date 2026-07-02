"""
run_all.py — 自进化系统一键执行

完整流程:
  Step 1: backtest_tracker     — 拉取选股后实际行情
  Step 2: multi_dimension_analysis — 7 维度分析
  Step 3: strategy_evaluator    — 策略有效性评估
  Step 4: weight_optimizer      — 权重自动优化
  Step 5: report_generator      — 生成 Markdown 报告

用法:
  python3 scripts/evolution/run_all.py --days=30
  python3 scripts/evolution/run_all.py --days=30 --skip-tracking  # 复用上次追踪数据

输出:
  /workspace/daily_picks/_tracking/tracking_YYYYMMDD.json
  /workspace/daily_picks/_evolution/analysis_YYYYMMDD.json
  /workspace/daily_picks/_evolution/evaluation_YYYYMMDD.json
  /workspace/daily_picks/_evolution/weights_YYYYMMDD.json
  /workspace/daily_picks/_evolution/evolution_YYYYMMDD.md
"""
from __future__ import annotations
import sys, argparse, time
from pathlib import Path
from datetime import datetime

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import log, DAILY_DIR


def banner(text: str, char: str = "─", width: int = 60) -> str:
    return f"\n{char * width}\n{text}\n{char * width}"


def main():
    parser = argparse.ArgumentParser(description="AI 选股自进化系统 — 一键执行")
    parser.add_argument("--days", type=int, default=30, help="回溯天数(默认 30)")
    parser.add_argument("--skip-tracking", action="store_true",
                        help="跳过追踪步骤,复用上次追踪数据(用于调试后续步骤)")
    parser.add_argument("--only-report", action="store_true",
                        help="仅生成报告(复用所有上次产物)")
    args = parser.parse_args()

    start = time.time()
    print(banner(f"🧬 AI 选股自进化系统 v1.0 启动", "="))
    print(f"启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"回溯天数: {args.days} 天")
    print(f"输出根目录: {DAILY_DIR}")

    # ── Step 1: backtest_tracker ──
    tracking: list = []
    if args.only_report:
        print(banner("Step 1: backtest_tracker — 跳过(--only-report)"))
    elif args.skip_tracking:
        print(banner("Step 1: backtest_tracker — 跳过(--skip-tracking),复用最新追踪数据"))
    else:
        print(banner("Step 1: backtest_tracker — 拉取选股后实际行情"))
        try:
            from backtest_tracker import run_tracking
            tracking = run_tracking(args.days)
            if not tracking:
                print("⚠ 无追踪数据,后续步骤可能无意义,但仍继续执行以生成空报告骨架")
        except Exception as e:
            print(f"❌ Step 1 失败: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

    # ── Step 2: multi_dimension_analysis ──
    print(banner("Step 2: multi_dimension_analysis — 7 维度分析"))
    analysis: dict = {}
    try:
        from multi_dimension_analysis import analyze, load_latest_tracking
        if not tracking:
            tracking = load_latest_tracking()
        if tracking:
            analysis = analyze(tracking)
            EVOLUTION_DIR = DAILY_DIR / "_evolution"
            EVOLUTION_DIR.mkdir(parents=True, exist_ok=True)
            out = EVOLUTION_DIR / f"analysis_{datetime.now().strftime('%Y%m%d')}.json"
            import json
            out.write_text(json.dumps(analysis, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"✅ 分析完成 → {out}")
        else:
            print("⚠ 无追踪数据,跳过分析")
    except Exception as e:
        print(f"❌ Step 2 失败: {e}")
        import traceback
        traceback.print_exc()

    # ── Step 3: strategy_evaluator ──
    print(banner("Step 3: strategy_evaluator — 策略有效性评估"))
    evaluation: dict = {}
    try:
        from strategy_evaluator import evaluate_all
        if analysis:
            evaluation = evaluate_all(analysis)
            EVOLUTION_DIR = DAILY_DIR / "_evolution"
            out = EVOLUTION_DIR / f"evaluation_{datetime.now().strftime('%Y%m%d')}.json"
            import json
            out.write_text(json.dumps(evaluation, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"✅ 评估完成 → {out}")
            summary = evaluation.get("summary", {})
            print(f"  优秀 ⭐⭐⭐: {summary.get('excellent_count', 0)} 个")
            print(f"  合格 ⭐⭐:   {summary.get('pass_count', 0)} 个")
            print(f"  不及格 ⭐:   {summary.get('fail_count', 0)} 个")
        else:
            print("⚠ 无分析数据,跳过评估")
    except Exception as e:
        print(f"❌ Step 3 失败: {e}")
        import traceback
        traceback.print_exc()

    # ── Step 4: weight_optimizer ──
    print(banner("Step 4: weight_optimizer — 权重自动优化"))
    weights: dict = {}
    try:
        from weight_optimizer import optimize_weights
        if evaluation:
            weights = optimize_weights(evaluation)
            EVOLUTION_DIR = DAILY_DIR / "_evolution"
            out = EVOLUTION_DIR / f"weights_{datetime.now().strftime('%Y%m%d')}.json"
            import json
            out.write_text(json.dumps(weights, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"✅ 权重优化完成 → {out}")
            print(f"  旧权重: {weights.get('old_weights')}")
            print(f"  新权重: {weights.get('new_weights')}")
        else:
            print("⚠ 无评估数据,跳过权重优化")
    except Exception as e:
        print(f"❌ Step 4 失败: {e}")
        import traceback
        traceback.print_exc()

    # ── Step 5: report_generator ──
    print(banner("Step 5: report_generator — 生成自进化 Markdown 报告"))
    try:
        from report_generator import generate, save_report
        md = generate(tracking, analysis, evaluation, weights, days=args.days)
        out = save_report(md, days=args.days)
        print(f"✅ 报告生成完成 → {out}")
        print(f"  报告大小: {out.stat().st_size} bytes")
    except Exception as e:
        print(f"❌ Step 5 失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    # ── 总结 ──
    elapsed = time.time() - start
    print(banner("🎉 自进化系统执行完成", "="))
    print(f"总耗时: {elapsed:.1f} 秒")
    print(f"输出目录: {DAILY_DIR / '_evolution'}")
    print(f"\n核心产物:")
    print(f"  - Markdown 报告: {DAILY_DIR}/_evolution/evolution_{datetime.now().strftime('%Y%m%d')}.md")
    print(f"\n下一步:")
    print(f"  - 人工审阅报告,确认权重调整方向")
    print(f"  - 若同意新权重,可将其同步到选股手册_x1.0.md 或 daily_pick_config.yaml")
    print(f"  - 下周一早盘选股将使用新权重")


if __name__ == "__main__":
    main()
