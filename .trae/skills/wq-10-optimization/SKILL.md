---
name: 顾问后Alpha策略优化
description: 顾问后Alpha策略优化、收入驱动因素(VF为王)、提交质量标准、官方学习路径、等级进阶
---
# 顾问后Alpha策略优化

## 何时使用
当用户提到以下关键词时触发：优化、VF、Value Factor、顾问后、提高收入、换手率、Fitness、主题日历、Genius、晋级、Expert、Master、Grandmaster

## 核心指令
1. 思维转变：从"达标即可"转向"最大化收益"，关注Alpha质量而非数量
2. 收入4大驱动因素：
   - 提交数量：每天计前4个Alpha
   - 质量：VF值越高收入越高
   - 自我提升：持续学习新数据源和策略
   - VF是王道：VF 0.95的收入可能是VF 0.5的十倍以上！
3. 提交质量标准（顾问后）：
   - Sub-universe Sharpe ≥ 0.7
   - Turnover < 30%
   - Margin > 4bps
4. Performance Comparison检查：只有当Change > 0时才提交
5. 优化策略：
   - 中性化选择：根据数据特性选择合适的中性化层级
   - 降低换手率：使用decay和ts_mean函数
   - 降低相关性：切换数据源、换算子（Operator）
   - 提升Fitness：优化表达式复杂度
6. 主题日历（Theme Calendar）：关注平台发布的主题日历，提交符合主题的Alpha可能有额外加成
7. 官方学习路径：
   - Learn页面系统学习
   - 官方Webinar和教程
   - Genius竞赛参与
8. 进阶路线：
   - Gold → Expert → Master → Grandmaster
   - 每个等级对应不同收入和奖金上限
   - 持续学习和优化是晋级的唯一途径

## ⚠️ 警告
- VF值是最核心的收入驱动因素，不要只看Sharpe
- 每天只计前4个Alpha，之后提交的不计入当日收入
- 过度提交低质量Alpha会拉低整体评估
- Genius等高阶功能有额外门槛，需先达到相应等级

## 💡 提示
- 建立自己的策略库，记录每种组合的效果
- 关注同行策略分享但不要直接复制
- 定期回顾和分析自己的Alpha表现
- 参加Genius等竞赛可以获得额外曝光和收入
- VF的提升需要长期积累和策略迭代