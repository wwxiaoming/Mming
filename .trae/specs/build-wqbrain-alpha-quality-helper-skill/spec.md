# WQ Brain Alpha 质量提升助手 Skill Spec

## Why
学员使用「老强说 Alpha 辅助工具 v1.0.5」(Windows 客户端) 在 WorldQuant BRAIN 平台批量挖 Alpha，但工具本身只负责"跑"，不负责"教"和"判"。学员经常卡在：① 阶段参数乱填导致 2000 次空跑；② 表达式跑出来后看不懂指标；③ 提交时被 Self Correlation 拦下来；④ Sharpen 0.8 离 1.25 还差一截不知道怎么改。本 skill 围绕工具的 3 阶段流水线，把"配置审查 → 表达式预审 → 结果诊断 → 提交建议"做成一个可被 AI 调用的判定器，让学员的每一次挖矿都更接近"提交"。

## What Changes
- 新增一个 `wqbrain-alpha-quality-helper` skill 入口，可在对话中被调用
- skill 内置 4 个子能力：配置审查器 / 表达式预审 / 结果诊断 / 提交策略建议
- 内置一份 WQ 提交硬性标准速查表（Sharpe>1.25, Fitness>1, SelfCorr<0.7）
- 内置老强教程 + WQ 官方文档的关键概念索引
- 给出可直接使用的 Markdown 报告模板（贴到工具 Alphas/统计 Tab 旁对照）
- **BREAKING** 无（本项目是新增 skill，不改任何已有代码或工具行为）

## Impact
- Affected specs: `learn-sillytavern-character-cards`（无影响，仅同级目录）
- Affected code: 在 `.trae/skills/`（或当前环境约定路径）下新增 `wqbrain-alpha-quality-helper/` 目录
- 依赖资源：
  - WQ 平台 `https://platform.worldquantbrain.com/`（参考资料，不直连）
  - 老强教程 `https://alphadoc.biglongxia.com/`（参考资料）
  - 工具 exe（学员本地 Windows，不在 skill 部署范围）
  - 学习任务 `https://www.kdocs.cn/l/chtbk1FwoNW5`（参考资料，登录态）
  - IMA 知识库 `https://ima.qq.com/wiki/?shareId=...`（参考资料）
  - 量化基础音频 `https://music.163.com/djradio?id=1491069988`（参考资料）

## ADDED Requirements

### Requirement: Skill 入口与触发词
skill SHALL 提供一个可被 AI 主对话识别的入口，触发词覆盖以下至少 3 种：
- "帮我审一下这个配置" / "看看一阶段参数"
- "这个表达式能过吗" / "alpha 预审"
- "Sharpe 1.0 / Fitness 0.6 还能救吗" / "帮我看回测"
- "今天还能交几个" / "提交策略"

#### Scenario: 学员贴一段配置文本
- **WHEN** 学员贴入一阶段或二阶段的参数（Dataset / Region / Delay / Neutralization / Decay / Max Run / Sharpe 阈值 / Fitness 阈值 / 最少做多空数）
- **THEN** skill 立刻返回「合理性评分 + 风险点 + 建议调整值」
- **AND** 指出至少 1 个新手最常踩的坑（如 Max Run 太大、Sharpe 阈值设到 0.75 但实际提交要求 1.25）

#### Scenario: 学员贴一段 Fast Expression
- **WHEN** 学员贴入一段 `rank(...)`、`ts_rank(...)` 之类的表达式
- **THEN** skill 返回：表达式结构拆解、潜在的数据字段覆盖度风险、可能触发的平台检查项（Self Correlation / Drawdown / Turnover）

### Requirement: 配置审查器
skill SHALL 内置一份"老强工具三阶段参数合理性"检查清单：
- 一阶段必查项：Dataset 是否支持中性化 Subindustry、Region 是否为 USA（学员主流）、Delay=1 vs 0 的取舍、Neutralization 选 Subindustry 时 Decay 是否合理、Max Run 2000 是否过大
- 二阶段必查项：Sharpe 阈值（0.75 是初筛门槛、不是提交门槛，需明确告知）、Fitness 阈值（0.5 同理）、最少做多/空数（默认 100，过滤小样本）
- 三阶段（截图未拍到，但根据上下文推测为最终精筛/提交）必查项：Sharpe 是否 > 1.25、Fitness 是否 > 1、Self Correlation 是否 < 0.7

#### Scenario: 默认配置审查
- **WHEN** 学员贴入工具默认截图所示配置（analyst4 / USA / Delay=1 / Subindustry / Max Run=2000；Sharpe 阈值 0.75 / Fitness 阈值 0.5 / 最少多空 100）
- **THEN** skill 输出：配置能跑，但二阶段阈值 0.75/0.5 是"种子筛选"门槛，不是 WQ 平台最终提交门槛；建议在三阶段把阈值上调到 1.25/1.0，或在三阶段做更严的二次过滤

### Requirement: 表达式预审
skill SHALL 能根据表达式静态文本给出预审结论，**不**模拟回测（因为 skill 没有 WQ API 权限），但能：
- 识别表达式是否使用了 3 大类操作（Arithmetic / Logical / Time Series）
- 识别是否包含常见低分陷阱：
  - 未做 rank / 归一化（直接用 close）
  - 使用了 `delay=0` 但未做中性化（市场暴露过强）
  - `trade_when` 条件过松
  - 时间窗口过短（< 5）或过长（> 252）
