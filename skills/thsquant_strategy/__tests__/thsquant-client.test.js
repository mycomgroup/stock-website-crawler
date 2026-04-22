import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import fs from 'node:fs';
import path from 'node:path';

vi.mock('node:fs');
vi.mock('node:path', () => ({
  join: vi.fn((...args) => args.join('/')),
  dirname: vi.fn((p) => p.split('/').slice(0, -1).join('/')),
  resolve: vi.fn((p) => p),
}));

vi.mock('../load-env.js', () => {});
vi.mock('../paths.js', () => ({
  OUTPUT_ROOT: '/tmp/thsquant-test-output',
  SESSION_FILE: '/tmp/thsquant-test-session.json'
}));

vi.mock('../../common/http-security.js', () => ({
  SecureHttpClient: vi.fn().mockImplementation(() => ({
    request: vi.fn(),
  })),
  USER_AGENT: 'Mozilla/5.0 Test User Agent',
  SEC_CH_UA: '"Test";v="1"',
}));

let THSQuantClient;
let loadJson;

beforeAll(async () => {
  const module = await import('../request/thsquant-client.js');
  THSQuantClient = module.THSQuantClient;
  loadJson = module.loadJson;
});

beforeEach(() => {
  vi.clearAllMocks();
  fs.existsSync.mockReturnValue(true);
  fs.readFileSync.mockReturnValue(JSON.stringify({
    cookies: [{ name: 'sid', value: 'test-session', domain: '.10jqka.com.cn' }]
  }));
  fs.mkdirSync.mockReturnValue();
  fs.writeFileSync.mockReturnValue();
});

describe('loadJson helper', () => {
  it('returns parsed JSON for existing file', () => {
    fs.existsSync.mockReturnValue(true);
    fs.readFileSync.mockReturnValue(JSON.stringify({ key: 'value' }));

    const result = loadJson('/test/file.json');

    expect(result).toEqual({ key: 'value' });
  });

  it('returns empty object for non-existent file', () => {
    fs.existsSync.mockReturnValue(false);

    const result = loadJson('/nonexistent.json');

    expect(result).toEqual({});
  });

  it('returns empty object for invalid JSON', () => {
    fs.existsSync.mockReturnValue(true);
    fs.readFileSync.mockReturnValue('invalid json');

    const result = loadJson('/invalid.json');

    expect(result).toEqual({});
  });
});

