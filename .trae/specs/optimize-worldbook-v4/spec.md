# 优化《帝王战队资料·世界书条目v4》 Spec

## Why

用户的《帝王战队资料》项目已积累 85 个世界书条目（v4 版本），分散在 10 个分类目录中。当前存在三类问题：

1. **配置层缺陷** — 多数条目缺少 `constant`、`preventRecursion`、`excludeRecursion`、`scanDepth` 等关键配置项。与 4 个参考世界书对比，参考 Tavo_异能英雄调教模拟器 171 个条目中有 161 个配置了双递归，Tavo_勇者指引指南 51 个条目中有 45 个配置双递归；而当前 v4 条目几乎无配置。
2. **内容质量参差** — 部分条目存在"作者视角解释"、万能美人描写、八股化、性格标签化等问题；另一些条目（如榨精自行车）则结构清晰、机制明确，参考价值高。
3. **格式不一致** — 文件结构混杂（部分用 `xml` 包裹，部分裸 `yaml`，部分缺闭合标签）；关键词使用中文逗号 + 空格（`问天, 秩序之子`），触发失败风险高。

用户明确要求：**暂不修改 YAML 格式**，仅基于 4 个参考世界书的最佳实践做内容与配置优化。

## What Changes

### 4 个参考世界书

| 参考书 | 条目数 | 关键模式 |
|--------|-------|----------|
| Tavo_小英雄's Lorebook | 52 | 位置 0 为主、少量位置 4 作行为指导；无双递归配置（不推荐） |
| Tavo_夏恋·私奔v3.0 | 81 | 位置 0/4 混合；55/81 启用 excludeRecursion |
| Tavo_勇者指引指南 v1 | 51 | 35 个位置 0（世界观）+ 16 个位置 4（行为指导）；45/51 启双递归 |
| Tavo_异能英雄调教模拟器 | 171 | **9 个位置 0（世界观蓝灯）+ 162 个位置 4（角色/场景绿灯）**；161/171 启双递归 |

**主要借鉴目标**：Tavo_异能英雄调教模拟器（主题最接近：英雄+调教+多角色），采用其**「世界观蓝灯置 0 + 角色/场景绿灯置 4」**的分层结构与全套双递归配置。

### 优化范围（85 个条目全量优化）

- 不新增/不删除条目
- 保留 YAML 格式（代码块+YAML 内容）
- 在每个 YAML 块顶部补全 `constant`、`preventRecursion`、`excludeRecursion`、`scanDepth` 字段
- 修正 `keys` 字段：英文逗号分隔、去空格、覆盖全称呼
- 按参考书最佳实践重写内容：补全结构、清理禁词、强化白描
- 对每个分类应用差异化的配置策略

### 不修改的内容

