import BaseParser from './base-parser.js';

/**
 * Core Content Parser - 仅提取页面核心正文
 */
class CoreContentParser extends BaseParser {
  /**
   * 当配置为核心正文模式时匹配
   * @param {string} url - 页面URL
   * @param {Object} options - 解析选项
   * @returns {boolean} 是否匹配
   */
  matches(url, options = {}) {
    return options.parserMode === 'core-content';
  }

  /**
   * 获取优先级
   * @returns {number} 优先级
   */
  getPriority() {
    return 200;
  }

  /**
   * 解析核心正文
   * @param {Page} page - Playwright页面对象
   * @param {string} url - 页面URL
   * @returns {Promise<Object>} 核心正文数据
   */
  async parse(page, url) {
    try {
      const title = await this.extractTitle(page);
      const mainContent = await this.extractCoreContent(page);
      const contentText = mainContent
        .map(item => item.content || '')
        .filter(Boolean)
        .join('\n\n');

      return {
        type: 'core-content',
        url,
        title,
        mainContent,
        contentText
      };
    } catch (error) {
      console.error('Failed to parse core content page:', error.message);
      return {
        type: 'core-content',
        url,
        title: '',
        mainContent: [],
        contentText: ''
      };
    }
  }

  /**
   * 提取核心正文块
   * @param {Page} page - Playwright页面对象
   * @returns {Promise<Array>} 正文块
   */
  async extractCoreContent(page) {
    try {
      return await page.evaluate(() => {
        const removeSelectors = [
          'script', 'style', 'noscript',
          'nav', 'header', 'footer',
          'aside', '.sidebar', '.menu', '.breadcrumb',
          '[role="navigation"]', '[role="complementary"]',
          '.advertisement', '.ads', '.ad', '.popup'
        ];

        const container =
          document.querySelector('main article') ||
          document.querySelector('article') ||
          document.querySelector('main') ||
          document.querySelector('[role="main"]') ||
          document.querySelector('#content') ||
          document.body;

        const working = container.cloneNode(true);
        removeSelectors.forEach(selector => {
          working.querySelectorAll(selector).forEach(el => el.remove());
        });

        const nodes = Array.from(working.querySelectorAll('h1, h2, h3, h4, p, li'));
        const blocks = [];

        nodes.forEach(node => {
          const text = (node.textContent || '').replace(/\s+/g, ' ').trim();
          if (!text) return;

          // 过滤菜单/导航等短文本噪音
          if ((node.tagName === 'LI' || node.tagName === 'P') && text.length < 25) {
            return;
          }

          if (/^h[1-4]$/i.test(node.tagName)) {
            blocks.push({
              type: 'heading',
              level: Number(node.tagName.substring(1)),
              content: text
            });
          } else {
            blocks.push({
              type: 'paragraph',
              content: text
            });
          }
        });

        return blocks;
      });
    } catch (error) {
      console.error('Failed to extract core content:', error.message);
      return [];
    }
  }
}

export default CoreContentParser;
