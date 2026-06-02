# BRAIN 平台 Dataset 速查表

> 覆盖工具截图中出现的数据集。每个 dataset 给出"典型用法 + 推荐运算符组合方向"。

## 一、Analyst（分析师预期）

### 1. analyst4 — Analyst Estimate Data for Equity

- **典型用法**：分析师对公司未来 EPS / 营收 / 盈利的预期值、调整值、共识值、离散度等。
- **推荐运算符组合方向**：
  - 用 `ts_mean` / `ts_std` 看预期**修正趋势**（向上修正 = 利好）；
  - 用 `quantile` 截面排序构造预期改善因子的多空组合；
  - 配合 `news12` / `news18` 做"预期 + 情绪"双因子叠加。

## 二、Fundamental（基本面）

### 2. fundamental2 — Report Footnotes

- **典型用法**：财报附注中的细分项，如收入构成、关联交易、衍生品头寸、租赁负债等"非主表"信息。
- **推荐运算符组合方向**：
  - 适合做"隐藏杠杆 / 表外风险"类 alpha；
  - 配合 `fundamental6` 的主表字段做交叉验证；
  - 用 `ts_delta` / `ts_rank` 跟踪异常附注变化。

### 3. fundamental6 — Company Fundamental Data for Equity

- **典型用法**：营收、净利润、ROE、资产负债率、市值、PE、PB 等**标准主表财务字段**。
- **推荐运算符组合方向**：
  - 经典价值/质量因子：`rank(value)`、`rank(quality)`；
  - 配合 `pv1` 价格字段做估值因子（PB、PE 倒数）；
  - 用 `group_neutralize(industry)` 消除行业偏差。

## 三、Model（模型打分）

### 4. model16 — Fundamental Scores

- **典型用法**：第三方对公司的**基本面综合评分**（价值、质量、成长、动量等维度）。
- **推荐运算符组合方向**：
  - 直接 `rank` 作为 alpha 主信号；
  - 配合 `pv1` 的反转字段做"好公司 + 超跌反弹"组合；
  - 用 `ts_mean` 平滑短期评分波动。

### 5. model51 — Systematic Risk Metrics

- **典型用法**：系统化风险指标——Beta、波动率、相关度、风险价值（VaR）、风格暴露等。
- **推荐运算符组合方向**：
  - 做**低风险异象 alpha**：`rank(low_vol)`、`rank(low_beta)`；
  - 配合 `pv1` 构造"价格动量 + 低风险"复合因子；
  - 用 `ts_rank` 跟踪风险水平的相对变化。

## 四、News（新闻）

### 6. news12 — US News Data

- **典型用法**：美国市场新闻的标题、来源、分类、热度、情感倾向等。
- **推荐运算符组合方向**：
  - 构造**新闻情绪因子**：`rank(sentiment_score)`；
  - 配合 `pv1` 短窗口价格做"消息 + 价量"短期反转；
  - 用 `group_neutralize(sector)` 避免行业新闻聚类。

### 7. news18 — Ravenpack News Data

- **典型用法**：Ravenpack 提供的**精细化新闻分析**，含事件类别、情感分、热度衰减、实体提及度等。
- **推荐运算符组合方向**：
  - 适合做**事件驱动型 alpha**：并购、分析师奖项、监管事件；
  - 用 `ts_decay_linear` 对新闻热度做时间衰减；
  - 与 `analyst4` 组合做"预期修正 + 新闻确认"双信号。

## 五、Option（期权）

### 8. option8 — Volatility Data

- **典型用法**：隐含波动率（IV）、历史波动率（HV）、波动率偏度（skew）、期限结构等。
- **推荐运算符组合方向**：
  - 经典**波动率风险溢价 alpha**：`rank(IV - HV)`；
  - 配合 `pv1` 构造"低 IV + 强趋势"组合；
  - 用 `ts_std` / `ts_rank` 跟踪波动率聚集效应。

### 9. option9 — Options Analytics

- **典型用法**：期权持仓、PCR（put/call ratio）、最大痛点、未平仓合约分布、Greeks 等衍生指标。
- **推荐运算符组合方向**：
  - 构造**投机情绪 / 风险对冲** alpha：`rank(PCR)`；
  - 与 `option8` 组合做完整期权情绪画像；
  - 用 `group_neutralize(sector)` 排除行业期权偏好差异。

