# 世界书条目v4 优化 Spec

## Why

用户拥有 `/workspace/帝王战队资料/世界书条目v4/` 下 85 个 Markdown 形式的帝王战队世界观条目（涵盖 15 位英雄、6 位 NPC、6 个阵营、10 个地区、6 条系统规则、15 件专属装置、6 件道具、16 条剧情线、6 个世界观、2 个组织势力）。这些条目当前存在**配置字段不统一、信息密度参差不齐、关键维度（敏感度/说话风格语料/专属 XP 触发场景）有缺漏、角色之间的认知层级和剧情钩子未对齐**等结构性问题。

用户提供了 5 个 SillyTavern 世界书 JSON 作为**优化基准**：
- `Tavo_小英雄's Lorebook`（52 条，校园异能系）
- `Tavo_夏恋·私奔v3.0's Lorebook`（81 条，恋爱私奔系）
- `Tavo_勇者指引指南 v1 四叶草编年史's Lorebook`（51 条，勇者冒险系）
- `Tavo_异能英雄调教模拟器's Lorebook`（171 条，调教模拟系）
- `Tavo_英雄纪元 淫堕训练师v1.27 MVU`（38 条，英雄调教系）

用户希望**借鉴这 5 个参考世界书在角色结构、敏感度字段、说话风格语料、阶段化调教、路线分支**等维度的成熟写法，**不动 YAML 格式**的前提下，把 85 个 Markdown 条目优化到**与参考世界书同一质量水位**。

## What Changes

- **新增**：基于 5 个参考世界书，提取出一套**条目质量对照清单**（优化评审标准），用于衡量每个 Markdown 条目的覆盖度与可读性。
- **新增**：基于参考世界书模式，归纳一份**条目内容模板**（Markdown 内的章节结构），作为每个 v4 条目的优化目标。
- **新增**：对全部 85 个 Markdown 文件执行**优化评审**，输出**待优化清单**（每条目 + 缺失/薄弱维度）。
- **新增**：对每个 Markdown 文件执行**内容优化**（增补缺失维度、补全说话风格语料、丰富敏感度/XP/路线分支、补充与世界观/剧情/其他英雄的关联钩子）。
- **新增**：在优化后执行**双递归检查 + 引用一致性校验**（避免与已有 `帝王战队v1.58_优化版.json` / `英雄纪元v1.27 MVU` 角色卡内嵌世界书条目产生冲突）。
- **BREAKING**：不动 YAML 格式（`key`/`secondary_keys`/`enabled`/`position`/`order`/`content: |` 块结构保持原样），仅优化 `content: |` 块内的文字与子章节。
- **BREAKING**：不动 Markdown 文件名、目录结构、`enabled`/`position`/`order` 等配置字段。

## Impact

- **Affected specs**：
  - `learn-sillytavern-character-cards`（已完成的 V2 字段学习，作为本任务的字段基础参考）
  - 用户的 `帝王战队v1.58_优化版.json` 和 `英雄纪元 淫堕训练师v1.27 MVU(1).json` 角色卡内嵌世界书（优化后条目应与其兼容而非冲突）
- **Affected code**：
  - `/workspace/帝王战队资料/世界书条目v4/` 下 85 个 `.md` 文件（10 个子目录）
  - 子目录：世界观/、剧情设定/、英雄设定/、NPC设定/、阵营/、地区设定/、系统规则/、专属装置/、道具设定/、组织势力/

## ADDED Requirements

### Requirement: 条目质量对照清单

The system SHALL produce a `quality-checklist.md` document under `.trae/specs/optimize-worldbook-entries-v4/` that defines the optimization evaluation dimensions.

#### Scenario: 清单覆盖所有参考世界书共有的核心维度
- **WHEN** 分析 5 个参考世界书的所有条目共有的章节标题与字段
- **THEN** 清单必须涵盖：基本信息 / 外貌 / 性格（含 core_traits、sexual_traits、speech_patterns）/ 身体特征（含敏感度分区、私处描写）/ 特殊设定 / 说话风格语料 / XP 触发场景 / 路线分支 / 关联钩子（与其他角色/剧情/世界观条目的链接）/ 装备/装置 / 行为模式

