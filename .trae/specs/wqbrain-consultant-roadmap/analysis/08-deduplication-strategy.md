# 降低 Alpha 重复率（Uniqueness）实操指南

> **面向读者**：正在用"老强说"等模板工具刷分、担心撞库的金融小白
> **核心目标**：让你的 alpha 在 BRAIN 平台上"与众不同"，顺利通过 Self-Correlation、Production Correlation、Peer Production 三道闸口
> **贯穿示例**：本文所有改造示例都以 `analyst4`（anl4，分析师一致预期数据）为起点，便于你对照练习

---

## 0. 写在前面：为什么这份指南对你至关重要

你可能刚刚用老强说工具冲到 10,000 分（Gold 等级），正准备开始顾问期——或者已经在顾问期但每天都在"撞库"的恐惧中提交 alpha。**撞库不是小问题**，它直接决定你的日均收入：

- 老强说工具的模板使用同一份代码框架（"6 天冲到 1 万分"方案是**完全公开**的）
- 全平台 25 万+用户中，至少有几万人在用类似工具
- 公开数据集 + 公开算子的"差异化空间"远比你想象的小
- 顾问期日均 1-5 美元 vs 20+ 美元的天壤之别，**核心就在于撞库率**

好消息是：**撞库是完全可解的**。本指南会从"为什么撞"到"怎么改"再到"怎么避坑"逐层展开，每一条技巧都配 anl4（analyst4 分析师数据）的改造示例，便于你直接套用。

---

## 1. 什么是"重复 alpha"

### 1.1 BRAIN 平台的三道重复检测闸口

WorldQuant BRAIN 平台通过 **三道闸口** 同时把关，确保你提交的 alpha 不是"老汤底"：

| 闸口 | 检测内容 | 通俗解释 |
|---|---|---|
| **Self-Correlation（自相关）** | 你新 alpha 与本人账户下**所有历史 alpha** 的皮尔逊相关系数 | "和自己以前交的像不像" |
| **Production Correlation（生产相关性）** | 与平台"已收录到生产组合"中的 alpha 相比 | "和平台金库里的策略撞没撞" |
| **Peer Production Threshold** | 与**全平台所有顾问**已提交 alpha 的相似度（开源工具源码反推） | "和全网所有用户撞没撞" |

此外平台还有 **表达式哈希比对**（识别 `rank(a/b)` 和 `rank(1/(b/a))` 这种等价变换）和 **PCA 投影分析**（判断你是不是已有因子的线性组合）作为暗线防护。

### 1.2 4 年滚动窗口

相关性不是用"全部历史数据"算的，而是用 **过去 4 年（约 1008 个交易日）** 的日 PnL 序列滚动计算。这意味着：

- 你 2 年前交的 alpha 仍然会影响今天的判重
- 临时换一个窗口（比如 `ts_rank(close, 10)` 改成 `ts_rank(close, 11)`）基本没用——皮尔逊相关系数对微小的窗口变化不敏感

### 1.3 默认阈值 0.6–0.7 意味着什么

- 0.6 是第三方工具（如老强说）的保守线
- 0.7 是平台硬门槛
- 越接近 1 越像，越接近 0 越不同
- **例外豁免**：若新 alpha 的 Sharpe 比历史相似 alpha **高出 10%**（即 > 1.375），可忽略 Self-Correlation 限制

### 1.4 对顾问评分的具体影响

被判定为"重复"意味着：
- **直接后果**：alpha 不能提交（绿色标记缺失），白浪费 1 个名额
- **间接后果**：长期提交低差异化 alpha 会拉低 **Value Factor（VF）** 评分；VF 0.95 与 0.5 的收入差距可达 5-10 倍
- **季度奖金影响**：重复率高的顾问，OS（样本外）权重累计慢，季度奖金分档低

### 1.5 一个真实的"撞库"案例

社区里 CSDN 博主 scdifsn 在他的《世坤量化兼职体验》一文中明确写到："成为顾问后的最直观感受就是，平台对于可提交 alpha 的测试要求大大提高了，而且不允许与他人提交的 alpha 相关性过高"——这句话翻译成大白话就是：**第一阶段允许"借鉴"别人的思路，但顾问阶段这种做法会被直接判重**。这正是为什么许多"用工具冲到 10,000 分"的顾问在第二阶段突然发现"再也交不出去了"的根本原因。

---

## 2. 为什么工具用户最容易撞库

### 2.1 模板代码框架是公开的

