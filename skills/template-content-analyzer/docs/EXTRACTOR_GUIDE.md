# 提取器配置指南

## 概述

提取器（Extractor）定义了如何从页面中提取特定类型的数据。每个提取器针对一个数据字段，使用CSS选择器定位元素，并根据类型执行相应的提取逻辑。

## 提取器结构

```typescript
interface Extractor {
  field: string;             // 字段名（必需）
  type: string;              // 提取器类型（必需）
  selector: string;          // CSS选择器（必需）
  required?: boolean;        // 是否必需（可选，默认false）
  pattern?: string;          // 匹配模式（可选）
  columns?: string[];        // 表格列名（table类型专用）
}
```

## 字段说明

### field (必需)
- **类型**: `string`
- **说明**: 提取数据的字段名，将作为结果对象的属性名
- **命名规范**: 使用驼峰命名法，如 `title`, `mainTable`, `apiExamples`
- **示例**: `"field": "title"`

### type (必需)
- **类型**: `string`
- **说明**: 提取器类型，决定如何处理选中的元素
- **有效值**: `text`, `table`, `code`, `list`
- **示例**: `"type": "text"`

### selector (必需)
- **类型**: `string`
- **说明**: CSS选择器，用于定位页面元素
- **格式**: 标准CSS选择器语法
- **支持**: 所有Playwright支持的选择器
- **示例**: `"selector": "h1, h2, title"`

### required (可选)
- **类型**: `boolean`
- **说明**: 是否为必需字段，如果提取失败是否抛出错误
- **默认值**: `false`
- **建议**: 关键字段（如标题）设置为 `true`
- **示例**: `"required": true`

### pattern (可选)
- **类型**: `string`
- **说明**: 正则表达式模式，用于过滤或匹配提取的文本
- **适用类型**: 主要用于 `text` 类型
- **示例**: `"pattern": "^获取"`

### columns (可选)
- **类型**: `string[]`
- **说明**: 表格的列名数组，用于验证表格结构
- **适用类型**: 仅用于 `table` 类型
- **示例**: `"columns": ["参数名称", "必选", "类型", "说明"]`

## 提取器类型

### 1. text - 文本提取器

提取元素的文本内容。

#### 基本用法

```json
{
  "field": "title",
  "type": "text",
  "selector": "h1",
  "required": true
}
```

#### 多选择器

可以使用逗号分隔多个选择器，提取第一个匹配的元素：

```json
{
  "field": "title",
  "type": "text",
  "selector": "h1, h2, title"
}
```

#### 使用 pattern 过滤

使用正则表达式匹配特定模式的文本：

```json
{
  "field": "briefDesc",
  "type": "text",
  "selector": "p",
  "pattern": "^获取"
}
```

这会提取所有段落，但只返回以"获取"开头的内容。

#### 提取特定属性

虽然当前实现提取 `textContent`，但可以通过选择器定位特定元素：

```json
{
  "field": "imageUrl",
  "type": "text",
  "selector": "img[src]"
}
```

#### 示例场景

- **页面标题**: `"selector": "h1, h2, title"`
- **描述文本**: `"selector": "p.description, div.intro"`
- **链接文本**: `"selector": "a.main-link"`
- **特定内容**: `"selector": "div#content", "pattern": "关键词"`

### 2. table - 表格提取器

提取表格数据，包括表头和数据行。

#### 基本用法

```json
{
  "field": "mainTable",
  "type": "table",
  "selector": "table"
}
```

#### 指定列名

使用 `columns` 字段验证表格结构：

```json
{
  "field": "parameters",
  "type": "table",
  "selector": "table",
  "columns": ["参数名称", "必选", "类型", "说明"]
}
```

#### 提取结果格式

单个表格：
```json
{
  "headers": ["列1", "列2", "列3"],
  "rows": [
    ["值1", "值2", "值3"],
    ["值4", "值5", "值6"]
  ]
}
```

多个表格（如果选择器匹配多个表格）：
```json
[
  {
    "headers": ["列1", "列2"],
    "rows": [["值1", "值2"]]
  },
  {
    "headers": ["列A", "列B"],
    "rows": [["值A", "值B"]]
  }
]
```

