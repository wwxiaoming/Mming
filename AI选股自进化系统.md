# AI 选股自进化系统 v1.0

> 让系统回顾历史选股记录，拉取选股后实际表现，多维度分析命中率与收益，输出策略优化建议
> 版本 v1.0 · 2026-06-16

---

## 一、核心理念

### 1.1 为什么需要自进化？

| 问题 | 表现 | 后果 |
|------|------|------|
| 策略不验证 | 每天选股但不回顾 | 不知道哪些策略有效 |
| 无反馈闭环 | 选完就忘 | 重复犯同样的错误 |
| 参数不调优 | 权重固定不变 | 市场变了策略没变 |
| 无命中统计 | 不知道准确率 | 无法评估系统价值 |

### 1.2 自进化闭环

```
每日选股（7:00）
    ↓
记录候选池（JSON 存档）
    ↓
    ┌──────────────────────────┐
    │  每周自进化分析（周日 8:00）  │
    │                            │
    │  1. 读取过去 N 天选股记录     │
    │  2. 拉取选股后实际行情        │
    │  3. 多维度分析命中率/收益     │
    │  4. 策略有效性评估           │
    │  5. 输出优化建议             │
    │  6. 自动调整权重/参数        │
    └──────────────────────────┘
    ↓
更新策略参数（daily_pick_config.yaml）
    ↓
下一周选股用新参数
```

### 1.3 核心指标定义

| 指标 | 定义 | 计算方式 |
|------|------|---------|
| **命中率** | 推荐后上涨的标的占比 | 上涨数 / 总推荐数 |
| **平均收益** | 推荐后 N 日平均涨跌幅 | mean(各标的 N 日涨幅) |
| **超额收益** | 跑赢沪深 300 的幅度 | 平均收益 - 沪深300同期涨幅 |
| **最佳表现** | 推荐池中涨幅最高 | max(各标的 N 日涨幅) |
| **最差表现** | 推荐池中跌幅最大 | min(各标的 N 日涨幅) |
| **胜率** | 盈利标的占比 | 盈利数 / 总数 |
| **盈亏比** | 平均盈利 / 平均亏损 | avg_win / avg_loss |

---

## 二、多维度分析框架

### 2.1 维度一：策略有效性

分析 9 大策略各自的命中率与收益表现。

| 策略 | 命中率 | 平均收益 | 超额收益 | 评级 | 动作 |
|------|-------|---------|---------|------|------|
| 策略1 强势股 | ?% | ?% | ?% | ⭐⭐⭐ | 保持/加大权重 |
| 策略2 主力资金 | ?% | ?% | ?% | ⭐⭐ | 保持 |
| 策略3 价值股 | ?% | ?% | ?% | ⭐ | 降低权重 |
| ... | ... | ... | ... | ... | ... |

**评级标准**：
- ⭐⭐⭐ 优秀：命中率 > 60% 且超额收益 > 2%
- ⭐⭐ 合格：命中率 50-60% 或超额收益 0-2%
- ⭐ 不及格：命中率 < 50% 或超额收益 < 0%

### 2.2 维度二：板块/题材表现

分析哪些板块/题材的推荐效果最好。

| 板块 | 推荐次数 | 命中率 | 平均收益 | 趋势 |
|------|---------|-------|---------|------|
| 半导体 | ? | ?% | ?% | ↑/↓ |
| AI/算力 | ? | ?% | ?% | ↑/↓ |
| 新能源 | ? | ?% | ?% | ↑/↓ |
| 创新药 | ? | ?% | ?% | ↑/↓ |
| ... | ... | ... | ... | ... |

### 2.3 维度三：时间窗口分析

分析推荐后不同时间窗口的表现。

| 持有天数 | 平均收益 | 胜率 | 最佳 | 最差 |
|---------|---------|------|------|------|
| T+1 | ?% | ?% | ?% | ?% |
| T+3 | ?% | ?% | ?% | ?% |
| T+5 | ?% | ?% | ?% | ?% |
| T+10 | ?% | ?% | ?% | ?% |
| T+20 | ?% | ?% | ?% | ?% |

**用途**：判断最佳持有周期。

### 2.4 维度四：市值区间分析

| 市值区间 | 推荐次数 | 命中率 | 平均收益 |
|---------|---------|-------|---------|
| < 50 亿 | ? | ?% | ?% |
| 50-100 亿 | ? | ?% | ?% |
| 100-300 亿 | ? | ?% | ?% |
| 300-1000 亿 | ? | ?% | ?% |
| > 1000 亿 | ? | ?% | ?% |

