# 模板分析器 - 设计文档

## 架构设计

### 系统架构图

```
┌─────────────────────────────────────────────────────────────┐
│                    Template Analyzer System                  │
│                         (Skills-Based)                       │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────┐         ┌──────────────────┐          │
│  │   Skill 1:       │         │   Skill 2:       │          │
│  │   URL Pattern    │────────▶│   Template       │          │
│  │   Analyzer       │         │   Content        │          │
│  │                  │         │   Analyzer       │          │
│  └──────────────────┘         │   +              │          │
│         │                     │   Config         │          │
│         │                     │   Generator      │          │
│         │                     └──────────────────┘          │
│         │                              │                     │
│         ▼                              ▼                     │
│  ┌──────────────────┐         ┌──────────────────┐          │
│  │   URL Patterns   │         │  template-rules  │          │
│  │   JSON           │         │  .jsonl          │          │
│  └──────────────────┘         └──────────────────┘          │
│                                        │                     │
│                                        ▼                     │
│                               ┌──────────────────┐          │
│                               │  Test Script:    │          │
│                               │  Template Parser │          │
│                               │  (验证配置)       │          │
│                               └──────────────────┘          │
│                                                               │
└─────────────────────────────────────────────────────────────┘

Skills位置: 项目根目录/skills/
  - skills/url-pattern-analyzer/
  - skills/template-content-analyzer/
```

### Skills架构

#### Skill 1: URL Pattern Analyzer

**位置**: `skills/url-pattern-analyzer/`

**结构**:
```
skills/url-pattern-analyzer/
├── README.md              # Skill说明文档
├── skill.json             # Skill配置
├── main.js                # 入口文件
├── lib/
│   ├── url-clusterer.js   # URL聚类算法
│   ├── similarity.js      # 相似度计算
│   └── pattern-gen.js     # 正则表达式生成
└── test/
    └── test-analyzer.js   # 测试脚本
```

**执行方式**: 由大模型调用，传入参数

**输入**:
```json
{
  "linksFile": "stock-crawler/output/lixinger-crawler/links.txt",
  "outputFile": "stock-crawler/output/lixinger-crawler/url-patterns.json",
  "similarityThreshold": 0.7
}
```

**输出**:
```json
{
  "patterns": [
    {
      "name": "api-doc",
      "pathTemplate": "/open/api/doc",
      "pattern": "^https://www\\.lixinger\\.com/open/api/doc\\?api-key=(.+)$",
      "queryParams": ["api-key"],
      "urlCount": 163,
      "samples": [...]
    }
  ]
}
```

#### Skill 2: Template Content Analyzer + Config Generator

**位置**: `skills/template-content-analyzer/`

**结构**:
```
skills/template-content-analyzer/
├── README.md                    # Skill说明文档
├── skill.json                   # Skill配置
├── main.js                      # 入口文件
├── lib/
│   ├── content-analyzer.js      # 内容分析
│   ├── frequency-calc.js        # 频率计算
│   ├── structure-detector.js    # 数据结构识别
│   ├── config-generator.js      # 配置生成器
│   └── validator.js             # 实时验证（可选）
├── scripts/
│   └── test-template-parser.js  # Template Parser测试脚本
└── test/
    └── test-analyzer.js         # 测试脚本
```

**执行方式**: 由大模型调用，传入参数

**输入**:
```json
{
  "urlPatternsFile": "stock-crawler/output/lixinger-crawler/url-patterns.json",
  "pagesDir": "stock-crawler/output/lixinger-crawler/pages",
  "outputFile": "stock-crawler/output/lixinger-crawler/template-rules.jsonl",
  "sampleUrls": ["https://..."],
  "frequencyThresholds": {
    "template": 0.8,
    "unique": 0.2
  }
}
```

**输出**:
```jsonl
{"name":"api-doc","description":"...","extractors":[...],"filters":[...],"metadata":{...}}
{"name":"dashboard","description":"...","extractors":[...],"filters":[...],"metadata":{...}}
```

#### Test Script: Template Parser

**位置**: `skills/template-content-analyzer/scripts/test-template-parser.js`

**功能**: 
- 加载生成的配置文件
- 创建TemplateParser实例
- 测试配置驱动的解析
- 验证提取效果

**不集成到现有代码**: 仅作为测试工具使用

#### 1. URL Pattern Analyzer（URL模式分析器）

