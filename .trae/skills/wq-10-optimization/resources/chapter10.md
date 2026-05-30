# 第十章 顾问后Alpha策略优化

## 10.1 思维转变
目标从"凑够1万分"变为"最大化Alpha质量和收入"

## 10.2 收入4大驱动因素
### 因素一：提交数量
每天只有前4个Alpha能获得收入，第5个及之后不计入当日收入。优先提交高质量的。

### 因素二：提交质量
核心指标：Sharpe≥1.25(D1)、Fitness越高越好、Turnover<30%、Margin>4bps

### 因素三：自我提升
新Alpha比历史水平更好→正面影响；更差→负面影响

### 因素四：VF(Value Factors，价值因子)——影响收入最大的单一因素
- VF范围0.5~1.0，越接近1.0收入越高
- VF 0.95的收入可能是VF 0.5的十倍以上
- 与其交10个低VF的Alpha，不如打磨2-3个高VF的
| VF范围 | 收入水平 |
| 0.95+ | 非常高 |
| 0.85-0.95 | 较高 |
| 0.7-0.85 | 良好 |
| 0.5-0.7 | 较低 |

## 10.3 提交质量标准（最低标准）
- Sub-universe Sharpe ≥ 0.7
- Turnover < 30%
- Margin > 4bps
- 禁忌：不要为降低相关性添加噪声（平台检测并惩罚）

## 10.4 Performance Comparison
- Change > 0: ✅提交（对组合正向贡献）
- Change < 0: ❌不提交（即使单个Sharpe很高，也会拖累整体）

## 10.5 优化策略
### 中性化选择
强度递增：NONE → MARKET → INDUSTRY → SUBINDUSTRY
基本面数据→INDUSTRY/SUBINDUSTRY | 价量数据→MARKET | 情绪数据→MARKET或INDUSTRY | 期权数据→MARKET | 模型数据→NONE

### 降低换手率
方法一：增加decay参数(5→10→20)
方法二：使用ts_mean平滑 alpha = ts_mean(raw_signal, 5)

### 降低相关性
1. 更换数据集 2. 使用不同算子 3. 改变信号逻辑 4. 调整时间窗口 5. 增加条件过滤

### 提升Fitness
高换手率→增加decay/ts_mean | 中性化不足→升级中性化 | Alpha重叠→降低Self-Correlation | 信号噪音→优化表达式逻辑

## 10.6 主题日历
平台定期发布主题，提交匹配主题的Alpha获得收入倍数加成。关注平台公告，提前准备。

## 10.7 等级进阶
Gold→Expert(VF>0.85)→Master(VF>0.90,数量多)→Grandmaster(VF>0.95,数量领先)
核心原则：等级提升关键是提交更高质量Alpha，VF是王道。

## 10.8 官方学习路径
1. 通读Learn页面核心文档 2. 完成Academy入门课程 3. Forum读高等级顾问分享帖 4. 尝试不同数据集+中性化 5. 关注Theme Calendar