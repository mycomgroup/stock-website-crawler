# 使用指南

本指南介绍如何使用模板配置文件进行页面解析。

## 目录

1. [快速开始](#快速开始)
2. [加载配置](#加载配置)
3. [创建解析器](#创建解析器)
4. [解析页面](#解析页面)
5. [修改配置](#修改配置)
6. [调试配置](#调试配置)
7. [常见问题](#常见问题)

## 快速开始

### 1. 准备配置文件

创建或生成 JSONL 格式的配置文件：

```bash
# 使用生成脚本
node scripts/generate-template-config.js

# 或手动创建
touch output/my-project/template-rules.jsonl
```

### 2. 加载配置

```javascript
const ConfigLoader = require('./lib/config-loader');

// 加载所有配置
const configs = ConfigLoader.loadConfigs('output/my-project/template-rules.jsonl');
console.log(`Loaded ${configs.length} configurations`);

// 查看配置统计
const stats = ConfigLoader.getConfigStats('output/my-project/template-rules.jsonl');
console.log('Config stats:', stats);
```

### 3. 创建解析器

```javascript
const TemplateParser = require('./lib/template-parser');

// 创建解析器实例
const parsers = ConfigLoader.createParsers(
  'output/my-project/template-rules.jsonl',
  TemplateParser
);

console.log(`Created ${parsers.length} parsers`);
```

### 4. 解析页面

```javascript
const { chromium } = require('playwright');

async function parsePage(url) {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto(url);

  // 找到匹配的解析器
  const parser = parsers.find(p => p.matches(url));
  if (!parser) {
    console.log('No parser found for URL:', url);
    return null;
  }

  // 解析页面
  const result = await parser.parse(page, url);
  console.log('Parsed result:', result);

  await browser.close();
  return result;
}

// 使用
parsePage('https://example.com/page').then(result => {
  console.log(JSON.stringify(result, null, 2));
});
```

## 加载配置

### 加载所有配置

```javascript
const ConfigLoader = require('./lib/config-loader');

try {
  const configs = ConfigLoader.loadConfigs('path/to/template-rules.jsonl');
  console.log(`Successfully loaded ${configs.length} configurations`);
} catch (error) {
  console.error('Failed to load configs:', error.message);
}
```

### 加载单个配置

```javascript
const config = ConfigLoader.loadConfigByName(
  'path/to/template-rules.jsonl',
  'api-doc'
);

if (config) {
  console.log('Found config:', config.name);
} else {
  console.log('Config not found');
}
```

### 获取配置统计

```javascript
const stats = ConfigLoader.getConfigStats('path/to/template-rules.jsonl');

console.log('Total configs:', stats.totalConfigs);
console.log('Config names:', stats.configNames);
console.log('Total extractors:', stats.totalExtractors);
console.log('Total filters:', stats.totalFilters);
console.log('Extractor types:', stats.extractorTypes);
console.log('Filter types:', stats.filterTypes);
```

输出示例：
```
Total configs: 2
Config names: [ 'api-doc', 'dashboard' ]
Total extractors: 9
Total filters: 2
Extractor types: { text: 4, table: 3, code: 2 }
Filter types: { remove: 2 }
```

## 创建解析器

### 创建所有解析器

```javascript
const TemplateParser = require('./lib/template-parser');
const ConfigLoader = require('./lib/config-loader');

const parsers = ConfigLoader.createParsers(
  'path/to/template-rules.jsonl',
  TemplateParser
);

console.log(`Created ${parsers.length} parsers`);
```

### 创建单个解析器

```javascript
const config = ConfigLoader.loadConfigByName(
  'path/to/template-rules.jsonl',
  'api-doc'
);

const parser = new TemplateParser(config);
console.log('Parser created:', parser.getName());
```

### 按优先级排序

```javascript
const parsers = ConfigLoader.createParsers(
  'path/to/template-rules.jsonl',
  TemplateParser
);

// 按优先级降序排序
parsers.sort((a, b) => b.getPriority() - a.getPriority());

console.log('Parsers by priority:');
parsers.forEach(p => {
  console.log(`  ${p.getName()}: ${p.getPriority()}`);
});
```

## 解析页面

### 基本解析

```javascript
const { chromium } = require('playwright');

async function parseWithConfig(url, configPath) {
  // 加载解析器
  const parsers = ConfigLoader.createParsers(configPath, TemplateParser);
  
  // 找到匹配的解析器
  const parser = parsers.find(p => p.matches(url));
  if (!parser) {
    throw new Error(`No parser found for URL: ${url}`);
  }

  console.log(`Using parser: ${parser.getName()}`);

  // 启动浏览器
  const browser = await chromium.launch();
  const page = await browser.newPage();
  
  try {
    // 访问页面
    await page.goto(url, { waitUntil: 'networkidle' });
    
    // 解析页面
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

### 批量解析

```javascript
async function parseMultiplePages(urls, configPath) {
  const parsers = ConfigLoader.createParsers(configPath, TemplateParser);
  const browser = await chromium.launch();
  const results = [];

  for (const url of urls) {
    const parser = parsers.find(p => p.matches(url));
    if (!parser) {
      console.log(`No parser for: ${url}`);
      continue;
    }

    const page = await browser.newPage();
    try {
      await page.goto(url, { waitUntil: 'networkidle' });
      const result = await parser.parse(page, url);
      results.push(result);
    } catch (error) {
      console.error(`Failed to parse ${url}:`, error.message);
    } finally {
      await page.close();
    }
  }

  await browser.close();
  return results;
}

// 使用
const urls = [
  'https://example.com/api/doc1',
  'https://example.com/api/doc2',
  'https://example.com/dashboard'
];

parseMultiplePages(urls, 'path/to/template-rules.jsonl').then(results => {
  console.log(`Parsed ${results.length} pages`);
  results.forEach(r => console.log(r.type, r.title));
});
```

### 处理解析错误

```javascript
async function safeParseWithConfig(url, configPath) {
  try {
    const result = await parseWithConfig(url, configPath);
    
    // 检查是否有错误
    if (result.error) {
      console.error('Parse error:', result.error);
      return null;
    }
    
    // 检查必需字段
    if (!result.title) {
      console.warn('Missing required field: title');
    }
    
    return result;
  } catch (error) {
    console.error('Failed to parse:', error.message);
    return null;
  }
}
```

## 修改配置

### 手动编辑

配置文件是 JSONL 格式，可以直接编辑：

```bash
# 使用文本编辑器
vim output/my-project/template-rules.jsonl

# 或使用 VS Code
code output/my-project/template-rules.jsonl
```

### 添加新配置

在文件末尾添加新行：

```jsonl
{"name":"new-parser","description":"New parser","priority":80,"urlPattern":{"pattern":"^https://example\\.com/new","pathTemplate":"/new","queryParams":[]},"extractors":[{"field":"title","type":"text","selector":"h1","required":true}],"filters":[],"metadata":{"generatedAt":"2024-02-25T10:00:00.000Z","pageCount":10,"version":"1.0.0"}}
```

### 修改现有配置

1. 找到要修改的配置行
2. 编辑 JSON 对象
3. 保存文件
4. 重新加载配置

### 使用大模型修改

配置文件设计为易于大模型理解和修改：

```
请修改 template-rules.jsonl 中的 api-doc 配置，
添加一个新的提取器来提取 "响应示例" 字段，
使用 code 类型，选择器为 "pre.response-example code"
```

### 验证修改

修改后使用 ConfigLoader 验证：

```javascript
try {
  const configs = ConfigLoader.loadConfigs('path/to/template-rules.jsonl');
  console.log('Configuration is valid');
} catch (error) {
  console.error('Configuration error:', error.message);
}
```

## 调试配置

### 1. 测试配置加载

```bash
node scripts/test-config-parsing.js
```

### 2. 测试解析器创建

```javascript
const configs = ConfigLoader.loadConfigs('path/to/template-rules.jsonl');
configs.forEach(config => {
  try {
    const parser = new TemplateParser(config);
    console.log(`✓ ${config.name}: OK`);
  } catch (error) {
    console.error(`✗ ${config.name}: ${error.message}`);
  }
});
```

### 3. 测试 URL 匹配

```javascript
const parser = new TemplateParser(config);
const testUrls = [
  'https://example.com/api/doc',
  'https://example.com/dashboard',
  'https://example.com/other'
];

testUrls.forEach(url => {
  const matches = parser.matches(url);
  console.log(`${url}: ${matches ? '✓' : '✗'}`);
});
```

### 4. 测试提取器

```bash
# 使用真实页面测试
node scripts/test-real-pages.js
```

### 5. 查看提取结果

```javascript
const result = await parser.parse(page, url);

// 查看所有字段
console.log('Fields:', Object.keys(result));

// 查看每个字段的值
Object.entries(result).forEach(([key, value]) => {
  console.log(`${key}:`, typeof value, Array.isArray(value) ? `[${value.length}]` : '');
});
```

### 6. 调试选择器

在浏览器开发者工具中测试选择器：

```javascript
// 在浏览器控制台中
document.querySelector('h1, h2, title')
document.querySelectorAll('table')
```

### 7. 添加日志

在 TemplateParser 中添加日志：

```javascript
async parse(page, url, options = {}) {
  console.log(`Parsing ${this.name} for ${url}`);
  
  for (const extractor of this.config.extractors) {
    console.log(`  Extracting ${extractor.field} (${extractor.type})`);
    const value = await this.executeExtractor(page, extractor);
    console.log(`    Result:`, value);
  }
  
  // ...
}
```

## 常见问题

### Q: 配置文件加载失败

**A**: 检查以下几点：
1. 文件路径是否正确
2. 文件是否存在
3. JSON 格式是否正确（每行一个完整的 JSON 对象）
4. 是否有语法错误（缺少引号、逗号等）

```bash
# 验证 JSON 格式
node -e "require('fs').readFileSync('path/to/file.jsonl', 'utf-8').split('\n').forEach((line, i) => { if (line.trim()) JSON.parse(line); console.log('Line', i+1, 'OK'); })"
```

### Q: 找不到匹配的解析器

**A**: 检查 URL 模式：
1. 正则表达式是否正确
2. 特殊字符是否转义（`.` 应该写成 `\\.`）
3. 使用测试脚本验证匹配

```javascript
const pattern = new RegExp(config.urlPattern.pattern);
console.log(pattern.test(url));
```

### Q: 提取器返回空值

**A**: 检查选择器：
1. 在浏览器开发者工具中测试选择器
2. 确认元素是否存在
3. 确认元素是否在页面加载后才出现（需要等待）
4. 检查选择器语法是否正确

### Q: 表格提取不完整

**A**: 检查表格结构：
1. 确认表格是否有 `<thead>` 和 `<tbody>`
2. 检查选择器是否匹配正确的表格
3. 查看提取结果的 `headers` 和 `rows`

### Q: 代码块语言识别错误

**A**: 检查代码块结构：
1. 确认是否有 `class="language-xxx"` 属性
2. 手动指定语言（未来功能）
3. 检查代码内容格式

### Q: 过滤器不生效

**A**: 当前实现中过滤器功能尚未完全实现。如需使用，需要扩展 `TemplateParser.applyFilters` 方法。

### Q: 如何处理动态内容

**A**: 使用 Playwright 的等待功能：

```javascript
// 等待元素出现
await page.waitForSelector('div.content');

// 等待网络空闲
await page.goto(url, { waitUntil: 'networkidle' });

// 等待特定时间
await page.waitForTimeout(1000);
```

### Q: 如何提取元素属性

**A**: 当前实现提取 `textContent`。如需属性，可以修改提取器：

```javascript
// 在 extractText 方法中
const text = await page.evaluate((selector, attr) => {
  const element = document.querySelector(selector);
  return attr ? element?.getAttribute(attr) : element?.textContent.trim();
}, extractor.selector, extractor.attribute);
```

### Q: 配置文件太大怎么办

**A**: 
1. 分割为多个文件
2. 只加载需要的配置
3. 使用流式处理（未来功能）

### Q: 如何集成到现有爬虫

**A**: 在爬虫主程序中加载配置：

```javascript
// 在 crawler-main.js 中
const configPath = path.join(outputDir, 'template-rules.jsonl');
if (fs.existsSync(configPath)) {
  const templateParsers = ConfigLoader.createParsers(configPath, TemplateParser);
  parsers.push(...templateParsers);
  console.log(`Loaded ${templateParsers.length} template parsers`);
}
```

## 测试脚本

### 测试配置解析

```bash
node scripts/test-config-parsing.js
```

### 测试模板解析器

```bash
node scripts/test-template-parser.js
```

### 测试真实页面

```bash
node scripts/test-real-pages.js
```

### 测试配置生成

```bash
node scripts/test-generate-config.js
```

## 相关文档

- [配置格式说明](./CONFIG_FORMAT.md) - 完整的配置格式
- [提取器配置指南](./EXTRACTOR_GUIDE.md) - 提取器详细说明
- [过滤器配置指南](./FILTER_GUIDE.md) - 过滤器详细说明
- [配置示例](./CONFIG_EXAMPLES.md) - 各种场景的示例
- [主文档](../README.md) - 项目概述

## 下一步

1. 阅读 [配置格式说明](./CONFIG_FORMAT.md) 了解配置结构
2. 查看 [配置示例](./CONFIG_EXAMPLES.md) 学习实际用法
3. 使用测试脚本验证配置
4. 根据需求修改和优化配置