- 给出至少 3 条改写建议模板

#### Scenario: 一个简单位反转表达式
- **WHEN** 学员贴入 `(high + low)/2 - close`
- **THEN** skill 返回：结构上属于 Arithmetic + Time Series；建议加 `rank()`、`group_neutralize(sector)`、考虑 `truncation=0.05` 控制单股权重；预测 Sharpe 大概率落在 1.2-1.8 区间（基于论坛共识）

### Requirement: 回测结果诊断
skill SHALL 解读 IS Summary 的所有指标，并给出"该指标不合格时的具体改进方向"：

| 指标 | 合格线 | 不合格时建议 |
|---|---|---|
| Sharpe | > 1.25（提交）/ > 1.5（IQC） | 加 rank / 减换手 / 调整 decay |
| Fitness | > 1 | 公式 `Sharpe * sqrt(abs(Returns)/max(Turnover, 0.125))`，需先压 turnover |
| Turnover | 1%-70% | 用 `decay_linear` / 减少高频字段 |
| Returns | 越高越好 | 看 Drawdown 是否过大 |
| Drawdown | 越小越好 | 检查是否单股集中 |
| Margin | 越高越好 | 减 truncation |
| Self Correlation | < 0.7 | 改一组字段 / 改中性化维度 |

#### Scenario: 学员贴入回测 JSON
- **WHEN** 学员贴入 `{sharpe: 1.05, fitness: 0.7, turnover: 0.65, drawdown: 0.18, returns: 0.12, self_correlation: 0.62}`
- **THEN** skill 返回：当前能过初筛但不能提交；Sharpe 1.05 离 1.25 差 0.2，建议加 rank + 缩短 decay；Fitness 0.7 偏低，主要被 turnover 0.65 拖累，建议用 `decay_linear(volume, 5)` 把换手降到 0.3 左右；Self Correlation 0.62 处于安全区

### Requirement: 提交策略建议
skill SHALL 根据学员的账户画像（截图头部信息：714/1800 用量、铜陵-4000 余额、2/3 进度、账户 3110175350）和 WQ 平台规则，给出当日提交策略。

#### Scenario: 学员问"今天还要交吗"
- **WHEN** 学员贴入"714/1800"（即当日已用 / 总额）
- **THEN** skill 返回：当日剩余 1086 次仿真额度；按 1 个高质量 alpha 需 200-400 次仿真估算，可再启动 3-5 个三阶段任务；建议把二阶段 Sharpe 阈值从 0.75 提到 1.0，避免后面堆积

#### Scenario: 学员问"怎么解锁 Super"
- **WHEN** 学员贴入"我已经交了 80 个 Regular"
- **THEN** skill 返回：按平台规则，100 个 Regular 解锁 Super（每天 1 个）；还差 20 个，建议在剩余 20 个内刻意去做高换手+低相关性方向，给 Super 让路

### Requirement: 学习资源索引
skill SHALL 在内部维护一份"高频引用资源"索引，引用时以 Markdown 链接返回：
- WQ 官方：`https://platform.worldquantbrain.com/learn/operators`（运算符字典）
- WQ 官方：`https://platform.worldquantbrain.com/learn/data-and-operators/datasets`（数据集字典）
- 老强教程：`https://alphadoc.biglongxia.com/`（学习路径主页）
- IMA 知识库：`https://ima.qq.com/wiki/?shareId=f609041b0a72e8c20a8462b896618312c4625986e8d5c5ba1bfb00a43d239ae8`
- 量化音频：`https://music.163.com/djradio?id=1491069988`

#### Scenario: 学员问"哪里学 group_neutralize"
- **WHEN** 学员提问包含运算符名
- **THEN** skill 返回 1-2 条直达链接 + 该运算符的中文用途 + 一段最小示例

## MODIFIED Requirements
无（这是全新 skill，不修改任何已有 spec）。

## REMOVED Requirements
无。

## Key References (论坛/官方汇总，供 skill 内置使用)

- 提交三硬性条件：Sharpe > 1.25、Fitness > 1、Self Correlation < 0.7
- 例外条款：Sharpe 比历史相似 alpha 高 10% 以上（即 > 1.375），可忽略 Self Correlation
- 路径：10000 分金牌 → 顾问邀请 → 累计 20+ 个 alpha（国内路径） → Regular 1-4 个/天 → 满 100 个解锁 Super
- IQC 加分指标：Sharpe > 1.5、Turnover 0.1-0.9、Fitness > 1、IC > 0.02
- 反面规则：严禁抄袭 alpha（永久封号风险）、非原创检测
- 经验共识：提升收入 = 优化代码（提效）+ 理解 operators 与字段（提质）；暴力组合不划算
- 工具观察：当前学员已用 714/1800 次仿真；账户 3110175350 处于活跃期；二阶段默认阈值 0.75/0.5 是"种子筛选"门槛而非"提交"门槛，混用是新手最大误区
