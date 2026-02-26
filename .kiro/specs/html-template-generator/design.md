# HTML Template Generator - 设计文档

## 📋 设计概述

本文档详细描述 html-template-generator 的技术设计，包括架构、模块设计、数据结构、算法和实现细节。

## 🏗️ 系统架构

### 整体架构图

```
┌─────────────────────────────────────────────────────────────┐
│                     html-template-generator                  │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │   CLI Layer  │───▶│  Main Logic  │───▶│    Output    │  │
│  │ run-skill.js │    │   main.js    │    │ template.json│  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│                             │                                │
│         ┌───────────────────┼───────────────────┐           │
│         ▼                   ▼                   ▼           │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    │
│  │   Pattern   │    │   Browser   │    │  Structure  │    │
│  │   Reader    │    │   Manager   │    │  Analyzer   │    │
│  └─────────────┘    └─────────────┘    └─────────────┘    │
│         │                   │                   │           │
│         ▼                   ▼                   ▼           │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    │
│  │url-patterns │    │    HTML     │    │    XPath    │    │
│  │   .json     │    │   Fetcher   │    │  Generator  │    │
│  └─────────────┘    └─────────────┘    └─────────────┘    │
│                             │                   │           │
│                             ▼                   ▼           │
│                      ┌─────────────┐    ┌─────────────┐    │
│                      │  Playwright │    │  Template   │    │
│                      │   Browser   │    │   Writer    │    │
│                      └─────────────┘    └─────────────┘    │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### 数据流图

```
url-patterns.json
      │
      ▼
[PatternReader.read()]
      │
      ▼
{ name, description, samples[] }
      │
      ▼
[BrowserManager.launch()]
      │
      ▼
[HTMLFetcher.fetchAll()]
      │
      ▼
[{ url, html, title }]
      │
      ▼
[StructureAnalyzer.analyze()]
      │
      ▼
{ mainContent, headings, tables, codeBlocks, lists }
      │
      ▼
[XPathGenerator.generate()]
      │
      ▼
{ title, sections, filters }
      │
      ▼
[TemplateWriter.write()]
      │
      ▼
template.json
```

## 📦 模块设计

### 1. PatternReader 模块

**文件**: `lib/pattern-reader.js`

**职责**: 读取和解析 url-patterns.json 文件


**类设计**:
```javascript
class PatternReader {
  /**
   * 读取 url-patterns.json 并提取指定模板
   * @param {string} patternsFile - url-patterns.json 文件路径
   * @param {string} templateName - 模板名称
   * @returns {Promise<Template>} 模板对象
   */
  async read(patternsFile, templateName) {
    // 1. 读取 JSON 文件
    // 2. 查找指定模板
    // 3. 验证模板数据
    // 4. 返回模板对象
  }
  
  /**
   * 验证模板数据完整性
   * @param {object} template - 模板对象
   * @throws {Error} 如果数据不完整
   */
  _validateTemplate(template) {
    // 检查必需字段
  }
}
```

**数据结构**:
```javascript
// Template 对象
{
  name: string,           // 模板名称，如 "api-doc"
  description: string,    // 模板描述
  samples: string[],      // 样例 URL 列表（5个）
  pathTemplate: string,   // URL 路径模板
  pattern: string,        // URL 正则模式
  urlCount: number        // 匹配的 URL 总数
}
```

**错误处理**:
- 文件不存在 → `FileNotFoundError`
- JSON 解析失败 → `JSONParseError`
- 模板不存在 → `TemplateNotFoundError`
- 数据不完整 → `ValidationError`

---

### 2. BrowserManager 模块

**文件**: `lib/browser-manager.js`

**职责**: 管理 Playwright 浏览器实例

**类设计**:
```javascript
class BrowserManager {
  constructor(config = {}) {
    this.userDataDir = config.userDataDir || '../../stock-crawler/chrome_user_data';
    this.headless = config.headless !== false;
    this.channel = config.channel || 'chrome';
    this.timeout = config.timeout || 30000;
    this.browser = null;
  }
  
  /**
   * 启动浏览器
   * @returns {Promise<BrowserContext>} 浏览器上下文
   */
  async launch() {
    const { chromium } = await import('playwright');
    const userDataDir = path.resolve(__dirname, this.userDataDir);
    
    this.browser = await chromium.launchPersistentContext(userDataDir, {
      headless: this.headless,
      channel: this.channel,
      args: [
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-dev-shm-usage'
      ]
    });
    
    return this.browser;
  }
  
  /**
   * 关闭浏览器
   */
  async close() {
    if (this.browser) {
      await this.browser.close();
      this.browser = null;
    }
  }
  
