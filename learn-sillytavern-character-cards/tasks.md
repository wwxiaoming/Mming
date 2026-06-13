# Tasks

本 changeset 为学习记录性质，任务以资料整理和文档编写为主。

- [x] Task 1: 收集并整理角色卡的基本概念与技术原理
  - [x] 从 SillyTavern 官方 Wiki 和社区资源收集资料
  - [x] 理解 PNG tEXt 元数据嵌入机制
  - [x] 理解 V1/V2/V3 版本演进历史
- [x] Task 2: 整理 V2 规范核心字段定义
  - [x] 从官方 spec_v2.md 提取字段定义
  - [x] 整理每个字段的用途、是否参与 Prompt、是否为永久 Token
- [x] Task 3: 整理角色描述写作方法与格式
  - [x] 收集常见格式（自由文本、W++、Boostyle、Ali:Chat、PLists）
  - [x] 整理各格式的特点与适用场景
- [x] Task 4: 整理角色卡质量评分标准与最佳实践
  - [x] 收集评分维度与常见错误
  - [x] 整理各字段的内容分配建议
  - [x] 整理 Token 预算管理建议
- [x] Task 5: 整理 Lorebook 角色知识库的使用方法
  - [x] 了解条目结构（keys、content、priority）
  - [x] 了解触发机制（关键词、selective、constant、recursive）
- [x] Task 6: 收集创建工具与分享平台清单
  - [x] 整理可用创建工具
  - [x] 整理主要分享平台
- [x] Task 7: 整理宏变量与占位符
  - [x] 记录 {{char}}、{{user}} 等角色占位符
  - [x] 记录 {{original}} 等提示词占位符
  - [x] 记录 {{newline}}、{{trim}}、{{noop}} 等工具宏
- [x] Task 8: 编写完整的综合学习记录文档
  - [x] 将所有资料整合为一份完整的学习记录

# Task Dependencies

- Task 2 依赖 Task 1（需要先理解基本概念）
- Task 3、4、5、6、7 可与 Task 2 并行进行
- Task 8 依赖所有前置任务