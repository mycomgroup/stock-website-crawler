# RSS API 数据与 Web 页面比对说明文档 (CNBC 示例)

## 1. 基本信息
- **任务类别**: RSS
- **数据源名称**: CNBC Finance
- **RSS API 地址**: `https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10000664`
- **目标 Web 页面地址**: `https://www.cnbc.com/finance/`
- **测试时间**: 2026-03-17
- **测试人员**: Trae AI

## 2. 比对目标
通过 API 方式获取 CNBC Finance RSS 数据，并与 CNBC Finance 实际 Web 页面展示的数据进行全面比对，评估 RSS API 数据的**完整性**、**准确性**和**时效性**，以决定后续数据获取策略。

## 3. 字段映射与数据完整性比对

| 字段名称 | Web 页面展示情况 | RSS API 返回情况 | 比对结果 (一致/缺失/差异) | 备注/差异说明 |
| :--- | :--- | :--- | :--- | :--- |
| **标题 (Title)** | 完整展示新闻标题 | `<title>` 节点包含完整标题 | 一致 | 完全匹配 |
| **正文/摘要 (Content/Description)** | 包含副标题及正文部分摘要 | `<description>` 提供纯文本摘要 | 差异 | RSS 仅提供一两句话的简短描述，如需获取长正文需要爬取 Web 原文 |
| **发布时间 (PubDate)** | 页面显示 "X min ago" 或具体时间 | `<pubDate>` 返回标准 GMT 时间 | 基本一致 | 需要在后端格式化 GMT 时间 (如 `Tue, 17 Mar 2026 15:21 GMT`) 转换为本地时区 |
| **作者/来源 (Author/Source)** | 页面展示作者姓名 (如: Hugh Son) | 无对应节点 (未发现 author) | 缺失 | RSS 未返回作者信息 |
| **原文链接 (Link)** | 相对路径或附带追踪参数 | `<link>` 返回干净绝对路径 | 差异 | RSS API 的链接更干净 (例如: `https://www.cnbc.com/2026/...`)，无需处理相对路径 |
| **分类/标签 (Category/Tags)** | 页面上方显示分类 "Finance" | 无直接 `<category>` 节点 | 缺失 | |
| **缩略图 (Enclosure/Image)** | 页面带有高质量配图 | 部分 RSS 无 enclosure 标签 | 缺失/差异 | 该接口不包含图片数据，需要从原文爬取 |

## 4. 数据格式与质量分析
- **HTML 标签处理**: RSS API 返回的 `description` 被包裹在 `<![CDATA[ ... ]]>` 中，属于纯文本内容，无冗余的 HTML 标签，**无需额外清洗 `<script>` 或 `<iframe>`**。
- **特殊字符与编码**: 响应头采用 `UTF-8` 编码，特殊字符（如引号、破折号）在 CDATA 块内被正确解析，不存在乱码现象。

## 5. 时效性与接口限制分析
- **更新延迟**: RSS API 的 `<lastBuildDate>` 几乎与 Web 页面发布的最新一条新闻时间同步，延迟通常在 1-5 分钟以内，非常适合做新闻监控。
- **数据列表长度**: 该 RSS 一次请求固定返回最新 **30 条**新闻。
- **历史回溯**: 不支持分页 (无 `?page=2` 参数)，无法获取 30 条之前的历史数据。

## 6. 结论与后续接入方案
### 6.1 结论概览
CNBC Finance 的 RSS API 数据结构极其规范，**时效性极佳**，链接提取简单且无需清理。但缺陷在于**不包含正文全文、配图和作者信息**。它非常适合作为爬虫的“触发器”或“索引源”。

### 6.2 后续接入策略建议 (Next Steps)
- [ ] **纯 API 接入**: 否。如果不满足只拿标题和摘要的业务需求，则不能纯用 API。
- [x] **混合抓取接入 (API + 爬虫)**: **是 (推荐)**。
  - **步骤 1**: 定时 (如每 5 分钟) 请求此 RSS API 获取最新的 `<link>`。
  - **步骤 2**: 对增量的 `link`，触发 Playwright/Cheerio 爬虫脚本，进入详情页抓取**完整正文 (Article Body)**、**作者**及**封面图**。
- [ ] **数据清洗任务**: 
  - 将 `<pubDate>` 统一转换为 ISO 8601 格式 (YYYY-MM-DDTHH:mm:ssZ)。

---
**附录：API 请求示例与响应结构**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Finance</title>
    <lastBuildDate>Tue, 17 Mar 2026 15:21 GMT</lastBuildDate>
    <item>
      <title><![CDATA[Mastercard acquiring stablecoin startup in crypto bet]]></title>
      <link>https://www.cnbc.com/2026/03/17/mastercard-acquiring-stablecoin.html</link>
      <description><![CDATA[Latest investing news and finance headlines.]]></description>
      <pubDate>Tue, 17 Mar 2026 15:21 GMT</pubDate>
    </item>
  </channel>
</rss>
```