**职责**: 分析links.txt，识别URL模式并分组

**核心算法**:
```javascript
class URLPatternAnalyzer {
  // 1. 提取URL结构特征
  extractFeatures(url) {
    return {
      protocol: url.protocol,
      host: url.host,
      pathSegments: url.pathname.split('/'),
      queryParams: Object.keys(url.searchParams),
      pathDepth: url.pathname.split('/').length
    };
  }
  
  // 2. 计算URL相似度
  calculateSimilarity(url1, url2) {
    const f1 = this.extractFeatures(url1);
    const f2 = this.extractFeatures(url2);
    
    // 路径深度相同 +20分
    // 路径段匹配 +10分/段
    // 查询参数匹配 +5分/参数
    // 总分100分，>70分认为相似
  }
  
  // 3. 聚类算法（层次聚类）
  clusterURLs(urls, threshold = 0.7) {
    // 初始化：每个URL一个簇
    // 迭代：合并最相似的两个簇
    // 停止：相似度 < threshold
  }
  
  // 4. 生成正则表达式
  generatePattern(urlGroup) {
    // 找出变化的部分（参数）
    // 固定的部分保持不变
    // 生成正则表达式
  }
}
```

**输入**: 
```json
[
  {"url": "https://www.lixinger.com/open/api/doc?api-key=cn/company"},
  {"url": "https://www.lixinger.com/open/api/doc?api-key=hk/index"},
  {"url": "https://www.lixinger.com/analytics/company/dashboard"}
]
```

**输出**:
```json
{
  "patterns": [
    {
      "name": "api-doc",
      "pattern": "^https://www\\.lixinger\\.com/open/api/doc\\?api-key=(.+)$",
      "pathTemplate": "/open/api/doc",
      "queryParams": ["api-key"],
      "urlCount": 163,
      "samples": [
        "https://www.lixinger.com/open/api/doc?api-key=cn/company",
        "https://www.lixinger.com/open/api/doc?api-key=hk/index"
      ]
    }
  ]
}
```

#### 2. Template Content Analyzer（模板内容分析器）

**职责**: 针对一个pathTemplate，分析其对应的所有页面，生成该模板的解析配置

**输入**：
- pathTemplate: URL模式（如 `/open/api/doc`）
- urlPattern: 正则表达式和查询参数
- markdownFiles: 该模板对应的所有已抓取页面
- sampleUrls: （可选）实时抓取样例进行验证

**输出**：
- 一个完整的TemplateConfig对象（包含extractors和filters）

