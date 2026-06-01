# WorldQuant BRAIN Alpha 挖掘专家技能

> 一站式顾问级指南：平台规则、流水线配置、模板库、提交流程、问题排查。

---

## 一、技能适用范围

当用户需要以下帮助时，激活本技能：

- 在 WorldQuant BRAIN 平台（platform.worldquantbrain.com）挖掘、提交 alpha
- 调优自动挖 alpha 工具（如「老强说 Alpha 辅助工具」类）
- 解释 Sharpe / Fitness / Turnover / Drawdown / Margin / 自相关等指标
- 诊断 alpha 不达标的原因
- 选择数据集、算子、中性化方式
- 提高可提交率、降低被拒概率

---

## 二、平台核心规则速查

### 2.1 提交门槛（USA D1 为例）

| 指标 | 合格线 | 优秀线 | 优化方向 |
|---|---|---|---|
| Sharpe | ≥ 1.25 | ≥ 1.58 | 加 group_neutralize / 改中性化 |
| Fitness | ≥ 1.0 | ≥ 1.5 | 提 Return、降 Turnover |
| Returns | > 0 | > 5% | 换数据集、换算子 |
| Drawdown | < 10% | < 5% | 加 winsorize、提 truncation |
| Turnover | 1%~70% | 12.5%~40% | 加 decay、用 rank、套 trade_when |
| Margin | > 0 | > 0.0003 | 换高流动性 universe |
| Weight Conc. | 分散 | 极分散 | 加 rank、truncation 0.05~0.1 |
| Self-Correlation | ≤ 0.6 | < 0.4 | 换数据集、加 trade_when |

### 2.2 4 类必过测试

1. **IS（样本内）**：Sharpe > 1.25，Fitness > 1.0
2. **OS（样本外）**：Sharpe > 1.0，IQC 评分仅看 OS
3. **Sub-Universe**：缩小池子后 Sharpe 仍达标
4. **Super-Universe**：放大池子 Sharpe ≥ 0.7×原 Sharpe
5. **Ranked Sharpe Test**：经 rank+power 后仍需通过

### 2.3 严禁事项

- ❌ 抄袭他人 alpha → 永久封号
- ❌ 重复提交同质化 alpha → 扣分
- ❌ 用 Delay=0 绕过前视偏差 → OS 必失败
- ❌ 跨多账号提交同一公式 → 关联封号

---

## 三、流水线架构（适用于自动化工具）

### 3.1 标准三阶流水线

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
提交 + 自相关检查
```

### 3.2 各阶段 Sharpe / Fitness 阈值推荐

| 阶段 | Sharpe 阈值 | Fitness 阈值 | 目的 |
|---|---|---|---|
| 一阶 | 0.85~1.0 | 0.6 | 抓种子 |
| 二阶 | 1.0~1.2 | 0.75 | 提质量 |
| 三阶 | 1.0~1.25 | 0.85 | 控最终可提交 |

---

## 四、数据集选择（按出高质量 alpha 概率排序）

| 优先级 | 数据集 ID | 名称 | 适用场景 |
|---|---|---|---|
| ⭐⭐⭐⭐⭐ | news18 | Ravenpack News Data | 高频更新、Sharpe 最高 |
| ⭐⭐⭐⭐⭐ | news12 | US News Data | news18 备选 |
| ⭐⭐⭐⭐ | model51 | Systematic Risk Metrics | 风险因子、结构化 |
| ⭐⭐⭐⭐ | model16 | Fundamental Scores | 综合分、加工好 |
| ⭐⭐⭐⭐ | socialmedia12 | Sentiment Data | 情绪因子 |
| ⭐⭐⭐⭐ | socialmedia8 | Social Media Data | 社交信号 |
| ⭐⭐⭐ | analyst4 | Analyst Estimate Data | 分析师预期修正 |
| ⭐⭐⭐ | fundamental6 | Company Fundamental Data | 量大、需 backfill |
| ⭐⭐⭐ | pv13 | Relationship Data | 做分组/中性化 |
| ⭐⭐ | pv1 | Price Volume Data | 易撞车、慎用 |
| ⭐⭐ | option8/9 | Volatility/Options Data | 字段少、独特 |
| ⭐ | fundamental2 | Report Footnotes | 信号弱 |

**轮换策略**：每天用 1 个数据集，避免同质化导致自相关。

---

## 五、常用算子速查

### 5.1 时序算子（ts_*）

```python
ts_rank(x, d)            # 时序百分位排名
ts_zscore(x, d)          # 时序标准化
ts_mean(x, d)            # 移动平均
ts_std_dev(x, d)         # 移动标准差
ts_delta(x, d)           # 差分
ts_arg_max(x, d)         # d 日内最大值位置
ts_arg_min(x, d)         # d 日内最小值位置
ts_corr(x, y, d)         # 时序相关系数
ts_decay_linear(x, d)    # 线性衰减加权
ts_backfill(x, d)        # 缺失值回填
ts_sum(x, d)             # 求和
ts_product(x, d)         # 累乘
```

### 5.2 截面算子

```python
rank(x)                  # 截面百分位排名
zscore(x)                # 截面标准化
quantile(x, n)           # 分桶
normalize(x)             # 归一化
scale(x)                 # 缩放
```

### 5.3 组算子（group_*）

```python
group_neutralize(x, group)  # 组内中性化
group_rank(x, group)        # 组内排名
group_zscore(x, group)      # 组内标准化
group_mean(x, group)        # 组内均值
group_backfill(x, group)    # 组内回填
group_count(x, group)       # 组内计数（覆盖率检查）
```

### 5.4 条件算子

```python
trade_when(open_event, signal, exit)   # 条件入场
is_nan(x) ? a : b                       # 缺失值条件
hump(x, threshold)                      # 阈值过滤
```

---

## 六、NaN / 覆盖率处理（被拒最常见原因）

### 6.1 三种处理方式

```python
# 方式 A：开 Settings → NAN HANDLING = On
# 方式 B：用 is_nan 兜底
is_nan(ts_rank(income_tax, 60)) ? ts_rank(sales, 60) : ts_rank(income_tax, 60)

