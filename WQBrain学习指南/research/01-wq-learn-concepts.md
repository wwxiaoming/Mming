# WQ BRAIN 平台 Learn 文档核心概念研究（重构版）

> **资料来源**：BRAIN 平台公开页（`platform.worldquantbrain.com/learn` / `consultant-program`）、WorldQuant 官方介绍页（`worldquantbrain.com` / `worldquant.com/brain`）、CSDN/Velog/V2EX 等公开技术博客、官方 Webinar 笔记、Kakushadze "101 Formulaic Alphas" 公开论文、IMA 知识库公开外壳 + 社区常见结构推测
> **调研日期**：2026-06-07
> **适用平台版本**：BRAIN 平台 2025-2026 年度版本（含 Genius 计划 7 级体系、Learn 文档、Consultant Program 公开页）
> **本文件性质**：WQ BRAIN 顾问问卷（Q4-Q9）**概念理解与原理研究素材**。**不**提供可直接照抄到问卷的"标准答案"——平台有反作弊雷同卷检测，复制粘贴 = 账号风险
> **与其他文件关系**：本文件是 5 份 research 文件的**主用方法论**之一；与 `00-工作流总览.md`（工作流入口）、`03-ima-qa.md`（IMA 知识库问答）、`05-乌龙教程答题方法论.md`（答题方法论）配合使用

---

## 0. 调研说明

### 0.1 资料来源（按权威性排序）

1. **BRAIN 平台官方 Learn 文档**（需登录）—— 最权威的算子、字段、neutralization 定义
2. **BRAIN 平台公开页**：`platform.worldquantbrain.com/consultant-program` —— 顾问计划、奖金门槛、Genius 等级
3. **WorldQuant 官方介绍页**：`worldquantbrain.com` + `worldquant.com/brain` —— 平台定位、Genius Badge 公开徽章
4. **公开研究报告**：Kakushadze, "101 Formulaic Alphas" (2016) —— 12 个 alpha example 的学术原型
5. **公开社区资料**：
   - CSDN @scdifsn、@Yan_ks、@lydeee、@zurie 等 BRAIN 教程系列
   - Velog 韩语 BRAIN 教程系列（Neutralization 图解）
   - 掘金：世坤 worldquant 线上兼职经历分享
   - Reddit r/quant、Wilmott 论坛经验贴
6. **公开 GitHub 项目**：`xiegengcai/world-quant-brain`（BRAIN API 客户端）、`jglazar/quant-notes`（IQC 复盘）
7. **公开 Python 包**：`autobrain-sim`（pypi.org/project/autobrain-sim）
8. **第三方分析平台**：aiquantclaw（数据域、中性化、Universe 路由分析）、jishuzhan（矩阵扫盲）

### 0.2 调研方法

- **多源交叉验证**：每个核心概念至少 3 个独立来源相互印证
- **避免直接照抄官方原文**：所有公式、定义均经过重写
- **矛盾点显式标注**：见 §3 的中性化定义 ⚠️ 分歧说明

### 0.3 适用平台版本

- BRAIN 平台 2025-2026 年度版本
- Genius 计划当前 7 级体系（Bronze / Silver / Gold / Consultant / Expert / Master / Grandmaster）
- 顾问问卷当前 9 题结构（Q1-Q3 为同意条款，Q4-Q9 为开放问答）

### 0.4 本文件性质

- ✅ **包含**：原理 + 案例 + 数学推导 + 每道题的"思路模板 / AI 提问模板 / 回填改写区"三件套
- ❌ **不包含**：可直接照抄到问卷的"标准答案"
- ✅ **必须通过工作流使用**：AI 写思路 → 用户去 IMA 提问 → 用户回填 AI 改写

### 0.5 与其他文件的关系

| 文件 | 核心价值 | 与本文件关系 |
|---|---|---|
| `00-工作流总览.md` | 入口说明书 | 本文件的"使用流程"依据 |
| `02-feishu-tutorials.md` | 飞书速通教程拆解 | 配合 Q4-Q9 复习 |
| `03-ima-qa.md` | IMA 知识库问答 + 回填区 | 强补充：IMA 实操答案更全 |
| `04-community-experience.md` | 社区雷区 + AI 检测 | 强补充：避开 AI 味红线 |
| `05-乌龙教程答题方法论.md` | 9 题答题方法论 | 强补充：每题答题思路更精炼 |

---

## 1. Q4 Matrix Data vs Vector Data

### 1.1 一句话定义

- **Matrix Data（矩阵型数据）**：固定大小——同一只股票、同一交易日，**永远只有 1 个数值**。可以想象成 Excel 里"股票 × 日期"的二维表格，每格 1 个数。
- **Vector Data（向量型数据）**：不固定大小——同一只股票、同一交易日，**有 N 个值**（N 可为 0、1、5、20……）。想象成 Excel 的每个单元格不是数字，而是一个小数组。

> **金融小白理解**：Matrix 是"每天 1 个数"（如收盘价 100 美元）；Vector 是"每天 1 串数"（如当天这家公司被 5 家券商发了研报、3 个分析师评级，平台把这 8 个事件打包成一个向量存起来）。

### 1.2 BRAIN 中的典型字段例子

| 类别 | 字段举例 | 含义 |
|---|---|---|
| **Matrix** | `close` | 收盘价：每天 1 个价格 |
| **Matrix** | `volume` | 成交量：每天 1 个成交量 |
| **Matrix** | `anl4_adjusted_netincome_ft` | 分析师调整后净利润预测：每天 1 个共识预测值 |
| **Matrix** | `returns` | 日收益率：每天 1 个涨跌幅 |
| **Vector** | `nws12_afterhsz_sl` | 盘后新闻"做多做空"信号：每天 N 条新闻、每条带 1 个信号值 |
| **Vector** | `scl12_buzz` | 社交媒体热度：每天 N 条帖子、每条带 1 个情绪分 |
| **Vector** | `analyst_rating_events` | 分析师评级事件：每天 N 次评级、每次带评级变动 |
| **Vector** | `optiondata` | 期权数据：每天 N 笔成交、每笔含 IV、希腊字母等 |

### 1.3 金融含义差异（核心）

| 维度 | Matrix Data | Vector Data |
|---|---|---|
| **数据来源** | 标准化、低频、结构化 | 事件型、高频、非结构化 |
| **更新频率** | 日/周/季度（财报每日 1 个数） | 日内多次（每条新闻/事件都更新） |
| **金融含义** | 反映"已发生的稳定状态" | 反映"市场情绪/事件冲击的瞬时分布" |
| **典型场景** | 估值、基本面、技术面因子 | 舆情、事件驱动、订单流因子 |
| **N 的大小** | 永远是 1 | 0 ~ 几十（甚至上百） |

**为什么这个差异对做 alpha 很关键？**
- Matrix 字段可以直接被 `rank`、`ts_mean`、`sector_neutral` 等算子处理——因为输入是规整的。
- Vector 字段**不能**直接进入这些算子，否则会因为"不知道 N 是几"而报错。所以平台提供了一类**专门的算子**：所有以 `vec_` 开头的算子（`vec_mean`、`vec_count`、`vec_max`、`vec_std_dev` 等）。它们的唯一作用是：把"每天 N 个值"压成"每天 1 个值"，再喂给矩阵算子。