**核心算法**:
```javascript
class TemplateContentAnalyzer {
  /**
   * 分析一个pathTemplate，生成其解析配置
   * @param {URLPattern} urlPattern - URL模式信息
   * @param {string[]} markdownFiles - 该模板的所有markdown文件路径
   * @param {string[]} sampleUrls - 可选的样例URL用于实时验证
   * @returns {TemplateConfig} 完整的模板配置
   */
  async analyzeTemplate(urlPattern, markdownFiles, sampleUrls = []) {
    // 1. 加载所有markdown文件
    const pages = await this.loadPages(markdownFiles);
    
    // 2. 提取内容块并计算频率
    const frequency = this.calculateFrequency(pages);
    
    // 3. 分类内容（模板/独特/混合）
    const classified = this.classifyContent(frequency, pages.length);
    
    // 4. 识别数据结构
    const dataStructures = this.identifyDataStructures(pages);
    
    // 5. 生成提取器配置
    const extractors = this.generateExtractors(dataStructures, classified);
    
    // 6. 生成过滤器配置
    const filters = this.generateFilters(classified.template);
    
    // 7. 如果提供了样例URL，实时验证配置
    if (sampleUrls.length > 0) {
      await this.validateConfig(extractors, filters, sampleUrls);
    }
    
    // 8. 返回完整配置
    return {
      name: this.generateTemplateName(urlPattern),
      description: `Parser configuration for ${urlPattern.pathTemplate}`,
      priority: 100,
      urlPattern: {
        pattern: urlPattern.pattern.toString(),
        pathTemplate: urlPattern.pathTemplate,
        queryParams: urlPattern.queryParams
      },
      extractors,
      filters,
      metadata: {
        generatedAt: new Date().toISOString(),
        pageCount: pages.length,
        version: '1.0.0'
      }
    };
  }
  
  // 1. 提取内容块
  extractContentBlocks(markdownContent) {
    const blocks = [];
    
    // 按markdown结构分块
    // - 标题（## xxx）
    // - 段落（连续的文本行）
    // - 表格（| xxx |）
    // - 代码块（```xxx```）
    // - 列表（- xxx 或 1. xxx）
    
    return blocks;
  }
  
  // 2. 标准化文本（用于比较）
  normalizeText(text) {
    return text
      .toLowerCase()
      .replace(/\s+/g, ' ')
      .replace(/[^\w\s]/g, '')
      .trim();
  }
  
  // 3. 计算内容频率
  calculateFrequency(pages) {
    const blockFrequency = new Map();
    
    pages.forEach(page => {
      const blocks = this.extractContentBlocks(page);
      blocks.forEach(block => {
        const normalized = this.normalizeText(block.content);
        const key = `${block.type}:${normalized}`;
        blockFrequency.set(key, (blockFrequency.get(key) || 0) + 1);
      });
    });
    
    return blockFrequency;
  }
  
  // 4. 分类内容
  classifyContent(frequency, totalPages) {
    const result = {
      template: [],  // 高频 >80%
      unique: [],    // 低频 <20%
      mixed: []      // 中频 20-80%
    };
    
    frequency.forEach((count, key) => {
      const ratio = count / totalPages;
      const [type, content] = key.split(':');
      
      if (ratio > 0.8) {
        result.template.push({ type, content, ratio });
      } else if (ratio < 0.2) {
        result.unique.push({ type, content, ratio });
      } else {
        result.mixed.push({ type, content, ratio });
      }
    });
    
    return result;
  }
  
  // 5. 识别数据结构
  identifyDataStructures(pages) {
    // 分析表格结构（列名、列数）
    // 分析代码块（语言、格式）
    // 分析列表（类型、层级）
    return {
      tables: this.analyzeTableStructures(pages),
      codeBlocks: this.analyzeCodeBlocks(pages),
      lists: this.analyzeLists(pages)
    };
  }
  
  // 6. 生成提取器配置
  generateExtractors(dataStructures, classified) {
    const extractors = [];
    
    // 标题提取
    extractors.push({
      field: 'title',
      type: 'text',
      selector: 'h1, h2, title',
      required: true
    });
    
    // 根据数据结构生成提取器
    if (dataStructures.tables.length > 0) {
      dataStructures.tables.forEach((table, index) => {
        extractors.push({
          field: index === 0 ? 'mainTable' : `table${index}`,
          type: 'table',
          selector: 'table',
          columns: table.columns
        });
      });
    }
    
    if (dataStructures.codeBlocks.length > 0) {
      extractors.push({
        field: 'codeBlocks',
        type: 'code',
        selector: 'pre code, pre, textarea[readonly]'
      });
    }
    
    return extractors;
  }
  
  // 7. 生成过滤器配置
  generateFilters(templateContent) {
    const filters = [];
    
    // 基于高频内容生成过滤规则
    templateContent.forEach(content => {
      if (content.ratio > 0.9) {
        filters.push({
          type: 'remove',
          target: content.type,
          pattern: this.escapeRegex(content.content.substring(0, 50)),
          reason: `Template noise (${(content.ratio * 100).toFixed(0)}% frequency)`
        });
      }
    });
    
    return filters;
  }
  
  // 8. 实时验证配置
  async validateConfig(extractors, filters, sampleUrls) {
    // 使用Playwright实时抓取样例URL
    // 应用extractors和filters
    // 验证提取效果
    // 如果效果不好，调整配置
    console.log(`Validating config with ${sampleUrls.length} sample URLs...`);
  }
}
```

**输入**: 
```javascript
{
  urlPattern: {
    name: "api-doc",
    pattern: /^https:\/\/www\.lixinger\.com\/open\/api\/doc\?api-key=(.+)$/,
    pathTemplate: "/open/api/doc",
    queryParams: ["api-key"],
    urlCount: 163,
    samples: [...]
  },
  markdownFiles: [
    "output/lixinger-crawler/pages/API文档_cn_company.md",
    "output/lixinger-crawler/pages/API文档_hk_index.md",
    // ... 163个文件
  ],
  sampleUrls: [
    "https://www.lixinger.com/open/api/doc?api-key=cn/company",
    "https://www.lixinger.com/open/api/doc?api-key=cn/index"
  ]
}
```