  /**
   * 获取浏览器实例
   * @returns {BrowserContext|null}
   */
  getBrowser() {
    return this.browser;
  }
}
```

**配置选项**:
```javascript
{
  userDataDir: string,    // 用户数据目录路径
  headless: boolean,      // 是否无头模式，默认 true
  channel: string,        // 浏览器通道，默认 'chrome'
  timeout: number         // 超时时间（毫秒），默认 30000
}
```

**错误处理**:
- 浏览器启动失败 → `BrowserLaunchError`
- 用户数据目录不存在 → `UserDataDirError`
- 超时 → `TimeoutError`

---

### 3. HTMLFetcher 模块

**文件**: `lib/html-fetcher.js`

**职责**: 抓取页面 HTML 内容

**类设计**:
```javascript
class HTMLFetcher {
  constructor(browserManager) {
    this.browserManager = browserManager;
    this.timeout = 30000;
  }
  
  /**
   * 抓取多个 URL 的 HTML
   * @param {string[]} urls - URL 列表
   * @returns {Promise<HTMLContent[]>} HTML 内容列表
   */
  async fetchAll(urls) {
    const results = [];
    
    for (const url of urls) {
      try {
        const content = await this.fetchOne(url);
        results.push(content);
      } catch (error) {
        console.error(`Failed to fetch ${url}:`, error.message);
        // 继续处理其他 URL
      }
    }
    
    return results;
  }
  
  /**
   * 抓取单个 URL 的 HTML
   * @param {string} url - URL
   * @returns {Promise<HTMLContent>} HTML 内容
   */
  async fetchOne(url) {
    const browser = this.browserManager.getBrowser();
    const page = await browser.newPage();
    
    try {
      // 访问页面
      await page.goto(url, { 
        waitUntil: 'networkidle',
        timeout: this.timeout 
      });
      
      // 等待页面稳定
      await page.waitForTimeout(1000);
      
      // 提取内容
      const html = await page.content();
      const title = await page.title();
      const url_final = page.url();
      
      return {
        url: url_final,
        html,
        title,
        timestamp: new Date().toISOString()
      };
    } finally {
      await page.close();
    }
  }
}
```

**数据结构**:
```javascript
// HTMLContent 对象
{
  url: string,          // 最终 URL（可能重定向）
  html: string,         // HTML 内容
  title: string,        // 页面标题
  timestamp: string     // 抓取时间戳
}
```

**错误处理**:
- 页面加载失败 → `PageLoadError`
- 超时 → `TimeoutError`
- 网络错误 → `NetworkError`

---

### 4. StructureAnalyzer 模块

**文件**: `lib/structure-analyzer.js`

**职责**: 分析 HTML 结构，识别共同模式

**类设计**:
```javascript
class StructureAnalyzer {
  constructor() {
    this.jsdom = null;
  }
  
  /**
   * 分析多个 HTML 内容
   * @param {HTMLContent[]} htmlContents - HTML 内容列表
   * @returns {Promise<Structure>} 结构分析结果
   */
  async analyze(htmlContents) {
    const structures = [];
    
    // 分析每个样例
    for (const content of htmlContents) {
      const structure = await this._analyzeSingle(content.html);
      structures.push(structure);
    }
    
    // 合并分析结果，找出共同模式
    return this._mergeStructures(structures);
  }
  
  /**
   * 分析单个 HTML
   * @param {string} html - HTML 内容
   * @returns {Promise<SingleStructure>} 单个结构
   */
  async _analyzeSingle(html) {
    const { JSDOM } = await import('jsdom');
    const dom = new JSDOM(html);
    const document = dom.window.document;
    
    return {
      mainContent: this._findMainContent(document),
      headings: this._extractHeadings(document),
      tables: this._extractTables(document),
      codeBlocks: this._extractCodeBlocks(document),
      lists: this._extractLists(document)
    };
  }
  
  /**
   * 查找主内容区域
   * @param {Document} document - DOM 文档
   * @returns {Element|null} 主内容元素
   */
  _findMainContent(document) {
    // 尝试常见的主内容选择器
    const selectors = [
      'main',
      'article',
      '[role="main"]',
      '.main-content',
      '.content',
      '#content',
      '.container'
    ];
    
    for (const selector of selectors) {
      const element = document.querySelector(selector);
      if (element) {
        return this._elementToInfo(element);
      }
    }
    
    return null;
  }
  
