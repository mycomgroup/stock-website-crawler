# 过滤器配置指南

## 概述

过滤器（Filter）用于清理提取的数据，移除模板噪音，保留有用信息。过滤器基于内容频率分析自动生成，也可以手动配置以满足特定需求。

## 过滤器结构

```typescript
interface Filter {
  type: string;              // 过滤器类型（必需）
  target: string;            // 目标类型（必需）
  pattern: string;           // 匹配模式（必需）
  reason: string;            // 原因说明（可选）
}
```

## 字段说明

### type (必需)
- **类型**: `string`
- **说明**: 过滤器类型，决定如何处理匹配的内容
- **有效值**: `remove`, `keep`, `transform`
- **示例**: `"type": "remove"`

### target (必需)
- **类型**: `string`
- **说明**: 目标内容类型，指定要过滤的内容类别
- **有效值**: `heading`, `paragraph`, `table`, `code`, `list`, `text`, `all`
- **示例**: `"target": "heading"`

### pattern (必需)
- **类型**: `string`
- **说明**: 匹配模式，用于识别要过滤的内容
- **格式**: 可以是普通字符串或正则表达式
- **注意**: 特殊字符需要转义
- **示例**: `"pattern": "API文档"`

### reason (可选)
- **类型**: `string`
- **说明**: 过滤原因说明，便于理解和维护
- **建议**: 包含频率信息或其他上下文
- **示例**: `"reason": "Template noise (100% frequency)"`

## 过滤器类型

### 1. remove - 移除过滤器

移除匹配的内容，用于清理模板噪音。

#### 基本用法

```json
{
  "type": "remove",
  "target": "heading",
  "pattern": "API文档",
  "reason": "Template noise (100% frequency)"
}
```

#### 工作原理

1. 在提取的数据中查找匹配 `target` 类型的内容
2. 检查内容是否匹配 `pattern`
3. 如果匹配，从结果中移除该内容

#### 使用场景

- **导航元素**: 页眉、页脚、侧边栏
- **重复标题**: 每个页面都有的标题
- **版权信息**: 页面底部的版权声明
- **广告内容**: 广告区块

#### 示例

移除导航标题：
```json
{
  "type": "remove",
  "target": "heading",
  "pattern": "导航",
  "reason": "Navigation header (100% frequency)"
}
```

移除版权信息：
```json
{
  "type": "remove",
  "target": "paragraph",
  "pattern": "^Copyright|^©",
  "reason": "Copyright notice"
}
```

移除空段落：
```json
{
  "type": "remove",
  "target": "paragraph",
  "pattern": "^\\s*$",
  "reason": "Empty paragraphs"
}
```

### 2. keep - 保留过滤器

只保留匹配的内容，移除其他内容。

#### 基本用法

```json
{
  "type": "keep",
  "target": "paragraph",
  "pattern": "^获取|^查询|^更新",
  "reason": "Keep only API description paragraphs"
}
```

#### 工作原理

1. 在提取的数据中查找匹配 `target` 类型的内容
2. 检查内容是否匹配 `pattern`
3. 只保留匹配的内容，移除不匹配的

#### 使用场景

- **特定内容**: 只保留特定格式的内容
- **关键信息**: 只保留包含关键词的段落
- **数据过滤**: 只保留符合条件的数据

#### 示例

只保留API描述：
```json
{
  "type": "keep",
  "target": "paragraph",
  "pattern": "^获取|^查询|^创建|^更新|^删除",
  "reason": "Keep only API operation descriptions"
}
```

只保留特定表格：
```json
{
  "type": "keep",
  "target": "table",
  "pattern": "参数|字段|属性",
  "reason": "Keep only data structure tables"
}
```

### 3. transform - 转换过滤器

转换匹配的内容，修改其格式或内容。

#### 基本用法

```json
{
  "type": "transform",
  "target": "text",
  "pattern": "\\s+",
  "reason": "Normalize whitespace"
}
```

#### 工作原理

1. 在提取的数据中查找匹配 `target` 类型的内容
2. 检查内容是否匹配 `pattern`
3. 对匹配的内容应用转换规则

#### 使用场景

- **格式标准化**: 统一空格、换行等
- **内容清理**: 移除特殊字符
- **数据转换**: 转换数据格式

#### 注意

当前 TemplateParser 实现中，`transform` 类型的过滤器尚未完全实现。如需使用，需要扩展 `applyFilters` 方法。

#### 示例（未来实现）

标准化空格：
```json
{
  "type": "transform",
  "target": "text",
  "pattern": "\\s+",
  "replacement": " ",
  "reason": "Normalize whitespace"
}
```

