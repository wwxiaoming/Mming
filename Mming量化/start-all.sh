#!/bin/bash
# 启动量化系统 + 一体化服务器(给你 Codespace 用)
set -e
cd "$(dirname "$0")"

echo "=== 1/3 启动量化系统 (docker compose) ==="
docker compose up -d

echo ""
echo "=== 2/3 等待后端就绪 ==="
for i in {1..60}; do
  if curl -sf http://localhost:8180/api/plugin/health > /dev/null 2>&1; then
    echo "✅ 后端就绪"
    break
  fi
  if [ $i -eq 60 ]; then
    echo "⚠️ 60 秒内后端未就绪,继续启动(可能需要更长时间)"
  fi
  sleep 1
done

echo ""
echo "=== 3/3 启动静态+代理服务器(端口 8000) ==="
echo "  → 浏览器转发 8000 端口打开页面"
echo "  → 8180 端口也建议转发(备用)"
echo ""
python3 server.py
