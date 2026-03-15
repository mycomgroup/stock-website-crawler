import BaseParser from './base-parser.js';

/**
 * Tushare Pro API Parser - 专门解析 tushare.pro/document 文档页面
 * Tushare Pro 提供中国股票、期货、期权、基金等金融数据 API
 * URL 格式: https://tushare.pro/document/2?doc_id=XXX
 */
class TushareProApiParser extends BaseParser {
  /**
   * 匹配 Tushare Pro API 文档页面
   * @param {string} url - 页面URL
   * @returns {boolean} 是否匹配
   */
  matches(url) {
    return /^https?:\/\/tushare\.pro\/document\//.test(url);
  }

  /**
   * 获取优先级
   * @returns {number} 优先级
   */
  getPriority() {
    return 100;
  }

  /**
   * 根据 URL 生成有意义的文件名
   * @param {string} url - 页面URL
   * @returns {string} 文件名
   */
  generateFilename(url, apiName = '') {
    try {
      const urlObj = new URL(url);
      const docId = urlObj.searchParams.get('doc_id');
      if (apiName) {
        // 清理 API 名称，生成安全的文件名
        const safeName = apiName
          .toLowerCase()
          .replace(/[^a-z0-9_\u4e00-\u9fa5]/g, '_')
          .replace(/_+/g, '_')
          .replace(/^_|_$/g, '');
        return `${safeName}_${docId}`;
      }
      return `doc_${docId}`;
    } catch (e) {
      return 'tushare_doc';
    }
  }

  /**
   * 从 URL 提取文档 ID
   * @param {string} url - 页面URL
   * @returns {string} 文档 ID
   */
  extractDocId(url) {
    try {
      const urlObj = new URL(url);
      return urlObj.searchParams.get('doc_id') || '';
    } catch (e) {
      return '';
    }
  }

  /**
   * 从 URL 提取文档类型
   * @param {string} url - 页面URL
   * @returns {string} 文档类型 (如 '1' = 平台介绍, '2' = 数据接口)
   */
  extractDocType(url) {
    try {
      const urlObj = new URL(url);
      const pathParts = urlObj.pathname.split('/').filter(p => p);
      return pathParts[1] || '2';
    } catch (e) {
      return '2';
    }
  }

