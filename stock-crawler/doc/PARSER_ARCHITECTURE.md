# 解析器架构文档（系统化分类与分层解析方案）

## 1. 背景与目标

当前解析能力已经覆盖了若干页面类型（如文章页、API 文档页、表格页、通用页），但仍存在以下问题：

- 解析入口以 URL 规则为主，页面语义识别能力不足。
- 页面类型定义较粗，列表页/目录页/正文页等边界不清晰。
- 不同解析器之间缺少统一的“分类 -> 策略 -> 抽取 -> 质量评估”闭环。
- 新站点接入时容易“临时加 parser”，架构逐步分散。

**目标**：建立“先分类、后解析、可回退、可评估、可扩展”的系统化解析框架，使 parser 从“散点规则”升级为“标准流水线”。

---

## 2. 调研结论（面向网页抽取的常见方法）

### 2.1 行业常见范式

网页内容抽取通常采用三段式：

1. **页面分类（Page Typing）**：先判断是列表/目录/正文/混合等。  
2. **模板或策略匹配（Strategy Selection）**：按类型进入对应解析策略。  
3. **结构化抽取（Structured Extraction）**：输出统一 schema，并做质量评分。

在工程实践中，最稳妥的方式不是单一模型，而是：

- **规则优先 + 统计特征兜底 + 通用解析回退**。
- 先用轻量特征快速分类，再进入专用 parser。
- 失败时统一降级到 GenericParser，保证可用性。

### 2.2 对本项目的启发

结合当前代码现状（已有 `CoreContentParser`、`ApiDocParser`、`TableOnlyParser`、`GenericParser`），最适合演进为：

- 从“按 URL 匹配 parser”升级为“按页面类型路由 parser”。
- URL 规则继续保留，但仅作为分类特征之一。
- 在解析前增加统一的页面特征提取层（DOM + 文本 + 链接 + 表格 + 交互控件）。

---

## 3. 系统化页面分类体系（推荐）

建议将页面分为 **L0 大类 + L1 子类**。

### 3.1 L0 大类

1. **导航类页面（Navigation-like）**
   - 列表页（List）
   - 目录页（Directory/Index）
   - 聚合页（Portal/Hub）

2. **内容类页面（Content-like）**
   - 文章正文页（Article）
   - 文档正文页（Doc）
   - 公告/资讯正文页（News/Notice）

3. **数据类页面（Data-like）**
   - 大表格正文页（Table-centric）
   - 指标看板页（Dashboard）
   - API 文档页（API Doc）

4. **功能类页面（Functional-like）**
   - 登录/注册页（Auth）
   - 查询/筛选页（Search/Form）
   - 下载中转页（Download/Redirect）

### 3.2 L1 关键子类定义（首批建议）

为满足你提到的“列表页、目录页、正文页（含表格/纯文）”场景，第一阶段建议重点支持以下 6 类：

- `list_page`：条目重复结构明显，链接密度高，常有分页。
- `directory_page`：层级导航明显，目录树或分类入口多。
- `article_page`：长段落文本为主，语义连续。
- `table_content_page`：主内容为 1 个或多个核心数据表。
- `api_doc_page`：请求地址、方法、参数、示例等模式明显。
- `generic_page`：无法高置信归类时的兜底类型。

---

## 4. 分类特征设计（Feature Set）

分类器不依赖单一信号，建议综合以下特征：

### 4.1 URL 与路由特征

- 路径关键词：`/api/`, `/doc/`, `/news/`, `/list/`, `/detail/` 等。
- 参数模式：`page=`, `id=`, `category=`。
- 路径深度与数字片段比例。

### 4.2 DOM 结构特征

- 文本块数量与平均长度（`p`、`li`、`h1-h4`）。
- 表格数量、行列规模、表头占比。
- 重复卡片/列表项结构（同类节点重复度）。
- 表单控件密度（`input/select/button`）。

### 4.3 文本语义特征（轻量规则）

- API 关键词：请求方式、参数说明、响应示例等。
- 新闻关键词：发布时间、来源、责任编辑等。
- 数据表关键词：单位、同比、环比、代码、简称等。

### 4.4 链接与交互特征

- 链接密度（link text / total text）。
- 站内链接占比、出站链接占比。
- 分页控件、Tab、展开按钮数量。

---

## 5. 统一解析流水线（核心设计）

推荐新增统一 pipeline：

1. **Page Snapshot**：采集页面快照与基础统计（轻量 evaluate）。
2. **Page Classification**：输出 `type + confidence + reasons`。
3. **Parser Routing**：根据类型路由到专用 parser。
4. **Content Extraction**：执行类型化抽取。
5. **Quality Scoring**：质量评分（完整性、噪声比、字段覆盖率）。
6. **Fallback**：低分或异常时降级到 `GenericParser`。

