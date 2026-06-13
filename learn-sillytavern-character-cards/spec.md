# SillyTavern 角色卡制作方式 学习记录

## Why

SillyTavern 是一个面向高级用户的 LLM 前端应用，其核心功能之一是角色卡（Character Card）系统。角色卡是将 AI 角色信息嵌入 PNG 图片元数据的标准格式，让用户能够创建、管理和分享个性化的 AI 角色。了解角色卡的制作方式是掌握 SillyTavern 使用的关键。

## What Changes

- 整理角色卡的基本概念与数据格式
- 记录 V1/V2/V3 三个版本规范的字段定义
- 整理角色卡各字段的最佳实践
- 记录常见角色描述格式（W++、Ali:Chat、Boostyle 等）
- 整理 Lorebook 角色知识库的使用方法
- 记录创建工具与分享平台的清单
- 整理常见错误与评分标准

## Impact

- Affected specs: 无（纯学习记录）
- Affected code: 无

## ADDED Requirements

### Requirement: 理解角色卡的基本概念

SillyTavern 角色卡是一种 PNG 图片文件，利用 PNG 的 `tEXt` 元数据块存储 JSON 格式的角色数据。

#### Scenario: 了解角色卡的技术原理
- **WHEN** 学习者查阅本记录
- **THEN** 应能理解：角色卡 = 头像图片 + JSON 角色数据（Base64 编码存入 PNG tEXt 块）
- **AND** 了解角色卡的特点：一图一角色、便于分享、跨平台兼容

### Requirement: 了解角色卡的版本差异

角色卡有三个版本：V1（基础）、V2（标准，当前主流）、V3（扩展格式）。

#### Scenario: 了解各版本差异
- **WHEN** 学习者查阅本记录
- **THEN** 应能区分三个版本的核心差异
- **AND** 了解 V2 是当前最广泛支持的版本，PNG 使用 `chara` 关键字
- **AND** 了解 V3 使用 `ccv3` 关键字，支持 .charx 压缩包格式

### Requirement: 掌握 V2 角色卡的核心字段

V2 规范定义了完整的角色数据字段。

#### Scenario: 了解 V2 核心字段
- **WHEN** 学习者查阅本记录
- **THEN** 应了解以下字段及其用途：
  - `name`: 角色名称
  - `description`: 外貌、背景、世界观设定
  - `personality`: 内在性格、动机、说话风格
  - `scenario`: 互动场景设定（时间/地点/原因）
  - `first_mes`: 首条消息，设定语气和风格
  - `mes_example`: 对话示例，用 `<START>` 分隔
  - `creator_notes`: 创作者备注（不影响 AI）
  - `system_prompt`: 角色专属系统提示词
  - `post_history_instructions`: 历史后指令（UJB/Jailbreak）
  - `alternate_greetings`: 可选的替代开场白
  - `character_book`: 嵌入式 Lorebook
  - `tags`: 分类标签
  - `creator`: 作者名
  - `character_version`: 角色版本号
  - `extensions`: 扩展数据

### Requirement: 理解各字段的 Token 特性

不同字段在提示词融入时行为不同。

#### Scenario: 了解永久 Token 与临时 Token
- **WHEN** 学习者查阅本记录
- **THEN** 应了解永久 Token（始终在上下文）：`name`、`description`、`personality`、`scenario`
- **AND** 应了解临时 Token：`first_mes`（仅聊天开始）、`mes_example`（随上下文填满被推出）
- **AND** 应了解理想 Token 总量：500~2200 tokens
- **AND** 应了解 Token 超标的后果：AI 记忆减少

### Requirement: 了解角色描述的写作格式

社区有多种角色描述格式。

#### Scenario: 了解常见写作格式
- **WHEN** 学习者查阅本记录
- **THEN** 应了解以下格式：
  - 自由文本：自然语言段落描述
  - W++：结构化属性格式
  - Boostyle：关键词/属性列表
  - Ali:Chat：通过对话示例表达角色特质
  - PLists：Pygmalion 模型的列表格式

### Requirement: 了解角色的最佳实践

角色卡质量评级有明确标准。

#### Scenario: 了解角色卡质量评分标准
- **WHEN** 学习者查阅本记录
- **THEN** 应了解五大评分维度（各 0-20 分）：
  1. 字段适配性与结构
  2. 角色连贯性与一致性
  3. 角色扮演实用性与沉浸感
  4. 创意与原创性
  5. 打磨与技术要求

#### Scenario: 了解常见错误
- **WHEN** 学习者查阅本记录
- **THEN** 应了解常见陷阱：
  - 空字段或字段误用（如将 personality 内容写进 description）
  - 缺少 first_mes 或只用泛泛的 "Hi"
  - 没有 mes_example 导致语气模糊
  - 单个字段过度填充
  - Token 总量过少（<250）或过多（>2700）

### Requirement: 了解 Lorebook（角色知识库）

Lorebook 提供关键词触发的上下文知识注入。

#### Scenario: 了解 Lorebook 功能
- **WHEN** 学习者查阅本记录
- **THEN** 应了解 Lorebook 条目包含：keys（关键词）、content（内容）、priority
- **AND** 了解支持属性：selective（双关键词）、constant（始终注入）、recursive_scanning（递归触发）
- **AND** 了解 position 属性：before_char / after_char

### Requirement: 了解角色卡的创建工具

#### Scenario: 了解可用工具
- **WHEN** 学习者查阅本记录
- **THEN** 应了解以下工具：
  - SillyTavern 内置编辑器
  - Chara Snap（浏览器端免费编辑器，无需账号）
  - MegaNova Studio
  - Character Card Extractor（元数据提取工具）

### Requirement: 了解角色卡分享平台

#### Scenario: 了解分享平台
- **WHEN** 学习者查阅本记录
- **THEN** 应了解以下平台：
  - Chub.ai（最大角色卡分享站）
  - CharacterHub
  - AICharacterCards.com
  - Janitor AI

### Requirement: 掌握 SillyTavern 宏和占位符

#### Scenario: 了解常用占位符
- **WHEN** 学习者查阅本记录
- **THEN** 应了解 `{{char}}`（角色名）、`{{user}}`（用户名）
- **AND** 了解 `{{original}}`（原始系统提示词占位符）
- **AND** 了解 `{{newline}}`、`{{trim}}`、`{{noop}}` 等工具宏