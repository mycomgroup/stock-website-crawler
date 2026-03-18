import BaseParser from './base-parser.js';

/**
 * QVeris API Parser - 解析 qveris.ai/docs 文档页面
 * QVeris 是一个工具搜索+执行层，为 LLM agents 提供 API
 * 文档是 Next.js SPA，所有内容嵌入在 JavaScript chunk 文件中
 *
 * 优化策略：
 * 1. 直接从 Next.js 的 JS chunk 文件提取文档数据（更快更可靠）
 * 2. 如果失败，回退到 Playwright 渲染页面
 */
class QverisApiParser extends BaseParser {
  /**
   * 匹配 QVeris API 文档页面
   * @param {string} url - 页面URL
   * @returns {boolean} 是否匹配
   */
  matches(url) {
    return /^https?:\/\/qveris\.ai\/docs\/?$/.test(url);
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
   * QVeris 文档是单页面，不需要发现其他链接
   * @returns {boolean}
   */
  supportsLinkDiscovery() {
    return false;
  }

  /**
   * 根据 URL 生成有意义的文件名
   * @param {string} url - 页面URL
   * @returns {string} 文件名
   */
  generateFilename(url) {
    return 'qveris-api-docs';
  }

  /**
   * 解析 QVeris API 文档页面
   * 优先从 JS chunk 文件直接提取数据，失败则回退到页面渲染
   * @param {Page} page - Playwright页面对象
   * @param {string} url - 页面URL
   * @param {Object} options - 解析选项
   * @returns {Promise<Object>} 解析后的页面数据
   */
  async parse(page, url, options = {}) {
    try {
      // 优先尝试从 JS chunk 文件直接提取数据
      const jsChunkData = await this.extractFromJsChunk(url);
      if (jsChunkData) {
        console.log('Successfully extracted data from JS chunk');
        return jsChunkData;
      }

      console.log('Falling back to page rendering...');
      // 回退到页面渲染方式
      await this.waitForContent(page);

      // 从页面提取内容
      const data = await page.evaluate(() => {
        const result = {
          title: '',
          description: '',
          sections: [],
          codeExamples: [],
          endpoints: [],
          rawContent: ''
        };

        // 获取主要内容区域
        const mainContent = document.querySelector('main') || document.body;

        // 提取标题
        const titleEl = mainContent.querySelector('h1, [class*="title"]');
        result.title = titleEl ? titleEl.textContent.trim() : document.title;

        // 提取所有段落文本
        const paragraphs = mainContent.querySelectorAll('p');
        const paragraphTexts = [];
        paragraphs.forEach(p => {
          const text = p.textContent.trim();
          if (text && text.length > 10) {
            paragraphTexts.push(text);
          }
        });

        // 设置描述（第一个段落）
        if (paragraphTexts.length > 0) {
          result.description = paragraphTexts[0];
        }

        // 提取代码块 - 改进选择器以捕获所有类型
        // 1. 标准 pre > code 结构
        // 2. 直接的 pre 元素
        // 3. 带有代码高亮 class 的元素
        const codeElements = new Set();

        // 收集所有 pre 元素
        mainContent.querySelectorAll('pre').forEach(pre => {
          codeElements.add(pre);
        });

        // 收集所有带有代码相关 class 的元素
        mainContent.querySelectorAll('[class*="code"], [class*="Code"], code').forEach(el => {
          // 如果是 code 元素，找到它的父 pre
          if (el.tagName === 'CODE') {
            const parentPre = el.closest('pre');
            if (parentPre) {
              codeElements.add(parentPre);
            } else {
              codeElements.add(el);
            }
          }
        });

        // 提取代码内容，去重
        const seenCode = new Set();
        codeElements.forEach(block => {
          const code = block.textContent.trim();
          // 使用内容的 hash 去重
          const codeHash = code.substring(0, 100);
          // 过滤掉太短的代码片段（通常是标签或短文本）
          if (code && code.length > 30 && !seenCode.has(codeHash)) {
            seenCode.add(codeHash);
            // 尝试检测语言
            let language = 'text';
            const classList = block.className || '';
            if (classList.includes('python') || classList.includes('Python')) language = 'python';
            else if (classList.includes('javascript') || classList.includes('JavaScript') || classList.includes('js')) language = 'javascript';
            else if (classList.includes('bash') || classList.includes('shell')) language = 'bash';
            else if (classList.includes('json')) language = 'json';
            else if (classList.includes('typescript') || classList.includes('ts')) language = 'typescript';

            // 检测代码内容推断语言
            if (language === 'text') {
              if (code.includes('pip install') || code.includes('curl ')) language = 'bash';
              else if (code.includes('import ') && code.includes('async def')) language = 'python';
              else if (code.startsWith('{') && code.endsWith('}')) language = 'json';
              else if (code.includes('function') || code.includes('const ') || code.includes('let ')) language = 'javascript';
            }

            result.codeExamples.push({ language, code });
          }
        });

        // 提取 API 端点信息
        // QVeris API 端点格式：POST /search, POST /tools/execute
        const textContent = mainContent.innerText;
        const endpointPatterns = [
          /POST\s+(\/[^\s\n]+)/g,
          /GET\s+(\/[^\s\n]+)/g,
          /PUT\s+(\/[^\s\n]+)/g,
          /DELETE\s+(\/[^\s\n]+)/g
        ];

        const foundEndpoints = new Set();
        endpointPatterns.forEach(pattern => {
          let match;
          while ((match = pattern.exec(textContent)) !== null) {
            foundEndpoints.add(match[1]);
          }
        });

        result.endpoints = Array.from(foundEndpoints);

        // 提取 sections（基于 h2, h3 标题）
        const headings = mainContent.querySelectorAll('h2, h3, [class*="heading"], [class*="section"]');
        headings.forEach(heading => {
          const title = heading.textContent.trim();
          if (title && title.length > 2) {
            // 获取该标题后的内容直到下一个标题
            let content = '';
            let sibling = heading.nextElementSibling;
            while (sibling && !['H2', 'H3'].includes(sibling.tagName)) {
              content += sibling.textContent.trim() + '\n';
              sibling = sibling.nextElementSibling;
              if (content.length > 2000) break; // 限制长度
            }
            // 清理内容中的格式化残留
            let cleanedContent = content.trim()
              .replace(/Line NumbersThemeCopy/g, '')
              .replace(/JSONBashPythonTypeScript/g, '')
              .replace(/BashPythonTypeScript/g, '')
              .replace(/JSONLine NumbersThemeCopy/g, '')
              // 移除行首的 JSON、bash、Python 等语言标签
              .replace(/^JSON\s*/gm, '')
              .replace(/^bash\s*/gmi, '')
              .replace(/^Python\s*\d/gm, '')
              .replace(/\n{3,}/g, '\n\n');
            result.sections.push({
              title,
              content: cleanedContent.substring(0, 1000)
            });
          }
        });

        // 提取完整文本内容
        result.rawContent = mainContent.innerText;

        return result;
      });

      // 结构化 API 信息
      const apiInfo = this.extractApiInfo(data.rawContent);

      return {
        type: 'qveris-api',
        url,
        title: data.title || 'QVeris Documentation',
        description: data.description,
        sections: data.sections,
        codeExamples: data.codeExamples,
        endpoints: data.endpoints,
        apiInfo,
        rawContent: data.rawContent,
        suggestedFilename: this.generateFilename(url)
      };
    } catch (error) {
      console.error('Failed to parse QVeris API doc page:', error.message);
      return {
        type: 'qveris-api',
        url,
        title: '',
        description: '',
        sections: [],
        codeExamples: [],
        endpoints: [],
        apiInfo: {},
        rawContent: '',
        suggestedFilename: this.generateFilename(url)
      };
    }
  }

  /**
   * 从文本中提取 API 信息
   * @param {string} content - 页面文本内容
   * @returns {Object} API 信息
   */
  extractApiInfo(content) {
    const apiInfo = {
      baseUrl: '',
      authMethod: '',
      endpoints: []
    };

    // 提取 Base URL
    const baseUrlMatch = content.match(/https:\/\/qveris\.ai\/api\/v1/);
    if (baseUrlMatch) {
      apiInfo.baseUrl = 'https://qveris.ai/api/v1';
    }

    // 提取认证方式
    if (content.includes('Authorization: Bearer')) {
      apiInfo.authMethod = 'Bearer Token';
    }

    // 提取端点信息
    const endpointDetails = [];

    // Search endpoint
    if (content.includes('POST /search')) {
      endpointDetails.push({
        method: 'POST',
        path: '/search',
        description: 'Search for tools using natural language query',
        params: ['query', 'limit']
      });
    }

    // Execute endpoint
    if (content.includes('POST /tools/execute')) {
      endpointDetails.push({
        method: 'POST',
        path: '/tools/execute',
        description: 'Execute a tool by tool_id with parameters',
        params: ['tool_id', 'search_id', 'parameters', 'max_response_size']
      });
    }

    apiInfo.endpoints = endpointDetails;

    return apiInfo;
  }

  /**
   * 从 Next.js JS chunk 文件直接提取文档数据
   * @param {string} url - 文档页面 URL
   * @returns {Promise<Object|null>} 提取的数据，失败返回 null
   */
  async extractFromJsChunk(url) {
    try {
      // 1. 获取 HTML 页面，找到 JS chunk 文件路径
      const htmlResponse = await fetch(url);
      const html = await htmlResponse.text();

      // 2. 查找文档页面的 JS chunk 文件路径
      // 格式: /_next/static/chunks/app/docs/page-[hash].js
      const jsChunkMatch = html.match(/\/_next\/static\/chunks\/app\/docs\/page-[^"]+\.js/);
      if (!jsChunkMatch) {
        console.log('Could not find docs JS chunk file');
        return null;
      }

      const jsChunkUrl = `https://qveris.ai${jsChunkMatch[0]}`;
      console.log(`Found JS chunk: ${jsChunkUrl}`);

      // 3. 下载 JS chunk 文件
      const jsResponse = await fetch(jsChunkUrl);
      const jsContent = await jsResponse.text();

      // 4. 从 JS 中提取文档数据
      return this.parseJsChunkContent(jsContent, url);
    } catch (error) {
      console.error('Error extracting from JS chunk:', error.message);
      return null;
    }
  }

  /**
   * 解析 JS chunk 文件内容，提取文档数据
   * @param {string} jsContent - JS 文件内容
   * @param {string} url - 原始 URL
   * @returns {Object} 解析后的数据
   */
  parseJsChunkContent(jsContent, url) {
    const codeExamples = [];
    const endpoints = [];
    const sections = [];

    // 提取代码块 - 匹配双引号中的多行代码（包含 \n 转义）
    const extractStringContent = (str) => {
      // 处理 JS 字符串中的转义字符
      return str
        .replace(/\\n/g, '\n')
        .replace(/\\t/g, '\t')
        .replace(/\\"/g, '"')
        .replace(/\\\\/g, '\\');
    };

    // 提取 API URL 和示例
    const apiUrlPattern = /"(https:\/\/qveris\.ai\/api\/v1[^"]*)"/g;
    let match;
    const seenUrls = new Set();
    while ((match = apiUrlPattern.exec(jsContent)) !== null) {
      const apiUrl = match[1];
      if (!seenUrls.has(apiUrl)) {
        seenUrls.add(apiUrl);
      }
    }

    // 提取认证示例
    const authPattern = /"(Authorization: Bearer[^"]*)"/g;
    while ((match = authPattern.exec(jsContent)) !== null) {
      const code = match[1];
      if (!codeExamples.find(e => e.code.includes('Authorization: Bearer'))) {
        codeExamples.push({ language: 'text', code });
      }
    }

    // 提取 JSON 请求/响应示例 - 匹配多行字符串
    // 格式1: "key": "value" 或 "key": {...}
    const jsonPatterns = [
      // 匹配完整的 JSON 对象字符串
      /"\{[^"]*\\"query\\"[^"]*\}"/g,
      /"\{[^"]*\\"tool_id\\"[^"]*\}"/g,
      /"\{[^"]*\\"search_id\\"[^"]*\}"/g,
      /"\{[^"]*\\"execution_id\\"[^"]*\}"/g,
      // 匹配 sample_parameters
      /"(sample_parameters[^"]*})"/g
    ];

    // 提取内嵌的 JSON 数据结构
    const seenCode = new Set();

    // 提取 shell/bash 命令示例
    // curl 命令可能直接嵌入在代码中，不一定是字符串
    const bashPatterns = [
      /curl -sS -X POST[^,}\]]{50,500}/g,
      /curl -X POST[^,}\]]{50,500}/g
    ];
    for (const pattern of bashPatterns) {
      while ((match = pattern.exec(jsContent)) !== null) {
        let code = match[0];
        // 处理转义字符
        code = code
          .replace(/\\n/g, '\n')
          .replace(/\\"/g, '"')
          .replace(/\\\\/g, '\\')
          .trim();
        if (code.length > 50) {
          const codeHash = code.substring(0, 80);
          if (!seenCode.has(codeHash)) {
            seenCode.add(codeHash);
            codeExamples.push({ language: 'bash', code });
          }
        }
      }
    }

    // 提取 Python 代码示例
    const pythonPattern = /import requests[^,}\]]{100,1000}/g;
    while ((match = pythonPattern.exec(jsContent)) !== null) {
      let code = match[0];
      code = code
        .replace(/\\n/g, '\n')
        .replace(/\\"/g, '"')
        .replace(/\\\\/g, '\\')
        .trim();
      if (code.length > 50) {
        const codeHash = code.substring(0, 80);
        if (!seenCode.has(codeHash)) {
          seenCode.add(codeHash);
          codeExamples.push({ language: 'python', code });
        }
      }
    }

    // 提取 TypeScript 代码示例
    const tsPattern = /"(export\s+(async\s+)?function[^"]+)"/g;
    while ((match = tsPattern.exec(jsContent)) !== null) {
      let code = extractStringContent(match[1]);
      if (code.length > 50) {
        const codeHash = code.substring(0, 80);
        if (!seenCode.has(codeHash)) {
          seenCode.add(codeHash);
          codeExamples.push({ language: 'typescript', code });
        }
      }
    }

    // 提取 JSON 示例（包含 \n 转义的字符串格式）
    // 这些是直接嵌入在 JS 代码中的 JSON 字符串
    // 需要提取完整的嵌套 JSON 对象
    const extractCompleteJson = (str, startPos) => {
      let depth = 0;
      let inString = false;
      let escape = false;
      let result = '';

      for (let i = startPos; i < str.length; i++) {
        const char = str[i];

        if (escape) {
          result += char;
          escape = false;
          continue;
        }

        if (char === '\\') {
          result += char;
          escape = true;
          continue;
        }

        if (char === '"' && !escape) {
          inString = !inString;
          result += char;
          continue;
        }

        result += char;

        if (!inString) {
          if (char === '{' || char === '[') depth++;
          if (char === '}' || char === ']') {
            depth--;
            if (depth === 0) {
              return result;
            }
          }
        }
      }
      return result;
    };

    // 查找所有 JSON 对象的起始位置
    const jsonStartPattern = /\{\\n\s*"/g;
    let jsonMatch;
    while ((jsonMatch = jsonStartPattern.exec(jsContent)) !== null) {
      const completeJson = extractCompleteJson(jsContent, jsonMatch.index);
      if (completeJson && completeJson.length > 30) {
        let code = completeJson
          .replace(/\\n/g, '\n')
          .replace(/\\"/g, '"')
          .replace(/\\\\/g, '\\')
          .trim();
        const codeHash = code.substring(0, 80);
        if (!seenCode.has(codeHash)) {
          seenCode.add(codeHash);
          codeExamples.push({ language: 'json', code });
        }
      }
    }

    // 提取简单的 JSON 对象（不包含 \n）
    const simpleJsonPattern = /\{"query":\s*"[^"]+[^}]*\}/g;
    while ((match = simpleJsonPattern.exec(jsContent)) !== null) {
      const code = match[0];
      const codeHash = code.substring(0, 80);
      if (!seenCode.has(codeHash)) {
        seenCode.add(codeHash);
        codeExamples.push({ language: 'json', code });
      }
    }

    // 提取 API 端点 - 改进正则表达式，支持下划线
    const endpointPatterns = [
      /"POST\s+(\/[a-z_\-\/{}?=]+)"/gi,
      /"GET\s+(\/[a-z_\-\/{}?=]+)"/gi
    ];
    const seenEndpoints = new Set();
    for (const pattern of endpointPatterns) {
      let m;
      while ((m = pattern.exec(jsContent)) !== null) {
        // 清理端点路径：移除 {} 和查询参数
        let endpoint = m[1]
          .replace(/[{}]/g, '')
          .split('?')[0];  // 移除查询参数部分
        if (!seenEndpoints.has(endpoint)) {
          seenEndpoints.add(endpoint);
          endpoints.push(endpoint);
        }
      }
    }

    // 如果没有从正则提取到端点，手动添加已知的端点
    if (endpoints.length === 0) {
      endpoints.push('/search', '/tools/execute', '/tools/by-ids');
    }

    // 提取文档章节结构
    const sectionPattern = /\{id:"([^"]+)",title:"([^"]+)"/g;
    let secMatch;
    while ((secMatch = sectionPattern.exec(jsContent)) !== null) {
      const [, id, title] = secMatch;
      if (title && title.length > 2) {
        sections.push({ id, title });
      }
    }

    // 去重代码示例 - 基于内容相似度和价值
    const uniqueCodeExamples = [];
    const uniqueCodeSet = new Set();

    for (const example of codeExamples) {
      // 跳过过长的示例（超过 2000 字符通常是嵌套太多）
      if (example.code.length > 2000) continue;
      // 跳过过短的示例
      if (example.code.length < 40) continue;

      // 清理 JSON 中的空白和格式差异进行比较
      const normalizedCode = example.code
        .replace(/\s+/g, ' ')
        .replace(/\s*([{}[\]:,])\s*/g, '$1')
        .trim();
      const codeHash = normalizedCode.substring(0, 80);

      let isDuplicate = false;
      for (const existing of uniqueCodeExamples) {
        const existingNormalized = existing.code
          .replace(/\s+/g, ' ')
          .replace(/\s*([{}[\]:,])\s*/g, '$1')
          .trim();

        // 如果新代码是现有代码的子集，跳过
        if (existingNormalized.includes(normalizedCode.substring(0, 50))) {
          isDuplicate = true;
          break;
        }
        // 如果现有代码是新代码的子集，替换
        if (normalizedCode.includes(existingNormalized.substring(0, 50))) {
          const idx = uniqueCodeExamples.indexOf(existing);
          uniqueCodeExamples[idx] = example;
          isDuplicate = true;
          break;
        }
      }

      if (!isDuplicate) {
        uniqueCodeSet.add(codeHash);
        uniqueCodeExamples.push(example);
      }
    }

    // 按优先级排序，确保多样化的示例
    const langPriority = { typescript: 1, bash: 2, python: 3, json: 4, text: 5 };
    uniqueCodeExamples.sort((a, b) => {
      const pa = langPriority[a.language] || 5;
      const pb = langPriority[b.language] || 5;
      if (pa !== pb) return pa - pb;
      return b.code.length - a.code.length;
    });

    // 限制最多保留 20 个最有价值的示例
    const finalExamples = uniqueCodeExamples.slice(0, 20);

    // 提取 Base URL
    const baseUrl = 'https://qveris.ai/api/v1';

    // 构建 API 信息
    const apiInfo = {
      baseUrl,
      authMethod: 'Bearer Token',
      endpoints: [
        {
          method: 'POST',
          path: '/search',
          description: 'Search for tools using natural language query',
          params: ['query', 'limit', 'session_id']
        },
        {
          method: 'POST',
          path: '/tools/execute',
          description: 'Execute a tool by tool_id with parameters',
          params: ['tool_id', 'search_id', 'parameters', 'max_response_size']
        },
        {
          method: 'POST',
          path: '/tools/by-ids',
          description: 'Get descriptions of tools based on tool_id',
          params: ['tool_ids', 'search_id', 'session_id']
        }
      ]
    };

    // 生成原始内容文本
    const rawContent = this.generateRawContent(finalExamples, apiInfo, sections);

    return {
      type: 'qveris-api',
      url,
      title: 'QVeris API Documentation',
      description: 'QVeris is a tool search and execution layer that provides APIs for LLM agents to discover and execute tools.',
      sections,
      codeExamples: finalExamples,
      endpoints,
      apiInfo,
      rawContent,
      suggestedFilename: this.generateFilename(url),
      source: 'js-chunk'
    };
  }

  /**
   * 生成原始内容文本
   */
  generateRawContent(codeExamples, apiInfo, sections) {
    let content = '# QVeris API Documentation\n\n';

    content += '## Base URL\n';
    content += `${apiInfo.baseUrl}\n\n`;

    content += '## Authentication\n';
    content += 'All API requests require authentication via Bearer Token:\n';
    content += 'Authorization: Bearer YOUR_API_KEY\n\n';

    content += '## API Endpoints\n\n';
    for (const endpoint of apiInfo.endpoints) {
      content += `### ${endpoint.method} ${endpoint.path}\n`;
      content += `${endpoint.description}\n`;
      content += `Parameters: ${endpoint.params.join(', ')}\n\n`;
    }

    content += '## Code Examples\n\n';
    for (const example of codeExamples) {
      content += `### ${example.language}\n`;
      content += '```\n';
      content += example.code;
      content += '\n```\n\n';
    }

    return content;
  }

  /**
   * 等待页面内容加载完成并切换到 API tab
   * @param {Page} page - Playwright页面对象
   */
  async waitForContent(page) {
    try {
      await page.waitForLoadState('networkidle', { timeout: 30000 });
      // 等待 Next.js 渲染
      await page.waitForTimeout(2000);

      // 尝试点击 API tab 以显示完整的 API 文档
      try {
        // 查找 API tab - 可能是按钮、链接或 tab 组件
        const apiTabSelectors = [
          'button:has-text("API")',
          'a:has-text("API")',
          '[role="tab"]:has-text("API")',
          '[role="tabbutton"]:has-text("API")',
          'div[role="tablist"] button:has-text("API")',
          '.tab:has-text("API")',
          '[class*="tab"]:has-text("API")'
        ];

        let tabClicked = false;
        for (const selector of apiTabSelectors) {
          try {
            const tab = await page.$(selector);
            if (tab) {
              // 检查是否已经是激活状态
              const isActive = await tab.evaluate(el => {
                return el.getAttribute('aria-selected') === 'true' ||
                       el.classList.contains('active') ||
                       el.classList.contains('selected') ||
                       el.getAttribute('data-state') === 'active';
              });

              if (!isActive) {
                await tab.click();
                console.log('Clicked API tab');
                tabClicked = true;
                // 等待 tab 内容加载
                await page.waitForTimeout(2000);
              } else {
                console.log('API tab already active');
              }
              break;
            }
          } catch (e) {
            // 继续尝试下一个选择器
          }
        }

        if (!tabClicked) {
          console.log('Could not find API tab, proceeding with default content');
        }
      } catch (tabError) {
        console.warn('Error switching to API tab:', tabError.message);
      }

      // 额外等待确保动态内容完全加载
      await page.waitForTimeout(1500);
    } catch (error) {
      console.warn('Wait for content timeout, proceeding anyway:', error.message);
    }
  }
}

export default QverisApiParser;