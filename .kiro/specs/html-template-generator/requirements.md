# HTML Template Generator - 需求文档

## 📋 项目概述

### 背景

当前工作流程中，我们已经有：
1. **url-pattern-analyzer**：从 links.txt 生成 url-patterns.json，识别 URL 模板
2. **stock-crawler**：通用爬虫，抓取页面生成 Markdown

但缺少关键环节：
- 如何从 HTML 页面生成精确的抽取规则？
- 如何确保抽取规则能提取所有关键内容？

### 目标

创建一个新的 skill：**html-template-generator**，功能是：

**输入**：url-patterns.json（包含模板和样例 URL）
**输出**：页面抽取模板（JSON 格式的抽取规则，使用 XPath）
**过程**：
1. 读取 url-patterns.json
2. 使用 Playwright 抓取样例页面的 HTML（复用已登录的浏览器状态）
3. 分析 HTML 结构，识别共同模式
4. 生成抽取规则（XPath 表达式）
5. 输出模板文件

### 设计原则

**完全独立**：
- 不依赖 stock-crawler 的任何代码
- 只需要 url-patterns.json 作为输入
- 自己管理浏览器（Playwright）
- 使用已保存的登录状态（不需要 login-handler）

**XPath 优先**：
- XPath 比 CSS 选择器更强大，支持更复杂的查询
- 可以基于文本内容选择元素
- 可以遍历父子兄弟节点
- 更适合生成通用的抽取模板

### 范围限定

**本次只做核心功能**：
- 单个模板的规则生成
- 基础的 HTML 结构分析
- XPath 表达式生成

**不做**：
- 交互式优化
- 批量处理
- 与爬虫集成

这些功能后续可以扩展。

## 🎯 核心需求

### 需求 1：读取 URL Patterns

**描述**：读取 url-patterns.json，获取模板和样例 URL。

**输入**：
- url-patterns.json 文件路径

**输出**：
- 模板列表，每个模板包含：
  - name: 模板名称
  - description: 模板描述
  - samples: 样例 URL 列表（5个）

**示例**：
```javascript
{
  name: "api-doc",
  description: "开放API文档 - API接口说明和使用指南",
  samples: [
    "https://www.lixinger.com/open/api/doc",
    "https://www.lixinger.com/open/api/doc?api-key=cn/fund",
    "https://www.lixinger.com/open/api/doc?api-key=cn/index",
    "https://www.lixinger.com/open/api/doc?api-key=hk/index",
    "https://www.lixinger.com/open/api/doc?api-key=us/index"
  ]
}
```

### 需求 2：抓取样例页面

**描述**：使用 Playwright 抓取样例页面的 HTML。

**输入**：
- 样例 URL 列表
- 用户数据目录：`/Users/fengzhi/Downloads/git/testlixingren/stock-crawler/chrome_user_data`

**输出**：
- 每个样例的 HTML 内容
- 页面元数据（标题、URL 等）

**实现方式**：
- 使用 Playwright 启动浏览器
- 使用 stock-crawler 的 chrome_user_data 目录（已保存登录状态）
- 无需登录逻辑，直接访问页面

**示例代码**：
```javascript
import { chromium } from 'playwright';
import path from 'path';

async function fetchSamples(sampleUrls) {
  const userDataDir = path.resolve(__dirname, '../../stock-crawler/chrome_user_data');
  
  const browser = await chromium.launchPersistentContext(userDataDir, {
    headless: true,
    channel: 'chrome'  // 使用 Chrome
  });
  
  const htmlContents = [];
  for (const url of sampleUrls) {
    const page = await browser.newPage();
    await page.goto(url, { waitUntil: 'networkidle' });
    const html = await page.content();
    const title = await page.title();
    htmlContents.push({ url, html, title });
    await page.close();
  }
  
  await browser.close();
  return htmlContents;
}
```

**Playwright 优势**：
- 更现代、更稳定
- 更好的 API 设计
- 原生支持多浏览器
- 更好的等待机制
- launchPersistentContext 直接支持用户数据目录

### 需求 3：HTML 结构分析

**描述**：分析多个样例页面的 HTML，识别共同的结构模式。

**分析内容**：
1. **主要内容区域**：识别包含核心内容的容器
2. **标题结构**：h1, h2, h3 等标题的层级和模式
3. **表格结构**：表格的位置、标题、列结构
4. **代码块**：代码示例的位置和格式
5. **列表结构**：有序/无序列表的模式
6. **导航元素**：Tab、下拉菜单等交互元素

