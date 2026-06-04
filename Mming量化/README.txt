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

------------------------------------------------------------
🤖 AI 功能（v1.1 新增）
------------------------------------------------------------

Mming量化内置了 AI 量化助手，需要配置大模型 API Key 才能使用。
不配 API Key 完全不影响原有功能。

支持的 Provider：
  - DeepSeek（推荐，国内便宜，1 元/百万 token）：https://platform.deepseek.com
  - OpenAI / GPT-4o / GPT-4o-mini
  - 自定义兼容 OpenAI 协议的 API（Azure / 通义千问 / 智谱等）

配置步骤：
  1. 打开 `config.json`（第一次启动会自动生成）
  2. 填入 `api_key` 字段
  3. 重启服务（双击 restart.bat 或 ./restart.sh）
  4. 浏览器打开 `http://localhost:8000`
  5. 切到「🤖 AI 助手」Tab
  6. 点「测试」按钮验证连通性

config.json 示例：
{
  "ai": {
    "provider": "deepseek",
    "base_url": "https://api.deepseek.com",
    "api_key": "sk-你的密钥",
    "model": "deepseek-chat"
  }
}

7 个 Tab 功能：
  - 数据查询     查 K线、资金流、统计指标
  - 资金图表     主力净流入可视化
  - 择时回测     跑策略、显示资金曲线
  - 📚 策略市场  11 个内置策略（MACD金叉/RSI超卖/黄金坑等），一键导入
  - 📊 策略详情  点卡片看买入/卖出逻辑 + K线 + 资金曲线对比
  - 🤖 AI 助手  对话流式生成策略 / K线 AI 解读
  - K线 🤖 按钮  K线区右上角"AI 解读"流式弹抽屉（趋势/信号/建议 3 段）

成本与限流：
  - 同 IP 1 分钟最多 10 次 AI 调用
  - 每次发送 prompt > 8000 token 自动截断
  - 设置页底部显示本月累计 token 用量与估算费用

------------------------------------------------------------
常见问题
------------------------------------------------------------

Q: Windows 下双击 start.bat 提示"路径含非英文字符",但路径明明是英文?
A: 极少数情况下,Anaconda 等工具会清理掉系统 PATH 里的 PowerShell 目录,
   导致脚本误判。新版脚本已自动回退到 pwsh 或绝对路径,无需手动处理。
   如果仍报错,管理员开 cmd 执行:
       setx PATH "%PATH%;C:\Windows\System32\WindowsPowerShell\v1.0"
   然后关闭所有 cmd 窗口重开,重新双击 start.bat 即可。