## 六、Price Volume（价量）

### 10. pv1 — Price Volume Data for Equity

- **典型用法**：开高低收、成交量、成交额、换手率、流通市值等**最基础价量字段**。
- **推荐运算符组合方向**：
  - 几乎所有 alpha 都会用到：`rank(returns)`、`ts_delta(close, n)`；
  - 配合 `ts_decay_linear` 做动量/反转；
  - 与 `fundamental6` / `model16` 组合做多因子打分。

### 11. pv13 — Relationship Data for Equity

- **典型用法**：股票间的**关联关系数据**——供应链、客户链、集团归属、共同股东、上下游等。
- **推荐运算符组合方向**：
  - 构造**关联性 alpha**：供应链溢出、龙头-跟随策略；
  - 配合 `pv1` 做"同行业 / 同供应链"动量传染；
  - 用 `group_neutralize` 配合关系字段做差异化中性化。

## 七、Social Media（社交媒体）

### 12. socialmedia12 — Sentiment Data for Equity

- **典型用法**：股票在 Twitter / Stocktwits / 论坛等渠道的**情绪打分**（正负面、热度、变化速度）。
- **推荐运算符组合方向**：
  - 构造**散户情绪 alpha**：`rank(sentiment)`、`ts_delta(sentiment, 5)`；
  - 与 `news18` 组合做"散户 + 机构"情绪差异；
  - 用 `ts_decay_linear` 抑制过快衰减的短期情绪。

### 13. socialmedia8 — Social Media Data for Equity

- **典型用法**：社交媒体的**原始热度数据**——提及量、转发量、讨论数、关注度变化等。
- **推荐运算符组合方向**：
  - 构造**热度 / 注意力因子**：`rank(mentions)`、`ts_rank(mentions, 20)`；
  - 配合 `pv1` 短期价格做"热度爆发 + 价量确认"；
  - 与 `socialmedia12` 组合形成"量（热度） × 价（情绪）"双因子。

## 八、Universe（股票池）

### 14. univ1 — Universe Dataset

- **典型用法**：平台提供的**可交易股票池**（市值、流动性、上市状态、退市、停牌等过滤条件）。
- **推荐运算符组合方向**：
  - 在 alpha 表达式末尾**必加**：`trade_when(univ1.acceptable, alpha, ...)` 或 `univ1.is_universe`；
  - 用 `univ1.is_main_board` / `is_active` 做股票池筛选；
  - 配合 `group_neutralize` 限定子池做子域 alpha。

## 九、组合速查（按策略方向）

| 策略方向 | 推荐 dataset 组合 | 关键运算符 |
|---|---|---|
| **价值 / 质量** | `fundamental6` + `model16` | `rank`、`group_neutralize(industry)` |
| **低风险异象** | `model51` + `pv1` | `rank(low_vol)`、`ts_std` |
| **动量 / 反转** | `pv1` + `model16` | `ts_delta`、`ts_decay_linear` |
| **情绪驱动** | `news12` + `news18` + `socialmedia12` | `rank(sentiment)`、`ts_delta` |
| **事件驱动** | `news18` + `analyst4` | `ts_decay_linear`、`quantile` |
| **波动率溢价** | `option8` + `option9` | `rank(IV - HV)`、`rank(PCR)` |
| **关联性传染** | `pv13` + `pv1` | `group_neutralize`、`ts_rank` |
| **隐藏 / 表外风险** | `fundamental2` + `fundamental6` | `ts_delta`、`ts_rank` |
| **散户跟随 / 反向** | `socialmedia8` + `socialmedia12` + `pv1` | `rank(mentions)`、`ts_decay_linear` |

## 十、使用注意事项

- **股票池收口**：所有 alpha 务必用 `univ1` 收口到平台认可的可交易范围。
- **跨数据集组合**：注意字段时间频率（高频 vs 低频），混用时建议先做时序对齐（`ts_mean` / `ts_decay_linear`）。
- **中性化维度**：根据所用 dataset 选择合适的中性化分组（行业 / 国家 / 市值），避免因子拥挤。
- **原创性**：跨数据集组合时优先选择**不常见**的字段组合，降低 Self Correlation。
