# x1.0 融合版自动化选股系统 Spec

## Why

用户已同时维护两条自动化选股链路，但二者在「方法论深度」与「工程可执行性」上各执一端：
- **N1.0（手册驱动）**：沉淀了 16 章交易手册 + 4 选 1 结论枚举 + 10 条排除规则 + S/A/B/C/D 环境闸门，**纪律强、风险前置清晰**，但执行层是纯 prompt，依赖 LLM 现场发挥，**评分主观漂移、无持仓联动、无美股联动**。
- **v1.7.0（脚本驱动）**：实现了 9 策略并行 + 五引擎加权打分 + 8b 深度分析 + 159941 持仓跟踪 + 美股隔夜 + 6 通道写出，**工程闭环、可复现**，但**缺少环境闸门、无强制结论枚举、无排除规则硬过滤、cron 时间与脚本注释打架**。

本次升级目标：**把 N1.0 的「方法论纪律」下沉为 v1.7 的「代码硬约束」**，形成一套"手册闸门 + 量化打分 + 工程闭环 + 持仓/美股联动 + 6 通道写盘 + 休市日处理 + 周末展望"为一体的 **x1.0 融合版**，作为后续所有自动化选股的唯一基线。

## What Changes

- **新增** 升级版选股手册 `选股手册_x1.0.md`：在 N1.0 v1.0 手册基础上新增第 17 章「量化评分映射」+ 第 18 章「持仓与跨市场联动」，明确 4 选 1 结论与五引擎打分的双向映射关系
- **新增** Python 工程包 `scripts/x1/`：在 v1.7 脚本栈基础上新增环境闸门模块、排除规则过滤器、结论枚举映射器、双源数据 fallback
- **修改** `scripts/daily_stock_pick.py`：在 `strategy_8_potential5` 评分前加 S/A/B/C/D 环境评级 + 10 条排除规则，评分后强制映射 4 选 1 结论
- **修改** `scripts/post_report.py`：报告每只股票按"N1.0 9 项结构 + v1.7 五引擎评分 + 4 选 1 结论 + emoji 风险标记"四合一输出
- **修改** `scripts/run_daily.sh`：注释时间从 09:30 修正为 07:30（与调度任务一致），并新增 `x1_mode=on` 环境变量
- **修改** `scripts/run_weekend.sh`：周末报告与工作日报告同结构（9 项 + 4 选 1）
- **修改** 调度任务 `8HBXYCBRO9_Y55`：cron 修正为 `30 9 * * 1-5`（开盘时，匹配脚本注释），消息体升级为 x1.0 双驱动版
- **修改** 调度任务 `Z54UKZQHEQYOIE`：消息体升级为 x1.0 周末展望版
- **修改** N1.0 旧任务 `R5.MLLFO6Z0NXQ` (EVZB7CF_I11J84)：标记为 deprecated，**暂停而非删除**（保留作为 fallback）
- **新增** `scripts/x1/environment_gate.py`：S/A/B/C/D 五级环境评级（基于指数/情绪/连板/量能/主线热度）
- **新增** `scripts/x1/exclusion_filter.py`：10 条排除规则的脚本化实现（高位加速/缩量硬质/题材发散等）
- **新增** `scripts/x1/conclusion_mapper.py`：五引擎评分 → 4 选 1 结论映射表
- **新增** `output/YYYY-MM-DD_早盘潜力股_x1.0.md`：x1.0 工作日主报告
- **新增** `output/YYYY-MM-DD_周末展望_x1.0.md`：x1.0 周末报告
- **修改** `选股手册.md`：在文件头加 v1.0 → x1.0 迁移说明

## Impact

- Affected specs:
  - `a-stock-daily-pick-automation/`（旧 N1.0 spec，标记为 deprecated）
- Affected code:
  - `/workspace/选股手册.md`（升级 v1.0 → x1.0 标注）
  - `/workspace/选股手册_x1.0.md`（新建）
  - `/workspace/scripts/daily_stock_pick.py`（前置闸门 + 后置结论映射）
  - `/workspace/scripts/post_report.py`（四合一输出）
  - `/workspace/scripts/post_report_weekend.py`（同结构）
  - `/workspace/scripts/run_daily.sh`（注释 + 环境变量）
  - `/workspace/scripts/run_weekend.sh`（同结构）
  - `/workspace/scripts/x1/environment_gate.py`（新建）
  - `/workspace/scripts/x1/exclusion_filter.py`（新建）
  - `/workspace/scripts/x1/conclusion_mapper.py`（新建）
  - `/workspace/output/`（新输出目录）
- Affected schedules:
  - 旧 N1.0 任务 `R5.MLLFO6Z0NXQ`（暂停）
  - v1.7 工作日任务 `8HBXYCBRO9_Y55`（更新 cron + 消息）
  - v1.7 周末任务 `Z54UKZQHEQYOIE`（更新消息）

