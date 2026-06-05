# QuantDinger K 线查看器 Checklist

> 每完成一项功能就勾选对应方框。所有项都通过后才能视为完成。

## 后端 API 补充（Task 1）

- [ ] A 股 K 线接口能拉到 sh600519 的日 K 线数据
- [ ] 股票搜索接口能搜出 "茅台" / "600519" / "平安银行"
- [ ] 自选股增删查 4 个 API 都正常
- [ ] **新增** A 股日度资金流向接口 `GET /api/market/cn-moneyflow` 返回正确格式
  - [ ] 字段齐全：date, main_net, super_net, big_net, mid_net, small_net, total_net
  - [ ] 单位正确（万元）
  - [ ] 数据源优先 Tencent，备选 AKShare

## 前端 K 线查看器（Task 2）

- [ ] 4 个 Tab 都能正常切换
- [ ] K 线 Tab 加载一只股票后显示 4 panel 联动图
  - [ ] K线 + MA5/10/20（panel 1）
  - [ ] 成交量（panel 2）
  - [ ] MACD（panel 3）
  - [ ] 主力净流入（panel 4）
  - [ ] 4 panel 共享 dataZoom（拖动主图，下方缩略条 + 其他 panel 同步）
  - [ ] 4 panel 共享 axisPointer（十字光标联动）
  - [ ] 缩放丝滑（throttle 50ms，无卡顿）
  - [ ] 双击还原
- [ ] 时间周期切换 1D/1W/1M 都能重新拉数据
- [ ] 资金流向 Tab 显示表格和饼图
- [ ] 买卖点回测 Tab
  - [ ] 跑回测后 K 线上能看到 ▲/▼ 标记
  - [ ] **关键**：marker 画在信号触发日的前一日 K 线收盘价上（不是当天的 k.low）
  - [ ] 统计卡片：年化、最大回撤、夏普、胜率
  - [ ] 收益曲线图（策略 vs 基准）
- [ ] 自选股 Tab
  - [ ] 搜索 + 添加成功
  - [ ] 列表显示已添加的股票
  - [ ] 点击跳到 K 线 Tab
  - [ ] × 按钮移除成功

## 部署集成（Task 3）

- [ ] `kline_viewer_proxy.py` 单文件能跑（端口 8000）
- [ ] `/api/*` 请求被正确代理到后端 5000
- [ ] `docker-compose.ghcr.yml` 添加 kline-viewer 服务
- [ ] `docker-compose.yml` 同样添加
- [ ] `docker compose up -d` 启动 5 个服务（postgres/redis/backend/frontend/kline-viewer）
- [ ] `env.example` 添加 KLINE_VIEWER_* 配置

## QuantDinger 入口集成（Task 4）

- [ ] dashboard 顶部显示蓝色 banner "🆕 量化系统 · A 股 K 线查看器"
- [ ] 点击 banner 跳到 `/kline-viewer/`
- [ ] banner 通过 env 控制（默认开/关）
- [ ] 在 README 添加使用说明
- [ ] banner 在 iPad Safari 上显示正常（不挡住菜单）

## AI 智能分析 A 股板块（Task 5）

- [ ] `ENABLED_MARKETS` 包含 `CNStock` 后，`/api/global-market/opportunities` 返回的板块包含 A 股
- [ ] `env.example` 推荐配置更新
- [ ] 在 dashboard banner 附近加"打开 A 股板块"链接
- [ ] iPad Safari 上 6 个板块切换能看到 A 股

## 文档（Task 6）

- [ ] `docs/CN_README_KLINE_VIEWER.md` 创建
- [ ] 主 `README.md` 顶部加新功能提示
- [ ] iPad Safari 端到端测试：
  - [ ] 登录 QuantDinger
  - [ ] 看到 dashboard 顶部 banner
  - [ ] 点击进入 K 线查看器
  - [ ] K 线 Tab 加载茅台数据
  - [ ] 切换到资金流向 Tab
  - [ ] 跑回测看买卖点
  - [ ] 添加一只自选股
  - [ ] 跳回 QuantDinger（浏览器后退）
