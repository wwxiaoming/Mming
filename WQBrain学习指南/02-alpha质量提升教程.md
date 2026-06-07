# Alpha 质量提升教程：从"能跑"到"跑得好"

> **副标题**：5 个指标优化 + 6 类经典模式 + 5 个改造方向 + 7 天质量飞跃
>
> **前提**：你已经按"01-平台实操教程"跑出第一条 alpha
>
> **贯穿示例**：你的 anl4 alpha
> ```python
> group_neutralize(
>     ts_decay_linear(
>         ts_backfill(anl4_adjusted_netincome_ft, 120),
>         240
>     ),
>     densify(subindustry)
> )
> ```

---

## 0. 质量提升的底层逻辑

### 0.1 一句话总结
> **质量 = (Sharpe × Returns) / (Turnover × Self-Correlation)**
>
> 你的 alpha 要么是"赚得稳"、要么是"赚得多"、要么是"换手低"、要么是"和别人不撞"

### 0.2 5 个指标的优先级
1. **Sharpe** （最核心，过线才能提交）
2. **Fitness** （综合指标，比 Sharpe 严苛）
3. **Self-Correlation** （最容易被判挂）
4. **Turnover** （决定实际能赚多少）
5. **Drawdown** （决定能不能扛住回撤）

### 0.3 质量提升的 3 个方向
- **A. 改表达式逻辑**（换数据集、换算子、改窗口）
- **B. 改配置**（Region/Universe/Delay/Neutralization）
- **C. 加组合/过滤**（叠加多个信号、加 trade_when）

---

## 1. Sharpe 优化：让 alpha 赚得更"稳"

### 1.1 Sharpe 低的 4 个常见原因
| 原因 | 表现 | 修复 |
|---|---|---|
| 信号太弱 | 长期横盘，收益小 | 换数据集、加强度 |
| 信号太杂 | 短期波动大 | 加 trade_when 过滤、加衰减 |
| 周期不匹配 | 时间窗口不对 | 改 ts_decay_linear 的 d 参数 |
| 中性化不当 | 行业 β 残留 | 换中性化层级 |

### 1.2 你的 anl4 alpha 怎么优化 Sharpe

#### 技巧 1：把"水平值"改成"60 天变化量"
```python
# 原版（用水平值，信号较平）
group_neutralize(
    ts_decay_linear(ts_backfill(anl4_adjusted_netincome_ft, 120), 240),
    densify(subindustry)
)
# 改造（用 60 天变化量，抓"分析师修订"）
group_neutralize(
    ts_decay_linear(ts_delta(anl4_adjusted_netincome_ft, 60), 120),
    densify(subindustry)
)
```
> **原理**：抓"分析师最近把预测调高还是调低"，信号更强

#### 技巧 2：缩短回填窗口，让信号更"新鲜"
```python
# 把 120 改成 60
ts_backfill(anl4_adjusted_netincome_ft, 60)
```
> **原理**：防止"远古预测"影响现在判断

#### 技巧 3：叠加多窗口
```python
# 双时间窗口（短期+长期共振）
group_neutralize(
    0.5 * ts_decay_linear(anl4_adjusted_netincome_ft, 60) +
    0.5 * ts_decay_linear(anl4_adjusted_netincome_ft, 240),
    densify(subindustry)
)
```

### 1.3 实战 SOP
- **Sharpe < 1.25** → 直接放弃，不要死磕
- **Sharpe 1.25 ~ 1.5** → 用上面 3 个技巧
- **Sharpe 1.5 ~ 2.0** → 微调参数即可
- **Sharpe > 2.0** → 太好了，**多跑几条类似的**

---

## 2. Fitness 优化：性价比 × 持久性

### 2.1 Fitness 公式
```
Fitness = Sharpe × √(|Returns| / Turnover)
```

### 2.2 4 种组合下的优化策略
| 场景 | Sharpe | Returns | Turnover | 优化方向 |
|---|---|---|---|---|
| Sharpe 高、Returns 高、Turnover 低 | ✓ | ✓ | ✓ | **已最优**，提交 |
| Sharpe 高、Returns 低 | ✓ | ✗ | - | 加过滤、抓短期信号 |
| Sharpe 高、Turnover 高 | ✓ | - | ✗ | 加 trade_when 控频 |
| Sharpe 低、Returns 高 | ✗ | ✓ | - | 加衰减/平滑 |

