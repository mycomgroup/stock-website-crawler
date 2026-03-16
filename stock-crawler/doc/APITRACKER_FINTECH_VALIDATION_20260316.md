# apitracker-fintech 抓取校验（2026-03-16）

## 执行情况

- 已运行 `config/apitracker-fintech.json` 超过 10 轮：
  - 前置轮次：`pages-20260316-195551`、`pages-20260316-195612`、`pages-20260316-195845`、`pages-20260316-200117`
  - 补充轮次：`pages-20260316-200214`、`pages-20260316-200447`、`pages-20260316-200719`、`pages-20260316-200955`、`pages-20260316-201230`、`pages-20260316-201503`、`pages-20260316-201735`

## Markdown 结构检查

抽样文件：
- `output/apitracker-fintech/pages-20260316-201735/Fintech_APIs.md`
- `output/apitracker-fintech/pages-20260316-201735/PayPal_API_-_Docs,_SDKs_&_Integration_a.md`
- `output/apitracker-fintech/pages-20260316-201735/Bankin'_API_-_Docs,_SDKs_&_Integration_a.md`

结论：
- Markdown 结构整体**清晰**，标题层级稳定（H1 + H2/H3），段落和列表未出现明显错乱。
- 链接列表采用编号格式，可读性良好。
- 特殊字符（如 `Bankin'`）在标题和正文中渲染正常。

## 与原网页信息对比（是否缺失）

### 类目页（`/categories/fintech`）
- MD 中保留了：
  - 页面标题
  - 源 URL
  - 分类名
  - 入口数量
  - 入口列表（公司名 + 详情页链接）
- 该页目标信息以目录列表为主，MD 保留度较高。

### 详情页（`/a/paypal`）
- MD 中目前保留了：
  - 标题
  - 源 URL
  - 公司名、slug
  - 文档入口（doc links）
  - URL include/exclude 建议
- 相比原始页面（`__NEXT_DATA__` 中 `pageData`）有明显信息缺失，示例包括：
  - `description`
  - `websiteUrl` / `developerPortalUrl` / `apiReferenceUrl`
  - `apiBaseEndpoint` / `graphqlEndpoint`
  - `categories`
  - `products`
  - `statusUrl` / `privacyUrl`
  - `apis` / `sdks` 等结构化字段

**综合判断**：
- Markdown 格式没有明显“乱掉”；结构段落清晰。
- 但详情页内容抽取偏保守，存在较多字段缺失（尤其是描述、链接生态、状态与隐私链接、产品和技术字段等）。
