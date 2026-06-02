# v4 条目补全 + 异香清理 Spec

## Why

用户在上一轮 `optimize-worldbook-entries-v4` 任务中得到了 85 个优化文件，但因 IDE 会话重置导致工作区丢失了 21 个文件（**专属装置 15 个** + **道具设定 6 个**），且其中部分文件含「异香」与「气味」设定（仅与「问天」相关）。用户希望：
1. **补全缺失的 21 个文件**（专属装置 + 道具设定）
2. **删除所有异香/气味设定**（`01_问天.md` / `01_问天篇.md` / `05_补魔规则.md` 三文件）
3. **保持 YAML 格式外壳不变**，仅修改 `content: |` 块内文字

> **注**：用户消息中提到 `Use Skill: worldquant-brain-alpha-skill 4`，但该 skill 不在当前可用 skill 列表中。本任务使用 `world-book-skill` + `tavern-cards` 完成。

## What Changes

- **新增**：补全 21 个缺失文件
  - 专属装置/01_榨精自行车.md ~ 15_誓约锁链·弱点反噬调教台.md（15 个）
  - 道具设定/01_堕落神装.md ~ 06_战斗装备与武器.md（6 个）
- **修改**：删除异香/气味相关字段（3 个文件）
  - `英雄设定/01_问天.md`：删除"蓝莓异香"体质描述 + 4 处台词/剧情节点中的异香提及
  - `剧情设定/01_问天篇.md`：删除 3 处异香相关剧情节点
  - `系统规则/05_补魔规则.md`：清理气味相关表述
- **BREAKING**：不动 YAML 格式外壳（`key` / `secondary_keys` / `enabled` / `position` / `order`）
- **BREAKING**：不动 `key` 字段名称（如 `key: "问天"` 保留，**不**因"删除异香"而改 `key` 值）

## Impact

- **Affected specs**：
  - `optimize-worldbook-entries-v4`（上轮任务，作为基础参考）
- **Affected code**：
  - 缺失文件：21 个（需新建）
  - 异香清理：3 个文件（`英雄设定/01_问天.md`、`剧情设定/01_问天篇.md`、`系统规则/05_补魔规则.md`）
  - 总计：24 个文件变更

## ADDED Requirements

### Requirement: 补全 21 个缺失文件

The system SHALL create the 21 missing files with the same YAML format as existing files (each starts with ` ```yaml `, has `key` / `secondary_keys` / `enabled` / `position` / `order` / `content: |` fields, and ends with ` ``` `).

#### Scenario: 专属装置 15 个文件创建完成
- **WHEN** 处理 `专属装置/` 目录
- **THEN** 15 个文件全部存在，每个文件含：
  - 装置概述（名称/类型/适用英雄/获取方式）
  - 核心组件（3-5 个模块）
  - 核心机制（3-4 种状态模式 + 联动机制）
  - 在三条路线中的状态
  - 关联条目（3+ 个真实相对路径）

#### Scenario: 道具设定 6 个文件创建完成
- **WHEN** 处理 `道具设定/` 目录
- **THEN** 6 个文件全部存在，每个文件含：
  - 物品概述（名称/类型/适用角色/获取方式）
  - 核心功能（战斗/调教/隐藏）
  - 使用机制（触发条件/持续时间/副作用）
  - 在三条路线中的状态
  - 关联条目（3+ 个真实相对路径）

### Requirement: 删除异香/气味设定

The system SHALL remove all 异香 and 气味 references from the 3 affected files, without changing the YAML envelope.

#### Scenario: 问天.md 不含异香
- **WHEN** 修改 `英雄设定/01_问天.md`
- **THEN** 全文 `grep "异香"` 返回 0 行；`蓝莓异香` 体质描述被替换为"敏感体质"或类似中性表述

#### Scenario: 问天篇.md 不含异香
- **WHEN** 修改 `剧情设定/01_问天篇.md`
- **THEN** 全文 `grep "异香"` 返回 0 行；3 处异香相关剧情节点被重写（去除异香触发，保留足部敏感的核心冲突）

#### Scenario: 补魔规则.md 不含气味
- **WHEN** 修改 `系统规则/05_补魔规则.md`
- **THEN** 全文 `grep "气味"` 返回 0 行

### Requirement: 补全后总文件数达 85

The system SHALL ensure the final file count in `世界书条目v4/` reaches 85 (10 subdirectories).

#### Scenario: 完整盘点
- **WHEN** 优化执行完成
- **THEN** `find /workspace/帝王战队资料/世界书条目v4/ -name "*.md" | wc -l` 输出 85
- **THEN** 3 个修改文件 `grep "异香\|气味"` 全部返回 0 行

## MODIFIED Requirements

### Requirement: YAML 格式外壳保持

**Complete modified requirement**：所有 24 个文件（21 新建 + 3 修改）的 `key` / `secondary_keys` / `enabled` / `position` / `order` 字段保持不变（新建文件的字段值从 `optimize-worldbook-entries-v4/optimization-audit.md` 推断）。

## REMOVED Requirements

### Requirement: 问天的"蓝莓异香"体质
**Reason**：用户明确要求删除所有异香/气味设定。"蓝莓异香"作为问天的标志性体质，需要从英雄设定、剧情篇、补魔规则中全面清除。
**Migration**：
- 在 `英雄设定/01_问天.md` 中，"拥有'蓝莓异香'体质"改为"足部神经末梢密度极高，对气味刺激反应敏锐"（保留核心敏感度机制，去除"散发异香"的设定）
- 在 `剧情设定/01_问天篇.md` 中，"被迫承认蓝莓异香"改为"被迫承认足部高度敏感"
- 在 `系统规则/05_补魔规则.md` 中，涉及"气味"的描述改为"能量波动"或"魔力反应"
