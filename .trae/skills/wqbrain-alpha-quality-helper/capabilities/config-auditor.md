# config-auditor（配置审查器）

> 对 WorldQuant BRAIN 一阶段挖掘参数与三阶段精筛阈值做"合理性体检"，给出 0-100 分与可执行的参数调整清单。

---

## 1. 能力定位

**一句话**：按 [wq-submission-standards.md](../references/wq-submission-standards.md) 的硬性条件与 [dataset-cheatsheet.md](../references/dataset-cheatsheet.md) 的数据集惯例，对学员贴出的"一/二/三阶段参数"做合规打分 + 风险分级 + 调参建议，**对接到 [`audit-report.md`](../../templates/audit-report.md) 模板**。

---

## 2. 触发场景

学员在老强工具（v1.0.5）里点完"一阶段"或"三阶段"配置按钮后，把参数贴出来问"这样配行不行"。

- 学员原话示例：
  - "帮我审一下这个一阶段配置，USA / Delay=1 / Decay=4，Sharpe 阈值只填了 0.5，能跑出可提交的 alpha 吗？"
  - "三阶段我把 Sharpe 提到 1.25、Fitness 提到 1.0，LongShortMin 留 100，你看合理吗？"
  - "我准备用 pv1 + None 中性化 + Decay=0 跑一阶段，这样会不会全是市场暴露？"
  - "Max Run 我设了 6000，仿真额度吃得消吗？"

---

## 3. 输入格式

学员要贴出一张参数表，至少包含下列字段（缺一不可，缺失项由审计器按"未填写"计为"中风险"）：

| 字段 | 是否必填 | 说明 |
| --- | --- | --- |
| 阶段 | 必填 | 一阶段 / 二阶段 / 三阶段 |
| Dataset | 必填 | 例如 `analyst4` / `pv1` / `fundamental6` |
| Region | 必填 | USA / CHN / EUR / ASI / GLB 等 |
| Delay | 必填 | 0 或 1（USA 必为 1） |
| Neutralization | 必填 | None / Market / Industry / Subindustry / Sector / Country |
| Decay | 必填 | 整数，建议 0-8 |
| Max Run | 必填 | 仿真次数上限 |
| Sharpe 阈值 | 必填 | 浮点数 |
| Fitness 阈值 | 必填 | 浮点数 |
| LongShortMin | 必填 | 多空最低股票数 |

可选：Truncation、Max Trade、Universe（TOP3000/TOP2000 等）、Group。

**输入示例**：

```yaml
阶段: 一阶段
Dataset: analyst4
Region: USA
Delay: 1
Neutralization: Subindustry
Decay: 4
Max Run: 2000
Sharpe 阈值: 0.75
Fitness 阈值: 0.5
LongShortMin: 100
```

---

## 4. 输出格式

按 [`audit-report.md`](../../templates/audit-report.md) 模板填充，重点产出以下五块：

1. **基本信息**（审查对象、阶段、数据集、区域）
2. **合理性评分**（0-100 分，分 5 个维度加权）
3. **风险点列表**（高/中/低 + 触发参数 + 后果）
4. **调整建议**（具体到参数值 + 调整前后对比 + 操作 Checklist）
5. **参考配置块**（修改后的 YAML）

> 模板填写规范见 [audit-report.md](../../templates/audit-report.md)，分数阈值与扣分点见第 5 节"决策规则"。

---

## 5. 决策规则 / 评分细则

### 5.1 五维评分（合计 100 分）

| 维度 | 权重 | 满分条件 | 扣分点 |
| --- | --- | --- | --- |
| 平台与 Delay 一致性 | 20 | Dataset 主流 + Delay=1（USA）/ Delay=0（CHN）| Delay=0 + USA 高换手字段直接扣 12 分 |
| 阈值与样本量 | 20 | Sharpe 阈值 0.75-1.25；Fitness 阈值 0.5-1.0 | Sharpe < 0.75 视为"过松"扣 8 分；Fitness < 0.5 扣 4 分 |
| 分组与池子选择 | 20 | Neutralization 与 Group 一致且匹配数据集 | None 中性化扣 10 分；中性化维度与数据源不匹配扣 6 分 |
| 衰减 / 持仓 / 换仓 | 20 | Decay 3-7、Max Trade 3-10、Truncation 0.05-0.10 | Decay=0 扣 8 分；Decay 与 Neutralization 不配合扣 6 分 |
| 多空最低要求 | 20 | LongShortMin ≥ 100 且 ≤ 200 | < 100 扣 8 分；> 200 在窄分组上易触发"无解"扣 4 分 |

### 5.2 必含硬规则（高风险触发条件）

- [ ] **Sharpe 阈值 ≥ 0.75 才算"种子门槛"**；< 0.75 视为"过松"，风险等级 = 中。
- [ ] **Sharpe 阈值 ≥ 1.25** 才算"提交门槛"；1.0-1.25 视为"种子门槛"，用于二阶段，不要直接提交。
- [ ] **Max Run > 5000** 提示"过耗仿真额度"风险 = 中；建议在挖到种子后改回 2000-3000。
- [ ] **Dataset 不是 USA 主流 dataset**（非 pv1 / fundamental6 / analyst4 / model16 / model51 / option8）时，提示"流动性风险"= 中，并建议补充 `univ1` 收口。
- [ ] **Decay 与 Neutralization 必须配合**：`Subindustry` + `Decay 3-7` 是稳定组合；`Decay=0` + `None` = 红线，扣 12 分。
- [ ] **USA + Delay=0** = 红线，直接扣 12 分（违反 [wq-submission-standards.md](../references/wq-submission-standards.md) 第四节"IQC 加分指标"的换手甜区）。
- [ ] **LongShortMin < 100** 在 TOP3000 + Subindustry 分组下极易触发"多空数不足"，扣 8 分。

