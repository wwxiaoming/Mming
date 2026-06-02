# WorldQuant BRAIN 顾问成长与 Alpha 优化研究 Spec

## Why

用户已通过 WorldQuant BRAIN 平台的「6 天 10000 分金牌」方案达成 Gold，目前处于 Consultant 阶段。当前工作流完全依赖「老强说 Alpha 辅助工具 v1.0.5」批量跑 alpha → 工具内筛选可提交 → 直接上交，存在 **重复率高（duplication）、alpha 质量低、长期无法变现** 的核心风险。需要系统性研究官方平台、工具文档、学习任务、IMA 知识库与社区（CSDN 等）资料，输出一份可落地的顾问成长与 alpha 优化路线图。

## What Changes

- 整理 WorldQuant BRAIN 平台的等级体系、顾问晋升路径、奖金机制
- 整理「老强说 Alpha 工具」官方文档与教学视频的核心要点
- 整理用户提供的学习任务文档（kdocs.cn）中的阶段目标与考核点
- 整理 IMA 知识库 + 网易云量化基础音频中的核心金融概念
- 抓取 CSDN / 知乎 / Reddit 等社区的 BRAIN 实战经验帖
- 诊断「工具批量法」的局限性，量化估算重复率与 Sharpe 衰减风险
- 整理 5 类经典 alpha 模式（动量/反转/质量/价值/情绪/波动率）的构造方法
- 给出降低重复率（uniqueness）的具体策略
- 输出一份从「工具跑量」到「顾问盈利」的短/中/长期成长路线图
- 最终以 Markdown 学习指南形式交付到 `.trae/specs/wqbrain-consultant-roadmap/学习记录.md`

## Impact

- Affected specs: 无（纯学习研究记录）
- Affected code: 无

## ADDED Requirements

### Requirement: 理解 BRAIN 平台的等级与变现机制

#### Scenario: 了解等级划分
- **WHEN** 用户查阅本记录
- **THEN** 应了解 BRAIN 的等级（Bronze → Silver → Gold → Consultant）的晋升规则与分数计算公式

#### Scenario: 了解顾问阶段的奖金结构
- **WHEN** 用户达到顾问门槛
- **THEN** 应了解顾问的奖金来源（提交奖金 / 绩效奖金 / 平台分成）
- **AND** 了解「可重复」与「一次性」alpha 在奖金机制上的差异
- **AND** 了解哪些 Region / Dataset 奖金池更大

### Requirement: 理解当前「工具批量法」的局限性

#### Scenario: 了解批量跑 alpha 的风险
- **WHEN** 用户使用老强说工具批量跑 alpha
- **THEN** 应了解平台对 duplication / uniqueness 的检测机制
- **AND** 了解「低质量刷量」在顾问阶段会被识别并影响评分
- **AND** 了解 Sharpe 自相关、Fitness 衰减的常见原因
- **AND** 了解"工业化挖矿"在半年内的 Sharpe 衰减曲线

### Requirement: 掌握 alpha 质量提升方法

#### Scenario: 了解「好 alpha」的结构特征
- **WHEN** 用户学习如何提升 alpha 质量
- **THEN** 应了解 Sharpe、Fitness、Turnover、Drawdown、Returns 的健康区间
- **AND** 了解"逻辑可解释性"对评分的影响
- **AND** 了解如何用 In-sample / Out-of-sample 区分过拟合与真信号

#### Scenario: 了解算子与组合技巧
- **WHEN** 用户编写 alpha 表达式
- **THEN** 应了解算子的金融含义（时序 / 截面 / 向量 三类）
- **AND** 了解 5 类经典 alpha 模式（动量 / 反转 / 质量 / 价值 / 情绪 / 波动率）
- **AND** 了解多数据集交叉验证的方法（如 fundamental × pv1）
- **AND** 了解中性化层级的合理选择（Market / Sector / Industry / Subindustry）

### Requirement: 降低重复率（uniqueness）的具体策略

#### Scenario: 了解重复检测规则
- **WHEN** 用户担心被判定为重复
- **THEN** 应了解 BRAIN 的 duplication 判定标准
- **AND** 了解 uniqueness 在顾问评分中的权重
- **AND** 了解与同 Region 同 Dataset 的常见"撞车点"

#### Scenario: 了解降低重复的技巧
- **WHEN** 用户想提高 alpha 唯一性
- **THEN** 应了解通过换数据集、换中性化层级、换算子组合来制造差异化的方法
- **AND** 了解通过小样本验证快速排除与他人相似的表达式
- **AND** 了解社区常见的"差异化思路"清单

### Requirement: 顾问阶段的成长路线图

#### Scenario: 短期行动（1-3 个月）
- **WHEN** 用户处于顾问初期
- **THEN** 应了解"质量优先"vs"数量优先"的取舍
- **AND** 了解每日提交数量的合理上限
- **AND** 了解立即可执行的高 ROI 学习动作

#### Scenario: 中期目标（3-12 个月）
- **WHEN** 用户稳定顾问 3 个月以上
- **THEN** 应了解如何进入"高奖金池"区域（USA、CHN、ASI）
- **AND** 了解如何从"工具跑"过渡到"自主设计"
- **AND** 了解搭建个人 alpha 库与模板体系的方法

#### Scenario: 长期目标（1 年+）
- **WHEN** 用户成长为高级顾问
- **THEN** 应了解"顾问兼职"与"全职量化研究员"的边界
- **AND** 了解从顾问到 BQP / 自营策略团队的转型路径
- **AND** 了解持续学习的资源清单（论文、播客、社区）

### Requirement: 整合输出最终学习指南

#### Scenario: 文档交付
- **WHEN** 所有研究任务完成
- **THEN** 应在 `.trae/specs/wqbrain-consultant-roadmap/学习记录.md` 输出完整 Markdown 指南
- **AND** 文档应包含：基础概念 / 等级与奖金 / 局限性诊断 / 算子与模式 / 降重策略 / 成长路线图 / 资源清单 等章节
- **AND** 文档语言通俗易懂，适合金融小白，必要时穿插类比与示例
