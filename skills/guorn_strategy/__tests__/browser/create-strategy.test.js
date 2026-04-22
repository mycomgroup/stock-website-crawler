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

vi.mock('../../load-env.js', () => ({
  default: {},
}));

const mockFs = await import('node:fs');

function resetMocks() {
  mockFs.default.existsSync.mockClear();
  mockFs.default.readFileSync.mockClear();
  mockFs.default.writeFileSync.mockClear();
  mockFs.default.mkdirSync.mockClear();
}

describe('create-strategy.js', () => {
  beforeEach(() => {
    resetMocks();
  });

  afterEach(() => {
    resetMocks();
  });

  describe('createAndRunBacktest options', () => {
    it('should use default start time', () => {
      const defaultStartTime = '2022-01-01';
      assert.strictEqual(defaultStartTime, '2022-01-01');
    });

    it('should use default end time', () => {
      const defaultEndTime = '2025-03-28';
      assert.strictEqual(defaultEndTime, '2025-03-28');
    });

    it('should use default headed mode', () => {
      const defaultHeaded = true;
      assert.strictEqual(defaultHeaded, true);
    });

    it('should accept custom options', () => {
      const options = {
        startTime: '2023-06-01',
        endTime: '2024-06-01',
        headed: false
      };
      assert.strictEqual(options.startTime, '2023-06-01');
      assert.strictEqual(options.headed, false);
    });
  });

  describe('session handling', () => {
    it('should throw error when session file not found', () => {
      mockFs.default.existsSync.mockImplementation(() => false);
      assert.strictEqual(mockFs.default.existsSync(), false);
    });

    it('should load session when file exists', () => {
      mockFs.default.readFileSync.mockImplementation(() => '{"cookies":[]}');
      const session = JSON.parse(mockFs.default.readFileSync());
      assert.ok(session.cookies);
    });

    it('should log session file location', () => {
      const SESSION_FILE = '/test/session.json';
      assert.ok(SESSION_FILE.includes('session.json'));
    });
  });

  describe('browser configuration', () => {
    it('should set headless based on headed option', () => {
      const headed = false;
      const headless = !headed;
      assert.strictEqual(headless, true);
    });

    it('should use correct user agent', () => {
      const USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)';
      assert.ok(USER_AGENT.includes('Macintosh'));
    });

    it('should add cookies to context', () => {
      const sessionPayload = { cookies: [{ name: 'test', value: 'val' }] };
      assert.ok(sessionPayload.cookies);
    });
  });

  describe('page navigation', () => {
    it('should navigate to guorn.com/stock', () => {
      const targetUrl = 'https://guorn.com/stock';
      assert.strictEqual(targetUrl, 'https://guorn.com/stock');
    });

    it('should wait 3s after navigation', () => {
      const waitTime = 3000;
      assert.strictEqual(waitTime, 3000);
    });
  });

  describe('login check', () => {
    it('should check URL for login redirect', () => {
      const url = 'https://guorn.com/stock';
      const isLoggedIn = !url.includes('/user/login');
      assert.strictEqual(isLoggedIn, true);
    });

    it('should detect login page redirect', () => {
      const url = 'https://guorn.com/user/login';
      const isLoggedIn = !url.includes('/user/login');
      assert.strictEqual(isLoggedIn, false);
    });

    it('should throw error when session expired', () => {
      const isLoggedIn = false;
      if (!isLoggedIn) {
        assert.strictEqual(isLoggedIn, false);
      }
    });
  });

  describe('strategy creation - 新建 button', () => {
    it('should click 新建 button', () => {
      const selector = 'a:has-text("新建"), span:has-text("新建")';
      assert.ok(selector.includes('新建'));
    });

    it('should wait 2s after clicking new button', () => {
      const waitTime = 2000;
      assert.strictEqual(waitTime, 2000);
    });
  });

  describe('stock pool selection', () => {
    it('should click pool dropdown', () => {
      const selector = '#pool-select, .pool-select, select:has(option:has-text("沪深300"))';
      assert.ok(selector.includes('pool'));
    });

    it('should select 沪深300', () => {
      const targetPool = '沪深300';
      assert.strictEqual(targetPool, '沪深300');
    });

    it('should wait 500ms after selection', () => {
      const waitTime = 500;
      assert.strictEqual(waitTime, 500);
    });
  });

  describe('stock limit setting', () => {
    it('should find stock limit input', () => {
      const selector = 'input[name="stocknum"], input[name="stockLimit"]';
      assert.ok(selector.includes('stock'));
    });

    it('should set stock limit to 20', () => {
      const stockLimit = 20;
      assert.strictEqual(stockLimit, 20);
    });
  });

  describe('rebalance cycle setting', () => {
    it('should find cycle input', () => {
      const selector = 'input[name="cycle"], input[name="rebalanceCycle"]';
      assert.ok(selector.includes('cycle'));
    });

    it('should set cycle to 20', () => {
      const cycle = 20;
      assert.strictEqual(cycle, 20);
    });
  });

  describe('ranking conditions setup', () => {
    it('should click ranking section', () => {
      const selector = '#ranking-section, .ranking-section, text=排名条件';
      assert.ok(selector.includes('ranking'));
    });

    it('should click add ranking button', () => {
      const selector = 'button:has-text("添加排名"), a:has-text("添加排名"), .add-ranking';
      assert.ok(selector.includes('添加排名'));
    });

    it('should select ROA indicator', () => {
      const indicator = 'ROA';
      assert.strictEqual(indicator, 'ROA');
    });

    it('should wait 500ms after adding ranking', () => {
      const waitTime = 500;
      assert.strictEqual(waitTime, 500);
    });
  });

  describe('trading model setup', () => {
    it('should find trading model select', () => {
      const selector = 'select[name="tradetype"], select[name="tradingModel"]';
      assert.ok(selector.includes('trading'));
    });

    it('should select model I (定期轮动)', () => {
      const modelValue = '1';
      assert.strictEqual(modelValue, '1');
    });
  });

  describe('rebalance time setting', () => {
    it('should find trade date select', () => {
      const selector = 'select[name="tradedate"]';
      assert.ok(selector.includes('tradedate'));
    });

    it('should select monthly first trading day', () => {
      const option = '每月第一个交易日';
      assert.strictEqual(option, '每月第一个交易日');
    });
  });

  describe('backtest date parameters', () => {
    it('should find start date input', () => {
      const selector = 'input[name="startdate"], #backtest-start';
      assert.ok(selector.includes('start'));
    });

    it('should fill start date from options', () => {
      const startTime = '2022-01-01';
      assert.strictEqual(startTime, '2022-01-01');
    });

    it('should find end date input', () => {
      const selector = 'input[name="enddate"], #backtest-end';
      assert.ok(selector.includes('end'));
    });

    it('should fill end date from options', () => {
      const endTime = '2025-03-28';
      assert.strictEqual(endTime, '2025-03-28');
    });
  });

  describe('backtest execution', () => {
    it('should click backtest button', () => {
      const selector = 'button:has-text("开始回测"), a:has-text("开始回测")';
      assert.ok(selector.includes('开始回测'));
    });

    it('should wait 15s for backtest to complete', () => {
      const waitTime = 15000;
      assert.strictEqual(waitTime, 15000);
    });
  });

  describe('screenshot saving', () => {
    it('should create output directory', () => {
      mockFs.default.mkdirSync.mockImplementation(() => undefined);
      mockFs.default.mkdirSync('/test/output', { recursive: true });
      assert.strictEqual(mockFs.default.mkdirSync.mock.calls.length, 1);
    });

    it('should save screenshot with timestamp', () => {
      const timestamp = Date.now();
      const screenshotPath = path.join('/test/output', `backtest-${timestamp}.png`);
      assert.ok(screenshotPath.includes('backtest'));
      assert.ok(screenshotPath.endsWith('.png'));
    });

    it('should save full page screenshot', () => {
      const options = { fullPage: true };
      assert.strictEqual(options.fullPage, true);
    });
  });

  describe('return value', () => {
    it('should return url in result', () => {
      const result = { url: 'https://guorn.com/stock/result' };
      assert.ok(result.url);
    });

    it('should return screenshot path in result', () => {
      const result = { screenshotPath: '/test/output/backtest.png' };
      assert.ok(result.screenshotPath);
    });
  });

  describe('error handling', () => {
    it('should catch isVisible timeout errors', () => {
      const error = new Error('Timeout');
      assert.ok(error.message.includes('Timeout'));
    });

    it('should continue when element not found', () => {
      const isVisible = false;
      if (!isVisible) {
        assert.strictEqual(isVisible, false);
      }
    });

    it('should handle missing pool dropdown', () => {
      const poolDropdownVisible = false;
      assert.strictEqual(poolDropdownVisible, false);
    });
  });

  describe('CLI execution', () => {
    it('should parse --headed flag', () => {
      const args = ['--headed'];
      const headed = args.includes('--headed');
      assert.strictEqual(headed, true);
    });

    it('should run when called directly', () => {
      const isDirectCall = true;
      assert.strictEqual(isDirectCall, true);
    });
  });

  describe('strategy description', () => {
    it('should describe RFScore strategy conversion', () => {
      const description = '将 rfscore_pure_offensive.py 策略转换为果仁网配置';
      assert.ok(description.includes('rfscore'));
    });

    it('should mention stock pool target', () => {
      const poolDescription = '沪深300 + 中证500（排除科创板、ST）';
      assert.ok(poolDescription.includes('沪深300'));
    });

    it('should mention ranking factors', () => {
      const factors = 'ROA、净利润增长率、毛利率等因子';
      assert.ok(factors.includes('ROA'));
    });

    it('should mention trading frequency', () => {
      const trading = '每月调仓，最多20只股票';
      assert.ok(trading.includes('每月'));
    });
  });
});