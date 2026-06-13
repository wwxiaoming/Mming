# A 股短线选股自动化 Tasks（v2.2）

> 本 tasks.md 配套 `/workspace/选股手册.md` v2.2 + `/workspace/股票分析技能整合文档_详细分析.md` v2.1 + `spec.md` v2.2
> 自动化任务 ID：`WXCF9ZUTD8-0W8` · cron `0 8 * * 1-5` · 时区 `Asia/Shanghai`
> 状态说明：✅ 已完成 · ⏳ 进行中 · ⬜ 待办

---

## Phase 1 · 选股文档与基础架构

| ID | 任务 | 状态 | 备注 |
|----|------|------|------|
| 1.1 | 创建 `选股手册.md` v1.0 | ✅ | 5 原则 + 5 维个股 + 10 排除规则 + 4 选 1 结论 |
| 1.2 | 创建 `股票分析技能整合文档.md` | ✅ | 9 节架构图 + 14 技能表 |
| 1.3 | 创建 `选股prompt.txt` | ✅ | 原始 16 段 prompt 源文件 |
| 1.4 | 创建 `scripts/daily_pick.py` | ✅ | 1148 行 Python 自动化脚本（保留为会话工具） |
| 1.5 | 创建 `scripts/requirements.txt` + `scripts/README.md` | ✅ | 脚本配套文档 |

## Phase 2 · v2.0 升级（USAGE.md 10 个 skill 引用）

| ID | 任务 | 状态 | 备注 |
|----|------|------|------|
| 2.1 | 读取 `/workspace/USAGE.md` 提取 10 个新 skill | ✅ | longbridge-earnings / akshare / longbridge-research / company-valuation / sector-analyst / macro-rates-monitor / market-breadth-analyzer / commodities-quote / market-top-detector / institutional-flow-tracker |
| 2.2 | 选股手册 v1.0 → v2.0：+ 6 维资金/筹码 + 13 排除规则 | ✅ | 第二章第 6 条多源验证、第五章第 6 项资金/筹码确认（5 项）、第七章 11-13 条排除 |
| 2.3 | 详细分析文档 v1.0 → v2.0：+ 5 层架构 + 24 技能 | ✅ | 新增 L0 层 + 10 个新 skill 评级 + 整体评价重写 + 角色适配表 |
| 2.4 | 创建 Schedule 任务 `R5.MLLFO6Z0NXQ` | ✅ | 已废弃（被 WXCF9ZUTD8-0W8 接管） |
| 2.5 | 创建 Schedule 任务 `WXCF9ZUTD8-0W8`（v2.0 详细版） | ✅ | 引用 `/workspace/选股手册.md` v2.0 + 13 排除规则 |
| 2.6 | 详细分析文档附录 + changelog 同步 | ✅ | 附录速查表 24 行 + v2.0 changelog 段 |

## Phase 3 · v2.1 升级（5 层架构 + 详细分析扩展）

| ID | 任务 | 状态 | 备注 |
|----|------|------|------|
| 3.1 | 详细分析 v2.0 → v2.1 准备（已通过 Phase 2 完成） | ✅ | 同 2.3 |
| 3.2 | 选股手册 v2.0 → v2.1：+ 7 原则 + 14 排除规则 | ✅ | 第二章第 7 条跨市场信号映射、第三章步骤 1.4 战术择时、第三章步骤 2.4 机构共识+2.5 估值锚点、第五章第 6 项扩展 2 项、第七章第 14 条、第八章 5 级表 + L0 列、附录 B 追加 10 行、附录 D 角色映射 2 行、附录 F v2.1 changelog |
| 3.3 | 详细分析 v2.0 → v2.1 复用（同步在 v2.0 实现） | ✅ | 见 2.3 |
| 3.4 | Schedule 任务 WXCF9ZUTD8-0W8 任务消息升级到 v2.1 | ✅ | 追加 7 原则 + 14 排除 + 10 数据源优先级 + 跨市场信号降级机制 |

