# Tasks

- [x] Task 1: 创建全局强制规则文件
  - [x] 创建 `.trae/rules` 文件，写入 WQ BRAIN 顾问全局强制规则，包含身份定位、6 条核心铁律和 5 条回答规范

- [x] Task 2: 创建 12 个核心 Skills
  - [x] 创建 `wq-01-background` 技能：项目背景、收益模型、准入条件
  - [x] 创建 `wq-02-faq` 技能：常见问题速查和踩坑避坑表
  - [x] 创建 `wq-03-cloud-server` 技能：腾讯云/阿里云免费服务器申请与配置
  - [x] 创建 `wq-04-registration` 技能：平台注册全流程（含邀请码获取）
  - [x] 创建 `wq-05-tool-setup` 技能：Alpha 辅助工具安装、配置和基础使用
  - [x] 创建 `wq-06-gold-medal` 技能：一万分金牌速通策略、数据集+中性化推荐、无产出诊断
  - [x] 创建 `wq-07-questionnaire` 技能：基础测试问卷 9 题知识点参考、答题注意事项
  - [x] 创建 `wq-08-workday` 技能：Workday 入职表逐字段填写指南、身份证上传要求
  - [x] 创建 `wq-09-consultant` 技能：顾问身份确认流程、面试准备指南
  - [x] 创建 `wq-10-optimization` 技能：顾问后 Alpha 策略优化、官方学习路径
  - [x] 创建 `wq-11-appendix` 技能：合同解读、发薪日期、纳税规则、推荐计划
  - [x] 创建 `wq-concepts` 技能：量化金融基础概念解释（Alpha、中性化、自相关等）

- [x] Task 3: 填充知识内容到技能 resources 目录
  - [x] 将第 01 章内容写入 `wq-01-background/resources/chapter01.md`
  - [x] 将第 02 章内容写入 `wq-02-faq/resources/chapter02.md`
  - [x] 将第 03 章内容写入 `wq-04-registration/resources/chapter03.md`
  - [x] 将第 04 章内容写入 `wq-03-cloud-server/resources/chapter04.md`
  - [x] 将第 05 章内容写入 `wq-05-tool-setup/resources/chapter05.md`
  - [x] 将第 06 章内容写入 `wq-06-gold-medal/resources/chapter06.md`
  - [x] 将第 07 章内容写入 `wq-07-questionnaire/resources/chapter07.md`
  - [x] 将第 08 章内容写入 `wq-08-workday/resources/chapter08.md`
  - [x] 将第 09 章内容写入 `wq-09-consultant/resources/chapter09.md`
  - [x] 将第 10 章内容写入 `wq-10-optimization/resources/chapter10.md`
  - [x] 将第 11 章内容写入 `wq-11-appendix/resources/chapter11.md`
  - [x] 将 7 天学习计划写入 `wq-06-gold-medal/resources/7day-plan.md`
  - [x] 将所有警告汇总写入 `wq-02-faq/resources/warnings.md`
  - [x] 将所有资源链接写入 `wq-02-faq/resources/links.md`

- [x] Task 4: 创建 5 个自定义 Agent 配置
  - [x] 创建 WQ主顾问 Agent 配置
  - [x] 创建 Alpha策略师 Agent 配置
  - [x] 创建 知识库检索员 Agent 配置
  - [x] 创建 进度追踪员 Agent 配置
  - [x] 创建 风控预警员 Agent 配置

- [x] Task 5: 配置 MCP Servers
  - [x] 创建 `.trae/mcp.json`，配置 playwright、filesystem、cron 三个 MCP Server

- [x] Task 6: 初始化用户状态跟踪系统
  - [x] 创建 `user_state.md` 文件，包含基本信息、核心进度、每日跟踪字段

- [x] Task 7: 配置 5 个每日自动提醒任务
  - [x] 通过 Cron MCP 配置 11:00 工具检查提醒
  - [x] 通过 Cron MCP 配置 12:00 Alpha 提交询问
  - [x] 通过 Cron MCP 配置 15:00 积分查看提醒
  - [x] 通过 Cron MCP 配置 18:00 邮箱检查询问
  - [x] 通过 Cron MCP 配置每周一 09:00 教程更新检查

- [x] Task 8: 执行快速功能验收测试
  - [x] 测试 1：新手第一天场景（"我是第一天，什么都不懂"）
  - [x] 测试 2：无产出诊断场景（"今天没有可提交的Alpha"）
  - [x] 测试 3：问卷警告场景（"我要填基础测试问卷了"）
  - [x] 测试 4：概念解释场景（"什么是中性化"）
  - [x] 测试 5：Workday 指导场景（"Workday怎么填"）

# Task Dependencies
- Task 3 依赖 Task 2（先创建技能目录，再填充内容）
- Task 7 依赖 Task 5（先配置 MCP，再设置定时任务）
- Task 8 依赖 Task 1-7（全部完成后进行验收测试）
- Task 1、2、4、5、6 可并行执行