# 10 大 Skill 使用文档

> A 股 / 港股 / 美股 Equity Research 一站式工具包
```

---

## 1. longbridge-earnings — 财报分析

### 用途
- **业绩前瞻**（财报发布前）：复盘上季度指引 + 近期事件 + 上次电话会 Q&A → 给出本期"关注要点"框架
- **业绩回顾**（财报发布后）：beat/miss、分部、利润率、指引、预测、估值全套分析
- 适用市场：美股 / 港股 / A 股

### 两种输出模式
| 模式 | 触发关键词 | 产物 | 耗时 |
|------|----------|------|------|
| **Lite（默认）** | 任何财报相关问题 | 聊天内 8 段摘要卡 | 2-3 分钟 |
| **完整研报** | "完整报告"/"深度分析"/"研报" | Markdown 文件 | 8-10 分钟 |

### 快速上手
```bash
# Step 1: 一次脚本拉全部数据
python3 ~/.claude/skills/longbridge-earnings/scripts/collect.py 700.HK

# Step 2: 在对话里看到 Lite 摘要卡

# Step 3: 想要完整版？
# 回复"生成完整报告" → 触发完整研报模式
```

### 输出摘要卡的 8 个模块
1. Header（公司+代码+季度+评级+目标价+当前价+隐含涨跌幅）
2. 核心 KPI 表（实际 / YoY / vs 估计）
3. 分部营收（含 Unicode 占比条）
4. 季度趋势（近 6-8 季）
5. Thesis 状态（🟢/🟡/🟠 标记）
6. 卖方一致预期
7. 下季度一致预期
8. 风险点

### 替代品选择指南
- 想要"PE/PB 历史分位" → `longbridge-fundamentals`
- 想要"X vs Y vs Z 多股对比" → `longbridge-research`
- 想要"实时报价/估值指数" → `longbridge-market-data`

### 注意事项
- 仅推荐 Longbridge 数据源，不主动引导到第三方平台
- HK 代码自动去前导零（`09988.HK` → `9988.HK`）
- 无 Python 时：可手动调用 `longbridge <cmd> --format json`，**并行**调用

---

## 2. akshare — 中文金融数据

### 用途
- A 股 / 港股 / 美股 / 期货 / 基金的实时与历史数据
- 宏观经济指标（GDP / CPI / PMI）
- 零门槛、Python 库、直接 import 用

### 安装
```bash
pip install akshare
```

### 速查代码片段
```python
import akshare as ak

# A 股实时行情
df = ak.stock_zh_a_spot_em()                    # 全 A 股
df = ak.stock_zh_a_hist("000001", "daily", "20240101", "20241231", adjust="qfq")

# 港股
df = ak.stock_hk_spot_em()
df = ak.stock_hk_hist("00700", "daily", adjust="qfq")

# 美股
df = ak.stock_us_spot_em()

# 期货
df = ak.futures_zh_spot()
df = ak.futures_zh_hist_sina("IF0")

# 基金
df = ak.fund_open_fund_info_em()
df = ak.fund_open_fund_info_em(fund="000001", indicator="单位净值走势")

# 宏观
df = ak.macro_china_gdp()       # GDP
df = ak.macro_china_cpi()       # CPI
df = ak.macro_china_pmi()       # PMI
```

### 周期与复权参数
- 周期：`daily` / `weekly` / `monthly`
- 复权：`qfq` 前复权 / `hfq` 后复权 / `""` 不复权

### 注意事项
- AkShare 不自带缓存，请求频繁可能被封 IP，需自建缓存
- 全部返回 pandas DataFrame，可直接 to_csv / 画图
- 网络错误要自己做重试逻辑

### 何时不用
- 需要**秒级实时**（AkShare 有分钟级延迟）→ 用券商/行情软件
- 需要**财务三表深度**→ 用 `longbridge-research` 或 `company-valuation`

---

## 3. longbridge-research — 机构数据 + 卖方研究框架

### 用途
**数据类**：
- 机构评级 / 目标价 / EPS 一致预期
- 财报日历 / 股东 / 基金持仓
- 内部人交易（SEC Form 4）/ 13F 持仓
- 空头持仓 / 行业排名 / 同业组树

**框架类**：
- 投资提案（investment proposal）
- 首次覆盖（coverage initiation）
- 股票研究快照 / 竞争分析
- 投资逻辑跟踪 / 投后监控
- 港股 IPO 分析 / 财务规划
- DeFi 收益 / 链上数据

### 快速上手
```bash
# 数据查询
longbridge institution-rating AAPL
longbridge forecast-eps NVDA
longbridge consensus TSLA
longbridge finance-calendar AAPL
longbridge shareholder BRK.B
longbridge insider-trades AAPL
longbridge investors BRK            # 13F 持仓
longbridge industry-rank Technology