## Phase 4 · v2.2 升级（A 股原生化 · ASHARE_README.md 6 skill 替换主流程美股 skill）

| ID | 任务 | 状态 | 备注 |
|----|------|------|------|
| 4.1 | 读取 `/workspace/ASHARE_README.md` 提取 6 个 A 股原生 skill | ✅ | A01 a-share-analysis / A02 sector-rotation-detector / A03 china-macro-analyst / A04 limit-up-pool-analyzer / A05 equity-pledge-risk-monitor / A06 fund-screener |
| 4.2 | 制定替换策略（用户确认） | ✅ | 完全替换为 A 股原生版本；美股 skill 仅在文末提及 |
| 4.3 | 详细分析 v2.0 → v2.1 调整：L0 6 个美股 skill 替换为 A 股原生 | ✅ | 0.1 macro-rates → china-macro-analyst / 0.2 sector-analyst → sector-rotation-detector / 0.3 market-breadth → limit-up-pool-analyzer / 0.4 market-top → equity-pledge-risk-monitor / 0.5 institutional-flow → fund-screener / 0.6 commodities-quote 保留（无 A 股替代） |
| 4.4 | 详细分析 v2.1：L3 company-valuation 删除,a-share-analysis 强化 | ✅ | 9. a-share-analysis 新增 DCF/相对/SOTP 估值能力 |
| 4.5 | 详细分析 v2.1：附录 A1 美股向工具附记 | ✅ | 7 个美股/跨市场向工具附记清单（macro-rates / sector-analyst / market-breadth / market-top / institutional-flow / commodities-quote / company-valuation） |
| 4.6 | 详细分析 v2.1：5.3 角色适配扩展 | ✅ | 新增「涨停打板选手」「股权质押风控」+ 调整「美股价值投资者」「跨市场套利者」改指文末附记 |
| 4.7 | 详细分析 v2.1：附录速查表 + changelog 同步 | ✅ | 22 个主流程 + 7 个附记 + v2.1 changelog 详细记录 |
| 4.8 | 选股手册 v2.1 → v2.2：第 0 章版本 + 配套文档加 ASHARE_README.md | ✅ | |
| 4.9 | 选股手册 v2.2：第二章第 7 条改写为「A 股宏观/行业/资金映射」 | ✅ | A 股原生 5 项 L0 工具引用 |
| 4.10 | 选股手册 v2.2：第三章步骤 1.4 重写为 A 股原生战术预检 | ✅ | 5 项 A 股原生：china-macro / sector-rotation / limit-up / equity-pledge / fund-screener |
| 4.11 | 选股手册 v2.2：第三章步骤 2.4/2.5 A 股化 | ✅ | 2.4 A 股机构共识（fund-screener 主 + longbridge 联动保留）+ 2.5 A 股估值锚点（a-share-analysis 强化） |
| 4.12 | 选股手册 v2.2：第五章第 6 项 2 项 A 股化 | ✅ | 公募 smart money + A 股情绪广度/股权质押 |
| 4.13 | 选股手册 v2.2：第七章第 14 条 A 股原生信号矛盾 | ✅ | 4 个 A 股原生风险场景 |
| 4.14 | 选股手册 v2.2：第八章 5 级表第 4 列 L0 A 股原生 | ✅ | 4 项 A 股原生指标 |
| 4.15 | 选股手册 v2.2：附录 B 数据源表 v2.1 10 行重排 | ✅ | 5 行升级为 A 股原生、3 行降为附记、1 行新增 A 股原生估值 |
| 4.16 | 选股手册 v2.2：附录 D 角色映射扩展 + 调整 | ✅ | 新增 2 行 A 股场景（涨停打板 + 股权质押风控）+ 2 行降为附录 G |
| 4.17 | 选股手册 v2.2：附录 F 追加 v2.2 changelog | ✅ | 详细记录 A 股 skill 替换映射 + 新增章节 + 未改动章节 |
| 4.18 | 选股手册 v2.2：附录 G 美股/跨市场向工具附记 | ✅ | 9 个美股/跨市场向工具清单 + 5 条使用原则 + 主流程/附记边界 |

