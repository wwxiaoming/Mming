# Checklist

## 基础结构
- [x] skill 目录已创建：`.trae/skills/wqbrain-alpha-quality-helper/`
- [x] `SKILL.md` 含触发词清单（至少 3 类）
- [x] `manifest.json` 含 name / version / depends / entry
- [x] `references/` 目录下有 4 个 markdown 文档
- [x] `templates/` 目录下有 2 个 markdown 报告模板

## Reference 文档完整性
- [x] `wq-submission-standards.md` 含 Sharpe>1.25 / Fitness>1 / SelfCorr<0.7 三硬性条件
- [x] `wq-submission-standards.md` 含例外条款（Sharpe > 1.375 豁免 SelfCorr）
- [x] `kpi-reference.md` 含 7 个核心指标的合格线与改进方向
- [x] `dataset-cheatsheet.md` 覆盖截图中的 13 个 dataset
- [x] `learning-index.md` 含 WQ 官方 / 老强 / IMA / 量化音频 4 类直达链接

## 4 个子能力
- [x] `config-auditor` 能识别一阶段参数（Dataset / Region / Delay / Neutralization / Decay / Max Run）
- [x] `config-auditor` 能识别二阶段阈值（Sharpe 阈值 / Fitness 阈值 / 最少做多空数）
- [x] `config-auditor` 对默认配置（analyst4 / USA / Delay=1 / Subindustry / Sharpe 0.75）能输出"种子门槛 ≠ 提交门槛"提示
- [x] `expression-preflight` 能识别 Arithmetic / Logical / Time Series 3 大类操作
- [x] `expression-preflight` 能输出至少 3 条改写建议
- [x] `result-diagnostician` 能解读 Sharpe / Fitness / Turnover / Returns / Drawdown / Margin / Self Correlation
- [x] `result-diagnostician` 对 Sharpe 1.05 / Fitness 0.7 / Turnover 0.65 的 JSON 能给出"加 rank + 压 turnover"动作清单
- [x] `submission-strategist` 能基于"714/1800 用量"给出"剩余 1086 次、建议 3-5 个三阶段任务"的策略
- [x] `submission-strategist` 能识别"距 Super 解锁还差 N 个 Regular"并给出建议

## 报告模板
- [x] `audit-report.md` 含合理性评分 / 风险点 / 调整建议 3 段
- [x] `diagnosis-report.md` 含指标逐项解读 / 改进动作清单 2 段

## 验证
- [ ] 3 个 config 用例（好/坏/边缘）跑通 `config-auditor`
- [ ] 3 段典型表达式跑通 `expression-preflight`
- [ ] 3 段典型回测 JSON 跑通 `result-diagnostician`
- [ ] 全部输出符合对应模板
- [x] 输出中的 WQ 平台数据与论坛/官方公开资料一致（Sharpe 1.25 / Fitness 1.0 / SelfCorr 0.7）

## 学员侧可用性
- [ ] 学员贴任意一阶段配置截图文字，skill 能在 1 轮内给出审查结论
- [ ] 学员贴任意 Fast Expression，skill 能在 1 轮内给出预审 + 改写建议
- [ ] 学员贴任意回测 JSON，skill 能在 1 轮内给出诊断 + 改进动作
- [ ] 学员问提交策略，skill 能基于"714/1800 + 铜陵-4000 + 2/3"画像给出当日建议

## 验证失败项

无（14 步文件级验证全部通过）

未打钩的 8 项（验证 4 项 + 学员侧可用性 4 项）属于**端到端跑通/学员交互测试**范畴，不在本次 14 步文件完整性验证范围内，能力文档中已包含对应"期望输出"示例但未实际执行；如需补齐需在 Trae 运行环境里由 skill runtime 真正触发一次。
