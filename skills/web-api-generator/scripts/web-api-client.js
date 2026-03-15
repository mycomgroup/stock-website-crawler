#!/usr/bin/env node

import BrowserManager from '../stock-crawler/src/browser-manager.js';
import LoginHandler from '../stock-crawler/src/login-handler.js';
import PageParser from '../stock-crawler/src/page-parser.js';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import dotenv from 'dotenv';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

dotenv.config();

/**
 * Web API 客户端
 * 像调用 API 一样使用网页抓取
 */
class WebApiClient {
  constructor() {
    this.patternsPath = path.join(__dirname, '../stock-crawler/output/lixinger-crawler/url-patterns.json');
    this.patterns = this.loadPatterns();
    this.browserManager = null;
    this.loginHandler = null;
    this.pageParser = null;
  }

  /**
   * 加载 patterns
   */
  loadPatterns() {
    const content = fs.readFileSync(this.patternsPath, 'utf-8');
    const data = JSON.parse(content);
    return data.patterns || [];
  }

  /**
   * 初始化
   */
  async initialize() {
    const username = process.env.LIXINGER_USERNAME;
    const password = process.env.LIXINGER_PASSWORD;

    if (!username || !password) {
      throw new Error('请在 .env 文件中设置 LIXINGER_USERNAME 和 LIXINGER_PASSWORD');
    }

    this.browserManager = new BrowserManager();
    await this.browserManager.launch({
      headless: true,
      timeout: 30000
    });

    this.loginHandler = new LoginHandler(username, password);
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
   * 列出所有 API
   */
  listApis() {
    console.log('\n可用的 Web APIs:\n');

    const categories = {};
    for (const pattern of this.patterns) {
      const pathParts = pattern.pathTemplate.split('/').filter(p => p && !p.startsWith('{'));
      const category = pathParts[0] || 'other';

      if (!categories[category]) {
        categories[category] = [];
      }
      categories[category].push(pattern);
    }

    for (const [category, patterns] of Object.entries(categories)) {
      console.log(`\n${category}:`);
      for (const pattern of patterns.slice(0, 5)) {
        console.log(`  - ${pattern.name}: ${pattern.description}`);
      }
      if (patterns.length > 5) {
        console.log(`  ... 还有 ${patterns.length - 5} 个`);
      }
    }

    console.log(`\n总计: ${this.patterns.length} 个 API\n`);
  }

  /**
   * 搜索 API
   */
  searchApis(keyword) {
    const results = [];
    const keywordLower = keyword.toLowerCase();

    for (const pattern of this.patterns) {
      if (pattern.name.toLowerCase().includes(keywordLower) ||
          pattern.description.toLowerCase().includes(keywordLower)) {
        results.push(pattern);
      }
    }

    console.log(`\n找到 ${results.length} 个匹配的 API:\n`);
    for (const pattern of results) {
      console.log(`- ${pattern.name}: ${pattern.description}`);
      console.log(`  示例: ${pattern.samples[0]}`);
      console.log('');
    }
  }

  /**
   * 调用 API
   */
  async callApi(apiName, params = {}) {
    // 查找 pattern
    const pattern = this.patterns.find(p => p.name === apiName);
    if (!pattern) {
      throw new Error(`API 不存在: ${apiName}`);
    }

    // 构建 URL
    const url = this.buildUrl(pattern, params);
    console.log(`\n正在抓取: ${url}\n`);

    // 抓取页面
    const page = await this.browserManager.newPage();
    try {
      await this.browserManager.goto(page, url);
      await page.waitForLoadState('networkidle', { timeout: 10000 }).catch(() => {});

      // 解析页面
      const data = await this.pageParser.parse(page, url, {
        filepath: 'temp.md',
        pagesDir: '/tmp'
      });

      return {
        success: true,
        api: apiName,
        url,
        data: this.simplifyData(data)
      };
    } finally {
      await page.close();
    }
  }

  /**
   * 构建 URL
   */
  buildUrl(pattern, params) {
    let url = pattern.samples[0];

    // 如果提供了参数，替换路径参数
    if (Object.keys(params).length > 0) {
      let path = pattern.pathTemplate;

      // 替换路径参数
      for (const [key, value] of Object.entries(params)) {
        path = path.replace(`{${key}}`, value);
      }

      // 构建完整 URL
      url = `https://www.lixinger.com${path}`;

      // 添加查询参数
      const queryParams = [];
      for (const [key, value] of Object.entries(params)) {
        if (!key.startsWith('param')) {
          queryParams.push(`${key}=${encodeURIComponent(value)}`);
        }
      }

      if (queryParams.length > 0) {
        url += '?' + queryParams.join('&');
      }
    }

    return url;
  }

  /**
   * 简化数据（只保留关键信息）
   */
  simplifyData(data) {
    return {
      type: data.type,
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
      tabsAndDropdowns: data.tabsAndDropdowns?.map(t => ({
        type: t.type,
        name: t.name,
        hasData: !!t.data
      }))
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

// 主程序
async function main() {
  const args = process.argv.slice(2);

  if (args.length === 0 || args[0] === '--help') {
    console.log(`
使用方法:
  node web-api-client.js list                    # 列出所有 API
  node web-api-client.js search <关键词>          # 搜索 API
  node web-api-client.js <api-name> [参数]        # 调用 API

示例:
  node web-api-client.js list
  node web-api-client.js search 公司详情
  node web-api-client.js detail-sh --param4=600519 --param5=600519
  node web-api-client.js api-doc --api-key=cn/company

参数格式:
  --param4=value
  --api-key=value
    `);
    process.exit(0);
  }

  const client = new WebApiClient();

  try {
    const command = args[0];

    if (command === 'list') {
      client.listApis();
    } else if (command === 'search') {
      if (args.length < 2) {
        console.error('错误: 请提供搜索关键词');
        process.exit(1);
      }
      client.searchApis(args[1]);
    } else {
      // 调用 API
      await client.initialize();

      // 解析参数
      const params = {};
      for (let i = 1; i < args.length; i++) {
        if (args[i].startsWith('--')) {
          const [key, value] = args[i].substring(2).split('=');
          params[key] = value;
        }
      }

      const result = await client.callApi(command, params);
      
      // 输出结果
      console.log('\n结果:\n');
      console.log(JSON.stringify(result, null, 2));
      
      // 保存到文件
      const outputFile = `output-${command}-${Date.now()}.json`;
      fs.writeFileSync(outputFile, JSON.stringify(result, null, 2));
      console.log(`\n已保存到: ${outputFile}\n`);

      await client.close();
    }
  } catch (error) {
    console.error('\n错误:', error.message);
    await client.close();
    process.exit(1);
  }
}

main();
