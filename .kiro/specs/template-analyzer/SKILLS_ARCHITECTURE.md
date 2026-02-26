# Skills架构说明

## 目录结构

```
项目根目录/
├── skills/                                    # Skills目录（2个skills）
│   ├── url-pattern-analyzer/                  # Skill 1
│   │   ├── README.md                          # 使用说明
│   │   ├── skill.json                         # Skill配置
│   │   ├── main.js                            # 入口（大模型调用）
│   │   ├── lib/                               # 算法库
│   │   │   ├── url-clusterer.js               # URL聚类
│   │   │   ├── similarity.js                  # 相似度计算
│   │   │   └── pattern-gen.js                 # 正则生成
│   │   └── test/
│   │       └── test-analyzer.js               # 测试脚本
│   │
│   └── template-content-analyzer/             # Skill 2
│       ├── README.md                          # 使用说明
│       ├── skill.json                         # Skill配置
│       ├── main.js                            # 入口（大模型调用）
│       ├── lib/                               # 算法库
│       │   ├── content-analyzer.js            # 内容分析
│       │   ├── frequency-calc.js              # 频率计算
│       │   ├── structure-detector.js          # 结构识别
│       │   └── config-generator.js            # 配置生成
│       └── test/
│           └── test-analyzer.js               # 测试脚本
│
└── stock-crawler/
    └── output/
        └── lixinger-crawler/
            ├── links.txt                      # 输入
            ├── pages/                         # 输入
            ├── url-patterns.json              # Skill 1输出
            └── template-rules.jsonl           # Skill 2输出
```

## Skill 1: url-pattern-analyzer

### 职责
从links.txt中识别URL模式，按pathTemplate分组

### 输入
```json
{
  "linksFile": "stock-crawler/output/lixinger-crawler/links.txt",
  "outputFile": "stock-crawler/output/lixinger-crawler/url-patterns.json",
  "minGroupSize": 5
}
```

### 处理流程
1. 读取links.txt（8403个URL）
2. 提取URL特征（协议、域名、路径、参数）
3. 计算URL之间的相似度
4. 使用聚类算法分组
5. 为每组生成pathTemplate和正则表达式
6. 输出url-patterns.json

### 输出
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
    },
    {
      "name": "dashboard",
      "pathTemplate": "/analytics/*/dashboard",
      "pattern": "^https://www\\.lixinger\\.com/analytics/[^/]+/dashboard$",
      "queryParams": [],
      "urlCount": 45,
      "samples": [...]
    }
  ]
}
```

### 算法库

#### url-clusterer.js
```javascript
/**
 * URL聚类算法
 * 基于URL正则匹配和后端渲染判断
 */
class URLClusterer {
  cluster(urls) {
    // 1. 初始化：每个URL一个簇
    // 2. 迭代：合并相似的簇
    // 3. 判断依据：URL正则匹配、页面是否同一个后端渲染
  }
}
```

#### similarity.js
```javascript
/**
 * URL相似度计算
 * 基于路径结构和参数
 * 不使用固定阈值，而是通过URL正则匹配和后端渲染判断
 */
class SimilarityCalculator {
  calculate(url1, url2) {
    // 路径深度相同 +20分
    // 路径段匹配 +10分/段
    // 查询参数匹配 +5分/参数
    // 返回相似度分数，由聚类算法决定分组
  }
}
```

#### pattern-gen.js
```javascript
/**
 * 正则表达式生成
 * 从URL组中提取模式
 */
class PatternGenerator {
  generate(urlGroup) {
    // 找出变化的部分（参数）
    // 固定的部分保持不变
    // 生成正则表达式
  }
}
```

## Skill 2: template-content-analyzer

### 职责
分析每个pathTemplate对应的页面，生成解析配置

### 输入
```json
{
  "urlPatternsFile": "stock-crawler/output/lixinger-crawler/url-patterns.json",
  "pagesDir": "stock-crawler/output/lixinger-crawler/pages",
  "outputFile": "stock-crawler/output/lixinger-crawler/template-rules.jsonl",
  "sampleUrls": [
    "https://www.lixinger.com/open/api/doc?api-key=cn/company"
  ],
  "frequencyThresholds": {
    "template": 0.8,
    "unique": 0.2
  }
}
```

### 处理流程
1. 读取url-patterns.json
2. 对每个pathTemplate：
   - 收集该模板的所有markdown文件
   - 提取内容块（标题、段落、表格、代码）
   - 计算每个块的出现频率
   - 分类内容：
     - 高频(>80%): 模板噪音 → 生成filters
     - 低频(<20%): 独特数据 → 需要提取
     - 中频(20-80%): 进一步分析
   - 识别数据结构（表格列名、代码块类型）
   - 生成extractors配置
   - 生成filters配置
   - 生成完整的TemplateConfig对象
3. 收集所有TemplateConfig
4. 保存为JSONL格式（每行一个JSON对象）

### 判断依据
- 根据模板抽取结果判断
- URL正则匹配
- 页面是否同一个后端渲染
- 不使用相似度阈值

### 输出
```jsonl
{"name":"api-doc","description":"Parser configuration for /open/api/doc","priority":100,"urlPattern":{"pattern":"/\\/api\\/doc/","pathTemplate":"/open/api/doc","queryParams":["api-key"]},"extractors":[{"field":"title","type":"text","selector":"h1, h2, title","required":true},{"field":"parameters","type":"table","selector":"table","columns":["参数名称","必选","类型","说明"]}],"filters":[{"type":"remove","target":"heading","pattern":"API文档","reason":"Template noise (100% frequency)"}],"metadata":{"generatedAt":"2026-02-25T10:00:00.000Z","pageCount":163,"version":"1.0.0"}}
{"name":"dashboard","description":"Parser configuration for /analytics/*/dashboard","priority":100,"urlPattern":{...},"extractors":[...],"filters":[...],"metadata":{...}}
```

### 算法库

#### content-analyzer.js
```javascript
/**
 * 内容分析器
 * 提取和分析markdown内容块
 */
