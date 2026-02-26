# Template Analyzer Skills - 架构文档

## 概述

Template Analyzer 系统由 2 个独立的 Skills 组成，用于自动分析网站 URL 模式和页面模板，生成配置驱动的解析规则。

## 系统架构

### 整体架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                  Template Analyzer System                        │
│                      (2 Skills 架构)                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  输入: links.txt (8403 URLs)                                     │
│         pages/*.md (已抓取的页面)                                │
│                                                                   │
│  ┌──────────────────────┐                                        │
│  │   Skill 1:           │                                        │
│  │   url-pattern-       │                                        │
│  │   analyzer           │                                        │
│  │                      │                                        │
│  │  职责:               │                                        │
│  │  - 读取 links.txt    │                                        │
│  │  - URL 聚类分组      │                                        │
│  │  - 生成正则表达式    │                                        │
│  └──────────┬───────────┘                                        │
│             │                                                     │
│             ▼                                                     │
│  输出: url-patterns.json                                         │
│  [                                                                │
│    {                                                              │
│      name: "api-doc",                                            │
│      pathTemplate: "/open/api/doc",                              │
│      pattern: "^https://...",                                    │
│      urlCount: 163,                                              │
│      samples: [...]                                              │
│    }                                                              │
│  ]                                                                │
│             │                                                     │
│             ▼                                                     │
│  ┌──────────────────────┐                                        │
│  │   Skill 2:           │                                        │
│  │   template-content-  │                                        │
│  │   analyzer           │                                        │
│  │                      │                                        │
│  │  职责:               │                                        │
│  │  - 读取 url-patterns │                                        │
│  │  - 分析页面内容      │                                        │
│  │  - 识别模板/数据     │                                        │
│  │  - 生成配置文件      │                                        │
│  └──────────┬───────────┘                                        │
│             │                                                     │
│             ▼                                                     │
│  输出: template-rules.jsonl                                      │
│  (每行一个 TemplateConfig JSON 对象)                             │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

### 目录结构

```
skills/
├── url-pattern-analyzer/              # Skill 1: URL 模式分析器
│   ├── main.js                        # 入口文件
│   ├── skill.json                     # Skill 配置
│   ├── README.md                      # 使用说明
│   ├── lib/                           # 算法库
│   │   ├── url-clusterer.js           # URL 聚类算法
│   │   ├── links-reader.js            # links.txt 读取器
│   │   └── report-generator.js        # 报告生成器
│   ├── test/                          # 测试
│   │   ├── url-clusterer.test.js
│   │   ├── links-reader.test.js
│   │   └── performance.test.js
│   └── scripts/                       # 工具脚本
│       └── analyze-url-patterns.js
│
├── template-content-analyzer/         # Skill 2: 模板内容分析器
│   ├── main.js                        # 入口文件
│   ├── skill.json                     # Skill 配置
│   ├── README.md                      # 使用说明
│   ├── lib/                           # 算法库
│   │   ├── content-analyzer.js        # 内容分析
│   │   ├── template-config-generator.js  # 配置生成
│   │   ├── template-parser.js         # 模板解析器
│   │   └── config-loader.js           # 配置加载器
│   ├── test/                          # 测试
│   │   ├── content-analyzer.test.js
│   │   ├── template-config-generator.test.js
│   │   ├── template-parser.test.js
│   │   └── performance.test.js
│   ├── scripts/                       # 工具脚本
│   │   ├── analyze-page-template.js
│   │   ├── generate-template-config.js
│   │   └── test-real-pages.js
│   └── docs/                          # 文档
│       ├── CONFIG_FORMAT.md
│       ├── EXTRACTOR_GUIDE.md
│       ├── FILTER_GUIDE.md
│       ├── CONFIG_EXAMPLES.md
│       └── USAGE_GUIDE.md
│
├── ARCHITECTURE.md                    # 本文档
├── INSTALLATION_GUIDE.md              # 安装指南
└── test-complete-workflow.js          # 完整工作流测试
```

## Skill 1: URL Pattern Analyzer

### 职责

从 `links.txt` 文件中识别 URL 模式，按 `pathTemplate` 分组。

### 核心算法

#### 1. URL 特征提取

```javascript
extractFeatures(url) {
  return {
    protocol: 'https',
    host: 'www.lixinger.com',
    pathSegments: ['open', 'api', 'doc'],
    queryParams: ['api-key'],
    pathDepth: 3
  };
}
```

**提取的特征:**
- **protocol**: 协议（http/https）
- **host**: 主机名
- **pathSegments**: 路径段数组（去除空段）
- **queryParams**: 查询参数键列表
- **pathDepth**: 路径深度

#### 2. URL 相似度计算

```javascript
calculateSimilarity(url1, url2) {
  // 评分规则:
  // - 协议和主机不同: 0 分
  // - 路径深度相同: +20 分
  // - 每个匹配的路径段: +10 分
  // - 每个匹配的查询参数: +5 分
  
  // 返回相似度分数，由聚类算法决定分组
}
```

**相似度评分规则:**
- 协议或主机不同 → 0 分（不会聚在一起）
- 路径深度相同 → +20 分
- 每个匹配的路径段 → +10 分
- 每个匹配的查询参数 → +5 分

**示例:**
```javascript
url1 = 'https://www.lixinger.com/open/api/doc?api-key=cn/company'
url2 = 'https://www.lixinger.com/open/api/doc?api-key=hk/index'

// 相似度 = 20 (深度) + 30 (3个路径段) + 5 (1个参数) = 55 分
```

#### 3. URL 聚类算法

使用**层次聚类（Hierarchical Clustering）**算法:

```javascript
clusterURLs(urls) {
  // 1. 初始化: 每个 URL 一个簇
  let clusters = urls.map(url => [url]);
  
  // 2. 迭代合并相似的簇
  while (canMerge) {
    // 找到最相似的两个簇
    const [cluster1, cluster2] = findMostSimilarClusters(clusters);
    
    // 合并簇
    clusters = mergeClusters(cluster1, cluster2);
  }
  
  // 3. 返回聚类结果
  return clusters;
}
```

**判断依据:**
- URL 正则匹配
- 页面是否同一个后端渲染
- **不使用固定阈值**，而是动态决定分组

#### 4. 正则表达式生成

```javascript
generatePattern(urlGroup) {
  // 分析 URL 组，识别固定部分和变化部分
  // 固定段: 保持不变
  // 变化段: 用捕获组 ([^/]+) 表示
  
  return {
    pattern: '^https://www\\.lixinger\\.com/open/api/([^/]+)(\\?.*)?$',
    pathTemplate: '/open/api/{param2}',
    queryParams: ['api-key']
  };
}
```

### 数据流

```
links.txt (8403 URLs)
    ↓
LinksReader.readLinksFile()
    ↓
LinksReader.extractURLs({ status: 'fetched', excludeErrors: true })
    ↓
URLClusterer.clusterURLs()
    ↓
URLClusterer.generatePattern() (for each cluster)
    ↓
ReportGenerator.generateJSON()
    ↓
url-patterns.json
```

### 输入输出

**输入:** `links.txt`
```json
{"url":"https://www.lixinger.com/open/api/doc?api-key=cn/company","status":"fetched","addedAt":1234567890}
{"url":"https://www.lixinger.com/open/api/doc?api-key=hk/index","status":"fetched","addedAt":1234567891}
```

**输出:** `url-patterns.json`
```json
{
  "success": true,
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

## Skill 2: Template Content Analyzer

### 职责

针对每个 `pathTemplate`，分析其对应的所有页面，生成该模板的解析配置。

### 核心算法

#### 1. 内容块提取

```javascript
extractContentBlocks(markdown) {
  // 识别 markdown 结构:
  // - 标题: # 标题, ## 标题
  // - 段落: 连续的文本行
  // - 表格: | 列1 | 列2 |
  // - 代码块: ```language ... ```
  // - 列表: - 项目 或 1. 项目
  
  return [
    { type: 'heading', content: '# API文档', lineNumber: 1 },
    { type: 'paragraph', content: '获取用户信息', lineNumber: 2 },
    { type: 'table', content: '...', rows: 3, lineNumber: 4 }
  ];
}
```

#### 2. 频率计算

```javascript
calculateFrequency(pages) {
  const frequency = new Map();
  
  pages.forEach((page, pageIndex) => {
    const blocks = extractContentBlocks(page);
    
    blocks.forEach(block => {
      const normalized = normalizeText(block.content);
      const key = `${block.type}:${normalized}`;
      
      if (!frequency.has(key)) {
        frequency.set(key, {
          type: block.type,
          content: block.content,
          normalizedContent: normalized,
          count: 0,
          pages: []
        });
      }
      
      const entry = frequency.get(key);
      if (!entry.pages.includes(pageIndex)) {
        entry.count++;
        entry.pages.push(pageIndex);
      }
    });
  });
  
  return frequency;
}
```

#### 3. 内容分类

```javascript
classifyContent(frequency, totalPages, thresholds) {
  const result = {
    template: [],  // 高频 >80%: 模板噪音
    unique: [],    // 低频 <20%: 独特数据
    mixed: []      // 中频 20-80%: 需进一步分析
  };
  
  frequency.forEach((entry, key) => {
    const ratio = entry.count / totalPages;
    
    if (ratio > thresholds.template) {
      result.template.push({ ...entry, ratio });
    } else if (ratio < thresholds.unique) {
      result.unique.push({ ...entry, ratio });
    } else {
      result.mixed.push({ ...entry, ratio });
    }
  });
  
  return result;
}
```

**分类规则:**
- **模板内容** (ratio > 0.8): 高频出现的内容，通常是导航、页眉、页脚等噪音
- **独特内容** (ratio < 0.2): 低频出现的内容，通常是页面特有的数据
- **混合内容** (0.2 ≤ ratio ≤ 0.8): 中频内容，需要进一步分析

#### 4. 数据结构识别

```javascript
identifyDataStructures(pages) {
  return {
    tables: analyzeTableStructures(pages),
    codeBlocks: analyzeCodeBlocks(pages),
    lists: analyzeLists(pages)
  };
}

analyzeTableStructures(pages) {
  // 识别表格列名、列数、数据类型
  return [
    {
      columns: ['参数名称', '必选', '类型', '说明'],
      rowCount: 5,
      frequency: 0.95
    }
  ];
}
```

#### 5. 配置生成

```javascript
generateConfig(urlPattern, analysisResult) {
  return {
    name: urlPattern.name,
    description: `Parser configuration for ${urlPattern.pathTemplate}`,
    priority: 100,
    
    urlPattern: {
      pattern: urlPattern.pattern,
      pathTemplate: urlPattern.pathTemplate,
      queryParams: urlPattern.queryParams
    },
    
    extractors: generateExtractors(analysisResult),
    filters: generateFilters(analysisResult),
    
    metadata: {
      generatedAt: new Date().toISOString(),
      pageCount: analysisResult.stats.totalPages,
      version: '1.0.0'
    }
  };
}
```

### 数据流

```
url-patterns.json + pages/*.md
    ↓
对每个 pathTemplate:
    ↓
ContentAnalyzer.extractContentBlocks()
    ↓
ContentAnalyzer.calculateFrequency()
    ↓
ContentAnalyzer.classifyContent()
    ↓
ContentAnalyzer.identifyDataStructures()
    ↓
TemplateConfigGenerator.generateExtractors()
    ↓
TemplateConfigGenerator.generateFilters()
    ↓
TemplateConfigGenerator.generateConfig()
    ↓
TemplateConfigGenerator.saveAsJSONL()
    ↓
template-rules.jsonl
```

### 输入输出

**输入:** `url-patterns.json` + `pages/*.md`

**输出:** `template-rules.jsonl`
```jsonl
{"name":"api-doc","description":"Parser configuration for /open/api/doc","priority":100,"urlPattern":{"pattern":"^https://www\\.lixinger\\.com/open/api/doc\\?api-key=(.+)$","pathTemplate":"/open/api/doc","queryParams":["api-key"]},"extractors":[{"field":"title","type":"text","selector":"h1, h2, title","required":true},{"field":"parameters","type":"table","selector":"table","columns":["参数名称","必选","类型","说明"]}],"filters":[{"type":"remove","target":"heading","pattern":"API文档","reason":"Template noise (100% frequency)"}],"metadata":{"generatedAt":"2026-02-25T10:00:00.000Z","pageCount":163,"version":"1.0.0"}}
```

## 算法库详解

### url-pattern-analyzer 算法库

#### LinksReader

**职责:** 读取和解析 `links.txt` 文件

**核心方法:**
- `readLinksFile(filePath)`: 读取 JSON 格式的 links 文件
- `extractURLs(records, options)`: 提取 URL 列表（支持过滤）
- `getStatistics(records)`: 获取统计信息

**特点:**
- 容错处理：跳过格式错误的行
- 灵活过滤：按状态、错误等条件过滤
- 统计分析：提供详细的统计信息

#### URLClusterer

**职责:** URL 聚类和模式识别

**核心方法:**
- `extractFeatures(url)`: 提取 URL 特征
- `calculateSimilarity(url1, url2)`: 计算相似度
- `clusterURLs(urls)`: URL 聚类
- `generatePattern(urlGroup)`: 生成正则表达式

**特点:**
- 层次聚类算法
- 动态阈值（不使用固定值）
- 基于 URL 正则匹配和后端渲染判断

#### ReportGenerator

**职责:** 生成分析报告

**核心方法:**
- `generateJSON(clusters)`: 生成 JSON 报告
- `generateMarkdown(clusters)`: 生成 Markdown 报告

### template-content-analyzer 算法库

#### ContentAnalyzer

**职责:** 内容分析和提取

**核心方法:**
- `extractContentBlocks(markdown)`: 提取内容块
- `normalizeText(text)`: 文本标准化
- `calculateFrequency(pages)`: 计算频率
- `classifyContent(frequency, totalPages, thresholds)`: 内容分类
- `analyzeTemplate(pages, options)`: 完整分析流程

**特点:**
- 精确的 markdown 解析
- 智能的文本标准化
- 基于频率的自动分类

#### TemplateConfigGenerator

**职责:** 生成模板配置

**核心方法:**
- `generateConfig(urlPattern, analysisResult)`: 生成配置对象
- `generateExtractors(dataStructures, classified)`: 生成提取器
- `generateFilters(cleaningRules, classified)`: 生成过滤器
- `saveAsJSONL(configs, outputPath)`: 保存为 JSONL

**特点:**
- 基于分析结果自动生成配置
- 支持多种提取器类型（text, table, code, list）
- 支持多种过滤器类型（remove, keep, transform）

#### TemplateParser

**职责:** 配置驱动的模板解析

**核心方法:**
- `matches(url)`: URL 匹配
- `parse(page, url, options)`: 解析页面
- `executeExtractor(page, extractor)`: 执行提取器
- `applyFilters(result)`: 应用过滤器

**特点:**
- 完全配置驱动
- 支持所有提取器和过滤器类型
- 易于测试和调试

#### ConfigLoader

**职责:** 配置加载和管理

**核心方法:**
- `loadConfigs(jsonlPath)`: 加载配置
- `loadConfigByName(jsonlPath, name)`: 按名称加载
- `createParsers(jsonlPath, ParserClass)`: 创建 Parser 实例
- `getConfigStats(jsonlPath)`: 获取统计信息

**特点:**
- 支持 JSONL 格式
- 配置验证
- 统计分析

## 执行流程

### 完整工作流

```bash
# 1. 执行 Skill 1: URL 模式分析
node skills/url-pattern-analyzer/main.js \
  --links-file stock-crawler/output/lixinger-crawler/links.txt \
  --output-file stock-crawler/output/lixinger-crawler/url-patterns.json

# 2. 执行 Skill 2: 模板内容分析
node skills/template-content-analyzer/main.js \
  --url-patterns stock-crawler/output/lixinger-crawler/url-patterns.json \
  --pages-dir stock-crawler/output/lixinger-crawler/pages \
  --output-file stock-crawler/output/lixinger-crawler/template-rules.jsonl

# 3. 测试生成的配置
node skills/template-content-analyzer/scripts/test-real-pages.js
```

### 测试流程

```bash
# 测试 Skill 1
cd skills/url-pattern-analyzer
npm test

# 测试 Skill 2
cd skills/template-content-analyzer
npm test

# 完整工作流测试
node skills/test-complete-workflow.js
```

## 性能指标

### Skill 1: URL Pattern Analyzer

- **处理速度**: 8403 个 URL < 10 秒
- **内存使用**: < 100 MB
- **准确率**: > 90%

### Skill 2: Template Content Analyzer

- **处理速度**: 163 个页面 < 30 秒
- **内存使用**: < 200 MB
- **准确率**: > 85%

### 配置生成

- **生成速度**: < 1 秒
- **配置加载**: < 100 ms

## 设计原则

### 1. 模块化

- 每个 Skill 独立运行
- 算法库可单独使用
- 清晰的职责划分

### 2. 配置驱动

- 生成配置文件而非代码
- 易于修改和调试
- 支持大模型优化

### 3. 可扩展性

- 支持添加新的提取器类型
- 支持添加新的过滤器类型
- 支持自定义分析策略

### 4. 错误容忍

- 格式错误的数据会被跳过
- 详细的错误日志
- 优雅的降级处理

### 5. 性能优化

- 批量处理
- 缓存机制
- 并行处理

## 判断依据

### URL 分组判断

- **URL 正则匹配**: 路径结构相似
- **后端渲染判断**: 页面是否由同一模板渲染
- **不使用固定阈值**: 动态决定分组

### 内容分类判断

- **频率分析**: 基于出现频率分类
- **数据结构识别**: 识别表格、代码块、列表
- **模板抽取结果**: 结合实际抽取效果

## 优势

1. **自动化**: 从 URL 分析到配置生成全自动
2. **准确性**: 基于统计分析，准确率高
3. **灵活性**: 支持自定义阈值和规则
4. **可维护性**: 配置驱动，易于修改
5. **可扩展性**: 易于添加新功能
6. **性能**: 处理大量数据速度快

## 局限性

1. **依赖数据质量**: 需要足够的样本数据
2. **阈值调整**: 可能需要根据实际情况调整阈值
3. **复杂页面**: 对于非常复杂的页面可能需要手动调整
4. **动态内容**: 对于 JavaScript 渲染的动态内容支持有限

## 未来改进

1. **机器学习**: 使用 ML 算法提高准确率
2. **增量分析**: 支持增量更新
3. **可视化**: 提供可视化的分析报告
4. **自动优化**: 根据使用情况自动优化配置
5. **多网站支持**: 支持多个网站的配置管理

## 相关文档

- [安装指南](./INSTALLATION_GUIDE.md)
- [URL Pattern Analyzer README](./url-pattern-analyzer/README.md)
- [Template Content Analyzer README](./template-content-analyzer/README.md)
- [配置格式说明](./template-content-analyzer/docs/CONFIG_FORMAT.md)
- [提取器配置指南](./template-content-analyzer/docs/EXTRACTOR_GUIDE.md)
- [过滤器配置指南](./template-content-analyzer/docs/FILTER_GUIDE.md)
- [使用指南](./template-content-analyzer/docs/USAGE_GUIDE.md)

## 总结

Template Analyzer 系统通过 2 个独立的 Skills 实现了从 URL 分析到配置生成的完整流程。系统采用配置驱动的设计，易于维护和扩展，性能优秀，准确率高。通过合理的算法设计和模块化架构，系统能够处理大量数据并生成高质量的解析配置。
