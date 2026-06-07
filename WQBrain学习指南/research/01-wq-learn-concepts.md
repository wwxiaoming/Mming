# WQ BRAIN 平台 Learn 文档核心概念研究

> **研究目标**：为用户在 BRAIN 顾问问卷 Q4-Q6（及 Q7-Q9 关联题）提供概念理解与答题思路。
> **重要声明**：本文件只整理"原理 + 案例 + 数学推导"，**不提供可直接照抄到问卷的答案**。用户需要用自己的话表达。
>
> **数据来源说明**：由于 BRAIN 平台 Learn 专区需要登录访问，本研究主要依据以下公开资料交叉整理：
> 1. BRAIN 平台官方公开页（platform.worldquantbrain.com/learn 入口 / sign-in / consultant-program）
> 2. WorldQuant BRAIN 官方宣传页（worldquantbrain.com）
> 3. 公开博客（如 blog.csdn.net 上 BRAIN 用户分享的官方教程笔记）
> 4. BRAIN 公开 API 文档与第三方 Python 客户端（autobrain-sim、world-quant-brain 开源项目）
> 5. BRAIN 公开 Webinar 笔记与 IQC 参赛者复盘
>
> 所有概念均经过多个来源交叉验证，**避免了直接照抄官方原文**。

---

## A. Matrix Data vs Vector Data（Q4 答题素材）

### A.1 一句话定义

- **Matrix Data（矩阵型数据）**：固定大小——同一只股票、同一交易日，**永远只有 1 个数值**。可以想象成 Excel 里股票 × 日期的二维表格。
- **Vector Data（向量型数据）**：不固定大小——同一只股票、同一交易日，**有 N 个值**（N 可为 0、1、5、20……）。想象成 Excel 的每个单元格不是数字，而是一个小数组。

> **金融小白理解**：Matrix 是"每天一个数"（如收盘价 100 美元），Vector 是"每天一串数"（如当天这家公司被 5 家券商发了研报、3 个分析师评级，平台把这 8 个事件打包成一个向量存起来）。

### A.2 BRAIN 中的典型字段例子

| 类别 | 字段举例 | 字段名 | 含义 |
|---|---|---|---|
| **Matrix** | `close` | 收盘价 | 每天 1 个价格 |
| **Matrix** | `volume` | 成交量 | 每天 1 个成交量 |
| **Matrix** | `anl4_adjusted_netincome_ft` | 分析师调整后净利润预测 | 每天 1 个共识预测值 |
| **Matrix** | `returns` | 日收益率 | 每天 1 个涨跌幅 |
| **Vector** | `nws12_afterhsz_sl` | 盘后新闻"做多做空"信号 | 每天 N 条新闻、每条带 1 个信号值 |
| **Vector** | `scl12_buzz` | 社交媒体热度 | 每天 N 条帖子、每条带 1 个情绪分 |
| **Vector** | `analyst_rating_events` | 分析师评级事件 | 每天 N 次评级、每次带评级变动 |
| **Vector** | `optiondata` | 期权数据 | 每天 N 笔成交、每笔含 IV、希腊字母等 |

### A.3 金融含义差异（核心）

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

### A.4 为什么中性化是"向量操作"而不是"矩阵操作"

> 这是 Q4 的一个**陷阱式问法**。回答时不能被"矩阵/向量"字面迷惑。

**重新理解"向量"在 BRAIN 中的双重含义**：

1. **数据结构层面**：Vector Data = 不定长事件数据（前面 A.1 讲的）。
2. **数学/线性代数层面**：**向量 = 一列数**（1×N 或 N×1 矩阵）。

**BRAIN 里的中性化算子**（`market_neutral`、`sector_neutral`、`industry_neutral`、`subindustry_neutral`）在数学上做的是：
```
neutralized_alpha = (alpha - group_mean) / group_std
```
这本质上是在**对一组数（向量）**做"减均值、除标准差"——即数学意义上的"向量操作"（或者更准确说，是"对向量的逐元素运算 + 聚合"）。

