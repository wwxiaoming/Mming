# 计划：将 USAGE.md 中 10 个新 Skill 整合到 2 份文档

> 用户请求：将 `/workspace/USAGE.md` 列出的 10 个新 skill，写入 `/workspace/股票分析技能整合文档_详细分析.md` 与 `/workspace/选股手册.md`。

---

## Summary

USAGE.md 中列出的 10 个新 skill 中，6 个为美股/全球市场工具（longbridge-earnings、longbridge-research、company-valuation、sector-analyst、macro-rates-monitor、market-breadth-analyzer、market-top-detector、institutional-flow-tracker、commodities-quote），1 个为中文金融数据（akshare）。整合策略：

- **详细分析.md**（架构文档）：扩展为 24 技能，新增 L0「战术与全球宏观」层，把 6 个宏观/战术工具放到 L0；L1 加入 akshare 作为中文数据源补充；L3 追加 3 个（longbridge-earnings、longbridge-research、company-valuation）。版本升至 v2.0。
- **选股手册.md**（A 股短线交易 SOP）：10 个新技能按相关性分层，akshare 入附录 B；sector-analyst / market-breadth / market-top / institutional-flow / longbridge-earnings / longbridge-research / company-valuation 写入第三章环境判断与方向归因、附录 B、附录 D；commodities-quote / macro-rates 在附录 D 简提。版本升至 v2.1。

---

## Phase 1 探索结果（已确认）

### 1.1 USAGE.md 10 个新 Skill 定位

| # | Skill | 类型 | 数据源 | 适配层级 |
|---|-------|------|--------|----------|
| 1 | `longbridge-earnings` | 业绩前瞻+回顾 | Longbridge | L3 分析（业绩） |
| 2 | `akshare` | 中文金融数据 | 公开 akshare | L3 数据中台（与 a-stock-data 并列/互补） |
| 3 | `longbridge-research` | 机构评级/13F/EPS 预测 | Longbridge | L3 分析（机构共识） |
| 4 | `company-valuation` | DCF + 相对 + SOTP | yfinance | L3 分析（估值） |
| 5 | `sector-analyst` | 板块轮动/周期定位 | TraderMonty CSV | L0/L1 战术（板块广度） |
| 6 | `macro-rates-monitor` | GDP/CPI/收益率曲线 | LSEG MCP | L0 宏观 |
| 7 | `market-breadth-analyzer` | 广度 0-100 分 | TraderMonty CSV | L0/L1 战术（广度） |
| 8 | `commodities-quote` | 黄金/原油/铜等报价 | Octagon MCP | L0 大宗 |
| 9 | `market-top-detector` | 见顶概率 0-100 分 | FMP API + WebSearch | L0/L1 战术（择时） |
| 10 | `institutional-flow-tracker` | 13F 季度持仓 | FMP API | L0/L1 资金流 |

### 1.2 现有 14 技能清单（详细分析.md）

L1：last30days
L2：a-share-screener, eastmoney_select_stock, longbridge-value-investing, china-stock-analysis, serenity-radar, serenity-stock-choke
L3：a-stock-data, a-share-analysis, serenity-skill, stock-watcher, data-analysis
L4：investment-memo, consulting-analysis

### 1.3 现有 选股手册.md 结构（v2.0）

- 17 章主线 + 6 附录
- 核心是 A 股短线 SOP（早盘 8:00 自动化选股）
- 数据源集中在 `a-stock-data`（a-stock-data 内部 7 层）
- v2.0 已经做了 6 维资金/筹码确认（北向/120 日资金流/龙虎榜/解禁/股东户数）
- 附录 B 数据源优先级表、附录 D 角色映射表、附录 F changelog 是新增内容的最佳落点

---

## 拟改动的文件

### 文件 1：`/workspace/股票分析技能整合文档_详细分析.md`

**目标版本**：v1.0 → v2.0
**改动幅度**：中等（新增 1 层 + 10 个技能评级 + 整体评价重写）

#### 改动清单

1. **文档元信息**（顶部）
   - 版本号 v1.0 → v2.0
   - 增加 changelog 段落：「v2.0 新增 L0 层 + 10 个新技能」

2. **总体评估**
   - 14 技能 → 24 技能
   - 4 层 → 5 层（新增 L0）
   - 更新「漏斗式工作流」描述为「L0 全球宏观 → L1 资讯 → L2 选股 → L3 分析 → L4 产出」

3. **新增 L0 战术与全球宏观层**（6 个技能）
   - 5.1 `macro-rates-monitor` — 宏观 + 利率仪表盘
   - 5.2 `sector-analyst` — 板块轮动 + 周期定位
   - 5.3 `market-breadth-analyzer` — 市场广度量化
   - 5.4 `market-top-detector` — 见顶概率 0-100
   - 5.5 `institutional-flow-tracker` — 13F 机构资金流
   - 5.6 `commodities-quote` — 大宗商品实时报价
   - 每个技能按现有「维度分析表」格式：核心价值 / 数据时效 / 关键能力 / 典型使用 / 局限性 / 集成评价