### 2.5 维度五：美股隔夜影响验证

验证美股隔夜信号对 A 股次日表现预测的准确性。

| 美股信号 | A 股实际开盘 | 预测准确？ | 平均收益 |
|---------|------------|-----------|---------|
| 纳指 +2% → 科技股利好 | ? | ✅/❌ | ?% |
| 费半 -2% → 半导体利空 | ? | ✅/❌ | ?% |
| ... | ... | ... | ... |

### 2.6 维度六：评分分位分析

按选股时的评分分位，验证评分越高是否收益越好。

| 评分区间 | 标的数 | 平均收益 | 胜率 |
|---------|-------|---------|------|
| 80-100 分 | ? | ?% | ?% |
| 60-80 分 | ? | ?% | ?% |
| 40-60 分 | ? | ?% | ?% |
| < 40 分 | ? | ?% | ?% |

**用途**：如果高分标的收益显著更好，说明评分体系有效。

### 2.7 维度七：错误分析

分析推荐失败的案例，找出共性错误。

| 错误类型 | 出现次数 | 占比 | 典型案例 | 改进建议 |
|---------|---------|------|---------|---------|
| 追高被套 | ? | ?% | ? | 加入涨幅过滤 |
| 利空未识别 | ? | ?% | ? | 加强新闻监控 |
| 解禁压力 | ? | ?% | ? | 加入解禁日历 |
| 周期反转 | ? | ?% | ? | 关注期货价格 |
| 流动性陷阱 | ? | ?% | ? | 加入成交量门槛 |

---

## 三、自进化脚本设计

### 3.1 文件结构

```
/workspace/scripts/
├── evolution/
│   ├── __init__.py
│   ├── backtest_tracker.py      # 拉取选股后实际行情
│   ├── multi_dimension_analysis.py  # 多维度分析引擎
│   ├── strategy_evaluator.py    # 策略有效性评估
│   ├── weight_optimizer.py      # 权重自动优化
│   └── report_generator.py      # 自进化报告生成
├── daily_stock_pick.py          # 每日选股（已有）
└── daily_pick_config.yaml       # 配置（已有，可被自进化更新）
```

### 3.2 backtest_tracker.py — 拉取选股后实际表现

```python
"""
回测追踪器：读取历史选股记录，拉取选股后实际行情。
"""
import json
import os
from pathlib import Path
from datetime import datetime, timedelta
from mootdx.quotes import Quotes

PICKS_DIR = Path("/workspace/daily_picks")
TRACK_DIR = Path("/workspace/daily_picks/_tracking")

def load_historical_picks(days: int = 30) -> list[dict]:
    """读取过去 N 天的选股记录"""
    records = []
    for f in sorted(PICKS_DIR.glob("*.json")):
        if f.name.startswith("_"):
            continue
        try:
            data = json.loads(f.read_text())
            date = data.get("date", f.stem[:10])
            for strategy, items in data.get("strategies", {}).items():
                for item in items:
                    records.append({
                        "date": date,
                        "strategy": strategy,
                        "code": item.get("code", ""),
                        "name": item.get("name", ""),
                        "score": item.get("score", 0),
                        "price_at_pick": item.get("price", 0),
                    })
        except Exception:
            continue
    # 过滤最近 N 天
    cutoff = datetime.now() - timedelta(days=days)
    return [r for r in records if datetime.strptime(r["date"][:10], "%Y-%m-%d") >= cutoff]

def fetch_post_pick_performance(code: str, pick_date: str, days: int = 20) -> dict:
    """拉取选股后 N 天的实际表现"""
    client = Quotes.factory(market='std')
    market = 1 if code.startswith("6") else 0
    klines = client.bars(symbol=code, category=4, offset=days + 5)

    # 找到选股日之后的 K 线
    post_klines = [k for k in klines if k["datetime"][:10] > pick_date]
    if not post_klines:
        return {"code": code, "error": "无选股后数据"}

    base_price = post_klines[0]["open"]  # 选股次日开盘价
    results = {"code": code, "base_price": base_price, "returns": {}}

    for d in [1, 3, 5, 10, 20]:
        if d <= len(post_klines):
            close = post_klines[d - 1]["close"]
            results["returns"][f"T+{d}"] = round((close / base_price - 1) * 100, 2)

    # 最高/最低
    results["max_return"] = round((max(k["high"] for k in post_klines) / base_price - 1) * 100, 2)
    results["min_return"] = round((min(k["low"] for k in post_klines) / base_price - 1) * 100, 2)

    return results

def run_tracking(days: int = 30) -> list[dict]:
    """执行追踪"""
    TRACK_DIR.mkdir(parents=True, exist_ok=True)
    picks = load_historical_picks(days)
    print(f"读取 {len(picks)} 条历史选股记录")

    results = []
    for i, p in enumerate(picks):
        if not p["code"]:
            continue
        perf = fetch_post_pick_performance(p["code"], p["date"], days=20)
        results.append({**p, **perf})
        if (i + 1) % 10 == 0:
            print(f"  进度: {i+1}/{len(picks)}")

    # 保存
    out = TRACK_DIR / f"tracking_{datetime.now().strftime('%Y%m%d')}.json"
    out.write_text(json.dumps(results, ensure_ascii=False, indent=2))
    print(f"追踪完成，保存到 {out}")
    return results
```