**输出**：
- 结构化的页面模式描述
- 每个元素的 XPath 表达式候选
- 元素出现频率统计

**示例**：
```javascript
{
  mainContent: {
    xpath: "//div[@class='main-content']",
    frequency: 5/5  // 在5个样例中都出现
  },
  headings: {
    h1: { 
      xpath: "//h1[@class='page-title']", 
      frequency: 5/5,
      samples: ["API文档", "基金接口", "公司接口"]
    },
    h2: { 
      xpath: "//h2[@class='section-title']", 
      frequency: 5/5 
    }
  },
  tables: [
    {
      xpath: "//table[contains(@class, 'params-table')]",
      frequency: 5/5,
      caption: "参数说明",
      columnCount: 4
    }
  ],
  codeBlocks: [
    {
      xpath: "//pre/code",
      frequency: 5/5,
      language: "json"
    }
  ]
}
```

**XPath 优势**：
- 可以基于文本内容选择：`//h2[contains(text(), '参数')]`
- 可以选择父节点：`//table[@class='params']/../div`
- 可以使用逻辑运算：`//div[@class='content' and not(@class='hidden')]`
- 更灵活的位置选择：`//table[1]`, `//table[last()]`

### 需求 4：生成抽取规则

**描述**：基于结构分析，生成 XPath 抽取规则。

**规则格式**：
```javascript
{
  templateName: "api-doc",
  version: "1.0.0",
  xpaths: {
    title: "//h1[@class='page-title']/text()",
    sections: {
      xpath: "//section[@class='api-section']",
      extract: {
        heading: ".//h2/text()",
        description: ".//p[@class='description']/text()",
        table: {
          xpath: ".//table[@class='params-table']",
          headers: ".//thead/tr/th/text()",
          rows: ".//tbody/tr"
        },
        codeExample: ".//pre/code/text()"
      }
    }
  },
  filters: {
    removeXPaths: [
      "//div[@class='ad-banner']",
      "//aside[@class='sidebar']"
    ],
    cleanText: true
  }
}
```

**生成策略**：
1. 优先选择在所有样例中都出现的元素（frequency = 1.0）
2. 使用稳定的 XPath（基于 class、id，避免位置依赖）
3. 为可选元素添加标记
4. 生成过滤规则（去除广告、导航等噪音）
5. 支持嵌套结构（sections 内的 table）

**XPath 最佳实践**：
- 使用相对路径：`.//div` 而不是 `//div`
- 避免绝对路径：不要用 `/html/body/div[3]/div[2]`
- 优先使用属性：`//div[@id='content']`
- 使用 contains：`//div[contains(@class, 'content')]`
- 提取文本：`/text()` 或 `string()`

### 需求 5：输出模板文件

**描述**：将生成的规则保存为 JSON 文件。

**输出格式**：
```javascript
{
  "templateName": "api-doc",
  "version": "1.0.0",
  "generatedAt": "2024-01-15T10:30:00Z",
  "samples": [
    "https://www.lixinger.com/open/api/doc",
    // ...
  ],
  "xpaths": {
    "title": "//h1[@class='page-title']/text()",
    "sections": {
      "xpath": "//section[@class='api-section']",
      "extract": {
        "heading": ".//h2/text()",
        "description": ".//p[@class='description']/text()",
        "table": {
          "xpath": ".//table[@class='params-table']",
          "headers": ".//thead/tr/th/text()",
          "rows": ".//tbody/tr"
        },
        "codeExample": ".//pre/code/text()"
      }
    }
  },
  "filters": {
    "removeXPaths": [
      "//div[@class='ad-banner']",
      "//aside[@class='sidebar']"
    ],
    "cleanText": true
  },
  "metadata": {
    "sampleCount": 5,
    "commonElements": {
      "title": 5,
      "sections": 5,
      "tables": 5
    }
  }
}
```

**保存位置**：
- 默认：`output/<template-name>.json`
- 可通过命令行参数指定

**后续用途**：
生成的模板可以用于：
1. 从 HTML 生成 Markdown 文件
2. 结构化数据提取
3. 内容验证和对比

## 📊 使用场景

### 场景 1：生成单个模板规则

```bash
# 在 skills/html-template-generator 目录下
node run-skill.js api-doc \
  --input ../../stock-crawler/output/lixinger-crawler/url-patterns.json \
  --output ./output/api-doc.json
```