### 2.3 ⭐ 你的 anl4 alpha 的常见组合
- 如果 Returns 高、Turnover 也高 → 加大 decay 窗口（240 → 480）
- 如果 Returns 低、Turnover 低 → 加大 ts_decay 强度
- 如果 Returns 高、Turnover 适中 → **直接提交**，这是金组合

### 2.4 关键参数速查
| 想提升 | 调整方向 |
|---|---|
| Fitness | 平衡 Sharpe 和 Turnover |
| Sharpe（信号强度）| 改数据集/算子 |
| Returns（绝对收益）| 改窗口长度 |
| Turnover（换手）| 改 decay 窗口或加 trade_when |

---

## 3. Self-Correlation 优化：避免撞库

### 3.1 撞库的 3 大原因
1. **同数据集 + 同算子** → 平台上有几千人跑过
2. **同 Region + 同 Delay** → 标准配置 = 标准撞库
3. **同中性化层级** → 越细的中性化撞库越严重（Subindustry > Industry > Sector > Market）

### 3.2 你的 anl4 alpha 当前 Self-Correlation
从你之前的截图看：
- 一阶段 anl4+SUBINDUSTRY：0.6%（已废）
- 二阶段 anl4+MARKET：5.4%
- 三阶段 anl4+MARKET：8.5% ⭐

> **结论**：换 Subindustry → Market 后，撞库率反而上升（因为跑的人少）

### 3.3 ⭐ 降 Self-Correlation 的 5 个实战技巧

#### 技巧 1：换数据集
```python
# 原来：anl4
ts_backfill(anl4_adjusted_netincome_ft, 120)
# 改成：fundamental6
ts_backfill(fun6_pe_ratio, 120)
```

#### 技巧 2：换中性化层级
```python
# 原来：Subindustry
densify(subindustry)
# 改成：Industry
densify(industry)
```

#### 技巧 3：加 trade_when
```python
trade_when(volume > 1000000, your_signal, 0)
```

#### 技巧 4：换算子
```python
# 原来：ts_decay_linear
ts_decay_linear(x, 240)
# 改成：ts_decay_exp
ts_decay_exp(x, 240)
```

#### 技巧 5：换字段后缀
```python
# 原来：_ft
anl4_adjusted_netincome_ft
# 改成：_f1 / _fy1 / _eps_mean
anl4_adjusted_netincome_f1
anl4_eps_mean
```

### 3.4 实战 SOP
- **Self-Corr > 0.7** → 必须改
- **Self-Corr 0.5 ~ 0.7** → 改 1 个维度（数据集/中性化/算子）
- **Self-Corr < 0.5** → 提交，但**记录下来**作为模板

---

## 4. Turnover 优化：降频提效

### 4.1 Turnover 高的 4 个原因
1. **信号变化剧烈**（用 ts_delta 而非 ts_decay_linear）
2. **横截面操作多**（用 rank/quantile 频繁重排）
3. **delay = 0**（T+0 调仓，换手极高）
4. **truncation 过大**（截断导致信号跳变）

### 4.2 4 个降 Turnover 的方法

#### 方法 1：把 ts_delta 改成 ts_decay_linear
```python
# 原来（高换手）
ts_delta(anl4_adjusted_netincome_ft, 60)
# 改成（低换手）
ts_decay_linear(anl4_adjusted_netincome_ft, 240)
```

#### 方法 2：加 trade_when 控频
```python
trade_when(
    ts_rank(your_signal, 20) > 0.7,  # 只在信号强时开仓
    your_signal,
    0
)
```

#### 方法 3：把 delay 从 0 改成 1
- T+0 → T+1 调仓
- 直接降换手 30%~50%

#### 方法 4：加 quantile 分桶
```python
quantile(your_signal, 5)  # 分 5 档，信号跳变更平滑
```