## ADDED Requirements

### Requirement: x1.0 升级版选股手册

系统 SHALL 提供一份升级版选股手册 `选股手册_x1.0.md`，在 v1.0 16 章基础上新增量化评分与跨市场联动两章。

#### Scenario: 手册覆盖原有 16 章
- **WHEN** 用户查阅 `选股手册_x1.0.md` 第 1-16 章
- **THEN** 应包含与 v1.0 手册一致的全部内容：交易定位、5 条原则、四步流程、4 选 1 结论、9 项输出结构、6 维排序、10 条排除、5 级环境、6 步工作流、表达风格、禁止事项、单只查询 8 问、"今天能不能做"模板、多选一比较、信息不足处理、任务目标
- **AND** 不允许删除或弱化 v1.0 任何原条款

#### Scenario: 第 17 章定义五引擎评分映射
- **WHEN** 用户查阅 `选股手册_x1.0.md` 第 17 章「量化评分映射」
- **THEN** 应包含：位置 0.20 + 估值 0.15 + 资金 0.30 + 题材 0.20 + 美股 0.15 的权重定义
- **AND** 应明确 4 选 1 结论与评分阈值的映射表：
  - 评分 ≥ 0.70 → **可直接试仓买入**
  - 评分 0.50~0.70 → **条件满足才可买入**
  - 评分 0.25~0.50 → **只可观察，不可买**
  - 评分 < 0.25 → **明确不买**
- **AND** 应明确"评分"与"LLM 主观判断"同时存在时的优先级：**评分优先**（当 LLM 主观判断与评分冲突时，以评分为准，并在结论理由中说明）

#### Scenario: 第 18 章定义持仓与跨市场联动
- **WHEN** 用户查阅 `选股手册_x1.0.md` 第 18 章「持仓与跨市场联动」
- **THEN** 应包含：① 持仓（159941 成本 1.623 / 700 股）盈亏跟踪流程 ② 美股隔夜（NDX/SPX/DJI/SOX）对 A 股科技股的联动权重 ③ 周末美股周五收盘对周一开盘的预测流程
- **AND** 应明确"持仓 + 潜力股 TOP 5"必须**同日**出现在报告中（持仓在前，TOP 5 在后）

#### Scenario: 手册版本号升级
- **WHEN** 用户查阅手册文件尾
- **THEN** 版本号 SHALL 为 `x1.0`
- **AND** SHALL 注明"基于 v1.0 升级，融合 v1.7.0 量化打分"

### Requirement: x1.0 Python 工程包

系统 SHALL 在 `/workspace/scripts/x1/` 下提供三个新增模块，作为融合版的"工程硬约束"。

#### Scenario: 环境闸门模块
- **WHEN** 调用 `scripts/x1/environment_gate.py evaluate(market_data)`
- **THEN** 应输出 S/A/B/C/D 五级评级（基于指数涨跌幅、情绪指数、连板梯队、量能、热点持续性 5 个输入）
- **AND** 应输出对应仓位建议（积极/轻仓/严格控制/观察/空仓）
- **AND** 评级 D SHALL 返回 `skip_stock_pick=True`（下游评分模块据此直接出空仓报告）

#### Scenario: 排除规则过滤器
- **WHEN** 调用 `scripts/x1/exclusion_filter.py filter(stock_list, market_data)`
- **THEN** 应应用 N1.0 第 7 章 10 条排除规则，移除不符合的标的
- **AND** 应输出被排除标的的清单与排除原因（每条规则对应一个 reason code）
- **AND** 排除规则 SHALL 包括：① 高位加速（涨幅 > 6%）② 缩量硬质（换手 < 1.5% 且 vol_ratio < 0.8）③ 高开过多（开盘涨幅 > 5%）④ 逻辑不清（题材 reason 为空）⑤ 题材发散（单一题材 > 50%）⑥ 非前排（不在板块 TOP 3）⑦ 板块持续性存疑（5 日板块涨跌 < -2%）⑧ 环境不支持（闸门评级为 D）⑨ 冲高回落历史（最近 5 日 K 线 3 根上影线 > 5%）⑩ 模式不匹配（持仓周期 > 短线）

#### Scenario: 结论枚举映射器
- **WHEN** 调用 `scripts/x1/conclusion_mapper.py map(score, sub_metrics)`
- **THEN** 应输出 4 选 1 结论（score ≥ 0.70 → 可直接试仓买入；0.50~0.70 → 条件满足才可买入；0.25~0.50 → 只可观察，不可买；< 0.25 → 明确不买）
- **AND** 应输出对应的"条件触发"提示（仅当结论为"条件满足"时）
- **AND** 应在 score 边缘（0.65~0.75）触发 LLM 二次确认，输出"评分边缘待确认"标记

