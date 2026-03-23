# HAR 自动化请求生成系统

## 概述

本文档介绍如何将 Playwright 浏览器抓取自动转换为高性能的直接 HTTP 请求，实现去浏览器化的批量数据采集。

## 核心思路

```
Playwright 成功 ≠ 数据必须浏览器渲染

实际流程：
HTML 外壳 → JS 发起 XHR/fetch → 调用 API → 返回 JSON → 前端渲染

优化目标：
找到真实 API 请求 → 复刻请求参数 → 直接调用 API
```

## 方案架构

### 方案一：HAR 自动录制与解析（推荐）

#### 1. 自动录制 HAR

```javascript
// scripts/record-har.js
const { chromium } = require('playwright');

async function recordHAR(url, outputPath) {
  const browser = await chromium.launch();
  
  const context = await browser.newContext({
    recordHar: { path: outputPath }
  });
  
  const page = await context.newPage();
  await page.goto(url);
  await page.waitForLoadState('networkidle');
  
  // 等待可能的异步请求
  await page.waitForTimeout(2000);
  
  await context.close();
  await browser.close();
  
  console.log(`HAR 已保存到: ${outputPath}`);
}

// 使用示例
recordHAR('https://example.com/data', 'output/site.har');
```

#### 2. 解析 HAR 提取 API

```javascript
// lib/har-parser.js
const fs = require('fs');

class HARParser {
  constructor(harPath) {
    this.har = JSON.parse(fs.readFileSync(harPath, 'utf8'));
    this.entries = this.har.log.entries;
  }

  // 筛选数据接口
  extractDataAPIs() {
    return this.entries.filter(entry => {
      const url = entry.request.url;
      const mimeType = entry.response.content.mimeType || '';
      
      // 判断条件
      return (
        mimeType.includes('json') ||
        url.includes('/api/') ||
        url.includes('/data/') ||
        this.isGraphQL(entry)
      );
    });
  }

  // 识别 GraphQL
  isGraphQL(entry) {
    const url = entry.request.url;
    const postData = entry.request.postData?.text || '';
    
    return url.includes('graphql') || 
           postData.includes('"query"');
  }

  // 提取请求详情
  extractRequestDetails(entry) {
    const req = entry.request;
    
    return {
      method: req.method,
      url: req.url,
      headers: this.cleanHeaders(req.headers),
      queryParams: req.queryString,
      postData: req.postData?.text,
      response: entry.response.content.text
    };
  }

  // 清理 headers（移除不必要的）
  cleanHeaders(headers) {
    const exclude = [
      'content-length',
      'connection',
      'accept-encoding'
    ];
    
    return headers
      .filter(h => !exclude.includes(h.name.toLowerCase()))
      .reduce((obj, h) => {
        obj[h.name] = h.value;
        return obj;
      }, {});
  }

  // 分类接口
  categorizeAPIs() {
    const apis = this.extractDataAPIs();
    
    return {
      rest: apis.filter(e => !this.isGraphQL(e)),
      graphql: apis.filter(e => this.isGraphQL(e)),
      total: apis.length
    };
  }
}

module.exports = HARParser;
```

#### 3. 自动生成 requests 代码