  /**
   * 解析 Tushare Pro API 文档页面
   * @param {Page} page - Playwright页面对象
   * @param {string} url - 页面URL
   * @param {Object} options - 解析选项
   * @returns {Promise<Object>} 解析后的页面数据
   */
  async parse(page, url, options = {}) {
    try {
      // 等待页面加载完成
      await this.waitForContent(page);

      // 从页面提取内容
      const data = await page.evaluate(() => {
        const result = {
          title: '',
          apiName: '',
          description: '',
          pointsRequired: '',
          inputParams: [],
          outputParams: [],
          codeExample: '',
          dataExample: '',
          category: '',
          paragraphs: [],
          lists: [],
          links: [],
          rawContent: '',
          sidebarLinks: []
        };

        // 提取标题 (h2)
        const h2 = document.querySelector('.content h2');
        if (h2) {
          result.title = h2.textContent.trim();
        }

        // 提取侧边栏导航链接
        const sidebarLinks = document.querySelectorAll('#jstree a');
        sidebarLinks.forEach(link => {
          const href = link.getAttribute('href');
          if (href && href.includes('doc_id=')) {
            result.sidebarLinks.push({
              title: link.textContent.trim(),
              url: href.startsWith('http') ? href : `https://tushare.pro${href}`
            });
          }
        });

        // 提取当前页面的分类路径（从侧边栏 active 状态）
        const activeItems = document.querySelectorAll('#jstree .active');
        const categoryPath = [];
        activeItems.forEach(item => {
          const link = item.querySelector('a');
          if (link) {
            categoryPath.push(link.textContent.trim());
          }
        });
        result.category = categoryPath.join(' > ');

        // 提取接口信息（接口、描述、积分等）
        const content = document.querySelector('.content');
        if (content) {
          const paragraphs = content.querySelectorAll('p');
          paragraphs.forEach(p => {
            const text = p.textContent.trim();

            // 提取接口名
            if (text.startsWith('接口：') || text.includes('接口：')) {
              const match = text.match(/接口[：:]\s*(\w+)/);
              if (match) {
                result.apiName = match[1];
              }
            }

            // 提取描述
            if (text.startsWith('描述：') || text.includes('描述：')) {
              const match = text.match(/描述[：:]\s*(.+)/);
              if (match) {
                result.description = match[1].trim();
              }
            }

            // 提取积分要求
            if (text.includes('积分')) {
              const pointsMatch = text.match(/至少\s*(\d+)\s*积分/);
              if (pointsMatch) {
                result.pointsRequired = pointsMatch[1];
              }
            }
          });

          // 提取段落内容（用于分类页面）
          const allParagraphs = content.querySelectorAll('p');
          allParagraphs.forEach(p => {
            const text = p.textContent.trim();
            // 跳过接口、描述、积分等已处理的段落
            if (text.startsWith('接口：') || text.startsWith('描述：') || text.includes('积分：')) {
              return;
            }
            // 跳过太短的段落
            if (text.length < 10) return;
            // 跳过空段落或只有换行的段落
            if (text === '<br>' || text === '') return;
            // 跳过只包含链接且文字很短的段落（导航性链接）
            const links = p.querySelectorAll('a');
            if (links.length > 0 && text.length < 30 && !text.includes('，')) {
              return;
            }
            result.paragraphs.push(text);
          });

          // 提取列表（用于分类页面）
          const allLists = content.querySelectorAll('ul, ol');
          allLists.forEach(list => {
            const items = [];
            list.querySelectorAll('li').forEach(li => {
              const text = li.textContent.trim();
              const link = li.querySelector('a');
              if (link) {
                const href = link.getAttribute('href');
                items.push({
                  text: text,
                  link: href ? (href.startsWith('http') ? href : `https://tushare.pro${href}`) : null
                });
              } else {
                items.push({ text: text, link: null });
              }
            });
            if (items.length > 0) {
              result.lists.push({
                type: list.tagName.toLowerCase(),
                items: items
              });
            }
          });

          // 提取表格 - 输入参数和输出参数
          const tables = content.querySelectorAll('table');
          let foundInputParams = false;

          tables.forEach((table, index) => {
            const headers = [];
            const rows = [];

            // 提取表头
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
            const bodyRows = table.querySelectorAll('tbody tr');
            const rowsToProcess = bodyRows.length > 0 ? bodyRows : table.querySelectorAll('tr');

            rowsToProcess.forEach((row, rowIndex) => {
              if (rowIndex === 0 && bodyRows.length === 0 && headers.length > 0) return;

              const cells = Array.from(row.querySelectorAll('td, th'));
              if (cells.length > 0) {
                const rowData = {};
                cells.forEach((cell, cellIndex) => {
                  const headerName = headers[cellIndex] || `col_${cellIndex}`;
                  rowData[headerName] = cell.textContent.trim();
                });
                rows.push(rowData);
              }
            });

            // 根据表格前的文字判断是输入参数还是输出参数
            // 查找表格前最近的段落标题
            let tableType = 'unknown';
            let prevElement = table.previousElementSibling;
            while (prevElement) {
              const prevText = prevElement.textContent.trim();
              if (prevText.includes('输入参数')) {
                tableType = 'input';
                break;
              } else if (prevText.includes('输出参数')) {
                tableType = 'output';
                break;
              }
              prevElement = prevElement.previousElementSibling;
            }

            const tableData = { headers, rows };

            if (tableType === 'input') {
              result.inputParams = rows;
            } else if (tableType === 'output') {
              result.outputParams = rows;
            }
          });

          // 提取代码示例 - 根据前面的标题判断类型
          const codeBlocks = content.querySelectorAll('.codehilite pre, pre code, pre');
          const interfaceExamples = [];
          const dataExamples = [];

          codeBlocks.forEach((block, index) => {
            const code = block.textContent.trim();
            if (code.length < 20) return;

            // 查找代码块前最近的标题
            let prevElement = block.closest('.codehilite')?.previousElementSibling || block.previousElementSibling;
            let blockTitle = '';
            while (prevElement) {
              const text = prevElement.textContent.trim();
              if (text.includes('接口示例')) {
                blockTitle = 'interface';
                break;
              } else if (text.includes('数据示例')) {
                blockTitle = 'data';
                break;
              }
              prevElement = prevElement.previousElementSibling;
            }

            // 判断代码类型
            if (blockTitle === 'interface' || code.includes('pro = ts.pro_api') || code.includes("pro.query(")) {
              // 接口示例
              interfaceExamples.push(code);
            } else if (blockTitle === 'data' || code.match(/^\s*ts_code\s+/m) || code.match(/^\s*\d+\s+/m)) {
              // 数据示例 - 以 ts_code 或数字开头
              dataExamples.push(code);
            } else if (index < codeBlocks.length / 2) {
              // 前半部分的代码块更可能是接口示例
              interfaceExamples.push(code);
            } else {
              // 后半部分的代码块更可能是数据示例
              dataExamples.push(code);
            }
          });

          // 去重
          const uniqueInterface = [...new Set(interfaceExamples)];
          const uniqueData = [...new Set(dataExamples)];

          result.codeExample = uniqueInterface.join('\n\n');
          result.dataExample = uniqueData.join('\n\n');
        }

        return result;
      });

      return {
        type: 'tushare-pro-api',
        url,
        docId: this.extractDocId(url),
        docType: this.extractDocType(url),
        title: data.title,
        apiName: data.apiName,
        description: data.description,
        pointsRequired: data.pointsRequired,
        category: data.category,
        inputParams: data.inputParams,
        outputParams: data.outputParams,
        codeExample: data.codeExample,
        dataExample: data.dataExample,
        paragraphs: data.paragraphs,
        lists: data.lists,
        sidebarLinks: data.sidebarLinks,
        suggestedFilename: this.generateFilename(url, data.apiName)
      };
    } catch (error) {
      console.error('Failed to parse Tushare Pro API doc page:', error.message);
      return {
        type: 'tushare-pro-api',
        url,
        docId: this.extractDocId(url),
        docType: this.extractDocType(url),
        title: '',
        apiName: '',
        description: '',
        pointsRequired: '',
        category: '',
        inputParams: [],
        outputParams: [],
        codeExample: '',
        dataExample: '',
        paragraphs: [],
        lists: [],
        sidebarLinks: [],
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
      await page.waitForSelector('.content h2, .content table', { timeout: 15000 });
      await page.waitForTimeout(1000);
    } catch (error) {
      console.warn('Wait for content timeout, proceeding anyway:', error.message);
    }
  }
}

export default TushareProApiParser;