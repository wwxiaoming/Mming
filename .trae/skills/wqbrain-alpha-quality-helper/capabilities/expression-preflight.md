# expression-preflight（表达式预审）

> 在学员把一阶段产物送进二阶段前，对 Fast Expression 做"结构拆解 + 陷阱扫描"，提前拦截过弱、缺中性化、市场暴露过强等红灯。

---

## 1. 能力定位

**一句话**：把学员贴出的一段 Fast Expression 拆成 Arithmetic / Logical / Time Series 三类操作，自动跑 5 条"陷阱检测"，再给出 ≥ 3 条可执行改写建议，**对接到 [`audit-report.md`](../../templates/audit-report.md) 的"风险点 + 调整建议"两节**。

---

## 2. 触发场景

学员从老强工具"挖掘"列表里看到一条 alpha 表达式，犹豫要不要送二阶段 / 直接提交，贴出来问"这个能过吗"。

- 学员原话示例：
  - "这条 `(high + low)/2 - close` 是不是太简单了？能过提交吗？"
  - "我写了 `rank(ts_mean(volume,10))`，看着挺干净，有没有坑？"
  - "trade_when 里我写了 `> 0.5`，这样条件是不是太松？"
  - "我这条用了 `ts_rank(x, 250)`，窗口这么长合理吗？"

---

## 3. 输入格式

学员要贴出一段 Fast Expression 文本（可多行），可附 Dataset / Region / Delay 上下文：

| 字段 | 是否必填 | 说明 |
| --- | --- | --- |
| 表达式 | 必填 | 一行或多行 Fast Expression |
| Dataset | 选填 | 用于判断字段是否在 [dataset-cheatsheet.md](../references/dataset-cheatsheet.md) 中合法 |
| Region | 选填 | 用于判断 Delay / 中性化是否配套 |
| Delay | 选填 | 0 / 1，与 Region 配合判断 |

**输入示例**：

```
表达式: (high + low)/2 - close
Dataset: pv1
Region: USA
Delay: 1
```

---

## 4. 输出格式

**复用 [`audit-report.md`](../../templates/audit-report.md) 模板的"风险点列表 + 调整建议"两节**，新增"操作结构拆解"作为第一节独特内容。完整输出包含：

1. **操作结构拆解**（三大类：Arithmetic / Logical / Time Series + 字段列表）
2. **陷阱检测结果**（5 条规则，每条命中/未命中 + 触发原因）
3. **改写建议**（≥ 3 条，按 P0 / P1 / P2 排序）
4. **改写后表达式示例**（YAML 块）

> 模板填写规范见 [audit-report.md](../../templates/audit-report.md) 第三节、第四节。

---

## 5. 决策规则 / 评分细则

### 5.1 三大类操作识别

| 类别 | 标识符（关键字 / 函数） | 典型示例 |
| --- | --- | --- |
| **Arithmetic（算术）** | `+` `-` `*` `/`，以及括号包裹的字段组合 | `(high + low)/2`、`volume * 0.5` |
| **Logical（逻辑）** | `and` `or` `?` `:`，以及 `trade_when(...)` | `x > 0 and y < 1`、`close > open ? 1 : 0` |
| **Time Series（时序）** | `ts_*`、`decay_*`、`delta`、`delay` | `ts_mean(close, 5)`、`decay_linear(volume, 4)` |

> 拆解时按"从外到内"扫描：先看顶层是否是逻辑三目（`? :`），再看是否有时序函数调用，最后看算术组合。

### 5.2 5 条陷阱检测（必含）

| # | 规则 | 命中等级 | 默认建议 |
| --- | --- | --- | --- |
| 1 | **长度 < 20 字符** | 中 | 提示"信号可能过弱"，建议叠加 `rank()` + 时序衰减 |
| 2 | **完全没有 `rank` / `group_neutralize`** | 高 | 提示"未做横截面归一化"，必须加其一 |
| 3 | **Delay=0 且 Neutralization=None** | 高 | 提示"市场暴露过强"，与 [wq-submission-standards.md](../references/wq-submission-standards.md) 第四节 IQC 换手甜区冲突 |
| 4 | **`trade_when` 条件含 `> 0.5` 这种过松阈值** | 中 | 提示"条件过松"，建议收紧到 0.7-0.8 或结合分位数 |
| 5 | **时间窗口 < 5 或 > 252** | 中 | 提示"窗口异常"；< 5 偏噪声，> 252 偏长周期难解释 |

### 5.3 改写建议生成规则

每条建议必须满足：

- [ ] 指明"在表达式哪一段插入/替换"
- [ ] 给出具体的算子名与参数值（如 `decay_linear(volume, 5)`）
- [ ] 引用 [kpi-reference.md](../references/kpi-reference.md) 对应改进方向
- [ ] 标注优先级 P0 / P1 / P2