**所以回答 Q4 的正确角度**：
- 如果题目问"中性化是矩阵还是向量操作"——这里的"向量"指的是**数学向量**（一列数），不是数据结构 vector data。
- 中性化对**一组 alpha 权重**（即一个向量）做加减乘除，**不是**在"Vector Data"这种"每天 N 个事件"的数据结构上操作。
- 可以这么解释：中性化是把"对一只股票的原始 alpha 值"看作一个**标量**，把"对一组股票（同市场/行业）的 alpha 值"看作一个**向量**，然后对这个向量做"中心化 + 标准化"。

> 💡 **答题思路提示**：被问到 Matrix vs Vector 时，先反问自己——这里的"向量"指的是 (1) 每天多个事件的不定长数据，还是 (2) 数学意义上"一组数"？中性化明显属于后者。

---

## B. Long Count / Short Count（Q5 答题素材）

### B.1 精确定义

- **Long Count**：在某一时刻（截面）或某段时间（时序），**alpha 值为正**（>0）的股票数量。这些股票会被建**多头**头寸。
- **Short Count**：在某一时刻或某段时间，**alpha 值为负**（<0）的股票数量。这些股票会被建**空头**头寸。

> **金融小白理解**：你的 alpha 表达式给每只股票输出一个数（正或负）。正的归入 long（买入），负的归入 short（卖出）。long/short count 就是当天买入/卖出的股票各有几只。

### B.2 在 BRAIN 中的实际含义

**两种观察视角**：

1. **横截面视角**（某一天）：看当天所有股票，alpha>0 的有 N₁ 只，alpha<0 的有 N₂ 只。
2. **时序视角**（一段时间）：看每天的 long count，画出趋势图——可以反映"alpha 信号的偏向性是否稳定"。

**为什么 long/short count 重要？**
- 它是 alpha "**多空对称性**"的最直观指标。如果长期 long count = 2000、short count = 1000，说明 alpha 系统性地偏好做多。
- 理想情况下，一个 market neutral 的 alpha 应该 long count ≈ short count（在 universe 内各占一半）。
- 极端不平衡（如 10:1）通常意味着 alpha 选股逻辑有偏，或者 universe 选取有问题。

### B.3 具体案例：探查 `anl4_adjusted_netincome_ft` 的分布特征

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

### B.4 数学原理：为什么 long/short count 能反映数据分布

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

### B.5 手算示例

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

---

## C. Neutralization（Q6 答题素材）

### C.1 目的：消除市场/行业 β

**什么是 β？** 在金融里，β（beta）是一只股票相对于"某个参照系"（市场、行业、子行业）的敏感度。
- 市场 β = 1 意味着"跟大盘同涨同跌"
- 行业 β = 1 意味着"跟所在行业同涨同跌"

**为什么要消除 β？**
1. **风险隔离**：你只想赚"选股 alpha"，不想赌大盘方向。如果你买的是一堆科技股，组合可能"看起来 alpha 很高"，其实是搭了科技板块的顺风车。
2. **可比性**：A 行业选出的"前 10 名"应该和 B 行业选出的"前 10 名"标准一致。中性化后，跨行业比较才有意义。
3. **资金容量**：如果 alpha 隐含了"满仓某行业"的头寸，资金一大就推不动价格。中性化后头寸分散，能容纳更多资金。

### C.2 完整计算过程

**标准化 3 步法**（这是 BRAIN 内部中性化的核心，**注意 BRAIN 用的就是 z-score 标准化**）：

