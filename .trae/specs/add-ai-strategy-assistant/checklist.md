# Checklist

## 数据层

- [ ] `system_config` 表新增 4 个默认配置（`ai.provider` / `ai.base_url` / `ai.api_key` / `ai.model`）
- [ ] `ai_usage` 表创建，含 user_id/model/prompt_tokens/completion_tokens/cost_estimate/created_at 字段
- [ ] AES 加密工具类实现，Key 从 `./config/.ai.key` 读（首次启动生成）
- [ ] AI 配置 GET / POST / DELETE 端点实现，POST 验密（解密后再加密）走通

## AI 服务（Python）

- [ ] FastAPI 启动后 `/health` 返回 ok
- [ ] `/ai/nl-to-strategy` 端点流式返回 Groovy 代码（用 EventSource/fetch+ReadableStream 验证）
- [ ] `/ai/analyze-kline` 端点先调 8180 拿 K线 + MA + MACD + 资金流，再调 LLM
- [ ] `/ai/optimize-strategy` 端点接收 strategy_script + backtest_result，返回 3 条建议
- [ ] LLMClient 支持 deepseek / openai / 自定义 base_url 三种
- [ ] Prompt 模板 3 个：策略生成 / K线解读 / 策略优化
- [ ] CodeValidator 拦 6 类危险调用（Runtime.exec / System.exit / new File / new URL / ProcessBuilder / Class.forName）
- [ ] 代码长度截断（>5000 字符）
- [ ] Dockerfile 构建成功，镜像启动后 8282 端口可访问
- [ ] 单元测试：故意让 LLM 输出 `Runtime.exec` → 验证 403

## Java 后端 SSE 代理

- [ ] `/api/plugin/ai/nl-to-strategy` 转发到 ai-service 8282
- [ ] SSE 头（Content-Type / Cache-Control / X-Accel-Buffering）完整透传
- [ ] 限流中间件：同 IP 1 分钟 > 10 次 → 429
- [ ] 限流计数器不依赖外部（用 Caffeine 本地缓存即可）

## 部署

- [ ] `compose-lite.yml` 增加 ai-service 服务
- [ ] `compose.yml` 同步增加
- [ ] `docker compose up -d` 启动 3 容器：db / app / ai-service 都健康
- [ ] 环境变量 `AI_DEFAULT_BASE_URL` / `AI_DEFAULT_MODEL` 注入成功

## web-app 前端 - 设置页

- [ ] `/settings/ai` 路由可访问
- [ ] 4 个字段渲染，API Key 脱敏显示
- [ ] 保存按钮可用，提示"已保存"
- [ ] "测试连接"按钮：成功显示绿色 ✓，失败显示红色 ✗ 与原因
- [ ] 删除配置按钮：清空 4 个字段

## web-app 前端 - 策略编辑器

- [ ] 编辑器右侧 AI 面板（380px 宽）可折叠
- [ ] 5 个快捷指令可点
- [ ] 输入自然语言 + 点发送 → 面板流式显示 AI 输出
- [ ] "应用"按钮把生成的代码填入主编辑器
- [ ] "自动检查 AI 是否听懂"勾选框可用
- [ ] 模型下拉可切（deepseek-chat / deepseek-coder / 自定义）

## web-app 前端 - K线 AI 解读

- [ ] K线图右上角 🤖 按钮渲染
- [ ] 点击弹右侧抽屉（420px 宽）
- [ ] 流式显示 3 段（趋势 / 信号 / 建议）
- [ ] 底部红字警示"AI 解读仅供参考"渲染
- [ ] AI 未配置时弹"请先在设置页配置 AI"

## web-app 前端 - 策略详情 AI 优化

- [ ] 回测结果卡片下方"AI 优化建议"折叠面板渲染
- [ ] 点击流式显示 3 条结构化建议（含代码 diff）
- [ ] 优化历史可折叠查看

## Mming量化

- [ ] 第 4 个 tab "🤖 AI 解读"渲染
- [ ] 复用已查询的 stockCode + 日期
- [ ] SSE 流式显示 3 段（趋势 / 信号 / 建议）

## 沙箱与安全

- [ ] CodeValidator 拦 6 类危险调用（已测）
- [ ] 长度 >5000 字符截断
- [ ] Groovy AST 校验（语法错误返回具体行号）

## 成本控制

- [ ] `ai_usage` 表写入成功
- [ ] 设置页底部显示本月累计 token 用量
- [ ] 估算费用按 DeepSeek 公开价 ¥1/M input, ¥2/M output 计算

## 文档

- [ ] `README.txt` 增加"AI 配置"章节
- [ ] `CODESPACES.md` 增加"AI 服务环境变量"说明
- [ ] 首次启动检测到无 AI 配置时弹引导卡

## 端到端验收

- [ ] 装好整个 docker compose → 启动 → 打开 http://localhost:18080
- [ ] 进入设置页填入 DeepSeek API Key → 测试连接通过
- [ ] 打开策略编辑器 → 输入"5日均线上穿20日均线买入" → 看到 AI 流式输出 Groovy 代码 → 应用 → 跑回测
- [ ] 打开 K线详情页 → 点 🤖 → 流式看到 AI 解读
- [ ] Mming量化 8000 端口 → AI 解读 tab 可用
- [ ] 关掉 API Key 后所有 AI 入口显示"请先配置"，老功能完全不受影响