| 优先级 | 触发条件 | 典型动作 |
| --- | --- | --- |
| **P0** | 命中"市场暴露过强"或"无中性化" | 加 `group_neutralize(Subindustry)` + `rank()` |
| **P1** | 命中"长度过短"或"窗口异常" | 叠 `decay_linear(field, 4-6)` 或 `ts_rank(field, 10-20)` |
| **P2** | 命中"条件过松"或风格优化 | 收紧 `trade_when` 阈值、加 `truncation=0.05` |

### 5.4 字段合法性检查（按 [dataset-cheatsheet.md](../references/dataset-cheatsheet.md)）

- 字段必须出现在所选 Dataset 的字段集合内（如 pv1 有 `open/high/low/close/volume/returns`，fundamental6 有 `sales/eps/roe/...`）。
- 跨数据集字段混用时，检查时间频率是否一致（高频 vs 低频），不一致建议插入 `ts_mean` / `ts_decay_linear` 对齐。

---

## 6. 工作示例

### 示例 A：极简算术式

**输入**：

```
表达式: (high + low)/2 - close
Dataset: pv1
Region: USA
Delay: 1
```

**期望输出**：

> **结构拆解**：
>
> - Arithmetic：`+` `/` `-` 三个算子
> - Time Series：隐含（`close` 默认取前一期，Delay=1）
> - Logical：无
> - 字段：`high` / `low` / `close`，均属 pv1
>
> **陷阱检测**：
>
> - 1. 长度 21 字符（合规）
> - 2. 完全没有 `rank` / `group_neutralize` —— **命中**，等级 = 高
> - 3. Delay=1（合规）
> - 4. 无 `trade_when`（合规）
> - 5. 无时序窗口（合规）
>
> **改写建议**：
>
> - **P0**：在表达式外层套 `rank(...)`，再叠 `group_neutralize(sector)`，消除行业偏差。
> - **P0**：加 `truncation=0.05` 抑制极值。
> - **P1**：用 `ts_decay_linear((high+low)/2 - close, 4)` 替换原始算术，让信号更稳。
> - **改写后**：`rank(ts_decay_linear((high+low)/2 - close, 4))`，配合工具中 `truncation=0.05` / `neutralization=Subindustry`。
>
> **Checklist**：
> - [ ] 加 `rank()`
> - [ ] 加 `group_neutralize(Subindustry)`
> - [ ] truncation 设为 0.05
> - [ ] 重测后看 Sharpe 是否从噪声中浮出来

### 示例 B：干净的时序式

**输入**：

```
表达式: rank(ts_mean(volume, 10))
Dataset: pv1
Region: USA
Delay: 1
```

**期望输出**：

> **结构拆解**：
>
> - Arithmetic：无外层算术
> - Time Series：`ts_mean(volume, 10)`，窗口 10
> - Logical：无
> - 字段：`volume`（pv1 合法）
>
> **陷阱检测**：
>
> - 1. 长度 27 字符（合规）
> - 2. 有 `rank`，但**无 `group_neutralize`** —— **命中（部分）**，等级 = 中
> - 3. Delay=1（合规）
> - 4. 无 `trade_when`（合规）
> - 5. 窗口 10 落在 5-252 区间（合规）
>
> **改写建议**：
>
> - **P0**：加 `group_neutralize(Subindustry)`，避免不同子行业成交量绝对值差异主导排序。
> - **P1**：把 `ts_mean` 换为 `decay_linear(volume, 5)`，给近期量更高权重，更利趋势捕捉。
> - **P1**：加 `trade_when(volume > ts_mean(volume, 20), alpha, ...)` 过滤极值交易日的无效信号。
> - **P2**：外层再叠一层 `ts_rank(..., 20)` 抑制短期反转噪声。
> - **改写后**：`rank(decay_linear(volume, 5))`，配合 `group_neutralize(Subindustry)` + `trade_when` 过滤。
>
> **Checklist**：
> - [ ] 把 `ts_mean` 换为 `decay_linear(volume, 5)`
> - [ ] 加 `group_neutralize(Subindustry)`
> - [ ] 加 `trade_when` 极值过滤
> - [ ] 重测后看 Turnover 是否从 0.5 降到 0.3

---

## 7. 引用清单

- [wq-submission-standards.md](../references/wq-submission-standards.md) —— IQC 加分指标中的换手甜区、中性化与分组要求。
- [kpi-reference.md](../references/kpi-reference.md) —— 改进优先级、Sharpe / Fitness / Turnover 改进方向。
- [dataset-cheatsheet.md](../references/dataset-cheatsheet.md) —— 字段合法性、数据集推荐运算符组合方向。
- [audit-report.md](../../templates/audit-report.md) —— 本能力产出的报告模板。
