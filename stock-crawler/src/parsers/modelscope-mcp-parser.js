import BaseParser from './base-parser.js';

/**
 * ModelScope MCP Parser - 专门解析 ModelScope MCP 服务器文档页面
 * ModelScope MCP 是一个 MCP (Model Context Protocol) 服务器目录
 * URL 格式: https://modelscope.cn/mcp/servers/{server-name}
 * 例如: https://modelscope.cn/mcp/servers/@modelcontextprotocol/fetch
 */
class ModelscopeMcpParser extends BaseParser {
  /**
   * 匹配 ModelScope MCP 页面
   * @param {string} url - 页面URL
   * @returns {boolean} 是否匹配
   */
  matches(url) {
    return /^https?:\/\/modelscope\.cn\/mcp/.test(url);
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
  generateFilename(url) {
    try {
      const urlObj = new URL(url);
      let pathname = urlObj.pathname;
      // 移除 /mcp 前缀
      pathname = pathname.replace(/^\/mcp\/?/, '');
      pathname = pathname.replace(/\/$/, '');
      // 处理 servers/ 前缀
      pathname = pathname.replace(/^servers\//, '');
      const filename = pathname.replace(/\//g, '_') || 'mcp_overview';
      return filename;
    } catch (e) {
      return 'modelscope_mcp_doc';
    }
  }

  /**
   * 从 URL 提取服务器路径
   * @param {string} url - 页面URL
   * @returns {string} 服务器路径
   */
  extractServerPath(url) {
    try {
      const urlObj = new URL(url);
      let pathname = urlObj.pathname;
      pathname = pathname.replace(/^\/mcp\/?/, '');
      return pathname;
    } catch (e) {
      return '';
    }
  }

  /**
   * 等待页面内容加载完成
   */
  async waitForContent(page) {
    try {
      await page.waitForLoadState('networkidle', { timeout: 30000 });
      // 等待主内容区域
      await page.waitForSelector('main', { timeout: 15000 });
      await page.waitForTimeout(3000); // 额外等待动态内容
    } catch (error) {
      console.warn('Wait for content timeout, proceeding anyway:', error.message);
    }
  }

  /**
   * 解析 ModelScope MCP 页面
   * @param {Page} page - Playwright页面对象
   * @param {string} url - 页面URL
   * @param {Object} options - 解析选项
   * @returns {Promise<Object>} 解析后的页面数据
   */
  async parse(page, url, options = {}) {
    try {
      await this.waitForContent(page);

      const serverPath = this.extractServerPath(url);
      const isServerDetail = serverPath.startsWith('servers/');

      const data = await page.evaluate(() => {
        const result = {
          title: '',
          description: '',
          serverInfo: {},
          tools: [],
          prompts: [],
          installation: '',
          configuration: '',
          codeBlocks: [],
          tables: [],
          rawContent: '',
          links: [],
          tags: []
        };

        // 获取 main 元素作为主要内容容器
        const main = document.querySelector('main');
        if (!main) {
          return result;
        }

        // 提取标题
        const h1 = main.querySelector('h1');
        if (h1) {
          result.title = h1.textContent.trim();
        }

        // 提取描述 - 通常是 h1 后的第一段或特定描述区域
        const descriptionEl = main.querySelector('.acss-j8jmz5') ||
                              main.querySelector('[class*="description"]');
        if (descriptionEl) {
          result.description = descriptionEl.textContent.trim();
        }

        // 提取服务器基本信息
        // 服务器名称和路径
        const serverNameEl = main.querySelector('.acss-cyoggp');
        const serverPathEl = main.querySelector('.acss-149f9ri');
        if (serverNameEl) {
          result.serverInfo['开发者'] = serverNameEl.textContent.trim();
        }
        if (serverPathEl) {
          result.serverInfo['路径'] = serverPathEl.textContent.trim();
        }

        // 提取标签
        const tags = main.querySelectorAll('.antd5-tag');
        tags.forEach(tag => {
          const tagText = tag.textContent.trim();
          if (tagText && !tagText.includes('License') && !tagText.includes('Developer')) {
            // 过滤掉一些不需要的标签
            if (tagText.length > 2 && tagText.length < 30) {
              result.tags.push(tagText);
            }
          }
        });

        // 提取许可证信息
        const licenseLabel = Array.from(main.querySelectorAll('*')).find(el =>
          el.textContent?.trim() === 'License:'
        );
        if (licenseLabel) {
          const licenseValue = licenseLabel.closest('.antd5-tag')?.querySelector('.acss-1m97cav')?.textContent.trim();
          if (licenseValue) {
            result.serverInfo['许可证'] = licenseValue;
          }
        }

        // 提取所有标题和内容段落
        const allText = main.innerText;
        result.rawContent = allText;

        // 提取工具信息
        // 查找 "Available Tools" 或 "工具" 部分
        const sections = allText.split(/\n(?=[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\n)/);
        sections.forEach(section => {
          const lines = section.trim().split('\n');
          if (lines.length > 0) {
            const sectionTitle = lines[0].trim();
            if (sectionTitle === 'Available Tools' || sectionTitle.includes('Tools')) {
              // 提取工具信息
              const toolMatch = section.match(/(\w+)\s*-\s*(.+?)(?:\n|$)/g);
              if (toolMatch) {
                toolMatch.forEach(match => {
                  const [, name, desc] = match.match(/(\w+)\s*-\s*(.+)/) || [];
                  if (name && desc) {
                    result.tools.push({ name, description: desc.trim() });
                  }
                });
              }
            }
          }
        });

        // 从原始内容提取工具和参数
        const toolRegex = /(\w+)\s*-\s*(.+?)(?:\n|$)/g;
        let toolMatch;
        while ((toolMatch = toolRegex.exec(allText)) !== null) {
          const [, name, desc] = toolMatch;
          if (name && desc && !result.tools.find(t => t.name === name)) {
            result.tools.push({ name, description: desc.trim() });
          }
        }

        // 提取代码块
        const codeElements = main.querySelectorAll('pre, code');
        codeElements.forEach(el => {
          const code = el.textContent.trim();
          if (code && code.length > 10) {
            // 避免重复
            let language = 'text';
            const classList = el.className || '';

            if (classList.includes('language-json') || code.startsWith('{')) {
              language = 'json';
            } else if (classList.includes('language-python') || code.includes('pip ') || code.includes('python ')) {
              language = 'bash';
            } else if (classList.includes('language-javascript') || code.includes('npm ') || code.includes('npx ')) {
              language = 'bash';
            } else if (code.startsWith('pip ') || code.startsWith('python ') || code.startsWith('npm ') || code.startsWith('npx ') || code.startsWith('cd ') || code.includes('docker ')) {
              language = 'bash';
            }

            // 检查是否已经存在相同的代码块
            if (!result.codeBlocks.find(b => b.code === code)) {
              result.codeBlocks.push({ language, code });
            }
          }
        });

        // 提取表格
        const tables = main.querySelectorAll('table');
        tables.forEach((table, index) => {
          const headers = [];
          const rows = [];

          // 提取表头
          const headerRow = table.querySelector('thead tr') || table.querySelector('tr');
          if (headerRow) {
            const headerCells = headerRow.querySelectorAll('th, td');
            headerCells.forEach(cell => headers.push(cell.textContent.trim()));
          }

          // 提取数据行
          const bodyRows = table.querySelectorAll('tbody tr');
          const rowsToProcess = bodyRows.length > 0 ? bodyRows : table.querySelectorAll('tr');

          rowsToProcess.forEach((row, rowIndex) => {
            if (rowIndex === 0 && bodyRows.length === 0) return;

            const cells = row.querySelectorAll('td, th');
            if (cells.length > 0) {
              const rowData = {};
              cells.forEach((cell, cellIndex) => {
                const headerName = headers[cellIndex] || `column_${cellIndex}`;
                rowData[headerName] = cell.textContent.trim();

                const link = cell.querySelector('a');
                if (link) {
                  rowData[`${headerName}_link`] = link.href;
                }
              });
              rows.push(rowData);
            }
          });

          if (rows.length > 0) {
            result.tables.push({ index, headers, rows });
          }
        });

        // 提取 MCP 相关链接
        const links = main.querySelectorAll('a[href*="/mcp"]');
        links.forEach(link => {
          const href = link.href;
          const text = link.textContent.trim();
          if (text && !result.links.find(l => l.href === href)) {
            result.links.push({ text, href });
          }
        });

        return result;
      });

      // 解析原始内容，提取安装和配置部分
      if (data.rawContent) {
        const sections = this.parseSections(data.rawContent);
        data.installation = sections.installation;
        data.configuration = sections.configuration;
        data.prompts = sections.prompts;
      }

      return {
        type: 'modelscope-mcp-server',
        url,
        serverPath,
        isServerDetail,
        title: data.title,
        description: data.description,
        serverInfo: data.serverInfo,
        tools: data.tools,
        prompts: data.prompts,
        tags: data.tags,
        installation: data.installation,
        configuration: data.configuration,
        codeBlocks: data.codeBlocks,
        tables: data.tables,
        links: data.links,
        rawContent: data.rawContent,
        suggestedFilename: this.generateFilename(url)
      };
    } catch (error) {
      console.error('Failed to parse ModelScope MCP page:', error.message);
      return {
        type: 'modelscope-mcp-server',
        url,
        serverPath: this.extractServerPath(url),
        isServerDetail: false,
        title: '',
        description: '',
        serverInfo: {},
        tools: [],
        prompts: [],
        tags: [],
        installation: '',
        configuration: '',
        codeBlocks: [],
        tables: [],
        links: [],
        rawContent: '',
        suggestedFilename: this.generateFilename(url)
      };
    }
  }

  /**
   * 解析原始内容，提取各个部分
   */
  parseSections(rawContent) {
    const result = {
      installation: '',
      configuration: '',
      prompts: []
    };

    // 提取安装部分
    const installMatch = rawContent.match(/Installation\s*([\s\S]*?)(?=Configuration|Debugging|Contributing|License|$)/i);
    if (installMatch) {
      result.installation = installMatch[1].trim();
    }

    // 提取配置部分
    const configMatch = rawContent.match(/Configuration\s*([\s\S]*?)(?=Debugging|Contributing|License|Service configuration|$)/i);
    if (configMatch) {
      result.configuration = configMatch[1].trim();
    }

    // 提取 Prompts 部分
    const promptsMatch = rawContent.match(/Prompts\s*([\s\S]*?)(?=Installation|Configuration|Debugging|Contributing|License|$)/i);
    if (promptsMatch) {
      result.prompts = [promptsMatch[1].trim()];
    }

    return result;
  }
}

export default ModelscopeMcpParser;