class ContentAnalyzer {
  extractContentBlocks(markdown) {
    // 提取标题、段落、表格、代码块、列表
  }
  
  normalizeText(text) {
    // 标准化文本用于比较
  }
}
```

#### frequency-calc.js
```javascript
/**
 * 频率计算器
 * 统计内容块出现频率
 */
class FrequencyCalculator {
  calculate(pages) {
    // 统计每个内容块在多少页面中出现
    // 返回频率Map
  }
  
  classify(frequency, totalPages, thresholds) {
    // 根据阈值分类：template/unique/mixed
  }
}
```

#### structure-detector.js
```javascript
/**
 * 数据结构识别器
 * 识别表格、代码块、列表的结构
 */
class StructureDetector {
  detectTableStructure(pages) {
    // 识别表格列名、列数
  }
  
  detectCodeBlockStructure(pages) {
    // 识别代码块语言、格式
  }
}
```

#### config-generator.js
```javascript
/**
 * 配置生成器
 * 生成TemplateConfig对象
 */
class ConfigGenerator {
  generate(analysis) {
    return {
      name: analysis.templateName,
      description: `Parser configuration for ${analysis.pathTemplate}`,
      priority: 100,
      urlPattern: {...},
      extractors: this.generateExtractors(analysis),
      filters: this.generateFilters(analysis),
      metadata: {...}
    };
  }
  
  generateExtractors(analysis) {
    // 基于数据结构生成提取器配置
  }
  
  generateFilters(analysis) {
    // 基于高频内容生成过滤器配置
  }
}
```

## Test Script: Template Parser (已移除)

原设计中的独立测试脚本已移除，现在只有2个skills：
1. url-pattern-analyzer
2. template-content-analyzer

测试功能已整合到各个skill的test目录中。

## 执行流程

### 1. 安装Skills
```bash
# Skills已经在项目根目录的skills/文件夹中
ls skills/
# url-pattern-analyzer/
# template-content-analyzer/
```

### 2. 执行Skill 1
```bash
# 大模型调用
node skills/url-pattern-analyzer/main.js \
  --links-file stock-crawler/output/lixinger-crawler/links.txt \
  --output-file stock-crawler/output/lixinger-crawler/url-patterns.json
```

### 3. 执行Skill 2
```bash
# 大模型调用
node skills/template-content-analyzer/main.js \
  --url-patterns stock-crawler/output/lixinger-crawler/url-patterns.json \
  --pages-dir stock-crawler/output/lixinger-crawler/pages \
  --output-file stock-crawler/output/lixinger-crawler/template-rules.jsonl
```

### 4. 测试配置
```bash
# 运行各skill的测试脚本
node skills/url-pattern-analyzer/test/test-analyzer.js
node skills/template-content-analyzer/test/test-analyzer.js
```

### 5. 验证效果
查看测试报告，确认配置生成效果

### 6. 后续集成（可选）
如果测试通过，可以考虑将生成的配置集成到爬虫系统中

## 优势

1. **模块化**: 2个Skills独立，易于维护和扩展
2. **AI驱动**: 由大模型执行，可以调用算法库
3. **配置驱动**: 生成配置文件而非代码，更安全
4. **易于测试**: 测试功能集成在各skill中
5. **灵活部署**: 先测试验证，再考虑集成
6. **简洁架构**: 只有2个核心skills，职责清晰

## 下一步

1. 实施M1: 基础分析功能（URL聚类、内容分析）
2. 实施M2: 配置生成功能（提取器、过滤器）
3. 实施M3: Skills封装（打包、测试、文档）
4. 整体测试验证
5. 根据测试结果决定是否集成到爬虫系统
