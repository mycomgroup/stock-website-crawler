import BrowserManager from '../../../stock-crawler/src/browser-manager.js';
import LoginHandler from '../../../stock-crawler/src/login-handler.js';
import PageParser from '../../../stock-crawler/src/page-parser.js';
import { PatternMatcher } from './pattern-matcher.js';
import fs from 'fs';

/**
 * Web API 客户端
 */
export class WebApiClient {
  constructor(config) {
    this.config = config;
    this.browserManager = null;
    this.loginHandler = null;
    this.pageParser = null;
    this.patternMatcher = new PatternMatcher(config.patternsPath);
    this.apiConfigs = this.loadApiConfigs(config.configPath);
  }

  /**
   * 加载 API 配置
   */
  loadApiConfigs(configPath) {
    if (!configPath || !fs.existsSync(configPath)) {
      return {};
    }

    const content = fs.readFileSync(configPath, 'utf-8');
    const configs = JSON.parse(content);
    
    // 转换为 Map 方便查找
    const configMap = {};
    for (const config of configs) {
      configMap[config.api] = config;
    }
    
    return configMap;
  }

  /**
   * 初始化
   */
  async initialize() {
    this.browserManager = new BrowserManager();
    await this.browserManager.launch({
      headless: true,
      timeout: 30000
    });

    this.loginHandler = new LoginHandler(
      this.config.username,
      this.config.password
    );

    this.pageParser = new PageParser();

    // 登录
    const page = await this.browserManager.newPage();
    try {
      await this.loginHandler.login(page, this.browserManager);
    } finally {
      await page.close();
    }
  }

  /**
   * 调用 API
   */
  async callApi(apiName, params = {}) {
    const pattern = this.patternMatcher.getPatternByName(apiName);
    
    if (!pattern) {
      throw new Error(`API 不存在: ${apiName}`);
    }

    const normalizedParams = this.normalizeParams(pattern, params);
    const url = this.patternMatcher.buildUrl(pattern, normalizedParams);
    console.log(`抓取: ${url}`);

    const page = await this.browserManager.newPage();
    
    try {
      await this.browserManager.goto(page, url);
      await page.waitForLoadState('networkidle', { timeout: 10000 }).catch(() => {});

      const data = await this.pageParser.parse(page, url, {
        filepath: 'temp.md',
        pagesDir: '/tmp'
      });

      // 获取 API 配置
      const apiConfig = this.apiConfigs[apiName];
      const outputFormat = apiConfig?.outputFormat || 'md';

      return {
        success: true,
        api: apiName,
        url,
        outputFormat,
        data: this.formatData(data, outputFormat, apiConfig)
      };
    } finally {
      await page.close();
    }
  }

  /**
   * 兼容参数名：支持原始 paramX 和路径模板参数名
   */
  normalizeParams(pattern, params = {}) {
    const normalized = { ...params };
    const pathParamNames = this.patternMatcher.getPathParamNames(pattern);

    pathParamNames.forEach((name, index) => {
      const fallbackName = `param${index + 1}`;
      if (normalized[name] === undefined && normalized[fallbackName] !== undefined) {
        normalized[name] = normalized[fallbackName];
      }
      if (normalized[fallbackName] === undefined && normalized[name] !== undefined) {
        normalized[fallbackName] = normalized[name];
      }
    });

    return normalized;
  }

  /**
   * 格式化数据
   */
  formatData(data, outputFormat, apiConfig) {
    if (outputFormat === 'csv') {
      return this.formatAsCSV(data, apiConfig);
    } else {
      return this.formatAsMD(data, apiConfig);
    }
  }

  /**
   * 格式化为 CSV
   */
  formatAsCSV(data, apiConfig) {
    const result = {
      type: 'csv',
      url: data.url,
      title: data.title,
      tables: []
    };

    // 提取主要表格数据
    if (data.tables && data.tables.length > 0) {
      for (const table of data.tables) {
        if (table.headers && table.headers.length > 0 && table.rows && table.rows.length > 0) {
          result.tables.push({
            headers: table.headers,
            rows: table.rows,
            csv: this.tableToCSV(table)
          });
        }
      }
    }

    return result;
  }

  /**
   * 表格转 CSV
   */
  tableToCSV(table) {
    const lines = [];
    
    // 添加表头
    lines.push(table.headers.map(h => this.escapeCSV(h)).join(','));
    
    // 添加数据行
    for (const row of table.rows) {
      lines.push(row.map(cell => this.escapeCSV(cell)).join(','));
    }
    
    return lines.join('\n');
  }

  /**
   * CSV 转义
   */
  escapeCSV(value) {
    if (value === null || value === undefined) {
      return '';
    }
    
    const str = String(value);
    
    // 如果包含逗号、引号或换行，需要用引号包裹
    if (str.includes(',') || str.includes('"') || str.includes('\n')) {
      return '"' + str.replace(/"/g, '""') + '"';
    }
    
    return str;
  }

  /**
   * 格式化为 MD
   */
  formatAsMD(data, apiConfig) {
    return {
      type: 'md',
      url: data.url,
      title: data.title,
      description: data.description,
      tables: data.tables?.map(t => ({
        headers: t.headers,
        rowCount: t.rows?.length || 0,
        rows: t.rows?.slice(0, 10) // 只返回前10行作为示例
      })),
      charts: data.charts?.length || 0,
      images: data.images?.length || 0,
      mainContent: data.mainContent?.slice(0, 20) // 只返回前20个内容块
    };
  }

  /**
   * 关闭
   */
  async close() {
    if (this.browserManager) {
      await this.browserManager.close();
    }
  }
}