**流程**：
1. 读取 api-doc 模板的样例 URL（5个）
2. 启动 Playwright，使用 `../../stock-crawler/chrome_user_data` 的登录状态
3. 抓取页面 HTML
4. 分析 HTML 结构
5. 生成 XPath 抽取规则
6. 保存规则文件

**输出**：
```
正在处理模板: api-doc
样例数量: 5

启动浏览器...
  ✓ 使用用户数据目录: ../../stock-crawler/chrome_user_data

抓取样例页面...
  ✓ https://www.lixinger.com/open/api/doc
  ✓ https://www.lixinger.com/open/api/doc?api-key=cn/fund
  ✓ https://www.lixinger.com/open/api/doc?api-key=cn/index
  ✓ https://www.lixinger.com/open/api/doc?api-key=hk/index
  ✓ https://www.lixinger.com/open/api/doc?api-key=us/index

分析 HTML 结构...
  发现共同元素:
    - 标题 (h1): 5/5
    - 章节 (section): 5/5
    - 表格 (table): 5/5
    - 代码块 (pre code): 5/5

生成 XPath 规则...
  ✓ 主标题: //h1[@class='page-title']/text()
  ✓ 章节: //section[@class='api-section']
  ✓ 表格: .//table[@class='params-table']
  ✓ 代码块: .//pre/code/text()

保存模板文件...
  ✓ 已保存: ./output/api-doc.json

完成！
```

## 🔧 技术要求

### 性能要求

- 单个模板处理：< 30s（包括抓取5个页面）
- 内存占用：< 500MB

### 依赖要求

- Node.js >= 14
- Playwright（浏览器自动化）
- xpath 或 xpath-html（XPath 解析和生成）
- jsdom（HTML 解析，原生支持 XPath）

### 完全独立

**不依赖任何外部代码**：
- 不依赖 stock-crawler 的代码
- 不依赖其他 skills
- 只需要 url-patterns.json 作为输入

**复用浏览器状态**：
- 使用 stock-crawler 的 chrome_user_data 目录
- 路径：`../../stock-crawler/chrome_user_data`（相对于 skill 目录）
- 绝对路径：`/Users/fengzhi/Downloads/git/testlixingren/stock-crawler/chrome_user_data`

**Playwright 配置**：
```javascript
import { chromium } from 'playwright';
import path from 'path';

const userDataDir = path.resolve(__dirname, '../../stock-crawler/chrome_user_data');

const browser = await chromium.launchPersistentContext(userDataDir, {
  headless: true,
  channel: 'chrome'
});
```

**配置文件**（可选）：
```javascript
// config.json
{
  "browser": {
    "headless": true,
    "userDataDir": "../../stock-crawler/chrome_user_data",
    "channel": "chrome"
  },
  "timeout": 30000,
  "waitUntil": "networkidle"
}
```

## 🎨 架构设计

### 模块划分

```
html-template-generator/
├── lib/
│   ├── pattern-reader.js      # 读取 url-patterns.json
│   ├── browser-manager.js      # 浏览器管理（Playwright）
│   ├── html-fetcher.js         # 抓取页面 HTML
│   ├── structure-analyzer.js   # 分析 HTML 结构
│   ├── xpath-generator.js      # 生成 XPath 表达式
│   └── template-writer.js      # 输出模板文件
├── test/
│   └── *.test.js
├── docs/
│   ├── README.md
│   ├── USAGE_GUIDE.md
│   └── XPATH_GUIDE.md
├── output/                     # 生成的模板文件
├── config.json                 # 可选配置
├── run-skill.js                # 主入口
├── main.js                     # 核心逻辑
├── package.json
├── SKILL.md
└── README.md
```

### 数据流

```
url-patterns.json
    ↓
[Pattern Reader]
    ↓
模板 + 样例 URLs
    ↓
[Browser Manager] → Playwright + chrome_user_data
    ↓
[HTML Fetcher]
    ↓
HTML 内容
    ↓
[Structure Analyzer] ← jsdom (XPath support)
    ↓
结构模式
    ↓
[XPath Generator]
    ↓
XPath 规则
    ↓
[Template Writer]
    ↓
template.json
```

### 核心类设计