老强说教程第 6.3 节的"6 天冲到 1 万分"方案是**公开发布的**：

```python
# 老强说 Day 1 默认配方（公开）
ts_rank(anl4_eps_mean, 20)
group_neutralize(ts_rank(anl4_eps_mean, 20), subindustry)
```

**所有用工具的用户都在跑这同一组表达式**。社区里掘金用户 qiaoxingxing 直接指出："培训提供了一套完整的寻找 alpha 因子的代码框架，日常任务就是选择数据集，跑代码"——同一份框架，撞车是必然。

### 2.2 换数据集/中性化的"伪差异化"陷阱

最常见的"假改造"是：

- **换数据集**：把 `anl4` 换成 `anl4` 的同义字段（`anl4_eps`、`anl4_revenue`）——皮尔逊相关几乎不变
- **换中性化**：从 `subindustry` 换成 `industry`——表面上不同，但 PnL 序列走势高度相似
- **加 delay**：从 delay=1 改到 delay=0——只是数据时移，相关性照样高

### 2.3 公开数据集 + 公开算子的组合空间有限

BRAIN 公开数据集约 16 个（`pv1`/`pv13`/`fundamental2/6`/`analyst4/7`/`model16/51`/`news12/18`/`socialmedia8/12`/`option8/9`/`sentiment1`），公开算子约 100 个。理论上组合空间很大，但 **新手常被锁死在"价量 + 几个基础算子"的小池子里**——这就是撞库的根因。

---

## 3. 降重的 3 大核心思路

> **核心原则**：**至少在"数据集 + 中性化 + 算子组合"三个维度中改两个**——只改一个维度的"微调"几乎一定撞库。

| 思路 | 改造方向 | 难度 | 撞库率下降 |
|---|---|---|---|
| **A. 换数据集** | 从 `anl4` 换到 `news18`、`option8`、`socialmedia8` 等冷门数据集 | ⭐⭐ | 高 |
| **B. 换中性化层级** | 从 `subindustry` 换到 `industry` / `sector` / `market` | ⭐ | 中 |
| **C. 换算子组合** | 用不常见的 `ts_decay_exp` / `trade_when` / `quantile` | ⭐⭐⭐ | 高 |

**最推荐组合**：A + C（换数据集 + 换算子）。这是社区公认最有效的差异化路径。

---

## 4. 10 条可立即执行的降重技巧

> 以下每条技巧给出 **原理 + 改造前/后表达式 + 预期效果**。所有示例以 anl4 起点。

### 技巧 1：把"水平值"换成"变化量"

**原理**：用 anl4 的盈利预测**绝对值**是最常见的用法；改用 **盈利预测的修订变化**（revisions）则非常冷门，相关性自然降低。

```python
# 改造前（撞库高发区）
ts_rank(anl4_eps_mean, 20)

# 改造后（修订变化）
ts_rank(anl4_eps_mean / ts_delay(anl4_eps_mean, 60) - 1, 20)
```

**预期效果**：与模板 alpha 的相关性通常从 0.7+ 降到 0.3-0.5。

### 技巧 2：把单一数据集换成多数据集交叉

**原理**：跨数据集 alpha（combo）天然低相关，因为数据源不同。

```python
# 改造前
ts_rank(anl4_eps_mean, 20)

# 改造后：anl4 + pv1 交叉
ts_rank(anl4_eps_mean * close, 20)
```

**预期效果**：与单一 anl4 alpha 的相关性可降到 0.2-0.4。

### 技巧 3：把简单时序窗口换成多窗口组合

**原理**：单窗口算子（`ts_rank(x, 20)`）是模板标配；**多窗口组合**（短+长+衰减）极少见。

```python
# 改造前
ts_rank(anl4_eps_mean, 20)

# 改造后：ts_decay_linear + ts_rank 组合
ts_decay_linear(ts_rank(anl4_eps_mean, 60), 30)
```

**预期效果**：撞库率显著下降，且对近期信号更敏感。

### 技巧 4：用 trade_when 加上"开仓/平仓"条件

**原理**：`trade_when` 是 2nd-order 工厂，**根据条件决定是否开仓/平仓**，是社区公认的"撞库绝缘体"。

```python
# 改造前
ts_rank(anl4_eps_mean, 20)

# 改造后：涨势中持有，跌破均线平仓
trade_when(close > ts_mean(close, 60), ts_rank(anl4_eps_mean, 20), 0)
```

