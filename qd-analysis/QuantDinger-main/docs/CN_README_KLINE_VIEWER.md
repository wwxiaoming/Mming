# 量化系统 · 多市场 K 线查看器

一个独立运行的多市场 K 线查看器,作为 QuantDinger 的辅助前端,部署在 `http://<host>:8000/`。

## 功能

| Tab | 说明 | 支持市场 |
|---|---|---|
| 📊 K 线 | 3 Panel 联动 K 线图 (K线+MA / 成交量 / MACD),时间周期 1D/1W/1M | **A 股 / 港股 / 美股 / 加密货币 / 外汇 / 期货** |
| 💰 资金流向 | 日度资金流向明细 + 柱状图 + 趋势线 (主力/特大/大/中/小) | **仅 A 股** |
| 🎯 买卖点回测 | 基于「主力 N 日均线 > 0 看多」规则回测,K线叠加买卖点 | **仅 A 股** |
| ⭐ 自选股 | 多市场股票搜索 + 添加/移除,跨市场跳转 | **A 股 / 港股 / 美股 / 加密货币 / 外汇 / 期货** |

> 资金流向和买卖点回测**仅 A 股**支持,因为这些数据由东方财富(国内)提供,其他市场无对应数据源。

## 部署(在 QuantDinger 主项目目录)

### 1. 拉取代码

```bash
# 假设 QuantDinger 已部署在 /workspace/QuantDinger
cd /workspace/QuantDinger
```

### 2. 配置环境变量

编辑 `backend.env`:

```bash
# K 线查看器开关
KLINE_VIEWER_ENABLED=true
KLINE_VIEWER_PORT=8000
KLINE_VIEWER_URL=http://localhost:8000
KLINE_VIEWER_TITLE=量化系统 · K 线多市场

# 自定义 dashboard 顶部 banner(可空)
KLINE_VIEWER_BANNER_HTML=

# 推荐:启用所有市场(含 A 股)
ENABLED_MARKETS=Crypto,USStock,CNStock,HKStock,Forex,Futures,MOEX
```

### 3. 启动

```bash
docker compose -f docker-compose.ghcr.yml up -d
```

会看到 5 个服务启动:
- `quantdinger-db` (PostgreSQL)
- `quantdinger-redis` (Redis)
- `quantdinger-backend` (Flask)
- `quantdinger-frontend` (Vue + nginx)
- **`quantdinger-kline-viewer`** (Python http.server, 端口 8000) ⭐

### 4. 访问

打开浏览器:

```
http://localhost:8000/
```

端口转发(iPad + Codespaces 用户):
- 在 Codespace 的 **PORTS** 面板找到 8000
- 鼠标悬停 → 点地球图标 🌐 → 在新标签页打开

## 使用流程

1. **选择市场**:顶部下拉框切到「🇨🇳 A 股」/「🇭🇰 港股」/「🇺🇸 美股」/「₿ 加密货币」/「💱 外汇」/「📊 期货」
2. **搜索标的**:输入代码(600519 / AAPL / BTCUSDT)或名称(茅台 / Apple / Bitcoin)
3. **加载 K 线**:点击搜索结果,自动跳到 K 线 Tab
4. **切换周期**:1D / 1W / 1M 按钮
5. **加自选**:K 线 Tab 右上「+ 加自选」按钮
6. **跑回测**(仅 A 股):切到「买卖点回测」Tab,设置 N (默认 5),点「跑回测」
7. **看资金流**(仅 A 股):切到「资金流向」Tab

## 架构

```
┌──────────────────┐
│ 浏览器 (iPad)    │
└────────┬─────────┘
         │
   ┌─────┴─────┐
   ▼           ▼
8888         8000
QuantDinger   K 线查看器
(私有 Vue)    (本次新增)
   │           │
   └─────┬─────┘
         ▼
   5000
   QuantDinger 后端 (Flask)
   │
   ├── Postgres (5432)
   └── Redis (6379)
```

K 线查看器通过 `kline_viewer_proxy.py` 把 `/api/*` 反向代理到后端 5000 端口(同集群内 `http://backend:5000`)。

## 文件清单

