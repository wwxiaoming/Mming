#!/bin/bash
# Codespace 首次创建时执行:解压 + 启动小宇量化 + 启动 Web 服务器
set -e

WORKSPACE_DIR="$(pwd)"
echo "📂 工作目录: $WORKSPACE_DIR"

# 1) 解压(只在第一次)
if [ -f "jzhu-trading.zip" ] && [ ! -d "jzhu-trading" ]; then
  echo "📦 解压 jzhu-trading.zip ..."
  unzip -o jzhu-trading.zip -d jzhu-trading
  echo "✅ 解压完成"
elif [ -d "jzhu-trading" ]; then
  echo "✅ jzhu-trading 目录已存在,跳过解压"
else
  echo "⚠️ 没找到 jzhu-trading.zip 也没找到 jzhu-trading 目录"
  echo "   请确认 jzhu-trading.zip 已上传到仓库根目录"
  exit 1
fi

cd jzhu-trading

# 2) 启动小宇量化(Docker Compose)
echo "🐳 启动小宇量化 (docker compose up -d) ..."
docker compose up -d 2>&1 | tail -10

# 3) 等后端就绪
echo "⏳ 等待后端就绪 ..."
for i in {1..90}; do
  if curl -sf http://localhost:8180/api/plugin/health > /dev/null 2>&1; then
    echo "✅ 后端已就绪(用了 ${i} 秒)"
    break
  fi
  if [ $i -eq 90 ]; then
    echo "⚠️ 90 秒内后端未响应,继续执行(可能首次启动较慢)"
  fi
  sleep 1
done

# 4) 启动 Web 服务器(后台)
echo "🌐 启动 Web 服务器(端口 8000,后台运行) ..."
nohup python3 server.py > /tmp/webserver.log 2>&1 &
echo $! > /tmp/webserver.pid
sleep 2
if ps -p $(cat /tmp/webserver.pid) > /dev/null 2>&1; then
  echo "✅ Web 服务器已启动,PID $(cat /tmp/webserver.pid)"
  echo "📜 日志: tail -f /tmp/webserver.log"
else
  echo "❌ Web 服务器启动失败,查看日志: cat /tmp/webserver.log"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 全部就绪!下一步:"
echo "   1) 底部 PORTS 标签确认 8000 端口已转发"
echo "   2) 点 8000 右侧的 🌍 图标打开工具页"
echo "   3) 股票代码输 600519,日期选近一年,点查询"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
