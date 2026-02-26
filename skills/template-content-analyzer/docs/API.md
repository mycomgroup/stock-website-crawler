# Template Content Analyzer - API 文档

本文档详细说明了 Template Content Analyzer 算法库的所有公共 API。

## 目录

- [ContentAnalyzer](#contentanalyzer) - 内容分析器
- [TemplateConfigGenerator](#templateconfiggenerator) - 配置生成器
- [TemplateParser](#templateparser) - 模板解析器
- [ConfigLoader](#configloader) - 配置加载器

---

## ContentAnalyzer

内容分析器，用于从 markdown 页面中提取和分析内容块。

### 构造函数

```javascript
const ContentAnalyzer = require('./lib/content-analyzer');
const analyzer = new ContentAnalyzer();
```

### 方法

#### extractContentBlocks(markdownContent)

从 markdown 内容中提取内容块。

**参数:**
- `markdownContent` (string): Markdown 内容

**返回:**
- `Array<Object>`: 内容块数组

**内容块对象结构:**
```javascript
{
  type: 'heading' | 'paragraph' | 'table' | 'code' | 'list',
  content: string,           // 块内容
  lineNumber: number,        // 起始行号
  endLine: number,           // 结束行号
  // 类型特定字段:
  rows: number,              // table: 行数
  language: string,          // code: 语言
  items: number              // list: 项目数
}
```

**支持的内容类型:**
- **heading**: `# 标题`, `## 标题`, etc.
- **paragraph**: 连续的文本行
- **table**: `| 列1 | 列2 |` 格式
- **code**: ` ```language ... ``` ` 格式
- **list**: `- 项目` 或 `1. 项目` 格式（支持嵌套）

**示例:**
```javascript
const markdown = `# API 文档
这是一个段落。

| 参数 | 说明 |
|------|------|
| id   | 用户ID |
`;

const blocks = analyzer.extractContentBlocks(markdown);
// [
//   { type: 'heading', content: '# API 文档', lineNumber: 1, endLine: 1 },
//   { type: 'paragraph', content: '这是一个段落。', lineNumber: 2, endLine: 2 },
//   { type: 'table', content: '...', rows: 3, lineNumber: 4, endLine: 6 }
// ]
```


#### normalizeText(text)

标准化文本用于比较。

**参数:**
- `text` (string): 原始文本

**返回:**
- `string`: 标准化后的文本

**标准化规则:**
- 转换为小写
- 合并多个空格为一个
- 移除标点符号（保留中文字符）
- 去除首尾空格

**示例:**
```javascript
const text1 = '  Hello,   World!  ';
const text2 = 'hello world';

console.log(analyzer.normalizeText(text1)); // 'hello world'
console.log(analyzer.normalizeText(text1) === analyzer.normalizeText(text2)); // true
```

---

#### calculateFrequency(pages)

计算内容块在多个页面中的出现频率。

**参数:**
- `pages` (Array<string>): 页面内容数组

**返回:**
- `Map`: 内容块频率映射

**Map 结构:**
- **key**: `${type}:${normalizedContent}`
- **value**: 
  ```javascript
  {
    type: string,              // 内容类型
    content: string,           // 原始内容
    normalizedContent: string, // 标准化内容
    count: number,             // 出现次数
    pages: Array<number>       // 出现的页面索引
  }
  ```

**注意:**
- 同一个内容块在同一页面中只计数一次
- 使用标准化文本进行匹配

**示例:**
```javascript
const pages = [
  '# 标题\n段落1',
  '# 标题\n段落2',
  '# 标题\n段落1'
];

const frequency = analyzer.calculateFrequency(pages);

// 标题出现在 3 个页面
const headingKey = Array.from(frequency.keys()).find(k => k.startsWith('heading:'));
console.log(frequency.get(headingKey).count); // 3

// 段落1 出现在 2 个页面
const para1Key = Array.from(frequency.keys()).find(k => k.includes('段落1'));
console.log(frequency.get(para1Key).count); // 2
```

---

#### classifyContent(frequency, totalPages, thresholds)

根据频率将内容分类。

**参数:**
- `frequency` (Map): 频率映射（来自 calculateFrequency）
- `totalPages` (number): 总页面数
- `thresholds` (Object): 阈值配置
  - `template` (number): 模板内容阈值（默认 0.8）
  - `unique` (number): 独特内容阈值（默认 0.2）

**返回:**
- `Object`: 分类结果
  ```javascript
  {
    template: Array,  // 高频内容（ratio > template 阈值）
    unique: Array,    // 低频内容（ratio < unique 阈值）
    mixed: Array      // 中频内容（介于两者之间）
  }
  ```

**分类规则:**
- **模板内容**: 出现率 > 80%（默认），通常是导航、页眉、页脚等
- **独特内容**: 出现率 < 20%（默认），通常是页面特有的数据
- **混合内容**: 出现率在 20%-80% 之间，需要进一步分析

**示例:**
```javascript
const classified = analyzer.classifyContent(frequency, 10, {
  template: 0.8,
  unique: 0.2
});

console.log(`模板内容: ${classified.template.length} 个`);
console.log(`独特内容: ${classified.unique.length} 个`);
console.log(`混合内容: ${classified.mixed.length} 个`);

// 查看高频模板内容
classified.template.forEach(item => {
  console.log(`${item.type}: ${item.content.substring(0, 30)}... (${(item.ratio * 100).toFixed(0)}%)`);
});
```

---

#### analyzeTemplate(pages, options)

完整的模板分析流程。

**参数:**
- `pages` (Array<string>): 页面内容数组
- `options` (Object): 选项
  - `thresholds` (Object): 频率阈值
    - `template` (number): 默认 0.8
    - `unique` (number): 默认 0.2

**返回:**
- `Object`: 分析结果
  ```javascript
  {
    stats: {
      totalPages: number,
      totalBlocks: number,
      templateBlocks: number,
      uniqueBlocks: number,
      mixedBlocks: number
    },
    classified: {
      template: Array,
      unique: Array,
      mixed: Array
    },
    frequency: Map
  }
  ```

**示例:**
```javascript
const pages = [
  '# API文档\n获取用户信息\n| 参数 | 说明 |\n|------|------|\n| id | 用户ID |',
  '# API文档\n获取订单信息\n| 参数 | 说明 |\n|------|------|\n| id | 订单ID |',
  '# API文档\n获取商品信息\n| 参数 | 说明 |\n|------|------|\n| id | 商品ID |'
];

const result = analyzer.analyzeTemplate(pages);

console.log('统计信息:', result.stats);
console.log('模板内容:', result.classified.template.length, '个');
console.log('独特内容:', result.classified.unique.length, '个');
```

---

## TemplateConfigGenerator

配置生成器，用于根据分析结果生成模板配置。

### 构造函数

```javascript
const TemplateConfigGenerator = require('./lib/template-config-generator');
const generator = new TemplateConfigGenerator();
```

### 方法

#### generateConfig(urlPattern, analysisResult)

生成完整的模板配置对象。

**参数:**
- `urlPattern` (Object): URL 模式信息
  ```javascript
  {
    name: string,              // 模式名称
    pattern: string,           // 正则表达式
    pathTemplate: string,      // 路径模板
    queryParams: Array<string> // 查询参数列表
  }
  ```
- `analysisResult` (Object): 模板分析结果（来自 ContentAnalyzer.analyzeTemplate）

**返回:**
- `Object`: 完整的模板配置对象

**配置对象结构:**
```javascript
{
  name: string,
  description: string,
  priority: number,
  urlPattern: {
    pattern: string,
    pathTemplate: string,
    queryParams: Array<string>
  },
  extractors: Array<Extractor>,
  filters: Array<Filter>,
  metadata: {
    generatedAt: string,
    pageCount: number,
    version: string
  }
}
```

**示例:**
```javascript
const urlPattern = {
  name: 'api-doc',
  pattern: '^https://www\\.lixinger\\.com/open/api/doc\\?api-key=(.+)$',
  pathTemplate: '/open/api/doc',
  queryParams: ['api-key']
};

const analysisResult = analyzer.analyzeTemplate(pages);
const config = generator.generateConfig(urlPattern, analysisResult);

console.log('Generated config:', config.name);
console.log('Extractors:', config.extractors.length);
console.log('Filters:', config.filters.length);
```

---

#### generateExtractors(dataStructures, classified)

生成提取器配置数组。

**参数:**
- `dataStructures` (Object): 数据结构信息
  ```javascript
  {
    tables: Array,      // 表格结构
    codeBlocks: Array,  // 代码块结构
    lists: Array        // 列表结构
  }
  ```
- `classified` (Object): 分类后的内容

**返回:**
- `Array<Extractor>`: 提取器配置数组

**Extractor 结构:**
```javascript
{
  field: string,           // 字段名
  type: 'text' | 'table' | 'code' | 'list',
  selector: string,        // CSS 选择器
  required: boolean,       // 是否必需
  pattern: string,         // 匹配模式（可选）
  columns: Array<string>   // 表格列名（table 类型）
}
```

**示例:**
```javascript
const extractors = generator.generateExtractors(dataStructures, classified);

extractors.forEach(ext => {
  console.log(`${ext.field} (${ext.type}): ${ext.selector}`);
});
```

---

#### generateFilters(cleaningRules, classified)

生成过滤器配置数组。

**参数:**
- `cleaningRules` (Object): 清洗规则
  ```javascript
  {
    removePatterns: Array<string>
  }
  ```
- `classified` (Object): 分类后的内容
  - `template` (Array): 高频模板内容

**返回:**
- `Array<Filter>`: 过滤器配置数组

**Filter 结构:**
```javascript
{
  type: 'remove' | 'keep' | 'transform',
  target: string,          // 目标类型
  pattern: string,         // 匹配模式
  reason: string           // 原因说明
}
```

**示例:**
```javascript
const filters = generator.generateFilters(cleaningRules, classified);

filters.forEach(filter => {
  console.log(`${filter.type}: ${filter.pattern} (${filter.reason})`);
});
```

---

#### saveAsJSONL(configs, outputPath)

保存配置为 JSONL 格式文件。

**参数:**
- `configs` (Array<Object>): 配置对象数组
- `outputPath` (string): 输出文件路径

**返回:**
- `Promise<void>`

**JSONL 格式:**
- 每行一个 JSON 对象
- 无逗号分隔
- 易于逐行读取和处理

**示例:**
```javascript
const configs = [config1, config2, config3];
await generator.saveAsJSONL(configs, 'output/template-rules.jsonl');
console.log('Configs saved successfully');
```

---

## TemplateParser

模板解析器，基于配置对象进行 URL 匹配和数据提取。

### 构造函数

```javascript
const TemplateParser = require('./lib/template-parser');

const parser = new TemplateParser(config);
```

**参数:**
- `config` (Object): 模板配置对象

### 方法

#### matches(url)

检查 URL 是否匹配此解析器。

**参数:**
- `url` (string): 页面 URL

**返回:**
- `boolean`: 是否匹配

**示例:**
```javascript
const matches = parser.matches('https://www.lixinger.com/open/api/doc?api-key=cn/company');
console.log('Matches:', matches); // true or false
```

---

#### getPriority()

获取解析器优先级。

**返回:**
- `number`: 优先级（数字越大优先级越高）

**示例:**
```javascript
const priority = parser.getPriority();
console.log('Priority:', priority); // 100
```

---

#### parse(page, url, options)

解析页面（主入口）。

**参数:**
- `page` (Page): Playwright 页面对象
- `url` (string): 页面 URL
- `options` (Object): 解析选项（可选）

**返回:**
- `Promise<Object>`: 解析后的数据

**返回对象结构:**
```javascript
{
  type: string,           // 模板类型
  url: string,            // 页面 URL
  [field]: any,           // 提取的字段数据
  error: string           // 错误信息（如果有）
}
```

**示例:**
```javascript
const { chromium } = require('playwright');

const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto(url);

const result = await parser.parse(page, url);
console.log('Result:', result);

await browser.close();
```

---

#### getName()

获取解析器名称。

**返回:**
- `string`: 名称

**示例:**
```javascript
const name = parser.getName();
console.log('Parser name:', name); // 'api-doc'
```

---

#### getConfig()

获取配置信息。

**返回:**
- `Object`: 配置对象

**示例:**
```javascript
const config = parser.getConfig();
console.log('Config:', config);
```

---

## ConfigLoader

配置加载器，用于从 JSONL 文件加载配置并创建 Parser 实例。

### 静态方法

#### loadConfigs(jsonlPath)

从 JSONL 文件加载所有配置。

**参数:**
- `jsonlPath` (string): JSONL 文件路径

**返回:**
- `Array<Object>`: 配置对象数组

**示例:**
```javascript
const ConfigLoader = require('./lib/config-loader');

const configs = ConfigLoader.loadConfigs('output/template-rules.jsonl');
console.log(`Loaded ${configs.length} configurations`);
```

---

#### loadConfigByName(jsonlPath, name)

加载指定名称的配置。

**参数:**
- `jsonlPath` (string): JSONL 文件路径
- `name` (string): 配置名称

**返回:**
- `Object|null`: 配置对象，如果未找到则返回 null

**示例:**
```javascript
const config = ConfigLoader.loadConfigByName('output/template-rules.jsonl', 'api-doc');

if (config) {
  console.log('Found config:', config.name);
} else {
  console.log('Config not found');
}
```

---

#### createParsers(jsonlPath, ParserClass)

创建 Parser 实例数组。

**参数:**
- `jsonlPath` (string): JSONL 文件路径
- `ParserClass` (Class): Parser 类（如 TemplateParser）

**返回:**
- `Array<Parser>`: Parser 实例数组

**示例:**
```javascript
const TemplateParser = require('./lib/template-parser');

const parsers = ConfigLoader.createParsers('output/template-rules.jsonl', TemplateParser);

console.log(`Created ${parsers.length} parsers`);

// 使用 parsers
const url = 'https://www.lixinger.com/open/api/doc?api-key=cn/company';
const parser = parsers.find(p => p.matches(url));
if (parser) {
  console.log(`Using parser: ${parser.getName()}`);
}
```

---

#### getConfigStats(jsonlPath)

获取配置统计信息。

**参数:**
- `jsonlPath` (string): JSONL 文件路径

**返回:**
- `Object`: 统计信息
  ```javascript
  {
    totalConfigs: number,
    configNames: Array<string>,
    totalExtractors: number,
    totalFilters: number,
    extractorTypes: Object,    // { text: 5, table: 3, ... }
    filterTypes: Object        // { remove: 10, keep: 2, ... }
  }
  ```

**示例:**
```javascript
const stats = ConfigLoader.getConfigStats('output/template-rules.jsonl');

console.log('Total configs:', stats.totalConfigs);
console.log('Config names:', stats.configNames);
console.log('Total extractors:', stats.totalExtractors);
console.log('Extractor types:', stats.extractorTypes);
console.log('Filter types:', stats.filterTypes);
```

---

#### generateTemplateConfig(urlPattern, analysisResult)

生成模板配置对象（便捷方法）。

**参数:**
- `urlPattern` (Object): URL 模式信息
- `analysisResult` (Object): 模板分析结果

**返回:**
- `Object`: 模板配置对象

**示例:**
```javascript
const config = ConfigLoader.generateTemplateConfig(urlPattern, analysisResult);
console.log('Generated config:', config.name);
```

---

## 完整使用示例

### 示例 1: 分析页面并生成配置

```javascript
const ContentAnalyzer = require('./lib/content-analyzer');
const TemplateConfigGenerator = require('./lib/template-config-generator');
const fs = require('fs').promises;

async function analyzeAndGenerateConfig() {
  // 1. 读取页面
  const pages = [
    await fs.readFile('pages/page1.md', 'utf-8'),
    await fs.readFile('pages/page2.md', 'utf-8'),
    await fs.readFile('pages/page3.md', 'utf-8')
  ];

  // 2. 分析页面
  const analyzer = new ContentAnalyzer();
  const analysisResult = analyzer.analyzeTemplate(pages);

  // 3. 生成配置
  const generator = new TemplateConfigGenerator();
  const urlPattern = {
    name: 'api-doc',
    pattern: '^https://example\\.com/api/doc$',
    pathTemplate: '/api/doc',
    queryParams: []
  };
  
  const config = generator.generateConfig(urlPattern, analysisResult);

  // 4. 保存配置
  await generator.saveAsJSONL([config], 'output/template-rules.jsonl');
  
  console.log('Config generated and saved');
}

analyzeAndGenerateConfig();
```

### 示例 2: 加载配置并解析页面

```javascript
const ConfigLoader = require('./lib/config-loader');
const TemplateParser = require('./lib/template-parser');
const { chromium } = require('playwright');

async function parseWithConfig(url, configPath) {
  // 1. 加载配置
  const parsers = ConfigLoader.createParsers(configPath, TemplateParser);
  console.log(`Loaded ${parsers.length} parsers`);

  // 2. 找到匹配的解析器
  const parser = parsers.find(p => p.matches(url));
  if (!parser) {
    throw new Error(`No parser found for URL: ${url}`);
  }
  console.log(`Using parser: ${parser.getName()}`);

  // 3. 启动浏览器
  const browser = await chromium.launch();
  const page = await browser.newPage();

  try {
    // 4. 访问页面
    await page.goto(url, { waitUntil: 'networkidle' });

    // 5. 解析页面
    const result = await parser.parse(page, url);

    return result;
  } finally {
    await browser.close();
  }
}

// 使用
parseWithConfig(
  'https://www.lixinger.com/open/api/doc?api-key=cn/company',
  'output/template-rules.jsonl'
).then(result => {
  console.log('Result:', JSON.stringify(result, null, 2));
});
```

---

## 错误处理

所有方法都包含错误处理：

- **文件读取错误**: 抛出详细的错误信息
- **格式错误**: 跳过错误行，记录警告
- **解析错误**: 返回包含 error 字段的结果对象
- **配置验证**: 检查必需字段，抛出验证错误

**示例:**
```javascript
try {
  const configs = ConfigLoader.loadConfigs('output/template-rules.jsonl');
} catch (error) {
  console.error('Failed to load configs:', error.message);
}
```

---

## 性能考虑

- **批量处理**: 使用批量方法处理多个页面
- **缓存**: 频率计算结果会被缓存
- **流式处理**: 大文件使用流式读取
- **并行处理**: 支持并行分析多个模板

---

## 相关文档

- [配置格式说明](./CONFIG_FORMAT.md)
- [提取器配置指南](./EXTRACTOR_GUIDE.md)
- [过滤器配置指南](./FILTER_GUIDE.md)
- [配置示例](./CONFIG_EXAMPLES.md)
- [使用指南](./USAGE_GUIDE.md)
- [架构文档](../../ARCHITECTURE.md)
