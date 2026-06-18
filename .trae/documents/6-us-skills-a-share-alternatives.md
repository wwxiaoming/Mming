# 6 个美股 Skill 的 A 股替代方案

> 为 best_10 中 6 个美股工具（#4/#5/#6/#7/#9/#10）精选 1 对 1 A 股替代，下载、翻译、打包成独立的 **A 股增强包**，与 best_10 并存而非替换。
> 计划创建时间：2026-06-13

---

## 1. Summary

针对 `/workspace/skills_pack/best_10/` 中被识别为美股向的 6 个 skill，从 `yuping322/finskills`、`nicepkg/ai-workflow`、`sososun/mutual-fund-skills`、`longbridge/skills` 四个仓库中精选对应的 A 股替代 skill，做以下工作：

1. **git clone** 4 个仓库到 `/workspace/skills_pack/_repos/`
2. **抽取 6 个目标 skill** 到 `/workspace/skills_pack/_skills_ashare/`
3. **中文翻译 description**（同 best_10 的 fix_robust.py 思路，输出单行引号格式避免 `|` 问题）
4. **重新打包** 到 `/workspace/skills_pack/best_10/zips_ashare/`（独立目录，不污染原 zips）
5. **生成总包** `/workspace/skills_pack/best_10/ashare_bundle.zip`
6. **写说明文档** `/workspace/skills_pack/best_10/ASHARE_README.md` 标注对应关系

---

## 2. Current State Analysis

### 2.1 best_10 现有结构

```
/workspace/skills_pack/best_10/
├── 01_05_longbridge-earnings/      # 美/港/A 三市（保留）
├── 02_18_akshare_succ985/          # A/H/US/期货/基金/宏观（保留）
├── 03_11_longbridge-research/      # 美/港/A 三市（保留）
├── 04_01_company-valuation_himself65/  # ⚠️ 美股 yfinance
├── 05_12_sector-analyst_tradermonty/   # ⚠️ 美股 ETF
├── 06_15_macro-rates-monitor_anthropics/ # ⚠️ LSEG 美债
├── 07_21_market-breadth-analyzer/  # ⚠️ S&P 500
├── 08_24_commodities-quote_octagonai/   # 通用大宗（保留）
├── 09_22_market-top-detector/      # ⚠️ S&P 500
├── 10_07_institutional-flow-tracker/  # ⚠️ SEC 13F
├── zips/                           # 10 个独立 zip
├── top10_bundle.zip                # 总包
├── EXPLAINER.md / README.md / USAGE.md
```

### 2.2 已克隆但未用上的 A 股 skill 资源

- `nicepkg-aw/workflows/stock-trader-workflow/.claude/skills/` 下有：
  - `a-share-analysis` (123 installs)
  - `a-share-screener` (本地，没列安装量)
  - `china-macro-analyst` (79 installs)

### 2.3 关键约束（继承自前几轮工作）

- YAML description 必须用单行引号格式 `description: "..."`（前文 fix_robust.py 已修过的坑）
- 保持英文触发关键词（YAML frontmatter 内的英文 trigger 不能删，匹配语义检索）
- zip 解压后**只含** skill 目录本身（不能带 `zips/` 中间层）
- 不替换 best_10，**新增独立 A 股增强包**

---

## 3. Proposed Changes

### 3.1 6 个候选清单（精选 1 对 1 替代）

| # | 原美股 skill | A 股替代（owner/repo@skill） | 安装量 | 仓库 | 已克隆？ |
|---|------------|---------------------------|-------|------|--------|
| 1 | `04_company-valuation` | `nicepkg/ai-workflow@a-share-analysis` | 123 | nicepkg-aw | ✅ |
| 2 | `05_sector-analyst` | `yuping322/finskills@sector-rotation-detector` | 33 | yuping322 | ❌ |
| 3 | `06_macro-rates-monitor` | `nicepkg/ai-workflow@china-macro-analyst` | 79 | nicepkg-aw | ✅ |
| 4 | `07_market-breadth-analyzer` | `yuping322/finskills@limit-up-pool-analyzer` | 85 | yuping322 | ❌ |
| 5 | `09_market-top-detector` | `yuping322/finskills@equity-pledge-risk-monitor` | 24 | yuping322 | ❌ |
| 6 | `10_institutional-flow-tracker` | `sososun/mutual-fund-skills@fund-screener` | 193 | sososun | ❌ |