4. **改造 L1 资讯层**
   - 1. `last30days`（保留）
   - 1.5（新增）`akshare` — 中文金融数据：与 last30days 互补，作为「中文数据快速通道」

5. **改造 L3 分析层**
   - 现有 5 个保留：`a-stock-data`, `a-share-analysis`, `serenity-skill`, `stock-watcher`, `data-analysis`
   - 新增 3 个：
     - 9.1 `longbridge-earnings` — 财报前瞻/回顾
     - 9.2 `longbridge-research` — 机构数据 + 卖方研究框架
     - 9.3 `company-valuation` — DCF + 相对 + SOTP

6. **重写「五、整体架构评价」**
   - 5.1 优点：补充「L0 战术层为跨市场择时提供量化锚点」
   - 5.2 可改进点：原 4 点保留 + 新增 1 点「L0 战术信号与 A 股个股联动需在文档中显式说明」
   - 5.3 适配建议表扩展 2-3 个新角色：
     - 「美股价值投资者」：macro-rates → sector-analyst → longbridge-earnings → company-valuation → investment-memo
     - 「跨市场套利者」：market-breadth → market-top → longbridge-research → institutional-flow → a-stock-data

7. **更新附录速查表**
   - 总技能数：14 → 24
   - 层级结构表更新
   - 新增 10 行 L0 层 + 1 行 akshare + 3 行 L3

8. **更新文末版本行**
   - 「文档版本：v1.0」→「v2.0 · 配套原文档：股票分析技能整合文档.md」

---

### 文件 2：`/workspace/选股手册.md`

**目标版本**：v2.0 → v2.1
**改动幅度**：小（仅在已有结构中追加 10 个技能的引用，不改主线交易逻辑）

#### 改动清单

1. **文档元信息**（第 0 章）
   - 版本号 v2.0 → v2.1
   - 主要改动记录：基于 USAGE.md 新增 10 个 skill 的引用

2. **第二章第 7 条工作原则**（新增）
   - 「跨市场信号映射」：海外宏观/财报/广度信号对 A 股的传导路径
   - 引用 `macro-rates-monitor`、`market-breadth-analyzer`、`longbridge-earnings`

3. **第三章步骤 1 大盘环境**（扩展）
   - 1.1 后新增 1.4「战术择时信号」：
     - `market-breadth-analyzer` 广度 0-100 分
     - `market-top-detector` 见顶概率 0-100 分
     - `institutional-flow-tracker` 13F 大资金方向
     - `sector-analyst` 板块轮动阶段
   - 不改变 5 选 1 结论枚举

4. **第三章步骤 2 方向归因**（扩展）
   - 2.4（新增）「机构共识与业绩前瞻」：
     - `longbridge-research` 看机构评级/目标价（覆盖港股美股联动 A 股的标的）
     - `longbridge-earnings` 做美股业绩前瞻/回顾（A/H 联动股、出口概念股）
   - 2.5（新增）「估值锚点」：
     - `company-valuation` 三方法估值作为方向内个股的目标价参考

5. **第五章第 6 项「资金/筹码确认」**（扩展）
   - 在现有 5 项后追加 2 项：
     - 「机构 13F 持仓变化」（美股标杆，跨市场参考）
     - 「板块广度/见顶信号」（大盘环境传导）

6. **第七章排除逻辑**（追加 1 条）
   - 第 14 条（新增）「跨市场信号矛盾」：当海外评级/业绩与 A 股技术面严重背离时，列为「明确不买」

7. **第八章环境分级**（扩展）
   - S 级新增附加条件：「L0 战术信号（广度/见顶/板块轮动）均支持」
   - D 级新增附加条件：「L0 战术信号全面恶化」

8. **附录 B 数据源优先级表**（追加 10 行）
   | 数据需求 | 首选技能 | 备选 | 用于本手册的环节 |
   |----------|----------|------|------------------|
   | 美股业绩前瞻/回顾 | `longbridge-earnings` | - | 步骤 2 方向（A/H 联动） |
   | 中文金融数据 | `akshare` | `a-stock-data` | 附录 A 兜底 |
   | 机构评级/13F | `longbridge-research` | - | 步骤 2 方向 |
   | DCF/相对/SOTP 估值 | `company-valuation` | `china-stock-analysis` | 步骤 3 量价（目标价） |
   | 板块轮动/周期 | `sector-analyst` | `eastmoney_select_stock` | 步骤 1 行业 |
   | 宏观+利率 | `macro-rates-monitor` | - | 步骤 1 政策（国际） |
   | 广度 0-100 | `market-breadth-analyzer` | - | 步骤 1 战术 |
   | 见顶概率 0-100 | `market-top-detector` | - | 步骤 1 战术 |
   | 13F 资金流 | `institutional-flow-tracker` | - | 步骤 1 资金（标杆股） |
   | 大宗商品报价 | `commodities-quote` | - | 步骤 1 政策（资源股） |

