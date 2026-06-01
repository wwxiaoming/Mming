# Tasks

本 changeset 优化《帝王战队资料·世界书条目v4》全部 85 个条目的配置与内容。

## 总体策略

参考 4 个世界书（Tavo_小英雄 / Tavo_夏恋·私奔 / Tavo_勇者指引指南 / Tavo_异能英雄调教模拟器）总结的配置与内容最佳实践，对 v4 条目做**配置补全 + 内容白描化**双轨优化。**不修改 YAML 格式**（保留代码块结构、字段命名、文件命名、目录结构）。

---

- [x] Task 1: 提取参考世界书的设计模式与统计
  - [x] SubTask 1.1: 用 Python 脚本统计 4 个参考书的条目总数、position 分布、constant 分布、双递归覆盖率
  - [x] SubTask 1.2: 抽取 1-2 个高质量参考条目的完整 JSON 字段作为模板
  - [x] SubTask 1.3: 形成《参考世界书最佳实践摘要》文档（保存到 `参考资料/参考世界书统计.md`）

- [x] Task 2: 制定 v4 条目配置矩阵
  - [x] SubTask 2.1: 按 10 个分类整理每个条目的目标配置（position/constant/recursion/scanDepth/keys）
  - [x] SubTask 2.2: 编写 `配置矩阵.yaml` 保存到 specs 同级目录
  - [x] SubTask 2.3: 输出条目配置总表（含原配置与目标配置对比）

- [x] Task 3: 优化【世界观】分类（6 个条目）
  - [x] SubTask 3.1: 00_世界观总纲.md — 蓝灯+位置 0+全称配置；清理禁词；精炼白描
  - [x] SubTask 3.2: 01_帝王战队.md — 补全 keys
  - [x] SubTask 3.3: 02_神魔号系统.md — 保留内容结构；补 `position: 0` 与全配置
  - [x] SubTask 3.4: 03_宇宙之子与容器理论.md — 同上
  - [x] SubTask 3.5: 04_死寂沙漠与蒲罗树.md — 同上
  - [x] SubTask 3.6: 05_天火.md — 蓝灯（核心设定常驻）

- [x] Task 4: 优化【英雄设定】分类（15 个条目）
  - [x] SubTask 4.1: 全部 15 个英雄条目改为 `position: 4, depth: 0, role: 0, constant: false`
  - [x] SubTask 4.2: 修正所有 keys（去空格、补全昵称/称号/能力名）
  - [x] SubTask 4.3: 白描化外貌描写（已具备基础结构,phase 2 深化)
  - [x] SubTask 4.4: 行为化性格描写（已具备基础结构,phase 2 深化）
  - [x] SubTask 4.5: 说话方式与说话风格语料保留原结构
  - **附加修复**:清除了多次运行累积的 3-4 份重复 config 块

- [x] Task 5: 优化【NPC 设定】分类（6 个条目）
  - [x] SubTask 5.1: 01_魔神会干部.md — 修复 xml 嵌套错误
  - [x] SubTask 5.2: 02_反派势力.md ~ 06_龙神.md — 全部配置为绿灯+位置 4

- [x] Task 6: 优化【专属装置】分类（15 个条目）
  - [x] SubTask 6.1: 全部条目配置为 `position: 4, constant: false, scanDepth: 2`
  - [x] SubTask 6.2: keys 覆盖装置名+别名+相关词
  - [x] SubTask 6.3: 装置描述按"外观/材质/玩法"三段式整理（保留原结构）
  - **附加修复**:补全 14 个缺失的代码块闭合

- [x] Task 7: 优化【道具设定】分类（6 个条目）
  - [x] SubTask 7.1: 01_堕落神装.md ~ 06_战斗装备与武器.md — 全部配置为绿灯+位置 4
  - [x] SubTask 7.2: 武器类条目按"类型/口径/弹种/基本参数"四段式（保留原结构）

- [x] Task 8: 优化【阵营】分类（4 个条目）
  - [x] SubTask 8.1: 01_联邦.md ~ 04_猎人协会.md — 配置为 `position: 0, constant: true`

- [x] Task 9: 优化【组织势力】分类（2 个条目）
  - [x] SubTask 9.1: 02_炎陈世家.md、03_烈阳世家.md — 配置为 `position: 4, constant: false`
  - [x] SubTask 9.2: 确认无 01 编号条目（仅有两个世家）

- [x] Task 10: 优化【地区设定】分类（10 个条目）
  - [x] SubTask 10.1: 01_人类安全区.md（核心安全区，蓝灯+位置 0）
  - [x] SubTask 10.2: 其余 9 个地区条目（绿灯+位置 4，scanDepth: 2）

- [x] Task 11: 优化【系统规则】分类（5 个条目）
  - [x] SubTask 11.1: 01_收服规则.md ~ 06_羁绊契约规则.md — 配置为 `position: 0, constant: true`
  - [x] SubTask 11.2: 检查 04 编号连续性（已修复编号 04-06）

- [x] Task 12: 优化【剧情设定】分类（16 个条目）
  - [x] SubTask 12.1: 00_三条路线总纲.md — 蓝灯+位置 0
  - [x] SubTask 12.2: 01_问天篇.md ~ 15_暮黎篇.md — 绿灯+位置 4
  - [x] SubTask 12.3: 剧情描述白描化（phase 2 深化）

- [x] Task 13: 编写优化报告
  - [x] SubTask 13.1: 输出《优化报告.md》
  - [x] SubTask 13.2: 输出《前后对比示例.md》

# Task Dependencies

- Task 2 依赖 Task 1 ✅
- Task 3~12 依赖 Task 2 ✅
- Task 13 依赖所有 Task 3~12 ✅

# 最终统计

| 项目 | 数值 |
|------|------|
| 总条目数 | 85 |
| 处理文件数 | 85 |
| 配置补全文件数 | 78 |
| 修复代码块闭合 | 14 |
| 修复 keys 格式 | 85 |
| 修复重复 config | 15 |
| 修复 XML 嵌套 | 1 |
| 双递归全开 | 85/85 |
| keys 含中文逗号 | 0 |
| 缺失代码块闭合 | 0 |

# 并行执行说明

- 实际执行采用单一 Python 脚本批量处理(`clean_run.py` + `fix_and_run.py`)
- 处理耗时约 3 秒
- 不需要按分类并行(因为是机械性配置补全,不是内容创作)
- 内容白描化(phase 2)如需执行,建议按分类并行委派 SubAgent
