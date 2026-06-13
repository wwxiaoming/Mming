# Checklist

## x1.0 升级版选股手册
- [ ] `/workspace/选股手册_x1.0.md` 已创建
- [ ] 文档第 1-16 章内容与 v1.0 保持一致（交易定位/原则/流程/4 选 1/9 项/6 维/10 条/5 级/6 步/风格/禁止/8 问/今天能不能做/多选一/信息不足/任务目标）
- [ ] 文档第 17 章「量化评分映射」包含五引擎权重 + 4 选 1 阈值映射表
- [ ] 文档第 17 章明确"评分优先于 LLM 主观判断"的冲突解决规则
- [ ] 文档第 18 章「持仓与跨市场联动」包含 159941 持仓流程 + 美股隔夜 + 周末美股周五
- [ ] 文档版本号标注为 x1.0
- [ ] `/workspace/选股手册.md` 文件头已加 v1.0 → x1.0 迁移说明

## x1.0 Python 工程包
- [ ] `/workspace/scripts/x1/__init__.py` 已创建
- [ ] `scripts/x1/environment_gate.py` 实现 S/A/B/C/D 评级函数
- [ ] `scripts/x1/exclusion_filter.py` 实现 10 条排除规则（N1.0 第 7 章）
- [ ] `scripts/x1/conclusion_mapper.py` 实现 4 选 1 映射 + 边缘确认
- [ ] 三个模块均可独立 `python3` 跑通

## v1.7 脚本部署
- [ ] 9 个 v1.7 脚本已移动到 `/workspace/scripts/`
- [ ] `run_daily.sh` 注释加 "（与 cron `30 9 * * 1-5` 对齐）"
- [ ] `run_weekend.sh` 注释加 x1.0 版本标识
- [ ] `bash scripts/run_daily.sh` STEP 1-3 跑通（不报 ImportError）
- [ ] `/workspace/v1.7-stock-trader/` 临时目录已删除

## daily_stock_pick.py 融合改造
- [ ] `main()` 头部接入 environment_gate
- [ ] 策略 8 评分前接入 exclusion_filter
- [ ] 策略 8 输出后接入 conclusion_mapper
- [ ] 输出 JSON 包含 `environment_grade / position_size / candidates_count / excluded_count / conclusions`
- [ ] 周末模式同样接入三件套
- [ ] `--mode=8` 跑通且新字段存在

## post_report.py 四合一
- [ ] 报告含「环境闸门」小节
- [ ] 每只股票后追加 4 选 1 结论 + 条件触发 + 评分映射
- [ ] 输出到 `output/YYYY-MM-DD_早盘潜力股_x1.0.md`（与 v1.7 daily_picks 并存）
- [ ] 休市日处理：标注「休市日，无交易」+ 复用最近交易日数据
- [ ] 报告 ≥ 8 KB

## post_report_weekend.py 同结构
- [ ] 周末报告与工作日同结构（9 项 + 4 选 1 + 环境闸门）
- [ ] 输出到 `output/YYYY-MM-DD_周末展望_x1.0.md`
- [ ] 周末报告 ≥ 6 KB

## auto_publish.py 4 选 1 同步
- [ ] STOCK_CONTEXT.md 摘要含 4 选 1 结论
- [ ] DAILY_LOG.md 9 策略精华后追加 4 选 1 结论表
- [ ] state.json 的 potential5 每条记录含 `conclusion` 字段
- [ ] state.json 是合法 JSON

## 调度任务升级
- [ ] 旧 N1.0 任务 `R5.MLLFO6Z0NXQ` 已 pause
- [ ] 旧任务名加 `(deprecated, x1.0 已接管)` 后缀
- [ ] v1.7 工作日任务 `8HBXYCBRO9_Y55` cron 改为 `30 9 * * 1-5`
- [ ] v1.7 工作日任务名改为 `x1.0 早盘潜力股(工作日9:30)`
- [ ] v1.7 工作日任务消息体升级为 x1.0
- [ ] v1.7 周末任务名改为 `x1.0 周末展望(周日22:00)`
- [ ] v1.7 周末任务消息体升级为 x1.0
- [ ] `Schedule` list 验证 3 个任务状态：旧 paused / 新 2 个 active

## 端到端验证
- [ ] trigger `8HBXYCBRO9_Y55` 一次成功
- [ ] `output/YYYY-MM-DD_早盘潜力股_x1.0.md` 已生成且 ≥ 8 KB
- [ ] `daily_picks/YYYY-MM-DD/state.json` 含 4 选 1 结论
- [ ] `STOCK_CONTEXT.md` 顶部已同步更新
- [ ] `DAILY_LOG.md` 已追加当日 4 选 1 结论表
- [ ] `POSITIONS.md` 159941 行已更新

## 旧 spec 标记
- [ ] `/workspace/.trae/specs/a-stock-daily-pick-automation/spec.md` 文件头加 deprecated 标记
- [ ] 旧 spec 文件保留（不删除）
