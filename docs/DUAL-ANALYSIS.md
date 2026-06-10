# DUAL-ANALYSIS 调度入口：双引擎配置

> 这是**主入口文档**。当你用一句话让 AI 分析股票时，它会按本文档的流程调度。
> 创建时间：2026-06-10
> 配套阅读：[README.md](./README.md) · [SERENITY.md](./SERENITY.md)

---

## 一、双引擎是什么？

```
┌──────────────────────────────────────────────────────────────┐
│                    DUAL-ANALYSIS 调度层                       │
│                                                              │
│  触发条件：用户说"分析" / "看看" / "能不能买" / "估值" 等      │
└──────────────────────────────────────────────────────────────┘
                              │
                  ┌───────────┴───────────┐
                  ▼                       ▼
        ┌──────────────────┐    ┌──────────────────┐
        │  Serenity 引擎   │    │ a-stock-data 引擎│
        │  (质性 / 方法论)  │    │ (量化 / 数据)    │
        └──────────────────┘    └──────────────────┘
                  │                       │
                  └───────────┬───────────┘
                              ▼
                  ┌──────────────────────┐
                  │  综合判断 + 操作建议  │
                  └──────────────────────┘
```

---

## 二、调度规则：何时启用哪个引擎

### 2.1 关键词自动匹配

| 关键词 | Serenity 引擎 | a-stock-data 引擎 | 备注 |
|---|:---:|:---:|---|
| "卡点" / "护城河" / "长期持有" | ✅ | ⚪ | Serenity 主导 |
| "估值" / "PE" / "PEG" / "PE 消化" | ⚪ | ✅ | a-stock-data 主导 |
| "产业链" / "供应链" / "瓶颈" | ✅ | ⚪ | Serenity 主导 |
| "研报" / "业绩" / "财务" | ⚪ | ✅ | a-stock-data 主导 |
| "回测" / "历史表现" | ⚪ | ✅ | backtest-expert 主导 |
| "估值泡沫" / "美股有泡沫吗" | ✅ | ✅ | 双引擎 |
| "我的 700 股 159941" | ⚪ | ✅ | a-stock-data 主导 |
| "用 Serenity 的方式看 XXX" | ✅ | ✅ | **强制双引擎** |
| "综合分析" / "能不能买" / "值不值得" | ✅ | ✅ | **默认双引擎** |

### 2.2 标的类型决定权重

| 标的类型 | Serenity 权重 | a-stock-data 权重 |
|---|:---:|:---:|
| 宽基 ETF（159941 / 510300）| 20% | 80% |
| 行业 ETF（159770 / 512480）| 50% | 50% |
| 主题 ETF / 主题股 | 70% | 30% |
| 价值股（银行 / 公用事业）| 60% | 40% |
| 成长股（半导体 / AI）| 70% | 30% |
| 周期股（钢铁 / 化工）| 30% | 70% |
| 妖股 / 微盘股 | 10% | 90% |

---

## 三、双重分析标准流程（4 步法）

### Step 1：标的识别（10 秒）

```
输入：股票代码 / 名称 / 用户描述
输出：
  - 标的类型（ETF / 个股 / 美股 / 港股）
  - 行业归属
  - 流动性等级
  - 风险等级
```

工具：
- `a-stock-data` 的 `tencent_quote()` 拉实时价
- `a-stock-data` 的 `eastmoney_concept_blocks()` 拉板块归属

### Step 2：Serenity 视角（30 秒）

```
输出：
  - Narrative（市场叙事）：现在市场讲什么故事
  - Structure（产业结构）：产业链上谁卡什么
  - Moat（护城河）：5 问评估卡点强度
  - 投资类型（壁垒/卡点/看涨期权/周期）
  - 关键风险（地缘/政策/技术替代）
```

工具：
- `serenity-skill` 的 5 问
- `china-macro-analyst` 拉政策
- `serenity-radar` 扫行业最新事件
- `follow-aleabito` 看 Serenity 原作者最新观点

### Step 3：a-stock-data 视角（30 秒）

```
输出：
  - 估值数据：PE / PB / 涨跌幅 / 资金流
  - 一致预期：研报覆盖数 / EPS 预测 / 评级
  - 资金信号：北向 / 主力 / 龙虎榜
  - 风险数据：波动率 / 换手率 / 涨跌幅历史分位
  - 新闻信号：最近新闻、公告、研报
```

工具：
- `a-stock-data` 7 层数据源
- `backtest-expert` 历史回测
- `market-news-analyst` 新闻影响

### Step 4：综合判断（10 秒）

```
输出（3 选 1）：
  🟢 建议买入 / 持有（双重确认）
  🟡 观望 / 等回调（一项确认，一项未确认）
  🔴 建议卖出 / 规避（双重否定）
```