# 框架：参考 references/ 下的 markdown
# 例如想做"投资提案" → 读 references/investment-proposal.md
```

### 23 个 references 文件
| 路由键 | 触发用户意图 |
|-------|-------------|
| institution-rating | 机构评级 / 目标价 |
| forecast-eps | EPS / 营收预测 |
| consensus | 一致目标价 |
| finance-calendar | 财报日历 / FOMC / 非农 |
| shareholder | 机构股东 |
| fund-holder | 基金 / ETF 持仓 |
| insider-trades | SEC Form 4 内部人 |
| investors | 13F 持仓 |
| short-positions | 空头持仓 |
| short-trades | 日内做空量 |
| industry-rank | 行业排名 |
| industry-peers | 同业组树 |
| investment-ideas | 投资想法 |
| investment-proposal | 投资提案 |
| coverage-initiation | 首次覆盖 |
| stock-research | 股票研究快照 |
| competitive-analysis | 竞争分析 |
| thesis-tracker | 投资逻辑跟踪 |
| post-investment | 投后监控 |
| hkipo-analysis | 港股 IPO |
| financial-planning | 财务规划 |
| company-profile | 公司画像 |
| company-tearsheet | 一页纸报告 |
| defi-yield / onchain | DeFi / 链上数据 |

### 注意事项
- **DeFi/链上数据**需 WebSearch 补（DefiLlama / CoinGecko / Glassnode）
- 内部人数据**只覆盖美股**（SEC Form 4）
- 全部 CLI 命令**无需登录**

### 何时用兄弟 skill
| 用户要 | 用 |
|------|---|
| 财报点评 / 业绩前瞻 | `longbridge-earnings` |
| 财务三表 / 估值深度 | `longbridge-fundamentals` |
| 每日增量简报 | `longbridge-intel` |

---

## 4. company-valuation — DCF + 相对估值 + SOTP

### 用途
三方法估值并加权得到隐含股价：
1. **DCF** — 5 年 FCFF 折现 + 终值
2. **相对估值** — 同行 P/E、EV/Rev、EV/EBITDA 中位数
3. **SOTP** — 多分部公司分部加总（如有 2+ 独立分部）

### 快速上手
```bash
# 安装
pip install yfinance numpy pandas
```
```python
import yfinance as yf
t = yf.Ticker("AAPL")
info = t.info
income = t.income_stmt
cashflow = t.cashflow
price = info.get("currentPrice")
shares = info.get("sharesOutstanding")
# ... 完整模板见 SKILL.md Step 3-7
```

### 4 步运行流程
1. **Step 1 — 环境检测**：yfinance 可用？FMP CLI 可用？10 年期国债利率？
2. **Step 2 — 方法选择**：
   - 成熟现金牛 → DCF + 相对
   - 高增长 SaaS → 相对为主（Rule of 40）
   - 多分部 → DCF + 相对 + SOTP
   - 银行/保险 → P/B、P/TBV（不用 DCF）
3. **Step 3-7 — 拉数据 + 三方法计算 + 5×5 敏感性 + Bull/Base/Bear**
4. **Step 8 — 输出 9 段研报**：Headline / Snapshot / 三方法表 / DCF 构建 / 同业对比 / SOTP / 敏感性 / 情景 / 风险

### 默认参数（用户不指定时用）
| 参数 | 默认值 | 依据 |
|------|-------|------|
| 预测期 | 5 年 | 标准 |
| 终值增速 g | 2.5% | ≈ 长期美国 GDP |
| 无风险 rf | 10 年期实时 / 4.5% | 当前资本成本锚 |
| 股权风险溢价 ERP | 5.5% | Damodaran 中位 |
| Beta | yfinance 实时 | 市场观测 |
| 税率 | 3 年中位，限 15-30% | 剔除一次性 |
| 利润率 | 3 年中位 | 平滑周期 |
| 同行业数 | 4-6 | 平衡信噪 |
| 权重（无 SOTP）| DCF 50% / 相对 50% | 等权三角 |
| 权重（有 SOTP）| DCF 40% / 相对 30% / SOTP 30% | 给 SOTP 加权 |

### 9 段输出结构
1. **Headline 判决**：blended 公允价 vs 现价，% 涨跌幅，最乐观/悲观方法
2. **Snapshot**：行业 / 市值 / 3M、12M 涨跌 / LTM 营收增速
3. **三方法表**：方法 | 隐含价 | 权重 | 理由
4. **DCF 构建**：假设表 + 5 年 FCFF 预测 + EV→股权桥
5. **同业对比**：含 P/E、EV/Rev、EV/EBITDA、毛利率、增速
6. **SOTP**（如有）
7. **5×5 敏感性表**：WACC ±1% × g 1.5-3.5%
8. **情景表**：Bull/Base/Bear + 杠杆 + 隐含价
9. **关键风险**：哪个假设一变答案就翻盘

### 注意事项
- ⚠️ TTM 数据滞后于实时
- ⚠️ DCF 是 garbage-in/garbage-out，**敏感性比点估计重要**
- ⚠️ yfinance 数据非官方，最终决策前查 10-K
- ⚠️ **不是投资建议**

### 何时不用
- 想要"是否便宜"快速判断 → 看 `longbridge-fundamentals` 的 PE/PB Band
- 想要"现价 vs 同行中位"快速判断 → 跳过 DCF，只用相对估值

---

## 5. sector-analyst — 板块轮动 + 周期定位

### 用途
- 分析 11 个 GICS 板块的**上涨趋势比率**（% 站上 50/200 日均线）
- 计算周期 vs 防御的**风险情景评分**
- 识别**超买/超卖**板块
- 估算当前**市场周期阶段**（早周期/中周期/晚周期/衰退）
- 可选：接收图表做行业层细节分析

### 快速上手
```bash
# 安装
pip install requests

