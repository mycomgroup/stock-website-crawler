/**
 * Base Parser - 所有解析器的基类
 */
class BaseParser {
  /**
   * 检查此解析器是否适用于给定的URL
   * @param {string} url - 页面URL
   * @returns {boolean} 是否匹配
   */
  matches(url) {
    throw new Error('matches() must be implemented by subclass');
  }

  /**
   * 解析页面内容
   * @param {Page} page - Playwright页面对象
   * @param {string} url - 页面URL
   * @param {Object} options - 解析选项
   * @returns {Promise<Object>} 解析后的页面数据
   */
  async parse(page, url, options = {}) {
    throw new Error('parse() must be implemented by subclass');
  }

  /**
   * 获取解析器优先级（数字越大优先级越高）
   * @returns {number} 优先级
   */
  getPriority() {
    return 0;
  }

  /**
   * 提取页面标题
   * @param {Page} page - Playwright页面对象
   * @returns {Promise<string>} 标题
   */
  async extractTitle(page) {
    try {
      const title = await page.evaluate(() => {
        const h1 = document.querySelector('h1');
        if (h1) return h1.textContent.trim();

        const h2 = document.querySelector('h2');
        if (h2) return h2.textContent.trim();

        const title = document.querySelector('title');
        if (title) return title.textContent.trim();

        return '';
      });
      return title;
    } catch (error) {
      return '';
    }
  }

  /**
   * 提取所有表格
   * @param {Page} page - Playwright页面对象
   * @returns {Promise<Array>} 表格数组
   */
  async extractTables(page) {
    try {
      const tables = await page.evaluate(() => {
        const tableElements = Array.from(document.querySelectorAll('table'));
        return tableElements.map((table, index) => {
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
            if (rowIndex === 0 && bodyRows.length === 0 && headers.length > 0) return;
            
            const cells = Array.from(row.querySelectorAll('td, th'));
            if (cells.length > 0) {
              const rowData = cells.map(cell => cell.textContent.trim());
              rows.push(rowData);
            }
          });

          return { 
            index,
            headers, 
            rows,
            caption: table.querySelector('caption')?.textContent.trim() || ''
          };
        });
      });
      return tables;
    } catch (error) {
      console.error('Failed to extract tables:', error.message);
      return [];
    }
  }

  /**
   * 提取代码块
   * @param {Page} page - Playwright页面对象
   * @returns {Promise<Array>} 代码块数组
   */
  async extractCodeBlocks(page) {
    try {
      const codeBlocks = await page.evaluate(() => {
        const blocks = [];

        const preCodeElements = document.querySelectorAll('pre code, pre');
        preCodeElements.forEach(element => {
          const code = element.textContent.trim();
          if (code) {
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

        const textareas = document.querySelectorAll('textarea[readonly]');
        textareas.forEach(textarea => {
          const code = textarea.value.trim();
          if (code) {
            let language = 'text';
            if (code.startsWith('{') || code.startsWith('[')) {
              language = 'json';
            } else if (code.startsWith('<')) {
              language = 'xml';
            }
            blocks.push({ language, code });
          }
        });

        return blocks;
      });
      return codeBlocks;
    } catch (error) {
      console.error('Failed to extract code blocks:', error.message);
      return [];
    }
  }
}

export default BaseParser;