  /**
   * 提取标题
   * @param {Document} document - DOM 文档
   * @returns {Headings} 标题信息
   */
  _extractHeadings(document) {
    const headings = {};
    
    for (let level = 1; level <= 6; level++) {
      const tag = `h${level}`;
      const elements = document.querySelectorAll(tag);
      
      if (elements.length > 0) {
        headings[tag] = Array.from(elements).map(el => ({
          text: el.textContent.trim(),
          class: el.className,
          id: el.id,
          xpath: this._generateXPath(el)
        }));
      }
    }
    
    return headings;
  }
  
  /**
   * 提取表格
   * @param {Document} document - DOM 文档
   * @returns {Table[]} 表格列表
   */
  _extractTables(document) {
    const tables = document.querySelectorAll('table');
    
    return Array.from(tables).map(table => {
      const caption = table.querySelector('caption');
      const thead = table.querySelector('thead');
      const tbody = table.querySelector('tbody');
      
      return {
        class: table.className,
        id: table.id,
        caption: caption ? caption.textContent.trim() : null,
        columnCount: thead ? thead.querySelectorAll('th').length : 0,
        rowCount: tbody ? tbody.querySelectorAll('tr').length : 0,
        xpath: this._generateXPath(table)
      };
    });
  }
  
  /**
   * 提取代码块
   * @param {Document} document - DOM 文档
   * @returns {CodeBlock[]} 代码块列表
   */
  _extractCodeBlocks(document) {
    const codeBlocks = document.querySelectorAll('pre code, pre, code');
    
    return Array.from(codeBlocks).map(code => ({
      class: code.className,
      language: this._detectLanguage(code),
      xpath: this._generateXPath(code)
    }));
  }
  
  /**
   * 提取列表
   * @param {Document} document - DOM 文档
   * @returns {List[]} 列表列表
   */
  _extractLists(document) {
    const lists = document.querySelectorAll('ul, ol');
    
    return Array.from(lists).map(list => ({
      type: list.tagName.toLowerCase(),
      class: list.className,
      id: list.id,
      itemCount: list.querySelectorAll('li').length,
      xpath: this._generateXPath(list)
    }));
  }
  
  /**
   * 生成元素的 XPath
   * @param {Element} element - DOM 元素
   * @returns {string} XPath 表达式
   */
  _generateXPath(element) {
    // 优先使用 id
    if (element.id) {
      return `//*[@id='${element.id}']`;
    }
    
    // 使用 class
    if (element.className) {
      const classes = element.className.trim().split(/\s+/);
      if (classes.length === 1) {
        return `//${element.tagName.toLowerCase()}[@class='${classes[0]}']`;
      } else {
        return `//${element.tagName.toLowerCase()}[contains(@class, '${classes[0]}')]`;
      }
    }
    
    // 使用标签名
    return `//${element.tagName.toLowerCase()}`;
  }
  
  /**
   * 合并多个结构，找出共同模式
   * @param {SingleStructure[]} structures - 结构列表
   * @returns {Structure} 合并后的结构
   */
  _mergeStructures(structures) {
    const sampleCount = structures.length;
    
    return {
      mainContent: this._findCommonElement(structures.map(s => s.mainContent)),
      headings: this._mergeHeadings(structures.map(s => s.headings), sampleCount),
      tables: this._mergeTables(structures.map(s => s.tables), sampleCount),
      codeBlocks: this._mergeCodeBlocks(structures.map(s => s.codeBlocks), sampleCount),
      lists: this._mergeLists(structures.map(s => s.lists), sampleCount),
      metadata: {
        sampleCount,
        analyzedAt: new Date().toISOString()
      }
    };
  }
  
  /**
   * 合并标题
   */
  _mergeHeadings(headingsList, sampleCount) {
    const merged = {};
    
    for (let level = 1; level <= 6; level++) {
      const tag = `h${level}`;
      const xpaths = {};
      
      // 统计每个 XPath 出现的次数
      for (const headings of headingsList) {
        if (headings[tag]) {
          for (const heading of headings[tag]) {
            const xpath = heading.xpath;
            xpaths[xpath] = (xpaths[xpath] || 0) + 1;
          }
        }
      }
      
      // 选择出现频率最高的 XPath
      const sortedXPaths = Object.entries(xpaths)
        .sort((a, b) => b[1] - a[1]);
      
      if (sortedXPaths.length > 0) {
        const [xpath, count] = sortedXPaths[0];
        merged[tag] = {
          xpath,
          frequency: count / sampleCount
        };
      }
    }
    
    return merged;
  }
  
