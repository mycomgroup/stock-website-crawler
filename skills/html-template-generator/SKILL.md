# HTML Template Generator

## Metadata

- **Name**: html-template-generator
- **Version**: 1.1.0
- **Category**: Web Scraping / Data Extraction
- **Dependencies**: playwright, jsdom, xpath
- **Author**: Auto-generated skill
- **Status**: Production Ready

## Description

Automatically generates HTML extraction templates with XPath rules by analyzing sample web pages, and renders HTML content to Markdown using those templates. This skill bridges the gap between URL pattern identification and content extraction.

## Purpose

1. **Generate Templates**: Analyze sample pages and create XPath extraction rules
2. **Render Content**: Use templates to extract and render HTML to Markdown
3. **Human-in-Loop**: Support preview and confirmation workflow

## Workflow (⚠️ 需要人工确认)

### Phase 1: Generate and Test Single Template

生成单个模板并立即测试渲染效果，**必须人工确认**提取规则是否正确：

```bash
cd skills/html-template-generator

node scripts/generate-and-test.js <template-name> \
  --input ../../stock-crawler/output/lixinger-crawler/url-patterns.json \
  --output-dir ../../stock-crawler/output/lixinger-crawler/templates \
  --preview-dir ../../stock-crawler/output/lixinger-crawler/previews
```

**示例**:
```bash
node scripts/generate-and-test.js api-doc \
  --input ../../stock-crawler/output/lixinger-crawler/url-patterns.json \
  --output-dir ../../stock-crawler/output/lixinger-crawler/templates \
  --preview-dir ../../stock-crawler/output/lixinger-crawler/previews
```

**输出**:
- `templates/api-doc.json` - 生成的模板文件
- `previews/api-doc.md` - 渲染的预览 Markdown

**⚠️ 重要 - 请人工检查**:
1. 打开 `previews/api-doc.md` 文件
2. 确认内容提取是否完整
3. 检查表格、列表格式是否正确
4. 验证标题层级是否合理
5. **确认无误后才能进入 Phase 2**

### Phase 2: Batch Generation (确认后批量执行)

**仅在 Phase 1 确认无误后执行**，批量生成所有 106 个模板：

```bash
node scripts/batch-generate-templates.js \
  --input ../../stock-crawler/output/lixinger-crawler/url-patterns.json \
  --output-dir ../../stock-crawler/output/lixinger-crawler/templates
```

**可选参数**:
- `--start-from <n>` - 从第 n 个模式开始
- `--limit <n>` - 只处理 n 个模式
- `--headless false` - 显示浏览器窗口（调试用）

## Components

### 1. Template Generator (生成模板)
```bash
node run-skill.js <template-name> \
  --input <url-patterns.json> \
  --output <output-template.json>
```

### 2. Template Renderer (渲染 Markdown)
```bash
node scripts/test-render-template.js <template-file> <url> [output-file]
```

### 3. Generate and Test (生成+测试，推荐)
```bash
node scripts/generate-and-test.js <template-name> \
  --input <patterns-file> \
  --output-dir <templates-dir> \
  --preview-dir <previews-dir>
```

### 4. Batch Generator (批量生成)
```bash
node scripts/batch-generate-templates.js \
  --input <patterns-file> \
  --output-dir <templates-dir>
```

## Output Files

### Template JSON
```json
{
  "templateName": "api-doc",
  "version": "1.0.0",
  "generatedAt": "2024-01-15T10:30:00Z",
  "samples": ["https://example.com/page1"],
  "xpaths": {
    "title": "//h1/text()",
    "sections": {
      "xpath": "//div[@class='section']",
      "extract": {
        "heading": ".//h2/text()",
        "table": {
          "xpath": ".//table",
          "headers": ".//thead/tr/th/text()",
          "rows": ".//tbody/tr"
        }
      }
    }
  },
  "filters": {
    "removeXPaths": ["//nav", "//aside"]
  }
}
```

### Preview Markdown
```markdown
# 模板信息

- **模板名称**: api-doc
- **描述**: API文档页面
- **生成时间**: 2024-01-15T10:30:00Z

---

## 提取内容

### API Documentation

#### Parameters

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| api_key | string | Yes | Your API key |
```

## Best Practices

1. ✅ **先测试单个**: 使用 `generate-and-test.js` 生成第一个模板
2. 👁️ **人工确认**: 仔细检查 preview Markdown 文件
3. 🔧 **调整模板**: 如需要可手动编辑 template JSON
4. 🚀 **批量生成**: 确认无误后使用 `batch-generate-templates.js`

## Key Features

- **Automatic XPath Generation**: 基于元素属性生成稳定的 XPath
- **Frequency-Based Pattern**: 分析多个样本，选择 80%+ 出现的元素
- **Comprehensive Support**: 支持标题、表格、列表、代码块等
- **Intelligent Filtering**: 自动识别并过滤导航、广告等噪音
- **Browser Session Reuse**: 复用登录会话，访问需认证的页面
- **Markdown Rendering**: 将提取的内容渲染为格式化的 Markdown

## Documentation

- [README.md](README.md) - 完整文档
- [USAGE_GUIDE.md](docs/USAGE_GUIDE.md) - 使用指南
- [XPATH_GUIDE.md](docs/XPATH_GUIDE.md) - XPath 规则说明
- [FAQ.md](docs/FAQ.md) - 常见问题

## Version History

- **1.1.0** (2024): Added template rendering and preview workflow
  - Template renderer for HTML to Markdown conversion
  - Generate-and-test script for human-in-loop workflow
  - Preview Markdown generation
- **1.0.0** (2024): Initial release
  - Pattern reading, page fetching, structure analysis
  - XPath generation, template output
