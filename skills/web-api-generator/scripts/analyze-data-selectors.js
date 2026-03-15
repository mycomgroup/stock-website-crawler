#!/usr/bin/env node

import BrowserManager from '../../../stock-crawler/src/browser-manager.js';
import LoginHandler from '../../../stock-crawler/src/login-handler.js';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import dotenv from 'dotenv';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

dotenv.config({ path: path.join(__dirname, '../../../.env') });

/**
 * 分析页面数据选择器
 * 为每个 URL pattern 找到核心数据块的选择器
 */
class DataSelectorAnalyzer {
  constructor() {
    this.browserManager = null;
    this.loginHandler = null;
  }

  async initialize() {
    const username = process.env.LIXINGER_USERNAME;
    const password = process.env.LIXINGER_PASSWORD;

    if (!username || !password) {
      throw new Error('请设置 LIXINGER_USERNAME 和 LIXINGER_PASSWORD');
    }

    this.browserManager = new BrowserManager();
    await this.browserManager.launch({ headless: true, timeout: 30000 });

    this.loginHandler = new LoginHandler(username, password);

    const page = await this.browserManager.newPage();
    try {
      await this.loginHandler.login(page, this.browserManager);
    } finally {
      await page.close();
    }
  }

  /**
   * 分析单个 URL 的数据选择器
   */
  async analyzeUrl(url) {
    const page = await this.browserManager.newPage();
    
    try {
      await this.browserManager.goto(page, url);
      await page.waitForLoadState('networkidle', { timeout: 10000 }).catch(() => {});

      // 分析页面结构
      const selectors = await page.evaluate(() => {
        const result = {
          tables: [],
          mainContent: null,
          dataContainers: []
        };

        // 1. 查找所有表格
        const tables = document.querySelectorAll('table');
        tables.forEach((table, index) => {
          const headers = [];
          const headerCells = table.querySelectorAll('thead th, thead td');
          headerCells.forEach(cell => headers.push(cell.textContent.trim()));

          const rowCount = table.querySelectorAll('tbody tr, tr').length;
          
          // 生成选择器
          let selector = '';
          if (table.id) {
            selector = `#${table.id}`;
          } else if (table.className) {
            selector = `table.${table.className.split(' ')[0]}`;
          } else {
            selector = `table:nth-of-type(${index + 1})`;
          }

          result.tables.push({
            selector,
            xpath: this.getXPath(table),
            headers: headers.slice(0, 5),
            rowCount,
            hasId: !!table.id,
            hasClass: !!table.className
          });
        });

        // 2. 查找主要内容容器
        const mainSelectors = [
          'main',
          '[role="main"]',
          '#content',
          '.content',
          '#main',
          '.main-content',
          'article'
        ];

        for (const sel of mainSelectors) {
          const el = document.querySelector(sel);
          if (el) {
            result.mainContent = {
              selector: sel,
              xpath: this.getXPath(el),
              hasTable: el.querySelectorAll('table').length > 0,
              hasChart: el.querySelectorAll('canvas, svg').length > 0
            };
            break;
          }
        }

        // 3. 查找数据容器（通常包含表格或图表）
        const containers = document.querySelectorAll('[class*="data"], [class*="table"], [class*="chart"], [id*="data"], [id*="table"]');
        containers.forEach(container => {
          if (container.querySelectorAll('table, canvas, svg').length > 0) {
            let selector = '';
            if (container.id) {
              selector = `#${container.id}`;
            } else if (container.className) {
              selector = `.${container.className.split(' ')[0]}`;
            }

            if (selector) {
              result.dataContainers.push({
                selector,
                xpath: this.getXPath(container),
                hasTables: container.querySelectorAll('table').length,
                hasCharts: container.querySelectorAll('canvas, svg').length
              });
            }
          }
        });

        return result;

        // Helper function
        function getXPath(element) {
          if (element.id) {
            return `//*[@id="${element.id}"]`;
          }
          
          const parts = [];
          while (element && element.nodeType === Node.ELEMENT_NODE) {
            let index = 0;
            let sibling = element.previousSibling;
            
            while (sibling) {
              if (sibling.nodeType === Node.ELEMENT_NODE && sibling.nodeName === element.nodeName) {
                index++;
              }
              sibling = sibling.previousSibling;
            }
            
            const tagName = element.nodeName.toLowerCase();
            const pathIndex = index > 0 ? `[${index + 1}]` : '';
            parts.unshift(tagName + pathIndex);
            
            element = element.parentNode;
          }
          
          return parts.length ? '/' + parts.join('/') : '';
        }
      });

      return selectors;
    } finally {
      await page.close();
    }
  }

