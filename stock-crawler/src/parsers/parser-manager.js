import ApiDocParser from './api-doc-parser.js';
import AlphavantageApiParser from './alphavantage-api-parser.js';
import AlltickApiParser from './alltick-api-parser.js';
import Api60sDocsParser from './api60s-docs-parser.js';
import BraveSearchParser from './brave-search-parser.js';
import EodhdApiParser from './eodhd-api-parser.js';
import EulerpoolApiParser from './eulerpool-api-parser.js';
import FinnhubApiParser from './finnhub-api-parser.js';
import FinancialDatasetsApiParser from './financial-datasets-api-parser.js';
import FinancialModelingPrepApiParser from './financial-modeling-prep-api-parser.js';
import InfowayApiParser from './infoway-api-parser.js';
import ItickApiParser from './itick-api-parser.js';
import MassiveApiParser from './massive-api-parser.js';
import ModelscopeMcpParser from './modelscope-mcp-parser.js';
import PolyrouterParser from './polyrouter-parser.js';
import TiingoApiParser from './tiingo-api-parser.js';
import RsshubParser from './rsshub-parser.js';
import SerpApiParser from './serpapi-parser.js';
import TavilyApiParser from './tavily-api-parser.js';
import TickdbApiParser from './tickdb-api-parser.js';
import TsanghiApiParser from './tsanghi-api-parser.js';
import TushareProApiParser from './tushare-pro-api-parser.js';
import QverisApiParser from './qveris-api-parser.js';
import SanhulianghuaParser from './sanhulianghua-parser.js';
import YfinanceApiParser from './yfinance-api-parser.js';
import GenericParser from './generic-parser.js';

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
    this.register(new AlphavantageApiParser());
    this.register(new AlltickApiParser());
    this.register(new Api60sDocsParser());
    this.register(new BraveSearchParser());
    this.register(new EodhdApiParser());
    this.register(new EulerpoolApiParser());
    this.register(new FinnhubApiParser());
    this.register(new FinancialDatasetsApiParser());
    this.register(new FinancialModelingPrepApiParser());
    this.register(new InfowayApiParser());
    this.register(new ItickApiParser());
    this.register(new MassiveApiParser());
    this.register(new ModelscopeMcpParser());
    this.register(new PolyrouterParser());
    this.register(new TiingoApiParser());
    this.register(new RsshubParser());
    this.register(new SerpApiParser());
    this.register(new TavilyApiParser());
    this.register(new TickdbApiParser());
    this.register(new TsanghiApiParser());
    this.register(new TushareProApiParser());
    this.register(new QverisApiParser());
    this.register(new SanhulianghuaParser());
    this.register(new YfinanceApiParser());
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
