# 上传到 Git 仓库

## 方式 1:新建空仓库(推荐)
```bash
cd <你的本地路径>
unzip v1.6-stock-trader.zip
cd v1.6-stock-trader
git init
git add .
git commit -m "init: v1.6 stock-trader-agent automation"
git branch -M main
git remote add origin https://github.com/<你的用户名>/<repo>.git
git push -u origin main
```

## 方式 2:加到已有仓库
```bash
cd <已有仓库>
unzip -o /path/to/v1.6-stock-trader.zip
git add scripts/ STOCK_CONTEXT.md POSITIONS.md DAILY_LOG.md
git commit -m "feat: add v1.6 stock-trader-agent daily automation"
git push
```

## 启用前要做的 3 件事

1. **改真实成本价**:编辑 `scripts/run_daily.sh`,把 `HOLDINGS_COST="1.55"` 改成你的真实平均成本
2. **加 cron 自动化**(可选,Trae IDE 里更方便):
   - 频率:工作日 07:00
   - 命令:`bash /workspace/scripts/run_daily.sh`
3. **挂飞书 Webhook**(可选):
   ```bash
   export FEISHU_WEBHOOK="https://open.feishu.cn/open-apis/bot/v2/hook/xxx"
   ```

## 验证
```bash
bash scripts/run_daily.sh
# 应该输出 6 通道文件:
ls -la daily_picks/$(date +%F).md
ls -la POSITIONS.md DAILY_LOG.md STOCK_CONTEXT.md
```

## 文件清单
| 文件 | 大小 | 作用 |
|---|---|---|
| scripts/_common.py | 8 KB | 公共基础(腾讯/东财/同花顺/news + 限流) |
| scripts/us_market_fetcher.py | 4 KB | 拉美股 5 指数 + 7 巨头 + 半导体 + 中概 |
| scripts/strategy_holdings_tracker.py | 4 KB | 159941 持仓跟踪 |
| scripts/daily_stock_pick.py | 16 KB | 9 策略并行 |
| scripts/post_report.py | 16 KB | 拼 Markdown 14+1 章节 |
| scripts/auto_publish.py | 20 KB | 6 通道自动写出 |
| scripts/run_daily.sh | 2 KB | 主调度 |
| scripts/README.md | 4 KB | 使用说明 |
| STOCK_CONTEXT.md | <1 KB | 上下文(自动更新) |
| POSITIONS.md | <1 KB | 持仓表(自动更新) |
| DAILY_LOG.md | 2 KB | 日志(自动追加) |

**总计 ~70 KB,11 个文件**

## 数据源
- 腾讯财经 qt.gtimg.cn(不封 IP)
- 同花顺热点 zx.10jqka.com.cn(零鉴权)
- 东财 np-weblist.eastmoney.com(已加 em_throttle 限流)

**零 API key,零依赖,纯 HTTP 直连。**