### 5.3 数据集适配速查（按 [dataset-cheatsheet.md](../references/dataset-cheatsheet.md)）

| Dataset | 推荐 Region | 推荐 Neutralization | 推荐 Decay | 备注 |
| --- | --- | --- | --- | --- |
| pv1 | USA / CHN | Subindustry | 3-7 | 必加 `univ1` 收口 |
| fundamental6 | USA / CHN | Industry | 0-3 | 低频字段，Decay 短 |
| analyst4 | USA | Subindustry | 3-5 | 配合 ts_mean 修正趋势 |
| model16 / model51 | USA | Industry | 0-3 | 第三方评分，中性化即可 |
| option8 / option9 | USA | Sector | 5-8 | 波动率因子用长 Decay |
| news12 / news18 | USA | Sector | 5-7 | 新闻热度做时间衰减 |
| socialmedia8 / socialmedia12 | USA | Subindustry | 4-6 | 散户情绪短周期 |

### 5.4 风险等级

- **高（High）**：直接导致回测失真或不可提交，必须修改。
- **中（Medium）**：可能导致 Sharpe / Fitness 虚高、过拟合或样本不足。
- **低（Low）**：风格偏好或可优化项。

### 5.5 与 KPI 速查的对照

| 检查项 | 引用 |
| --- | --- |
| Sharpe / Fitness / Turnover 阈值 | [kpi-reference.md](../references/kpi-reference.md) 一节 |
| Self Correlation 红线 < 0.7 | [wq-submission-standards.md](../references/wq-submission-standards.md) 一节 |
| 改进优先级 | [kpi-reference.md](../references/kpi-reference.md) 三节 |
| 数据集运算符方向 | [dataset-cheatsheet.md](../references/dataset-cheatsheet.md) 九节 |

---

## 6. 工作示例

### 示例 A：默认配置（合格偏弱）

**输入**：

```yaml
阶段: 一阶段
Dataset: analyst4
Region: USA
Delay: 1
Neutralization: Subindustry
Decay: 4
Max Run: 2000
Sharpe 阈值: 0.75
Fitness 阈值: 0.5
LongShortMin: 100
```

**期望输出（摘要）**：

> **综合评分：70 / 100**
>
> - **风险点（中）**：
>   - 1. "种子门槛 ≠ 提交门槛"——Sharpe 0.75 是一阶段筛种子的合理值，但若直接拿这个一阶段产物去提交会全部卡在 1.25 红线下。
>   - 2. LongShortMin=100 在 Subindustry 分组下部分行业多空数 < 100，会触发"无解"。
>   - 3. Fitness 0.5 处于推荐区间下沿，建议提到 0.7。
> - **调整建议**：
>   - 三阶段 Sharpe 阈值 → **1.25**，Fitness 阈值 → **1.0**；
>   - LongShortMin → 留 100，但加 fallback：若分组内不足 100 则回退 Industry；
>   - 配合 [kpi-reference.md](../references/kpi-reference.md) 第一节"Sharpe 改进方向"加 `rank()` 与 `decay_linear`。
> - **Checklist**：
>   - [ ] 三阶段 Sharpe 1.25 / Fitness 1.0
>   - [ ] 在工具里"二阶段 → 三阶段"勾选"复用一阶段 Sharpe 阈值"为 false

### 示例 B：坏配置（红线级）

**输入**：

```yaml
阶段: 一阶段
Dataset: pv1
Region: USA
Delay: 0
Neutralization: None
Decay: 0
Max Run: 2000
Sharpe 阈值: 0.3
Fitness 阈值: 0.2
LongShortMin: 50
```

**期望输出（摘要）**：

> **综合评分：30 / 100**
>
> - **风险点（高）**：
>   - 1. **市场暴露过强**：`Neutralization=None` + `Delay=0` + `Decay=0` 同时触发，红线组合，预期产物的 Self Correlation 普遍 > 0.8。
>   - 2. **Sharpe 门槛过低**：0.3 会让纯噪声因子通过，跑出一堆"看起来有 alpha"但提交必被拒的废品。
>   - 3. **LongShortMin=50**：在 Subindustry 缺省时实际分组可能落到 30 上下，多空结构不稳。
>   - 4. **Delay=0 + USA 价量字段**：与 [wq-submission-standards.md](../references/wq-submission-standards.md) 第四节"IQC 加分指标"推荐的换手甜区（0.1-0.9）冲突。
> - **调整建议**：
>   - `Delay 0 → 1`；`Neutralization None → Subindustry`；`Decay 0 → 4`；`Sharpe 0.3 → 0.75`；`LongShortMin 50 → 100`。
>   - 改完后回到一阶段重跑，预期通过率从 ~5% 升到 ~25%。
> - **Checklist**：
>   - [ ] Delay 改为 1
>   - [ ] Neutralization 改为 Subindustry
>   - [ ] Decay 改为 4
>   - [ ] Sharpe 阈值改为 0.75、Fitness 改为 0.5
>   - [ ] LongShortMin 改为 100

---

## 7. 引用清单

- [wq-submission-standards.md](../references/wq-submission-standards.md) —— Sharpe / Fitness / Self Correlation 硬性条件、IQC 加分指标。
- [kpi-reference.md](../references/kpi-reference.md) —— 7 大指标合格线、改进方向与优先级。
- [dataset-cheatsheet.md](../references/dataset-cheatsheet.md) —— 数据集分类、推荐运算符组合方向。
- [audit-report.md](../../templates/audit-report.md) —— 本能力产出的报告模板。
