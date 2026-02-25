import BaseParser from './base-parser.js';

/**
 * Generic Parser - 通用页面解析器
 * 作为fallback，匹配所有页面
 */
class GenericParser extends BaseParser {
  /**
   * 匹配所有页面
   * @param {string} url - 页面URL
   * @returns {boolean} 总是返回true
   */
  matches(url) {
    return true;
  }

  /**
   * 获取优先级（最低）
   * @returns {number} 优先级
   */
  getPriority() {
    return 0;
  }

  /**
   * 解析通用页面
   * @param {Page} page - Playwright页面对象
   * @param {string} url - 页面URL
   * @param {Object} options - 解析选项
   * @param {Function} options.onDataChunk - 数据块回调函数
   * @param {string} options.filepath - 输出文件路径
   * @returns {Promise<Object>} 解析后的页面数据
   */
  async parse(page, url, options = {}) {
    try {
      // 设置API响应拦截
      const apiData = [];
      page.on('response', async (response) => {
        const responseUrl = response.url();
        const status = response.status();
        
        // 拦截可能包含数据的API调用
        if ((responseUrl.includes('/api/') || responseUrl.includes('/data/') || responseUrl.includes('/query/')) && status === 200) {
          try {
            const contentType = response.headers()['content-type'] || '';
            
            if (contentType.includes('json')) {
              const data = await response.json();
              
              // 保存数组类型的数据
              if (Array.isArray(data) && data.length > 0) {
                apiData.push({
                  url: responseUrl,
                  data: data
                });
              } else if (data && typeof data === 'object') {
                // 检查对象中是否有数组字段
                for (const key of Object.keys(data)) {
                  if (Array.isArray(data[key]) && data[key].length > 0) {
                    apiData.push({
                      url: responseUrl,
                      data: data[key],
                      field: key
                    });
                  }
                }
              }
            }
          } catch (e) {
            // 忽略解析错误
          }
        }
      });
      
      const title = await this.extractTitle(page);
      const description = await this.extractDescription(page);
      const headings = await this.extractHeadings(page);
      
      // 先提取初始数据
      const initialParagraphs = await this.extractParagraphs(page);
      const initialLists = await this.extractLists(page);
      const initialCodeBlocks = await this.extractCodeBlocks(page);
      const initialImages = await this.extractImages(page, options.filepath, options.pagesDir);
      const blockquotes = await this.extractBlockquotes(page);
      const definitionLists = await this.extractDefinitionLists(page);
      const horizontalRules = await this.extractHorizontalRules(page);
      const videos = await this.extractVideos(page);
      const audios = await this.extractAudios(page);
      
      // 提取并保存图表（Canvas/SVG）
      const charts = await this.extractAndSaveCharts(page, options.filepath, options.pagesDir);
      
      // 1. 先点击所有"更多/展开"按钮，展开折叠内容
      await this.clickAllExpandButtons(page);
      
      // 2. 处理无限滚动加载更多内容（优化版）
      await this.handleInfiniteScrollEnhanced(page);
      
      // 3. 提取运行时图表数据（ECharts/Highcharts）
      const chartData = await this.extractChartData(page);
      
      // 提取主内容区域的混排内容（段落、图片、列表等按原始顺序）
      const mainContent = await this.extractMainContentWithOrder(page, options.filepath, options.pagesDir);
      
      // 提取表格（支持分页和虚拟表格）
      const tables = await this.extractTablesWithPaginationAndVirtual(page, options.onDataChunk);
      
      // 尝试提取Tab页和下拉框内容（会检测数据变化）
      const tabsAndDropdowns = await this.extractTabsAndDropdowns(page, options.filepath, options.onDataChunk);

      // 尝试处理时间筛选（如果页面有时间筛选控件）
      const dateFilters = await this.findAndProcessDateFilters(page, options.filepath, options.onDataChunk);

      // 如果没有提取到表格，但有API数据，尝试从API数据生成表格
      if (tables.length === 0 && apiData.length > 0) {
        const apiTables = await this.convertAPIDataToTables(apiData, options.onDataChunk);
        tables.push(...apiTables);
      }

      return {
        type: 'generic',
        url,
        title,
        description,
        headings,
        mainContent, // 新增：按顺序的混排内容
        paragraphs: initialParagraphs,
        lists: initialLists,
        tables,
        codeBlocks: initialCodeBlocks,
        images: initialImages,
        charts,
        chartData, // 新增：运行时图表数据
        blockquotes,
        definitionLists,
        horizontalRules,
        videos,
        audios,
        tabsAndDropdowns,
        dateFilters,
        apiData: apiData.length
      };
    } catch (error) {
      console.error('Failed to parse generic page:', error.message);
      return {
        type: 'generic',
        url,
        title: '',
        description: '',
        headings: [],
        paragraphs: [],
        lists: [],
        tables: [],
        codeBlocks: [],
        images: [],
        charts: [],
        tabsAndDropdowns: [],
        dateFilters: [],
        apiData: 0
      };
    }
  }

  /**
   * 提取页面描述
   * @param {Page} page - Playwright页面对象
   * @returns {Promise<string>} 描述
   */
  async extractDescription(page) {
    try {
      const description = await page.evaluate(() => {
        const meta = document.querySelector('meta[name="description"]');
        if (meta) return meta.getAttribute('content') || '';

        const ogDesc = document.querySelector('meta[property="og:description"]');
        if (ogDesc) return ogDesc.getAttribute('content') || '';

        return '';
      });
      return description;
    } catch (error) {
      return '';
    }
  }

  /**
   * 提取所有标题
   * @param {Page} page - Playwright页面对象
   * @returns {Promise<Array>} 标题数组
   */
  async extractHeadings(page) {
    try {
      const headings = await page.evaluate(() => {
        const headingElements = document.querySelectorAll('h1, h2, h3, h4, h5, h6');
        return Array.from(headingElements).map(h => {
          // 提取标题中的文本和链接
          let text = '';
          const processNode = (node) => {
            if (node.nodeType === Node.TEXT_NODE) {
              text += node.textContent;
            } else if (node.nodeType === Node.ELEMENT_NODE) {
              if (node.tagName === 'A' && node.href) {
                const linkText = node.textContent.trim();
                const href = node.href;
                if (linkText && href) {
                  text += `[${linkText}](${href})`;
                }
              } else {
                // 递归处理子节点
                Array.from(node.childNodes).forEach(processNode);
              }
            }
          };
          
          Array.from(h.childNodes).forEach(processNode);
          
          return {
            level: parseInt(h.tagName.substring(1)),
            text: text.trim()
          };
        });
      });
      return headings;
    } catch (error) {
      return [];
    }
  }

  /**
   * 提取段落（支持格式化文本）
   * @param {Page} page - Playwright页面对象
   * @returns {Promise<Array>} 段落数组
   */
  async extractParagraphs(page) {
    try {
      const paragraphs = await page.evaluate(() => {
        const main = document.querySelector('main') || 
                     document.querySelector('article') || 
                     document.querySelector('[role="main"]') ||
                     document.querySelector('#content') ||
                     document.body;
        
        const pElements = main.querySelectorAll('p');
        
        // 处理节点，保留格式
        const processNode = (node) => {
          let result = '';
          
          if (node.nodeType === Node.TEXT_NODE) {
            result += node.textContent;
          } else if (node.nodeType === Node.ELEMENT_NODE) {
            const tag = node.tagName;
            const text = node.textContent.trim();
            
            if (tag === 'A' && node.href) {
              result += `[${text}](${node.href})`;
            } else if ((tag === 'STRONG' || tag === 'B') && text) {
              result += `**${text}**`;
            } else if ((tag === 'EM' || tag === 'I') && text) {
              result += `*${text}*`;
            } else if ((tag === 'DEL' || tag === 'S' || tag === 'STRIKE') && text) {
              result += `~~${text}~~`;
            } else if (tag === 'CODE' && text) {
              result += `\`${text}\``;
            } else if (tag === 'SUP' && text) {
              result += `^${text}^`;
            } else if (tag === 'SUB' && text) {
              result += `~${text}~`;
            } else if (tag === 'BR') {
              result += '  \n'; // Markdown换行
            } else {
              // 递归处理子节点
              Array.from(node.childNodes).forEach(child => {
                result += processNode(child);
              });
            }
          }
          
          return result;
        };
        
        return Array.from(pElements)
          .map(p => {
            let result = '';
            Array.from(p.childNodes).forEach(node => {
              result += processNode(node);
            });
            return result.trim();
          })
          .filter(text => text.length > 0);
      });
      return paragraphs;
    } catch (error) {
      return [];
    }
  }

  /**
   * 提取列表
   * @param {Page} page - Playwright页面对象
   * @returns {Promise<Array>} 列表数组
   */
  async extractLists(page) {
    try {
      const lists = await page.evaluate(() => {
        const listElements = document.querySelectorAll('ul, ol');
        return Array.from(listElements).map(list => {
          const items = Array.from(list.querySelectorAll('li')).map(li => {
            // 提取列表项中的文本和链接
            let result = '';
            const processNode = (node) => {
              if (node.nodeType === Node.TEXT_NODE) {
                result += node.textContent;
              } else if (node.nodeType === Node.ELEMENT_NODE) {
                if (node.tagName === 'A' && node.href) {
                  const text = node.textContent.trim();
                  const href = node.href;
                  if (text && href) {
                    result += `[${text}](${href})`;
                  }
                } else {
                  // 递归处理子节点
                  Array.from(node.childNodes).forEach(processNode);
                }
              }
            };
            
            Array.from(li.childNodes).forEach(processNode);
            return result.trim();
          });
          
          return {
            type: list.tagName.toLowerCase(),
            items: items.filter(item => item.length > 0)
          };
        });
      });
      return lists;
    } catch (error) {
      return [];
    }
  }

