import BaseParser from './base-parser.js';

/**
 * Tsanghi API Parser - 专门解析沧海数据金融 API 文档页面
 * 网站: https://tsanghi.com/fin/doc
 * 这是一个 SPA 应用，使用 Element UI 框架
 */
class TsanghiApiParser extends BaseParser {
  constructor() {
    super();
    this.processedMenus = new Set();
  }

  /**
   * 匹配 Tsanghi API 文档页面
   * @param {string} url - 页面URL
   * @returns {boolean} 是否匹配
   */
  matches(url) {
    return /^https?:\/\/(www\.)?tsanghi\.com\/fin\/doc/.test(url);
  }

  /**
   * 获取优先级
   * @returns {number} 优先级
   */
  getPriority() {
    return 100;
  }

  /**
   * 根据 URL 和菜单路径生成文件名
   * @param {string} url - 页面URL
   * @param {string} menuPath - 菜单路径
   * @returns {string} 文件名
   */
  generateFilename(url, menuPath = '') {
    if (menuPath) {
      return menuPath
        .replace(/ > /g, '_')
        .replace(/[^a-zA-Z0-9_\u4e00-\u9fa5]/g, '')
        .substring(0, 50);
    }

    try {
      const urlObj = new URL(url);
      const index = urlObj.searchParams.get('index') || 'main';
      return `doc_${index.replace(/-/g, '_')}`;
    } catch (e) {
      return 'api_doc';
    }
  }

  /**
   * 解析 Tsanghi API 文档页面
   * 这是一个 SPA，需要遍历菜单获取所有内容
   * @param {Page} page - Playwright页面对象
   * @param {string} url - 页面URL
   * @param {Object} options - 解析选项
   * @returns {Promise<Object>} 解析后的页面数据
   */
  async parse(page, url, options = {}) {
    try {
      // 等待页面加载
      await this.waitForContent(page);

      // 获取所有菜单项并遍历获取内容
      const pages = await this.crawlAllPages(page);

      return {
        type: 'tsanghi-api',
        url,
        pages: pages,
        suggestedFilename: this.generateFilename(url)
      };
    } catch (error) {
      console.error('Failed to parse Tsanghi API doc page:', error.message);
      return {
        type: 'tsanghi-api',
        url,
        pages: [],
        suggestedFilename: this.generateFilename(url)
      };
    }
  }

  /**
   * 等待页面内容加载完成
   */
  async waitForContent(page) {
    try {
      await page.waitForLoadState('domcontentloaded', { timeout: 30000 });
      await page.waitForSelector('.el-menu', { timeout: 15000 });
      await page.waitForTimeout(3000);
    } catch (error) {
      console.warn('Wait for content timeout:', error.message);
    }
  }

  /**
   * 展开所有子菜单
   */
  async expandAllMenus(page) {
    const submenus = await page.$$('.el-submenu');
    for (const submenu of submenus) {
      try {
        const isExpanded = await submenu.evaluate(el => {
          const ul = el.querySelector('ul');
          return ul && ul.style.display !== 'none';
        });

        if (!isExpanded) {
          await submenu.click();
          await page.waitForTimeout(200);
        }
      } catch (e) {
        // 忽略错误
      }
    }
    await page.waitForTimeout(500);
  }