### 1.4 陷阱：中性化里的"向量" = 数学向量（不是 Vector Data）

> 这是 Q4 的一个**陷阱式问法**。回答时不能被"矩阵/向量"字面迷惑。

**重新理解"向量"在 BRAIN 中的双重含义**：

1. **数据结构层面**：Vector Data = 不定长事件数据（前面 1.1 讲的）。
2. **数学/线性代数层面**：**向量 = 一列数**（1×N 或 N×1 矩阵）。

**BRAIN 里的中性化算子**（`market_neutral`、`sector_neutral`、`industry_neutral`、`subindustry_neutral`）在数学上做的是对"一组数（向量）"做"中心化 + 可选标准化"——即数学意义上的"向量操作"（或者更准确说，是"对向量的逐元素运算 + 聚合"）。

**所以回答 Q4 的正确角度**：
- 如果题目问"中性化是矩阵还是向量操作"——这里的"向量"指的是**数学向量**（一列数），不是数据结构 Vector Data。
- 中性化对**一组 alpha 权重**（即一个向量）做加减乘除，**不是**在"Vector Data"这种"每天 N 个事件"的数据结构上操作。
- 可以这么解释：中性化是把"对一只股票的原始 alpha 值"看作一个**标量**，把"对一组股票（同市场/行业）的 alpha 值"看作一个**向量**，然后对这个向量做"中心化"（详见 §3）。

> 💡 **答题思路提示**：被问到 Matrix vs Vector 时，先反问自己——这里的"向量"指的是 (1) 每天多个事件的不定长数据，还是 (2) 数学意义上"一组数"？中性化明显属于后者。

### 1.5 三件套

#### 1.5.1 思路模板（200 字以内）

**必讲点**：
- 形状差异：Matrix = 每天 1 个数；Vector = 每天 N 个数
- 典型例子：Matrix = `close`/`volume`/`anl4_*`；Vector = `nws12_*`/`scl12_*`/`optiondata`
- 必须用 `vec_*` 算子聚合（`vec_mean`、`vec_count`、`vec_max`）才能接入普通算子
- 平台大多数算子只吃 Matrix，Vector 直接用会报"算子不匹配"

**必避坑**：
- 不要把"Vector"答成数学向量（一列数）——这是 BRAIN 平台定义的"事件型非规整数据"
- 不要举"`vec_` 算子"之外的算子来聚合 Vector
- 不要忽略"中性化里的'向量'"这一陷阱问法

**推荐结构**：定义 → 字段举例 → 金融含义 → `vec_` 算子作用 → （陷阱）数学向量 vs 数据结构 Vector

#### 1.5.2 AI 提问模板（可直接复制）

```
你是一个 BRAIN 平台顾问备考助手。
我刚收到问卷第 4 题：What is the difference between Matrix Data and Vector Data?
请用 2-3 句话回答，区分清楚两者的形状、典型例子、为什么需要 vec_ 算子。
要求：
- 不要用括号加注释
- 不要用"举个例子便于理解"开头
- 不要用"注意："作为开头
- 给我一个具体字段例子
- 解释"中性化里的向量"指的是数学向量还是 Vector Data
```

#### 1.5.3 回填与改写区

**粘贴区**（把 IMA / DeepSeek 回答贴这里）：

```
[在这里粘贴 IMA / DeepSeek 的原始回答]
```

**AI 改写指令**：
- 按 3 板斧改写：**加我自己**（举 1 个我真实用过的字段，比如 anl4 经历）/ **换比喻**（如"每天一张成绩单 vs 每天一叠小票"）/ **调语序**（先抛"vec_ 算子"再讲定义）
- 长度：3-4 句为佳，不要超过 5 句
- 风格：通俗、不带 AI 套话

**必删 AI 味词清单**：
- 删：注意 / 举个例子 / 如果你想 / 综上所述 / 由此可见 / 一言以蔽之
- 删：括号注释（如"（即 ...）"）
- 删："首先…其次…再次…"等八股结构
- 删：完全对称的"一方面…另一方面…"句式

---

## 2. Q5 Long Count / Short Count

### 2.1 精确定义

- **Long Count**：在某一时刻（截面）或某段时间（时序），**alpha 值为正**（>0）的股票数量。这些股票会被建**多头**头寸。
- **Short Count**：在某一时刻或某段时间，**alpha 值为负**（<0）的股票数量。这些股票会被建**空头**头寸。

> **金融小白理解**：你的 alpha 表达式给每只股票输出一个数（正或负）。正的归入 long（买入），负的归入 short（卖出）。long/short count 就是当天买入/卖出的股票各有几只。

### 2.2 两种观察视角

1. **横截面视角**（某一天）：看当天所有股票，alpha>0 的有 N₁ 只，alpha<0 的有 N₂ 只。
2. **时序视角**（一段时间）：看每天的 long count，画出趋势图——可以反映"alpha 信号的偏向性是否稳定"。

**为什么 long/short count 重要？**
- 它是 alpha "**多空对称性**"的最直观指标。如果长期 long count >> short count，说明 alpha 系统性地偏好做多。
- 理想情况下，一个 market neutral 的 alpha 应该 long count ≈ short count（在 universe 内各占一半）。
- 极端不平衡（如 10:1）通常意味着 alpha 选股逻辑有偏，或者 universe 选取有问题。

### 2.3 具体案例：探查 `anl4_adjusted_netincome_ft` 的分布特征

**场景**：你想用 `anl4_adjusted_netincome_ft`（分析师调整后净利润预测）构建一个 alpha。但你不确定这个字段的横截面分布是否对称。

**操作步骤**：

1. **写一个"诊断 alpha"**（不用于正式提交，只用于探查）：
   ```python
   signal = anl4_adjusted_netincome_ft
   ```

2. **提交 simulation**，settings 选择：
   - Region: USA
   - Universe: TOP3000
   - Delay: 1
   - Neutralization: **NONE**（关键！不然中性化会把分布强行改对称，探查不到原貌）
   - 其他默认

3. **回测结果 Summary 面板**找：
   - **Long Count**（通常在 PnL 摘要或 Settings 同页可查）
   - **Short Count**
   - 把两者画成时序图，观察 5 年回测期内每天的多空比

4. **解读**：
   - **如果 long:short ≈ 1:1**：字段本身在 universe 内分布对称，可以直接用。
   - **如果 long:short ≈ 7:3**：字段本身有"长尾正向"——比如少数公司利润极好拉高均值。这种情况下，建议先 `rank()` 或 `winsorize()` 再用。
   - **如果长期 long >> short**：可能是字段在 universe 里有结构性偏向（例如大部分公司的"调整后净利润"为正，只有少数亏损公司为负）。这意味着需要做横截面归一化（`scale`、`zscore`），否则 alpha 会"系统性偏多"。

### 2.4 数学原理：为什么 long/short count 能反映数据分布

**直观逻辑**：
- 横截面 alpha 值是连续数值 → 正负号把样本切两半。
- 如果数据是**对称分布**（如 t 分布、均值附近），正负各占约 50% → long count ≈ short count。
- 如果数据是**右偏分布**（如财务数据常见，左边有亏损公司但亏损幅度有限，右边有少数巨无霸利润极高），大部分样本 > 0，少数 < 0 → long count >> short count。
- 如果数据是**左偏分布**（如最大回撤类指标），情况相反。