```javascript
// lib/request-generator.js
class RequestGenerator {
  constructor(harParser) {
    this.parser = harParser;
  }

  // 生成 Python requests 代码
  generatePythonCode(entry) {
    const details = this.parser.extractRequestDetails(entry);
    const method = details.method.toLowerCase();
    
    let code = `import requests\n\n`;
    code += `# ${details.url}\n`;
    code += `headers = ${this.formatPythonDict(details.headers)}\n\n`;
    
    if (method === 'get') {
      code += `response = requests.get(\n`;
      code += `    "${details.url}",\n`;
      code += `    headers=headers\n`;
      code += `)\n`;
    } else if (method === 'post') {
      code += `data = ${this.formatPostData(details.postData)}\n\n`;
      code += `response = requests.post(\n`;
      code += `    "${details.url}",\n`;
      code += `    headers=headers,\n`;
      code += `    json=data\n`;
      code += `)\n`;
    }
    
    code += `\nprint(response.json())\n`;
    
    return code;
  }

  // 生成 Node.js axios 代码
  generateNodeCode(entry) {
    const details = this.parser.extractRequestDetails(entry);
    const method = details.method.toLowerCase();
    
    let code = `const axios = require('axios');\n\n`;
    code += `// ${details.url}\n`;
    code += `const config = {\n`;
    code += `  method: '${method}',\n`;
    code += `  url: '${details.url}',\n`;
    code += `  headers: ${JSON.stringify(details.headers, null, 2)}\n`;
    
    if (details.postData) {
      code += `,\n  data: ${details.postData}\n`;
    }
    
    code += `};\n\n`;
    code += `axios(config)\n`;
    code += `  .then(response => console.log(response.data))\n`;
    code += `  .catch(error => console.error(error));\n`;
    
    return code;
  }

  // 生成 curl 命令
  generateCurlCommand(entry) {
    const details = this.parser.extractRequestDetails(entry);
    
    let cmd = `curl -X ${details.method} '${details.url}'`;
    
    Object.entries(details.headers).forEach(([key, value]) => {
      cmd += ` \\\n  -H '${key}: ${value}'`;
    });
    
    if (details.postData) {
      cmd += ` \\\n  -d '${details.postData}'`;
    }
    
    return cmd;
  }

  formatPythonDict(obj) {
    return JSON.stringify(obj, null, 2)
      .replace(/"/g, "'")
      .replace(/: /g, ': ');
  }

  formatPostData(postData) {
    if (!postData) return '{}';
    try {
      return JSON.stringify(JSON.parse(postData), null, 2);
    } catch {
      return `"${postData}"`;
    }
  }

  // 批量生成所有接口代码
  generateAll(format = 'python') {
    const apis = this.parser.extractDataAPIs();
    const generators = {
      python: this.generatePythonCode.bind(this),
      node: this.generateNodeCode.bind(this),
      curl: this.generateCurlCommand.bind(this)
    };
    
    return apis.map((entry, index) => ({
      index,
      url: entry.request.url,
      code: generators[format](entry)
    }));
  }
}

module.exports = RequestGenerator;
```

### 方案二：运行时监听（实时抓取）

```javascript
// lib/runtime-interceptor.js
class RuntimeInterceptor {
  constructor(page) {
    this.page = page;
    this.capturedAPIs = [];
  }

  // 启动监听
  async startCapture() {
    this.page.on('response', async (response) => {
      await this.handleResponse(response);
    });
  }

  // 处理响应
  async handleResponse(response) {
    const contentType = response.headers()['content-type'] || '';
    
    if (this.isDataAPI(response.url(), contentType)) {
      const request = response.request();
      
      const apiInfo = {
        url: response.url(),
        method: request.method(),
        headers: request.headers(),
        postData: request.postData(),
        status: response.status(),
        responseBody: await this.safeGetBody(response),
        timestamp: Date.now()
      };
      
      this.capturedAPIs.push(apiInfo);
      console.log(`[API] ${apiInfo.method} ${apiInfo.url}`);
    }
  }

  // 判断是否为数据接口
  isDataAPI(url, contentType) {
    return (
      contentType.includes('json') ||
      url.includes('/api/') ||
      url.includes('/data/') ||
      url.includes('graphql')
    );
  }

  // 安全获取响应体
  async safeGetBody(response) {
    try {
      return await response.text();
    } catch (error) {
      return null;
    }
  }

  // 导出捕获的 API
  export(outputPath) {
    const fs = require('fs');
    fs.writeFileSync(
      outputPath,
      JSON.stringify(this.capturedAPIs, null, 2)
    );
    console.log(`已导出 ${this.capturedAPIs.length} 个 API 到 ${outputPath}`);
  }

  // 获取统计信息
  getStats() {
    const methods = {};
    const domains = {};
    
    this.capturedAPIs.forEach(api => {
      methods[api.method] = (methods[api.method] || 0) + 1;
      
      const domain = new URL(api.url).hostname;
      domains[domain] = (domains[domain] || 0) + 1;
    });
    
    return {
      total: this.capturedAPIs.length,
      methods,
      domains
    };
  }
}

