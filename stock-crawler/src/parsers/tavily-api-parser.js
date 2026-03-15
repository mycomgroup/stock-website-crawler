import BaseParser from './base-parser.js';

/**
 * Tavily API Parser - 专门解析 docs.tavily.com/documentation/api-reference 文档页面
 * Tavily 是一个 AI 搜索 API 服务，提供网页搜索、内容提取等功能
 * 文档页面使用 Mintlify/Next.js，需要精确提取主内容区域
 */
class TavilyApiParser extends BaseParser {
  /**
   * 匹配 Tavily API 文档页面
   * @param {string} url - 页面URL
   * @returns {boolean} 是否匹配
   */
  matches(url) {
    return /^https?:\/\/docs\.tavily\.com\/documentation\/api-reference/.test(url);
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
      // 移除 /documentation/api-reference 前缀
      pathname = pathname.replace(/^\/documentation\/api-reference\/?/, '');
      pathname = pathname.replace(/\/$/, '');
      const filename = pathname.replace(/\//g, '_') || 'api_overview';
      return filename;
    } catch (e) {
      return 'api_doc';
    }
  }

  /**
   * 从 URL 提取 API 路径
   * @param {string} url - 页面URL
   * @returns {string} API 路径（不含前导斜杠）
   */
  extractApiPath(url) {
    try {
      const urlObj = new URL(url);
      let pathname = urlObj.pathname;
      // 移除 /documentation/api-reference 前缀
      pathname = pathname.replace(/^\/documentation\/api-reference\/?/, '');
      return pathname;
    } catch (e) {
      return '';
    }
  }

