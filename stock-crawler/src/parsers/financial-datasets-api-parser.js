import BaseParser from './base-parser.js';

/**
 * Financial Datasets API Parser - 专门解析 docs.financialdatasets.ai API 文档页面
 * 适用于 Mintlify 风格的文档站点
 */
class FinancialDatasetsApiParser extends BaseParser {
  /**
   * 匹配 Financial Datasets API 文档页面
   * @param {string} url - 页面URL
   * @returns {boolean} 是否匹配
   */
  matches(url) {
    return /^https?:\/\/docs\.financialdatasets\.ai\/api\//.test(url);
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
      // 移除 /api 前缀
      pathname = pathname.replace(/^\/api\/?/, '');
      pathname = pathname.replace(/\/$/, '');
      const filename = pathname.replace(/\//g, '_') || 'api_overview';
      return filename;
    } catch (e) {
      return 'api_doc';
    }
  }

  /**
   * 解析 Financial Datasets API 文档页面
   * @param {Page} page - Playwright页面对象
   * @param {string} url - 页面URL
   * @param {Object} options - 解析选项
   * @returns {Promise<Object>} 解析后的页面数据
   */
  async parse(page, url, options = {}) {
    try {
      // 等待内容加载完成
      await this.waitForContent(page);

      // 从页面提取内容
      const data = await page.evaluate(() => {
        const result = {
          title: '',
          description: '',
          method: 'GET',
          endpoint: '',
          parameters: [],
          requestParams: [],
          responseFields: [],
          codeExamples: [],
          rawContent: ''
        };

        // Mintlify 文档通常使用特定的内容区域
        // 尝试多种选择器
        const contentSelectors = [
          'main',
          'article',
          '[class*="docs-content"]',
          '[class*="content"]',
          '[class*="prose"]',
          '.markdown-body',
          '[class*="article"]',
          'div[class*="mx-auto"]'
        ];

        let mainContent = null;
        for (const selector of contentSelectors) {
          const el = document.querySelector(selector);
          if (el && el.innerText && el.innerText.trim().length > 50) {
            mainContent = el;
            break;
          }
        }

        if (!mainContent) {
          mainContent = document.body;
        }

        // 提取标题
        const h1 = mainContent.querySelector('h1');
        if (h1) {
          result.title = h1.textContent.trim();
        }

        // 提取描述（标题后的第一段有意义的内容）
        const allParagraphs = mainContent.querySelectorAll('p');
        for (const p of allParagraphs) {
          const text = p.textContent.trim();
          // 跳过太短的、代码片段、或者是导航链接
          if (text.length > 30 && !text.startsWith('{') && !text.startsWith('[') && !text.startsWith('http')) {
            result.description = text;
            break;
          }
        }

        // 提取 HTTP 方法 - Mintlify 通常显示 GET/POST 等
        const methodPatterns = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH'];
        const allText = mainContent.innerText;
        for (const method of methodPatterns) {
          // 查找独立的方法标识
          const methodRegex = new RegExp(`\\b${method}\\b`, 'i');
          if (methodRegex.test(allText)) {
            result.method = method;
            break;
          }
        }

        // 提取 API 端点 - 查找 api.financialdatasets.ai 开头的 URL
        const apiEndpointMatch = allText.match(/https?:\/\/api\.financialdatasets\.ai[\/a-zA-Z0-9\-_{}]*/);
        if (apiEndpointMatch) {
          result.endpoint = apiEndpointMatch[0];
        } else {
          // 备选：查找 /api/ 开头的路径
          const endpointMatch = allText.match(/\/api\/[a-zA-Z0-9\/\-_{}]+/);
          if (endpointMatch) {
            result.endpoint = endpointMatch[0];
          }
        }

        // 解析 Mintlify 风格的参数（非表格格式）
        // Mintlify 参数格式通常是：参数名\n类型[required]\n描述
        const parseMintlifyParams = (sectionText) => {
          const params = [];
          // 按双换行分割成块
          const blocks = sectionText.split(/\n\s*\n/);

          for (let i = 0; i < blocks.length; i++) {
            const block = blocks[i].trim();
            if (!block || block.length < 3) continue;

            // 每个参数块通常是：参数名\n类型\n描述
            // 但也可能是：参数名\n类型required\n描述 或 参数名\n类型 required\n描述
            const lines = block.split('\n').map(l => l.trim()).filter(l => l && l !== '​');

            if (lines.length >= 2) {
              const name = lines[0];
              const typeLine = lines[1] || '';
              const desc = lines.slice(2).join(' ').trim();

              // 验证这是参数名（通常较短，不含空格）
              if (name.length < 50 && !name.includes(' ') && !name.startsWith('{') && !name.startsWith('[') && !name.startsWith('http')) {
                // 检查第二行是否是类型（可能包含 required）
                const typeMatch = typeLine.match(/^(string|boolean|number|integer|object|array|enum(?:<[^>]+>)?)\s*(required)?$/i);
                if (typeMatch) {
                  params.push({
                    name: name,
                    type: typeMatch[1],
                    required: typeMatch[2] ? '是' : '',
                    description: desc || ''
                  });
                }
              }
            }
          }

          return params;
        };

        // 使用更直接的方法提取参数
        // Mintlify 格式：参数块格式为 "paramName\ntype[required]"，描述在下一个块
        // 参数块之间用双换行分隔
        const extractParams = (text) => {
          const params = [];

          // 按双换行分割成块
          const blocks = text.split(/\n\s*\n/);

          // 跳过关键词列表
          const skipParamNames = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'Copy', 'Overview',
            'Example', 'Response', 'Authorizations', 'Query', 'Parameters', 'Support',
            'application', 'json', 'Available', 'options', 'Hide', 'child', 'attributes',
            'Analyst', 'Estimates', 'Company', 'Earnings', 'Financial', 'Metrics', 'Statements',
            'Insider', 'Trades', 'News', 'Institutional', 'Ownership', 'Interest', 'Rates',
            'Search', 'SEC', 'Filings', 'Segmented', 'Stock', 'Prices'];

          for (let i = 0; i < blocks.length; i++) {
            const block = blocks[i].trim();

            // 跳过空块
            if (!block) continue;

            // 将当前块按单换行分割
            const lines = block.split('\n').map(l => l.trim()).filter(l => l);

            // 在块中搜索符合 paramName + typeLine 模式的连续两行
            for (let j = 0; j < lines.length - 1; j++) {
              const paramName = lines[j];
              const typeLine = lines[j + 1];

              // 验证参数名格式（应该是简单的标识符）
              if (!/^[a-z_][a-z0-9_]*$/i.test(paramName)) continue;

              // 跳过特殊关键词
              if (skipParamNames.includes(paramName)) continue;

              // 跳过以特定前缀开头的（通常是响应字段）
              if (paramName.startsWith('company_facts') || paramName.startsWith('analyst_estimates') ||
                  paramName.startsWith('earnings.') || paramName.startsWith('financials.') ||
                  paramName.startsWith('insider_trades.') || paramName.startsWith('news.') ||
                  paramName.startsWith('prices.') || paramName.startsWith('filings.')) continue;

              // 检查类型格式
              // 支持格式：string, stringrequired, string required, enum<string>, enum<string>required 等
              // 还要支持 stringheaderrequired (Mintlify 把 header 参数类型显示为 "stringheaderrequired")
              const typeBlock = typeLine.replace(/\s+/g, ''); // 移除空格便于匹配
              // 匹配类型，允许后面跟着 "required"、"headerrequired" 等
              const typeMatch = typeBlock.match(/^(string|boolean|number|integer|object|array|enum(?:<[^>]+>)?)(header)?(required)?$/i);

              if (typeMatch) {
                // 找到描述 - 在下一个块中
                let description = '';
                if (blocks[i + 1]) {
                  description = blocks[i + 1].trim();
                  // 如果描述太长（超过200字符），可能是其他内容，清空
                  if (description.length > 200) {
                    description = '';
                  }
                }

                // 检查是否已经存在
                if (!params.some(p => p.name === paramName)) {
                  params.push({
                    name: paramName,
                    type: typeMatch[1],
                    required: typeMatch[3] ? '是' : '',
                    description: description
                  });
                }
              }
            }
          }

          return params;
        };

        // 提取 Query Parameters 部分 - 使用更简单的方法
        // 直接在整个文本中查找参数模式，而不是先提取 Query Parameters 部分
        // 这样可以避免正则表达式匹配问题
        const allParams = extractParams(allText);

        // 将找到的参数添加到 requestParams（排除已经在表格中的）
        if (allParams.length > 0) {
          for (const param of allParams) {
            if (!result.requestParams.some(p => p.name === param.name)) {
              result.requestParams.push(param);
            }
          }
        }

        // 提取 Authorizations 部分（Header 参数）
        const authMatch = allText.match(/Authorizations\s*​?([\s\S]*?)(?=Query Parameters|Response|^[A-Z][a-z]+\s+\(|$)/i);
        if (authMatch) {
          const authText = authMatch[1];
          // 查找 X-API-KEY
          if (authText.includes('X-API-KEY')) {
            // 检查是否已经存在
            const hasApiKey = result.requestParams.some(p => p.name === 'X-API-KEY');
            if (!hasApiKey) {
              result.requestParams.unshift({
                name: 'X-API-KEY',
                type: 'string',
                required: '是',
                description: 'API key for authentication. (Header参数)'
              });
            }
          }
        }

        // 提取 Response 字段 - 改进版本
        // 查找 company_facts.字段名 或类似格式的字段
        const responseFields = [];
        const fieldPattern = /(?:company_facts|analyst_estimates|financials|insider_trades|news|prices|earnings|filings)\.([a-z_]+)\s*\n?\s*(string|boolean|number|integer|object|array|enum[^\n]*)?\s*\n?\s*([^\n]+)/gi;
        let fieldMatch;
        const seenFields = new Set();

        while ((fieldMatch = fieldPattern.exec(allText)) !== null) {
          const fieldName = fieldMatch[1];
          const fieldType = (fieldMatch[2] || '').replace(/required/i, '').trim();
          const fieldDesc = fieldMatch[3].trim();

          // 跳过已见过的字段
          if (seenFields.has(fieldName)) continue;
          seenFields.add(fieldName);

          responseFields.push({
            name: fieldName,
            type: fieldType,
            description: fieldDesc
          });
        }

        result.responseFields = responseFields;

        // 查找包含参数的表格（作为备选）
        const tables = mainContent.querySelectorAll('table');
        for (const table of tables) {
          const rows = table.querySelectorAll('tr');
          if (rows.length < 2) continue;

          const headerRow = rows[0];
          const headerCells = headerRow.querySelectorAll('th, td');
          const headers = Array.from(headerCells).map(cell => cell.textContent.trim().toLowerCase());

          // 判断是请求参数表还是响应字段表
          const isRequestParams = headers.some(h =>
            h.includes('param') || h.includes('name') || h.includes('参数') || h.includes('field') || h.includes('column')
          );
          const isResponseTable = headers.some(h =>
            h.includes('response') || h.includes('返回') || h.includes('output') || h.includes('type')
          );

          for (let i = 1; i < rows.length; i++) {
            const cells = rows[i].querySelectorAll('td, th');
            if (cells.length < 2) continue;

            const rowData = {
              name: cells[0]?.textContent.trim() || '',
              type: cells[1]?.textContent.trim() || '',
              required: cells[2]?.textContent.trim() || '',
              description: cells[3]?.textContent.trim() || cells[2]?.textContent.trim() || ''
            };

            if (isRequestParams && !isResponseTable && rowData.name) {
              result.requestParams.push(rowData);
            } else if (isResponseTable && rowData.name) {
              result.responseFields.push(rowData);
            }
          }
        }

        // 提取代码示例
        const codeBlocks = mainContent.querySelectorAll('pre code, pre');
        for (const block of codeBlocks) {
          const code = block.textContent.trim();
          if (code && code.length > 10) {
            let language = 'text';
            const classList = block.className || '';
            const langMatch = classList.match(/language-(\w+)/);
            if (langMatch) {
              language = langMatch[1];
            } else if (code.startsWith('curl') || code.includes('curl ')) {
              language = 'bash';
            } else if (code.startsWith('{') || code.startsWith('[')) {
              language = 'json';
            } else if (code.startsWith('import') || code.startsWith('from') || code.includes('import ')) {
              language = 'python';
            } else if (code.startsWith('const') || code.startsWith('let') || code.startsWith('function')) {
              language = 'javascript';
            }

            result.codeExamples.push({ language, code });
          }
        }

        // 提取完整内容作为原始内容
        result.rawContent = mainContent.innerText;

        return result;
      });

      return {
        type: 'financial-datasets-api',
        url,
        title: data.title,
        description: data.description,
        requestMethod: data.method,
        endpoint: data.endpoint,
        requestParams: data.requestParams,
        responseFields: data.responseFields,
        codeExamples: data.codeExamples,
        rawContent: data.rawContent,
        suggestedFilename: this.generateFilename(url)
      };
    } catch (error) {
      console.error('Failed to parse Financial Datasets API doc page:', error.message);
      return {
        type: 'financial-datasets-api',
        url,
        title: '',
        description: '',
        requestMethod: '',
        endpoint: '',
        requestParams: [],
        responseFields: [],
        codeExamples: [],
        rawContent: '',
        suggestedFilename: this.generateFilename(url)
      };
    }
  }

  /**
   * 等待内容加载完成
   */
  async waitForContent(page) {
    try {
      await page.waitForLoadState('domcontentloaded', { timeout: 30000 });

      // 等待主要内容元素出现
      const contentSelectors = [
        'main',
        'article',
        'h1',
        '[class*="content"]',
        '[class*="prose"]'
      ];

      for (const selector of contentSelectors) {
        try {
          await page.waitForSelector(selector, { timeout: 5000 });
          break;
        } catch (e) {
          // 继续尝试下一个选择器
        }
      }

      // 额外等待动态内容加载
      await page.waitForTimeout(3000);
    } catch (error) {
      console.warn('Wait for content timeout, proceeding anyway:', error.message);
    }
  }
}

export default FinancialDatasetsApiParser;