# 扩展指南

本文档说明如何扩展 Template Content Analyzer 系统。

## 添加新的提取器类型

### 步骤 1: 在 TemplateParser 中添加提取方法

编辑 `lib/template-parser.js`:

```javascript
async executeExtractor(page, extractor) {
  switch (extractor.type) {
    case 'text':
      return await this.extractText(page, extractor);
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
```

### 步骤 2: 在配置生成器中添加生成逻辑

编辑 `lib/template-config-generator.js`:

```javascript
generateExtractors(analysisResult) {
  const extractors = [];
  
  if (analysisResult.stats.imageCount > 0) {
    extractors.push({
      field: 'images',
      type: 'image',
      selector: 'img',
      required: false
    });
  }
  
  return extractors;
}
```

## 添加新的过滤器类型

在 `TemplateParser` 中实现过滤方法:

```javascript
applyFilters(data) {
  for (const filter of this.config.filters) {
    if (filter.type === 'replace') {
      data = this.replaceFilter(data, filter);
    }
  }
  return data;
}

replaceFilter(data, filter) {
  const pattern = new RegExp(filter.pattern, 'g');
  Object.keys(data).forEach(key => {
    if (typeof data[key] === 'string') {
      data[key] = data[key].replace(pattern, filter.replacement);
    }
  });
  return data;
}
```

## 自定义分析算法

编辑 `lib/content-analyzer.js`:

```javascript
calculateFrequencyCustom(pages, algorithm = 'tfidf') {
  if (algorithm === 'tfidf') {
    return this.calculateTFIDF(pages);
  }
  return this.calculateFrequency(pages);
}
```

## 添加新的输出格式

创建 `lib/yaml-generator.js`:

```javascript
const yaml = require('js-yaml');

class YAMLGenerator {
  async saveAsYAML(configs, outputPath) {
    const yamlContent = yaml.dump(configs);
    await fs.writeFile(outputPath, yamlContent, 'utf-8');
  }
}
```

## 最佳实践

1. 保持向后兼容
2. 添加验证逻辑
3. 编写完整测试
4. 更新相关文档

详见 [API 文档](./API.md) 和 [配置格式](./CONFIG_FORMAT.md)。
