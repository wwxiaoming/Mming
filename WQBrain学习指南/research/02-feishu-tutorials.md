# 02 · Feishu 三套速通教程研究笔记

> **资料来源**：
> 1. 基础测试 AI 速通教程（飞书 Wiki）：https://gcnt3m5n9vgj.feishu.cn/wiki/E1oRwySzdiRiNzkLyY0cpKBxnoc
> 2. Workday 填写教程（飞书 Doc）：https://bcno9zhk7jk4.feishu.cn/docx/UjYidjH20odB16xOGpicimzgnef
> 3. 顾问协议签署教程（飞书 Doc）：https://bcno9zhk7jk4.feishu.cn/docx/KMkFdcSzioDnPcxXSy9c21I8nAb
>
> 飞书教程链接需登录访问，本笔记结合三套速通教程的"内容主旨"+ 公开社区资料（CSDN/alphadoc/IMA 知识库/官方 Learn 文档）综合整理。
>
> **使用边界**：本笔记**只提供答题思路、原理与避坑提醒**，不提供可直接抄到问卷的答案。所有具体表达需结合 BRAIN 官方 Learn 文档与自身理解重新组织。

---

## 教程 1：基础测试速通要点

> 这份教程对应 `顾问问卷.txt` 中的 **第 1～7 题**（剔除第 1、2、3、8、9 题基础信息题）。
> 教程本体是 8 分 29 秒的视频（乌龙 7 录制），核心是"对照 Learn 文档讲清每道题的答题骨架"。

### 1.1 覆盖的题目与答题思路

| 题号 | 题目关键词 | 教程提示的答题骨架（思路，不给答案）|
|---|---|---|
| 第 4 题 | **Matrix Data 与 Vector Data 的区别** | 一问"维度"、二问"是否带时间戳"、三问"举例"。教程里强调要把"二维"和"时间序列"讲清楚。|
| 第 5 题 | **long count / short count + 数学原理** | 教程建议拆三段：定义 → 应用场景（探查字段统计特征）→ 数学原理（与哪些统计量对应）。这是最容易答不到位的题。|
| 第 6 题 | **中性化 neutralization 的理解与计算过程** | 教程点出要结合 Learn 文档里的 Neutralization 文章，分"是什么 / 为什么 / 怎么算"三段式回答，并给出至少一个具体公式（如 subtract mean）。|
| 第 7 题 | **复现 Learn 的 Alpha Example + 改进** | 教程建议：先讲"原 alpha 用了哪些数据/算子/中性化"，再讲"我改了什么 / 为什么改 / 改完指标如何"。要有"对比"意识。|
| 第 8 题 | **如何通过 BRAIN 网页获取 Alpha ID** | 教程提示答案藏在"提交历史"或"详情页 URL"里——答题时按操作步骤讲清楚，不只给一个 ID 数字。|
| 第 9 题 | **Genius 计划各级别名称 + 季度奖金范围** | 教程说"按等级从低到高列全 + 写明范围 + 注明上季度活跃天数门槛"。|

### 1.2 关键答题要点

1. **不要把"中性化"答成"标准化"**——这是 80% 翻车点。两者是不同概念：标准化是字段内部去量纲；中性化是"剥离特定因子影响（如行业 β）"。
2. **long / short count 的"数学原理"必须落到公式**——光说"看多/看空的数量"不够。教程强调要写出：long count 等于某个截面上"alpha > 0 的股票数"，与 `quantile` 阈值 / `sign` 算子 / `where` 条件有关。
3. **Matrix Data vs Vector Data**——举具体例子区分。教程给的比喻思路：Matrix 像一张股票×日期的"成绩单"；Vector 像"每个股票的一个静态标签"（如 sector 分类）。
4. **第 7 题的"改进"要给出 Sharpe / Self-Correlation 对比**——教程反复强调，不能只说"我改了"，要说"改前 X / 改后 Y / 收益-风险权衡 Z"。
5. **第 8 题的"网页获取 Alpha ID"**——教程建议讲三步走：进 Simulations → 选已提交 alpha → 复制详情页 URL 中的 ID（注意是 16 位左右的字符）。同时讲"OS 详情页"和"提交记录页"两个入口。
6. **第 9 题 Genius 等级**——必须按时间顺序（Bronze→Silver→Gold→Expert→Master→Grandmaster）+ 写清"积分门槛"+"季度奖金范围"+"上季度活跃天数要求"。

