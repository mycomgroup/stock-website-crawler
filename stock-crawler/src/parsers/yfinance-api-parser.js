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
   * 清理标题，移除 Sphinx 文档中的 permalink 符号 (#)
   * @param {string} title - 原始标题
   * @returns {string} 清理后的标题
   */
  cleanTitle(title) {
    if (!title) return '';
    // 移除 Sphinx 文档标题末尾的 # 符号（permalink）
    return title.replace(/#+$/, '').trim();
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

      // 优先使用 apiName（从标题提取的类名/方法名）
      if (apiName) {
        // 保持原有的大小写和点号结构
        return apiName.replace(/[^a-zA-Z0-9._]/g, '');
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
          signature: '',
          parameters: [],
          returns: [],
          attributes: [],
          examples: [],
          codeExamples: [],
          notes: [],
          seeAlso: [],
          category: '',
          sidebarLinks: [],
          tables: [],
          rawContent: ''
        };

        // 提取主要内容区域 - PyData Sphinx Theme 优先
        const mainContent = document.querySelector('.bd-article, article.bd-article, .wy-nav-content, .document, main, article, .content');

        // 提取标题 - 优先从主内容区域获取 h1
        let h1 = null;
        if (mainContent) {
          h1 = mainContent.querySelector('h1');
        }
        // 如果主内容区域没有 h1，尝试从整个文档获取
        if (!h1) {
          h1 = document.querySelector('main h1, article h1, .bd-content h1, .wy-nav-content h1, h1');
        }
        if (h1) {
          let titleText = h1.textContent.trim();
          // 移除 Sphinx 文档标题末尾的 # 符号（permalink）
          titleText = titleText.replace(/#+$/, '').trim();
          result.title = titleText;

          // 从标题提取 API 名称 (如 yfinance.market, Ticker 等)
          const titleMatch = result.title.match(/^([a-zA-Z_]\w*(?:\.\w+)*)/);
          if (titleMatch) {
            result.apiName = titleMatch[1];
          }
        }

        // 提取侧边栏导航链接
        const sidebarLinks = document.querySelectorAll('.bd-sidebar a, .wy-menu-vertical a, .sidebar a, nav.bd-links a');
        sidebarLinks.forEach(link => {
          const href = link.getAttribute('href');
          if (href) {
            result.sidebarLinks.push({
              title: link.textContent.trim(),
              url: href.startsWith('http') ? href : `https://www.aidoczh.com${href}`
            });
          }
        });

        if (mainContent) {
          // 提取 API 签名（如 "Ticker.history(*args, **kwargs) → DataFrame"）
          const sigElement = mainContent.querySelector('.sig, dl.class > dt, dl.method > dt, dl.function > dt, dl.py-method > dt, dl.py-function > dt');
          if (sigElement) {
            let sig = sigElement.textContent.trim();
            // 移除末尾的 # 符号
            sig = sig.replace(/#+$/, '').trim();
            result.signature = sig;
          }

          // 提取描述（第一个有意义的段落）
          const paragraphs = mainContent.querySelectorAll('p');
          for (const p of paragraphs) {
            const text = p.textContent.trim();
            // 跳过空段落和太短的段落
            if (text.length > 10 && !text.startsWith('>>>') && !text.startsWith('Copy to clipboard')) {
              if (!result.description) {
                result.description = text;
              }
              // 收集其他段落作为示例说明
              if (text !== result.description && text.length > 20) {
                result.examples.push(text);
              }
            }
          }

          // 提取所有表格
          const tables = mainContent.querySelectorAll('table');
          tables.forEach((table, tableIndex) => {
            const headers = [];
            const rows = [];

            // 提取表头
            const headerCells = table.querySelectorAll('thead th, thead td');
            if (headerCells.length > 0) {
              headerCells.forEach(cell => {
                let headerText = cell.textContent.trim().toLowerCase();
                // 清理表头文本
                headerText = headerText.replace(/#+$/, '').trim();
                headers.push(headerText);
              });
            } else {
              // 尝试从第一行提取表头
              const firstRow = table.querySelector('tr');
              if (firstRow) {
                const cells = firstRow.querySelectorAll('th, td');
                cells.forEach(cell => {
                  let headerText = cell.textContent.trim().toLowerCase();
                  headerText = headerText.replace(/#+$/, '').trim();
                  headers.push(headerText);
                });
              }
            }

            // 提取数据行
            const bodyRows = table.querySelectorAll('tbody tr');
            const rowsToProcess = bodyRows.length > 0 ? bodyRows : table.querySelectorAll('tr');

            rowsToProcess.forEach((row, rowIndex) => {
              // 如果没有 tbody，跳过第一行（表头行）
              if (bodyRows.length === 0 && rowIndex === 0 && headers.length > 0) return;

              const cells = Array.from(row.querySelectorAll('td, th'));
              if (cells.length > 0) {
                const rowData = {};
                cells.forEach((cell, cellIndex) => {
                  const headerName = headers[cellIndex] || `col_${cellIndex}`;
                  let cellText = cell.textContent.trim();
                  // 清理单元格文本
                  cellText = cellText.replace(/#+$/, '').trim();
                  rowData[headerName] = cellText;
                });
                rows.push(rowData);
              }
            });

            // 存储表格信息
            if (headers.length > 0 || rows.length > 0) {
              result.tables.push({
                headers,
                rows,
                index: tableIndex
              });
            }

            // 判断表格类型并分配到相应字段
            const tableType = this.determineTableType(table, headers);
            if (tableType === 'parameters') {
              result.parameters = rows;
            } else if (tableType === 'returns') {
              result.returns = rows;
            } else if (tableType === 'attributes') {
              result.attributes = rows;
            }
          });

          // 提取代码示例 - PyData Sphinx Theme 使用 pre 标签
          const codeBlocks = mainContent.querySelectorAll('pre');
          codeBlocks.forEach(block => {
            const code = block.textContent.trim();
            // 过滤掉太短的代码和 "Copy to clipboard" 文本
            if (code.length > 10 && !code.includes('Copy to clipboard')) {
              let language = 'python';
              const classList = block.className || '';
              const langMatch = classList.match(/language-(\w+)/);
              if (langMatch) {
                language = langMatch[1];
              } else if (code.includes('import ') || code.includes('def ') || code.includes('class ')) {
                language = 'python';
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

          // 提取原始文本内容（作为备份）
          result.rawContent = mainContent.textContent.trim().substring(0, 5000);
        }

        return result;
      });

      // 清理标题
      const cleanTitle = this.cleanTitle(data.title);

      return {
        type: 'yfinance-api',
        url,
        pageType: this.extractPageType(url),
        title: cleanTitle,
        apiName: data.apiName,
        description: data.description,
        signature: data.signature,
        parameters: data.parameters,
        returns: data.returns,
        attributes: data.attributes,
        tables: data.tables,
        codeExamples: data.codeExamples,
        notes: data.notes,
        examples: data.examples,
        seeAlso: data.seeAlso,
        category: data.category,
        sidebarLinks: data.sidebarLinks,
        rawContent: data.rawContent,
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
        signature: '',
        parameters: [],
        returns: [],
        attributes: [],
        tables: [],
        codeExamples: [],
        notes: [],
        examples: [],
        seeAlso: [],
        category: '',
        sidebarLinks: [],
        rawContent: '',
        suggestedFilename: this.generateFilename(url)
      };
    }
  }

  /**
   * 判断表格类型
   * @param {Element} table - 表格元素
   * @param {string[]} headers - 表头列表
   * @returns {string} 表格类型
   */
  determineTableType(table, headers) {
    // 检查表头
    const headerText = headers.join(' ').toLowerCase();
    if (headerText.includes('参数') || headerText.includes('parameter') || headerText.includes('name') && headerText.includes('type')) {
      return 'parameters';
    }
    if (headerText.includes('返回') || headerText.includes('return') || headerText.includes('response')) {
      return 'returns';
    }
    if (headerText.includes('属性') || headerText.includes('attribute') || headerText.includes('field')) {
      return 'attributes';
    }

    // 检查表格前面的标题
    let prevElement = table.previousElementSibling;
    while (prevElement) {
      const text = prevElement.textContent.toLowerCase();
      if (text.includes('参数') || text.includes('parameter')) {
        return 'parameters';
      }
      if (text.includes('返回') || text.includes('return')) {
        return 'returns';
      }
      if (text.includes('属性') || text.includes('attribute')) {
        return 'attributes';
      }
      // 只检查最近的几个兄弟元素
      if (prevElement.tagName === 'H2' || prevElement.tagName === 'H3') {
        break;
      }
      prevElement = prevElement.previousElementSibling;
    }

    return 'unknown';
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
      // 确保我们在正确的页面上
      const currentUrl = page.url();
      const expectedBase = 'https://www.aidoczh.com/yfinance/reference/';

      // 如果当前 URL 不在 reference 目录，导航到正确页面
      if (!currentUrl.includes('/yfinance/reference/')) {
        console.log(`YFinance parser: redirecting from ${currentUrl} to reference/index.html`);
        await page.goto(expectedBase + 'index.html', {
          waitUntil: 'networkidle',
          timeout: 60000
        });
      }

      // 获取当前页面URL
      const finalUrl = page.url();
      console.log(`YFinance parser current page URL: ${finalUrl}`);

      // Sphinx 文档的侧边栏链接是相对于文档根目录的，不是相对于当前页面
      // 所以我们使用固定的 base URL
      const baseUrl = 'https://www.aidoczh.com/yfinance/reference/';
      console.log(`YFinance parser using baseUrl: ${baseUrl}`);

      const links = await page.evaluate((base) => {
        const foundLinks = [];
        const seenUrls = new Set();

        // 使用 URL 构造器正确解析相对路径
        const addLink = (href) => {
          if (!href || href.startsWith('#') || href.startsWith('javascript:')) return;

          try {
            // 使用 URL 构造器正确解析相对路径
            const fullUrl = new URL(href, base).href;

            // 过滤只保留 yfinance 相关链接，排除静态资源
            if (fullUrl.includes('/yfinance/') &&
                !seenUrls.has(fullUrl) &&
                !fullUrl.match(/\.(png|jpg|jpeg|gif|svg|css|js|ico|woff|woff2|ttf|eot|py|pyc|txt|pdf|zip)$/i) &&
                !fullUrl.includes('_static/') &&
                !fullUrl.includes('_sources/') &&
                !fullUrl.includes('#')) {
              seenUrls.add(fullUrl);
              foundLinks.push(fullUrl);
            }
          } catch (e) {
            // URL 解析失败，跳过
          }
        };

        // 主要侧边栏选择器 - PyData Sphinx Theme
        const sidebarSelectors = [
          '.bd-sidebar a',
          '.wy-menu-vertical a',
          '.wy-menu a',
          '.sidebar a',
          'nav.bd-links a',
          '.nav.bd-links a'
        ];

        // 从侧边栏提取链接
        for (const selector of sidebarSelectors) {
          document.querySelectorAll(selector).forEach(link => {
            addLink(link.getAttribute('href'));
          });
        }

        return foundLinks;
      }, baseUrl);

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
      // 等待 PyData Sphinx Theme 的主内容区域
      await page.waitForSelector('.bd-article, h1, .wy-nav-content, main, article', { timeout: 15000 });
      await page.waitForTimeout(2000);
    } catch (error) {
      console.warn('Wait for content timeout, proceeding anyway:', error.message);
    }
  }
}

export default YfinanceApiParser;