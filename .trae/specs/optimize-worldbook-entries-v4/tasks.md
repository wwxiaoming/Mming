# Tasks

- [x] Task 1: 阅读并提炼 5 个参考世界书的内容模式
  - [x] SubTask 1.1: 用 `query.py --brief` 与 `--uid` 抽样 5 个参考世界书，输出「角色 / 规则 / 世界观 / 装置」四类条目的章节结构对照表
  - [x] SubTask 1.2: 提取共有的核心维度清单（基本信息 / 外貌 / 性格 / 身体特征 / XP / 说话风格 / 路线 / 关联钩子）
  - [x] SubTask 1.3: 归纳每类条目的章节模板（英雄模板、NPC 模板、规则模板、装置模板、世界观模板、剧情模板）

- [x] Task 2: 编写 `quality-checklist.md`（条目质量对照清单）
  - [x] SubTask 2.1: 列出 12 个评审维度，每个维度给「完整 / 部分 / 缺失」三档定义
  - [x] SubTask 2.2: 标注每个维度对应的参考世界书字段（用于回查溯源）
  - [x] SubTask 2.3: 输出到 `.trae/specs/optimize-worldbook-entries-v4/quality-checklist.md`

- [x] Task 3: 编写 `content-template.md`（条目内容优化模板）
  - [x] SubTask 3.1: 英雄设定模板（含 XP / 敏感度 / 说话风格语料 / 路线分支）
  - [x] SubTask 3.2: NPC 设定模板（含势力归属 / 与天火/英雄的交互模式 / 调教手段 / 失败模式）
  - [x] SubTask 3.3: 规则 / 装置 / 世界观 / 剧情 / 地区 / 阵营 / 组织模板
  - [x] SubTask 3.4: 输出到 `.trae/specs/optimize-worldbook-entries-v4/content-template.md`

- [x] Task 4: 评审 85 个 Markdown 条目，输出 `optimization-audit.md`
  - [x] SubTask 4.1: 按子目录批量读取（10 个子目录），用 `quality-checklist.md` 逐条打分
  - [x] SubTask 4.2: 按优先级排序（核心英雄 → 世界观 → 规则 → 装置 → 剧情 → NPC → 地区 → 阵营 → 组织 → 道具）
  - [x] SubTask 4.3: 输出到 `.trae/specs/optimize-worldbook-entries-v4/optimization-audit.md`

- [ ] Task 5: 优化世界书条目 v4（按优先级分批执行）
  - [ ] SubTask 5.1: 批 1 — 世界观（6 个文件：00_世界观总纲 + 01-05_世界观）
  - [ ] SubTask 5.2: 批 2 — 英雄设定（15 个文件：01-15_英雄）
  - [ ] SubTask 5.3: 批 3 — 剧情设定（16 个文件：00_三条路线总纲 + 01-15_剧情篇）
  - [ ] SubTask 5.4: 批 4 — 系统规则（5 个文件：01/02/03/05/06_规则）
  - [ ] SubTask 5.5: 批 5 — 专属装置（15 个文件：01-15_装置）
  - [ ] SubTask 5.6: 批 6 — 道具设定（6 个文件：01-06_道具）
  - [ ] SubTask 5.7: 批 7 — NPC 设定（6 个文件：01-06_NPC）
  - [ ] SubTask 5.8: 批 8 — 地区设定（10 个文件：01-10_地区）
  - [ ] SubTask 5.9: 批 9 — 阵营（4 个文件：01-04_阵营）
  - [ ] SubTask 5.10: 批 10 — 组织势力（2 个文件：02-03_组织）

- [ ] Task 6: 优化后兼容性校验
  - [ ] SubTask 6.1: 用 `diff` 验证每个文件仅 `content: |` 块内的内容被修改
  - [ ] SubTask 6.2: 比对优化后的 `key` / `secondary_keys` 与 2 个角色卡内嵌世界书条目的 key 字段，标注潜在冲突
  - [ ] SubTask 6.3: 输出 `compatibility-report.md`

# Task Dependencies

- Task 2 依赖 Task 1（需先归纳核心维度才能编写清单）
- Task 3 依赖 Task 1（需先归纳模板）
- Task 4 依赖 Task 2、Task 3（需先有清单和模板才能评审）
- Task 5 依赖 Task 4（需先评审才能按优先级优化）
  - SubTask 5.2 ~ 5.10 可在 5.1 完成后并行处理
- Task 6 依赖 Task 5（需先优化完才能校验）
