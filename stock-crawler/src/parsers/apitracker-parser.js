import BaseParser from './base-parser.js';

/**
 * ApiTracker Parser - 解析 apitracker.io 分类页与 API 详情页
 *
 * 目标：
 * 1. 从 /categories/fintech 页面抓取入口链接（/a/{slug}）
 * 2. 从 /a/{slug} 页面提取文档入口与 URL 规则相关字段
 */
class ApiTrackerParser extends BaseParser {
  /**
   * 匹配 apitracker 分类与详情页
   * @param {string} url
   * @returns {boolean}
   */
  matches(url) {
    return /^https?:\/\/apitracker\.io\/(categories\/[^/?#]+|a\/[a-z0-9-]+)\/?(?:[?#].*)?$/i.test(url);
  }

  /**
   * 优先级高于 GenericParser
   * @returns {number}
   */
  getPriority() {
    return 110;
  }

  /**
   * 等待 Next.js 页面就绪
   * @param {Page} page
   */
  async waitForContent(page) {
    try {
      await page.waitForSelector('script#__NEXT_DATA__', { timeout: 15000 });
      await page.waitForLoadState('networkidle', { timeout: 15000 });
    } catch (error) {
      // 允许降级解析
    }
  }

  /**
   * 提取分类页中的 API 详情入口
   * @param {Page} page
   * @returns {Promise<Array>}
   */
  async extractCategoryEntries(page) {
    return await page.evaluate(() => {
      const links = new Map();
      const anchors = Array.from(document.querySelectorAll('a[href^="/a/"]'));

      anchors.forEach((anchor) => {
        const href = anchor.getAttribute('href') || '';
        const slugMatch = href.match(/^\/a\/([a-z0-9-]+)/i);
        if (!slugMatch) return;

        const slug = slugMatch[1].toLowerCase();
        const absUrl = new URL(`/a/${slug}`, window.location.origin).toString();
        const name = (anchor.textContent || '').trim();

        links.set(slug, {
          slug,
          name,
          url: absUrl
        });
      });

      return Array.from(links.values()).sort((a, b) => a.slug.localeCompare(b.slug));
    });
  }

  /**
   * 解析页面
   * @param {Page} page
   * @param {string} url
   * @returns {Promise<Object>}
   */
  async parse(page, url) {
    try {
      await this.waitForContent(page);

      const parsedUrl = new URL(url);
      const isCategoryPage = /^\/categories\//.test(parsedUrl.pathname);

      const data = await page.evaluate(({ targetUrl, categoryMode }) => {
        const normalizeUrlField = (value) => {
          if (typeof value !== 'string') return '';
          const trimmed = value.trim();
          return /^https?:\/\//i.test(trimmed) ? trimmed : '';
        };

        const normalizeText = (value) => {
          if (typeof value !== 'string') return '';
          return value.replace(/\s+/g, ' ').trim();
        };

        const toArray = (value) => {
          if (Array.isArray(value)) return value;
          return [];
        };

        const pushUniqueText = (arr, text) => {
          const normalized = normalizeText(text);
          if (!normalized) return;
          if (!arr.some((item) => item === normalized)) {
            arr.push(normalized);
          }
        };

        const pushUniqueLink = (arr, url, title = '') => {
          const normalizedUrl = normalizeUrlField(url);
          if (!normalizedUrl) return;
          if (!arr.some((item) => item.url === normalizedUrl)) {
            arr.push({
              title: normalizeText(title) || normalizedUrl,
              url: normalizedUrl
            });
          }
        };

        const emptyResult = {
          type: categoryMode ? 'apitracker-category' : 'apitracker-api-detail',
          url: targetUrl,
          title: document.title || '',
          description: '',
          category: '',
          entries: [],
          slug: '',
          companyName: '',
          status: '',
          foundedYear: '',
          lastUpdatedAt: '',
          websiteUrl: '',
          developerPortalUrl: '',
          apiReferenceUrl: '',
          apiExplorerUrl: '',
          statusUrl: '',
          pricingUrl: '',
          changelogUrl: '',
          termsUrl: '',
          privacyUrl: '',
          supportUrl: '',
          contactEmail: '',
          headquarters: '',
          apiBaseEndpoint: '',
          graphqlEndpoint: '',
          categories: [],
          products: [],
          protocols: [],
          authMethods: [],
          languages: [],
          sdks: [],
          apis: [],
          notes: [],
          relatedLinks: [],
          links: [],
          docsEntrances: [],
          apiSpecs: [],
          postmanCollections: [],
          urlRules: {
            include: [
              '^https://apitracker\\\\.io/a/[a-z0-9-]+/?$'
            ],
            exclude: [
              '^https://apitracker\\\\.io/_next/.*',
              '^https://apitracker\\\\.io/(all-apis|compare|specifications|glossary|mcp-servers).*$'
            ]
          },
          rawContent: '',
          rawPageData: {}
        };

        const nextDataNode = document.querySelector('script#__NEXT_DATA__');
        if (!nextDataNode) return emptyResult;

        let nextData = null;
        try {
          nextData = JSON.parse(nextDataNode.textContent || '{}');
        } catch (error) {
          return emptyResult;
        }

        const pageProps = nextData?.props?.pageProps || {};

        if (categoryMode) {
          const categorySlug = window.location.pathname.split('/').filter(Boolean).pop() || '';
          emptyResult.category = categorySlug;

          const links = new Map();
          Array.from(document.querySelectorAll('a[href^="/a/"]')).forEach((a) => {
            const href = a.getAttribute('href') || '';
            const match = href.match(/^\/a\/([a-z0-9-]+)/i);
            if (!match) return;
            const slug = match[1].toLowerCase();
            links.set(slug, {
              slug,
              name: (a.textContent || '').trim(),
              url: new URL(`/a/${slug}`, window.location.origin).toString()
            });
          });

          emptyResult.entries = Array.from(links.values()).sort((a, b) => a.slug.localeCompare(b.slug));
          emptyResult.rawContent = JSON.stringify({
            category: emptyResult.category,
            entryCount: emptyResult.entries.length
          }, null, 2);
          return emptyResult;
        }

        const pageData = pageProps.pageData || {};
        const apiSpecs = Array.isArray(pageProps.apiSpecs) ? pageProps.apiSpecs : [];
        const postmanCollections = Array.isArray(pageProps.postmanCollections) ? pageProps.postmanCollections : [];
        const rawPageData = pageData && typeof pageData === 'object' ? pageData : {};

        const docsEntrances = [];
        const docCandidates = [
          pageData.developerPortalUrl,
          pageData.apiReferenceUrl,
          pageData.apiExplorerUrl
        ].filter(Boolean);

        const pushUnique = (arr, item) => {
          if (!item) return;
          if (!arr.some((x) => x === item)) {
            arr.push(item);
          }
        };

        docCandidates.forEach((candidate) => pushUnique(docsEntrances, candidate));

        const normalizedApiSpecs = apiSpecs.map((spec) => {
          const item = spec && typeof spec === 'object' ? spec : {};
          const specUrl = normalizeUrlField(item.url) || normalizeUrlField(item.downloadUrl);
          return {
            type: typeof item.type === 'string' ? item.type : '',
            format: typeof item.format === 'string' ? item.format : '',
            url: specUrl,
            source: typeof item.source === 'string' ? item.source : ''
          };
        }).filter((spec) => spec.url);

        normalizedApiSpecs.forEach((spec) => pushUnique(docsEntrances, spec.url));

        const normalizedPostman = postmanCollections.map((item) => {
          if (typeof item === 'string') {
            return {
              name: '',
              url: normalizeUrlField(item)
            };
          }

          const candidate = item && typeof item === 'object' ? item : {};
          return {
            name: typeof candidate.name === 'string' ? candidate.name : '',
            url: normalizeUrlField(candidate.url) || normalizeUrlField(candidate.link)
          };
        }).filter((item) => item.url);

        normalizedPostman.forEach((item) => pushUnique(docsEntrances, item.url));
        const relatedLinks = [];
        pushUniqueLink(relatedLinks, pageData.websiteUrl, 'Website');
        pushUniqueLink(relatedLinks, pageData.developerPortalUrl, 'Developer Portal');
        pushUniqueLink(relatedLinks, pageData.apiReferenceUrl, 'API Reference');
        pushUniqueLink(relatedLinks, pageData.apiExplorerUrl, 'API Explorer');
        pushUniqueLink(relatedLinks, pageData.statusUrl, 'Status');
        pushUniqueLink(relatedLinks, pageData.pricingUrl, 'Pricing');
        pushUniqueLink(relatedLinks, pageData.changelogUrl, 'Changelog');
        pushUniqueLink(relatedLinks, pageData.termsUrl, 'Terms');
        pushUniqueLink(relatedLinks, pageData.privacyUrl, 'Privacy');
        pushUniqueLink(relatedLinks, pageData.supportUrl, 'Support');

        normalizedApiSpecs.forEach((spec) => {
          pushUniqueLink(relatedLinks, spec.url, `API Spec ${spec.format || spec.type || ''}`.trim());
          pushUnique(docsEntrances, spec.url);
        });

        normalizedPostman.forEach((item) => {
          pushUniqueLink(relatedLinks, item.url, item.name || 'Postman Collection');
          pushUnique(docsEntrances, item.url);
        });

        const categories = [];
        const products = [];
        const protocols = [];
        const authMethods = [];
        const languages = [];
        const sdks = [];
        const apis = [];
        const notes = [];

        toArray(pageData.categories).forEach((item) => {
          if (typeof item === 'string') return pushUniqueText(categories, item);
          if (item && typeof item === 'object') {
            pushUniqueText(categories, item.name || item.slug || item.title);
          }
        });

        toArray(pageData.products).forEach((item) => {
          if (typeof item === 'string') return pushUniqueText(products, item);
          if (item && typeof item === 'object') {
            pushUniqueText(products, item.name || item.slug || item.title);
          }
        });

        toArray(pageData.protocols).forEach((item) => {
          if (typeof item === 'string') return pushUniqueText(protocols, item);
          if (item && typeof item === 'object') {
            pushUniqueText(protocols, item.name || item.slug || item.title);
          }
        });

        toArray(pageData.authMethods).forEach((item) => {
          if (typeof item === 'string') return pushUniqueText(authMethods, item);
          if (item && typeof item === 'object') {
            pushUniqueText(authMethods, item.name || item.type || item.title);
          }
        });

        toArray(pageData.languages).forEach((item) => {
          if (typeof item === 'string') return pushUniqueText(languages, item);
          if (item && typeof item === 'object') {
            pushUniqueText(languages, item.name || item.slug || item.title);
          }
        });

        toArray(pageData.sdks).forEach((item) => {
          if (typeof item === 'string') {
            pushUniqueText(sdks, item);
            return;
          }
          if (item && typeof item === 'object') {
            const label = normalizeText(item.name || item.language || item.title || item.type);
            if (label) {
              pushUniqueText(sdks, label);
            } else {
              const asText = Object.values(item).find((v) => typeof v === 'string' && normalizeText(v));
              pushUniqueText(sdks, asText);
            }
          }
        });

        toArray(pageData.apis).forEach((item) => {
          if (typeof item === 'string') {
            pushUniqueText(apis, item);
            return;
          }
          if (item && typeof item === 'object') {
            const endpointText = normalizeText(item.baseUrl || item.baseEndpoint || item.url || item.endpoint || item.name);
            pushUniqueText(apis, endpointText);
          }
        });

        if (normalizeText(pageData.description)) {
          notes.push({ type: 'summary', content: normalizeText(pageData.description) });
        }
        if (normalizeText(pageData.pricingModel)) {
          notes.push({ type: 'pricing', content: `Pricing model: ${normalizeText(pageData.pricingModel)}` });
        }
        if (normalizeText(pageData.status)) {
          notes.push({ type: 'status', content: `Status: ${normalizeText(pageData.status)}` });
        }
        if (normalizeText(pageData.contactEmail)) {
          notes.push({ type: 'contact', content: `Contact: ${normalizeText(pageData.contactEmail)}` });
        }

        emptyResult.docsEntrances = docsEntrances.filter((x) => typeof x === 'string' && x.trim());

        emptyResult.slug = pageData.slug || '';
        emptyResult.companyName = pageData.name || '';
        emptyResult.description = normalizeText(pageData.description || pageData.summary || '');
        emptyResult.status = normalizeText(pageData.status || '');
        emptyResult.foundedYear = normalizeText(String(pageData.foundedYear || ''));
        emptyResult.lastUpdatedAt = normalizeText(pageData.updatedAt || pageData.lastUpdatedAt || '');
        emptyResult.websiteUrl = pageData.websiteUrl || '';
        emptyResult.developerPortalUrl = pageData.developerPortalUrl || '';
        emptyResult.apiReferenceUrl = pageData.apiReferenceUrl || '';
        emptyResult.apiExplorerUrl = pageData.apiExplorerUrl || '';
        emptyResult.statusUrl = pageData.statusUrl || '';
        emptyResult.pricingUrl = pageData.pricingUrl || '';
        emptyResult.changelogUrl = pageData.changelogUrl || '';
        emptyResult.termsUrl = pageData.termsUrl || '';
        emptyResult.privacyUrl = pageData.privacyUrl || '';
        emptyResult.supportUrl = pageData.supportUrl || '';
        emptyResult.contactEmail = normalizeText(pageData.contactEmail || '');
        emptyResult.headquarters = normalizeText(pageData.headquarters || pageData.location || '');
        emptyResult.apiBaseEndpoint = pageData.apiBaseEndpoint || '';
        emptyResult.graphqlEndpoint = pageData.graphqlEndpoint || '';
        emptyResult.categories = categories;
        emptyResult.products = products;
        emptyResult.protocols = protocols;
        emptyResult.authMethods = authMethods;
        emptyResult.languages = languages;
        emptyResult.sdks = sdks;
        emptyResult.apis = apis;
        emptyResult.notes = notes;
        emptyResult.relatedLinks = relatedLinks;
        emptyResult.links = relatedLinks;
        emptyResult.apiSpecs = normalizedApiSpecs;
        emptyResult.postmanCollections = normalizedPostman;
        emptyResult.rawPageData = rawPageData;
        emptyResult.rawContent = JSON.stringify({
          description: emptyResult.description,
          slug: emptyResult.slug,
          companyName: emptyResult.companyName,
          status: emptyResult.status,
          categories: emptyResult.categories,
          products: emptyResult.products,
          docsEntrances: emptyResult.docsEntrances,
          relatedLinks: emptyResult.relatedLinks,
          apiBaseEndpoint: emptyResult.apiBaseEndpoint,
          graphqlEndpoint: emptyResult.graphqlEndpoint,
          pageData: rawPageData,
          apiSpecs: normalizedApiSpecs,
          postmanCollections: normalizedPostman
        }, null, 2);

        return emptyResult;
      }, { targetUrl: url, categoryMode: isCategoryPage });

      if (isCategoryPage && (!data.entries || data.entries.length === 0)) {
        data.entries = await this.extractCategoryEntries(page);
      }

      return data;
    } catch (error) {
      return {
        type: 'apitracker-error',
        url,
        title: '',
        error: error.message,
        entries: [],
        docsEntrances: []
      };
    }
  }
}

export default ApiTrackerParser;