可表达为：

```
PageParser
  -> FeatureExtractor
  -> PageClassifier
      -> ParserRouter
          -> {ListParser | DirectoryParser | ArticleParser | TableContentParser | ApiDocParser | GenericParser}
  -> ResultValidator
  -> MarkdownGenerator
```

---

## 6. Parser 设计规范（统一接口）

建议所有 parser 输出统一元数据，避免后续处理分叉：

```js
{
  type: 'article_page',
  subtype: 'news_article',
  confidence: 0.87,
  url: '...',
  title: '...',
  content: {...},
  meta: {
    classifierReasons: [...],
    extractionScore: 0.82,
    parserVersion: 'v2'
  }
}
```

### 6.1 必须统一的方法

- `canHandle(classification)`：是否处理该类型。
- `parse(page, context)`：执行抽取。
- `validate(result)`：字段完整性与噪声检查。
- `toMarkdown(result)`（可选）：特殊类型的 markdown 渲染。

### 6.2 建议的基础 parser 分工

- `ListParser`：抽取列表项、链接、时间、分页关系。
- `DirectoryParser`：抽取层级目录树、栏目入口、映射关系。
- `ArticleParser`：抽取标题、时间、作者、正文块、附件。
- `TableContentParser`：抽取主表、字段映射、单位与注释。
- `ApiDocParser`：保留并继续增强。
- `GenericParser`：兜底与异常场景。

---

## 7. 与现有代码的映射与改造建议

当前已有 parser 可以直接映射：

- `CoreContentParser` -> `ArticleParser`（可作为文章正文主干）。
- `TableOnlyParser` -> `TableContentParser`（增强为“表格正文页”而非仅 URL 规则）。
- `ApiDocParser` -> 保留。
- `GenericParser` -> 保留兜底。

### 7.1 第一阶段（低风险）

- 保持 `ParserManager` 主体不变。
- 新增 `PageClassifier`，先给 `selectParser()` 提供 `classification`。
- parser 继续支持 URL 匹配，同时增加基于 `classification` 的匹配。

### 7.2 第二阶段（结构升级）

- `ParserManager` 从“URL 匹配优先”改为“分类路由优先”。
- 增加 `ListParser`、`DirectoryParser`。
- 增加 `ResultValidator` 统一打分与回退策略。

### 7.3 第三阶段（质量闭环）

- 记录每页分类结果与最终解析器命中情况。
- 对低分页面自动打标（便于后续规则优化）。
- 基于日志进行类型误判分析与特征迭代。

---

## 8. 分类决策示例（规则版）

可先采用可解释规则，后续再逐步引入学习策略：

```text
if api_keywords_score >= 0.7 -> api_doc_page
else if table_density >= 0.45 and main_table_rows >= 8 -> table_content_page
else if paragraph_count >= 5 and avg_paragraph_len >= 80 and link_density < 0.3 -> article_page
else if repeated_item_blocks >= 10 and pagination_detected -> list_page
else if nav_tree_depth >= 3 and category_links >= 15 -> directory_page
else -> generic_page
```

---

## 9. 输出 Schema 建议（按类型）

### 9.1 列表页

- `items[]`: `title`, `url`, `summary`, `date`, `tags`
- `pagination`: `current`, `next`, `totalPages?`
- `listMeta`: 列表模板特征、去重 key

### 9.2 目录页

- `tree`: 层级节点（`name`, `url`, `children[]`）
- `directoryMeta`: 最大层级、覆盖栏目数

### 9.3 文章页

- `article`: `title`, `publishTime`, `author`, `blocks[]`, `attachments[]`
- `contentText`: 合并后的纯文本正文

### 9.4 表格正文页

- `tables[]`: `caption`, `headers[]`, `rows[]`, `unit`, `notes`
- `tableMeta`: 主表识别得分、字段标准化映射

---

## 10. 验收指标（Definition of Done）

系统化方案落地后，建议以以下指标验收：

- 分类准确率（抽样标注）：`>= 85%`。
- 关键类型召回率（article/table/api）：`>= 90%`。
- 兜底 parser 占比持续下降。
- Markdown 可读性评分提升（标题层级、表格完整率）。
- 低质量解析页可定位（日志包含分类原因与失败原因）。

---

## 11. 结论

“先分类，再按类型解析”是将 parser 体系从零散规则升级为工程化能力的关键。  
对于当前项目，建议以 **分类器 + 路由器 + 类型化 parser + 质量回退** 为核心架构，分三阶段渐进落地：

1. 先接入分类结果，不破坏现有流程。
2. 再补齐列表页/目录页 parser，并把路由主导权切到分类器。
3. 最后通过质量评分与日志闭环持续优化。

该方案可在保持现有稳定性的同时，显著提升可扩展性与解析一致性。