# 默认：打印人类可读分析
python3 scripts/analyze_sector_rotation.py

# JSON 输出
python3 scripts/analyze_sector_rotation.py --json

# 保存到文件
python3 scripts/analyze_sector_rotation.py --save --output-dir reports/
```

### 数据源
- **零 API key** —— 从 TraderMonty 公开 GitHub 仓库拉 CSV
- `sector_summary.csv`：上涨趋势比 + 趋势 + 斜率 + 状态
- `uptrend_ratio_timeseries.csv`：日期新鲜度检查

### 5 步分析工作流
1. **CSV 抓取**：跑脚本拿数据
2. **周期评估**：对照 references/sector_rotation.md 框架
3. **当前情况**：综合周期定位 + 表现模式
4. **情景发展**：2-4 个未来情景 + 概率
5. **生成报告**：6 段 Markdown

### 输出文件名
`sector_analysis_YYYY-MM-DD.md`

### 6 段必备输出
1. Executive Summary（2-3 句结论）
2. Current Situation（周期 + 表现模式）
3. Supporting Evidence（支持信号 + 矛盾信号）
4. Scenario Analysis（2-4 个情景 + 概率，**总和 ≈ 100%**）
5. Recommended Positioning（战略 + 战术配置）
6. Key Risks（监控点）

### 概率区间规则
| 区间 | 含义 |
|------|------|
| 70-85% | 强证据 + 多重确认 |
| 50-70% | 中等证据 + 部分混杂 |
| 30-50% | 弱证据 + 冲突 |
| 15-30% | 反向猜测但可能 |

### 注意事项
- 数据可能滞后数天 → 报告里要标注 freshness warning
- **不要先入为主**，让数据引导结论
- 周期阶段是**估计**而非定论，用概率表达

### 何时用兄弟 skill
| 用户要 | 用 |
|------|---|
| 个股是否健康 | `market-breadth-analyzer`（广度） |
| 是不是要减仓 | `market-top-detector`（见顶概率） |
| 宏观背景 | `macro-rates-monitor`（利率曲线） |

---

## 6. macro-rates-monitor — 宏观 + 利率仪表盘

### 用途
- GDP / CPI / 失业率 / PMI 综合判断经济周期位置
- 国债收益率曲线形态（normal / flat / inverted / humped）
- 2s10s、3M-10Y 斜率
- 通胀盈亏平衡 → 实际利率分解
- 掉期利差 → 金融条件松紧
- 历史定价 → 当前利率在历史什么分位

### 前置条件
**必须**：LSEG MCP 已配置（`qa_macroeconomic`、`interest_rate_curve`、`inflation_curve`、`ir_swap`、`tscc_historical_pricing_summaries`）

### 6 步工具链
1. **`qa_macroeconomic`** — GDP / CPI / PCE / 失业 / 薪资 / PMI（多国）
2. **`interest_rate_curve`** — 国债 / 掉期曲线（list → calculate 两步）
3. **`inflation_curve`** — 通胀盈亏平衡 + 实际利率（search → calculate）
4. **`ir_swap`** — 掉期利率（list → price）
5. **`tscc_historical_pricing_summaries`** — 历史定价
6. **综合** — 输出仪表盘

### 4 段输出
1. **Macro Summary 表**：GDP / 核心通胀 / 失业 / PMI，含当前 / 前期 / 方向 / 信号
2. **Yield Curve Snapshot**：3M/2Y/5Y/10Y/30Y 收益 + 2s10s + 3M-10Y 斜率 + 曲线形态
3. **Real Rate Decomposition 表**：5Y/10Y 名义 - 盈亏平衡 = 实际，含"宽松/紧缩"标签
4. **Swap Spread 表**：2Y/5Y/10Y swap - 国债 = 利差 bp
5. **Overall Assessment**：2-3 句综合判断

### 搜索模式
- 美：`"US*GDP*"`、`"US*CPI*"`、`"US*PCE*"`、`"US*UNEMP*"`
- 欧：`"EZ*GDP*"`、`"EZ*HICP*"`
- 英：`"UK*GDP*"`、`"UK*CPI*"`
- 优先**季调**序列；月度为主，GDP 季度

### 注意事项
- **永远先广后深**：先看 GDP / 央行，再看曲线，再看实际利率
- 实际利率 > 0 = 紧缩，< 0 = 宽松
- Swap spread 为负或异常高 = 金融条件紧张
- **不引导用户去 Bloomberg/Refinitiv 之外的终端**

---

## 7. market-breadth-analyzer — 市场广度量化

### 用途
用 6 维度打分系统量化市场广度健康度（0-100）：
1. **Breadth Level & Trend**（25%）：8MA 水平 + 200MA 趋势 + 8MA 方向
2. **8MA vs 200MA 交叉**（20%）：均线缺口 + 方向
3. **峰/谷周期**（20%）：当前在广度周期的位置
4. **Bearish Signal**（15%）：回测过的看跌信号
5. **历史百分位**（10%）：当前 vs 全历史分布
6. **S&P 500 背离**（10%）：20d + 60d 价格 vs 广度

### 快速上手
```bash
# 安装
pip install requests

