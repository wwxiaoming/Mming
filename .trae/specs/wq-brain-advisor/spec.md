# WQ BRAIN 顶级AI赚钱顾问 Spec

## Why
为 WorldQuant BRAIN 平台的用户构建一套完整的 AI 顾问智能体系统，帮助他们安全、高效地从零基础到成为签约顾问并最大化收入。基于 AlphaDoc（https://alphadoc.biglongxia.com/guide/）11 章完整教程内容，将分步骤的操作指导和量化金融知识整合为可交互的 AI 技能体系。

## What Changes
- 创建全局强制规则文件 `.trae/rules`，定义"老强"顾问身份定位、核心铁律和回答规范
- 创建 12 个专业技能（Skills），覆盖从项目背景到顾问后优化的全流程知识域
- 从 AlphaDoc 抓取并结构化填充所有章节知识内容到对应技能的 resources 目录
- 创建 5 个自定义 Agent（WQ主顾问、Alpha策略师、知识库检索员、进度追踪员、风控预警员）
- 配置 MCP Servers（playwright、filesystem、cron）用于浏览器自动化、文件操作和定时任务
- 初始化用户状态跟踪系统（user_state.md），记录用户进度、积分、等级等
- 配置每日自动提醒任务（Cron MCP），覆盖 Alpha 提交截止、积分查看、邮箱检查等节点
- 执行 5 项快速功能验收测试，验证智能体核心功能

## Impact
- Affected specs: 新建 specs，无现有 specs 受影响
- Affected code: 全新项目，将在项目根目录创建 `.trae/rules`、`.trae/skills/`、`.trae/mcp.json`、`user_state.md` 等文件

## ADDED Requirements

### Requirement: 全局强制规则
系统 SHALL 在 `.trae/rules` 中定义"老强"身份定位、6 条核心铁律和 5 条回答规范，作为最高优先级的约束规则。

#### Scenario: 每次对话末尾附安全提醒
- **WHEN** 每次对话结束
- **THEN** 输出"⚠️ 切记：不要在社群范围以外提到工具及教程站相关，低调干大事，闷声发大财！"

#### Scenario: 用户违反铁律操作
- **WHEN** 用户行为可能违反核心铁律（如想先提交 Workday 再填问卷）
- **THEN** 立即以 ⚠️ 开头输出最高级警告并阻止操作

### Requirement: 12 个核心技能（Skills）
系统 SHALL 在 `.trae/skills/` 目录下创建 12 个技能文件，每个包含 `name`、`description`、`when_to_use`、`instructions` 四部分，覆盖 WQ BRAIN 全流程知识。

#### Scenario: 技能触发
- **WHEN** 用户提及与某技能相关的关键词
- **THEN** 系统加载对应技能并提供结构化的操作指导

### Requirement: 知识内容结构化填充
系统 SHALL 从 AlphaDoc 抓取 11 章教材全文内容、7 天学习计划、所有警告和提示、官方资源链接，并结构化存储到对应技能的 `resources/` 目录。

#### Scenario: 内容同步
- **WHEN** 技能被触发
- **THEN** 可引用 resources 目录下的对应章节内容作为回答依据

### Requirement: 5 个自定义 Agent
系统 SHALL 创建 5 个专业 Agent，分别负责总调度、Alpha 策略、知识库检索、进度追踪和风控预警，每个 Agent 关联对应的 Skills。

#### Scenario: 多 Agent 协作
- **WHEN** 用户提出复杂问题（如"我今天该做什么"）
- **THEN** WQ主顾问总调度，分发任务给对应子 Agent 获取专业回复

### Requirement: MCP Servers 配置
系统 SHALL 在 `.trae/mcp.json` 中配置 playwright、filesystem、cron 三个 MCP Server。

#### Scenario: 定时提醒
- **WHEN** 到达配置的 cron 时间节点
- **THEN** cron MCP 触发对应的提醒任务

### Requirement: 用户状态跟踪
系统 SHALL 创建 `user_state.md` 文件持久化记录用户基本信息、核心进度和每日跟踪数据。

#### Scenario: 状态更新
- **WHEN** 用户完成某一阶段性任务（如通过问卷、提交 Alpha）
- **THEN** 更新 user_state.md 中的对应字段

### Requirement: 7 个每日自动提醒任务
系统 SHALL 通过 Cron MCP 配置以下定时提醒：11:00 工具检查提醒、12:00 Alpha 提交询问、15:00 积分查看提醒、18:00 邮箱检查询问、每周一 09:00 教程更新检查。

#### Scenario: 中午提醒
- **WHEN** 北京时间每天 12:00
- **THEN** 输出"今天是否有可提交的 Alpha？如有请立即提交"

### Requirement: 5 项功能验收测试
系统 SHALL 执行 5 项测试验证智能体功能：新手引导测试、无产出诊断测试、问卷警告测试、概念解释测试、Workday 指导测试。

#### Scenario: 测试执行
- **WHEN** 构建完成后执行测试
- **THEN** 输出 5 项测试的实际响应结果，确认每项符合预期输出要求