#### Scenario: 清单可被逐条对照评分
- **WHEN** 对任一 Markdown 条目执行评审
- **THEN** 每个维度可标记为「完整 / 部分 / 缺失」，并能产出可读的优化建议

### Requirement: 条目内容优化模板

The system SHALL produce a `content-template.md` document that defines the target Markdown content structure for each entry type (hero / NPC / faction / region / device / plot / worldview / rules / organization).

#### Scenario: 模板适配每种条目类型
- **WHEN** 优化某类条目（如英雄设定）
- **THEN** 模板提供该类型专有的章节（如英雄的 `## XP` 与 `## 路线分支`），并保留 YAML 格式外壳不变

#### Scenario: 模板与 5 个参考世界书的内容结构兼容
- **WHEN** 比对模板与任意参考世界书条目的章节
- **THEN** 模板的章节能映射到参考世界书的至少一个字段（如模板的 `## 说话风格语料` 对应参考的 `personality.speech_patterns`）

### Requirement: 85 个 Markdown 条目优化评审

The system SHALL produce a `optimization-audit.md` listing each of the 85 files with its current state and optimization priorities.

#### Scenario: 审计覆盖全部 85 个文件
- **WHEN** 生成审计报告
- **THEN** 报告按子目录分组列出 85 个文件名，并标注每个文件在「条目质量对照清单」中的得分

#### Scenario: 优先级排序合理
- **WHEN** 用户查看审计报告
- **THEN** 关键路径（核心英雄、世界观总纲、收服/补魔/羁绊契约规则、榨精自行车）排在最前；NPC 列表、地区设定排在之后

### Requirement: 85 个 Markdown 条目内容优化

The system SHALL optimize the `content: |` block of each Markdown file based on the audit priorities, without touching the YAML envelope.

#### Scenario: 优化仅限 content 块
- **WHEN** 修改任一 Markdown 文件
- **THEN** `key` / `secondary_keys` / `enabled` / `position` / `order` 字段保持不变；仅 `content: |` 块内的文字与子章节可改

#### Scenario: 优化补全所有缺失维度
- **WHEN** 某条目对照清单存在「缺失」或「部分」维度
- **THEN** 在 `content: |` 块内新增对应章节并填充内容

#### Scenario: 说话风格语料与 XP 触发场景必须新增
- **WHEN** 优化英雄设定类条目
- **THEN** 每个英雄至少有 5 条说话风格语料（覆盖日常/被挑逗/羞耻/自述/与天火互动等场景），以及 2-3 条 XP 触发场景

#### Scenario: 路线分支完整
- **WHEN** 优化剧情设定类条目
- **THEN** 至少包含 `路线A 收服者` / `路线B 小英雄` / `路线C 已收服` 三种路线，每条路线含 3-5 个剧情节点

#### Scenario: 关联钩子显式
- **WHEN** 优化任一条目
- **THEN** 在文末添加 `## 关联条目` 段，列出本条目引用的其他文件路径（用于将来在酒馆中作为绿灯触发器时正确激活）

### Requirement: 双递归与配置兼容性校验

The system SHALL run `--list` on the 2 个角色卡 JSON 与查询所有优化条目使用的 `key` / `secondary_keys`，验证优化后条目与角色卡内嵌世界书无冲突。

#### Scenario: key 引用一致性
- **WHEN** 校验 key 字段
- **THEN** 优化条目使用的 `secondary_keys` 不应与角色卡内嵌条目的 `key` 冲突（避免重复触发或误激活）

#### Scenario: 双递归与配置字段不被修改
- **WHEN** 完成优化
- **THEN** 所有 Markdown 文件的 `enabled` / `position` / `order` 字段与原始版本一致（YAML 格式外壳无变更）