### Requirement: 融合版评分流程

系统 SHALL 在 `scripts/daily_stock_pick.py` 中实现"环境闸门 → 排除规则 → 五引擎评分 → 结论映射"四步流程。

#### Scenario: 工作日评分流程
- **WHEN** 调用 `python3 scripts/daily_stock_pick.py --mode=8`
- **THEN** 应依次执行：① 读取指数/情绪/量能数据 → 调 `environment_gate` 拿 S/A/B/C/D ② 读取 WATCH_UNIVERSE → 调 `exclusion_filter` 过滤 → 输出候选池 ③ 对候选池跑 `strategy_8_potential5` 五引擎打分 → 输出 TOP 5 ④ 对 TOP 5 调 `conclusion_mapper` 映射 4 选 1 结论
- **AND** 若环境闸门评级为 D，应跳过步骤 ②③④，直接返回空仓报告
- **AND** 输出 JSON SHALL 包含字段：`environment_grade`、`position_size`、`candidates_count`、`top5`、`conclusions`、`excluded_list`

#### Scenario: 周末评分流程
- **WHEN** 调用 `python3 scripts/daily_stock_pick.py --mode=weekend`
- **THEN** 应使用 4 引擎（行业 0.30 + 资金 0.30 + 美股 0.15 + 资讯 0.10 + 估值 0.15）跑周一潜力股 TOP 5
- **AND** 应复用相同的 `environment_gate`（周末环境基于行业 + 资金 + 美股周五收盘）
- **AND** 输出结构与工作日一致（9 项 + 4 选 1 结论）

### Requirement: 四合一报告输出

系统 SHALL 在 `scripts/post_report.py` 中实现"N1.0 9 项结构 + v1.7 五引擎评分 + 4 选 1 结论 + emoji 风险标记"四合一输出。

#### Scenario: 工作日主报告
- **WHEN** 调用 `python3 scripts/post_report.py`
- **THEN** 输出文件 SHALL 同时包含：① v1.7 五引擎评分表 ② v1.7 持仓跟踪（159941）③ v1.7 美股隔夜 ④ N1.0 9 项结构（每只 TOP 5） ⑤ N1.0 4 选 1 结论 ⑥ emoji 风险标记（🟢/🟡/🔴/⚪）
- **AND** 输出文件 SHALL 保存到 `output/YYYY-MM-DD_早盘潜力股_x1.0.md`（与 v1.7 的 `daily_picks/YYYY-MM-DD.md` 并存）
- **AND** 文件大小 SHALL ≥ 8 KB（确保深度分析不被截断）

#### Scenario: 周末报告
- **WHEN** 调用 `python3 scripts/post_report_weekend.py`
- **THEN** 输出文件 SHALL 保存到 `output/YYYY-MM-DD_周末展望_x1.0.md`
- **AND** 报告章节 SHALL 包含：美股周五收盘 / 周一潜力股 TOP 5（9 项 + 4 选 1） / 周末 7×24 资讯 / 159941 持仓跟踪 / 风险点

#### Scenario: 休市日处理
- **WHEN** 当日为 A 股法定节假日或临时休市日
- **THEN** 工作日报告 SHALL 在「市场环境总评」中明确标注「休市日，无交易」
- **AND** TOP 5 SHALL 标注为「仅作研究跟踪，不构成交易建议」
- **AND** 5 支标的 SHALL 复用最近一个交易日的数据，并在文末注明数据日期

### Requirement: 6 通道 + 4 选 1 报告写出

系统 SHALL 在 x1.0 工作流中保留 v1.7 的 6 通道自动写出，并在 `auto_publish.py` 中新增 4 选 1 结论同步到 `STOCK_CONTEXT.md` 与 `DAILY_LOG.md`。

#### Scenario: 通道 1：本地 Markdown + summary + state.json
- **WHEN** `auto_publish.py` 跑完
- **THEN** SHALL 写：`daily_picks/YYYY-MM-DD/{md, summary.txt, console.txt, state.json}` 与 `output/YYYY-MM-DD_早盘潜力股_x1.0.md`

#### Scenario: 通道 2：POSITIONS.md
- **WHEN** `auto_publish.py` 跑完
- **THEN** SHALL 更新 `/workspace/POSITIONS.md` 中 159941 行的现价 / 当日盈亏 / 累计盈亏

#### Scenario: 通道 3：DAILY_LOG.md
- **WHEN** `auto_publish.py` 跑完
- **THEN** SHALL 在 `## YYYY-MM-DD` 区块下追加：美股隔夜、159941 持仓、TOP 5（含 4 选 1 结论）、风险点

#### Scenario: 通道 4：STOCK_CONTEXT.md
- **WHEN** `auto_publish.py` 跑完
- **THEN** SHALL 在「最近一次更新」区块更新：环境评级（S/A/B/C/D）、持仓汇总、TOP 3、4 选 1 结论摘要