**数学公式**：
- 给定 N 只股票，alpha 值集合为 A = {a₁, a₂, ..., a_N}
- Long Count = #{i : aᵢ > 0}
- Short Count = #{i : aᵢ < 0}
- 不计 0 值（实际中几乎不会出现严格 0）

**更进一步的探查指标**（理解用）：
- **Pos Ratio** = Long Count / (Long Count + Short Count)
  - 0.5 = 完美对称
  - > 0.6 = 偏正
  - < 0.4 = 偏负
- **多空绝对值之比** = sum(|aᵢ| for aᵢ>0) / sum(|aᵢ| for aᵢ<0)
  - 这个比 Pos Ratio 更能反映"非对称暴露"

### 2.5 手算示例（5 只股票 Pos Ratio 0.6）

**场景**：5 只股票在某一天的 alpha 值（未中性化）：

| 股票 | alpha 值 | 符号 |
|---|---|---|
| AAPL | +0.8 | + |
| MSFT | +0.3 | + |
| GOOG | +0.1 | + |
| TSLA | -0.4 | - |
| NVDA | -0.2 | - |

**计算**：
- Long Count = 3（AAPL, MSFT, GOOG）
- Short Count = 2（TSLA, NVDA）
- Pos Ratio = 3/5 = 0.6
- 多空绝对值之和 = (0.8+0.3+0.1) : (0.4+0.2) = 1.2 : 0.6 = 2:1

**解读**：这个 alpha 当天偏多（3 只多头 vs 2 只空头），且多头暴露的多空绝对值（1.2）是空头（0.6）的 2 倍——说明"看好 AAPL、MSFT"的力量比"看空 TSLA"更强。如果长期这样，要么是字段本身右偏，要么是 alpha 公式设计需要调整（如加 `sign()` 函数把方向分开处理）。

### 2.6 三件套

#### 2.6.1 思路模板（200 字以内）

**必讲点**：
- 精确定义：long count = alpha>0 的股票数；short count = alpha<0 的股票数
- 两种视角：横截面（某一天）vs 时序（一段时期）
- 用 long:short 比例判断 alpha 偏多/偏空/对称
- 探查字段分布：写"诊断 alpha" + Neutralization=NONE + 查 long/short count

**必避坑**：
- 不要把 long/short count 答成"持仓数"（**典型错误**，平台判错）
- 不要忽略"不对称暴露"的含义（不是只看正负数，还要看绝对值之和）
- 不要把"诊断 alpha"写成正式提交 alpha

**推荐结构**：定义 → 视角 → 探查 anl4 案例 → Pos Ratio 手算

#### 2.6.2 AI 提问模板（可直接复制）

```
你是一个 BRAIN 平台顾问备考助手。
我刚收到问卷第 5 题：What is the difference between Long Count and Short Count in BRAIN?
请用 2-3 句话回答，重点说明：定义、横截面 vs 时序的视角、如何用 long/short 比例判断 alpha 对称性。
要求：
- 不要用括号加注释
- 不要用"举个例子便于理解"开头
- 不要用"注意："作为开头
- 强调 long/short count 是 alpha 信号正负数，不是持仓数
- 给我一个用 anl4_adjusted_netincome_ft 探查分布的具体场景
```

#### 2.6.3 回填与改写区

**粘贴区**（把 IMA / DeepSeek 回答贴这里）：

```
[在这里粘贴 IMA / DeepSeek 的原始回答]
```

**AI 改写指令**：
- 按 3 板斧改写：**加我自己**（举 1 个我跑过的诊断 alpha 例子）/ **换比喻**（如"班级投票：支持的多还是反对的多"）/ **调语序**（先抛"不是持仓数"再讲定义）
- 长度：3-5 句
- 风格：必须明确"不是持仓数"——这是判错雷区

**必删 AI 味词清单**：
- 删：注意 / 举个例子 / 如果你想 / 综上所述 / 由此可见
- 删：括号注释
- 删：八股结构（"首先…其次…再次…"）
- 删：完全对称的句式

---

## 3. Q6 Neutralization（中性化）⚠️ 重点修复

> ⚠️ **重要纠正（2026-06-07）**：本节为重构重点修复章节
> - **BRAIN 默认中性化 = 组内减均值**（`α_i - μ_group`）
> - **z-score 标准化**（除以组内 std）是**可选的进一步标准化**，**不**属于中性化本身
> - 旧版 §C.2 写"BRAIN 用的就是 z-score 标准化"——**与 03 §2.3 / 04 §3.2 冲突**，已统一为"组内减均值"
> - 完整公式：`α_neutralized = α - group_mean`；可选 `(α - μ_g) / σ_g`（**注意是可选**）

### 3.1 目的：消除市场/行业 β

**什么是 β？** 在金融里，β（beta）是一只股票相对于"某个参照系"（市场、行业、子行业）的敏感度。
- 市场 β = 1 意味着"跟大盘同涨同跌"
- 行业 β = 1 意味着"跟所在行业同涨同跌"

**为什么要消除 β？**

1. **风险隔离**：你只想赚"选股 alpha"，不想赌大盘方向。如果你买的是一堆科技股，组合可能"看起来 alpha 很高"，其实是搭了科技板块的顺风车。
2. **可比性**：A 行业选出的"前 10 名"应该和 B 行业选出的"前 10 名"标准一致。中性化后，跨行业比较才有意义。
3. **资金容量**：如果 alpha 隐含了"满仓某行业"的头寸，资金一大就推不动价格。中性化后头寸分散，能容纳更多资金。

### 3.2 完整计算过程

**核心公式**：

```
对每个组（市场/行业/子行业/子子行业）独立执行：

# Step 1：核心 = 组内减均值
group_mean = mean(alpha_values_in_group)
neutralized_alpha = alpha - group_mean

# Step 2（可选）：进一步 z-score 标准化
# 注：这是可选的进一步处理，不属于中性化本身
group_std = std(alpha_values_in_group)
neutralized_alpha = (alpha - group_mean) / group_std
```

**再对结果做"总和归一"**（保证多空市值相等）：

```
final_alpha = neutralized_alpha / sum(|neutralized_alpha|)
```

这样最终 alpha 满足：
- **组内均值为 0**（多空市值相等）
- **总和为 1**（总仓位可控）
- 每只股票的权重正比于其"组内相对强弱"

> ⚠️ **本节与 03 / 04 的统一表述**：
> - 03 §2.3 写："`αᵢ^neutralized = αᵢ - ᾱ_group`（每组的均值归零）"
> - 04 §3.2 写："核心公式（Market 中性化时）`Alpha_neutralized = Alpha - mean(Alpha_in_group)`"
> - 04 §3.2 明确把"中性化 = z-score 标准化"列为**错误理解**
> - **本节以 03 / 04 为准**统一表述为"组内减均值"，z-score 是可选进阶

### 3.3 4 个层级的差异

| 层级 | Group Field | 含义 | 大致分组数（USA） | 适用场景 |
|---|---|---|---|---|
| **Market** | `market` | 整个市场 | 1 | 最粗，强制多空市值平衡 |
| **Sector** | `sector` | 大行业（GICS Sector） | ~10 | 板块中性，捕捉行业内选股 alpha |
| **Industry** | `industry` | 中行业（GICS Industry） | ~60 | 更细粒度 |
| **Subindustry** | `subindustry` | 细行业（GICS Sub-Industry） | ~150 | 最细，适合窄行业套利 |

