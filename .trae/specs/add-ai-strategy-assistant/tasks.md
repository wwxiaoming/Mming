# Tasks

- [ ] Task 1: AI 配置后端（Java 端 system_config 增删改查 + AES 加密）
  - [ ] SubTask 1.1: 写 `AIConfigController` 暴露 4 个端点（GET 读 / POST 写 / POST 验密 / DELETE 清空）
  - [ ] SubTask 1.2: 写 `AESUtil` 加密工具（Key 从 `HOST_INSTALL_PATH/config/.ai.key` 读，启动时生成）
  - [ ] SubTask 1.3: 在 `db-init/04_init_system_config.sql` 增加 4 个默认配置（`ai.provider=deepseek` 等）
  - [ ] SubTask 1.4: 写 1 个单元测试：保存 → 读取 → 验证解密后明文匹配

- [ ] Task 2: Python AI 服务（ai-service 容器）
  - [ ] SubTask 2.1: 搭 FastAPI 骨架（`/ai/nl-to-strategy` `/ai/analyze-kline` `/ai/optimize-strategy` 3 端点，全 SSE 流式）
  - [ ] SubTask 2.2: 写 `LLMClient`（OpenAI 协议，stream=True, 支持 DeepSeek/OpenAI/自定义 base_url）
  - [ ] SubTask 2.3: 写 `PromptTemplates` 三个 prompt 模板（system + few-shot）
    - 子提示：策略代码模板必须用 Groovy（不是 backtrader Python），引用 `ctx.close / ctx.ma5 / ctx.macd.dif / ctx.macd.dea / ctx.macd.macd / ctx.fundFlow.mainNet`
  - [ ] SubTask 2.4: 写 `DataFetcher`（调 Java 8180 拿 K线/MA/MACD/资金流/财务，组织成结构化 dict）
  - [ ] SubTask 2.5: 写 `CodeValidator`（正则拦危险调用 + 长度截断 + AST 校验 Groovy 语法）
  - [ ] SubTask 2.6: 写 Dockerfile（python:3.11-slim + 依赖：fastapi/uvicorn/openai/httpx）
  - [ ] SubTask 2.7: 启动后自动注册到 `ai_usage` 表（通过 Java 端写入）

- [ ] Task 3: Java 后端 SSE 代理
  - [ ] SubTask 3.1: 在 Spring WebFlux 用 `WebClient` 转发 `/api/plugin/ai/*` → `http://ai-service:8282/*`
  - [ ] SubTask 3.2: 透传 SSE 头（`Content-Type: text/event-stream` / `Cache-Control: no-cache` / `X-Accel-Buffering: no`）
  - [ ] SubTask 3.3: 限流中间件（同一 IP 1 分钟 > 10 次 → 429）

- [ ] Task 4: 改 compose.yml / compose-lite.yml 加 ai-service 服务
  - [ ] SubTask 4.1: compose-lite.yml 增加 `ai-service` 服务（依赖 app depends_on）
  - [ ] SubTask 4.2: 配置环境变量 `AI_DEFAULT_BASE_URL` / `AI_DEFAULT_MODEL`
  - [ ] SubTask 4.3: 验证 `docker compose up -d` 后 8282 端口可访问

- [ ] Task 5: web-app 前端 - 设置页
  - [ ] SubTask 5.1: 新建 `/settings/ai` 路由（4 个表单字段 + 保存按钮 + 测试连接按钮）
  - [ ] SubTask 5.2: API Key 字段脱敏显示（仅显示首 3 + 尾 4 字符）
  - [ ] SubTask 5.3: "测试连接"按钮：POST `/api/plugin/ai/test` 触发一次小请求

- [ ] Task 6: web-app 前端 - 策略编辑器 AI 助手
  - [ ] SubTask 6.1: 编辑器右侧加可折叠面板（380px 宽）
  - [ ] SubTask 6.2: 实现 SSE 客户端（EventSource 不支持 POST → 用 fetch + ReadableStream 解析）
  - [ ] SubTask 6.3: 5 个快捷指令（一键帮我写 / 我有代码想回测 / 验证可行性 / 帮我优化 / 分析走势）
  - [ ] SubTask 6.4: 模型选择下拉（deepseek-chat / deepseek-coder / 用户自定义）
  - [ ] SubTask 6.5: "应用"按钮：把生成的代码填入主编辑器

- [ ] Task 7: web-app 前端 - K线 AI 解读按钮
  - [ ] SubTask 7.1: K线图右上角加 🤖 按钮
  - [ ] SubTask 7.2: 点击弹右侧抽屉（420px 宽），流式显示 3 段
  - [ ] SubTask 7.3: 底部红字警示"AI 解读仅供参考,不构成投资建议"
  - [ ] SubTask 7.4: 在策略详情页 + K线详情页同步加

- [ ] Task 8: web-app 前端 - 策略详情页 AI 优化
  - [ ] SubTask 8.1: 回测结果卡片下方加"AI 优化建议"折叠面板
  - [ ] SubTask 8.2: 点"AI 优化"流式显示 3 条结构化建议（带代码 diff 片段）

- [ ] Task 9: 改 Mming量化 index.html 加 AI 入口
  - [ ] SubTask 9.1: 新增第 4 个 tab "🤖 AI 解读"
  - [ ] SubTask 9.2: 复用已查询的 stockCode/日期
  - [ ] SubTask 9.3: SSE 流式显示 3 段（趋势 / 信号 / 建议）

- [ ] Task 10: 沙箱与安全
  - [ ] SubTask 10.1: `CodeValidator` 拦截 6 类危险调用
  - [ ] SubTask 10.2: 长度限制 5000 字符
  - [ ] SubTask 10.3: 单元测试：故意让 LLM 输出 `Runtime.exec` → 验证 403

- [ ] Task 11: 成本统计
  - [ ] SubTask 11.1: 新建 `ai_usage` 表（user_id/model/prompt_tokens/completion_tokens/cost_estimate/created_at）
  - [ ] SubTask 11.2: AI 服务每次调用结束把 token 数 POST 给 Java 端入库
  - [ ] SubTask 11.3: 设置页底部显示本月累计 token 用量与估算费用

- [ ] Task 12: 文档 & 启动脚本
  - [ ] SubTask 12.1: `README.txt` 加"AI 配置"章节
  - [ ] SubTask 12.2: `CODESPACES.md` 加"AI 服务的环境变量"说明
  - [ ] SubTask 12.3: 在 `start.sh` / `start.bat` 加"AI 未配置"检测（首次启动提示）

# Task Dependencies

- Task 2 (Python AI 服务) 依赖 Task 1 (Java 端 system_config 写入)
- Task 3 (Java SSE 代理) 依赖 Task 2
- Task 4 (compose 集成) 依赖 Task 2 + Task 3
- Task 6 / 7 / 8 (web-app 前端) 依赖 Task 3
- Task 9 (Mming量化) 依赖 Task 3
- Task 10 (沙箱) 依赖 Task 2.5
- Task 11 (成本) 依赖 Task 2
- Task 12 (文档) 是最后做

# 并行可拆分

- Task 1、Task 2.1~2.3、Task 5 可并行
- Task 6/7/8/9 前端可并行
- Task 10、Task 11 独立