module.exports = RuntimeInterceptor;
```

## 完整工作流

### 批量自动化脚本

```javascript
// scripts/auto-extract-apis.js
const { chromium } = require('playwright');
const HARParser = require('../lib/har-parser');
const RequestGenerator = require('../lib/request-generator');
const RuntimeInterceptor = require('../lib/runtime-interceptor');
const fs = require('fs');
const path = require('path');

class APIExtractor {
  constructor(config) {
    this.config = config;
    this.outputDir = config.outputDir || 'output/apis';
  }

  // 方法 1: HAR 方式
  async extractViaHAR(url, name) {
    console.log(`[HAR] 开始抓取: ${url}`);
    
    const harPath = path.join(this.outputDir, `${name}.har`);
    const browser = await chromium.launch();
    
    const context = await browser.newContext({
      recordHar: { path: harPath }
    });
    
    const page = await context.newPage();
    await page.goto(url);
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(2000);
    
    await context.close();
    await browser.close();
    
    // 解析 HAR
    const parser = new HARParser(harPath);
    const generator = new RequestGenerator(parser);
    
    // 生成代码
    const pythonCodes = generator.generateAll('python');
    const nodeCodes = generator.generateAll('node');
    
    // 保存
    this.saveResults(name, {
      python: pythonCodes,
      node: nodeCodes,
      stats: parser.categorizeAPIs()
    });
    
    console.log(`[HAR] 完成: 发现 ${pythonCodes.length} 个 API`);
  }

  // 方法 2: 运行时监听
  async extractViaRuntime(url, name) {
    console.log(`[Runtime] 开始抓取: ${url}`);
    
    const browser = await chromium.launch();
    const page = await browser.newPage();
    
    const interceptor = new RuntimeInterceptor(page);
    await interceptor.startCapture();
    
    await page.goto(url);
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(2000);
    
    // 导出捕获的 API
    const apisPath = path.join(this.outputDir, `${name}-apis.json`);
    interceptor.export(apisPath);
    
    console.log(`[Runtime] 统计:`, interceptor.getStats());
    
    await browser.close();
  }

  // 保存结果
  saveResults(name, results) {
    const dir = path.join(this.outputDir, name);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
    
    // 保存 Python 代码
    results.python.forEach((item, index) => {
      const filename = `api_${index + 1}.py`;
      fs.writeFileSync(
        path.join(dir, filename),
        item.code
      );
    });
    
    // 保存 Node 代码
    results.node.forEach((item, index) => {
      const filename = `api_${index + 1}.js`;
      fs.writeFileSync(
        path.join(dir, filename),
        item.code
      );
    });
    
    // 保存统计
    fs.writeFileSync(
      path.join(dir, 'stats.json'),
      JSON.stringify(results.stats, null, 2)
    );
    
    // 生成索引
    this.generateIndex(dir, results);
  }

  // 生成索引文件
  generateIndex(dir, results) {
    let md = `# API 提取结果\n\n`;
    md += `## 统计\n\n`;
    md += `- 总计: ${results.stats.total} 个接口\n`;
    md += `- REST: ${results.stats.rest.length} 个\n`;
    md += `- GraphQL: ${results.stats.graphql.length} 个\n\n`;
    
    md += `## 接口列表\n\n`;
    results.python.forEach((item, index) => {
      md += `### API ${index + 1}\n\n`;
      md += `- URL: ${item.url}\n`;
      md += `- Python: [api_${index + 1}.py](./api_${index + 1}.py)\n`;
      md += `- Node.js: [api_${index + 1}.js](./api_${index + 1}.js)\n\n`;
    });
    
    fs.writeFileSync(path.join(dir, 'README.md'), md);
  }

  // 批量处理
  async batchExtract(urls) {
    for (const { url, name } of urls) {
      try {
        await this.extractViaHAR(url, name);
      } catch (error) {
        console.error(`[Error] ${name}:`, error.message);
      }
    }
  }
}

