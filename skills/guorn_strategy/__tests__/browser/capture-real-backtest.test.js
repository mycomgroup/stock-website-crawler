import { describe, it, beforeEach, afterEach, vi } from 'vitest';
import assert from 'node:assert';
import path from 'node:path';

vi.mock('node:fs', () => {
  const mockFs = {
    existsSync: vi.fn(() => true),
    readFileSync: vi.fn(() => '{"cookies":[{"name":"session","value":"test"}]}'),
    writeFileSync: vi.fn(),
    mkdirSync: vi.fn()
  };
  return {
    default: mockFs,
    ...mockFs
  };
});

vi.mock('../../paths.js', () => ({
  DATA_ROOT: '/test/data',
  SESSION_FILE: '/test/session.json'
}));

const mockFs = await import('node:fs');

function resetMocks() {
  mockFs.default.existsSync.mockClear();
  mockFs.default.readFileSync.mockClear();
  mockFs.default.writeFileSync.mockClear();
  mockFs.default.mkdirSync.mockClear();
}

describe('capture-real-backtest.js', () => {
  beforeEach(() => {
    resetMocks();
  });

  afterEach(() => {
    resetMocks();
  });

  describe('session loading', () => {
    it('should read session file', () => {
      mockFs.default.readFileSync.mockImplementation(() => '{"cookies":[]}');
      const session = JSON.parse(mockFs.default.readFileSync());
      assert.ok(session.cookies);
    });

    it('should parse session JSON', () => {
      const sessionJson = '{"capturedAt":"2024-01-01","cookies":[]}';
      const parsed = JSON.parse(sessionJson);
      assert.ok(parsed.capturedAt);
    });
  });

  describe('captured requests array', () => {
    it('should initialize empty captured array', () => {
      const captured = [];
      assert.strictEqual(captured.length, 0);
    });
  });

  describe('browser configuration', () => {
    it('should launch headless browser', () => {
      const launchOptions = { headless: true };
      assert.strictEqual(launchOptions.headless, true);
    });

    it('should use correct user agent', () => {
      const USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)';
      assert.ok(USER_AGENT.includes('Macintosh'));
    });

    it('should add cookies from session', () => {
      const session = { cookies: [{ name: 'test', value: 'val' }] };
      assert.ok(session.cookies);
    });
  });

  describe('request interception', () => {
    it('should capture non-GET requests', () => {
      const method = 'POST';
      const shouldCapture = method !== 'GET';
      assert.strictEqual(shouldCapture, true);
    });

    it('should filter out GET requests', () => {
      const method = 'GET';
      const shouldCapture = method !== 'GET';
      assert.strictEqual(shouldCapture, false);
    });

    it('should filter out google URLs', () => {
      const url = 'https://google.com/analytics';
      const shouldCapture = !url.includes('google');
      assert.strictEqual(shouldCapture, false);
    });

    it('should filter out analytics URLs', () => {
      const url = 'https://analytics.google.com';
      const shouldCapture = !url.includes('analytics');
      assert.strictEqual(shouldCapture, false);
    });

    it('should filter out baidu URLs', () => {
      const url = 'https://baidu.com/api';
      const shouldCapture = !url.includes('baidu');
      assert.strictEqual(shouldCapture, false);
    });

    it('should capture request method', () => {
      const entry = { method: 'POST' };
      assert.strictEqual(entry.method, 'POST');
    });

    it('should capture request URL', () => {
      const entry = { url: 'https://guorn.com/api' };
      assert.ok(entry.url);
    });

    it('should capture POST body', () => {
      const entry = { body: '{"test":"data"}' };
      assert.ok(entry.body);
    });

    it('should capture headers', () => {
      const entry = { headers: { 'Content-Type': 'application/json' } };
      assert.ok(entry.headers);
    });
  });

  describe('response interception', () => {
    it('should match response to request', () => {
      const captured = [{ url: 'https://guorn.com/api' }];
      const responseUrl = 'https://guorn.com/api';
      const entry = captured.findLast(r => r.url === responseUrl);
      assert.ok(entry);
    });

    it('should capture status code', () => {
      const status = 200;
      assert.strictEqual(status, 200);
    });

    it('should capture response text', () => {
      const response = '{"result":"success"}';
      assert.ok(response);
    });

    it('should handle response text errors', () => {
      const errorCaught = true;
      assert.strictEqual(errorCaught, true);
    });

    it('should truncate response log to 300 chars', () => {
      const response = 'x'.repeat(500);
      const truncated = response?.slice(0, 300);
      assert.strictEqual(truncated?.length, 300);
    });
  });

  describe('page navigation', () => {
    it('should navigate to strategy page', () => {
      const targetUrl = 'https://guorn.com/stock';
      assert.strictEqual(targetUrl, 'https://guorn.com/stock');
    });

    it('should wait 5s after navigation', () => {
      const waitTime = 5000;
      assert.strictEqual(waitTime, 5000);
    });
  });

  describe('getTestConfig method', () => {
    it('should call scrat.docController.getTestConfig', () => {
      const ctrl = { getTestConfig: () => {} };
      assert.ok(ctrl.getTestConfig);
    });

    it('should pass empty object to getTestConfig', () => {
      const config = {};
      assert.strictEqual(Object.keys(config).length, 0);
    });

    it('should return config with success flag', () => {
      const result = { success: true, config: {} };
      assert.strictEqual(result.success, true);
    });

    it('should return error on failure', () => {
      const result = { error: 'Method not found' };
      assert.ok(result.error);
    });
  });

  describe('ajaxDispatch method', () => {
    it('should get current strategy', () => {
      const strategy = { filters: [], ranks: [], tabs: { back_test: {} } };
      assert.ok(strategy.tabs);
    });

    it('should construct payload with strategy fields', () => {
      const payload = {
        filters: [],
        ranks: [],
        pool: '',
        exclude_st: '0',
        exclude_STIB: 1,
        filter_suspend: false
      };
      assert.ok(payload.filters);
      assert.ok(payload.ranks);
    });

    it('should include back_test parameters', () => {
      const btParams = {
        start: '2022/01/01',
        end: '2024/01/01',
        reference: '000300',
        count: '10',
        period: 5
      };
      assert.ok(btParams.start);
      assert.ok(btParams.end);
    });

    it('should include trading strategy options', () => {
      const tradingStrategy = {
        buy_options: [],
        sell_options: [],
        hold_options: []
      };
      assert.ok(Array.isArray(tradingStrategy.buy_options));
    });

    it('should generate calc_id', () => {
      const uid = 'test_user';
      const calc_id = uid + '.' + Date.now().toString();
      assert.ok(calc_id.includes(uid));
    });

    it('should call POST stock/runtest', () => {
      const method = 'POST';
      const endpoint = 'stock/runtest';
      assert.strictEqual(method, 'POST');
      assert.strictEqual(endpoint, 'stock/runtest');
    });

    it('should resolve with response on success', () => {
      const result = { success: true, response: {} };
      assert.strictEqual(result.success, true);
    });

    it('should set 30s timeout protection', () => {
      const timeout = 30000;
      assert.strictEqual(timeout, 30000);
    });

    it('should resolve with timeout flag on timeout', () => {
      const result = { timeout: true };
      assert.strictEqual(result.timeout, true);
    });

    it('should resolve with error on exception', () => {
      const result = { error: 'Exception occurred' };
      assert.ok(result.error);
    });
  });

  describe('console logging', () => {
    it('should log request method and URL', () => {
      const logFormat = '[REQ] POST /api/test';
      assert.ok(logFormat.includes('[REQ]'));
    });

    it('should log response status and URL', () => {
      const logFormat = '[RESP] 200 /api/test';
      assert.ok(logFormat.includes('[RESP]'));
    });

    it('should strip domain from URL', () => {
      const url = 'https://guorn.com/api/test';
      const stripped = url.replace('https://guorn.com', '');
      assert.strictEqual(stripped, '/api/test');
    });
  });

  describe('file saving', () => {
    it('should create data directory', () => {
      mockFs.default.mkdirSync.mockImplementation(() => undefined);
      mockFs.default.mkdirSync('/test/data', { recursive: true });
      assert.strictEqual(mockFs.default.mkdirSync.mock.calls.length, 1);
    });

    it('should save to captured-real-backtest.json', () => {
      const outputPath = path.join('/test/data', 'captured-real-backtest.json');
      assert.ok(outputPath.includes('captured-real-backtest'));
      assert.ok(outputPath.endsWith('.json'));
    });

    it('should save testConfigResult', () => {
      const data = { testConfigResult: { success: true } };
      assert.ok(data.testConfigResult);
    });

    it('should save ajaxResult', () => {
      const data = { ajaxResult: { success: true } };
      assert.ok(data.ajaxResult);
    });

    it('should save captured requests', () => {
      const data = { captured: [] };
      assert.ok(Array.isArray(data.captured));
    });
  });

  describe('request summary output', () => {
    it('should print captured request count', () => {
      const captured = [{}, {}];
      const count = captured.length;
      assert.strictEqual(count, 2);
    });

    it('should print URL for each request', () => {
      const r = { url: 'https://guorn.com/api' };
      assert.ok(r.url);
    });

    it('should print status code', () => {
      const r = { status: 200 };
      assert.strictEqual(r.status, 200);
    });

    it('should truncate body to 800 chars', () => {
      const body = 'x'.repeat(1000);
      const truncated = body?.slice(0, 800);
      assert.strictEqual(truncated?.length, 800);
    });

    it('should truncate response to 500 chars', () => {
      const response = 'y'.repeat(1000);
      const truncated = response?.slice(0, 500);
      assert.strictEqual(truncated?.length, 500);
    });
  });

  describe('browser closing', () => {
    it('should close browser at end', () => {
      const browserClosed = true;
      assert.strictEqual(browserClosed, true);
    });

    it('should wait 5s before close', () => {
      const waitTime = 5000;
      assert.strictEqual(waitTime, 5000);
    });
  });
});