#### 表格识别逻辑

1. **表头识别**:
   - 优先从 `<thead>` 中提取
   - 如果没有 `<thead>`，使用第一行作为表头
   
2. **数据行提取**:
   - 优先从 `<tbody>` 中提取
   - 如果没有 `<tbody>`，提取所有行（跳过表头行）

#### 选择器技巧

- **特定表格**: `"selector": "table.data-table"`
- **第一个表格**: `"selector": "table:first-of-type"`
- **包含特定内容的表格**: `"selector": "table:has(th:contains('参数'))"`

#### 示例场景

- **API参数表**: `"columns": ["参数", "类型", "必选", "说明"]`
- **响应数据表**: `"columns": ["字段", "类型", "说明"]`
- **数据列表**: `"selector": "table.data-list"`

### 3. code - 代码块提取器

提取代码块内容，支持多种代码容器。

#### 基本用法

```json
{
  "field": "codeBlocks",
  "type": "code",
  "selector": "pre code"
}
```

#### 多种代码容器

```json
{
  "field": "apiExamples",
  "type": "code",
  "selector": "textarea, pre code, pre"
}
```

#### 提取结果格式

```json
[
  {
    "language": "javascript",
    "code": "console.log('hello');"
  },
  {
    "language": "json",
    "code": "{\"key\": \"value\"}"
  }
]
```

#### 语言识别

自动识别代码语言：

1. **从class识别**: `class="language-javascript"` → `"language": "javascript"`
2. **从内容推断**:
   - 以 `{` 或 `[` 开头 → `json`
   - 以 `<` 开头 → `xml`
   - 默认 → `text`

#### 支持的容器

- **`<pre><code>`**: 标准代码块
- **`<pre>`**: 纯文本代码块
- **`<textarea>`**: 只读文本区域（常用于API示例）

#### 选择器技巧

- **特定语言**: `"selector": "pre code.language-javascript"`
- **只读文本框**: `"selector": "textarea[readonly]"`
- **代码示例区**: `"selector": "div.code-example pre"`

#### 示例场景

- **API请求示例**: `"selector": "textarea.request-example"`
- **代码片段**: `"selector": "pre code"`
- **JSON响应**: `"selector": "pre.json-response"`

### 4. list - 列表提取器

提取有序或无序列表的内容。

#### 基本用法

```json
{
  "field": "features",
  "type": "list",
  "selector": "ul"
}
```

#### 提取有序列表

```json
{
  "field": "steps",
  "type": "list",
  "selector": "ol"
}
```

#### 提取所有列表

```json
{
  "field": "allLists",
  "type": "list",
  "selector": "ul, ol"
}
```

#### 提取结果格式

单个列表：
```json
{
  "type": "ul",
  "items": ["项目1", "项目2", "项目3"]
}
```

多个列表：
```json
[
  {
    "type": "ul",
    "items": ["项目1", "项目2"]
  },
  {
    "type": "ol",
    "items": ["步骤1", "步骤2"]
  }
]
```

#### 选择器技巧

- **特定类的列表**: `"selector": "ul.feature-list"`
- **导航列表**: `"selector": "nav ul"`
- **嵌套列表**: 会提取所有 `<li>` 的文本内容

#### 示例场景

- **功能列表**: `"selector": "ul.features"`
- **步骤说明**: `"selector": "ol.steps"`
- **导航菜单**: `"selector": "nav ul"`

## 提取器组合策略

### 1. 标题 + 描述 + 表格

典型的文档页面结构：

```json
{
  "extractors": [
    {
      "field": "title",
      "type": "text",
      "selector": "h1",
      "required": true
    },
    {
      "field": "description",
      "type": "text",
      "selector": "p.intro"
    },
    {
      "field": "dataTable",
      "type": "table",
      "selector": "table.main-data"
    }
  ]
}
```

### 2. API文档结构

