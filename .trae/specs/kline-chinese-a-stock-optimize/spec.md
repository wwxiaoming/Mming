# K 线中文化 + a-stock-data 优化 Spec

## Why
当前 K 线的 tooltip 显示的是 ECharts 默认英文（open/close/low/high），不符合中文用户阅读习惯。同时 `jzhu-quant` 项目目前只调用了本地 `8180` 端口的 `moneyflow` + `kline` 接口，缺少实时行情（涨跌停价、换手率、PE/PB）、行业板块归属等核心数据。本 spec 一次性解决：
1. K 线 tooltip 中文化
2. 按 `a-stock-data` skill 给页面补上 A 股核心数据维度

## What Changes
- **K 线 tooltip 中文化**：`open/close/low/high` → `开盘/收盘/最低/最高`，并加上 `涨跌额/涨跌幅/成交量`
- **新增「实时行情」卡片**：用腾讯财经 API 拉 `价格/PE/PB/市值/换手率/涨跌停价/量比`（不封 IP）
- **新增「所属板块」标签**：用东财 `slist` API 拉 `行业/概念/地域` 标签（沿用 V3.2.2 slist 替换方案）
- **K 线加涨跌停标记**：从腾讯接口拿 `limit_up/limit_down` 后，在 K 线最高/最低附近画虚线
- **K 线加换手率副轴**：用腾讯接口的 `turnover_pct` 在成交量 panel 旁加副轴
- **加载逻辑改造**：先查 `moneyflow` → 自动调腾讯拿实时行情 → 用户点"加载 K 线"时再调 `kline` 接口

## Impact
- Affected specs: 无（新增能力）
- Affected code:
  - `/workspace/jzhu-quant/index.html`（全部单文件实现）
  - 不引入新依赖（CDN 已加载 ECharts，腾讯/东财 HTTP API 零依赖）
- 数据源策略：按 a-stock-data V3.2.2 原则
  - 行情（实时价/PE/PB/涨跌停）→ **腾讯财经**（不封 IP）
  - 板块归属 → **东财 slist**（spt=3，一次拿全）
  - K 线/资金流 → **继续走本地 8180**（项目既定的接口）

## ADDED Requirements

### Requirement: K 线 Tooltip 中文化
`index.html` 中所有 candlestick 的 tooltip SHALL 用中文标签显示 OHLC + 涨跌额 + 涨跌幅 + 成交量。

#### Scenario: 用户悬停 K 线某一天
- **WHEN** 鼠标停在 candlestick 某根 K 线上
- **THEN** tooltip 显示：`开盘 X.XX / 收盘 X.XX / 最低 X.XX / 最高 X.XX / 涨跌额 +X.XX / 涨跌幅 +X.XX% / 成交量 XXXX`

#### Scenario: 用户查看 K 线任意一天
- **WHEN** tooltip 触发
- **THEN** 涨跌幅 = (close - prevClose) / prevClose × 100%（取前一根 K 线的 close 作基准）

### Requirement: 实时行情卡
页面 SHALL 在「资金流向」tab 的统计卡行下方增加一张「实时行情」卡，数据来自腾讯财经 API（`https://qt.gtimg.cn/q=sh600519`）。

#### Scenario: 资金流查询成功后
- **WHEN** `query()` 成功获取资金流数据
- **THEN** 自动调腾讯 API 拉 `实时价/PE/PB/总市值/换手率/涨跌停价/量比` 渲染到行情卡
- **THEN** 行情卡显示在「交易日区间 / 累计主力净流入」统计卡**之后**、「K 线卡」**之前**

#### Scenario: 腾讯 API 失败
- **WHEN** 腾讯接口超时或返回非预期格式
- **THEN** 行情卡显示「暂未获取到实时行情」灰色提示，不影响其他功能

### Requirement: 所属板块标签
页面 SHALL 在行情卡下方显示一个标签列表，列出该股所属的全部板块（行业/概念/地域混合），用东财 `slist` 接口（`https://push2.eastmoney.com/api/qt/slist/get?spt=3`）。

#### Scenario: 行情卡加载完成后
- **WHEN** 实时行情获取成功
- **THEN** 自动调东财 slist 拉板块归属
- **THEN** 渲染为深色 chip 标签列表（如「食品饮料 / 白酒 / 贵州板块 / HS300_」）

#### Scenario: 东财被封或超时
- **WHEN** slist 请求失败
- **THEN** 板块区显示「暂未获取到板块信息」灰字，不抛错

### Requirement: 涨跌停标记
K 线图 SHALL 在 K 线 panel 顶部画两条水平虚线，分别标记 `limit_up`（涨停价）和 `limit_down`（跌停价）。

#### Scenario: 用户查看 K 线
- **WHEN** 实时行情拉取到 `limit_up` / `limit_down` 字段
- **THEN** K 线 panel 增加两条 `markLine`：橙红虚线 = 涨停，灰虚线 = 跌停
- **THEN** 标记线缩放/平移时跟随联动

#### Scenario: 没有涨跌停价数据
- **WHEN** 实时行情未拉取到
- **THEN** 不绘制涨跌停线（不是必填）

### Requirement: 换手率副轴
K 线图的成交量 panel SHALL 增加一个右侧 Y 轴，显示每日换手率（`turnover_pct`）。

#### Scenario: 实时行情拉取到换手率
- **WHEN** 加载 K 线时
- **THEN** 成交量 panel 右侧副轴显示换手率（百分比）
- **THEN** 副轴折线跟随主 K 线 X 轴联动

## MODIFIED Requirements

### Requirement: K 线加载流程
原流程：用户必须点「加载 K 线」按钮才能看到 K 线。
新流程：用户在资金流 tab 查询成功后，**自动**拉取实时行情 + 板块，**K 线**仍保持懒加载（按需点按钮）。

#### Scenario: 资金流查询成功
- **WHEN** `query()` 完成
- **THEN** 1) 渲染统计卡；2) 自动请求腾讯实时行情 → 渲染行情卡；3) 自动请求东财 slist → 渲染板块；4) 加载 K 线按钮变为可点
- **THEN** K 线本身**不**自动加载（避免一上来就请求大段 K 线数据，按用户意愿触发）

## REMOVED Requirements

无。
