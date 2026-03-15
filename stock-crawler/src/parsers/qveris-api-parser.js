import BaseParser from './base-parser.js';

/**
 * QVeris API Parser - 解析 qveris.ai/docs 文档页面
 * QVeris 是一个工具搜索+执行层，为 LLM agents 提供 API
 * 文档是 Next.js SPA，所有内容在单页面
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
   * 等待页面内容加载完成
   * @param {Page} page - Playwright页面对象
   */
  async waitForContent(page) {
    try {
      await page.waitForLoadState('networkidle', { timeout: 30000 });
      // 等待 Next.js 渲染
      await page.waitForTimeout(3000);
    } catch (error) {
      console.warn('Wait for content timeout, proceeding anyway:', error.message);
    }
  }
}

export default QverisApiParser;