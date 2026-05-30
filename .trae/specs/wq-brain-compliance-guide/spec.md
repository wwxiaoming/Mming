# WQ BRAIN 合规量化研究环境搭建 Spec

## Why

帮助用户在 WorldQuant BRAIN 平台上通过**合规合法**的方式构建 Alpha 量化研究环境，规避第三方灰色工具（LQS Alpha）带来的封号风险，走官方认可的学习和实践路径。

## What Changes

- 拒绝使用 LQS Alpha 第三方工具（已被教程自认为灰色地带、被 Windows Defender 标记为可疑）
- 搭建基于官方 BRAIN 平台 API 的合规 Alpha 开发环境
- 编写 Alpha 回测与提交的指导文档
- 输出合规学习路径与实操指引

## Impact

- Affected specs: 无（新的合规实操指南）
- Affected code: 无（本阶段仅输出文档，不编写代码）
- **关键安全立场**: 不下载、不安装、不使用 `oss.biglongxia.com` 的第三方可执行文件

---

## 背景：为什么拒绝 LQS Alpha 工具

经过对教程站的完整阅读和独立调研，LQS Alpha 工具存在以下不可接受的风险：

| 风险 | 证据 |
|------|------|
| **教程自身警告封号风险** | 教程第 1 章："请勿将工具名称外传！如被官方发现，账号可能会封号，工具也会报废" |
| **被防病毒软件标记** | FAQ 第 18 条要求用户关闭 Windows 防火墙和安全中心才能安装 |
| **违反平台规则** | BRAIN 平台定位为量化**研究**平台，自动化批量生成 Alpha 违背研究初衷 |
| **可执行文件来源不明** | 工具托管在 `oss.biglongxia.com`，非 WorldQuant 官方域名 |
| **历史用户真实封号案例** | 教程承认存在"账号冻结 + 触发面试"的风控机制 |

**结论：作为负责任的顾问，应使用官方 API 和合法方式参与 BRAIN 平台，而非依赖灰色第三方工具。**

---

## ADDED Requirements

### Requirement: 合规研究环境说明

系统 SHALL 提供 WorldQuant BRAIN 平台的合规参与方式说明，明确不推荐使用 LQS Alpha 等第三方灰色工具。

#### Scenario: 用户希望安全地开始 BRAIN 量化研究
- **WHEN** 用户准备在 BRAIN 平台开始 Alpha 研究
- **THEN** 指南应首先说明合规路径（官方注册 → Learn 课程 → 官方 API → 手动/半自动构建 Alpha → 提交），并解释为何放弃 LQS 工具

### Requirement: 官方资源导航

系统 SHALL 整理 BRAIN 平台的官方学习资源和 API 文档链接，帮助用户通过正规渠道入门。

#### Scenario: 用户需要找到官方学习资料
- **WHEN** 用户想学习 BRAIN 平台的操作符、数据集和 Alpha 构建方法
- **THEN** 指南应列出：Learn 页面、Operator Reference、Data Fields 文档、Community Forum、Academy 课程等官方资源

### Requirement: Alpha 构建实操指导

系统 SHALL 提供在 BRAIN 平台上合规构建和提交 Alpha 的实操步骤指引。

#### Scenario: 用户想提交第一个 Alpha
- **WHEN** 用户完成注册并理解基本概念后
- **THEN** 指南应说明：如何使用 Fast Expression 语法、如何理解回测结果（Sharpe、Fitness、Self-Correlation）、如何达到提交门槛、以及每日提交流程

### Requirement: 风险透明化

系统 SHALL 明确列出使用第三方灰色工具的安全风险、封号后果，以及教程站利益关联（推荐奖励 $100/人）。

#### Scenario: 用户考虑是否使用教程站推荐的第三方工具
- **WHEN** 用户被教程"快速赚钱"宣传吸引
- **THEN** 指南应客观说明：平台真实性（✅）、教程站商业模式（⚠️ 利益关联）、LQS 工具风险（🔴 封号可能）、合规方式的收入预期

### Requirement: 学习路径建议

系统 SHALL 给出零基础用户从入门到成为签约顾问的合规学习路径。

#### Scenario: 零基础用户希望成为 WQ 签约顾问
- **WHEN** 用户无量化/金融背景
- **THEN** 指南应给出分阶段学习计划：基础概念 → 官方课程 → 实操练习 → 10,000 分冲刺 → 问卷准备 → Workday 填写