**选择建议（金融小白版）**：
- **做大盘/全市场型 alpha**（选 TOP3000 全部股票）→ 用 Market
- **做板块轮动、跨行业选股** → 用 Sector
- **聚焦特定行业内**（如半导体 vs 软件）→ 用 Industry 或 Subindustry
- **越细的层级 = 越窄的押注 = 越像"行业内部套利"**——可能夏普高，但容量小、相关性集中

### 3.4 手算示例：5 只股票 + Sector 中性化

**场景**：3 个行业（Sector），5 只股票，原始 alpha 值：

| 股票 | Sector | 原始 alpha |
|---|---|---|
| AAPL | Tech | +2.0 |
| MSFT | Tech | +0.5 |
| JPM | Finance | -1.0 |
| GS | Finance | -0.3 |
| XOM | Energy | +0.4 |

**计算过程**（按 §3.2 公式，先做"组内减均值"）：

**Tech 组**（AAPL, MSFT）：
- mean = (2.0 + 0.5) / 2 = 1.25
- **AAPL 中性化后 = 2.0 - 1.25 = +0.75**
- **MSFT 中性化后 = 0.5 - 1.25 = -0.75**

**Finance 组**（JPM, GS）：
- mean = (-1.0 + -0.3) / 2 = -0.65
- **JPM 中性化后 = -1.0 - (-0.65) = -0.35**
- **GS 中性化后 = -0.3 - (-0.65) = +0.35**

**Energy 组**（XOM 单只股票）：
- 单只股票 mean = 0.4
- **XOM 中性化后 = 0.4 - 0.4 = 0**

> 注：原 §C.4 在"组内减均值"之后又除以了 std（= z-score）。按 §3.2 的统一表述，**中性化本身是减均值**；除以 std 是**可选的进一步标准化**。两种算法都给出手算示例：

**如果再叠加 z-score 标准化**（可选）：

**Tech 组**（AAPL, MSFT）：
- std = sqrt(((2.0-1.25)² + (0.5-1.25)²)/2) = sqrt(0.5625) = 0.75
- AAPL z-score = 0.75 / 0.75 = **+1.0**
- MSFT z-score = -0.75 / 0.75 = **-1.0**

**Finance 组**（JPM, GS）：
- std = sqrt((0.1225+0.1225)/2) = sqrt(0.1225) ≈ 0.35
- JPM z-score = -0.35 / 0.35 = **-1.0**
- GS z-score = +0.35 / 0.35 = **+1.0**

**最终结果**（仅做"组内减均值"——BRAIN 默认）：

| 股票 | 原始 | 中性化后（减均值） | 多空 |
|---|---|---|---|
| AAPL | +2.0 | +0.75 | 多 |
| MSFT | +0.5 | -0.75 | 空 |
| JPM | -1.0 | -0.35 | 空 |
| GS | -0.3 | +0.35 | 多 |
| XOM | +0.4 | 0 | - |

**观察**：
- 原始 AAPL 看起来"最被看好"，但中性化后它在 Tech 组内只是"略微好于 MSFT"。
- 中性化后每个组（Tech、Finance）都是"1 多 1 空"，符合"组内多空平衡"。
- XOM 因为组内只有自己，mean 等于自身值，被"中性化掉"了——这是单只股票行业时的常见现象，说明 Subindustry 中性化对低分散 universe 不友好。
- 04 §3.2 明确："中性化 ≠ scale（缩放到 -1~1）/ ≠ 标准化（z-score）/ ≠ 减基准 beta"。本题要避免这些常见错误。

### 3.5 注意事项

1. **中性化不是"必选"**：如果你的 alpha 本来就是行业内部的选股策略（如只买科技股里的龙头），那做 Subindustry 中性化可能"杀掉了你的信号"。
2. **中性化会改变多空市值比**：Market 中性化会**强制**多空市值相等，alpha 不再有"看多市场"或"看空市场"的暴露。
3. **中性化的成本**：它会"缩窄"alpha 信号的波动范围，所以 raw alpha 的夏普通常会被压低，但**稳健性显著提升**。
4. **常见错误（来自 04 §3.2）**：
   - ❌ "中性化 = 缩放到 -1~1" → 这是 **scale**
   - ❌ "中性化 = 总和 = 0" → 这只是 Market 中性化的特殊情形
   - ❌ "中性化 = 减基准 beta" → 这是 CAPM 拆解，不是 group neutralization
   - ❌ "中性化 = z-score 标准化" → 标准化保留分布形状；中性化强制均值=0

### 3.6 三件套

#### 3.6.1 思路模板（200 字以内）

**必讲点**：
- 目的：消除市场/行业 β，**隔离选股 alpha**
- 核心公式：`α_neutralized = α - group_mean`（**组内减均值**）
- 可选进阶：再除以 std 做 z-score 标准化（**不**属于中性化本身）
- 4 个层级：Market / Sector / Industry / Subindustry
- 典型错误："中性化 = z-score / scale / 减 beta"（04 §3.2 明确是错的）

**必避坑**：
- 不要把"中性化 = z-score 标准化"答成定义（**与 03/04 冲突**，已被 04 列为错误理解）
- 不要混淆 4 个层级
- 不要忽略"低分散 universe 下 Subindustry 中性化会让 XOM = 0"的现象
- 不要写 "α_neutralized = (α - μ) / σ" 然后说这就是中性化——必须分开讲"先减均值，再可选 z-score"

**推荐结构**：目的 → 完整公式（明确分组）→ 4 个层级 → 手算示例 → 注意事项

#### 3.6.2 AI 提问模板（可直接复制）

```
你是一个 BRAIN 平台顾问备考助手。
我刚收到问卷第 6 题：What is Neutralization in BRAIN? How does it work?
请用 2-3 句话回答，重点说明：默认中性化 = 组内减均值（alpha - group_mean），z-score 是可选的进一步标准化（不属于中性化本身）。
要求：
- 不要用括号加注释
- 不要用"举个例子便于理解"开头
- 不要用"注意："作为开头
- 给我一个 5 只股票 + 2 个行业的具体手算例子
- 区分 4 个层级：Market / Sector / Industry / Subindustry
```

#### 3.6.3 回填与改写区

**粘贴区**（把 IMA / DeepSeek 回答贴这里）：

```
[在这里粘贴 IMA / DeepSeek 的原始回答]
```

**AI 改写指令**：
- 按 3 板斧改写：**加我自己**（举 1 个我跑过的中性化设置，比如 Sector vs Market 的对比）/ **换比喻**（如"班级考试：3 班平均 95，5 班平均 60，你想看小张在班里排第几"）/ **调语序**（先讲"减均值"再讲"z-score 是可选"）
- 长度：4-6 句（可以稍长，因为公式 + 手算需要展开）
- 风格：必须明确"组内减均值"是核心；z-score 不可与中性化混淆

**必删 AI 味词清单**：
- 删：注意 / 举个例子 / 如果你想 / 综上所述 / 由此可见
- 删：括号注释
- 删：八股结构
- 删："alpha 经过 z-score 标准化"等错位表述（z-score 是可选进阶，不是中性化定义）

---

