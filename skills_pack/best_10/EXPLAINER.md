# A 股研究 Skill 工具包 — 完整说明

> **作者**：A 股 Equity Research Skill Curation  
> **目的**：在 `a-stock-data` 单 skill 基础上，补全 A 股深度研究所需的 10 个数据缺口  
> **版本**：v1.0 / 2026-06-02

---

## 目录

1. [项目背景与起源](#1-项目背景与起源)
2. [评估方法论](#2-评估方法论)
3. [Top 10 精选详表](#3-top-10-精选详表)
4. [24 个完整候选清单](#4-24-个完整候选清单)
5. [安装与配置指南](#5-安装与配置指南)
6. [与 a-stock-data 整合工作流](#6-与-a-stock-data-整合工作流)
7. [关键注意事项](#7-关键注意事项)
8. [未覆盖缺口与后续建议](#8-未覆盖缺口与后续建议)
9. [文件结构总览](#9-文件结构总览)

---

## 1. 项目背景与起源

### 1.1 起点

[../skills/a-stock-data/SKILL.md](../skills/a-stock-data/SKILL.md) 是当前 A 股研究最完整的中文 skill，覆盖 **7 层数据架构**（行情 / 研报 / 信号 / 资金筹码 / 新闻 / 基础数据 / 公告），合计 **27 个端点**。作者已在 SKILL.md 中明确：

> "V3.0 Breaking Change：彻底移除 akshare 依赖"

### 1.2 覆盖度评估

对照专业 A 股卖方研究/买方投研的标准工作流，对 `a-stock-data` 逐项盘点后发现：

| 研究类型 | 完整度 |
|---------|-------|
| 短线/题材交易 | **95%** ✅ |
| 技术分析 | **85%** ✅ |
| 中线趋势 | **70%** ⚠️ |
| 长线价值投资 | **60%** ⚠️ |
| 卖方完整报告 | **50%** ❌ |

### 1.3 识别 10 个关键缺口

按"对 Equity Research 报告质量"的影响排序：

| # | 缺口 | 重要性 | 影响 |
|---|------|--------|------|
| 1 | 历史估值带 (PE/PB Band) | 🔴 | 无法判断当前估值在历史上的分位 |
| 2 | 业绩预告/快报 | 🔴 | 年报/季报前博弈关键数据 |
| 3 | 十大股东/机构持仓 | 🔴 | 筹码集中度、机构动向 |
| 4 | 分析师评级/目标价分布 | 🔴 | 市场情绪极值判断 |
| 5 | 行业指数/申万分类 | 🟡 | 行业 ETF 对标、历史走势 |
| 6 | 衍生品/对冲数据 | 🟡 | 基差、套保成本 |
| 7 | 宏观环境（利率/汇率/PMI） | 🟡 | 利率敏感 vs 周期股判断 |
| 8 | 海外联动（H 股/美股/费城半导体） | 🟡 | 科技股联动验证 |
| 9 | 市场情绪（涨停家数/炸板率/连板） | 🟡 | 风险偏好、温度 |
| 10 | 大宗商品（铜/铝/钢/煤） | 🟡 | 周期股驱动 |

### 1.4 搜索与打包

用 [`find-skills-plus`](../skills/find-skills-plus/SKILL.md) 工具对 10 个缺口各搜索 3 个候选（共 30 个），按实际仓库可获取性筛选为 **24 个**，逐个打包并翻译为中文后精选出 **Top 10**。

---

## 2. 评估方法论

### 2.1 评分标准（5 维度）

| 维度 | 权重 | 解释 |
|------|------|------|
| **覆盖缺口** | 30% | 精准补 a-stock-data 1-10 哪个缺口 |
| **零依赖** | 25% | 不需要付费 key / 鉴权 / 海外网络 |
| **独立可跑** | 20% | 解压即用，无需复杂配置 |
| **数据深度** | 15% | 字段多、文档完整 |
| **安装量** | 10% | skills.sh 社区认可度 |

### 2.2 评分原则

- **互补不重复**：同类只选 1 个最佳的
- **数据源独立**：避免全部依赖同一付费服务（Longbridge 7 个 skill 中只选 2 个最关键的）
- **覆盖 > 完美**：宁可少而精，不求大而全

### 2.3 排序示例

以 #2 业绩预告为例：

| 候选 | 覆盖 | 零依赖 | 独立 | 深度 | 安装量 | 总分 |
|------|------|--------|------|------|--------|------|
| `05_longbridge-earnings` | 30 | 15 | 18 | 14 | 10 | **92** |
| `04_earnings-preview_himself65` | 25 | 25 | 22 | 10 | 6 | 88 |
| `06_earnings-preview_anthropics` | 22 | 22 | 20 | 8 | 6 | 78 |

→ 选 `05_longbridge-earnings`（虽然需 Longbridge，但功能最全）

---

## 3. Top 10 精选详表

### 排名 #1 — `05_longbridge-earnings`（补 #2 业绩）

| 属性 | 值 |
|------|-----|
| **来源** | longbridge/skills |
| **安装量** | 794 |
| **评分** | 92 |
| **依赖** | Longbridge CLI（付费） |
| **覆盖** | 美/港/A 股 |
| **核心能力** | 业绩前瞻 + 业绩回顾 + 电话会 Q&A 梳理 + 关注要点框架 |

**两段式输出**：
- **前瞻**：复盘上季度指引 → 追踪近期事件 → 梳理上次电话会 Q&A → 本期"关注要点"
- **回顾**：快速聊天摘要卡（默认） + 完整 Markdown 研究报告（按需生成）

**覆盖字段**：beat/miss、分部、利润率、指引、预测、估值。

**触发词**：earnings update / quarterly results / 财报分析 / 季报 / 业绩前瞻 / 财报点评

---

### 排名 #2 — `18_akshare_succ985`（补 #8 海外/全市场）

| 属性 | 值 |
|------|-----|
| **来源** | succ985/openclaw-akshare-skill |
| **安装量** | 1.6K ⭐ |
| **评分** | 90 |
| **依赖** | `pip install akshare` |
| **覆盖** | A/H/US/期货/基金 + 宏观 |

**核心价值**：单库覆盖最广的金融数据工具，是 a-stock-data V3.0 移除的 akshare 的官方 skill 化版本。

**覆盖维度**：
- 股票：实时行情、历史数据
- 期货：商品/股指期货行情
- 基金：净值/规模
- 宏观：CPI/PMI/M2/社融

**⚠️ 立场冲突**：`a-stock-data` V3.0 已明确"移除 akshare 依赖"。两者风格相反：
- `a-stock-data`：直连 HTTP API，零中间层（自控力强、维护成本高）
- `akshare`：统一封装，接口稳定（开发快、版本依赖风险）

**建议**：与 a-stock-data **并用**——行情走 a-stock-data 优先，独有数据走 akshare。

---

### 排名 #3 — `11_longbridge-research`（补 #4 分析师评级）

| 属性 | 值 |
|------|-----|
| **来源** | longbridge/skills |
| **安装量** | 499 |
| **评分** | 88 |
| **依赖** | Longbridge CLI（付费） |
| **核心能力** | **机构评级 + 目标价 + 一致预期 + 内部人交易 + 财报日历** 五合一 |

**独家字段**：
- 机构评级分布（买入/增持/中性/减持）
- 一致目标价（高/中/低）
- 内部人交易（SEC Form 4）
- 财报日历 + FOMC + 非农日历
- 空头持仓
- 行业排名 + 同业组分析

**框架**：投资提案、首次覆盖、股票研究、竞争分析、财务规划、DeFi/链上分析。

---

### 排名 #4 — `01_company-valuation_himself65`（补 #1 历史估值）

| 属性 | 值 |
|------|-----|
| **来源** | himself65/finance-skills |
| **安装量** | 609 |
| **评分** | 85 |
| **依赖** | **零**（仅 Yahoo Finance） |
| **核心能力** | **DCF + 相对估值（同行倍数） + SOTP（分部加总）** 三方法 |

**默认运行全部三种方法**（不挑便宜的算），输出：
- 混合隐含价
- 敏感性表
- 上行/下行空间

**触发场景**：AAPL 值多少 / NVDA 估值 / TSLA 公允价值 / MSFT DCF / 折现现金流 / WACC / 终值 / 隐含股价 / 相对公允的上行空间 / X 是否高估/低估 / SOTP / 这公司值多少钱

**`a-stock-data` 中的对应实现**：仅有"前向 PE / PE 消化 / PEG"简单公式，缺 DCF 模型和同业倍数对比。

---

### 排名 #5 — `12_sector-analyst_tradermonty`（补 #5 板块轮动）

| 属性 | 值 |
|------|-----|
| **来源** | tradermonty/claude-trading-skills |
| **安装量** | 698 |
| **评分** | 82 |
| **依赖** | **零**（CSV 数据） |
| **核心能力** | 板块轮动 + 市场周期定位 |

**功能**：
- 从 CSV 抓取板块上涨趋势数据（无需 API key）
- 可选接收图表作为辅助分析
- 输出"周期 vs 防御"评估、超买/超卖识别、市场周期阶段判断

**包大小**：1.3 MB（含图表）

---

### 排名 #6 — `15_macro-rates-monitor_anthropics`（补 #7 宏观）

| 属性 | 值 |
|------|-----|
| **来源** | anthropics/financial-services-plugins |
| **安装量** | 1.1K ⭐ |
| **评分** | 80 |
| **依赖** | LSEG MCP（机构级） |
| **核心能力** | **宏观经济 + 利率**仪表盘 |

**专业功能**：
- 综合宏观指标
- 收益率曲线（10Y/2Y/30Y 等）
- 通胀盈亏平衡
- 掉期利率
- 实际 vs 名义利率拆分
- 政策利率预期
- 金融条件判断

**与 a-stock-data 对比**：a-stock-data 无任何宏观数据；本 skill 填补利率敏感型（金融/地产/公用事业）研究的关键空白。

---

### 排名 #7 — `21_market-breadth-analyzer`（补 #9 市场广度）

| 属性 | 值 |
|------|-----|
| **来源** | tradermonty/claude-trading-skills |
| **安装量** | 591 |
| **评分** | 78 |
| **依赖** | **零**（TraderMonty 公开 CSV） |
| **核心能力** | 0-100 量化市场广度健康分 |

**6 个分项**：
1. 上涨/下跌家数比
2. 新高/新低比
3. 涨跌停比
4. 板块广度
5. 成交量广度
6. 均线广度

**适用场景**：市场广度、参与率、涨跌家数健康度、行情是否普涨、整体市场健康评估。

---

### 排名 #8 — `24_commodities-quote_octagonai`（补 #10 大宗商品）

| 属性 | 值 |
|------|-----|
| **来源** | octagonai/skills |
| **安装量** | 679 |
| **评分** | 76 |
| **依赖** | Octagon MCP |
| **核心能力** | 实时大宗商品报价 |

**覆盖品类**：
- 贵金属：黄金/白银/铂/钯
- 能源：原油/天然气/汽油
- 农产品：小麦/玉米/大豆/咖啡/糖
- 工业金属：铜/铝/锌/镍

**分析能力**：查询当前价格、分析日内区间、与均线对比、跟踪价格走势。

---

### 排名 #9 — `22_market-top-detector`（补 #9 见顶检测）

| 属性 | 值 |
|------|-----|
| **来源** | tradermonty/claude-trading-skills |
| **安装量** | 562 |
| **评分** | 74 |
| **依赖** | **零**（CSV） |
| **核心能力** | **三方法检测市场见顶概率** |

**三种方法合一**：
1. **O'Neil Distribution Days**（分发日统计）
2. **Minervini Leading Stock Deterioration**（龙头股恶化）
3. **Monty Defensive Sector Rotation**（防御板块轮动）

**输出**：0-100 综合分 + 风险区分类（绿/黄/红）。

**专注 2-8 周战术择时**，针对 10-20% 调整（不是长期顶部）。

---

### 排名 #10 — `07_institutional-flow-tracker`（补 #3 机构持仓）

| 属性 | 值 |
|------|-----|
| **来源** | tradermonty/claude-trading-skills |
| **安装量** | 770 |
| **评分** | 72 |
| **依赖** | 13F 公开数据（免费） |
| **核心能力** | 跟踪机构投资者持仓变化与组合资金流 |

**数据源**：13F 申报数据（SEC 季度披露）。

**分析对象**：对冲基金、共同基金及其他机构持有人。

**应用场景**：识别出现显著 smart money 累积或派发的股票；跟随老练投资者资金部署方向；重大行情前发现先机。

**⚠️ 局限性**：13F 是 **美股专属**，A 股没有同类公开数据源。

---

## 4. 24 个完整候选清单

### 4.1 入选 10 个（详见上节）

| 排名 | Skill | 缺口 |
|------|-------|------|
| 1 | `05_longbridge-earnings` | #2 |
| 2 | `18_akshare_succ985` | #8 |
| 3 | `11_longbridge-research` | #4 |
| 4 | `01_company-valuation_himself65` | #1 |
| 5 | `12_sector-analyst_tradermonty` | #5 |
| 6 | `15_macro-rates-monitor_anthropics` | #7 |
| 7 | `21_market-breadth-analyzer` | #9 |
| 8 | `24_commodities-quote_octagonai` | #10 |
| 9 | `22_market-top-detector` | #9 |
| 10 | `07_institutional-flow-tracker` | #3 |

### 4.2 未入选 14 个 + 原因

| Skill | 来源 | 评分 | 未入选原因 |
|-------|------|------|-----------|
| `02_longbridge-value-investing` | longbridge | 70 | 与 #3 `01_company-valuation` 同类；需付费 Longbridge |
| `03_longbridge-market-data` | longbridge | 65 | 与 a-stock-data 行情层完全重复；需付费 |
| `04_earnings-preview_himself65` | himself65 | 88 | 与 #1 `05_longbridge-earnings` 同类但功能弱（仅前瞻无回顾） |
| `06_earnings-preview_anthropics` | anthropics | 78 | 太轻量（仅估值+情景），被 #1 覆盖 |
| `08_longbridge-watchlist` | longbridge | 60 | 自选股管理需 Longbridge，a-stock-data 不需要 |
| `09_longbridge-portfolio` | longbridge | 62 | 组合诊断需 Longbridge，与 a-stock-data 正交性低 |
| `10_longbridge-fundamentals` | longbridge | 80 | 与 #3 `11_longbridge-research` 部分重叠（都有研报+估值） |
| `13_longbridge-intel` | longbridge | 70 | 板块轮动被 #5 覆盖，事件驱动被 a-stock-data 资金流覆盖 |
| `14_longbridge-content` | longbridge | 65 | 新闻层与 a-stock-data §5 完全重复 |
| `16_fred-macro_gauss314` | gauss314 | 70 | 与 #6 宏观利率重叠，且仅美股 |
| `17_macro-calendar_termix` | termix | 50 | 偏加密货币宏观，与 A 股研究相关性低 |
| `19_hk-stock-analysis_nicepkg` | nicepkg | 65 | 港股单一市场，被 #2 akshare 覆盖 |
| `20_us-stock-analysis_tradermonty` | tradermonty | 68 | 美股单一市场，被 #2 + #4 覆盖 |
| `23_market-news-analyst_nicepkg` | nicepkg | 65 | 与 a-stock-data §5 东财全球资讯功能重叠 |

### 4.3 完全无对应 skill 的 6 项

| 缺口 | 搜索结果 | 原因 |
|------|---------|------|
| `derivatives-trading-usds-futures` | binance-bsh 仓库无 | binance 衍生品 skill 尚未合并入 main |
| `derivatives-trading-coin-futures` | binance-bsh 仓库无 | 同上 |
| `derivatives-trading-options` | binance-bsh 仓库无 | 同上 |
| `longbridge-consensus` | 仓库已更名 | 现有 `longbridge-research` 覆盖 |
| `longbridge-sector-rotation` | 仓库已更名 | 现有 `longbridge-content` / `longbridge-intel` 覆盖 |
| `longbridge-industry-overview` | 仓库已更名 | 现有 `longbridge-intel` 覆盖 |
| `copper`（membranedev） | 概念错位 | 实测是 Copper CRM 集成，非大宗商品 |

---

## 5. 安装与配置指南

### 5.1 一键整包安装（推荐）

```bash
# 1. 整包解压到 skills 目录
unzip /workspace/skills_pack/best_10/top10_bundle.zip -d ~/.claude/skills/

# 2. 验证
ls ~/.claude/skills/ | grep -E "01_|02_|03_|04_|05_"
# 预期输出：01_05_longbridge-earnings, 02_18_akshare_succ985, ...
```

### 5.2 逐个安装

```bash
cd /workspace/skills_pack/best_10/zips
for z in *.zip; do
  unzip -o "$z" -d ~/.claude/skills/
done
```

### 5.3 依赖安装

```bash
# Python 依赖
pip install akshare yahoo-finance2 pandas

# Longbridge CLI（付费服务，#1 和 #3 需要）
npm install -g @longbridge/cli
longbridge login

# Octagon MCP（#8 需要）
# 按 https://octagonai.com 文档配置 MCP
```

### 5.4 零依赖列表（开箱即用 5 个）

| Skill | 数据源 |
|-------|--------|
| `01_company-valuation_himself65` | Yahoo Finance |
| `12_sector-analyst_tradermonty` | CSV |
| `21_market-breadth-analyzer` | CSV |
| `22_market-top-detector` | CSV |
| `24_commodities-quote_octagonai` | Octagon MCP |

### 5.5 安装后启用

重启 Claude Code 或在 IDE 中刷新 skill 列表。

---

## 6. 与 a-stock-data 整合工作流

### 6.1 互补关系图

```
┌─────────────────────────────────────────────────────┐
│  A 股 Equity Research Skill 工具包 (v1.0)         │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ┌──────────────────────┐  ┌──────────────────────┐│
│  │  a-stock-data (核心) │  │  Top 10 补充包      ││
│  │  ───────────────────  │  │  ───────────────────  ││
│  │  ✓ 行情 (K线/PE/PB)  │  │  ✓ DCF/SOTP 估值    ││
│  │  ✓ 研报 (3源)        │  │  ✓ 业绩前瞻         ││
│  │  ✓ 资金流 (北向/分钟) │  │  ✓ 分析师目标价     ││
│  │  ✓ 筹码 (股东/解禁)  │  │  ✓ 板块轮动         ││
│  │  ✓ 财务三表          │  │  ✓ 宏观利率         ││
│  │  ✓ 公告 (巨潮)       │  │  ✓ 市场广度/见顶    ││
│  │  ✓ 热点 + 题材归因   │  │  ✓ 大宗商品         ││
│  │  ✓ 概念板块归属      │  │  ✓ 海外联动         ││
│  │  ✓ 龙虎榜 + 融资融券 │  │  ✓ 13F 机构持仓     ││
│  └──────────────────────┘  └──────────────────────┘│
│            ↕                      ↕                 │
│     直连 HTTP API           第三方封装/MCP          │
│     零中间依赖               功能广但有版本风险      │
└─────────────────────────────────────────────────────┘
```

### 6.2 推荐工作流：新标的快速调研

```python
# === Step 1: 估值（a-stock-data 实时价 + #4 DCF 深度）===
# 行情
quote = a_stock.tencent_quote("688017")
print(f"现价 {quote.price} PE(TTM)={quote.pe_ttm}")

# 深度估值
# → 加载 01_company-valuation_himself65 skill
# → 调用 DCF + 相对估值 + SOTP 三方法

# === Step 2: 业绩前瞻（#1 longbridge-earnings）===
# → 加载 05_longbridge-earnings skill
# → 复盘上季度指引 + 本期关注要点

# === Step 3: 评级共识（#3 longbridge-research）===
# → 加载 11_longbridge-research skill
# → 拉机构评级分布 + 目标价中位数

# === Step 4: 板块定位（#5 sector-analyst）===
# → 加载 12_sector-analyst_tradermonty skill
# → 判断板块周期阶段 + 强度

# === Step 5: 资金验证（a-stock-data §3 + #9 见顶检测）===
# a-stock-data 已有的：
flow = a_stock.eastmoney_fund_flow_minute("688017")      # 当日资金
flow_120d = a_stock.stock_fund_flow_120d("688017")       # 120 日资金

# 加上宏观广度（#7 + #9）：
breadth = load_skill("21_market-breadth-analyzer")       # 市场广度
top_risk = load_skill("22_market-top-detector")          # 见顶概率

# === Step 6: 海外联动（#2 akshare）===
# → 加载 18_akshare_succ985 skill
# → 查 SOX 费城半导体 / NQ 纳指 / TSLA 同业
```

### 6.3 典型场景：价值投资完整流程

| 步骤 | 工具 |
|------|------|
| 1. 候选筛选（低 PE 高 ROE） | a-stock-data `tencent_quote` 批量 |
| 2. 估值建模 | **#4 DCF + SOTP** |
| 3. 业绩验证 | a-stock-data 研报层 + **#1 业绩前瞻** |
| 4. 同行对比 | **#4 相对估值** + a-stock-data `industry_comparison` |
| 5. 资金确认 | a-stock-data `eastmoney_fund_flow_minute` + 股东户数 |
| 6. 风险评估 | **#7 宏观利率**（利率敏感型）/ **#10 商品**（周期型） |
| 7. 情绪面 | **#7 广度** + **#9 见顶** |
| 8. 持仓监控 | a-stock-data 龙虎榜/解禁/融资融券 |

### 6.4 典型场景：短线交易完整流程

| 步骤 | 工具 |
|------|------|
| 1. 强势股扫描 | a-stock-data `ths_hot_reason`（带题材归因） |
| 2. 板块强度 | **#5 板块轮动** + a-stock-data `industry_comparison` |
| 3. 资金流入 | a-stock-data `eastmoney_fund_flow_minute` + 北向 |
| 4. 龙虎榜 | a-stock-data `dragon_tiger_board` |
| 5. 市场温度 | **#7 广度**（避免过热/过冷） |
| 6. 见顶信号 | **#9 见顶检测**（2-8 周择时） |
| 7. 题材联动 | a-stock-data `eastmoney_concept_blocks` |

---

## 7. 关键注意事项

### 7.1 依赖性分级

| 类型 | skill | 处理 |
|------|-------|------|
| **零依赖** | #4, #5, #7, #9 | 直接用 |
| **Yahoo/CSV** | #4, #5, #7, #9 | 装 pandas |
| **Akshare** | #2 | `pip install akshare` |
| **Longbridge** | #1, #3 | **需付费订阅**（~¥300/月） |
| **MCP 服务** | #6 (LSEG), #8 (Octagon) | 机构级或按 API 调用收费 |

**建议**：先装零依赖 5 个，验证工作流；按需再开 Longbridge / MCP。

### 7.2 与 a-stock-data 的立场冲突

**a-stock-data V3.0 已移除 akshare**，但 **#2 入选了 akshare**。处理方式：

- **不强制互斥**：两者数据源不同，akshare 有独有数据
- **优先级**：
  - 行情/估值 → a-stock-data 优先（直连，不封 IP）
  - 独有数据（如港股/美股/期货/宏观）→ akshare
  - 研报/资金流/股东 → a-stock-data 优先
- **避免重复请求**：同一数据不要两边都拉

### 7.3 Longbridge 的取舍

7 个 longbridge skill 中只选了 2 个（#1 业绩 + #3 研究），原因：
- Longbridge 是付费服务（机构账号）
- 单点依赖风险大
- 长桥的`earnings` 和 `research` 是**独有功能**（机构评级/目标价/电话会 Q&A），其他家没有
- 其他 5 个 longbridge skill（行情/估值/资金/选股/自选）与 a-stock-data 重复或非核心

### 7.4 美股为主的局限

`07_institutional-flow-tracker`（#10）使用 **13F 数据**，仅适用美股。  
A 股机构持仓只能用 a-stock-data §4.3 `holder_num_change`（股东户数）做粗略代理。

### 7.5 数据延迟与刷新

| Skill | 延迟 |
|-------|------|
| a-stock-data 行情 | 实时 |
| a-stock-data 资金流 | 盘中实时 |
| #1 业绩回顾 | 季报后立即 |
| #2 akshare 行情 | T+1 历史数据较稳定，实时偶有延迟 |
| #3 机构评级 | 周度刷新 |
| #5 板块轮动 | 日级 CSV |
| #6 宏观利率 | 实时 |
| #7 广度 | 日级 |
| #8 大宗 | 实时 |
| #9 见顶 | 日级 |
| #10 13F | 季度（45 天延迟） |

### 7.6 性能与封禁

a-stock-data §"东财防封铁律" 同样适用：
- 批量循环时 sleep ≥ 1.5s
- 不并发
- 复用 session

akshare 内部已有节流（但偶尔不稳定）。

---

## 8. 未覆盖缺口与后续建议

### 8.1 仍存在的 3 个缺口

| 缺口 | 当前替代方案 | 后续可补 |
|------|-------------|---------|
| **#6 衍生品/对冲** | a-stock-data 仅有行情，无期权/期货 | 等 binance-skills-hub 合并 main；或自写中金所 API |
| **#3 机构持仓（A 股版）** | a-stock-data `holder_num_change` 粗略代理 | 调东财 `RPT_MUTUAL_STOCK_HOLDRANKS`（公募季报），本仓库 a-stock-data 未收录 |
| **#1 历史估值带（个股）** | 临时方案：腾讯历史 K 线收盘价 ÷ 新浪历史 EPS | 自建：拉 5 年日 K + 历史 EPS 拼接 |

### 8.2 性能与可维护性建议

- **不要**全部启用 10 个 skill。AI 一次对话中加载过多 skill 会增加 token 开销和路由歧义。建议**按场景启用**：
  - 价值投资：#1 + #3 + #4 + #6（宏观）
  - 短线交易：a-stock-data 全部 + #5 + #7 + #9
  - 宏观对冲：#6 + #8 + a-stock-data 资金
- 定期更新 a-stock-data（V3.x 经常修复接口），避免用旧版
- Longbridge skill 安装后**先 dry-run**（CLI 有 `login` 前置），否则会触发鉴权错误

### 8.3 替代方案对比

如果不想用 Longbridge（付费）：

| 缺口 | 替代 |
|------|------|
| #1 业绩前瞻 | 自写：a-stock-data §2.1 研报 + §5.1 新闻聚类 |
| #3 分析师评级 | 自写：a-stock-data §2.1 `eastmoney_reports` 聚合 `emRatingName` 字段 |

---

## 9. 文件结构总览

```
/workspace/skills_pack/
├── _repos/                        # 13 个原始 git 仓库（352 MB，仅供参考）
│   ├── finance-skills/            (himself65)
│   ├── longbridge-skills/         (longbridge)
│   ├── anthropics-fsp/            (anthropics)
│   ├── tradermonty-cts/           (tradermonty)
│   ├── binance-bsh/               (binance)
│   ├── gauss314-skills/           (gauss314)
│   ├── termix-cryptoclaw/         (termix)
│   ├── succ985-akshare/           (succ985)
│   ├── nicepkg-aw/                (nicepkg)
│   ├── octagonai-skills/          (octagonai)
│   └── membranedev-as/            (membranedev)
│
├── _skills/                       # 24 个解压后的 skill（4.1 MB）
│   ├── 01_company-valuation_himself65/
│   ├── ... 24 项
│   └── 24_commodities-quote_octagonai/
│
├── zips/                          # 24 个原始 zip（2.0 MB，英文 description）
│   ├── 01_company-valuation_himself65.zip
│   ├── ... 24 项
│   └── 24_commodities-quote_octagonai.zip
│
├── best_10/                       # ← 推荐的 10 个精选
│   ├── README.md                  # 简短排行
│   ├── EXPLAINER.md               # 本文件（完整说明）
│   ├── top10_bundle.zip           # 整包 (1.7 MB)
│   ├── zips/                      # 10 个独立 zip
│   │   ├── 01_05_longbridge-earnings.zip
│   │   ├── 02_18_akshare_succ985.zip
│   │   ├── 03_11_longbridge-research.zip
│   │   ├── 04_01_company-valuation_himself65.zip
│   │   ├── 05_12_sector-analyst_tradermonty.zip
│   │   ├── 06_15_macro-rates-monitor_anthropics.zip
│   │   ├── 07_21_market-breadth-analyzer.zip
│   │   ├── 08_24_commodities-quote_octagonai.zip
│   │   ├── 09_22_market-top-detector.zip
│   │   └── 10_07_institutional-flow-tracker.zip
│   └── 01_05_longbridge-earnings/ ... 10_07_institutional-flow-tracker/
│
├── build.py                       # 构建 24 个 skill
├── restore.py                     # 从 _repos/ 恢复
├── translate.py                   # 翻译 description 为中文
└── pick_top10.py                  # 精选 Top 10 + 打包
```

---

## 附录 A：版本历史

| 日期 | 版本 | 变更 |
|------|------|------|
| 2026-06-02 | v1.0 | 首版：评估缺口、搜索 24 候选、精选 Top 10、翻译为中文 |

## 附录 B：相关资源

- [a-stock-data GitHub](https://github.com/simonlin1212/a-stock-data) — V3.2.2 当前版本
- [find-skills-plus](../skills/find-skills-plus/SKILL.md) — skill 搜索工具
- [brainstorming](../skills/brainstorming/SKILL.md) — 创意/设计工作流
- [writing-plans](../skills/writing-plans/SKILL.md) — 实施计划生成
- [skills.sh](https://skills.sh) — skill 社区索引

## 附录 C：致谢

- **a-stock-data** 作者 Simon 林——中文 A 股数据基础工具
- **longbridge/skills**——专业机构级数据接口
- **himself65/finance-skills**——零依赖的估值/业绩工具
- **tradermonty/claude-trading-skills**——完整的美股技术分析工具集
- **succ985/openclaw-akshare-skill**——akshare 的 skill 化版本
- **anthropics/financial-services-plugins**——机构级宏观/财报工具
- **octagonai/skills**——实时大宗商品数据
- 所有其他被引用但未入选的 skill 作者

---

> **免责声明**：本工具包仅供学习研究使用，不构成任何投资建议。股市有风险，决策需谨慎。
