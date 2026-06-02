# result-diagnostician（回测结果诊断）

> 对学员贴出的单次/批量回测 JSON，按 [kpi-reference.md](../references/kpi-reference.md) 的 7 大指标逐项解读，给出"达标 / 边缘 / 不达标"状态 + P0/P1/P2 改进动作清单，**对接到 [`diagnosis-report.md`](../../templates/diagnosis-report.md) 模板**。

---

## 1. 能力定位

**一句话**：把一份回测 JSON（Sharpe / Fitness / Turnover / Drawdown / Returns / Self Correlation / 可选 Margin）按指标逐项打分，定位瓶颈指标，给出可执行改进动作，**对接到 [`diagnosis-report.md`](../../templates/diagnosis-report.md) 模板**。

---

## 2. 触发场景

学员在老强工具"Alphas"或"统计"页拿到回测结果，贴出来问"还能救吗 / 能不能交"。

- 学员原话示例：
  - "Sharpe 1.05 还能救吗？"
  - "Fitness 才 0.7、Turnover 0.65 是不是换手拖累了？"
  - "Self Correlation 0.72 算高吗？要改字段吗？"
  - "我这条 Sharpe 1.6、Fitness 1.3，是不是可以直接交？"

---

## 3. 输入格式

学员要贴出一段回测 JSON，**至少**含 6 个核心字段，可选 Margin：

| 字段 | 是否必填 | 说明 |
| --- | --- | --- |
| `sharpe` | 必填 | 夏普比率（年化） |
| `fitness` | 必填 | 健康度 |
| `turnover` | 必填 | 换手率（0-1） |
| `drawdown` | 必填 | 最大回撤（0-1） |
| `returns` | 必填 | 年化收益（0-1） |
| `self_correlation` | 必填 | 与历史 alpha 的相关性 |
| `margin` | 选填 | 多空对冲安全边际 |

可附：表达式、Dataset、Region、Delay、中性化（用于交叉解读）。

**输入示例**：

```json
{
  "sharpe": 1.05,
  "fitness": 0.7,
  "turnover": 0.65,
  "drawdown": 0.18,
  "returns": 0.12,
  "self_correlation": 0.62
}
```

---

## 4. 输出格式

**完全按 [`diagnosis-report.md`](../../templates/diagnosis-report.md) 模板填充**，包含四节：

1. **基本信息**（模拟 ID、表达式、数据集、Delay、中性化）
2. **指标逐项解读**（7 大指标，状态 = 达标/边缘/不达标）
3. **改进动作清单**（P0/P1/P2 + 经验性参数区间）
4. **状态汇总**（达标 N / 边缘 N / 不达标 N + 综合结论）

> 模板填写规范见 [diagnosis-report.md](../../templates/diagnosis-report.md) 全文。

---

## 5. 决策规则 / 评分细则

### 5.1 Sharpe 状态分级（最核心）

| Sharpe 区间 | 状态 | 含义 | 默认建议 |
| --- | --- | --- | --- |
| **< 1.0** | 不达标 | 边缘 | 必须重做，加 `rank` + 调整 `decay` |
| **1.0 ≤ Sharpe < 1.25** | 边缘 | 接近门槛、但不能提交 | 再优化一轮，再观察 |
| **1.25 ≤ Sharpe < 1.5** | 达标 | 满足 [wq-submission-standards.md](../references/wq-submission-standards.md) 硬性条件 | 可考虑提交 |
| **1.5 ≤ Sharpe < 1.62** | 达标（IQC） | 显著高于 1.25 红线 | 强烈建议提交 |
| **≥ 1.62** | 强 IQC | 进入"准精选"区 | 直接提交，配合 Self Correlation 豁免条款 |

> 阈值依据：[wq-submission-standards.md](../references/wq-submission-standards.md) 第一节"三硬性条件"与第四节"IQC 加分指标"。

### 5.2 7 大指标合格线（按 [kpi-reference.md](../references/kpi-reference.md)）

| 指标 | 不达标 | 边缘 | 达标 | 强达标（IQC） |
| --- | --- | --- | --- | --- |
| Sharpe | < 1.0 | 1.0-1.25 | 1.25-1.5 | ≥ 1.5 |
| Fitness | < 0.5 | 0.5-1.0 | 1.0-1.5 | ≥ 1.5 |
| Turnover | > 0.9 或 < 0.1 | 0.7-0.9 或 0.1-0.2 | 0.2-0.7 | 0.1-0.5 |
| Returns | < 0.05 | 0.05-0.10 | 0.10-0.15 | ≥ 0.15 |
| Drawdown | > 0.30 | 0.20-0.30 | 0.10-0.20 | ≤ 0.10 |
| Margin | < 0.03 | 0.03-0.05 | 0.05-0.10 | ≥ 0.10 |
| Self Correlation | ≥ 0.8 | 0.7-0.8 | 0.5-0.7 | ≤ 0.5 |

### 5.3 Self Correlation 红线分级（必须严格）

| Self Correlation | 风险等级 | 默认建议 |
| --- | --- | --- |
| **< 0.5** | 安全 | 可提交 |
| **0.5 - 0.6** | 边缘 | 改一组字段观察 |
| **0.6 - 0.7** | 风险 | 建议换字段 / 改中性化维度 |
| **0.7 - 0.8** | 高风险 | 必然被拒（除非 Sharpe > 1.375 豁免） |
| **≥ 0.8** | 必然被拒 | 必须重做 |

> 0.7 红线来自 [wq-submission-standards.md](../references/wq-submission-standards.md) 第一节"三硬性条件"；1.375 豁免条款见同文件第二节。

### 5.4 改进动作优先级