# 方式 C：ts_backfill 补缺失
ts_backfill(x, lookback=120, k=1, ignore="NAN")
```

### 6.2 覆盖率检查

先用 `group_count(field, group)` 检查覆盖率：

| 覆盖率 | 处理方式 |
|---|---|
| > 60% | 直接使用 |
| 30%~60% | 加 group_mean / group_backfill |
| < 30% | 换字段或放弃 |

---

## 七、中性化（Neutralization）选择

### 7.1 平台支持的中性化

| 选项 | 粒度 | 适用 |
|---|---|---|
| None | 无 | 需自定义 |
| Market | 市场 | 跨区域 |
| Sector | 板块 | 10 大类 |
| Industry | 行业 | 30+ 类 |
| **Subindustry**（推荐） | 子行业 | 100+ 类 |
| Country | 国家 | 跨区域 |
| Style | 风格 | 跨因子 |

### 7.2 推荐配置

- **默认 Subindustry** —— 粒度合适、信号保留好
- **formula 中性化 = Settings 中性化**，效果相同：
  ```python
  group_neutralize(-ts_returns(close, 5), industry)
  # 等价于在 Setting 中选 industry
  ```

### 7.3 自定义分组

```python
# 用 bucket() 创建自定义分组
bucket(rank(volume), 10)              # 按成交量分 10 桶
bucket(rank(market_cap), 5)          # 按市值分 5 桶

# 用 densify() 填充分组空缺
densify(pv13_r2_min2_3000_sector)     # 行业分组
densify(market)                       # 市场分组
```

---

## 八、trade_when 条件逻辑（提升 Sharpe 神器）

### 8.1 标准结构

```python
trade_when(open_event, signal, exit)
# open_event：入场条件（True 时持仓）
# signal：信号主体（一/二阶 alpha）
# exit：出场条件（True 时平仓，或 -1 一直持仓）
```

### 8.2 常用 open_event 模板

```python
# 模板 1：放量突破
ts_arg_max(volume, 5) == 0

# 模板 2：站上均线
close > ts_mean(close, 22)

# 模板 3：波动率放大
ts_std_dev(returns, 5) > ts_std_dev(returns, 20)

# 模板 4：量价齐升
ts_corr(close, volume, 10) > 0.5

