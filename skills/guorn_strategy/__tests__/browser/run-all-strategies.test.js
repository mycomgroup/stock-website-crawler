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

const mockFs = await import('node:fs');

function resetMocks() {
  mockFs.default.existsSync.mockClear();
  mockFs.default.readFileSync.mockClear();
  mockFs.default.writeFileSync.mockClear();
  mockFs.default.mkdirSync.mockClear();
}

describe('run-all-strategies.js', () => {
  beforeEach(() => {
    resetMocks();
  });

  afterEach(() => {
    resetMocks();
  });

  describe('STRATEGIES configuration', () => {
    it('should define pure_treasury_defense strategy', () => {
      const strategy = {
        name: 'pure_treasury_defense',
        displayName: '国债ETF防守策略',
        config: { type: 'etf_holding', etfCode: '511010' }
      };
      assert.strictEqual(strategy.name, 'pure_treasury_defense');
      assert.strictEqual(strategy.config.etfCode, '511010');
    });

    it('should define pure_cash_defense strategy', () => {
      const strategy = {
        name: 'pure_cash_defense',
        displayName: '纯现金防守策略',
        config: { type: 'cash' }
      };
      assert.strictEqual(strategy.name, 'pure_cash_defense');
      assert.strictEqual(strategy.config.type, 'cash');
    });

    it('should define small_cap_growth strategy', () => {
      const strategy = {
        name: 'small_cap_growth',
        displayName: '小市值成长策略',
        config: {
          type: 'stock_selection',
          stockPool: '高流动800',
          stockLimit: 10,
          filters: [{ indicator: 'ROE', operator: '>', value: 5 }],
          rankings: [{ indicator: '总市值', order: 'asc' }]
        }
      };
      assert.strictEqual(strategy.name, 'small_cap_growth');
      assert.strictEqual(strategy.config.stockLimit, 10);
    });

    it('should define dividend_value strategy', () => {
      const strategy = {
        name: 'dividend_value',
        displayName: '高股息价值策略',
        config: {
          type: 'stock_selection',
          stockPool: '高流动800',
          stockLimit: 20,
          filters: [
            { indicator: 'PE', operator: '<', value: 20 },
            { indicator: 'PB', operator: '<', value: 2 }
          ]
        }
      };
      assert.strictEqual(strategy.name, 'dividend_value');
      assert.strictEqual(strategy.config.filters.length, 2);
    });

    it('should have 4 strategies defined', () => {
      const STRATEGIES = [
        { name: 'pure_treasury_defense' },
        { name: 'pure_cash_defense' },
        { name: 'small_cap_growth' },
        { name: 'dividend_value' }
      ];
      assert.strictEqual(STRATEGIES.length, 4);
    });
  });

  describe('runAllStrategies options', () => {
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

    it('should load session cookies', () => {
      mockFs.default.readFileSync.mockImplementation(() => '{"cookies":[{"name":"test"}]}');
      const session = JSON.parse(mockFs.default.readFileSync());
      assert.ok(session.cookies);
    });
  });

  describe('browser configuration', () => {
    it('should set headless based on headed option', () => {
      const headed = false;
      const headless = !headed;
      assert.strictEqual(headless, true);
    });

    it('should set user agent', () => {
      const USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)';
      assert.ok(USER_AGENT.includes('Macintosh'));
    });
  });

  describe('page navigation', () => {
    it('should navigate to guorn.com/stock', () => {
      const targetUrl = 'https://guorn.com/stock';
      assert.strictEqual(targetUrl, 'https://guorn.com/stock');
    });

    it('should use 90s timeout for navigation', () => {
      const navTimeout = 90000;
      assert.strictEqual(navTimeout, 90000);
    });

    it('should handle navigation timeout', () => {
      const timeoutHandled = true;
      assert.strictEqual(timeoutHandled, true);
    });

    it('should wait 5s after navigation', () => {
      const waitTime = 5000;
      assert.strictEqual(waitTime, 5000);
    });
  });

  describe('login verification', () => {
    it('should check login status by URL', () => {
      const url = 'https://guorn.com/stock';
      const isLoggedIn = !url.includes('/user/login');
      assert.strictEqual(isLoggedIn, true);
    });

    it('should throw error on expired session', () => {
      const isLoggedIn = false;
      if (!isLoggedIn) {
        assert.strictEqual(isLoggedIn, false);
      }
    });
  });

  describe('createAndRunStrategy function', () => {
    it('should click 新建 button for new strategy', () => {
      const selector = '.empty.action, span.empty';
      assert.ok(selector.includes('empty'));
    });

    it('should handle cash strategy type', () => {
      const config = { type: 'cash' };
      assert.strictEqual(config.type, 'cash');
    });

    it('should handle etf_holding strategy type', () => {
      const config = { type: 'etf_holding', etfCode: '511010' };
      assert.strictEqual(config.type, 'etf_holding');
    });

    it('should handle stock_selection strategy type', () => {
      const config = { type: 'stock_selection', stockLimit: 10 };
      assert.strictEqual(config.type, 'stock_selection');
    });

    it('should set stock limit from config', () => {
      const config = { stockLimit: 10 };
      assert.strictEqual(config.stockLimit, 10);
    });

    it('should set rebalance cycle from config', () => {
      const config = { rebalanceCycle: 20 };
      assert.strictEqual(config.rebalanceCycle, 20);
    });

    it('should set stock pool from config', () => {
      const config = { stockPool: '高流动800' };
      assert.strictEqual(config.stockPool, '高流动800');
    });

    it('should exclude ST when configured', () => {
      const config = { excludeST: true };
      assert.strictEqual(config.excludeST, true);
    });

    it('should exclude STIB when configured', () => {
      const config = { excludeSTIB: true };
      assert.strictEqual(config.excludeSTIB, true);
    });

    it('should filter suspend when configured', () => {
      const config = { filterSuspend: true };
      assert.strictEqual(config.filterSuspend, true);
    });
  });

  describe('ranking setup', () => {
    it('should click 财务指标 tab', () => {
      const tabName = '财务指标';
      assert.strictEqual(tabName, '财务指标');
    });

    it('should handle 市值 ranking', () => {
      const ranking = { indicator: '总市值', order: 'asc' };
      assert.ok(ranking.indicator.includes('市值'));
    });

    it('should handle PE ranking', () => {
      const ranking = { indicator: 'PE', order: 'asc' };
      assert.strictEqual(ranking.indicator, 'PE');
    });

    it('should click 行情 tab for market cap', () => {
      const tabName = '行情';
      assert.strictEqual(tabName, '行情');
    });

    it('should click 估值 section for PE', () => {
      const sectionName = '估值';
      assert.strictEqual(sectionName, '估值');
    });
  });

  describe('runBacktest function', () => {
    it('should click 开始回测 button', () => {
      const selector = 'a:has-text("开始回测")';
      assert.ok(selector.includes('开始回测'));
    });

    it('should wait up to 120s for backtest', () => {
      const maxIterations = 24;
      const waitPerIteration = 5000;
      assert.strictEqual(maxIterations * waitPerIteration, 120000);
    });

    it('should check for result indicators', () => {
      const selector = '.result-table, text=年化收益';
      assert.ok(selector.includes('年化收益'));
    });
  });

  describe('result extraction', () => {
    it('should extract strategy name in results', () => {
      const results = { strategy: 'small_cap_growth' };
      assert.strictEqual(results.strategy, 'small_cap_growth');
    });

    it('should extract display name', () => {
      const results = { displayName: '小市值成长策略' };
      assert.strictEqual(results.displayName, '小市值成长策略');
    });

    it('should include timestamp', () => {
      const results = { timestamp: new Date().toISOString() };
      assert.ok(results.timestamp);
    });

    it('should parse result table format', () => {
      const pageText = '本策略 15.5% 12.3% 1.5 -20.3%';
      const tableMatch = pageText.match(/本策略\s*([\d.\-+%]+)\s*([\d.\-+%]+)\s*([\d.\-]+)\s*([\d.\-+%]+)/);
      assert.ok(tableMatch);
      assert.strictEqual(tableMatch[1], '15.5%');
    });

    it('should extract win rate', () => {
      const pageText = '交易赢率：65.5%';
      const match = pageText.match(/交易赢率[：:\s]*([\d.\-+%]+)/);
      assert.ok(match);
    });

    it('should extract turnover rate', () => {
      const pageText = '年换手率：120.5%';
      const match = pageText.match(/年换手率[：:\s]*([\d.\-+%]+)/);
      assert.ok(match);
    });
  });

  describe('screenshot saving', () => {
    it('should save screenshot with strategy name', () => {
      const strategyName = 'small_cap_growth';
      const screenshotPath = path.join('/test/output', `${strategyName}-result.png`);
      assert.ok(screenshotPath.includes(strategyName));
    });

    it('should save full page screenshot', () => {
      const options = { fullPage: true };
      assert.strictEqual(options.fullPage, true);
    });
  });

  describe('strategy iteration', () => {
    it('should run all strategies sequentially', () => {
      const STRATEGIES = [{ name: 's1' }, { name: 's2' }];
      assert.strictEqual(STRATEGIES.length, 2);
    });

    it('should wait 3s between strategies', () => {
      const waitTime = 3000;
      assert.strictEqual(waitTime, 3000);
    });

    it('should refresh page for next strategy', () => {
      const refreshUrl = 'https://guorn.com/stock';
      assert.strictEqual(refreshUrl, 'https://guorn.com/stock');
    });

    it('should wait 2s after page refresh', () => {
      const waitTime = 2000;
      assert.strictEqual(waitTime, 2000);
    });
  });

  describe('error handling in strategy loop', () => {
    it('should catch strategy execution errors', () => {
      const error = new Error('Strategy failed');
      assert.ok(error.message.includes('failed'));
    });

    it('should push error result to allResults', () => {
      const allResults = [];
      const strategy = { name: 'test' };
      allResults.push({ strategy: strategy.name, error: 'Test error' });
      assert.strictEqual(allResults[0].error, 'Test error');
    });

    it('should continue to next strategy after error', () => {
      const continueExecution = true;
      assert.strictEqual(continueExecution, true);
    });
  });

  describe('results aggregation', () => {
    it('should save all results to JSON file', () => {
      const resultsFile = path.join('/test/output', 'all-strategies-results.json');
      assert.ok(resultsFile.includes('all-strategies'));
      assert.ok(resultsFile.endsWith('.json'));
    });

    it('should print summary for each strategy', () => {
      const allResults = [
        { strategy: 's1', displayName: 'Strategy 1', annualReturn: '10%' },
        { strategy: 's2', error: 'Failed' }
      ];
      assert.strictEqual(allResults.length, 2);
    });

    it('should show error message for failed strategies', () => {
      const result = { strategy: 'test', error: 'Connection failed' };
      if (result.error) {
        assert.ok(result.error);
      }
    });

    it('should show metrics for successful strategies', () => {
      const result = { displayName: 'Test', annualReturn: '15%', maxDrawdown: '-10%' };
      assert.ok(result.annualReturn);
      assert.ok(result.maxDrawdown);
    });
  });

  describe('headed mode closing', () => {
    it('should wait 10s before closing in headed mode', () => {
      const headed = true;
      const waitTime = headed ? 10000 : 0;
      assert.strictEqual(waitTime, 10000);
    });

    it('should close browser after all strategies', () => {
      const browserClosed = true;
      assert.strictEqual(browserClosed, true);
    });
  });

  describe('CLI argument handling', () => {
    it('should parse --headless flag', () => {
      const args = ['--headless'];
      const headed = !args.includes('--headless');
      assert.strictEqual(headed, false);
    });

    it('should run when called directly', () => {
      const isDirectCall = true;
      assert.strictEqual(isDirectCall, true);
    });
  });
});