| 文件 | 说明 |
|---|---|
| `kline_viewer_proxy.py` | 8000 端口服务器 + CORS 代理 |
| `backend_api_python/app/static/kline_viewer/index.html` | K 线查看器 SPA |
| `backend_api_python/app/routes/market_cn_moneyflow.py` | A 股资金流向 API |
| `backend_api_python/app/openapi/register.py` | 注册新蓝图 |
| `backend_api_python/app/routes/settings.py` | brand-config 暴露 kline_viewer 字段 |
| `backend_api_python/env.example` | 新增 KLINE_VIEWER_* 配置项 |
| `docker-compose.yml` + `docker-compose.ghcr.yml` | 新增 kline-viewer 服务 |

## API 端点

### 复用 QuantDinger 现有 API

| 端点 | 用途 |
|---|---|
| `GET /api/kline?market=...&symbol=...&timeframe=...&limit=...` | K 线数据 |
| `GET /api/market/symbols/search?market=...&keyword=...` | 标的搜索 |
| `GET /api/market/price?market=...&symbol=...` | 实时价 |
| `GET /api/market/watchlist/get` | 自选股列表 |
| `POST /api/market/watchlist/add` | 添加自选 |
| `POST /api/market/watchlist/remove` | 移除自选 |
| `GET /api/settings/brand-config` | 品牌配置(含 kline_viewer URL) |

### 本次新增

| 端点 | 用途 |
|---|---|
| `GET /api/market/cn-moneyflow?symbol=...&days=...` | A 股日度资金流向 |

## 故障排查

### 1. 端口 8000 访问不到

```bash
# 看 kline-viewer 容器状态
docker ps | grep kline-viewer

# 看日志
docker logs quantdinger-kline-viewer

# 健康检查
curl -sf http://127.0.0.1:8000/
# 应该返回 HTML
```

### 2. /api/* 返回 502

说明 proxy 无法连到后端。检查 `BACKEND_URL` 环境变量:

```bash
docker exec quantdinger-kline-viewer env | grep BACKEND_URL
# 应该是 http://backend:5000
```

如果是 Codespaces 开发模式(不在 docker 网络内),改成 `http://127.0.0.1:5000` 重启:

```bash
# 停止容器
docker compose -f docker-compose.ghcr.yml stop kline-viewer

# 用环境变量覆盖启动
BACKEND_URL=http://127.0.0.1:5000 python3 kline_viewer_proxy.py
```

### 3. A 股资金流加载失败

```bash
# 看后端日志
docker logs quantdinger-backend --tail 50

# 可能原因:akshare 未安装
docker exec quantdinger-backend pip install akshare -q
docker compose -f docker-compose.ghcr.yml restart backend
```

### 4. 搜索 A 股无结果

检查后端是否启用了 A 股:

```bash
docker exec quantdinger-backend env | grep -E "ENABLED_MARKETS|SHOW_CN_STOCK"
# 应包含 CNStock
```

如果没设,改 `backend.env` 加:
```bash
ENABLED_MARKETS=Crypto,USStock,CNStock,HKStock,Forex,Futures,MOEX
```

重启后端:
```bash
docker compose -f docker-compose.ghcr.yml restart backend
```

## 开发模式(Codespaces)

不用 Docker,直接 Python 起服务:

```bash
# 终端 1:启动后端(假设已经 docker 跑着后端,只要 5000 端口可达)
# 或者本地起:
cd backend_api_python && python3 run.py

# 终端 2:启动 K 线查看器
cd /workspace/QuantDinger
BACKEND_URL=http://127.0.0.1:5000 PORT=8000 python3 kline_viewer_proxy.py
```

打开 `http://localhost:8000/` 即可。

## 限制

1. **Vue 前端私有**:QuantDinger 的 Vue 前端在私有仓库,无法直接修改,因此无法在 QuantDinger 主界面加链接入口。
   - 替代方案:浏览器直接书签 `http://<host>:8000/`
   - 备选方案:品牌配置已暴露 `kline_viewer` 字段,若将来 QuantDinger 读取它则自动显示

2. **资金流向仅 A 股**:其他市场数据源(美股/港股/加密)不提供资金流明细。如需类似功能,可对接 IBKR、CCXT 等。

3. **回测模型简单**:当前只支持「主力 N 日均线 > 0」单规则,无手续费/滑点/仓位管理。后续可扩展。