# 运行（输出到目录）
mkdir -p reports/2026-06-13
python3 skills/market-breadth-analyzer/scripts/market_breadth_analyzer.py \
  --detail-url "https://tradermonty.github.io/market-breadth-analysis/market_breadth_data.csv" \
  --summary-url "https://tradermonty.github.io/market-breadth-analysis/market_breadth_summary.csv" \
  --output-dir reports/2026-06-13
```

### 5 个健康分区
| 分数 | 区域 | 股票仓位 | 动作 |
|------|------|---------|------|
| 80-100 | Strong | 90-100% | 满仓 + 成长/动量 |
| 60-79 | Healthy | 75-90% | 正常 |
| 40-59 | Neutral | 60-75% | 精选 + 紧止损 |
| 20-39 | Weakening | 40-60% | 止盈 + 提现金 |
| 0-19 | Critical | 25-40% | 资本保护 + 等待底部 |

### 数据源
**零 API key** —— GitHub Pages 公开 CSV
- `market_breadth_data.csv`：~2,500 行（2016-至今）
- `market_breadth_summary.csv`：8 个聚合指标

### 输出文件
- `market_breadth_YYYY-MM-DD_HHMMSS.json`
- `market_breadth_YYYY-MM-DD_HHMMSS.md`
- `market_breadth_history.json`（最多 20 条，跨运行持久）

### 注意事项
- 数据 > 5 天会**发出新鲜度警告**
- 任何分项数据缺失时**自动按比例重分配权重**
- 趋势标签（improving / deteriorating / stable）需多次观测
- 报告由脚本生成 → **不要凭记忆写分数**

### 何时用兄弟 skill
| 用户要 | 用 |
|------|---|
| 是不是要减仓 | `market-top-detector`（更战术 2-8 周） |
| 板块层广度 | `sector-analyst` |

---

## 8. commodities-quote — 大宗商品实时报价

### 用途
实时查询贵金属 / 能源 / 农产品的：
- 当前价 + 涨跌 + 涨跌 %
- 日内区间（low/high）
- 50 / 200 日均线
- 52 周区间
- 成交量 + 前收

### 前置条件
**必须**：Octagon MCP 已配置（`octagon-agent` 工具）

### 4 步工作流
1. **确定商品代码**（GCUSD / CLUSD 等，见下表）
2. **调用 Octagon MCP**：
   ```json
   {
     "server": "octagon-mcp",
     "toolName": "octagon-agent",
     "arguments": {"prompt": "Retrieve the real-time price quote for GCUSD."}
   }
   ```
3. **解读数据**（10 字段指标）
4. **分析**（区间位置、均线形态、量价）

### 常用商品代码
**贵金属**：`GCUSD` 黄金 / `SIUSD` 白银 / `PLUSD` 铂 / `PAUSD` 钯
**能源**：`CLUSD` WTI 原油 / `BZUSD` 布伦特 / `NGUSD` 天然气 / `HOUSD` 取暖油 / `RBUSD` 汽油
**基本金属**：`HGUSD` 铜 / `ALUSD` 铝 / `ZNUSD` 锌 / `NIUSD` 镍
**农产品**：`ZCUSD` 玉米 / `ZSUSD` 大豆 / `ZWUSD` 小麦 / `KCUSD` 咖啡 / `SBUSD` 糖 / `CTUSD` 棉花

### 区间位置公式
```
日内位置 = (Current - Day Low) / (Day High - Day Low) × 100%
52 周位置 = (Current - Year Low) / (Year High - Year Low) × 100%
```

### 均线形态速查
| 形态 | 含义 |
|------|------|
| Price > 50D > 200D | 强上升趋势 |
| Price > 200D > 50D | 复苏中 |
| Price < 200D < 50D | 下降趋势起点 |
| Price < 50D < 200D | 强下降趋势 |
| 50D 上穿 200D | 金叉（看涨） |
| 50D 下穿 200D | 死叉（看跌） |

### 量价组合解读
| 组合 | 含义 |
|------|------|
| 高量 + 价升 | 强势买入 |
| 高量 + 价跌 | 强势卖出 |
| 低量 + 价升 | 弱反弹 |
| 低量 + 价跌 | 弱下跌 |

### 商品基本面驱动
| 商品 | 主要驱动 |
|------|---------|
| 黄金 | 美元强弱（反向）、利率（反向）、通胀、地缘 |
| 原油 | OPEC 决策、经济增长（需求）、库存、地缘 |
| 天然气 | 天气、库存、产量、LNG 出口 |

### 何时用兄弟 skill
| 用户要 | 用 |
|------|---|
| 商品市场背景 | `commodities-list` |
| 大盘背景 | `stock-historical-index` |
| 能源板块背景 | `sector-performance-snapshot` |

---

## 9. market-top-detector — 见顶概率 0-100 分

### 用途
**战术** 2-8 周择时信号，预测 10-20% 回调概率。融合 3 大方法：
1. **O'Neil** — Distribution Day 累计（机构卖出）
2. **Minervini** — 龙头股恶化模式
3. **Monty** — 防御板块轮动信号

### 6 维度打分
| # | 分项 | 权重 | 数据源 |
|---|------|------|--------|
| 1 | Distribution Day 数 | 25% | FMP API |
| 2 | 龙头股健康度 | 20% | FMP API |
| 3 | 防御板块轮动 | 15% | FMP API |
| 4 | 广度背离 | 15% | 200DMA 自动 + 50DMA WebSearch |
| 5 | 指数技术形态 | 15% | FMP API |
| 6 | 情绪 + 投机 | 10% | FMP + WebSearch |

### 5 个风险区
| 分数 | 区域 | 风险预算 | 动作 |
|------|------|---------|------|
| 0-20 | Green 正常 | 100% | 正常 |
| 21-40 | Yellow 早期预警 | 80-90% | 紧止损 + 减新仓 |
| 41-60 | Orange 风险升高 | 60-75% | 弱股止盈 |
| 61-80 | Red 高概率见顶 | 40-55% | 激进止盈 |
| 81-100 | Critical 见顶形成 | 20-35% | 最大化防御 + 对冲 |

### 前置条件
- **FMP API Key**：`export FMP_API_KEY=your_key`（免费版 ~33 次/运行）
- **WebSearch 访问**：必填
- **数据新鲜度**：所有手动数据 ≤ 3 个交易日

### 3 步工作流
**Step 1 — WebSearch 抓数据**：
- ✅ 200DMA：自动从 TraderMonty CSV 抓（无需 WebSearch）
- ✅ 50DMA：搜索 "S&P 500 percent stocks above 50 day moving average"
- ✅ Put/Call：搜索 "CBOE equity put call ratio today"
- ⭕ VIX term structure：可选，FMP API 可自动检测
- ⭕ Margin debt YoY：可选（滞后 1-2 月）

**Step 2 — 跑脚本**：
```bash
python3 skills/market-top-detector/scripts/market_top_detector.py \
  --api-key $FMP_API_KEY \
  --breadth-50dma [VALUE] --breadth-50dma-date [YYYY-MM-DD] \
  --put-call [VALUE] --put-call-date [YYYY-MM-DD] \
  --vix-term [steep_contango|contango|flat|backwardation] \
  --output-dir reports/