### 4.3 你的 anl4 alpha 已经用 ts_decay_linear + Delay=1，所以 Turnover 应该不高
- 如果 Turnover > 30% → 检查是不是中性化层级太细
- 如果 Turnover < 10% → 考虑加大信号强度（避免"几乎不交易"）

---

## 5. Drawdown 优化：抗回撤能力

### 5.1 4 种回撤类型
| 类型 | 表现 | 修复 |
|---|---|---|
| 长期阴跌 | 收益缓慢下降 | 改信号逻辑 |
| 短期跳水 | 某天突然 -5% | 加 trade_when 加过滤 |
| 行业集中踩雷 | 某个行业暴跌 | 中性化不够细 |
| 周期错配 | 牛熊切换失灵 | 改时间窗口 |

### 5.2 实战建议
- **Drawdown < 5%** → 安全
- **Drawdown 5% ~ 10%** → 注意
- **Drawdown 10% ~ 20%** → 危险
- **Drawdown > 20%** → 别交

### 5.3 你的 anl4 alpha 通常 Drawdown 较低
- 分析师预测是慢变量，回撤不会很剧烈
- 但**极端市场**（如 2008、2020）回撤会放大

---

## 6. 6 类经典 alpha 模式（必学）

### 6.1 动量（Momentum）
```python
# 经典：20 日价格变化
ts_delta(close, 20)
```
> 适用：趋势市

### 6.2 反转（Reversal）
```python
# 经典：5 日反转
-ts_delta(close, 5)
```
> 适用：震荡市

### 6.3 质量（Quality）
```python
# 经典：ROE 排名
rank(roe)
```
> 适用：长期持有

### 6.4 价值（Value）
```python
# 经典：低 PE
-rank(pe_ratio)
```
> 适用：低估反弹

### 6.5 情绪（Sentiment）
```python
# 经典：分析师预测修订
ts_decay_linear(ts_delta(anl4_eps_mean, 60), 240)
```
> **你的 anl4 风格就是这种** ⭐

### 6.6 波动率（Volatility）
```python
# 经典：低波动率
-ts_std_dev(returns, 60)
```
> 适用：避险

### 6.7 ⭐ 6 类对比表
| 模式 | 核心逻辑 | 数据集 | 难度 |
|---|---|---|---|
| 动量 | 涨了的还会涨 | pv1 | 简单 |
| 反转 | 跌了的会反弹 | pv1 | 简单 |
| 质量 | 好公司更赚钱 | fundamental6 | 中等 |
| 价值 | 便宜的有上涨空间 | fundamental6 | 中等 |
| 情绪 | 分析师预期反映基本面 | analyst4 | 中等 |
| 波动率 | 稳定的更安全 | option8 / pv1 | 中等 |

---

## 7. 5 个改造方向（实战模板）

### 方向 1：换数据集
```python
# 原来
ts_backfill(anl4_adjusted_netincome_ft, 120)
# 改成（基本面 + 量价）
ts_backfill(anl4_eps_mean, 120) * rank(pv1_volume)
```

### 方向 2：换算子
```python
# 原来
ts_decay_linear(x, 240)
# 改成（指数衰减更"重视最近"）
ts_decay_exp(x, 240)
```

### 方向 3：改窗口
```python
# 原来
ts_decay_linear(x, 240)
# 改成（缩短窗口）
ts_decay_linear(x, 120)
```

### 方向 4：加 trade_when 过滤
```python
# 原来
group_neutralize(signal, densify(subindustry))
# 改成（只在流动性好时开仓）
group_neutralize(
    trade_when(volume > 100000, signal),
    densify(subindustry)
)
```

### 方向 5：多信号共振
```python
# 三源共振模板（推荐尝试）
signal_fundamental = rank(roe)
signal_analyst    = ts_decay_linear(ts_delta(anl4_eps_mean, 60), 240)
signal_technic    = ts_rank(close / volume, 20)
composite = signal_fundamental * signal_analyst * signal_technic
group_neutralize(composite, densify(industry))
```

---

## 8. 调试诊断 SOP

