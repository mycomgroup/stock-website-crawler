import BaseParser from './base-parser.js';

/**
 * Apify API Parser - 解析 Apify API v2 文档与 OpenAPI 文件
 */
class ApifyApiParser extends BaseParser {
  /**
   * 匹配 Apify API 文档相关 URL
   * @param {string} url - 页面URL
   * @returns {boolean} 是否匹配
   */
  matches(url) {
    return /^https?:\/\/docs\.apify\.com\/api\/(v2(?:\.md)?|openapi\.(json|yaml))(?:[?#].*)?$/.test(url);
  }

  /**
   * 获取优先级
   * @returns {number} 优先级
   */
  getPriority() {
    return 110;
  }

  /**
   * 解析 Apify API 页面
   * @param {Page} page - Playwright 页面对象
   * @param {string} url - 页面URL
   * @returns {Promise<Object>} 解析结果
   */
  async parse(page, url) {
    if (/openapi\.json(?:[?#].*)?$/.test(url)) {
      return await this.parseOpenApiJson(page, url);
    }

    return await this.parseApiDoc(page, url);
  }

  async parseApiDoc(page, url) {
    const data = await page.evaluate(() => {
      const title = document.querySelector('h1')?.textContent?.trim() || document.title || 'Apify API';
      const description = document.querySelector('meta[name="description"]')?.getAttribute('content') || '';

      const allLinks = Array.from(document.querySelectorAll('a[href]')).map(a => ({
        href: a.getAttribute('href') || '',
        text: (a.textContent || '').trim()
      }));

      const openapiLinks = allLinks
        .filter(link => /openapi\.(json|yaml)/.test(link.href))
        .map(link => link.href.startsWith('http') ? link.href : new URL(link.href, location.origin).href);

      const referenceRoutes = Array.from(new Set(
        allLinks
          .map(link => link.href)
          .filter(href => href.startsWith('#/reference/'))
      ));

      return {
        title,
        description,
        openapiLinks,
        referenceRoutes,
        rawContent: document.body?.innerText || ''
      };
    });

    return {
      type: 'apify-api-doc',
      url,
      title: data.title,
      description: data.description,
      api: {
        method: 'MULTI',
        endpoint: '/v2/*',
        baseUrl: 'https://api.apify.com'
      },
      entryPoints: [
        'https://docs.apify.com/api/v2',
        ...data.openapiLinks
      ],
      referenceRoutes: data.referenceRoutes,
      urlRules: {
        include: [
          '^https://docs\\.apify\\.com/api/v2(?:\\.md)?(?:[?#].*)?$',
          '^https://docs\\.apify\\.com/api/openapi\\.(json|yaml)(?:[?#].*)?$'
        ],
        exclude: ['\\?(?:.*&)?utm_', '#/?(?!/reference/)']
      },
      rawContent: data.rawContent
    };
  }

  async parseOpenApiJson(page, url) {
    const textContent = await page.evaluate(() => {
      const pre = document.querySelector('pre');
      if (pre?.textContent) return pre.textContent;
      return document.body?.innerText || '';
    });

    let openapi;
    try {
      openapi = JSON.parse(textContent);
    } catch (error) {
      return {
        type: 'apify-openapi',
        url,
        title: 'Apify OpenAPI (JSON parse failed)',
        description: `Failed to parse OpenAPI JSON: ${error.message}`,
        api: {
          method: 'MULTI',
          endpoint: '/v2/*',
          baseUrl: 'https://api.apify.com'
        },
        rawContent: textContent
      };
    }

    const servers = Array.isArray(openapi.servers) ? openapi.servers.map(s => s.url).filter(Boolean) : [];
    const baseUrl = servers[0] || 'https://api.apify.com';

    const operations = [];
    for (const [path, methods] of Object.entries(openapi.paths || {})) {
      for (const [method, operation] of Object.entries(methods || {})) {
        if (!['get', 'post', 'put', 'delete', 'patch', 'options', 'head'].includes(method)) continue;
        operations.push({
          method: method.toUpperCase(),
          path,
          operationId: operation?.operationId || '',
          summary: operation?.summary || '',
          tags: Array.isArray(operation?.tags) ? operation.tags : []
        });
      }
    }

    const operationsPreview = operations
      .slice(0, 300)
      .map(op => `${op.method} ${op.path}${op.summary ? ` - ${op.summary}` : ''}`)
      .join('\n');

    return {
      type: 'apify-openapi',
      url,
      title: openapi.info?.title || 'Apify API OpenAPI',
      description: openapi.info?.description || '',
      api: {
        method: 'MULTI',
        endpoint: '/v2/*',
        baseUrl
      },
      version: openapi.info?.version || '',
      servers,
      operationCount: operations.length,
      operations,
      rawContent: operationsPreview
    };
  }
}

export default ApifyApiParser;
