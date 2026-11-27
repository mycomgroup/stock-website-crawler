import ApifyApiParser, { extractMarkdownMetadata, parseOpenApiDocument } from '../src/parsers/apify-api-parser.js';
import MarkdownGenerator from '../src/parsers/markdown-generator.js';

describe('ApifyApiParser', () => {
  let parser;

  beforeEach(() => {
    parser = new ApifyApiParser();
  });

  describe('matches', () => {
    test('should match docs.apify.com/api/v2 URLs', () => {
      expect(parser.matches('https://docs.apify.com/api/v2')).toBe(true);
      expect(parser.matches('https://docs.apify.com/api/v2.md')).toBe(true);
      expect(parser.matches('https://docs.apify.com/api/v2?query=test')).toBe(true);
    });

    test('should match openapi URLs', () => {
      expect(parser.matches('https://docs.apify.com/api/openapi.json')).toBe(true);
      expect(parser.matches('https://docs.apify.com/api/openapi.yaml')).toBe(true);
    });

    test('should not match other URLs', () => {
      expect(parser.matches('https://docs.apify.com/actors')).toBe(false);
      expect(parser.matches('https://apify.com')).toBe(false);
      expect(parser.matches('https://api.apify.com/v2')).toBe(false);
    });
  });

  describe('getPriority', () => {
    test('should return 110', () => {
      expect(parser.getPriority()).toBe(110);
    });
  });

  describe('parse', () => {
    test('should route to parseApiDoc for v2 URLs', async () => {
      const mockPage = {
        evaluate: async () => ({
          title: 'Apify API',
          description: 'API documentation',
          openapiLinks: ['https://docs.apify.com/api/openapi.json'],
          referenceRoutes: ['#/reference/actors'],
          rawContent: 'raw content',
          canonicalMarkdown: ''
        })
      };

      parser.fetchCanonicalMarkdown = async () => '';

      const result = await parser.parse(mockPage, 'https://docs.apify.com/api/v2');

      expect(result.type).toBe('apify-api-doc');
      expect(result.api.method).toBe('MULTI');
      expect(result.api.baseUrl).toBe('https://api.apify.com');
    });

    test('should route to parseOpenApiJson for openapi URLs', async () => {
      const mockPage = {
        evaluate: async () => '{"info":{"title":"Apify API"},"paths":{"/v2/acts":{"get":{"summary":"Get acts"}}},"servers":[{"url":"https://api.apify.com"}]}'
      };

      const result = await parser.parse(mockPage, 'https://docs.apify.com/api/openapi.json');

      expect(result.type).toBe('apify-openapi');
      expect(result.title).toBe('Apify API');
    });

    test('should handle JSON parse errors', async () => {
      const mockPage = {
        evaluate: async () => 'invalid json'
      };

      const result = await parser.parse(mockPage, 'https://docs.apify.com/api/openapi.json');

      expect(result.type).toBe('apify-openapi');
      expect(result.description).toContain('Failed to parse');
    });
  });

  describe('parseOpenApiJson', () => {
    test('should parse OpenAPI specification', async () => {
      const mockPage = {
        evaluate: async () => JSON.stringify({
          info: { title: 'Apify API v2', version: '1.0.0', description: 'The API' },
          servers: [{ url: 'https://api.apify.com' }],
          paths: {
            '/v2/acts': {
              get: { operationId: 'getActs', summary: 'List all acts', tags: ['Acts'] },
              post: { operationId: 'createAct', summary: 'Create act' }
            }
          }
        })
      };

      const result = await parser.parseOpenApiJson(mockPage, 'https://docs.apify.com/api/openapi.json');

      expect(result.type).toBe('apify-openapi');
      expect(result.title).toBe('Apify API v2');
      expect(result.version).toBe('1.0.0');
      expect(result.servers).toContain('https://api.apify.com');
      expect(result.operations).toHaveLength(2);
      expect(result.operationCount).toBe(2);
    });

    test('should filter valid HTTP methods', async () => {
      const mockPage = {
        evaluate: async () => JSON.stringify({
          info: { title: 'Test' },
          paths: {
            '/test': {
              get: { summary: 'GET' },
              post: { summary: 'POST' },
              options: { summary: 'OPTIONS' },
              xCustom: { summary: 'Custom' }
            }
          }
        })
      };

      const result = await parser.parseOpenApiJson(mockPage, 'https://docs.apify.com/api/openapi.json');

      expect(result.operations).toHaveLength(3);
    });
  });

  describe('parseApiDoc', () => {
    test('should merge DOM and markdown content', async () => {
      const mockPage = {
        evaluate: async () => ({
          title: 'Apify API v2',
          description: 'Documentation',
          openapiLinks: [],
          referenceRoutes: ['#/reference/runs'],
          rawContent: 'DOM content',
          canonicalMarkdown: ''
        })
      };

      parser.fetchCanonicalMarkdown = async () => '# Apify API\n\nMarkdown content\n\n#/reference/actors';

      const result = await parser.parseApiDoc(mockPage, 'https://docs.apify.com/api/v2');

      expect(result.entryPoints).toContain('https://docs.apify.com/api/v2');
      expect(result.referenceRoutes).toContain('#/reference/runs');
      expect(result.referenceRoutes).toContain('#/reference/actors');
    });
  });

  describe('extractMarkdownMetadata & parseOpenApiDocument', () => {
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
});