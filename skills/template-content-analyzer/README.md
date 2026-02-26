# Template Content Analyzer

分析markdown页面内容，识别模板内容和独特数据，生成模板配置文件。

## 功能

- **提取内容块**: 从markdown中提取标题、段落、表格、代码块、列表
- **文本标准化**: 标准化文本用于比较（去除空格、标点、统一大小写）
- **频率计算**: 计算每个内容块在所有页面中的出现频率
- **内容分类**: 将内容分为模板内容（高频）、独特数据（低频）、混合内容（中频）
- **模板分析**: 完整的模板分析流程
- **配置生成**: 生成JSONL格式的模板配置文件
- **配置驱动解析**: 使用TemplateParser基于配置解析页面

## 文档

### 配置文件文档
- **[配置格式说明](./docs/CONFIG_FORMAT.md)** - JSONL格式和配置对象结构详解
- **[提取器配置指南](./docs/EXTRACTOR_GUIDE.md)** - 如何配置text、table、code、list提取器
- **[过滤器配置指南](./docs/FILTER_GUIDE.md)** - 如何配置remove、keep、transform过滤器
- **[配置示例](./docs/CONFIG_EXAMPLES.md)** - 各种场景的完整配置示例
- **[使用指南](./docs/USAGE_GUIDE.md)** - 如何加载、使用和调试配置文件