**输出**:
```json
{
  "name": "api-doc",
  "description": "Parser configuration for /open/api/doc",
  "priority": 100,
  "urlPattern": {
    "pattern": "/^https:\\/\\/www\\.lixinger\\.com\\/open\\/api\\/doc\\?api-key=(.+)$/",
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
      "field": "requestUrl",
      "type": "text",
      "selector": "code, pre",
      "pattern": "open\\.lixinger\\.com|api\\.lixinger"
    },
    {
      "field": "parameters",
      "type": "table",
      "selector": "table",
      "columns": ["参数名称", "必选", "类型", "说明"]
    },
    {
      "field": "responseData",
      "type": "table",
      "selector": "table",
      "columns": ["字段", "类型", "说明"]
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
    },
    {
      "type": "remove",
      "target": "heading",
      "pattern": "导航",
      "reason": "Template noise (100% frequency)"
    }
  ],
  "metadata": {
    "generatedAt": "2026-02-25T10:00:00.000Z",
    "pageCount": 163,
    "version": "1.0.0",
    "validated": true,
    "sampleCount": 2
  }
}
```

#### 3. Template Config Generator（模板配置生成器）

**职责**: 根据分析结果生成JSONL格式的模板配置文件

**配置格式**:
```javascript
class TemplateConfigGenerator {
  /**
   * 生成模板配置
   * @param {TemplateAnalysis} analysis - 模板分析结果
   * @returns {Object} 配置对象
   */
  generateConfig(analysis) {
    return {
      // 基本信息
      name: analysis.templateName,
      description: `Parser configuration for ${analysis.templateName}`,
      priority: 100,
      
      // URL匹配规则
      urlPattern: {
        pattern: analysis.urlPattern.pattern.toString(),
        pathTemplate: analysis.urlPattern.pathTemplate,
        queryParams: analysis.urlPattern.queryParams
      },
      
      // 数据提取规则
      extractors: this.generateExtractors(analysis),
      
      // 噪音过滤规则
      filters: this.generateFilters(analysis),
      
      // 元数据
      metadata: {
        generatedAt: new Date().toISOString(),
        pageCount: analysis.pageCount,
        version: '1.0.0'
      }
    };
  }
  
  /**
   * 生成提取器配置
   */
  generateExtractors(analysis) {
    const extractors = [];
    
    // 标题提取
    extractors.push({
      field: 'title',
      type: 'text',
      selector: 'h1, h2, title',
      required: true
    });
    
    // 根据数据结构生成提取器
    if (analysis.dataStructures.tables.length > 0) {
      extractors.push({
        field: 'tables',
        type: 'table',
        selector: 'table',
        columns: analysis.dataStructures.tables[0].columns
      });
    }
    
    if (analysis.dataStructures.codeBlocks.length > 0) {
      extractors.push({
        field: 'codeBlocks',
        type: 'code',
        selector: 'pre code, pre, textarea[readonly]'
      });
    }
    
    return extractors;
  }
  
  /**
   * 生成过滤器配置
   */
  generateFilters(analysis) {
    const filters = [];
    
    // 基于高频内容生成过滤规则
    analysis.templateContent.forEach(content => {
      if (content.ratio > 0.9) {
        filters.push({
          type: 'remove',
          target: content.type,
          pattern: this.escapeRegex(content.content.substring(0, 50)),
          reason: `Template noise (${(content.ratio * 100).toFixed(0)}% frequency)`
        });
      }
    });
    
    return filters;
  }
  
  /**
   * 保存为JSONL格式
   */
  saveAsJSONL(configs, outputPath) {
    const lines = configs.map(config => JSON.stringify(config));
    fs.writeFileSync(outputPath, lines.join('\n'), 'utf-8');
  }
}
```

**配置示例**:
```json
{
  "name": "api-doc",
  "description": "Parser configuration for api-doc",
  "priority": 100,
  "urlPattern": {
    "pattern": "/\\/api\\/doc/",
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
      "field": "requestUrl",
      "type": "text",
      "selector": "code, pre",
      "pattern": "open\\.lixinger\\.com|api\\.lixinger"
    },
    {
      "field": "parameters",
      "type": "table",
      "selector": "table",
      "columns": ["参数", "必选", "类型", "说明"]
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
    "generatedAt": "2026-02-25T10:00:00.000Z",
    "pageCount": 163,
    "version": "1.0.0"
  }
}
```

