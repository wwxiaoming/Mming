# WorldQuant BRAIN 平台官方机制研究

> **研究目标**：为"金融小白"系统性梳理 WorldQuant BRAIN 量化平台的官方机制，重点覆盖等级体系、奖金机制、Alpha 评价指标、重复率检测、Region/Dataset 分布以及平台对第三方工具的态度。
>
> **数据来源**：
> - 官方页面：https://platform.worldquantbrain.com/、https://worldquantbrain.com/consultant
> - 官方文档/帮助：https://platform.worldquantbrain.com/learn/operators、https://platform.worldquantbrain.com/learn/documentation
> - 官方竞赛规则：https://www.worldquant.com/brain/iqc-guidelines/
> - 一手顾问实践记录（CSDN、博客、知乎、GitHub 自动化项目）
> - 公开的 WorldQuant BRAIN 自动化工具源码（github.com/xiegengcai/world-quant-brain、rocky-d/wqb）
>
> **重要前提**：BRAIN 平台核心数据页面均需登录访问，本研究综合官方公开宣传、IQC 竞赛官方规则、以及公开的开源自动化项目代码来反推其内部机制。涉及到"奖金具体数额"等非公开数据，均以官方宣传与顾问社区披露区间为准，并以"约"或"区间"标注。

---

## 一、BRAIN 平台是什么

WorldQuant BRAIN 是 WorldQuant（全球知名量化资管公司，旗下管理 70 亿美元资产，26 个办公室）于 2017 年前后推出的"云端量化研究模拟平台"。

- 官方定义：**Alphas** 是"用于预测各类金融工具未来价格走势的数学模型"。
- 平台规模（2026 年最新数据）：
  - 累计用户 **250,000+**（2024 年披露为 80,000+ → 2025 年 375,000 → 2026 年约 25 万活跃用户 + 累计更高）
  - 研究顾问 **9,000+**
  - 覆盖 **17 个国家和地区**：中国大陆、香港、台湾、肯尼亚、韩国、印度尼西亚、印度、马来西亚、新加坡、英国、越南、泰国、美国、亚米尼亚、匈牙利、尼日利亚、格鲁吉亚
  - 数据字段 **200,000+**
- 平台目的：让任何掌握 Python 的人都能"挖因子"贡献想法，高质量 Alpha 会被买断，贡献者可获得报酬，并有机会被 WorldQuant 招聘为正职/实习生。
- 官方宣传：「*WorldQuant defines "alphas" as mathematical models that seek to predict the future price movements of various financial instruments.*」

---

## 二、等级体系：Bronze → Silver → Gold → Consultant

### 2.1 等级晋升路径（一图速览）

```
注册账户 (无等级)
   │
   ↓  累计提交 2,000 Challenge 积分
   │
  Bronze（铜牌）
   │
   ↓  累计 5,000 Challenge 积分
   │
  Silver（银牌）
   │
   ↓  累计 10,000 Challenge 积分
   │
  Gold（金牌）── 自动收到顾问邀请
   │
   ↓  填写问卷 → 背调 → 签约
   │
（有条件顾问）── 提交可获 Base Payment
   │
   ↓  背调通过
   │
  Consultant（正式研究顾问）── 收益可提现
   │
   ↓  持续高质量提交
   │
  Master / Grandmaster（季度奖金等级）
```

### 2.2 关键规则（Challenge Score 挑战积分）

| 规则 | 具体内容 | 备注 |
|---|---|---|
| 目标分数 | **10,000 Challenge 积分** = 达到 Gold 等级 | 平台次日自动发邀请邮件 |
| 每日上限 | **2,000 分/天** | 提交再多也不超过 |
| 单 Alpha 得分 | 1,500–2,000 分（高质量 Alpha 当天可拿满分） | 提交 2 个通常就能打满当日 |
| 积分更新 | T+1 日，北京时间 14:00–15:00 刷新 | 非实时 |
| 日期切分 | 美东时间 (ET) 为准 | 北京时间 19:00 后算第二天 |
| 时间限制 | 无 | 中断几天不影响累计 |
| 连续性要求 | 无 | 不要求每天提交 |
| 衰减机制 | 积分随时间小幅衰减 | 推荐"每天稳定提交 1–2 个"而非"一次性堆量" |

