/**
 * TemplateParser - 配置驱动的模板解析器
 * 
 * 职责：
 * 1. 基于配置对象进行URL匹配
 * 2. 基于配置对象进行数据提取
 * 3. 执行提取器（text, table, code, list）
 * 4. 应用过滤器（remove, keep, transform）
 * 
 * 继承自BaseParser，实现配置驱动的解析逻辑
 */

/**
 * 简化的BaseParser（用于独立测试）
 * 如果要集成到爬虫系统，应该继承 stock-crawler/src/parsers/base-parser.js
 */
class BaseParser {
  matches(url) {
    throw new Error('matches() must be implemented by subclass');
  }

  async parse(page, url, options = {}) {
    throw new Error('parse() must be implemented by subclass');
  }

  getPriority() {
    return 0;
  }
}

class TemplateParser extends BaseParser {
  /**
   * 构造函数
   * @param {Object} config - 模板配置对象
   * @param {string} config.name - 模板名称
   * @param {Object} config.urlPattern - URL匹配规则
   * @param {Array} config.extractors - 提取器配置
   * @param {Array} config.filters - 过滤器配置
   * @param {number} config.priority - 优先级
   */
  constructor(config) {
    super();
    
    // 验证配置
    if (!config) {
      throw new Error('Config is required');
    }
    if (!config.name) {
      throw new Error('Config.name is required');
    }
    if (!config.urlPattern || !config.urlPattern.pattern) {
      throw new Error('Config.urlPattern.pattern is required');
    }
    if (!config.extractors || !Array.isArray(config.extractors)) {
      throw new Error('Config.extractors must be an array');
    }

    this.config = config;
    this.name = config.name;
    
    // 编译正则表达式
    try {
      // 如果pattern是字符串，转换为RegExp
      if (typeof config.urlPattern.pattern === 'string') {
        // 移除可能的正则表达式标记（如 /pattern/flags）
        const match = config.urlPattern.pattern.match(/^\/(.+)\/([gimuy]*)$/);
        if (match) {
          this.pattern = new RegExp(match[1], match[2]);
        } else {
          this.pattern = new RegExp(config.urlPattern.pattern);
        }
      } else {
        this.pattern = config.urlPattern.pattern;
      }
    } catch (error) {
      throw new Error(`Invalid URL pattern: ${error.message}`);
    }
  }

  /**
   * 检查URL是否匹配此解析器
   * @param {string} url - 页面URL
   * @returns {boolean} 是否匹配
   */
  matches(url) {
    return this.pattern.test(url);
  }

  /**
   * 获取解析器优先级
   * @returns {number} 优先级（数字越大优先级越高）
   */
  getPriority() {
    return this.config.priority || 0;
  }

  /**
   * 解析页面（主入口）
   * @param {Page} page - Playwright页面对象
   * @param {string} url - 页面URL
   * @param {Object} options - 解析选项
   * @returns {Promise<Object>} 解析后的数据
   */
  async parse(page, url, options = {}) {
    try {
      const result = {
        type: this.config.name,
        url,
        timestamp: new Date().toISOString()
      };

      // 执行所有提取器
      for (const extractor of this.config.extractors) {
        try {
          const value = await this.executeExtractor(page, extractor);
          result[extractor.field] = value;
        } catch (error) {
          console.error(`Failed to execute extractor "${extractor.field}":`, error.message);
          result[extractor.field] = null;
          
          // 如果是必需字段，抛出错误
          if (extractor.required) {
            throw new Error(`Required field "${extractor.field}" extraction failed: ${error.message}`);
          }
        }
      }

      // 应用过滤器
      if (this.config.filters && this.config.filters.length > 0) {
        return this.applyFilters(result);
      }

      return result;
    } catch (error) {
      console.error(`Failed to parse ${this.config.name} page:`, error.message);
      return {
        type: this.config.name,
        url,
        error: error.message,
        timestamp: new Date().toISOString()
      };
    }
  }

