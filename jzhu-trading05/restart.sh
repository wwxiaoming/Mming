#!/bin/bash
echo "Restarting 小宇量化 (JZhu Trading)..."
echo ""

# macOS: APFS is case-insensitive but Docker's file-sharing allowlist checks
# case-sensitively. If the user cd'd via /users/... instead of /Users/...,
# Docker will reject volume mounts. Fix the case before anything else.
if [ "$(uname)" = "Darwin" ]; then
    case "$PWD" in
        /[Uu]sers/*)
            _expected="/Users/${PWD#/[Uu]sers/}"
            if [ -d "$_expected" ] && [ "$PWD" != "$_expected" ]; then
                cd "$_expected"
            fi
            ;;
    esac
fi

# Pre-flight: reject paths with spaces / non-ASCII (see start.sh for rationale).
case "$PWD" in
  *" "*)
    echo "============================================"
    echo "  [错误 / ERROR] 安装路径包含空格 / Install path contains a space"
    echo "  当前路径 / Current: $PWD"
    echo ""
    echo "  Docker Desktop 不能可靠处理带空格的 bind-mount 路径。"
    echo "  请把 jzhu-trading 文件夹移到无空格路径下重新运行。"
    echo ""
    echo "  Move the folder to a no-space path and re-run."
    echo "  推荐 / Recommended: ~/jzhu-trading/"
    echo "============================================"
    exit 1
    ;;
esac
# Whitelist check: path must only contain safe chars (a-z A-Z 0-9 / . _ -)
if printf '%s' "$PWD" | grep -qE '[^a-zA-Z0-9/._ -]'; then
    echo "============================================"
    echo "  [错误 / ERROR] 安装路径包含非英文字符"
    echo "  当前路径 / Current: $PWD"
    echo ""
    echo "  请把文件夹移到纯英文路径下,然后重新运行 ./restart.sh。"
    echo "  Move the folder to a pure-English path and re-run."
    echo "  推荐 / Recommended: ~/jzhu-trading/"
    echo "============================================"
    exit 1
fi

export HOST_INSTALL_PATH="$PWD"

# LAN IP detection (see start.sh for rationale). Silently empty on failure.
HOST_LAN_IP=$(ipconfig getifaddr en0 2>/dev/null)
[ -z "$HOST_LAN_IP" ] && HOST_LAN_IP=$(ipconfig getifaddr en1 2>/dev/null)
[ -z "$HOST_LAN_IP" ] && HOST_LAN_IP=$(hostname -I 2>/dev/null | awk '{print $1}')
export HOST_LAN_IP

# Check Docker Desktop. Auto-launch if installed but not running.
if ! docker info >/dev/null 2>&1; then
    if [ ! -d "/Applications/Docker.app" ]; then
        echo "============================================"
        echo "  ❌ Docker Desktop 未安装"
        echo ""
        echo "  请先安装 Docker Desktop（免费）："
        echo "  https://docker.com/products/docker-desktop"
        echo ""
        echo "  点击 Download Docker Desktop，选择匹配的版本："
        echo "    Mac (Apple芯片 M1/M2/M3/M4)  → Apple Silicon"
        echo "    Mac (Intel芯片)               → Intel Chip"
        echo "    Windows (绝大多数电脑)         → Windows AMD64"
        echo ""
        echo "  安装后无需注册登录，弹出的登录页面直接 Skip 跳过即可"
        echo "  安装完成后重新运行本脚本。"
        echo "============================================"
        exit 1
    fi

    echo "Docker Desktop 未启动，正在自动启动..."
    open -a Docker 2>/dev/null
    echo "等待 Docker 引擎就绪（最长 3 分钟）"
    printf "  "
    elapsed=0
    while ! docker info >/dev/null 2>&1; do
        sleep 3
        elapsed=$((elapsed + 3))
        printf "."
        if [ "$elapsed" -ge 180 ]; then
            echo ""
            echo "============================================"
            echo "  ❌ Docker 引擎 3 分钟内未启动"
            echo ""
            echo "  请手动打开 Docker Desktop 并检查："
            echo "    - 菜单栏 🐳 图标显示为 'Docker Desktop is running'?"
            echo "    - 是否有首次启动的设置弹窗等待确认?"
            echo "    - 系统设置 → 隐私与安全性 是否允许 Docker 运行?"
            echo ""
            echo "  确认 Docker 已运行后重新执行本脚本。"
            echo "============================================"
            exit 1
        fi
    done
    echo ""
    echo "Docker 就绪（耗时 ${elapsed}s）"
    echo ""
fi

# Stop our own containers first — releases their host-port bindings cleanly.
docker compose down 2>/dev/null

# If another Docker container is holding our ports, stop it too.
# (Never kill host processes ourselves: on Docker Desktop those ports may be
# held by com.docker.backend / vpnkit, and kill -9 would take Docker down.)
our_project=$(basename "$PWD" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9_-]//g')
for port in 18080 8180; do
    while IFS=$'\t' read -r cid cname cproject; do
        [ -z "$cid" ] && continue
        if [ "$cproject" != "$our_project" ]; then
            echo "⚠️  端口 $port 被另一个 Docker 容器占用: $cname (项目: ${cproject:-无})"
            echo "   正在停止该容器..."
            docker stop "$cid" >/dev/null 2>&1
        fi
    done < <(docker ps --filter "publish=$port" --format "{{.ID}}	{{.Names}}	{{.Label \"com.docker.compose.project\"}}")
done

echo "正在检查更新并启动服务，请稍候..."
docker compose pull --quiet
if ! docker compose up -d; then
    echo ""
    echo "============================================"
    echo "  ❌ 启动失败！"
    echo ""
    echo "  请尝试以下步骤："
    echo "    1. 完全退出 Docker Desktop 后重新打开"
    echo "    2. 等待 Docker Desktop 启动完成（图标不再转动）"
    echo "    3. 重新运行 ./restart.sh"
    echo ""
    echo "  如果仍然失败，请检查 Docker Desktop 设置："
    echo "    Settings → Resources → File Sharing"
    echo "    确保包含当前路径: $PWD"
    echo "============================================"
    exit 1
fi
echo ""
echo "============================================"
echo "  启动成功！正在打开浏览器..."
echo "  http://localhost:18080"
echo "============================================"

# Auto-open browser (works on Mac and Linux)
sleep 3
if command -v open >/dev/null 2>&1; then
    open http://localhost:18080
elif command -v xdg-open >/dev/null 2>&1; then
    xdg-open http://localhost:18080
fi