```javascript
// main.js
class TemplateGenerator {
  constructor(config) {
    this.patternReader = new PatternReader();
    this.browserManager = new BrowserManager({
      userDataDir: '../../stock-crawler/chrome_user_data',
      headless: true
    });
    this.htmlFetcher = new HTMLFetcher(this.browserManager);
    this.structureAnalyzer = new StructureAnalyzer();
    this.xpathGenerator = new XPathGenerator();
    this.templateWriter = new TemplateWriter();
  }
  
  async generate(templateName, patternsFile, outputFile) {
    // 1. 读取模板
    const template = await this.patternReader.read(patternsFile, templateName);
    
    // 2. 抓取样例
    const htmlContents = await this.htmlFetcher.fetchAll(template.samples);
    
    // 3. 分析结构
    const structure = await this.structureAnalyzer.analyze(htmlContents);
    
    // 4. 生成 XPath
    const xpaths = await this.xpathGenerator.generate(structure);
    
    // 5. 输出模板
    await this.templateWriter.write(outputFile, {
      templateName,
      xpaths,
      metadata: structure.metadata
    });
  }
}
```

## 🚀 实施计划

### 阶段 1：基础设施（1天）

- [ ] 创建项目结构
- [ ] 实现 pattern-reader（读取 url-patterns.json）
- [ ] 实现 html-fetcher（复用 stock-crawler）
- [ ] 测试页面抓取功能

### 阶段 2：结构分析（1-2天）

- [ ] 实现 structure-analyzer（使用 cheerio）
- [ ] 识别共同元素（标题、表格、代码块等）
- [ ] 计算元素频率

### 阶段 3：规则生成（1天）

- [ ] 实现 xpath-generator
- [ ] 生成 XPath 表达式
- [ ] 输出 JSON 格式规则

### 阶段 4：测试和文档（1天）

- [ ] 测试完整流程
- [ ] 编写文档
- [ ] 示例和教程

## 🎯 后续扩展

以下功能暂不实现，但预留扩展空间：

1. **规则验证**：在样例上验证生成的规则
2. **交互式优化**：人工/AI 调整规则
3. **批量处理**：一次处理多个模板
4. **与爬虫集成**：规则直接用于 stock-crawler

这些功能可以在核心功能稳定后逐步添加。

## 🤔 关键技术问题

### 1. XPath vs CSS 选择器

**为什么选择 XPath？**

✅ **XPath 优势**：
- 更强大：支持基于文本内容选择 `//h2[contains(text(), '参数')]`
- 更灵活：可以向上选择父节点 `//table/../div`
- 更精确：支持复杂逻辑 `//div[@class='content' and not(@class='hidden')]`
- 更适合模板：可以表达更复杂的抽取逻辑

❌ **CSS 选择器限制**：
- 不能基于文本内容选择
- 不能向上选择父节点
- 逻辑运算有限
- 主要用于样式，不是为数据抽取设计

**结论**：使用 XPath 生成模板

### 2. 浏览器状态管理

**问题**：如何处理需要登录的页面？

**方案**：使用 Playwright 的 launchPersistentContext

```javascript
import { chromium } from 'playwright';
import path from 'path';

const userDataDir = path.resolve(__dirname, '../../stock-crawler/chrome_user_data');

const browser = await chromium.launchPersistentContext(userDataDir, {
  headless: true,
  channel: 'chrome'
});
```

**优势**：
- 复用 stock-crawler 的 chrome_user_data 目录
- 已保存的登录状态（cookies、localStorage）自动加载
- 不需要登录逻辑
- 不需要配置用户名密码
- 完全独立，不依赖 stock-crawler 代码

**Playwright 优势**：
- ✅ 更现代、更稳定的 API
- ✅ 更好的等待机制（waitUntil: 'networkidle'）
- ✅ launchPersistentContext 原生支持
- ✅ 更好的错误处理
- ✅ 跨浏览器支持（虽然我们只用 Chrome）

### 3. HTML 解析库选择

**选项**：
1. **cheerio**：轻量、快速、类 jQuery API
2. **jsdom**：完整的 DOM 实现，支持 XPath

**推荐**：jsdom
- 原生支持 XPath：`document.evaluate()`
- 完整的 DOM API
- 更适合复杂的结构分析

### 4. 独立性设计

**原则**：完全独立，零依赖外部代码

**输入**：
- url-patterns.json（必需）
- userDataDir（可选，用于登录状态）

**输出**：
- template.json（XPath 抽取规则）

**不依赖**：
- stock-crawler
- 其他 skills
- 任何项目特定的代码

## 📚 参考资料

- url-pattern-analyzer 的设计模式
- stock-crawler 的 parser 架构
- Playwright 文档
- XPath 规范和最佳实践
- jsdom 文档
