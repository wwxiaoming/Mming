# Tasks

- [x] Task 1: 创建一夜持股法策略文档 `一夜持股法.md`
  - [x] SubTask 1.1: 写第一章「核心逻辑」（14:30 买 / 10:00 前卖 / 类 T+0 / 高胜率小盈利复利）
  - [x] SubTask 1.2: 写第二章「8 步选股标准」（涨幅3%-5% / 20天涨停 / 量比>1.4 / 换手率5%-10% / 市值50-200亿 / 量能趋势 / K线多头 / 分时站均线）
  - [x] SubTask 1.3: 写第三章「买入纪律」（14:45-14:55 窗口 / 仓位 ≤5成 / 单票 ≤2成 / 最多2只）
  - [x] SubTask 1.4: 写第四章「卖出纪律」（9:30-10:00 清仓 / 止盈3% / 止损-2% / 涨停可持）
  - [x] SubTask 1.5: 写第五章「风控规则」（环境过滤 / 大盘跌>1%暂停 / 单日亏≥2%停止 / 基本面排雷）
  - [x] SubTask 1.6: 写第六章「仓位管理」（单笔≤5% / 每日1-2只 / 大资金降仓）

- [x] Task 2: 创建尾盘选股定时任务
  - [x] SubTask 2.1: 使用 `Schedule` 工具创建定时任务（cron: `30 14 * * 1-5`，时区: `Asia/Shanghai`）
  - [x] SubTask 2.2: 任务名称：`一夜持股法-尾盘选股-14:30`（ID: KDPXFFIVTEVMUS）
  - [x] SubTask 2.3: 任务消息包含完整执行上下文：当日日期、严格遵守 `一夜持股法.md`、输出到 `output/YYYY-MM-DD_尾盘选股.md`、使用 a-stock-data + akshare + limit-up-pool-analyzer + equity-pledge-risk-monitor + sector-rotation-detector、输出包含环境预检 + 8步筛选 + 候选评分 + 操作结论

- [x] Task 3: 创建次日卖出提醒定时任务
  - [x] SubTask 3.1: 使用 `Schedule` 工具创建定时任务（cron: `40 9 * * 1-5`，时区: `Asia/Shanghai`）
  - [x] SubTask 3.2: 任务名称：`一夜持股法-卖出提醒-09:40`（ID: LM6UGJRG83.DJR）
  - [x] SubTask 3.3: 任务消息包含完整执行上下文：读取昨日 `output/YYYY-MM-DD_尾盘选股.md` 推荐标的、拉取实时行情、输出到 `output/YYYY-MM-DD_卖出提醒.md`、包含盈亏计算 + 操作建议

- [x] Task 4: 验证
  - [x] SubTask 4.1: 确认策略文档 6 章完整（258 行，6 个 ## 标题）
  - [x] SubTask 4.2: 确认尾盘选股任务 cron `30 14 * * MON-FRI` / 时区 `Asia/Shanghai` / 消息包含 4 大章节
  - [x] SubTask 4.3: 确认卖出提醒任务 cron `40 9 * * MON-FRI` / 时区 `Asia/Shanghai` / 消息包含 3 大章节

# Task Dependencies

- Task 2 依赖 Task 1（自动化消息需引用已存在的 `一夜持股法.md`）
- Task 3 依赖 Task 2（卖出提醒需读取尾盘选股的输出）
- Task 4 依赖 Task 2 + Task 3