**输入**: TemplateAnalysis对象

**输出**: JSONL配置文件 (`output/{project}/template-rules.jsonl`)

#### 4. Template Parser（模板解析器）

**职责**: 读取配置文件并执行数据提取

**实现**:
```javascript
class TemplateParser extends BaseParser {
  constructor(config) {
    super();
    this.config = config;
    this.pattern = new RegExp(config.urlPattern.pattern);
  }
  
  /**
   * 检查URL是否匹配
   */
  matches(url) {
    return this.pattern.test(url);
  }
  
  /**
   * 获取优先级
   */
  getPriority() {
    return this.config.priority || 0;
  }
  
  /**
   * 解析页面
   */
  async parse(page, url, options = {}) {
    try {
      const result = {
        type: this.config.name,
        url
      };
      
      // 执行所有提取器
      for (const extractor of this.config.extractors) {
        result[extractor.field] = await this.executeExtractor(page, extractor);
      }
      
      // 应用过滤器
      return this.applyFilters(result);
    } catch (error) {
      console.error(`Failed to parse ${this.config.name} page:`, error.message);
      return { type: this.config.name, url, error: error.message };
    }
  }
  
  /**
   * 执行提取器
   */
  async executeExtractor(page, extractor) {
    switch (extractor.type) {
      case 'text':
        return await this.extractText(page, extractor);
      case 'table':
        return await this.extractTable(page, extractor);
      case 'code':
        return await this.extractCode(page, extractor);
      default:
        return null;
    }
  }
  
  /**
   * 应用过滤器
   */
  applyFilters(result) {
    // 根据配置的filters移除噪音内容
    return result;
  }
}

/**
 * 配置加载器
 */
class ConfigLoader {
  /**
   * 从JSONL文件加载配置
   */
  static loadConfigs(jsonlPath) {
    const content = fs.readFileSync(jsonlPath, 'utf-8');
    const lines = content.trim().split('\n');
    return lines.map(line => JSON.parse(line));
  }
  
  /**
   * 创建Parser实例
   */
  static createParsers(jsonlPath) {
    const configs = this.loadConfigs(jsonlPath);
    return configs.map(config => new TemplateParser(config));
  }
}
```

**使用方式**:
```javascript
// 在crawler-main.js中加载配置
const configPath = path.join(outputDir, 'template-rules.jsonl');
if (fs.existsSync(configPath)) {
  const templateParsers = ConfigLoader.createParsers(configPath);
  parsers.push(...templateParsers);
}
```

## 数据流

```
1. 读取 links.txt
   ↓
2. 【Skill 1: URL Pattern Analyzer】
   ├─ 由大模型执行
   ├─ 调用算法库（聚类、相似度计算）
   ├─ 提取URL特征
   ├─ 计算相似度
   ├─ 聚类分组（按pathTemplate）
   └─ 生成正则表达式
   ↓
3. 输出 url-patterns.json
   [
     { name: "api-doc", pathTemplate: "/open/api/doc", urls: [...] },
     { name: "dashboard", pathTemplate: "/analytics/*/dashboard", urls: [...] }
   ]
   ↓
4. 【Skill 2: Template Content Analyzer + Config Generator】
   ├─ 由大模型执行
   ├─ 读取url-patterns.json
   ├─ 对每个pathTemplate：
   │  ├─ 收集该模板的所有markdown文件
   │  ├─ 提取内容块
   │  ├─ 计算频率
   │  ├─ 分类内容（模板/独特/混合）
   │  ├─ 识别数据结构（表格/代码/列表）
   │  ├─ 生成提取器配置
   │  ├─ 生成过滤器配置
   │  ├─ 实时验证（可选）
   │  └─ 生成TemplateConfig对象
   ├─ 收集所有TemplateConfig
   └─ 保存为JSONL格式
   ↓
5. 输出 template-rules.jsonl
   每行一个TemplateConfig JSON对象
   ↓
6. 【测试脚本: Template Parser】
   ├─ 位置：skills/template-content-analyzer/scripts/
   ├─ 加载template-rules.jsonl
   ├─ 创建TemplateParser实例
   ├─ 测试配置驱动的解析
   ├─ 验证提取效果
   └─ 生成测试报告
```