```

**Step 3 — 解读报告**：综合分 + 风险区 + 最强警告信号 + 历史最相似顶部 + 假设敏感性 + Follow-Through Day 状态

### 与 Bubble Detector 的区别
| 维度 | Top Detector | Bubble Detector |
|------|-------------|-----------------|
| 时间尺度 | 2-8 周 | 数月到数年 |
| 目标 | 10-20% 回调 | 泡沫崩盘（30%+）|
| 方法 | O'Neil / Minervini / Monty | Minsky / Kindleberger |
| 数据 | 价量 + 广度 | 估值 + 情绪 + 社交 |
| 分数范围 | 0-100 综合 | 0-15 分 |

### 注意事项
- **数据陈旧 > 3 天**会严重降低分析质量
- 没有"绝对见顶"，给的是**概率 + 区间**
- 应**配合** `market-breadth-analyzer` 使用

### 何时用兄弟 skill
| 用户要 | 用 |
|------|---|
| 长期泡沫风险 | Bubble Detector（不同 skill） |
| 板块层轮动 | `sector-analyst` |
| 宏观背景 | `macro-rates-monitor` |

---

## 10. institutional-flow-tracker — 13F 机构资金流

### 用途
通过 SEC 13F 季度申报跟踪：
- 机构（对冲基金 / 共同基金 / 养老金）持仓变化
- 识别 **smart money 累积/派发** 的股票
- 跟踪**特定投资人**（巴菲特、ARK 等）的持仓
- 板块层资金轮动

### 数据源
**FMP API**（必填）：
```bash
export FMP_API_KEY=your_key
```
- 免费版：250 次/天（够每季度看 20-30 只股）
- 13F 季度滞后 45 天申报

### 13F 申报时间表
| 季度 | 申报截止 |
|------|---------|
| Q1 (1-3 月) | 5 月中 |
| Q2 (4-6 月) | 8 月中 |
| Q3 (7-9 月) | 11 月中 |
| Q4 (10-12 月) | 2 月中 |

### 5 步分析工作流

**Step 1 — 扫描显著异动**：
```bash
# Top 50 最大变化
python3 scripts/track_institutional_flow.py --top 50 --min-change-percent 10

