import BaseParser from './base-parser.js';

/**
 * SerpApi AI Overview Parser - 专门解析 serpapi.com/ai-overview 文档页面
 * SerpApi 提供 Google AI Overview 结果的 API 抓取服务
 * 文档页面包含 API 端点、参数说明、响应结构和多个示例
 */
class SerpApiParser extends BaseParser {
  /**
   * 匹配 SerpApi AI Overview 文档页面
   * @param {string} url - 页面URL
   * @returns {boolean} 是否匹配
   */
  matches(url) {
    return /^https?:\/\/serpapi\.com\/ai-overview/.test(url);
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
    return 'ai-overview-api';
  }

  /**
   * 解析 SerpApi AI Overview 文档页面
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
          endpoint: 'https://serpapi.com/search',
          engine: 'google',
          method: 'GET',
          parameters: [],
          responseStructure: [],
          examples: [],
          rawContent: ''
        };

        // 提取标题
        const h1 = document.querySelector('h1');
        if (h1) {
          result.title = h1.textContent.trim();
        }

        // 提取描述 - 页面顶部的主要说明文字
        const descTexts = [];

        // 辅助函数：清理文本中的多余空白
        const cleanText = (text) => {
          return text
            .replace(/\s+/g, ' ')  // 将多个空白字符替换为单个空格
            .trim();
        };

        // 方法1: 从页面顶部的主要区域提取
        const topSections = document.querySelectorAll('.my-4 .d-flex, .dashboard-page-header ~ .my-4, .box-wrapper.main-text');
        topSections.forEach(section => {
          const paragraphs = section.querySelectorAll('p');
          paragraphs.forEach(p => {
            const text = cleanText(p.textContent);
            // 过滤掉太短的文字和重复内容
            if (text.length > 20 && !descTexts.includes(text)) {
              descTexts.push(text);
            }
          });
        });

        // 方法2: 直接从包含 API endpoint 的区域提取
        const endpointSection = document.querySelector('.dashboard-page-header');
        if (endpointSection) {
          const allPs = endpointSection.parentElement?.querySelectorAll('.my-4 p') || [];
          allPs.forEach(p => {
            const text = cleanText(p.textContent);
            if (text.length > 20 && !descTexts.includes(text)) {
              descTexts.push(text);
            }
          });
        }

        // 方法3: 获取 API Examples 之前的所有段落
        const apiExamples = document.getElementById('api-examples');
        if (apiExamples) {
          let sibling = apiExamples.previousElementSibling;
          while (sibling) {
            const paragraphs = sibling.querySelectorAll('p');
            paragraphs.forEach(p => {
              const text = cleanText(p.textContent);
              if (text.length > 20 && !descTexts.includes(text) &&
                  !text.includes('page_token') && !text.includes('serpapi_link')) {
                descTexts.unshift(text); // 添加到开头
              }
            });
            sibling = sibling.previousElementSibling;
          }
        }

        result.description = descTexts.join('\n\n');

        // 提取 API Examples 部分
        const apiExamplesSection = document.getElementById('api-examples');
        if (apiExamplesSection) {
          // 查找所有示例块
          const exampleWrappers = document.querySelectorAll('.box-wrapper[id^="api-examples-"]');

          exampleWrappers.forEach(wrapper => {
            const example = {
              title: '',
              description: '',
              requestParams: {},
              responseJson: ''
            };

            // 提取示例标题
            const h3 = wrapper.querySelector('h3');
            if (h3) {
              example.title = h3.textContent.trim();
            }

            // 提取示例描述
            const paraDiv = wrapper.querySelector('.docu-para');
            if (paraDiv) {
              example.description = paraDiv.textContent.trim();
            }

            // 提取请求参数（从 data-react-props）
            const integrationsDiv = wrapper.querySelector('[data-react-class="Integrations"]');
            if (integrationsDiv) {
              const reactProps = integrationsDiv.getAttribute('data-react-props');
              if (reactProps) {
                try {
                  const props = JSON.parse(reactProps);
                  if (props.params) {
                    example.requestParams = props.params;
                  }
                } catch (e) {
                  // 忽略解析错误
                }
              }
            }

            // 提取 JSON 响应示例
            const codeBlock = wrapper.querySelector('pre code.language-json');
            if (codeBlock) {
              example.responseJson = codeBlock.textContent.trim();
            }

            if (example.title) {
              result.examples.push(example);
            }
          });
        }

        // 提取重要说明
        const infoBoxes = document.querySelectorAll('.box-wrapper.main-text, .docu-para');
        const importantNotes = [];
        infoBoxes.forEach(box => {
          const text = box.textContent.trim();
          if (text.includes('page_token') || text.includes('serpapi_link') ||
              text.includes('extra request') || text.includes('expire')) {
            importantNotes.push(text);
          }
        });
        result.importantNotes = importantNotes;

        // 构建参数列表
        result.parameters = [
          { name: 'engine', type: 'string', required: true, description: 'Set to google to use the Google Search API' },
          { name: 'q', type: 'string', required: true, description: 'The search query' },
          { name: 'api_key', type: 'string', required: true, description: 'Your SerpApi API key' },
          { name: 'hl', type: 'string', required: false, description: 'Language code (e.g., en). AI Overview only works with hl=en' },
          { name: 'gl', type: 'string', required: false, description: 'Country code (e.g., us)' },
          { name: 'page_token', type: 'string', required: false, description: 'Token for additional AI Overview requests when needed' }
        ];

        // 构建响应结构
        result.responseStructure = [
          { path: 'ai_overview', type: 'object', description: 'AI Overview object containing the response' },
          { path: 'ai_overview.text_blocks', type: 'array', description: 'Array of text blocks (paragraphs, headings, lists)' },
          { path: 'ai_overview.references', type: 'array', description: 'Array of reference objects with links' },
          { path: 'ai_overview.images', type: 'array', description: 'Array of image objects' },
          { path: 'ai_overview.page_token', type: 'string', description: 'Token for additional requests when needed' },
          { path: 'ai_overview.serpapi_link', type: 'string', description: 'Link to SerpApi for additional requests' }
        ];

        // 提取原始内容
        const allText = [];
        document.querySelectorAll('h1, h2, h3, p, pre code').forEach(el => {
          const text = el.textContent.trim();
          if (text && text.length > 5) {
            allText.push(text);
          }
        });
        result.rawContent = allText.slice(0, 100).join('\n\n');

        return result;
      });

      return {
        type: 'serpapi-ai-overview',
        url,
        title: data.title,
        description: data.description,
        endpoint: data.endpoint,
        engine: data.engine,
        method: data.method,
        parameters: data.parameters,
        responseStructure: data.responseStructure,
        examples: data.examples,
        importantNotes: data.importantNotes,
        rawContent: data.rawContent,
        suggestedFilename: this.generateFilename(url)
      };
    } catch (error) {
      console.error('Failed to parse SerpApi AI Overview page:', error.message);
      return {
        type: 'serpapi-ai-overview',
        url,
        title: '',
        description: '',
        endpoint: 'https://serpapi.com/search',
        engine: 'google',
        method: 'GET',
        parameters: [],
        responseStructure: [],
        examples: [],
        importantNotes: [],
        rawContent: '',
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
      await page.waitForSelector('h1, .box-wrapper', { timeout: 15000 });
      await page.waitForTimeout(2000);
    } catch (error) {
      console.warn('Wait for content timeout, proceeding anyway:', error.message);
    }
  }
}

export default SerpApiParser;