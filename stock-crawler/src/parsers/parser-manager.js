import ApiDocParser from './api-doc-parser.js';
import CoreContentParser from './core-content-parser.js';
import DirectoryParser from './directory-parser.js';
import GenericParser from './generic-parser.js';
import ListParser from './list-parser.js';
import PageClassifier from './page-classifier.js';
import TableOnlyParser from './table-only-parser.js';

/**
 * Parser Manager - 管理所有解析器，根据URL选择合适的解析器
 */
class ParserManager {
  constructor() {
    this.parsers = [];
    this.classifier = new PageClassifier();
    this.classificationParserMap = {
      api_doc_page: 'ApiDocParser',
      article_page: 'CoreContentParser',
      list_page: 'ListParser',
      directory_page: 'DirectoryParser',
      table_content_page: 'TableOnlyParser'
    };
    this.classificationConfidenceThreshold = 0.7;
    this.registerDefaultParsers();
  }

  /**
   * 注册默认解析器
   */
  registerDefaultParsers() {
    this.register(new CoreContentParser());
    this.register(new ApiDocParser());
    this.register(new ListParser());
    this.register(new DirectoryParser());
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
  selectParser(url, options = {}) {
    const forcedParser = this.selectParserByUrlPattern(url, options.parserUrlPatternOverrides);
    if (forcedParser) {
      return forcedParser;
    }

    const classificationParser = this.selectParserByClassification(options.classification);
    if (classificationParser) {
      return classificationParser;
    }

    const genericParser = this.getParserByName('GenericParser');
    if (genericParser) {
      return genericParser;
    }

    for (const parser of this.parsers) {
      if (parser.matches(url, options)) {
        return parser;
      }
    }
    // 理论上不会到这里，因为GenericParser匹配所有URL
    return this.parsers[this.parsers.length - 1];
  }

  selectParserByUrlPattern(url, parserUrlPatternOverrides = []) {
    if (!Array.isArray(parserUrlPatternOverrides) || parserUrlPatternOverrides.length === 0) {
      return null;
    }

    for (const rule of parserUrlPatternOverrides) {
      const regex = this.toRegExp(rule?.pattern);
      if (!regex || !regex.test(url)) {
        continue;
      }

      const parser = this.getParserByName(rule?.parser);
      if (parser) {
        return parser;
      }
    }

    return null;
  }

  selectParserByClassification(classification) {
    if (!this.isClassificationPrecise(classification)) {
      return null;
    }

    const parserName = this.classificationParserMap[classification.type];
    return this.getParserByName(parserName);
  }

  isClassificationPrecise(classification = {}) {
    if (!classification?.type) return false;
    if (!(classification.type in this.classificationParserMap)) return false;

    return (classification.confidence ?? 0) >= this.classificationConfidenceThreshold;
  }

  getParserByName(parserName) {
    if (!parserName) return null;
    return this.parsers.find((parser) => parser.constructor.name === parserName) || null;
  }

  toRegExp(pattern) {
    if (!pattern || typeof pattern !== 'string') {
      return null;
    }

    try {
      return new RegExp(pattern);
    } catch (error) {
      return null;
    }
  }

  /**
   * 解析页面
   * @param {Page} page - Playwright页面对象
   * @param {string} url - 页面URL
   * @param {Object} options - 解析选项
   * @returns {Promise<Object>} 解析后的页面数据
   */
  async parse(page, url, options = {}) {
    const forcedParser = this.selectParserByUrlPattern(url, options.parserUrlPatternOverrides);
    const classification = options.classification || (forcedParser ? null : await this.classifier.classify(page, url));

    const parser = this.selectParser(url, {
      ...options,
      classification
    });

    const pageData = await parser.parse(page, url, {
      ...options,
      classification
    });

    return {
      ...pageData,
      classification
    };
  }
}

export default ParserManager;
