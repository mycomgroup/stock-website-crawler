# 解析器架构文档

## 概述

爬虫使用可扩展的解析器架构，支持针对不同类型页面使用不同的解析策略。

## 架构设计

```
PageParser (入口)
    └── ParserManager (解析器管理器)
            ├── ApiDocParser (API文档解析器) - 优先级: 100
            ├── GenericParser (通用解析器) - 优先级: 0
            └── [自定义解析器] - 优先级: 自定义
```

## 核心组件

### 1. BaseParser (基类)

所有解析器的基类，定义了通用接口和共享方法。

**必须实现的方法：**
- `matches(url)` - 判断是否匹配该URL
- `parse(page, url)` - 解析页面内容
- `getPriority()` - 返回优先级（数字越大优先级越高）

**共享方法：**
- `extractTitle(page)` - 提取标题
- `extractTables(page)` - 提取表格
- `extractCodeBlocks(page)` - 提取代码块

### 2. ApiDocParser (API文档解析器)

**匹配规则：** URL包含 `/api/doc`

**优先级：** 100

**提取内容：**
- 简要描述
- 请求URL
- 请求方式
- 参数表格
- API示例（通过点击按钮）
- 返回数据说明

**输出格式：**
```javascript
{
  type: 'api-doc',
  url: '...',
  title: '...',
  briefDesc: '...',
  requestUrl: '...',
  requestMethod: '...',
  params: [...],
  apiExamples: [...],
  responseData: {...},
  tables: [...],
  codeBlocks: [...]
}
```

### 3. GenericParser (通用解析器)

**匹配规则：** 匹配所有URL（作为fallback）

**优先级：** 0

**提取内容：**
- 标题和描述
- 页面结构（标题层级）
- Tab页内容（自动点击切换）
- 段落文本
- 列表
- 表格
- 代码块
- 图片

**输出格式：**
```javascript
{
  type: 'generic',
  url: '...',
  title: '...',
  description: '...',
  headings: [...],
  paragraphs: [...],
  lists: [...],
  tables: [...],
  codeBlocks: [...],
  images: [...],
  tabs: [...]
}
```

### 4. ParserManager (解析器管理器)

负责管理所有解析器，根据URL选择合适的解析器。

**工作流程：**
1. 按优先级排序所有已注册的解析器
2. 遍历解析器，调用`matches(url)`
3. 返回第一个匹配的解析器
4. 调用解析器的`parse()`方法

## 添加自定义解析器

### 步骤1：创建解析器类

在`src/parsers/`目录下创建新文件，例如`custom-parser.js`：

```javascript
import BaseParser from './base-parser.js';

class CustomParser extends BaseParser {
  /**
   * 匹配规则 - 使用正则表达式匹配URL
   */
  matches(url) {
    return /your-pattern/.test(url);
  }

  /**
   * 优先级 - 数字越大优先级越高
   */
  getPriority() {
    return 50; // 介于ApiDocParser(100)和GenericParser(0)之间
  }

  /**
   * 解析页面
   */
  async parse(page, url) {
    const title = await this.extractTitle(page);
    
    // 自定义提取逻辑
    const customData = await page.evaluate(() => {
      // 在浏览器上下文中执行
      return {
        // 提取你需要的数据
      };
    });

    return {
      type: 'custom',
      url,
      title,
      ...customData
    };
  }
}

export default CustomParser;
```

### 步骤2：注册解析器

在`src/parsers/parser-manager.js`中注册：

```javascript
import CustomParser from './custom-parser.js';

class ParserManager {
  registerDefaultParsers() {
    this.register(new ApiDocParser());
    this.register(new CustomParser());  // 添加这行
    this.register(new GenericParser());
  }
}
```

### 步骤3：更新Markdown生成器

在`src/markdown-generator.js`中添加生成方法：

```javascript
generate(pageData) {
  if (pageData.type === 'api-doc') {
    return this.generateApiDoc(pageData);
  } else if (pageData.type === 'custom') {
    return this.generateCustom(pageData);  // 添加这行
  } else if (pageData.type === 'generic') {
    return this.generateGeneric(pageData);
  }
}

generateCustom(pageData) {
  // 自定义Markdown生成逻辑
  const sections = [];
  // ...
  return sections.join('\n');
}
```