- YAML 整体代码块结构（保留 ```yaml 或 ```xml>```yaml 包裹）
- 文件命名、目录结构
- 字段命名（key/keys/secondary_keys/content）
- 用户的具体剧情设定、角色设定（仅做表述优化，不改设定）

## Impact

- **Affected specs**:
  - 学习记录（SillyTavern 角色卡基础）
  - wq-brain-tutorial-usage（教程用法）
  - wq-brain-compliance-guide（合规指南）
- **Affected code（文件）**:
  - `/workspace/帝王战队资料/世界书条目v4/` 下 85 个 `.md` 条目
  - 不涉及任何代码逻辑变更

## ADDED Requirements

### Requirement: 条目配置标准化

每个 YAML 块必须包含 6 个配置字段，且依据条目类型采用差异化策略。

#### Scenario: 世界观核心条目（蓝灯+位置 0）

- **WHEN** 条目属于世界观/总纲/系统层（例：00_世界观总纲、01_帝王战队、02_神魔号系统）
- **THEN** 配置为 `position: 0`, `constant: true`, `preventRecursion: true`, `excludeRecursion: true`, 无 `keys` 字段
- **AND** 此类条目 AI 始终可见，作为全局基础设定

#### Scenario: 角色/英雄/场景条目（绿灯+位置 4）

- **WHEN** 条目为角色详情、场景/地区、NPC、剧情篇章、专属装置、道具
- **THEN** 配置为 `position: 4`, `depth: 0`, `role: 0`, `constant: false`, `preventRecursion: true`, `excludeRecursion: true`, `scanDepth: 2`
- **AND** 必须有 `keys` 字段，英文逗号分隔，覆盖全名+昵称+外号
- **AND** 位置 4（@D 深度 0）是参考书中最高优先级注入点

#### Scenario: 系统规则条目（蓝灯+位置 0）

- **WHEN** 条目为收服规则、战斗规则、补魔规则、羁绊契约等机械性规则
- **THEN** 配置为 `position: 0`, `constant: true`, `preventRecursion: true`, `excludeRecursion: true`
- **AND** 需添加 `order` 字段参与排序

### Requirement: 关键词格式规范化

#### Scenario: 触发词配置

- **WHEN** 任何条目声明 `keys` 字段
- **THEN** 必须使用英文半角逗号 `,` 作为分隔符
- **AND** 不得有空格：`问天,秩序之子,祖龙,脚奴` 而非 `问天, 秩序之子, 祖龙, 脚奴`
- **AND** 覆盖完整：全名+昵称+外号+职务+关键能力名（例：神魔号,神魔号系统,共生飞船）

### Requirement: 内容质量白描化

#### Scenario: 角色外貌描述

- **WHEN** 编写角色外貌
- **THEN** 删除万能美人词（精致、漂亮、帅气等）
- **AND** 删除 AI 默认信息（中国人的黑发、18 岁等）
- **AND** 必须有可识别特征（独特发色/装饰/服装细节/身体标记）
- **AND** 禁止"像一道闪电""如星辰般"等解释性比喻

#### Scenario: 角色性格描述

- **WHEN** 编写性格
- **THEN** 禁止直接贴标签（"她很温柔"）
- **AND** 改为行为展现（"会把受伤的小动物带回家照顾"）
- **AND** 性格描述与基本档案分离至独立字段或独立条目

#### Scenario: 道具/装置描述

- **WHEN** 编写装置或道具
- **THEN** 服装类：只写外观、材质、剪裁，不写优缺点
- **AND** 性玩具类：只写外形、玩法、结构，不写精确尺寸
- **AND** 武器/机械类：写类型、参数、使用方式，不写"威力巨大"等评价

### Requirement: 双递归强制开启

#### Scenario: 防 token 爆炸

- **WHEN** 任何条目完成配置
- **THEN** `preventRecursion: true` 与 `excludeRecursion: true` 必须同时为 true
- **AND** 蓝灯和绿灯条目均需开启
- **AND** 参考 Tavo_异能英雄调教模拟器（161/171 = 94% 启用）

### Requirement: 配置文件结构统一

#### Scenario: YAML 块完整性

- **WHEN** 处理条目文件
- **THEN** 修正因嵌套错误导致的格式问题（例：01_魔神会干部.md 中 `xml` 标签在 `yaml` 块外）
- **AND** 闭合所有未关闭的 `</yaml>` 标签
- **AND** 保持原有字段顺序与命名（key/keys/secondary_keys/content）

## MODIFIED Requirements

### Requirement: 既有 85 个条目的配置补全

**修改前**：多数 YAML 块仅含 `key`/`keys`/`position`/`content`，缺少 `constant`/`preventRecursion`/`excludeRecursion`/`scanDepth`。

**修改后**：每个 YAML 块顶部按类型补全 6 个配置字段，参考 4 个参考世界书的最优实践。

**理由**：当前配置缺失会导致条目无法被 AI 正确触发或引发 token 爆炸。

**迁移**：逐条目扫描 → 识别类型（世界观/角色/场景/规则/装置）→ 应用对应模板 → 不变更 `content` 主体文字，仅做白描化与禁词清理。

## REMOVED Requirements

无。
