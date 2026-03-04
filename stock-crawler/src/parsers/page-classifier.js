/**
 * Page Classifier - 页面分类器
 * 输出标准化分类结果：type + confidence + reasons + features
 */
class PageClassifier {
  /**
   * 分类页面
   * @param {Page} page - Playwright页面对象
   * @param {string} url - 页面URL
   * @returns {Promise<Object>} 分类结果
   */
  async classify(page, url) {
    const urlFeatures = this.extractUrlFeatures(url);

    if (urlFeatures.apiPattern) {
      return this.buildResult('api_doc_page', 0.95, ['url-api-pattern'], urlFeatures);
    }

    let domFeatures = {};
    try {
      domFeatures = await this.extractDomFeatures(page);
    } catch (error) {
      return this.buildResult('generic_page', 0.2, ['dom-features-failed'], {
        ...urlFeatures,
        domError: error.message
      });
    }

    return this.classifyByRules({ ...urlFeatures, ...domFeatures });
  }

  extractUrlFeatures(url = '') {
    const normalized = String(url).toLowerCase();
    return {
      url,
      apiPattern: /\/api\/(doc|docs|reference)?/.test(normalized),
      listHint: /(\/list|\/category|\/catalog|page=\d+|\/news)/.test(normalized),
      directoryHint: /(\/directory|\/index|\/menu|\/guide|\/docs)/.test(normalized),
      detailHint: /(\/detail|\/article|\/post|id=\d+)/.test(normalized)
    };
  }

  async extractDomFeatures(page) {
    return await page.evaluate(() => {
      const clean = (text = '') => text.replace(/\s+/g, ' ').trim();
      const body = document.body;

      const totalText = clean(body?.innerText || '');
      const totalTextLength = totalText.length;

      const paragraphs = Array.from(document.querySelectorAll('p'))
        .map(p => clean(p.innerText || p.textContent || ''))
        .filter(t => t.length >= 30);
      const paragraphCount = paragraphs.length;
      const avgParagraphLength = paragraphCount
        ? paragraphs.reduce((sum, t) => sum + t.length, 0) / paragraphCount
        : 0;

      const tables = Array.from(document.querySelectorAll('table'));
      const tableCount = tables.length;
      const maxTableRows = tables.reduce((max, table) => {
        const rows = table.querySelectorAll('tr').length;
        return Math.max(max, rows);
      }, 0);

      const links = Array.from(document.querySelectorAll('a'));
      const linkCount = links.length;
      const linkTextLength = links
        .map(a => clean(a.innerText || a.textContent || '').length)
        .reduce((sum, len) => sum + len, 0);
      const linkDensity = totalTextLength > 0 ? linkTextLength / totalTextLength : 0;

      const listItems = document.querySelectorAll('li').length;
      const headingCount = document.querySelectorAll('h1,h2,h3,h4').length;
      const paginationDetected = !!document.querySelector('.pagination, .pager, [class*="page"], [aria-label*="page"]');

      const repeatedListBlocks = (() => {
        const containers = Array.from(document.querySelectorAll('ul, ol, .list, .news-list, .article-list'));
        let max = 0;
        containers.forEach((el) => {
          const count = el.querySelectorAll('li, .item, article').length;
          if (count > max) max = count;
        });
        return max;
      })();

      const navLinks = document.querySelectorAll('nav a, aside a, [role="navigation"] a').length;
      const hasTreeStyle = !!document.querySelector('.tree, .directory, [class*="catalog"]');

      return {
        totalTextLength,
        paragraphCount,
        avgParagraphLength,
        tableCount,
        maxTableRows,
        linkCount,
        linkDensity,
        listItems,
        headingCount,
        paginationDetected,
        repeatedListBlocks,
        navLinks,
        hasTreeStyle
      };
    });
  }

  classifyByRules(features) {
    if (features.tableCount >= 1 && features.maxTableRows >= 8 && features.paragraphCount <= 8) {
      return this.buildResult('table_content_page', 0.82, ['table-dominant'], features);
    }

    if (features.paragraphCount >= 5 && features.avgParagraphLength >= 80 && features.linkDensity < 0.3) {
      return this.buildResult('article_page', 0.8, ['long-article-signals'], features);
    }

    if ((features.repeatedListBlocks >= 10 || features.listItems >= 20 || features.paginationDetected) && features.linkDensity >= 0.15) {
      return this.buildResult('list_page', 0.76, ['list-structure-signals'], features);
    }

    if ((features.navLinks >= 15 || features.hasTreeStyle || features.directoryHint) && features.linkDensity >= 0.2) {
      return this.buildResult('directory_page', 0.72, ['directory-navigation-signals'], features);
    }

    if (features.detailHint && features.paragraphCount >= 3) {
      return this.buildResult('article_page', 0.65, ['detail-url-with-content'], features);
    }

    return this.buildResult('generic_page', 0.4, ['fallback-generic'], features);
  }

  buildResult(type, confidence, reasons, features) {
    return {
      type,
      confidence,
      reasons,
      features
    };
  }
}

export default PageClassifier;