**预期效果**：PnL 序列被条件过滤后与模板高度不同。

### 技巧 5：把截面 rank 换成 quantile 分位数

**原理**：`rank` 是 0-1 线性分布；`quantile` 是离散分箱，**改变 PnL 分布形态**。

```python
# 改造前
-rank(anl4_eps_mean)

# 改造后
-quantile(anl4_eps_mean, 5)
```

**预期效果**：与同字段 `rank` 类 alpha 的相关性可降到 0.3 以下。

### 技巧 6：用 densify 处理的字段做更细的中性化

**原理**：`densify(anl4_field, subindustry)` 把字段按子行业填充，使后续中性化更精确。

```python
# 改造前
group_neutralize(ts_rank(anl4_eps_mean, 20), subindustry)

# 改造后
group_neutralize(ts_rank(densify(anl4_eps_mean, subindustry), 20), subindustry)
```

**预期效果**：与同字段的 group_neutralize alpha 相关性下降 20-30%。

### 技巧 7：尝试用 option8 / option9 这类冷门期权数据

**原理**：option8（期权 Greeks、隐含波动率曲面）使用率 < 5%，撞库概率极低。

```python
# 起点：anl4 + 模板
ts_rank(anl4_eps_mean, 20)

# 改用 option8（隐含波动率）
-rank(opt8_iv_30d)  # 隐含波动率越低，未来收益越好（风险溢价）
```

**预期效果**：与 anl4 用户的相关性 < 0.2（完全不同的数据域）。

### 技巧 8：尝试 news18 / socialmedia8 这类情绪数据的非常规用法

**原理**：情绪数据绝大多数用户都只用 `news12`（新闻计数），`news18`（细粒度情绪）使用率极低。

```python
# 冷门用法 1：情绪的"动量"
ts_rank(news18_sentiment, 5) - ts_rank(news18_sentiment, 60)

# 冷门用法 2：情绪与基本面的"剪刀差"
ts_rank(news18_sentiment, 20) - ts_rank(anl4_eps_mean, 20)
```

**预期效果**：与 anl4 模板 alpha 的相关性 < 0.25。

### 技巧 9：用 ts_decay_exp 替代 ts_decay_linear

**原理**：`ts_decay_linear` 是线性权重（新旧数据等差衰减），`ts_decay_exp` 是指数权重（**近期数据权重远高于远期**），绝大多数工具用户只用前者。

```python
# 改造前
ts_decay_linear(ts_rank(anl4_eps_mean, 60), 20)

# 改造后
ts_decay_exp_window(ts_rank(anl4_eps_mean, 60), 20, 0.95)
```

**预期效果**：与线性衰减类 alpha 的相关性降到 0.4 左右。

### 技巧 10：参考论文改造（必读 5 篇核心论文）

| 论文 | 核心 alpha 模板 | 落地改造 |
|---|---|---|
| **Jegadeesh & Titman (1993) 动量** | `ts_rank(returns, 60) - ts_rank(returns, 250)` | 用 anl4 字段做"盈利预期动量" |
| **Fama-French (2015) 五因子** | `rank(value) + rank(momentum) + rank(size)` | 用 anl4 + fundamental6 多因子合成 |
| **Stambaugh & Yuan (2017) 误定价** | 12 个 anomaly 组合 | 用 anl4 + pv1 实现 mispricing 因子 |
| **Novy-Marx (2013) 毛利因子** | `rank(gross_profit/assets)` | 直接用 fundamental6 的 `gp/a` 字段 |
| **Asness, Frazzini (2013) 质量-动量** | `rank(quality) * rank(momentum)` | anl4 盈利稳定性 × pv1 价格动量 |

**预期效果**：论文派 alpha 的"经济直觉"清晰，OS 表现稳健，长期价值高。

---

## 5. 小样本快速验证法

> **核心目的**：用更短的样本快速预判撞库风险，**节省提交名额和平台资源**。

### 5.1 缩样本到 2-3 年

BRAIN 平台默认 4 年样本，但你可以在 simulation 设置中**选择更短的样本期**（如 2-3 年）。这能：

- 把回测时间从 30-40 秒缩短到 15-20 秒
- 提早发现"撞库风险"（相关性的滚动计算在短样本上更敏感）
- 节省每日提交配额

### 5.2 Self-Correlation 模拟快速判重