describe('THSQuantClient', () => {
  let client;
  let mockSecureClient;

  beforeEach(async () => {
    mockSecureClient = {
      request: vi.fn(),
    };

    const { SecureHttpClient } = await import('../../common/http-security.js');
    SecureHttpClient.mockImplementation(() => mockSecureClient);

    client = new THSQuantClient();
  });

  describe('constructor', () => {
    it('initializes with default options', () => {
      expect(client.sessionFile).toBe('/tmp/thsquant-test-session.json');
      expect(client.outputRoot).toBe('/tmp/thsquant-test-output');
      expect(client.origin).toBe('https://quant.10jqka.com.cn');
    });

    it('initializes with custom options', () => {
      const customClient = new THSQuantClient({
        sessionFile: '/custom/session.json',
        outputRoot: '/custom/output',
      });

      expect(customClient.sessionFile).toBe('/custom/session.json');
      expect(customClient.outputRoot).toBe('/custom/output');
    });

    it('loads cookies from session file', () => {
      expect(client.cookieJar).toEqual([
        { name: 'sid', value: 'test-session', domain: '.10jqka.com.cn' }
      ]);
    });

    it('accepts direct cookies option', () => {
      const customCookies = [{ name: 'custom', value: 'cookie' }];
      const customClient = new THSQuantClient({ cookies: customCookies });

      expect(customClient.cookieJar).toEqual(customCookies);
    });

    it('handles empty session file', () => {
      fs.existsSync.mockReturnValue(false);

      const newClient = new THSQuantClient();

      expect(newClient.cookieJar).toEqual([]);
    });
  });

  describe('getCookieHeader', () => {
    it('formats cookies correctly', () => {
      client.cookieJar = [
        { name: 'sid', value: 'abc123' },
        { name: 'token', value: 'xyz789' }
      ];

      const result = client.getCookieHeader();

      expect(result).toBe('sid=abc123; token=xyz789');
    });

    it('returns empty string for no cookies', () => {
      client.cookieJar = [];

      const result = client.getCookieHeader();

      expect(result).toBe('');
    });
  });

  describe('buildHeaders', () => {
    it('returns correct headers with default referer', () => {
      client.cookieJar = [{ name: 'sid', value: 'test' }];

      const headers = client.buildHeaders();

      expect(headers['Content-Type']).toBe('application/x-www-form-urlencoded');
      expect(headers['X-Requested-With']).toBe('XMLHttpRequest');
      expect(headers['Cookie']).toBe('sid=test');
      expect(headers['Referer']).toBe('https://quant.10jqka.com.cn/view/study-index.html');
    });

    it('uses custom referer when provided', () => {
      const headers = client.buildHeaders('https://custom.url/page');

      expect(headers['Referer']).toBe('https://custom.url/page');
    });
  });

  describe('request', () => {
    it('makes request with correct URL', async () => {
      mockSecureClient.request.mockResolvedValue(JSON.stringify({ errorcode: 0 }));

      await client.request('/platform/test');

      expect(mockSecureClient.request).toHaveBeenCalledWith(
        'https://quant.10jqka.com.cn/platform/test',
        expect.any(Object)
      );
    });

    it('appends isajax=1 to body', async () => {
      mockSecureClient.request.mockResolvedValue(JSON.stringify({ errorcode: 0 }));

      await client.request('/test', 'param=value');

      const callArgs = mockSecureClient.request.mock.calls[0][1];
      expect(callArgs.body).toBe('param=value&isajax=1');
    });

    it('parses JSON response', async () => {
      const mockResponse = { errorcode: 0, result: { data: 'test' } };
      mockSecureClient.request.mockResolvedValue(JSON.stringify(mockResponse));

      const result = await client.request('/test');

      expect(result).toEqual(mockResponse);
    });

    it('parses JSONP response with parentheses', async () => {
      const mockResponse = { errorcode: 0, result: 'success' };
      mockSecureClient.request.mockResolvedValue(`(${JSON.stringify(mockResponse)})`);

      const result = await client.request('/test');

      expect(result).toEqual(mockResponse);
    });

    it('returns parse error for invalid response', async () => {
      mockSecureClient.request.mockResolvedValue('invalid response text');

      const result = await client.request('/test');

      expect(result).toHaveProperty('raw');
      expect(result).toHaveProperty('parseError');
    });
  });

  describe('checkLogin', () => {
    it('returns logged status for successful login', async () => {
      const mockResponse = { errorcode: 0, result: { user_id: '12345' } };
      mockSecureClient.request.mockResolvedValue(JSON.stringify(mockResponse));

      const result = await client.checkLogin();

      expect(result.logged).toBe(true);
      expect(result.userId).toBe('12345');
    });

    it('returns not logged in for error', async () => {
      const mockResponse = { errorcode: -1 };
      mockSecureClient.request.mockResolvedValue(JSON.stringify(mockResponse));

      const result = await client.checkLogin();

      expect(result.logged).toBe(false);
    });
  });

  describe('listStrategies', () => {
    it('returns formatted strategies list', async () => {
      const mockResponse = {
        errorcode: 0,
        result: {
          strategys: [
            { algo_id: '1', algo_name: 'Strategy 1', backtest_number: 5, backtest_id: 'bt1', modified: '2024-01-01' }
          ]
        }
      };
      mockSecureClient.request.mockResolvedValue(JSON.stringify(mockResponse));

      const result = await client.listStrategies();

      expect(result).toHaveLength(1);
      expect(result[0].id).toBe('1');
      expect(result[0].name).toBe('Strategy 1');
    });

    it('throws on API error', async () => {
      const mockResponse = { errorcode: -1, errormsg: 'Failed' };
      mockSecureClient.request.mockResolvedValue(JSON.stringify(mockResponse));

      await expect(client.listStrategies()).rejects.toThrow('Failed');
    });

    it('returns empty array when no strategies', async () => {
      const mockResponse = { errorcode: 0, result: {} };
      mockSecureClient.request.mockResolvedValue(JSON.stringify(mockResponse));

      const result = await client.listStrategies();

      expect(result).toEqual([]);
    });
  });

  describe('getStrategyInfo', () => {
    it('returns strategy info', async () => {
      const mockResponse = {
        errorcode: 0,
        result: { _id: 'algo-123', algo_name: 'Test' }
      };
      mockSecureClient.request.mockResolvedValue(JSON.stringify(mockResponse));

      const result = await client.getStrategyInfo('algo-123');

      expect(result._id).toBe('algo-123');
    });

    it('throws on error', async () => {
      const mockResponse = { errorcode: -1, errormsg: 'Not found' };
      mockSecureClient.request.mockResolvedValue(JSON.stringify(mockResponse));

      await expect(client.getStrategyInfo('invalid')).rejects.toThrow('Not found');
    });
  });

  describe('getStrategyContext', () => {
    it('returns combined strategy context', async () => {
      const infoResponse = {
        errorcode: 0,
        result: { _id: 'algo-123', algo_name: 'Test', language: 'python', stock_market: 'STOCK' }
      };
      const loginResponse = {
        errorcode: 0,
        result: { user_id: 'user-456' }
      };

      mockSecureClient.request
        .mockResolvedValueOnce(JSON.stringify(infoResponse))
        .mockResolvedValueOnce(JSON.stringify(loginResponse));

      const result = await client.getStrategyContext('algo-123');

      expect(result.algoId).toBe('algo-123');
      expect(result.name).toBe('Test');
      expect(result.userId).toBe('user-456');
    });
  });

  describe('saveStrategy', () => {
    it('saves strategy and returns success', async () => {
      const mockResponse = { errorcode: 0 };
      mockSecureClient.request.mockResolvedValue(JSON.stringify(mockResponse));

      const result = await client.saveStrategy('algo-123', 'New Name', 'new code');

      expect(result.success).toBe(true);
    });

    it('returns failure for error', async () => {
      const mockResponse = { errorcode: -1, errormsg: 'Save failed' };
      mockSecureClient.request.mockResolvedValue(JSON.stringify(mockResponse));

      const result = await client.saveStrategy('algo-123', 'Name', 'code');

      expect(result.success).toBe(false);
      expect(result.message).toBe('Save failed');
    });
  });

  describe('createStrategy', () => {
    it('creates strategy with correct parameters', async () => {
      const mockResponse = {
        errorcode: 0,
        result: { _id: 'new-algo-123' }
      };
      mockSecureClient.request.mockResolvedValue(JSON.stringify(mockResponse));

      const result = await client.createStrategy('My Strategy', 'my code', 'STOCK');

      expect(result.success).toBe(true);
      expect(result.algoId).toBe('new-algo-123');

      const callArgs = mockSecureClient.request.mock.calls[0][1];
      expect(callArgs.body).toContain('algoName=My+Strategy');
    });
  });

  describe('deleteStrategy', () => {
    it('deletes strategy successfully', async () => {
      const mockResponse = { errorcode: 0 };
      mockSecureClient.request.mockResolvedValue(JSON.stringify(mockResponse));

      const result = await client.deleteStrategy('algo-123');

      expect(result.success).toBe(true);
    });
  });

  describe('runBacktest', () => {
    it('runs backtest with default config', async () => {
      const mockResponse = {
        errorcode: 0,
        result: { backtest_id: 'bt-123', progress: 0 }
      };
      mockSecureClient.request.mockResolvedValue(JSON.stringify(mockResponse));

      const result = await client.runBacktest('algo-123');

      expect(result.backtestId).toBe('bt-123');

      const callArgs = mockSecureClient.request.mock.calls[0][1];
      expect(callArgs.body).toContain('beginDate=2023-01-01');
      expect(callArgs.body).toContain('endDate=2024-12-31');
      expect(callArgs.body).toContain('capitalBase=100000');
    });

    it('runs backtest with custom config', async () => {
      const mockResponse = { errorcode: 0, result: { backtest_id: 'bt-123' } };
      mockSecureClient.request.mockResolvedValue(JSON.stringify(mockResponse));

      await client.runBacktest('algo-123', {
        beginDate: '2024-01-01',
        endDate: '2024-06-30',
        capitalBase: 500000
      });

      const callArgs = mockSecureClient.request.mock.calls[0][1];
      expect(callArgs.body).toContain('beginDate=2024-01-01');
      expect(callArgs.body).toContain('endDate=2024-06-30');
      expect(callArgs.body).toContain('capitalBase=500000');
    });

    it('throws on ERROR type result', async () => {
      const mockResponse = {
        errorcode: 0,
        result: { type: 'ERROR', value: 'Strategy code error' }
      };
      mockSecureClient.request.mockResolvedValue(JSON.stringify(mockResponse));

      await expect(client.runBacktest('algo-123')).rejects.toThrow('回测启动失败');
    });
  });

  describe('cancelBacktest', () => {
    it('cancels backtest successfully', async () => {
      const mockResponse = { errorcode: 0 };
      mockSecureClient.request.mockResolvedValue(JSON.stringify(mockResponse));

      const result = await client.cancelBacktest('bt-123');

      expect(result.success).toBe(true);
    });
  });

  describe('pollBacktestStatus', () => {
    it('returns status info', async () => {
      const mockResponse = {
        errorcode: 0,
        result: { status: 'RUNNING', progress: 50 }
      };
      mockSecureClient.request.mockResolvedValue(JSON.stringify(mockResponse));

      const result = await client.pollBacktestStatus('bt-123');

      expect(result.status).toBe('RUNNING');
      expect(result.progress).toBe(50);
    });

    it('returns ERROR status on API error', async () => {
      const mockResponse = { errorcode: -1, errormsg: 'Poll failed' };
      mockSecureClient.request.mockResolvedValue(JSON.stringify(mockResponse));

      const result = await client.pollBacktestStatus('bt-123');

      expect(result.status).toBe('ERROR');
      expect(result.error).toBe('Poll failed');
    });
  });

  describe('waitForBacktest', () => {
    it('waits for SUCCESS status', async () => {
      mockSecureClient.request
        .mockResolvedValueOnce(JSON.stringify({ errorcode: 0, result: { status: 'RUNNING' } }))
        .mockResolvedValueOnce(JSON.stringify({ errorcode: 0, result: { status: 'SUCCESS' } }));

      const result = await client.waitForBacktest('bt-123', { interval: 100, maxWait: 1000 });

      expect(result.success).toBe(true);
    });

    it('returns failure on FAILED status', async () => {
      mockSecureClient.request.mockResolvedValue(
        JSON.stringify({ errorcode: 0, result: { status: 'FAILED' } })
      );

      const result = await client.waitForBacktest('bt-123', { interval: 100 });

      expect(result.success).toBe(false);
    });

    it('returns timeout failure', async () => {
      mockSecureClient.request.mockResolvedValue(
        JSON.stringify({ errorcode: 0, result: { status: 'RUNNING' } })
      );

      const result = await client.waitForBacktest('bt-123', { maxWait: 200, interval: 100 });

      expect(result.success).toBe(false);
      expect(result.error).toBe('回测超时');
    });
  });

  describe('getBacktestInfo', () => {
    it('returns backtest info', async () => {
      const mockResponse = { errorcode: 0, result: { backtest_id: 'bt-123' } };
      mockSecureClient.request.mockResolvedValue(JSON.stringify(mockResponse));

      const result = await client.getBacktestInfo('bt-123');

      expect(result.backtest_id).toBe('bt-123');
    });
  });

  describe('getBacktestDetail', () => {
    it('returns backtest detail', async () => {
      const mockResponse = { errorcode: 0, result: { detail: 'full' } };
      mockSecureClient.request.mockResolvedValue(JSON.stringify(mockResponse));

      const result = await client.getBacktestDetail('bt-123');

      expect(result.detail).toBe('full');
    });
  });

  describe('getBacktestPerformance', () => {
    it('returns performance data', async () => {
      const mockResponse = { errorcode: 0, result: { sharpe: 1.5 } };
      mockSecureClient.request.mockResolvedValue(JSON.stringify(mockResponse));

      const result = await client.getBacktestPerformance('bt-123');

      expect(result.sharpe).toBe(1.5);
    });
  });

  describe('getTradeLog', () => {
    it('returns trade log array', async () => {
      const mockResponse = { errorcode: 0, result: { data: [{ trade: 1 }] } };
      mockSecureClient.request.mockResolvedValue(JSON.stringify(mockResponse));

      const result = await client.getTradeLog('bt-123');

      expect(result).toEqual([{ trade: 1 }]);
    });

    it('returns empty array on error', async () => {
      const mockResponse = { errorcode: -1 };
      mockSecureClient.request.mockResolvedValue(JSON.stringify(mockResponse));

      const result = await client.getTradeLog('bt-123');

      expect(result).toEqual([]);
    });
  });

  describe('getBacktestLog', () => {
    it('returns log list', async () => {
      const mockResponse = { errorcode: 0, result: { list: [{ log: 1 }] } };
      mockSecureClient.request.mockResolvedValue(JSON.stringify(mockResponse));

      const result = await client.getBacktestLog('bt-123');

      expect(result).toEqual([{ log: 1 }]);
    });

    it('returns empty array on error', async () => {
      const mockResponse = { errorcode: -1 };
      mockSecureClient.request.mockResolvedValue(JSON.stringify(mockResponse));

      const result = await client.getBacktestLog('bt-123');

      expect(result).toEqual([]);
    });
  });

  describe('getDailyPositionGains', () => {
    it('returns daily gains', async () => {
      const mockResponse = { errorcode: 0, result: { data: [{ gain: 0.01 }] } };
      mockSecureClient.request.mockResolvedValue(JSON.stringify(mockResponse));

      const result = await client.getDailyPositionGains('bt-123');

      expect(result).toEqual([{ gain: 0.01 }]);
    });

    it('returns empty array on error', async () => {
      const mockResponse = { errorcode: -1 };
      mockSecureClient.request.mockResolvedValue(JSON.stringify(mockResponse));

      const result = await client.getDailyPositionGains('bt-123');

      expect(result).toEqual([]);
    });
  });

  describe('getBacktestSpecificInfo', () => {
    it('returns specific info', async () => {
      const mockResponse = { errorcode: 0, result: { profit: 100 } };
      mockSecureClient.request.mockResolvedValue(JSON.stringify(mockResponse));

      const result = await client.getBacktestSpecificInfo('bt-123', 'profit');

      expect(result.profit).toBe(100);
    });

    it('returns null on error', async () => {
      const mockResponse = { errorcode: -1 };
      mockSecureClient.request.mockResolvedValue(JSON.stringify(mockResponse));

      const result = await client.getBacktestSpecificInfo('bt-123');

      expect(result).toBeNull();
    });
  });

  describe('getRiskAnalysis', () => {
    it('returns risk analysis', async () => {
      const mockResponse = { errorcode: 0, result: { max_drawdown: 0.1 } };
      mockSecureClient.request.mockResolvedValue(JSON.stringify(mockResponse));

      const result = await client.getRiskAnalysis('bt-123');

      expect(result.max_drawdown).toBe(0.1);
    });

    it('returns null on error', async () => {
      const mockResponse = { errorcode: -1 };
      mockSecureClient.request.mockResolvedValue(JSON.stringify(mockResponse));

      const result = await client.getRiskAnalysis('bt-123');

      expect(result).toBeNull();
    });
  });

  describe('getLatestBacktest', () => {
    it('returns latest backtest', async () => {
      const mockResponse = { errorcode: 0, result: { backtest_id: 'latest' } };
      mockSecureClient.request.mockResolvedValue(JSON.stringify(mockResponse));

      const result = await client.getLatestBacktest('algo-123');

      expect(result.backtest_id).toBe('latest');
    });

    it('returns null on error', async () => {
      const mockResponse = { errorcode: -1 };
      mockSecureClient.request.mockResolvedValue(JSON.stringify(mockResponse));

      const result = await client.getLatestBacktest('algo-123');

      expect(result).toBeNull();
    });
  });

  describe('listBacktests', () => {
    it('returns backtest history', async () => {
      const mockResponse = { errorcode: 0, result: { history: [{ id: 'bt1' }] } };
      mockSecureClient.request.mockResolvedValue(JSON.stringify(mockResponse));

      const result = await client.listBacktests('algo-123', 1, 10);

      expect(result).toEqual([{ id: 'bt1' }]);
    });

    it('returns empty array on error', async () => {
      const mockResponse = { errorcode: -1 };
      mockSecureClient.request.mockResolvedValue(JSON.stringify(mockResponse));

      const result = await client.listBacktests('algo-123');

      expect(result).toEqual([]);
    });
  });

  describe('getFullReport', () => {
    it('returns full report with all data', async () => {
      mockSecureClient.request.mockResolvedValue(JSON.stringify({ errorcode: 0, result: {} }));

      const result = await client.getFullReport('bt-123');

      expect(result.backtestId).toBe('bt-123');
    });
  });

  describe('writeArtifact', () => {
    it('writes JSON artifact', () => {
      const data = { test: 'data' };

      const result = client.writeArtifact('test-name', data);

      expect(result).toContain('test-name');
      expect(result).toContain('.json');
      expect(fs.writeFileSync).toHaveBeenCalled();
    });

    it('includes timestamp in filename', () => {
      const result = client.writeArtifact('test', {});

      expect(result).toMatch(/test-\d+\.json$/);
    });
  });
});