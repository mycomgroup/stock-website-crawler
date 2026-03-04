import ApiDocParser from './api-doc-parser.js';
import GenericParser from './generic-parser.js';
import TableOnlyParser from './table-only-parser.js';

/**
 * Parser Manager - 管理所有解析器，根据URL选择合适的解析器
 */
class ParserManager {
  constructor() {
    this.parsers = [];
    this.registerDefaultParsers();
  }

  /**
   * 注册默认解析器
   */
  registerDefaultParsers() {
    this.register(new ApiDocParser());
    this.register(new TableOnlyParser());
    this.register(new GenericParser());
  }

  /**
   * 注册新的解析器
   * @param {BaseParser} parser - 解析器实例
   */
  register(parser) {
    this.parsers.push(parser);
    // 按优先级排序（高优先级在前）
    this.parsers.sort((a, b) => b.getPriority() - a.getPriority());
  }

  /**
   * 根据URL选择合适的解析器
   * @param {string} url - 页面URL
   * @returns {BaseParser} 匹配的解析器
   */
  selectParser(url) {
    for (const parser of this.parsers) {
      if (parser.matches(url)) {
        return parser;
      }
    }
    // 理论上不会到这里，因为GenericParser匹配所有URL
    return this.parsers[this.parsers.length - 1];
  }

  /**
   * 解析页面
   * @param {Page} page - Playwright页面对象
   * @param {string} url - 页面URL
   * @param {Object} options - 解析选项
   * @returns {Promise<Object>} 解析后的页面数据
   */
  async parse(page, url, options = {}) {
    const parser = this.selectParser(url);
    return await parser.parse(page, url, options);
  }
}

export default ParserManager;
