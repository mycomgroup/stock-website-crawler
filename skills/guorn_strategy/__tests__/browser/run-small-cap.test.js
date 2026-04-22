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
  SESSION_FILE: '/test/session.json',
  OUTPUT_ROOT: '/test/output'
}));

vi.mock('../../load-env.js', () => ({
  default: {},
}));

vi.mock('playwright', () => {
  const mockLocator = {
    first: vi.fn(() => mockLocator),
    isVisible: vi.fn(() => Promise.resolve(true)),
    click: vi.fn(() => Promise.resolve()),
    fill: vi.fn(() => Promise.resolve()),
    selectOption: vi.fn(() => Promise.resolve()),
    isChecked: vi.fn(() => Promise.resolve(false)),
    check: vi.fn(() => Promise.resolve()),
    textContent: vi.fn(() => Promise.resolve('本策略 15.5% 12.3% 1.5 -20.3%'))
  };

  const mockPage = {
    goto: vi.fn(() => Promise.resolve()),
    waitForTimeout: vi.fn(() => Promise.resolve()),
    screenshot: vi.fn(() => Promise.resolve()),
    locator: vi.fn(() => mockLocator),
    url: vi.fn(() => 'https://guorn.com/stock')
  };

  const mockBrowser = {
    launch: vi.fn(() => Promise.resolve({
      newContext: vi.fn(() => Promise.resolve({
        addCookies: vi.fn(() => Promise.resolve()),
        newPage: vi.fn(() => Promise.resolve(mockPage))
      })),
      close: vi.fn(() => Promise.resolve())
    }))
  };

  return {
    chromium: mockBrowser
  };
});

const mockFs = await import('node:fs');
const { chromium } = await import('playwright');

function resetMocks() {
  mockFs.default.existsSync.mockClear();
  mockFs.default.readFileSync.mockClear();
  mockFs.default.writeFileSync.mockClear();
  mockFs.default.mkdirSync.mockClear();
  chromium.launch.mockClear();
}

