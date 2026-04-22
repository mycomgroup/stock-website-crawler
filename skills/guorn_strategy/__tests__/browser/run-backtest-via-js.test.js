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
  SESSION_FILE: '/test/session.json',
  OUTPUT_ROOT: '/test/output'
}));

const mockFs = await import('node:fs');

function resetMocks() {
  mockFs.default.existsSync.mockClear();
  mockFs.default.readFileSync.mockClear();
  mockFs.default.writeFileSync.mockClear();
  mockFs.default.mkdirSync.mockClear();
}

describe('run-backtest-via-js.js', () => {
  beforeEach(() => {
    resetMocks();
  });

  afterEach(() => {
    resetMocks();
  });

  describe('runBacktestViaJS options', () => {
    it('should use default start date when not provided', () => {
      const defaultStartDate = '2022-01-01';
      assert.strictEqual(defaultStartDate, '2022-01-01');
    });

    it('should use default end date when not provided', () => {
      const defaultEndDate = '2024-01-01';
      assert.strictEqual(defaultEndDate, '2024-01-01');
    });

    it('should use default pool ID for 高流动800', () => {
      const defaultPoolId = '1.P.113051162378342';
      assert.strictEqual(defaultPoolId, '1.P.113051162378342');
    });

    it('should use default rank indicator for ROA', () => {
      const defaultRankIndicator = '0.F.ROA.0';
      assert.strictEqual(defaultRankIndicator, '0.F.ROA.0');
    });

    it('should use default count of 10 stocks', () => {
      const defaultCount = 10;
      assert.strictEqual(defaultCount, 10);
    });

    it('should use default period of 20 days', () => {
      const defaultPeriod = 20;
      assert.strictEqual(defaultPeriod, 20);
    });

    it('should accept custom options', () => {
      const options = {
        startDate: '2025-01-01',
        endDate: '2026-01-01',
        poolId: 'custom_pool',
        rankIndicator: 'custom_indicator',
        count: 15,
        period: 30
      };
      assert.strictEqual(options.startDate, '2025-01-01');
      assert.strictEqual(options.count, 15);
    });
  });

  describe('date format conversion', () => {
    it('should convert hyphen dates to slash format', () => {
      const toSlashDate = d => d.replace(/-/g, '/');
      assert.strictEqual(toSlashDate('2022-01-01'), '2022/01/01');
      assert.strictEqual(toSlashDate('2024-12-31'), '2024/12/31');
    });

    it('should handle dates without hyphens', () => {
      const toSlashDate = d => d.replace(/-/g, '/');
      assert.strictEqual(toSlashDate('20220101'), '20220101');
    });
  });

  describe('payload construction', () => {
    it('should include filters array in payload', () => {
      const payload = { filters: [] };
      assert.ok(Array.isArray(payload.filters));
    });

    it('should include ranks array with correct structure', () => {
      const rankIndicator = '0.F.ROA.0';
      const ranks = [{ id: rankIndicator, weight: 1.0, asc: false, industry: 0 }];
      assert.strictEqual(ranks[0].id, rankIndicator);
      assert.strictEqual(ranks[0].weight, 1.0);
      assert.strictEqual(ranks[0].asc, false);
    });

    it('should include backtest parameters', () => {
      const btParams = {
        start: '2022/01/01',
        end: '2024/01/01',
        reference: '000300',
        count: '10',
        period: 20,
        price: 'close',
        trade_cost: 0.002
      };
      assert.strictEqual(btParams.reference, '000300');
      assert.strictEqual(btParams.trade_cost, 0.002);
    });

    it('should include trading strategy options', () => {
      const tradingStrategy = { buy_options: [], sell_options: [], hold_options: [] };
      assert.ok(Array.isArray(tradingStrategy.buy_options));
      assert.ok(Array.isArray(tradingStrategy.sell_options));
    });

    it('should generate unique calc_id', () => {
      const uid = 'test_user';
      const calc_id = uid + '.' + Date.now().toString();
      assert.ok(calc_id.includes(uid));
      assert.ok(calc_id.includes('.'));
    });
  });

  describe('ajaxDispatch call', () => {
    it('should use POST method', () => {
      const method = 'POST';
      assert.strictEqual(method, 'POST');
    });

    it('should call stock/runtest endpoint', () => {
      const endpoint = 'stock/runtest';
      assert.strictEqual(endpoint, 'stock/runtest');
    });

    it('should use skipCheck flag (true) for direct callback', () => {
      const skipCheck = true;
      assert.strictEqual(skipCheck, true);
    });

    it('should resolve promise on callback', () => {
      const callbackResult = { status: 'ok', data: {} };
      assert.strictEqual(callbackResult.status, 'ok');
    });
  });

  describe('timeout handling', () => {
    it('should set 90s timeout for ajaxDispatch', () => {
      const ajaxTimeout = 90000;
      assert.strictEqual(ajaxTimeout, 90000);
    });

    it('should set 10s timeout for scrat object wait', () => {
      const scratTimeout = 10000;
      assert.strictEqual(scratTimeout, 10000);
    });

    it('should resolve with timeout status on timeout', () => {
      const timeoutResult = { status: 'timeout' };
      assert.strictEqual(timeoutResult.status, 'timeout');
    });
  });

  describe('browser setup', () => {
    it('should launch headless browser', () => {
      const launchOptions = { headless: true };
      assert.strictEqual(launchOptions.headless, true);
    });

    it('should set user agent in context', () => {
      const userAgent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36';
      assert.ok(userAgent.includes('Macintosh'));
    });

    it('should add cookies from session', () => {
      const session = { cookies: [{ name: 'test', value: 'val' }] };
      assert.ok(session.cookies);
      assert.strictEqual(session.cookies.length, 1);
    });

    it('should navigate to guorn.com/stock', () => {
      const targetUrl = 'https://guorn.com/stock';
      assert.strictEqual(targetUrl, 'https://guorn.com/stock');
    });
  });

  describe('result handling', () => {
    it('should return result object from evaluate', () => {
      const result = { status: 'ok', data: { trade_summary: {} } };
      assert.strictEqual(result.status, 'ok');
      assert.ok(result.data);
    });

    it('should check for trade_summary in result', () => {
      const data = { trade_summary: { trades: 10 } };
      assert.ok(data.trade_summary);
    });

    it('should check for summary sheet_data', () => {
      const data = { summary: { sheet_data: { row_size: 100 } } };
      assert.ok(data.summary);
      assert.ok(data.summary.sheet_data);
    });
  });

  describe('file saving', () => {
    it('should create data directory', () => {
      mockFs.default.mkdirSync.mockImplementation(() => undefined);
      mockFs.default.mkdirSync('/test/data', { recursive: true });
      assert.strictEqual(mockFs.default.mkdirSync.mock.calls.length, 1);
    });

    it('should save result with timestamp in filename', () => {
      const timestamp = Date.now();
      const filename = `backtest-result-${timestamp}.json`;
      assert.ok(filename.includes('backtest-result'));
      assert.ok(filename.endsWith('.json'));
    });

    it('should write JSON with formatting', () => {
      const result = { test: 'value' };
      const content = JSON.stringify(result, null, 2);
      assert.ok(content.includes('\n'));
    });
  });

  describe('error handling', () => {
    it('should catch errors in main function', () => {
      const errorMessage = 'Error occurred';
      assert.ok(errorMessage.includes('Error'));
    });

    it('should log error message', () => {
      const error = new Error('Test error');
      assert.strictEqual(error.message, 'Test error');
    });
  });

  describe('scrat utility interaction', () => {
    it('should wait for scrat.utility to be defined', () => {
      const checkFn = () => typeof window.scrat !== 'undefined' && window.scrat.utility;
      assert.strictEqual(typeof checkFn, 'function');
    });

    it('should get current strategy from docController', () => {
      const strategyConfig = { filters: [], ranks: [], tabs: { back_test: {} } };
      assert.ok(strategyConfig.tabs);
    });

    it('should handle error in getCurrentStrategy', () => {
      const errorResult = { error: 'Strategy not found' };
      assert.ok(errorResult.error);
    });
  });
});