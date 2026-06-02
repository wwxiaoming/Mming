# Tasks

本 changeset 为学习研究性质，任务以资料收集、分析与文档编写为主。

- [ ] Task 1: 抓取 WorldQuant BRAIN 官方平台的关键资料
  - [ ] SubTask 1.1: 抓取 platform.worldquantbrain.com 关于等级、晋升、顾问的说明
  - [ ] SubTask 1.2: 整理 BRAIN 文档中 alpha 评价指标（Sharpe / Fitness / Turnover / Returns / Drawdown / Correlation）的定义与阈值
  - [ ] SubTask 1.3: 整理顾问阶段的奖金结构与计分规则

- [ ] Task 2: 整理「老强说 Alpha 辅助工具」官方文档
  - [ ] SubTask 2.1: 抓取 alphadoc.biglongxia.com 的核心文档（数据集、中性化、延迟、批次运行机制）
  - [ ] SubTask 2.2: 提取工具的"一/二/三阶段"配置差异与适用场景
  - [ ] SubTask 2.3: 整理工具的"可提交筛选"逻辑与限制

- [ ] Task 3: 抓取并整理学习任务文档（kdocs.cn）
  - [ ] SubTask 3.1: 抓取 https://www.kdocs.cn/l/chtbk1FwoNW5 的完整学习路线
  - [ ] SubTask 3.2: 标注用户已完成的里程碑（6 天 10000 分金牌）
  - [ ] SubTask 3.3: 提取顾问阶段的学习要求与考核点

- [ ] Task 4: 整理 IMA 知识库与网易云量化音频的核心知识点
  - [ ] SubTask 4.1: 抓取 ima.qq.com 知识库中关于 BRAIN / 顾问 / alpha 优化的内容
  - [ ] SubTask 4.2: 提炼网易云量化基础音频的关键金融概念（Sharpe、IC、换手率、因子模型等）

- [ ] Task 5: 搜索社区实战经验（CSDN / 知乎 / Reddit / 公众号）
  - [ ] SubTask 5.1: 搜索"WQ BRAIN 顾问 赚钱 / 收入"主题
  - [ ] SubTask 5.2: 搜索"BRAIN alpha 重复 / uniqueness / duplication"主题
  - [ ] SubTask 5.3: 搜索"BRAIN alpha 优化 / Sharpe 提升"主题
  - [ ] SubTask 5.4: 搜索"老强说工具 / 第三方辅助工具"的口碑与争议

- [ ] Task 6: 编写「工具批量法局限性」分析
  - [ ] SubTask 6.1: 拆解老强说工具的"工业化挖矿"逻辑
  - [ ] SubTask 6.2: 量化估算当前方法的重复率与 Sharpe 衰减风险
  - [ ] SubTask 6.3: 对比"工具跑量"与"自主设计"的 ROI 差异

- [ ] Task 7: 编写「alpha 质量提升」指南
  - [ ] SubTask 7.1: 整理 3 类算子（时序 / 截面 / 向量）的金融含义与常见用法
  - [ ] SubTask 7.2: 整理 5-6 类经典 alpha 模式（动量 / 反转 / 质量 / 价值 / 情绪 / 波动率）的构造模板
  - [ ] SubTask 7.3: 给出 3-5 个可立即尝试的 alpha 改造案例（基于用户现有的 `anl4_adjusted_netincome_ft` 风格 alpha）
  - [ ] SubTask 7.4: 解释中性化层级的合理选择与误用风险

- [ ] Task 8: 编写「降低重复率」具体策略
  - [ ] SubTask 8.1: 解释 BRAIN 的 duplication / uniqueness 判定机制
  - [ ] SubTask 8.2: 整理"换数据集 / 换中性化 / 换算子"的具体操作清单
  - [ ] SubTask 8.3: 总结社区常见的"差异化思路"清单

- [ ] Task 9: 编写「顾问成长路线图」
  - [ ] SubTask 9.1: 短期（1-3 个月）行动清单
  - [ ] SubTask 9.2: 中期（3-12 个月）目标
  - [ ] SubTask 9.3: 长期（1 年+）方向与转型路径

- [ ] Task 10: 整合输出最终学习指南
  - [ ] SubTask 10.1: 章节结构定稿（基础概念 / 等级奖金 / 局限诊断 / 算子模式 / 降重策略 / 路线图 / 资源清单）
  - [ ] SubTask 10.2: 关键概念配图（可选，从 Image Guidelines 生成示意）
  - [ ] SubTask 10.3: 通篇校对，确保语言适合金融小白

# Task Dependencies

- Task 1、2、3、4 可并行
- Task 5 依赖 Task 1、2（需要先理解官方机制再去找社区对应讨论）
- Task 6 依赖 Task 1、5
- Task 7 依赖 Task 1、5
- Task 8 依赖 Task 1、5
- Task 9 依赖 Task 6、7、8
- Task 10 依赖 Task 9