# 模板 5：价格新高
ts_arg_max(close, 20) == 0
```

### 8.3 注意事项

- ✅ trade_when 是「锦上添花」，signal 本身 Sharpe > 1.0 才有用
- ✅ 出场写 -1 = 一直持仓（最稳）
- ❌ 不要让条件过严（一年没几天触发 → 没收益）
- ❌ 不要三层 trade_when 嵌套（过拟合）

---

## 九、经典 Alpha 模板库

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

## 十、Sharpe / Fitness / Turnover 调优

### 10.1 提高 Sharpe

1. **提 Return**（重点）
   - 用 lower decay
   - 流动性高的 universe
   - news/sentiment 等高频数据
2. **降波动**
   - 用 `group_neutralize`
   - 用 `trade_when` 砍无效信号
   - 用 `winsorize` 截极值

### 10.2 提高 Fitness

Fitness = Sharpe × sqrt(|Returns| / max(Turnover, 0.125))

- 提 Return + 降 Turnover 双管齐下

### 10.3 调节 Turnover

| 目标 | 动作 |
|---|---|
| **降 Turnover** | 加 decay、用 rank、用 trade_when、用 hump、组合低换手 alpha |
| **升 Turnover** | 减 decay、缩小 universe（如 TOP3000→TOP1000）、缩短窗口 |

### 10.4 降低 Weight Concentration

1. 加 `rank(...)` 归一化
2. truncation 设 0.05~0.1
3. 用 `ts_backfill` 同时解决低覆盖率

---

## 十一、自动化工具配置（以「老强说 Alpha 辅助工具 v1.0.5」为例）

### 11.1 Stage 1 推荐配置

```
数据集：news18 - Ravenpack News Data（轮换）
区域：USA
延迟：1
股票池：TOP3000
资产类型：Equity
中性化：Subindustry
任务表达式数 Max Run：1500
Sharpe 阈值：0.9
Fitness 阈值：0.6
最少做多数：80
最少做空数：80
```

### 11.2 Stage 2/3 推荐配置

```
数据集：同 Stage 1（可换）
区域：USA
延迟：1
股票池：TOP3000
中性化：Subindustry
任务表达式数 Max Run：1500
Sharpe 阈值：1.0~1.15
Fitness 阈值：0.85
最少做多数：100
最少做空数：100
```

### 11.3 Alphas Tab 操作

```
1. 开启「行颜色标记」
2. 切到「可提交」Tab
3. 按 Sharpe 排序
4. 先提交 1 个，等 5 分钟看结果
5. 成功后再提交其余
6. 自相关 > 0.6 立即放弃
```

### 11.4 工具参数速查表

| 参数 | 推荐值 | 说明 |
|---|---|---|
| Region | USA | 池子大、Sharpe 高 |
| Delay | 1 | 避免前视偏差 |
| Universe | TOP3000 | 平衡流动性与广度 |
| Instrument Type | Equity | 股票 |
| Neutralization | Subindustry | 粒度合适 |
| Max Run | 1500 | 省铜牌 |
| Sharpe | 0.9~1.2 | 看阶段 |
| Fitness | 0.6~0.85 | 看阶段 |
| 最少做多/空 | 80~120 | 防过拟合 |

---

## 十二、每日操作 SOP

### 12.1 早晨（10 分钟）

```
1. 登录 BRAIN 平台 → 看今日可用提交次数
2. 打开工具 → 「Alphas」Tab → 处理昨天未提交
3. 切到「可提交」Tab → 按 Sharpe 排序
4. 先提交 1 个 → 等待 5 分钟看结果
5. 成功则继续提交 1~2 个
```

### 12.2 上午（30~60 分钟）

```
6. Stage 1：选新数据集（每天换）
7. 配置参数（按 11.1）
8. 启动一阶段任务
9. 同步近 3 天 Alpha（每天 1 次）
```

### 12.3 下午（30~60 分钟）

```
10. Stage 1 完成 → 自动进入 Stage 2
11. Stage 2 完成 → 自动进入 Stage 3
12. Stage 3 完成 → 「Alphas」Tab 看结果
13. 跑「快速查可提交」自动筛选
```

### 12.4 晚上（10 分钟）

```
14. 提交当天产出的最优 alpha
15. 记录今天产率（Excel/Notion）
16. 复盘：哪个数据集产出最好？明天继续
```

---

## 十三、数据集轮换排期

| 周几 | 数据集 | 备注 |
|---|---|---|
| 周一 | news18 | 高命中率 |
| 周二 | model16 | 稳 |
| 周三 | news12 | 高频 |
| 周四 | model51 | 风险类 |
| 周五 | socialmedia12 | 情绪 |
| 周六 | analyst4 | 分析师 |
| 周日 | pv13 | 关系数据 |

**重要**：同一数据集不要连续用 2 天以上，避免自相关。

---

## 十四、问题排查清单

| 现象 | 原因 | 解决 |
|---|---|---|
| 一阶 0 个种子 | 阈值太高 | 降到 0.5 |
| 一阶种子 > 500 | 阈值太低 | 提到 1.0 |
| 二阶全军覆没 | group 选择不当 | 换 industry / subindustry |
| 三阶全失败 | trade_when 模板不合适 | 换模板 |
| 提交失败：自相关高 | 与历史 alpha 太像 | 换数据集、加 trade_when |
| 提交失败：Weight 集中 | 缺归一化 | 加 rank、truncation 0.08 |
| 提交失败：Sharpe < 1.25 | 信号弱 | 换数据集、改中性化 |
| 提交失败：Turnover > 70% | decay 太小 | 加大 decay 到 4~8 |
| 提交失败：Sub-Universe 不通过 | 信号只在 TOP3000 有效 | 在更小池先测 Sharpe 达标再交大池 |
| 铜牌消耗快 | Max Run 太大 | 降到 1000 |
| 跑完无结果 | 任务未启动 | 检查是否点「开始」 |

---

## 十五、关键概念速查

### 15.1 Decay

- 控制 alpha 权重随时间衰减速度
- **0** = 无衰减（噪声大）
- **1~5** = 短期信号
- **5~15** = 中期（**推荐**）
- **> 20** = 长期（接近无效）

### 15.2 Truncation

- 限制单只股票最大权重
- **0.05** = 5% 上限（**推荐稳健型**）
- **0.08~0.10** = 平衡（**常用**）
- **0.20+** = 集中

### 15.3 Neutralization

- 剥离不想要的因子影响
- 公式法：`group_neutralize(x, group)`
- Setting 法：选 industry / subindustry
- 效果相同

### 15.4 Fitness 公式

```
Fitness = Sharpe × sqrt(|Returns| / max(Turnover, 0.125))
```

- 提 Return + 降 Turnover 同时提升

### 15.5 自相关 (Self-Correlation)

- 与已提交 alpha 的相关性
- **≤ 0.6** 为通过门槛
- 公式太相似会被判定抄袭

---

## 十六、资源索引

| 资源 | 链接 |
|---|---|
| BRAIN 官方文档 | platform.worldquantbrain.com/learn/documentation |
| Operators 文档 | /learn/documentation/create-alphas/operators |
| Neutralization 文档 | /learn/documentation/create-alphas/neutralization |
| 中文社区 | 平台 Events 页面入口 |
| CSDN 实战博客 | 搜索「世坤量化」「worldquant brain」 |
| 韩国社区 | brain-kr.com、velog.io/@kjy718 |
| 开源工具 | github.com/xiegengcai/world-quant-brain |
| 开源工具 | github.com/zhutoutoutousan/worldquant-miner |

---

## 十七、回答用户问题时的输出规范

1. **先判断场景**：是问平台规则、工具配置、还是 alpha 模板？
2. **场景 → 章节**：用本文档对应章节作为回答蓝本
3. **数据驱动**：所有指标/阈值都引用本文档的速查表
4. **可执行**：给出具体配置参数、公式代码、操作按钮
5. **中文输出**：用户用中文则全中文回答

---

## 十八、常见问答模板

### Q: 如何提高可提交率？

A: 五件套：①干净的字段 ②中性化 ③trade_when ④合理 decay/truncation ⑤多样性。具体阈值见本文档第二、八、十章。

### Q: 哪个数据集最好？

A: news18 / news12 命中最高，但每天要换。完整排期见第十三章。

### Q: Sharpe 老是上不去？

A: ①加 group_neutralize ②换中性化粒度 ③加 trade_when ④换数据集。详见第十章。

### Q: 自相关过高怎么办？

A: ①换数据集 ②加 trade_when 改信号 ③套不同中性化（industry vs subindustry）。

### Q: 工具怎么配？

A: Stage 1 Max Run=1500，Fitness=0.6；Stage 2/3 Sharpe=1.0，Fitness=0.85。完整见第十一章。

### Q: 今天能提交几个？

A: 看账户状态。右上角「3/3」= 已满。明日刷新。新人期 1 个、正式顾问 2~4 个。

---

> 最后更新：2026-06
> 维护：随平台规则变化同步更新