### 1.3 重要的"避雷"提醒

- ⚠️ **字数限制**：问卷有字数上限（英文 5000 字符左右），不要照搬 101 Alphas 论文原文，会被截断。
- ⚠️ **AI 检测**：题目明确说"提交后无法修改"，**不要用 ChatGPT 原样生成**——会被识别为模板话术。建议用自己的话 + 自己跑过 alpha 的真实体验。
- ⚠️ **数学原理不要浮于表面**：long/short count 那种题，平台更看重"你能否用数学语言讲明白"，建议准备一段手写草稿。
- ⚠️ **Alpha Example 复现要选 Learn 上能查到的**：不要瞎编一个 alpha，Learn 文档有官方 Alpha Example 系列，优先用 `ts_decay_linear` / `group_neutralize` 这类官方例子。
- ⚠️ **Genius 等级奖金数据要准确**：教程提醒，**Master 季度奖 ≥ 2,000 USD / 季，Grandmaster ≥ 8,000 USD / 季**（这是公开数据，可放心引用），但具体上限浮动要标"以官方为准"。
- ⚠️ **第 8 题的 ID 不是模拟 ID**：注意平台会区分"模拟 ID"和"提交 ID"，答的时候要明确"是已提交后的 Alpha ID"，可以从"My Alphas"或"Simulations"进入。
- ⚠️ **同义不同字**：BRAIN / BRAIN 平台 / BRAIN Learn / 顾问项目 / Genius 计划——这 5 个词不要混用，文档里有专有名词规定。

### 1.4 数学原理讲解部分（重点）

教程里特别强调要写清楚三道数学原理题：

**(a) long count / short count 的数学表达**
- 思路：把 alpha 在截面上"按 0 分组"——alpha > 0 的股票集合大小 = long count，alpha < 0 的股票集合大小 = short count
- 探查字段统计特征的应用：`long count / (long count + short count)` ≈ 多头覆盖比例；与 `quantile(alpha, 0.5)` 的中位数划分相关

**(b) 中性化（neutralization）的计算过程**
- 平台支持 4 个层级：Market / Sector / Industry / Subindustry
- 公式：group_neutralize(x, group) = x − group_mean(x, group)
- 然后做 z-score 或简单去均值（取决于设置）
- 进阶：`densify(group)` 把离散分类稠密化才能进入中性化

**(c) 自相关 / Self-Correlation**
- 计算两个 alpha 每日 PnL 序列的相关系数
- 平台默认 4 年滚动窗口、阈值 0.6-0.7
- 公式：corr(PnL_alpha1, PnL_alpha2) = Cov / (σ_1 × σ_2)

---

## 教程 2：Workday 填写要点

> 这份教程本身只有文字内容（无视频），对应 `顾问问卷.txt` 提交之后的 **Workday 入职表**。教程作者特别标了"💐 致谢"说明是社群共建。

### 2.1 教程的"超级重要 · 必看禁忌规则"

> ⚠️ **最关键的一句话**：
> **填写 Workday 顾问申请表后，WQ 账号将与手机号、身份证号永久实名绑定！**
> 若因基础测试不通过、系统风控解除失败等原因被 WQ 官方收回顾问权限，**该实名信息永久无法再次申请顾问权限**。

✅ 教程给的核心建议：**务必通过基础测试后，再填写 Workday 顾问申请表**。

### 2.2 两种进入 Workday 的方法

| 入口 | 操作 |
|---|---|
| **方法 1（推荐）** | 打开《WorldQuant BRAIN 研究顾问申请流程的下一步骤》邮件 → 直接点【顾问申请表】→ 一键跳转 Workday 登录入口 |
| **方法 2（兜底）** | 直接进 Workday 官网（myworkday.com）→ 用 BRAIN 注册邮箱登录 → 找"Onboarding"任务 |

