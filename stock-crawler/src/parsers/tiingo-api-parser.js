import BaseParser from './base-parser.js';

/**
 * Tiingo API Parser - 专门解析 tiingo.com/documentation 文档页面
 * Tiingo 提供股票、基金、加密货币等金融数据 API
 * Tiingo 文档是 Angular SPA，使用交替的 section-header 和 documentation-body 结构
 * 注意: Tiingo 的侧边栏导航使用 Angular 点击事件而非 href/routerLink
 */
class TiingoApiParser extends BaseParser {
  /**
   * 匹配 Tiingo API 文档页面
   * @param {string} url - 页面URL
   * @returns {boolean} 是否匹配
   */
  matches(url) {
    return /^https?:\/\/www\.tiingo\.com\/documentation/.test(url);
  }

  /**
   * 获取优先级
   * @returns {number} 优先级
   */
  getPriority() {
    return 100;
  }

  /**
   * 是否支持链接发现
   * @returns {boolean}
   */
  supportsLinkDiscovery() {
    return true;
  }

  /**
   * 从 Tiingo 侧边栏提取所有文档链接
   * Tiingo 使用 Angular Material sidenav，链接通过点击事件触发导航
   * @param {Page} page - Playwright页面对象
   * @returns {Promise<string[]>} 发现的URL列表
   */
  async discoverLinks(page) {
    const discoveredUrls = new Set();
    const currentUrl = page.url();

    try {
      // 等待侧边栏加载
      await page.waitForSelector('.side-bar-link-container', { timeout: 5000 });

      // 获取所有侧边栏项目的数量
      const itemCount = await page.evaluate(() => {
        return document.querySelectorAll('.side-bar-link-container').length;
      });

      console.log(`[TiingoParser] Found ${itemCount} sidebar items`);

      // 点击每个侧边栏项目并记录 URL
      for (let i = 0; i < itemCount; i++) {
        try {
          // 每次重新获取元素（因为导航会改变 DOM）
          const items = await page.$$('.side-bar-link-container');
          if (i >= items.length) break;

          const item = items[i];
          const text = await item.evaluate(el => el.textContent?.trim());

          // 点击项目
          await item.click();
          await page.waitForTimeout(500);

          // 获取当前 URL
          const newUrl = page.url();
          if (newUrl.includes('/documentation/') && newUrl !== currentUrl) {
            discoveredUrls.add(newUrl);
          }
        } catch (e) {
          // 忽略单个项目的错误
        }
      }

      // 导航回原始 URL
      if (page.url() !== currentUrl) {
        await page.goto(currentUrl);
        await this.waitForContent(page);
      }
    } catch (error) {
      console.warn('[TiingoParser] Link discovery failed:', error.message);
    }

    return Array.from(discoveredUrls);
  }