  /**
   * 执行提取器
   * @param {Page} page - Playwright页面对象
   * @param {Object} extractor - 提取器配置
   * @returns {Promise<any>} 提取的数据
   */
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
      default:
        throw new Error(`Unknown extractor type: ${extractor.type}`);
    }
  }

  /**
   * 提取文本
   * @param {Page} page - Playwright页面对象
   * @param {Object} extractor - 提取器配置
   * @returns {Promise<string>} 提取的文本
   */
  async extractText(page, extractor) {
    try {
      const text = await page.evaluate((selector) => {
        const element = document.querySelector(selector);
        return element ? element.textContent.trim() : '';
      }, extractor.selector);

      // 如果有pattern，进行匹配过滤
      if (extractor.pattern && text) {
        const regex = new RegExp(extractor.pattern);
        const match = text.match(regex);
        return match ? match[0] : text;
      }

      return text;
    } catch (error) {
      throw new Error(`Text extraction failed: ${error.message}`);
    }
  }

  /**
   * 提取表格
   * @param {Page} page - Playwright页面对象
   * @param {Object} extractor - 提取器配置
   * @returns {Promise<Object>} 提取的表格数据
   */
  async extractTable(page, extractor) {
    try {
      const tables = await page.evaluate((selector) => {
        const tableElements = Array.from(document.querySelectorAll(selector));
        return tableElements.map((table) => {
          // 提取表头
          const headers = [];
          const headerCells = table.querySelectorAll('thead th, thead td');
          if (headerCells.length > 0) {
            headerCells.forEach(cell => headers.push(cell.textContent.trim()));
          } else {
            const firstRow = table.querySelector('tr');
            if (firstRow) {
              const cells = firstRow.querySelectorAll('th, td');
              cells.forEach(cell => headers.push(cell.textContent.trim()));
            }
          }

          // 提取数据行
          const rows = [];
          const bodyRows = table.querySelectorAll('tbody tr');
          const rowsToProcess = bodyRows.length > 0 ? bodyRows : table.querySelectorAll('tr');
          
          rowsToProcess.forEach((row, rowIndex) => {
            // 跳过表头行
            if (rowIndex === 0 && bodyRows.length === 0 && headers.length > 0) return;
            
            const cells = Array.from(row.querySelectorAll('td, th'));
            if (cells.length > 0) {
              const rowData = cells.map(cell => cell.textContent.trim());
              rows.push(rowData);
            }
          });

          return { headers, rows };
        });
      }, extractor.selector);

      // 如果指定了列名，验证表格结构
      if (extractor.columns && tables.length > 0) {
        const table = tables[0];
        // 简单验证：检查列数是否匹配
        if (table.headers.length !== extractor.columns.length) {
          console.warn(`Table column count mismatch: expected ${extractor.columns.length}, got ${table.headers.length}`);
        }
      }

      return tables.length === 1 ? tables[0] : tables;
    } catch (error) {
      throw new Error(`Table extraction failed: ${error.message}`);
    }
  }

  /**
   * 提取代码块
   * @param {Page} page - Playwright页面对象
   * @param {Object} extractor - 提取器配置
   * @returns {Promise<Array>} 提取的代码块数组
   */
  async extractCode(page, extractor) {
    try {
      const codeBlocks = await page.evaluate((selector) => {
        const blocks = [];
        const elements = document.querySelectorAll(selector);
        
        elements.forEach(element => {
          let code = '';
          
          // 处理textarea
          if (element.tagName === 'TEXTAREA') {
            code = element.value.trim();
          } else {
            code = element.textContent.trim();
          }

          if (code) {
            // 尝试识别语言
            let language = 'text';
            const classList = element.className;
            const langMatch = classList.match(/language-(\w+)/);
            if (langMatch) {
              language = langMatch[1];
            } else if (code.startsWith('{') || code.startsWith('[')) {
              language = 'json';
            } else if (code.startsWith('<')) {
              language = 'xml';
            }
            
            blocks.push({ language, code });
          }
        });

        return blocks;
      }, extractor.selector);

      return codeBlocks;
    } catch (error) {
      throw new Error(`Code extraction failed: ${error.message}`);
    }
  }

  /**
   * 提取列表
   * @param {Page} page - Playwright页面对象
   * @param {Object} extractor - 提取器配置
   * @returns {Promise<Array>} 提取的列表数组
   */
  async extractList(page, extractor) {
    try {
      const lists = await page.evaluate((selector) => {
        const listElements = Array.from(document.querySelectorAll(selector));
        return listElements.map(list => {
          const items = Array.from(list.querySelectorAll('li'));
          return {
            type: list.tagName.toLowerCase(),
            items: items.map(item => item.textContent.trim())
          };
        });
      }, extractor.selector);

      return lists;
    } catch (error) {
      throw new Error(`List extraction failed: ${error.message}`);
    }
  }

  /**
   * 应用过滤器
   * @param {Object} result - 解析结果
   * @returns {Object} 过滤后的结果
   */
  applyFilters(result) {
    if (!this.config.filters || this.config.filters.length === 0) {
      return result;
    }

    let filteredResult = { ...result };

    // 遍历所有过滤器并应用
    for (const filter of this.config.filters) {
      try {
        switch (filter.type) {
          case 'remove':
            filteredResult = this.removeFilter(filteredResult, filter);
            break;
          case 'keep':
            filteredResult = this.keepFilter(filteredResult, filter);
            break;
          case 'transform':
            filteredResult = this.transformFilter(filteredResult, filter);
            break;
          default:
            console.warn(`Unknown filter type: ${filter.type}`);
        }
      } catch (error) {
        console.error(`Failed to apply filter ${filter.type}:`, error.message);
      }
    }

    return filteredResult;
  }

  /**
   * 移除过滤器 - 移除匹配的内容
   * @param {Object} result - 解析结果
   * @param {Object} filter - 过滤器配置
   * @returns {Object} 过滤后的结果
   */
  removeFilter(result, filter) {
    const { target, pattern } = filter;
    const regex = new RegExp(pattern);

    // 遍历结果中的所有字段
    for (const [key, value] of Object.entries(result)) {
      // 跳过元数据字段
      if (key === 'type' || key === 'url' || key === 'timestamp' || key === 'error') {
        continue;
      }

      // 处理字符串类型
      if (typeof value === 'string' && (target === 'text' || target === 'all')) {
        if (regex.test(value)) {
          result[key] = '';
        }
      }

      // 处理数组类型（表格、代码块、列表）
      if (Array.isArray(value)) {
        if (target === 'all' || this.matchesArrayTarget(key, target)) {
          result[key] = value.filter(item => {
            if (typeof item === 'string') {
              return !regex.test(item);
            }
            if (typeof item === 'object' && item !== null) {
              // 对于对象，检查其文本内容
              const text = this.extractTextFromObject(item);
              return !regex.test(text);
            }
            return true;
          });
        }
      }

      // 处理对象类型（表格）
      if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
        if (target === 'table' || target === 'all') {
          // 过滤表格行
          if (value.rows && Array.isArray(value.rows)) {
            value.rows = value.rows.filter(row => {
              const rowText = Array.isArray(row) ? row.join(' ') : String(row);
              return !regex.test(rowText);
            });
          }
        }
      }
    }

    return result;
  }

  /**
   * 保留过滤器 - 只保留匹配的内容
   * @param {Object} result - 解析结果
   * @param {Object} filter - 过滤器配置
   * @returns {Object} 过滤后的结果
   */
  keepFilter(result, filter) {
    const { target, pattern } = filter;
    const regex = new RegExp(pattern);

    // 遍历结果中的所有字段
    for (const [key, value] of Object.entries(result)) {
      // 跳过元数据字段
      if (key === 'type' || key === 'url' || key === 'timestamp' || key === 'error') {
        continue;
      }

      // 处理字符串类型
      if (typeof value === 'string' && (target === 'text' || target === 'all')) {
        if (!regex.test(value)) {
          result[key] = '';
        }
      }

      // 处理数组类型（表格、代码块、列表）
      if (Array.isArray(value)) {
        if (target === 'all' || this.matchesArrayTarget(key, target)) {
          result[key] = value.filter(item => {
            if (typeof item === 'string') {
              return regex.test(item);
            }
            if (typeof item === 'object' && item !== null) {
              // 对于对象，检查其文本内容
              const text = this.extractTextFromObject(item);
              return regex.test(text);
            }
            return false;
          });
        }
      }

      // 处理对象类型（表格）
      if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
        if (target === 'table' || target === 'all') {
          // 过滤表格行
          if (value.rows && Array.isArray(value.rows)) {
            value.rows = value.rows.filter(row => {
              const rowText = Array.isArray(row) ? row.join(' ') : String(row);
              return regex.test(rowText);
            });
          }
        }
      }
    }

    return result;
  }

  /**
   * 转换过滤器 - 转换内容
   * @param {Object} result - 解析结果
   * @param {Object} filter - 过滤器配置
   * @returns {Object} 过滤后的结果
   */
  transformFilter(result, filter) {
    const { target, pattern, replacement = '' } = filter;
    const regex = new RegExp(pattern, 'g');

    // 遍历结果中的所有字段
    for (const [key, value] of Object.entries(result)) {
      // 跳过元数据字段
      if (key === 'type' || key === 'url' || key === 'timestamp' || key === 'error') {
        continue;
      }

      // 处理字符串类型
      if (typeof value === 'string' && (target === 'text' || target === 'all')) {
        result[key] = value.replace(regex, replacement);
      }

      // 处理数组类型
      if (Array.isArray(value)) {
        if (target === 'all' || this.matchesArrayTarget(key, target)) {
          result[key] = value.map(item => {
            if (typeof item === 'string') {
              return item.replace(regex, replacement);
            }
            if (typeof item === 'object' && item !== null) {
              return this.transformObjectText(item, regex, replacement);
            }
            return item;
          });
        }
      }

      // 处理对象类型（表格）
      if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
        if (target === 'table' || target === 'all') {
          if (value.rows && Array.isArray(value.rows)) {
            value.rows = value.rows.map(row => {
              if (Array.isArray(row)) {
                return row.map(cell => String(cell).replace(regex, replacement));
              }
              return String(row).replace(regex, replacement);
            });
          }
          if (value.headers && Array.isArray(value.headers)) {
            value.headers = value.headers.map(header => String(header).replace(regex, replacement));
          }
        }
      }
    }

    return result;
  }

  /**
   * 检查字段名是否匹配目标类型
   * @param {string} fieldName - 字段名
   * @param {string} target - 目标类型
   * @returns {boolean} 是否匹配
   */
  matchesArrayTarget(fieldName, target) {
    const fieldLower = fieldName.toLowerCase();
    switch (target) {
      case 'table':
        return fieldLower.includes('table');
      case 'code':
        return fieldLower.includes('code');
      case 'list':
        return fieldLower.includes('list');
      case 'paragraph':
        return fieldLower.includes('paragraph') || fieldLower.includes('content');
      case 'heading':
        return fieldLower.includes('heading') || fieldLower.includes('title');
      default:
        return false;
    }
  }

  /**
   * 从对象中提取文本内容
   * @param {Object} obj - 对象
   * @returns {string} 文本内容
   */
  extractTextFromObject(obj) {
    if (obj.code) return obj.code;
    if (obj.items) return Array.isArray(obj.items) ? obj.items.join(' ') : String(obj.items);
    if (obj.rows) return Array.isArray(obj.rows) ? obj.rows.flat().join(' ') : String(obj.rows);
    return JSON.stringify(obj);
  }

  /**
   * 转换对象中的文本
   * @param {Object} obj - 对象
   * @param {RegExp} regex - 正则表达式
   * @param {string} replacement - 替换文本
   * @returns {Object} 转换后的对象
   */
  transformObjectText(obj, regex, replacement) {
    const transformed = { ...obj };
    
    if (transformed.code) {
      transformed.code = transformed.code.replace(regex, replacement);
    }
    if (transformed.items && Array.isArray(transformed.items)) {
      transformed.items = transformed.items.map(item => String(item).replace(regex, replacement));
    }
    if (transformed.rows && Array.isArray(transformed.rows)) {
      transformed.rows = transformed.rows.map(row => {
        if (Array.isArray(row)) {
          return row.map(cell => String(cell).replace(regex, replacement));
        }
        return String(row).replace(regex, replacement);
      });
    }
    
    return transformed;
  }

  /**
   * 获取配置信息
   * @returns {Object} 配置对象
   */
  getConfig() {
    return this.config;
  }

  /**
   * 获取解析器名称
   * @returns {string} 名称
   */
  getName() {
    return this.name;
  }
}

module.exports = TemplateParser;