**关键点**：
- Skills放在项目根目录 `skills/`
- 由大模型执行，可调用算法库
- Template Parser作为测试脚本，不集成到现有代码
- 整体测试后再考虑集成

## 技术选型

### 核心技术
- **语言**: JavaScript (ES6+)
- **运行环境**: Node.js
- **文件系统**: fs/promises
- **正则表达式**: 内置RegExp

### 算法选择
- **URL聚类**: 层次聚类（Hierarchical Clustering）
- **文本相似度**: 编辑距离（Levenshtein Distance）
- **频率统计**: HashMap计数

### 数据格式
- **输入**: JSON (links.txt), Markdown (pages/*.md)
- **中间**: JSON (分析报告)
- **输出**: JavaScript (Parser代码)

## 接口设计

### Skill 1: url-pattern-analyzer

**安装位置**: `skills/url-pattern-analyzer/`

**调用方式**: 大模型执行

**输入**:
```json
{
  "linksFile": "stock-crawler/output/lixinger-crawler/links.txt",
  "outputFile": "stock-crawler/output/lixinger-crawler/url-patterns.json",
  "similarityThreshold": 0.7,
  "minGroupSize": 5
}
```

**输出**:
```json
{
  "success": true,
  "patternsFile": "stock-crawler/output/lixinger-crawler/url-patterns.json",
  "patternCount": 5,
  "totalUrls": 8403,
  "patterns": [
    {
      "name": "api-doc",
      "pathTemplate": "/open/api/doc",
      "pattern": "^https://www\\.lixinger\\.com/open/api/doc\\?api-key=(.+)$",
      "queryParams": ["api-key"],
      "urlCount": 163,
      "samples": [
        "https://www.lixinger.com/open/api/doc?api-key=cn/company",
        "https://www.lixinger.com/open/api/doc?api-key=hk/index"
      ]
    }
  ]
}
```

### Skill 2: template-content-analyzer

**安装位置**: `skills/template-content-analyzer/`

**调用方式**: 大模型执行

**输入**:
```json
{
  "urlPatternsFile": "stock-crawler/output/lixinger-crawler/url-patterns.json",
  "pagesDir": "stock-crawler/output/lixinger-crawler/pages",
  "outputFile": "stock-crawler/output/lixinger-crawler/template-rules.jsonl",
  "sampleUrls": [
    "https://www.lixinger.com/open/api/doc?api-key=cn/company",
    "https://www.lixinger.com/open/api/doc?api-key=cn/index"
  ],
  "frequencyThresholds": {
    "template": 0.8,
    "unique": 0.2
  },
  "enableValidation": true
}
```

**输出**:
```json
{
  "success": true,
  "configFile": "stock-crawler/output/lixinger-crawler/template-rules.jsonl",
  "configsGenerated": 5,
  "totalExtractors": 23,
  "totalFilters": 15,
  "configs": [
    {
      "name": "api-doc",
      "pageCount": 163,
      "extractorsGenerated": 6,
      "filtersGenerated": 2,
      "validated": true
    }
  ]
}
```

### Test Script: test-template-parser.js

**位置**: `skills/template-content-analyzer/scripts/test-template-parser.js`

**用途**: 测试生成的配置文件

**运行方式**:
```bash
node skills/template-content-analyzer/scripts/test-template-parser.js \
  --config stock-crawler/output/lixinger-crawler/template-rules.jsonl \
  --test-urls stock-crawler/output/lixinger-crawler/test-urls.txt
```

**功能**:
1. 加载配置文件
2. 创建TemplateParser实例
3. 对测试URL进行解析
4. 验证提取效果
5. 生成测试报告

## 配置设计

### config/template-analyzer.json

```json
{
  "urlAnalysis": {
    "similarityThreshold": 0.7,
    "minGroupSize": 5,
    "maxGroups": 20
  },
  "contentAnalysis": {
    "frequencyThresholds": {
      "template": 0.8,
      "unique": 0.2
    },
    "minBlockLength": 10,
    "ignorePatterns": [
      "^\\s*$",
      "^Copyright",
      "^©"
    ]
  },
  "configGeneration": {
    "outputFormat": "jsonl",
    "includeComments": true,
    "includeMetadata": true,
    "defaultPriority": 100
  }
}
```

## 错误处理

### 错误类型

1. **文件读取错误**
   - links.txt不存在
   - markdown文件不存在
   - 文件格式错误

2. **分析错误**
   - URL格式无效
   - 无法识别模式
   - 页面内容为空

3. **生成错误**
   - 模板文件不存在
   - 生成的代码语法错误
   - 文件写入失败

### 错误处理策略

```javascript
class ErrorHandler {
  handle(error, context) {
    // 1. 记录错误日志
    logger.error(`Error in ${context}:`, error);
    
    // 2. 根据错误类型决定是否继续
    if (error.type === 'CRITICAL') {
      throw error;  // 停止执行
    } else {
      // 记录警告，继续处理其他项
      logger.warn(`Skipping ${context} due to error`);
      return null;
    }
  }
}
```

## 性能优化

### 1. 批量处理
```javascript
// 不要一次性加载所有页面
// 使用流式处理
async function* readPagesInBatches(urls, batchSize = 100) {
  for (let i = 0; i < urls.length; i += batchSize) {
    const batch = urls.slice(i, i + batchSize);
    yield await Promise.all(batch.map(loadPage));
  }
}
```

### 2. 缓存计算结果
```javascript
class CachedAnalyzer {
  constructor() {
    this.cache = new Map();
  }
  
  analyze(key, fn) {
    if (this.cache.has(key)) {
      return this.cache.get(key);
    }
    const result = fn();
    this.cache.set(key, result);
    return result;
  }
}
```

### 3. 并行处理
```javascript
// 多个URL组可以并行分析
const analyses = await Promise.all(
  urlGroups.map(group => analyzeTemplate(group))
);
```

## 测试策略

### 单元测试

```javascript
describe('URLPatternAnalyzer', () => {
  test('should extract URL features correctly', () => {
    const url = 'https://www.lixinger.com/open/api/doc?api-key=cn/company';
    const features = analyzer.extractFeatures(url);
    expect(features.pathSegments).toEqual(['', 'open', 'api', 'doc']);
    expect(features.queryParams).toEqual(['api-key']);
  });
  
  test('should calculate similarity correctly', () => {
    const url1 = 'https://www.lixinger.com/open/api/doc?api-key=cn/company';
    const url2 = 'https://www.lixinger.com/open/api/doc?api-key=hk/index';
    const similarity = analyzer.calculateSimilarity(url1, url2);
    expect(similarity).toBeGreaterThan(0.7);
  });
});
```

### 集成测试

```javascript
describe('Template Analyzer Workflow', () => {
  test('should complete full analysis workflow', async () => {
    const result = await runWorkflow({
      linksFile: 'test/fixtures/links.txt',
      pagesDir: 'test/fixtures/pages',
      outputDir: 'test/output'
    });
    
    expect(result.success).toBe(true);
    expect(result.parsersGenerated).toBeGreaterThan(0);
    expect(fs.existsSync(result.files[0])).toBe(true);
  });
});
```

## 部署和使用

### 安装Skills

```bash
# 将skills放到项目的.kiro/skills目录
mkdir -p .kiro/skills
cp -r skills/template-analyzer .kiro/skills/
```

### 使用方式

```bash
# 方式1: 使用完整工作流
node scripts/run-template-analyzer.js

# 方式2: 分步执行
node scripts/analyze-url-patterns.js
node scripts/analyze-page-template.js api-doc
node scripts/generate-parser-code.js api-doc

# 方式3: 通过Kiro调用skill
# (如果集成到Kiro系统中)
```

## 维护和扩展

### 添加新的URL模式识别算法

```javascript
// 在 URLPatternAnalyzer 中添加新方法
class URLPatternAnalyzer {
  // 现有方法...
  
  // 新增：基于机器学习的模式识别
  mlBasedClustering(urls) {
    // 实现基于ML的聚类
  }
}
```

### 添加新的代码模板

```javascript
// 在 config/templates/ 中添加新模板
// custom-parser-template.js
```

### 支持其他网站

```javascript
// 创建网站特定的配置
// config/templates/eastmoney-analyzer.json
```

## 文档

- 用户手册：如何使用skills
- 开发文档：如何扩展功能
- API文档：各个类和方法的说明
- 示例：常见使用场景

## 总结

这个设计提供了一个完整的、可扩展的模板分析和代码生成系统。通过将功能封装为skills，使得整个流程可以自动化执行，大大提高了开发效率。