9. **附录 D 工作流场景映射表**（追加 2 行 + 扩展 1 行）
   - 新增「美股投资者」行：longbridge-research → longbridge-earnings → company-valuation → investment-memo
   - 新增「跨市场套利者」行：market-breadth → market-top → longbridge-research → a-stock-data
   - 「A 股短线交易者」行扩展：在工作流前增加「可选 L0 战术预检」

10. **附录 F 改动日志**（追加 v2.1 段）
    - 列出 10 个新 skill 的章节落点
    - 标注「未改动章节：第一章/第四章/第六章/第九章/第十章/第十六章」

---

## 关键决策（已与现状对齐）

- **不重写主线交易逻辑**：选股手册的核心是 A 股短线 SOP，4 选 1 结论枚举、6 维排序、13 条排除规则保持不变
- **新技能作为「辅助层」**：详细分析.md 新增 L0 层是「战术与全球宏观」,手册中作为步骤 1 大盘环境的补充维度
- **跨市场信号合理化**：10 个新技能中 6 个是美股/全球工具，定位为「海外信号 → A 股个股」的传导桥梁，不替代 A 股自身数据
- **数据源优先级兜底**：akshare 加入 a-stock-data 不可用时的备选链
- **版本号策略**：详细分析.md v1.0→v2.0（结构级变更），选股手册 v2.0→v2.1（追加级变更）

---

## 实施步骤

1. **Step 1**：编辑 `/workspace/股票分析技能整合文档_详细分析.md`
   - 用 Read 重新读取（已读取过）
   - 用 Edit/Write 按 1.1-1.8 节顺序插入新内容
   - 重点：先插入 L0 章节，再追加 L1/L3 章节，最后更新总评和附录

2. **Step 2**：编辑 `/workspace/选股手册.md`
   - 用 Edit 工具按 2.1-2.10 节顺序追加
   - 重点：每条 Edit 的 old_string 必须 unique，避免误改

3. **Step 3**：核对
   - 在两文件末尾追加版本号更新行
   - 在 选股手册.md 附录 F 追加 v2.1 changelog

4. **Step 4**：验证
   - 用 Read 抽查每文件至少 3 个修改点确认
   - 检查所有 USAGE.md 提到的 10 个 skill 都被引用到

---

## 假设与边界

- **假设 1**：用户接受 5 层架构（详细分析.md 升级到 L0 战术 + 全球宏观）
- **假设 2**：用户接受 选股手册 主线流程不变、仅追加引用（v2.0 → v2.1）
- **假设 3**：用户希望保留「未改动章节」的明确标注（与 v2.0 升级时同样的处理方式）
- **边界**：不修改附录 C（自动化执行注意事项）、附录 E（快速决策树）、第十一章输出文件结构

---

## Verification

执行完成后应满足：

1. `/workspace/股票分析技能整合文档_详细分析.md`：
   - [ ] 版本号 v2.0
   - [ ] 总技能数 24
   - [ ] L0 层包含 6 个新 skill（macro-rates / sector-analyst / market-breadth / market-top / institutional-flow / commodities-quote）
   - [ ] L1 层包含 akshare
   - [ ] L3 层包含 longbridge-earnings / longbridge-research / company-valuation
   - [ ] 角色适配表新增「美股价值投资者」「跨市场套利者」
   - [ ] 附录速查表 24 行

2. `/workspace/选股手册.md`：
   - [ ] 版本号 v2.1
   - [ ] 第二章有第 7 条「跨市场信号映射」原则
   - [ ] 第三章步骤 1 有 1.4「战术择时信号」节
   - [ ] 第三章步骤 2 有 2.4「机构共识与业绩前瞻」和 2.5「估值锚点」节
   - [ ] 第五章第 6 项资金/筹码确认扩展为 7 项
   - [ ] 第七章排除逻辑第 14 条「跨市场信号矛盾」
   - [ ] 第八章 S/D 级附加条件
   - [ ] 附录 B 数据源优先级表追加 10 行
   - [ ] 附录 D 角色映射表追加 2 行 + 1 行扩展
   - [ ] 附录 F changelog 有 v2.1 段

3. 两个文件中都出现的 10 个 skill 一致性：longbridge-earnings, akshare, longbridge-research, company-valuation, sector-analyst, macro-rates-monitor, market-breadth-analyzer, commodities-quote, market-top-detector, institutional-flow-tracker

---

> **计划文件**：`/workspace/.trae/documents/新增10个skill整合到详细分析与选股手册.md`
> **待用户确认后**进入实施阶段