  /**
   * 合并表格
   */
  _mergeTables(tablesList, sampleCount) {
    const xpaths = {};
    
    // 统计每个表格 XPath 出现的次数
    for (const tables of tablesList) {
      for (const table of tables) {
        const xpath = table.xpath;
        if (!xpaths[xpath]) {
          xpaths[xpath] = {
            count: 0,
            caption: table.caption,
            columnCount: table.columnCount
          };
        }
        xpaths[xpath].count++;
      }
    }
    
    // 转换为数组并计算频率
    return Object.entries(xpaths)
      .map(([xpath, data]) => ({
        xpath,
        frequency: data.count / sampleCount,
        caption: data.caption,
        columnCount: data.columnCount
      }))
      .sort((a, b) => b.frequency - a.frequency);
  }
  
  /**
   * 合并代码块
   */
  _mergeCodeBlocks(codeBlocksList, sampleCount) {
    const xpaths = {};
    
    // 统计每个代码块 XPath 出现的次数
    for (const codeBlocks of codeBlocksList) {
      for (const code of codeBlocks) {
        const xpath = code.xpath;
        if (!xpaths[xpath]) {
          xpaths[xpath] = {
            count: 0,
            language: code.language
          };
        }
        xpaths[xpath].count++;
      }
    }
    
    // 转换为数组并计算频率
    return Object.entries(xpaths)
      .map(([xpath, data]) => ({
        xpath,
        frequency: data.count / sampleCount,
        language: data.language
      }))
      .sort((a, b) => b.frequency - a.frequency);
  }
  
  /**
   * 合并列表
   */
  _mergeLists(listsList, sampleCount) {
    const xpaths = {};
    
    // 统计每个列表 XPath 出现的次数
    for (const lists of listsList) {
      for (const list of lists) {
        const xpath = list.xpath;
        if (!xpaths[xpath]) {
          xpaths[xpath] = {
            count: 0,
            type: list.type,
            itemCount: list.itemCount
          };
        }
        xpaths[xpath].count++;
      }
    }
    
    // 转换为数组并计算频率
    return Object.entries(xpaths)
      .map(([xpath, data]) => ({
        xpath,
        frequency: data.count / sampleCount,
        type: data.type,
        itemCount: data.itemCount
      }))
      .sort((a, b) => b.frequency - a.frequency);
  }
}
```

**数据结构**:
```javascript
// Structure 对象
{
  mainContent: {
    xpath: string,
    frequency: number
  },
  headings: {
    h1: { xpath: string, frequency: number },
    h2: { xpath: string, frequency: number },
    // ...
  },
  tables: [{
    xpath: string,
    frequency: number,
    caption: string,
    columnCount: number
  }],
  codeBlocks: [{
    xpath: string,
    frequency: number,
    language: string
  }],
  lists: [{
    xpath: string,
    frequency: number,
    type: 'ul' | 'ol'
  }],
  metadata: {
    sampleCount: number,
    analyzedAt: string
  }
}
```


---

### 5. XPathGenerator 模块

**文件**: `lib/xpath-generator.js`

**职责**: 基于结构分析生成 XPath 抽取规则

**类设计**:
```javascript
class XPathGenerator {
  /**
   * 生成 XPath 规则
   * @param {Structure} structure - 结构分析结果
   * @returns {XPathRules} XPath 规则
   */
  generate(structure) {
    return {
      title: this._generateTitleXPath(structure.headings),
      sections: this._generateSectionsXPath(structure),
      filters: this._generateFilters(structure)
    };
  }
  
  /**
   * 生成标题 XPath
   * @param {Headings} headings - 标题信息
   * @returns {string} XPath 表达式
   */
  _generateTitleXPath(headings) {
    // 优先使用 h1
    if (headings.h1 && headings.h1.frequency >= 0.8) {
      return `${headings.h1.xpath}/text()`;
    }
    
    // 回退到 h2
    if (headings.h2 && headings.h2.frequency >= 0.8) {
      return `${headings.h2.xpath}/text()`;
    }
    
    return null;
  }
  
  /**
   * 生成章节 XPath
   * @param {Structure} structure - 结构
   * @returns {object} 章节规则
   */
  _generateSectionsXPath(structure) {
    // 查找主要的内容容器
    const containerXPath = this._findContentContainer(structure);
    
    if (!containerXPath) {
      return null;
    }
    
    return {
      xpath: containerXPath,
      extract: {
        heading: this._generateRelativeXPath(structure.headings, 'h2'),
        description: './/p/text()',
        table: this._generateTableXPath(structure.tables),
        codeExample: this._generateCodeXPath(structure.codeBlocks),
        list: this._generateListXPath(structure.lists)
      }
    };
  }
  
  /**
   * 查找内容容器
   * @param {Structure} structure - 结构
   * @returns {string|null} 容器 XPath
   */
  _findContentContainer(structure) {
    if (structure.mainContent && structure.mainContent.frequency >= 0.8) {
      return structure.mainContent.xpath;
    }
    
    // 尝试使用常见的容器
    return "//main | //article | //div[contains(@class, 'content')]";
  }
  
