# Tasks

- [ ] Task 1: 升级选股手册 v1.0 → x1.0
  - [ ] SubTask 1.1: 创建 `/workspace/选股手册_x1.0.md`，复制 v1.0 16 章内容
  - [ ] SubTask 1.2: 在文件尾追加第 17 章「量化评分映射」（4 选 1 与五引擎打分阈值映射表）
  - [ ] SubTask 1.3: 在文件尾追加第 18 章「持仓与跨市场联动」（159941 持仓 + 美股隔夜 + 周末美股周五）
  - [ ] SubTask 1.4: 修改 `/workspace/选股手册.md` 文件头加 v1.0 → x1.0 迁移说明
  - [ ] SubTask 1.5: 验证 `选股手册_x1.0.md` 字数 ≥ 6000 且版本号标注为 x1.0

- [ ] Task 2: 创建 x1.0 Python 工程包
  - [ ] SubTask 2.1: 创建 `/workspace/scripts/x1/__init__.py`
  - [ ] SubTask 2.2: 创建 `scripts/x1/environment_gate.py`，实现 S/A/B/C/D 评级函数 `evaluate(market_data) -> {grade, position_size, skip_stock_pick}`
  - [ ] SubTask 2.3: 创建 `scripts/x1/exclusion_filter.py`，实现 10 条排除规则函数 `filter(stock_list, market_data) -> (passed, excluded_with_reason)`
  - [ ] SubTask 2.4: 创建 `scripts/x1/conclusion_mapper.py`，实现 4 选 1 映射函数 `map(score, sub_metrics) -> {conclusion, condition_trigger, edge_flag}`
  - [ ] SubTask 2.5: 为 x1/ 三个模块写最小单元自测（直接 `python3 scripts/x1/environment_gate.py` 跑通）

- [ ] Task 3: 部署 v1.7 脚本栈到 `/workspace/scripts/`
  - [ ] SubTask 3.1: 移动（mv）9 个文件：`_common.py / us_market_fetcher.py / strategy_holdings_tracker.py / daily_stock_pick.py / post_report.py / post_report_weekend.py / auto_publish.py / run_daily.sh / run_weekend.sh` 从 `/workspace/v1.7-stock-trader/scripts/` 到 `/workspace/scripts/`
  - [ ] SubTask 3.2: 修正 `run_daily.sh` 注释：加 "（与 cron `30 9 * * 1-5` 对齐）" 备注
  - [ ] SubTask 3.3: 修正 `run_weekend.sh` 注释：加 x1.0 版本标识
  - [ ] SubTask 3.4: 验证 `bash scripts/run_daily.sh` 至少能跑通 STEP 1-3（不要求真实数据成功，但要求不报 ImportError）

- [ ] Task 4: 融合 v1.7 评分 + N1.0 闸门（修改 `daily_stock_pick.py`）
  - [ ] SubTask 4.1: 在 `main()` 函数头部加环境闸门调用：`from x1.environment_gate import evaluate as env_eval`
  - [ ] SubTask 4.2: 在 `strategy_8_potential5` 评分前加排除过滤器调用：`from x1.exclusion_filter import filter as exc_filter`
  - [ ] SubTask 4.3: 在策略 8 输出后加结论映射调用：`from x1.conclusion_mapper import map as conc_map`
  - [ ] SubTask 4.4: 在策略 8 输出 JSON 中加字段：`environment_grade / position_size / candidates_count / excluded_count / conclusions`
  - [ ] SubTask 4.5: 在周末模式 (`strategy_weekend_pick`) 中同样接入闸门 + 过滤 + 映射
  - [ ] SubTask 4.6: 验证 `python3 scripts/daily_stock_pick.py --mode=8` 跑通且输出 JSON 包含新字段

- [ ] Task 5: 改造 `post_report.py` 为四合一输出
  - [ ] SubTask 5.1: 修改 `section_potential5_summary` 增加"环境闸门"小节
  - [ ] SubTask 5.2: 修改 `section_per_stock_analysis` 在每只股票后追加"4 选 1 结论"+"条件触发"+"评分映射"
  - [ ] SubTask 5.3: 修改输出路径：除了 `daily_picks/YYYY-MM-DD.md`，再加 `output/YYYY-MM-DD_早盘潜力股_x1.0.md`
  - [ ] SubTask 5.4: 加休市日处理逻辑：从 `STOCK_CONTEXT.md` 读取 `is_trading_day`，若为 False 则改写章节标题为「休市日，无交易」
  - [ ] SubTask 5.5: 验证报告文件 ≥ 8 KB 且包含所有 6 大章节

