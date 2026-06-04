# Tasks

- [ ] Task 1: 实现腾讯财经 API 调用函数（real-time quote）
  - [ ] SubTask 1.1: 实现 `tencentQuote(code)` 函数（GBK 解码，字段映射）
  - [ ] SubTask 1.2: 实现 `tencentKlineMA(code, days)` 占位（暂不调用，先留接口）
  - [ ] SubTask 1.3: 实现单股/批量拉取 + UA + timeout

- [ ] Task 2: 实现东财 slist 板块归属函数
  - [ ] SubTask 2.1: 实现 `eastmoneyConceptBlocks(code)`（V3.2.2 替换方案）
  - [ ] SubTask 2.2: 错误处理（无鉴权时返回空数组 + 友好提示）

- [ ] Task 3: K 线 Tooltip 中文化
  - [ ] SubTask 3.1: 修改 `loadKlineChart()` 的 candlestick 配置，加 `tooltip.formatter`
  - [ ] SubTask 3.2: 字段映射：open→开盘, close→收盘, low→最低, high→最高
  - [ ] SubTask 3.3: 加上「涨跌额」「涨跌幅」「成交量」（前一根 close 算基准）

- [ ] Task 4: 新增「实时行情」卡片
  - [ ] SubTask 4.1: HTML 插入 `#quoteArea` 卡片（在统计卡和 K 线卡之间）
  - [ ] SubTask 4.2: `query()` 成功后自动调用 `tencentQuote()` 渲染
  - [ ] SubTask 4.3: 显示字段：当前价 / 涨跌幅 / PE / PB / 总市值 / 换手率 / 涨跌停价 / 量比
  - [ ] SubTask 4.4: 失败时显示「暂未获取到实时行情」

- [ ] Task 5: 新增「所属板块」标签列表
  - [ ] SubTask 5.1: HTML 插入 `#sectorArea` 卡片（在行情卡下方）
  - [ ] SubTask 5.2: `tencentQuote()` 成功后自动调 `eastmoneyConceptBlocks()`
  - [ ] SubTask 5.3: 渲染为 chip 标签列表，hover 显示涨跌幅（可选）
  - [ ] SubTask 5.4: 失败时显示「暂未获取到板块信息」

- [ ] Task 6: K 线加涨跌停标记线
  - [ ] SubTask 6.1: 缓存 `limit_up` / `limit_down` 到全局 `currentQuote`
  - [ ] SubTask 6.2: `loadKlineChart()` 末尾给 K 线 series 加 `markLine`
  - [ ] SubTask 6.3: 橙红虚线 = 涨停，灰虚线 = 跌停
  - [ ] SubTask 6.4: 无涨跌停数据时不画

- [ ] Task 7: K 线加换手率副轴
  - [ ] SubTask 7.1: 用 `tencentKlineMA` 或东财接口的「换手率」数据
  - [ ] SubTask 7.2: 成交量 panel 加右侧 yAxis（百分比格式）
  - [ ] SubTask 7.3: 副轴加 line series 展示换手率折线
  - [ ] SubTask 7.4: 数据缺失时副轴不渲染

- [ ] Task 8: clearResults 与参数变更时清空新数据
  - [ ] SubTask 8.1: `clearResults()` 增加清空 `currentQuote` / 行情卡 / 板块卡
  - [ ] SubTask 8.2: change 事件中同步重置

- [ ] Task 9: 验证
  - [ ] SubTask 9.1: 用 `curl https://qt.gtimg.cn/q=sh600519` 验证腾讯接口（开发机可达性）
  - [ ] SubTask 9.2: 浏览器打开页面，肉眼检查 tooltip 是否中文、卡是否正常
  - [ ] SubTask 9.3: 模拟失败场景（断网时）确认降级提示正常

# Task Dependencies
- Task 3 依赖 Task 1（tooltip 显示的「涨跌额/涨跌幅」需要 K 线数据，本身有）
- Task 4 依赖 Task 1
- Task 5 依赖 Task 1（实时行情拿到后再拉板块）
- Task 6 依赖 Task 4（涨跌停价从实时行情缓存里取）
- Task 7 可独立（也可与 Task 1 合并获取）
- Task 8 依赖 Task 4/5/6/7

# Parallelizable
- Task 1、2、3 可并行（无前置依赖）
- Task 6、7 可并行
- Task 8 必须在 Task 4/5/6/7 之后
