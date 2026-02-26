# 扩展指南 - Template Content Analyzer

本文档介绍如何扩展 Template Content Analyzer 系统，添加新的功能和自定义分析算法。

## 目录

- [添加新的提取器类型](#添加新的提取器类型)
- [添加新的过滤器类型](#添加新的过滤器类型)
- [自定义分析算法](#自定义分析算法)
- [添加新的输出格式](#添加新的输出格式)
- [扩展内容块识别](#扩展内容块识别)
- [自定义配置验证](#自定义配置验证)

---

## 添加新的提取器类型

提取器用于从页面中提取特定类型的数据。系统目前支持 4 种提取器类型：`text`、`table`、`code`、`list`。

### 步骤 1: 定义提取器类型

在 `lib/template-parser.js` 中添加新的提取器类型处理：

```javascript
// lib/template-parser.js

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
      
      // 添加新的提取器类型
      case 'image':
        return await this.extractImage(page, extractor);
      
      default:
        console.warn(`Unknown extractor type: ${extractor.type}`);
        return null;
    }
  }

  // 实现新的提取方法
  async extractImage(page, extractor) {
    try {
      const elements = await page.$$(extractor.selector);
      const images = [];
      
      for (const element of elements) {
        const src = await element.getAttribute('src');
        const alt = await element.getAttribute('alt');
        
        if (src) {
          images.push({
            src,
            alt: alt || '',
            url: new URL(src, page.url()).href
          });
        }
      }
      
      return images;
    } catch (error) {
      console.error(`Failed to extract images:`, error.message);
      return [];
    }
  }
}
```

### 步骤 2: 更新配置生成器

在 `lib/template-config-generator.js` 中添加生成新提取器的逻辑：

```javascript
// lib/template-config-generator.js

class TemplateConfigGenerator {
  generateExtractors(dataStructures, classified) {
    const extractors = [];
    
    // 现有提取器...
    
    // 添加图片提取器
    if (dataStructures.images && dataStructures.images.length > 0) {
      extractors.push({
        field: 'images',
        type: 'image',
        selector: 'img',
        required: false
      });
    }
    
    return extractors;
  }
}
```


### 步骤 3: 添加数据结构识别

在 `lib/content-analyzer.js` 中添加识别新数据结构的方法：

```javascript
// lib/content-analyzer.js

class ContentAnalyzer {
  identifyDataStructures(pages) {
    return {
      tables: this.analyzeTableStructures(pages),
      codeBlocks: this.analyzeCodeBlocks(pages),
      lists: this.analyzeLists(pages),
      images: this.analyzeImages(pages)  // 新增
    };
  }
  
  analyzeImages(pages) {
    const imagePatterns = [];
    
    pages.forEach(page => {
      // 从 markdown 中提取图片信息
      const imageRegex = /!\[([^\]]*)\]\(([^)]+)\)/g;
      let match;
      
      while ((match = imageRegex.exec(page)) !== null) {
        imagePatterns.push({
          alt: match[1],
          src: match[2]
        });
      }
    });
    
    return imagePatterns;
  }
}
```

### 步骤 4: 编写测试

创建测试文件 `test/image-extractor.test.js`：

```javascript
const TemplateParser = require('../lib/template-parser');
const { chromium } = require('playwright');

describe('Image Extractor', () => {
  let browser, page;
  
  beforeAll(async () => {
    browser = await chromium.launch();
    page = await browser.newPage();
  });
  
  afterAll(async () => {
    await browser.close();
  });
  
  test('should extract images correctly', async () => {
    const config = {
      name: 'test',
      extractors: [
        {
          field: 'images',
          type: 'image',
          selector: 'img'
        }
      ]
    };
    
    const parser = new TemplateParser(config);
    
    await page.setContent(`
      <html>
        <body>
          <img src="/image1.jpg" alt="Image 1">
          <img src="/image2.jpg" alt="Image 2">
        </body>
      </html>
    `);
    
    const result = await parser.parse(page, 'http://example.com');
    
    expect(result.images).toHaveLength(2);
    expect(result.images[0].alt).toBe('Image 1');
  });
});
```

### 完整示例：添加视频提取器

```javascript
// 1. 在 TemplateParser 中添加
async extractVideo(page, extractor) {
  const elements = await page.$$(extractor.selector);
  const videos = [];
  
  for (const element of elements) {
    const src = await element.getAttribute('src');
    const poster = await element.getAttribute('poster');
    
    videos.push({
      src: src || '',
      poster: poster || '',
      url: src ? new URL(src, page.url()).href : ''
    });
  }
  
  return videos;
}

// 2. 在配置中使用
{
  "field": "videos",
  "type": "video",
  "selector": "video",
  "required": false
}
```

---

## 添加新的过滤器类型

过滤器用于清理和转换提取的数据。系统目前支持 3 种过滤器类型：`remove`、`keep`、`transform`。

### 步骤 1: 定义过滤器类型

在 `lib/template-parser.js` 中添加新的过滤器处理：

```javascript
// lib/template-parser.js

class TemplateParser {
  applyFilters(result) {
    if (!this.config.filters || this.config.filters.length === 0) {
      return result;
    }
    
    this.config.filters.forEach(filter => {
      switch (filter.type) {
        case 'remove':
          result = this.applyRemoveFilter(result, filter);
          break;
        case 'keep':
          result = this.applyKeepFilter(result, filter);
          break;
        case 'transform':
          result = this.applyTransformFilter(result, filter);
          break;
        
        // 添加新的过滤器类型
        case 'validate':
          result = this.applyValidateFilter(result, filter);
          break;
        
        default:
          console.warn(`Unknown filter type: ${filter.type}`);
      }
    });
    
    return result;
  }
  
  applyValidateFilter(result, filter) {
    // 验证字段是否符合规则
    const field = filter.target;
    const pattern = new RegExp(filter.pattern);
    
    if (result[field] && !pattern.test(result[field])) {
      console.warn(`Validation failed for ${field}: ${result[field]}`);
      result[`${field}_valid`] = false;
    } else {
      result[`${field}_valid`] = true;
    }
    
    return result;
  }
}
```


### 步骤 2: 在配置中使用

```json
{
  "type": "validate",
  "target": "email",
  "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$",
  "reason": "Validate email format"
}
```

### 完整示例：添加格式化过滤器

```javascript
// 格式化过滤器：统一日期格式
applyFormatFilter(result, filter) {
  const field = filter.target;
  const format = filter.format;
  
  if (result[field]) {
    if (format === 'date') {
      // 将各种日期格式统一为 ISO 格式
      const date = new Date(result[field]);
      if (!isNaN(date.getTime())) {
        result[field] = date.toISOString().split('T')[0];
      }
    } else if (format === 'number') {
      // 移除数字中的逗号和空格
      result[field] = result[field].replace(/[,\s]/g, '');
    }
  }
  
  return result;
}

// 配置示例
{
  "type": "format",
  "target": "publishDate",
  "format": "date",
  "reason": "Normalize date format"
}
```

---

## 自定义分析算法

### 修改频率阈值算法

默认的频率阈值是固定的（模板 > 0.8，独特 < 0.2），你可以实现动态阈值算法：

```javascript
// lib/content-analyzer.js

class ContentAnalyzer {
  // 动态计算阈值
  calculateDynamicThresholds(frequency, totalPages) {
    const ratios = Array.from(frequency.values())
      .map(entry => entry.count / totalPages)
      .sort((a, b) => a - b);
    
    // 使用四分位数
    const q1 = ratios[Math.floor(ratios.length * 0.25)];
    const q3 = ratios[Math.floor(ratios.length * 0.75)];
    
    return {
      template: q3,  // 第三四分位数作为模板阈值
      unique: q1     // 第一四分位数作为独特阈值
    };
  }
  
  classifyContent(frequency, totalPages, thresholds) {
    // 如果没有提供阈值，使用动态计算
    if (!thresholds) {
      thresholds = this.calculateDynamicThresholds(frequency, totalPages);
    }
    
    // 原有的分类逻辑...
  }
}
```

### 添加相似度计算

实现更智能的内容相似度判断：

```javascript
// lib/content-analyzer.js

class ContentAnalyzer {
  // 计算两个文本的相似度（Levenshtein 距离）
  calculateSimilarity(text1, text2) {
    const len1 = text1.length;
    const len2 = text2.length;
    const matrix = [];
    
    for (let i = 0; i <= len1; i++) {
      matrix[i] = [i];
    }
    
    for (let j = 0; j <= len2; j++) {
      matrix[0][j] = j;
    }
    
    for (let i = 1; i <= len1; i++) {
      for (let j = 1; j <= len2; j++) {
        if (text1[i - 1] === text2[j - 1]) {
          matrix[i][j] = matrix[i - 1][j - 1];
        } else {
          matrix[i][j] = Math.min(
            matrix[i - 1][j - 1] + 1,
            matrix[i][j - 1] + 1,
            matrix[i - 1][j] + 1
          );
        }
      }
    }
    
    const distance = matrix[len1][len2];
    const maxLen = Math.max(len1, len2);
    return 1 - distance / maxLen;
  }
  
  // 使用相似度进行模糊匹配
  calculateFrequencyWithSimilarity(pages, similarityThreshold = 0.9) {
    const blockFrequency = new Map();
    
    pages.forEach((page, pageIndex) => {
      const blocks = this.extractContentBlocks(page);
      
      blocks.forEach(block => {
        const normalized = this.normalizeText(block.content);
        let matched = false;
        
        // 查找相似的已有块
        for (const [key, entry] of blockFrequency.entries()) {
          const similarity = this.calculateSimilarity(
            normalized,
            entry.normalizedContent
          );
          
          if (similarity >= similarityThreshold) {
            // 找到相似块，增加计数
            if (!entry.pages.includes(pageIndex)) {
              entry.count++;
              entry.pages.push(pageIndex);
            }
            matched = true;
            break;
          }
        }
        
        // 没有找到相似块，创建新条目
        if (!matched) {
          const key = `${block.type}:${normalized}`;
          blockFrequency.set(key, {
            type: block.type,
            content: block.content,
            normalizedContent: normalized,
            count: 1,
            pages: [pageIndex]
          });
        }
      });
    });
    
    return blockFrequency;
  }
}
```

### 添加机器学习分类

使用简单的朴素贝叶斯分类器：

```javascript
// lib/ml-classifier.js

class MLClassifier {
  constructor() {
    this.vocabulary = new Set();
    this.templateProb = new Map();
    this.dataProb = new Map();
  }
  
  // 训练分类器
  train(templateSamples, dataSamples) {
    // 构建词汇表
    [...templateSamples, ...dataSamples].forEach(text => {
      const words = this.tokenize(text);
      words.forEach(word => this.vocabulary.add(word));
    });
    
    // 计算模板内容的词频
    templateSamples.forEach(text => {
      const words = this.tokenize(text);
      words.forEach(word => {
        this.templateProb.set(word, (this.templateProb.get(word) || 0) + 1);
      });
    });
    
    // 计算数据内容的词频
    dataSamples.forEach(text => {
      const words = this.tokenize(text);
      words.forEach(word => {
        this.dataProb.set(word, (this.dataProb.get(word) || 0) + 1);
      });
    });
  }
  
  // 分类新文本
  classify(text) {
    const words = this.tokenize(text);
    let templateScore = 0;
    let dataScore = 0;
    
    words.forEach(word => {
      templateScore += Math.log((this.templateProb.get(word) || 1) / this.vocabulary.size);
      dataScore += Math.log((this.dataProb.get(word) || 1) / this.vocabulary.size);
    });
    
    return templateScore > dataScore ? 'template' : 'data';
  }
  
  tokenize(text) {
    return text.toLowerCase().split(/\s+/).filter(w => w.length > 0);
  }
}

// 使用示例
const classifier = new MLClassifier();
classifier.train(
  ['导航', '页眉', '页脚', '版权'],  // 模板样本
  ['用户名', '订单号', '金额', '日期']  // 数据样本
);

const result = classifier.classify('用户信息');
console.log(result); // 'data'
```

---

## 添加新的输出格式

### 添加 CSV 输出

```javascript
// lib/template-config-generator.js

class TemplateConfigGenerator {
  saveAsCSV(configs, outputPath) {
    const rows = [];
    
    // CSV 头部
    rows.push([
      'Name',
      'Description',
      'Priority',
      'Pattern',
      'Extractors',
      'Filters',
      'Page Count'
    ].join(','));
    
    // 数据行
    configs.forEach(config => {
      rows.push([
        config.name,
        `"${config.description}"`,
        config.priority,
        `"${config.urlPattern.pattern}"`,
        config.extractors.length,
        config.filters.length,
        config.metadata.pageCount
      ].join(','));
    });
    
    fs.writeFileSync(outputPath, rows.join('\n'), 'utf-8');
  }
}
```
