# Checklist

## K 线 Tooltip 中文化
- [x] candlestick tooltip 显示「开盘/收盘/最低/最高」中文
- [x] tooltip 同时显示「涨跌额」「涨跌幅」「成交量」
- [x] 涨跌幅用前一根 K 线的 close 作基准，避免首日无数据（首日取自身不显示涨跌色）

## 实时行情卡
- [x] 资金流查询成功后自动拉取腾讯行情（`loadQuoteAndSectors()` 在 `query()` 末尾调用）
- [x] 行情卡字段齐全：当前价 / 涨跌幅 / 涨跌额 / 换手率 / 量比 / PE(TTM) / PB / 总市值 / 流通市值 / 涨停价 / 跌停价
- [x] 行情卡位置在「统计卡」之后、「K 线卡」之前（插入在 `#stats` 和 `#klineArea` 之间）
- [x] 腾讯 API 失败时显示「⚠️ 暂未获取到实时行情」降级提示
- [x] 行情卡配色：正（涨）蓝 `#58a6ff`、负（跌）橙 `#fdba74`、中性白
- [x] 不引入新依赖，纯原生 fetch + ECharts

## 所属板块卡
- [x] 行情卡加载完成后自动调东财 slist
- [x] 板块标签以 chip 形式展示（`renderSectors()` 用 inline 圆角 span）
- [x] 东财失败时显示「⚠️ 暂未获取到板块信息」降级提示
- [x] 板块 chip 用深色背景 + 浅色文字

## 涨跌停标记线
- [x] K 线 panel 顶部画涨停价虚线（橙红 #fd7e35）
- [x] K 线 panel 顶部画跌停价虚线（灰 #6e7681）
- [x] 标记线作为 K 线 series 的 `markLine.data`，缩放/平移自动跟随
- [x] 数据缺失时不画标记线（`markLines.length` 为 0 时不传 `markLine`）

## 换手率副轴
- [x] 成交量 panel 增加右侧 yAxis（`yAxisIndex: 2`）
- [x] 副轴 label 格式化为百分比（`formatter: '{value}%'`）
- [x] 副轴折线颜色用紫 `#c678dd`，与主轴区分
- [x] 数据缺失时不渲染副轴（`show: turnoverArr.some(v => v != null)`）

## 状态管理
- [x] `clearResults()` 时清空 `currentQuote` 和行情/板块卡
- [x] 改股票代码/日期时同步重置（change 事件 + clearResults 双重保险）
- [x] 标签页切换不会丢失已加载的行情（数据存在全局 `currentQuote`，切 tab 不重置）

## 数据源策略
- [x] 行情数据走腾讯（`https://qt.gtimg.cn/q=sh600519`，不封 IP）
- [x] 板块数据走东财 slist（`https://push2.eastmoney.com/api/qt/slist/get?spt=3`）
- [x] K 线/资金流继续走本地 8180 端口（项目既定的 `/api/plugin/kline` + `/api/plugin/moneyflow`）
- [x] 不引入 mootdx / akshare 等额外依赖

## 验证
- [x] JS 语法 `new Function()` 解析通过（无错误）
- [x] HTTP 服务 200 OK
- [x] 浏览器肉眼检查：tooltip 中文 ✅ / 行情卡数据正常 ✅ / 板块 chip 正常 ✅
- [x] 模拟断网：降级提示正常显示（renderQuote(null) / renderSectors(null)）
- [x] 不影响「择时回测」和「图表」tab 的现有功能（K 线买卖点修复、backtest 不动）
- [x] zip 更新到 `/workspace/jzhu-trading.zip`（35 文件，173KB）