移除HTML标签：
```json
{
  "type": "transform",
  "target": "text",
  "pattern": "<[^>]+>",
  "replacement": "",
  "reason": "Remove HTML tags"
}
```

## 目标类型

### heading
- **说明**: 标题元素（h1, h2, h3等）
- **常见用途**: 移除重复的页面标题、导航标题
- **示例**: `"target": "heading"`

### paragraph
- **说明**: 段落元素（p）
- **常见用途**: 移除版权信息、广告文本
- **示例**: `"target": "paragraph"`

### table
- **说明**: 表格元素
- **常见用途**: 移除导航表格、保留数据表格
- **示例**: `"target": "table"`

### code
- **说明**: 代码块元素
- **常见用途**: 移除示例代码、保留API代码
- **示例**: `"target": "code"`

### list
- **说明**: 列表元素（ul, ol）
- **常见用途**: 移除导航列表、保留内容列表
- **示例**: `"target": "list"`

### text
- **说明**: 所有文本内容
- **常见用途**: 全局文本转换
- **示例**: `"target": "text"`

### all
- **说明**: 所有类型的内容
- **常见用途**: 全局过滤规则
- **示例**: `"target": "all"`

## 模式匹配

### 普通字符串匹配

精确匹配字符串：

```json
{
  "pattern": "API文档"
}
```

匹配包含"API文档"的内容。

### 正则表达式匹配

使用正则表达式进行复杂匹配：

```json
{
  "pattern": "^获取|^查询|^更新"
}
```

匹配以"获取"、"查询"或"更新"开头的内容。

### 常用正则模式

#### 开头匹配
```json
{"pattern": "^关键词"}
```

#### 结尾匹配
```json
{"pattern": "关键词$"}
```

#### 包含匹配
```json
{"pattern": "关键词"}
```

#### 多个关键词（或）
```json
{"pattern": "关键词1|关键词2|关键词3"}
```

#### 空白内容
```json
{"pattern": "^\\s*$"}
```

#### 特殊字符
```json
{"pattern": "^Copyright|^©|^版权"}
```

## 自动生成规则

过滤器通常基于内容频率分析自动生成：

### 高频内容（模板噪音）

出现率 > 80% 的内容被识别为模板噪音，自动生成 `remove` 过滤器：

```json
{
  "type": "remove",
  "target": "heading",
  "pattern": "API文档",
  "reason": "Template noise (100% frequency)"
}
```

### 生成逻辑

```javascript
// 伪代码
if (content.frequency > 0.9) {
  filters.push({
    type: 'remove',
    target: content.type,
    pattern: escapeRegex(content.text.substring(0, 50)),
    reason: `Template noise (${(content.frequency * 100).toFixed(0)}% frequency)`
  });
}
```

## 过滤器组合

### 多个移除规则

```json
{
  "filters": [
    {
      "type": "remove",
      "target": "heading",
      "pattern": "API文档",
      "reason": "Template noise (100% frequency)"
    },
    {
      "type": "remove",
      "target": "heading",
      "pattern": "导航",
      "reason": "Navigation header (100% frequency)"
    },
    {
      "type": "remove",
      "target": "paragraph",
      "pattern": "^Copyright|^©",
      "reason": "Copyright notice"
    }
  ]
}
```

### 移除 + 保留

先移除噪音，再保留特定内容：

```json
{
  "filters": [
    {
      "type": "remove",
      "target": "heading",
      "pattern": "导航",
      "reason": "Remove navigation"
    },
    {
      "type": "keep",
      "target": "paragraph",
      "pattern": "^获取|^查询",
      "reason": "Keep only API descriptions"
    }
  ]
}
```

## 实现细节

### 当前实现

TemplateParser 的 `applyFilters` 方法：

```javascript
applyFilters(result) {
  // 当前实现：简单返回结果
  // 未来可以实现：
  // - remove: 移除匹配的内容
  // - keep: 只保留匹配的内容
  // - transform: 转换内容
  
  return result;
}
```

### 扩展实现

如需完整的过滤功能，可以扩展 `applyFilters` 方法：

```javascript
applyFilters(result) {
  if (!this.config.filters || this.config.filters.length === 0) {
    return result;
  }

  // 遍历所有过滤器
  this.config.filters.forEach(filter => {
    switch (filter.type) {
      case 'remove':
        result = this.applyRemoveFilter(result, filter);
        break;
      case 'keep':
        result = this.applyKeepFilter(result, filter);
        break;
      case 'transform':
        result = this.applyTransformFilter(result, filter);
        break;
    }
  });

  return result;
}
```

## 最佳实践