### 3.3 multi_dimension_analysis.py — 多维度分析引擎

```python
"""
多维度分析引擎：对追踪结果进行 7 维度分析。
"""
import json
from collections import defaultdict
from statistics import mean

def analyze(results: list[dict]) -> dict:
    """执行 7 维度分析"""
    return {
        "dim1_strategy": analyze_by_strategy(results),
        "dim2_sector": analyze_by_sector(results),
        "dim3_timeframe": analyze_by_timeframe(results),
        "dim4_mcap": analyze_by_mcap(results),
        "dim5_us_market": analyze_us_market_impact(results),
        "dim6_score": analyze_by_score(results),
        "dim7_errors": analyze_errors(results),
    }

def analyze_by_strategy(results: list[dict]) -> list[dict]:
    """维度1：按策略分析"""
    by_strategy = defaultdict(list)
    for r in results:
        by_strategy[r.get("strategy", "unknown")].append(r)

    output = []
    for strategy, items in by_strategy.items():
        t5_returns = [i["returns"].get("T+5", 0) for i in items if "returns" in i and "T+5" in i["returns"]]
        if not t5_returns:
            continue
        wins = [r for r in t5_returns if r > 0]
        losses = [r for r in t5_returns if r < 0]
        avg_win = mean(wins) if wins else 0
        avg_loss = abs(mean(losses)) if losses else 0
        output.append({
            "strategy": strategy,
            "count": len(items),
            "hit_rate": round(len(wins) / len(t5_returns) * 100, 1),
            "avg_return_t5": round(mean(t5_returns), 2),
            "win_rate": round(len(wins) / len(t5_returns) * 100, 1),
            "profit_loss_ratio": round(avg_win / avg_loss, 2) if avg_loss else float("inf"),
            "best": round(max(t5_returns), 2),
            "worst": round(min(t5_returns), 2),
        })
    return sorted(output, key=lambda x: x["avg_return_t5"], reverse=True)

def analyze_by_timeframe(results: list[dict]) -> list[dict]:
    """维度3：时间窗口分析"""
    timeframes = ["T+1", "T+3", "T+5", "T+10", "T+20"]
    output = []
    for tf in timeframes:
        returns = [r["returns"][tf] for r in results if "returns" in r and tf in r["returns"]]
        if not returns:
            continue
        wins = [r for r in returns if r > 0]
        output.append({
            "timeframe": tf,
            "count": len(returns),
            "avg_return": round(mean(returns), 2),
            "win_rate": round(len(wins) / len(returns) * 100, 1),
            "best": round(max(returns), 2),
            "worst": round(min(returns), 2),
        })
    return output

def analyze_by_score(results: list[dict]) -> list[dict]:
    """维度6：评分分位分析"""
    bands = [(80, 100), (60, 80), (40, 60), (0, 40)]
    output = []
    for lo, hi in bands:
        items = [r for r in results if lo <= r.get("score", 0) < hi and "returns" in r and "T+5" in r["returns"]]
        if not items:
            continue
        returns = [i["returns"]["T+5"] for i in items]
        wins = [r for r in returns if r > 0]
        output.append({
            "score_band": f"{lo}-{hi}",
            "count": len(items),
            "avg_return_t5": round(mean(returns), 2),
            "win_rate": round(len(wins) / len(returns) * 100, 1) if returns else 0,
        })
    return output

def analyze_errors(results: list[dict]) -> list[dict]:
    """维度7：错误分析"""
    errors = []
    for r in results:
        if "returns" not in r or "T+5" not in r["returns"]:
            continue
        ret = r["returns"]["T+5"]
        if ret < -5:
            errors.append({
                "code": r["code"],
                "name": r.get("name", ""),
                "date": r["date"],
                "strategy": r.get("strategy", ""),
                "return_t5": ret,
                "error_type": classify_error(r, ret),
            })
    return sorted(errors, key=lambda x: x["return_t5"])

def classify_error(r: dict, ret: float) -> str:
    """错误分类"""
    if r.get("price_at_pick", 0) > 0:
        # 简单启发式
        pass
    if ret < -10:
        return "大幅下跌"
    elif ret < -5:
        return "持续下跌"
    return "小幅亏损"

# 其他维度分析函数类似...
```