  /**
   * 提取图片
   * @param {Page} page - Playwright页面对象
   * @returns {Promise<Array>} 图片数组
   */
  /**
   * 提取图片并下载到同名文件夹
   * @param {Page} page - Playwright页面对象
   * @param {string} filepath - 输出文件路径
   * @param {string} pagesDir - 页面目录
   * @returns {Promise<Array>} 图片数组
   */
  async extractImages(page, filepath, pagesDir) {
    try {
      const fs = await import('fs');
      const path = await import('path');
      const https = await import('https');
      const http = await import('http');
      
      // 获取基础文件名（不含扩展名）
      const baseFilename = filepath ? path.basename(filepath, '.md') : 'images';
      
      // 创建同名文件夹来存放图片
      const imagesDir = path.join(pagesDir, baseFilename);
      if (!fs.existsSync(imagesDir)) {
        fs.mkdirSync(imagesDir, { recursive: true });
      }
      
      const images = await page.evaluate(() => {
        const imgElements = document.querySelectorAll('img');
        return Array.from(imgElements).map((img, index) => ({
          src: img.src,
          alt: img.alt || '',
          title: img.title || '',
          index: index + 1
        }));
      });
      
      const downloadedImages = [];
      
      for (const img of images) {
        try {
          // 跳过data URL和无效URL
          if (!img.src || img.src.startsWith('data:')) {
            continue;
          }
          
          // 获取文件扩展名
          const urlObj = new URL(img.src);
          let ext = path.extname(urlObj.pathname) || '.jpg';
          if (!ext.match(/\.(jpg|jpeg|png|gif|webp|svg)$/i)) {
            ext = '.jpg';
          }
          
          // 生成本地文件名
          const localFilename = `image_${img.index}${ext}`;
          const localPath = path.join(imagesDir, localFilename);
          
          // 下载图片
          await new Promise((resolve, reject) => {
            const protocol = img.src.startsWith('https') ? https : http;
            const file = fs.createWriteStream(localPath);
            
            protocol.get(img.src, (response) => {
              if (response.statusCode === 200) {
                response.pipe(file);
                file.on('finish', () => {
                  file.close();
                  resolve();
                });
              } else {
                file.close();
                fs.unlinkSync(localPath);
                resolve(); // 继续处理其他图片
              }
            }).on('error', (err) => {
              file.close();
              if (fs.existsSync(localPath)) {
                fs.unlinkSync(localPath);
              }
              resolve(); // 继续处理其他图片
            });
          });
          
          downloadedImages.push({
            src: img.src,
            localPath: `${baseFilename}/${localFilename}`,
            alt: img.alt,
            title: img.title
          });
        } catch (error) {
          console.error(`Error downloading image ${img.src}:`, error.message);
        }
      }
      
      return downloadedImages;
    } catch (error) {
      console.error('Failed to extract images:', error.message);
      return [];
    }
  }

  /**
   * 提取Tab页内容
   * @param {Page} page - Playwright页面对象
   * @returns {Promise<Array>} Tab数组
   */
  async extractTabs(page) {
    try {
      // 查找所有可能的tab按钮
      const tabButtons = await page.evaluate(() => {
        const selectors = [
          '[role="tab"]',
          '.tab',
          '.tabs button',
          '.tabs a',
          '[class*="tab-"]',
          'button[class*="tab"]'
        ];
        
        const buttons = [];
        for (const selector of selectors) {
          const elements = document.querySelectorAll(selector);
          if (elements.length > 0) {
            Array.from(elements).forEach((el, index) => {
              buttons.push({
                text: el.textContent.trim(),
                index,
                selector
              });
            });
            break; // 找到一组就停止
          }
        }
        return buttons;
      });

      const tabs = [];
      
      // 点击每个tab并提取内容
      for (const btn of tabButtons) {
        try {
          // 点击tab
          await page.evaluate((args) => {
            const { selector, index } = args;
            const elements = document.querySelectorAll(selector);
            if (elements[index]) {
              elements[index].click();
            }
          }, { selector: btn.selector, index: btn.index });
          
          // 等待内容加载
          await page.waitForTimeout(500);
          
          // 提取当前显示的内容
          const content = await page.evaluate(() => {
            const contentSelectors = [
              '[role="tabpanel"]:not([hidden])',
              '.tab-content:not([style*="display: none"])',
              '.tab-pane.active',
              '[class*="tab-content"].active'
            ];
            
            for (const selector of contentSelectors) {
              const el = document.querySelector(selector);
              if (el) {
                return {
                  text: el.textContent.trim(),
                  html: el.innerHTML
                };
              }
            }
            
            return { text: '', html: '' };
          });
          
          if (content.text) {
            tabs.push({
              name: btn.text,
              content: content.text
            });
          }
        } catch (e) {
          // 忽略单个tab的错误
        }
      }
      
      return tabs;
    } catch (error) {
      console.error('Failed to extract tabs:', error.message);
      return [];
    }
  }

  /**
   * 提取表格（支持分页）
   * @param {Page} page - Playwright页面对象
   * @param {Function} onDataChunk - 数据块回调函数
   * @returns {Promise<Array>} 表格数组
   */
  async extractTablesWithPagination(page, onDataChunk) {
    try {
      const tables = [];
      const tableElements = await page.locator('table').all();
      
      for (let tableIndex = 0; tableIndex < tableElements.length; tableIndex++) {
        const tableEl = tableElements[tableIndex];
        
        // 提取表格基本信息
        const tableInfo = await this.extractSingleTable(tableEl, tableIndex);
        
        // 查找分页控件
        const paginationInfo = await this.findPaginationControls(page, tableEl);
        
        if (paginationInfo.hasPagination) {
          // 分页表格处理
          const allRows = [...tableInfo.rows];
          let currentPage = 1;
          const maxPages = paginationInfo.totalPages || 100; // 最多100页
          
          // 发送第一页数据
          if (onDataChunk) {
            await onDataChunk({
              type: 'table',
              tableIndex,
              page: currentPage,
              headers: tableInfo.headers,
              rows: tableInfo.rows,
              isFirstPage: true,
              isLastPage: false
            });
          }
          
          // 翻页并提取数据
          while (currentPage < maxPages) {
            const hasNextPage = await this.clickNextPage(page, paginationInfo);
            
            if (!hasNextPage) {
              break;
            }
            
            currentPage++;
            
            // 等待新数据加载
            await page.waitForTimeout(1000);
            
            // 提取当前页的表格数据
            const currentTableEl = (await page.locator('table').all())[tableIndex];
            const currentPageData = await this.extractSingleTable(currentTableEl, tableIndex);
            
            // 检查表格结构是否一致
            const headersMatch = this.compareHeaders(tableInfo.headers, currentPageData.headers);
            
            if (headersMatch) {
              // 结构一致，追加数据
              allRows.push(...currentPageData.rows);
              
              // 发送数据块
              if (onDataChunk) {
                await onDataChunk({
                  type: 'table',
                  tableIndex,
                  page: currentPage,
                  headers: currentPageData.headers,
                  rows: currentPageData.rows,
                  isFirstPage: false,
                  isLastPage: false
                });
              }
            } else {
              // 结构不一致，作为新表格
              if (onDataChunk) {
                await onDataChunk({
                  type: 'table-new',
                  tableIndex: tables.length + 1,
                  page: 1,
                  headers: currentPageData.headers,
                  rows: currentPageData.rows,
                  isFirstPage: true,
                  isLastPage: false
                });
              }
              
              tables.push({
                index: tableIndex,
                headers: tableInfo.headers,
                rows: allRows,
                caption: tableInfo.caption,
                totalPages: currentPage - 1
              });
              
              // 开始新表格
              tableInfo.headers = currentPageData.headers;
              allRows.length = 0;
              allRows.push(...currentPageData.rows);
            }
            
            // 避免过快翻页
            await page.waitForTimeout(500);
          }
          
          // 发送最后一页标记
          if (onDataChunk) {
            await onDataChunk({
              type: 'table',
              tableIndex,
              page: currentPage,
              headers: tableInfo.headers,
              rows: [],
              isFirstPage: false,
              isLastPage: true
            });
          }
          
          tables.push({
            index: tableIndex,
            headers: tableInfo.headers,
            rows: allRows,
            caption: tableInfo.caption,
            totalPages: currentPage
          });
        } else {
          // 无分页，直接添加
          tables.push(tableInfo);
          
          if (onDataChunk) {
            await onDataChunk({
              type: 'table',
              tableIndex,
              page: 1,
              headers: tableInfo.headers,
              rows: tableInfo.rows,
              isFirstPage: true,
              isLastPage: true
            });
          }
        }
      }
      
      return tables;
    } catch (error) {
      console.error('Failed to extract tables with pagination:', error.message);
      return [];
    }
  }

  /**
   * 提取单个表格
   * @param {Locator} tableEl - 表格元素
   * @param {number} index - 表格索引
   * @returns {Promise<Object>} 表格数据
   */
  async extractSingleTable(tableEl, index) {
    const tableData = await tableEl.evaluate((table, idx) => {
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
        index: idx,
        headers, 
        rows,
        caption: table.querySelector('caption')?.textContent.trim() || ''
      };
    }, index);
    
