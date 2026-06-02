# 配置审查报告

> 本报告用于审查 WorldQuant BRAIN 模拟（simulation）配置参数设置的合理性，帮助在提交模拟前发现潜在风险。
> 模板由 Alpha Quality Helper 自动生成，请按下方示例填写。

---

## 一、基本信息

| 字段 | 值 |
| --- | --- |
| 审查对象 | <!-- TODO: 模拟 ID / 平台用户 / 脑名称 --> |
| 审查日期 | <!-- TODO: YYYY-MM-DD --> |
| 审查人 | <!-- TODO: 姓名 / 系统自动 --> |
| 数据集 | <!-- TODO: 例如 USA Equities --> |
| 区域 | <!-- TODO: 例如 USA / CHN / EUR --> |
| Alpha 类型 | <!-- TODO: 例如 截面 / 时序 --> |
| 工具 | <!-- TODO: 例如 analyst4 / IDE / 模板 --> |

---

## 二、合理性评分

> 满分 100 分；分数 ≥ 80 为合理，60-79 为可接受但需关注，< 60 为不合理。

**综合评分：<!-- TODO: 例如 78 --> / 100**

<!-- TODO: 文字解释，2-4 句说明扣分点与亮点，例如：
- 数据集与 Delay 配置是否一致（Delay=1 应配合 TOP3000 / TOP2000 等高频数据）；
- 阈值（Sharpe / Fitness）是否过松或过严，可能导致假阳性或漏判；
- 行业 / 子行业分组（Subindustry / Industry / Sector）是否匹配策略逻辑；
- 衰减（Decay）、最长持仓期（Max Trade）、Universe 范围等关键参数是否落在合理区间。 -->

### 评分细则

| 维度 | 权重 | 得分 | 说明 |
| --- | --- | --- | --- |
| 平台与 Delay 一致性 | 20 | <!-- TODO --> | <!-- TODO --> |
| 阈值与样本量 | 20 | <!-- TODO --> | <!-- TODO --> |
| 分组与池子选择 | 20 | <!-- TODO --> | <!-- TODO --> |
| 衰减 / 持仓 / 换仓 | 20 | <!-- TODO --> | <!-- TODO --> |
| 多空最低要求 | 20 | <!-- TODO --> | <!-- TODO --> |

---

## 三、风险点列表

> 每条风险请给出严重程度（**高 / 中 / 低**）、触发的参数与改进方向。

| # | 严重程度 | 风险点 | 触发参数 | 说明 |
| - | - | - | - | - |
| 1 | <!-- TODO: 高/中/低 --> | <!-- TODO: 风险描述 --> | <!-- TODO: 参数名 = 值 --> | <!-- TODO: 后果 --> |
| 2 | <!-- TODO --> | <!-- TODO --> | <!-- TODO --> | <!-- TODO --> |
| 3 | <!-- TODO --> | <!-- TODO --> | <!-- TODO --> | <!-- TODO --> |
| 4 | <!-- TODO --> | <!-- TODO --> | <!-- TODO --> | <!-- TODO --> |
| 5 | <!-- TODO --> | <!-- TODO --> | <!-- TODO --> | <!-- TODO --> |

### 风险等级说明

- **高（High）**：直接导致回测结果失真或不可提交；建议立即修改。
- **中（Medium）**：可能导致 Sharpe/Fitness 虚高、过拟合或样本不足；建议在提交前调整。
- **低（Low）**：属于风格偏好或可优化项；不影响提交，但长期看有提升空间。

---

## 四、调整建议

> 每条建议需"具体到参数值"，并给出修改前后对比。

### 4.1 参数调整清单

| # | 参数 | 当前值 | 建议值 | 调整理由 | 预期影响 |
| - | - | - | - | - | - |
| 1 | <!-- TODO: 平台/Region/Decay/... --> | <!-- TODO --> | <!-- TODO --> | <!-- TODO --> | <!-- TODO --> |
| 2 | <!-- TODO --> | <!-- TODO --> | <!-- TODO --> | <!-- TODO --> | <!-- TODO --> |
| 3 | <!-- TODO --> | <!-- TODO --> | <!-- TODO --> | <!-- TODO --> | <!-- TODO --> |
| 4 | <!-- TODO --> | <!-- TODO --> | <!-- TODO --> | <!-- TODO --> | <!-- TODO --> |
| 5 | <!-- TODO --> | <!-- TODO --> | <!-- TODO --> | <!-- TODO --> | <!-- TODO --> |

### 4.2 配置块示例（修改后）

```yaml
# 修改后的建议配置（示例，请按实际替换）
platform: analyst4
region: USA
delay: 1
group: Subindustry
decay: 4
truncation: 0.08
neutralization: Subindustry
maxTrade: 5
universe: TOP3000
thresholds:
  sharpe: 0.75
  fitness: 0.5
  longShortMin: 100
  maxDrawdown: 0.5
```

### 4.3 操作 Checklist

