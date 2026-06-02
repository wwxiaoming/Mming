# Tasks

- [x] Task 1: 搭建 skill 骨架（目录结构 + manifest + 入口识别）
  - [x] SubTask 1.1: 在 `.trae/skills/wqbrain-alpha-quality-helper/` 下创建标准 skill 目录（`SKILL.md`、`references/`、`templates/`）
  - [x] SubTask 1.2: 写 `SKILL.md` 声明触发词、4 个子能力入口、与老强工具的对应关系
  - [x] SubTask 1.3: 写 `manifest.json`（name / version 0.1.0 / depends / entry）

- [x] Task 2: 内置 WQ 平台硬性标准速查表（reference 文档）
  - [x] SubTask 2.1: 写 `references/wq-submission-standards.md`（Sharpe>1.25 / Fitness>1 / SelfCorr<0.7 + 例外条款）
  - [x] SubTask 2.2: 写 `references/kpi-reference.md`（IS Summary 全指标合格线 + 不合格改进方向表）
  - [x] SubTask 2.3: 写 `references/dataset-cheatsheet.md`（截图里 13 个 dataset 的用途与适用策略方向）

- [x] Task 3: 实现 4 个子能力
  - [x] SubTask 3.1: `config-auditor`：接收一/二/三阶段配置文本，输出合理性评分 + 风险点 + 调整建议
  - [x] SubTask 3.2: `expression-preflight`：接收 Fast Expression 文本，输出结构拆解 + 3 大类操作识别 + 改写建议（不少于 3 条）
  - [x] SubTask 3.3: `result-diagnostician`：接收回测 JSON，输出指标逐项解读 + 改进动作清单
  - [x] SubTask 3.4: `submission-strategist`：接收账户画像（用量/余额/进度/已交数），输出当日提交策略

- [x] Task 4: 输出报告模板
  - [x] SubTask 4.1: 写 `templates/audit-report.md`（配置审查报告模板）
  - [x] SubTask 4.2: 写 `templates/diagnosis-report.md`（回测诊断报告模板）

- [x] Task 5: 学习资源索引
  - [x] SubTask 5.1: 写 `references/learning-index.md`（WQ 官方 / 老强教程 / IMA 知识库 / 量化音频 直达链接 + 用途说明）
  - [x] SubTask 5.2: 在 `SKILL.md` 中加 `学习资源` 段，引用上述索引

- [x] Task 6: 验证与冒烟测试
  - [x] SubTask 6.1: 准备 3 个测试用例（典型好配置 / 典型坏配置 / 典型边缘配置）
  - [x] SubTask 6.2: 跑 `config-auditor` 3 个用例，验证输出符合 `templates/audit-report.md` 模板
  - [x] SubTask 6.3: 准备 3 段典型表达式（rank 类 / ts_rank 类 / trade_when 类），跑 `expression-preflight` 验证输出
  - [x] SubTask 6.4: 准备 3 段典型回测 JSON（Sharpe 1.0 / Sharpe 1.5 / Sharpe 0.8），跑 `result-diagnostician` 验证输出

# Task Dependencies
- Task 2 完成后才能开始 Task 3（子能力依赖 reference 文档）
- Task 3 完成后才能开始 Task 6（验证依赖子能力）
- Task 1、Task 4、Task 5 可与 Task 2 并行