**总安装量**：123 + 33 + 79 + 85 + 24 + 193 = **537** 社区认可

### 3.2 文件变更清单

| 操作 | 路径 | 备注 |
|------|------|------|
| **新建** | `/workspace/skills_pack/_repos/yuping322-finskills/` | git clone |
| **新建** | `/workspace/skills_pack/_repos/sososun-mutual-fund/` | git clone |
| **新建** | `/workspace/skills_pack/_skills_ashare/` | 6 个 skill 抽取 |
| **新建** | `/workspace/skills_pack/build_ashare.py` | 抽取+翻译+打包 |
| **新建** | `/workspace/skills_pack/best_10/zips_ashare/` | 6 个独立 zip |
| **新建** | `/workspace/skills_pack/best_10/ashare_bundle.zip` | 总包 |
| **新建** | `/workspace/skills_pack/best_10/ASHARE_README.md` | 6 对 6 对应表 |
| **修改** | `/workspace/skills_pack/best_10/README.md` | 末尾加"6 个 A 股增强包"链接 |
| **修改** | `/workspace/skills_pack/best_10/USAGE.md` | 末尾加 A 股路由节 |

### 3.3 build_ashare.py 工作流（伪代码）

```python
import os, re, shutil, subprocess, zipfile

# 1. 确认/克隆 3 个新仓库（nicepkg-aw 已存在）
new_repos = {
    'yuping322-finskills': 'https://github.com/yuping322/finskills.git',
    'sososun-mutual-fund': 'https://github.com/sososun/mutual-fund-skills.git',
}
for name, url in new_repos.items():
    dst = f'/workspace/skills_pack/_repos/{name}'
    if not os.path.exists(dst):
        subprocess.run(['git', 'clone', '--depth=1', url, dst], check=True)

# 2. nicepkg-aw 已有 SKILL.md 路径映射
nicepkg_skills = '/workspace/skills_pack/_repos/nicepkg-aw/workflows/stock-trader-workflow/.claude/skills'

# 3. 6 个目标 skill 的 (源, 目标名) 映射
mapping = [
    ('nicepkg-aw/.../a-share-analysis',     'A01_a-share-analysis'),
    ('yuping322-finskills/.../sector-rotation-detector', 'A02_sector-rotation-detector'),
    ('nicepkg-aw/.../china-macro-analyst',  'A03_china-macro-analyst'),
    ('yuping322-finskills/.../limit-up-pool-analyzer',   'A04_limit-up-pool-analyzer'),
    ('yuping322-finskills/.../equity-pledge-risk-monitor','A05_equity-pledge-risk-monitor'),
    ('sososun-mutual-fund/.../fund-screener', 'A06_fund-screener'),
]

# 4. 抽取 → 翻译 → 打包
#    翻译策略: 复用 best_10/fix_robust.py 的 BLOCK_RE / QUOTED_RE / BARE_RE 三重匹配
#    翻译表预定义（每个 skill 的 description 人工翻译为中文 + 保留英文触发词）
zh_descs = {
    'a-share-analysis': "A 股综合分析工具，...",
    'sector-rotation-detector': "用申万/中证板块数据...",
    'china-macro-analyst': "中国宏观分析...",
    'limit-up-pool-analyzer': "A 股涨停池分析...",
    'equity-pledge-risk-monitor': "A 股股权质押风险监控...",
    'fund-screener': "公募基金筛选与持仓分析...",
}

# 5. 输出到 best_10/zips_ashare/A0N_xxx.zip
#    + 总包 ashare_bundle.zip
```

### 3.4 中文翻译要点（参考 best_10 经验）

- 每条 description 控制在 100-300 字符
- 必须保留**英文触发词**（如"DCF"、"sector rotation"、"limit-up"）
- 用单行引号格式 `description: "..."` 防止 `|` 解析问题
- 翻译完成后用 `yaml.safe_load` 双重验证

### 3.5 ASHARE_README.md 必备内容