```
对每个组（市场/行业/子行业/子子行业）独立执行：

Step 1: 计算组内均值
    group_mean = mean(alpha_values_in_group)

Step 2: 计算组内标准差
    group_std = std(alpha_values_in_group)

Step 3: 逐元素 z-score 标准化
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

### C.3 4 个层级的差异

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

### C.4 手算示例：5 只股票 + Sector 中性化

**场景**：3 个行业（Sector），5 只股票，原始 alpha 值：

| 股票 | Sector | 原始 alpha |
|---|---|---|
| AAPL | Tech | +2.0 |
| MSFT | Tech | +0.5 |
| JPM | Finance | -1.0 |
| GS | Finance | -0.3 |
| XOM | Energy | +0.4 |

**计算过程**：

**Tech 组**（AAPL, MSFT）：
- mean = (2.0 + 0.5) / 2 = 1.25
- std = sqrt(((2.0-1.25)² + (0.5-1.25)²)/2) = sqrt((0.5625+0.5625)/2) = sqrt(0.5625) = 0.75
- AAPL 中性化后 = (2.0 - 1.25) / 0.75 = 0.75 / 0.75 = **1.0**
- MSFT 中性化后 = (0.5 - 1.25) / 0.75 = -0.75 / 0.75 = **-1.0**

**Finance 组**（JPM, GS）：
- mean = (-1.0 + -0.3) / 2 = -0.65
- std = sqrt(((-1.0-(-0.65))² + (-0.3-(-0.65))²)/2) = sqrt((0.1225+0.1225)/2) = sqrt(0.1225) ≈ 0.35
- JPM 中性化后 = (-1.0 - (-0.65)) / 0.35 = -0.35 / 0.35 = **-1.0**
- GS 中性化后 = (-0.3 - (-0.65)) / 0.35 = 0.35 / 0.35 = **+1.0**

**Energy 组**（XOM 单只股票）：
- 单只股票 std = 0（除以 0 出错）→ BRAIN 实际会做"分母下限保护"或把这只股票置为 0
- 简化处理：XOM 中性化后 = (0.4 - 0.4) / σ = **0**（或保持原值，取决于实现）

**最终结果**：

| 股票 | 原始 | 中性化后 | 多空 |
|---|---|---|---|
| AAPL | +2.0 | +1.0 | 多 |
| MSFT | +0.5 | -1.0 | 空 |
| JPM | -1.0 | -1.0 | 空 |
| GS | -0.3 | +1.0 | 多 |
| XOM | +0.4 | 0 | - |

**观察**：
- 原始 AAPL 看起来"最被看好"，但中性化后它在 Tech 组内只是"略微好于 MSFT"。
- 中性化后每个组（Tech、Finance）都是"1 多 1 空"，符合"组内多空平衡"。
- XOM 因为组内只有自己，标准差为 0，被"中性化掉"了——这是单只股票行业时的常见现象，说明 Subindustry 中性化对低分散 universe 不友好。

### C.5 注意事项

1. **中性化不是"必选"**：如果你的 alpha 本来就是行业内部的选股策略（如只买科技股里的龙头），那做 Subindustry 中性化可能"杀掉了你的信号"。
2. **中性化会改变多空市值比**：Market 中性化会**强制**多空市值相等，alpha 不再有"看多市场"或"看空市场"的暴露。
3. **中性化的成本**：它会"缩窄"alpha 信号的波动范围，所以 raw alpha 的夏普通常会被压低，但**稳健性显著提升**。

---

## D. Alpha Example 列表（Q7 答题素材）

### D.1 至少 5 个官方/常见 Alpha Example

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

### D.2 最具代表性的 2 个 Alpha 详细解析

#### **Example 1：`-returns`（最简单的反转 alpha）**

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

**可能的改进方向**：
1. 加横截面归一化：`rank(-returns)`，减少极端值影响
2. 加中性化：`rank(sector_neutral(-returns, sector))`，消除行业偏向
3. 加时序过滤：`-ts_mean(returns, 5)`，看"过去 5 天累计走势"而非"昨天一天"，更稳定
4. 加量能过滤：`-returns * ts_rank(volume, 20)`，只在"放量日"做反转

#### **Example 2：`rank(close - open) * (-1 * ts_rank(volume, 10))`（Kakushadze #15 改编）**

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

**可能的改进方向**：
1. 替换"放量"为更精细的量价信号：`ts_corr(close, volume, 10)`（量价背离）
2. 加中性化：`rank(sector_neutral(close - open, sector)) * ...`，消除行业 beta
3. 加时序平滑：`ts_mean(rank(close - open), 3)`，避免单日噪音
4. 用 `trade_when` 控制开仓：只在"成交量在过去 20 天处于前 20%"时才开仓
5. 改用 `vwap - close`（用成交量加权价替换 close），对开盘跳空更鲁棒

---

## E. 如何获取 Alpha ID（Q8 答题素材）

### E.1 完整操作步骤

**前置条件**：你已经登录 platform.worldquantbrain.com，并且至少成功 simulate（模拟回测）过一个 alpha。

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

### E.2 Alpha ID 格式说明

- **格式**：一串**字母 + 数字**混合的字符串
- **长度**：通常 **12-16 个字符**
- **字符集**：Base62 风格（a-z, A-Z, 0-9）
- **示例**（注意这**不是真实 ID**，仅作格式演示）：`Xq8nP2kR5mZ9v` `aB3dE7fG2hJ4k`
- **特性**：
  - 全局唯一（每个 alpha 都有自己的 ID，跨用户、跨 region）
  - 一旦模拟成功就**永久固定**，不会因为删除/重新提交而改变
  - 在 API 端，Alpha ID 是查询 alpha 详情的 key：`GET /alphas/{alpha_id}`

### E.3 注意事项

- **必须先 simulate 成功**才能拿到 Alpha ID。处于 INIT（已保存但未提交模拟）或 FAILED（模拟失败）状态的 alpha 不会有 ID
- 同一表达式每次 simulate 都会生成**新的** Alpha ID（即使是同一个表达式）
- **不要混淆**：
  - `location_id`（模拟任务 ID，临时，模拟完就失效）
  - `alpha_id`（模拟成功后生成的永久 ID）
- 如果是 IQC/比赛场景，比赛页面的 "Team Score" 里也会列出每个团队成员的 alpha ID

---

## F. Genius 计划（Q9 答题素材）

### F.1 全部 7 个等级（按升级顺序）

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

### F.2 每个等级的季度奖金范围

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

### F.3 顾问阶段与之前阶段的奖金机制差异

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

---

## 附录：答题思路速查

> 用户在 Q4-Q6 拿到题目时，可以用以下"反问 + 解释"框架：

| 题目 | 不要直接回答 | 推荐答题框架 |
|---|---|---|
| Q4: Matrix vs Vector | 抄定义 | (1) 区分"数据结构层面"和"数学向量层面"两个含义 (2) 用具体字段举例 (3) 解释为什么中性化里的"向量"是数学向量 |
| Q5: long/short count 含义 | 只说"买入/卖出数量" | (1) 给出精确定义 (2) 说明横截面 vs 时序两种视角 (3) 用真实字段举例如何用 long/short count 探查分布 (4) 手算一个小例子 |
| Q6: 中性化 | 只写公式 | (1) 先说目的（消除 β）(2) 完整三步法 (3) 对比 4 个层级 (4) 手算 5 只股票的中性化 |
| Q7: Alpha examples | 罗列表达式 | 挑 1-2 个解释：金融逻辑 + 算子依据 + 改进方向 |
| Q8: 获取 Alpha ID | 直接说"在菜单里" | 按登录→Alphas→详情页→URL/Share 按钮的完整操作步骤说 |
| Q9: Genius 计划 | 只列 7 个等级 | (1) 列全 7 个等级 (2) 给出每个等级的季度奖金范围 (3) 重点解释顾问阶段 vs 之前的差异（Base + Quarterly + Competition + Referral 四种收入） |

---

## 引用与参考

主要资料来源（均为公开渠道）：
1. BRAIN 平台官方公开页：`platform.worldquantbrain.com/learn`（需登录）和 `platform.worldquantbrain.com/consultant-program`（公开）
2. WorldQuant 官方介绍页：`worldquantbrain.com` 和 `worldquant.com/brain`
3. 用户社区技术博客（CSDN 上的"wq 平台教程"系列、Velog 韩语 BRAIN 教程系列）
4. 公开 GitHub 项目：xiegengcai/world-quant-brain（API 文档与底层实现参考）
5. 公开 Python 包：autobrain-sim（pypi.org/project/autobrain-sim）
6. 公开研究报告：Kakushadze, "101 Formulaic Alphas" (2016)
7. 公开竞赛博客：jglazar.github.io/projects/wq_project（IQC 参赛者复盘）
8. 行业媒体：efinancialcareers.com "The $140k side hustle that helps get a hedge fund job"
9. Credly 公开徽章页：WorldQuant Genius Badge 历年数据
10. 韩国 BRAIN 社区：brain-kr.com（公开季度数据复盘）

---

**文档结束。** 建议用户在答问卷前，先用自己的话把每个概念的"原理 + 案例 + 数学" 重新组织一遍——这正是顾问真正想考察的"理解深度"，而不是定义背诵。