| 优先级 | 触发条件 | 典型动作 |
| --- | --- | --- |
| **P0** | Sharpe < 1.25；Self Correlation ≥ 0.7；Fitness < 0.5 | 必做：加 `rank` + 改中性化 + 改字段 |
| **P0** | Fitness 受 Turnover 拖累 | 优先压换手（`decay_linear` / 减少高频字段） |
| **P1** | Sharpe 1.0-1.25；Turnover > 0.7 | 调 `decay` 形态 + 提 `truncation` |
| **P1** | Drawdown > 0.20 | 检查单股集中 + 叠 1-2 个低相关辅助信号 |
| **P2** | Returns < 0.10；Margin < 0.05 | 减 `truncation` + 拉长持仓周期 |

> 优先级表与 [kpi-reference.md](../references/kpi-reference.md) 第三节保持一致。

### 5.5 综合结论判定

| 状态汇总 | 综合结论 |
| --- | --- |
| 不达标项 ≥ 2 | 建议丢弃，重做 |
| 不达标项 = 1（Sharpe 边缘） | 需优化后重测 |
| 全达标 + Sharpe ≥ 1.5 | 可提交（优先） |
| 全达标 + Sharpe 1.25-1.5 | 可提交 |
| 仅 Self Correlation 边缘（0.5-0.7） | 可提交，但观察 |

---

## 6. 工作示例

### 示例 A：边缘结果（Sharpe 1.05）

**输入**：

```json
{
  "sharpe": 1.05,
  "fitness": 0.7,
  "turnover": 0.65,
  "drawdown": 0.18,
  "returns": 0.12,
  "self_correlation": 0.62
}
```

**期望输出（摘要）**：

> **状态汇总**：
>
> - Sharpe 1.05 → **边缘**（不达标，离 1.25 差 0.2）
> - Fitness 0.7 → **边缘**（Fitness 0.5-1.0 区间）
> - Turnover 0.65 → **达标**（0.2-0.7）
> - Drawdown 0.18 → **达标**（≤ 0.20）
> - Returns 0.12 → **达标**（0.10-0.15）
> - Self Correlation 0.62 → **风险**（0.6-0.7）
>
> **综合结论**：需优化后重测。Sharpe 1.05 离 1.25 红线 0.2 个点，Self Correlation 0.62 处于"换字段"区间。
>
> **改进动作清单**：
>
> - **P0（Sharpe）**：加 `rank(...)`、把 `decay` 从当前值缩短 1-2 档，预期 Sharpe 提升 0.1-0.2。
> - **P0（Fitness）**：Fitness 0.7 < 1.0 且 Turnover 0.65 偏高，**优先压换手**：用 `decay_linear(volume, 5)` 把 Turnover 降到 0.3-0.4，预期 Fitness 升到 0.9-1.1。
> - **P0（Self Correlation）**：0.62 在"换字段"区间，建议替换 1-2 个贡献最大的字段，或把中性化从 `Industry` 换为 `Subindustry` / `Sector`。
> - **P1（Drawdown）**：0.18 略偏高，加 `truncation=0.08` 抑制单股集中，预期降至 0.12-0.15。
> - **P2（Returns）**：当前 0.12 达标，等上述调整自然回归到 0.13-0.15。
>
> **Checklist**：
>
> - [ ] 加 `rank(...)`
> - [ ] 缩短 `decay` 1-2 档
> - [ ] 引入 `decay_linear` 把 Turnover 压到 0.3-0.4
> - [ ] 替换 1-2 个字段 / 改中性化维度
> - [ ] `truncation` 设为 0.08

### 示例 B：达标 + IQC 级（Sharpe 1.62）

**输入**：

```json
{
  "sharpe": 1.62,
  "fitness": 1.3,
  "turnover": 0.28,
  "drawdown": 0.09,
  "returns": 0.21,
  "self_correlation": 0.55
}
```

**期望输出（摘要）**：

> **状态汇总**：
>
> - Sharpe 1.62 → **强 IQC**（≥ 1.5，进入"准精选"区）
> - Fitness 1.3 → **达标**（> 1.0）
> - Turnover 0.28 → **强达标**（0.1-0.5 IQC 甜区）
> - Drawdown 0.09 → **强达标**（≤ 0.10）
> - Returns 0.21 → **强达标**（≥ 0.15）
> - Self Correlation 0.55 → **边缘**（0.5-0.7，但 Sharpe > 1.375 触发豁免）
>
> **综合结论**：可提交（优先）。Sharpe 1.62 触发 [wq-submission-standards.md](../references/wq-submission-standards.md) 第二节"例外条款"，Self Correlation 0.55 自动豁免。
>
> **改进动作清单**：
>
> - **P1（Self Correlation 边缘）**：建议小幅优化（替换 1 个字段），但**不阻塞提交**。
> - **P2（Returns）**：0.21 已强达标，无需调整。
> - 提交前自检清单见 [wq-submission-standards.md](../references/wq-submission-standards.md) 第六节。
>
> **Checklist**：
>
> - [ ] 直接提交
> - [ ] 提交后监控 24h 内的 Self Correlation 复核
> - [ ] 复制表达式 + Dataset 留存，作为后续"高产模板"

---

## 7. 引用清单

- [wq-submission-standards.md](../references/wq-submission-standards.md) —— Sharpe 1.25 / Fitness 1.0 / Self Correlation 0.7 三硬性条件、1.375 豁免条款、IQC 加分指标。
- [kpi-reference.md](../references/kpi-reference.md) —— 7 大指标合格线、改进方向、改进优先级。
- [dataset-cheatsheet.md](../references/dataset-cheatsheet.md) —— 数据集差异与中性化维度选择。
- [diagnosis-report.md](../../templates/diagnosis-report.md) —— 本能力产出的报告模板。