    return tableData;
  }

  /**
   * 查找分页控件
   * @param {Page} page - Playwright页面对象
   * @param {Locator} tableEl - 表格元素
   * @returns {Promise<Object>} 分页信息
   */
  async findPaginationControls(page, tableEl) {
    try {
      const paginationInfo = await page.evaluate(() => {
        // 常见的分页控件选择器
        const selectors = [
          '.pagination',
          '.pager',
          '[class*="pagination"]',
          '[class*="pager"]',
          'nav[aria-label*="pagination"]',
          '.page-navigation',
          '[class*="page-nav"]',
          'ul[class*="page"]',
          'div[class*="page"]'
        ];
        
        let paginationEl = null;
        for (const selector of selectors) {
          paginationEl = document.querySelector(selector);
          if (paginationEl) break;
        }
        
        if (!paginationEl) {
          return { hasPagination: false };
        }
        
        // 查找"下一页"按钮 - 使用原生JavaScript方法
        let nextButton = null;
        
        // 方法1: 查找包含"下一页"或"Next"文本的按钮/链接
        const allButtons = paginationEl.querySelectorAll('button, a, li');
        for (const btn of allButtons) {
          const text = btn.textContent.trim();
          if (text === '下一页' || text === 'Next' || text === '›' || text === '>' || text === '》') {
            nextButton = btn;
            break;
          }
        }
        
        // 方法2: 查找带有next类名的元素
        if (!nextButton) {
          const nextElements = paginationEl.querySelectorAll('.next, [class*="next"], [aria-label*="next"]');
          if (nextElements.length > 0) {
            nextButton = nextElements[0];
          }
        }
        
        // 尝试获取总页数
        let totalPages = null;
        const pageText = paginationEl.textContent;
        const pageMatch = pageText.match(/共\s*(\d+)\s*页|total\s*(\d+)\s*pages?/i);
        if (pageMatch) {
          totalPages = parseInt(pageMatch[1] || pageMatch[2]);
        }
        
        return {
          hasPagination: !!nextButton,
          totalPages,
          nextButtonSelector: nextButton ? nextButton.className : null
        };
      });
      
      return paginationInfo;
    } catch (error) {
      return { hasPagination: false };
    }
  }

  /**
   * 点击下一页
   * @param {Page} page - Playwright页面对象
   * @param {Object} paginationInfo - 分页信息
   * @returns {Promise<boolean>} 是否成功翻页
   */
  async clickNextPage(page, paginationInfo) {
    try {
      // 尝试多种方式查找并点击下一页按钮
      const nextButtonSelectors = [
        'text="下一页"',
        'text="Next"',
        'text="›"',
        'text=">"',
        '.next:not(.disabled)',
        '[class*="next"]:not(.disabled)',
        '[aria-label*="next"]:not([disabled])',
        'button[class*="next"]:not([disabled])',
        'a[class*="next"]:not(.disabled)',
        'li:has-text("›")',
        'li:has-text(">")'
      ];
      
      for (const selector of nextButtonSelectors) {
        try {
          const button = page.locator(selector).first();
          const count = await button.count();
          
          if (count > 0) {
            // 检查按钮是否可点击
            const isDisabled = await button.evaluate(el => {
              return el.disabled || 
                     el.classList.contains('disabled') || 
                     el.getAttribute('aria-disabled') === 'true' ||
                     el.style.pointerEvents === 'none';
            });
            
            if (!isDisabled) {
              await button.click();
              return true;
            }
          }
        } catch (e) {
          continue;
        }
      }
      
      return false;
    } catch (error) {
      console.error('Failed to click next page:', error.message);
      return false;
    }
  }

  /**
   * 比较表头是否一致
   * @param {Array} headers1 - 表头1
   * @param {Array} headers2 - 表头2
   * @returns {boolean} 是否一致
   */
  compareHeaders(headers1, headers2) {
    if (headers1.length !== headers2.length) {
      return false;
    }
    
    for (let i = 0; i < headers1.length; i++) {
      if (headers1[i] !== headers2[i]) {
        return false;
      }
    }
    
    return true;
  }

  /**
   * 生成内容的Markdown文本（用于比较）
   * @param {Object} data - 数据对象
   * @returns {string} Markdown文本
   */
  generateContentMarkdown(data) {
    const sections = [];
    
    // 段落
    if (data.paragraphs && data.paragraphs.length > 0) {
      data.paragraphs.forEach(p => {
        if (p.trim()) {
          sections.push(p.trim());
        }
      });
    }
    
    // 列表
    if (data.lists && data.lists.length > 0) {
      data.lists.forEach(list => {
        list.items.forEach((item, i) => {
          if (list.type === 'ol') {
            sections.push(`${i + 1}. ${item}`);
          } else {
            sections.push(`- ${item}`);
          }
        });
      });
    }
    
    // 表格
    if (data.tables && data.tables.length > 0) {
      data.tables.forEach(table => {
        if (table.headers && table.headers.length > 0) {
          sections.push(table.headers.join('|'));
          if (table.rows && table.rows.length > 0) {
            table.rows.forEach(row => {
              sections.push(row.join('|'));
            });
          }
        }
      });
    }
    
    // 代码块
    if (data.codeBlocks && data.codeBlocks.length > 0) {
      data.codeBlocks.forEach(block => {
        sections.push(block.code);
      });
    }
    
    return sections.join('\n').trim();
  }

  /**
   * 检查内容是否已存在于文件中
   * @param {string} filepath - 文件路径
   * @param {string} content - 要检查的内容
   * @returns {boolean} 是否已存在
   */
  async isContentInFile(filepath, content) {
    try {
      const fs = await import('fs');
      if (!fs.existsSync(filepath)) {
        return false;
      }
      
      const fileContent = fs.readFileSync(filepath, 'utf-8');
      // 标准化内容进行比较（去除多余空格和换行）
      const normalizedFileContent = fileContent.replace(/\s+/g, ' ').trim();
      const normalizedContent = content.replace(/\s+/g, ' ').trim();
      
      return normalizedFileContent.includes(normalizedContent);
    } catch (error) {
      console.error('Error checking file content:', error.message);
      return false;
    }
  }

  /**
   * 提取Tab页和下拉框内容（检测数据变化）
   * @param {Page} page - Playwright页面对象
   * @param {string} filepath - 输出文件路径
   * @param {Function} onDataChunk - 数据块回调
   * @returns {Promise<Array>} Tab和下拉框数据
   */
  async extractTabsAndDropdowns(page, filepath, onDataChunk) {
    const results = [];
    
    try {
      // 1. 查找并处理Tab页
      const tabs = await this.findAndProcessTabs(page, filepath, onDataChunk);
      results.push(...tabs);
      
      // 2. 查找并处理下拉框
      const dropdowns = await this.findAndProcessDropdowns(page, filepath, onDataChunk);
      results.push(...dropdowns);
      
      return results;
    } catch (error) {
      console.error('Failed to extract tabs and dropdowns:', error.message);
      return results;
    }
  }

  /**
   * 查找并处理Tab页
   * @param {Page} page - Playwright页面对象
   * @param {string} filepath - 输出文件路径
   * @param {Function} onDataChunk - 数据块回调
   * @returns {Promise<Array>} Tab数据
   */
  async findAndProcessTabs(page, filepath, onDataChunk) {
    const tabs = [];
    
    try {
      // 查找所有可能的tab按钮 - 使用更通用的策略
      const tabButtons = await page.evaluate(() => {
        const buttons = [];
        
        // 策略1: 标准tab选择器
        const standardSelectors = [
          '[role="tab"]',
          '.tab',
          '.tabs button',
          '.tabs a',
          '[class*="tab-"]',
          'button[class*="tab"]',
          'a[class*="tab"]'
        ];
        
        for (const selector of standardSelectors) {
          const elements = document.querySelectorAll(selector);
          if (elements.length > 1) { // 至少2个tab才算
            Array.from(elements).forEach((el, index) => {
              buttons.push({
                text: el.textContent.trim(),
                index,
                selector,
                strategy: 'standard'
              });
            });
            break;
          }
        }
        
        // 策略2: 如果没找到标准tab，查找可点击的文本元素（可能是自定义tab）
        if (buttons.length === 0) {
          // 查找所有可点击的元素（button, a, div with click handler）
          const clickableElements = Array.from(document.querySelectorAll('button, a, [onclick], [role="button"]'));
          
          // 过滤出可能是tab的元素：
          // 1. 文本长度适中（2-50字符）
          // 2. 同级元素有多个类似的
          // 3. 不是导航链接（不包含http）
          const potentialTabs = clickableElements.filter(el => {
            const text = el.textContent.trim();
            const hasHref = el.tagName === 'A' && el.href && el.href.startsWith('http');
            return text.length >= 2 && text.length <= 50 && !hasHref;
          });
          
          // 按父元素分组
          const groupedByParent = new Map();
          potentialTabs.forEach(el => {
            const parent = el.parentElement;
            if (parent) {
              const key = parent.tagName + parent.className;
              if (!groupedByParent.has(key)) {
                groupedByParent.set(key, []);
              }
              groupedByParent.get(key).push(el);
            }
          });
          
          // 找到最大的组（最可能是tab组）
          let maxGroup = [];
          groupedByParent.forEach(group => {
            if (group.length > maxGroup.length && group.length >= 2) {
              maxGroup = group;
            }
          });
          
          if (maxGroup.length >= 2) {
            maxGroup.forEach((el, index) => {
              // 生成唯一选择器
              let selector = el.tagName.toLowerCase();
              if (el.id) {
                selector = `#${el.id}`;
              } else if (el.className) {
                const classes = el.className.split(' ').filter(c => c.trim());
                if (classes.length > 0) {
                  selector = `.${classes[0]}`;
                }
              }
              
              buttons.push({
                text: el.textContent.trim(),
                index,
                selector,
                strategy: 'clickable',
                element: el
              });
            });
          }
        }
        
        // 策略3: 查找包含特定关键词的元素（如股东名称）
        if (buttons.length === 0) {
          // 查找可能是公司/股东名称的元素
          const nameKeywords = ['公司', '银行', '集团', 'CO.', 'LTD', 'INC', 'CORP', 'GROUP'];
          const allElements = Array.from(document.querySelectorAll('div, span, button, a'));
          
          const nameElements = allElements.filter(el => {
            const text = el.textContent.trim();
            // 只取叶子节点或子节点很少的节点
            if (el.children.length > 2) return false;
            // 文本长度适中
            if (text.length < 3 || text.length > 100) return false;
            // 包含关键词
            return nameKeywords.some(keyword => text.includes(keyword));
          });
          
          // 按父元素分组
          const groupedNames = new Map();
          nameElements.forEach(el => {
            const parent = el.parentElement;
            if (parent) {
              const key = parent.tagName + parent.className;
              if (!groupedNames.has(key)) {
                groupedNames.set(key, []);
              }
              groupedNames.get(key).push(el);
            }
          });
          
          // 找到最大的组
          let maxNameGroup = [];
          groupedNames.forEach(group => {
            if (group.length > maxNameGroup.length && group.length >= 2) {
              maxNameGroup = group;
            }
          });
          
          if (maxNameGroup.length >= 2) {
            maxNameGroup.forEach((el, index) => {
              buttons.push({
                text: el.textContent.trim(),
                index,
                selector: el.tagName.toLowerCase(),
                strategy: 'name-based',
                element: el
              });
            });
          }
        }
        
        return buttons;
      });

      if (tabButtons.length === 0) {
        return tabs;
      }

      console.log(`  找到 ${tabButtons.length} 个可能的Tab (策略: ${tabButtons[0]?.strategy})`);

      if (tabButtons.length === 0) {
        return tabs;
      }

      // 点击每个tab并检查数据变化
      for (const btn of tabButtons) {
        try {
          console.log(`  尝试Tab: "${btn.text.substring(0, 30)}..."`);
          
          // 点击tab - 根据策略使用不同的点击方法
          if (btn.strategy === 'standard') {
            await page.evaluate((args) => {
              const { selector, index } = args;
              const elements = document.querySelectorAll(selector);
              if (elements[index]) {
                elements[index].click();
              }
            }, { selector: btn.selector, index: btn.index });
          } else {
            // 对于自定义tab，尝试多种点击方式
            const clicked = await page.evaluate((args) => {
              const { text, index } = args;
              
              // 方法1: 通过文本内容查找并点击
              const allClickable = Array.from(document.querySelectorAll('button, a, [onclick], [role="button"], div, span'));
              const matching = allClickable.filter(el => el.textContent.trim() === text);
              
              if (matching[index]) {
                matching[index].click();
                return true;
              }
              
              // 方法2: 通过部分文本匹配
              const partialMatch = allClickable.filter(el => el.textContent.trim().includes(text.substring(0, 10)));
              if (partialMatch[index]) {
                partialMatch[index].click();
                return true;
              }
              
              return false;
            }, { text: btn.text, index: btn.index });
            
            if (!clicked) {
              console.log(`    无法点击Tab: "${btn.text}"`);
              continue;
            }
          }
          
          // 等待内容加载
          await page.waitForTimeout(1000);
          
          // 提取当前数据
          const currentParagraphs = await this.extractParagraphs(page);
          const currentLists = await this.extractLists(page);
          
          // 使用简单的表格提取而不是分页版本
          const currentTables = [];
          try {
            const tableElements = await page.locator('table').all();
            for (let i = 0; i < Math.min(tableElements.length, 5); i++) {
              const table = await this.extractSingleTable(tableElements[i], i);
              currentTables.push(table);
            }
          } catch (e) {
            // 忽略表格提取错误
          }
          
          const currentCodeBlocks = await this.extractCodeBlocks(page);
          
          // 生成当前内容的Markdown
          const currentContent = this.generateContentMarkdown({
            paragraphs: currentParagraphs,
            lists: currentLists,
            tables: currentTables,
            codeBlocks: currentCodeBlocks
          });
          
          // 检查内容是否已存在于文件中
          const isExisting = await this.isContentInFile(filepath, currentContent);
          
          if (!isExisting && currentContent.length > 0) {
            const tabData = {
              type: 'tab',
              name: btn.text,
              paragraphs: currentParagraphs,
              lists: currentLists,
              tables: currentTables,
              codeBlocks: currentCodeBlocks
            };
            
            tabs.push(tabData);
            
            // 通知数据块
            if (onDataChunk) {
              await onDataChunk({
                type: 'tab',
                name: btn.text,
                data: tabData
              });
            }
          }
        } catch (e) {
          console.error(`Error processing tab "${btn.text}":`, e.message);
        }
      }
      
      return tabs;
    } catch (error) {
      console.error('Failed to find and process tabs:', error.message);
      return tabs;
    }
  }

  /**
   * 查找并处理下拉框
   * @param {Page} page - Playwright页面对象
   * @param {string} filepath - 输出文件路径
   * @param {Function} onDataChunk - 数据块回调
   * @returns {Promise<Array>} 下拉框数据
   */
  async findAndProcessDropdowns(page, filepath, onDataChunk) {
    const dropdowns = [];
    
    try {
      // 查找所有下拉框
      const dropdownElements = await page.evaluate(() => {
        const selectors = [
          'select',
          '[role="combobox"]',
          '.dropdown select',
          '[class*="select"]',
          '[class*="dropdown"]'
        ];
        
        const elements = [];
        for (const selector of selectors) {
          const found = document.querySelectorAll(selector);
          if (found.length > 0) {
            Array.from(found).forEach((el, index) => {
              // 获取选项
              let options = [];
              if (el.tagName === 'SELECT') {
                options = Array.from(el.options).map(opt => ({
                  value: opt.value,
                  text: opt.textContent.trim()
                }));
              }
              
              if (options.length > 1) {
                elements.push({
                  index,
                  selector,
                  options,
                  label: el.getAttribute('aria-label') || el.name || `下拉框${index + 1}`
                });
              }
            });
          }
        }
        return elements;
      });

      if (dropdownElements.length === 0) {
        return dropdowns;
      }

      // 检测下拉框数量，决定处理策略
      const dropdownCount = dropdownElements.length;
      const MAX_DROPDOWNS_FOR_COMBINATION = 5;
      
      if (dropdownCount > MAX_DROPDOWNS_FOR_COMBINATION) {
        console.log(`  检测到 ${dropdownCount} 个下拉框（超过${MAX_DROPDOWNS_FOR_COMBINATION}个），使用依次遍历模式（不做排列组合）`);
      } else {
        console.log(`  检测到 ${dropdownCount} 个下拉框，使用标准遍历模式`);
      }

      // 处理每个下拉框
      for (const dropdown of dropdownElements) {
        try {
          const dropdownData = {
            type: 'dropdown',
            label: dropdown.label,
            options: []
          };
          
          // 尝试每个选项
          for (const option of dropdown.options) {
            try {
              // 选择选项
              await page.evaluate((args) => {
                const { selector, index, value } = args;
                const elements = document.querySelectorAll(selector);
                if (elements[index] && elements[index].tagName === 'SELECT') {
                  elements[index].value = value;
                  // 触发change事件
                  elements[index].dispatchEvent(new Event('change', { bubbles: true }));
                }
              }, { selector: dropdown.selector, index: dropdown.index, value: option.value });
              
              // 等待内容更新
              await page.waitForTimeout(1000);
              
              // 提取当前数据
              const currentParagraphs = await this.extractParagraphs(page);
              const currentLists = await this.extractLists(page);
              
              // 使用简单的表格提取而不是分页版本（避免在下拉框处理中触发复杂逻辑）
              const currentTables = [];
              try {
                const tableElements = await page.locator('table').all();
                for (let i = 0; i < Math.min(tableElements.length, 5); i++) {
                  const table = await this.extractSingleTable(tableElements[i], i);
                  currentTables.push(table);
                }
              } catch (e) {
                // 忽略表格提取错误
              }
              
              const currentCodeBlocks = await this.extractCodeBlocks(page);
              
              // 生成当前内容的Markdown
              const currentContent = this.generateContentMarkdown({
                paragraphs: currentParagraphs,
                lists: currentLists,
                tables: currentTables,
                codeBlocks: currentCodeBlocks
              });
              
              // 检查内容是否已存在于文件中
              const isExisting = await this.isContentInFile(filepath, currentContent);
              
              if (!isExisting && currentContent.length > 0) {
                dropdownData.options.push({
                  value: option.value,
                  text: option.text,
                  paragraphs: currentParagraphs,
                  lists: currentLists,
                  tables: currentTables,
                  codeBlocks: currentCodeBlocks
                });
                
                // 通知数据块
                if (onDataChunk) {
                  await onDataChunk({
                    type: 'dropdown-option',
                    dropdown: dropdown.label,
                    option: option.text,
                    data: {
                      paragraphs: currentParagraphs,
                      lists: currentLists,
                      tables: currentTables,
                      codeBlocks: currentCodeBlocks
                    }
                  });
                }
              }
            } catch (e) {
              console.error(`  Error processing option "${option.text}":`, e.message);
            }
          }
          
          if (dropdownData.options.length > 0) {
            dropdowns.push(dropdownData);
          }
        } catch (e) {
          console.error(`Error processing dropdown "${dropdown.label}":`, e.message);
        }
      }
      
      return dropdowns;
    } catch (error) {
      console.error('Failed to find and process dropdowns:', error.message);
      return dropdowns;
    }
  }

  /**
   * 查找并处理时间筛选控件
   * @param {Page} page - Playwright页面对象
   * @param {string} filepath - 输出文件路径
   * @param {Function} onDataChunk - 数据块回调
   * @returns {Promise<Array>} 时间筛选结果
   */
  async findAndProcessDateFilters(page, filepath, onDataChunk) {
    const results = [];
    
    try {
      // 查找日期筛选控件
      const dateControls = await page.evaluate(() => {
        const controls = [];
        
        // 查找日期输入框
        const dateInputs = document.querySelectorAll('input[type="date"], input[placeholder*="日期"], input[placeholder*="时间"], input[placeholder*="date"], input[placeholder*="time"]');
        
        // 查找包含"开始"和"结束"的输入框对
        const allInputs = Array.from(document.querySelectorAll('input'));
        const startInputs = allInputs.filter(input => {
          const placeholder = input.placeholder || '';
          const label = input.getAttribute('aria-label') || '';
          const id = input.id || '';
          return /开始|起始|from|start/i.test(placeholder + label + id);
        });
        
        const endInputs = allInputs.filter(input => {
          const placeholder = input.placeholder || '';
          const label = input.getAttribute('aria-label') || '';
          const id = input.id || '';
          return /结束|截止|to|end/i.test(placeholder + label + id);
        });
        
        if (startInputs.length > 0 && endInputs.length > 0) {
          controls.push({
            type: 'date-range',
            startSelector: startInputs[0].id ? `#${startInputs[0].id}` : `input[placeholder*="${startInputs[0].placeholder}"]`,
            endSelector: endInputs[0].id ? `#${endInputs[0].id}` : `input[placeholder*="${endInputs[0].placeholder}"]`,
            hasSubmitButton: !!document.querySelector('button[type="submit"], button:has-text("查询"), button:has-text("搜索"), button:has-text("确定")')
          });
        }
        
        return controls;
      });
      
      if (dateControls.length === 0) {
        return results;
      }
      
      // 处理每个日期筛选控件
      for (const control of dateControls) {
        try {
          await this.processDateRangeFilter(page, control, filepath, onDataChunk);
          results.push(control);
        } catch (error) {
          console.error(`Error processing date filter:`, error.message);
        }
      }
      
      return results;
    } catch (error) {
      console.error('Failed to find and process date filters:', error.message);
      return results;
    }
  }

  /**
   * 处理日期范围筛选
   * @param {Page} page - Playwright页面对象
   * @param {Object} control - 日期控件信息
   * @param {string} filepath - 输出文件路径
   * @param {Function} onDataChunk - 数据块回调
   */
  async processDateRangeFilter(page, control, filepath, onDataChunk) {
    const today = new Date();
    const todayStr = today.toISOString().split('T')[0]; // YYYY-MM-DD
    
    // 定义要尝试的时间范围（从最大到最小）
    const dateRanges = [
      { label: '2000年至今', startYear: 2000 },
      { label: '最近10年', startYear: today.getFullYear() - 10 },
      { label: '最近5年', startYear: today.getFullYear() - 5 },
      { label: '最近3年', startYear: today.getFullYear() - 3 },
      { label: '最近1年', startYear: today.getFullYear() - 1 }
    ];
    
    for (const range of dateRanges) {
      try {
        const startDate = `${range.startYear}-01-01`;
        
        // 填充开始日期
        await page.locator(control.startSelector).fill(startDate);
        await page.waitForTimeout(500);
        
        // 填充结束日期
        await page.locator(control.endSelector).fill(todayStr);
        await page.waitForTimeout(500);
        
        // 如果有提交按钮，点击它
        if (control.hasSubmitButton) {
          const submitButton = page.locator('button[type="submit"], button:has-text("查询"), button:has-text("搜索"), button:has-text("确定")').first();
          await submitButton.click();
          await page.waitForTimeout(2000); // 等待数据加载
        } else {
          // 触发change事件
          await page.locator(control.endSelector).press('Enter');
          await page.waitForTimeout(2000);
        }
        
        // 检查是否有数据或错误
        const hasData = await this.checkForDataOrError(page);
        
        if (hasData.hasData && !hasData.hasError) {
          // 提取数据
          const tables = await this.extractTablesWithPagination(page, onDataChunk);
          
          if (tables.length > 0) {
            // 通知数据块
            if (onDataChunk) {
              await onDataChunk({
                type: 'date-filter',
                range: range.label,
                startDate,
                endDate: todayStr,
                tables
              });
            }
            
            // 成功提取数据，不再尝试其他范围
            break;
          }
        } else if (hasData.hasError) {
          continue;
        } else {
          continue;
        }
      } catch (error) {
        console.error(`Error trying date range ${range.label}:`, error.message);
        continue;
      }
    }
  }

  /**
   * 检查页面是否有数据或错误
   * @param {Page} page - Playwright页面对象
   * @returns {Promise<Object>} {hasData, hasError}
   */
  async checkForDataOrError(page) {
    try {
      const result = await page.evaluate(() => {
        // 检查是否有错误提示
        const errorSelectors = [
          '.error',
          '.alert-error',
          '[class*="error"]',
          '.message.error',
          '[role="alert"]'
        ];
        
        let hasError = false;
        for (const selector of errorSelectors) {
          const elements = document.querySelectorAll(selector);
          if (elements.length > 0) {
            const text = Array.from(elements).map(el => el.textContent).join(' ');
            if (text.includes('错误') || text.includes('失败') || text.includes('error') || text.includes('无数据') || text.includes('no data')) {
              hasError = true;
              break;
            }
          }
        }
        
        // 检查是否有数据表格
        const tables = document.querySelectorAll('table');
        let hasData = false;
        
        for (const table of tables) {
          const rows = table.querySelectorAll('tbody tr, tr');
          if (rows.length > 1) { // 至少有表头和一行数据
            hasData = true;
            break;
          }
        }
        
        // 检查是否有"无数据"提示
        const noDataTexts = ['暂无数据', '无数据', '没有数据', 'no data', 'no results'];
        const bodyText = document.body.textContent.toLowerCase();
        for (const text of noDataTexts) {
          if (bodyText.includes(text.toLowerCase())) {
            hasData = false;
            break;
          }
        }
        
        return { hasData, hasError };
      });
      
      return result;
    } catch (error) {
      return { hasData: false, hasError: true };
    }
  }

  /**
   * 将API数据转换为表格格式
   * @param {Array} apiDataList - API数据列表
   * @param {Function} onDataChunk - 数据块回调
   * @returns {Promise<Array>} 表格数组
   */
  async convertAPIDataToTables(apiDataList, onDataChunk) {
    const tables = [];
    
    for (const apiResponse of apiDataList) {
      try {
        const { url, data } = apiResponse;
        
        if (!Array.isArray(data) || data.length === 0) {
          continue;
        }
        
        // 分析数据结构
        const firstItem = data[0];
        const keys = Object.keys(firstItem);
        
        // 扁平化嵌套对象
        const flattenedData = data.map(item => {
          const flat = {};
          
          for (const key of keys) {
            const value = item[key];
            
            if (value && typeof value === 'object' && !Array.isArray(value)) {
              // 嵌套对象，展开
              for (const subKey of Object.keys(value)) {
                const subValue = value[subKey];
                if (subValue && typeof subValue === 'object' && !Array.isArray(subValue)) {
                  // 再次嵌套
                  for (const subSubKey of Object.keys(subValue)) {
                    flat[`${key}.${subKey}.${subSubKey}`] = subValue[subSubKey];
                  }
                } else {
                  flat[`${key}.${subKey}`] = subValue;
                }
              }
            } else {
              flat[key] = value;
            }
          }
          
          return flat;
        });
        
        // 获取所有列名
        const allKeys = new Set();
        flattenedData.forEach(item => {
          Object.keys(item).forEach(key => allKeys.add(key));
        });
        
        const headers = Array.from(allKeys);
        
        // 转换为行数据
        const rows = flattenedData.map(item => {
          return headers.map(header => {
            const value = item[header];
            if (value === null || value === undefined) {
              return '';
            }
            if (typeof value === 'object') {
              return JSON.stringify(value);
            }
            return String(value);
          });
        });
        
        const table = {
          index: tables.length,
          headers,
          rows,
          caption: `API数据: ${url.split('/').pop()}`,
          source: 'api'
        };
        
        tables.push(table);
        
        // 通知数据块
        if (onDataChunk) {
          await onDataChunk({
            type: 'table',
            tableIndex: tables.length - 1,
            page: 1,
            headers,
            rows,
            isFirstPage: true,
            isLastPage: true,
            source: 'api'
          });
        }
        
      } catch (error) {
        console.error(`Error converting API data to table:`, error.message);
      }
    }
    
    return tables;
  }

  /**
   * 提取并保存图表（Canvas/SVG）
   * @param {Page} page - Playwright页面对象
   * @param {string} filepath - 输出文件路径（包含.md扩展名）
   * @param {string} pagesDir - 页面目录
   * @returns {Promise<Array>} 图表信息数组
   */
  async extractAndSaveCharts(page, filepath, pagesDir) {
    const charts = [];
    
    try {
      // 等待图表渲染完成
      await page.waitForTimeout(2000);
      
      const fs = await import('fs');
      const path = await import('path');
      
      // 获取基础文件名（不含扩展名）
      const baseFilename = filepath ? path.basename(filepath, '.md') : 'chart';
      
      // 创建同名文件夹来存放图表
      const chartsDir = path.join(pagesDir, baseFilename);
      if (!fs.existsSync(chartsDir)) {
        fs.mkdirSync(chartsDir, { recursive: true });
      }
      
      // 查找所有Canvas元素
      const canvases = await page.locator('canvas').all();
      
      for (let i = 0; i < canvases.length; i++) {
        try {
          const canvas = canvases[i];
          
          // 检查canvas是否可见且有尺寸
          const isVisible = await canvas.isVisible();
          if (!isVisible) {
            continue;
          }
          
          const box = await canvas.boundingBox();
          if (!box || box.width < 10 || box.height < 10) {
            continue;
          }
          
          // 生成文件名 - 保存到同名文件夹中
          const chartFilename = `canvas_${i + 1}.png`;
          const chartPath = path.join(chartsDir, chartFilename);
          
          // 截图
          await canvas.screenshot({ path: chartPath });
          
          charts.push({
            type: 'canvas',
            index: i + 1,
            filename: `${baseFilename}/${chartFilename}`,
            width: Math.round(box.width),
            height: Math.round(box.height)
          });
        } catch (error) {
          console.error(`Error saving canvas ${i + 1}:`, error.message);
        }
      }
      
      // 查找所有SVG元素
      const svgs = await page.locator('svg').all();
      
      for (let i = 0; i < svgs.length; i++) {
        try {
          const svg = svgs[i];
          
          // 检查SVG是否可见且有尺寸
          const isVisible = await svg.isVisible();
          if (!isVisible) {
            continue;
          }
          
          const box = await svg.boundingBox();
          if (!box || box.width < 10 || box.height < 10) {
            continue;
          }
          
          // 生成文件名 - 保存到同名文件夹中
          const chartFilename = `svg_${i + 1}.png`;
          const chartPath = path.join(chartsDir, chartFilename);
          
          // 截图
          await svg.screenshot({ path: chartPath });
          
          charts.push({
            type: 'svg',
            index: i + 1,
            filename: `${baseFilename}/${chartFilename}`,
            width: Math.round(box.width),
            height: Math.round(box.height)
          });
        } catch (error) {
          console.error(`Error saving SVG ${i + 1}:`, error.message);
        }
      }
      
      return charts;
    } catch (error) {
      console.error('Failed to extract and save charts:', error.message);
      return charts;
    }
  }

  /**
   * 处理无限滚动加载
   * @param {Page} page - Playwright页面对象
   * @returns {Promise<void>}
   */
  async handleInfiniteScroll(page) {
    try {
      const maxScrolls = 30; // 最多滚动30次
      const scrollTimeout = 60000; // 60秒超时
      const startTime = Date.now();
      
      let scrollCount = 0;
      let previousHeight = 0;
      let noChangeCount = 0;
      
      while (scrollCount < maxScrolls) {
        // 检查是否超时
        if (Date.now() - startTime > scrollTimeout) {
          break;
        }
        
        // 获取当前页面高度
        const currentHeight = await page.evaluate(() => document.body.scrollHeight);
        
        // 如果高度没有变化，说明可能已经到底了
        if (currentHeight === previousHeight) {
          noChangeCount++;
          // 连续3次没有变化，认为已经加载完成
          if (noChangeCount >= 3) {
            break;
          }
        } else {
          noChangeCount = 0;
        }
        
        previousHeight = currentHeight;
        
        // 滚动到页面底部
        await page.evaluate(() => {
          window.scrollTo(0, document.body.scrollHeight);
        });
        
        scrollCount++;
        
        // 等待新内容加载
        await page.waitForTimeout(2000);
        
        // 检查是否有"加载中"或"加载更多"的指示器
        const hasLoadingIndicator = await page.evaluate(() => {
          const loadingTexts = ['加载中', 'loading', '加载更多', 'load more', '正在加载'];
          const bodyText = document.body.textContent.toLowerCase();
          return loadingTexts.some(text => bodyText.includes(text.toLowerCase()));
        });
        
        if (hasLoadingIndicator) {
          // 如果有加载指示器，多等待一会儿
          await page.waitForTimeout(2000);
        }
        
        // 检查是否有"没有更多"或"到底了"的提示
        const hasNoMoreIndicator = await page.evaluate(() => {
          const noMoreTexts = ['没有更多', 'no more', '已经到底', '暂无更多', '全部加载完成', 'end of list'];
          const bodyText = document.body.textContent.toLowerCase();
          return noMoreTexts.some(text => bodyText.includes(text.toLowerCase()));
        });
        
        if (hasNoMoreIndicator) {
          break;
          break;
        }
      }
      
      if (scrollCount > 0) {
        // 滚动回顶部，方便后续提取
        await page.evaluate(() => window.scrollTo(0, 0));
        await page.waitForTimeout(1000);
      }
      
    } catch (error) {
      console.error('Error handling infinite scroll:', error.message);
    }
  }

  /**
   * 提取引用块
   * @param {Page} page - Playwright页面对象
   * @returns {Promise<Array>} 引用块数组
   */
  async extractBlockquotes(page) {
    try {
      const blockquotes = await page.evaluate(() => {
        const elements = document.querySelectorAll('blockquote');
        return Array.from(elements).map(bq => bq.textContent.trim()).filter(text => text.length > 0);
      });
      return blockquotes;
    } catch (error) {
      return [];
    }
  }

  /**
   * 提取定义列表
   * @param {Page} page - Playwright页面对象
   * @returns {Promise<Array>} 定义列表数组
   */
  async extractDefinitionLists(page) {
    try {
      const dlists = await page.evaluate(() => {
        const elements = document.querySelectorAll('dl');
        return Array.from(elements).map(dl => {
          const items = [];
          let currentTerm = null;
          
          Array.from(dl.children).forEach(child => {
            if (child.tagName === 'DT') {
              currentTerm = child.textContent.trim();
            } else if (child.tagName === 'DD' && currentTerm) {
              items.push({
                term: currentTerm,
                definition: child.textContent.trim()
              });
              currentTerm = null;
            }
          });
          
          return items;
        }).filter(list => list.length > 0);
      });
      return dlists;
    } catch (error) {
      return [];
    }
  }

  /**
   * 提取水平分隔线位置
   * @param {Page} page - Playwright页面对象
   * @returns {Promise<number>} 水平线数量
   */
  async extractHorizontalRules(page) {
    try {
      const count = await page.evaluate(() => {
        return document.querySelectorAll('hr').length;
      });
      return count;
    } catch (error) {
      return 0;
    }
  }

  /**
   * 提取视频
   * @param {Page} page - Playwright页面对象
   * @returns {Promise<Array>} 视频数组
   */
  async extractVideos(page) {
    try {
      const videos = await page.evaluate(() => {
        const elements = document.querySelectorAll('video');
        return Array.from(elements).map(video => ({
          src: video.src || (video.querySelector('source') ? video.querySelector('source').src : ''),
          poster: video.poster || '',
          width: video.width || '',
          height: video.height || ''
        })).filter(v => v.src);
      });
      return videos;
    } catch (error) {
      return [];
    }
  }

  /**
   * 提取音频
   * @param {Page} page - Playwright页面对象
   * @returns {Promise<Array>} 音频数组
   */
  async extractAudios(page) {
    try {
      const audios = await page.evaluate(() => {
        const elements = document.querySelectorAll('audio');
        return Array.from(elements).map(audio => ({
          src: audio.src || (audio.querySelector('source') ? audio.querySelector('source').src : '')
        })).filter(a => a.src);
      });
      return audios;
    } catch (error) {
      return [];
    }
  }

  /**
   * 提取主内容区域的混排内容（保持原始顺序）
   * @param {Page} page - Playwright页面对象
   * @param {string} filepath - 输出文件路径
   * @param {string} pagesDir - 页面目录
   * @returns {Promise<Array>} 按顺序的内容数组
   */
  async extractMainContentWithOrder(page, filepath, pagesDir) {
    try {
      const fs = await import('fs');
      const path = await import('path');
      const https = await import('https');
      const http = await import('http');
      
      // 获取基础文件名
      const baseFilename = filepath ? path.basename(filepath, '.md') : 'content';
      const contentDir = path.join(pagesDir, baseFilename);
      if (!fs.existsSync(contentDir)) {
        fs.mkdirSync(contentDir, { recursive: true });
      }
      
      const content = await page.evaluate(() => {
        // 查找主内容区域
        const main = document.querySelector('main') || 
                     document.querySelector('article') || 
                     document.querySelector('[role="main"]') ||
                     document.querySelector('#content') ||
                     document.querySelector('.content') ||
                     document.body;
        
        const result = [];
        let imageIndex = 0;
        
        // 处理节点，保留格式
        const processTextNode = (node) => {
          let text = '';
          
          if (node.nodeType === Node.TEXT_NODE) {
            text += node.textContent;
          } else if (node.nodeType === Node.ELEMENT_NODE) {
            const tag = node.tagName;
            const nodeText = node.textContent.trim();
            
            if (tag === 'A' && node.href) {
              text += `[${nodeText}](${node.href})`;
            } else if ((tag === 'STRONG' || tag === 'B') && nodeText) {
              text += `**${nodeText}**`;
            } else if ((tag === 'EM' || tag === 'I') && nodeText) {
              text += `*${nodeText}*`;
            } else if ((tag === 'DEL' || tag === 'S' || tag === 'STRIKE') && nodeText) {
              text += `~~${nodeText}~~`;
            } else if (tag === 'CODE' && nodeText) {
              text += `\`${nodeText}\``;
            } else if (tag === 'BR') {
              text += '  \n';
            } else {
              Array.from(node.childNodes).forEach(child => {
                text += processTextNode(child);
              });
            }
          }
          
          return text;
        };
        
        // 遍历主内容区域的所有子元素
        const processElement = (element) => {
          const tag = element.tagName;
          
          // 段落
          if (tag === 'P') {
            let text = '';
            Array.from(element.childNodes).forEach(node => {
              text += processTextNode(node);
            });
            text = text.trim();
            if (text) {
              result.push({ type: 'paragraph', content: text });
            }
          }
          // 标题
          else if (/^H[1-6]$/.test(tag)) {
            let text = '';
            Array.from(element.childNodes).forEach(node => {
              text += processTextNode(node);
            });
            result.push({ 
              type: 'heading', 
              level: parseInt(tag[1]), 
              content: text.trim() 
            });
          }
          // 图片
          else if (tag === 'IMG') {
            imageIndex++;
            result.push({
              type: 'image',
              src: element.src,
              alt: element.alt || '',
              title: element.title || '',
              index: imageIndex
            });
          }
          // 列表
          else if (tag === 'UL' || tag === 'OL') {
            const items = [];
            Array.from(element.querySelectorAll('li')).forEach(li => {
              let text = '';
              Array.from(li.childNodes).forEach(node => {
                text += processTextNode(node);
              });
              text = text.trim();
              if (text) {
                items.push(text);
              }
            });
            if (items.length > 0) {
              result.push({
                type: 'list',
                listType: tag.toLowerCase(),
                items
              });
            }
          }
          // 引用块
          else if (tag === 'BLOCKQUOTE') {
            result.push({
              type: 'blockquote',
              content: element.textContent.trim()
            });
          }
          // 代码块
          else if (tag === 'PRE') {
            const code = element.querySelector('code');
            result.push({
              type: 'codeblock',
              language: code ? (code.className.match(/language-(\w+)/) || ['', ''])[1] : '',
              content: element.textContent.trim()
            });
          }
          // 水平线
          else if (tag === 'HR') {
            result.push({ type: 'hr' });
          }
          // 表格（简单提取）
          else if (tag === 'TABLE') {
            const headers = [];
            const rows = [];
            
            element.querySelectorAll('thead th, thead td').forEach(cell => {
              headers.push(cell.textContent.trim());
            });
            
            element.querySelectorAll('tbody tr, tr').forEach((row, idx) => {
              if (idx === 0 && headers.length === 0) return;
              const cells = Array.from(row.querySelectorAll('td, th')).map(cell => cell.textContent.trim());
              if (cells.length > 0) {
                rows.push(cells);
              }
            });
            
            if (headers.length > 0 || rows.length > 0) {
              result.push({
                type: 'table',
                headers,
                rows
              });
            }
          }
          // 递归处理子元素（对于div等容器）
          else if (tag === 'DIV' || tag === 'SECTION' || tag === 'ARTICLE') {
            Array.from(element.children).forEach(child => {
              processElement(child);
            });
          }
        };
        
        // 处理主内容区域的所有直接子元素
        Array.from(main.children).forEach(child => {
          processElement(child);
        });
        
        return result;
      });
      
      // 下载图片
      for (const item of content) {
        if (item.type === 'image' && item.src && !item.src.startsWith('data:')) {
          try {
            const urlObj = new URL(item.src);
            let ext = path.extname(urlObj.pathname) || '.jpg';
            if (!ext.match(/\.(jpg|jpeg|png|gif|webp|svg)$/i)) {
              ext = '.jpg';
            }
            
            const localFilename = `image_${item.index}${ext}`;
            const localPath = path.join(contentDir, localFilename);
            
            await new Promise((resolve) => {
              const protocol = item.src.startsWith('https') ? https : http;
              const file = fs.createWriteStream(localPath);
              
              protocol.get(item.src, (response) => {
                if (response.statusCode === 200) {
                  response.pipe(file);
                  file.on('finish', () => {
                    file.close();
                    resolve();
                  });
                } else {
                  file.close();
                  fs.unlinkSync(localPath);
                  resolve();
                }
              }).on('error', () => {
                file.close();
                if (fs.existsSync(localPath)) {
                  fs.unlinkSync(localPath);
                }
                resolve();
              });
            });
            
            item.localPath = `${baseFilename}/${localFilename}`;
          } catch (error) {
            console.error(`Error downloading image ${item.src}:`, error.message);
          }
        }
      }
      
      return content;
    } catch (error) {
      console.error('Failed to extract main content with order:', error.message);
      return [];
    }
  }

  /**
   * 点击所有"更多/展开/查看全部"按钮
   * @param {Page} page - Playwright页面对象
   * @returns {Promise<number>} 点击的按钮数量
   */
  async clickAllExpandButtons(page) {
    try {
      const buttonTexts = [
        '更多', '展开', '查看全部', '加载更多', '全部', '历史', '明细',
        'More', 'Expand', 'Show All', 'Load More', 'View All'
      ];
      
      let totalClicked = 0;
      let clicked = true;
      let maxClicks = 50; // 防止无限循环
      
      console.log('  查找并点击展开按钮...');
      
      while (clicked && maxClicks > 0) {
        clicked = false;
        
        for (const text of buttonTexts) {
          try {
            // 查找包含该文本的按钮或链接
            const buttons = await page.locator(`button:has-text("${text}"), a:has-text("${text}"), [class*="more"]:has-text("${text}"), [class*="expand"]:has-text("${text}")`).all();
            
            for (const button of buttons) {
              try {
                // 检查按钮是否可见且可点击
                const isVisible = await button.isVisible();
                if (!isVisible) continue;
                
                const isDisabled = await button.evaluate(el => {
                  return el.disabled || 
                         el.classList.contains('disabled') ||
                         el.getAttribute('aria-disabled') === 'true' ||
                         el.style.display === 'none';
                });
                
                if (isDisabled) continue;
                
                // 点击按钮
                await button.click();
                await page.waitForTimeout(800);
                
                clicked = true;
                totalClicked++;
                maxClicks--;
                
                console.log(`    ✓ 点击了"${text}"按钮 (${totalClicked})`);
                
                // 每点击一个按钮就跳出内层循环，重新查找
                break;
              } catch (e) {
                // 单个按钮点击失败，继续尝试下一个
                continue;
              }
            }
            
            if (clicked) break; // 如果点击了按钮，跳出文本循环，重新开始
          } catch (e) {
            // 查找失败，继续下一个文本
            continue;
          }
        }
      }
      
      if (totalClicked > 0) {
        console.log(`  ✓ 共点击了 ${totalClicked} 个展开按钮`);
        // 等待内容加载完成
        await page.waitForTimeout(2000);
      }
      
      return totalClicked;
    } catch (error) {
      console.error('Error clicking expand buttons:', error.message);
      return 0;
    }
  }

  /**
   * 处理无限滚动加载（增强版）
   * @param {Page} page - Playwright页面对象
   * @returns {Promise<void>}
   */
  async handleInfiniteScrollEnhanced(page) {
    try {
      console.log('  处理无限滚动...');
      
      // 1. 识别滚动容器
      const scrollContainer = await this.findScrollContainer(page);
      
      const maxScrolls = 30;
      const scrollTimeout = 60000;
      const startTime = Date.now();
      
      let scrollCount = 0;
      let previousHash = '';
      let noChangeCount = 0;
      
      while (scrollCount < maxScrolls && noChangeCount < 3) {
        if (Date.now() - startTime > scrollTimeout) {
          console.log('    滚动超时');
          break;
        }
        
        // 2. 混合模式：先尝试点击"加载更多"按钮
        const loadMoreClicked = await this.clickLoadMoreButton(page);
        if (loadMoreClicked) {
          await page.waitForTimeout(1500);
        }
        
        // 3. 滚动（容器或window）
        if (scrollContainer) {
          await page.evaluate(() => {
            const container = document.querySelector('[class*="scroll"], [class*="list"], [style*="overflow"]');
            if (container) {
              container.scrollTop = container.scrollHeight;
            }
          });
        } else {
          await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
        }
        
        scrollCount++;
        await page.waitForTimeout(2000);
        
        // 4. 检查内容变化（使用hash）
        const currentHash = await page.evaluate(() => {
          const content = document.body.innerText;
          return content.length + '_' + content.slice(-200);
        });
        
        if (currentHash === previousHash) {
          noChangeCount++;
        } else {
          noChangeCount = 0;
          previousHash = currentHash;
        }
        
        // 5. 检查"没有更多"提示
        const hasNoMore = await page.evaluate(() => {
          const noMoreTexts = ['没有更多', 'no more', '已经到底', '暂无更多', '全部加载完成', 'end of list', '到底了'];
          const bodyText = document.body.textContent.toLowerCase();
          return noMoreTexts.some(text => bodyText.includes(text.toLowerCase()));
        });
        
        if (hasNoMore) {
          console.log('    检测到"没有更多"提示');
          break;
        }
      }
      
      if (scrollCount > 0) {
        console.log(`    ✓ 滚动了 ${scrollCount} 次`);
        // 滚动回顶部
        await page.evaluate(() => window.scrollTo(0, 0));
        await page.waitForTimeout(1000);
      }
      
    } catch (error) {
      console.error('Error handling infinite scroll:', error.message);
    }
  }

  /**
   * 查找滚动容器
   * @param {Page} page - Playwright页面对象
   * @returns {Promise<boolean>} 是否找到滚动容器
   */
  async findScrollContainer(page) {
    try {
      const hasContainer = await page.evaluate(() => {
        const selectors = [
          '[class*="scroll-container"]',
          '[class*="list-container"]',
          '[class*="table-container"]',
          '[style*="overflow: auto"]',
          '[style*="overflow: scroll"]',
          '[style*="overflow-y: auto"]',
          '[style*="overflow-y: scroll"]'
        ];
        
        for (const selector of selectors) {
          const el = document.querySelector(selector);
          if (el && el.scrollHeight > el.clientHeight) {
            return true;
          }
        }
        return false;
      });
      
      return hasContainer;
    } catch (error) {
      return false;
    }
  }

  /**
   * 点击"加载更多"按钮
   * @param {Page} page - Playwright页面对象
   * @returns {Promise<boolean>} 是否成功点击
   */
  async clickLoadMoreButton(page) {
    try {
      const buttonTexts = ['加载更多', '查看更多', 'Load More', 'Show More', '更多'];
      
      for (const text of buttonTexts) {
        try {
          const button = page.locator(`button:has-text("${text}"), a:has-text("${text}")`).first();
          const count = await button.count();
          
          if (count > 0) {
            const isVisible = await button.isVisible();
            if (isVisible) {
              await button.click();
              return true;
            }
          }
        } catch (e) {
          continue;
        }
      }
      
      return false;
    } catch (error) {
      return false;
    }
  }

  /**
   * 提取运行时图表数据（ECharts/Highcharts）
   * @param {Page} page - Playwright页面对象
   * @returns {Promise<Array>} 图表数据数组
   */
  async extractChartData(page) {
    try {
      console.log('  提取运行时图表数据...');
      
      const chartData = await page.evaluate(() => {
        const data = [];
        
        // 1. ECharts
        if (window.echarts) {
          try {
            // 查找所有ECharts实例
            const echartsElements = document.querySelectorAll('[_echarts_instance_]');
            echartsElements.forEach((el, index) => {
              try {
                const instance = window.echarts.getInstanceByDom(el);
                if (instance) {
                  const option = instance.getOption();
                  if (option) {
                    data.push({
                      type: 'echarts',
                      index: index + 1,
                      title: option.title ? option.title[0]?.text || '' : '',
                      series: option.series || [],
                      xAxis: option.xAxis || [],
                      yAxis: option.yAxis || [],
                      legend: option.legend || {},
                      tooltip: option.tooltip || {}
                    });
                  }
                }
              } catch (e) {
                // 忽略单个实例的错误
              }
            });
          } catch (e) {
            // ECharts不可用或出错
          }
        }
        
        // 2. Highcharts
        if (window.Highcharts && window.Highcharts.charts) {
          try {
            window.Highcharts.charts.forEach((chart, index) => {
              if (chart) {
                try {
                  data.push({
                    type: 'highcharts',
                    index: index + 1,
                    title: chart.title ? chart.title.textStr : '',
                    series: chart.series.map(s => ({
                      name: s.name,
                      type: s.type,
                      data: s.data.map(p => {
                        if (p && typeof p === 'object') {
                          return { x: p.x, y: p.y, name: p.name };
                        }
                        return p;
                      })
                    })),
                    xAxis: chart.xAxis ? chart.xAxis.map(x => ({
                      categories: x.categories,
                      type: x.type
                    })) : [],
                    yAxis: chart.yAxis ? chart.yAxis.map(y => ({
                      title: y.axisTitle ? y.axisTitle.textStr : '',
                      type: y.type
                    })) : []
                  });
                } catch (e) {
                  // 忽略单个图表的错误
                }
              }
            });
          } catch (e) {
            // Highcharts不可用或出错
          }
        }
        
        // 3. Chart.js
        if (window.Chart && window.Chart.instances) {
          try {
            Object.values(window.Chart.instances).forEach((chart, index) => {
              if (chart && chart.config) {
                try {
                  data.push({
                    type: 'chartjs',
                    index: index + 1,
                    chartType: chart.config.type,
                    data: chart.config.data,
                    options: chart.config.options
                  });
                } catch (e) {
                  // 忽略单个图表的错误
                }
              }
            });
          } catch (e) {
            // Chart.js不可用或出错
          }
        }
        
        return data;
      });
      
      if (chartData.length > 0) {
        console.log(`    ✓ 提取了 ${chartData.length} 个图表的运行时数据`);
      }
      
      return chartData;
    } catch (error) {
      console.error('Error extracting chart data:', error.message);
      return [];
    }
  }

  /**
   * 提取表格（支持分页和虚拟表格）
   * @param {Page} page - Playwright页面对象
   * @param {Function} onDataChunk - 数据块回调函数
   * @returns {Promise<Array>} 表格数组
   */
  async extractTablesWithPaginationAndVirtual(page, onDataChunk) {
    try {
      const tables = [];
      const tableElements = await page.locator('table').all();
      
      for (let tableIndex = 0; tableIndex < tableElements.length; tableIndex++) {
        const tableEl = tableElements[tableIndex];
        
        // 检测是否为虚拟表格
        const isVirtual = await this.detectVirtualTable(page, tableEl);
        
        if (isVirtual) {
          console.log(`  检测到虚拟表格 ${tableIndex + 1}，使用虚拟表格提取模式`);
          const virtualTableData = await this.extractVirtualTable(page, tableEl, tableIndex, onDataChunk);
          tables.push(virtualTableData);
        } else {
          // 使用原有的分页表格提取逻辑
          const tableInfo = await this.extractSingleTable(tableEl, tableIndex);
          const paginationInfo = await this.findPaginationControls(page, tableEl);
          
          if (paginationInfo.hasPagination) {
            // 分页表格处理（原有逻辑）
            const paginatedTable = await this.extractPaginatedTable(page, tableEl, tableIndex, tableInfo, paginationInfo, onDataChunk);
            tables.push(paginatedTable);
          } else {
            // 无分页，直接添加
            tables.push(tableInfo);
            
            if (onDataChunk) {
              await onDataChunk({
                type: 'table',
                tableIndex,
                page: 1,
                headers: tableInfo.headers,
                rows: tableInfo.rows,
                isFirstPage: true,
                isLastPage: true
              });
            }
          }
        }
      }
      
      return tables;
    } catch (error) {
      console.error('Failed to extract tables:', error.message);
      return [];
    }
  }

  /**
   * 检测是否为虚拟表格
   * @param {Page} page - Playwright页面对象
   * @param {Locator} tableEl - 表格元素
   * @returns {Promise<boolean>} 是否为虚拟表格
   */
  async detectVirtualTable(page, tableEl) {
    try {
      const virtualIndicators = await tableEl.evaluate((table) => {
        const indicators = {
          hasDataId: false,
          hasAriaRowIndex: false,
          hasVirtualClass: false,
          hasScrollParent: false,
          rowCountLow: false
        };
        
        // 1. 检查是否有data-id或aria-rowindex属性
        const rows = table.querySelectorAll('tr');
        if (rows.length > 0) {
          const firstRow = rows[0];
          indicators.hasDataId = !!firstRow.getAttribute('data-id') || 
                                 !!firstRow.getAttribute('data-key') ||
                                 !!firstRow.getAttribute('data-row-key');
          indicators.hasAriaRowIndex = !!firstRow.getAttribute('aria-rowindex');
        }
        
        // 2. 检查是否有虚拟列表相关的class
        const virtualClasses = ['virtual', 'virtualized', 'react-window', 'react-virtualized'];
        const tableClasses = table.className.toLowerCase();
        indicators.hasVirtualClass = virtualClasses.some(cls => tableClasses.includes(cls));
        
        // 3. 检查父元素是否有滚动容器
        let parent = table.parentElement;
        let depth = 0;
        while (parent && depth < 5) {
          const style = window.getComputedStyle(parent);
          const overflow = style.overflow + style.overflowY;
          if (overflow.includes('auto') || overflow.includes('scroll')) {
            // 检查是否真的可滚动
            if (parent.scrollHeight > parent.clientHeight) {
              indicators.hasScrollParent = true;
              break;
            }
          }
          parent = parent.parentElement;
          depth++;
        }
        
        // 4. 检查行数是否异常少（可能是虚拟表格只渲染可见行）
        const bodyRows = table.querySelectorAll('tbody tr');
        indicators.rowCountLow = bodyRows.length > 0 && bodyRows.length < 50;
        
        return indicators;
      });
      
      // 判断逻辑：满足以下任一条件即认为是虚拟表格
      // 1. 有data-id或aria-rowindex（强特征）
      // 2. 有虚拟列表class（强特征）
      // 3. 有滚动父容器 + 行数少（弱特征组合）
      const isVirtual = 
        virtualIndicators.hasDataId ||
        virtualIndicators.hasAriaRowIndex ||
        virtualIndicators.hasVirtualClass ||
        (virtualIndicators.hasScrollParent && virtualIndicators.rowCountLow);
      
      return isVirtual;
    } catch (error) {
      return false;
    }
  }

  /**
   * 提取虚拟表格数据
   * @param {Page} page - Playwright页面对象
   * @param {Locator} tableEl - 表格元素
   * @param {number} tableIndex - 表格索引
   * @param {Function} onDataChunk - 数据块回调
   * @returns {Promise<Object>} 表格数据
   */
  async extractVirtualTable(page, tableEl, tableIndex, onDataChunk) {
    try {
      console.log(`    开始提取虚拟表格数据...`);
      
      // 提取表头
      const headers = await this.extractTableHeaders(tableEl);
      
      // 查找滚动容器
      const scrollContainer = await this.findTableScrollContainer(page, tableEl);
      
      // 使用Map存储数据，按主键去重
      const recordsMap = new Map();
      let noNewRecords = 0;
      let scrollPosition = 0;
      const scrollStep = 300; // 小步长滚动
      const maxNoNewCount = 5; // 连续5次没有新数据就停止
      const maxScrolls = 200; // 最多滚动200次
      let scrollCount = 0;
      
      while (noNewRecords < maxNoNewCount && scrollCount < maxScrolls) {
        // 提取当前可见行
        const currentRows = await this.extractVisibleRows(tableEl);
        let newCount = 0;
        
        for (const row of currentRows) {
          const rowKey = row.key;
          
          if (!recordsMap.has(rowKey)) {
            recordsMap.set(rowKey, row.cells);
            newCount++;
          }
        }
        
        if (newCount === 0) {
          noNewRecords++;
        } else {
          noNewRecords = 0;
          console.log(`      已收集 ${recordsMap.size} 行数据 (+${newCount})`);
        }
        
        // 滚动
        scrollPosition += scrollStep;
        
        if (scrollContainer) {
          // 滚动容器
          await page.evaluate((pos) => {
            const container = document.querySelector('[class*="scroll"], [class*="table"], [style*="overflow"]');
            if (container) {
              container.scrollTop = pos;
            }
          }, scrollPosition);
        } else {
          // 滚动表格本身或其父元素
          await tableEl.evaluate((table, pos) => {
            let scrollTarget = table;
            let parent = table.parentElement;
            let depth = 0;
            
            // 查找可滚动的父元素
            while (parent && depth < 5) {
              const style = window.getComputedStyle(parent);
              const overflow = style.overflow + style.overflowY;
              if ((overflow.includes('auto') || overflow.includes('scroll')) && 
                  parent.scrollHeight > parent.clientHeight) {
                scrollTarget = parent;
                break;
              }
              parent = parent.parentElement;
              depth++;
            }
            
            scrollTarget.scrollTop = pos;
          }, scrollPosition);
        }
        
        await page.waitForTimeout(300); // 等待渲染
        scrollCount++;
        
        // 检查是否到底
        const isAtBottom = await this.checkScrollAtBottom(page, tableEl);
        if (isAtBottom && noNewRecords > 0) {
          console.log(`      已滚动到底部`);
          break;
        }
      }
      
      const allRows = Array.from(recordsMap.values());
      
      console.log(`    ✓ 虚拟表格提取完成: ${allRows.length} 行数据`);
      
      // 发送数据块
      if (onDataChunk) {
        await onDataChunk({
          type: 'table',
          tableIndex,
          page: 1,
          headers,
          rows: allRows,
          isFirstPage: true,
          isLastPage: true,
          isVirtual: true,
          totalRows: allRows.length
        });
      }
      
      return {
        index: tableIndex,
        headers,
        rows: allRows,
        caption: '',
        isVirtual: true,
        totalRows: allRows.length
      };
    } catch (error) {
      console.error('Error extracting virtual table:', error.message);
      // 降级到普通提取
      return await this.extractSingleTable(tableEl, tableIndex);
    }
  }

  /**
   * 提取表格表头
   * @param {Locator} tableEl - 表格元素
   * @returns {Promise<Array>} 表头数组
   */
  async extractTableHeaders(tableEl) {
    try {
      const headers = await tableEl.evaluate((table) => {
        const headerCells = table.querySelectorAll('thead th, thead td');
        if (headerCells.length > 0) {
          return Array.from(headerCells).map(cell => cell.textContent.trim());
        }
        
        const firstRow = table.querySelector('tr');
        if (firstRow) {
          const cells = firstRow.querySelectorAll('th, td');
          return Array.from(cells).map(cell => cell.textContent.trim());
        }
        
        return [];
      });
      
      return headers;
    } catch (error) {
      return [];
    }
  }

  /**
   * 提取当前可见的表格行
   * @param {Locator} tableEl - 表格元素
   * @returns {Promise<Array>} 行数据数组
   */
  async extractVisibleRows(tableEl) {
    try {
      const rows = await tableEl.evaluate((table) => {
        const bodyRows = table.querySelectorAll('tbody tr');
        const rowsToProcess = bodyRows.length > 0 ? bodyRows : table.querySelectorAll('tr');
        
        const result = [];
        
        rowsToProcess.forEach((row, index) => {
          // 跳过表头行
          if (row.querySelector('th') && !row.querySelector('td')) {
            return;
          }
          
          // 提取主键（优先级：data-id > data-key > aria-rowindex > 首列文本 > 行索引）
          let rowKey = row.getAttribute('data-id') ||
                       row.getAttribute('data-key') ||
                       row.getAttribute('data-row-key') ||
                       row.getAttribute('aria-rowindex');
          
          if (!rowKey) {
            // 使用首列文本作为主键
            const firstCell = row.querySelector('td');
            if (firstCell) {
              rowKey = firstCell.textContent.trim();
            }
          }
          
          if (!rowKey) {
            // 最后使用行索引
            rowKey = `row_${index}`;
          }
          
          // 提取单元格数据
          const cells = Array.from(row.querySelectorAll('td, th'));
          const cellData = cells.map(cell => cell.textContent.trim());
          
          if (cellData.length > 0) {
            result.push({
              key: rowKey,
              cells: cellData
            });
          }
        });
        
        return result;
      });
      
      return rows;
    } catch (error) {
      return [];
    }
  }

  /**
   * 查找表格的滚动容器
   * @param {Page} page - Playwright页面对象
   * @param {Locator} tableEl - 表格元素
   * @returns {Promise<boolean>} 是否找到滚动容器
   */
  async findTableScrollContainer(page, tableEl) {
    try {
      const hasContainer = await tableEl.evaluate((table) => {
        let parent = table.parentElement;
        let depth = 0;
        
        while (parent && depth < 5) {
          const style = window.getComputedStyle(parent);
          const overflow = style.overflow + style.overflowY;
          
          if ((overflow.includes('auto') || overflow.includes('scroll')) && 
              parent.scrollHeight > parent.clientHeight) {
            return true;
          }
          
          parent = parent.parentElement;
          depth++;
        }
        
        return false;
      });
      
      return hasContainer;
    } catch (error) {
      return false;
    }
  }

  /**
   * 检查是否滚动到底部
   * @param {Page} page - Playwright页面对象
   * @param {Locator} tableEl - 表格元素
   * @returns {Promise<boolean>} 是否到底
   */
  async checkScrollAtBottom(page, tableEl) {
    try {
      const isAtBottom = await tableEl.evaluate((table) => {
        let scrollTarget = table;
        let parent = table.parentElement;
        let depth = 0;
        
        // 查找可滚动的父元素
        while (parent && depth < 5) {
          const style = window.getComputedStyle(parent);
          const overflow = style.overflow + style.overflowY;
          if ((overflow.includes('auto') || overflow.includes('scroll')) && 
              parent.scrollHeight > parent.clientHeight) {
            scrollTarget = parent;
            break;
          }
          parent = parent.parentElement;
          depth++;
        }
        
        // 检查是否到底（允许5px的误差）
        const scrollTop = scrollTarget.scrollTop;
        const scrollHeight = scrollTarget.scrollHeight;
        const clientHeight = scrollTarget.clientHeight;
        
        return scrollTop + clientHeight >= scrollHeight - 5;
      });
      
      return isAtBottom;
    } catch (error) {
      return false;
    }
  }

  /**
   * 提取分页表格（原有逻辑提取为独立方法）
   * @param {Page} page - Playwright页面对象
   * @param {Locator} tableEl - 表格元素
   * @param {number} tableIndex - 表格索引
   * @param {Object} tableInfo - 表格基本信息
   * @param {Object} paginationInfo - 分页信息
   * @param {Function} onDataChunk - 数据块回调
   * @returns {Promise<Object>} 表格数据
   */
  async extractPaginatedTable(page, tableEl, tableIndex, tableInfo, paginationInfo, onDataChunk) {
    const allRows = [...tableInfo.rows];
    let currentPage = 1;
    const maxPages = paginationInfo.totalPages || 100;
    
    // 发送第一页数据
    if (onDataChunk) {
      await onDataChunk({
        type: 'table',
        tableIndex,
        page: currentPage,
        headers: tableInfo.headers,
        rows: tableInfo.rows,
        isFirstPage: true,
        isLastPage: false
      });
    }
    
    // 翻页并提取数据
    while (currentPage < maxPages) {
      const hasNextPage = await this.clickNextPage(page, paginationInfo);
      
      if (!hasNextPage) {
        break;
      }
      
      currentPage++;
      await page.waitForTimeout(1000);
      
      // 提取当前页的表格数据
      const currentTableEl = (await page.locator('table').all())[tableIndex];
      const currentPageData = await this.extractSingleTable(currentTableEl, tableIndex);
      
      // 检查表格结构是否一致
      const headersMatch = this.compareHeaders(tableInfo.headers, currentPageData.headers);
      
      if (headersMatch) {
        allRows.push(...currentPageData.rows);
        
        if (onDataChunk) {
          await onDataChunk({
            type: 'table',
            tableIndex,
            page: currentPage,
            headers: currentPageData.headers,
            rows: currentPageData.rows,
            isFirstPage: false,
            isLastPage: false
          });
        }
      } else {
        break;
      }
      
      await page.waitForTimeout(500);
    }
    
    // 发送最后一页标记
    if (onDataChunk) {
      await onDataChunk({
        type: 'table',
        tableIndex,
        page: currentPage,
        headers: tableInfo.headers,
        rows: [],
        isFirstPage: false,
        isLastPage: true
      });
    }
    
    return {
      index: tableIndex,
      headers: tableInfo.headers,
      rows: allRows,
      caption: tableInfo.caption,
      totalPages: currentPage
    };
  }
}

export default GenericParser;
