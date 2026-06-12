# 任务清单

- [x] Task 1: 解析参考源 — Read 4 个原 03-06 文件、Tavo_异能英雄调教模拟器 order 134-163 道具条目、帝王战队.txt / 帝王战队番外.txt 中涉及榨精自行车 / 千手魔罂粟 / 淫魔触手 / 银质乳钉 / 机械犬 / 烙印 / 神纹 等关键词段落
  - [x] SubTask 1.1: 提取 03-06 原文件中所有"核心功能 / 使用机制 / 关联条目"片段（**不**提取路线分支段）
  - [x] SubTask 1.2: 列出 Tavo 模拟器 30 件道具的格式范本
  - [x] SubTask 1.3: Grep 小说正文提取可用具体道具名

- [x] Task 2: 草拟 4 大类道具条目表（**排除**专属装置目录已收录的 15 件）
  - [x] SubTask 2.1: **魔神会黑科技类**（8 条）
  - [x] SubTask 2.2: **通用调教道具类**（10 条）
  - [x] SubTask 2.3: **魔物相关道具类**（7 条）
  - [x] SubTask 2.4: **战斗装备与武器类**（9 条）

- [x] Task 3: 写入 `/workspace/帝王战队资料/世界书条目v4/道具设定/07_道具图鉴.md`
  - [x] SubTask 3.1: 头部 YAML 块：key="道具图鉴"，secondary_keys=[...]，enabled=true，position=1，order=93
  - [x] SubTask 3.2: `content: |` 块按 5 段 + 4 大类 H2 段（**不写**"在三条路线中的状态"）

- [x] Task 4: 验证 YAML 格式合法（python yaml.safe_load 通过）
- [x] Task 5: 验证小说事实可追溯（27/32 = 84.4% Grep 命中帝王战队.txt / 帝王战队番外.txt）
- [x] Task 6: 验证文件内不出现"路线A/B/C"（0 处）与 15 件专属装置名（body 0 处，关联条目路径 4 处）
- [x] Task 7: 删除 03/04/05/06 四个原文件
- [x] Task 8: 最终目录检查 — `/workspace/帝王战队资料/世界书条目v4/道具设定/` 仅含 01/02/07

# Task Dependencies
- Task 3 依赖 Task 1 + Task 2
- Task 4 依赖 Task 3
- Task 5 依赖 Task 3
- Task 6 依赖 Task 3
- Task 7 依赖 Task 4 + Task 5 + Task 6
- Task 8 依赖 Task 7
