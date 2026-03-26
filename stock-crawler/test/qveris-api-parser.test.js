import { describe, expect, test, beforeEach } from '@jest/globals';
import QverisApiParser from '../src/parsers/qveris-api-parser.js';

describe('QverisApiParser', () => {
  let parser;

  beforeEach(() => {
    parser = new QverisApiParser();
  });

  test('extractEndpointsFromText should keep key endpoint paths', () => {
    const text = `
      POST /search
      POST /tools/execute?tool_id={tool_id}
      POST /tools/by-ids
    `;
    const endpoints = parser.extractEndpointsFromText(text);

    expect(endpoints).toContain('/search');
    expect(endpoints).toContain('/tools/execute?tool_id={tool_id}');
    expect(endpoints).toContain('/tools/by-ids');
  });

  test('normalizeCodeExamples should infer language and deduplicate', () => {
    const codeExamples = parser.normalizeCodeExamples([
      { className: 'language-bash', code: 'curl -X POST https://qveris.ai/api/v1/search -d "{\\"query\\": \\"weather\\"}"' },
      { className: 'language-bash', code: 'curl -X POST https://qveris.ai/api/v1/search -d "{\\"query\\": \\"weather\\"}"' },
      { className: 'language-json', code: '{\n  "query": "weather",\n  "limit": 5\n}' }
    ]);

    expect(codeExamples.length).toBe(2);
    expect(codeExamples.find((item) => item.language === 'bash')).toBeTruthy();
    expect(codeExamples.find((item) => item.language === 'json')).toBeTruthy();
  });

  test('mergeRenderedAndChunkData should retain important fields', () => {
    const renderedData = {
      title: 'QVeris API Docs',
      description: 'rendered',
      endpoints: ['/search'],
      codeExamples: [{ language: 'bash', code: 'curl -X POST /search' }],
      parameters: [{ name: 'query' }],
      apiInfo: {
        baseUrl: 'https://qveris.ai/api/v1',
        authMethod: 'Bearer Token',
        endpoints: [{ method: 'POST', path: '/search', params: ['query', 'limit'] }]
      },
      baseUrl: 'https://qveris.ai/api/v1',
      authMethod: 'Bearer Token',
      authentication: 'Bearer Token',
      markdownContent: '## 目录\n- Quick start',
      source: 'rendered-page'
    };

    const jsChunkData = {
      title: 'QVeris API Documentation',
      description: 'chunk',
      endpoints: ['/tools/execute', '/tools/by-ids'],
      codeExamples: [{ language: 'json', code: '{ "tool_id": "abc" }' }],
      apiInfo: {
        baseUrl: 'https://qveris.ai/api/v1',
        authMethod: 'Bearer Token',
        endpoints: [{ method: 'POST', path: '/tools/execute', params: ['tool_id'] }]
      },
      source: 'js-chunk'
    };

    const merged = parser.mergeRenderedAndChunkData(renderedData, jsChunkData, 'https://qveris.ai/docs');
    expect(merged).toBeTruthy();
    expect(merged.baseUrl).toBe('https://qveris.ai/api/v1');
    expect(merged.authMethod).toBe('Bearer Token');
    expect(merged.endpoints).toEqual(expect.arrayContaining(['/search', '/tools/execute', '/tools/by-ids']));
    expect(merged.parameters).toEqual(expect.arrayContaining([
      expect.objectContaining({ name: 'query' }),
      expect.objectContaining({ name: 'tool_id' })
    ]));
  });
});
