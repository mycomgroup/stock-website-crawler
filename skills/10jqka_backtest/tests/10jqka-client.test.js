import { jest, describe, test, expect, beforeEach, afterEach } from '@jest/globals';
import fs from 'node:fs';
import path from 'node:path';
import { JqkaBacktestClient, loadJson } from '../request/10jqka-client.js';

describe('JqkaBacktestClient', () => {
  const testSessionFile = './tests/fixtures/test-session.json';
  const testOutputDir = './tests/fixtures/test-output';

  beforeEach(() => {
    if (!fs.existsSync('./tests/fixtures')) {
      fs.mkdirSync('./tests/fixtures', { recursive: true });
    }
  });

  afterEach(() => {
    if (fs.existsSync(testSessionFile)) {
      fs.unlinkSync(testSessionFile);
    }
    if (fs.existsSync(testOutputDir)) {
      fs.rmSync(testOutputDir, { recursive: true, force: true });
    }
  });

  describe('constructor', () => {
    test('should create instance with default options', () => {
      const client = new JqkaBacktestClient({ cookies: [] });
      expect(client.origin).toBe('https://backtest.10jqka.com.cn');
      expect(client.cookieJar).toEqual([]);
    });

    test('should create instance with custom cookies', () => {
      const cookies = [
        { name: 'v', value: 'test123' },
        { name: 'SID', value: 'sid456' }
      ];
      const client = new JqkaBacktestClient({ cookies });
      expect(client.cookieJar).toEqual(cookies);
    });

    test('should create instance with custom session file', () => {
      fs.writeFileSync(testSessionFile, JSON.stringify({
        cookies: [{ name: 'test', value: 'value' }]
      }));
      
      const client = new JqkaBacktestClient({ sessionFile: testSessionFile });
      expect(client.cookieJar).toHaveLength(1);
    });

    test('should create instance with custom output root', () => {
      const client = new JqkaBacktestClient({ outputRoot: '/custom/output' });
      expect(client.outputRoot).toBe('/custom/output');
    });

    test('should create instance with session payload', () => {
      const sessionPayload = {
        cookies: [{ name: 'custom', value: 'payload' }]
      };
      const client = new JqkaBacktestClient({ sessionPayload });
      expect(client.cookieJar).toEqual(sessionPayload.cookies);
    });

    test('should prioritize cookies over session file', () => {
      fs.writeFileSync(testSessionFile, JSON.stringify({
        cookies: [{ name: 'file', value: 'cookie' }]
      }));
      
      const cookies = [{ name: 'direct', value: 'cookie' }];
      const client = new JqkaBacktestClient({
        cookies,
        sessionFile: testSessionFile
      });
      
      expect(client.cookieJar).toEqual(cookies);
    });
  });

  describe('getCookieHeader', () => {
    test('should format single cookie', () => {
      const client = new JqkaBacktestClient({
        cookies: [{ name: 'v', value: 'test123' }]
      });
      
      expect(client.getCookieHeader()).toBe('v=test123');
    });

    test('should format multiple cookies', () => {
      const client = new JqkaBacktestClient({
        cookies: [
          { name: 'v', value: 'test123' },
          { name: 'SID', value: 'sid456' }
        ]
      });
      
      expect(client.getCookieHeader()).toBe('v=test123; SID=sid456');
    });

    test('should handle empty cookie jar', () => {
      const client = new JqkaBacktestClient({ cookies: [] });
      expect(client.getCookieHeader()).toBe('');
    });

    test('should handle cookies with special characters', () => {
      const client = new JqkaBacktestClient({
        cookies: [
          { name: 'token', value: 'abc%3D%3D' },
          { name: 'session', value: 'xyz/123' }
        ]
      });
      
      expect(client.getCookieHeader()).toBe('token=abc%3D%3D; session=xyz/123');
    });
  });

  describe('buildHeaders', () => {
    test('should build headers with default referer', () => {
      const client = new JqkaBacktestClient({
        cookies: [{ name: 'v', value: 'test' }]
      });
      
      const headers = client.buildHeaders();
      
      expect(headers['Content-Type']).toBe('application/json');
      expect(headers['User-Agent']).toContain('Mozilla');
      expect(headers['Accept']).toBe('application/json, text/plain, */*');
      expect(headers['Accept-Language']).toBe('zh-CN,zh;q=0.9');
      expect(headers['Origin']).toBe('https://backtest.10jqka.com.cn');
      expect(headers['Referer']).toBe('https://backtest.10jqka.com.cn/backtest/app.html');
      expect(headers['Cookie']).toBe('v=test');
    });

    test('should build headers with custom referer', () => {
      const client = new JqkaBacktestClient();
      const customReferer = 'https://backtest.10jqka.com.cn/custom';
      
      const headers = client.buildHeaders(customReferer);
      
      expect(headers['Referer']).toBe(customReferer);
    });

    test('should build headers with empty cookies', () => {
      const client = new JqkaBacktestClient({ cookies: [] });
      const headers = client.buildHeaders();
      
      expect(headers['Cookie']).toBe('');
    });

    test('should include required headers', () => {
      const client = new JqkaBacktestClient();
      const headers = client.buildHeaders();
      
      expect(headers).toHaveProperty('Content-Type');
      expect(headers).toHaveProperty('User-Agent');
      expect(headers).toHaveProperty('Accept');
      expect(headers).toHaveProperty('Accept-Language');
      expect(headers).toHaveProperty('Origin');
      expect(headers).toHaveProperty('Referer');
      expect(headers).toHaveProperty('Cookie');
    });
  });

  describe('request', () => {
    test('should build full URL from endpoint', () => {
      const client = new JqkaBacktestClient();
      
      const url = client.origin + '/api/test';
      expect(url).toBe('https://backtest.10jqka.com.cn/api/test');
    });

    test('should use full URL if provided', () => {
      const client = new JqkaBacktestClient();
      expect(client.origin).toBe('https://backtest.10jqka.com.cn');
    });
  });

  describe('runBacktest', () => {
    test('should merge config with defaults', async () => {
      const client = new JqkaBacktestClient();
      
      const mockFetch = jest.fn(() => Promise.resolve({
        ok: true,
        text: () => Promise.resolve(JSON.stringify({ errorcode: 0 }))
      }));
      global.fetch = mockFetch;
      
      await client.runBacktest({ query: 'custom query' });
      
      const requestBody = JSON.parse(mockFetch.mock.calls[0][1].body);
      expect(requestBody.query).toBe('custom query');
      expect(requestBody.capital).toBe('10000000');
      expect(requestBody.engine).toBe('undefined');
      expect(requestBody.period).toBe('2,3');
      
      mockFetch.mockRestore();
    });

    test('should throw error for -401 errorcode', async () => {
      const client = new JqkaBacktestClient();
      
      const mockFetch = jest.fn(() => Promise.resolve({
        ok: true,
        text: () => Promise.resolve(JSON.stringify({ errorcode: -401 }))
      }));
      global.fetch = mockFetch;
      
      await expect(client.runBacktest({}))
        .rejects.toThrow('未授权');
      
      mockFetch.mockRestore();
    });

    test('should return success for valid response', async () => {
      const client = new JqkaBacktestClient();
      
      const mockFetch = jest.fn(() => Promise.resolve({
        ok: true,
        text: () => Promise.resolve(JSON.stringify({ errorcode: 0, task_id: 'test123' }))
      }));
      global.fetch = mockFetch;
      
      const result = await client.runBacktest({});
      
      expect(result.success).toBe(true);
      expect(result.data.errorcode).toBe(0);
      
      mockFetch.mockRestore();
    });

    test('should use all provided config values', async () => {
      const client = new JqkaBacktestClient();
      
      const mockFetch = jest.fn(() => Promise.resolve({
        ok: true,
        text: () => Promise.resolve(JSON.stringify({ errorcode: 0 }))
      }));
      global.fetch = mockFetch;
      
      const config = {
        query: '涨停板',
        period: '5,10',
        start_date: '2024-01-01',
        end_date: '2024-12-31',
        stock_hold: '5',
        upper_income: '30',
        lower_income: '15',
        fall_income: '8',
        day_buy_stock_num: '3',
        capital: '5000000',
        engine: 'undefined'
      };
      
      await client.runBacktest(config);
      
      const requestBody = JSON.parse(mockFetch.mock.calls[0][1].body);
      expect(requestBody).toEqual(config);
      
      mockFetch.mockRestore();
    });
  });

  describe('writeArtifact', () => {
    test('should write JSON artifact', () => {
      const client = new JqkaBacktestClient({ outputRoot: testOutputDir });
      const data = { test: 'data', value: 123 };
      
      const filePath = client.writeArtifact('test', data);
      
      expect(filePath).toMatch(/test-\d+\.json$/);
      expect(fs.existsSync(filePath)).toBe(true);
      
      const saved = JSON.parse(fs.readFileSync(filePath, 'utf8'));
      expect(saved).toEqual(data);
    });

    test('should write string artifact', () => {
      const client = new JqkaBacktestClient({ outputRoot: testOutputDir });
      const data = 'plain text data';
      
      const filePath = client.writeArtifact('test', data);
      
      expect(filePath).toMatch(/test-\d+\.json$/);
      expect(fs.existsSync(filePath)).toBe(true);
      
      const saved = fs.readFileSync(filePath, 'utf8');
      expect(saved).toBe('plain text data');
    });

    test('should write artifact with custom extension', () => {
      const client = new JqkaBacktestClient({ outputRoot: testOutputDir });
      const data = 'text content';
      
      const filePath = client.writeArtifact('test', data, 'txt');
      
      expect(filePath).toMatch(/test-\d+\.txt$/);
      expect(fs.existsSync(filePath)).toBe(true);
    });

    test('should create output directory if not exists', () => {
      const newDir = './tests/fixtures/new-output';
      if (fs.existsSync(newDir)) {
        fs.rmSync(newDir, { recursive: true, force: true });
      }
      
      const client = new JqkaBacktestClient({ outputRoot: newDir });
      const filePath = client.writeArtifact('test', { data: 'test' });
      
      expect(fs.existsSync(newDir)).toBe(true);
      expect(fs.existsSync(filePath)).toBe(true);
      
      fs.rmSync(newDir, { recursive: true, force: true });
    });

    test('should include timestamp in filename', () => {
      const client = new JqkaBacktestClient({ outputRoot: testOutputDir });
      const before = Date.now();
      
      const filePath = client.writeArtifact('test', { data: 'test' });
      const after = Date.now();
      
      const match = filePath.match(/test-(\d+)\.json$/);
      if (match) {
        const timestamp = parseInt(match[1]);
        expect(timestamp).toBeGreaterThanOrEqual(before);
        expect(timestamp).toBeLessThanOrEqual(after);
      }
    });
  });
});

