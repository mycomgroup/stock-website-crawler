/**
 * Link Finder模块
 * 负责从页面中发现和提取符合规则的链接
 */

import { toAbsoluteUrl, filterLinks } from './url-utils.js';

/**
 * Link Finder类
 */
class LinkFinder {
  /**
   * 展开页面中的折叠内容
   * @param {Page} page - Playwright页面对象
   */
  async expandCollapsibles(page) {
      try {
        // 展开所有<details>元素
        await page.evaluate(() => {
          const details = document.querySelectorAll('details');
          details.forEach(detail => {
            detail.open = true;
          });
        });

        // 更激进的展开策略 - 点击所有可能的展开元素
        await page.evaluate(() => {
          // 点击所有可能的折叠菜单（排除details和summary，因为已经处理过了）
          document.querySelectorAll('[class*="collapse"]:not(details):not(summary), [class*="expand"]:not(details):not(summary)').forEach((el) => {
            try {
              el.click();
            } catch (_) {}
          });

          // 点击所有包含展开文本的按钮、链接、span、div
          document.querySelectorAll('button, a, span, div').forEach((el) => {
            const text = el.textContent || '';
            const className = el.className || '';
            if (text.includes('展开') || text.includes('▶') || text.includes('>') ||
                className.includes('expand') || className.includes('collapse')) {
              try {
                el.click();
              } catch (_) {}
            }
          });
        });

        await page.waitForTimeout(1500);

        // 再次尝试展开
        await page.evaluate(() => {
          document.querySelectorAll('[class*="collapse"]:not(details):not(summary), [class*="expand"]:not(details):not(summary)').forEach((el) => {
            try {
              el.click();
            } catch (_) {}
          });
        });

        await page.waitForTimeout(500);
      } catch (error) {
        // 展开失败不影响后续流程
        console.warn('Failed to expand collapsibles:', error.message);
      }
    }
  
  /**
   * 提取页面中的所有链接
   * @param {Page} page - Playwright页面对象
   * @param {Object} urlRules - URL过滤规则
   * @returns {string[]} URL数组
   */
  async extractLinks(page, urlRules) {
    try {
      // 获取当前页面的URL作为基础URL
      const baseUrl = page.url();
      
      // 从页面中提取所有链接
      // 优先查找包含 api-key 的链接（针对 lixinger.com 等API文档站点）
      const links = await page.evaluate(() => {
        const allLinks = new Set();
        
        // 查找所有包含 api-key 的链接
        document.querySelectorAll('a[href*="api-key="]').forEach((a) => {
          const href = a.getAttribute('href');
          if (href) {
            try {
              const url = href.startsWith('http') ? href : new URL(href, window.location.origin).href;
              
              // 验证 api-key 参数的有效性
              const urlObj = new URL(url);
              const apiKey = urlObj.searchParams.get('api-key');
              
              // 过滤掉无效的 api-key
              if (!apiKey || apiKey === 'undefined' || apiKey === 'null' || apiKey.trim() === '') {
                console.warn(`Skipped invalid api-key in URL: ${url}`);
                return; // 跳过这个链接
              }
              
              // 只保留 doc?api-key= 格式的链接
              if (url.includes('/open/api/doc') && url.includes('api-key=')) {
                allLinks.add(url);
              }
            } catch (_) {}
          }
        });
        
        // 如果没有找到 api-key 链接，则提取所有普通链接
        if (allLinks.size === 0) {
          const anchors = document.querySelectorAll('a[href]');
          anchors.forEach(a => allLinks.add(a.href));
        }
        
        return Array.from(allLinks);
      });
      
      // 转换为绝对URL
      const absoluteLinks = links.map(link => toAbsoluteUrl(link, baseUrl));
      
      // 去重
      const uniqueLinks = [...new Set(absoluteLinks)];
      
      // 过滤链接
      const filteredLinks = filterLinks(uniqueLinks, urlRules);
      
      return filteredLinks;
    } catch (error) {
      console.error('Failed to extract links:', error.message);
      return [];
    }
  }
}

export default LinkFinder;