- [ ] <!-- TODO: 例如 "将 Delay 从 0 改为 1，配合 TOP3000 数据" -->
- [ ] <!-- TODO: 例如 "把 Neutralization 从 None 改为 Subindustry" -->
- [ ] <!-- TODO: 例如 "把 Sharpe 阈值从 0.5 收紧到 0.75" -->
- [ ] <!-- TODO: 例如 "把 Long/Short Minimum 都设为 100" -->
- [ ] <!-- TODO: 例如 "把 Decay 从 0 改为 4，配合 4 个交易日均线的逻辑" -->

---

## 五、参考示例（完整填充）

> 下面给出一份基于工具默认配置的完整示例报告，方便学员对照。

### 5.1 基本信息

| 字段 | 值 |
| --- | --- |
| 审查对象 | analyst4 默认配置 / USA / Subindustry |
| 审查日期 | 2026-06-02 |
| 审查人 | Alpha Quality Helper |
| 数据集 | USA Equities TOP3000 |
| 区域 | USA |
| Alpha 类型 | 截面因子 |
| 工具 | analyst4 |

### 5.2 合理性评分

**综合评分：78 / 100**

- Delay=1 与 USA 平台 TOP3000 数据匹配，配置正确；
- 阈值（Sharpe 0.75 / Fitness 0.5）属于平台推荐水平，过滤能力适中；
- 分组（Subindustry）+ 中性化（Subindustry）一致，可消除行业内偏差；
- Decay=4 与 4 个交易日均线逻辑相符，时序因子较稳定；
- 扣分点：Long/Short Minimum=100 处于临界，TOP3000 池子下若子行业分布不均，多空数容易不足。

### 5.3 评分细则

| 维度 | 权重 | 得分 | 说明 |
| --- | --- | --- | --- |
| 平台与 Delay 一致性 | 20 | 18 | analyst4 + Delay=1 + USA 一致，仅 Decay 略激进 |
| 阈值与样本量 | 20 | 16 | 阈值合理，但 longShortMin=100 在细分子行业上偏紧 |
| 分组与池子选择 | 20 | 18 | Subindustry 与 TOP3000 匹配良好 |
| 衰减 / 持仓 / 换仓 | 20 | 14 | Decay=4 略快，建议回测对比 Decay=2/6 |
| 多空最低要求 | 20 | 12 | 100 在部分子行业上低于平台推荐 200 |

### 5.4 风险点列表

| # | 严重程度 | 风险点 | 触发参数 | 说明 |
| - | - | - | - | - |
| 1 | 中 | Decay=4 偏快，敏感于短窗口噪声 | `decay=4` | 在高换手池子中可能放大 Turnover |
| 2 | 中 | Long/Short Minimum=100 临界 | `thresholds.longShortMin=100` | 子行业划分下部分组多空数不足 100 |
| 3 | 低 | Sharpe 阈值 0.75 略宽松 | `thresholds.sharpe=0.75` | 仍可能通过低 Sharpe 弱因子 |
| 4 | 低 | Fitness 阈值 0.5 | `thresholds.fitness=0.5` | 处于推荐区间下沿 |
| 5 | 低 | Max Run=2000 在大池下样本偏少 | `simulation.maxRun=2000` | 在 TOP3000 上统计意义略弱 |

### 5.5 调整建议

| # | 参数 | 当前值 | 建议值 | 调整理由 | 预期影响 |
| - | - | - | - | - | - |
| 1 | `thresholds.sharpe` | 0.5 | 0.75 | 提高 Sharpe 阈值，弱因子会被过滤 | 通过率下降，但入选质量提升 |
| 2 | `thresholds.fitness` | 0.4 | 0.5 | 同步提高 Fitness 阈值 | 配合 Sharpe 形成组合过滤 |
| 3 | `thresholds.longShortMin` | 100 | 100 | 保持 100 | 当前已是合理水平，不调整 |
| 4 | `decay` | 0 | 4 | 引入时序衰减，增强稳定性 | Sharpe/Fitness 略降，但更稳健 |
| 5 | `group` / `neutralization` | None | Subindustry | 加入子行业中性化，消除行业内偏差 | Turnover 略升，但行业外因子更纯 |

**修改后配置块：**

```yaml
platform: analyst4
region: USA
delay: 1
universe: TOP3000
group: Subindustry
decay: 4
truncation: 0.08
neutralization: Subindustry
maxTrade: 5
maxRun: 2000
thresholds:
  sharpe: 0.75
  fitness: 0.5
  longShortMin: 100
  longMin: 100
  shortMin: 100
  maxDrawdown: 0.5
```

### 5.6 操作 Checklist

- [x] 平台与 Delay 一致（analyst4 + USA + Delay=1）
- [x] Sharpe 阈值上调至 0.75
- [x] Fitness 阈值上调至 0.5
- [x] Decay 从 0 调整为 4
- [x] 分组与中性化都设为 Subindustry
- [ ] Max Run 视回测时长再决定是否扩到 4000

---

> 报告生成工具：Alpha Quality Helper v1.0