### 3.4 weight_optimizer.py — 权重自动优化

```python
"""
权重自动优化器：基于策略有效性，自动调整各策略权重。
"""
import json

def optimize_weights(analysis: dict, current_config: dict) -> dict:
    """根据分析结果优化权重"""
    strategy_results = analysis.get("dim1_strategy", [])
    if not strategy_results:
        return current_config

    # 按平均收益排序，表现好的加权，表现差的减权
    total_score = 0
    weights = {}
    for s in strategy_results:
        # 综合评分 = 命中率 * 0.4 + 平均收益 * 0.4 + 盈亏比 * 0.2
        score = s["hit_rate"] * 0.4 + max(s["avg_return_t5"], 0) * 0.4 + min(s["profit_loss_ratio"], 3) * 5 * 0.2
        weights[s["strategy"]] = max(score, 1)  # 最低权重 1
        total_score += max(score, 1)

    # 归一化
    for k in weights:
        weights[k] = round(weights[k] / total_score, 3)

    return {
        "old_weights": current_config.get("strategy_weights", {}),
        "new_weights": weights,
        "changes": {k: round(weights[k] - current_config.get("strategy_weights", {}).get(k, 0), 3)
                    for k in weights},
        "rationale": "基于近30天命中率与超额收益自动优化",
    }
```

### 3.5 report_generator.py — 自进化报告生成