// 使用示例
async function main() {
  const extractor = new APIExtractor({
    outputDir: 'output/extracted-apis'
  });

  const urls = [
    { url: 'https://example.com/stocks', name: 'stocks' },
    { url: 'https://example.com/funds', name: 'funds' }
  ];

  await extractor.batchExtract(urls);
}

if (require.main === module) {
  main();
}

module.exports = APIExtractor;
```

## 自动验证与回退

```javascript
// lib/request-validator.js
const axios = require('axios');

class RequestValidator {
  // 测试直接请求是否可行
  async testDirectRequest(apiInfo) {
    try {
      const response = await axios({
        method: apiInfo.method,
        url: apiInfo.url,
        headers: apiInfo.headers,
        data: apiInfo.postData,
        timeout: 10000
      });
      
      return {
        success: true,
        status: response.status,
        canBypassBrowser: true
      };
    } catch (error) {
      return {
        success: false,
        error: error.message,
        canBypassBrowser: false,
        reason: this.diagnoseFailure(error)
      };
    }
  }

  // 诊断失败原因
  diagnoseFailure(error) {
    if (error.response?.status === 403) {
      return 'Anti-bot protection detected';
    }
    if (error.response?.status === 401) {
      return 'Authentication required';
    }
    if (error.message.includes('timeout')) {
      return 'Request timeout';
    }
    return 'Unknown error';
  }

  // 批量验证
  async validateAll(apis) {
    const results = [];
    
    for (const api of apis) {
      const result = await this.testDirectRequest(api);
      results.push({
        url: api.url,
        ...result
      });
      
      console.log(
        `[${result.success ? '✓' : '✗'}] ${api.url}`
      );
    }
    
    return {
      total: results.length,
      success: results.filter(r => r.success).length,
      failed: results.filter(r => !r.success).length,
      details: results
    };
  }
}

module.exports = RequestValidator;
```

## 智能调度器

```javascript
// lib/smart-scheduler.js
const axios = require('axios');
const { chromium } = require('playwright');

class SmartScheduler {
  constructor() {
    this.browser = null;
  }

  // 智能获取数据（自动选择方式）
  async fetchData(url, apiInfo) {
    // 优先尝试直接请求
    try {
      return await this.directRequest(apiInfo);
    } catch (error) {
      console.log(`[Fallback] 直接请求失败，使用浏览器: ${url}`);
      return await this.browserRequest(url);
    }
  }

  // 直接 HTTP 请求
  async directRequest(apiInfo) {
    const response = await axios({
      method: apiInfo.method,
      url: apiInfo.url,
      headers: apiInfo.headers,
      data: apiInfo.postData,
      timeout: 10000
    });
    
    return {
      method: 'direct',
      data: response.data,
      cost: 'low'
    };
  }

  // 浏览器请求（回退方案）
  async browserRequest(url) {
    if (!this.browser) {
      this.browser = await chromium.launch();
    }
    
    const page = await this.browser.newPage();
    await page.goto(url);
    
    const data = await page.evaluate(() => {
      // 提取页面数据
      return window.__DATA__ || {};
    });
    
    await page.close();
    
    return {
      method: 'browser',
      data,
      cost: 'high'
    };
  }

  // 批量调度
  async batchFetch(tasks) {
    const results = [];
    let directCount = 0;
    let browserCount = 0;
    
    for (const task of tasks) {
      const result = await this.fetchData(task.url, task.apiInfo);
      results.push(result);
      
      if (result.method === 'direct') {
        directCount++;
      } else {
        browserCount++;
      }
    }
    
    console.log(`\n统计:`);
    console.log(`- 直接请求: ${directCount} (${(directCount/tasks.length*100).toFixed(1)}%)`);
    console.log(`- 浏览器: ${browserCount} (${(browserCount/tasks.length*100).toFixed(1)}%)`);
    
    return results;
  }

  async close() {
    if (this.browser) {
      await this.browser.close();
    }
  }
}

