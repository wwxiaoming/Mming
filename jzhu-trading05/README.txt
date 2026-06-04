小宇量化 (JZhu Trading)
======================

系统要求：
  - 内存：最低 8GB，推荐 16GB
  - 磁盘：至少 5GB 可用空间
  - 安装 Docker Desktop (https://docker.com/products/docker-desktop)

启动：
  Windows:  双击 start.bat
  Mac:      终端运行 ./start.sh

停止：
  Windows:  双击 stop.bat
  Mac:      终端运行 ./stop.sh

重启（自动更新到最新版本，无需重新下载）：
  Windows:  双击 restart.bat
  Mac:      终端运行 ./restart.sh

访问：http://localhost:18080

磁盘清理（可选）：
  如果磁盘空间不足，可运行以下命令清理旧版本镜像：
  docker image prune -f

数据存放在 data/ 目录下。删除整个文件夹即可完全卸载。

------------------------------------------------------------
常见问题
------------------------------------------------------------

Q: Windows 下双击 start.bat 提示"路径含非英文字符",但路径明明是英文?
A: 极少数情况下,Anaconda 等工具会清理掉系统 PATH 里的 PowerShell 目录,
   导致脚本误判。新版脚本已自动回退到 pwsh 或绝对路径,无需手动处理。
   如果仍报错,管理员开 cmd 执行:
       setx PATH "%PATH%;C:\Windows\System32\WindowsPowerShell\v1.0"
   然后关闭所有 cmd 窗口重开,重新双击 start.bat 即可。
