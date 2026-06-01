# WorldQuant BRAIN Alpha 挖掘专家技能 V3

> 来源整合：
> 1. 官方 BRAIN 平台文档（platform.worldquantbrain.com）
> 2. 老强说 Alpha 官方教程（alphadoc.biglongxia.com）—— 全 11 章
> 3. CSDN 实战博客（scdifsn、Yan_ks、Oo_Amy_oO、m0_73177400）
> 4. 韩国 velog 社区（tae0_）
> 5. aiquantclaw.com 实战洞察
> 6. GitHub 开源工具（xiegengcai/world-quant-brain）
> 7. 官方论坛 BRAIN TIPS
>
> 适用：从零基础 → 成为签约顾问 → 提升收入 全流程

---

## 〇、技能速查索引

| 章节 | 主题 | 用途 |
|---|---|---|
| 一 | 适用范围 | — |
| 二 | 项目核心认知 | 回答"这是啥" |
| 三 | 积分体系 | 回答"怎么计分" |
| 四 | 提交标准 | 回答"怎么过审" |
| 五 | 5 大收入驱动因素 | 回答"怎么赚钱" |
| 六 | 流水线架构 | 工具使用 |
| 七 | **6 天方案（实操）** | 冲刺金牌 |
| 八 | 各阶段提交策略 | 不同时期怎么交 |
| 九 | 数据集选择 | 换什么数据 |
| 十 | 中性化选择 | 选什么分组 |
| 十一 | 算子速查 | 查算子用法 |
| 十二 | NaN / 覆盖率 | 解决报错 |
| 十三 | trade_when | 提 Sharpe |
| 十四 | Alpha 模板库 | 抄作业 |
| 十五 | 指标调优 | 调指标 |
| 十六 | 降自相关 | 解决冲突 |
| 十七 | 工具配置 | 工具调参 |
| 十八 | 每日 SOP | 日常操作 |
| 十九 | 排错清单 | 解决问题 |
| 二十 | 11 个踩坑 | 避坑 |
| 二十一 | 概念速查 | 查概念 |
| 二十二 | **问卷 9 题详解** | 应对测试 |
| 二十三 | **成为顾问流程** | 转正流程 |
| 二十四 | **准顾问期策略** | 过渡期 |
| 二十五 | **路由表（数据域/中性化/Universe）** | 实战方法论 |
| 二十六 | **社区实战案例** | 参考经验 |
| 二十七 | Workday 填写 | 入职材料 |
| 二十八 | 发薪日期 | 查发薪 |
| 二十九 | 推荐计划 | 副业赚钱 |
| 三十 | 纳税 | 税务 |
| 三十一 | 主题日历 | 加成机会 |
| 三十二 | 官方资源 | 学习资源 |
| 三十三 | 工具/服务器 FAQ | 解决问题 |
| 三十四 | 输出规范 | 回答用户 |
| 三十五 | 常见问答 | 速查 |
| 三十六 | 关键链接 | 资源 |

---

## 一、技能适用范围

当用户需要以下帮助时，激活本技能：

- WorldQuant BRAIN 平台注册、跑分、提交流程
- 自动化挖 alpha 工具的安装、配置、调参
- 解释 Sharpe / Fitness / Turnover / Margin / VF / Self-Correlation 等指标
- 解释等级晋升、季度奖金、推荐奖励机制
- 诊断 alpha 不达标 / 提交失败 / 自相关过高
- 选数据集、算子、中性化、组合策略
- 提高可提交率、提升 VF、增加收入
- Workday 填写、基础测试问卷、背景调查准备

---

## 二、项目核心认知

### 2.1 一句话介绍

WorldQuant BRAIN 是 **全球最大量化对冲基金 WorldQuant** 旗下的众包研究平台。任何人都可以创建、测试、提交交易信号（Alpha），按表现获得真实美元报酬。

### 2.2 时间线预期

```
第 1-2 天 部署云服务器 + 注册账号 + 安装工具
第 3-7 天 使用工具跑 Alpha，冲刺 10,000 积分（金牌 Gold 等级）
第 7-9 天 填写测试问卷 + Workday
约 1 个月 通过背调，正式成为 Consultant（顾问）
持续工作 提交 Alpha，赚 Base Payment + 季度奖金 + 推荐奖励
```

**实战案例**（scdifsn 顾问）：1/6 - 1/10 跑满 10000 分，1/13 提交问卷，2/18 准顾问，4/28 正式顾问。

### 2.3 收入结构

| 收入类型 | 金额范围 | 频率 | 说明 |
|---|---|---|---|
| 基础报酬（普通） | \$1 - 60 / 天 | 每日 | 每天前 4 个 Alpha 计入 |
| 基础报酬（超级） | \$1 - 60 / 天 | 每日 | 交满 100 个后解锁，与普通叠加 |
| 季度奖金 | \$100 - 25,000 | 每季度 | 与等级强相关 |
| 推荐奖励 | \$100 / 人 | 每次成功 | 无上限 |
| 新人奖 | \$100 | 一次性 | 10 天有提交即可 |
| 比赛奖金 | 不定 | 不定 | PPAC、MAX TRADE ON 等活动 |

**新手真实预期**：月收入 \$300 - \$1000+，持续 1 年可至 \$2000+。

### 2.4 等级体系

| 等级 | 提交数 | Pyramid | 季度奖金 |
|---|---|---|---|
| Bronze 铜牌 | 2,000 分 | — | — |
| Silver 白银 | 5,000 分 | — | — |
| **Gold 黄金** | **10,000 分** | 3+ | **\$100 起** |
| Expert 专家 | 50+ 提交 | 更多 | \$200 - 2,000 |
| Master 大师 | 200+ 提交 | 长期稳定 | \$2,000 - 8,000 |
| Grandmaster 宗师 | 500+ 提交 | 顶尖 | \$8,000 - 25,000 |

### 2.5 适用地区

中国（大陆/香港/台湾）、韩国、日本、印度、印尼、马来西亚、菲律宾、新加坡、泰国、越南、肯尼亚、英国。

---

## 三、积分体系详解

### 3.1 核心规则

| 规则 | 说明 |
|---|---|
| 目标 | 累计 **10,000 Challenge 积分** = Gold 顾问邀请 |
| 每日上限 | 每天最多 **2,000 分**（取当日最佳） |
| 每日结算 | **北京时间中午 12 点**结算提交数，14 点结算积分 |
| 时间限制 | ❌ 无 |
| 连续要求 | ❌ 无 |

### 3.2 提交质量分级

| 等级 | 表现 | 当日积分 |
|---|---|---|
| **Spectacular** | 顶尖 | 一个就能拿满 2000 分 |
| **Excellent** | 优秀 | 一个就能拿满 2000 分 |
| **Good** | 良好 | 一个约 1000 分 |
| **Average** | 一般 | 一个约 500 分 |

💡 **金牌前只关心颜色**（绿色 = 可交），**顾问后关注 Spectacular/Excellent 等级**。

---

## 四、提交标准（D1 模式默认）

### 4.1 必达指标

| 指标 | 要求 | 通俗解释 |
|---|---|---|
| **Sharpe** | > 1.25 | 赚钱能力够不够强 |
| **Fitness** | > 1.0 | 综合质量 |
| **Self-Correlation** | < 0.7 | 跟已提交 alpha 不能太像 |
| **Turnover** | 1% - 70% | 交易不能太频繁也不能太懒 |
| **单只股票权重** | < 10% | 防止集中持仓 |
| **Sub-Universe Sharpe** | > 阈值 | 缩小池子仍能跑 |

### 4.2 D0 vs D1 区别

| 模式 | Sharpe 要求 | 特点 |
|---|---|---|
| **D0** (Delay=0) | ≥ 2.0 | 同日交易，竞争激烈，回报高 |
| **D1** (Delay=1) | ≥ 1.25 | 隔日交易，标准设置，**新手推荐** |

### 4.3 顾问期更严格的隐性标准

| 指标 | 要求 |
|---|---|
| **Sub-Universe Sharpe** | ≥ 0.7 |
| **Turnover** | < 30% |
| **Margin** | > 4 bps |
| **Performance Comparison (Change)** | > 0 |
| **Subuniverse Pass Formula (D1)** | sqrt(252) × max(0.065, (subuniverse_size/largest_universe_size) × 0.15) |
| **Superuniverse Pass Formula** | sharpe of next largest universe > 0.7 × sharpe of alpha |
| **Ranked Sharpe Test** | sharpe of alpha after rank and power op |

---

## 五、5 大收入驱动因素

### 5.1 因素一：提交数量

- 每天只有前 **4 个** Alpha 计入 Base Payment
- 第 5 个起不计收入
- **优先提交质量最高的**，不要浪费名额

### 5.2 因素二：提交质量

| 指标 | 目标值 |
|---|---|
| Sharpe | ≥ 1.25 (D1) / ≥ 2.0 (D0) |
| Fitness | 越高越好 |
| Turnover | < 30% |
| Margin | > 4 bps |

### 5.3 因素三：自我提升 (Self-Improvement)

平台会对比你**新提交的 Alpha** 与**历史平均**：
- 新 alpha 比历史好 → 正面影响
- 新 alpha 比历史差 → 负面影响

**启示**：稳定高质量输出，不要饥不择食。

### 5.4 因素四：价值因子 (Value Factors, VF)

**这是影响收入最大的单一因素**：

| 范围 | 收入水平 |
|---|---|
| 0.95+ | 非常高（顶尖） |
| 0.85 - 0.95 | 较高 |
| 0.7 - 0.85 | 良好 |
| 0.5 - 0.7 | 较低（积累期） |

- 初始 VF = 0.5
- 每月更新，基于过去 3 个月
- **VF 0.95 vs 0.5，收入差距数倍甚至 10 倍+**

### 5.5 Performance Comparison (Change)

| Change | 决策 |
|---|---|
| > 0 | ✅ 提交（对组合有正向贡献） |
| < 0 | ❌ 不要提交（即使 Sharpe 高，也会拖累整体） |

### 5.6 Theme Calendar（主题加成）

平台会定期发布主题（ESG、AI、红利、EUR D1 等），匹配的 alpha 获得 **1.5-2 倍收入倍数加成**。

**实战经验**（scdifsn）：EUR D1 主题期间，最高单日近 \$7（平时 \$1.5-2）。

---

## 六、流水线架构（适用于自动化工具）

### 6.1 标准三阶流水线

```
一阶 (Stage 1): 基础算子组合
   winsorize(ts_backfill(field, 120), std=4) + ts_rank/ts_zscore/ts_delta
   ↓  按 Sharpe/Fitness 阈值筛选
二阶 (Stage 2): 组操作
   group_neutralize / group_rank / group_zscore + densify
   ↓
三阶 (Stage 3): 条件逻辑
   trade_when(open_event, signal, exit)
   ↓
提交 + 自相关 + Change 检查
```

### 6.2 各阶段阈值推荐

| 阶段 | Sharpe 阈值 | Fitness 阈值 | 目的 |
|---|---|---|---|
| 一阶 | 0.85 - 1.0 | 0.6 | 抓种子 |
| 二阶 | 1.0 - 1.2 | 0.75 | 提质量 |
| 三阶 | 1.0 - 1.25 | 0.85 | 控最终可提交 |

---

## 七、6 天达成 10000 积分方案（官方推荐）

### 7.1 核心策略：逐步切换数据集 + 中性化

| 天数 | Step 1 | Step 2 | Step 3 | 预期产出 |
|---|---|---|---|---|
| **Day 1** | analyst4 + Subindustry (3线程) | — | — | 1-2 个 |
| **Day 2** | analyst4 + Subindustry (1线程) | analyst4 + Subindustry (2线程) | — | 3-4 个 |
| **Day 3** | fundamental6 + industry | analyst4 + MARKET | analyst4 + MARKET | 3-4 个 |
| **Day 4** | fundamental6 + industry | fundamental6 + industry | analyst4 + MARKET | 继续产出 |
| **Day 5** | fundamental2 + industry | fundamental6 + industry | fundamental6 + industry | 继续产出 |
| **Day 6** | — | fundamental2 + INDUSTRY (1线程) | fundamental6 + MARKET (2线程) | 🎯 达到 10,000 |

### 7.2 自相关性管理

- 自相关性 < 0.7 即可提交
- 但高自相关 + Sharpe 高出 10% 的，仍可提交
- 同一数据集、同一参数连续用 → 自相关爆表
- **从 Day 3 开始必须换数据集**

### 7.3 积分进度参考

| 时间 | 累计积分 |
|---|---|
| Day 1-2 | 0 - 4,000 |
| Day 3-4 | 4,000 - 8,000 |
| Day 5-6 | 8,000 - 10,000+ |

### 7.4 实战案例：scdifsn 5 天达 10000 分

| 日期 | 进展 |
|---|---|
| 1/6 | 开始提交 |
| 1/10 | 达到 10,000 分 |
| 1/13 | 收到金牌邀请 + 提交问卷 |
| 2/18 | 准顾问（提交 34 个） |
| 4/28 | 正式顾问 |