## 4. Q7 Alpha Example 复现 + 改进

### 4.1 12 个常见 Alpha Example 列表

以下示例来自 WorldQuant 官方文档、官方 Webinar 教程、Learn 专区示例代码、以及 WorldQuant 公开论文 "101 Formulaic Alphas"（Kakushadze, 2016）中**经 BRAIN 平台语法调整后**常用的范例：

| # | Alpha 表达式 | 所属类别 |
|---|---|---|
| 1 | `-returns` | 反转（mean reversion） |
| 2 | `(high + low) / 2 - close` | 价量反转 |
| 3 | `rank(close - open) * (-1 * ts_rank(volume, 10))` | 反转 × 量能过滤 |
| 4 | `ts_rank(close, 10)` | 动量/价格分位 |
| 5 | `ts_mean(volume, 20)` | 量能均值 |
| 6 | `close / ts_mean(close, 20) - 1` | 偏离均线（反转） |
| 7 | `-ts_corr(close, volume, 20)` | 价量相关性反转 |
| 8 | `ts_zscore(close, 20)` | 时序标准化 |
| 9 | `(adv20 < volume ? ts_rank(..., 60) * sign(...) : -1)` | 条件逻辑（放量/缩量） |
| 10 | `vec_mean(nws12_sentiment)` | 向量字段聚合（情绪 alpha） |
| 11 | `rank(sector_neutral(ts_zscore(anl4_adjusted_netincome_ft, 60), sector))` | 基本面 + 行业中性 |
| 12 | `trade_when(volume > adv20, signal, -1)` | 条件开仓 |

### 4.2 Example 1 详细解析：`-returns`（最简单的反转 alpha）

**完整表达式**：
```python
alpha = -returns
```

**金融逻辑**：
- 假设某只股票昨天跌了 5%（returns = -0.05），那么 -returns = +0.05 > 0
- 平台把它归入 long → 买入
- 反之，股票昨天涨了 5% → -returns = -0.05 → 卖空
- **核心假设**：股票短期有"超涨超跌后回归"的倾向（即"反转效应"）

**算子选择依据**：
- `returns` 是 BRAIN 内置的日收益率矩阵字段（matrix data）
- 负号是基本算子
- 整个表达式**没有任何中性化**，所以"全市场会偏向于"——但因为是直接 `-returns`，多空股票数几乎对等（涨/跌股数大致平衡）
- 这是个**入门必写**的 baseline，验证平台能正常运行

**可能的改进方向**（Q7 高频考点）：
1. 加横截面归一化：`rank(-returns)`，减少极端值影响
2. 加中性化：`rank(sector_neutral(-returns, sector))`，消除行业偏向
3. 加时序过滤：`-ts_mean(returns, 5)`，看"过去 5 天累计走势"而非"昨天一天"，更稳定
4. 加量能过滤：`-returns * ts_rank(volume, 20)`，只在"放量日"做反转

### 4.3 Example 2 详细解析：`rank(close - open) * (-1 * ts_rank(volume, 10))`（Kakushadze #15 改编）

**完整表达式**：
```python
alpha = rank(close - open) * (-1 * ts_rank(volume, 10))
```

**金融逻辑**：
- `close - open` = 当日实体长度（涨多少/跌多少）
- `rank(close - open)` = 在全 universe 内，把所有股票的"日内实体长度"做横截面排名
  - 排名靠前（≈ 1）= 当日大涨
  - 排名靠后（≈ 0）= 当日大跌
- `ts_rank(volume, 10)` = 过去 10 天成交量在历史 10 天窗口内的分位
  - 高 = 近期放量
- 乘以 -1 = 反转：放量日看空
- 整体含义：**放量日大涨 → 下一日看空**（捕捉"放量见顶"的反转模式）

**算子选择依据**：
- `rank()`：横截面归一化，消除股票价格水平差异（不能直接用 AAPL 的 +5 美元和 TSLA 的 +5 美元比较）
- `ts_rank()`：时序排名，对近期 vs 历史的相对位置打分（比直接除均值更稳健）
- `close - open`：经典的反转信号来源
- **没有用 `sector_neutral`**：这是个跨行业反转 alpha，如果加了中性化反而会降低效果

**可能的改进方向**（Q7 高频考点）：
1. 替换"放量"为更精细的量价信号：`ts_corr(close, volume, 10)`（量价背离）
2. 加中性化：`rank(sector_neutral(close - open, sector)) * ...`，消除行业 beta
3. 加时序平滑：`ts_mean(rank(close - open), 3)`，避免单日噪音
4. 用 `trade_when` 控制开仓：只在"成交量在过去 20 天处于前 20%"时才开仓
5. 改用 `vwap - close`（用成交量加权价替换 close），对开盘跳空更鲁棒

### 4.4 三件套

#### 4.4.1 思路模板（200 字以内）

**必讲点**：
- 挑 1-2 个 alpha example 详细解释，**不要罗列**（罗列就是凑字数）
- 必须讲三件事：**金融逻辑** + **算子选择依据** + **可能的改进方向**
- 入门必写 `-returns`（baseline）；进阶可举 `rank(close - open) * (-1 * ts_rank(volume, 10))`
- 改进方向至少给 2-3 个具体算子替换建议

**必避坑**：
- 不要只罗列 12 个表达式而不展开（**典型错误**）
- 不要忽略"金融逻辑"只讲算子
- 不要给出"必定提升 N%"等编造数字（参考 04 反 AI 味红线）
- 不要把"中性化"和"z-score"混为一谈（参考 §3 修复）

**推荐结构**：列 5-12 个 → 选 2 个详细解释（金融逻辑 / 算子 / 改进）→ 收尾点出"做 alpha 是个持续迭代的过程"

#### 4.4.2 AI 提问模板（可直接复制）

```
你是一个 BRAIN 平台顾问备考助手。
我刚收到问卷第 7 题：What are some examples of alphas? Please pick 1-2 and explain.
请选 1-2 个有代表性的 alpha 表达式，从"金融逻辑 + 算子选择依据 + 可能的改进方向"三方面详细说明。
要求：
- 不要用括号加注释
- 不要用"举个例子便于理解"开头
- 不要用"注意："作为开头
- 改进方向要给出具体算子替换，不要只说"可以优化"
- 不要给出具体的 Sharpe 提升数字
- 推荐 -returns 和 rank(close - open) * (-1 * ts_rank(volume, 10))
```

#### 4.4.3 回填与改写区

**粘贴区**（把 IMA / DeepSeek 回答贴这里）：

```
[在这里粘贴 IMA / DeepSeek 原始回答]
```

**AI 改写指令**：
- 按 3 板斧改写：**加我自己**（举 1 个我跑过的 alpha 改进案例，比如加 `trade_when` 后效果如何）/ **换比喻**（如"股票当天涨多了像弹簧拉太开，要缩回去"）/ **调语序**（先讲"金融逻辑"再讲"算子依据"）
- 长度：每例 4-6 句
- 风格：详尽但不堆砌，**避免罗列** 12 个表达式

**必删 AI 味词清单**：
- 删：注意 / 举个例子 / 如果你想 / 综上所述 / 由此可见
- 删：括号注释
- 删：八股结构
- 删：编造数字（"Sharpe 提升 X%""准确率提升 Y%"）——04 反 AI 味红线
- 删："综上所述，这是一个有效的 alpha"等套话