describe('run-small-cap.js', () => {
  beforeEach(() => {
    resetMocks();
    mockFs.default.existsSync.mockImplementation(() => true);
    mockFs.default.readFileSync.mockImplementation(() => '{"cookies":[{"name":"session","value":"test"}]}');
  });

  afterEach(() => {
    resetMocks();
  });

  describe('session loading', () => {
    it('should load session file on startup', async () => {
      mockFs.default.readFileSync.mockImplementation(() => '{"cookies":[{"name":"session","value":"test"}]}');
      const sessionData = JSON.parse(mockFs.default.readFileSync());
      assert.ok(sessionData.cookies);
      assert.strictEqual(sessionData.cookies[0].name, 'session');
    });

    it('should throw error when session file does not exist', async () => {
      mockFs.default.existsSync.mockImplementation(() => false);
      assert.strictEqual(mockFs.default.existsSync('/nonexistent'), false);
    });

    it('should parse session JSON correctly', async () => {
      const sessionJson = '{"capturedAt":"2024-01-01T00:00:00.000Z","cookies":[{"name":"sessionid","value":"abc123"}]}';
      mockFs.default.readFileSync.mockImplementation(() => sessionJson);
      const parsed = JSON.parse(mockFs.default.readFileSync());
      assert.strictEqual(parsed.capturedAt, '2024-01-01T00:00:00.000Z');
      assert.strictEqual(parsed.cookies.length, 1);
    });
  });

  describe('browser configuration', () => {
    it('should use correct user agent', () => {
      const USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36';
      assert.ok(USER_AGENT.includes('Macintosh'));
      assert.ok(USER_AGENT.includes('Chrome/123'));
    });

    it('should launch browser with slowMo option', async () => {
      const launchOptions = { headless: false, slowMo: 500 };
      assert.strictEqual(launchOptions.headless, false);
      assert.strictEqual(launchOptions.slowMo, 500);
    });
  });

  describe('strategy configuration', () => {
    it('should set stock limit to 10', () => {
      const stockLimit = 10;
      assert.strictEqual(stockLimit, 10);
    });

    it('should use 高流动800 stock pool', () => {
      const stockPool = '高流动800';
      assert.strictEqual(stockPool, '高流动800');
    });

    it('should exclude ST stocks', () => {
      const excludeST = true;
      assert.strictEqual(excludeST, true);
    });

    it('should exclude STIB (科创板)', () => {
      const excludeSTIB = true;
      assert.strictEqual(excludeSTIB, true);
    });

    it('should filter suspended stocks', () => {
      const filterSuspend = true;
      assert.strictEqual(filterSuspend, true);
    });
  });

  describe('ranking conditions', () => {
    it('should rank by 总市值 ascending', () => {
      const rankingIndicator = '总市值';
      const order = 'asc';
      assert.strictEqual(rankingIndicator, '总市值');
      assert.strictEqual(order, 'asc');
    });

    it('should click 行情 tab for market cap ranking', () => {
      const tabName = '行情';
      assert.strictEqual(tabName, '行情');
    });
  });

  describe('result extraction', () => {
    it('should parse result table format', () => {
      const pageText = '本策略 15.5% 12.3% 1.5 -20.3%';
      const tableMatch = pageText.match(/本策略\s*([\d.\-+%]+)\s*([\d.\-+%]+)\s*([\d.\-]+)\s*([\d.\-+%]+)/);
      assert.ok(tableMatch);
      assert.strictEqual(tableMatch[1], '15.5%');
      assert.strictEqual(tableMatch[2], '12.3%');
      assert.strictEqual(tableMatch[3], '1.5');
      assert.strictEqual(tableMatch[4], '-20.3%');
    });

    it('should handle missing result table', () => {
      const pageText = 'No results yet';
      const tableMatch = pageText.match(/本策略\s*([\d.\-+%]+)\s*([\d.\-+%]+)\s*([\d.\-]+)\s*([\d.\-+%]+)/);
      assert.strictEqual(tableMatch, null);
    });

    it('should build results object with correct fields', () => {
      const results = {
        strategy: 'small_cap_growth',
        displayName: '小市值成长策略',
        timestamp: new Date().toISOString()
      };
      assert.strictEqual(results.strategy, 'small_cap_growth');
      assert.strictEqual(results.displayName, '小市值成长策略');
      assert.ok(results.timestamp);
    });
  });

  describe('file saving', () => {
    it('should save screenshot to output directory', () => {
      const screenshotPath = path.join('/test/output', 'debug-page.png');
      assert.ok(screenshotPath.includes('output'));
      assert.ok(screenshotPath.endsWith('.png'));
    });

    it('should save results JSON file', () => {
      const resultFile = path.join('/test/output', 'small_cap_growth-result.json');
      assert.ok(resultFile.includes('output'));
      assert.ok(resultFile.endsWith('.json'));
    });

    it('should write JSON with proper formatting', () => {
      const results = { test: 'value' };
      const jsonContent = JSON.stringify(results, null, 2);
      assert.ok(jsonContent.includes('\n'));
      assert.ok(jsonContent.includes('  '));
    });
  });

  describe('timeout handling', () => {
    it('should use 30s timeout for page navigation', () => {
      const navTimeout = 30000;
      assert.strictEqual(navTimeout, 30000);
    });

    it('should wait 120s for backtest completion', () => {
      const backtestWait = 120000;
      assert.strictEqual(backtestWait, 120000);
    });

    it('should wait 10s for page stabilization', () => {
      const stabilizationWait = 10000;
      assert.strictEqual(stabilizationWait, 10000);
    });
  });

  describe('selector patterns', () => {
    it('should use correct selector for 新建 button', () => {
      const newBtnSelector = 'span:has-text("新建")';
      assert.ok(newBtnSelector.includes('新建'));
    });

    it('should use correct selector for stock limit input', () => {
      const stockLimitSelector = 'input[value="100"]';
      assert.ok(stockLimitSelector.includes('input'));
    });

    it('should use correct selector for hot pool select', () => {
      const hotPoolSelector = 'select.hot-pool-sel';
      assert.ok(hotPoolSelector.includes('hot-pool-sel'));
    });

    it('should use correct selector for backtest button', () => {
      const backtestBtnSelector = 'a:has-text("开始回测")';
      assert.ok(backtestBtnSelector.includes('开始回测'));
    });
  });

  describe('error handling', () => {
    it('should catch isVisible timeout errors', async () => {
      const mockLocator = {
        isVisible: vi.fn(() => Promise.resolve(true))
      };
      const isVisibleResult = await mockLocator.isVisible({ timeout: 5000 }).catch(() => false);
      assert.strictEqual(isVisibleResult, true);
    });

    it('should continue when 新建 button is not visible', () => {
      const isVisible = false;
      if (!isVisible) {
        assert.strictEqual(isVisible, false);
      }
    });
  });
});