module.exports = SmartScheduler;
```

## 使用示例

### 基础用法

```javascript
const APIExtractor = require('./scripts/auto-extract-apis');

// 1. 提取 API
const extractor = new APIExtractor({
  outputDir: 'output/apis'
});

await extractor.extractViaHAR(
  'https://example.com/data',
  'example'
);

// 2. 验证可用性
const RequestValidator = require('./lib/request-validator');
const validator = new RequestValidator();

const apis = require('./output/apis/example-apis.json');
const validation = await validator.validateAll(apis);

console.log(`成功率: ${validation.success}/${validation.total}`);

// 3. 智能调度
const SmartScheduler = require('./lib/smart-scheduler');
const scheduler = new SmartScheduler();

const results = await scheduler.batchFetch([
  { url: 'https://example.com/api/1', apiInfo: apis[0] },
  { url: 'https://example.com/api/2', apiInfo: apis[1] }
]);
```

### 完整工作流

```bash
# 1. 录制 HAR
node scripts/record-har.js https://example.com output/site.har

# 2. 提取 API
node scripts/auto-extract-apis.js

# 3. 验证接口
node scripts/validate-apis.js

# 4. 生成调用代码
node scripts/generate-code.js --format python

# 5. 批量测试
node scripts/test-all-apis.js
```

## 特殊场景处理

### Next.js / SSR 页面

```javascript
// 检测 SSR 数据
async function extractSSRData(html) {
  const nextDataMatch = html.match(/<script id="__NEXT_DATA__"[^>]*>(.*?)<\/script>/);
  if (nextDataMatch) {
    return JSON.parse(nextDataMatch[1]);
  }
  
  const nuxtMatch = html.match(/window\.__NUXT__\s*=\s*({.*?});/);
  if (nuxtMatch) {
    return eval(`(${nuxtMatch[1]})`);
  }
  
  return null;
}
```

### GraphQL 接口

```javascript
// 生成 GraphQL 请求代码
function generateGraphQLCode(entry) {
  const postData = JSON.parse(entry.request.postData.text);
  
  return `
const query = \`${postData.query}\`;
const variables = ${JSON.stringify(postData.variables, null, 2)};

const response = await fetch('${entry.request.url}', {
  method: 'POST',
  headers: ${JSON.stringify(entry.request.headers, null, 2)},
  body: JSON.stringify({ query, variables })
});

const data = await response.json();
console.log(data);
  `;
}
```

### 带签名的接口

```javascript
// 识别签名参数
function detectSignature(headers, queryParams) {
  const signatureKeys = [
    'x-sign', 'signature', 'sign',
    'x-signature', 'auth-sign'
  ];
  
  for (const key of signatureKeys) {
    if (headers[key] || queryParams[key]) {
      return {
        found: true,
        location: headers[key] ? 'header' : 'query',
        key,
        value: headers[key] || queryParams[key]
      };
    }
  }
  
  return { found: false };
}
```

## 性能对比

| 方式 | 速度 | 资源消耗 | 成功率 | 适用场景 |
|------|------|----------|--------|----------|
| 直接请求 | ⚡⚡⚡⚡⚡ | 极低 | 70-90% | 简单 API |
| HAR 回放 | ⚡⚡⚡⚡ | 低 | 80-95% | 标准接口 |
| Playwright | ⚡⚡ | 高 | 95-100% | 复杂页面 |

## 最佳实践

1. **优先级策略**: 直接请求 → HAR 回放 → 浏览器渲染
2. **批量处理**: 使用队列管理，避免并发过高
3. **错误处理**: 实现自动重试和降级机制
4. **数据验证**: 对比浏览器和直接请求的结果
5. **定期更新**: API 可能变化，需要重新提取

## 总结

通过 HAR 自动化系统，可以：

- ✅ 自动识别页面中的数据接口
- ✅ 批量生成请求代码（Python/Node.js/curl）
- ✅ 自动验证接口可用性
- ✅ 智能选择最优请求方式
- ✅ 大幅降低抓取成本（95%+ 场景可去浏览器化）

这是一个完整的去浏览器化数据采集解决方案。