模板：

```markdown
# {代码} {名称} 双重分析报告

## 1. 标的速览
- 当前价: ¥{price}
- 涨跌: {chg}%
- 行业: {industry}
- 市值: {mcap}亿

## 2. Serenity 视角
- 叙事: ...
- 卡点: .../5
- 护城河: ...
- 投资类型: ...
- Serenity 评分: {X}/10

## 3. a-stock-data 视角
- PE(TTM): ...
- 一致预期: ...
- 资金流: ...
- 数据评分: {Y}/10

## 4. 综合判断
- 双重评分: {X+Y}/20
- 决策: 🟢/🟡/🔴
- 操作建议: ...
- 关键风险: ...
- 后续观察点: ...
```

---

## 四、决策矩阵

| Serenity 评分 | a-stock-data 评分 | 决策 |
|:---:|:---:|:---:|
| 8-10 | 8-10 | 🟢 **强烈买入**（双满分）|
| 8-10 | 5-7 | 🟡 **谨慎买入**（等数据改善）|
| 8-10 | 0-4 | 🟡 **观望**（题材好但价格贵）|
| 5-7 | 8-10 | 🟡 **观察**（数据好但逻辑不硬）|
| 5-7 | 5-7 | 🟡 **中性**（不参与）|
| 5-7 | 0-4 | 🔴 **卖出**（逻辑不硬 + 价格贵）|
| 0-4 | 8-10 | 🔴 **规避**（伪热点）|
| 0-4 | 5-7 | 🔴 **卖出**（无逻辑）|
| 0-4 | 0-4 | 🔴 **立即卖出**（双否定）|

---

## 五、典型场景的双引擎协作

### 场景 1："159941 现在能买吗？"

| 步骤 | Serenity 输出 | a-stock-data 输出 |
|---|---|---|
| 标的识别 | — | ETF，跟踪 NDX100 |
| 视角 1 | 159941 = 间接投资 NDX | 现价 1.585，昨收 1.632 |
| 视角 2 | 长期投资 OK（NDX 长期向上）| 跌 -2.88% 今日 |
| 综合 | 🟡 长期持有 OK，**但已过夜风险高**| 价格 1.585，PE 不可用（ETF）|

**结论**：🟡 **长期可持有，但不要追高，逢回调分批买。**

### 场景 2："用 Serenity 的方式看 半导体"

| 步骤 | Serenity 输出 | a-stock-data 输出 |
|---|---|---|
| 标的识别 | — | 板块识别 + 成分股列表 |
| 视角 1 | 叙事: AI 算力 / 结构: 卡点强 / 5 问=5/5 | 板块当日 +3.5%，北向净流入 8 亿 |
| 视角 2 | 5 问全 YES = 真卡点 | 龙头 PE 45-65x（偏贵）|
| 综合 | 🟢 板块强卡点 + 🟡 估值偏贵 | **等回调 15% 再买** |

**结论**：🟡 **板块强逻辑，但价格偏贵，等回调。**

### 场景 3："688017（绿的谐波）能不能买？"

| 步骤 | Serenity 输出 | a-stock-data 输出 |
|---|---|---|
| 标的识别 | — | 科创板，谐波减速器龙头 |
| 视角 1 | 卡点: 5 问 = 4/5 (人形机器人核心零部件) | PE 88x, PB 8.5x, 一致预期 EPS 增速 35% |
| 视角 2 | 护城河: 强（技术 + 客户认证）| PEG = 88/35 = 2.5（偏贵）|
| 综合 | 🟢 卡点 + 🟡 PEG 偏贵 | **值得长期持有，但短期等回调** |

**结论**：🟡 **长期持有 OK，PE 消化需要 2-3 年，短期追高风险大。**

---

## 六、避免双重分析的"双重失误"

| 失误类型 | 表现 | 解决 |
|---|---|---|
| **过度自信** | 两个引擎都给高分就重仓 | 永远单仓不超 10% |
| **数据陷阱** | a-stock-data 数据看起来好就买 | 必须有 Serenity 逻辑支撑 |
| **逻辑陷阱** | Serenity 卡点强就无脑买 | 必须有数据验证（PE/资金流）|
| **时间错配** | Serenity 是 3 年视角，a-stock-data 是 1 天视角 | 区分投资周期 |

---

## 七、引擎选择的"3 选 1"规则

**简单情况下只用一个引擎**：

| 情况 | 用哪个 | 例子 |
|---|---|---|
| 只想看价格 | a-stock-data | "159941 现价多少" |
| 只想看逻辑 | Serenity | "半导体卡点在哪" |
| 决策性问题 | 双引擎 | "688017 能不能买" |
| 操作性问题 | a-stock-data | "159941 怎么止损" |
| 研究性问题 | Serenity | "人形机器人产业链" |
| 验证性问题 | 双引擎 | "我之前判断对吗" |