```markdown
# A 股增强包（6 个 Skill）

> 对应 best_10 中 6 个美股 skill 的 A 股替代。

## 对应关系

| # | A 股 Skill | 替代的 best_10 # | 用途 |
|---|-----------|----------------|------|
| 1 | a-share-analysis | 04 company-valuation | A 股估值分析 |
| 2 | sector-rotation-detector | 05 sector-analyst | A 股板块轮动 |
| 3 | china-macro-analyst | 06 macro-rates-monitor | 中国宏观 |
| 4 | limit-up-pool-analyzer | 07 market-breadth-analyzer | A 股涨停广度 |
| 5 | equity-pledge-risk-monitor | 09 market-top-detector | A 股股权质押风险 |
| 6 | fund-screener | 10 institutional-flow-tracker | A 股公募基金 |

## 安装

unzip ashare_bundle.zip -d ~/.claude/skills/
```

---

## 4. Assumptions & Decisions

| 决策 | 选择 | 理由 |
|------|------|------|
| 是否替换 best_10 | **不替换**，并行新包 | 保留美股覆盖（H 股/美股联动仍有用） |
| A 股候选数量 | 1 对 1 共 6 个 | 用户确认 6 个精选 |
| 数据源优先级 | `yuping322 + nicepkg + sososun + longbridge` | 用户确认四个源 |
| 文件命名 | `A0N_xxx` 前缀 | 与 best_10 数字前缀区分 |
| 翻译策略 | 中文 description + 保留英文触发词 | 复用前文 best_10 经验 |
| 仓库克隆深度 | `--depth=1` | 节省空间，加快下载 |
| 失败回退 | 若 yuping322 仓库目录结构异常，回退到 longbridge-northbound-flow 等 | 见 §6 |

---

## 5. Verification Steps

执行完成后做 4 步验证：

1. **解压验证**：unzip -l ashare_bundle.zip 看是否含 6 个 A0N_*.zip 内层
2. **YAML 解析验证**：用 `yaml.safe_load` 测每个 SKILL.md 的 description 可读
3. **正则解析验证**：用 frontmatter 简单正则测 description 含中文且不含 `|`
4. **结构对比**：6 个 A 股 skill 字段对应正确（与 ASHARE_README.md 表对账）

预期输出示例（与前文 best_10 验证一致）：
```
A01_a-share-analysis.zip: 234 chars, 156 Chinese  OK
A02_sector-rotation-detector.zip: 187 chars, 124 Chinese  OK
A03_china-macro-analyst.zip: 165 chars, 102 Chinese  OK
A04_limit-up-pool-analyzer.zip: 201 chars, 143 Chinese  OK
A05_equity-pledge-risk-monitor.zip: 178 chars, 117 Chinese  OK
A06_fund-screener.zip: 213 chars, 168 Chinese  OK
TOTAL: 6 files | Regex OK: 6/6 | YAML OK: 6/6
```

---

## 6. Risk & Mitigation

| 风险 | 缓解 |
|------|------|
| `yuping322/finskills` 仓库可能已被作者删除/改名 | 备选 `nicepkg/ai-workflow` 内类似 skill |
| `sososun/mutual-fund-skills` 仓库可能不存在 | 备选 `yuping322/finskills@shareholder-structure-monitor` (23) |
| yuping322 仓库内 skill 目录结构不规范（如直接放根目录） | build_ashare.py 加 glob 兜底 |
| 中文翻译不准确 | 仅做最小化翻译（结构化字段如"宏观指标/板块/涨停"等术语稳定） |

---

## 7. 任务步骤清单（执行顺序）

| # | 步骤 | 工具 |
|---|------|------|
| 1 | git clone `yuping322/finskills` | RunCommand |
| 2 | git clone `sososun/mutual-fund-skills` | RunCommand |
| 3 | 6 个 skill 的 SKILL.md 路径 glob 验证 | Glob/Grep |
| 4 | 写 `build_ashare.py` | Write |
| 5 | 跑 `build_ashare.py` 生成 `_skills_ashare/` + `zips_ashare/` + `ashare_bundle.zip` | RunCommand |
| 6 | 写 `ASHARE_README.md` 对应表 | Write |
| 7 | 更新 `README.md` + `USAGE.md` 加 A 股路由 | Edit |
| 8 | 4 步验证 | RunCommand |
| 9 | 总结给用户 | text |

---

**版本**：v1.0 / 2026-06-13
**作者**：plan-mode 自动生成，待用户批准后执行