```python
"""
自进化报告生成器：输出 Markdown 格式的多维度分析报告。
"""
import json
from datetime import datetime

def generate(analysis: dict, weight_changes: dict, results: list[dict]) -> str:
    """生成自进化报告"""
    md = []
    md.append(f"# AI 选股自进化报告\n")
    md.append(f"> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    md.append(f"> 分析样本：{len(results)} 条选股记录\n")

    # 执行摘要
    md.append("## 一、执行摘要\n")
    t5_returns = [r["returns"]["T+5"] for r in results if "returns" in r and "T+5" in r["returns"]]
    if t5_returns:
        wins = [r for r in t5_returns if r > 0]
        md.append(f"- **T+5 命中率**：{len(wins)/len(t5_returns)*100:.1f}%\n")
        md.append(f"- **T+5 平均收益**：{sum(t5_returns)/len(t5_returns):.2f}%\n")
        md.append(f"- **最佳表现**：{max(t5_returns):.2f}%\n")
        md.append(f"- **最差表现**：{min(t5_returns):.2f}%\n")

    # 维度1：策略有效性
    md.append("## 二、策略有效性分析\n")
    md.append("| 策略 | 推荐数 | 命中率 | 平均收益(T+5) | 胜率 | 盈亏比 | 评级 |\n")
    md.append("|------|-------|-------|-------------|------|-------|------|\n")
    for s in analysis.get("dim1_strategy", []):
        rating = "⭐⭐⭐" if s["hit_rate"] > 60 and s["avg_return_t5"] > 2 else \
                 "⭐⭐" if s["hit_rate"] > 50 else "⭐"
        md.append(f"| {s['strategy']} | {s['count']} | {s['hit_rate']}% | {s['avg_return_t5']}% | {s['win_rate']}% | {s['profit_loss_ratio']} | {rating} |\n")

    # 维度3：时间窗口
    md.append("\n## 三、最佳持有周期\n")
    md.append("| 持有天数 | 平均收益 | 胜率 | 最佳 | 最差 |\n")
    md.append("|---------|---------|------|------|------|\n")
    for tf in analysis.get("dim3_timeframe", []):
        md.append(f"| {tf['timeframe']} | {tf['avg_return']}% | {tf['win_rate']}% | {tf['best']}% | {tf['worst']}% |\n")

    # 维度6：评分分位
    md.append("\n## 四、评分体系有效性\n")
    md.append("| 评分区间 | 标的数 | 平均收益(T+5) | 胜率 |\n")
    md.append("|---------|-------|-------------|------|\n")
    for s in analysis.get("dim6_score", []):
        md.append(f"| {s['score_band']} | {s['count']} | {s['avg_return_t5']}% | {s['win_rate']}% |\n")

    # 维度7：错误分析
    md.append("\n## 五、错误分析（TOP 10 亏损标的）\n")
    md.append("| 代码 | 名称 | 选股日 | 策略 | T+5收益 | 错误类型 |\n")
    md.append("|------|------|-------|------|---------|---------|\n")
    for e in analysis.get("dim7_errors", [])[:10]:
        md.append(f"| {e['code']} | {e['name']} | {e['date']} | {e['strategy']} | {e['return_t5']}% | {e['error_type']} |\n")

    # 权重优化建议
    md.append("\n## 六、策略权重优化建议\n")
    md.append("| 策略 | 旧权重 | 新权重 | 变化 |\n")
    md.append("|------|-------|-------|------|\n")
    for k, v in weight_changes.get("new_weights", {}).items():
        old = weight_changes.get("old_weights", {}).get(k, 0)
        change = weight_changes.get("changes", {}).get(k, 0)
        arrow = "↑" if change > 0 else "↓" if change < 0 else "→"
        md.append(f"| {k} | {old} | {v} | {arrow} {abs(change)} |\n")

    # 行动建议
    md.append("\n## 七、行动建议\n")
    suggestions = generate_suggestions(analysis)
    for i, s in enumerate(suggestions, 1):
        md.append(f"{i}. {s}\n")

    return "".join(md)

def generate_suggestions(analysis: dict) -> list[str]:
    """基于分析结果生成行动建议"""
    suggestions = []
    for s in analysis.get("dim1_strategy", []):
        if s["hit_rate"] < 40:
            suggestions.append(f"⚠️ 策略「{s['strategy']}」命中率仅 {s['hit_rate']}%，建议降低权重或暂停")
        elif s["hit_rate"] > 65:
            suggestions.append(f"✅ 策略「{s['strategy']}」命中率 {s['hit_rate']}%，建议加大权重")

    # 时间窗口建议
    timeframes = analysis.get("dim3_timeframe", [])
    if timeframes:
        best_tf = max(timeframes, key=lambda x: x["avg_return"])
        suggestions.append(f"📊 最佳持有周期为 {best_tf['timeframe']}（平均收益 {best_tf['avg_return']}%），建议以此周期为主")

    # 评分体系
    scores = analysis.get("dim6_score", [])
    if len(scores) >= 2:
        high = [s for s in scores if "80" in s["score_band"]]
        low = [s for s in scores if "0-40" in s["score_band"]]
        if high and low:
            if high[0]["avg_return_t5"] > low[0]["avg_return_t5"]:
                suggestions.append("✅ 评分体系有效：高分标的收益显著优于低分标的")
            else:
                suggestions.append("⚠️ 评分体系失效：高分标的收益未优于低分，需要重新校准评分逻辑")

    return suggestions
```

---

## 四、使用方式

### 4.1 每日选股时自动存档

每日选股报告生成时，同时保存一份 JSON 格式的结构化记录：

```json
{
  "date": "2026-06-12",
  "strategies": {
    "01_strong": [
      {"code": "000001", "name": "平安银行", "score": 72, "price": 12.34, "tags": ["金融", "央国企"]},
      ...
    ],
    "02_capital": [...],
    ...
  },
  "us_market": {"IXIC": 2.54, "SPX": 1.2, ...},
  "holdings": {"159941": {"price": 1.598, "pnl": 33.6}}
}
```

### 4.2 每周自进化分析

```bash
# 1. 拉取选股后实际表现
python3 scripts/evolution/backtest_tracker.py --days=30

# 2. 多维度分析
python3 scripts/evolution/multi_dimension_analysis.py --days=30

# 3. 优化权重
python3 scripts/evolution/weight_optimizer.py --days=30

# 4. 生成报告
python3 scripts/evolution/report_generator.py --days=30

# 一键执行
python3 scripts/evolution/run_all.py --days=30
```