---

## 八、各阶段提交策略

### 8.1 金牌之前

- **目标**：拿到 10,000 分
- **数量**：每天 1-2 个
- **原因**：每个 alpha 1000-2000 分，多了不加分

### 8.2 金牌后、顾问前

- **目标**：加速审核（提交满 20 个 + 2000 次回测）
- **数量**：前两天 5 个/天，之后每 2 天 1 个
- **注意**：还没成为顾问，**提交了也拿不到钱**
- ⚠️ 提交多了拉低自相关池子，反而不好

### 8.3 背调期、顾问前

- **目标**：保持活跃，等 office
- **数量**：每 2 天 1 个
- **原因**：保持活跃有助于提前排队

### 8.4 顾问期

- **目标**：开始赚钱
- **数量**：每天 1-4 个，**质量优先**
- **收入**：前 4 个算 Base Payment

### 8.5 ⚠️ 准顾问期的隐藏规则（重要）

**在收到顾问合同前**的提交策略：

1. **保活频率**：提高到 2 天 1 个
2. **保留高质量的**：特别是 Spectacular 级
3. **不要交特别好**：尤其是特殊豁免（高 SP 豁免），**留着过了顾问再交**
4. **也不要交太差**：交中间偏上质量
5. **避免高自相关**：会拉低正式顾问后的 VF 值

💡 原因：高自相关的「好 alpha」一旦准顾问期间交完，正式顾问后同样好但已经不能交（自相关高），反而被坑。

---

## 九、数据集选择

### 9.1 优先级排序

| 优先级 | 数据集 | 名称 | 适用 |
|---|---|---|---|
| ⭐⭐⭐⭐⭐ | news18 | Ravenpack News Data | 高频更新，Sharpe 最高 |
| ⭐⭐⭐⭐⭐ | news12 | US News Data | news18 备选 |
| ⭐⭐⭐⭐ | model51 | Systematic Risk Metrics | 风险因子，结构化 |
| ⭐⭐⭐⭐ | model16 | Fundamental Scores | 综合分 |
| ⭐⭐⭐⭐ | socialmedia12 | Sentiment Data | 情绪因子 |
| ⭐⭐⭐⭐ | socialmedia8 | Social Media Data | 社交信号 |
| ⭐⭐⭐ | analyst4 | Analyst Estimate Data | 分析师预期，**官方推荐入门** |
| ⭐⭐⭐ | fundamental6 | Company Fundamental Data | 量大，**官方 6 天方案主力** |
| ⭐⭐⭐ | pv13 | Relationship Data | 分组用 |
| ⭐⭐ | pv1 | Price Volume Data | 易撞车 |
| ⭐⭐ | option8/9 | Volatility/Options Data | 字段少 |
| ⭐ | fundamental2 | Report Footnotes | 信号弱 |

### 9.2 Vector vs Matrix 数据（重要概念）

**Matrix Data**：每天每只股票一个值（普通）
**Vector Data**：每天每只股票**多个值**（事件型）

| 维度 | Vector | Matrix |
|---|---|---|
| 数据形态 | 事件流（如新闻、订单） | 数值序列 |
| 处理 | 需先聚合 `vec_avg` / `vec_sum` | 直接用 |
| 算子链 | `vec_avg(vec_a) + ts_rank(vec_b, 22)` | `ts_rank(close, 22)` |

💡 **Vector 数据必须先用 vec_avg / vec_sum / vec_std 等聚合**才能进入普通算子链。

### 9.3 探索新数据集的 6 种方法

官方社区推荐：

1. **覆盖率检查**：`group_count(field, group)` 看覆盖率
2. **Long/Short Count**：(Long Count + Short Count) / Universe Size 看信号覆盖
3. **时序分布**：`ts_std_dev(x, 5/22/66)` 看 N 日内波动
4. **截面分布**：`rank(x)` 看横截面分散度
5. **正态性**：`winsorize(x, std=4)` 后看异常值比例
6. **试跑**：`ts_rank(field, 22)` 跑一组看 Sharpe

### 9.4 提高 Return 的数据集

1. 提升 turnover → 用 lower decay
2. 流动性高的 universe（smaller）
3. 提高收益波动性（保持 Sharpe）
4. 尝试用 new 和 analyst 数据集

---

## 十、中性化（Neutralization）选择

### 10.1 强度递增

`NONE → MARKET → INDUSTRY → SUBINDUSTRY`

### 10.2 按数据类型选择

| 数据类型 | 建议起始 | 原因 |
|---|---|---|
| 基本面（fundamental6, analyst4） | INDUSTRY / SUBINDUSTRY | 行业因素影响大 |
| 量价（pv1, pv13） | MARKET | 市场整体趋势影响大 |
| 情绪（sentiment1, nws77） | MARKET 或 INDUSTRY | 视具体数据 |
| 期权（option8, option9） | MARKET | 市场因素主导 |
| 模型（Model 类） | NONE | 已经过处理 |

### 10.3 计算过程（重要）

**核心逻辑**（韩国 velog 详解）：

```
Neutralization = 减去组内均值
例如：
原值 = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
组均值 = 0.5
中性化后 = [-0.3, -0.2, -0.1, 0, 0.1, 0.2, 0.3, 0.4]
```

**目的**：构建多空平衡的投资组合，避免全多头/全空头。

### 10.4 公式 vs Setting（等价）

```python
alpha1 = -ts_returns(close, 5) with industry in Neutralization
# 等价于
alpha1 = group_neutralize(-ts_returns(close, 5), industry)
```

### 10.5 实操建议

- 用同一表达式分别测试不同中性化
- 选 Sharpe + Fitness 综合最优的
- 没有"万能"中性化方式

---

## 十一、常用算子速查

### 11.1 时序算子 ts_*

```python
ts_rank(x, d)            # 时序百分位排名
ts_zscore(x, d)          # 时序标准化
ts_mean(x, d)            # 移动平均
ts_std_dev(x, d)         # 移动标准差
ts_delta(x, d)           # 差分
ts_arg_max(x, d)         # d 日内最大值位置
ts_arg_min(x, d)         # d 日内最小值位置
ts_corr(x, y, d)         # 时序相关系数
ts_decay_linear(x, d)    # 线性衰减
ts_backfill(x, d)        # 缺失回填
ts_sum(x, d)             # 求和
ts_regression(y, x, d)   # 时序回归
```

### 11.2 截面算子

```python
rank(x)                  # 截面百分位排名（0~1）
zscore(x)                # 截面标准化
quantile(x, n)           # 分桶
normalize(x)             # 归一化
scale(x)                 # 缩放
sign(x)                  # 符号
```

### 11.3 组算子 group_*

```python
group_neutralize(x, group)  # 组内中性化
group_rank(x, group)        # 组内排名
group_zscore(x, group)      # 组内标准化
group_mean(x, group)        # 组内均值
group_backfill(x, group)    # 组内回填
group_count(x, group)       # 组内计数
# 加权版本
group_mean(x, weight, group) # 用 weight 加权计算组内均值
```

### 11.4 条件算子

```python
trade_when(open_event, signal, exit)  # 条件入场
is_nan(x) ? a : b                      # 缺失值条件
hump(x, threshold)                     # 阈值过滤
```

### 11.5 向量算子 vec_*

```python
vec_avg(x)      # 向量取平均
vec_sum(x)      # 向量求和
vec_std(x)      # 向量标准差
```

### 11.6 逻辑算子

```python
x > y           # 大于
x == y          # 等于
x ? a : b       # 三元
and, or, not    # 逻辑
```

💡 **BRAIN 中 true = 1，false = 0**。

---

## 十二、NaN / 覆盖率处理

### 12.1 三种方式

```python
# 方式 A：Settings → NAN HANDLING = On
# 方式 B：用 is_nan 兜底
is_nan(ts_rank(income_tax, 60)) ? ts_rank(sales, 60) : ts_rank(income_tax, 60)

# 方式 C：ts_backfill
ts_backfill(x, lookback=120, k=1, ignore="NAN")
```

### 12.2 覆盖率阈值

| 覆盖率 | 处理 |
|---|---|
| > 60% | 直接用 |
| 30% - 60% | 加 group_mean / group_backfill |
| < 30% | 换字段 |

### 12.3 降低 Weight 集中的方法

- 添加归一化函数（rank）
- 降低 truncation（建议 0.05 - 0.1，即 5-10%）
- 使用 ts_backfill 解决低覆盖率

---

## 十三、trade_when 条件逻辑

### 13.1 标准结构

```python
trade_when(open_event, signal, exit)
# open_event：入场条件（True 时持仓）
# signal：信号主体（一/二阶 alpha）
# exit：出场条件（-1 = 一直持仓）
```

### 13.2 ⚠️ exit = -1 的含义

- 退场条件写 -1 = **bool 变量，等同于 False**
- 表示**不退出**，一直持仓
- 退场写 1 = 立即平仓
- 退场写其他条件 = 满足时平仓

### 13.3 常用 open_event 模板

```python
# 放量突破
ts_arg_max(volume, 5) == 0
# 站上均线
close > ts_mean(close, 22)
# 波动率放大
ts_std_dev(returns, 5) > ts_std_dev(returns, 20)
# 量价齐升
ts_corr(close, volume, 10) > 0.5
# 价格新高
ts_arg_max(close, 20) == 0
```

### 13.4 注意事项

- trade_when 是「锦上添花」，signal 本身 Sharpe > 1.0 才有用
- 出场 -1 = 一直持仓（最稳）
- ❌ 不要三层 trade_when 嵌套（过拟合）

---

## 十四、经典 Alpha 模板库

### 模板 A：动量反转（pv1 + news12）

```python
rank(ts_zscore(close, 22)) * -ts_rank(volume, 5)
```

### 模板 B：分析师预期修正（analyst4）

```python
ts_rank(eps_est_chg_30d, 60) - ts_rank(revenue_est_chg_30d, 60)
```

### 模板 C：风险因子（model51）

```python
group_neutralize(-ts_rank(beta, 252), subindustry)
```

### 模板 D：新闻情绪（news18）

```python
ts_rank(sentiment_score, 5) * ts_delta(close, 1)
```

### 模板 E：跨资产综合（model16 + pv1）

```python
group_neutralize(
    ts_zscore(value_score, 66) - ts_zscore(momentum_score, 66),
    industry
)
```

### 模板 F：完整实战范例

```python
group_neutralize(
    ts_mean(
        winsorize(
            ts_backfill(implied_volatility_call_1080 / implied_volatility_mean_10, 120),
            std=4
        ),
        22
    ),
    densify(pv13_r2_min2_3000_sector)
)
```

### 模板 G：量价回归（pv 数据）

```python
# vwap/close 均值回归（社区实战）
rank(vwap / close)
```

### 模板 H：质量因子

```python
# mdf_qty 质量数据 + 行业压力期测试
group_mean(returns, volume, densify(sector))
```

---

## 十五、指标调优

### 15.1 提高 Sharpe

1. **提 Return**（重点）
2. **降波动性**：
   - 用 `group_neutralize`
   - 用 `trade_when` 砍无效信号
   - 用 `winsorize` 截极值

### 15.2 提高 Return

1. 提升 turnover，用 lower decay
2. 用流动性高的 universe（smaller）
3. 在保持收益与回撤水平不变的前提下，提高策略波动性
4. 尝试 new 和 analyst 数据集

### 15.3 调节 Turnover

| 目标 | 动作 |
|---|---|
| **降 Turnover** | 加 decay、用 rank、用 trade_when、用 hump、组合低换手 alpha |
| **升 Turnover** | 减 decay、缩小 universe（top3000→top1000）、缩短窗口、用高频数据 |

💡 **top3000 是流动性较高的 top1000 + 流动性较差的 2000 只组成**。top3000 反而流动性较低。

### 15.4 提高 Fitness

```
Fitness = Sharpe × sqrt(abs(Returns) / max(Turnover, 0.125))
```

依照公式调整变量即可：
1. 增加 return
2. 降低 turnover

### 15.5 提升 Sub-Universe 通过率

通过公式（D1）：`sqrt(252) × max(0.065, (subuniverse_size/largest_universe_size) × 0.15)`

策略：
1. 在更小的子池子测试 alpha 表现
2. 然后提交到更大的 universe

### 15.6 提升 Super-Universe 通过率

通过条件：`sharpe of next largest universe > 0.7 × sharpe of alpha`

策略：
1. 测试 alpha 在更大 universe 的表现
2. Sharpe 衰减 < 30% 才算稳定

---

## 十六、降低自相关性的 5 种方法

1. **更换数据集**：pv1 → pv13，fundamental6 → analyst4
2. **使用不同算子**：ts_rank → ts_zscore，group_rank → rank
3. **改变信号逻辑**：动量 → 均值回归，截面 → 时序
4. **调整时间窗口**：5 天 → 20 天
5. **增加条件过滤**：trade_when 条件

❌ **不要为降自相关加噪声**（平台会检测惩罚）

