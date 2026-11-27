import BaseParser from './base-parser.js';

const APIFY_CANONICAL_MD_URL = 'https://docs.apify.com/api/v2.md';
const APIFY_OPENAPI_PATTERN = /https?:\/\/docs\.apify\.com\/api\/openapi\.(?:json|yaml)/g;
const APIFY_REFERENCE_ROUTE_PATTERN = /#\/reference\/[A-Za-z0-9\-_/]+/g;

function unique(values = []) {
  return Array.from(new Set((values || []).filter(Boolean)));
}

function extractSection(markdown = '', heading) {
  if (!markdown || !heading) return '';
  const escaped = heading.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const pattern = new RegExp(`(?:^|\\n)#{1,4}\\s+${escaped}\\s*\\n([\\s\\S]*?)(?=\\n#{1,4}\\s+|$)`, 'i');
  const match = markdown.match(pattern);
  return match?.[1]?.trim() || '';
}

function extractCodeExamplesFromMarkdown(markdown = '') {
  const examples = [];
  const codeBlockRegex = /```([a-zA-Z0-9_-]*)\n([\s\S]*?)```/g;
  let match;

  while ((match = codeBlockRegex.exec(markdown)) !== null && examples.length < 10) {
    const language = (match[1] || 'text').trim().toLowerCase() || 'text';
    const code = (match[2] || '').trim();
    if (!code || code.length < 10) continue;
    examples.push({ language, code });
  }

  return examples;
}

function extractMarkdownMetadata(markdown = '') {
  const openapiLinks = unique(markdown.match(APIFY_OPENAPI_PATTERN) || []);
  const referenceRoutes = unique(markdown.match(APIFY_REFERENCE_ROUTE_PATTERN) || []);

  const authenticationSection = extractSection(markdown, 'Authentication') ||
    extractSection(markdown, 'Authorization');

  const rateLimitSection = extractSection(markdown, 'Rate limiting') ||
    extractSection(markdown, 'Rate limits') ||
    extractSection(markdown, 'Limits');

  const noteCandidates = markdown
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter((line) => /^[-*]\s+/.test(line))
    .map((line) => line.replace(/^[-*]\s+/, '').trim())
    .filter((line) => /(token|rate\s*limit|pagination|webhook|dataset)/i.test(line))
    .slice(0, 12);

  const responseStatuses = unique((markdown.match(/\b([1-5][0-9]{2})\b/g) || []))
    .slice(0, 20)
    .map((code) => ({ code, description: '' }));

  const codeExamples = extractCodeExamplesFromMarkdown(markdown);

  return {
    openapiLinks,
    referenceRoutes,
    authentication: authenticationSection,
    rateLimit: rateLimitSection,
    noteCandidates,
    responseStatuses,
    codeExamples
  };
}

export function parseOpenApiDocument(openapi = {}) {
  const servers = Array.isArray(openapi.servers) ? openapi.servers.map(s => s.url).filter(Boolean) : [];
  const baseUrl = servers[0] || 'https://api.apify.com';

  const operations = [];
  const responseStatusesSet = new Set();
  const tagsSet = new Set();

  for (const [path, methods] of Object.entries(openapi.paths || {})) {
    for (const [method, operation] of Object.entries(methods || {})) {
      if (!['get', 'post', 'put', 'delete', 'patch', 'options', 'head'].includes(method)) continue;

      const responses = operation?.responses || {};
      Object.keys(responses).forEach((statusCode) => {
        if (/^[1-5][0-9][0-9]$/.test(statusCode)) {
          responseStatusesSet.add(statusCode);
        }
      });

      const tags = Array.isArray(operation?.tags) ? operation.tags : [];
      tags.forEach((tag) => tagsSet.add(tag));

      operations.push({
        method: method.toUpperCase(),
        path,
        operationId: operation?.operationId || '',
        summary: operation?.summary || '',
        description: operation?.description || '',
        tags
      });
    }
  }

  const securitySchemes = openapi.components?.securitySchemes || {};
  const authSummary = Object.entries(securitySchemes)
    .map(([name, scheme]) => `${name}: ${scheme?.type || 'unknown'}${scheme?.scheme ? ` (${scheme.scheme})` : ''}`)
    .join('\n');

  const responseStatuses = Array.from(responseStatusesSet)
    .sort((a, b) => Number(a) - Number(b))
    .map((code) => ({ code, description: '' }));

  const operationLines = operations
    .slice(0, 400)
    .map(op => `${op.method} ${op.path}${op.summary ? ` - ${op.summary}` : ''}`)
    .join('\n');

  return {
    api: {
      method: 'MULTI',
      endpoint: '/v2/*',
      baseUrl
    },
    servers,
    operationCount: operations.length,
    operations,
    responseStatuses,
    authentication: authSummary,
    tags: Array.from(tagsSet),
    rawContent: JSON.stringify(openapi, null, 2),
    markdownContent: operationLines
  };
}