```json
{
  "extractors": [
    {
      "field": "apiName",
      "type": "text",
      "selector": "h1",
      "required": true
    },
    {
      "field": "briefDesc",
      "type": "text",
      "selector": "p",
      "pattern": "^获取"
    },
    {
      "field": "requestUrl",
      "type": "text",
      "selector": "code.url"
    },
    {
      "field": "parameters",
      "type": "table",
      "selector": "table",
      "columns": ["参数", "类型", "必选", "说明"]
    },
    {
      "field": "responseFields",
      "type": "table",
      "selector": "table:nth-of-type(2)",
      "columns": ["字段", "类型", "说明"]
    },
    {
      "field": "examples",
      "type": "code",
      "selector": "textarea, pre code"
    }
  ]
}
```

### 3. 多表格提取

当页面包含多个表格时：

```json
{
  "extractors": [
    {
      "field": "mainTable",
      "type": "table",
      "selector": "table:first-of-type"
    },
    {
      "field": "detailTable",
      "type": "table",
      "selector": "table:nth-of-type(2)"
    },
    {
      "field": "summaryTable",
      "type": "table",
      "selector": "table.summary"
    }
  ]
}
```

## 错误处理

### 提取失败

当提取器执行失败时：

1. **非必需字段**: 返回 `null`，继续执行其他提取器
2. **必需字段**: 抛出错误，停止解析

### 选择器未匹配

- **text**: 返回空字符串 `""`
- **table**: 返回空数组 `[]`
- **code**: 返回空数组 `[]`
- **list**: 返回空数组 `[]`

### 调试技巧

1. **使用浏览器开发者工具**: 测试CSS选择器
2. **从宽到窄**: 先用宽泛的选择器，再逐步精确
3. **查看提取结果**: 运行测试脚本查看实际提取的数据
4. **添加日志**: 在TemplateParser中添加日志输出

## 最佳实践

### 1. 选择器精确性

❌ 不好：
```json
{"selector": "div"}  // 太宽泛
```

✅ 好：
```json
{"selector": "div.content h1"}  // 精确定位
```

### 2. 必需字段

关键字段设置 `required: true`：

```json
{
  "field": "title",
  "type": "text",
  "selector": "h1",
  "required": true  // 标题是必需的
}
```

### 3. 多选择器备选

使用多个选择器提高鲁棒性：

```json
{
  "field": "title",
  "type": "text",
  "selector": "h1, h2, title, .page-title"
}
```

### 4. 表格列名验证

指定列名以验证表格结构：

```json
{
  "field": "parameters",
  "type": "table",
  "selector": "table",
  "columns": ["参数", "类型", "说明"]  // 验证列结构
}
```

### 5. 代码块多容器

支持多种代码容器：

```json
{
  "field": "code",
  "type": "code",
  "selector": "textarea[readonly], pre code, pre"
}
```

## 常见问题

### Q: 如何提取元素属性（如href, src）？

A: 当前实现提取 `textContent`。如需属性，可以：
1. 修改 TemplateParser 的 `extractText` 方法
2. 或使用自定义提取器类型

### Q: 如何处理动态加载的内容？

A: TemplateParser 使用 Playwright，支持等待元素加载。可以在调用 `parse()` 前等待页面加载完成。

### Q: 如何提取嵌套结构？

A: 使用更精确的选择器，或多个提取器分别提取不同层级的内容。

### Q: 表格列数不匹配怎么办？

A: ConfigLoader 会输出警告，但不会阻止提取。检查选择器是否正确。

### Q: 如何提取多个相同类型的元素？

A: 
- **table/code/list**: 自动返回数组
- **text**: 只返回第一个匹配元素，如需多个，使用多个提取器

## 测试提取器

使用测试脚本验证提取器配置：

```bash
# 测试配置文件
node scripts/test-template-parser.js

# 测试真实页面
node scripts/test-real-pages.js
```

## 相关文档

- [配置格式说明](./CONFIG_FORMAT.md) - 完整的配置格式
- [过滤器配置指南](./FILTER_GUIDE.md) - 数据过滤配置
- [配置示例](../examples/template-config.jsonl) - 实际示例
- [TemplateParser API](../README.md) - Parser实现细节

## 下一步

- 阅读 [过滤器配置指南](./FILTER_GUIDE.md) 了解如何过滤数据
- 查看 [配置示例](../examples/template-config.jsonl) 学习实际用法
- 运行测试脚本验证配置有效性
