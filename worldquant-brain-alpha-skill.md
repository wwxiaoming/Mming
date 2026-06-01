# WorldQuant BRAIN Alpha 挖掘专家技能 V2

> 来源整合：
> 1. 官方 BRAIN 平台文档（platform.worldquantbrain.com）
> 2. 老强说 Alpha 官方教程（alphadoc.biglongxia.com）
> 3. CSDN/官方论坛实战经验
> 4. 自动化工具（老强说 Alpha 辅助工具）使用心得
>
> 适用：从零基础 → 成为签约顾问 → 提升收入 全流程

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

### 2.3 收入结构

| 收入类型 | 金额范围 | 频率 | 说明 |
|---|---|---|---|
| 基础报酬（普通） | \$1 - 60 / 天 | 每日 | 每天前 4 个 Alpha 计入 |
| 基础报酬（超级） | \$1 - 60 / 天 | 每日 | 交满 100 个后解锁，与普通叠加 |
| 季度奖金 | \$100 - 25,000 | 每季度 | 与等级强相关 |
| 推荐奖励 | \$100 / 人 | 每次成功 | 无上限 |

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
| **Sub-Universe** | Sharpe 通过 | 缩小池子仍能跑 |

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

| VF 范围 | 收入水平 |
|---|---|
| 0.95+ | 非常高（顶尖） |
| 0.85 - 0.95 | 较高 |
| 0.7 - 0.85 | 良好 |
| 0.5 - 0.7 | 较低（积累期） |

- 初始 VF = 0.5
- 每月更新，基于过去 3 个月所有 alpha 表现
- **VF 0.95 vs 0.5，收入差距数倍甚至 10 倍+**

### 5.5 Performance Comparison (Change)

| Change | 决策 |
|---|---|
| > 0 | ✅ 提交（对组合有正向贡献） |
| < 0 | ❌ 不要提交（即使 Sharpe 高，也会拖累整体） |

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
- **收入**：前 4 个算 Base Payment，普通 +60 美金/天，超级解锁后 +60 美金/天

---

## 九、数据集选择（按出高质量 alpha 概率排序）

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

**轮换策略**：每天用 1 个数据集（见第七天表），避免同质化导致自相关。

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

### 10.3 实操建议

- 用同一表达式分别测试不同中性化
- 选 Sharpe + Fitness 综合最优的
- 没有"万能"中性化方式

### 10.4 公式 vs Setting

