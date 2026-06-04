# 小宇量化工具(运行在 GitHub Codespaces)

## 快速启动

```bash
cd jzhu-quant
bash start-all.sh
```

启动后:
- **8000 端口**(必转发):打开 `http://localhost:8000` —— 资金流向工具主页
- **8180 端口**(可选转发):打开 `http://localhost:8180` —— 量化系统自带 UI

## 文件说明

| 文件 | 作用 |
|---|---|
| `index.html` | 资金流向工具主页面(打开 8000 看的就是这个) |
| `server.py` | 一体化服务器:静态文件 + 反向代理 `/api/* → 8180` |
| `start-all.sh` | 一键启动(量化系统 + 服务器) |
| `compose.yml` | 量化系统的 Docker 配置 |
| `start.sh` / `stop.sh` | 量化系统单独的启停(被 start-all.sh 包含) |
| `prompt-1.txt` ~ `prompt-5.txt` | 5 个提示词,本仓库的 `index.html` 已按它们实现 |
| `API.html` | 本地 API 浏览器(打开 8000/API.html) |
| `db-init/` | 数据库初始化 SQL |

## 端口转发(Codespaces 关键步骤)

1. 底部 **PORTS** 标签
2. 加 **8000**(主页面)和 **8180**(API 备用)
3. 8000 右边的 🌍 图标点开就是工具页

## iPad 注意事项

- Safari 打开 GitHub → Codespace 完全可以用
- 文件小、用文件树点选比拖拽方便
- 转发 URL 在 Safari 直接点 globe 图标打开就行
- 服务器不要关(Codespace 会按空闲自动休眠)
