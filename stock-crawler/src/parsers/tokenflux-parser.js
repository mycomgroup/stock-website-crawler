import BaseParser from './base-parser.js';

/**
 * TokenFlux Parser - 解析 tokenflux.ai 的 docs 与 MCP 页面
 */
class TokenfluxParser extends BaseParser {
  matches(url) {
    return /^https?:\/\/tokenflux\.ai\/(docs\/quickstart|mcps(?:\/.*)?)/.test(url);
  }

  getPriority() {
    return 110;
  }

  generateFilename(url) {
    try {
      const urlObj = new URL(url);
      let pathname = urlObj.pathname.replace(/^\//, '').replace(/\/$/, '');
      if (!pathname) return 'tokenflux_index';
      return pathname.replace(/\//g, '_');
    } catch (e) {
      return 'tokenflux_page';
    }
  }

  async waitForContent(page) {
    await page.waitForLoadState('domcontentloaded', { timeout: 15000 }).catch(() => {});
    await page.waitForLoadState('networkidle', { timeout: 20000 }).catch(() => {});
    await page.waitForSelector('main, #app, h1', { timeout: 15000 }).catch(() => {});
    await page.waitForTimeout(1500).catch(() => {});
  }

  async parse(page, url, options = {}) {
    await this.waitForContent(page);

    const data = await page.evaluate(() => {
      const text = (el) => (el?.textContent || '').trim();
      const unique = (items) => [...new Set(items.filter(Boolean))];

      const title = text(document.querySelector('h1')) ||
        text(document.querySelector('title')) ||
        'Untitled';

      const description =
        document.querySelector('meta[name="description"]')?.getAttribute('content')?.trim() || '';

      const main = document.querySelector('main') || document.querySelector('#app') || document.body;

      const links = unique(
        Array.from(document.querySelectorAll('a[href]'))
          .map((a) => a.getAttribute('href'))
          .map((href) => {
            if (!href) return null;
            if (href.startsWith('http')) return href;
            if (href.startsWith('/')) return `${location.origin}${href}`;
            return null;
          })
      );

      const headings = Array.from(main.querySelectorAll('h2, h3'))
        .map((h) => text(h))
        .filter(Boolean);

      const paragraphs = Array.from(main.querySelectorAll('p'))
        .map((p) => text(p))
        .filter((p) => p.length > 20)
        .slice(0, 80);

      const listItems = Array.from(main.querySelectorAll('li'))
        .map((li) => text(li))
        .filter((li) => li.length > 0)
        .slice(0, 150);

      const codeBlocks = Array.from(main.querySelectorAll('pre, code'))
        .map((el) => text(el))
        .filter((code) => code.length > 20)
        .slice(0, 50)
        .map((code) => ({ language: '', code }));

      return {
        title,
        description,
        headings,
        paragraphs,
        listItems,
        codeBlocks,
        links
      };
    });

    const content = [];

    if (data.description) {
      content.push({ type: 'text', content: data.description });
    }

    data.headings.forEach((heading) => {
      content.push({ type: 'heading', content: heading });
    });

    data.paragraphs.forEach((paragraph) => {
      content.push({ type: 'text', content: paragraph });
    });

    if (data.listItems.length > 0) {
      content.push({ type: 'list', items: data.listItems });
    }

    data.codeBlocks.forEach((block) => {
      content.push({ type: 'code', language: block.language, code: block.code });
    });

    return {
      type: 'tokenflux-doc',
      url,
      title: data.title,
      description: data.description,
      content,
      links: data.links,
      metadata: {
        platform: 'tokenflux',
        section: url.includes('/mcps') ? 'mcps' : 'docs'
      }
    };
  }
}

export default TokenfluxParser;
