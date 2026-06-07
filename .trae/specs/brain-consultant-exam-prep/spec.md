# BRAIN 顾问问卷备考与速通学习 Spec

## Why

用户已完成 6 天 10000 分金牌方案，已收到 BRAIN Consultant 研究基础知识测试问卷（共 9 题），需要在 1-2 周内高质量完成问卷以进入审核队列。问卷明确要求"严禁直接照抄 AI 生成内容"，因此用户需要**真正理解**每个概念后再用自己的话作答。本项目通过研究官方 Learn 文档、Feishu 速通教程、IMA 知识库、社区资料，整理出**带原理、带案例、带答题思路**的备考指南，帮助用户学习理解、独立作答。

## What Changes

- 整理 WQ 官方 Learn 文档中关于 **Matrix Data vs Vector Data** 的定义、差异与金融含义
- 整理 **Long Count / Short Count** 的数学原理、统计特征探查方法、具体案例
- 整理 **Neutralization（中性化）** 的定义、计算过程、不同层级的数学原理
- 整理 **Alpha Example** 系列文章的复现方法、改进思路、案例库
- 整理 **如何获取 Alpha ID** 的网页操作步骤
- 整理 **Genius 计划各级别与季度奖金范围**
- 抓取并整理 3 个 Feishu 速通教程的内容
- 抓取并整理 IMA 知识库（龙桑版）的相关问答
- 输出一份**带原理 + 带案例 + 带答题思路**的备考指南到 `.trae/specs/brain-consultant-exam-prep/学习记录.md`

## Impact

- Affected specs: 无
- Affected code: 无
- Affected deliverables:
  - `学习记录.md`（最终学习指南）
  - 可选：`参考答题框架.md`（每题的答题思路与要点，但**禁止直接照抄**）

## ADDED Requirements

### Requirement: 理解并能讲清 Matrix Data vs Vector Data

#### Scenario: 掌握两种数据的定义与差异
- **WHEN** 用户复习问卷第 4 题
- **THEN** 应能用通俗语言讲清楚：什么是矩阵数据、什么是向量数据、两者在 BRAIN 平台中的金融含义与典型代表
- **AND** 应能举出至少 3 个矩阵数据字段例子（如 `pv1_close`, `anl4_adjusted_netincome`）和至少 3 个向量数据字段例子（如 `subindustry`, `sector`, `market`）
- **AND** 应能解释为什么中性化是"向量操作"而不是"矩阵操作"

### Requirement: 理解 Long Count / Short Count 的数学原理

#### Scenario: 掌握 long/short count 的概念
- **WHEN** 用户复习问卷第 5 题
- **THEN** 应能讲清楚 long count / short count 的精确定义（在某截面/时序上多头/空头股票数量）
- **AND** 应能给出至少 1 个**具体案例**展示如何用它们探查数据字段的统计特征
- **AND** 应能阐述背后的数学原理（多空头寸分离、信号分布分析）

### Requirement: 理解 Neutralization 的完整计算过程

#### Scenario: 掌握中性化的数学原理
- **WHEN** 用户复习问卷第 6 题
- **THEN** 应能讲清楚中性化的**目的**（消除市场/行业 β）、**计算过程**（分组 → 求均值/标准差 → z-score）
- **AND** 应能讲清楚 4 个层级（Market / Sector / Industry / Subindustry）的差异与适用场景
- **AND** 应能给出至少 1 个手算示例（用 3-5 只股票 + 中性化步骤推演）

### Requirement: 掌握 Alpha Example 的复现与改进

#### Scenario: 能复现并改进一个 alpha
- **WHEN** 用户复习问卷第 7 题
- **THEN** 应能选择一个官方 Alpha Example 完整复现（截图 + 指标 + 复现结果）
- **AND** 应能说出该 example 的金融逻辑、算子选择依据
- **AND** 应能提出至少 1 个**有依据的改进**（换数据集 / 换算子 / 改窗口 / 加过滤）

### Requirement: 掌握获取 Alpha ID 的网页操作

#### Scenario: 能完整描述操作流程
- **WHEN** 用户复习问卷第 8 题
- **THEN** 应能完整描述从登录 BRAIN → 进入 Alphas → 找到某条 alpha → 复制其 ID 的每一步
- **AND** 应能说明 alpha ID 的格式（如 `pw8928lq`）与含义

### Requirement: 掌握 Genius 计划等级与季度奖金范围

#### Scenario: 能列出全部等级与奖金
- **WHEN** 用户复习问卷第 9 题
- **THEN** 应能列出全部 Genius 计划等级（Bronze / Silver / Gold / Consultant / Expert / Master / Grandmaster）
- **AND** 应能说出每个等级对应的季度奖金范围
- **AND** 应能讲清楚顾问阶段与之前阶段的奖金机制差异

### Requirement: 理解并能讲清全部 9 道题

#### Scenario: 完成全部问卷准备
- **WHEN** 用户开始填写问卷
- **THEN** 应能用自己的话、结合案例与原理，逐一回答 9 道题
- **AND** 应保证所有答案都不是直接照抄 AI 生成内容
- **AND** 答案长度应合理（不超字数限制、不太空洞）

### Requirement: 输出最终学习指南

#### Scenario: 文档交付
- **WHEN** 所有研究任务完成
- **THEN** 应在 `.trae/specs/brain-consultant-exam-prep/学习记录.md` 输出完整备考指南
- **AND** 文档应按问卷题号组织（Q1 ~ Q9），每题包含：考点 / 核心概念 / 数学原理 / 案例 / 答题思路 / 避坑提醒
- **AND** 文档语言通俗易懂，适合金融小白
- **AND** 文档**不应包含可以直接照抄的答案**（仅提供思路与原理）
