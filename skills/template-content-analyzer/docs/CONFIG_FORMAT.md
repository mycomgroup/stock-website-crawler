# 模板配置文件格式说明

## 概述

模板配置文件使用 **JSONL (JSON Lines)** 格式，每行包含一个完整的JSON对象，代表一个模板的解析配置。这种格式易于阅读、编辑和版本控制，特别适合大模型进行自动修改和优化。

## JSONL 格式

### 什么是 JSONL？

JSONL (JSON Lines) 是一种文本格式，其中：
- 每行是一个有效的JSON对象
- 行与行之间用换行符 (`\n`) 分隔
- 每行可以独立解析，无需加载整个文件

### 为什么使用 JSONL？

1. **易于编辑**: 每个模板配置独立一行，便于添加、删除或修改
2. **版本控制友好**: Git diff 可以清晰显示每个模板的变化
3. **流式处理**: 可以逐行读取，不需要一次性加载所有配置
4. **大模型友好**: 结构清晰，易于理解和修改
5. **可扩展**: 添加新模板只需追加新行

### 示例

```jsonl
{"name":"api-doc","description":"API文档解析器","urlPattern":{...},"extractors":[...],"filters":[...]}
{"name":"dashboard","description":"仪表板解析器","urlPattern":{...},"extractors":[...],"filters":[...]}
{"name":"report","description":"报告解析器","urlPattern":{...},"extractors":[...],"filters":[...]}
```

## 配置对象结构

每个配置对象包含以下字段：

```typescript
interface TemplateConfig {
  // 基本信息
  name: string;              // 模板名称（必需）
  description: string;       // 模板描述（必需）
  priority: number;          // 优先级，数字越大优先级越高（可选，默认0）
  
  // URL匹配规则
  urlPattern: {
    pattern: string;         // 正则表达式字符串（必需）
    pathTemplate: string;    // 路径模板（必需）
    queryParams: string[];   // 查询参数列表（可选）
  };
  
  // 数据提取规则
  extractors: Extractor[];   // 提取器数组（必需，至少一个）
  
  // 噪音过滤规则
  filters: Filter[];         // 过滤器数组（可选）
  
  // 元数据
  metadata: {
    generatedAt: string;     // ISO 8601时间戳（可选）
    pageCount: number;       // 分析的页面数量（可选）
    version: string;         // 配置版本（可选）
  };
}
```

## 字段详解

### 1. 基本信息

#### name (必需)
- **类型**: `string`
- **说明**: 模板的唯一标识符，用于识别和引用此模板
- **命名规范**: 使用小写字母和连字符，如 `api-doc`, `user-dashboard`
- **示例**: `"name": "api-doc"`

#### description (必需)
- **类型**: `string`
- **说明**: 模板的简短描述，说明此模板用于解析什么类型的页面
- **示例**: `"description": "Parser configuration for API documentation pages"`

#### priority (可选)
- **类型**: `number`
- **说明**: 解析器优先级，当多个解析器匹配同一URL时，优先级高的优先使用
- **默认值**: `0`
- **建议值**: 
  - 通用解析器: 0-50
  - 特定解析器: 50-100
  - 高优先级解析器: 100+
- **示例**: `"priority": 100`

### 2. URL匹配规则 (urlPattern)

#### pattern (必需)
- **类型**: `string`
- **说明**: 用于匹配URL的正则表达式字符串
- **格式**: 可以是纯正则表达式字符串，或 `/pattern/flags` 格式
- **注意**: 特殊字符需要转义（如 `.` 写成 `\\.`）
- **示例**: 
  ```json
  "pattern": "^https://www\\.lixinger\\.com/open/api/doc\\?api-key=(.+)$"
  ```

#### pathTemplate (必需)
- **类型**: `string`
- **说明**: URL路径模板，用于人类可读的路径表示
- **格式**: 使用 `*` 表示通配符
- **示例**: 
  - `"/open/api/doc"` - 固定路径
  - `"/analytics/*/dashboard"` - 包含通配符

#### queryParams (可选)
- **类型**: `string[]`
- **说明**: URL查询参数列表
- **默认值**: `[]`
- **示例**: `["api-key", "version"]`

### 3. 数据提取规则 (extractors)

提取器数组定义了如何从页面中提取数据。每个提取器包含以下字段：

