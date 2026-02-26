# 常见问题 FAQ

本文档回答关于模板内容分析器的常见问题。

## 目录

- [安装和设置](#安装和设置)
- [使用和工作流](#使用和工作流)
- [配置格式](#配置格式)
- [故障排除](#故障排除)
- [性能优化](#性能优化)
- [集成和扩展](#集成和扩展)

---

## 安装和设置

### Q1: 如何安装模板内容分析器？

**A**: 在项目根目录运行：

```bash
cd skills/template-content-analyzer
npm install
```

依赖项包括：
- `playwright` - 用于浏览器自动化
- `cheerio` - 用于 HTML 解析（可选）

### Q2: 需要什么前置条件？

**A**: 
- Node.js 14+ 
- npm 或 yarn
- 已爬取的 markdown 页面文件
- links.txt 文件（如果使用 url-pattern-analyzer）

### Q3: 如何验证安装成功？

**A**: 运行测试脚本：

```bash
node test/content-analyzer.test.js
node test/config-loader.test.js
node test/template-parser.test.js
```

所有测试应该通过。

### Q4: 可以在现有项目中使用吗？

**A**: 可以。将 `skills/template-content-analyzer` 目录复制到你的项目中，然后：

```javascript
const ContentAnalyzer = require('./skills/template-content-analyzer/lib/content-analyzer');
const analyzer = new ContentAnalyzer();
```

---

## 使用和工作流

### Q5: 完整的工作流程是什么？

**A**: 标准工作流包括 3 个步骤：

```bash
# 步骤 1: 分析 URL 模式（使用 url-pattern-analyzer）
node skills/url-pattern-analyzer/scripts/analyze-url-patterns.js

# 步骤 2: 分析页面模板并生成配置
node skills/template-content-analyzer/scripts/generate-template-config.js

# 步骤 3: 使用配置解析页面
node scripts/test-real-pages.js
```

### Q6: 如何生成模板配置文件？

**A**: 使用生成脚本：

```bash
node scripts/generate-template-config.js \
  --links output/my-project/links.txt \
  --pages output/my-project/pages \
  --output output/my-project/template-rules.jsonl
```

或在代码中：

```javascript
const TemplateConfigGenerator = require('./lib/template-config-generator');
const generator = new TemplateConfigGenerator();

const config = generator.generateConfig(urlPattern, analysisResult);
await generator.saveAsJSONL([config], 'output/template-rules.jsonl');
```

### Q7: 如何使用生成的配置文件？

**A**: 加载配置并创建解析器：

```javascript
const ConfigLoader = require('./lib/config-loader');
const TemplateParser = require('./lib/template-parser');

// 加载配置
const parsers = ConfigLoader.createParsers(
  'output/template-rules.jsonl',
  TemplateParser
);

// 找到匹配的解析器
const parser = parsers.find(p => p.matches(url));

// 解析页面
const result = await parser.parse(page, url);
```

详见 [使用指南](./USAGE_GUIDE.md)。

### Q8: 可以手动编辑配置文件吗？

**A**: 可以。配置文件是 JSONL 格式（每行一个 JSON 对象），可以用任何文本编辑器编辑：

```bash
vim output/template-rules.jsonl
# 或
code output/template-rules.jsonl
```

编辑后验证格式：

```javascript
const configs = ConfigLoader.loadConfigs('output/template-rules.jsonl');
console.log('Valid!');
```

### Q9: 如何调试配置？

**A**: 使用测试脚本：

```bash
# 测试配置加载
node scripts/test-config-parsing.js

# 测试解析器创建
node scripts/test-template-parser.js

# 测试实际页面解析
node scripts/test-real-pages.js
```

在代码中添加日志：

```javascript
const parser = new TemplateParser(config);
console.log('Parser name:', parser.getName());
console.log('URL pattern:', parser.getConfig().urlPattern);
console.log('Extractors:', parser.getConfig().extractors.length);
```

---

## 配置格式

### Q10: 配置文件是什么格式？

**A**: JSONL（JSON Lines）格式，每行一个完整的 JSON 对象：

```jsonl
{"name":"api-doc","description":"API documentation pages","priority":90,"urlPattern":{"pattern":"^https://example\\.com/api/doc","pathTemplate":"/api/doc","queryParams":["api-key"]},"extractors":[{"field":"title","type":"text","selector":"h1, h2, title","required":true}],"filters":[],"metadata":{"generatedAt":"2024-02-25T10:00:00.000Z","pageCount":163,"version":"1.0.0"}}
{"name":"dashboard","description":"Dashboard pages","priority":80,"urlPattern":{"pattern":"^https://example\\.com/dashboard","pathTemplate":"/dashboard","queryParams":[]},"extractors":[{"field":"metrics","type":"table","selector":"table.metrics","required":true}],"filters":[],"metadata":{"generatedAt":"2024-02-25T10:00:00.000Z","pageCount":50,"version":"1.0.0"}}
```

详见 [配置格式说明](./CONFIG_FORMAT.md)。

### Q11: 支持哪些提取器类型？

**A**: 支持 4 种提取器类型：

1. **text** - 提取文本内容
2. **table** - 提取表格数据
3. **code** - 提取代码块
4. **list** - 提取列表项

详见 [提取器配置指南](./EXTRACTOR_GUIDE.md)。

### Q12: 支持哪些过滤器类型？

**A**: 支持 3 种过滤器类型：

1. **remove** - 移除匹配的内容
2. **keep** - 只保留匹配的内容
3. **transform** - 转换内容

详见 [过滤器配置指南](./FILTER_GUIDE.md)。

### Q13: 如何配置 CSS 选择器？

**A**: 使用标准 CSS 选择器语法：

```javascript
{
  "field": "title",
  "type": "text",
  "selector": "h1, h2, title",  // 多个选择器用逗号分隔
  "required": true
}
```

常用选择器：
- `h1` - 标签选择器
- `.class-name` - 类选择器
- `#id` - ID 选择器
- `div > p` - 子元素选择器
- `table.data` - 组合选择器

在浏览器开发者工具中测试：

```javascript
document.querySelector('h1, h2, title')
document.querySelectorAll('table')
```

### Q14: 如何处理动态内容？

**A**: 使用 Playwright 的等待功能：

```javascript
// 在解析前等待元素出现
await page.waitForSelector('div.content');

// 或等待网络空闲
await page.goto(url, { waitUntil: 'networkidle' });

// 或等待特定时间
await page.waitForTimeout(1000);
```

---

## 故障排除

### Q15: 配置文件加载失败怎么办？

**A**: 检查以下几点：

1. **文件路径是否正确**：
```javascript
const fs = require('fs');
console.log(fs.existsSync('path/to/file.jsonl')); // 应该是 true
```

2. **JSON 格式是否正确**：
```bash
# 验证每行 JSON
node -e "require('fs').readFileSync('file.jsonl', 'utf-8').split('\n').forEach((line, i) => { if (line.trim()) { try { JSON.parse(line); console.log('Line', i+1, 'OK'); } catch(e) { console.error('Line', i+1, 'ERROR:', e.message); } } })"
```

3. **是否有语法错误**：
- 缺少引号
- 缺少逗号
- 括号不匹配

### Q16: 找不到匹配的解析器怎么办？

**A**: 检查 URL 模式：

```javascript
const parser = new TemplateParser(config);
const url = 'https://example.com/api/doc';

// 测试匹配
console.log('Pattern:', config.urlPattern.pattern);
console.log('Matches:', parser.matches(url));

// 测试正则表达式
const pattern = new RegExp(config.urlPattern.pattern);
console.log('Regex test:', pattern.test(url));
```

常见问题：
- 特殊字符未转义（`.` 应该写成 `\\.`）
- 正则表达式语法错误
- URL 格式不匹配

### Q17: 提取器返回空值怎么办？

**A**: 调试步骤：

1. **在浏览器中测试选择器**：
```javascript
// 在浏览器控制台
document.querySelector('h1, h2, title')
```

2. **检查元素是否存在**：
```javascript
const element = await page.$('h1');
console.log('Element exists:', !!element);
```

3. **检查元素内容**：
```javascript
const text = await page.$eval('h1', el => el.textContent);
console.log('Text:', text);
```

4. **添加等待**：
```javascript
await page.waitForSelector('h1');
const text = await page.$eval('h1', el => el.textContent);
```

### Q18: 表格提取不完整怎么办？

**A**: 检查表格结构：

```javascript
// 查看表格 HTML
const tableHTML = await page.$eval('table', el => el.outerHTML);
console.log(tableHTML);

// 检查是否有 thead 和 tbody
const hasHeader = await page.$('table thead');
const hasBody = await page.$('table tbody');
console.log('Has header:', !!hasHeader);
console.log('Has body:', !!hasBody);
```

常见问题：
- 表格没有 `<thead>` 或 `<tbody>`
- 选择器匹配了错误的表格
- 表格是动态生成的（需要等待）

### Q19: 代码块语言识别错误怎么办？

**A**: 检查代码块的 class 属性：

```javascript
// 查看代码块 HTML
const codeHTML = await page.$eval('pre code', el => el.outerHTML);
console.log(codeHTML);

// 检查 class 属性
const className = await page.$eval('pre code', el => el.className);
console.log('Class:', className);
```

代码块应该有 `class="language-xxx"` 属性：

```html
<pre><code class="language-javascript">
console.log('hello');
</code></pre>
```

### Q20: 过滤器不生效怎么办？

**A**: 当前实现中过滤器功能尚未完全实现。如需使用，需要扩展 `TemplateParser.applyFilters` 方法：

```javascript
applyFilters(data) {
  for (const filter of this.config.filters) {
    if (filter.type === 'remove') {
      // 实现移除逻辑
      data = this.removeFilter(data, filter);
    } else if (filter.type === 'keep') {
      // 实现保留逻辑
      data = this.keepFilter(data, filter);
    } else if (filter.type === 'transform') {
      // 实现转换逻辑
      data = this.transformFilter(data, filter);
    }
  }
  return data;
}
```

---

## 性能优化

### Q21: 如何提高分析速度？

**A**: 优化建议：

1. **批量处理**：
```javascript
const batchSize = 10;
for (let i = 0; i < pages.length; i += batchSize) {
  const batch = pages.slice(i, i + batchSize);
  await Promise.all(batch.map(page => analyzePage(page)));
}
```

2. **使用缓存**：
```javascript
const cache = new Map();
function analyzeWithCache(page) {
  const key = page.url;
  if (cache.has(key)) {
    return cache.get(key);
  }
  const result = analyzer.analyzeTemplate([page]);
  cache.set(key, result);
  return result;
}
```

3. **减少等待时间**：
```javascript
// 使用更快的等待策略
await page.goto(url, { waitUntil: 'domcontentloaded' });
```

### Q22: 配置文件太大怎么办？

**A**: 优化策略：

1. **分割为多个文件**：
```javascript
// 按网站分割
const configs1 = ConfigLoader.loadConfigs('site1-rules.jsonl');
const configs2 = ConfigLoader.loadConfigs('site2-rules.jsonl');
const allConfigs = [...configs1, ...configs2];
```

2. **只加载需要的配置**：
```javascript
const config = ConfigLoader.loadConfigByName('rules.jsonl', 'api-doc');
const parser = new TemplateParser(config);
```

3. **压缩配置文件**：
```bash
gzip template-rules.jsonl
```

### Q23: 如何减少内存使用？

**A**: 内存优化：

1. **流式处理页面**：
```javascript
async function* pageGenerator(files) {
  for (const file of files) {
    yield await fs.readFile(file, 'utf-8');
  }
}

for await (const page of pageGenerator(files)) {
  const result = analyzer.analyzeTemplate([page]);
  // 处理结果
}
```

2. **及时释放资源**：
```javascript
const browser = await chromium.launch();
try {
  const page = await browser.newPage();
  const result = await parser.parse(page, url);
  await page.close(); // 关闭页面
  return result;
} finally {
  await browser.close(); // 关闭浏览器
}
```

3. **限制并发数**：
```javascript
const pLimit = require('p-limit');
const limit = pLimit(5); // 最多 5 个并发

const promises = urls.map(url => 
  limit(() => parsePage(url))
);
await Promise.all(promises);
```

### Q24: 如何监控性能？

**A**: 添加性能监控：

```javascript
const startTime = Date.now();

const result = await parser.parse(page, url);

const duration = Date.now() - startTime;
console.log(`Parsed in ${duration}ms`);

// 记录到文件
fs.appendFileSync('performance.log', 
  `${url},${duration},${Date.now()}\n`
);
```

---

## 集成和扩展

### Q25: 如何集成到现有爬虫系统？

**A**: 在爬虫主程序中加载配置：

```javascript
// 在 crawler-main.js 中
const ConfigLoader = require('./skills/template-content-analyzer/lib/config-loader');
const TemplateParser = require('./skills/template-content-analyzer/lib/template-parser');

// 加载配置
const configPath = path.join(outputDir, 'template-rules.jsonl');
if (fs.existsSync(configPath)) {
  const templateParsers = ConfigLoader.createParsers(configPath, TemplateParser);
  
  // 添加到现有 parsers 数组
  parsers.push(...templateParsers);
  
  console.log(`Loaded ${templateParsers.length} template parsers`);
}

// 使用时自动匹配
for (const url of urls) {
  const parser = parsers.find(p => p.matches(url));
  if (parser) {
    const result = await parser.parse(page, url);
    // 保存结果
  }
}
```

### Q26: 如何扩展提取器类型？

**A**: 在 `TemplateParser` 中添加新的提取方法：

```javascript
class TemplateParser {
  async executeExtractor(page, extractor) {
    switch (extractor.type) {
      case 'text':
        return await this.extractText(page, extractor);
      case 'table':
        return await this.extractTable(page, extractor);
      case 'code':
        return await this.extractCode(page, extractor);
      case 'list':
        return await this.extractList(page, extractor);
      case 'image':  // 新类型
        return await this.extractImage(page, extractor);
      default:
        throw new Error(`Unknown extractor type: ${extractor.type}`);
    }
  }

  async extractImage(page, extractor) {
    const images = await page.$$eval(extractor.selector, imgs => 
      imgs.map(img => ({
        src: img.src,
        alt: img.alt,
        width: img.width,
        height: img.height
      }))
    );
    return images;
  }
}
```

### Q27: 如何添加自定义过滤器？

**A**: 扩展 `applyFilters` 方法：

```javascript
applyFilters(data) {
  for (const filter of this.config.filters) {
    if (filter.type === 'custom') {
      // 自定义过滤逻辑
      data = this.customFilter(data, filter);
    }
  }
  return data;
}

customFilter(data, filter) {
  // 实现自定义过滤逻辑
  if (filter.action === 'uppercase') {
    Object.keys(data).forEach(key => {
      if (typeof data[key] === 'string') {
        data[key] = data[key].toUpperCase();
      }
    });
  }
  return data;
}
```

### Q28: 如何支持多网站？

**A**: 为每个网站创建独立的配置文件：

```
output/
├── site1/
│   ├── links.txt
│   ├── pages/
│   └── template-rules.jsonl
├── site2/
│   ├── links.txt
│   ├── pages/
│   └── template-rules.jsonl
└── site3/
    ├── links.txt
    ├── pages/
    └── template-rules.jsonl
```

加载时合并：

```javascript
const sites = ['site1', 'site2', 'site3'];
const allParsers = [];

for (const site of sites) {
  const configPath = `output/${site}/template-rules.jsonl`;
  if (fs.existsSync(configPath)) {
    const parsers = ConfigLoader.createParsers(configPath, TemplateParser);
    allParsers.push(...parsers);
  }
}

console.log(`Loaded ${allParsers.length} parsers from ${sites.length} sites`);
```

### Q29: 如何导出为其他格式？

**A**: 实现格式转换：

```javascript
// JSONL 转 JSON
function jsonlToJson(jsonlPath, jsonPath) {
  const configs = ConfigLoader.loadConfigs(jsonlPath);
  fs.writeFileSync(jsonPath, JSON.stringify(configs, null, 2));
}

// JSONL 转 YAML
function jsonlToYaml(jsonlPath, yamlPath) {
  const yaml = require('js-yaml');
  const configs = ConfigLoader.loadConfigs(jsonlPath);
  const yamlStr = yaml.dump(configs);
  fs.writeFileSync(yamlPath, yamlStr);
}

// 使用
jsonlToJson('template-rules.jsonl', 'template-rules.json');
jsonlToYaml('template-rules.jsonl', 'template-rules.yaml');
```

### Q30: 如何与大模型集成？

**A**: 配置文件设计为易于大模型理解和修改：

```javascript
// 1. 读取配置
const configs = ConfigLoader.loadConfigs('template-rules.jsonl');

// 2. 转换为易读格式
const readableConfig = JSON.stringify(configs, null, 2);

// 3. 发送给大模型
const prompt = `
请修改以下配置，添加一个新的提取器来提取"响应示例"字段：

${readableConfig}

要求：
- 使用 code 类型
- 选择器为 "pre.response-example code"
- 字段名为 "responseExample"
`;

// 4. 接收大模型的修改
const modifiedConfig = JSON.parse(llmResponse);

// 5. 保存回 JSONL
const generator = new TemplateConfigGenerator();
await generator.saveAsJSONL([modifiedConfig], 'template-rules.jsonl');
```

---

## 相关资源

### 文档
- [配置格式说明](./CONFIG_FORMAT.md) - 完整的配置格式
- [提取器配置指南](./EXTRACTOR_GUIDE.md) - 提取器详细说明
- [过滤器配置指南](./FILTER_GUIDE.md) - 过滤器详细说明
- [配置示例](./CONFIG_EXAMPLES.md) - 各种场景的示例
- [使用指南](./USAGE_GUIDE.md) - 如何使用配置文件
- [主文档](../README.md) - 项目概述

### 脚本
- [脚本说明](../scripts/README.md) - 所有脚本的使用说明

### 测试
- [单元测试](../test/) - 完整的测试套件

### 示例
- [配置示例](../examples/) - 实际的配置文件和报告

---

## 获取帮助

如果你的问题没有在这里得到解答：

1. **查看文档** - 阅读完整的文档了解更多细节
2. **运行测试** - 测试脚本可以帮助诊断问题
3. **查看示例** - 示例代码展示了最佳实践
4. **提交 Issue** - 在 GitHub 上提交问题
5. **联系维护者** - 通过邮件或其他方式联系

---

**最后更新**: 2024-02-25  
**版本**: 1.0.0