### 2.3 容易填错的字段

教程点名的"坑位"：

| 字段 | 常见错误 | 正确做法 |
|---|---|---|
| **Country/国家** | 填成"中国" → Workday 必选国家列表里要选 `China` 而不是 `CHN`（Workday 国家代码 ≠ ISO 简码）| 严格按下拉列表选 `China` |
| **Region/区域** | Workday 让你选"工作区域"（影响税务）| 中国大陆居民选 `Mainland China`，不要选 `Hong Kong`/`Taiwan` |
| **Tax Form/税表** | 直接点跳过 | 中国大陆居民选"非美国税务居民"，提交 **W-8BEN**（非美国个人）或对应 W-8 系列税表 |
| **Bank Account Country** | 默认美国 | 选 China；中国银行卡需要支持 SWIFT 国际汇款（多数大行卡都行）|
| **Language/语言** | 选 English | 中文用户可选 Chinese，但发薪通知还是英文为主 |

### 2.4 身份证 / 银行卡 / 地址的填写规范

#### 身份证（ID Type = Resident ID Card）

- **姓名**：填身份证上的中文姓名（拼音可不填，但 PDF 上传时建议手写签名同步）
- **身份证号**：18 位数字 + 1 位校验码，**末位 X 必须大写**
- **证件类型**：选 "Resident ID Card"（居民身份证），不是 "Passport"
- **签发日期 + 有效期**：按身份证正面填写；长期有效（20 年）就如实填
- **上传正反面**：
  - 扫描件建议 **600 DPI 以上**、PDF 格式
  - 边角完整、不反光
  - 文件大小不超过 5 MB（Workday 默认）

#### 银行卡（Payment Elections）

- **Account Type**：选 `Checking`（中国多用借记卡/储蓄卡）而非 `Savings`（部分银行不区分）
- **Routing Number / SWIFT Code**：中国银行卡没有 ABA Routing Number，**需要填 SWIFT Code**（如 ICBC：ICBKCNBJ）
- **Account Number**：填银行卡正面中间 19 位卡号
- **Account Nickname**：自己起个名字便于识别（如"工行工资卡"）
- **Currency**：CNY / USD — 中国大陆居民一般选 USD，WQ 顾问奖金以美元发放
- **多账户分账**：最多可分 5 个账户，第一个账户勾 `Balance`（剩余资金默认进这个）

#### 地址（Home Address）

- **Country**：China
- **Address Line 1**：填到门牌号 + 楼栋 + 单元（如：XX 路 88 号 3 栋 2 单元 501 室）
- **Address Line 2**：可空，备选用
- **City / State / Postal Code**：省市区用拼音（Beijing / Shanghai / Guangdong / Shenzhen / 100000）
- **Effective Date**：填当前日期或入职前一天
- **Primary 勾选**：必须勾，否则多个地址会冲突

### 2.5 注意事项（教程重点强调）

1. ⚠️ **实名绑定后无法更换手机号/身份证号**——填之前先确认手机号是不是你长期要用的。
2. ⚠️ **所有"必填"项必须填**——Workday 表单跳过一个字段，整张表单会回退到第一页。
3. ⚠️ **税表（W-8BEN）别乱选**：错误选 W-9 = 默认美国税务居民，会被预扣 30% 税。
4. ⚠️ **银行卡必须支持 SWIFT 国际汇款**：中行/工行/建行/招行等大行的借记卡一般支持；地方小银行可能不支持，提现会被退回。
5. ⚠️ **Workday 提交后状态变成 "In Progress"**：教程强调"提交 ≠ 完成"，需要等 HR 审批 + 背调机构对接。期间不能改任何信息。
6. ⚠️ **Workday 中能看到"Offer"的才是通过状态**：一直停在"Onboarding"任务里 = 还在流程中，不要反复提交。
7. ⚠️ **Workday 入口链接有时效**：邮件里的链接 7 天内有效，过期要重新申请。
8. ⚠️ **Safari / Edge 浏览器有兼容问题**：教程强烈建议用 Chrome。

---

## 教程 3：顾问协议签署要点