### 2.3 各等级分值门槛（综合多份资料）

| 等级 | 分数门槛 | 解锁能力 |
|---|---|---|
| **Bronze（铜牌）** | 2,000 分 | 可继续提交 Alpha 攒分 |
| **Silver（银牌）** | 5,000 分 | 数据字段更多、平台功能扩展 |
| **Gold（金牌）** | **10,000 分** | 收到顾问邀请邮件、获取欧洲/亚洲 125,000+ 数据字段访问权、Python API、SuperAlpha、并行回测、可视化图表 |
| **Consultant** | 平台邀请 | 提交可获 Base Payment 收益 |
| **Master** | 平台评定 | 季度奖金 ≥ $2,000 |
| **Grandmaster** | 平台评定 | 季度奖金 ≥ $8,000 |

> 官方原话：「*Once you hit 10,000 points on BRAIN and reach gold, you may receive an invitation to join the BRAIN Research Consultant Program. Once you are successfully on the program, you will receive advanced features, the ability to submit alphas and be compensated for them, get BRAIN consultant exclusive events, and more.*」（[worldquantbrain.com/consultant](https://worldquantbrain.com/consultant)）

### 2.4 中国大陆申请者特别路径

- **国际通用路径**：10,000 分（Gold）即可收到邀请。
- **国内补充路径**：除 10,000 分外，需 **累计提交 ≥ 20 个 Alpha**，并通过 "Alpha 研究能力测试"（题目来自官方"零基础学量化"讲座）。
- 国内路径实际操作周期：实战案例显示 **5–7 天** 即可达到 10,000 分门槛，但完成从"金牌"到"正式顾问"的背景调查常需 1–3 个月。

---

## 三、顾问阶段奖金机制

### 3.1 顾问收入构成（EARN 模块）

BRAIN 顾问的"工资"由四大模块组成：**Base Payment（基础津贴）+ Quarterly Payment（季度奖金）+ Competition（竞赛奖金）+ Referral（推荐奖金）**。

#### 3.1.1 Base Payment（基础日津贴）

| 项目 | 数额 | 规则 |
|---|---|---|
| 日津贴范围 | **1 – 120 USD/天** | 0 提交 = 0 收入 |
| Regular Alpha 贡献 | 1 – 60 USD/天 | 顾问每天可提交 1–4 个 Regular Alpha |
| Super Alpha 贡献 | 1 – 60 USD/天 | 交满 100 个 Regular 后解锁，每天可提交 1 个 |
| 决定要素 | (1) 提交数量（全球相对排名）<br>(2) 提交质量（全球相对排名）<br>(3) 与自己历史相比的成长<br>(4) **Value Factors**（越接近 1 越好） | 平台每日结算 |
| 主题加成 | 当前 Theme（数据集/区域/Super）下，质量分会有倍数加成 | Learn → Theme Calendar 查看当前主题 |

> 实战经验（CSDN 博主 @scdifsn）："每天平均提交 1–2 个，新顾问初期每天约 1.5–2 美元；有 EUR D1 主题加成周最高单日近 7 美元"。

#### 3.1.2 Quarterly Payment（季度奖金）

| 项目 | 数额 | 规则 |
|---|---|---|
| 范围 | **100 – 25,000 USD/季度** | 1,000 – 8,000 美元是 Master/Grandmaster 主流区间 |
| 触发条件 | 上季度 **超过 20 个自然日有提交** | 没满 20 天则当季为 0 |
| 决定因素 | (1) **Weight**（平台分配的"权重"账户）<br>(2) **OS（Out-of-Sample，样本外）表现**<br>(3) Weight 需时间积累<br>(4) OS 结果与 Value Factors 直接挂钩 | 平台季度末结算 |

> Grandmaster 官方宣传：「*Grandmaster level consultants can potentially earn upwards of $8,000 or more in a quarterly payment amount.*」（[worldquantbrain.com/consultant](https://worldquantbrain.com/consultant)）

#### 3.1.3 好 Alpha 的"软性"门槛（影响季度奖金）

社区总结的"高质量 Alpha"标准（与季度奖金挂钩）：

- sub-universe（更小股票池）测试 Sharpe ≥ 70% 原 Alpha 的 Sharpe
- super-universe（更大股票池）测试 Sharpe ≥ 70% 原 Alpha 的 Sharpe
- **Turnover ≤ 30%**
- **Margin ≥ 4 bps**（每美元交易额年化利润 ≥ 0.04%）
- 不为通过相关性而人为加噪音（否则被识别为 overfitting，会扣分）

#### 3.1.4 Competition（竞赛奖金）

顾问可参加：BRAIN 平台上的 **Super Alpha Competition、ACE Competition、Global Alphathon、Local Alphathon、IQC** 等。Global Alphathon 2025 奖金池为 $100,000，其中全球总决赛冠军 $20,000 / 亚军 $10,000 / 季军 $5,000。

#### 3.1.5 Referral（推荐奖金）

- 奖励金额：**200 USD / 成功推荐一人**
- 条件：(1) 新用户注册时填你的 User Alias；(2) 被推荐人在 10 个不同自然日提交 Alpha；(3) 保持顾问身份 1 个月以上；(4) 不设上限
- 限时活动：早期参与推广活动，**新人顾问 30 天内满 10 天提交可拿 $100 一次性奖励**；当季累计 20 天可获 $100–200 季度奖励（该奖励会随时间变化）

### 3.2 "可重复 Alpha" vs "一次性 Alpha" 的区别

这是顾问阶段的关键概念。

| 维度 | 可重复 Alpha（Recurring/Repeatable） | 一次性 Alpha（One-off） |
|---|---|---|
| **含义** | 长期贡献于投资组合的稳定 Alpha 源 | 一次提交就结算、不可累积 |
| **结算方式 | Base Payment + Quarterly Payment 长期滚动 | 通常仅一次性小额 Base Payment |
| **OS 表现 | 持续稳健 | 一次性之后价值归零 |
| **平台态度** | 核心奖励对象 | 边际贡献，奖金贡献小 |
| **Quarterly 影响 | 大（决定 Weight 累计） | 小 |

> 直白理解：可重复 Alpha = "会下金蛋的鸡"，平台希望你持续输出；一次性 Alpha = "一次性玩具"，收益天花板低。

平台官方目的：把顾问当成"外包研究员"，希望找到"可重复"的 alpha 源 → 把 Weight（账户权重）按季度滚动分配给产出高 OS 收益的顾问 → 形成长期供给关系。

### 3.3 奖金发放频率与计算规则

- **Base Payment**：每日结算（具体到账时间以平台公告为准）
- **Quarterly Payment**：按"自然季度"结算（1–3 月、4–6 月、7–9 月、10–12 月）
- **Competition & Referral**：活动结束后按规则批量打款
- **支付币种**：默认 USD；当地法律禁止美元支付的国家，平台可能以本地货币等价支付
- **税务**：自行申报（美国/中国/英国等地区规则不同）；中国大陆地区通常需自行申报劳务报酬所得税

---

## 四、Alpha 评价指标体系

提交 Alpha 后，平台会显示 **IS Summary（样本内摘要）** 和 **Correlation（相关性）** 两类指标。**真正决定"能不能提交 + 能挣多少钱"的是这些指标。**

### 4.1 提交硬性门槛（必须同时满足）

> 官方原话（参考 [BRAIN Basics Chapter 6](https://blog.csdn.net/zurie/article/details/156424353)、第三方开源项目源码 [xiegengcai/world-quant-brain](https://github.com/xiegengcai/world-quant-brain) 总结）：

| 指标 | 阈值 | 不达标后果 |
|---|---|---|
| **Sharpe Ratio** | > **1.25** | 不能提交 |
| **Fitness** | > **1.0** | 不能提交 |
| **Self Correlation** | < **0.7**（默认保守 0.6） | 不能提交 |
| **Turnover** | 1% – 70% 区间 | 极端值被拒 |
| **Delay** | 0 或 1（部分 0 有更严约束） | 必须明示 |

**例外条款**：如果你的 Sharpe 比"历史上相似 Alpha"高出 ≥ 10%，可豁免 Self Correlation 限制（实际阈值变为 1.25 × 1.1 = **1.375**）。

> WorldQuant 内部标准（更严苛）：「*对于日内 alpha 而言，其夏普应该大于 3.95；对于延迟 1 日的 alpha 而言，其夏普应该大于 2.5*」（[BigQuant：寻找市场中的 Alpha](https://blog.csdn.net/bigquant/article/details/112693265)）

### 4.2 指标详细解读

#### 4.2.1 Sharpe Ratio（夏普比率）
- **定义**：风险调整后的平均收益。`Sharpe = Returns / StdDev(Returns)`
- **健康区间**：1.25–2.5（提交门槛） / ≥ 2.5（"好 alpha"目标）/ 3.95+（日内 alpha 顶级）
- **通俗理解**：每承担 1 单位风险，能换回多少收益
- **提高方法**：(1) 增加 Return；(2) 降低波动；(3) 用 neutralization；(4) 用 trade_when / winsorize

#### 4.2.2 Fitness（健康度）
- **公式**：`Fitness = Sharpe × Sqrt( |Returns| / max(Turnover, 0.125) )`
- **健康区间**：> 1.0（提交门槛） / 1.5–2.5+（"好"） / ≥ 3（顶级）
- **通俗理解**：综合"赚得多不多 + 交易成本高不高"的一个综合分
- **提高方法**：提高 Return + 降低 Turnover

#### 4.2.3 Turnover（换手率）
- **公式**：`Daily Turnover = Dollar Trading Volume / Booksize`，Booksize 默认 \$20M
- **健康区间**：1% – 70% / 推荐 30%–40% / 顾问季度奖看 ≤ 30%
- **通俗理解**：每天交易额占本金的比例，反映交易频率和摩擦成本
- **降低方法**：加 decay、用 rank、用 trade_when、用 hump 阈值
- **提高方法**：减 decay、用更小更流动的 universe（如 TOP1000 代替 TOP3000）、用高频更新的数据（新闻/情绪）

#### 4.2.4 Returns（收益率）
- **公式**：`AnnualReturn = AnnualizedPnL / (0.5 × BookSize)`
- **健康区间**：越高越好（与 universe 有关；USA TOP3000 上 5%–15% 年化已是好）
- **提高方法**：(1) 提升 turnover + lower decay；(2) 用流动性更高的小 universe；(3) 尝试 new 和 analyst 数据集

#### 4.2.5 Drawdown（回撤）
- **定义**：回测期内资金曲线的最大累计跌幅
- **健康区间**：< 5%（严苛） / 5%–10%（好） / > 20%（差）
- **降低方法**：用 neutralization、降低仓位集中度、用 trade_when 控制风险

#### 4.2.6 Margin（边际收益）
- **定义**：每单位交易金额产生的平均盈亏（bps）
- **健康区间**：> 4 bps（顾问季度奖参考线）
- **意义**：与"换手成本"形成对照——只有 margin 高于交易摩擦成本时，alpha 才是"真金白银"能赚钱的

#### 4.2.7 Correlation（相关性）
- **Self Correlation（自相关）**：新 Alpha 与该账户下"所有已提交 Alpha"的最大皮尔逊相关系数，4 年滚动窗口计算
- **生产相关性（Production Correlation）**：与平台"生产组合"中 Alpha 的相关性
- **同区域相关性 / 跨区域相关性**：新 Alpha 与"同 Region 已存在 Alpha"的最大相关性
- **阈值**：< 0.7 提交门槛，第三方工具默认 0.6 更保守
- **通俗理解**：越低代表越"新颖"、与已有策略重合度越低

### 4.3 进阶稳健性测试（Robustness Test）

提交后，平台会自动跑以下"附加考试"：

| 测试 | Pass 条件 | 说明 |
|---|---|---|
| **Sub-universe test** | 下一级更小 universe 的 Sharpe ≥ √252 × max(0.065, ratio × 0.15) | Delay0 用 0.25 |
| **Super-universe test** | 下一级更大 universe 的 Sharpe ≥ 0.7 × 原 Sharpe | 检查在更广股票池是否还稳健 |
| **Ranked Sharpe test** | 应用 rank + power 操作后的 Sharpe 不能差太多 | 检查排序后的稳定性 |
| **OS test（样本外）** | 真正决定季度奖金；IS 表现再高，OS 崩了就无价值 | 平台内部会预留 30% 之后的数据作 OOS |

---

## 五、重复率检测机制（Duplication / Uniqueness）

### 5.1 平台检测机制

平台通过三道闸口防止"重复提交"：

1. **Self-Correlation（自相关）**：新 Alpha 与该用户账户下所有已提交 Alpha 的最大皮尔逊相关。默认阈值 0.6–0.7。
2. **Production Correlation（生产相关性）**：与平台"已收录在生产组合中"的 Alpha 的相关性，避免"撞车"已有策略。
3. **Peer Production Threshold**：开源项目源码披露，平台使用此参数评估"和全平台其他顾问已提交 Alpha 的相似度"。

### 5.2 对评分的影响权重

| 维度 | 权重（社区经验） | 备注 |
|---|---|---|
| IS Sharpe / Fitness | 高（约 50%） | 决定能否提交 |
| Self-Correlation | 决定"能否提交"（硬门槛） | 不达标 = 不能提交 |
| Production Correlation | 决定"OS 权重累计" | 影响季度奖金 |
| Sub/Super Universe | 决定"最终 Grade" | PASS / INFERIOR / FAIL |
| 平台 Grade | 决定是否进入"生产组合" | Grade = PASS 才会被纳入 |

### 5.3 平台给出的"等级评分"（Grade）

平台在每次 simulation 后会分配一个 Grade：
- **PASS**：可参与生产组合、获权重
- **INFERIOR**：可提交但不分配 Weight
- **FAIL**：直接被丢弃

Grade 是平台不公开的"暗分"，但与上述所有指标强相关。

### 5.4 如何规避"撞车"

- **理解动机**：WorldQuant 真正稀缺的是"独立信号"，重复 alpha 没有商业价值。
- **实战建议**：(1) 用 group_neutralize / group_rank 在子组上差异化；(2) 用 trade_when 加条件逻辑；(3) 用 2nd/3rd Order 工厂组合（参考 factory.py 中的 `get_group_second_order_factory`、`trade_when_factory`）；(4) 在小众 Dataset（如 analyst、sentiment）上挖。

---

## 六、Region 与 Dataset 分布

### 6.1 Region（区域）支持情况

| 区域 | 代码 | 公开可访问 | 顾问级访问 | 备注 |
|---|---|---|---|---|
| 美国 | **USA** | ✅ | ✅ | 默认区域、TOP3000/TOP1000/TOP500/TOP200 |
| 中国 | **CHN** | ✅ | ✅ | 大陆 + 港股概念 |
| 亚洲 | **ASI** | ❌ | ✅ | 多亚洲市场组合 |
| 欧洲 | **EUR** | ❌ | ✅ | 多欧洲市场组合 |
| 韩国 | **KOR** | ❌ | ✅ | |
| 日本 | **JPN** | ❌ | ✅ | |
| 台湾 | **TWN** | ❌ | ✅ | |
| 香港 | **HKG** | ❌ | ✅ | |
| 美洲（除美国） | **AMR** | ❌ | ✅ | |
| 全球组合 | **GLB** | ❌ | ✅ | 多区域同步模拟 |

> 官方说明：「*Currently, you can simulate in United States (USA) region. Once you reach the level and become a BRAIN consultant, you'll be able to run simulations in more regions. Regions supported at the consultant level include Asia (ASI), Europe (EUR), China (CHN), Korea (KOR), Taiwan (TWN), Hong Kong (HKG), Japan (JPN), Americas (AMR), and Global (GLB).*」（[BRAIN Basics Chapter 6 - Settings](https://blog.csdn.net/zurie/article/details/156424353)）

### 6.2 Dataset（数据集）分类

| 类别 | 典型 Dataset ID | 说明 |
|---|---|---|
| 价格/成交量 | `pv1`, `option8` | 行情数据，最常用 |
| 基本面 | `fundamental2`, `fundamental6` | 财报、估值 |
| 分析师 | `analyst7`, `analyst4` | 券商一致预期 |
| 新闻/情绪 | `news12`, `news18`, `socialmedia12`, `sentiment1` | 文本情感 |
| 期权/衍生品 | `option8`, `option9` | 波动率曲面 |
| 模型/风险 | `model51` | 系统性风险因子 |

> 开源参考 [dataset_config.py](https://github.com/xiegengcai/world-quant-brain/blob/97e8c852/dataset_config.py) 列出 16 个常用 dataset 详细配置。

### 6.3 哪个 Region / Dataset 奖金池更大？

- **美国（USA）奖金池最大**：用户基数大、数据字段最多、Bonus Theme 最频繁、Value Factor 也最高。
- **欧洲（EUR）次之**：2025–2026 多次推出 EUR D1 主题加成（如 1.5x 加成周）。
- **亚洲（ASI）也有定期主题**：2025 年韩 IQC、东南亚多国集中推广。
- **Dataset 优先级（社区经验）**：
  - 高 Value Score：`pv1`、`fundamental6`、`analyst7`、`model51`
  - "低垂果实"已被挖光：标准 pv1 + rank + ts_delta 类
  - "仍有空间"：`news12`、`socialmedia12`、`option8/9`、`analyst4`
- **Theme（主题）轮换**：平台会按周/月轮换"数据集/区域/Super Alpha"主题。Learn → Theme Calendar 可以查当前主题。

### 6.4 Universe（股票池）

按流动性选股：TOP3000 / TOP1000 / TOP500 / TOP200（数字越小 = 流动性越高、覆盖越集中）。
- TOP3000 = TOP1000（高流动性）+ 2000 只次流动性，组合流动性较低
- TOP1000 反而是更"小更流动"的池子

> Turnover 与 Universe 直接相关：TOP1000 交易更容易 → Turnover 高；TOP3000 偏向低频 → Turnover 低。

---

## 七、平台对第三方工具的态度

### 7.1 官方立场（基于 IQC 官方规则反推）

IQC 2026 官方规则明确：

> 「*A participant's account and login credentials may not be shared with any other individual. A participant may only have one active BRAIN account. Duplicate accounts for one individual are grounds for disqualification not only from the IQC but also from BRAIN and the WorldQuant Challenge.*」

由此可推断：

- ✅ **允许**：本人使用第三方工具/脚本（自动化 Alpha 生成、批量回测、调用 API）进行研究和提交
- ❌ **禁止**：账号共享、多账号、刷量行为
- ⚠️ **灰色地带**：是否允许"完全无人值守的 7×24 自动化刷分"？官方未明文禁止，但会被 OS 表现反噬（低质量 alpha 提交越多，越拖累 Value Factor 与 Grade）

### 7.2 实际社区生态

BRAIN 生态中存在大量**第三方自动化工具**（公开 GitHub 上有数十个），常见类型：

| 类型 | 工具 | 功能 |
|---|---|---|
| API 封装 | `wqb`（rocky-d） | Python 客户端，调用 BRAIN 平台 API |
| Alpha 生成器 | `worldquant-miner` | 模板化生成 + 模拟 + 提交 |
| Super Alpha 自动挖掘 | `worldquantbrian` 进化算法 | 50% 探索 + 50% 精英变异 |
| 端到端流水线 | `world-quant-brain`（xiegengcai） | 含 correlation filter、self-correlation 分析、批量提交 |
| 浏览器辅助 | Selenium / Playwright 脚本 | UI 操作自动化 |

### 7.3 平台风控（基于 API 行为反推）

开源工具源码显示，平台有如下风控：

1. **Rate Limit（速率限制）**：API 返回 `429 Too Many Requests`，响应头含 `Retry-After`
2. **Session 过期**：Session 3 小时左右过期，需重新登录
3. **Self-Correlation 实时计算**：使用 4 年滚动窗口
4. **相关数据延迟**：相关性数据可能在回测完成后数十秒才就绪（开源工具代码注释明确说明）
5. **主题加成识别**：平台区分"主题内 alpha"和"非主题 alpha"，分别打分

### 7.4 是否会被"封号"？

社区共识：

- **使用自动化工具本身不违规**——平台甚至在 Learn 模块专门讲解 Python API 集成。
- **真正会被惩罚的行为**：
  - 账号共享 / 多账号 → 立即封号
  - 大规模"零思考"刷量 → Grade 持续 INFERIOR → 季度奖金归零 → 长期会被取消顾问资格
  - 试图绕过相关性检测（人为加噪声）→ 平台会识别 overfitting，OS 表现会塌方
- **"安全"使用第三方工具的建议**：
  - 只用工具加速"挖掘"，不放弃"质量判断"
  - 每日提交量控制在平台建议范围（1–4 个 Regular + 1 个 Super）
  - 持续跟踪 OS / Grade，不只看 IS 指标

---

## 八、关键术语速查表（金融小白版）

| 术语 | 白话解释 |
|---|---|
| **Alpha** | 一个"预测股票未来涨跌"的数学公式 |
| **Sharpe Ratio** | 收益/风险比，越高越好（每承担 1 单位风险能赚多少） |
| **Fitness** | "性价比"打分 = Sharpe × √(收益绝对值/换手率) |
| **Turnover** | 每天换手比例，越低 = 交易成本越低 |
| **Drawdown** | 资金曲线从最高点回撤的最大幅度 |
| **Margin** | 每 1 美元交易能赚多少 bps（万分之几） |
| **Self Correlation** | 你的新 alpha 和你之前所有 alpha 的"相似度"，越低越好 |
| **Delay** | 数据延迟天数，0=当天数据，1=前一天数据 |
| **Universe** | 股票范围（TOP3000 = 美股流动性前 3000 名） |
| **Neutralization** | 行业/风格中性化（让 alpha 不偏向某行业） |
| **Decay** | 持仓权重的衰减速度 |
| **Truncation** | 单只股票最大持仓比例（防过度集中） |
| **OS（Out-of-Sample）** | 样本外测试，用回测时没见过的数据检验 |
| **IS（In-Sample）** | 样本内，回测时用的数据 |
| **Weight** | 平台给你"账户"的权重，决定季度奖金分配 |
| **Value Factor (VF)** | 平台对你 alpha 质量的综合评分（越接近 1 越好） |
| **Theme** | 平台当期重点关注的 Dataset / Region，提交对应主题有加成 |
| **Regular Alpha** | 普通 alpha，顾问每天可交 1–4 个 |
| **Super Alpha** | 高级 alpha（更复杂规则 + 更高收益），交满 100 个 Regular 后解锁 |
| **Challenge Score** | 挑战积分，攒到 10,000 升 Gold、获顾问邀请 |

---

## 九、研究摘要（简明版）

1. **等级体系**：Bronze（2,000）→ Silver（5,000）→ Gold（10,000）→ Consultant，10,000 分门槛 + 国内 20 个 Alpha + 研究能力测试，通过后收顾问邀请。
2. **顾问收入**：日 Base Payment（1–120 USD/天）+ 季度奖（100–25,000 USD/季，Master ≥ 2,000、Grandmaster ≥ 8,000）+ 比赛奖金 + 推荐奖金。Quarterly Payment 需要"上季度 20 天有提交"才能拿到。
3. **可重复 vs 一次性 Alpha**：可重复 = 长期贡献 + 季度奖滚动累计；一次性 = 单次提交，收益天花板低。平台真正奖励的是"可重复 alpha"。
4. **Alpha 硬门槛**：Sharpe > 1.25、Fitness > 1.0、Self Correlation < 0.7、Turnover 1%–70%。
5. **指标体系**：Sharpe / Fitness / Turnover / Returns / Drawdown / Margin / Correlation 七大指标 + Sub/Super Universe 鲁棒性测试 + OS 表现（真正决定季度奖金）。
6. **重复率检测**：Self-Correlation（自相关，4 年滚动窗口，默认阈值 0.6–0.7）+ Production Correlation（同全平台已收录 alpha 相似度）+ Peer Production Threshold。
7. **Region 奖金池**：USA 奖金池最大、Theme 最频繁；EUR、CHN、ASI 也有定期主题活动。公开用户仅能跑 USA，顾问可解锁 9+ 个区域。
8. **Dataset 优先级**：标准 pv 已被挖光，analyst/sentiment/option/model 还有空间。Learn → Theme Calendar 看当期主题。
9. **第三方工具**：官方允许用 API/脚本加速，但禁止账号共享、刷量；过度自动化但质量低劣会被 Grade 机制反噬。安全做法 = 工具加速挖掘 + 人工把关质量 + 严控每日提交量。

---

## 十、参考资料

### 官方页面
- BRAIN 平台首页：https://platform.worldquantbrain.com/
- BRAIN 顾问介绍：https://worldquantbrain.com/consultant
- IQC 2026 官方规则：https://www.worldquant.com/brain/iqc-guidelines/
- IQC 2026 中文版：https://www.worldquant.com/zh-hant/iqc-26/
- WorldQuant 官方新闻：https://www.worldquant.com/ideas/

### 公开技术文档与开源项目
- 开源 BRAIN 工具（详细 API 行为）：https://github.com/xiegengcai/world-quant-brain
- 简化版 BRAIN 客户端：https://github.com/rocky-d/wqb
- Alpha Generator 工具：https://github.com/zhutoutoutousan/worldquant-miner

### 实战经验与教程
- gentlecactus.top：BRAIN 平台指南（指标详解 + 提交标准）https://gentlecactus.top/archives/132
- BigQuant：寻找市场中的 Alpha（WorldQuant 设计理念）https://blog.csdn.net/bigquant/article/details/112693265
- scdifsn CSDN：世坤量化兼职体验（5 天上 1 万分）https://blog.csdn.net/scdifsn/article/details/145904641
- PearlOwl67 CSDN：Python 量化兼职初体验（顾问认证流程 + 收益）https://blog.csdn.net/PearlOwl67/article/details/154641045
- Yan_ks CSDN：EARN 顾问收入构成 https://blog.csdn.net/Yan_ks/article/details/147701524
- zurie CSDN：BRAIN Basics Chapter 6 Settings（区域 + Universe + Delay）https://blog.csdn.net/zurie/article/details/156424353
- Oo_Amy_oO CSDN：如何提高 alpha 质量（指标优化）https://blog.csdn.net/Oo_Amy_oO/article/details/147725000
- alphadoc.biglongxia.com：第六章 跑到 1 万分成为顾问 https://alphadoc.biglongxia.com/guide/06-一万分获得金牌
- eleduck 社区：WorldQuant BRAIN Consultant 招聘 https://eleduck.com/posts/OGfRbB
- brain-kr.com：2025 IQC 韩国赛区介绍 https://brain-kr.com/
- proginn.com：SuperAlpha 自动挖掘工具（多线程 + 进化算法）https://www.proginn.com/w/1576270

### 第三方解读与新闻
- briefglance.com：WorldQuant IQC 2026 启动 + BRAIN 平台解读 https://briefglance.com/articles/worldquants-global-hunt-for-quant-talent-enters-the-ai-era
- aicodingedu.org：WorldQuant Training 课程 https://www.aicodingedu.org/course_webpages/WorldQuant.html

### 相关社区
- BRAIN 平台韩国论坛：https://qr.wqbrain.com/krforum

---

> **免责声明**：本研究综合官方宣传、官方竞赛规则、第三方开源代码与顾问社区实战经验整理而成。涉及到"具体奖金数额""Region 奖金池大小"等数据，可能随平台政策、季度活动而变化，请在做出决策前以 BRAIN 平台账户内的最新规则为准。
