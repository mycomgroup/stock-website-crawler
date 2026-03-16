import BaseParser from './base-parser.js';

/**
 * Aliyun Bailian MCP Parser - 解析阿里云百炼 MCP 市场页面
 * 主要 URL 规则：
 * - https://bailian.console.aliyun.com/cn-beijing/?tab=mcp#/mcp-market
 * - https://bailian.console.aliyun.com/cn-beijing/?tab=mcp#/...
 */
class AliyunBailianMcpParser extends BaseParser {
  matches(url) {
    return /^https?:\/\/bailian\.console\.aliyun\.com\/cn-beijing\/\?tab=mcp(?:#.*)?$/.test(url);
  }

  getPriority() {
    return 110;
  }

  async waitForContent(page) {
    try {
      await page.waitForLoadState('domcontentloaded', { timeout: 30000 });
      await page.waitForTimeout(2500);
    } catch (error) {
      console.warn('Aliyun Bailian MCP parser: wait timeout, continue with best-effort extraction.');
    }
  }

  async parse(page, url) {
    try {
      await this.waitForContent(page);

      const data = await page.evaluate(() => {
        const normalizeText = (text = '') => text.replace(/\s+/g, ' ').trim();

        const title = normalizeText(
          document.querySelector('h1')?.textContent ||
          document.querySelector('title')?.textContent ||
          'Aliyun Bailian MCP'
        );

        const pageText = normalizeText(document.body?.innerText || '');

        const links = [];
        const seen = new Set();

        document.querySelectorAll('a[href]').forEach((a) => {
          const href = a.getAttribute('href') || '';
          if (!href) return;

          const fullUrl = href.startsWith('http') ? href : new URL(href, window.location.origin).toString();

          // 只保留 MCP 相关路由
          if (!fullUrl.includes('bailian.console.aliyun.com')) return;
          if (!fullUrl.includes('tab=mcp')) return;

          if (!seen.has(fullUrl)) {
            seen.add(fullUrl);
            links.push({
              text: normalizeText(a.textContent || ''),
              url: fullUrl
            });
          }
        });

        // 抽取 hash 路由（规则分析重点）
        const routeLinks = links
          .filter((item) => item.url.includes('#/'))
          .map((item) => {
            const route = item.url.split('#')[1] || '';
            return {
              ...item,
              route,
              routeBase: route.split('?')[0]
            };
          });

        const routeBases = Array.from(new Set(routeLinks.map((l) => l.routeBase).filter(Boolean))).sort();

        return {
          title,
          description: pageText.slice(0, 500),
          routeRules: {
            prefix: 'https://bailian.console.aliyun.com/cn-beijing/?tab=mcp#',
            routeBases
          },
          routeLinks,
          links,
          rawContentLength: pageText.length
        };
      });

      return {
        type: 'aliyun-bailian-mcp',
        url,
        title: data.title,
        description: data.description,
        routeRules: data.routeRules,
        routeLinks: data.routeLinks,
        links: data.links,
        rawContentLength: data.rawContentLength,
        tables: [],
        codeBlocks: []
      };
    } catch (error) {
      console.error('Failed to parse aliyun bailian mcp page:', error.message);
      return {
        type: 'aliyun-bailian-mcp',
        url,
        title: '',
        description: '',
        routeRules: {
          prefix: 'https://bailian.console.aliyun.com/cn-beijing/?tab=mcp#',
          routeBases: []
        },
        routeLinks: [],
        links: [],
        rawContentLength: 0,
        tables: [],
        codeBlocks: []
      };
    }
  }
}

export default AliyunBailianMcpParser;