```python
# 伪代码：提交前自检
my_alpha_pnl = get_pnl(my_alpha_id)
history_pnl = get_all_my_alpha_pnls()

max_corr = max([pearson(my_alpha_pnl, h) for h in history_pnl])
if max_corr > 0.6:
    print("警告：撞库风险高，需要改造")
elif max_corr > 0.5:
    print("注意：可考虑加一层 operator 进一步降相关")
else:
    print("OK：可提交")
```

### 5.3 节省额度的"先验证后提交"流程

1. **Step 1**：用 2 年缩样本跑出 alpha，记录 IS 指标
2. **Step 2**：用工具代码（`xiegengcai/world-quant-brain` 的 `self_correlation.py`）算 Self-Correlation
3. **Step 3**：若 Self-Corr > 0.5，先改造再跑完整 4 年样本
4. **Step 4**：4 年样本达标后才提交

**好处**：把"撞库"风险消灭在提交前，每日 4 个名额用在刀刃上。

### 5.4 实战中的"试错成本"对比

| 验证方式 | 单次耗时 | 平台配额消耗 | 信息完整度 |
|---|---|---|---|
| **直接 4 年提交** | 30-40 秒 | 1 个名额 | 完整但浪费 |
| **2 年缩样本 + 自检** | 15-20 秒 | 0（不提交） | Self-Corr 仍准确 |
| **仅看工具绿色标记** | 0 秒 | 1 个名额 | 只看 Sharpe/Fitness，不看 Self-Corr |

**强烈推荐第 2 种**：把"撞库"风险消灭在提交前，是社区里活得好的顾问都在用的方法。

---

## 6. 社区常见的"差异化思路"清单

### 6.1 波动率调整动量因子（CSDN Wenku 案例）

```python
# 起点：单一动量
ts_rank(anl4_eps_mean, 20)

# 改造：动量 / 波动率（Sharpe-like）
ts_rank(anl4_eps_mean, 20) / ts_std_dev(anl4_eps_mean, 30)
```

**原理**：把"原始信号"除以"波动率"做标准化，类似夏普比率的思路。

### 6.2 2nd-order 升级（一阶动量 → 二阶动量变化率）

```python
# 一阶动量
ts_rank(anl4_eps_mean, 20)

# 二阶动量（一阶的变化率）
ts_rank(ts_rank(anl4_eps_mean, 20), 5)
```

**原理**：把 alpha 本身当作"新数据"，再套一层时序算子——这是社区公认最有效的升级路径。

### 6.3 读论文改造

qiaoxingxing 在掘金分享的真实经验：她用 AI 读论文后 **1 个月评上 grandmaster**。关键方法论：

- **论文 → 经济直觉 → 数学表达 → 平台 alpha**
- 不要直接抄论文公式，要理解背后的"市场无效性"
- 用 anl4 / fundamental6 / pv1 重新实现论文逻辑

### 6.4 Sharpe +10% 豁免规则

若新 alpha 的 Sharpe > 1.375（D1 模式下），平台**自动豁免 Self-Correlation 检测**。这是新手最容易错过的"快速通道"——把"中等 Sharpe + 高度原创"改成"高 Sharpe + 中度原创"，反而能更快过审。

### 6.5 主题活动（Theme）期间的差异化策略

平台每月/每季会发布 **主题**（如 ESG、红利策略、AI 概念），命中可获 1.5x-2x 收入加成。**主题期间差异化思路**：

- 看 Theme Calendar，提前 1-2 周准备
- 主题数据集的"非常规用法" = 撞库最低
- 主题期内**降低提交频率、提高单 alpha 质量**（因为加成倍率 = 质量 × 数量）

---

## 7. 撞库检测与应对

### 7.1 提交前自检"会不会和别人撞"

| 检查项 | 方法 | 阈值 |
|---|---|---|
| Self-Correlation | 用开源工具 `xiegengcai/world-quant-brain` 的 `self_correlation.py` | < 0.6 |
| Production Correlation | 平台 simulation 结果自动给出 | < 0.7 |
| 表达式哈希 | 自己用 MD5 算表达式哈希，与历史对比 | 哈希不同 ≠ 一定不同，但哈希相同 = 一定相同 |
| 视觉检查 | 你的 alpha 与最近 10 个通过 alpha 的 PnL 曲线是否"长得像" | 主观但有效 |

### 7.2 被判重复后怎么改

**步骤**：
1. 查看平台反馈的"高相关 alpha ID"
2. 拉取那个 alpha 的 PnL 序列
3. 用 `pearson(your_pnl, their_pnl)` 算精确相关
4. 在**三个维度中至少改两个**（数据集/中性化/算子组合）
5. 重新提交