  /**
   * 生成相对 XPath
   * @param {Headings} headings - 标题
   * @param {string} tag - 标签名
   * @returns {string} 相对 XPath
   */
  _generateRelativeXPath(headings, tag) {
    if (headings[tag] && headings[tag].frequency >= 0.8) {
      const xpath = headings[tag].xpath;
      // 转换为相对路径
      return xpath.replace(/^\/\//, './/');
    }
    
    return `.//$ {tag}/text()`;
  }
  
  /**
   * 生成表格 XPath
   * @param {Table[]} tables - 表格列表
   * @returns {object|null} 表格规则
   */
  _generateTableXPath(tables) {
    // 找出频率最高的表格
    const commonTable = tables.find(t => t.frequency >= 0.8);
    
    if (!commonTable) {
      return null;
    }
    
    return {
      xpath: commonTable.xpath.replace(/^\/\//, './/'),
      headers: './/thead/tr/th/text()',
      rows: './/tbody/tr',
      cells: './/td/text()'
    };
  }
  
  /**
   * 生成代码块 XPath
   * @param {CodeBlock[]} codeBlocks - 代码块列表
   * @returns {string|null} 代码块 XPath
   */
  _generateCodeXPath(codeBlocks) {
    const commonCode = codeBlocks.find(c => c.frequency >= 0.8);
    
    if (!commonCode) {
      return null;
    }
    
    return commonCode.xpath.replace(/^\/\//, './/') + '/text()';
  }
  
  /**
   * 生成列表 XPath
   * @param {List[]} lists - 列表列表
   * @returns {string|null} 列表 XPath
   */
  _generateListXPath(lists) {
    const commonList = lists.find(l => l.frequency >= 0.8);
    
    if (!commonList) {
      return null;
    }
    
    return {
      xpath: commonList.xpath.replace(/^\/\//, './/'),
      items: './/li/text()'
    };
  }
  
  /**
   * 生成过滤规则
   * @param {Structure} structure - 结构
   * @returns {object} 过滤规则
   */
  _generateFilters(structure) {
    return {
      removeXPaths: [
        "//nav",
        "//header",
        "//footer",
        "//aside",
        "//div[contains(@class, 'ad')]",
        "//div[contains(@class, 'advertisement')]",
        "//div[contains(@class, 'sidebar')]"
      ],
      cleanText: true
    };
  }
}
```

**数据结构**:
```javascript
// XPathRules 对象
{
  title: string,              // 标题 XPath
  sections: {
    xpath: string,            // 章节容器 XPath
    extract: {
      heading: string,        // 章节标题 XPath
      description: string,    // 描述 XPath
      table: {
        xpath: string,        // 表格 XPath
        headers: string,      // 表头 XPath
        rows: string,         // 行 XPath
        cells: string         // 单元格 XPath
      },
      codeExample: string,    // 代码块 XPath
      list: {
        xpath: string,        // 列表 XPath
        items: string         // 列表项 XPath
      }
    }
  },
  filters: {
    removeXPaths: string[],   // 要移除的元素 XPath
    cleanText: boolean        // 是否清理文本
  }
}
```

---

### 6. TemplateWriter 模块

**文件**: `lib/template-writer.js`

**职责**: 将生成的规则写入 JSON 文件

**类设计**:
```javascript
class TemplateWriter {
  /**
   * 写入模板文件
   * @param {string} outputFile - 输出文件路径
   * @param {object} data - 模板数据
   */
  async write(outputFile, data) {
    const template = this._buildTemplate(data);
    const json = JSON.stringify(template, null, 2);
    
    // 确保输出目录存在
    const dir = path.dirname(outputFile);
    await fs.mkdir(dir, { recursive: true });
    
    // 写入文件
    await fs.writeFile(outputFile, json, 'utf-8');
  }
  
  /**
   * 构建模板对象
   * @param {object} data - 数据
   * @returns {object} 模板对象
   */
  _buildTemplate(data) {
    return {
      templateName: data.templateName,
      version: "1.0.0",
      generatedAt: new Date().toISOString(),
      samples: data.samples || [],
      xpaths: data.xpaths,
      filters: data.filters || {},
      metadata: {
        sampleCount: data.metadata?.sampleCount || 0,
        commonElements: data.metadata?.commonElements || {}
      }
    };
  }
}
```

---

### 7. TemplateGenerator 主类

**文件**: `main.js`

**职责**: 协调所有模块，实现主流程

**类设计**:
```javascript
class TemplateGenerator {
  constructor(config = {}) {
    this.patternReader = new PatternReader();
    this.browserManager = new BrowserManager(config.browser);
    this.htmlFetcher = new HTMLFetcher(this.browserManager);
    this.structureAnalyzer = new StructureAnalyzer();
    this.xpathGenerator = new XPathGenerator();
    this.templateWriter = new TemplateWriter();
  }
  
  /**
   * 生成模板
   * @param {string} templateName - 模板名称
   * @param {string} patternsFile - url-patterns.json 路径
   * @param {string} outputFile - 输出文件路径
   */
  async generate(templateName, patternsFile, outputFile) {
    console.log(`正在处理模板: ${templateName}`);
    
    try {
      // 1. 读取模板
      console.log('\n读取 URL patterns...');
      const template = await this.patternReader.read(patternsFile, templateName);
      console.log(`样例数量: ${template.samples.length}`);
      
      // 2. 启动浏览器
      console.log('\n启动浏览器...');
      await this.browserManager.launch();
      console.log('✓ 浏览器已启动');
      
      // 3. 抓取样例
      console.log('\n抓取样例页面...');
      const htmlContents = await this.htmlFetcher.fetchAll(template.samples);
      console.log(`✓ 已抓取 ${htmlContents.length} 个页面`);
      
      // 4. 分析结构
      console.log('\n分析 HTML 结构...');
      const structure = await this.structureAnalyzer.analyze(htmlContents);
      console.log('✓ 结构分析完成');
      
      // 5. 生成 XPath
      console.log('\n生成 XPath 规则...');
      const xpaths = this.xpathGenerator.generate(structure);
      console.log('✓ XPath 规则已生成');
      
      // 6. 输出模板
      console.log('\n保存模板文件...');
      await this.templateWriter.write(outputFile, {
        templateName,
        samples: template.samples,
        xpaths,
        filters: xpaths.filters,
        metadata: structure.metadata
      });
      console.log(`✓ 已保存: ${outputFile}`);
      
      console.log('\n完成！');
      
    } finally {
      // 关闭浏览器
      await this.browserManager.close();
    }
  }
}

export default TemplateGenerator;
```

---

## 🔄 执行流程

### 完整流程图

```
开始
  │
  ▼
解析命令行参数
  │
  ▼
创建 TemplateGenerator 实例
  │
  ▼
读取 url-patterns.json
  │
  ├─ 查找指定模板
  ├─ 提取样例 URL
  └─ 验证数据
  │
  ▼
启动 Playwright 浏览器
  │
  ├─ 使用 chrome_user_data
  └─ 配置 headless 模式
  │
  ▼
抓取样例页面 (循环)
  │
  ├─ 访问 URL
  ├─ 等待页面加载
  ├─ 提取 HTML
  └─ 提取标题
  │
  ▼
分析 HTML 结构 (循环)
  │
  ├─ 解析 HTML (jsdom)
  ├─ 提取标题
  ├─ 提取表格
  ├─ 提取代码块
  └─ 提取列表
  │
  ▼
合并结构分析结果
  │
  ├─ 统计元素频率
  ├─ 识别共同模式
  └─ 生成 XPath 候选
  │
  ▼
生成 XPath 规则
  │
  ├─ 选择高频元素
  ├─ 生成相对路径
  ├─ 生成嵌套结构
  └─ 生成过滤规则
  │
  ▼
写入模板文件
  │
  ├─ 构建 JSON 对象
  ├─ 格式化输出
  └─ 保存文件
  │
  ▼
关闭浏览器
  │
  ▼
结束
```

### 错误处理流程

```
任何步骤发生错误
  │
  ▼
捕获异常
  │
  ├─ 记录错误日志
  ├─ 显示友好错误消息
  └─ 清理资源
  │
  ▼
关闭浏览器 (如果已启动)
  │
  ▼
退出程序 (非零退出码)
```

---

## 📊 数据结构详细设计

### 核心数据结构

```javascript
// 1. Template (从 url-patterns.json 读取)
{
  name: "api-doc",
  description: "开放API文档 - API接口说明和使用指南",
  pathTemplate: "/open/api/doc",
  pattern: "^https://www\\.lixinger\\.com/open/api/doc(\\?.*)?$",
  queryParams: ["api-key"],
  urlCount: 162,
  samples: [
    "https://www.lixinger.com/open/api/doc",
    "https://www.lixinger.com/open/api/doc?api-key=cn/fund",
    "https://www.lixinger.com/open/api/doc?api-key=cn/index",
    "https://www.lixinger.com/open/api/doc?api-key=hk/index",
    "https://www.lixinger.com/open/api/doc?api-key=us/index"
  ]
}

// 2. HTMLContent (抓取的页面内容)
{
  url: "https://www.lixinger.com/open/api/doc",
  html: "<html>...</html>",
  title: "API文档 - 理杏仁",
  timestamp: "2024-01-15T10:30:00.000Z"
}

// 3. SingleStructure (单个页面的结构)
{
  mainContent: {
    xpath: "//div[@class='main-content']",
    class: "main-content",
    id: null
  },
  headings: {
    h1: [{
      text: "API文档",
      class: "page-title",
      id: null,
      xpath: "//h1[@class='page-title']"
    }],
    h2: [{
      text: "基础信息",
      class: "section-title",
      id: null,
      xpath: "//h2[@class='section-title']"
    }]
  },
  tables: [{
    class: "params-table",
    id: null,
    caption: "参数说明",
    columnCount: 4,
    rowCount: 10,
    xpath: "//table[@class='params-table']"
  }],
  codeBlocks: [{
    class: "language-json",
    language: "json",
    xpath: "//pre/code[@class='language-json']"
  }],
  lists: [{
    type: "ul",
    class: "api-list",
    id: null,
    itemCount: 5,
    xpath: "//ul[@class='api-list']"
  }]
}

// 4. Structure (合并后的结构)
{
  mainContent: {
    xpath: "//div[@class='main-content']",
    frequency: 1.0
  },
  headings: {
    h1: {
      xpath: "//h1[@class='page-title']",
      frequency: 1.0
    },
    h2: {
      xpath: "//h2[@class='section-title']",
      frequency: 1.0
    }
  },
  tables: [{
    xpath: "//table[@class='params-table']",
    frequency: 1.0,
    caption: "参数说明",
    columnCount: 4
  }],
  codeBlocks: [{
    xpath: "//pre/code",
    frequency: 1.0,
    language: "json"
  }],
  lists: [{
    xpath: "//ul[@class='api-list']",
    frequency: 1.0,
    type: "ul"
  }],
  metadata: {
    sampleCount: 5,
    analyzedAt: "2024-01-15T10:30:00.000Z"
  }
}

// 5. XPathRules (生成的规则)
{
  title: "//h1[@class='page-title']/text()",
  sections: {
    xpath: "//div[@class='main-content']",
    extract: {
      heading: ".//h2[@class='section-title']/text()",
      description: ".//p/text()",
      table: {
        xpath: ".//table[@class='params-table']",
        headers: ".//thead/tr/th/text()",
        rows: ".//tbody/tr",
        cells: ".//td/text()"
      },
      codeExample: ".//pre/code/text()",
      list: {
        xpath: ".//ul[@class='api-list']",
        items: ".//li/text()"
      }
    }
  },
  filters: {
    removeXPaths: [
      "//nav",
      "//header",
      "//footer",
      "//aside",
      "//div[contains(@class, 'ad')]"
    ],
    cleanText: true
  }
}

// 6. Template Output (最终输出)
{
  "templateName": "api-doc",
  "version": "1.0.0",
  "generatedAt": "2024-01-15T10:30:00.000Z",
  "samples": [...],
  "xpaths": {...},
  "filters": {...},
  "metadata": {
    "sampleCount": 5,
    "commonElements": {
      "title": 5,
      "sections": 5,
      "tables": 5,
      "codeBlocks": 5,
      "lists": 5
    }
  }
}
```

---

## 🎯 算法设计

### 1. XPath 生成算法

**目标**: 为 HTML 元素生成稳定、可靠的 XPath 表达式

**策略**:
1. 优先使用 `id` 属性（最稳定）
2. 其次使用 `class` 属性
3. 使用 `contains()` 处理多个 class
4. 避免使用位置索引（如 `[1]`, `[2]`）
5. 使用相对路径（`.//`）而不是绝对路径

**伪代码**:
```
function generateXPath(element):
  if element.id exists:
    return "//*[@id='" + element.id + "']"
  
  if element.class exists:
    classes = element.class.split()
    if classes.length == 1:
      return "//" + element.tag + "[@class='" + classes[0] + "']"
    else:
      return "//" + element.tag + "[contains(@class, '" + classes[0] + "')]"
  
  return "//" + element.tag
```

### 2. 结构合并算法

**目标**: 从多个样例中找出共同的结构模式

**策略**:
1. 统计每个 XPath 在样例中的出现次数
2. 计算频率 = 出现次数 / 样例总数
3. 选择频率 >= 0.8 的元素作为共同模式
4. 对于多个候选，选择频率最高的

**伪代码**:
```
function mergeStructures(structures):
  xpathCounts = {}
  sampleCount = structures.length
  
  for structure in structures:
    for element in structure.elements:
      xpath = element.xpath
      xpathCounts[xpath] = xpathCounts.get(xpath, 0) + 1
  
  commonElements = []
  for xpath, count in xpathCounts:
    frequency = count / sampleCount
    if frequency >= 0.8:
      commonElements.append({
        xpath: xpath,
        frequency: frequency
      })
  
  return commonElements.sortBy(frequency, descending)
```

### 3. 主内容识别算法

**目标**: 识别页面的主要内容区域

**策略**:
1. 尝试常见的主内容选择器
2. 计算内容密度（文本长度 / HTML 长度）
3. 选择密度最高的区域

**伪代码**:
```
function findMainContent(document):
  selectors = ['main', 'article', '[role="main"]', '.main-content', '.content']
  
  for selector in selectors:
    element = document.querySelector(selector)
    if element exists:
      return element
  
  // 回退：计算内容密度
  candidates = document.querySelectorAll('div')
  bestCandidate = null
  bestDensity = 0
  
  for candidate in candidates:
    textLength = candidate.textContent.length
    htmlLength = candidate.innerHTML.length
    density = textLength / htmlLength
    
    if density > bestDensity:
      bestDensity = density
      bestCandidate = candidate
  
  return bestCandidate
```

---

## 🔒 错误处理策略

### 错误类型

```javascript
// 自定义错误类
class TemplateGeneratorError extends Error {
  constructor(message, code) {
    super(message);
    this.name = 'TemplateGeneratorError';
    this.code = code;
  }
}

class FileNotFoundError extends TemplateGeneratorError {
  constructor(filePath) {
    super(`File not found: ${filePath}`, 'FILE_NOT_FOUND');
  }
}

class TemplateNotFoundError extends TemplateGeneratorError {
  constructor(templateName) {
    super(`Template not found: ${templateName}`, 'TEMPLATE_NOT_FOUND');
  }
}

class BrowserLaunchError extends TemplateGeneratorError {
  constructor(message) {
    super(`Failed to launch browser: ${message}`, 'BROWSER_LAUNCH_ERROR');
  }
}

class PageLoadError extends TemplateGeneratorError {
  constructor(url, message) {
    super(`Failed to load page ${url}: ${message}`, 'PAGE_LOAD_ERROR');
  }
}
```

### 错误处理原则

1. **捕获所有异常**: 使用 try-catch 包裹所有异步操作
2. **友好的错误消息**: 提供清晰、可操作的错误信息
3. **资源清理**: 确保浏览器等资源被正确关闭
4. **部分失败容忍**: 某个样例失败不影响其他样例
5. **日志记录**: 记录详细的错误信息用于调试

---

## 📈 性能优化

### 优化策略

1. **并发抓取**: 同时抓取多个页面（控制并发数）
2. **缓存机制**: 缓存已抓取的 HTML
3. **增量分析**: 只分析变化的部分
4. **内存管理**: 及时释放大对象
5. **超时控制**: 设置合理的超时时间

### 性能指标

- 单个样例抓取: < 5s
- 单个样例分析: < 1s
- 总处理时间: < 30s (5个样例)
- 内存占用: < 500MB

---

## 🧪 测试策略

### 单元测试

每个模块都需要单元测试：
- PatternReader: 测试文件读取、模板查找
- BrowserManager: 测试浏览器启动、关闭
- HTMLFetcher: 测试页面抓取
- StructureAnalyzer: 测试结构分析
- XPathGenerator: 测试 XPath 生成
- TemplateWriter: 测试文件写入

### 集成测试

测试模块间的协作：
- 完整流程测试
- 错误处理测试
- 边界条件测试

### 端到端测试

使用真实数据测试：
- 使用 api-doc 模板测试
- 验证输出文件格式
- 验证 XPath 有效性

---

## 📝 配置管理

### 配置文件格式

```javascript
// config.json
{
  "browser": {
    "headless": true,
    "userDataDir": "../../stock-crawler/chrome_user_data",
    "channel": "chrome",
    "timeout": 30000
  },
  "analyzer": {
    "minFrequency": 0.8,
    "maxSamples": 5
  },
  "output": {
    "format": "json",
    "indent": 2
  }
}
```

### 配置优先级

1. 命令行参数（最高）
2. 配置文件
3. 默认值（最低）

---

## 🎯 总结

本设计文档详细描述了 html-template-generator 的技术实现，包括：

- 清晰的模块划分和职责
- 完整的数据结构定义
- 详细的算法设计
- 全面的错误处理
- 性能优化策略
- 测试策略

设计遵循以下原则：
- 单一职责原则
- 开闭原则
- 依赖倒置原则
- 接口隔离原则

下一步可以根据此设计文档开始实现。
