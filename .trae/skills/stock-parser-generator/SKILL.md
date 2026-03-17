---
name: "stock-parser-generator"
description: "Generates a new Playwright-based API parser for the stock crawler. Invoke when the user asks to create or add a new parser for a website."
---

# Stock Parser Generator

This skill helps you generate a new parser for the stock-website-crawler project. Parsers are used to extract API documentation from various financial data websites using Playwright.

## Parser Structure

A new parser should be created in `src/parsers/<name>-api-parser.js`.
It must extend `BaseParser` and return data that conforms to the `UNIFIED_SCHEMA` so that `markdown-generator.js` can automatically generate the markdown without requiring a custom generator method.

### Template

```javascript
import BaseParser from './base-parser.js';

/**
 * [Website Name] API Parser
 */
class NewApiParser extends BaseParser {
  /**
   * 匹配 [Website Name] API 文档页面
   * @param {string} url - 页面URL
   * @returns {boolean} 是否匹配
   */
  matches(url) {
    return /^https?:\/\/(www\.)?example\.com\/docs/.test(url);
  }

  /**
   * 获取优先级 (通常为 100)
   * @returns {number} 优先级
   */
  getPriority() {
    return 100;
  }

  /**
   * 是否支持链接发现 (可选)
   * @returns {boolean}
   */
  supportsLinkDiscovery() {
    return true; // 或 false
  }

  /**
   * 发现页面中的其他文档链接 (可选)
   * @param {Page} page - Playwright页面对象
   * @returns {Promise<string[]>} 发现的URL列表
   */
  async discoverLinks(page) {
    // 使用 page.evaluate 提取同域名下的其他文档链接
    return [];
  }

  /**
   * 解析 API 文档页面
   * @param {Page} page - Playwright页面对象
   * @param {string} url - 页面URL
   * @param {Object} options - 解析选项
   * @returns {Promise<Object>} 解析后的页面数据，需符合 UNIFIED_SCHEMA
   */
  async parse(page, url, options = {}) {
    // 等待核心内容加载
    await page.waitForSelector('main', { timeout: 5000 }).catch(() => {});

    // 提取数据
    const data = await page.evaluate(() => {
      // 在浏览器上下文中提取 DOM 数据
      const title = document.querySelector('h1')?.textContent?.trim() || '';
      const description = document.querySelector('.description')?.textContent?.trim() || '';
      
      const method = document.querySelector('.http-method')?.textContent?.trim() || 'GET';
      const endpoint = document.querySelector('.endpoint')?.textContent?.trim() || '';
      
      // 提取参数
      const parameters = [];
      document.querySelectorAll('.params-table tr').forEach(tr => {
        // ... 提取 name, type, required, description
      });

      // 提取响应字段
      const responseFields = [];
      // ... 提取 name, type, description

      // 提取代码示例
      const codeExamples = [];
      // ... 提取 language, code

      return {
        title,
        description,
        api: { method, endpoint, baseUrl: 'https://api.example.com' },
        parameters,
        responseFields,
        codeExamples,
        rawContent: document.body.innerText
      };
    });

    // 返回符合 UNIFIED_SCHEMA 的数据结构
    return {
      type: 'example-api', // 替换为实际名称
      url,
      ...data
    };
  }
}

export default NewApiParser;
```

## Steps to Generate a New Parser

When the user asks you to write a new parser, follow these steps:

1. **Create the Parser File**: 
   - Create a new file in `src/parsers/` named `<website>-api-parser.js`.
   - Implement the class extending `BaseParser` using the template above.
   - Use `page.evaluate` to extract data according to the target website's DOM structure.
   - **Crucial**: Ensure the `parse` method returns an object matching the `UNIFIED_SCHEMA` (fields: `type`, `url`, `title`, `description`, `api`, `parameters`, `responseFields`, `codeExamples`, `rawContent`). This allows `markdown-generator.js`'s `generateUnified` method to handle it automatically.

2. **Register the Parser**:
   - Open `src/parsers/parser-manager.js`.
   - Import the newly created parser at the top of the file.
   - Add it to the `registerDefaultParsers()` method (e.g., `this.register(new NewApiParser());`).

3. **Verify**:
   - Ensure the `matches(url)` regex correctly matches the target URL.
   - Inform the user that the parser has been created and registered, and is ready for testing.