### 4.3 自动化 Schedule（可选）

```yaml
# 每周日 8:00 自动跑自进化分析
cron: "0 8 * * 0"
timezone: Asia/Shanghai
message: "运行 AI 选股自进化分析，读取过去 30 天选股记录，拉取实际表现，多维度分析命中率与收益，输出优化建议到 /workspace/daily_picks/_evolution/ 目录"
```

---

## 五、自进化报告模板

```markdown
# AI 选股自进化报告

> 生成时间：2026-06-16 08:00
> 分析样本：120 条选股记录（2026-05-17 ~ 2026-06-15）

## 一、执行摘要
- T+5 命中率：58.3%
- T+5 平均收益：+1.82%
- 超额收益（vs 沪深300）：+0.55%
- 最佳表现：+18.5%
- 最差表现：-12.3%

## 二、策略有效性
| 策略 | 推荐数 | 命中率 | 平均收益 | 评级 |
|------|-------|-------|---------|------|
| 策略1 强势股 | 30 | 63% | +2.8% | ⭐⭐⭐ |
| 策略6 Serenity | 15 | 60% | +3.5% | ⭐⭐⭐ |
| 策略2 主力资金 | 25 | 56% | +1.2% | ⭐⭐ |
| 策略3 价值股 | 20 | 45% | -0.5% | ⭐ |
...

## 三、最佳持有周期
| 持有天数 | 平均收益 | 胜率 |
|---------|---------|------|
| T+1 | +0.8% | 55% |
| T+3 | +1.5% | 57% |
| T+5 | +1.8% | 58% |  ← 最佳
| T+10 | +1.2% | 52% |
| T+20 | +0.5% | 48% |

## 四、评分体系有效性
| 评分区间 | 标的数 | 平均收益 | 胜率 |
|---------|-------|---------|------|
| 80-100 | 15 | +3.5% | 73% |
| 60-80 | 45 | +2.0% | 60% |
| 40-60 | 40 | +1.0% | 50% |
| 0-40 | 20 | -1.5% | 35% |
✅ 评分体系有效

## 五、错误分析（TOP 10 亏损）
...

## 六、权重优化建议
| 策略 | 旧权重 | 新权重 | 变化 |
|------|-------|-------|------|
| 策略1 | 0.20 | 0.25 | ↑ |
| 策略3 | 0.15 | 0.08 | ↓ |
...

## 七、行动建议
1. ✅ 策略「强势股」命中率 63%，建议加大权重
2. ⚠️ 策略「价值股」命中率 45%，建议降低权重
3. 📊 最佳持有周期为 T+5，建议以此周期为主
4. ✅ 评分体系有效，高分标的收益显著优于低分
5. ⚠️ 近期追高标的亏损较多，建议加入涨幅过滤（涨幅 > 8% 减分）
```

---

## 六、数据流

```
每日选股（7:00）
    ↓ JSON 存档
/workspace/daily_picks/2026-06-12-all.json
    ↓
每周自进化（周日 8:00）
    ↓ 读取 + 拉行情
/workspace/daily_picks/_tracking/tracking_20260616.json
    ↓ 多维分析
/workspace/daily_picks/_evolution/evolution_20260616.json
    ↓ 生成报告
/workspace/daily_picks/_evolution/evolution_20260616.md
    ↓ 优化权重
更新 daily_pick_config.yaml
    ↓
下一周用新参数选股
```

---

## 七、注意事项

1. **数据完整性**：追踪需要选股日之后至少 5 个交易日的行情数据，最近 5 天的选股无法完整追踪
2. **T+1 制度**：选股当日无法买入，以**次日开盘价**为基准计算收益
3. **停牌处理**：选股后停牌的标的，跳过不计入统计
4. **样本量**：建议至少积累 30 天数据后再做自进化分析，样本太少不具统计意义
5. **过拟合风险**：权重优化不要过于激进，每次调整幅度建议 ≤ 30%
6. **市场环境变化**：牛市/熊市策略表现差异大，建议分市场环境分别统计
7. **滑点与手续费**：实际交易有滑点（约 0.1%）和手续费（约 0.05%），回测收益需打折

---

**版本历史**：
- v1.0 (2026-06-16)：初版自进化系统，7 维度分析 + 权重自动优化