### 1. 明确原因

始终提供 `reason` 字段：

❌ 不好：
```json
{
  "type": "remove",
  "target": "heading",
  "pattern": "API文档"
}
```

✅ 好：
```json
{
  "type": "remove",
  "target": "heading",
  "pattern": "API文档",
  "reason": "Template noise (100% frequency)"
}
```

### 2. 精确模式

使用精确的匹配模式：

❌ 不好：
```json
{"pattern": "文档"}  // 太宽泛
```

✅ 好：
```json
{"pattern": "^API文档$"}  // 精确匹配
```

### 3. 频率信息

在 `reason` 中包含频率信息：

```json
{
  "reason": "Template noise (95% frequency)"
}
```

### 4. 测试验证

添加过滤器后，使用测试脚本验证效果：

```bash
node scripts/test-template-parser.js
```

### 5. 渐进式过滤

从宽松到严格，逐步添加过滤规则：

1. 先移除明显的噪音（100%频率）
2. 再移除次要噪音（>90%频率）
3. 最后根据实际效果调整

## 常见场景

### API文档页面

```json
{
  "filters": [
    {
      "type": "remove",
      "target": "heading",
      "pattern": "API文档|导航|菜单",
      "reason": "Template headers"
    },
    {
      "type": "remove",
      "target": "paragraph",
      "pattern": "^Copyright|^版权所有",
      "reason": "Copyright notice"
    },
    {
      "type": "keep",
      "target": "paragraph",
      "pattern": "^获取|^查询|^创建|^更新|^删除",
      "reason": "API operation descriptions"
    }
  ]
}
```

### 数据仪表板

```json
{
  "filters": [
    {
      "type": "remove",
      "target": "heading",
      "pattern": "仪表板|Dashboard",
      "reason": "Page title"
    },
    {
      "type": "remove",
      "target": "list",
      "pattern": "首页|设置|帮助",
      "reason": "Navigation menu"
    }
  ]
}
```

### 新闻文章

```json
{
  "filters": [
    {
      "type": "remove",
      "target": "paragraph",
      "pattern": "相关阅读|推荐文章|热门新闻",
      "reason": "Related content links"
    },
    {
      "type": "remove",
      "target": "paragraph",
      "pattern": "^广告$|^Advertisement$",
      "reason": "Advertisement blocks"
    }
  ]
}
```

## 调试技巧

### 1. 查看原始数据

先不使用过滤器，查看原始提取的数据：

```json
{
  "filters": []
}
```

### 2. 逐个添加

一次添加一个过滤器，观察效果：

```json
{
  "filters": [
    {
      "type": "remove",
      "target": "heading",
      "pattern": "API文档"
    }
    // 先测试这一个，确认有效后再添加其他
  ]
}
```

### 3. 使用测试脚本

运行测试脚本查看过滤效果：

```bash
node scripts/test-template-parser.js
```

### 4. 检查日志

在 TemplateParser 中添加日志输出：

```javascript
console.log('Applying filters:', this.config.filters);
console.log('Before filtering:', result);
// ... apply filters ...
console.log('After filtering:', result);
```

## 性能考虑

### 过滤器数量

- **建议**: 每个配置不超过10个过滤器
- **原因**: 过多过滤器会影响解析性能

### 正则表达式复杂度

- **建议**: 使用简单的正则表达式
- **避免**: 复杂的回溯、嵌套量词

### 过滤顺序

- **建议**: 先执行 `remove`，再执行 `keep`
- **原因**: 减少需要处理的数据量

## 未来扩展

### 1. 条件过滤

基于其他字段的值进行过滤：

```json
{
  "type": "remove",
  "target": "paragraph",
  "pattern": "广告",
  "condition": {
    "field": "title",
    "contains": "免费"
  }
}
```

### 2. 自定义函数

支持自定义过滤函数：

```json
{
  "type": "custom",
  "function": "removeShortParagraphs",
  "params": {"minLength": 50}
}
```

### 3. 统计信息

记录过滤统计：

```json
{
  "filterStats": {
    "removed": 15,
    "kept": 8,
    "transformed": 3
  }
}
```

## 相关文档

- [配置格式说明](./CONFIG_FORMAT.md) - 完整的配置格式
- [提取器配置指南](./EXTRACTOR_GUIDE.md) - 数据提取配置
- [配置示例](../examples/template-config.jsonl) - 实际示例
- [TemplateParser API](../README.md) - Parser实现细节

## 下一步

- 查看 [配置示例](../examples/template-config.jsonl) 学习实际用法
- 运行测试脚本验证过滤效果
- 根据实际需求调整过滤规则
