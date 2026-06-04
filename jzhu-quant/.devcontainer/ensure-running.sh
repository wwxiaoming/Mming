#!/bin/bash
# Codespace 每次启动时执行:如果服务挂了,自动重启
# (不重复 docker compose up,避免占用太多资源)

# 检查小宇量化
if ! curl -sf http://localhost:8180/api/plugin/health > /dev/null 2>&1; then
  echo "⚠️ 检测到小宇量化未运行,正在重启 ..."
  cd "$(dirname "$0")/.." 2>/dev/null || cd "$(pwd)"
  if [ -d jzhu-trading ]; then
    cd jzhu-trading && docker compose up -d 2>&1 | tail -5
  fi
fi

# 检查 Web 服务器
if [ -f /tmp/webserver.pid ] && ps -p $(cat /tmp/webserver.pid) > /dev/null 2>&1; then
  : # 已经在跑,啥也不做
else
  echo "⚠️ Web 服务器不在跑,正在启动 ..."
  cd "$(dirname "$0")/.." 2>/dev/null || cd "$(pwd)"
  if [ -d jzhu-trading ]; then
    cd jzhu-trading
    nohup python3 server.py > /tmp/webserver.log 2>&1 &
    echo $! > /tmp/webserver.pid
    sleep 1
    echo "✅ Web 服务器已重启,PID $(cat /tmp/webserver.pid)"
  fi
fi