  /**
   * 提取当前显示页面内容
   */
  async extractPageContent(page) {
    return await page.evaluate(() => {
      // 获取右侧内容区域
      const elMain = document.querySelector('.el-main');
      if (!elMain) return null;

      const elCols = elMain.querySelectorAll('.el-col');
      let rightCol = null;

      // 找到最宽的列作为内容区域
      elCols.forEach(col => {
        if (col.className.includes('el-col-19') || col.className.includes('el-col-18')) {
          rightCol = col;
        }
      });

      if (!rightCol) return null;

      // 获取面包屑导航
      const breadcrumb = rightCol.querySelector('.el-breadcrumb, .breadcrumb');
      let breadcrumbText = '';
      if (breadcrumb) {
        breadcrumbText = breadcrumb.textContent.trim();
      } else {
        // 尝试从文本中提取路径
        const text = rightCol.textContent;
        const match = text.match(/([^\n]+)\s*>\s*([^\n]+)/);
        if (match) {
          breadcrumbText = `${match[1]} > ${match[2]}`;
        }
      }

      // 获取标题
      const titleEl = rightCol.querySelector('h1, h2, .title, .el-heading');
      let title = titleEl ? titleEl.textContent.trim() : '';

      // 如果没有标题，从面包屑提取
      if (!title && breadcrumbText) {
        const parts = breadcrumbText.split(' > ');
        title = parts[parts.length - 1];
      }

      // 获取 API 端点
      let apiUrl = '';
      const preElements = rightCol.querySelectorAll('pre');
      preElements.forEach(pre => {
        const text = pre.textContent;
        const urlMatch = text.match(/https?:\/\/[^\s]+/);
        if (urlMatch) {
          apiUrl = urlMatch[0];
        }
      });

      // 获取请求方式
      let httpMethod = '';
      const methodMatch = rightCol.textContent.match(/\b(GET|POST|PUT|DELETE)\b/);
      if (methodMatch) {
        httpMethod = methodMatch[1];
      }

      // 获取表格数据
      const tables = rightCol.querySelectorAll('table');
      const tableData = [];
      tables.forEach(table => {
        const rows = table.querySelectorAll('tr');
        const tableContent = [];
        rows.forEach(row => {
          const cells = row.querySelectorAll('th, td');
          const rowData = Array.from(cells).map(cell => cell.textContent.trim().replace(/\n+/g, ' '));
          if (rowData.some(d => d)) {
            tableContent.push(rowData);
          }
        });
        if (tableContent.length > 0) {
          tableData.push(tableContent);
        }
      });

      // 获取代码示例
      const codeExamples = [];
      preElements.forEach(pre => {
        const code = pre.textContent.trim();
        let lang = '';
        if (code.includes('curl') || code.includes('--url')) {
          lang = 'bash';
        } else if (code.startsWith('{') || code.startsWith('[')) {
          lang = 'json';
        } else if (code.includes('import ') || code.includes('def ')) {
          lang = 'python';
        }
        if (code) {
          codeExamples.push({ language: lang, code });
        }
      });

      // 获取主要文本内容（排除菜单部分）
      let contentText = rightCol.innerText;

      // 清理内容
      // 移除 "API Token 复制" 等无关内容
      contentText = contentText.replace(/API Token\s*复制\n?/g, '');
      contentText = contentText.replace(/按量付费：可用[\s\S]*?畅享版：可用\n?/g, '');

      return {
        breadcrumb: breadcrumbText,
        title: title,
        apiUrl: apiUrl,
        httpMethod: httpMethod,
        tables: tableData,
        codeExamples: codeExamples,
        content: contentText.trim()
      };
    });
  }

  /**
   * 遍历所有菜单并收集内容
   */
  async crawlAllPages(page) {
    const results = [];
    const visitedBreadcrumb = new Set();

    // 先展开所有菜单
    await this.expandAllMenus(page);

    // 获取所有菜单项
    const menuItems = await page.$$('.el-menu-item');

    for (let i = 0; i < menuItems.length; i++) {
      try {
        // 重新获取菜单项（DOM 可能已更新）
        const currentItems = await page.$$('.el-menu-item');
        if (i >= currentItems.length) continue;

        const item = currentItems[i];

        // 点击菜单项
        await item.click();
        await page.waitForTimeout(1000);

        // 获取内容
        const content = await this.extractPageContent(page);

        if (content && content.title && content.breadcrumb) {
          // 使用面包屑作为唯一标识
          const key = content.breadcrumb;

          if (!visitedBreadcrumb.has(key)) {
            visitedBreadcrumb.add(key);

            results.push({
              menuIndex: i,
              breadcrumb: content.breadcrumb,
              title: content.title,
              apiUrl: content.apiUrl,
              httpMethod: content.httpMethod,
              tables: content.tables,
              codeExamples: content.codeExamples,
              content: content.content
            });
          }
        }
      } catch (e) {
        console.error(`Error processing menu item ${i}:`, e.message);
      }
    }

    return results;
  }
}

export default TsanghiApiParser;