# 早盘潜力股自动化

依据 [`/workspace/选股手册.md`](../选股手册.md) **v2.0** 编写的 A 股短线选股自动化脚本。

## 文件清单

| 文件 | 用途 |
|------|------|
| `daily_pick.py` | 主入口：数据拉取 → 评级 → 候选分析 → Markdown 报告 |
| `requirements.txt` | Python 依赖清单 |

## 触发方式

**TRAE 定时任务**（cron）：

```
0 8 * * 1-5   # 周一至周五 08:00（Asia/Shanghai）
```

会话消息模板见 `/workspace/.trae/specs/a-stock-daily-pick-automation/` 中的 `tasks.md`。

## 运行

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 直接运行（生成当日报告）
python daily_pick.py

# 3. 指定日期
python daily_pick.py --date 2026-06-16

# 4. 仅打印不写文件
python daily_pick.py --dry-run
```

## 输出

- 文件路径：`/workspace/output/YYYY-MM-DD_早盘潜力股.md`
- 日志路径：`/workspace/logs/YYYY-MM-DD.log`
- 缓存路径：`/workspace/data/cache/`（北向资金等本地缓存）

## 数据源

严格遵守手册附录 B「数据源优先级」：

| 层级 | 数据源 | 用途 |
|------|--------|------|
| 1 | mootdx（TCP 7709） | 备用：K线/财务/F10 |
| 2 | 腾讯财经（HTTP） | 指数/个股 PE/PB/市值 |
| 3 | 东财 datacenter | 龙虎榜/解禁/股东户数/融资融券 |
| 4 | 东财 push2/push2his | 行业排名/120日资金流/板块归属 |
| 7 | 同花顺热点 | 当日强势股 + 题材归因 |
| 8 | 同花顺 hsgtApi | 北向资金 |

**防封**：所有 eastmoney.com 走 `em_get()` 串行限流，间隔 ≥ 1.5s + 随机抖动。

## 多源交叉验证

任何"亮点"必须 ≥ 2 个独立数据源相互印证，单源信号降级一档（手册第二章第 6 条）。

## 兜底顺序

主数据源不可用时，按手册附录 A 顺序兜底：
1. `eastmoney_select_stock`（板块/成分股）
2. `a-share-screener`（批量筛选结果）
3. `last30days`（舆情热度）
4. 仍不足 → 标注「数据缺失，结论仅作初步判断」

## 维护

- 修改交易逻辑 → 同步更新 `/workspace/选股手册.md` 并在附录 F 记录 changelog
- 新增/废弃数据源 → 更新本目录 `requirements.txt` + 手册附录 B
- 节假日表更新 → 修改 `daily_pick.py` 中 `is_trading_day()` 的 `closed` 集合