#### Scenario: 通道 5：飞书 Webhook
- **WHEN** `FEISHU_WEBHOOK` 环境变量已设置
- **THEN** SHALL 推送摘要（持仓 + TOP 5 4 选 1 结论 + 风险等级 emoji）

#### Scenario: 通道 6：state.json 前端可消费
- **WHEN** `auto_publish.py` 跑完
- **THEN** SHALL 写 `daily_picks/YYYY-MM-DD/state.json`，包含字段：`environment_grade`、`holdings_159941`、`top5_picks`（含 `conclusion` 与 `score`）

### Requirement: 调度任务升级

系统 SHALL 升级现有 3 个调度任务：暂停 N1.0 旧任务，更新 v1.7 工作日 + 周末任务为 x1.0 版本。

#### Scenario: 暂停 N1.0 旧任务
- **WHEN** 本 spec 实施完成
- **THEN** `Schedule` 工具 SHALL 对 `R5.MLLFO6Z0NXQ` 执行 `pause` 动作
- **AND** 任务名 SHALL 改为 `N1.0 (deprecated, x1.0 已接管)`
- **AND** 不删除（保留 fallback）

#### Scenario: 更新 v1.7 工作日任务为 x1.0
- **WHEN** 本 spec 实施完成
- **THEN** `Schedule` 工具 SHALL 对 `8HBXYCBRO9_Y55` 执行 `update` 动作
- **AND** cron SHALL 修正为 `30 9 * * 1-5`（开盘时，与脚本注释一致）
- **AND** 任务名 SHALL 改为 `x1.0 早盘潜力股(工作日9:30)`
- **AND** 消息体 SHALL 升级为：① 当日日期 ② 严格遵守 `选股手册_x1.0.md` ③ 使用 x1.0 融合版脚本栈 ④ 输出 `output/YYYY-MM-DD_早盘潜力股_x1.0.md` + `daily_picks/YYYY-MM-DD/`

#### Scenario: 更新 v1.7 周末任务为 x1.0
- **WHEN** 本 spec 实施完成
- **THEN** `Schedule` 工具 SHALL 对 `Z54UKZQHEQYOIE` 执行 `update` 动作
- **AND** 任务名 SHALL 改为 `x1.0 周末展望(周日22:00)`
- **AND** 消息体 SHALL 升级为：① 当日日期 ② 严格遵守 `选股手册_x1.0.md` ③ 周末模式 ④ 输出 `output/YYYY-MM-DD_周末展望_x1.0.md`

### Requirement: 脚本部署与修正

系统 SHALL 将 `v1.7-stock-trader/scripts/` 下的 9 个 Python/sh 文件部署到 `/workspace/scripts/`，并修正 cron 注释与脚本注释的一致性。

#### Scenario: 脚本部署
- **WHEN** 本 spec 实施完成
- **THEN** SHALL 移动（而非复制）：`_common.py` / `us_market_fetcher.py` / `strategy_holdings_tracker.py` / `daily_stock_pick.py` / `post_report.py` / `post_report_weekend.py` / `auto_publish.py` / `run_daily.sh` / `run_weekend.sh` 到 `/workspace/scripts/`
- **AND** SHALL 新建 `/workspace/scripts/x1/` 子目录
- **AND** SHALL 删除 `/workspace/v1.7-stock-trader/` 临时目录

#### Scenario: run_daily.sh 注释与 cron 对齐
- **WHEN** 脚本被修改
- **THEN** `run_daily.sh` 注释 SHALL 由 "工作日 09:30" 改为 "工作日 09:30"（保留）+ 加 "（与 cron `30 9 * * 1-5` 对齐）" 备注
- **AND** 调度任务 `8HBXYCBRO9_Y55` 的 cron 也对齐为 `30 9 * * 1-5`

#### Scenario: 持仓参数同步
- **WHEN** 脚本被修改
- **THEN** `run_daily.sh` 与 `run_weekend.sh` 中的 `HOLDINGS_COST="1.623"` SHALL 保持（与 `POSITIONS.md` 一致）

## MODIFIED Requirements

### Requirement: 旧 N1.0 spec 标记为 deprecated

**REASON**: x1.0 融合版已接管选股自动化全部职责，N1.0 spec（`a-stock-daily-pick-automation/`）仅作为历史参考保留。
**MODIFIED**: `a-stock-daily-pick-automation/spec.md` SHALL 在文件头加 `> **DEPRECATED**: 本 spec 已被 x1.0 融合版取代，请参阅 `.trae/specs/x1-0-fusion-trader/spec.md`。
**MIGRATION**: 所有 `a-stock-daily-pick-automation` 引用的调度任务暂停后保留；后续若需回滚可手动 resume。

## REMOVED Requirements

无（无删除项）。
