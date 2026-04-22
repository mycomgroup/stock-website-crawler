import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import fs from 'node:fs';
import path from 'node:path';

vi.mock('node:fs', () => ({
  default: {
    existsSync: vi.fn(),
    readFileSync: vi.fn(),
    writeFileSync: vi.fn(),
    mkdirSync: vi.fn(),
  },
  existsSync: vi.fn(),
  readFileSync: vi.fn(),
  writeFileSync: vi.fn(),
  mkdirSync: vi.fn(),
}));

vi.mock('node:path', () => ({
  default: {
    dirname: vi.fn((p) => p.split('/').slice(0, -1).join('/')),
    resolve: vi.fn((...args) => args.join('/')),
    join: vi.fn((...args) => args.join('/')),
  },
  dirname: vi.fn((p) => p.split('/').slice(0, -1).join('/')),
  resolve: vi.fn((...args) => args.join('/')),
  join: vi.fn((...args) => args.join('/')),
}));

vi.mock('../paths.js', () => ({
  OUTPUT_ROOT: '/test/output',
  SESSION_FILE: '/test/sessions/guorn.json',
}));

vi.mock('../load-env.js', () => {});

const originalFetch = global.fetch;

describe('guorn-strategy-client.js', () => {
  let client;
  let mockFetch;
  let consoleLogSpy;
  let consoleErrorSpy;

  beforeEach(async () => {
    vi.clearAllMocks();
    mockFetch = vi.fn();
    global.fetch = mockFetch;
    consoleLogSpy = vi.spyOn(console, 'log').mockImplementation(() => {});
    consoleErrorSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
    
    vi.mocked(fs.existsSync).mockReturnValue(true);
    vi.mocked(fs.readFileSync).mockReturnValue(JSON.stringify({
      cookies: [
        { name: '_xsrf', value: 'xsrf_token_123' },
        { name: 'session', value: 'session_value' }
      ]
    }));
    vi.mocked(fs.mkdirSync).mockImplementation(() => {});
    vi.mocked(fs.writeFileSync).mockImplementation(() => {});
    
    vi.resetModules();
    const module = await import('../../request/guorn-strategy-client.js');
    client = new module.GuornStrategyClient();
  });

  afterEach(() => {
    global.fetch = originalFetch;
    consoleLogSpy.mockRestore();
    consoleErrorSpy.mockRestore();
    vi.clearAllMocks();
  });

  describe('FACTOR_IDS', () => {
    it('should export factor IDs constant', async () => {
      const { FACTOR_IDS } = await import('../../request/guorn-strategy-client.js');
      expect(FACTOR_IDS).toBeDefined();
      expect(FACTOR_IDS.ROA).toBe('0.M.股票每日指标_中性ROA.0');
      expect(FACTOR_IDS.ROE).toBe('0.M.股票每日指标_中性ROE.0');
      expect(FACTOR_IDS.PE).toBe('0.M.股票每日指标_市盈率.0');
      expect(FACTOR_IDS.PB).toBe('0.M.股票每日指标_市净率.0');
      expect(FACTOR_IDS.MOMENTUM).toBe('0.M.股票每日指标_动量.0');
    });
  });

  describe('loadJson', () => {
    it('should return empty object for non-existent file', async () => {
      vi.mocked(fs.existsSync).mockReturnValue(false);
      vi.resetModules();
      const { loadJson } = await import('../../request/guorn-strategy-client.js');
      
      const result = loadJson('/nonexistent.json');
      expect(result).toEqual({});
    });

    it('should parse JSON from existing file', async () => {
      vi.mocked(fs.existsSync).mockReturnValue(true);
      vi.mocked(fs.readFileSync).mockReturnValue(JSON.stringify({ key: 'value' }));
      vi.resetModules();
      const { loadJson } = await import('../../request/guorn-strategy-client.js');
      
      const result = loadJson('/test.json');
      expect(result).toEqual({ key: 'value' });
    });

    it('should throw error for invalid JSON', async () => {
      vi.mocked(fs.existsSync).mockReturnValue(true);
      vi.mocked(fs.readFileSync).mockReturnValue('invalid json');
      vi.resetModules();
      const { loadJson } = await import('../../request/guorn-strategy-client.js');
      
      expect(() => loadJson('/test.json')).toThrow();
    });
  });

  describe('GuornStrategyClient constructor', () => {
    it('should initialize with default options', async () => {
      vi.resetModules();
      const { GuornStrategyClient } = await import('../../request/guorn-strategy-client.js');
      const testClient = new GuornStrategyClient();
      
      expect(testClient.sessionFile).toBeDefined();
      expect(testClient.outputRoot).toBeDefined();
      expect(testClient.origin).toBe('https://guorn.com');
      expect(testClient.cookieJar).toBeDefined();
      expect(testClient.timestamp).toBeDefined();
    });

    it('should use custom options', async () => {
      vi.resetModules();
      const { GuornStrategyClient } = await import('../../request/guorn-strategy-client.js');
      const customSessionPayload = { cookies: [{ name: 'test', value: 'test_value' }] };
      const testClient = new GuornStrategyClient({
        sessionFile: '/custom/session.json',
        outputRoot: '/custom/output',
        sessionPayload: customSessionPayload
      });
      
      expect(testClient.sessionFile).toBe('/custom/session.json');
      expect(testClient.outputRoot).toBe('/custom/output');
      expect(testClient.sessionPayload).toEqual(customSessionPayload);
    });

    it('should load session from file if no payload provided', async () => {
      vi.mocked(fs.existsSync).mockReturnValue(true);
      vi.mocked(fs.readFileSync).mockReturnValue(JSON.stringify({
        cookies: [{ name: 'loaded', value: 'loaded_value' }]
      }));
      
      vi.resetModules();
      const { GuornStrategyClient } = await import('../../request/guorn-strategy-client.js');
      const testClient = new GuornStrategyClient({ sessionFile: '/test/session.json' });
      
      expect(testClient.cookieJar).toEqual([{ name: 'loaded', value: 'loaded_value' }]);
    });
  });

  describe('buildHeaders', () => {
    it('should build headers with cookies', async () => {
      vi.mocked(fs.readFileSync).mockReturnValue(JSON.stringify({
        cookies: [
          { name: 'cookie1', value: 'value1' },
          { name: 'cookie2', value: 'value2' }
        ]
      }));
      vi.resetModules();
      const { GuornStrategyClient } = await import('../../request/guorn-strategy-client.js');
      const testClient = new GuornStrategyClient();
      
      const headers = testClient.buildHeaders('https://guorn.com/test');
      
      expect(headers['Cookie']).toBe('cookie1=value1; cookie2=value2');
      expect(headers['User-Agent']).toBeDefined();
      expect(headers['Referer']).toBe('https://guorn.com/test');
      expect(headers['X-Requested-With']).toBe('XMLHttpRequest');
    });

    it('should override headers', async () => {
      const headers = client.buildHeaders('https://guorn.com/test', { 'Custom-Header': 'custom_value' });
      expect(headers['Custom-Header']).toBe('custom_value');
    });

    it('should handle empty cookie jar', async () => {
      vi.mocked(fs.readFileSync).mockReturnValue(JSON.stringify({ cookies: [] }));
      vi.resetModules();
      const { GuornStrategyClient } = await import('../../request/guorn-strategy-client.js');
      const testClient = new GuornStrategyClient();
      
      const headers = testClient.buildHeaders('https://guorn.com/test');
      expect(headers['Cookie']).toBe('');
    });
  });

  describe('buildPostUrl', () => {
    it('should add _xsrf parameter to URL', async () => {
      vi.mocked(fs.readFileSync).mockReturnValue(JSON.stringify({
        cookies: [{ name: '_xsrf', value: 'xsrf_token' }]
      }));
      vi.resetModules();
      const { GuornStrategyClient } = await import('../../request/guorn-strategy-client.js');
      const testClient = new GuornStrategyClient();
      testClient.cookieJar = [{ name: '_xsrf', value: 'xsrf_token' }];
      
      const url = testClient.buildPostUrl('/stock/runtest');
      expect(url).toBe('/stock/runtest?_xsrf=xsrf_token');
    });

    it('should use & separator for URLs with query params', async () => {
      vi.resetModules();
      const { GuornStrategyClient } = await import('../../request/guorn-strategy-client.js');
      const testClient = new GuornStrategyClient();
      testClient.cookieJar = [{ name: '_xsrf', value: 'xsrf_token' }];
      
      const url = testClient.buildPostUrl('/stock/runtest?id=123');
      expect(url).toBe('/stock/runtest?id=123&_xsrf=xsrf_token');
    });

    it('should return original URL if no _xsrf cookie', async () => {
      vi.resetModules();
      const { GuornStrategyClient } = await import('../../request/guorn-strategy-client.js');
      const testClient = new GuornStrategyClient();
      testClient.cookieJar = [{ name: 'other', value: 'value' }];
      
      const url = testClient.buildPostUrl('/stock/runtest');
      expect(url).toBe('/stock/runtest');
    });

    it('should encode xsrf value', async () => {
      vi.resetModules();
      const { GuornStrategyClient } = await import('../../request/guorn-strategy-client.js');
      const testClient = new GuornStrategyClient();
      testClient.cookieJar = [{ name: '_xsrf', value: 'token with spaces' }];
      
      const url = testClient.buildPostUrl('/stock/runtest');
      expect(url).toBe('/stock/runtest?_xsrf=token%20with%20spaces');
    });
  });

  describe('request', () => {
    it('should make GET request', async () => {
      mockFetch.mockResolvedValue({
        ok: true,
        text: async () => JSON.stringify({ status: 'ok' })
      });
      
      const result = await client.request('/user/profile');
      
      expect(mockFetch).toHaveBeenCalledWith(
        'https://guorn.com/user/profile',
        expect.objectContaining({ method: 'GET' })
      );
      expect(result).toEqual({ status: 'ok' });
    });

    it('should make POST request', async () => {
      mockFetch.mockResolvedValue({
        ok: true,
        text: async () => JSON.stringify({ status: 'ok' })
      });
      
      const result = await client.request('/stock/runtest', {
        method: 'POST',
        body: JSON.stringify({ data: 'test' })
      });
      
      expect(mockFetch).toHaveBeenCalledWith(
        'https://guorn.com/stock/runtest',
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify({ data: 'test' })
        })
      );
    });

    it('should handle full URL', async () => {
      mockFetch.mockResolvedValue({
        ok: true,
        text: async () => 'response'
      });
      
      await client.request('https://other.com/api');
      
      expect(mockFetch).toHaveBeenCalledWith('https://other.com/api', expect.any(Object));
    });

    it('should throw error for non-ok response', async () => {
      mockFetch.mockResolvedValue({
        ok: false,
        status: 500,
        text: async () => 'Server Error'
      });
      
      await expect(client.request('/api')).rejects.toThrow('Request failed 500');
    });

    it('should return text for non-JSON response', async () => {
      mockFetch.mockResolvedValue({
        ok: true,
        text: async () => '<html>content</html>'
      });
      
      const result = await client.request('/page');
      expect(result).toBe('<html>content</html>');
    });

    it('should truncate error message to 500 chars', async () => {
      const longText = 'a'.repeat(1000);
      mockFetch.mockResolvedValue({
        ok: false,
        status: 500,
        text: async () => longText
      });
      
      try {
        await client.request('/api');
      } catch (error) {
        expect(error.message).toContain(longText.slice(0, 500));
        expect(error.message.length).toBeLessThan(600);
      }
    });
  });

  describe('getUserProfile', () => {
    it('should fetch user profile', async () => {
      mockFetch.mockResolvedValue({
        ok: true,
        text: async () => JSON.stringify({ status: 'ok', data: { username: 'test' } })
      });
      
      const result = await client.getUserProfile();
      
      expect(result).toEqual({ status: 'ok', data: { username: 'test' } });
      expect(mockFetch).toHaveBeenCalledWith(
        expect.stringContaining('/user/profile'),
        expect.any(Object)
      );
    });
  });

  describe('getStockPoolList', () => {
    it('should fetch stock pool list with default category', async () => {
      mockFetch.mockResolvedValue({
        ok: true,
        text: async () => JSON.stringify({ data: { pool_list: [] } })
      });
      
      await client.getStockPoolList();
      
      expect(mockFetch).toHaveBeenCalledWith(
        expect.stringContaining('/stock/pool/all?category=stock'),
        expect.any(Object)
      );
    });

    it('should fetch stock pool list with custom category', async () => {
      mockFetch.mockResolvedValue({
        ok: true,
        text: async () => JSON.stringify({ data: { pool_list: [] } })
      });
      
      await client.getStockPoolList('fund');
      
      expect(mockFetch).toHaveBeenCalledWith(
        expect.stringContaining('category=fund'),
        expect.any(Object)
      );
    });
  });

  describe('getHotPoolList', () => {
    it('should fetch hot pool list', async () => {
      mockFetch.mockResolvedValue({
        ok: true,
        text: async () => JSON.stringify({ data: { hot_pool_list: [] } })
      });
      
      await client.getHotPoolList();
      
      expect(mockFetch).toHaveBeenCalledWith(
        expect.stringContaining('/stock/hotpool/all'),
        expect.any(Object)
      );
    });
  });

  describe('getStockMeta', () => {
    it('should fetch stock meta', async () => {
      mockFetch.mockResolvedValue({
        ok: true,
        text: async () => JSON.stringify({ data: { measure: {} } })
      });
      
      await client.getStockMeta();
      
      expect(mockFetch).toHaveBeenCalledWith(
        expect.stringContaining('/stock/meta'),
        expect.any(Object)
      );
    });
  });

  describe('getStrategyList', () => {
    it('should parse strategy list from HTML', async () => {
      const html = `<a href="/stock?id=strategy1">Strategy One</a><a href="/stock?id=strategy2">Strategy Two</a><a href="/stock?id=strategy1">Strategy One Duplicate</a>`;
      mockFetch.mockResolvedValue({
        ok: true,
        text: async () => html
      });
      
      const result = await client.getStrategyList();
      
      expect(result).toEqual([
        { id: 'strategy1', name: 'Strategy One' },
        { id: 'strategy2', name: 'Strategy Two' }
      ]);
    });

    it('should filter duplicates', async () => {
      const html = `<a href="/stock?id=dup">First</a><a href="/stock?id=dup">Second</a><a href="/stock?id=dup">Third</a>`;
      mockFetch.mockResolvedValue({
        ok: true,
        text: async () => html
      });
      
      const result = await client.getStrategyList();
      
      expect(result.length).toBe(1);
      expect(result[0].id).toBe('dup');
    });

    it('should trim strategy names', async () => {
      const html = `<a href="/stock?id=test">  Strategy Name  </a>`;
      mockFetch.mockResolvedValue({
        ok: true,
        text: async () => html
      });
      
      const result = await client.getStrategyList();
      expect(result[0].name).toBe('Strategy Name');
    });

    it('should return empty array for no strategies', async () => {
      mockFetch.mockResolvedValue({
        ok: true,
        text: async () => '<html><body>No strategies</body></html>'
      });
      
      const result = await client.getStrategyList();
      expect(result).toEqual([]);
    });
  });

  describe('getStrategy', () => {
    it('should fetch strategy detail', async () => {
      mockFetch.mockResolvedValue({
        ok: true,
        text: async () => '<html>Strategy HTML</html>'
      });
      
      const result = await client.getStrategy('test_id');
      expect(result).toEqual({ id: 'test_id', html: '<html>Strategy HTML</html>' });
    });
  });

  describe('saveStrategy', () => {
    it('should throw error indicating browser automation is required', async () => {
      await expect(client.saveStrategy({})).rejects.toThrow(
        'Strategy save not available via API. Use browser automation instead.'
      );
    });
  });

  describe('buildRunBacktestPayload', () => {
    it('should build backtest payload with all fields', async () => {
      const config = {
        filters: [{ indicator: 'PE', operator: '>', value: 10 }],
        ranks: [{ indicator: 'ROE', weight: 1 }],
        pool: 'test_pool',
        start: '2024-01-01',
        end: '2024-12-31',
        count: 20,
        period: 10,
        trade_cost: 0.003,
        reference: '000905'
      };
      
      const payload = client.buildRunBacktestPayload(config, 'test_uid');
      
      expect(payload.filters).toEqual(config.filters);
      expect(payload.ranks).toEqual(config.ranks);
      expect(payload.pool).toBe('test_pool');
      expect(payload.start).toBe('2024/01/01');
      expect(payload.end).toBe('2024/12/31');
      expect(payload.count).toBe('20');
      expect(payload.period).toBe(10);
      expect(payload.trade_cost).toBe(0.003);
      expect(payload.reference).toBe('000905');
      expect(payload.calc_id).toContain('test_uid.');
    });

    it('should convert dates to slash format', async () => {
      const payload = client.buildRunBacktestPayload({
        start: '2024-01-01',
        end: '2025-12-31'
      }, 'uid');
      
      expect(payload.start).toBe('2024/01/01');
      expect(payload.end).toBe('2025/12/31');
    });

    it('should use startTime and endTime as fallback', async () => {
      const payload = client.buildRunBacktestPayload({
        startTime: '2023-01-01',
        endTime: '2024-01-01'
      }, 'uid');
      
      expect(payload.start).toBe('2023/01/01');
      expect(payload.end).toBe('2024/01/01');
    });

    it('should use defaults for missing fields', async () => {
      const payload = client.buildRunBacktestPayload({}, 'uid');
      
      expect(payload.filters).toEqual([]);
      expect(payload.ranks).toEqual([]);
      expect(payload.pool).toBe('');
      expect(payload.start).toBe('2022/01/01');
      expect(payload.end).toBe('2024/01/01');
      expect(payload.count).toBe('10');
      expect(payload.period).toBe(5);
      expect(payload.trade_cost).toBe(0.002);
      expect(payload.reference).toBe('000300');
    });

    it('should handle exclude_STIB nullish coalescing correctly', async () => {
      const payload1 = client.buildRunBacktestPayload({ exclude_STIB: 0 }, 'uid');
      const payload2 = client.buildRunBacktestPayload({ exclude_STIB: 1 }, 'uid');
      const payload3 = client.buildRunBacktestPayload({}, 'uid');
      
      expect(payload1.exclude_STIB).toBe(0);
      expect(payload2.exclude_STIB).toBe(1);
      expect(payload3.exclude_STIB).toBe(1);
    });

    it('should handle trading_strategy field', async () => {
      const trading_strategy = { buy_options: ['opt1'], sell_options: ['opt2'], hold_options: ['opt3'] };
      const payload = client.buildRunBacktestPayload({ trading_strategy }, 'uid');
      
      expect(payload.trading_strategy).toEqual(trading_strategy);
    });

    it('should include timing configuration', async () => {
      const timing = { indicators: ['ind1'], position: '1', threshold: ['-0.5', '0.5'] };
      const payload = client.buildRunBacktestPayload({ timing }, 'uid');
      
      expect(payload.timing).toEqual(timing);
    });
  });

  describe('getBacktestResult', () => {
    it('should fetch backtest result', async () => {
      mockFetch.mockResolvedValue({
        ok: true,
        text: async () => JSON.stringify({ status: 'ok', data: {} })
      });
      
      await client.getBacktestResult('backtest_id');
      
      expect(mockFetch).toHaveBeenCalledWith(
        expect.stringContaining('/stock/backtest/result?id=backtest_id'),
        expect.any(Object)
      );
    });
  });

  describe('getBacktestHistory', () => {
    it('should fetch backtest history', async () => {
      mockFetch.mockResolvedValue({
        ok: true,
        text: async () => JSON.stringify({ data: [] })
      });
      
      await client.getBacktestHistory('strategy_id');
      
      expect(mockFetch).toHaveBeenCalledWith(
        expect.stringContaining('/stock/backtest/history?id=strategy_id'),
        expect.any(Object)
      );
    });
  });

  describe('getRealtimeSelection', () => {
    it('should make POST request with form data', async () => {
      mockFetch.mockResolvedValue({
        ok: true,
        text: async () => JSON.stringify({ status: 'ok' })
      });
      
      const config = {
        stockPool: { poolId: 'pool123' },
        filters: [{ indicator: 'PE' }],
        rankings: [{ indicator: 'ROE' }]
      };
      
      await client.getRealtimeSelection(config);
      
      expect(mockFetch).toHaveBeenCalledWith(
        'https://guorn.com/stock/realtime',
        expect.objectContaining({
          method: 'POST',
          headers: expect.objectContaining({
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
          })
        })
      );
    });

    it('should handle missing stockPool', async () => {
      mockFetch.mockResolvedValue({
        ok: true,
        text: async () => JSON.stringify({ status: 'ok' })
      });
      
      await client.getRealtimeSelection({});
      expect(mockFetch).toHaveBeenCalled();
    });
  });

  describe('getHistoricalSelection', () => {
    it('should make POST request with date', async () => {
      mockFetch.mockResolvedValue({
        ok: true,
        text: async () => JSON.stringify({ status: 'ok' })
      });
      
      const config = {
        date: '2024-01-01',
        stockPool: { poolId: 'pool123' }
      };
      
      await client.getHistoricalSelection(config);
      
      expect(mockFetch).toHaveBeenCalledWith(
        'https://guorn.com/stock/history',
        expect.objectContaining({ method: 'POST' })
      );
    });
  });

  describe('writeArtifact', () => {
    it('should write JSON artifact', async () => {
      vi.mocked(fs.writeFileSync).mockImplementation(() => {});
      vi.mocked(fs.mkdirSync).mockImplementation(() => {});
      
      const filePath = client.writeArtifact('test', { data: 'value' });
      
      expect(fs.writeFileSync).toHaveBeenCalled();
      expect(fs.mkdirSync).toHaveBeenCalled();
      expect(filePath).toContain('test-');
      expect(filePath).toContain('.json');
    });

    it('should write text artifact', async () => {
      vi.mocked(fs.writeFileSync).mockImplementation(() => {});
      
      const filePath = client.writeArtifact('test', 'text content', 'txt');
      expect(filePath).toContain('.txt');
    });

    it('should use custom extension', async () => {
      vi.mocked(fs.writeFileSync).mockImplementation(() => {});
      
      const filePath = client.writeArtifact('test', 'content', 'log');
      expect(filePath).toContain('.log');
    });

    it('should JSON stringify object data', async () => {
      vi.mocked(fs.writeFileSync).mockImplementation(() => {});
      
      client.writeArtifact('test', { key: 'value' });
      
      const writtenContent = vi.mocked(fs.writeFileSync).mock.calls[0][1];
      expect(JSON.parse(writtenContent)).toEqual({ key: 'value' });
    });
  });
});