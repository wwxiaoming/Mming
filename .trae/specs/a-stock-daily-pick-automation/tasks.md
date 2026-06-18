# Tasks

- [x] Task 1: 创建选股手册文档 `选股手册.md`
  - [x] SubTask 1.1: 整合交易定位（市场范围/风格/持仓/目标）
  - [x] SubTask 1.2: 整合核心工作原则（5 条）
  - [x] SubTask 1.3: 整合交易逻辑四步流程（环境→方向→个股→判断）
  - [x] SubTask 1.4: 整合固定输出结构（单只 9 项 + 单只查询 8 问）
  - [x] SubTask 1.5: 整合固定结论枚举（4 类）
  - [x] SubTask 1.6: 整合排序与排除逻辑（6 维排序 + 10 条排除）
  - [x] SubTask 1.7: 整合环境分级与仓位建议（S/A/B/C/D）
  - [x] SubTask 1.8: 整合工作流与表达风格（6 步流程 + 模板 + 规则）
  - [x] SubTask 1.9: 整合禁止事项（10 条）

- [x] Task 2: 创建每日选股自动化任务
  - [x] SubTask 2.1: 使用 `Schedule` 工具创建定时任务（cron: `0 8 * * 1-5`，时区: `Asia/Shanghai`）
  - [x] SubTask 2.2: 任务名称：`A股早盘潜力股筛选-工作日8点`（ID: `EVZB7CF_I11J84`）
  - [x] SubTask 2.3: 任务消息包含完整执行上下文：当日日期、严格遵守 `选股手册.md`、输出到 `output/YYYY-MM-DD_早盘潜力股.md`、使用 `a-stock-data` + `a-share-screener`、输出包含 6 大章节

- [x] Task 3: 验证（手测一次）
  - [x] SubTask 3.1: 使用 `Schedule` 工具的 `trigger` 动作手动触发一次成功（Executions: 1，Last run: 2026-06-13T20:48:08+08:00）
  - [x] SubTask 3.2: 通过 `get` 动作确认 cron / 时区 / 消息 / 名称全部正确（cron `0 8 * * MON-FRI`，时区 `Asia/Shanghai`）
  - [x] SubTask 3.3: 任务消息已包含「市场环境总评」「方向优先级」「个股逐只判断」「最终结论」4 大章节与单只 9 项结构模板

# Task Dependencies

- Task 2 依赖 Task 1（自动化消息需引用已存在的 `选股手册.md`）
- Task 3 依赖 Task 2
