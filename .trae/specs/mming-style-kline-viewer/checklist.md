# Checklist — Mming 风格 K 线查看器

按以下检查点逐项验证，全部 ✅ 才算完成。

## 数据 & 渲染

- [ ] `qd-kline.html` URL 接受 `market`, `symbol`, `tf`, `limit` 四个参数
- [ ] `qd-kline.html` 通过 `/qd-api/*` 代理成功调用 QuantDinger `/api/kline`
- [ ] 字段映射正确：`time → date`, `open/close/high/low/volume → [o,c,l,h,v]`
- [ ] 4 个 panel 全部渲染：K线（含 MA5/MA10/MA20）、成交量、MACD、主力净流入
- [ ] `dataZoom.xAxisIndex: [0,1,2,3]` 4 个 panel 联动缩放
- [ ] `axisPointer.link: {xAxisIndex: 'all'}` 4 panel 鼠标十字线联动
- [ ] `animation: false`，缩放丝滑不卡顿
- [ ] 配色：背景 `#0d1117`、红 `#ef4444`、绿 `#10b981`、MA `#fbbf24/#60a5fa/#a78bfa`

## 中文本地化

- [ ] tooltip 显示「时间 / 开盘 / 收盘 / 最高 / 最低 / 成交量 / 涨跌幅 / MA5 / MA10 / MA20 / DIF / DEA / MACD / 主力净流入」全部中文
- [ ] 没有残留的 `Open / High / Low / Close / Volume` 英文标签
- [ ] 周期按钮显示「1分 / 5分 / 15分 / 30分 / 1时 / 4时 / 1日 / 1周」
- [ ] 错误条中文：「加载 K 线失败: ...，请确认 QuantDinger 已启动 (端口 5000)」

## 集成入口

- [ ] `index.html` 资金流向 tab K 线区域顶部有新按钮「🎨 Mming 风格 (QD数据)」
- [ ] 按钮在用户已成功查询一次数据后才显示（避免空 URL 跳转）
- [ ] 点击后新窗口打开 `qd-kline.html?market=CNStock&symbol=shXXXXXX&tf=1D&limit=180`
- [ ] 输入代码 `600519` 自动补 `sh` 前缀
- [ ] 输入代码 `000001` / `300750` 自动补 `sz` 前缀
- [ ] 输入代码 `430047` 自动补 `bj` 前缀（北交所）

## 代理

- [ ] `server.py` 新增 `/qd-api/*` 转发到 `QD_API_BASE + path.replace('/qd-api', '/api')`
- [ ] 502 时返回 JSON `{"error":"QuantDinger backend not reachable on port 5000"}`
- [ ] 原 `/api/*`（jzhu-quant 8180）行为不变
- [ ] `QD_API_BASE` 从环境变量读取，默认 `http://localhost:5000`

## 健壮性

- [ ] K 线 0 根（空数组）时显示「暂无数据」占位，不崩
- [ ] `market=USStock&symbol=TSLA` 美股也正常工作（红涨绿跌）
- [ ] 周期切换 1D ↔ 1W ↔ 1m 重渲染正常
- [ ] 拉取超时 15s 后自动 abort 并显示错误
- [ ] 重试按钮不重复触发（防抖 1s）
- [ ] iPad Safari 横屏 / 竖屏 4 panel 比例正常

## 文件清单（完成后应有）

- [ ] `/workspace/jzhu-quant/qd-kline.html` 新文件
- [ ] `/workspace/jzhu-quant/qd-kline.js` 新文件
- [ ] `/workspace/jzhu-quant/mock-qd-server.py` 新文件（仅本地验证用）
- [ ] `/workspace/jzhu-quant/server.py` 修改（+QD 代理）
- [ ] `/workspace/jzhu-quant/index.html` 修改（+1 按钮 +1 监听 +1 前缀函数）
- [ ] `/workspace/jzhu-quant/start-all.sh` 可选修改（QD 同时启动）
- [ ] `/workspace/.trae/specs/mming-style-kline-viewer/spec.md` 已存在
- [ ] `/workspace/.trae/specs/mming-style-kline-viewer/tasks.md` 已存在
- [ ] `/workspace/.trae/specs/mming-style-kline-viewer/checklist.md` 本文件