## 示例：创建特定网站解析器

假设要为`lixinger.com/analytics`页面创建专用解析器：

```javascript
// src/parsers/lixinger-analytics-parser.js
import BaseParser from './base-parser.js';

class LixingerAnalyticsParser extends BaseParser {
  matches(url) {
    return /lixinger\.com\/analytics/.test(url);
  }

  getPriority() {
    return 80; // 高于通用解析器，低于API文档解析器
  }

  async parse(page, url) {
    const title = await this.extractTitle(page);
    
    // 等待页面加载
    await page.waitForTimeout(2000);
    
    // 提取数据表格
    const dataTable = await page.evaluate(() => {
      const table = document.querySelector('.data-table');
      if (!table) return null;
      
      const rows = Array.from(table.querySelectorAll('tr'));
      return rows.map(row => {
        const cells = Array.from(row.querySelectorAll('td, th'));
        return cells.map(cell => cell.textContent.trim());
      });
    });
    
    // 提取图表数据
    const charts = await page.evaluate(() => {
      const chartElements = document.querySelectorAll('.chart');
      return Array.from(chartElements).map(chart => ({
        title: chart.querySelector('.chart-title')?.textContent.trim(),
        type: chart.dataset.chartType
      }));
    });

    return {
      type: 'lixinger-analytics',
      url,
      title,
      dataTable,
      charts
    };
  }
}

export default LixingerAnalyticsParser;
```

## 最佳实践

### 1. 优先级设置

- **100+**: 非常特定的解析器（特定URL模式）
- **50-99**: 中等特定的解析器（特定域名或路径）
- **1-49**: 较通用的解析器
- **0**: 完全通用的fallback解析器

### 2. URL匹配

使用正则表达式进行精确匹配：

```javascript
// 好的做法
matches(url) {
  return /^https:\/\/example\.com\/api\/v\d+\//.test(url);
}

// 避免过于宽泛
matches(url) {
  return url.includes('api'); // 太宽泛
}
```

### 3. 错误处理

始终在`parse()`方法中处理错误：

```javascript
async parse(page, url) {
  try {
    // 解析逻辑
    return { type: 'custom', url, ... };
  } catch (error) {
    console.error('Parse error:', error);
    return { type: 'custom', url, error: error.message };
  }
}
```

### 4. 等待页面加载

对于动态内容，使用适当的等待：

```javascript
// 等待特定元素
await page.waitForSelector('.data-loaded', { timeout: 5000 });

// 等待网络空闲
await page.waitForLoadState('networkidle');

// 固定等待（最后的选择）
await page.waitForTimeout(2000);
```

### 5. Tab页处理

通用解析器已经支持Tab页，但如果需要自定义：

```javascript
// 查找tab按钮
const tabs = await page.locator('[role="tab"]').all();

for (const tab of tabs) {
  await tab.click();
  await page.waitForTimeout(500);
  
  // 提取当前tab内容
  const content = await page.locator('[role="tabpanel"]').textContent();
  // ...
}
```

## 调试

### 查看使用的解析器

解析器管理器会在控制台输出使用的解析器：

```
Using parser: ApiDocParser for https://example.com/api/doc
Using parser: GenericParser for https://example.com/page
```

### 测试解析器

创建测试文件`test/custom-parser.test.js`：

```javascript
import CustomParser from '../src/parsers/custom-parser.js';

describe('CustomParser', () => {
  const parser = new CustomParser();

  test('should match correct URLs', () => {
    expect(parser.matches('https://example.com/custom')).toBe(true);
    expect(parser.matches('https://example.com/other')).toBe(false);
  });

  test('should have correct priority', () => {
    expect(parser.getPriority()).toBe(50);
  });
});
```

## 配置

可以在配置文件中指定使用的解析器（未来功能）：

```json
{
  "parsers": {
    "enabled": ["api-doc", "custom", "generic"],
    "custom": {
      "pattern": "your-pattern",
      "priority": 50
    }
  }
}
```

## 总结

- 解析器架构支持灵活扩展
- 通过优先级控制解析器选择
- API文档和通用页面都有专门的解析器
- 可以轻松添加自定义解析器处理特定网站