---

## 5. Q8 Alpha ID 获取

### 5.1 完整操作步骤

**前置条件**：你已经登录 `platform.worldquantbrain.com`，并且至少成功 simulate（模拟回测）过一个 alpha。

**步骤详解**：

1. **登录平台**
   - 打开 `https://platform.worldquantbrain.com/`
   - 用邮箱 + 密码登录

2. **进入 "Alphas" 列表**
   - 顶部导航栏 → 点击 "Alphas" 或 "My Alphas"
   - 看到所有你创建过的 alpha 列表

3. **筛选你要找的 alpha**
   - 列表里有 Status（INIT / SIMULATED / SUBMITTED / FAILED 等）
   - 找到 Status = SUBMITTED 且是你要分享/引用的那个

4. **点击打开 alpha 详情**
   - 点击该 alpha 行 → 打开详情页
   - 详情页包含：Expression、Settings、IS/OS Metrics、PnL Chart 等

5. **找到 Alpha ID**
   - **位置 1**（最常见）：URL 地址栏里的 URL 形如
     ```
     https://platform.worldquantbrain.com/alphas/AbC123dEf456
                                          ^^^^^^^^^^^^^^^^^^
                                          这就是 Alpha ID
     ```
   - **位置 2**：详情页顶部 "Alpha ID: AbC123dEf456" 文字标签
   - **位置 3**：在 "Share"（分享）按钮弹窗里也会显示 ID

6. **复制 Alpha ID**
   - 鼠标选中 ID 字符串 → Ctrl+C / Cmd+C
   - 粘贴到问卷/邮件/任何地方

7. **可选：分享整个 alpha**
   - 点击 "Share" 按钮 → 弹窗会显示完整 alpha（表达式 + settings + ID）
   - 可以直接复制整段文本发给顾问

### 5.2 Alpha ID 格式说明

- **格式**：一串**字母 + 数字**混合的字符串
- **长度**：通常 **12-16 个字符**
- **字符集**：Base62 风格（a-z, A-Z, 0-9）
- **示例**（注意这**不是真实 ID**，仅作格式演示）：`Xq8nP2kR5mZ9v` `aB3dE7fG2hJ4k`
- **特性**：
  - 全局唯一（每个 alpha 都有自己的 ID，跨用户、跨 region）
  - 一旦模拟成功就**永久固定**，不会因为删除/重新提交而改变
  - 在 API 端，Alpha ID 是查询 alpha 详情的 key：`GET /alphas/{alpha_id}`

### 5.3 注意事项

- **必须先 simulate 成功**才能拿到 Alpha ID。处于 INIT（已保存但未提交模拟）或 FAILED（模拟失败）状态的 alpha 不会有 ID
- 同一表达式每次 simulate 都会生成**新的** Alpha ID（即使是同一个表达式）
- **不要混淆**：
  - `location_id`（模拟任务 ID，临时，模拟完就失效）
  - `alpha_id`（模拟成功后生成的永久 ID）
- 如果是 IQC/比赛场景，比赛页面的 "Team Score" 里也会列出每个团队成员的 alpha ID

### 5.4 三件套

#### 5.4.1 思路模板（200 字以内）

**必讲点**：
- 完整操作步骤：登录 → Alphas → 详情页 → URL/Share 按钮
- Alpha ID 在 3 个位置：URL 末尾 / 详情页顶部 "Alpha ID:" 标签 / Share 弹窗
- 必须先 simulate 成功才有 ID（INIT/FAILED 状态没有）
- 格式：Base62 字符串，12-16 字符，全局唯一

**必避坑**：
- 不要说"在菜单里"（Q8 高频错误：太模糊）
- 不要把 `location_id` 和 `alpha_id` 混为一谈
- 不要忽略"3 个位置"——只讲 URL 是高分答案，但不完整

**推荐结构**：前置条件 → 7 步操作 → 3 个位置 → 格式说明 → 注意事项

#### 5.4.2 AI 提问模板（可直接复制）

```
你是一个 BRAIN 平台顾问备考助手。
我刚收到问卷第 8 题：How do you find the Alpha ID on the BRAIN platform?
请按操作步骤回答：登录 → 进入 Alphas 列表 → 点击 alpha → 找 Alpha ID。
要求：
- 不要用括号加注释
- 不要用"举个例子便于理解"开头
- 不要用"注意："作为开头
- 明确说 Alpha ID 出现在 3 个位置：URL、详情页顶部、Share 弹窗
- 强调必须先 simulate 成功才有 Alpha ID
```

#### 5.4.3 回填与改写区

**粘贴区**（把 IMA / DeepSeek 回答贴这里）：

```
[在这里粘贴 IMA / DeepSeek 原始回答]
```

**AI 改写指令**：
- 按 3 板斧改写：**加我自己**（举 1 个我真实找过 ID 的场景，比如填问卷时找不到 ID 的经历）/ **换比喻**（如"商品条形码——每个商品都有一个唯一编号"）/ **调语序**（先讲"必须先 simulate"再讲操作步骤）
- 长度：5-7 句
- 风格：操作步骤要清晰，**避免 "在菜单里" 模糊表述**

**必删 AI 味词清单**：
- 删：注意 / 举个例子 / 如果你想 / 综上所述 / 由此可见
- 删：括号注释
- 删：八股结构
- 删："在某个地方"等模糊指代

---

## 6. Q9 Genius 计划

### 6.1 全部 7 个等级（按升级顺序）

| 等级 | 名称 | 入门要求（公开来源） | 累计积分门槛（推测/公开） |
|---|---|---|---|
| 1 | **Bronze** | 注册即可 | 0 ~ 1,000 |
| 2 | **Silver** | 提交合格 alpha | 1,000 ~ 5,000 |
| 3 | **Gold** | 持续提交高质量 alpha | 5,000 ~ 10,000 |
| 4 | **Consultant** | 10,000 分 + 通过背调 + 签约 | 10,000+ |
| 5 | **Expert** | 顾问阶段，按季度评选 | 顾问后需 1-2 季度 |
| 6 | **Master** | 顾问阶段，季度奖金 $2,000+ | 顾问后 3-6 季度 |
| 7 | **Grandmaster** | 顾问阶段，季度奖金 $8,000+ | 顾问后 1-2 年 |

> ⚠️ **门槛说明**：Bronze/Silver/Gold 的具体积分门槛未在公开渠道明确披露，上面是基于用户社区分享的常见经验值（仅供参考）。Consultant 阶段的 "10,000 分门槛" 在 BRAIN 官方"顾问计划"介绍页明确提到过。Expert/Master/GM 的门槛由 WorldQuant 内部按季度动态评定。

### 6.2 每个等级的季度奖金范围

| 等级 | 季度奖金范围（USD） | 日津贴（Base Payment） |
|---|---|---|
| Bronze | $0 | 无 |
| Silver | $0 | 无 |
| Gold | $0（仍无顾问身份） | 无 |
| Consultant | **$100 ~ $25,000** | $1 ~ $120/天 |
| Expert | **$500 ~ $2,000**（推测） | $1 ~ $60/天 alphas + $1 ~ $60/天 super alphas |
| Master | **$2,000 ~ $8,000**（官方明确） | 同上 |
| Grandmaster | **$8,000 ~ $25,000+**（官方明确） | 同上 |