- [ ] Task 6: 改造 `post_report_weekend.py` 与 x1.0 对齐
  - [ ] SubTask 6.1: 复制工作日报告结构到周末报告（9 项 + 4 选 1 + 环境闸门）
  - [ ] SubTask 6.2: 输出文件改为 `output/YYYY-MM-DD_周末展望_x1.0.md`
  - [ ] SubTask 6.3: 验证周末报告 ≥ 6 KB

- [ ] Task 7: 升级 `auto_publish.py` 同步 4 选 1 结论
  - [ ] SubTask 7.1: 修改 `build_context_snapshot`：在结论中加 4 选 1 摘要
  - [ ] SubTask 7.2: 修改 `build_log_section`：在 9 策略精华后追加 4 选 1 结论表
  - [ ] SubTask 7.3: 修改 `write_state_json`：在 `top_picks.potential5` 每条记录中加 `conclusion` 字段
  - [ ] SubTask 7.4: 验证 `state.json` 是合法 JSON 且能被前端消费

- [ ] Task 8: 升级 3 个调度任务
  - [ ] SubTask 8.1: 用 `Schedule` pause 旧 N1.0 任务 `R5.MLLFO6Z0NXQ`
  - [ ] SubTask 8.2: 用 `Schedule` update `R5.MLLFO6Z0NXQ` 名称加 `(deprecated, x1.0 已接管)`
  - [ ] SubTask 8.3: 用 `Schedule` update `8HBXYCBRO9_Y55`：cron 改为 `30 9 * * 1-5`，名称改为 `x1.0 早盘潜力股(工作日9:30)`，消息体升级为 x1.0
  - [ ] SubTask 8.4: 用 `Schedule` update `Z54UKZQHEQYOIE`：名称改为 `x1.0 周末展望(周日22:00)`，消息体升级为 x1.0
  - [ ] SubTask 8.5: 用 `Schedule` list 验证 3 个任务状态正确（旧 paused、新 active）

- [ ] Task 9: 端到端验证
  - [ ] SubTask 9.1: `Schedule` trigger `8HBXYCBRO9_Y55` 一次（手动验证 cron + 脚本可跑通）
  - [ ] SubTask 9.2: 检查 `output/YYYY-MM-DD_早盘潜力股_x1.0.md` 是否生成且 ≥ 8 KB
  - [ ] SubTask 9.3: 检查 `daily_picks/YYYY-MM-DD/state.json` 是否包含 4 选 1 结论
  - [ ] SubTask 9.4: 检查 `STOCK_CONTEXT.md` 与 `DAILY_LOG.md` 是否同步更新
  - [ ] SubTask 9.5: 验证 `POSITIONS.md` 159941 行已更新

- [ ] Task 10: 标记旧 spec 为 deprecated
  - [ ] SubTask 10.1: 修改 `/workspace/.trae/specs/a-stock-daily-pick-automation/spec.md` 文件头加 deprecated 标记
  - [ ] SubTask 10.2: 不删除旧 spec 文件（保留作为历史参考）

# Task Dependencies

- Task 1（手册）独立，可最先开始
- Task 2（x1 工程包）独立，可最先开始
- Task 3（脚本部署）依赖 Task 2（脚本导入 x1 模块）
- Task 4（daily_stock_pick.py 改造）依赖 Task 2 + Task 3
- Task 5（post_report.py 四合一）依赖 Task 4（需要新字段输出）
- Task 6（post_report_weekend.py）依赖 Task 5（同结构）
- Task 7（auto_publish.py 升级）依赖 Task 5（需要 4 选 1 字段）
- Task 8（调度任务升级）依赖 Task 4-7（消息体引用新产物）
- Task 9（端到端验证）依赖 Task 8
- Task 10（标记 deprecated）独立，可与 Task 8 并行
