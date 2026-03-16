import GenericParser from './generic-parser.js';

/**
 * 302.AI 文档站解析器
 * 入口示例: https://doc.302.ai
 */
class Ai302DocsParser extends GenericParser {
  matches(url) {
    return /^https?:\/\/doc\.302\.ai(?:\/.*)?$/.test(url);
  }

  getPriority() {
    return 115;
  }

  supportsLinkDiscovery() {
    return true;
  }

  async discoverLinks(page) {
    try {
      await page.waitForSelector('a[href]', { timeout: 15000 }).catch(() => {});
      await page.waitForTimeout(1200);

      const links = await page.evaluate(() => {
        const results = new Set();

        const addIfDocUrl = (candidate) => {
          if (!candidate) return;

          let absolute = candidate;
          if (!candidate.startsWith('http')) {
            absolute = new URL(candidate, window.location.origin).href;
          }

          let parsed;
          try {
            parsed = new URL(absolute);
          } catch {
            return;
          }

          if (parsed.hostname !== 'doc.302.ai') return;

          const normalized = `${parsed.origin}${parsed.pathname}`;
          if (parsed.pathname === '/' || /^\/\d+[de]0$/.test(parsed.pathname)) {
            results.add(normalized);
          }
        };

        document.querySelectorAll('a[href]').forEach((anchor) => {
          addIfDocUrl(anchor.getAttribute('href') || '');
        });

        const html = document.documentElement?.innerHTML || '';
        const matches = html.match(/\/\d+[de]0/g) || [];
        matches.forEach((path) => addIfDocUrl(path));

        return Array.from(results);
      });

      return links;
    } catch (error) {
      console.warn('[Ai302DocsParser] discoverLinks failed:', error.message);
      return [];
    }
  }

  async parse(page, url, options = {}) {
    await page.waitForSelector('main, h1, article, [class*="content"]', { timeout: 15000 }).catch(() => {});
    await page.waitForTimeout(1000);
    return super.parse(page, url, options);
  }
}

export default Ai302DocsParser;