  /**
   * 根据 URL 生成有意义的文件名
   * @param {string} url - 页面URL
   * @returns {string} 文件名
   */
  generateFilename(url) {
    try {
      const urlObj = new URL(url);
      let pathname = urlObj.pathname;
      // 移除 /documentation 前缀
      pathname = pathname.replace(/^\/documentation\/?/, '');
      pathname = pathname.replace(/\/$/, '');
      const filename = pathname.replace(/\//g, '_') || 'overview';
      return filename;
    } catch (e) {
      return 'api_doc';
    }
  }

  /**
   * 从 URL 提取文档路径
   * @param {string} url - 页面URL
   * @returns {string} 文档路径
   */
  extractDocPath(url) {
    try {
      const urlObj = new URL(url);
      let pathname = urlObj.pathname;
      pathname = pathname.replace(/^\/documentation\/?/, '');
      return pathname;
    } catch (e) {
      return '';
    }
  }

  /**
   * 解析 Tiingo API 文档页面
   * @param {Page} page - Playwright页面对象
   * @param {string} url - 页面URL
   * @param {Object} options - 解析选项
   * @returns {Promise<Object>} 解析后的页面数据
   */
  async parse(page, url, options = {}) {
    try {
      // 等待页面加载完成
      await this.waitForContent(page);

      // 从 URL 提取文档路径
      const docPath = this.extractDocPath(url);

      // 先提取基本内容（不包括 tab 内容）
      const data = await page.evaluate((targetPath) => {
        const result = {
          title: '',
          description: '',
          sections: [],
          codeExamples: [],
          tables: [],
          rawContent: ''
        };

        // Tiingo 使用 .documentation-container 作为主要内容容器
        const docContainer = document.querySelector('.documentation-container');
        if (!docContainer) {
          // 回退到 tiingo-canvas-wrapper
          const wrapper = document.querySelector('.tiingo-canvas-wrapper');
          if (wrapper) {
            result.rawContent = wrapper.innerText;
            result.title = document.title;
          }
          return result;
        }

        // 提取所有 section-header 和 documentation-body 对
        const headers = docContainer.querySelectorAll('.documentation-section-header');
        const bodies = docContainer.querySelectorAll('.documentation-body');

        // 将 header 和 body 配对
        headers.forEach((header, index) => {
          const h2 = header.querySelector('h2');
          const title = h2 ? h2.textContent.trim() : `Section ${index + 1}`;

          // 获取对应的 body
          let body = null;
          let nextEl = header.nextElementSibling;
          if (nextEl && nextEl.classList.contains('documentation-body')) {
            body = nextEl;
          } else {
            body = bodies[index];
          }

          const sectionContent = [];

          if (body) {
            // 提取 body 中的内容
            const paragraphs = body.querySelectorAll('p');
            paragraphs.forEach(p => {
              const text = p.textContent.trim();
              if (text) {
                sectionContent.push({ type: 'text', content: text });
              }
            });

            // 提取 h3 标题
            const h3s = body.querySelectorAll('h3');
            h3s.forEach(h3 => {
              sectionContent.push({ type: 'heading', content: h3.textContent.trim() });
            });

            // 提取标准表格
            const tables = body.querySelectorAll('table');
            tables.forEach(table => {
              const rows = [];
              table.querySelectorAll('tr').forEach(tr => {
                const cells = Array.from(tr.querySelectorAll('th, td')).map(c => c.textContent.trim());
                if (cells.length > 0) rows.push(cells);
              });
              if (rows.length > 0) {
                sectionContent.push({ type: 'table', data: rows });
              }
            });

            // 提取 Tiingo 自定义的参数表格 (.parameter-table)
            const paramTables = body.querySelectorAll('.parameter-table');
            paramTables.forEach(paramTable => {
              const rows = [];
              // 获取表头
              const headerRow = paramTable.querySelector('.header-row');
              if (headerRow) {
                const headers = Array.from(headerRow.querySelectorAll('.header-cell')).map(cell => cell.textContent.trim());
                if (headers.length > 0) rows.push(headers);
              }
              // 获取数据行
              const paramRows = paramTable.querySelectorAll('.parameter-row');
              paramRows.forEach(row => {
                const name = row.querySelector('.parameter-cell.name');
                const jsonField = row.querySelector('.parameter-cell.json-field');
                const type = row.querySelector('.parameter-cell.type');
                const description = row.querySelector('.parameter-cell.description');
                const rowData = [
                  name ? name.textContent.trim() : '',
                  jsonField ? jsonField.textContent.trim() : '',
                  type ? type.textContent.trim() : '',
                  description ? description.textContent.trim() : ''
                ];
                if (rowData.some(cell => cell)) rows.push(rowData);
              });
              if (rows.length > 1) {
                sectionContent.push({ type: 'table', data: rows });
              }
            });

            // 提取代码块 - 但排除 parameter-table 内的 pre 元素
            const codeBlocks = body.querySelectorAll('pre, code');
            codeBlocks.forEach(block => {
              if (block.closest('.parameter-table')) {
                return;
              }
              const code = block.textContent.trim();
              if (code && code.length > 10) {
                sectionContent.push({ type: 'code', content: code });
                result.codeExamples.push(code);
              }
            });

            // 提取列表
            const lists = body.querySelectorAll('ul, ol');
            lists.forEach(list => {
              const items = Array.from(list.querySelectorAll('li')).map(li => li.textContent.trim());
              sectionContent.push({ type: 'list', items });
            });
          }

          result.sections.push({ title, content: sectionContent });

          if (index === 0) {
            result.title = title;
            const firstText = sectionContent.find(c => c.type === 'text');
            if (firstText) {
              result.description = firstText.content;
            }
          }
        });

        // 提取原始内容
        result.rawContent = docContainer.innerText;

        return result;
      }, docPath);

      // 提取 tab 内容（需要逐个点击 tab 来加载内容）
      const tabContents = await this._extractTabContents(page);

      return {
        type: 'tiingo-api',
        url,
        title: data.title || 'Tiingo Documentation',
        description: data.description,
        sections: data.sections,
        codeExamples: data.codeExamples,
        tables: data.tables,
        tabContents: tabContents,
        rawContent: data.rawContent,
        suggestedFilename: this.generateFilename(url)
      };
    } catch (error) {
      console.error('Failed to parse Tiingo API doc page:', error.message);
      return {
        type: 'tiingo-api',
        url,
        title: '',
        description: '',
        sections: [],
        codeExamples: [],
        tables: [],
        tabContents: [],
        rawContent: '',
        suggestedFilename: this.generateFilename(url)
      };
    }
  }

  /**
   * 逐个点击 tab 并提取内容
   * @param {Page} page - Playwright页面对象
   * @returns {Promise<Array>} tab 内容数组
   */
  async _extractTabContents(page) {
    const allTabContents = [];

    try {
      // 等待 tab group 加载
      await page.waitForSelector('mat-tab-group', { timeout: 5000 });

      // 获取所有 section 的标题（用于关联 tab 内容）
      const sectionTitles = await page.evaluate(() => {
        const titles = [];
        document.querySelectorAll('.documentation-section-header').forEach(header => {
          const h2 = header.querySelector('h2');
          titles.push(h2 ? h2.textContent.trim() : '');
        });
        return titles;
      });

      // 获取所有 tab group
      const tabGroupCount = await page.evaluate(() => {
        return document.querySelectorAll('mat-tab-group').length;
      });

      console.log(`[TiingoParser] Found ${tabGroupCount} tab groups`);

      for (let groupIndex = 0; groupIndex < tabGroupCount; groupIndex++) {
        // 获取该 tab group 中的 tab 数量和标签
        const tabInfo = await page.evaluate((gi) => {
          const tabGroups = document.querySelectorAll('mat-tab-group');
          if (gi >= tabGroups.length) return [];

          const tabGroup = tabGroups[gi];
          const labels = [];

          // 获取 tab 标签文本
          tabGroup.querySelectorAll('.mat-tab-label').forEach(label => {
            labels.push(label.textContent.trim());
          });

          return labels;
        }, groupIndex);

        console.log(`[TiingoParser] Group ${groupIndex}: ${tabInfo.length} tabs - ${tabInfo.join(', ')}`);

        // 获取该 tab group 对应的 section 索引
        const sectionIndex = Math.floor(groupIndex / 2); // 每个 section 有 2 个 tab group
        const sectionTitle = sectionTitles[sectionIndex] || `Section ${sectionIndex + 1}`;

        // 逐个点击 tab 并提取内容
        for (let tabIndex = 0; tabIndex < tabInfo.length; tabIndex++) {
          try {
            // 重新获取 tab label 元素并点击
            const clicked = await page.evaluate(({ gi, ti }) => {
              const tabGroups = document.querySelectorAll('mat-tab-group');
              if (gi >= tabGroups.length) return false;

              const tabGroup = tabGroups[gi];
              const tabLabels = tabGroup.querySelectorAll('.mat-tab-label');
              if (ti >= tabLabels.length) return false;

              tabLabels[ti].click();
              return true;
            }, { gi: groupIndex, ti: tabIndex });

            if (!clicked) continue;

            // 等待 tab 内容加载
            await page.waitForTimeout(500);

            // 提取当前活动 tab 的内容
            const tabContent = await page.evaluate((gi) => {
              const tabGroups = document.querySelectorAll('mat-tab-group');
              if (gi >= tabGroups.length) return null;

              const tabGroup = tabGroups[gi];
              const activeBody = tabGroup.querySelector('mat-tab-body.mat-tab-body-active');
              if (!activeBody) return null;

              const tabLabel = activeBody.getAttribute('aria-label') || '';
              const contentEl = activeBody.querySelector('.mat-tab-body-content');
              if (!contentEl) return null;

              const result = {
                label: tabLabel,
                content: contentEl.innerText.trim(),
                tables: [],
                codeExamples: []
              };

              // 提取参数表格
              const paramTables = contentEl.querySelectorAll('.parameter-table');
              paramTables.forEach(paramTable => {
                const rows = [];
                const headerRow = paramTable.querySelector('.header-row');
                if (headerRow) {
                  const headers = Array.from(headerRow.querySelectorAll('.header-cell')).map(cell => cell.textContent.trim());
                  if (headers.length > 0) rows.push(headers);
                }
                const paramRows = paramTable.querySelectorAll('.parameter-row');
                paramRows.forEach(row => {
                  const cells = row.querySelectorAll('.parameter-cell');
                  const rowData = Array.from(cells).map(cell => cell.textContent.trim());
                  if (rowData.some(cell => cell)) rows.push(rowData);
                });
                if (rows.length > 1) result.tables.push(rows);
              });

              // 提取标准表格
              const standardTables = contentEl.querySelectorAll('table');
              standardTables.forEach(table => {
                const rows = [];
                table.querySelectorAll('tr').forEach(tr => {
                  const cells = Array.from(tr.querySelectorAll('th, td')).map(c => c.textContent.trim());
                  if (cells.length > 0) rows.push(cells);
                });
                if (rows.length > 1) result.tables.push(rows);
              });

              // 提取代码示例
              const codeBlocks = contentEl.querySelectorAll('pre');
              codeBlocks.forEach(pre => {
                const code = pre.textContent.trim();
                if (code.length > 5) result.codeExamples.push(code);
              });

              return result;
            }, groupIndex);

            if (tabContent && (tabContent.content || tabContent.tables.length > 0 || tabContent.codeExamples.length > 0)) {
              allTabContents.push({
                sectionTitle,
                groupIndex,
                tabIndex,
                label: tabContent.label || tabInfo[tabIndex],
                content: tabContent.content,
                tables: tabContent.tables,
                codeExamples: tabContent.codeExamples
              });

              console.log(`[TiingoParser]   Tab ${tabIndex + 1} (${tabInfo[tabIndex]}): ${tabContent.tables.length} tables, ${tabContent.codeExamples.length} code blocks`);
            }
          } catch (e) {
            console.warn(`[TiingoParser] Failed to extract tab ${tabIndex} in group ${groupIndex}:`, e.message);
          }
        }
      }
    } catch (error) {
      console.warn('[TiingoParser] Tab extraction failed:', error.message);
    }

    return allTabContents;
  }

  
  /**
   * 等待页面内容加载完成
   */
  async waitForContent(page) {
    try {
      await page.waitForLoadState('domcontentloaded', { timeout: 30000 });
      // 等待 Tiingo 特定的文档容器加载
      await page.waitForSelector('.documentation-container, .tiingo-canvas-wrapper', { timeout: 15000 });
      // 额外等待 Angular 渲染
      await page.waitForTimeout(3000);
    } catch (error) {
      console.warn('Wait for content timeout, proceeding anyway:', error.message);
    }
  }
}

export default TiingoApiParser;