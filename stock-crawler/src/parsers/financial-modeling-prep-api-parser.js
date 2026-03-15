import BaseParser from './base-parser.js';

/**
 * Financial Modeling Prep API Parser - 专门解析 financialmodelingprep.com/developer/docs API 文档页面
 * Financial Modeling Prep 使用 SPA 架构，参数表格和响应示例通过 JavaScript 动态渲染
 */
class FinancialModelingPrepApiParser extends BaseParser {
  /**
   * 匹配 Financial Modeling Prep API 文档页面
   * @param {string} url - 页面URL
   * @returns {boolean} 是否匹配
   */
  matches(url) {
    return /^https?:\/\/site\.financialmodelingprep\.com\/developer\/docs/.test(url);
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
      // 移除 /developer/docs 前缀
      pathname = pathname.replace(/^\/developer\/docs\/?/, '');
      pathname = pathname.replace(/\/$/, '');

      // 如果有 hash，使用 hash 作为文件名
      const hash = urlObj.hash.replace('#', '');
      if (hash) {
        return hash.replace(/\//g, '_');
      }

      const filename = pathname.replace(/\//g, '_') || 'api_overview';
      return filename;
    } catch (e) {
      return 'api_doc';
    }
  }

  /**
   * 解析 Financial Modeling Prep API 文档页面
   * @param {Page} page - Playwright页面对象
   * @param {string} url - 页面URL
   * @param {Object} options - 解析选项
   * @returns {Promise<Object>} 解析后的页面数据
   */
  async parse(page, url, options = {}) {
    try {
      // 等待 SPA 内容加载完成
      await this.waitForContent(page);

      // 提取结构化的 API 文档内容
      const data = await page.evaluate(() => {
        const result = {
          title: '',
          description: '',
          sections: []
        };

        // 查找主内容区域
        const wrapper = document.querySelector('[class*="documentationWrapper"]');
        if (!wrapper) {
          return result;
        }

        // 提取标题
        const h1 = wrapper.querySelector('h1');
        if (h1) {
          result.title = h1.textContent.trim();
        }

        // 提取描述（h1 后的第一段文本）
        if (h1) {
          let sibling = h1.nextElementSibling;
          while (sibling) {
            if (sibling.tagName.toLowerCase() === 'p') {
              const text = sibling.textContent.trim();
              if (text.length > 30 && !text.startsWith('Endpoint:')) {
                result.description = text;
                break;
              }
            }
            sibling = sibling.nextElementSibling;
          }
        }

        // 遍历所有子元素
        const children = Array.from(wrapper.children);

        for (const child of children) {
          const tagName = child.tagName.toLowerCase();
          const text = child.textContent?.trim() || '';
          const className = child.className || '';

          // H4 是小节标题（如 Authorization）
          if (tagName === 'h4') {
            result.sections.push({
              type: 'section',
              title: text,
              content: ''
            });
            continue;
          }

          // P 标签可能是描述
          if (tagName === 'p' && result.sections.length > 0) {
            const lastSection = result.sections[result.sections.length - 1];
            if (lastSection.type === 'section' && text.length > 10 && !text.startsWith('Endpoint:')) {
              lastSection.content += (lastSection.content ? '\n\n' : '') + text;
            }
          }

          // DIV 没有类名的包含 API 分类
          if (tagName === 'div' && !className) {
            const h2 = child.querySelector('h2');
            if (h2) {
              const categoryTitle = h2.textContent.trim();

              // 提取该分类下的完整文本内容
              // API 条目的结构: 标题DIV -> 描述DIV -> 端点DIV -> P(Parameters) -> 空DIV -> 空DIV -> 下一个API...
              const apis = [];
              const apiChildren = Array.from(child.children);

              // 跳过 H2 标题
              let i = 1;
              while (i < apiChildren.length) {
                const apiChild = apiChildren[i];
                const apiTag = apiChild.tagName.toLowerCase();
                const apiText = apiChild.textContent?.trim() || '';
                const apiClass = apiChild.className || '';

                // 跳过空 DIV（响应占位符）
                if (apiTag === 'div' && !apiText) {
                  i++;
                  continue;
                }

                // 检测 API 标题：以 "API" 结尾且不太长的文本
                if (apiTag === 'div' && apiText.includes('API') && apiText.length < 80) {
                  const currentApi = {
                    title: apiText,
                    description: '',
                    endpoint: ''
                  };

                  // 下一个 DIV 应该是描述
                  if (i + 1 < apiChildren.length) {
                    const nextDiv = apiChildren[i + 1];
                    if (nextDiv.tagName === 'DIV') {
                      const nextText = nextDiv.textContent?.trim() || '';
                      // 描述通常很长
                      if (nextText.length > 50 && !nextText.startsWith('Endpoint:')) {
                        currentApi.description = nextText;
                        i++; // 跳过已处理的描述
                      }
                    }
                  }

                  // 再下一个 DIV 应该是端点
                  if (i + 1 < apiChildren.length) {
                    const endpointDiv = apiChildren[i + 1];
                    if (endpointDiv.tagName === 'DIV') {
                      const endpointText = endpointDiv.textContent?.trim() || '';
                      if (endpointText.startsWith('Endpoint:')) {
                        const match = endpointText.match(/Endpoint:\s*(https?:\/\/[^\s]+)/);
                        if (match) {
                          currentApi.endpoint = match[1];
                          i++; // 跳过已处理的端点
                        }
                      }
                    }
                  }

                  apis.push(currentApi);
                }

                // 跳过 Parameters P 标签
                if (apiTag === 'p' && apiText === 'Parameters') {
                  // 下两个应该是空的响应占位符
                  i += 2;
                }

                i++;
              }

              result.sections.push({
                type: 'category',
                title: categoryTitle,
                apis: apis.filter(api => api.title && !api.title.includes('Stock Directory')) // 过滤无效条目
              });
            }
          }
        }

        return result;
      });

      // 将结构化数据转换为 Markdown
      const markdown = this.convertToMarkdown(data);

      return {
        type: 'financial-modeling-prep-api',
        url,
        title: data.title,
        description: data.description,
        markdownContent: markdown,
        rawContent: '',
        suggestedFilename: this.generateFilename(url)
      };
    } catch (error) {
      console.error('Failed to parse Financial Modeling Prep API doc page:', error.message);
      return {
        type: 'financial-modeling-prep-api',
        url,
        title: '',
        description: '',
        markdownContent: '',
        rawContent: '',
        suggestedFilename: this.generateFilename(url)
      };
    }
  }

  /**
   * 将结构化数据转换为 Markdown
   */
  convertToMarkdown(data) {
    const lines = [];

    // 主标题
    if (data.title) {
      lines.push(`# ${data.title}`, '');
    }

    // 描述
    if (data.description) {
      lines.push(data.description, '');
    }

    // 各部分
    for (const section of data.sections) {
      if (section.type === 'category') {
        // 分类标题
        lines.push('', `## ${section.title}`, '');

        // 该分类下的 API
        for (const api of section.apis || []) {
          if (api.title) {
            lines.push(`### ${api.title}`, '');
          }
          if (api.description) {
            lines.push(api.description, '');
          }
          if (api.endpoint) {
            lines.push('**Endpoint:**', '');
            lines.push('```text');
            lines.push(api.endpoint);
            lines.push('```', '');
          }
          if (api.hasParams) {
            lines.push('> **Parameters:** See the API documentation for parameter details.', '');
          }
          lines.push('---', '');
        }
      } else if (section.type === 'section') {
        // 小节标题
        lines.push('', `#### ${section.title}`, '');
        if (section.content) {
          lines.push(section.content, '');
        }
        if (section.endpoint) {
          lines.push('**Endpoint:**', '');
          lines.push('```text');
          lines.push(section.endpoint);
          lines.push('```', '');
        }
      }
    }

    return lines.join('\n');
  }

  /**
   * 等待 SPA 内容加载完成
   */
  async waitForContent(page) {
    try {
      await page.waitForLoadState('domcontentloaded', { timeout: 30000 });
      await page.waitForSelector('h1, h2', { timeout: 15000 });
      await page.waitForTimeout(3000);
    } catch (error) {
      console.warn('Wait for content timeout, proceeding anyway:', error.message);
    }
  }
}

export default FinancialModelingPrepApiParser;