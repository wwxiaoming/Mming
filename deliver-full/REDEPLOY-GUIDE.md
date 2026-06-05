# Mming 量化 — 全新部署教程 (GitHub Codespace / 云服务器)

> 假设你已经删掉旧的 Codespace / 云服务器,从零开始。

## 0. 前置条件

- 一个 GitHub 账号 (Codespace 免费 60h/月)
- Docker (云服务器需要;Codespace 已自带)
- iPad Safari 或桌面浏览器

## 1. 部署方案选择

| 方案 | 适用 | 速度 | 自定义前端 |
|---|---|---|---|
| **A: 一键 install.sh (GHCR 镜像)** | 想最快跑起来 | ⭐ | ❌ 不能改前端 |
| **B: 本地 build (推荐本次)** | 改了前端 (主力净流入 / 搜索 / 暗色) | ⭐⭐ | ✅ 改了就生效 |
| **C: 完全源码 build** | 还要改后端 Python | ⭐⭐⭐ | ✅ 改了前端+后端 |

**本次教程用方案 B** — 改了前端但不动后端。

## 2. 在 GitHub Codespace 创建容器

1. 打开 https://github.com/codespaces
2. 点 "New codespace"
3. 选 "Blank" 模板 (4-core, 8GB RAM 即可)
4. 等 30 秒容器创建完
5. 在浏览器里点 VSCode 顶栏 "Terminal" → "New Terminal"

> ⚠️ 不要选过大的容器 (8-core 16GB),免费的 60h/月会很快用完。

## 3. 把本 zip 上传到 Codespace

**方式 1 (推荐):** 用 Codespace 的文件上传按钮

- VSCode 侧边栏点 "..." → "Upload..." → 选 `mming-qd-full.zip`

**方式 2:** 用 `curl` 拉到容器里 (如果你把 zip 放到了 Gist / 自己的 HTTP server)

```bash
cd ~
curl -o mming-qd-full.zip <你的 zip 下载链接>
```

## 4. 解压并补全源码

```bash
cd ~
unzip -o mming-qd-full.zip -d quantdinger
cd quantdinger
ls -la
```

解压后应该看到:
```
docker-compose.yml
docker-compose.ghcr.yml
docker-compose.build.yml
backend.env          ← 已预配置 A股 + Mming 品牌
backend.env.example
.env.example
install.sh
dev-rebuild.sh
QuantDinger-Vue/     ← 只有 3 个改过的文件,需要从 GitHub 补全
demo/
  mming-kline-demo.html
```

**关键: 补全 QuantDinger-Vue 仓库的其他文件**

```bash
# 把官方 QuantDinger-Vue 仓库 clone 到临时目录
cd ~
git clone --depth 1 https://github.com/brokermr810/QuantDinger-Vue.git qd-vue-orig

# 把 3 个改过的文件覆盖到原版
cp ~/quantdinger/QuantDinger-Vue/src/charts/indicators/netInflow.js \
   qd-vue-orig/src/charts/indicators/
cp ~/quantdinger/QuantDinger-Vue/src/views/indicator-analysis/components/KlineChart.vue \
   qd-vue-orig/src/views/indicator-analysis/components/
cp ~/quantdinger/QuantDinger-Vue/src/views/indicator-ide/index.vue \
   qd-vue-orig/src/views/indicator-ide/

# 替换 quantdinger/QuantDinger-Vue 为完整版
rm -rf ~/quantdinger/QuantDinger-Vue
mv qd-vue-orig ~/quantdinger/QuantDinger-Vue
cd ~/quantdinger/QuantDinger-Vue
ls src/views/indicator-ide/
# 应该能看到 index.vue 和其他文件
```

> ⏱️ `git clone` 大约 1-2 分钟。

## 5. 启动后端 (用 GHCR 预编译镜像,不用本地 build 后端)

```bash
cd ~/quantdinger
docker compose -f docker-compose.ghcr.yml up -d postgres redis backend
```

> 第一次会从 ghcr.io 拉 3 个镜像 (postgres / redis / backend),大约 2-3 分钟。
> 注意: 这里**没起 frontend**,frontend 我们要本地 build。

**等后端就绪:**

```bash
# 看 backend health
docker compose -f docker-compose.ghcr.yml ps
# 等 backend status = (healthy),大约 30-60 秒

# 测试 API
curl -s http://127.0.0.1:5000/api/health
# 应该返回 {"status":"ok",...}
```

## 6. 构建前端 (本地 build,带我们的 3 个修改)

```bash
cd ~/quantdinger/QuantDinger-Vue
npm install --registry=https://registry.npmmirror.com
```

> ⏱️ 第一次 `npm install` 大约 2-3 分钟 (从淘宝镜像)。

**然后构建 Docker 镜像:**

```bash
cd ~/quantdinger
docker compose -f docker-compose.yml -f docker-compose.build.yml build frontend
```

> ⏱️ 第一次前端 build 大约 3-5 分钟 (有 npm + vue 编译)。
> 之后改代码 rebuild 只要 30-60 秒。

**启动前端容器:**

```bash
docker compose -f docker-compose.yml -f docker-compose.build.yml up -d frontend
sleep 5
docker compose -f docker-compose.yml -f docker-compose.build.yml ps
```

## 7. 打开页面