describe('loadJson', () => {
  const testFile = './tests/fixtures/test-load.json';

  afterEach(() => {
    if (fs.existsSync(testFile)) {
      fs.unlinkSync(testFile);
    }
  });

  test('should load JSON file successfully', () => {
    const data = { test: 'value', number: 123 };
    fs.writeFileSync(testFile, JSON.stringify(data));
    
    const result = loadJson(testFile);
    expect(result).toEqual(data);
  });

  test('should return empty object for non-existent file', () => {
    const result = loadJson('./tests/fixtures/non-existent.json');
    expect(result).toEqual({});
  });

  test('should return empty object for invalid JSON', () => {
    fs.writeFileSync(testFile, 'invalid json {');
    
    const result = loadJson(testFile);
    expect(result).toEqual({});
  });

  test('should return empty object for empty file', () => {
    fs.writeFileSync(testFile, '');
    
    const result = loadJson(testFile);
    expect(result).toEqual({});
  });

  test('should load complex JSON object', () => {
    const data = {
      nested: {
        array: [1, 2, 3],
        object: { a: 'b' }
      },
      string: 'test',
      null: null,
      boolean: true
    };
    fs.writeFileSync(testFile, JSON.stringify(data));
    
    const result = loadJson(testFile);
    expect(result).toEqual(data);
  });
});