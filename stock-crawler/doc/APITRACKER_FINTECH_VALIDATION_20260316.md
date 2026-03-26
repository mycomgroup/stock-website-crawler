# apitracker-fintech 抓取校验（2026-03-16）

> 2026-03-18 增量更新：已增强 `ApiTrackerParser`，补齐详情页关键字段，并再次进行多轮抓取与 Markdown 结构校验。

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

---

## 2026-03-18 增量复测（字段完整性 + MD 格式）

### 代码改动摘要
- 详情页新增字段抽取：`description`、`status`、`website/developer/apiReference/apiExplorer`、`terms/privacy`、`categories/products/apis/sdks` 等。
- 新增 `relatedLinks` / `notes`，统一输出关键信息，便于 Markdown 的“相关链接”“注意事项”区展示。
- `rawContent` 中补充 `pageData + apiSpecs + postmanCollections` 的结构化原始数据，保证可追溯性，尽量贴近网页原始数据（`__NEXT_DATA__`）。

### 多轮执行记录（2026-03-18）
- 第 1 轮：`pages-20260318-220727`（类目页）
- 第 2 轮：`pages-20260318-220758`（8 个详情页）
- 第 3 轮：`pages-20260318-221024`（8 个详情页）

### Markdown 格式校验
- 对以上三轮共 **17 个 md 文件**执行结构检查：
  - 必须包含 YAML frontmatter（起始 `---` 且存在结束分隔）
  - 必须包含 H1 标题
- 结果：`checked=17, badCount=0`，未发现格式损坏或结构缺失。

### 字段完整性抽样结论
- 抽样 `Blend_API_-_Docs,_SDKs_&_Integration_a.md`：
  - 已包含 `description`、`categories`、`products`、`website/developerPortal/terms/privacy`、`relatedLinks`。
  - `rawContent` 中包含完整 `pageData`（含 `technologies/customers/...`），与网页原始 JSON 保持一致性显著提升。

**更新结论**：
- 当前 `apitracker-fintech` 抽取结果已明显贴近网页原始结构；
- 关键字段缺失问题较 2026-03-16 版本显著收敛；
- 多轮产物的 Markdown 格式稳定，未出现结构性错误。
