import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import fs from 'node:fs';
import path from 'node:path';

vi.mock('node:fs');
vi.mock('../load-env.js', () => {});
vi.mock('../paths.js', () => ({
  OUTPUT_ROOT: '/tmp/thsquant-test-output',
  SESSION_FILE: '/tmp/thsquant-test-session.json'
}));

const mockFetch = vi.spyOn(global, 'fetch', 'get');

const mockSession = {
  cookies: [
    { name: 'ths_session', value: 'test-session-token', domain: 'quant.10jqka.com.cn' },
    { name: 'user_id', value: '12345', domain: 'quant.10jqka.com.cn' }
  ],
  timestamp: Date.now()
};

let THSQuantAPIClient;

beforeAll(async () => {
  ({ THSQuantAPIClient } = await import('../browser/thsquant-api.js'));
});

beforeEach(() => {
  vi.clearAllMocks();
  fs.existsSync.mockReturnValue(true);
  fs.readFileSync.mockReturnValue(JSON.stringify(mockSession));
  fs.mkdirSync.mockReturnValue();
  fs.writeFileSync.mockReturnValue();
});

afterEach(() => {
  mockFetch.mockReset();
});

describe('THSQuantAPIClient', () => {
  let client;

  beforeEach(() => {
    client = new THSQuantAPIClient();
  });

  describe('constructor', () => {
    it('initializes with default options', () => {
      expect(client.baseUrl).toBe('https://quant.10jqka.com.cn');
      expect(client.sessionFile).toBe('/tmp/thsquant-test-session.json');
      expect(client.outputRoot).toBe('/tmp/thsquant-test-output');
    });

    it('initializes with custom options', () => {
      const customClient = new THSQuantAPIClient({
        sessionFile: '/custom/session.json',
        outputRoot: '/custom/output'
      });
      expect(customClient.sessionFile).toBe('/custom/session.json');
      expect(customClient.outputRoot).toBe('/custom/output');
    });

    it('loads session from file on construction', () => {
      expect(fs.existsSync).toHaveBeenCalledWith('/tmp/thsquant-test-session.json');
      expect(fs.readFileSync).toHaveBeenCalledWith('/tmp/thsquant-test-session.json', 'utf8');
      expect(client.cookies).toEqual(mockSession.cookies);
      expect(client.cookieHeader).toBe('ths_session=test-session-token; user_id=12345');
    });

    it('handles missing session file gracefully', () => {
      fs.existsSync.mockReturnValue(false);
      const newClient = new THSQuantAPIClient();
      expect(newClient.cookies).toEqual([]);
      expect(newClient.cookieHeader).toBe('');
    });

    it('handles malformed session JSON', () => {
      fs.existsSync.mockReturnValue(true);
      fs.readFileSync.mockReturnValue('invalid json');
      const newClient = new THSQuantAPIClient();
      expect(newClient.cookies).toEqual([]);
      expect(newClient.cookieHeader).toBe('');
    });
  });

  describe('_request', () => {
    it('makes POST request with correct headers', async () => {
      const mockResponse = { errorcode: 0, result: { user_id: '12345' } };
      mockFetch.mockResolvedValueOnce({
        ok: true,
        text: () => Promise.resolve(JSON.stringify(mockResponse))
      });

      const result = await client._request('/platform/user/getauthdata');

      expect(mockFetch).toHaveBeenCalledWith(
        'https://quant.10jqka.com.cn/platform/user/getauthdata',
        expect.objectContaining({
          method: 'POST',
          headers: expect.objectContaining({
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': 'ths_session=test-session-token; user_id=12345',
            'X-Requested-With': 'XMLHttpRequest'
          })
        })
      );
      expect(result).toEqual(mockResponse);
    });

    it('parses JSONP response', async () => {
      const jsonResponse = { errorcode: 0, result: 'success' };
      const jsonpResponse = `callback(${JSON.stringify(jsonResponse)})`;
      mockFetch.mockResolvedValueOnce({
        ok: true,
        text: () => Promise.resolve(jsonpResponse)
      });

      const result = await client._request('/test');

      expect(result).toEqual(jsonResponse);
    });

    it('parses plain JSON response', async () => {
      const jsonResponse = { errorcode: 0, result: 'success' };
      mockFetch.mockResolvedValueOnce({
        ok: true,
        text: () => Promise.resolve(JSON.stringify(jsonResponse))
      });

      const result = await client._request('/test');

      expect(result).toEqual(jsonResponse);
    });

    it('returns raw text for non-JSON response', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: true,
        text: () => Promise.resolve('plain text response')
      });

      const result = await client._request('/test');

      expect(result).toEqual({ raw: 'plain text response' });
    });

    it('defaults body to isajax=1', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: true,
        text: () => Promise.resolve('{}')
      });

      await client._request('/test');

      expect(mockFetch).toHaveBeenCalledWith(
        expect.any(String),
        expect.objectContaining({
          body: 'isajax=1'
        })
      );
    });
  });

  describe('checkLogin', () => {
    it('returns logged status for logged in user', async () => {
      const mockResponse = { errorcode: 0, result: { user_id: '12345' } };
      mockFetch.mockResolvedValueOnce({
        ok: true,
        text: () => Promise.resolve(JSON.stringify(mockResponse))
      });

      const result = await client.checkLogin();

      expect(result).toEqual({
        logged: true,
        userId: '12345',
        data: mockResponse
      });
    });

    it('returns not logged in for error response', async () => {
      const mockResponse = { errorcode: -1, errormsg: 'Not logged in' };
      mockFetch.mockResolvedValueOnce({
        ok: true,
        text: () => Promise.resolve(JSON.stringify(mockResponse))
      });

      const result = await client.checkLogin();

      expect(result).toEqual({
        logged: false,
        userId: undefined,
        data: mockResponse
      });
    });
  });

  describe('listStrategies', () => {
    it('returns strategies list on success', async () => {
      const mockResponse = {
        errorcode: 0,
        result: {
          strategys: [
            { algo_id: '1', algo_name: 'Strategy 1' },
            { algo_id: '2', algo_name: 'Strategy 2' }
          ]
        }
      };
      mockFetch.mockResolvedValueOnce({
        ok: true,
        text: () => Promise.resolve(JSON.stringify(mockResponse))
      });

      const result = await client.listStrategies();

      expect(result).toEqual(mockResponse.result.strategys);
    });

    it('throws on error response', async () => {
      const mockResponse = { errorcode: -1, errormsg: '获取策略列表失败' };
      mockFetch.mockResolvedValueOnce({
        ok: true,
        text: () => Promise.resolve(JSON.stringify(mockResponse))
      });

      await expect(client.listStrategies()).rejects.toThrow('获取策略列表失败');
    });

    it('returns empty array when no strategies', async () => {
      const mockResponse = { errorcode: 0, result: {} };
      mockFetch.mockResolvedValueOnce({
        ok: true,
        text: () => Promise.resolve(JSON.stringify(mockResponse))
      });

      const result = await client.listStrategies();

      expect(result).toEqual([]);
    });
  });

  describe('createStrategy', () => {
    it('creates strategy successfully', async () => {
      const loginResponse = { errorcode: 0, result: { user_id: '12345' } };
      const createResponse = { errorcode: 0, result: { algo_id: 'new-algo-123' } };

      mockFetch
        .mockResolvedValueOnce({
          ok: true,
          text: () => Promise.resolve(JSON.stringify(loginResponse))
        })
        .mockResolvedValueOnce({
          ok: true,
          text: () => Promise.resolve(JSON.stringify(createResponse))
        });

      const result = await client.createStrategy('Test Strategy', 'print(1)');

      expect(result.success).toBe(true);
      expect(result.algoId).toBe('new-algo-123');
    });

    it('throws when not logged in', async () => {
      const loginResponse = { errorcode: -1 };
      mockFetch.mockResolvedValueOnce({
        ok: true,
        text: () => Promise.resolve(JSON.stringify(loginResponse))
      });

      await expect(client.createStrategy('Test', 'code')).rejects.toThrow('未登录');
    });

    it('returns failure for error response', async () => {
      const loginResponse = { errorcode: 0, result: { user_id: '12345' } };
      const createResponse = { errorcode: -1, errormsg: 'Strategy name exists' };

      mockFetch
        .mockResolvedValueOnce({
          ok: true,
          text: () => Promise.resolve(JSON.stringify(loginResponse))
        })
        .mockResolvedValueOnce({
          ok: true,
          text: () => Promise.resolve(JSON.stringify(createResponse))
        });

      const result = await client.createStrategy('Test Strategy', 'code');

      expect(result.success).toBe(false);
      expect(result.algoId).toBeUndefined();
    });
  });

  describe('runBacktest', () => {
    it('runs backtest with default config', async () => {
      const mockResponse = {
        errorcode: 0,
        result: { backtest_id: 'backtest-123' }
      };
      mockFetch.mockResolvedValueOnce({
        ok: true,
        text: () => Promise.resolve(JSON.stringify(mockResponse))
      });

      const result = await client.runBacktest('algo-123');

      expect(result.success).toBe(true);
      expect(result.backtestId).toBe('backtest-123');

      const call = mockFetch.mock.calls[0];
      expect(call[1].body).toContain('start_date=2023-01-01');
      expect(call[1].body).toContain('end_date=2024-12-31');
      expect(call[1].body).toContain('capital_base=100000');
      expect(call[1].body).toContain('frequency=DAILY');
      expect(call[1].body).toContain('benchmark=000300.SH');
    });

    it('runs backtest with custom config', async () => {
      const mockResponse = {
        errorcode: 0,
        result: { backtest_id: 'backtest-123' }
      };
      mockFetch.mockResolvedValueOnce({
        ok: true,
        text: () => Promise.resolve(JSON.stringify(mockResponse))
      });

      const result = await client.runBacktest('algo-123', {
        start_date: '2024-01-01',
        end_date: '2024-06-30',
        capital_base: 500000,
        frequency: 'MINUTE',
        benchmark: '000016.SH'
      });

      expect(result.success).toBe(true);

      const call = mockFetch.mock.calls[0];
      expect(call[1].body).toContain('start_date=2024-01-01');
      expect(call[1].body).toContain('capital_base=500000');
      expect(call[1].body).toContain('frequency=MINUTE');
    });

    it('returns failure for error response', async () => {
      const mockResponse = { errorcode: -1, errormsg: 'Backtest failed' };
      mockFetch.mockResolvedValueOnce({
        ok: true,
        text: () => Promise.resolve(JSON.stringify(mockResponse))
      });

      const result = await client.runBacktest('algo-123');

      expect(result.success).toBe(false);
      expect(result.data.errormsg).toBe('Backtest failed');
    });
  });

  describe('getBacktestResult', () => {
    it('fetches backtest result', async () => {
      const mockResponse = {
        errorcode: 0,
        result: {
          backtest_id: 'backtest-123',
          status: 'SUCCESS'
        }
      };
      mockFetch.mockResolvedValueOnce({
        ok: true,
        text: () => Promise.resolve(JSON.stringify(mockResponse))
      });

      const result = await client.getBacktestResult('backtest-123');

      expect(result).toEqual(mockResponse);
    });
  });

  describe('listSimuPapers', () => {
    it('returns simu papers list on success', async () => {
      const mockResponse = {
        errorcode: 0,
        result: [
          { algo_id: '1', name: 'Paper 1' },
          { algo_id: '2', name: 'Paper 2' }
        ]
      };
      mockFetch.mockResolvedValueOnce({
        ok: true,
        text: () => Promise.resolve(JSON.stringify(mockResponse))
      });

      const result = await client.listSimuPapers();

      expect(result).toEqual(mockResponse.result);
    });

    it('throws on error response', async () => {
      const mockResponse = { errorcode: -1, errormsg: '获取模拟交易列表失败' };
      mockFetch.mockResolvedValueOnce({
        ok: true,
        text: () => Promise.resolve(JSON.stringify(mockResponse))
      });

      await expect(client.listSimuPapers()).rejects.toThrow('获取模拟交易列表失败');
    });

    it('returns empty array when no result', async () => {
      const mockResponse = { errorcode: 0 };
      mockFetch.mockResolvedValueOnce({
        ok: true,
        text: () => Promise.resolve(JSON.stringify(mockResponse))
      });

      const result = await client.listSimuPapers();

      expect(result).toEqual([]);
    });
  });

  describe('saveResult', () => {
    it('saves result to file', () => {
      const data = { backtestId: '123', result: 'success' };
      const result = client.saveResult('test-backtest', data);

      expect(result).toContain('test-backtest');
      expect(result).toContain('.json');
      expect(fs.writeFileSync).toHaveBeenCalledWith(
        expect.any(String),
        JSON.stringify(data, null, 2)
      );
    });

    it('creates output directory if needed', () => {
      client.saveResult('test', {});
      expect(fs.mkdirSync).toHaveBeenCalled();
    });

    it('includes timestamp in filename', () => {
      const beforeTime = Date.now();
      const result = client.saveResult('test', {});
      const afterTime = Date.now();

      const match = result.match(/test-(\d+)\.json$/);
      expect(match).not.toBeNull();

      const timestamp = parseInt(match[1]);
      expect(timestamp).toBeGreaterThanOrEqual(beforeTime);
      expect(timestamp).toBeLessThanOrEqual(afterTime);
    });
  });
});