---

## 十七、自动化工具配置（以「老强说 Alpha 辅助工具 v1.0.5」为例）

### 17.1 Stage 1 推荐配置

```
数据集：news18 / analyst4（按 6 天方案轮换）
区域：USA
延迟：1
股票池：TOP3000
中性化：Subindustry
任务表达式数 Max Run：1500
Sharpe 阈值：0.9
Fitness 阈值：0.6
最少做多数：80
最少做空数：80
```

### 17.2 Stage 2/3 推荐配置

```
数据集：同 Stage 1
区域：USA
延迟：1
股票池：TOP3000
中性化：Subindustry
Max Run：1500
Sharpe 阈值：1.0 - 1.15
Fitness 阈值：0.85
最少做多：100
最少做空：100
```

### 17.3 工具参数速查

| 参数 | 推荐值 | 说明 |
|---|---|---|
| Region | USA | 池子大、Sharpe 高 |
| Delay | 1 | 避免前视偏差 |
| Universe | TOP3000 | 平衡流动性与广度 |
| Instrument Type | Equity | 股票 |
| Neutralization | Subindustry | 粒度合适 |
| Max Run | 1500 | 省铜牌 |
| Sharpe | 0.9 - 1.2 | 看阶段 |
| Fitness | 0.6 - 0.85 | 看阶段 |
| 最少做多/空 | 80 - 120 | 防过拟合 |

### 17.4 三线程分配技巧

工具支持一/二/三阶并行跑：
- **线程 1**：继续跑一阶（产出新种子）
- **线程 2**：跑二阶（消耗一阶种子）
- **线程 3**：跑三阶（套 trade_when）
- 三阶段产出的 alpha 数量通常比一阶段多 2-3 倍

### 17.5 Super Alpha 框架（GitHub 开源工具）

```python
# 来自 xiegengcai/world-quant-brain
combo_ops = [ts_rank, ts_zscore, ts_arg_min, ts_delta, ts_std_dev, ts_mean]
days = [5, 22, 66, 120, 240]

# 一阶生成：op(field, day) 的笛卡尔积
# 二阶工厂：ts_second_order / group_second_order
# 三阶工厂：trade_when_factory
```

---

## 十八、每日操作 SOP

### 18.1 早晨（10 分钟）

```
1. 登录 BRAIN 平台 → 看今日可用提交次数
2. 打开工具 → 「Alphas」Tab → 处理昨天未提交
3. 切到「可提交」Tab → 按 Sharpe 排序
4. 开启「行颜色标记」
5. 先提交 1 个 → 等待 5 分钟看结果
6. 成功则继续提交 1-2 个
```

### 18.2 上午（30-60 分钟）

```
7. Stage 1：选新数据集（每天换，按 6 天方案）
8. 配置参数（按 17.1）
9. 启动一阶段任务
10. 同步近 3 天 Alpha（每天 1 次）
```

### 18.3 下午（30-60 分钟）

```
11. Stage 1 完成 → 自动进入 Stage 2
12. Stage 2 完成 → 自动进入 Stage 3
13. Stage 3 完成 → 「Alphas」Tab 看结果
14. 跑「快速查可提交」自动筛选
```

### 18.4 晚上（10 分钟）

```
15. 提交当天产出的最优 alpha
16. 记录今天产率（Excel/Notion）
17. 复盘：哪个数据集产出最好
```

---

## 十九、问题排查清单

| 现象 | 原因 | 解决 |
|---|---|---|
| 一阶 0 个种子 | 阈值太高 | 降到 0.5 |
| 一阶种子 > 500 | 阈值太低 | 提到 1.0 |
| 二阶全军覆没 | group 选择不当 | 换 industry / subindustry |
| 三阶全失败 | trade_when 模板不合适 | 换模板 |
| 提交失败：自相关高 | 与历史太像 | 换数据集、加 trade_when |
| 提交失败：Weight 集中 | 缺归一化 | 加 rank、truncation 0.08 |
| 提交失败：Sharpe < 1.25 | 信号弱 | 换数据集、改中性化 |
| 提交失败：Turnover > 70% | decay 太小 | 加大 decay 到 4-8 |
| 提交失败：Sub-Universe 不通过 | 信号只在 TOP3000 有效 | 在更小池先测 |
| Change < 0 | 与历史池子冲突 | 换数据集方向 |
| Weight 集中 / 分配股票少 | 数据字段稀疏 | 加 NAN HANDLING / ts_backfill |
| 工具一直转圈 | 网络/平台问题 | 重启工具/换时段 |
| 错误码 1001 | IP 被封 | 联系导师去 ippure.com 解锁 |
| 提示账号密码错误 | 密码有空格 | 检查大小写、空格 |
| 官网 504 | 平台繁忙 | 稍后再试 |
| 进程被锁 | 工具并发已满 | 一阶段 1-2 线程即可 |
| 获取字段池失败 | 官网炸了 | 稍后重试 |
| WebView2 错误 | 环境缺失 | 手动安装 webview2 |
| 当前 scope 无可消费 | 二阶段被锁 | 释放后重新分配 |

---

## 二十、11 个常见踩坑（必看）

| # | ❌ 错误 | ✅ 正确 | 严重 |
|---|---|---|---|
| 1 | 自行注册账号 | 在导师引导下用邀请码注册 | ⭐⭐⭐⭐ |
| 2 | 抄袭问卷答案 | 用自己语言组织 | ⭐⭐⭐ |
| 3 | 添加噪声降自相关 | 换数据集或改信号逻辑 | ⭐⭐⭐ |
| 4 | 地址用拼音 | 用 AI 翻译成标准英文 | ⭐⭐⭐⭐ |
| 5 | 5 年地址有空白 | 时间线连续无间断 | ⭐⭐⭐⭐ |
| 6 | 在职填了截止日期 | Date To 留空 | ⭐⭐⭐⭐ |
| 7 | 离职原因与在职矛盾 | B.01=No 则 B.01.12 也 N/A | ⭐⭐⭐⭐ |
| 8 | 服务器开代理 | 国内直连，不开 VPN | ⭐⭐⭐ |
| 9 | 服务器休眠 | 电源选项设为「从不」 | ⭐⭐⭐ |
| 10 | 身份、银行信息不一致 | 手机/身份证/银行卡三一致 | ⭐⭐⭐ |
| 11 | 忘记确认发票 | 账单日登录 Workday 确认 | ⭐⭐⭐ |

---

## 二十一、关键概念速查

### 21.1 Decay

- 控制 alpha 权重随时间衰减速度
- **0** = 无衰减（噪声大）
- **1 - 5** = 短期信号
- **5 - 15** = 中期（**推荐**）
- **> 20** = 长期（接近无效）

### 21.2 Truncation

- 限制单只股票最大权重
- **0.05** = 5% 上限（稳健）
- **0.08 - 0.10** = 平衡（**常用**）
- **0.20+** = 集中

### 21.3 Value Factor (VF)

- 平台对 alpha 的综合评分
- 范围 0 - 1（也有 0-10 体系）
- 越高越好
- 每月更新，基于过去 3 个月
- 0.95 vs 0.5 收入差 10 倍+

### 21.4 Pyramid

- 至少 3 个不同数据集/策略类型 = Gold 门槛
- 升 Expert/Master 需要更多 Pyramid

### 21.5 Neutralization 强度

NONE < MARKET < INDUSTRY < SUBINDUSTRY

### 21.6 Self-Color 标记

- 🟢 绿色 = 可提交
- 🟡 黄色 = 边缘
- 🔴 红色 = 不可提交

### 21.7 Book Size

- 假设的资金规模：**\$20 Million**（默认）
- 用于计算 Return = AnnualizedPnL / (0.5 × BookSize)

### 21.8 Self-Coloration 计算方法

平台方式是计算两两 Alpha 之间 **PnL 的相关系数**：
- 一个 Alpha 每天产生一个 PnL
- 多天的 PnL 构成时间序列
- 两组 PnL 序列比对 → 相关系数

### 21.9 Sharpe（IR）

```
IR = Return / std_dev(Return)
```

- 衡量风险调整后的收益
- D1 需 > 1.25
- D0 需 > 2.0

### 21.10 Annual Return

```
AnnualReturn = AnnualizedPnL / (0.5 × BookSize)
BookSize = $20M (假设)
```

---

## 二十二、基础测试问卷 9 题详解（核心章节，alphadoc 第七章完整版）

