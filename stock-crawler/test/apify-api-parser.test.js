import ApifyApiParser, { extractMarkdownMetadata, parseOpenApiDocument } from '../src/parsers/apify-api-parser.js';
import MarkdownGenerator from '../src/parsers/markdown-generator.js';

describe('ApifyApiParser', () => {
  test('matches apify v2 and openapi urls', () => {
    const parser = new ApifyApiParser();

    expect(parser.matches('https://docs.apify.com/api/v2')).toBe(true);
    expect(parser.matches('https://docs.apify.com/api/v2.md')).toBe(true);
    expect(parser.matches('https://docs.apify.com/api/openapi.json')).toBe(true);
    expect(parser.matches('https://docs.apify.com/api/openapi.yaml')).toBe(true);
    expect(parser.matches('https://docs.apify.com/docs')).toBe(false);
  });

  test('extracts important metadata from canonical markdown', () => {
    const markdown = `# Apify API\n\n## Authentication\nUse token auth.\n\n## Rate limiting\n429 response may happen.\n\n- token required\n- rate limit depends on plan\n\nReference #/reference/actors-collection/get-list-of-actors\n\nhttps://docs.apify.com/api/openapi.json\n`;

    const meta = extractMarkdownMetadata(markdown);

    expect(meta.openapiLinks).toContain('https://docs.apify.com/api/openapi.json');
    expect(meta.referenceRoutes).toContain('#/reference/actors-collection/get-list-of-actors');
    expect(meta.authentication).toContain('token auth');
    expect(meta.rateLimit).toContain('429');
    expect(meta.noteCandidates.length).toBeGreaterThan(0);
    expect(meta.responseStatuses.map((item) => item.code)).toContain('429');
  });

  test('parses openapi document into operations and status codes', () => {
    const openapi = {
      openapi: '3.0.0',
      info: { title: 'Apify API', version: '2.0' },
      servers: [{ url: 'https://api.apify.com' }],
      paths: {
        '/v2/acts': {
          get: {
            summary: 'List actors',
            tags: ['Actors'],
            responses: {
              200: { description: 'ok' },
              401: { description: 'unauthorized' }
            }
          }
        }
      },
      components: {
        securitySchemes: {
          bearerAuth: {
            type: 'http',
            scheme: 'bearer'
          }
        }
      }
    };

    const parsed = parseOpenApiDocument(openapi);

    expect(parsed.operationCount).toBe(1);
    expect(parsed.operations[0]).toMatchObject({ method: 'GET', path: '/v2/acts' });
    expect(parsed.responseStatuses.map((s) => s.code)).toEqual(['200', '401']);
    expect(parsed.authentication).toContain('bearerAuth');
    expect(parsed.api.baseUrl).toBe('https://api.apify.com');
  });

  test('keeps markdown format stable across multiple rounds', () => {
    const markdownGenerator = new MarkdownGenerator();
    const canonicalMarkdown = `# Apify API

## Authentication
Use token auth.

## Rate limiting
429 response may happen.

\`\`\`bash
curl -H "Authorization: Bearer <token>" https://api.apify.com/v2/acts
\`\`\`
`;

    const metadata = extractMarkdownMetadata(canonicalMarkdown);

    for (let round = 1; round <= 3; round += 1) {
      const md = markdownGenerator.generate({
        type: 'apify-api-doc',
        url: 'https://docs.apify.com/api/v2',
        title: 'Apify API',
        description: 'API v2 reference',
        api: { method: 'MULTI', endpoint: '/v2/*', baseUrl: 'https://api.apify.com' },
        authentication: metadata.authentication,
        rateLimit: metadata.rateLimit,
        codeExamples: metadata.codeExamples,
        markdownContent: canonicalMarkdown,
        rawContent: canonicalMarkdown
      });

      expect(md.includes('# Apify API')).toBe(true);
      expect(md.includes('## API 端点')).toBe(true);
      expect(md.includes('## 认证方式')).toBe(true);
      expect(md.includes('## 速率限制')).toBe(true);
      expect(md.includes('## 文档正文')).toBe(true);
      expect(((md.match(/```/g) || []).length % 2)).toBe(0);
    }
  });

});