/**
 * Apify API Parser - 解析 Apify API v2 文档与 OpenAPI 文件
 */
class ApifyApiParser extends BaseParser {
  async fetchCanonicalMarkdown() {
    try {
      const response = await fetch(APIFY_CANONICAL_MD_URL, {
        headers: {
          Accept: 'text/markdown,text/plain;q=0.9,*/*;q=0.8'
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const text = await response.text();
      return text?.trim() || '';
    } catch (error) {
      this.logger?.debug?.(`Apify canonical markdown fetch failed: ${error.message}`);
      return '';
    }
  }

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
    const canonicalMarkdown = await this.fetchCanonicalMarkdown();

    const data = await page.evaluate(async () => {
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

      let canonicalMarkdownFromPage = '';
      try {
        const response = await fetch('https://docs.apify.com/api/v2.md', {
          headers: {
            Accept: 'text/markdown,text/plain;q=0.9,*/*;q=0.8'
          }
        });
        if (response.ok) {
          canonicalMarkdownFromPage = (await response.text())?.trim() || '';
        }
      } catch (_) {
        // ignore and fallback to DOM text
      }

      return {
        title,
        description,
        openapiLinks,
        referenceRoutes,
        rawContent: document.body?.innerText || '',
        canonicalMarkdown: canonicalMarkdownFromPage
      };
    });

    const normalizedRawContent = canonicalMarkdown || data.canonicalMarkdown || data.rawContent;
    const markdownMeta = extractMarkdownMetadata(normalizedRawContent);

    const mergedOpenApiLinks = unique([...data.openapiLinks, ...markdownMeta.openapiLinks]);
    const mergedReferenceRoutes = unique([...data.referenceRoutes, ...markdownMeta.referenceRoutes]);

    const relatedLinks = [
      ...mergedOpenApiLinks.map((item) => ({ title: 'OpenAPI', url: item })),
      ...mergedReferenceRoutes.map((item) => ({ title: item, url: `https://docs.apify.com/api/v2${item}` }))
    ];

    const notes = markdownMeta.noteCandidates.map((content) => ({ type: 'important', content }));

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
      authentication: markdownMeta.authentication,
      rateLimit: markdownMeta.rateLimit,
      responseStatuses: markdownMeta.responseStatuses,
      codeExamples: markdownMeta.codeExamples,
      entryPoints: [
        'https://docs.apify.com/api/v2',
        ...mergedOpenApiLinks
      ],
      referenceRoutes: mergedReferenceRoutes,
      relatedLinks,
      notes,
      urlRules: {
        include: [
          '^https://docs\\.apify\\.com/api/v2(?:\\.md)?(?:[?#].*)?$',
          '^https://docs\\.apify\\.com/api/openapi\\.(json|yaml)(?:[?#].*)?$'
        ],
        exclude: ['\\?(?:.*&)?utm_', '#/?(?!/reference/)']
      },
      markdownContent: normalizedRawContent,
      rawContent: normalizedRawContent
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

    const parsed = parseOpenApiDocument(openapi);

    return {
      type: 'apify-openapi',
      url,
      title: openapi.info?.title || 'Apify API OpenAPI',
      description: openapi.info?.description || '',
      ...parsed,
      version: openapi.info?.version || ''
    };
  }
}

export default ApifyApiParser;
export { extractMarkdownMetadata, extractCodeExamplesFromMarkdown };