**核心原则**：**小修小补无效，必须做"结构性改造"**。

### 7.3 平台反馈的解读

平台会显示 `Self-Correlation: 0.XX`（账户内）和 `Production Correlation: 0.XX`（与生产组合）：

- < 0.5：优秀，几乎无撞库风险
- 0.5-0.7：可接受，**但不要连续 3 个都在 0.6+**（会被 VF 惩罚）
- > 0.7：硬性拒收

---

## 8. 避坑提醒

### 8.1 看起来差异化，实际不算差异化

| 假差异化 | 为什么没用 |
|---|---|
| 单纯换 `delay`（1→0 或 0→1） | PnL 序列只是时移，相关性变化 < 0.05 |
| 单纯换窗口（20→21） | 皮尔逊对微窗口变化不敏感 |
| 单纯换中性化（subindustry→industry） | 中性化只调整"截面权重"，PnL 走势高度相似 |
| 给 alpha 加微小噪声 | **平台明文禁止**——IQC 协议第 23 条规定"deliberate introduction of noise to subvert our scoring systems"会被直接封号 |
| 改字段名（`anl4_eps_mean` → `anl4_eps`） | 字段不同但 PnL 几乎相同 |

### 8.2 看起来撞车，实际不算撞车

| 情况 | 解释 |
|---|---|
| **不同 Region**（USA / EUR / ASI）的同样表达式 | Region 数据完全不同，平台**分开计算相关性** |
| **不同 Universe**（TOP3000 / TOP1000） | Universe 是子集筛选，PnL 序列会不同 |
| **不同 Delay**（D0 vs D1） | 严格来说 D0 算"日内 alpha"，平台有专门的相关性库 |
| **不同 Dataset**（anl4 vs anl7） | 即使字段语义接近，平台也按 dataset 隔离判重 |

### 8.3 第三方工具内置的"降重"是否真的有效

**答案：多数无效。** 原因：

- 老强说等工具的"降重"本质是**自动换数据集/中性化**——这是 8.1 节的"假差异化"
- 工具没有"理解经济含义"，只是机械替换参数
- 真正有效的降重是**结构性创新**（如 trade_when、二阶动量、跨数据集组合），这需要人工设计

**正确做法**：把工具当作"挖掘加速器"，把差异化设计留给自己。

### 8.4 关于"延迟（Delay）"的常见误解

很多新手以为 D0（Delay=0）比 D1（Delay=1）"更高级"，但事实是：

- D0 的 Sharpe 门槛是 ≥ 2.0（远高于 D1 的 1.25）
- D0 的 Self-Correlation 计算窗口与 D1 不同
- 同一 alpha 表达式的 D0 和 D1 版本**会被平台视为不同 alpha**（这是少有的"免费差异化"路径）
- 但 D0 在顾问期前无法提交，**新手优先做 D1**

### 8.5 关于"中性化"的深层逻辑

很多用户不理解中性化的本质，把它当作"减分项"——其实恰恰相反：

- **正确的做法**：先看 alpha 的 PnL 是否"集中在某行业"。若集中，加 `group_neutralize(industry)`；若集中在某子行业，加 `subindustry`
- **错误做法**：盲目套用 `subindustry`（工具默认）导致与全平台撞库
- **进阶做法**：尝试**多重中性化**（`group_neutralize(group_neutralize(x, industry), market)`），效果类似"先剥行业，再剥市场 beta"

---

## 总结

降低 alpha 重复率的核心方法论：

1. **三维改造**：数据集 + 中性化 + 算子组合，至少改两个维度
2. **善用冷门**：option8 / news18 / socialmedia8 / densify / trade_when 是差异化金矿
3. **论文派路线**：理解经济含义 → 重写为平台 alpha，长期 VF 高
4. **先验证后提交**：用 2 年缩样本 + Self-Corr 模拟自检
5. **避免假动作**：换 delay/窗口/中性化=无效，加噪声=违规

**最后提醒**：**撞库是工具用户的"成人礼"**——只有跨过这一关，才能从"日均 1-5 美元"升到"日均 20 美元以上"的金字塔中部。社区里活得好的顾问，没有一个纯靠工具——他们都是"工具 + 读论文 + 微改 + 提交策略优化"组合拳。

> **字数统计**：约 4,800 字（含表格与代码块）