```typescript
interface Extractor {
  field: string;             // 字段名（必需）
  type: string;              // 提取器类型（必需）
  selector: string;          // CSS选择器（必需）
  required?: boolean;        // 是否必需（可选）
  pattern?: string;          // 匹配模式（可选）
  columns?: string[];        // 表格列名（table类型专用）
}
```

详细说明请参考 [提取器配置指南](./EXTRACTOR_GUIDE.md)。

### 4. 噪音过滤规则 (filters)

过滤器数组定义了如何清理提取的数据。每个过滤器包含以下字段：

```typescript
interface Filter {
  type: string;              // 过滤器类型（必需）
  target: string;            // 目标类型（必需）
  pattern: string;           // 匹配模式（必需）
  reason: string;            // 原因说明（可选）
}
```

详细说明请参考 [过滤器配置指南](./FILTER_GUIDE.md)。

### 5. 元数据 (metadata)

#### generatedAt (可选)
- **类型**: `string`
- **说明**: 配置生成时间，ISO 8601格式
- **示例**: `"2024-02-25T10:00:00.000Z"`

#### pageCount (可选)
- **类型**: `number`
- **说明**: 分析时使用的页面数量
- **示例**: `163`

#### version (可选)
- **类型**: `string`
- **说明**: 配置版本号，建议使用语义化版本
- **示例**: `"1.0.0"`

## 完整示例

```json
{
  "name": "api-doc",
  "description": "Parser configuration for /open/api/doc",
  "priority": 100,
  "urlPattern": {
    "pattern": "^https://www\\.lixinger\\.com/open/api/doc\\?api-key=(.+)$",
    "pathTemplate": "/open/api/doc",
    "queryParams": ["api-key"]
  },
  "extractors": [
    {
      "field": "title",
      "type": "text",
      "selector": "h1, h2, title",
      "required": true
    },
    {
      "field": "briefDesc",
      "type": "text",
      "selector": "p",
      "pattern": "^获取"
    },
    {
      "field": "parameters",
      "type": "table",
      "selector": "table",
      "columns": ["参数名称", "必选", "类型", "说明"]
    },
    {
      "field": "apiExamples",
      "type": "code",
      "selector": "textarea, pre code"
    }
  ],
  "filters": [
    {
      "type": "remove",
      "target": "heading",
      "pattern": "API文档",
      "reason": "Template noise (100% frequency)"
    }
  ],
  "metadata": {
    "generatedAt": "2024-02-25T10:00:00.000Z",
    "pageCount": 163,
    "version": "1.0.0"
  }
}
```

## 配置验证

ConfigLoader 会自动验证配置的有效性，检查：

1. **必需字段**: name, urlPattern, extractors
2. **字段类型**: 确保字段类型正确
3. **数组非空**: extractors 不能为空
4. **提取器完整性**: 每个提取器必须有 field, type, selector
5. **类型有效性**: type 必须是 text, table, code, list 之一

验证失败会抛出详细的错误信息，指出具体的问题。

## 最佳实践

1. **命名规范**: 使用描述性的名称，如 `api-doc` 而不是 `parser1`
2. **优先级设置**: 特定解析器优先级高于通用解析器
3. **选择器精确性**: 使用尽可能精确的CSS选择器
4. **必需字段**: 关键字段设置 `required: true`
5. **注释说明**: 在 description 和 reason 中提供清晰的说明
6. **版本管理**: 修改配置时更新 version 字段
7. **测试验证**: 修改后使用测试脚本验证配置有效性

## 文件位置

配置文件通常保存在：
```
output/{project}/template-rules.jsonl
```

例如：
```
stock-crawler/output/lixinger-crawler/template-rules.jsonl
```

## 相关文档

- [提取器配置指南](./EXTRACTOR_GUIDE.md) - 详细的提取器配置说明
- [过滤器配置指南](./FILTER_GUIDE.md) - 详细的过滤器配置说明
- [配置示例](../examples/template-config.jsonl) - 实际的配置示例
- [使用指南](./USAGE_GUIDE.md) - 如何使用配置文件

## 下一步

- 阅读 [提取器配置指南](./EXTRACTOR_GUIDE.md) 了解如何配置数据提取
- 阅读 [过滤器配置指南](./FILTER_GUIDE.md) 了解如何配置数据过滤
- 查看 [配置示例](../examples/template-config.jsonl) 学习实际用法
