import { jest } from '@jest/globals';
import FinnhubApiParser from '../src/parsers/finnhub-api-parser.js';

describe('FinnhubApiParser', () => {
  let parser;

  beforeEach(() => {
    parser = new FinnhubApiParser();
  });

  describe('matches', () => {
    test('should match finnhub.io/docs/api URLs', () => {
      expect(parser.matches('https://finnhub.io/docs/api')).toBe(true);
      expect(parser.matches('https://finnhub.io/docs/api/stock-candles')).toBe(true);
      expect(parser.matches('http://finnhub.io/docs/api/company-profile')).toBe(true);
    });

    test('should not match other finnhub URLs', () => {
      expect(parser.matches('https://finnhub.io/')).toBe(false);
      expect(parser.matches('https://finnhub.io/register')).toBe(false);
      expect(parser.matches('https://finnhub.io/dashboard')).toBe(false);
    });

    test('should not match other domains', () => {
      expect(parser.matches('https://example.com/docs/api')).toBe(false);
      expect(parser.matches('https://api.finnhub.io/docs/api')).toBe(false);
    });
  });

  describe('getPriority', () => {
    test('should return 100 (high priority)', () => {
      expect(parser.getPriority()).toBe(100);
    });
  });

  describe('generateFilename', () => {
    test('should generate filename from URL path', () => {
      expect(parser.generateFilename('https://finnhub.io/docs/api/stock-candles')).toBe('stock-candles');
      expect(parser.generateFilename('https://finnhub.io/docs/api/company-profile')).toBe('company-profile');
    });

    test('should handle nested paths', () => {
      expect(parser.generateFilename('https://finnhub.io/docs/api/forex/exchange')).toBe('forex_exchange');
    });

    test('should handle root API docs URL', () => {
      expect(parser.generateFilename('https://finnhub.io/docs/api')).toBe('api_overview');
      expect(parser.generateFilename('https://finnhub.io/docs/api/')).toBe('api_overview');
    });

    test('should handle invalid URLs', () => {
      expect(parser.generateFilename('invalid-url')).toBe('api_doc');
    });
  });

  describe('extractApiPath', () => {
    test('should extract API path from URL', () => {
      expect(parser.extractApiPath('https://finnhub.io/docs/api/stock-candles')).toBe('stock-candles');
      expect(parser.extractApiPath('https://finnhub.io/docs/api/forex/exchange')).toBe('forex/exchange');
    });

    test('should return empty string for root API docs URL', () => {
      expect(parser.extractApiPath('https://finnhub.io/docs/api')).toBe('');
      expect(parser.extractApiPath('https://finnhub.io/docs/api/')).toBe('');
    });

    test('should handle invalid URLs', () => {
      expect(parser.extractApiPath('invalid-url')).toBe('');
    });
  });

  describe('waitForContent', () => {
    test('should wait for content to load', async () => {
      const page = {
        waitForLoadState: jest.fn().mockResolvedValue(undefined),
        waitForSelector: jest.fn().mockResolvedValue(undefined),
        waitForTimeout: jest.fn().mockResolvedValue(undefined)
      };

      await parser.waitForContent(page);
      expect(page.waitForLoadState).toHaveBeenCalled();
      expect(page.waitForSelector).toHaveBeenCalled();
      expect(page.waitForTimeout).toHaveBeenCalled();
    });

    test('should handle errors gracefully', async () => {
      const page = {
        waitForLoadState: jest.fn().mockRejectedValue(new Error('Timeout')),
        waitForSelector: jest.fn().mockResolvedValue(undefined),
        waitForTimeout: jest.fn().mockResolvedValue(undefined)
      };

      // Should not throw
      await expect(parser.waitForContent(page)).resolves.not.toThrow();
    });
  });

  describe('parse', () => {
    test('should return finnhub-api type', async () => {
      const mockPage = {
        waitForSelector: jest.fn().mockResolvedValue(undefined),
        waitForTimeout: jest.fn().mockResolvedValue(undefined),
        evaluate: jest.fn().mockResolvedValue({
          title: 'Stock Candles',
          description: 'Get candlestick data',
          endpoint: '/stock/candle',
          method: 'GET',
          parameters: [],
          response: {}
        })
      };

      const result = await parser.parse(mockPage, 'https://finnhub.io/docs/api/stock-candles');

      expect(result.type).toBe('finnhub-api');
      expect(result.url).toBe('https://finnhub.io/docs/api/stock-candles');
    });

    test('should handle errors gracefully', async () => {
      const mockPage = {
        waitForSelector: jest.fn().mockRejectedValue(new Error('Page error')),
        waitForTimeout: jest.fn().mockResolvedValue(undefined),
        evaluate: jest.fn().mockRejectedValue(new Error('Parse error'))
      };

      const result = await parser.parse(mockPage, 'https://finnhub.io/docs/api/stock-candles');

      expect(result.type).toBe('finnhub-api');
      expect(result.url).toBe('https://finnhub.io/docs/api/stock-candles');
    });
  });
});