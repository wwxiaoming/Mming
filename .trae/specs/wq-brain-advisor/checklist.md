# Checklist

- [x] `.trae/rules` 文件已创建，包含完整的身分定位、6 条核心铁律和 5 条回答规范
- [x] 每次对话末尾会输出安全提醒语句
- [x] 12 个 Skills 全部在 `.trae/skills/` 下创建完毕，每个包含 name、description、when_to_use、instructions
- [x] 11 个章节内容文件已写入对应 skills 的 resources 目录
- [x] 7 天学习计划文件已写入 wq-06-gold-medal/resources/7day-plan.md
- [x] 警告汇总文件已写入 wq-02-faq/resources/warnings.md
- [x] 资源链接文件已写入 wq-02-faq/resources/links.md
- [x] 5 个自定义 Agent 配置已创建（WQ主顾问、Alpha策略师、知识库检索员、进度追踪员、风控预警员）
- [x] `.trae/mcp.json` 已创建，包含 playwright、filesystem、cron 三个 server
- [x] `user_state.md` 已创建，包含基本信息、核心进度和每日跟踪字段
- [x] 5 个 Cron 定时任务已配置（11:00、12:00、15:00、18:00、周一 09:00）
- [x] 测试 1（新手引导）通过：输出项目背景、收益、注册指导、第一天任务清单
- [x] 测试 2（无产出诊断）通过：检查连续无产出天数，推荐数据集+中性化搭配，给出排查步骤
- [x] 测试 3（问卷警告）通过：先弹出最高级警告（2 次机会、禁止抄袭），再提供 9 题知识点参考
- [x] 测试 4（概念解释）通过：用大白话解释中性化定义、作用和用法
- [x] 测试 5（Workday 指导）通过：逐字段指导，附检查清单，强调如实填写和审核周期