### 8.1 指标不达标时的诊断顺序
```
Sharpe < 1.25（最严重）
  ↓ 检查算子是否合规
  ↓ 检查字段是否选对
  ↓ 换数据集重试
  → 实在不行就放弃

Self-Correlation > 0.7
  ↓ 换数据集（最有效）
  ↓ 换中性化层级
  ↓ 换算子
  → 至少改 2 个维度

Turnover > 70%
  ↓ 把 ts_delta 改成 ts_decay_linear
  ↓ 加 trade_when
  ↓ Delay 改 1

Drawdown > 20%
  ↓ 加 trade_when 过滤
  ↓ 中性化改 Industry
  ↓ 缩短时间窗口
```

### 8.2 5 个常见"伪修复"（看起来改了但没改）
| 伪修复 | 为什么无效 |
|---|---|
| 只改 delay 0 → 1 | 不算真正的"差异化" |
| 只换 Region（USA → ASI）| 公开账户不能用 ASI |
| 加 `+ 0.0001` | 噪声降重 = 违规 |
| 改时间窗口但不改其他 | 撞库率仍然高 |
| 改字段后缀但数据相同 | 平台不认 |

### 8.3 真有效的"必杀技"组合
- **3 维度改 2 个**：数据集 + 中性化 + 算子，至少改 2 个
- **加新数据集交叉**：用 2-3 个数据集的信号相乘
- **加 trade_when 控频**：同时降低 Turnover 和 Self-Corr
- **换 decay 类型**：linear vs exp 是真差异

---

## 9. 7 天质量提升计划

### Day 1：通读 + 跑通基线
- 通读本教程
- 跑 1 次你现有的 anl4 alpha
- **记录 5 个指标的基线值**

### Day 2-3：换数据集实验
- 把 anl4 换成 anl4_eps_mean、anl4_revenue_ft
- 跑 5 次，对比 Sharpe/Fitness
- **找 Sharpe 最高的字段**

### Day 4-5：换中性化实验
- 把 Subindustry 换成 Industry、Sector、Market
- 跑 3-5 次
- **找 Self-Correlation 最低的配置**

### Day 6：加 trade_when
- 给最优的版本加 trade_when
- 跑 2-3 次
- **看 Turnover 能否降到 20% 以下**

### Day 7：提交
- 选 1-2 条最优的提交
- 截图保存
- **作为模板记录下来**

---

## 10. ⭐ 长期质量提升的核心心法

### 心法 1：质量 > 数量
- 每天 1 条 Sharpe 1.8 的 alpha > 每天 10 条 Sharpe 1.3 的
- 顾问阶段每天只算前 4 个的钱

### 心法 2：3 维度改 2 个
- 数据集 / 中性化 / 算子 = 3 个维度
- 至少改 2 个才算"真差异化"

### 心法 3：先理解，再跑数
- 不理解金融逻辑就改参数 = 撞库
- 理解后改 = 创新

### 心法 4：记录 + 复盘
- 每次跑 alpha 截图保存 5 个指标
- 每周复盘：哪些表达式成功了？为什么？
- 建立**个人 alpha 武器库**

### 心法 5：从"水平值"到"变化量"
- `ts_backfill(x, n)` 看的是"现在的值"
- `ts_delta(x, n)` 看的是"变化方向"
- **后者信号更强，撞库率更低**

---

## 11. 自检清单（每天跑 alpha 前必看）

- [ ] 我能讲清这条 alpha 的金融逻辑
- [ ] 我知道它在抓哪个信号（动量/反转/质量/价值/情绪/波动率）
- [ ] 我至少改了 2 个维度（数据集/中性化/算子）
- [ ] 我预计 Sharpe > 1.25
- [ ] 我预计 Self-Correlation < 0.7
- [ ] 我预计 Turnover 在 10%-30% 区间
- [ ] 我知道这条 alpha 的潜在风险

---

## 12. 资源链接

- 你的 anl4 alpha 改造案例：见 `学习记录.md` 第 5.4 节
- 算子速查：见 `学习记录.md` 附录 B
- 经典 alpha 模式：见 `学习记录.md` 附录 C
- 降重 10 招：见 `学习记录.md` 第 6 章

---

**下一步**：跑出第一条 alpha → 用 5 个改造方向各试一次 → 找到你的"专属模板" → 提交 1-2 条 → 截图给我看。