  /**
   * 解析 Tavily API 文档页面
   * @param {Page} page - Playwright页面对象
   * @param {string} url - 页面URL
   * @param {Object} options - 解析选项
   * @returns {Promise<Object>} 解析后的页面数据
   */
  async parse(page, url, options = {}) {
    try {
      // 等待页面内容加载完成
      await this.waitForContent(page);

      // 从 URL 提取 API 路径
      const apiPath = this.extractApiPath(url);

      // 从页面提取内容
      const data = await page.evaluate((targetPath) => {
        const result = {
          title: '',
          description: '',
          method: '',
          endpoint: '',
          baseUrl: 'https://api.tavily.com',
          parameters: [],
          requestHeaders: [],
          requestBody: null,
          responseStructure: [],
          examples: [],
          mainContent: [],
          rawContent: ''
        };

        // 提取标题
        const h1 = document.querySelector('h1');
        if (h1) {
          result.title = h1.textContent.trim();
        }

        // 提取 HTTP 方法和端点（Tavily 特殊结构）
        // 方法显示在 method-pill 元素中
        const methodPill = document.querySelector('[class*="method-pill"]');
        if (methodPill) {
          const methodText = methodPill.textContent.trim();
          if (['GET', 'POST', 'PUT', 'DELETE', 'PATCH'].includes(methodText.toUpperCase())) {
            result.method = methodText.toUpperCase();
          }
        }

        // 端点路径通常在 method-pill 后面的元素中
        // 查找包含 "/" 开头文本的容器
        const methodContainer = document.querySelector('[class*="flex"][class*="items-center"][class*="gap"]');
        if (methodContainer) {
          const containerText = methodContainer.textContent || '';
          // 提取端点路径（以 / 开头的文本）
          const pathMatch = containerText.match(/\/[a-zA-Z0-9_\-\/]+/);
          if (pathMatch) {
            result.endpoint = pathMatch[0];
          }
        }

        // 如果还没找到端点，从 URL 路径推断
        if (!result.endpoint && targetPath && targetPath.startsWith('endpoint/')) {
          const endpointName = targetPath.replace('endpoint/', '');
          result.endpoint = '/' + endpointName;
        }

        // 提取描述
        const metaDesc = document.querySelector('meta[name="description"]');
        if (metaDesc) {
          result.description = metaDesc.getAttribute('content') || '';
        }

        // Mintlify 文档结构：查找主内容区域
        // 优先使用特定的内容选择器，排除导航和侧边栏
        let mainContentDiv = null;

        // 方法1: 查找包含 mdx 的容器（Mintlify 特征）
        const mdxContainer = document.querySelector('[class*="mdx"]');
        if (mdxContainer && mdxContainer.textContent.length > 1000) {
          mainContentDiv = mdxContainer;
        }

        // 方法2: 查找包含 API 文档特征的 div
        if (!mainContentDiv) {
          const allDivs = document.querySelectorAll('div');
          for (const div of allDivs) {
            const text = div.innerText || '';
            const classList = (div.className || '').toString();

            // 排除导航、侧边栏、页脚
            if (classList.includes('nav') || classList.includes('sidebar') ||
                classList.includes('header') || classList.includes('footer') ||
                classList.includes('menu')) {
              continue;
            }

            // 寻找包含 API 文档特征的内容
            const hasApiFeatures = text.includes('Authorization') ||
                                   text.includes('Parameters') ||
                                   text.includes('Response') ||
                                   text.includes('request');

            // 内容应该适中大小，不包含过多导航元素
            if (hasApiFeatures && text.length > 3000 && text.length < 15000) {
              // 检查是否包含大量导航链接（排除）
              const links = div.querySelectorAll('a');
              const linkCount = links.length;
              // 如果链接太多，可能是包含侧边栏的容器
              if (linkCount < 30) {
                mainContentDiv = div;
                break;
              }
            }
          }
        }

        // 方法3: 回退到包含 h1 的内容区域
        if (!mainContentDiv && h1) {
          let parent = h1.parentElement;
          while (parent) {
            const text = parent.innerText || '';
            if (text.length > 3000 && text.length < 15000) {
              mainContentDiv = parent;
              break;
            }
            parent = parent.parentElement;
          }
        }

        // ========== 提取 Mintlify 参数结构 ==========
        // Mintlify 使用 param-field 类来标记参数
        // 格式: ​paramNametype[default:value][required][header]Description...
        const extractMintlifyParams = () => {
          const params = [];
          const paramSelectors = [
            '[class*="primitive-param-field"]',
            '[class*="object-param-field"]',
            '[class*="array-param-field"]'
          ];

          // 已知的类型关键字（按长度降序排列，确保优先匹配更长的类型）
          const typePatterns = [
            'enum(?:<[^>]+>)?',
            'string\\[\\]',      // string[] 数组类型
            'integer',
            'number(?:<[^>]+>)?',
            'boolean',
            'string',
            'object',
            'array'
          ];

          paramSelectors.forEach(selector => {
            const paramFields = document.querySelectorAll(selector);
            paramFields.forEach(field => {
              const text = field.textContent || '';

              // Mintlify 文本格式解析:
              // 零宽度空格 + 参数名 + 类型 + [default:xxx] + [required] + [header/body/query] + 描述

              // 移除开头的零宽度空格
              let cleanText = text.replace(/^[\u200B\u200C\u200D]+/, '');

              // 移除可能混入的 CSS 内容
              if (cleanText.includes('#opt-') || cleanText.includes(':has(') || cleanText.includes('display:')) {
                cleanText = cleanText.split(/#opt-|:has\(|display:/)[0];
              }

              // 使用动态构建的正则，类型按长度排序确保正确匹配
              const typeGroup = typePatterns.join('|');
              // 参数名不能以已知类型关键字结尾
              const paramPattern = new RegExp(
                `^([a-zA-Z_][a-zA-Z0-9_\\[\\]\\.]*?)(${typeGroup})(header|body|query|path)?(required)?(?:default:([^\\s\\u200B]+))?([\\s\\S]*)$`,
                'i'
              );

              const match = cleanText.match(paramPattern);

              if (match) {
                let paramName = match[1];
                const paramType = match[2];
                const location = match[3] || '';
                const isRequired = !!match[4];
                const defaultValue = (match[5] || '').replace(/[\u200B\u200C\u200D]+/g, '').trim();
                let description = match[6] || '';

                // 清理描述
                description = description
                  .replace(/^[\u200B\u200C\u200D\s:]+/, '')
                  .replace(/[\u200B\u200C\u200D]+/g, ' ')
                  .trim()
                  .substring(0, 500);

                // 验证参数名不以类型关键字结尾（避免错误分割）
                const typeCheckPattern = new RegExp(`(${typePatterns.join('|')})$`, 'i');
                if (typeCheckPattern.test(paramName)) {
                  // 参数名以类型结尾，这是错误的分割，跳过
                  console.log('Skipping invalid param split:', paramName, paramType);
                } else if (paramName && description.length > 5) {
                  const param = {
                    name: paramName,
                    type: paramType.toLowerCase(),
                    required: isRequired,
                    default: defaultValue,
                    description: description
                  };
                  if (location) {
                    param.location = location.toLowerCase();
                  }
                  params.push(param);
                }
              } else {
                // 回退：尝试简单提取参数名（以空格或特殊字符结束）
                const simpleMatch = cleanText.match(/^([a-zA-Z_][a-zA-Z0-9_\[\]\.]{2,40}?)(?=[A-Z][a-z]|\\s|\\u200B|$)/);
                if (simpleMatch) {
                  params.push({
                    name: simpleMatch[1],
                    type: '',
                    required: false,
                    default: '',
                    description: cleanText.substring(simpleMatch[1].length).substring(0, 500)
                  });
                }
              }
            });
          });

          return params;
        };

        // 提取参数
        const mintlifyParams = extractMintlifyParams();
        if (mintlifyParams.length > 0) {
          result.parameters = mintlifyParams;
        }

        // 提取混排内容（按顺序）
        if (mainContentDiv) {
          // 用于过滤导航/UI文本
          const skipTexts = [
            'Skip to main content',
            'Tavily Docs home page',
            'Search...',
            '⌘K',
            'Ask AI',
            'Support',
            'Get an API key',
            'Copy page',
            'Copy',
            'Powered by',
            'This documentation is built and hosted on Mintlify',
            'Previous',
            'Next',
            '⌘I'
          ];

          const isUiText = (text) => {
            return skipTexts.some(skip => text.includes(skip)) && text.length < 100;
          };

          const extractContent = (element) => {
            const items = [];

            // 遍历所有子元素
            const walk = (el) => {
              if (!el || el.tagName === 'SCRIPT' || el.tagName === 'STYLE' ||
                  el.tagName === 'NOSCRIPT' || el.tagName === 'NAV' ||
                  el.tagName === 'HEADER' || el.tagName === 'FOOTER') return;

              const tagName = el.tagName;
              const classList = (el.className || '').toString();

              // 跳过导航和侧边栏
              if (classList.includes('nav') || classList.includes('sidebar') ||
                  classList.includes('menu') || classList.includes('toc')) {
                return;
              }

              // Mintlify 参数结构检测
              // Mintlify 使用特定的类名模式来标记参数
              if (classList.includes('param') || classList.includes('property') ||
                  classList.includes('request-body') || classList.includes('field')) {
                const paramName = el.querySelector('code, [class*="name"], [class*="key"]');
                const paramType = el.querySelector('[class*="type"]');
                const paramDesc = el.querySelector('[class*="desc"], [class*="description"]');

                if (paramName || paramDesc) {
                  const name = paramName ? paramName.textContent.trim() : '';
                  const type = paramType ? paramType.textContent.trim() : '';
                  const desc = paramDesc ? paramDesc.textContent.trim() : el.textContent.trim();

                  items.push({
                    type: 'parameter',
                    name,
                    paramType: type,
                    description: desc
                  });
                  return; // 不再递归处理这个元素
                }
              }

              // 检测 Mintlify 的参数列表结构
              // 通常是 div 容器包含参数名（code 元素）和描述
              const paramCode = el.querySelector(':scope > code, :scope > strong > code');
              if (paramCode && tagName === 'DIV') {
                const paramName = paramCode.textContent.trim();
                const siblings = Array.from(el.children);
                let description = '';

                // 收集参数名之后的文本作为描述
                siblings.forEach(sibling => {
                  if (sibling !== paramCode && sibling.tagName !== 'CODE') {
                    description += ' ' + sibling.textContent.trim();
                  }
                });
                description = description.trim() || el.textContent.replace(paramName, '').trim();

                if (paramName && description) {
                  items.push({
                    type: 'parameter',
                    name: paramName,
                    description: description
                  });
                  return;
                }
              }

              // 标题
              if (/^H[1-6]$/.test(tagName)) {
                const text = el.textContent.trim();
                if (text && !isUiText(text)) {
                  items.push({
                    type: 'heading',
                    level: parseInt(tagName[1]),
                    content: text
                  });
                }
              }
              // 段落
              else if (tagName === 'P') {
                const text = el.textContent.trim();
                if (text && text.length > 10 && !isUiText(text)) {
                  items.push({
                    type: 'paragraph',
                    content: text
                  });
                }
              }
              // 代码块
              else if (tagName === 'PRE') {
                const code = el.querySelector('code') || el;
                const text = code.textContent.trim();
                if (text && !isUiText(text)) {
                  // 检测语言
                  let language = 'text';
                  const codeClassList = code.className || '';
                  if (codeClassList.includes('json') || text.startsWith('{') || text.startsWith('[')) {
                    language = 'json';
                  } else if (codeClassList.includes('python') || text.includes('import ') || text.includes('def ')) {
                    language = 'python';
                  } else if (codeClassList.includes('javascript') || text.includes('const ') || text.includes('function ')) {
                    language = 'javascript';
                  } else if (codeClassList.includes('bash') || text.includes('curl ') || text.includes('npm ')) {
                    language = 'bash';
                  }

                  items.push({
                    type: 'codeblock',
                    language,
                    content: text.substring(0, 10000) // 限制长度
                  });
                }
              }
              // 行内代码（包含路径或方法）
              else if (tagName === 'CODE' && !el.closest('pre')) {
                const text = el.textContent.trim();
                // 检测 HTTP 方法
                if (['GET', 'POST', 'PUT', 'DELETE', 'PATCH'].includes(text.toUpperCase())) {
                  result.method = text.toUpperCase();
                }
                // 检测端点路径
                else if (text.startsWith('/') && !text.includes(' ')) {
                  result.endpoint = text;
                }
              }
              // 列表
              else if (tagName === 'UL' || tagName === 'OL') {
                const listItems = [];
                el.querySelectorAll(':scope > li').forEach(li => {
                  const text = li.textContent.trim();
                  if (text && !isUiText(text)) listItems.push(text);
                });
                if (listItems.length > 0) {
                  items.push({
                    type: 'list',
                    listType: tagName.toLowerCase(),
                    items: listItems
                  });
                }
              }
              // 表格
              else if (tagName === 'TABLE') {
                const table = { headers: [], rows: [] };

                // 提取表头
                const headerRow = el.querySelector('thead tr, tr:first-child');
                if (headerRow) {
                  headerRow.querySelectorAll('th, td').forEach(cell => {
                    table.headers.push(cell.textContent.trim());
                  });
                }

                // 提取数据行
                const bodyRows = el.querySelectorAll('tbody tr, tr:not(:first-child)');
                bodyRows.forEach(row => {
                  const rowData = [];
                  row.querySelectorAll('td, th').forEach(cell => {
                    rowData.push(cell.textContent.trim());
                  });
                  if (rowData.length > 0) {
                    table.rows.push(rowData);
                  }
                });

                if (table.headers.length > 0 || table.rows.length > 0) {
                  items.push({
                    type: 'table',
                    ...table
                  });

                  // 如果表格包含参数信息，提取参数
                  if (table.headers.some(h => h.toLowerCase().includes('name') || h.toLowerCase().includes('param'))) {
                    const nameIdx = table.headers.findIndex(h => h.toLowerCase().includes('name'));
                    const typeIdx = table.headers.findIndex(h => h.toLowerCase().includes('type'));
                    const reqIdx = table.headers.findIndex(h => h.toLowerCase().includes('required'));
                    const descIdx = table.headers.findIndex(h => h.toLowerCase().includes('desc'));

                    table.rows.forEach(row => {
                      result.parameters.push({
                        name: nameIdx >= 0 ? row[nameIdx] || '' : row[0] || '',
                        type: typeIdx >= 0 ? row[typeIdx] || '' : '',
                        required: reqIdx >= 0 ? (row[reqIdx] || '').toLowerCase().includes('true') || row[reqIdx] === '是' : false,
                        description: descIdx >= 0 ? row[descIdx] || '' : ''
                      });
                    });
                  }
                }
              }
              // 引用块
              else if (tagName === 'BLOCKQUOTE') {
                const text = el.textContent.trim();
                if (text && !isUiText(text)) {
                  items.push({
                    type: 'blockquote',
                    content: text
                  });
                }
              }
              // 递归处理子元素
              else if (el.children && el.children.length > 0) {
                Array.from(el.children).forEach(child => walk(child));
              }
            };

            walk(element);
            return items;
          };

          result.mainContent = extractContent(mainContentDiv);

          // 提取清理后的原始内容
          let rawText = mainContentDiv.innerText || '';
          // 移除UI文本
          skipTexts.forEach(skip => {
            rawText = rawText.replace(new RegExp(skip.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g'), '');
          });
          result.rawContent = rawText.trim();
        }

        // 提取代码示例
        const codeBlocks = document.querySelectorAll('pre');
        codeBlocks.forEach(pre => {
          const code = pre.querySelector('code') || pre;
          const text = code.textContent.trim();

          let language = 'text';
          const classList = code.className || '';
          if (classList.includes('json') || text.startsWith('{')) {
            language = 'json';
          } else if (classList.includes('python')) {
            language = 'python';
          } else if (classList.includes('javascript')) {
            language = 'javascript';
          } else if (classList.includes('bash') || text.includes('curl')) {
            language = 'bash';
          }

          if (text.length > 10) {
            result.examples.push({
              language,
              code: text.substring(0, 5000)
            });
          }
        });

        return result;
      }, apiPath);

      return {
        type: 'tavily-api',
        url,
        title: data.title,
        description: data.description,
        method: data.method,
        endpoint: data.endpoint,
        baseUrl: data.baseUrl,
        parameters: data.parameters,
        requestHeaders: data.requestHeaders,
        requestBody: data.requestBody,
        responseStructure: data.responseStructure,
        examples: data.examples,
        mainContent: data.mainContent,
        rawContent: data.rawContent,
        suggestedFilename: this.generateFilename(url)
      };
    } catch (error) {
      console.error('Failed to parse Tavily API doc page:', error.message);
      return {
        type: 'tavily-api',
        url,
        title: '',
        description: '',
        method: '',
        endpoint: '',
        baseUrl: 'https://api.tavily.com',
        parameters: [],
        requestHeaders: [],
        requestBody: null,
        responseStructure: [],
        examples: [],
        mainContent: [],
        rawContent: '',
        suggestedFilename: this.generateFilename(url)
      };
    }
  }

  /**
   * 等待页面内容加载完成
   * @param {Page} page - Playwright页面对象
   */
  async waitForContent(page) {
    try {
      await page.waitForLoadState('networkidle', { timeout: 30000 });
      // 等待主要内容区域出现
      await page.waitForSelector('h1', { timeout: 15000 });
      // 额外等待动态内容
      await page.waitForTimeout(3000);
    } catch (error) {
      console.warn('Wait for content timeout, proceeding anyway:', error.message);
    }
  }
}

export default TavilyApiParser;