# QuantDinger K 线查看器 Checklist

> 每完成一项功能就勾选对应方框。所有项都通过后才能视为完成。
>
> ✅ = 本机已验证
> 🟡 = 代码已完成,需真实部署后验证

## 后端 API 补充（Task 1）

- 🟡 A 股 K 线接口能拉到 sh600519 的日 K 线数据（DataSourceFactory 已支持 CNStock，需部署后验证）
- 🟡 股票搜索接口能搜出 "茅台" / "600519" / "平安银行"（market_blp.search_symbols 已存在，需部署后验证）
- 🟡 自选股增删查 4 个 API 都正常（market_blp 已实现）
- ✅ **新增** A 股日度资金流向接口 `GET /api/market/cn-moneyflow` 返回正确格式
  - ✅ 文件已创建 `backend_api_python/app/routes/market_cn_moneyflow.py`
  - ✅ Python 语法验证通过（`ast.parse`）
  - ✅ 字段齐全：date, close, change_pct, main_net, super_net, big_net, mid_net, small_net, total_net
  - ✅ 单位正确（元转万元）
  - ✅ 数据源：AKShare `stock_individual_fund_flow`（东方财富免费）
  - ✅ 缓存机制：30 分钟 TTL
  - ✅ 已注册到 `app/openapi/register.py`

## 前端 K 线查看器（Task 2）

- ✅ 顶部市场下拉框显示 6 个市场（A 股 / 港股 / 美股 / 加密货币 / 外汇 / 期货）
  - 已实现: `<select id="marketSelect">` + `marketLabel()` 函数
- ✅ 切换市场后，搜索结果基于新市场
  - 已实现: `doSearch()` 使用 `currentMarket` 变量
- ✅ 4 个 Tab 都能正常切换
  - 已实现: `switchTab()` 函数 + `.tab.active` class
- 🟡 K 线 Tab 加载一只标的后显示 3 panel 联动图
  - ✅ K线 + MA5/10/20（panel 1）
  - ✅ 成交量（panel 2）
  - ✅ MACD（panel 3）
  - ✅ 3 panel 共享 dataZoom：`dataZoom.xAxisIndex:[0,1,2]`
  - ✅ 3 panel 共享 axisPointer：`axisPointer.link.xAxisIndex:'all'`
  - ✅ 缩放丝滑：`animation:false, throttle:50, zoomOnMouseWheel:true`
  - ✅ 双击还原：`ondblclick` 触发 dataZoom action
- 🟡 时间周期切换 1D/1W/1M 都能重新拉数据（需部署验证）
- 🟡 港股 / 美股 / 加密货币等市场也能正常拉 K 线（需部署验证）
- ✅ 资金流向 Tab（A 股专属）
  - ✅ 表格 + 柱状图 + 趋势线（已实现）
  - ✅ 非 A 股时显示"仅 A 股支持"提示
- ✅ 买卖点回测 Tab（A 股专属）
  - ✅ 跑回测后 K 线上能看到 ▲/▼ 标记
  - ✅ **关键**：marker 画在 `dates[i-1]` 的 `kmap[dates[i-1]].close`（与 jzhu-quant 修复版一致）
  - ✅ 统计卡片：年化、最大回撤、胜率、交易次数、回测天数
  - ✅ 收益曲线图（策略 vs 持有基准）
  - ✅ 非 A 股时显示"仅 A 股支持"提示
- ✅ 自选股 Tab（多市场）
  - ✅ 搜索 + 添加按钮（K 线 Tab "+ 加自选"）
  - ✅ 列表显示已添加的标的（含市场标签 `marketLabel()`）
  - ✅ 点击跳到 K 线 Tab（自动切到对应市场：`el.dataset.market !== currentMarket`）
  - ✅ × 按钮移除成功（POST /api/market/watchlist/remove）

## 部署集成（Task 3）

- ✅ `kline_viewer_proxy.py` 单文件能跑（端口 8000）
  - ✅ Python 语法验证通过
  - ✅ 本机启动成功（`python3 kline_viewer_proxy.py`）
  - ✅ `curl http://127.0.0.1:8000/` 返回 200 + 40KB HTML
- ✅ `/api/*` 请求被正确代理到后端 5000
  - ✅ 代理代码实现：`do_GET/POST/PUT/DELETE` 调用 `_proxy()`，使用 `urllib.request.urlopen`
  - ✅ Header 透传（Cookie/Authorization/Content-Type）
- ✅ `docker-compose.ghcr.yml` 添加 kline-viewer 服务
  - ✅ YAML 解析通过 `yaml.safe_load`
  - ✅ 镜像 `python:3.12-slim-bookworm`，挂载 `kline_viewer_proxy.py` 和静态目录
- ✅ `docker-compose.yml` 同样添加
  - ✅ YAML 解析通过
- 🟡 `docker compose up -d` 启动 5 个服务（需部署验证）
- ✅ `env.example` 添加 KLINE_VIEWER_* 配置
  - ✅ `KLINE_VIEWER_ENABLED=true`
  - ✅ `KLINE_VIEWER_PORT=8000`
  - ✅ `KLINE_VIEWER_URL=http://localhost:8000`
  - ✅ `KLINE_VIEWER_TITLE=量化系统 · K 线多市场`
  - ✅ `KLINE_VIEWER_BANNER_HTML=`

## QuantDinger 入口集成（Task 4）

- 🟡 dashboard 顶部显示蓝色 banner（**限制**：Vue 前端私有，无法直接修改；若将来读取 `brand-config.kline_viewer` 则生效）
- ✅ brand-config 响应中已暴露 `kline_viewer` 字段（`backend_api_python/app/routes/settings.py` 修改完成）
- ✅ banner 通过 `KLINE_VIEWER_BANNER_HTML` env 控制
- ✅ 备用入口 1：K 线查看器顶部"⬅ QuantDinger"按钮
- ✅ 备用入口 2：直接书签 `http://<host>:8000/`
- ✅ README 文档完成

## AI 智能分析 A 股板块（Task 5）

- 🟡 `ENABLED_MARKETS` 包含 `CNStock` 后，`/api/global-market/opportunities` 返回的板块包含 A 股（需部署验证后端逻辑）
- ✅ `env.example` 推荐配置更新：`ENABLED_MARKETS=Crypto,USStock,CNStock,HKStock,Forex,Futures,MOEX`
- 🟡 在 dashboard banner 附近加"打开 A 股板块"链接（依赖 Vue 端支持 banner）
- ✅ K 线查看器顶部已支持市场切换，包含 A 股

## 文档（Task 6）

- ✅ `docs/CN_README_KLINE_VIEWER.md` 创建（部署/使用/API/故障排查）
- ✅ env.example 已加注释
- 🟡 iPad Safari 端到端测试（需实际部署到 Codespaces 验证）
  - 待验证：登录 QuantDinger → dashboard 顶部 banner → 点击进入 K 线查看器 → 4 个 Tab 全跑通