> 数据来源：[alphadoc.biglongxia.com/guide/07-填写基础测试问卷](https://alphadoc.biglongxia.com/guide/07-填写基础测试问卷)
> 视频教程：<https://ucnxcevc36pi.feishu.cn/minutes/obcnoib9212zgmfs6q7m344h>

### 22.1 问卷概述

- **名称**：Research Capability Test（研究能力测试）
- **时机**：达到 **Gold** 等级后，平台向注册邮箱发送链接
- **期限**：**一周内**完成，实际一晚即可
- **机会**：**仅 2 次**作答机会，**第 2 次比第 1 次审核更严苛**
- **提交 Workday 必须先过问卷**，否则账号与顾问无缘
- ⚠️ **机器审核查重**，严禁抄袭
- ⚠️ 切勿在社群范围外提到工具及教程站，低调干大事

### 22.2 ⚠️ 三大死亡红线（来自 alphadoc）

1. ❌ **切勿直接复制他人答案** — 平台机器审核自动检测相似度
2. ❌ **填写到一半不会保存，不能暂停** — 一次性填完再提交
3. ❌ **问卷两次都失败 + 已提交 Workday = 永久失去顾问资格**

### 22.3 答题思路（5 步法）

```
1. 读 Learn 板块官方文档（documentation 页面）
2. 用 AI 辅助理解概念（不是抄答案）
3. 用自己的语言组织答案
4. 让 AI 互相检查确认无幻觉
5. 新建文档写答案，再粘贴进答题区（因答题区显示框难用）
```

**重要原则**：
- 参考但不要抄袭 — AI 和知识库可帮你理解方向，但必须重新表达
- 使用 AI 辅助作答和检查 — 让 AI 给你讲，看不懂的概念让它解释
- ⚠️ AI 容易出现幻觉，必须多 AI 交叉核查

### 22.4 时间要求 Q&A

**Q：测试和问卷，有填写时间要求吗？**

A：
- **时间要求**：一周内填写完成，实际一晚上搞定
- **可以打开看题目，写好答案再复制进去**
- ⚠️ **填写到一半不会保存，不能暂停**

### 22.5 各题完整参考答案方向

#### Q1-Q3（基础概念题，题目每年变化）
- 建议读 Learn 板块的 Overview 页面
- 不必死记硬背，AI 辅助理解后用自己的话答

#### Q4：What is the difference between Matrix Data and Vector Data?

**参考答案方向**：

**Matrix Data**（矩阵型数据）：
- 每天每只股票 **1 个值**
- 例：`close`、`volume`、`returns`

**Vector Data**（向量型数据）：
- 每天每只股票 **多个值**（事件型）
- 例：一天 5 条新闻 → 5 个情绪分数
- 例：分析师评级：买入/持有/卖出 → 3 个分值

**处理方式**：
```python
# Vector 数据需要先用 vec_* 聚合
ts_rank(vec_avg(news_sentiment), 22)  # 正确
ts_rank(news_sentiment, 22)          # 错误
```

**参考资料**：
- <https://platform.worldquantbrain.com/learn/documentation/understanding-data/data>

#### Q5：什么是 long count? short count? 如何使用?

**参考答案方向**：

**做多（Long Position）**：
- 操作：看好某资产会涨，现在买入，等涨价卖出
- 生活例子：球鞋 1000 元买，1500 元卖，净赚 500
- 风险：最大损失 = 买入价（跌到 0）
- 收益：理论上无上限

**做空（Short Position）**：
- 操作：看空某资产，先借来以高价卖出，等跌价买回归还
- 生活例子：玩具娃娃 100 元借 1 个卖 100，跌到 50 元买 1 个还，净赚 50
- 关键步骤：借入 → 高价卖 → 低价买 → 归还
- 风险：损失理论上无上限（价格可能无限涨）
- 收益：上限 = 卖出价（跌到 0）

**Long Count**：策略在某时点建议做多的股票数量
**Short Count**：策略在某时点建议做空的股票数量

**使用场景**：
1. **估算覆盖率**：(Long Count + Short Count) / Universe Size
2. **评估数据字段活跃度**：日均非零值数量
3. **公式模板**：
   ```python
   # 把字段二值化
   (mdl77_2400_chg12msip != 0) ? 1 : 0
   # 求日均非零值
   ts_mean(...)
   ```
4. **窗口影响**：
   - N=66（季度）→ 接近真实覆盖率
   - N=22（月）→ 约 1/3 覆盖率
   - N=5（周）→ 接近 0

**官方论坛参考资料**：
- <https://support.worldquantbrain.com/hc/en-us/community/posts/11807866133911>
- 标题："BRAIN TIPS: 6 ways to quickly evaluate a new dataset"

#### Q6：请查阅 Learn 文档，谈谈您对中性化 (neutralization) 的理解及其计算过程

**参考答案方向**：

**定义**：中性化是构建**多空平衡投资组合**的过程，**减去组内均值**让每个组内多空暴露平衡。

**计算过程**（手算示例）：
```
原值 = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
组均值 = 0.5
中性化后 = [v - 0.5 for v in 原值]
        = [-0.3, -0.2, -0.1, 0, 0.1, 0.2, 0.3, 0.4]
```

**目的**：
- 避免全多头或全空头组合
- 剥离不想要的风险因子暴露
- 让 alpha 信号更纯粹

**分组层级**（粒度递增）：
- NONE → MARKET → SECTOR → INDUSTRY → SUBINDUSTRY

**与公式等价**：
```python
# 以下两种写法等价
group_neutralize(-ts_returns(close, 5), industry)
# 等价于
-ts_returns(close, 5) + industry in Neutralization
# 都用 None in Neutralization, 0 in Decay, 0 in Truncation
```

**参考资料**：
- <https://platform.worldquantbrain.com/learn/documentation/create-alphas/neut-cons>

#### Q7：复现一个 Alpha Example，阐述理解与改进

**答题模板**（视频中给出，7 步法）：
```
1. 我复现了哪个 Alpha
2. 它背后的市场逻辑是什么
3. 我用什么参数跑出来什么结果
4. 我发现它有什么问题
5. 我为什么这样改
6. 改完以后哪些指标变好，哪些指标变差
7. 最后我从结果中得到了什么理解
```

**实施建议**：
- 选择一个简单 Alpha 起步（14 个官方示例可选）
- 逐步添加算子优化，每一步解释原因
- ⚠️ 开放型答案，没有标准答案
- 教程视频：<https://ucnxcevc36pi.feishu.cn/minutes/obcnnqn66utoiy55ppyenk3y>

**模板的妙用**：这套 7 步法**也可以作为与 AI 沟通的提示词**，在搞懂并优化一个 Alpha 后，用这套模板作为答题结构，条理清晰。

#### Q8：请阐述如何通过 BRAIN 平台网页获取 Alpha ID?

**操作步骤**（4 步法）：
```
1. 打开 Alpha 页面
2. 在 Alpha 页面中选择一个 Alpha 点开详情页
3. 点击 "Open details in a new tab"
4. 浏览器地址栏最后一个标识符就是 Alpha ID
   （字母数字组合，7 位左右，ima 知识库说"7 位"不完全准确）
```

#### Q9：请详尽列举 Genius 计划各个级别的名称及其对应的季度奖金范围

**答案**（直接查官方）：

| 等级 | 季度奖金范围 |
|---|---|
| Gold（金牌） | \$100 固定 |
| Expert（专家） | \$200 - \$2,000 |
| Master（大师） | \$2,000 - \$8,000 |
| Grandmaster（特级大师） | \$8,000 - \$25,000 |

**参考资料**：
- <https://support.worldquantbrain.com/hc/zh-cn/community/posts/27294185989527>

### 22.6 注意事项

1. **用自己的语言** — 机器审核检测相似度，照搬必被拒
2. **理解而非记忆** — 彻底理解再组织答案
3. **善用 Learn 页面** — 官方文档是最权威的参考
4. **答案有条理** — 分点、分段使答案清晰
5. **适当使用英文术语** — 部分中文翻译不准确（universe、fitness 等），可直接用英文

---

## 二十三、成为顾问流程（alphadoc 第九章完整版）

> 数据来源：[alphadoc.biglongxia.com/guide/09-成为顾问](https://alphadoc.biglongxia.com/guide/09-成为顾问)
> 注：alphadoc 第 08 章是 Workday 填写截图教程

### 23.1 全流程时间线

```
注册平台 → 跑 Alpha（1-7 天）→ 10000 分
    ↓
收到金牌邀请邮件（1-2 天）
    ↓
填测试问卷（1 天） + Workday（1 天）
    ↓
进入「有条件顾问」状态
    ↓
背景调查（几天到几周）
    ↓
正式顾问 → 收入开始
```

**最快路径**：约 2 周即可成为正式顾问并看到第一笔收入

### 23.2 有条件顾问阶段

Workday 表格提交后，**立即**进入「有条件顾问」状态：

- ✅ **可以开始提交 Alpha**，这些提交会计入 Base Payment（\$1-60/天）
- ⏳ 背景调查（Background Check）正在进行中
- 💰 Base Payment 的钱会**先累积**，等背调通过后一并发放

⚠️ **三大注意事项**：
1. 如背调未通过，则提交的 Alpha **不会** 计入 Base Payment
2. 请留意查看邮件（含垃圾邮件）或电话，及时签署**背景审查授权文件**，否则可能影响转正
3. ⚠️ **等到收到背调完成的通知邮件后**，再更新银行账户信息，**提前更新可能导致流程问题**

### 23.3 背景调查

#### 调查内容

- 核实个人信息真实性
- 核实学历信息
- 核实工作经历（如填写了，会查劳动合同）
- **通常不需要**提供无犯罪记录证明

#### 调查时长

- **无工作经验或经验简单** → 较快（可能几天到一周）
- **有较多工作经历** → 较慢（可能两周到一个月）
- 受排队等因素影响

#### 背调期间

- 不影响 Base Payment 的累积
- 可以继续提交 Alpha
- **不需要做任何额外操作**

### 23.4 银行卡填写

#### 填写位置

Workday 系统中 **「Bank Account Details」** 模块

#### 填写信息

- 银行名称（英文）：如 `Agricultural Bank of China`
- 银行账号
- 开户行信息
- 账户持有人姓名（**须与注册姓名一致**）

⚠️ **确保银行信息填写正确**，否则会延误付款。如有变更及时在 Workday 更新。

⚠️ **必须等背调完成通知邮件到了再更新**银行账户，提前更新可能导致流程问题

### 23.5 正式顾问

背调通过后，你成为正式顾问：

- ✅ Base Payment 正常到账
- ✅ 获得**完整的顾问权限**
- ✅ 可以使用**更多数据集和操作符**（根据等级）
- ✅ 可以申请 Genius Program 中的 **Super Alpha 功能**（Expert 及以上）

### 23.6 收入开始

#### 首笔收入

- 确认银行信息后，**下一个账单周期**即可收到付款
- 账单确认日期到了后，登录 Workday **手动确认**
- 确认后约 **一周内到账**（**农行最快，通常第二天**）

#### 收入构成

| 收入类型 | 频率 | 金额范围 |
|---|---|---|
| Base Payment（基础薪酬） | 每 2 个月 | \$1-60/天（最高 \$120/天，含 alphas + super alphas） |
| Quarterly Payment（季度奖金） | 每季度 | \$100 - \$25,000 |
| 比赛奖金 | 不定期 | 视赛事而定（IQC 总奖池 \$10 万） |
| 推荐费 | 每成功一人 | \$100-200（无上限） |

#### 日收入四大影响因素

你的日收入**不是固定的**，而是与**全球顾问比较**的结果：

1. **提交数量** — 你比别人提交的多吗？
2. **提交质量** — Sharpe、Fitness 高吗？
3. **自我成长（Self-Improvement）** — 你比自己过去进步了吗？
4. **Value Factors (VF)** — 平台打分，范围 **0-10**，分数越高越好，根据 Alpha 表现和季度积累决定
   - ⚠️ **VF 值直接影响你的收入**！当前 Theme 对质量分有倍数加成（Dataset Themes / Region Themes / Super Alpha Themes）

#### Base Payment 决定要素（详细版）

```
- 提交数量（相比全球其他顾问）
- 提交质量（相比全球其他顾问）
- 自我成长与历史相比的比较
- Value Factors（**越接近 1 越好**）
- 当前 Theme 对质量分有倍数加成
```

#### Quarterly Payment 决定要素

```
- 金额范围：100 - 25,000 USD/季度
- 条件：上季度超过 20 天有提交
- 决定因素：
  - 由 Weight 和 OS 表现决定
  - Weight 需要时间的积累
  - OS 结果与 Value Factors 直接相关
- 通常情况下好的 Alpha 具备：
  - sub-universe 和 super universe 有 70% Sharpe
  - Turnover 在 30% 以下
  - Margin 大于 4 bps
  - 不要为了通过相关性检测加噪音（避免 overfitting）
```

### 23.7 成为顾问后的第一件事

1. ✅ 确认银行信息已填写正确
2. ✅ 提交 alpha 策略变更：**质量最重要**，其次是活跃度和数量
3. ✅ 拓展数据集使用范围（Pyramid ≥ 3）
4. ✅ 关注 Performance Comparison，**确保每次提交的 Change 为正**
5. ✅ 养成习惯：只提交 **Sub-universe Sharpe ≥ 0.7、Turnover < 30%、Margin > 4 bps** 的因子

### 23.8 准顾问期间的提交策略（重要！）

⚠️ **在收到顾问合同前**，保持活跃（**2 天至少交 1 个**），保护 fitness 值高的，特别是 SP 级别的，但注意**相关性要低**，特殊豁免的 SC 值高会影响后续 VF 值。

#### 提交策略要点

1. **保活频率**：提高到 **2 天 1 个**
2. **保留高质量的**：特别是 **SP 级的**
3. **不要交特别好的**：日常交一般、good（自相关性高的，**不建议交，会影响 VF 值，影响正式顾问收益**）
4. **也不要交太差**：交**中间偏上**质量就可以了
5. **不要交特殊豁免的**：留着过了顾问再交

### 23.9 ⏰ 时间线总结

```plaintext
注册平台 → 使用工具提交 Alpha（1-7 天）→ 达到 10,000 分
 → 收到金牌邀请邮件（1-2 天）
 → 填写 Workday + 问卷（1 天）
 → 背景调查（几天到几周）
 → 正式顾问，开始稳定收入
```

最快路径约 **2 周**即可成为正式顾问并看到第一笔收入。

📖 **下一步**：第十章 顾问后 Alpha 策略优化

---

## 二十四、准顾问期提交策略（重要！）

### 24.1 ⚠️ 核心原则

**在收到顾问合同前**，策略与正式顾问**完全不同**。

### 24.2 具体策略

1. **保活频率**：2 天 1 个
2. **保留高质量**：特别是 Spectacular 级
3. **不交特别好**：高 SP 豁免的**留到正式顾问后**再交
4. **交中间偏上**：质量过得去，但别是最好的
5. **避免高自相关**：会拉低正式顾问后的 VF 值

### 24.3 为什么

- 准顾问期间的提交也占用了"自相关池子"
- 高 SC 值的 alpha 一旦交了，正式顾问后无法再交同款
- 影响后续 VF 值和收入

---

## 二十五、路由表方法论（实战精华）

### 25.1 核心观点

来自 aiquantclaw.com 的实战洞察：

> **Brain 公式成败，常常先由路由关系决定，而不是由长度决定。**
> **数据域、中性化和 Universe 梯度定义了 alpha 在和谁比较。**
> **先写路由表再扩公式，能显著降低无效试错。**

### 25.2 路由三要素

| 要素 | 决定什么 |
|---|---|
| **数据域** | 比较对象（财务？价格？新闻？） |
| **中性化** | 比较坐标（行业？子行业？市场？） |
| **Universe 梯度** | 比较场景（TOP200？TOP1000？TOP3000？） |

### 25.3 路由卡模板

在写每个 alpha 前，先填这张卡：

```
原始字段：____________
数据域：____________ [Vector / Matrix]
是否需 vector 聚合：____________
中性化层级：____________ [NONE/MARKET/SECTOR/INDUSTRY/SUBINDUSTRY]
Universe 梯度：____________ [TOP200/1000/3000/全市场]
Decay：____________
Truncation：____________
Delay：____________ [0/1]
预期 Sharpe 区间：____________
```

### 25.4 Vector 数据的特殊处理

Vector 字段（事件型）必须先聚合：

```python
# 错误：直接用 vector 字段
ts_rank(news_sentiment, 22)  # ❌

# 正确：先 vec_avg 聚合
ts_rank(vec_avg(news_sentiment), 22)  # ✅
```

---

## 二十六、社区实战案例

### 26.1 案例 A：scdifsn（CSDN，2.8w 阅读）

**时间线**：
| 日期 | 事件 |
|---|---|
| 1/6 | 开始提交 |
| 1/10 | 10000 分 |
| 1/13 | 提交问卷 |
| 2/18 | 准顾问（34 个） |
| 4/28 | 正式顾问 |

**收入**：
- 第一周：每天 \$1.5-2
- EUR D1 主题周：最高 \$7/天
- 100 USD 新人奖

**建议**：
> 后续提高收入主要从两点入手：一是优化代码，提高挖掘因子的效率；二是理解 Operators 和各类数据字段，发掘更多更好的 Alpha 模板。

### 26.2 案例 B：Yan_ks（CSDN，量化学习笔记）

**对核心术语的解读**：
- Base Payment: 1-120 USD/Day（普通 + 超级）
- 决定要素：提交数量、提交质量、自我成长、Value Factors
- Theme Calendar 有倍数加成
- IQC 等比赛也是收入来源
- **推荐奖励：200 USD / 成功推荐**（社区版本）

**动量 vs 反转**：
- 动量：跟随趋势，趋势确立后继续
- 反转：趋势方向改变，价格回归

**横截面 vs 时序**：
- 横截面：某时点所有股票（rank、zscore、scale、sign）
- 时序：单只股票历史（ts_delta、ts_delay、ts_sum、ts_mean、ts_rank、ts_zscore、ts_std_dev、ts_regression）

### 26.3 案例 C：Oo_Amy_oO（CSDN，3.9k 阅读）

**Sharpe 提升方法**：
1. 增加 return（重点）
2. 降低波动性
3. 使用 neutralization
4. 使用 trade_when，winsorize

**Return 提升**：
1. 提升 turnover，用 lower decay
2. 用流动性高的 universe（smaller）
3. 提高收益波动性
4. 试 new 和 analyst 数据集

**Turnover 调节**：
- 降：加 decay、rank、trade_when、hump
- 升：减 decay、缩小 universe、缩短窗口、用高频数据

**Subuniverse 公式**（D1）：
```
sqrt(252) × max(0.065, (subuniverse_size/largest_universe_size) × 0.15)
```

**Superuniverse 公式**：
```
sharpe of next largest universe > 0.7 × sharpe of alpha
```

### 26.4 案例 D：tae0_（韩国 velog）

**rank + Neutralization 详解**：
```
原值 = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
rank 后 = [1/7, 2/7, 3/7, 4/7, 5/7, 6/7, 7/7, 1.0]   # 0~1 均匀
# 全部为正 → 全部做多（风险集中）
中性化 = 减去组均值 = [-0.3, -0.2, -0.1, 0, 0.1, 0.2, 0.3, 0.4]
# 多空平衡 ✅
```

### 26.5 案例 E：m0_73177400（CSDN）

**group_mean 加权**：
```python
group_mean(returns, volume, densify(sector))
# 用 volume 加权计算每个 sector 的平均 returns
# 然后组内所有元素都替换为该加权均值
```

**多 alpha 相关性计算**：
- 平台方式：计算两两 Alpha 之间 **PnL 的相关系数**
- 一个 Alpha 每天产生一个 PnL
- 多天 PnL 序列 → 相关系数

**Drawdown 定义**：
- 只考虑峰到其后谷的下降
- 例子 [4, 14, 3, 21, 9, 32, 17, 49] 的 Drawdown = 32 - 17 = **15**，不是 49 - 3 = 46

### 26.6 实战技巧汇总

1. **不要单纯调参**，要有数学建模依据和内在经济含义
2. **越高频的数据 → 越高频的换手**，但不代表更好
3. **VU 路由**比**加算子**更有效
4. **质量 > 数量**（顾问期）
5. **SP 豁免的好 alpha**留到正式顾问后再交

---

## 二十七、Workday 填写要点

| 项目 | 注意事项 |
|---|---|
| 地址 | 必须英文翻译，不能拼音 |
| 5 年历史 | 连续无间断 |
| 当前在职 | Date To 留空 |
| 离职原因 | 与在职状态自洽 |
| 身份信息 | 手机/身份证/银行卡三一致 |
| WQU 课程 | 填 N/A |
| 身份证 | 正反面拼一张图 |
| 账单 | 账单日手动确认 |

---

## 二十八、发薪日期

### 28.1 Base Payment（每 2 个月）

| 周期 | 账单确认日 |
|---|---|
| 2025/11 - 12 | 2026/01/31 |
| 2026/01 - 02 | 2026/03/31 |
| 2026/03 - 04 | 2026/05/31 |
| 2026/05 - 06 | 2026/07/31 |
| 2026/07 - 08 | 2026/09/30 |
| 2026/09 - 10 | 2026/11/30 |

### 28.2 Quarterly Payment

| 周期 | 发布日 | 账单确认 |
|---|---|---|
| Q4 2025 | 2026/02/23 | 2026/03/31 |
| Q1 2026 | 2026/05/27 | 2026/06/30 |
| Q2 2026 | 2026/08/25 | 2026/09/30 |
| Q3 2026 | 2026/11/24 | 2026/12/31 |

**条件**：上个季度有超过 20 天有提交记录

---

## 二十九、推荐计划

### 29.1 奖励

- 每成功推荐一位新顾问 = **\$100**（老强说版本）/ **\$200**（CSDN Yan_ks 版本）
- **无上限**

### 29.2 被推荐人需满足

1. 使用你的推荐码（Alias）注册
2. 最终成为正式顾问
3. 在 10 个不同的日子里提交过 Alpha
4. 保持顾问身份至少 1 个月

### 29.3 如何推荐

```
https://platform.worldquantbrain.com/referral/你的推荐码
```

### 29.4 推荐码查看

登录平台 → 右上角头像 → Account → 查看 User ID / Alias

---

## 三十、纳税

- 平台**代扣代缴**劳务所得税
- 这部分收益会与其他收益一起计入**次年税务汇算清缴**
- 保留所有收入记录
- 官方联系邮箱：mainlandchina@worldquantbrain.com

---

## 三十一、主题日历（Theme Calendar）

### 31.1 机制

- 平台定期发布主题（ESG、AI、红利、EUR D1 等）
- 匹配的 alpha 获得**收入倍数加成**（1.5-2 倍）
- 主题通常提前公布

### 31.2 应对策略

1. 关注 BRAIN 平台 Theme Calendar 页面
2. 看到主题后针对性开发
3. 日常高质量 alpha 仍是基本盘
4. 主题匹配时集中精力多交

### 31.3 Theme 类型

- **Dataset Themes**（数据集主题）
- **Region Themes**（区域主题）
- **Super Alpha Themes**（超级 alpha 主题）

---

## 三十二、官方学习资源

| 资源 | 位置 | 说明 |
|---|---|---|
| Learn 文档 | 平台内 Learn | 最权威知识库 |
| Operator Reference | Learn → Documentation → Operators | 算子完整说明 |
| Data Fields | Learn → Documentation → Data Fields | 数据字段解释 |
| Community Forum | 平台 Forum | 全球顾问交流 |
| Academy 课程 | Learn → Academy | 系统化视频课 |
| Theme Calendar | Learn → Theme Calendar | 主题活动 |
| BRAIN TIPS 帖 | Community Forum | 实用技巧 |

**建议学习顺序**：
```
1. 通读 Learn 核心文档
2. 完成 Academy 入门课程
3. 在 Forum 读 Expert/Master 分享
4. 尝试不同数据集 + 中性化组合
5. 关注 Theme Calendar
```

---

## 三十三、工具/服务器 FAQ

| Q | A |
|---|---|
| 工具要一直开吗？ | 是。24h 连续运行，建议云服务器 |
| 需要下载 Python 吗？ | 不需要，工具内置环境 |
| Mac 能用吗？ | 可以，用 Microsoft Remote Desktop |
| 服务器配置？ | 2 核 4GB 就够 |
| 服务器休眠？ | 控制面板 → 电源选项 → 从不 |
| 工具输入无反应？ | 重连远程桌面 |
| 二阶段只能跑 720？ | 平台上限，不是工具问题 |
| 因子提交后其他消失？ | 自相关 > 0.7 被隐藏，**正常** |
| 错误码 1001？ | IP 被封，去 ippure.com 解锁 |
| 提示 WebView2 错误？ | 手动安装 webview2 环境 |
| 平台并发已满？ | 关掉多余进程 |
| 4 个月免费到期？ | 买低价服务器（¥10/月） |
| 一阶跑多少线程？ | 1-2 线程足够 |
| 二阶段为什么比一阶段多？ | 套了 group 算子，命中率更高 |
| 工具能自动恢复任务吗？ | 能，登录后自动继续 |

---

## 三十四、回答用户问题时的输出规范

1. **判断场景**：是注册、跑分、提交流程，还是工具调优，还是 alpha 优化？
2. **场景 → 章节**：用本文档对应章节作为蓝本
3. **数据驱动**：所有指标/阈值都引用本文档速查表
4. **可执行**：给出具体配置参数、公式代码、操作按钮
5. **中文输出**：用户用中文则全中文

---

## 三十五、常见问答模板

### Q: 如何提高可提交率？

A: 五件套：①干净的字段 ②中性化 ③trade_when ④合理 decay/truncation ⑤多样性。具体阈值见第 15 章。

### Q: 哪个数据集最好？

A: news18 / news12 命中最高，但每天要换。6 天方案见第 7 章。

### Q: Sharpe 老是上不去？

A: ①加 group_neutralize ②换中性化粒度 ③加 trade_when ④换数据集。详见第 15 章。

### Q: 自相关过高怎么办？

A: ①换数据集 ②加 trade_when 改信号 ③套不同中性化。详见第 16 章。

### Q: 工具怎么配？

A: Stage 1 Max Run=1500，Fitness=0.6；Stage 2/3 Sharpe=1.0，Fitness=0.85。详见第 17 章。

### Q: 今天能提交几个？

A: 顾问前每天 1-2 个；顾问后每天最多 4 个（计入收入）。

### Q: 怎么提升收入？

A: 提升 VF（核心）、Sub-Universe Sharpe > 0.7、Turnover < 30%、Margin > 4 bps。详见第 5 章。

### Q: Workday 怎么填？

A: 见第 27 章要点。地址用英文、时间连续、身份三一致。

### Q: 问卷怎么答？

A: 见第 22 章详解。**用自己的语言**，理解后写，**严禁抄袭**。

### Q: 准顾问期间怎么提交？

A: 详见第 24 章。**2 天 1 个**，中间偏上质量，**SP 豁免的好 alpha 留着正式顾问后再交**。

### Q: 路由表是什么？

A: 见第 25 章。**数据域 + 中性化 + Universe 梯度**三件套，比公式复杂度更重要。

### Q: Vector 和 Matrix 数据区别？

A: 见第 9.2 节。Vector 是事件型（多值），需先 vec_avg/vec_sum 聚合。

### Q: 推荐奖励多少？

A: 每成功推荐一位 \$100（老强说版本）/ \$200（社区版本），无上限。详见第 29 章。

### Q: 季度奖金多少？

A: Gold \$100，Expert \$200-2000，Master \$2000-8000，Grandmaster \$8000-25000。详见 2.4。

---

## 三十六、关键链接

| 用途 | 链接 |
|---|---|
| BRAIN 官网 | platform.worldquantbrain.com |
| 官方文档 | /learn/documentation |
| Operators 文档 | /learn/documentation/create-alphas/operators |
| Neutralization 文档 | /learn/documentation/create-alphas/neutralization |
| 数据类型文档 | /learn/documentation/understanding-data/data |
| Vector 聚合 | /learn/documentation/vector-data |
| 官方论坛 | /learn/community |
| BRAIN TIPS 帖 | support.worldquantbrain.com/hc/en-us/community/posts/11807866133911 |
| 老强说教程 | alphadoc.biglongxia.com/guide/ |
| 老强说第 7 章 | alphadoc.biglongxia.com/guide/07-...问卷 |
| 老强说第 9 章 | alphadoc.biglongxia.com/guide/09-成为顾问 |
| CSDN 实战博客 | blog.csdn.net/scdifsn |
| CSDN 量化术语 | blog.csdn.net/Yan_ks/article/details/147701524 |
| CSDN 提 alpha 质量 | blog.csdn.net/Oo_Amy_oO/article/details/147725000 |
| CSDN 数据集 | blog.csdn.net/m0_73177400/article/details/148017247 |
| 韩国 velog | velog.io/@tae0_ |
| aiquantclaw 实战 | aiquantclaw.com/academy/insights |
| 开源工具 | github.com/xiegengcai/world-quant-brain |
| 推荐注册 | /referral/你的推荐码 |
| 中国官方邮箱 | mainlandchina@worldquantbrain.com |
| IP 解封 | ippure.com |

---

## 三十七、社区实战经验拓展（核心新增章节）

> 本章整合官方论坛 BRAIN TIPS、CSDN 实战博客、掘金、proginn、GitHub 开源工具、aiquantclaw 路由表方法论、韩国 IQC 比赛等 7 大社区资源的实战经验。

### 37.1 官方 BRAIN TIPS 论坛：6 种快速评估新数据集的方法

> 链接：<https://support.worldquantbrain.com/hc/en-us/community/posts/11807866133911>
> 标题："BRAIN TIPS: 6 ways to quickly evaluate a new dataset"

| # | 方法 | 核心思路 | 操作要点 |
|---|---|---|---|
| 1 | **Long/Short Count 评估** | 看字段在 universe 中的覆盖率 | 把字段二值化后 ts_mean 看日均覆盖率 |
| 2 | **样本内 vs 样本外（IS/OS）拆解** | IS Sharpe 高但 OS 拉胯 = 过拟合 | 比较 PnL 一致性 |
| 3 | **Sub-Universe 拆分测试** | 在 TOP3000 / TOP2000 / TOP1000 梯度跑 | 看信号在不同子池是否稳定 |
| 4 | **跨区域迁移测试** | 用 USA 数据集跑出 Sharpe，再在 ASI/EUR 验证 | 判断信号是否区域特异性 |
| 5 | **延迟（Delay）影响测试** | 试 Delay=0/1/2，看 Sharpe 衰减幅度 | Delay=0 显著好 = 可能未来函数 |
| 6 | **NaN 覆盖率回填测试** | 关闭/开启 NaN handling，看 Sharpe 变化 | 变化 > 0.1 需排查 NaN 来源 |

**核心结论**：
- 一个"好"的数据集 = 在 Sub-Universe 梯度上**信号稳定** + 跨区域**可迁移** + 延迟**鲁棒** + NaN 处理**一致**

### 37.2 CSDN 实战时间线汇总（5 个博主真实案例）

#### 案例 1：scdifsn（Python 兼职博主，2.8w 阅读）

> 链接：<https://blog.csdn.net/scdifsn/article/details/145904641>

**完整时间线**：
```
2025-01-06  开始用工具每天提交 1 个 Alpha
2025-01-10  5 天达到 10,000 分（每天 2000 分）  → 收到金牌邀请
2025-01-13  提交顾问问卷 + 参加官方新人培训
2025-02-18  累计提交 34 个 Alpha → 签约"有条件顾问"
2025-02-22  完成新顾问线上培训
2025-04-28  背调通过 → 正式顾问，填银行卡
2025-05-22  文章发布 → 收到第一笔顾问费（2.20-4.28 累计）
```

**关键数据**：
- 日均提交 1-2 个 Alpha
- Base Payment 1.5-2 美元/天（首月）
- 第二周最高单日近 7 美元（EUR D1 主题加成 ≥ 1.5 倍）
- 新人奖 100 美元
- 背调周期 2.5 个月（从有条件 → 正式顾问）

**他的核心建议**：
> 后续提高收入主要还是从两点入手：**一是优化代码，提高挖掘因子的效率**；**二是理解 Operators 和各类数据字段，发掘更多更好的 Alpha 模板**。

#### 案例 2：qiaoxingxing（掘金博主，3 个月做到日均 100 元）

> 链接：<https://juejin.cn/post/7474119575575298085>

**完整时间线**：
```
2024-09  B 站看到推荐信息，参加免费培训
2024-10  4 节线上课（每次 1 小时），需要 Python 基础
2024-11  月底成为顾问，开始使用官方提供的代码框架
2024-12  交够 100 个 Alpha → 进入官方研究小组
2025-01  参加「带你读论文」培训 → 借助 AI 读论文 + 写 Alpha → 优胜奖 500 元
2025-02  Value Factor 更新达到 0.9 → 日均收入增加十几倍
2025-Q3  评上 Grandmaster → 季度奖 8000 美元保底
```

**关键洞察**：
- **VF 值更新是收入翻倍的关键**（从 0.5 → 0.9 收入增十几倍）
- **官方研究小组**门槛是 100 个 Alpha
- **AI 辅助读论文**是高效产出的捷径

#### 案例 3：PearlOwl67（金融工程学生）

> 链接：<https://blog.csdn.net/PearlOwl67/article/details/154641045>

**关键要点**：
- 5 天达成 10,000 分
- 提交 34 个 Alpha 完成顾问认证
- 初期日均 1.5-2 美元
- 最高单日 7 美元（主题加成）
- 两个月后收到第一笔顾问费

**她的总结**：
> 提高收入主要还是从两点入手：一是优化代码，提高挖掘因子的效率；二是理解 Operators 和各类数据字段，发掘更多更好的 Alpha 模板。

#### 案例 4：Yan_ks（量化学习笔记，3.8k 阅读）

> 链接：<https://blog.csdn.net/Yan_ks/article/details/147701524>

**核心术语解释**（比官方文档更通俗）：
- Base Payment = 1-60 USD/Day（alphas）+ 1-60 USD/Day（super alphas）= 最高 120 USD/Day
- Quarterly Payment 决定因素：Weight + OS 表现
- Theme Calendar 加成：Dataset Themes / Region Themes / Super Alpha Themes

#### 案例 5：weixin_56202583（WorldQuant 综述）

> 链接：<https://blog.csdn.net/weixin_56202583/article/details/150611896>

**3 大误区澄清**：
1. ❌ 「必须金融背景」 → ✅ 平台官方低代码（Fast Expression）+ Python/Rust API
2. ❌ 「需要昂贵软件」 → ✅ BRAIN 平台自带回测系统
3. ❌ 「只能赚零花钱」 → ✅ 兼职研究者月均 3000-5000 元，大佬年入 10w+

**用户场景案例**：
- **学生/新手**：免费学习 + 实习机会 + 竞赛奖金
- **兼职研究者**：日均 2-3 小时，月均 3000-5000 元
- **金融机构**：批量验证策略 + 招聘优秀量化人才

### 37.3 韩国 IQC 比赛（2025 完整赛程与奖金）

> 链接：<https://brain-kr.com/>

**2025 IQC 时间表**：
| 阶段 | 时间 | 奖励 |
|---|---|---|
| 报名组队 | 3/4 - 5/14 | — |
| 预选赛 | 3/18 - 5/19 | — |
| 国家代表赛 | 5/27 - 7/中 | 国内 1 等 \$3,000 / 2 等 \$2,000 / 3 等 \$1,000 |
| 全球决赛 | 7/22 - 9/中 | 全球 1 等 \$20,000 / 2 等 \$12,000 / 3 等 \$8,000 |

**总奖池 \$10 万**，国内线下国家代表赛 + 新加坡全球决赛。

**韩国版官方课程（免费，5-6 月）**：
- 3/19：股价/交易量数据
- 4/2：In-Sample Test 理解与拟合
- 4/9：Delay 对 alpha 的影响
- 4/30：避免过拟合
- 5/7：新闻和 SNS 数据
- 5/14：期权/向量/关系数据
- 5/21：中性化改善表现
- 5/28：Alpha 研究深化
- 6/25：论文驱动的 alpha 研究

**韩国社区入口**：<https://qr.wqbrain.com/krforum>

### 37.4 掘金 + 博客园 实战经验

#### qiaoxingxing 的「学习氛围」感悟（掘金）

> 链接：<https://juejin.cn/post/7474119575575298085>

**worldquant 三大特色**：
1. **官方中文论坛** — 教学贴 + 模板 + 数据集 + 经验分享，每天更新
2. **官方研究小组微信群** — 每天几百条群消息，高质量讨论
3. **双周会** — 4 个奖项（100-300 美元/项），保底 8000 美元大佬分享

**他的下步计划**：
- 补基础知识
- 重构代码
- 完善自动化流程
- 进一步提升效率

### 37.5 aiquantclaw.com 路由表方法论（深度）

> 链接：<https://www.aiquantclaw.com/academy/insights/worldquant-brain-needs-datafield-neutralization-and-universe-routing>

**核心观点**：
> **Brain 公式成败，常常先由路由关系决定，而不是由长度决定。**

**为什么路由表比写公式更重要**：
- 同一想法，到底用 matrix 还是先从 vector 聚合？
- 到底用 subindustry neutralization 还是 industry neutralization？
- 到底在窄 Universe 追求纯度，还是在宽 Universe 换稳定性？
- 这些决定往往比多加两个算子更重要

**三大路由维度**：

| 路由维度 | 决定内容 | 影响 |
|---|---|---|
| **数据域** | 比较什么（财务 / 价格 / 新闻 / 向量事件） | 噪声结构 + 更新节奏 |
| **中性化** | 比较的相对坐标（同行业 / 跨行业 / 风格） | 信号是风格暴露还是局部选股 |
| **Universe 梯度** | 比较的资产池（TOP500 / TOP2000 / TOP3000） | 信号纯度 vs 稳定性 |

**实战工作流（路由卡模板）**：

```
┌─────────────────────────────────────────────┐
│              Alpha 想法路由卡                  │
├─────────────────────────────────────────────┤
│ 1. 原始字段：                                 │
│    - 数据集：fundamental6                     │
│    - 字段类型：matrix / vector                │
│    - 字段名：xxx                              │
│                                              │
│ 2. 预处理：                                   │
│    - vec 聚合方式：vec_avg / vec_sum          │
│    - ts_backfill：120 天                      │
│    - winsorize：std=4                         │
│                                              │
│ 3. 中性化层级：                                │
│    - 目标：subindustry                       │
│    - 测试备选：industry / market / none       │
│                                              │
│ 4. Universe 梯度：                            │
│    - 起点：TOP3000                           │
│    - 备选：TOP2000 / TOP1000                  │
│                                              │
│ 5. 决策：先跑 TOP3000 + subindustry，          │
│    Sharpe > 1.5 再扩 universe                 │
└─────────────────────────────────────────────┘
```

**关键结论**：
- 数据域定义**比较对象**
- 中性化定义**比较坐标**
- Universe 梯度定义**比较场景**
- **先写路由表再扩公式**，能显著降低无效试错

### 37.6 GitHub 开源工具：xiegengcai/world-quant-brain

> 链接：<https://github.com/xiegengcai/world-quant-brain>
> DeepWiki：<https://deepwiki.com/xiegengcai/world-quant-brain>

**系统架构**：
```
WQB API Client → Alpha Generation (1st/2nd/3rd order) 
  → Batch Simulation → Self-Correlation Analysis 
  → Robustness Testing → Automated Submission
```

**核心模块**：
- **Generator**：使用 factory.py 转换 dataset fields 为 FASTEXPR 字符串
- **Simulator**：批量发送 + 轮询结果，处理限流
- **AlphaMapper**：本地 SQLite 数据库存储 alpha_id + location_id
- **Checker**：本地 + 服务端双重质量验证
- **SuperAlpha**：特殊生成路径，穷举时序算子 × 窗口组合

**SuperAlpha 框架核心配置**：
```python
# SuperAlpha.py 中的标准配置
combo_ops = [
    'ts_rank',     # 时间序列排名
    'ts_zscore',   # 时间序列标准分
    'ts_arg_min',  # 时间序列最小值索引
    'ts_delta',    # 时间序列差分
    'ts_std_dev',  # 时间序列标准差
    'ts_mean',     # 时间序列均值
]
days = [5, 22, 66, 120, 240]  # 标准回溯窗口
```

**Field Preprocessing 模板**：
```python
def process_datafields(field):
    # Vector 字段先用 vec_avg/vec_sum 转 scalar
    if field.type == 'VECTOR':
        field = vec_avg(field)
    # 标准预处理：ts_backfill + winsorize
    return winsorize(ts_backfill(field, 120), std=4)
```

**Factory 体系**：

| Factory 函数 | 逻辑 | 用途 |
|---|---|---|
| `get_group_second_order_factory` | group_ops 应用到 first-order alphas | 行业中性化 |
| `get_ts_second_order_factory` | ts_ops 应用到 first-order alphas | 时序平滑 |
| `ts_group_factory` | group-transformed field 套上 ts 操作 | 行业平均 + 时序 |
| `group_ts_factory` | ts-transformed field 套上 group 操作 | 时序 + 行业中性 |
| `trade_when_factory` | 条件入场（第三阶） | 触发式策略 |

**Common `open_events`（trade_when 条件模板）**：
```python
# 成交量模式
trade_when(ts_arg_max(volume, 5) == 0, signal, -1)
# 量价相关性
trade_when(ts_corr(close, volume, 20) > 0, signal, 0)
# 价格突破
trade_when(close > ts_max(close, 60), signal, 0)
```

### 37.7 GitHub 开源工具：zhutoutoutousan/worldquant-miner（Alpha Generator）

> 链接：<https://github.com/zhutoutoutousan/worldquant-miner>

**核心功能**：
1. **Alpha Generator**：调用 BRAIN API 自动生成 alpha 想法（用 Moonshot API 创意）
2. **Promising Alpha Miner**：优化有前景的 alpha，系统测试参数变化
3. **Authentication**：HTTPBasicAuth 认证
4. **Data Fields Fetch**：调用 `/data-fields` 接口

**典型 API 调用**：
```python
# 认证
self.sess.post('https://api.worldquantbrain.com/authentication')

# 获取数据字段
params = {
    'dataset.id': 'fundamental6',
    'delay': 1,
    'instrumentType': 'EQUITY',
    'limit': 20,
    'offset': 0,
    'region': 'USA',
    'universe': 'TOP3000'
}
response = self.sess.get(
    'https://api.worldquantbrain.com/data-fields',
    params=params
)
```

### 37.8 性价比超高的小王：自动 SuperAlpha 工具（proginn）

> 链接：<https://www.proginn.com/w/1576270>

**项目特点**：
- 自动寻找 super alpha（普通用户难度极高）
- 多线程 + 网络重试 + 自动染色 + 相关性自检
- 触发限流（429）自动读取 Retry-After 头并等待
- 残疾人也能稳定提交 super alpha

**技术栈**：
- Python 3.X + requests + concurrent.futures + collections.deque + random + colorama + json
- 4 层架构：
  - **BrainAPI** 封装所有 WQB API 调用
  - **EvolutionManager** 进化算法（50% 探索 + 50% 精英变异）
  - **WorkerTask** 多线程工作单元
  - **主程序** 启动 + 信号控制

**30 个 Selection 模板**（5 大流派）：
1. **强力去相关**
2. **统计学中性化猎手**
3. **分段换手率狙击**
4. **反拥挤和数据源隔离**
5. **质量优先与混合策略**

**5 个可变参数**（组合出 403,200 种配置）：
- 相关性上限
- 相关性下限
- 换手率上限
- Fitness 门槛
- Decay 值

**实战踩坑（来自该工具作者）**：
1. ⚠️ **SUPER Alpha 回测慢 3-5 倍** — 等待循环从 24 次加到 120 次（最多等 10 分钟）
2. ⚠️ **相关性数据延迟** — 立即查常拿到默认值 1.0，误判为超标。改用 5 次重试
3. ⚠️ **多线程 429 限流** — 读取 `Retry-After` 头，睡一会儿递归重试
4. ⚠️ **Session 超时** — WQB 的 Session 3 小时过期，所有 API 调用前检查 Session 年龄

**进化策略核心**：
- 50% 随机探索 + 50% 精英变异
- 变异概率精心设计，**不是全量替换而是局部改良**
- 精英池最多 50 个配置

### 37.9 WorldQuant Brain 平台核心机制（wenku.csdn.net 深度文）

> 链接：<https://wenku.csdn.net/column/6f1k9qh4cy>

**8 大黄金技巧**（精炼版）：

1. **从可证伪假设开始** — 不是写公式，是构建可验证的投资假设
2. **数据域匹配** — 价格类用 ts_*，财务类用 group_*，新闻类用 vec_avg
3. **预处理标准化** — `winsorize(ts_backfill(field, 120), std=4)` 是基础
4. **中性化由粗到细** — 起点 MARKET，向上 INDUSTRY/SUBINDUSTRY
5. **Universe 梯度验证** — TOP3000 跑出 Sharpe，再测 TOP2000/TOP1000
6. **延迟鲁棒性** — Delay=0 显著好于 Delay=1 → 检查未来函数
7. **相关性去重** — 提交前查 Self Correlation > 0.7 需改思路
8. **OS 验证** — IS Sharpe 1.8 + OS Sharpe 1.3 = 真正可用

### 37.10 ⚠️ 准顾问期提交策略的反例教训

**来自 scdifsn 的真实教训**：
- 1 月 6 日开始每天交 1 个，1 月 10 日就达到 10,000 分
- ⚠️ 这导致后面**交了 34 个后才等到签约**（因为前期没交满 15 个）
- **官方建议**：交满 15 个 Alpha 可优先进行顾问问卷审核

**正确节奏**：
```
Day 1-7  : 跑分（每天 2000 分封顶，1-2 个 Alpha 足够）
Day 8-10 : 多交一些质量普通的 Alpha（凑够 15 个）
Day 10+  : 等待金牌 + Workday + 问卷
```

**避免的坑**：
- ❌ 一开始就交 SP 级的 → 占用自相关池子，影响正式顾问后收入
- ❌ 每天都交同样思路的 → 自相关性堆积
- ❌ 准顾问期突击交太高质量 → VF 值被锁定在低水平

### 37.11 5 种官方收益的细分对比

| 收入类型 | 频率 | 金额范围 | 决定因素 | 关键期 |
|---|---|---|---|---|
| **Base Payment** | 每 2 个月 | \$1-60/天 | VF + 提交数 + 质量 | 持续 |
| **Quarterly Payment** | 每季度 | \$100-25,000 | Weight + OS 表现 | 季度末 |
| **比赛奖金** | 不定期 | 视赛事（IQC 总池 \$10w） | 排名 | 比赛期 |
| **推荐费** | 每成功一人 | \$100-200 | 对方成为顾问 | 长期 |
| **新人奖** | 一次性 | \$100 | 注册时填推荐码 + 10 天有提交 + 1 个月顾问 | 注册 30 天内 |

**推荐奖励的条件（详细版）**：
- 被推荐用户注册时填你的 User Alias
- 被推荐用户在 10 个不同自然日提交 Alpha
- 被推荐用户保持顾问身份 1 个月以上
- 推荐人获得 \$100-200/人（无上限）

### 37.12 VF (Value Factor) 提升路径（qiaoxingxing 实证）

**VF 演变曲线**（来自掘金博主）：
```
0.5 (初始)  →  0.7 (3 个月)  →  0.9 (5 个月)  →  Grandmaster
  ↑              ↑                ↑               ↑
基础收入 2x  收入 4x        收入 10x+        季度奖 8000 USD
```

**VF 提升关键动作**：
1. **持续学习** — 听完官方课程 + 读论文
2. **代码重构** — 提升挖掘效率，跑更多 alpha
3. **加入研究小组** — 100 个 Alpha 门槛
4. **主题日历对齐** — 跟踪 Dataset/Region/Super Alpha Themes
5. **避开低质量提交** — 别为了数量交垃圾 alpha

### 37.13 总结：社区资源导航表

| 资源类型 | 链接 | 用途 |
|---|---|---|
| **官方文档** | platform.worldquantbrain.com/learn/documentation | 最权威 |
| **官方论坛 BRAIN TIPS** | support.worldquantbrain.com/hc/en-us/community/posts/11807866133911 | 6 种评估方法 |
| **老强说教程（中文）** | alphadoc.biglongxia.com/guide/ | 11 章系统教程 |
| **老强说第 7 章** | alphadoc.biglongxia.com/guide/07-... | 基础测试问卷 |
| **老强说第 9 章** | alphadoc.biglongxia.com/guide/09-成为顾问 | 成为顾问流程 |
| **CSDN 实战案例** | blog.csdn.net/scdifsn | scdifsn 时间线 |
| **CSDN 量化术语** | blog.csdn.net/Yan_ks | 3.8k 阅读 |
| **掘金** | juejin.cn/post/7474119575575298085 | 3 个月做到日均 100 元 |
| **velog（韩国）** | velog.io/@tae0_ | 韩国社区实战 |
| **韩国 IQC** | brain-kr.com | 2025 比赛 + 课程 |
| **韩国论坛** | qr.wqbrain.com/krforum | 韩语自由讨论 |
| **官方 VRC** | worldquantvrc.com | 顾问申请 + 等级 |
| **aiquantclaw** | aiquantclaw.com/academy/insights | 路由表方法论 |
| **GitHub xiegengcai** | github.com/xiegengcai/world-quant-brain | SuperAlpha 框架 |
| **GitHub zhutoutoutousan** | github.com/zhutoutoutousan/worldquant-miner | Alpha Generator |
| **GitHub DeepWiki** | deepwiki.com/xiegengcai/world-quant-brain | 详细文档 |
| **proginn（小王）** | proginn.com/w/1576270 | 自动 SuperAlpha 工具 |
| **wenku.csdn.net** | wenku.csdn.net/column/6f1k9qh4cy | 8 大黄金技巧 |
| **gentlecactus（个人博客）** | gentlecactus.top/archives/132 | 提交硬性标准 |


## 三十八、★ 老强说 Alpha 辅助工具 v1.0.5 操作精通（基于 EXE UI 详解）

> ⚠️ **诚实声明**：EXE 是二进制文件，无法反编译。本章基于**v1.0.5 安装版 UI 截图** + **老强说公开教程** + **BRAIN 平台官方规则**推导出的可操作手册。如需精确实现，建议用 IDA/Ghidra 反汇编或直接联系老强获取接口文档。

### 38.1 工具版本识别

| 字段 | 取值 |
|---|---|
| 安装包 | `lqs-alpha_win_1.0.5_x64-setup 3.exe` |
| 可执行 | `lqs-wqbrain-tool.exe` |
| 平台 | Windows x64 |
| 运行依赖 | WebView2（Win10 1803+ 自带；Win7 需手动装） |
| 工具名 | 老强说 Alpha 辅助工具 |
| 跑分特性 | 内置三阶流水线 + 多线程 + 自动染色 + Task Pool 调度 |

### 38.2 UI 全景图（基于截图逐元素解读）

```
┌─────────────────────────────────────────────────────────────┐
│ 🐉 老强说Alpha辅助工具                            ─ □ ✕  │
├─────────────────────────────────────────────────────────────┤
│  ▲ 从二阶段的结果中挑选种子（进入本阶段的门槛）                │
│                                                             │
│  Sharpe 阈值  ?                                             │
│  [ 1.1 ............................................. ]    │
│                                                             │
│  Fitness 阈值  ?                                            │
│  [ 0.85 ............................................ ]    │
│                                                             │
│  最少做多数  ?                                               │
│  [ 100 ▼ ]                                                  │
│                                                             │
│  最少做空数  ?                                               │
│  [ 100 ............................................. ]    │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  ▶  添加任务                                          │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                             │
│  ⊞ Task Pool                                                │
│  ┌────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┐    │
│  │总数│排队中│回测中│ 进度 │ 失败 │ 达标 │达标率│      │    │
│  │4000│ 1970 │  1   │57/4000│ 33  │  3   │12.5% │      │    │
│  └────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┘    │
│  ┌────────────────────────────────┬────────────────────┐   │
│  │⚠ step3-run-1780327327712859800 │⚙ step3-run-17803... │   │
│  │               [已停止]         │         [运行中]    │   │
│  └────────────────────────────────┴────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### 38.3 四大核心参数（Stage 3 入口筛选器）

> 这 4 个参数控制「二阶输出 → 三阶输入」的门槛。

| 参数 | 截图默认值 | 含义 | 推荐区间 | 调高后果 | 调低后果 |
|---|---|---|---|---|---|
| **Sharpe 阈值** | 1.1 | 二阶通过此阈值才进三阶 | 1.0 ~ 1.25 | 三阶种子更稀，浪费平台并发 | 大量低质种子涌入，三阶回测变慢 |
| **Fitness 阈值** | 0.85 | 综合质量过滤 | 0.75 ~ 1.0 | 跑出 SP 级概率高 | Good/Average 涌入 |
| **最少做多数** | 100 | 信号必须至少覆盖 100 只多头股 | 80 ~ 150 | 强制剔除冷门股票，Sharpe 更稳 | 允许小众 alpha，OS 风险高 |
| **最少做空数** | 100 | 同上，空头端 | 80 ~ 150 | 同上 | 同上 |

**实战调参建议**（按当前 12.5% 达标率反推）：

```
当前：Sharpe 1.1 / Fitness 0.85 / Long 100 / Short 100
结果：4000 总数 → 3 达标（12.5%）

方案 A（保守，提高质量）：
  Sharpe 1.2 / Fitness 0.9 / Long 120 / Short 120
  预计：达标率 → 8% 左右，但每个 alpha 质量更高

方案 B（激进，提高数量）：
  Sharpe 1.05 / Fitness 0.8 / Long 90 / Short 90
  预计：达标率 → 18% 左右，但平均质量下降

方案 C（稳进，金牌冲刺期推荐）：
  Sharpe 1.15 / Fitness 0.85 / Long 100 / Short 100
  预计：达标率 → 14% 左右，平衡
```

### 38.4 Task Pool 7 大指标精读

| 指标 | 截图值 | 健康范围 | 异常诊断 |
|---|---|---|---|
| **总数** | 4000 | 任意 | 配置好的总任务数 |
| **排队中** | 1970 | < 总数 × 60% | 49% 健康；> 70% 平台并发拥挤 |
| **回测中** | 1 | 1 ~ 5 | 平台实际并发槽位，通常 1-3 |
| **进度** | 57/4000 (1.4%) | 任务刚启动 | 看增长速率判断健康 |
| **失败** | 33 | < 总数 × 5% | 33/4000 = 0.8% 极健康 |
| **达标** | 3 | 持续增长 | 看增长率 |
| **达标率** | 12.5% | 5% ~ 30% | 12.5% 在合理偏低区 |

**从截图数据反推当前状态**：
- 平台并发极低（回测中 = 1）→ 可能是晚间跑批期
- 排队积压严重（1970/4000 = 49%）→ 平台服务端繁忙
- 失败率 0.8% 极低 → 工具配置正确
- 达标率 12.5% 偏低 → 适合调高阈值筛选（方案 C）

### 38.5 Task Pool 任务卡片识别

| 状态 | 颜色 | 含义 | 操作 |
|---|---|---|---|
| **运行中** | 黄色边框 | 正在跑 | 不可删除，等待完成 |
| **已停止** | 红色边框 | 用户中断或失败 | 可点击查看日志/重启 |
| **排队中** | 蓝色边框 | 等待平台并发 | 等待即可 |
| **完成** | 绿色边框 | 全部跑完 | 可看结果列表 |

**任务 ID 含义**（如 `step3-run-1780327327712859800`）：
- `step3-run-` 前缀 → 第三阶段任务
- `1780327327712859800` → Unix 毫秒时间戳 = `2026-06-02 00:42:07 UTC+8`
- 同理 step1-run、step2-run 是一/二阶

### 38.6 三阶流水线在工具中的调度流程

```
用户操作：
  1. 配置 Stage 1（数据集/中性化/Max Run）
  2. 点击「▶ 添加任务」
  3. Stage 1 完成 → 自动产出种子
  4. 配置 Stage 3 入口（4 个阈值：Sharpe/Fitness/Long/Short）
  5. Stage 3 自动从 Stage 2 产出中筛种子
  6. Stage 3 完成后 → Alphas 标签查看可提交列表
  7. 染色（绿/黄/红）+ 一键提交

工具内部：
  Task Pool 调度 → API 调用 → 染色 → 自相关检查 → 提交建议
```

### 38.7 工具常见功能区（推测，基于公开教程）

| Tab | 功能 | 关键操作 |
|---|---|---|
| **任务配置** | 数据集/区域/池子/中性化 | 选择 + 阈值 |
| **Alphas** | 产出列表 | 按 Sharpe 排序 |
| **可提交** | 自动染色结果 | 一键提交 |
| **设置** | 账号/并发/线程 | 1-2 线程推荐 |
| **日志** | 任务运行日志 | 排查失败原因 |

### 38.8 与官方平台的 6 大协同点

| 工具操作 | 平台对应 | 注意 |
|---|---|---|
| 配置数据集 | Settings → Dataset | 必须用官方支持的数据集 ID（如 fundamental6、news18） |
| 配置中性化 | Settings → Neutralization | 选 MARKET/INDUSTRY/SUBINDUSTRY |
| 配置延迟 | Settings → Delay | D0/D1，新手用 D1 |
| 配置池子 | Settings → Universe | TOP3000/2000/1000 |
| 配置 Max Run | Settings → Max Trade | 推荐 1500（省铜牌） |
| 配置 Decay/Truncation | Settings → Decay/Truncation | Decay 5-15，Truncation 0.08-0.1 |

### 38.9 工具调参的"3 个不要"

1. ❌ **不要频繁改阈值** — 任务跑起来再改无效，要等该批次结束
2. ❌ **不要开超过 3 线程** — BRAIN 平台限流，多线程反而触发 429
3. ❌ **不要关工具再开** — 排队中的任务会丢失，需要重新添加

### 38.10 工具配置黄金模板（v1.0.5 推荐）

#### Stage 1 模板
```
数据集：news18（Sharpe 最高）/ fundamental6（量大）
区域：USA
延迟：1
池子：TOP3000
中性化：Subindustry
Max Run：1500
线程：2
```

#### Stage 2 模板
```
继承 Stage 1 设置
新增：group_neutralize / group_rank 二阶算子
Sharpe 阈值：1.0
Fitness 阈值：0.75
```

#### Stage 3 入口（4 个阈值）— 对应截图
```
Sharpe 阈值：1.1（可调到 1.15 ~ 1.2 提质）
Fitness 阈值：0.85（可调到 0.9）
最少做多数：100
最少做空数：100
```

### 38.11 工具报错与排错

| 现象 | 可能原因 | 解决 |
|---|---|---|
| 工具打不开 | WebView2 缺失 | 装 Microsoft Edge WebView2 Runtime |
| 登录失败 | 密码含空格/大小写 | 检查账号 |
| 任务一直排队 | 平台并发已满 | 减少线程/换时段（北京时间 12-14 点为结算期，避开） |
| 错误码 1001 | IP 被封 | 去 ippure.com 解锁 |
| 错误码 429 | 触发限流 | 工具自动重试，无需操作 |
| 加载字段失败 | 官网 504 | 等 5-10 分钟重试 |
| 任务消失 | 自相关 > 0.7 被隐藏 | 正常，**不要慌** |
| 工具卡死 | Session 超时（3 小时） | 重新登录 |

### 38.12 工具每日使用节奏（参考 SOP）

```
08:00  开机，打开工具，登录账号
08:10  检查昨日 Task Pool，处理失败任务
08:30  启动 Stage 1（按 6 天方案选数据集）
10:00  Stage 1 完成 → 启动 Stage 2/3
12:00  ⚠️ 平台结算期（北京时间），工具自动暂停
14:00  结算完成，工具自动恢复
17:00  Stage 3 完成 → Alphas 标签看结果
18:00  染色 + 提交当天最优 alpha（每天最多 4 个）
22:00  关电脑，工具继续在云服务器跑
```

### 38.13 工具 vs 手动操作对比

| 维度 | 工具 | 手动 |
|---|---|---|
| **效率** | 24h 跑 1000+ alpha | 每天 5-10 个 |
| **成本** | 工具费 + 云服务器 | 时间成本极高 |
| **质量** | 中等 | 顶尖（精细调参） |
| **适合** | 冲量、金牌冲刺 | 顾问后精雕 |
| **风险** | 自相关堆积（需换数据集） | 无 |

### 38.14 v1.0.5 工具的关键更新点（推测）

| 版本特性 | 用途 |
|---|---|
| 多任务并发 | 同时跑多个数据集/中性化组合 |
| 自动染色 | 绿色 = 可提交，红色 = 不可提交 |
| 自相关预检 | 提交前自动查 Self-Correlation |
| Task Pool 调度 | 失败自动重试，排队管理 |
| 4 维阈值筛选 | Stage 3 入口的 Sharpe/Fitness/Long/Short |

### 38.15 精通工具的 5 个里程碑

| 等级 | 描述 | 标志 |
|---|---|---|
| **L1 新手** | 能配置基础 Stage 1 | 1 周内跑出第 1 个可提交 alpha |
| **L2 入门** | 会用三阶流水线 | 1 个月内达到 10,000 分 |
| **L3 熟练** | 能调 4 维阈值 | 达标率稳定 > 15% |
| **L4 高手** | 理解工具与平台协同 | 月收入 $300+ |
| **L5 大师** | 自定义算子链 | 加入官方研究小组（100 个 alpha） |

### 38.16 与本 skill 其他章节的引用

| 工具问题 | 跳转章节 |
|---|---|
| 阈值怎么定 | 第 15 章 指标调优 |
| 数据集怎么选 | 第 9 章 数据集选择 |
| 自相关高 | 第 16 章 降低自相关性 |
| 整体工作流 | 第 18 章 每日 SOP |
| 出错排查 | 第 19 章 问题排查清单 |
| 官方规则 | 第 4 章 提交标准 |
| 顾问策略 | 第 23 章 成为顾问流程 |

### 38.17 工具使用红线（必看）

1. ⚠️ **服务器必须国内直连** — 开 VPN 会触发 IP 封禁
2. ⚠️ **电源选项设为「从不」** — 服务器休眠 = 任务中断
3. ⚠️ **不要 24h 不关工具** — 每周重启 1 次清缓存
4. ⚠️ **不要共享账号** — 平台会检测多 IP 登录
5. ⚠️ **不要在社群外讨论工具** — alphadoc 红线

### 38.18 工具升级到 v1.0.5+ 的检查清单

- [ ] 备份 Task Pool 历史任务
- [ ] 导出账号配置
- [ ] 检查 WebView2 是否最新
- [ ] 清理本地缓存（一般在 `%APPDATA%/lqs-alpha/`）
- [ ] 重启工具并重新登录
- [ ] 跑 1 个测试任务验证

---

## 三十九、★ 老强说 Alpha 工具的「参数-指标」关系图（量化调参决策树）

> 本章将工具的 4 大参数（第 38 章）与 alpha 指标体系（第 15 章）做交叉映射。

### 39.1 参数调高的连锁影响

```
Sharpe 阈值 ↑ 1.1 → 1.2
   ↓
二阶种子数 ↓（约 30-50% 减少）
   ↓
三阶回测任务 ↓（平台压力 ↓）
   ↓
达标率 ↑（质量过滤更严）
   ↓
单 alpha 质量 ↑（Sharpe/Fitness 更高）
   ↓
提交成功率 ↑ / 自相关 ↓
   ↓
月收入 ↑（顾问后）
```

### 39.2 参数调低的连锁影响

```
Fitness 阈值 ↓ 0.85 → 0.75
   ↓
二阶种子数 ↑（约 2-3 倍）
   ↓
三阶回测任务 ↑（平台压力 ↑，可能 429）
   ↓
达标率 ↓（垃圾种子涌入）
   ↓
单 alpha 质量 ↓
   ↓
提交成功率 ↓ / 自相关 ↑（容易与历史冲突）
   ↓
收益下降风险
```

### 39.3 4 参数的优先级

| 优先级 | 参数 | 原因 |
|---|---|---|
| 1️⃣ | **Sharpe 阈值** | 直接决定可提交率 |
| 2️⃣ | **最少做多/空数** | 决定覆盖稳定性 |
| 3️⃣ | **Fitness 阈值** | 综合过滤（与 Sharpe 有重叠） |
| 4️⃣ | **Fitness 阈值** | 在 Sharpe 已经筛过后作用减弱 |

**实战建议**：先固定 Sharpe，调 Long/Short，最后微调 Fitness。

### 39.4 何时应该调高参数

| 信号 | 行动 |
|---|---|
| Task Pool 排队 > 70% | 调高 Sharpe / Fitness 减少任务量 |
| 自相关冲突频繁 | 调高 Long/Short 减少相似信号 |
| 提交后 Change < 0 | 调高 Sharpe 提升质量 |
| 想冲 SP 级 | 调高所有参数到上限 |
| 月底结算前 | 保持高质量（高 Sharpe 阈值） |

### 39.5 何时应该调低参数

| 信号 | 行动 |
|---|---|
| 总数太少 (< 500) | 调低 Sharpe 到 0.9 / Fitness 到 0.6 |
| 离 10,000 分还远 | 调低所有参数冲量 |
| 刚换数据集 | 调低 Sharpe 试探 |
| Sub-Universe 不通过 | 调低 Sharpe + 提高 Long/Short |

### 39.6 量化调参公式（建议）

```
理想 Sharpe 阈值 = 提交标准（1.25）× 0.85 - 0.05
                 = 1.25 × 0.85 - 0.05
                 = 1.01
建议值：1.0 ~ 1.1

理想 Fitness 阈值 = Sharpe × 0.7
                  = 1.0 × 0.7
                  = 0.7
建议值：0.7 ~ 0.85

理想 Long/Short = 池子规模 × 5%
                 = TOP3000 × 5%
                 = 150
建议值：100 ~ 150
```

### 39.7 调参记录表（建议每天填）

```
日期：________
Stage 3 入口：Sharpe=___ / Fitness=___ / Long=___ / Short=___
总任务数：___
达标数：___
达标率：___%
最佳 Sharpe：___
最佳 Fitness：___
最优数据集：___
最优中性化：___
明日计划：_________________________________
```

---

## 四十、★ 老强说 Alpha 工具的「任务-时间」日历

> 把工具每天的跑分节奏画成日历形式，对应 38.12 SOP。

### 40.1 北京时间日历

| 时段 | 工具状态 | 平台状态 | 用户操作 |
|---|---|---|---|
| 00:00 - 06:00 | 🟢 全力跑 | 🟢 低峰 | 睡觉 |
| 06:00 - 08:00 | 🟢 继续跑 | 🟡 渐忙 | 起床看 Task Pool |
| 08:00 - 10:00 | 🟢 启动新任务 | 🟢 健康 | 配置 Stage 1 |
| 10:00 - 12:00 | 🟡 排队累积 | 🟡 渐忙 | 准备结算期 |
| 12:00 - 14:00 | 🟡 **平台结算** | 🔴 **暂停** | **不要操作** |
| 14:00 - 17:00 | 🟢 自动恢复 | 🟢 恢复 | 检查产出 |
| 17:00 - 20:00 | 🟢 跑 Stage 3 | 🟢 健康 | 染色 + 提交 |
| 20:00 - 22:00 | 🟡 平台晚高峰 | 🟡 渐忙 | 提交高峰 |
| 22:00 - 24:00 | 🟢 夜间低峰 | 🟢 低峰 | 关电脑，工具继续跑 |

### 40.2 ⚠️ 关键时点

| 时点 | 事件 | 操作 |
|---|---|---|
| 12:00 | 北京时间积分结算 | 不操作 |
| 14:00 | 平台服务恢复 | 检查工具自动续跑 |
| 24:00 | 平台提交数清零 | 第二天新额度 |

### 40.3 周末/节假日

- 平台**正常运营**
- 流量**略低**（适合跑大任务）
- 顾问工作**照常**计费

---

> 最后更新：2026-06-01
> 版本：V5（新增第 38 章工具精通 + 第 39 章参数决策树 + 第 40 章时间日历，共 40 章，约 2400 行）
> 整合内容：v1.0.5 EXE UI 详解 + 4 维阈值调参 + Task Pool 解读 + 工具 vs 手动对比 + 每日 SOP
> 维护：随工具版本更新