```python
group_neutralize(-ts_returns(close, 5), industry)
# 等价于在 Setting 中选 industry
```

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
```

### 11.2 截面算子

```python
rank(x)                  # 截面百分位排名
zscore(x)                # 截面标准化
quantile(x, n)           # 分桶
normalize(x)             # 归一化
```

### 11.3 组算子 group_*

```python
group_neutralize(x, group)  # 组内中性化
group_rank(x, group)        # 组内排名
group_zscore(x, group)      # 组内标准化
group_mean(x, group)        # 组内均值
group_backfill(x, group)    # 组内回填
group_count(x, group)       # 组内计数
```

### 11.4 条件算子

```python
trade_when(open_event, signal, exit)  # 条件入场
is_nan(x) ? a : b                      # 缺失值条件
hump(x, threshold)                     # 阈值过滤
```

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

---

## 十三、trade_when 条件逻辑

### 13.1 标准结构

```python
trade_when(open_event, signal, exit)
# open_event：入场条件（True 时持仓）
# signal：信号主体（一/二阶 alpha）
# exit：出场条件（-1 = 一直持仓）
```

### 13.2 常用 open_event 模板

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

### 13.3 注意事项

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

---

## 十五、Sharpe / Fitness / Turnover / Margin 调优

### 15.1 提高 Sharpe

1. **提 Return**（重点）
   - 用 lower decay
   - 流动性高的 universe
   - news/sentiment 等高频数据
2. **降波动**
   - 用 `group_neutralize`
   - 用 `trade_when` 砍无效信号
   - 用 `winsorize` 截极值

### 15.2 提高 Fitness

Fitness = Sharpe × sqrt(|Returns| / max(Turnover, 0.125))

- 提 Return + 降 Turnover 双管齐下

### 15.3 调节 Turnover

| 目标 | 动作 |
|---|---|
| **降 Turnover** | 加 decay、用 rank、用 trade_when、用 hump、组合低换手 alpha |
| **升 Turnover** | 减 decay、缩小 universe、缩短窗口 |

### 15.4 提升 Margin

- 换高流动性 universe（TOP1000）
- 降低 Turnover
- 增加 decay
- 减少交易成本

### 15.5 降低 Weight Concentration

1. 加 `rank(...)` 归一化
2. truncation 设 0.05 - 0.1
3. 用 `ts_backfill` 同时解决低覆盖率

---

## 十六、降低自相关性的 5 种方法（按推荐顺序）

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
| 工具一直转圈 | 网络/平台问题 | 重启工具/换时段 |
| 错误码 1001 | IP 被封 | 联系导师去 ippure.com 解锁 |
| 提示账号密码错误 | 密码有空格 | 检查大小写、空格 |
| 官网 504 | 平台繁忙 | 稍后再试 |

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
- 范围 0.5 - 1.0，越高越好
- 每月更新，基于过去 3 个月
- 0.95 vs 0.5 收入差 10 倍+

### 21.4 Pyramid

- 至少 3 个不同数据集/策略类型 = Gold 门槛
- 升 Expert/Master 需要更多 Pyramid

### 21.5 Neutralization 强度

NONE < MARKET < INDUSTRY < SUBINDUSTRY

### 21.6 Self-Color 标记（平台官网）

- 🟢 绿色 = 可提交
- 🟡 黄色 = 边缘
- 🔴 红色 = 不可提交

---

## 二十二、Workday 填写要点

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

## 二十三、发薪日期

### 23.1 Base Payment（每 2 个月）

| 周期 | 账单确认日 |
|---|---|
| 2025/11 - 12 | 2026/01/31 |
| 2026/01 - 02 | 2026/03/31 |
| 2026/03 - 04 | 2026/05/31 |
| 2026/05 - 06 | 2026/07/31 |
| 2026/07 - 08 | 2026/09/30 |
| 2026/09 - 10 | 2026/11/30 |

### 23.2 Quarterly Payment

| 周期 | 发布日 | 账单确认 |
|---|---|---|
| Q4 2025 | 2026/02/23 | 2026/03/31 |
| Q1 2026 | 2026/05/27 | 2026/06/30 |
| Q2 2026 | 2026/08/25 | 2026/09/30 |
| Q3 2026 | 2026/11/24 | 2026/12/31 |

**条件**：上个季度有超过 20 天有提交记录

---

## 二十四、推荐计划

### 24.1 奖励

- 每成功推荐一位新顾问 = **\$100**
- **无上限**

### 24.2 被推荐人需满足

1. 使用你的推荐码（Alias）注册
2. 最终成为正式顾问
3. 在 10 个不同的日子里提交过 Alpha
4. 保持顾问身份至少 1 个月

### 24.3 如何推荐

```
https://platform.worldquantbrain.com/referral/你的推荐码
```

### 24.4 推荐码查看

登录平台 → 右上角头像 → Account → 查看 User ID / Alias

---

## 二十五、纳税

- 平台**代扣代缴**劳务所得税
- 这部分收益会与其他收益一起计入**次年税务汇算清缴**
- 保留所有收入记录
- 官方联系邮箱：mainlandchina@worldquantbrain.com

---

## 二十六、主题日历（Theme Calendar）

### 26.1 机制

- 平台定期发布主题（ESG、AI、红利等）
- 匹配的 alpha 获得**收入倍数加成**
- 主题通常提前公布

### 26.2 应对策略

1. 关注 BRAIN 平台 Theme Calendar 页面
2. 看到主题后针对性开发
3. 日常高质量 alpha 仍是基本盘
4. 主题匹配时集中精力多交

---

## 二十七、官方学习资源

| 资源 | 位置 | 说明 |
|---|---|---|
| Learn 文档 | 平台内 Learn | 最权威知识库 |
| Operator Reference | Learn → Documentation → Operators | 算子完整说明 |
| Data Fields | Learn → Documentation → Data Fields | 数据字段解释 |
| Community Forum | 平台 Forum | 全球顾问交流 |
| Academy 课程 | Learn → Academy | 系统化视频课 |

**建议学习顺序**：
```
1. 通读 Learn 核心文档
2. 完成 Academy 入门课程
3. 在 Forum 读 Expert/Master 分享
4. 尝试不同数据集 + 中性化组合
5. 关注 Theme Calendar
```

---

## 二十八、工具与服务器 FAQ

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

---

## 二十九、回答用户问题时的输出规范

1. **判断场景**：是注册、跑分、提交流程，还是工具调优，还是 alpha 优化？
2. **场景 → 章节**：用本文档对应章节作为蓝本
3. **数据驱动**：所有指标/阈值都引用本文档速查表
4. **可执行**：给出具体配置参数、公式代码、操作按钮
5. **中文输出**：用户用中文则全中文

---

## 三十、常见问答模板

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

A: 见第 22 章要点。地址用英文、时间连续、身份三一致。

### Q: 推荐奖励多少？

A: 每成功推荐一位 \$100，无上限。详见第 24 章。

### Q: 季度奖金多少？

A: Gold \$100，Expert \$200-2000，Master \$2000-8000，Grandmaster \$8000-25000。详见 2.4。

---

## 三十一、关键链接

| 用途 | 链接 |
|---|---|
| BRAIN 官网 | platform.worldquantbrain.com |
| 官方文档 | /learn/documentation |
| 官方论坛 | /learn/community |
| 官方博客 | worldquantbrain.com |
| 老强说教程 | alphadoc.biglongxia.com/guide/ |
| 推荐注册 | /referral/你的推荐码 |
| 中国官方邮箱 | mainlandchina@worldquantbrain.com |
| IP 解封 | ippure.com |
| 韩国社区 | brain-kr.com |
| CSDN 教程 | 搜索「世坤量化」/「worldquant brain」 |
| 开源工具 1 | github.com/xiegengcai/world-quant-brain |
| 开源工具 2 | github.com/zhutoutoutousan/worldquant-miner |

---

> 最后更新：2026-06
> 版本：V2（基于 alphadoc V1 教程 + 官方文档 + 实战经验整合）
> 维护：随平台规则变化同步更新