**关键来源**：
- BRAIN 官方 consultant-program 页明确：Master 顾问 "potentially earn upwards of **$2,000 or more** in a quarterly payment amount"
- BRAIN 官方 consultant-program 页明确：Grandmaster 顾问 "potentially earn upwards of **$8,000 or more** in a quarterly payment amount"
- 公开社区数据（Reddit、CSDN 用户分享）补充：单日津贴上限 $120/天，季度奖金上限 $25,000
- 中国 Q3 季报数据：Grandmaster 季度奖金 $8,000-$25,000；Master 季度奖金 $2,000-$8,000

### 6.3 顾问阶段与之前阶段的奖金机制差异

**Bronze / Silver / Gold 阶段**：
- **没有现金奖励**——纯积分 + 升级解锁功能
- 解锁的功能包括：更多数据集、更多 region、更长 simulation 周期、可视化、Python API、SuperAlpha 等
- 适合"学习 + 攒作品集 + 等顾问邀请"

**Consultant 阶段**（关键转折点）：
- **Base Payment（日津贴）**：按日发放，$1 ~ $120/天
  - 来源：每提交一个 alpha 都可以累积"质量分"
  - 上限：alphas 部分 $60/天 + super alphas 部分 $60/天 = 总 $120/天
  - 决定因素：提交数量、提交质量、self-growth、Value Factor（越接近 1 越好）
  - 主题加成：当前活跃的 Dataset/Region/SuperAlpha Theme 有倍数加成
- **Quarterly Payment（季度奖金）**：按季度发放，$100 ~ $25,000
  - 前提：上季度超过 20 天有提交
  - 决定因素：Weight（组合权重） × Out-of-Sample 表现
  - Weight 随时间积累（"老顾问比新顾问有更高权重"）
  - OS 表现与 Value Factor 直接相关
- **Competition 奖金**：参加 Super Alpha / ACE / Global Alphathon / Local Alphathon / IQC 等比赛，奖金另计
- **Referral 奖金**：$200 / 成功推荐一位新顾问（被推荐人需完成 10 天提交 + 保持顾问身份 1 个月+）

**Expert / Master / Grandmaster 阶段**：
- **奖金机制相同**（Base + Quarterly + Competition + Referral）
- **区别在于**：
  - **季度奖金的"下限"被拉高**（Master ≥ $2,000，GM ≥ $8,000）
  - **能使用的"超级 alpha 池"更大**（更多高级数据集、专属比赛）
  - **能接触到的资源更专**（如参与 WorldQuant 内部研究讨论）
  - **GM 偶尔会收到全职 offer**——这是 BRAIN 平台转化为正式 quant 员工的主要通道

**总结成一句话**：
- 顾问之前 = 学习 + 攒积分
- 顾问 = 真正"按提交赚钱"（日津贴 + 季度奖金 + 比赛 + 推荐）
- 顾问高等级 = 季度奖金下限被锁高、容量更大、有机会转正

### 6.4 三件套

#### 6.4.1 思路模板（200 字以内）

**必讲点**：
- 列全 7 个等级（Bronze → Silver → Gold → Consultant → Expert → Master → Grandmaster）
- 给每个等级的季度奖金范围（**官方明确** Master $2,000+ / GM $8,000+）
- 重点解释**顾问阶段 vs 之前**的差异：4 种收入（Base 日津贴 + Quarterly 季度奖金 + Competition 比赛 + Referral 推荐）
- 强调 Bronze/Silver/Gold 没有现金奖励

**必避坑**：
- 不要只列 7 个等级名称而不展开（**典型错误**）
- 不要把 Master/GM 奖金范围答成"$X,000 / 月"——是**季度**奖金
- 不要把"积分门槛"和"季度奖金"混为一谈
- 不要给出编造的"每月/每年"具体数字

**推荐结构**：7 个等级 + 奖金表 → 顾问前 vs 顾问后差异 → 4 种收入解释 → 一句话总结

#### 6.4.2 AI 提问模板（可直接复制）

```
你是一个 BRAIN 平台顾问备考助手。
我刚收到问卷第 9 题：Please describe the Genius Program and its tier system.
请按 7 个等级（Bronze / Silver / Gold / Consultant / Expert / Master / Grandmaster）展开，重点说明：
- 顾问阶段（Consultant 及以上）有 4 种收入：Base 日津贴 + Quarterly 季度奖金 + Competition 比赛 + Referral 推荐
- Bronze/Silver/Gold 没有现金奖励
- 官方明确：Master 季度奖金 $2,000+，Grandmaster 季度奖金 $8,000+
要求：
- 不要用括号加注释
- 不要用"举个例子便于理解"开头
- 不要用"注意："作为开头
- 不要给"每月/每年"的具体数字
```

#### 6.4.3 回填与改写区

**粘贴区**（把 IMA / DeepSeek 回答贴这里）：

```
[在这里粘贴 IMA / DeepSeek 原始回答]
```

**AI 改写指令**：
- 按 3 板斧改写：**加我自己**（举 1 个我真实的目标，比如"我打算先冲到 Silver 解锁更多 region"）/ **换比喻**（如"游戏段位——青铜到王者"）/ **调语序**（先讲"顾问前没现金"再讲"顾问后才赚钱"）
- 长度：6-8 句（信息量大）
- 风格：清晰列出等级 + 奖金范围

**必删 AI 味词清单**：
- 删：注意 / 举个例子 / 如果你想 / 综上所述 / 由此可见
- 删：括号注释
- 删：八股结构
- 删：编造的"年化收益"数字
- 删：把"季度"和"月/年"混用的表述

---

## 7. 总结：9 题知识图谱

> 6 道主答题（Q4-Q9）的概念之间存在**强依赖关系**。本节用图谱方式梳理它们之间的逻辑链。

### 7.1 知识图谱（ASCII 版）

```
                 ┌─────────────────────────────────┐
                 │   Q4 Matrix vs Vector Data      │
                 │   (数据是什么形状？)              │
                 └────────────┬────────────────────┘
                              │
                              │ 平台大多数算子只吃 Matrix
                              │ Vector 必须用 vec_* 聚合
                              ↓
                 ┌─────────────────────────────────┐
                 │   Q5 Long/Short Count           │
                 │   (alpha 输出的多空对称性)         │
                 └────────────┬────────────────────┘
                              │
                              │ Pos Ratio ≈ 0.5 = 完美对称
                              │ 实际跑出来可能 7:3 偏正
                              ↓
                 ┌─────────────────────────────────┐
                 │   Q6 Neutralization              │
                 │   (消除市场/行业 β)                │
                 │   ⚠️ 默认 = 组内减均值            │
                 │   z-score 是可选进阶              │
                 └────────────┬────────────────────┘
                              │
                              │ 中性化是"基础"操作
                              │ 实际 alpha 会组合其他算子
                              ↓
                 ┌─────────────────────────────────┐
                 │   Q7 Alpha Example               │
                 │   (把上面的概念组合成表达式)        │
                 │   rank() + vec_* + neutral + ts_*│
                 └────────────┬────────────────────┘
                              │
                              │ 写完 alpha 提交 simulate
                              │ 成功后才有 Alpha ID
                              ↓
                 ┌─────────────────────────────────┐
                 │   Q8 Alpha ID 获取                │
                 │   (URL / 详情页 / Share 弹窗)     │
                 └────────────┬────────────────────┘
                              │
                              │ 提交足够多高质量 alpha
                              │ 累计积分升级 Genius 等级
                              ↓
                 ┌─────────────────────────────────┐
                 │   Q9 Genius 计划                 │
                 │   (Bronze → ... → Grandmaster)   │
                 │   顾问后才有 Base/Quarterly 收入  │
                 └─────────────────────────────────┘
```