  /**
   * 为 pattern 生成数据选择器配置
   */
  async analyzePattern(pattern) {
    console.log(`\n分析 ${pattern.name}...`);
    
    // 使用第一个示例 URL
    const url = pattern.samples[0];
    console.log(`  URL: ${url}`);

    try {
      const selectors = await this.analyzeUrl(url);
      
      // 生成配置
      const config = {
        api: pattern.name,
        url: url,
        dataSelectors: {
          // 主表格选择器
          primaryTable: selectors.tables.length > 0 ? selectors.tables[0].selector : null,
          primaryTableXPath: selectors.tables.length > 0 ? selectors.tables[0].xpath : null,
          
          // 所有表格
          allTables: selectors.tables.map(t => ({
            selector: t.selector,
            xpath: t.xpath,
            headers: t.headers
          })),
          
          // 主内容区域
          mainContent: selectors.mainContent?.selector || 'main',
          mainContentXPath: selectors.mainContent?.xpath || null,
          
          // 数据容器
          dataContainers: selectors.dataContainers.map(c => c.selector)
        },
        analysis: {
          tableCount: selectors.tables.length,
          hasMainContent: !!selectors.mainContent,
          dataContainerCount: selectors.dataContainers.length
        }
      };

      console.log(`  ✓ 找到 ${selectors.tables.length} 个表格`);
      if (selectors.tables.length > 0) {
        console.log(`    主表格: ${selectors.tables[0].selector}`);
      }

      return config;
    } catch (error) {
      console.error(`  ✗ 分析失败: ${error.message}`);
      return {
        api: pattern.name,
        url: url,
        error: error.message,
        dataSelectors: {
          primaryTable: null,
          allTables: [],
          mainContent: 'main',
          dataContainers: []
        }
      };
    }
  }

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
  node analyze-data-selectors.js [options]

选项:
  --patterns=<path>    url-patterns.json 文件路径
  --output=<path>      输出文件路径
  --limit=<number>     限制分析的 pattern 数量（用于测试）
  --apis=<names>       只分析指定的 API（逗号分隔）

示例:
  # 分析所有 patterns
  node analyze-data-selectors.js

  # 只分析前 5 个
  node analyze-data-selectors.js --limit=5

  # 只分析特定 API
  node analyze-data-selectors.js --apis=detail-sh,constituents-list
    `);
    process.exit(0);
  }

  // 解析参数
  const params = {};
  for (const arg of args) {
    if (arg.startsWith('--')) {
      const [key, value] = arg.substring(2).split('=');
      params[key] = value || true;
    }
  }

  const patternsPath = params.patterns || path.join(__dirname, '../../../stock-crawler/output/lixinger-crawler/url-patterns.json');
  const outputPath = params.output || path.join(__dirname, '../output/data-selectors.json');
  const limit = params.limit ? parseInt(params.limit) : null;
  const apiFilter = params.apis ? params.apis.split(',') : null;

  // 加载 patterns
  const content = fs.readFileSync(patternsPath, 'utf-8');
  const data = JSON.parse(content);
  let patterns = data.patterns || [];

  // 过滤
  if (apiFilter) {
    patterns = patterns.filter(p => apiFilter.includes(p.name));
  }

  if (limit) {
    patterns = patterns.slice(0, limit);
  }

  console.log(`将分析 ${patterns.length} 个 patterns\n`);

  const analyzer = new DataSelectorAnalyzer();
  await analyzer.initialize();

  const results = [];
  
  for (let i = 0; i < patterns.length; i++) {
    const pattern = patterns[i];
    console.log(`[${i + 1}/${patterns.length}]`);
    
    const config = await analyzer.analyzePattern(pattern);
    results.push(config);

    // 避免请求过快
    await new Promise(resolve => setTimeout(resolve, 1000));
  }

  await analyzer.close();

  // 保存结果
  const outputDir = path.dirname(outputPath);
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  fs.writeFileSync(outputPath, JSON.stringify(results, null, 2));
  
  console.log(`\n✓ 分析完成！`);
  console.log(`结果已保存到: ${outputPath}`);
  console.log(`\n统计:`);
  console.log(`  - 总数: ${results.length}`);
  console.log(`  - 有表格: ${results.filter(r => r.analysis?.tableCount > 0).length}`);
  console.log(`  - 有主内容: ${results.filter(r => r.analysis?.hasMainContent).length}`);
}

main().catch(error => {
  console.error('错误:', error);
  process.exit(1);
});
