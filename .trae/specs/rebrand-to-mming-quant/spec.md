# 改名 Mming 量化 + 优化 Spec

## Why
`/workspace/index.html` 当前是"小宇量化"品牌的资金流向工具页面(带推广 banner、微信二维码、外部链接),需要把它改造成"Mming 量化"白标版本:替换品牌名,优化 fetch 路径(改用相对路径走 Codespaces 反向代理),并清理已不适用的外部推广内容。

## What Changes
- **BREAKING**: 替换所有页面文案中的"小宇量化"为"量化系统"
- **BREAKING**: 替换所有页面文案中的"小宇量化系统"为"Mming 量化"
- 优化:两处 `fetch('http://localhost:8180/...')` 改为相对路径 `/api/plugin/...`(走 server.py 反向代理,解决 iPad/Codespaces 跨域)
- 删除/简化:小宇量化的推广 banner(WeChat 二维码、jzhu.net 链接、客服信息)
- 标题、页脚等用户可见文案中"小宇量化"相关字样全部清除或改为"Mming 量化"

## Impact
- Affected specs: 无
- Affected code: `/workspace/index.html`(单文件,纯前端,无其他依赖)

## ADDED Requirements

### Requirement: 品牌替换为 Mming 量化
The page SHALL 在用户可见的所有位置(标题、页脚、推广 banner 等)将"小宇量化"替换为"量化系统"、"小宇量化系统"替换为"Mming 量化"。

#### Scenario: 用户打开页面
- **WHEN** 用户在浏览器打开 `/workspace/index.html`
- **THEN** 页面标题(浏览器标签)、`<title>`、`<h1>`、banner、页脚中**不出现**"小宇量化"四个字
- **AND** banner 中出现的品牌名为"Mming 量化"

### Requirement: 移除小宇量化专属推广内容
The page SHALL 不再展示小宇量化的微信二维码、客服微信号、jzhu.net 外部下载链接。

#### Scenario: 页面加载完成
- **WHEN** 用户加载页面
- **THEN** 页面中**不出现**:`XYLH8338` 微信号、jzhu.net 链接、小宇量化专属的微信二维码图

### Requirement: 优化 API 调用走相对路径
The page SHALL 使用相对路径 `/api/plugin/...` 调用后端,**不再硬编码** `http://localhost:8180`。

#### Scenario: 用户点查询按钮
- **WHEN** 用户在 iPad Safari / Codespaces 转发 URL 中点查询
- **THEN** fetch 走相对路径,请求落在 server.py 的反向代理上,绕过 CORS

## MODIFIED Requirements

### Requirement: 页脚说明
原页脚"数据都来自你本机的行情服务" — 保留这一句(仍然成立),但去掉"小宇量化"相关指代。

#### Scenario: 滚动到页脚
- **WHEN** 用户滚到页脚
- **THEN** 出现类似"数据来自本机的量化系统(8180 端口),不上传、不外发"的描述
- **AND** 不出现"小宇量化"字样

## REMOVED Requirements

### Requirement: 小宇量化推广 banner
**Reason**: 品牌已变更为 Mming 量化,小宇量化的推广内容不再适用
**Migration**: 整个 `.xy-ad` 区块删除,不留痕迹

### Requirement: 微信客服联系方式
**Reason**: 原 WeChat 联系方式属于"小宇量化"作者,白标后不应保留
**Migration**: 整个 `.xy-ad-contact` 子区块删除