1. 在 Codespace 底部点 "Ports" 面板
2. 找到端口 8888 (frontend)
3. 点右边的 "Open in Browser" 地球图标
4. 浏览器自动跳到 `https://<codespace>-8888.app.github.dev/`
5. 登录: `quantdinger` / `123456`

## 8. 验证 4 个改动都生效

### 改动 1: K线图默认 4 指标

进入 "Indicator IDE" 页面,等几秒加载。
图表区**应该同时显示 4 个面板**:
- 顶部: K线 + MA(5,10,20) 3 条均线
- 副图 1: 成交量 (红绿柱)
- 副图 2: MACD (DIF/DEA/柱)
- 副图 3: 主力净流入 (红绿柱)

### 改动 2: 主力净流入按钮不再叠加

**反复点 "主力净流入" 按钮 5 次 → 图表里只出现 1 个 NET_INFLOW pane** (toggle off 后再点又出现)。

### 改动 3: 顶部搜索栏

工具栏顶部 watchlist 旁边应该有 "🔍 全市场搜索 600519 / TSLA" 输入框。
输入 "600519" 等 0.5 秒 → 浮层显示 "贵州茅台 sh600519"。

### 改动 4: tooltip / 周期按钮中文

- 鼠标悬停 K 线 → tooltip 显示 "时间 / 开盘 / 收盘 / 最高 / 最低 / 成交量" (中文)
- 周期按钮组: 1分 / 5分 / 15分 / 30分 / 1时 / 4时 / 1日 / 1周 (中文)

## 9. 离线 demo 网页

iPad Safari 直接打开:
```
file:///home/coder/quantdinger/demo/mming-kline-demo.html
```

> Codespace 容器内的 file:// 路径,iPad 看不到。要让 iPad 看 demo,需要起个 http server:
>
> ```bash
> cd ~/quantdinger/demo
> python3 -m http.server 8000
> ```
>
> 然后在 Codespace Ports 面板转发 8000,iPad Safari 打开 `https://<codespace>-8000.app.github.dev/mming-kline-demo.html`。

## 10. 改前端代码后重新 build

```bash
cd ~/quantdinger
./dev-rebuild.sh
```

30-60 秒后刷新页面即可。

## 常见问题

| 问题 | 解决 |
|---|---|
| `npm install` 卡死 | 删 `node_modules` 重试;加 `--registry=https://registry.npmmirror.com` |
| `docker compose` 报 "port already in use" | Codespace 端口 8888 已被占用,改 `.env` 文件里 `FRONTEND_PORT=9999` |
| build 报 `loadLocales is not exported by klinecharts` | 打开 `QuantDinger-Vue/src/views/indicator-analysis/components/KlineChart.vue` 第 171 行,删掉 `loadLocales,` 这个 import 名字,只保留 try/catch 里的动态 require |
| 看到 "Build error: Cannot find module 'klinecharts'" | 漏了 `npm install`;回到第 6 步重跑 |
| 搜索栏输入 "TSLA" 没反应 | 后端 `searchSymbols` 接口可能被墙;Codespace 里 curl 测一下 `http://localhost:5000/api/symbol/search?market=USStock&keyword=TSLA` |
| toggle 点了没反应 | 父组件 `updateIndicators` 没正确响应 `indicator-toggle` 事件;看浏览器 DevTools console |

## 备份重要数据

```bash
# 备份 backend.env
cp ~/quantdinger/backend.env ~/backend.env.bak

# 备份数据库
docker compose -f docker-compose.ghcr.yml exec -T postgres \
  pg_dump -U quantdinger quantdinger > ~/quantdinger-db-$(date +%F).sql
```

## 完整删除 (重新来)

```bash
cd ~/quantdinger
docker compose -f docker-compose.yml -f docker-compose.build.yml down -v
docker compose -f docker-compose.ghcr.yml down -v
docker system prune -af
cd ~
rm -rf quantdinger
```

## 步骤总览 (5 分钟快查)

```bash
# 0. 上传 zip 到 Codespace
# 1. 解压
cd ~ && unzip -o mming-qd-full.zip -d quantdinger && cd quantdinger

# 2. 补全 QuantDinger-Vue 源码
cd ~ && git clone --depth 1 https://github.com/brokermr810/QuantDinger-Vue.git qd-vue-orig
cp ~/quantdinger/QuantDinger-Vue/src/charts/indicators/netInflow.js qd-vue-orig/src/charts/indicators/
cp ~/quantdinger/QuantDinger-Vue/src/views/indicator-analysis/components/KlineChart.vue qd-vue-orig/src/views/indicator-analysis/components/
cp ~/quantdinger/QuantDinger-Vue/src/views/indicator-ide/index.vue qd-vue-orig/src/views/indicator-ide/
rm -rf ~/quantdinger/QuantDinger-Vue && mv qd-vue-orig ~/quantdinger/QuantDinger-Vue

# 3. 启动后端 (GHCR 预编译)
cd ~/quantdinger && docker compose -f docker-compose.ghcr.yml up -d postgres redis backend

# 4. npm install
cd ~/quantdinger/QuantDinger-Vue && npm install --registry=https://registry.npmmirror.com

# 5. 构建并启动前端
cd ~/quantdinger && docker compose -f docker-compose.yml -f docker-compose.build.yml up -d --build frontend

# 6. 浏览器打开 Codespace 端口 8888
```

🎉 完成。
