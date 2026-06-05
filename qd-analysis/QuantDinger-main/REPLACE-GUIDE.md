# REPLACE-GUIDE — QuantDinger 改源码后,如何"换进"现有部署

> 改好源码 → 浏览器看到改动的 3 种方法

---

## 方法 A：Codespace commit + `./dev-rebuild.sh`（⭐ 推荐）

适用：你正在 Codespace 里改 + 想立即看到效果

### 步骤

```bash
# 1. 看改了什么
cd /workspaces/<你的仓库名>
git status
git diff --stat

# 2. 提交（建议每改一次就 commit 一次,方便回滚）
git add -A
git commit -m "feat: add 主力净流入 indicator + global search + zh-CN default"

# 3. 增量重建前端容器（~2-3 分钟,不会重建后端）
./dev-rebuild.sh
```

### 输出

```
==> [1/3] 构建 frontend 镜像
...
==> [2/3] 重启 frontend 容器
...
==> [3/3] 等 10 秒让容器就绪
NAME                        STATUS              PORTS
quantdinger-frontend        Up 10 seconds       0.0.0.0:80->80/tcp
```

### 看效果

- 浏览器按 `Ctrl+Shift+R` **强制刷新**（避免缓存）
- Codespace 端口 8888 转发 → 指标 IDE → 验证 3 个改动：
  1. 顶部股票选择器输入「600519」→ 应该看到「贵州茅台 sh600519 — CNStock — 全市场」
  2. 指标工具栏 → 应该看到「主力净流入」按钮 → 点击后下方多一个 pane
  3. 整个页面应该是中文（之前默认英文）

### 改坏了怎么办

```bash
# 回到上一个 commit
git reset --hard HEAD~1
./dev-rebuild.sh
```

---

## 方法 B：本地 build dist/ 覆盖挂载

适用：你在 Codespace 改完,想搬到**自建服务器**（不是 Codespace）

### 步骤

**A 端（Codespace）**：
```bash
# 1. 在 Codespace 里 build 出 dist/
cd QuantDinger-Vue
npm install --registry https://registry.npmmirror.com
npm run build
# 产物在 QuantDinger-Vue/dist/

# 2. 打包
cd ..
tar -czf quantdinger-vue-dist.tar.gz -C QuantDinger-Vue/dist .
```

**B 端（你的服务器）**：
```bash
# 3. 拷到服务器
scp quantdinger-vue-dist.tar.gz user@server:/tmp/

# 4. 服务器上解压覆盖
ssh user@server
cd /opt/quantdinger/frontend-data
tar -xzf /tmp/quantdinger-vue-dist.tar.gz

# 5. 重启容器
cd /opt/quantdinger
docker compose restart frontend
```

---

## 方法 C：导出 git patch 包,分享给他人

适用：你改完了,想发给朋友用

### A 端（你的 Codespace）

```bash
# 1. 先确保所有改动已 commit
git add -A
git commit -m "feat: add 主力净流入 + 全市场搜索 + 默认中文"

# 2. 导出最近 1 个 commit 的 patch
git format-patch -1 --output=/tmp/patches/

# 3. 打包 patch
tar -czf quantdinger-custom-patches.tar.gz /tmp/patches/

# 4. 上传 / 邮件 / 网盘 发给别人
```

### B 端（朋友）

```bash
# 1. 先 clone QuantDinger 和 QuantDinger-Vue
git clone https://github.com/brokermr810/QuantDinger.git
git clone https://github.com/brokermr810/QuantDinger-Vue.git

# 2. 应用 patch
cd QuantDinger-Vue
git am /path/to/patches/*.patch

# 3. 启动
cd ..
docker compose -f docker-compose.yml -f docker-compose.build.yml up -d --build
```

---

## FAQ

### Q1：重启后白屏 / `ERR_CONNECTION_REFUSED`？
A：容器没起来。看日志：
```bash
docker compose -f docker-compose.yml -f docker-compose.build.yml logs frontend --tail 50
```
常见原因：
- `npm run build` 失败 → 看 stderr
- 端口 80 被宿主机占用 → `docker ps` 看冲突

### Q2：浏览器看到的还是旧版？
A：**强制刷新** `Ctrl+Shift+R`（或 `Cmd+Shift+R`），别用 F5。
Codespace 还有一层浏览器缓存，可以 DevTools → Network → 勾 "Disable cache"。

### Q3：改坏了,如何回滚？
A：
```bash
git log --oneline -5     # 看 commit 历史
git reset --hard HEAD~1  # 回滚到上一个 commit
./dev-rebuild.sh
```

### Q4：build 一次要多久？
A：
- **第一次**：5-10 分钟（npm install 几百 MB 依赖）
- **第二次起**：1-3 分钟（增量 build,只重编改动的 .vue）
- **只改一个 .vue** 的情况：~30-60 秒

### Q5：build 时内存爆 / `JavaScript heap out of memory`？
A：Codespace 选 4-core / 16GB 机器。在 `QuantDinger-Vue/.env` 或构建时加：
```bash
NODE_OPTIONS=--max-old-space-size=4096 npm run build
```

### Q6：如何加环境变量（如 `ENABLED_MARKETS=...CNStock...`）？
A：编辑 `backend_api_python/.env`：
```bash
# 打开 A 股开关
ENABLED_MARKETS=Crypto,USStock,CNStock,HKStock,Forex,Futures,MOEX
SHOW_CN_STOCK=true
```
然后重启后端：
```bash
docker compose -f docker-compose.yml -f docker-compose.build.yml restart backend
```

### Q7：怎么把改动同步到 GitHub 仓库？
A：
```bash
git remote add origin https://github.com/<你的账号>/<你的仓库>.git
git push -u origin main
```

### Q8：默认密码忘了 / 想重置？
A：
```bash
docker compose -f docker-compose.yml -f docker-compose.build.yml exec backend \
  python -c "from app.utils.auth import hash_pwd; print(hash_pwd('新密码'))"
# 把 hash 写进数据库 user 表的 password_hash 字段
```

### Q9：怎么换回官方原版前端？
A：改 `docker-compose.yml` 的 frontend 段：
```yaml
frontend:
  image: ghcr.io/brokermr810/quantdinger-frontend:v3.0.28   # ← 用这个
  # build:
  #   context: ./QuantDinger-Vue
  #   dockerfile: Dockerfile
```
然后 `docker compose up -d frontend`。

### Q10：Codespace 配额用完了怎么办？
A：GitHub 每月免费 60 小时 core-time。可在 Settings → Codespaces → Usage 查看。建议：
- 不使用时主动 Stop Codespace
- 用 2-core 机器（4-core 2 倍速用配额）
- 不用时把改动 push 到 GitHub,下次开新 Codespace pull 即可