## Phase 5 · 自动化任务升级（v2.2）

| ID | 任务 | 状态 | 备注 |
|----|------|------|------|
| 5.1 | 优化 Schedule 任务 WXCF9ZUTD8-0W8 消息（v2.0 → v2.2） | ✅ | 任务消息全面升级：L0 A 股战术预检 + 14 排除规则 + 双层降级 + 附录 G 边界 + 报告末尾工具版本声明 |
| 5.2 | 升级 spec.md（v1.0 → v2.2） | ✅ | 重写以反映 v2.2 手册结构：7 原则/6 维/14 排除 + L0 A 股化 + 附录 G 附记 + 详细分析 v2.1 + 角色适配 10 个 |
| 5.3 | 升级 tasks.md（v1.0 → v2.2） | ✅ | 补充 v2.1/v2.2 升级完成记录 + Phase 4/5 完整任务列表 |
| 5.4 | 验证 任务消息 + spec + tasks 三者引用一致 | ⏳ | 当前任务 |

## Phase 6 · 后续维护

| ID | 任务 | 状态 | 备注 |
|----|------|------|------|
| 6.1 | 监控 Schedule 任务下次运行（2026-06-15 08:00） | ⬜ | 任务 ID: WXCF9ZUTD8-0W8 |
| 6.2 | 监控输出文件 `/workspace/output/YYYY-MM-DD_早盘潜力股.md` | ⬜ | 每日生成 |
| 6.3 | 收集 v2.2 实际运行反馈（首次 2026-06-15） | ⬜ | 检查 L0 预检 / 双层降级 / 附录 G 边界是否生效 |
| 6.4 | 决定是否需要进一步升级到 v3.0（重大结构调整） | ⬜ | 待 v2.2 实际运行后再评估 |
| 6.5 | 决定 x1.0 融合版（8HBXYCBRO9_Y55）是否同步升级 | ⬜ | 独立体系，引用 x1.0-stock-trader 选股手册 |

## 版本历史

- **v1.0** · 2026-06-13 — Phase 1-2 基础架构 + 选股手册 + USAGE.md 10 skill 引用
- **v2.0** · 2026-06-13 — Phase 2 6 维资金/筹码 + 13 排除 + 详细分析 24 技能 5 层架构
- **v2.1** · 2026-06-13 — Phase 3 7 原则 + 14 排除 + 跨市场信号映射 + L0 战术预检（美股向）
- **v2.2** · 2026-06-13 — Phase 4-5 主流程 A 股化（ASHARE 6 skill 替换）+ 详细分析 5 层 A 股化 + 附录 A1/G 附记 + 14 排除 + 双层降级 + spec/tasks/schedule 全部升级

## 关键统计

- 选股手册：v1.0 → v2.2（17 章 + 7 附录）· 全文 ≈ 895 行
- 详细分析：v1.0 → v2.1（5 层架构 + 附录 A1）· 全文 ≈ 418 行
- Schedule 任务消息：v2.0 → v2.2（10 章节全面升级）· 消息 ≈ 5.0 KB
- spec.md：v1.0 → v2.2（11 个 Scenario + 5 个 MODIFIED + 0 REMOVED）· 全文 ≈ 250 行
- tasks.md：v1.0 → v2.2（5 个 Phase + 36 个子任务）· 全文 ≈ 本次升级

## 下次运行预期

- 任务 ID：WXCF9ZUTD8-0W8
- 下次运行：2026-06-15 08:00（北京时间）
- 引用文档：选股手册 v2.2 + 详细分析 v2.1
- 输出路径：`/workspace/output/2026-06-15_早盘潜力股.md`
- 关键校验：L0 五项 A 股战术预检 / 14 排除规则 / 双层降级 / 附录 G 边界
