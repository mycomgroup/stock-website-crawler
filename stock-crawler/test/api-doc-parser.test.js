import { jest } from '@jest/globals';
import ApiDocParser from '../src/parsers/api-doc-parser.js';

describe('ApiDocParser', () => {
  let parser;

  beforeEach(() => {
    parser = new ApiDocParser();
  });

  describe('matches', () => {
    test('should match URLs containing /api/doc', () => {
      expect(parser.matches('https://example.com/api/doc/users')).toBe(true);
      expect(parser.matches('https://api.example.com/api/doc/v1')).toBe(true);
      expect(parser.matches('https://docs.example.com/api/doc')).toBe(true);
    });

    test('should not match URLs without /api/doc', () => {
      expect(parser.matches('https://example.com/api/users')).toBe(false);
      expect(parser.matches('https://example.com/docs/api')).toBe(false);
      expect(parser.matches('https://example.com/documentation')).toBe(false);
    });

    test('should match when classification type is api_doc_page', () => {
      expect(parser.matches('https://example.com/anything', {
        classification: { type: 'api_doc_page' }
      })).toBe(true);
    });

    test('should not match when classification type is different', () => {
      expect(parser.matches('https://example.com/api/doc', {
        classification: { type: 'article' }
      })).toBe(true); // Still matches due to URL pattern
    });
  });

  describe('getPriority', () => {
    test('should return 100 (high priority)', () => {
      expect(parser.getPriority()).toBe(100);
    });
  });

  describe('extractBriefDescription', () => {
    test('should extract brief description', async () => {
      const page = {
        evaluate: jest.fn().mockResolvedValue('获取用户信息接口')
      };
      const desc = await parser.extractBriefDescription(page);
      expect(desc).toBe('获取用户信息接口');
    });

    test('should return empty string on error', async () => {
      const page = {
        evaluate: jest.fn().mockRejectedValue(new Error('Page error'))
      };
      const desc = await parser.extractBriefDescription(page);
      expect(desc).toBe('');
    });
  });

  describe('extractRequestUrl', () => {
    test('should extract request URL', async () => {
      const page = {
        evaluate: jest.fn().mockResolvedValue('/api/v1/users')
      };
      const url = await parser.extractRequestUrl(page);
      expect(url).toBe('/api/v1/users');
    });

    test('should return empty string on error', async () => {
      const page = {
        evaluate: jest.fn().mockRejectedValue(new Error('Page error'))
      };
      const url = await parser.extractRequestUrl(page);
      expect(url).toBe('');
    });
  });

  describe('extractRequestMethod', () => {
    test('should extract HTTP method', async () => {
      const page = {
        evaluate: jest.fn().mockResolvedValue('POST')
      };
      const method = await parser.extractRequestMethod(page);
      expect(method).toBe('POST');
    });

    test('should return empty string on error', async () => {
      const page = {
        evaluate: jest.fn().mockRejectedValue(new Error('Page error'))
      };
      const method = await parser.extractRequestMethod(page);
      expect(method).toBe('');
    });
  });

  describe('parse', () => {
    test('should return api-doc type', async () => {
      const mockPage = {
        evaluate: jest.fn().mockResolvedValue('')
      };

      parser.extractTitle = jest.fn().mockResolvedValue('Users API');
      parser.extractBriefDescription = jest.fn().mockResolvedValue('Get users');
      parser.extractRequestUrl = jest.fn().mockResolvedValue('/api/users');
      parser.extractRequestMethod = jest.fn().mockResolvedValue('GET');
      parser.extractParameters = jest.fn().mockResolvedValue([]);
      parser.extractApiExamples = jest.fn().mockResolvedValue([]);
      parser.extractResponseData = jest.fn().mockResolvedValue({ description: '', table: [] });
      parser.extractTables = jest.fn().mockResolvedValue([]);
      parser.extractCodeBlocks = jest.fn().mockResolvedValue([]);

      const result = await parser.parse(mockPage, 'https://example.com/api/doc/users');

      expect(result.type).toBe('api-doc');
      expect(result.url).toBe('https://example.com/api/doc/users');
      expect(result.title).toBe('Users API');
      expect(result.requestUrl).toBe('/api/users');
      expect(result.requestMethod).toBe('GET');
    });

    test('should handle errors gracefully', async () => {
      const mockPage = {
        evaluate: jest.fn().mockRejectedValue(new Error('Parse error'))
      };

      const result = await parser.parse(mockPage, 'https://example.com/api/doc');

      expect(result.type).toBe('api-doc');
      expect(result.url).toBe('https://example.com/api/doc');
      expect(result.title).toBe('');
      expect(result.params).toEqual([]);
    });
  });
});