---

## 八、自动化调度（推荐实现）

**伪代码**（未来可封装为脚本）：

```python
def dual_analyze(query: str) -> dict:
    """双引擎调度"""
    # 1. 解析意图
    intent = classify_intent(query)  # "估值" / "卡点" / "综合" / ...
    code = extract_stock_code(query)
    
    # 2. 决定引擎权重
    if intent == "综合分析":
        serenity_w = 0.5
        data_w = 0.5
    elif intent == "卡点":
        serenity_w = 0.8
        data_w = 0.2
    elif intent == "估值":
        serenity_w = 0.2
        data_w = 0.8
    # ... 其他意图
    
    # 3. 调度 Serenity
    serenity_result = run_serenity_skill(
        code=code,
        moat_5_questions=True,
        valuation_anchor="30x",
    )
    
    # 4. 调度 a-stock-data
    data_result = run_a_stock_data(
        code=code,
        layers=["quote", "report", "news", "money_flow"],
    )
    
    # 5. 综合判断
    final_score = (
        serenity_result["score"] * serenity_w +
        data_result["score"] * data_w
    )
    
    # 6. 生成报告
    return format_report(
        serenity_result, data_result, final_score, intent
    )
```

---

## 九、当前已激活的双引擎

| 引擎 | 版本 | 技能文件 | 状态 |
|---|---|---|---|
| **a-stock-data** | V3.2.2 | `~/.claude/skills/a-stock-data/SKILL.md` | ✅ |
| **Serenity** | 1.0.0 | `~/.claude/skills/serenity-skill/SKILL.md` | ✅ |
| **akshare** | latest | `~/.claude/skills/akshare/SKILL.md` | ✅ |
| **backtest-expert** | latest | `~/.claude/skills/backtest-expert/SKILL.md` | ✅ |
| **us-market-bubble-detector** | v2.1 | `~/.claude/skills/us-market-bubble-detector/SKILL.md` | ✅ |
| **china-macro-analyst** | latest | `~/.claude/skills/china-macro-analyst/SKILL.md` | ✅ |
| **market-news-analyst** | latest | `~/.claude/skills/market-news-analyst/SKILL.md` | ✅ |
| **a-share-analysis** | latest | `~/.claude/skills/a-share-analysis/SKILL.md` | ✅ |
| **portfolio-manager** | latest | `~/.claude/skills/portfolio-manager/SKILL.md` | ✅ |
| **serenity-method** | latest | `~/.claude/skills/serenity-method/SKILL.md` | ✅ |
| **serenity-radar** | latest | `~/.claude/skills/serenity-radar/SKILL.md` | ✅ |
| **follow-aleabito** | latest | `~/.claude/skills/follow-aleabito/SKILL.md` | ✅ |

---

## 十、双引擎的"边界条件"

| 边界 | 处理方式 |
|---|---|
| **数据接口失败** | 回退到 Serenity 推理（不依赖数据）|
| **Serenity 无明确卡点** | 用 a-stock-data 估值给意见 |
| **新上市标的** | Serenity 主导（数据不足）|
| **退市 / 停牌** | a-stock-data 主导（看公告）|
| **小盘妖股** | a-stock-data 主导 + 高风险警告 |
| **宽基 ETF** | a-stock-data 主导（Serenity 不适用）|
| **跨境标的**（港股/美股）| 双引擎（数据部分用对应 API）|

---

## 十一、一句话总结

> **a-stock-data 告诉你"是什么"，Serenity 告诉你"为什么"，两者交叉验证 = 决策。**

---

## 附录：快速调用样例

### 调用 1：估值查询（a-stock-data 主导）
> 用户："688017 PE 多少"
→ 调度：`tencent_quote()` + `ths_eps_forecast()`
→ 输出：PE 88x, 一致预期 2.15 元

### 调用 2：卡点分析（Serenity 主导）
> 用户："半导体设备卡点在哪"
→ 调度：`serenity-method` + `china-macro-analyst`
→ 输出：5 问评估表 + 投资逻辑

### 调用 3：综合判断（双引擎）
> 用户："159941 能不能长期持有"
→ 调度：a-stock-data（历史走势）+ Serenity（ETF 框架 + 美股宏观）
→ 输出：双重评分 + 操作建议

### 调用 4：风险预警（双引擎）
> 用户："美股有泡沫吗"
→ 调度：`us-market-bubble-detector` + `risk-metrics-calculation` + `market-news-analyst`
→ 输出：泡沫指数 + 历史分位 + 风险等级