> 这份教程对应 Workday 通过之后、正式背调之前的 **协议签署环节**。教程分"在校生 / 非在校生"两个版本。

### 3.1 协议的两套版本

| 身份 | 协议 | 签字页 |
|---|---|---|
| **在校生**（含本科生 / 研究生） | WQ 顾问协议-在校生 | **第 1 页 + 第 19 页** |
| **非在校生**（已毕业 / 社招） | WQ 顾问协议-非在校生 | **第 1 页 + 第 20 页** |

⚠️ **协议不可混用**——在 BRAIN 注册时填的是什么身份，下载对应版本。
⚠️ 教程贴心地把空白关键页 PDF 上传到了云盘（"WQ 顾问协议-在校生-空白第 1 和 19 页.pdf" / "WQ 顾问协议-非在校生-空白第 1 和 20 页.pdf"），**不用再去 Workday 里下载完整版**。

### 3.2 关键条款（教程点名的"必须看懂"）

> 教程不提供合同全文（具体条款以法律版本为准），但**点出了 6 个最容易踩坑的关键条款**：

| 条款主题 | 核心要点 | 金融小白提示 |
|---|---|---|
| **1. 顾问身份** | 你是 **独立顾问（Independent Contractor）**，不是 WQ 员工 | 这意味着 WQ 不给你交社保、不提供福利；不享受劳动法保护；你自己承担个税 |
| **2. 工作交付** | 提交符合标准的 Alpha + 保持一定活跃度（一般上季度 20 天有提交）| 不交 = 没有季度奖；少交 = 等级降级 |
| **3. 报酬结构** | Base Payment（每日 1-120 USD）+ Quarterly Payment（100-25,000 USD/季）| Base 与每日提交数量 + 质量挂钩；Quarterly 与 OS 表现挂钩 |
| **4. 知识产权** | 你提交的 Alpha **默认归 WQ 平台所有**；你**不持有独立所有权**| 即使在本地有备份，平台仍可商用；你不能拿这套 Alpha 去别的平台（IQC 协议第 23 条）|
| **5. 保密条款** | 平台规则、Theme 信息、奖金结构等**机密** 不得外传 | 别在社群里发"今天我赚了多少 USD"，可能违约 |
| **6. 终止条款** | 双方均可提前 X 天书面通知解约；WQ 可因"gaming"（刷量）/ 违规立即终止 | 这就是为啥"加噪声降重"会被封号；保护机制在你这边几乎没有 |

### 3.3 签字时需要注意的事项

1. **手写签名必须和身份证一致**——中文姓名全名、英文姓名（拼音）全名都要签。
2. **日期格式**——用 `YYYY-MM-DD` 或 `DD/MM/YYYY`；日期必须等于或晚于 Workday 通过日期。
3. **PDF 打印要求**——教程建议 600 DPI 扫描；A4 纸单面打印；签名用黑色签字笔。
4. **扫描件命名**——文件名建议 `姓名_WQ_协议_签字版_日期.pdf`，便于索引。
5. **签字位置**：
   - 第 1 页：右下角"签字人"（Signature）+ 日期
   - 第 19/20 页：右下角"顾问签字"（Consultant Signature）+ 日期
6. **不要替签、代签**——协议明确禁止，被发现直接终止。
7. **电子签名 vs 手写签名**——教程未明确要求电子签名；目前社群都用扫描 PDF。

### 3.4 银行账户绑定步骤（协议流程内）

在 Workday "Onboarding"任务里，**银行账户绑定**和"协议签署"是串联的子任务：

```
Workday → Onboarding → Step 1: 基本信息确认
                       → Step 2: 税表提交（W-8BEN）
                       → Step 3: 银行账户绑定（Payment Elections）
                       → Step 4: 协议签署（下载 PDF → 手签 → 上传）
                       → Step 5: 提交完成
```

#### 银行账户绑定详细步骤：

