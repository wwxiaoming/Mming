---
name: wqbrain-alpha-quality-helper
description: 帮助 WorldQuant BRAIN 学员结合"老强说 Alpha 辅助工具 v1.0.5"批量挖出更高质量 alpha 的判定器
---

# wqbrain-alpha-quality-helper

帮助 WorldQuant BRAIN 学员结合"老强说 Alpha 辅助工具 v1.0.5"批量挖出更高质量 alpha 的判定器。本 skill 不直接生成 alpha，而是把学员提交的"一阶段参数 / 表达式 / 回测结果 / 提交计划"按四个子能力逐项审一遍，给出可执行的取舍建议。

## 触发词清单

- 配置审阅类："帮我审一下这个配置" / "看看一阶段参数"
- 表达式预审类："这个表达式能过吗" / "alpha 预审"
- 结果诊断类："Sharpe 1.0 还能救吗" / "帮我看回测"
- 提交规划类："今天还要交几个" / "提交策略"

## 四个子能力入口

| 入口 | 用途 | 对应老强工具位置 |
|------|------|------------------|
| `config-auditor` | 审"一阶段"挖掘配置 | 一阶段 |
| `expression-preflight` | 审表达式结构与字段合规性 | 挖掘生成后、二阶段前 |
| `result-diagnostician` | 诊断回测 Sharpe / 换手 / 收益 | 统计 + Alphas |
| `submission-strategist` | 排今日提交顺序与数量 | Alphas + 统计 |

调用方式示例：

- "用 `config-auditor` 帮我审一下这组一阶段参数。"
- "走一遍 `expression-preflight`，这个表达式能过吗？"
- "用 `result-diagnostician` 看看这个 Sharpe 1.0 还能不能救。"
- "按 `submission-strategist` 给我排今天还要交几个。"

## 与老强工具的对应关系

| 老强工具按钮 | 含义 | 本 skill 哪条子能力接管 |
|--------------|------|------------------------|
| 一阶段 | 批量挖掘 alpha 的参数配置 | `config-auditor` |
| 二阶段 | 对一阶段产出做种子筛选 | `expression-preflight` + `result-diagnostician` |
| 三阶段 | 对二阶段种子做精筛 | `result-diagnostician` |
| Alphas | 已生成的 alpha 列表 | `result-diagnostician` + `submission-strategist` |
| 统计 | 多 alpha 汇总指标 | `submission-strategist` |

## 工作流程

1. 学员说明当前在老强工具的哪个阶段，贴出对应配置 / 表达式 / 结果。
2. skill 按对应子能力逐项给出：风险点、建议动作、是否进入下一步。
3. 学员按建议在老强工具里调整，回到对应阶段重跑。
4. 在提交环节调用 `submission-strategist`，决定今天交哪几个。

## 学习资源

更多运算符、数据集、模板与背景知识见 [learning-index.md](references/learning-index.md)。
