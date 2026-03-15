import BaseParser from './base-parser.js';

/**
 * YFinance API Parser - 专门解析 yfinance API 文档页面
 * YFinance 是一个用于获取 Yahoo Finance 数据的 Python 库
 * URL 格式: https://www.aidoczh.com/yfinance/...
 */
class YfinanceApiParser extends BaseParser {
  /**
   * 匹配 YFinance API 文档页面
   * @param {string} url - 页面URL
   * @returns {boolean} 是否匹配
   */
  matches(url) {
    return /^https?:\/\/www\.aidoczh\.com\/yfinance\//.test(url);
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
   * @param {string} apiName - API 名称
   * @returns {string} 文件名
   */
  generateFilename(url, apiName = '') {
    try {
      const urlObj = new URL(url);
      const pathParts = urlObj.pathname.split('/').filter(p => p);

      if (apiName) {
        const safeName = apiName
          .toLowerCase()
          .replace(/[^a-z0-9_]/g, '_')
          .replace(/_+/g, '_')
          .replace(/^_|_$/g, '');
        return safeName;
      }

      // 从路径生成文件名
      if (pathParts.length > 1) {
        const lastPart = pathParts[pathParts.length - 1].replace('.html', '');
        return lastPart;
      }

      return 'yfinance_doc';
    } catch (e) {
      return 'yfinance_doc';
    }
  }

  /**
   * 从 URL 提取页面类型
   * @param {string} url - 页面URL
   * @returns {string} 页面类型
   */
  extractPageType(url) {
    try {
      const urlObj = new URL(url);
      const pathname = urlObj.pathname;

      if (pathname.includes('/reference/')) return 'reference';
      if (pathname.includes('/tutorial/')) return 'tutorial';
      if (pathname.includes('/guide/')) return 'guide';

      return 'doc';
    } catch (e) {
      return 'doc';
    }
  }

  /**
   * 解析 YFinance API 文档页面
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
          parameters: [],
          returns: [],
          attributes: [],
          examples: [],
          codeExamples: [],
          notes: [],
          seeAlso: [],
          category: '',
          sidebarLinks: [],
          rawContent: ''
        };

        // 提取标题
        const h1 = document.querySelector('h1');
        if (h1) {
          result.title = h1.textContent.trim();
          // 从标题提取 API 名称
          const titleMatch = result.title.match(/^(\w+(?:\.\w+)*)/);
          if (titleMatch) {
            result.apiName = titleMatch[1];
          }
        }

        // 提取侧边栏导航链接
        const sidebarLinks = document.querySelectorAll('.wy-menu-vertical a, .sidebar a, nav a');
        sidebarLinks.forEach(link => {
          const href = link.getAttribute('href');
          if (href) {
            result.sidebarLinks.push({
              title: link.textContent.trim(),
              url: href.startsWith('http') ? href : `https://www.aidoczh.com${href}`
            });
          }
        });

        // 提取主要内容区域
        const mainContent = document.querySelector('.wy-nav-content, .document, main, article, .content');

        if (mainContent) {
          // 提取描述（第一个段落）
          const firstParagraph = mainContent.querySelector('p');
          if (firstParagraph) {
            result.description = firstParagraph.textContent.trim();
          }

          // 提取参数表格
          const tables = mainContent.querySelectorAll('table');
          tables.forEach(table => {
            const headers = [];
            const rows = [];

            // 提取表头
            const headerCells = table.querySelectorAll('thead th, thead td');
            if (headerCells.length > 0) {
              headerCells.forEach(cell => headers.push(cell.textContent.trim().toLowerCase()));
            } else {
              const firstRow = table.querySelector('tr');
              if (firstRow) {
                const cells = firstRow.querySelectorAll('th, td');
                cells.forEach(cell => headers.push(cell.textContent.trim().toLowerCase()));
              }
            }

            // 判断表格类型
            let tableType = 'unknown';
            const prevHeading = table.previousElementSibling;
            if (prevHeading) {
              const prevText = prevHeading.textContent.toLowerCase();
              if (prevText.includes('参数') || prevText.includes('parameter')) {
                tableType = 'parameters';
              } else if (prevText.includes('返回') || prevText.includes('return')) {
                tableType = 'returns';
              } else if (prevText.includes('属性') || prevText.includes('attribute')) {
                tableType = 'attributes';
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

            // 根据类型存储
            if (tableType === 'parameters') {
              result.parameters = rows;
            } else if (tableType === 'returns') {
              result.returns = rows;
            } else if (tableType === 'attributes') {
              result.attributes = rows;
            }
          });

          // 提取代码示例
          const codeBlocks = mainContent.querySelectorAll('pre code, pre');
          codeBlocks.forEach(block => {
            const code = block.textContent.trim();
            if (code.length > 10) {
              let language = 'python';
              const classList = block.className || '';
              const langMatch = classList.match(/language-(\w+)/);
              if (langMatch) {
                language = langMatch[1];
              }

              result.codeExamples.push({
                language,
                code
              });
            }
          });

          // 提取注意事项
          const notes = mainContent.querySelectorAll('.admonition, .note, .warning, .attention');
          notes.forEach(note => {
            const titleEl = note.querySelector('.admonition-title, .title');
            const title = titleEl ? titleEl.textContent.trim() : 'Note';
            const content = note.textContent.replace(title, '').trim();
            result.notes.push({
              type: title.toLowerCase(),
              content
            });
          });

          // 提取段落内容
          const paragraphs = mainContent.querySelectorAll('p');
          paragraphs.forEach((p, index) => {
            const text = p.textContent.trim();
            if (index > 0 && text.length > 20 && !text.startsWith('>>>')) {
              result.examples.push(text);
            }
          });

          // 提取 "See Also" 部分
          const seeAlsoSection = mainContent.querySelector('.see-also, #see-also');
          if (seeAlsoSection) {
            const links = seeAlsoSection.querySelectorAll('a');
            links.forEach(link => {
              result.seeAlso.push({
                title: link.textContent.trim(),
                url: link.getAttribute('href')
              });
            });
          }
        }

        return result;
      });

      return {
        type: 'yfinance-api',
        url,
        pageType: this.extractPageType(url),
        title: data.title,
        apiName: data.apiName,
        description: data.description,
        parameters: data.parameters,
        returns: data.returns,
        attributes: data.attributes,
        codeExamples: data.codeExamples,
        notes: data.notes,
        examples: data.examples,
        seeAlso: data.seeAlso,
        category: data.category,
        sidebarLinks: data.sidebarLinks,
        suggestedFilename: this.generateFilename(url, data.apiName)
      };
    } catch (error) {
      console.error('Failed to parse YFinance API doc page:', error.message);
      return {
        type: 'yfinance-api',
        url,
        pageType: this.extractPageType(url),
        title: '',
        apiName: '',
        description: '',
        parameters: [],
        returns: [],
        attributes: [],
        codeExamples: [],
        notes: [],
        examples: [],
        seeAlso: [],
        category: '',
        sidebarLinks: [],
        suggestedFilename: this.generateFilename(url)
      };
    }
  }

  /**
   * 是否支持链接发现
   * @returns {boolean}
   */
  supportsLinkDiscovery() {
    return true;
  }

  /**
   * 从 Sphinx 文档侧边栏发现链接
   * @param {Page} page - Playwright页面对象
   * @returns {Promise<Array<string>>} 发现的链接列表
   */
  async discoverLinks(page) {
    try {
      // 首先展开所有折叠内容
      await this.expandSidebar(page);

      const links = await page.evaluate(() => {
        const foundLinks = [];
        const seenUrls = new Set();

        // 提取所有 yfinance 相关链接的通用函数
        const addLink = (href) => {
          if (!href || href.startsWith('#') || href.startsWith('javascript:')) return;

          let fullUrl = href;
          if (href.startsWith('/')) {
            fullUrl = `https://www.aidoczh.com${href}`;
          } else if (!href.startsWith('http')) {
            // 相对路径
            fullUrl = `https://www.aidoczh.com/yfinance/${href}`;
          }

          // 过滤只保留 yfinance 相关链接，排除静态资源
          if (fullUrl.includes('/yfinance/') &&
              !seenUrls.has(fullUrl) &&
              !fullUrl.match(/\.(png|jpg|jpeg|gif|svg|css|js|ico|woff|woff2|ttf|eot)$/i) &&
              !fullUrl.includes('_static/') &&
              !fullUrl.includes('_sources/')) {
            seenUrls.add(fullUrl);
            foundLinks.push(fullUrl);
          }
        };

        // 提取所有 a 标签
        document.querySelectorAll('a[href]').forEach(link => {
          addLink(link.getAttribute('href'));
        });

        // 特定选择器 - Sphinx 文档侧边栏
        const selectors = [
          '.wy-menu-vertical a',
          '.wy-menu a',
          '.sidebar a',
          'nav a',
          '.toctree-wrapper a',
          '.local-toc a',
          '#bd-docs-nav a',
          '.bd-sidebar a',
          '.nav-links a',
          // PyData Sphinx Theme 选择器
          '.bd-links a',
          '.nav.bd-links a',
          // 内容区域的目录
          '.contents a',
          '.toctree a',
          // API 参考链接
          '.api a',
          '.reference a',
          'dt a',
          'code a'
        ];

        for (const selector of selectors) {
          document.querySelectorAll(selector).forEach(link => {
            addLink(link.getAttribute('href'));
          });
        }

        return foundLinks;
      });

      console.log(`YFinance parser discovered ${links.length} links`);
      return links;
    } catch (error) {
      console.error('Failed to discover links:', error.message);
      return [];
    }
  }

  /**
   * 展开侧边栏折叠内容
   * @param {Page} page - Playwright页面对象
   */
  async expandSidebar(page) {
    try {
      // 滚动侧边栏以显示更多链接
      await page.evaluate(() => {
        const sidebar = document.querySelector('.wy-menu-vertical, .wy-side-scroll, .sidebar, nav');
        if (sidebar) {
          // 滚动到底部再回到顶部
          sidebar.scrollTop = sidebar.scrollHeight;
          setTimeout(() => {
            sidebar.scrollTop = 0;
          }, 500);
        }
      });

      await page.waitForTimeout(1000);

      // 展开 details 元素
      await page.evaluate(() => {
        // 展开 details 元素
        document.querySelectorAll('details').forEach(detail => {
          detail.open = true;
        });

        // 点击 Sphinx 章节展开按钮 (通常是包含 caption 的元素)
        document.querySelectorAll('.wy-menu-vertical .caption, .wy-menu-vertical .toctree-l1 > a').forEach(el => {
          try {
            el.click();
          } catch (_) {}
        });

        // 点击可能有子菜单的项目
        document.querySelectorAll('.wy-menu-vertical li').forEach(li => {
          if (li.querySelector('ul')) {
            const link = li.querySelector('a');
            if (link) {
              try {
                link.click();
              } catch (_) {}
            }
          }
        });

        // PyData Sphinx Theme 的展开
        document.querySelectorAll('.bd-links .nav-link, .nav.bd-links a').forEach(el => {
          try {
            el.click();
          } catch (_) {}
        });
      });

      await page.waitForTimeout(1500);

      // 再次滚动侧边栏
      await page.evaluate(() => {
        const sidebar = document.querySelector('.wy-menu-vertical, .wy-side-scroll');
        if (sidebar) {
          // 逐步滚动
          let scrollPos = 0;
          const scrollStep = 200;
          const interval = setInterval(() => {
            scrollPos += scrollStep;
            sidebar.scrollTop = scrollPos;
            if (scrollPos >= sidebar.scrollHeight) {
              clearInterval(interval);
            }
          }, 200);

          // 3秒后停止
          setTimeout(() => clearInterval(interval), 3000);
        }
      });

      await page.waitForTimeout(3500);
    } catch (error) {
      console.warn('Failed to expand sidebar:', error.message);
    }
  }

  /**
   * 等待页面内容加载完成
   */
  async waitForContent(page) {
    try {
      await page.waitForLoadState('domcontentloaded', { timeout: 30000 });
      await page.waitForSelector('h1, .wy-nav-content, main, article', { timeout: 15000 });
      await page.waitForTimeout(2000);
    } catch (error) {
      console.warn('Wait for content timeout, proceeding anyway:', error.message);
    }
  }
}

export default YfinanceApiParser;