### 快速链接
- [API文档](#api-文档) - TemplateContentAnalyzer API
- [配置加载](#配置加载) - ConfigLoader API
- [模板解析](#模板解析) - TemplateParser API
- [测试脚本](#运行测试) - 如何运行测试

## 安装

```bash
npm install
```

## 使用

### TemplateContentAnalyzer API

```javascript
const TemplateContentAnalyzer = require('./lib/content-analyzer');
const analyzer = new TemplateContentAnalyzer();

// 1. 提取内容块
const markdown = `# 标题
这是一个段落。

| 列1 | 列2 |
|-----|-----|
| 值1 | 值2 |

\`\`\`javascript
console.log('hello');
\`\`\`

- 列表项1
- 列表项2
`;

const blocks = analyzer.extractContentBlocks(markdown);
console.log(blocks);
// [
//   { type: 'heading', content: '# 标题', lineNumber: 1 },
//   { type: 'paragraph', content: '这是一个段落。', lineNumber: 2 },
//   { type: 'table', content: '...', rows: 3, lineNumber: 4 },
//   { type: 'code', content: '...', language: 'javascript', lineNumber: 8 },
//   { type: 'list', content: '...', items: 2, lineNumber: 12 }
// ]

// 2. 文本标准化
const text = '  Hello,   World!  ';
const normalized = analyzer.normalizeText(text);
console.log(normalized); // 'hello world'

// 3. 计算频率
const pages = [
  '# API文档\n这是说明',
  '# API文档\n这是另一个说明',
  '# API文档\n这是说明'
];

const frequency = analyzer.calculateFrequency(pages);
console.log(frequency);
// Map {
//   'heading:api文档' => { type: 'heading', content: '# API文档', count: 3, pages: [0,1,2] },
//   'paragraph:这是说明' => { type: 'paragraph', content: '这是说明', count: 2, pages: [0,2] },
//   ...
// }

// 4. 分类内容
const classified = analyzer.classifyContent(frequency, pages.length);
console.log(classified);
// {
//   template: [{ type: 'heading', content: '# API文档', ratio: 1.0, ... }],
//   unique: [{ type: 'paragraph', content: '...', ratio: 0.1, ... }],
//   mixed: [{ type: 'paragraph', content: '...', ratio: 0.5, ... }]
// }

// 5. 完整分析流程
const result = analyzer.analyzeTemplate(pages, {
  thresholds: { template: 0.8, unique: 0.2 }
});
console.log(result);
// {
//   stats: { totalPages: 3, totalBlocks: 5, templateBlocks: 2, ... },
//   classified: { template: [...], unique: [...], mixed: [...] },
//   frequency: Map { ... }
// }
```

## API 文档

### TemplateContentAnalyzer

#### `extractContentBlocks(markdownContent)`

从markdown内容中提取内容块。

**参数:**
- `markdownContent` (string): Markdown内容

**返回:**
- `Array<Object>`: 内容块数组，每个块包含:
  - `type` (string): 块类型（heading, paragraph, table, code, list）
  - `content` (string): 块内容
  - `lineNumber` (number): 起始行号
  - `endLine` (number): 结束行号
  - 其他类型特定字段（如table的rows，code的language等）

**支持的内容类型:**
- **标题**: `# 标题`, `## 标题`, etc.
- **段落**: 连续的文本行
- **表格**: `| 列1 | 列2 |` 格式
- **代码块**: ` ```language ... ``` ` 格式
- **列表**: `- 项目` 或 `1. 项目` 格式（支持嵌套）

**示例:**
```javascript
const blocks = analyzer.extractContentBlocks(markdown);
blocks.forEach(block => {
  console.log(`${block.type}: ${block.content.substring(0, 50)}...`);
});
```

#### `normalizeText(text)`

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
console.log(analyzer.normalizeText(text1) === analyzer.normalizeText(text2)); // true
```

#### `calculateFrequency(pages)`

计算内容块在多个页面中的出现频率。

**参数:**
- `pages` (Array<string>): 页面内容数组

**返回:**
- `Map`: 内容块频率映射
  - key: `${type}:${normalizedContent}`
  - value: `{ type, content, normalizedContent, count, pages }`

**注意:**
- 同一个内容块在同一页面中只计数一次
- 使用标准化文本进行匹配

**示例:**
```javascript
const pages = ['# 标题\n段落', '# 标题\n另一段落', '# 标题\n段落'];
const frequency = analyzer.calculateFrequency(pages);

// 标题出现在3个页面
const headingKey = Array.from(frequency.keys()).find(k => k.startsWith('heading:'));
console.log(frequency.get(headingKey).count); // 3

// 段落出现在2个页面
const paraKey = Array.from(frequency.keys()).find(k => k.includes('段落'));
console.log(frequency.get(paraKey).count); // 2
```

#### `classifyContent(frequency, totalPages, thresholds)`

根据频率将内容分类。

**参数:**
- `frequency` (Map): 频率映射（来自calculateFrequency）
- `totalPages` (number): 总页面数
- `thresholds` (Object): 阈值配置
  - `template` (number): 模板内容阈值（默认0.8）
  - `unique` (number): 独特内容阈值（默认0.2）

**返回:**
- `Object`: 分类结果
  - `template` (Array): 高频内容（ratio > template阈值）
  - `unique` (Array): 低频内容（ratio < unique阈值）
  - `mixed` (Array): 中频内容（介于两者之间）

**分类规则:**
- **模板内容**: 出现率 > 80%（默认），通常是导航、页眉、页脚等
- **独特内容**: 出现率 < 20%（默认），通常是页面特有的数据
- **混合内容**: 出现率在20%-80%之间，需要进一步分析

**示例:**
```javascript
const classified = analyzer.classifyContent(frequency, 10, {
  template: 0.8,
  unique: 0.2
});

console.log(`模板内容: ${classified.template.length}个`);
console.log(`独特内容: ${classified.unique.length}个`);
console.log(`混合内容: ${classified.mixed.length}个`);

// 查看高频模板内容
classified.template.forEach(item => {
  console.log(`${item.type}: ${item.content.substring(0, 30)}... (${(item.ratio * 100).toFixed(0)}%)`);
});
```

#### `analyzeTemplate(pages, options)`

完整的模板分析流程。

**参数:**
- `pages` (Array<string>): 页面内容数组
- `options` (Object): 选项
  - `thresholds` (Object): 频率阈值

**返回:**
- `Object`: 分析结果
  - `stats` (Object): 统计信息
    - `totalPages`: 总页面数
    - `totalBlocks`: 总内容块数
    - `templateBlocks`: 模板内容块数
    - `uniqueBlocks`: 独特内容块数
    - `mixedBlocks`: 混合内容块数
  - `classified` (Object): 分类结果（template, unique, mixed）
  - `frequency` (Map): 频率数据

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

## 运行测试

```bash
# 运行单元测试
node test/content-analyzer.test.js
```

## 测试覆盖

项目包含完整的测试套件：

### TemplateContentAnalyzer 测试
- ✓ 提取标题
- ✓ 提取段落
- ✓ 提取表格
- ✓ 提取代码块
- ✓ 提取列表
- ✓ 提取混合内容
- ✓ 文本标准化
- ✓ 中文支持
- ✓ 计算内容频率
- ✓ 内容分类
- ✓ 自定义阈值
- ✓ 完整分析流程
- ✓ 空内容处理
- ✓ 嵌套列表

## 设计原则

- **精确提取**: 准确识别markdown的各种结构
- **智能分类**: 基于频率自动分类内容
- **灵活配置**: 支持自定义阈值
- **中文支持**: 正确处理中文字符
- **错误容忍**: 优雅处理各种边界情况

## 文件结构

```
skills/template-content-analyzer/
├── lib/
│   └── content-analyzer.js    # 内容分析器
├── test/
│   └── content-analyzer.test.js  # 单元测试
├── README.md
├── package.json
└── skill.json
```

## 下一步

- [x] 实现 `extractContentBlocks()` 方法
- [x] 实现 `normalizeText()` 方法
- [x] 实现 `calculateFrequency()` 方法
- [x] 实现 `classifyContent()` 方法
- [x] 实现 `analyzeTemplate()` 方法
- [x] 实现数据结构识别（表格、代码块、列表）
- [x] 实现清洗规则生成
- [x] 实现报告生成（JSON和Markdown格式）
- [x] 实现清洗前后对比示例
- [x] 单元测试
- [ ] 实现配置生成器
- [ ] 创建主入口文件 `main.js`
- [ ] 集成到完整的分析工作流

## 报告生成

### `generateAnalysisJSON(analysisResult, urlPattern, options)`

生成JSON格式的分析报告。

**参数:**
- `analysisResult` (Object): 分析结果（来自analyzeTemplate）
- `urlPattern` (Object): URL模式信息
  - `name` (string): 模式名称
  - `pathTemplate` (string): 路径模板
  - `pattern` (string): 正则表达式
  - `queryParams` (Array): 查询参数列表
  - `urlCount` (number): URL数量
- `options` (Object): 选项（可选）

**返回:**
- `Object`: JSON格式的报告，包含:
  - `templateName`: 模板名称
  - `urlPattern`: URL模式信息
  - `metadata`: 元数据（生成时间、页面数、版本）
  - `statistics`: 统计信息
  - `contentClassification`: 内容分类（template, unique, mixed）
  - `dataStructures`: 数据结构（tables, codeBlocks, lists）
  - `cleaningRules`: 清洗规则

**示例:**
```javascript
const analysisResult = analyzer.analyzeTemplate(pages);
const urlPattern = {
  name: 'api-doc',
  pathTemplate: '/open/api/doc',
  pattern: '^https://www\\.lixinger\\.com/open/api/doc\\?api-key=(.+)$',
  queryParams: ['api-key'],
  urlCount: 163
};

const jsonReport = analyzer.generateAnalysisJSON(analysisResult, urlPattern);

// 保存为文件
const fs = require('fs').promises;
await fs.writeFile('analysis-report.json', JSON.stringify(jsonReport, null, 2));
```

### `generateAnalysisMarkdown(analysisResult, urlPattern, options)`

生成Markdown格式的分析报告。

**参数:**
- `analysisResult` (Object): 分析结果（来自analyzeTemplate）
- `urlPattern` (Object): URL模式信息
- `options` (Object): 选项（可选）

**返回:**
- `string`: Markdown格式的报告

**报告包含:**
- 标题和基本信息
- 统计概览表格
- 模板内容（噪音）列表
- 独特内容（数据）列表
- 数据结构详情（表格、代码块、列表）
- 清洗规则摘要
- 建议

**示例:**
```javascript
const markdownReport = analyzer.generateAnalysisMarkdown(analysisResult, urlPattern);

// 保存为文件
const fs = require('fs').promises;
await fs.writeFile('analysis-report.md', markdownReport);
```

### `generateCleaningExamples(pages, cleaningRules, options)`

生成清洗前后对比示例。

**参数:**
- `pages` (Array<string>): 页面内容数组
- `cleaningRules` (Object): 清洗规则（来自analyzeTemplate）
- `options` (Object): 选项
  - `maxExamples` (number): 最大示例数（默认3）

**返回:**
- `Array<Object>`: 对比示例数组，每个示例包含:
  - `index`: 示例索引
  - `original`: 原始内容（content, length, preview）
  - `cleaned`: 清洗后内容（content, length, preview）
  - `stats`: 统计信息（originalLength, cleanedLength, reduction, removedLength）

**示例:**
```javascript
const cleaningExamples = analyzer.generateCleaningExamples(
  pages, 
  analysisResult.cleaningRules,
  { maxExamples: 3 }
);

cleaningExamples.forEach(example => {
  console.log(`示例 ${example.index}:`);
  console.log(`  原始长度: ${example.stats.originalLength}`);
  console.log(`  清洗后长度: ${example.stats.cleanedLength}`);
  console.log(`  减少: ${example.stats.reduction}`);
});

// 保存为文件
const fs = require('fs').promises;
await fs.writeFile('cleaning-examples.json', JSON.stringify(cleaningExamples, null, 2));
```

## 完整示例

查看 `examples/generate-reports.js` 获取完整的使用示例：

```bash
node examples/generate-reports.js
```

这将生成：
- `analysis-report.json` - JSON格式的分析报告
- `analysis-report.md` - Markdown格式的分析报告
- `cleaning-examples.json` - 清洗前后对比示例


## 配置加载

### ConfigLoader

ConfigLoader 用于从 JSONL 文件加载模板配置并创建 Parser 实例。

#### `loadConfigs(jsonlPath)`

从 JSONL 文件加载所有配置。

**参数:**
- `jsonlPath` (string): JSONL 文件路径

**返回:**
- `Array<Object>`: 配置对象数组

**示例:**
```javascript
const ConfigLoader = require('./lib/config-loader');

const configs = ConfigLoader.loadConfigs('output/my-project/template-rules.jsonl');
console.log(`Loaded ${configs.length} configurations`);
```

#### `loadConfigByName(jsonlPath, name)`

加载指定名称的配置。

**参数:**
- `jsonlPath` (string): JSONL 文件路径
- `name` (string): 配置名称

**返回:**
- `Object|null`: 配置对象，如果未找到则返回 null

**示例:**
```javascript
const config = ConfigLoader.loadConfigByName(
  'output/my-project/template-rules.jsonl',
  'api-doc'
);

if (config) {
  console.log('Found config:', config.name);
}
```

#### `createParsers(jsonlPath, ParserClass)`

创建 Parser 实例数组。

**参数:**
- `jsonlPath` (string): JSONL 文件路径
- `ParserClass` (Class): Parser 类（如 TemplateParser）

**返回:**
- `Array<Parser>`: Parser 实例数组

**示例:**
```javascript
const TemplateParser = require('./lib/template-parser');

const parsers = ConfigLoader.createParsers(
  'output/my-project/template-rules.jsonl',
  TemplateParser
);

console.log(`Created ${parsers.length} parsers`);
```

#### `getConfigStats(jsonlPath)`

获取配置统计信息。

**参数:**
- `jsonlPath` (string): JSONL 文件路径

**返回:**
- `Object`: 统计信息
  - `totalConfigs`: 配置总数
  - `configNames`: 配置名称列表
  - `totalExtractors`: 提取器总数
  - `totalFilters`: 过滤器总数
  - `extractorTypes`: 提取器类型统计
  - `filterTypes`: 过滤器类型统计

**示例:**
```javascript
const stats = ConfigLoader.getConfigStats('output/my-project/template-rules.jsonl');

console.log('Total configs:', stats.totalConfigs);
console.log('Config names:', stats.configNames);
console.log('Total extractors:', stats.totalExtractors);
console.log('Extractor types:', stats.extractorTypes);
```

#### `generateTemplateConfig(urlPattern, analysisResult)`

生成模板配置对象。

**参数:**
- `urlPattern` (Object): URL 模式信息
- `analysisResult` (Object): 模板分析结果

**返回:**
- `Object`: 模板配置对象

**示例:**
```javascript
const urlPattern = {
  name: 'api-doc',
  pathTemplate: '/open/api/doc',
  pattern: '^https://www\\.lixinger\\.com/open/api/doc\\?api-key=(.+)$',
  queryParams: ['api-key']
};

const analysisResult = analyzer.analyzeTemplate(pages);
const config = ConfigLoader.generateTemplateConfig(urlPattern, analysisResult);

console.log('Generated config:', config.name);
```

### TemplateConfigGenerator

TemplateConfigGenerator 是专门用于生成模板配置的类，提供了更细粒度的配置生成控制。

#### `generateConfig(urlPattern, analysisResult)`

生成完整的模板配置对象。

**参数:**
- `urlPattern` (Object): URL 模式信息
  - `name` (string): 模式名称
  - `pattern` (string): 正则表达式
  - `pathTemplate` (string): 路径模板
  - `queryParams` (Array<string>): 查询参数列表
- `analysisResult` (Object): 模板分析结果
  - `stats` (Object): 统计信息
  - `classified` (Object): 分类后的内容
  - `dataStructures` (Object): 数据结构信息
  - `cleaningRules` (Object): 清洗规则

**返回:**
- `Object`: 完整的模板配置对象

**示例:**
```javascript
const TemplateConfigGenerator = require('./lib/template-config-generator');
const generator = new TemplateConfigGenerator();

const config = generator.generateConfig(urlPattern, analysisResult);
console.log('Generated config:', config);
```

#### `generateExtractors(dataStructures, classified)`

生成提取器配置数组。

**参数:**
- `dataStructures` (Object): 数据结构信息
  - `tables` (Array): 表格结构
  - `codeBlocks` (Array): 代码块结构
  - `lists` (Array): 列表结构
- `classified` (Object): 分类后的内容

**返回:**
- `Array<Object>`: 提取器配置数组

**示例:**
```javascript
const extractors = generator.generateExtractors(dataStructures, classified);
console.log('Generated extractors:', extractors.length);
```

#### `generateFilters(cleaningRules, classified)`

生成过滤器配置数组。

**参数:**
- `cleaningRules` (Object): 清洗规则
  - `removePatterns` (Array): 移除模式列表
- `classified` (Object): 分类后的内容
  - `template` (Array): 高频模板内容

**返回:**
- `Array<Object>`: 过滤器配置数组

**示例:**
```javascript
const filters = generator.generateFilters(cleaningRules, classified);
console.log('Generated filters:', filters.length);
```

#### `saveAsJSONL(configs, outputPath)`

保存配置为 JSONL 格式文件。

**参数:**
- `configs` (Array<Object>): 配置对象数组
- `outputPath` (string): 输出文件路径

**返回:**
- `Promise<void>`

**示例:**
```javascript
const configs = [config1, config2, config3];
await generator.saveAsJSONL(configs, 'output/template-rules.jsonl');
console.log('Configs saved successfully');
```

## 模板解析

### TemplateParser

TemplateParser 是配置驱动的模板解析器，基于配置对象进行 URL 匹配和数据提取。

#### 构造函数

```javascript
const TemplateParser = require('./lib/template-parser');

const parser = new TemplateParser(config);
```

**参数:**
- `config` (Object): 模板配置对象

#### `matches(url)`

检查 URL 是否匹配此解析器。

**参数:**
- `url` (string): 页面 URL

**返回:**
- `boolean`: 是否匹配

**示例:**
```javascript
const matches = parser.matches('https://example.com/api/doc');
console.log('Matches:', matches);
```

#### `getPriority()`

获取解析器优先级。

**返回:**
- `number`: 优先级（数字越大优先级越高）

**示例:**
```javascript
const priority = parser.getPriority();
console.log('Priority:', priority);
```

#### `parse(page, url, options)`

解析页面（主入口）。

**参数:**
- `page` (Page): Playwright 页面对象
- `url` (string): 页面 URL
- `options` (Object): 解析选项（可选）

**返回:**
- `Promise<Object>`: 解析后的数据

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

#### `getName()`

获取解析器名称。

**返回:**
- `string`: 名称

**示例:**
```javascript
const name = parser.getName();
console.log('Parser name:', name);
```

#### `getConfig()`

获取配置信息。

**返回:**
- `Object`: 配置对象

**示例:**
```javascript
const config = parser.getConfig();
console.log('Config:', config);
```

### 完整使用示例

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
  'output/lixinger-crawler/template-rules.jsonl'
).then(result => {
  console.log('Result:', JSON.stringify(result, null, 2));
});
```

## 测试脚本

### 测试配置解析

```bash
node scripts/test-config-parsing.js
```

测试配置文件的加载和验证。

### 测试模板解析器

```bash
node scripts/test-template-parser.js
```

测试 TemplateParser 的创建和 URL 匹配。

### 测试真实页面

```bash
node scripts/test-real-pages.js
```

使用真实页面测试配置驱动的解析。

### 测试配置生成

```bash
node scripts/test-generate-config.js
```

测试配置生成功能。

## 相关文档

### 配置文件文档
- **[配置格式说明](./docs/CONFIG_FORMAT.md)** - JSONL 格式和配置对象结构详解
- **[提取器配置指南](./docs/EXTRACTOR_GUIDE.md)** - 如何配置 text、table、code、list 提取器
- **[过滤器配置指南](./docs/FILTER_GUIDE.md)** - 如何配置 remove、keep、transform 过滤器
- **[配置示例](./docs/CONFIG_EXAMPLES.md)** - 各种场景的完整配置示例
- **[使用指南](./docs/USAGE_GUIDE.md)** - 如何加载、使用和调试配置文件

### 脚本文档
- **[脚本说明](./scripts/README.md)** - 所有脚本的使用说明

## 贡献

欢迎贡献！请查看 [贡献指南](../../CONTRIBUTING.md)。

## 许可证

MIT