### 7.2 5 个核心概念之间的递进

| 顺序 | 概念 | 前置依赖 | 在 alpha 中的角色 |
|---|---|---|---|
| 1 | **Matrix vs Vector** | 无 | 数据形状：决定你能用什么算子 |
| 2 | **Long/Short Count** | Matrix vs Vector | 衡量 alpha 输出的多空对称性 |
| 3 | **Neutralization** | Matrix vs Vector | 消除 β，让 long/short 平衡 |
| 4 | **Alpha Expression** | 上面 3 个 | 算子的组合 = 完整 alpha |
| 5 | **Genius 计划** | Alpha Expression | 长期提交 → 升级 → 赚钱 |

**核心递进逻辑**：
- 没有"数据形状"概念 → 写不出正确 alpha
- 没有"多空对称"概念 → 不知道 alpha 哪里有偏
- 没有"中性化"概念 → 不知道如何消除行业偏向
- 上面 3 个都会了 → 才能写出合格 alpha
- 持续提交 → 累计积分 → 升级 Genius → 变现

### 7.3 Q4-Q6 的关键陷阱（必看）

| 题目 | 陷阱 | 正确理解 |
|---|---|---|
| Q4 | "中性化里的'向量'是 Vector Data 吗？" | ❌ 这里的"向量"是**数学向量**（一列数），不是 Vector Data |
| Q5 | "Long Count = 持仓数？" | ❌ Long Count = **alpha 信号为正的股票数**，不是持仓数 |
| Q6 | "中性化 = z-score 标准化？" | ❌ 中性化 = **组内减均值**；z-score 是可选的进一步标准化 |

---

## 附录 A：引用与参考

主要资料来源（均为公开渠道）：

1. **BRAIN 平台官方公开页**：
   - `platform.worldquantbrain.com/learn/documentation`（需登录）—— 算子、字段、neutralization 权威定义
   - `platform.worldquantbrain.com/consultant-program`（公开）—— 顾问计划、奖金门槛、Genius 等级
2. **WorldQuant 官方介绍页**：
   - `worldquantbrain.com`
   - `worldquant.com/brain`
   - `worldquant.com/ideas/?topic=brain`（Consultant Spotlight 系列）
3. **CSDN 公开博客**：
   - @scdifsn "世坤量化兼职体验"（2.8w 阅读）
   - @Yan_ks "WQ 平台术语理解"
   - @lydeee "WorldQuant BRAIN Alpha 全解"
   - @zurie "Option Alphas Chapter 3: About Neutralization"
   - @lincyang "矩阵扫盲"（1.7k 阅读）
4. **Velog 韩语 BRAIN 教程**（Neutralization 图解）
5. **掘金公开文章**：
   - 世坤 worldquant 线上兼职经历分享（1.8w 阅读）
   - 图解 AI 线性代数与矩阵论
6. **Reddit / r/quant & Wilmott 论坛**：
   - forum.wilmott.com/viewtopic.php?t=70877
   - climbtheladder.com/worldquant-interview-questions/
7. **公开 GitHub 项目**：
   - xiegengcai/world-quant-brain（BRAIN API 客户端）
   - jglazar 量化笔记（IQC 复盘）
8. **公开 Python 包**：
   - autobrain-sim（pypi.org/project/autobrain-sim）
9. **公开研究报告**：
   - Kakushadze, "101 Formulaic Alphas" (2016)
10. **公开竞赛博客**：
    - jglazar.github.io/projects/wq_project（IQC 参赛者复盘）
11. **行业媒体**：
    - efinancialcareers.com "The $140k side hustle that helps get a hedge fund job"
12. **Credly 公开徽章页**：
    - WorldQuant Genius Badge 历年数据
13. **韩国 BRAIN 社区**：
    - brain-kr.com（公开季度数据复盘）
14. **第三方分析平台**：
    - aiquantclaw.com/academy/insights/worldquant-brain-needs-datafield-neutralization-and-universe-routing
    - jishuzhan.net（矩阵扫盲）
15. **IMA 知识库公开外壳**：
    - ima.qq.com 的"WQ 知识库（龙桑版）"（4,328 人 / 3,343 内容）
    - 公开标签：datasets 17 / community_topics 8 / official_articles 6
16. **民间教程**：
    - 老强说教程 alphadoc.biglongxia.com/guide（11 章中文教程）

---

## 附录 B：免责声明

> ⚠️ **使用本文件前必读**

1. **本文件不提供"标准答案"**：
   - 本文件只整理"原理 + 案例 + 数学推导 + 每道题的工作流三件套"
   - **不**包含可直接照抄到 BRAIN 顾问问卷的"标准答案"
   - BRAIN 平台有 4 类反作弊机制：文字相似度 + 语义相似度 + 答题时长 + IP/设备指纹
   - 复制粘贴他人答案 = 雷同卷 = 账号风险

2. **本文件不保证"积分/奖金数字"的实时性**：
   - Genius 计划等级门槛、季度奖金范围等数据来自公开渠道（2025-2026 年度）
   - 平台可能在不通知的情况下调整门槛、奖金、上限
   - 实际以你登录平台后看到的为准

3. **本文件的"中性化"定义以 03 / 04 为准**：
   - **BRAIN 默认中性化 = 组内减均值**（`α - group_mean`）
   - z-score 标准化是**可选**的进一步处理，**不**是中性化本身
   - 旧版 §C.2 写"BRAIN 用的就是 z-score 标准化"——**已被本次重构纠正**
   - 若你读到旧版本，**以本版为准**

4. **本文件的"必讲点/必避坑"仅供参考**：
   - 这些是基于公开资料 + 社区经验的整理
   - BRAIN 官方未明确披露问卷评分细则
   - 建议结合 04 社区经验 + 05 乌龙教程答题方法论一起使用

5. **本文件"加我自己/换比喻/调语序"三板斧的来源**：
   - 改写方法论见 05 §1-§4 和 04 §5
   - 改写目标是"让你的答案带上'人类痕迹'"，而不是"让 AI 写得更好"
   - **不要在改写后还在用 AI 味红线词**（注意 / 举个例子 / 如果你想 / 综上所述 等）

6. **本文件不构成投资建议**：
   - 所有 alpha 示例、金融逻辑仅用于说明概念
   - 实际投资决策请以专业顾问意见为准
   - BRAIN 平台 alpha 回测结果**不**等同于实盘收益

7. **反馈与更新**：
   - 每次你用这套工作流跑完一道题，可以告诉我"Q4 改完了，请帮我扫 AI 味"等
   - 我会帮你做最终检查 + 细化思路
   - 本文件持续迭代：基于 00-工作流总览.md 的统一规范

---

> **最后一句**：你的理解 + 你的表达 = 最佳答案。抄答案 = 雷同卷 = 账号风险。AI 是**翻译机**和**参考书**，不是**答题器**。
