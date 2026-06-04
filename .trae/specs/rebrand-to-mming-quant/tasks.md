# Tasks

- [ ] Task 1: 重写 /workspace/index.html 为 Mming 量化版本
  - [ ] SubTask 1.1: 删除整个 `.xy-ad` 推广 banner 区块(包含小宇量化品牌、jzhu.net 链接、微信二维码)
  - [ ] SubTask 1.2: 修改 `<title>` 为"Mming 量化 · 资金流向查询器"
  - [ ] SubTask 1.3: 修改页头(`.subtitle` 或新加一行)展示品牌名"Mming 量化",并说明数据来源为"量化系统(本地 8180 端口)"
  - [ ] SubTask 1.4: 修改页脚,移除"小宇量化"指代,保留"数据来自本地行情服务"的描述
  - [ ] SubTask 1.5: 把第 1363 行的 kline fetch URL `http://localhost:8180/api/plugin/kline` 改为 `/api/plugin/kline`
  - [ ] SubTask 1.6: 把第 1471 行的 moneyflow fetch URL `http://localhost:8180/api/plugin/moneyflow` 改为 `/api/plugin/moneyflow`
  - [ ] SubTask 1.7: 全文件搜索确认无残留"小宇量化"字样、`XYLH8338`、`jzhu.net`(允许出现在注释中)

# Task Dependencies
无依赖(单文件操作)