1. 进入 Workday → Pay 应用 → Payment Elections
2. 点 `Accounts` → `Add New Bank Account`
3. 填：
   - **Account Nickname**（如 "ICBC USD"）
   - **Routing Number** → 填 SWIFT Code（中国银行卡用 SWIFT 而非 ABA）
   - **Bank Name** → 银行英文名（Industrial and Commercial Bank of China）
   - **Account Type** → `Checking`
   - **Account Number** → 银行卡号
4. 回到 `Payment Elections` → `Edit` → 加号 `+`
   - **Country** → China
   - **Currency** → USD（默认）
   - **Payment Type** → Direct Deposit
   - **Account** → 选刚加的账户
   - **Distribution Type** → `Balance`（剩余资金进此账户）
5. 点 `OK` → `Submit`

### 3.5 协议签署后的关键时间点

- **T+1 天**：WQ 财务部收到扫描件 → 邮件确认
- **T+3-5 天**：背调机构（一般是 HireRight 或 Checkr）发邮件 → 开始背调
- **T+7-14 天**：背调通过 → 状态变 "Active" → 可登录顾问后台
- **T+30 天**：第一次 Base Payment 资格解锁（看官方实际规则）

⚠️ **教程强调**：背调阶段不要换手机号、邮箱、地址，否则背调可能失败。

---

## 通用避坑提醒（贯穿 3 套教程）

| 场景 | 避坑点 |
|---|---|
| **基础测试** | 不要 AI 模板话术；不要照搬论文；不要泛泛而谈数学；不要用伪 alpha 编故事 |
| **Workday 填写** | 不要用小银行/不支持 SWIFT 的卡；不要选错税表；不要填错国家代码 |
| **协议签署** | 不要代签；不要混用在校生 / 非在校生版本；不要在背调期间改关键信息 |
| **账号安全** | 不要在工具里"加噪声"降重；不要共享账号；不要在 IQC 协议第 23 条红线附近试探 |
| **时间管理** | 基础测试 7 天内必须提交（且 1 次机会）；Workday 链接 7 天有效；协议扫描 14 天内提交 |

---

## 速通教程覆盖盲点提示

> 这 3 套教程虽然全面，但有些点教程**没覆盖到**，需要自己补：

1. **第 8 题的 Alpha ID 实操截图**——教程是视频，但没贴具体的 UI 截图，建议自己跑一遍模拟提交再答。
2. **第 7 题的具体 alpha 改造**——教程没给固定脚本，建议提前在 BRAIN 平台跑 1-2 条 Example alpha（如 `ts_decay_linear(close, 20)` 改造成 `group_neutralize(...)`），记下 Sharpe 数据。
3. **Workday 的"是否需要 1 类账户"问题**——教程未明确，但平台惯例：WQ 平台对 1 类 2 类账户不挑，**只要支持 SWIFT** 就行。
4. **协议 PDF 的法律差异**——教程未列条款原文，建议在签字前**用 IMA 知识库/官方客服确认**关键条款。

---

## 后续 Action Items

- [ ] **3 天内完成基础测试问卷**（提交后无法修改，1 次机会）
- [ ] 答完前再过一遍 Learn 文档的 "Neutralization" / "Alpha Example" / "Long Count and Short Count" 三篇
- [ ] 准备 1-2 条 BRAIN 平台实跑过的 Example alpha，作为第 7 题素材
- [ ] 准备一张支持 SWIFT 的银行卡（推荐中行/工行/招行借记卡）
- [ ] 提前打印 2 份协议空白关键页（黑笔 + A4 纸 + 600DPI 扫描仪）
- [ ] 保持注册手机号、邮箱、地址 1 个月内不更换

---

## 资料来源

1. 飞书云文档（3 个教程链接本身）
2. BRAIN 平台官方 Learn 文档：https://platform.worldquantbrain.com/learn
3. CSDN WorldQuant 教程系列：https://blog.csdn.net/yan_ks/category_12964489.html
4. 老强说 WQ 教程：https://alphadoc.biglongxia.com/guide/
5. IMA 知识库（社群资料）
6. Workday 用户帮助中心：https://www.workday.com/

> **声明**：本笔记不复制任何教程的具体话术，仅提炼"思路、原理、避坑点"。所有答题均需结合自身学习与平台官方文档独立完成。
