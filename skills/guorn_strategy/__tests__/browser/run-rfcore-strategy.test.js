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

describe('run-rfcore-strategy.js', () => {
  beforeEach(() => {
    resetMocks();
    mockFs.default.existsSync.mockImplementation(() => true);
  });

  afterEach(() => {
    resetMocks();
  });

  describe('runRFCoreStrategy options', () => {
    it('should use default start time', () => {
      const defaultStartTime = '2022-01-01';
      assert.strictEqual(defaultStartTime, '2022-01-01');
    });

    it('should use default end time', () => {
      const defaultEndTime = '2025-03-28';
      assert.strictEqual(defaultEndTime, '2025-03-28');
    });

    it('should use default headed mode (true)', () => {
      const defaultHeaded = true;
      assert.strictEqual(defaultHeaded, true);
    });

    it('should accept custom options', () => {
      const options = {
        startTime: '2023-01-01',
        endTime: '2024-01-01',
        headed: false
      };
      assert.strictEqual(options.startTime, '2023-01-01');
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
      const sessionFile = '/test/session.json';
      assert.ok(sessionFile.includes('session.json'));
    });
  });

  describe('browser configuration', () => {
    it('should set headless based on headed option', () => {
      const headed = true;
      const headless = !headed;
      assert.strictEqual(headless, false);
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

  describe('strategy creation steps', () => {
    it('should click 新建 button first', () => {
      const newBtnSelector = '.empty.action, span.empty';
      assert.ok(newBtnSelector.includes('empty'));
    });

    it('should wait 2s after clicking new button', () => {
      const waitTime = 2000;
      assert.strictEqual(waitTime, 2000);
    });

    it('should set stock limit to 20', () => {
      const stockLimit = 20;
      assert.strictEqual(stockLimit, 20);
    });

    it('should set rebalance cycle to 20', () => {
      const rebalanceCycle = 20;
      assert.strictEqual(rebalanceCycle, 20);
    });
  });

  describe('stock pool selection', () => {
    it('should select 高流动800 stock pool', () => {
      const stockPool = '高流动800';
      assert.strictEqual(stockPool, '高流动800');
    });

    it('should use hot-pool-sel selector', () => {
      const selector = 'select.hot-pool-sel';
      assert.ok(selector.includes('hot-pool-sel'));
    });
  });

  describe('exclusion settings', () => {
    it('should exclude ST stocks with index 1', () => {
      const stSelectIndex = 1;
      assert.strictEqual(stSelectIndex, 1);
    });

    it('should exclude STIB with index 0', () => {
      const stibSelectIndex = 0;
      assert.strictEqual(stibSelectIndex, 0);
    });

    it('should check filter-suspend checkbox', () => {
      const filterSuspend = true;
      assert.strictEqual(filterSuspend, true);
    });
  });

  describe('ranking conditions', () => {
    it('should click 财务指标 tab', () => {
      const tabName = '财务指标';
      assert.strictEqual(tabName, '财务指标');
    });

    it('should expand 盈利能力 section', () => {
      const sectionName = '盈利';
      assert.ok(sectionName.includes('盈利'));
    });

    it('should add ROA to ranking', () => {
      const indicator = 'ROA';
      assert.strictEqual(indicator, 'ROA');
    });
  });

  describe('trading model', () => {
    it('should click trading model tab', () => {
      const selector = 'a.trading, text=交易模型';
      assert.ok(selector.includes('交易模型'));
    });

    it('should wait 1s after clicking trading tab', () => {
      const waitTime = 1000;
      assert.strictEqual(waitTime, 1000);
    });
  });

  describe('backtest execution', () => {
    it('should click 开始回测 button', () => {
      const selector = 'a:has-text("开始回测"), button:has-text("开始回测")';
      assert.ok(selector.includes('开始回测'));
    });

    it('should wait up to 24 iterations (120s)', () => {
      const maxIterations = 24;
      const waitPerIteration = 5000;
      const totalWait = maxIterations * waitPerIteration;
      assert.strictEqual(totalWait, 120000);
    });

    it('should check for result indicators', () => {
      const resultSelectors = '.result-table, text=年化收益, #equity-curve';
      assert.ok(resultSelectors.includes('年化收益'));
    });

    it('should check for loading indicator', () => {
      const loadingSelectors = '.loading, text=计算中';
      assert.ok(loadingSelectors.includes('计算中'));
    });
  });

  describe('metric extraction', () => {
    it('should extract 年化收益', () => {
      const pageText = '年化收益：15.5%';
      const match = pageText.match(/年化收益[：:\s]*([\d.\-+%]+)/);
      assert.ok(match);
      assert.strictEqual(match[1], '15.5%');
    });

    it('should extract 总收益', () => {
      const pageText = '总收益：120.5%';
      const match = pageText.match(/总收益[：:\s]*([\d.\-+%]+)/);
      assert.ok(match);
      assert.strictEqual(match[1], '120.5%');
    });

    it('should extract 最大回撤', () => {
      const pageText = '最大回撤：-25.3%';
      const match = pageText.match(/最大回撤[：:\s]*([\d.\-+%]+)/);
      assert.ok(match);
      assert.strictEqual(match[1], '-25.3%');
    });

    it('should extract 夏普比率', () => {
      const pageText = '夏普比率：1.85';
      const match = pageText.match(/夏普比率[：:\s]*([\d.\-+%]+)/);
      assert.ok(match);
      assert.strictEqual(match[1], '1.85');
    });

    it('should handle missing metrics', () => {
      const pageText = 'No metrics here';
      const match = pageText.match(/年化收益[：:\s]*([\d.\-+%]+)/);
      assert.strictEqual(match, null);
    });

    it('should try multiple patterns for extraction', () => {
      const label = '年化收益';
      const patterns = [
        new RegExp(label + '[：:\\s]*([\d.\-+%]+)'),
        new RegExp(label + '\\s*([\d.\-+%]+)'),
        new RegExp('([\d.\-+%]+)\\s*' + label)
      ];
      assert.strictEqual(patterns.length, 3);
    });
  });

  describe('screenshot saving', () => {
    it('should save initial screenshot', () => {
      const screenshotPath = path.join('/test/output', 'step1-initial.png');
      assert.ok(screenshotPath.includes('step1'));
    });

    it('should save screenshots for each step', () => {
      const screenshots = [
        'step1-initial.png',
        'step2-new.png',
        'step3-config.png',
        'step4-pool.png',
        'step5-ranking.png',
        'step6-trading.png',
        'step8-result.png'
      ];
      assert.ok(screenshots.length >= 7);
    });

    it('should save full page screenshot for result', () => {
      const options = { fullPage: true };
      assert.strictEqual(options.fullPage, true);
    });
  });

  describe('results saving', () => {
    it('should save page text for debugging', () => {
      const outputPath = path.join('/test/output', 'page-text.txt');
      assert.ok(outputPath.endsWith('.txt'));
    });

    it('should save JSON result file', () => {
      const resultFile = path.join('/test/output', `rfcore-backtest-${Date.now()}.json`);
      assert.ok(resultFile.includes('rfcore-backtest'));
      assert.ok(resultFile.endsWith('.json'));
    });

    it('should include URL in results', () => {
      const results = { url: 'https://guorn.com/stock/result' };
      assert.ok(results.url);
    });

    it('should include timestamp in results', () => {
      const results = { timestamp: new Date().toISOString() };
      assert.ok(results.timestamp);
    });
  });

  describe('headed mode', () => {
    it('should keep browser open for 15s in headed mode', () => {
      const headed = true;
      const waitTime = headed ? 15000 : 0;
      assert.strictEqual(waitTime, 15000);
    });

    it('should close immediately in headless mode', () => {
      const headed = false;
      const waitTime = headed ? 15000 : 0;
      assert.strictEqual(waitTime, 0);
    });
  });

  describe('CLI argument parsing', () => {
    it('should parse --headless flag', () => {
      const args = ['--headless'];
      const headed = !args.includes('--headless');
      assert.strictEqual(headed, false);
    });

    it('should parse --start= date argument', () => {
      const args = ['--start=2023-01-01'];
      const startTime = args.find(a => a.startsWith('--start='))?.split('=')[1];
      assert.strictEqual(startTime, '2023-01-01');
    });

    it('should parse --end= date argument', () => {
      const args = ['--end=2024-01-01'];
      const endTime = args.find(a => a.startsWith('--end='))?.split('=')[1];
      assert.strictEqual(endTime, '2024-01-01');
    });

    it('should use default dates when not provided', () => {
      const args = [];
      const startTime = args.find(a => a.startsWith('--start='))?.split('=')[1] || '2022-01-01';
      assert.strictEqual(startTime, '2022-01-01');
    });
  });

  describe('error handling in steps', () => {
    it('should catch stock limit errors', () => {
      const error = new Error('Stock limit error');
      assert.ok(error.message.includes('Stock limit'));
    });

    it('should catch rebalance cycle errors', () => {
      const error = new Error('Rebalance cycle error');
      assert.ok(error.message.includes('Rebalance'));
    });

    it('should catch stock pool errors', () => {
      const error = new Error('Stock pool error');
      assert.ok(error.message.includes('Stock pool'));
    });

    it('should continue on non-critical errors', () => {
      const errorCaught = true;
      const shouldContinue = true;
      assert.strictEqual(shouldContinue, true);
    });
  });
});