# 行业筛选
python3 scripts/track_institutional_flow.py --sector Technology --min-institutions 20

# 自定义筛选
python3 scripts/track_institutional_flow.py \
  --min-market-cap 2000000000 \
  --min-change-percent 15 \
  --top 100 \
  --output results.json
```

**Step 2 — 个股深度**：
```bash
python3 scripts/analyze_single_stock.py AAPL
# 输出：8 季度历史 + Top 20 持有人 + 集中度 + 新进/加仓/减仓
```

**Step 3 — 跟踪特定投资人**：
> ⚠️ `track_institution_portfolio.py` **尚未实现**。FMP API 按股票组织数据，按机构重建全组合不现实。
> 替代方案：
> - `analyze_single_stock.py` 输出里搜 "Berkshire"/"ARK"
> - 外部资源：**WhaleWisdom** / **SEC EDGAR** / **DataRoma**

**Step 4 — 信号解读**：
| 信号 | 持仓变化 | 机构数变化 | 当前持仓 | 行动 |
|------|---------|-----------|---------|------|
| **强看涨** | +15% QoQ | +10% | <40% | 考虑买入 |
| **中看涨** | +5-15% | 净正 | 40-70% | 关注 |
| **中性** | <5% | 平衡 | 稳定 | 持有 |
| **中看跌** | -5-15% | 净负 | >80% | 减仓 |
| **强看跌** | -15% | -10% | 集中度高 | 卖出/回避 |

**Step 5 — 组合应用**：
- 新建仓：用机构数据确认 smart money 共识
- 现有持仓：每季度复核 13F，机构撤 → 复核你的逻辑

### 数据可靠度评级
| 等级 | 条件 | 用途 |
|------|------|------|
| **A** | 有前季可比 + 持有人 ≥ 50 | 可直接排名 |
| **B** | 有前季可比 + 持有人 ≥ 10 | 仅参考 |
| **C** | 无前季可比 或 持有人 < 10 | **从筛选结果中排除** |

`track_institutional_flow.py` 自动排除 C 级，`analyze_single_stock.py` 显示 C 级警告。

### 局限性
- ⚠️ **45 天报告延迟** → 是确认指标，不是领先信号
- ⚠️ 只覆盖管理规模 > $100M 的机构
- ⚠️ 只报**多头**（不含空头、期权、债券）
- ⚠️ 季末快照，期间可能已变动
- ⚠️ 相关性 ≠ 因果性

### 何时不用
- 想要**实时盘中信号**（13F 不够快）
- 微市值股（< $100M 市值，机构兴趣低）
- **< 3 个月**短线择时

### 高级组合
- **内部人 + 机构同步买入**：强信号
- **板块层轮动**：聚合板块资金流，领先价格
- **逆向投资**：高质量股被机构卖出 = 潜在价值（需强基本面信念）

### 何时用兄弟 skill
| 用户要 | 用 |
|------|---|
| 候选股筛选 | Value Dividend Screener → 本 skill 验证 |
| 美股深度分析 | US Stock Analysis + 本 skill |
| 组合监控 | Portfolio Manager + 本 skill |
| 技术形态确认 | Technical Analyst + 本 skill |

---

## 附录 A：Skill 路由速查

| 你的问题 | 召唤 |
|---------|------|
| "NVDA 财报前瞻" | `longbridge-earnings` |
| "比亚迪今日行情" | `akshare` |
| "AAPL 机构目标价" | `longbridge-research` |
| "MSFT DCF" | `company-valuation` |
| "现在哪个板块强" | `sector-analyst` |
| "美债曲线倒挂？" | `macro-rates-monitor` |
| "市场广度健康吗" | `market-breadth-analyzer` |
| "黄金现价多少" | `commodities-quote` |
| "是不是见顶了" | `market-top-detector` |
| "巴菲特加仓了什么" | `institutional-flow-tracker` |

---

## 附录 B：常见组合用法

### 1. 个股深度研究（从宏观到个股）
```
macro-rates-monitor     → 看经济周期位置
sector-analyst          → 看板块强弱
market-breadth-analyzer → 看广度健康
longbridge-research     → 拉机构评级 + 目标价
company-valuation       → 算隐含价
longbridge-earnings     → 看最近一份财报
```

### 2. 战术择时（2-8 周）
```
macro-rates-monitor     → 大背景
sector-analyst          → 板块轮动
market-breadth-analyzer → 广度
market-top-detector     → 见顶概率
→ 决定仓位 % 和对冲
```

### 3. A 股多面手
```
akshare                 → 实时行情 / 财务 / 宏观
longbridge-research     → 港股 / 美股联动
sector-analyst          → 板块层
longbridge-earnings     → 业绩点评
company-valuation       → 估值
```

### 4. 季度复盘
```
institutional-flow-tracker → 看 13F 异动
longbridge-research       → 看目标价 / EPS 调整
longbridge-earnings       → 业绩趋势
sector-analyst            → 板块配置再平衡
```

---

## 附录 C：依赖矩阵

| Skill | 零依赖 | CSV/公开 | yfinance | FMP API | Longbridge | MCP | Python 库 |
|-------|-------|---------|----------|---------|------------|-----|----------|
| longbridge-earnings | | | | | ✅ | (MCP 替代) | stdlib |
| akshare | | | | | | | `akshare` |
| longbridge-research | | | | | ✅ | (MCP 替代) | — |
| company-valuation | | | ✅ | (CLI 替代) | | | `yfinance` `numpy` `pandas` |
| sector-analyst | | ✅ | | | | | `requests` |
| macro-rates-monitor | | | | | | ✅ LSEG | — |
| market-breadth-analyzer | | ✅ | | | | | `requests` |
| commodities-quote | | | | | | ✅ Octagon | — |
| market-top-detector | | 部分 | | ✅ | | | `requests` |
| institutional-flow-tracker | | | | ✅ | | | `requests` |

**零 API key / 零登录即可跑**（5 个）：
- `sector-analyst`、`market-breadth-analyzer`、`akshare`（仅 pip）、`company-valuation`（yfinance 免费）、`macro-rates-monitor`（需 MCP）

---

## 附录 D：常见错误排查

| 报错 | 原因 | 解决 |
|------|------|------|
| `command not found: longbridge` | CLI 未装 | 装 longbridge-terminal |
| `ModuleNotFoundError: akshare` | Python 库未装 | `pip install akshare` |
| `ModuleNotFoundError: yfinance` | Python 库未装 | `pip install yfinance numpy pandas` |
| `401 Unauthorized` (FMP) | API key 无效 | 重新申请或检查 `FMP_API_KEY` |
| `MCP tool not found: octagon-agent` | Octagon MCP 未配 | 见 commodities-quote/references/mcp-setup.md |
| `MCP tool not found: qa_macroeconomic` | LSEG MCP 未配 | 配置 LSEG MCP server |
| `Empty CSV response` (Breadth) | GitHub Pages 临时不可用 | 等几分钟重试 |
| `HK symbol 09988.HK not found` | Longbridge 自动去前导零 | 改用 `9988.HK` |

---

## 附录 E：所有文件的本地路径

```
best_10/
├── EXPLAINER.md            ← 项目总览（你已读过）
├── README.md               ← 排行速查
├── USAGE.md                ← 本文档
├── top10_bundle.zip        ← 1.7 MB 总包
├── zips/                   ← 10 个独立 zip
│   ├── 01_05_longbridge-earnings.zip
│   ├── 02_18_akshare_succ985.zip
│   ├── 03_11_longbridge-research.zip
│   ├── 04_01_company-valuation_himself65.zip
│   ├── 05_12_sector-analyst_tradermonty.zip
│   ├── 06_15_macro-rates-monitor_anthropics.zip
│   ├── 07_21_market-breadth-analyzer.zip
│   ├── 08_24_commodities-quote_octagonai.zip
│   ├── 09_22_market-top-detector.zip
│   └── 10_07_institutional-flow-tracker.zip
└── 01_05_longbridge-earnings/  ← 解压后的目录
    ├── SKILL.md
    ├── commands/
    ├── references/
    └── scripts/
```

---

**版本**：v1.0 / 2026-06-13
**配套**：`EXPLAINER.md`（项目背景）/ `README.md`（排行速查）/ `USAGE.md`（本文）
