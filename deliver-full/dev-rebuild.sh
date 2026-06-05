#!/bin/bash
# dev-rebuild.sh — QuantDinger-Vue 改源码后,增量重建前端容器
#
# 用法: 在 Codespace 仓库根目录(与 docker-compose.yml 同级)执行
#   ./dev-rebuild.sh
#
# 假设目录结构:
#   ./
#   ├── docker-compose.yml
#   ├── docker-compose.build.yml
#   ├── QuantDinger-Vue/         ← 你改的源码
#   ├── backend_api_python/
#   └── dev-rebuild.sh           ← 这个脚本

set -e

cd "$(dirname "$0")"

echo "==> [1/3] 构建 frontend 镜像 (增量 build, ~2-3 分钟)"
docker compose \
  -f docker-compose.yml \
  -f docker-compose.build.yml \
  build frontend

echo "==> [2/3] 重启 frontend 容器"
docker compose \
  -f docker-compose.yml \
  -f docker-compose.build.yml \
  up -d frontend

echo "==> [3/3] 等 10 秒让容器就绪"
sleep 10
docker compose \
  -f docker-compose.yml \
  -f docker-compose.build.yml \
  ps frontend

echo ""
echo "✅ 完成。浏览器刷新页面即可看到改动。"
echo "   - Codespace 端口 8888 转发: 点击 Ports 面板的地球图标"
echo "   - 看实时日志: docker compose -f docker-compose.yml -f docker-compose.build.yml logs -f frontend"
