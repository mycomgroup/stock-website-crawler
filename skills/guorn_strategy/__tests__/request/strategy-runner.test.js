import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import fs from 'node:fs';
import path from 'node:path';

vi.mock('node:fs');
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

const mockLaunch = vi.fn();

vi.mock('playwright', () => ({
  chromium: {
    launch: mockLaunch,
  },
}));

vi.mock('../../request/guorn-strategy-client.js', () => ({
  GuornStrategyClient: vi.fn().mockImplementation(() => ({
    getUserProfile: vi.fn(),
    buildPostUrl: vi.fn((url) => url),
    request: vi.fn(),
    getStockMeta: vi.fn(),
  })),
}));

vi.mock('../../request/ensure-session.js', () => ({
  ensureGuornSession: vi.fn(),
}));

vi.mock('../../request/config-normalizer.js', () => ({
  normalizeConfig: vi.fn((config) => config),
}));

vi.mock('../../paths.js', () => ({
  DATA_ROOT: '/test/data',
  OUTPUT_ROOT: '/test/output',
  SESSION_FILE: '/test/sessions/guorn.json',
}));

vi.mock('../../load-env.js', () => {});

describe('strategy-runner.js', () => {
  let mockBrowser;
  let mockContext;
  let mockPage;
  let consoleLogSpy;

  beforeEach(() => {
    vi.clearAllMocks();
    
    mockPage = {
      goto: vi.fn(),
      waitForTimeout: vi.fn(),
      waitForFunction: vi.fn(),
      evaluate: vi.fn(),
      screenshot: vi.fn(),
    };
    
    mockContext = {
      newPage: vi.fn(() => mockPage),
      addCookies: vi.fn(),
      cookies: vi.fn(() => []),
    };
    
    mockBrowser = {
      newContext: vi.fn(() => mockContext),
      close: vi.fn(),
    };
    
    mockLaunch.mockResolvedValue(mockBrowser);
    
    vi.mocked(fs.existsSync).mockReturnValue(true);
    vi.mocked(fs.readFileSync).mockReturnValue(JSON.stringify({
      cookies: [{ name: '_xsrf', value: 'test_token' }]
    }));
    vi.mocked(fs.mkdirSync).mockImplementation(() => {});
    vi.mocked(fs.writeFileSync).mockImplementation(() => {});
    
    consoleLogSpy = vi.spyOn(console, 'log').mockImplementation(() => {});
  });

  afterEach(() => {
    consoleLogSpy.mockRestore();
  });

  describe('runBacktestViaBrowser', () => {
    it('should run backtest and return result', async () => {
      const { runBacktestViaBrowser } = await import('../../request/strategy-runner.js');
      
      mockPage.waitForFunction.mockResolvedValue();
      
      let evaluateCallCount = 0;
      mockPage.evaluate.mockImplementation((fn, ...args) => {
        evaluateCallCount++;
        if (evaluateCallCount === 1) {
          return Promise.resolve();
        }
        if (evaluateCallCount === 2) {
          return Promise.resolve(true);
        }
        return Promise.resolve({ status: 'ok', data: {} });
      });
      
      vi.mocked(fs.readFileSync).mockReturnValue(JSON.stringify({
        cookies: [{ name: '_xsrf', value: 'token', expires: null }]
      }));
      
      const result = await runBacktestViaBrowser({}, '/test/session.json');
      
      expect(mockBrowser.close).toHaveBeenCalled();
    });

    it('should throw timeout error after 90 seconds', async () => {
      const { runBacktestViaBrowser } = await import('../../request/strategy-runner.js');
      
      mockPage.evaluate.mockResolvedValue(false);
      
      vi.mocked(fs.readFileSync).mockReturnValue(JSON.stringify({
        cookies: [{ name: '_xsrf', value: 'token' }]
      }));
      
      await expect(runBacktestViaBrowser({}, '/test/session.json')).rejects.toThrow('Backtest timed out');
    });

    it('should handle cookies with null expires', async () => {
      const { runBacktestViaBrowser } = await import('../../request/strategy-runner.js');
      
      vi.mocked(fs.readFileSync).mockReturnValue(JSON.stringify({
        cookies: [
          { name: '_xsrf', value: 'token', expires: null },
          { name: 'session', value: 'value', expires: { _type: 'Date' } }
        ]
      }));
      
      mockPage.evaluate.mockResolvedValue({ status: 'ok' });
      
      await runBacktestViaBrowser({}, '/test/session.json');
      
      expect(mockContext.addCookies).toHaveBeenCalled();
    });

    it('should convert date format in payload', async () => {
      const { runBacktestViaBrowser } = await import('../../request/strategy-runner.js');
      
      const config = {
        start: '2024-01-01',
        end: '2024-12-31',
      };
      
      vi.mocked(fs.readFileSync).mockReturnValue(JSON.stringify({
        cookies: [{ name: '_xsrf', value: 'token' }]
      }));
      
      mockPage.evaluate.mockResolvedValue({ status: 'ok' });
      
      await runBacktestViaBrowser(config, '/test/session.json');
      
      expect(mockPage.evaluate).toHaveBeenCalled();
    });
  });

  describe('runStrategyWorkflow', () => {
    it('should execute full workflow', async () => {
      const { runStrategyWorkflow } = await import('../../request/strategy-runner.js');
      const { ensureGuornSession } = await import('../../request/ensure-session.js');
      const { GuornStrategyClient } = await import('../../request/guorn-strategy-client.js');
      
      vi.mocked(ensureGuornSession).mockResolvedValue({ sessionFile: '/test/session.json' });
      
      const mockClient = {
        getUserProfile: vi.fn().mockResolvedValue({ data: { username: 'test', level: 1 } }),
      };
      vi.mocked(GuornStrategyClient).mockImplementation(() => mockClient);
      
      vi.mocked(fs.readFileSync).mockReturnValue(JSON.stringify({
        cookies: [{ name: '_xsrf', value: 'token' }]
      }));
      
      mockPage.evaluate.mockResolvedValue({ status: 'ok', data: { trade_summary: {} } });
      
      const result = await runStrategyWorkflow({
        strategyConfig: { filters: [] },
        backtestConfig: { startTime: '2024-01-01', endTime: '2024-12-31' },
      });
      
      expect(ensureGuornSession).toHaveBeenCalled();
      expect(mockClient.getUserProfile).toHaveBeenCalled();
    });

    it('should throw error when backtest fails', async () => {
      const { runStrategyWorkflow } = await import('../../request/strategy-runner.js');
      const { ensureGuornSession } = await import('../../request/ensure-session.js');
      
      vi.mocked(ensureGuornSession).mockResolvedValue({ sessionFile: '/test/session.json' });
      
      vi.mocked(fs.readFileSync).mockReturnValue(JSON.stringify({
        cookies: [{ name: '_xsrf', value: 'token' }]
      }));
      
      mockPage.evaluate.mockResolvedValue({ status: 'error', message: 'Failed' });
      
      await expect(runStrategyWorkflow({})).rejects.toThrow('Backtest failed');
    });

    it('should handle benchmark conversion', async () => {
      const { runStrategyWorkflow } = await import('../../request/strategy-runner.js');
      const { ensureGuornSession } = await import('../../request/ensure-session.js');
      
      vi.mocked(ensureGuornSession).mockResolvedValue({ sessionFile: '/test/session.json' });
      
      vi.mocked(fs.readFileSync).mockReturnValue(JSON.stringify({
        cookies: [{ name: '_xsrf', value: 'token' }]
      }));
      
      mockPage.evaluate.mockResolvedValue({ status: 'ok', data: {} });
      
      await runStrategyWorkflow({
        backtestConfig: { benchmark: 'zz500' }
      });
      
      expect(mockPage.evaluate).toHaveBeenCalled();
    });

    it('should handle missing profile data', async () => {
      const { runStrategyWorkflow } = await import('../../request/strategy-runner.js');
      const { ensureGuornSession } = await import('../../request/ensure-session.js');
      const { GuornStrategyClient } = await import('../../request/guorn-strategy-client.js');
      
      vi.mocked(ensureGuornSession).mockResolvedValue({ sessionFile: '/test/session.json' });
      
      const mockClient = {
        getUserProfile: vi.fn().mockResolvedValue({ status: 'ok' }),
      };
      vi.mocked(GuornStrategyClient).mockImplementation(() => mockClient);
      
      vi.mocked(fs.readFileSync).mockReturnValue(JSON.stringify({
        cookies: [{ name: '_xsrf', value: 'token' }]
      }));
      
      mockPage.evaluate.mockResolvedValue({ status: 'ok', data: {} });
      
      const result = await runStrategyWorkflow({});
      
      expect(result.status).toBe('ok');
    });

    it('should return summary with trade_summary data', async () => {
      const { runStrategyWorkflow } = await import('../../request/strategy-runner.js');
      const { ensureGuornSession } = await import('../../request/ensure-session.js');
      
      vi.mocked(ensureGuornSession).mockResolvedValue({ sessionFile: '/test/session.json' });
      
      vi.mocked(fs.readFileSync).mockReturnValue(JSON.stringify({
        cookies: [{ name: '_xsrf', value: 'token' }]
      }));
      
      const tradeSummary = {
        winsorize_annual: 0.15,
        win_ratio: 0.6,
        year_information_ratio: 1.2,
        maxdrop_day: 30,
        avg_holding_days: 10,
        sell_count: 100,
        annual_turnover_rate: 2.5,
      };
      
      mockPage.evaluate.mockResolvedValue({ 
        status: 'ok', 
        data: { trade_summary: tradeSummary } 
      });
      
      const result = await runStrategyWorkflow({});
      
      expect(result.summary.annualReturn).toBe(0.15);
      expect(result.summary.winRate).toBe(0.6);
    });
  });

  describe('runRealtimeSelection', () => {
    it('should run realtime selection', async () => {
      const { runRealtimeSelection } = await import('../../request/strategy-runner.js');
      const { ensureGuornSession } = await import('../../request/ensure-session.js');
      const { GuornStrategyClient } = await import('../../request/guorn-strategy-client.js');
      
      vi.mocked(ensureGuornSession).mockResolvedValue({ sessionFile: '/test/session.json' });
      
      const mockClient = {
        buildPostUrl: vi.fn((url) => url),
        request: vi.fn().mockResolvedValue({ status: 'ok', data: { stocks: [] } }),
      };
      vi.mocked(GuornStrategyClient).mockImplementation(() => mockClient);
      
      const result = await runRealtimeSelection({
        strategyConfig: { filters: [] }
      });
      
      expect(result.stocks).toEqual([]);
    });

    it('should throw error when realtime selection fails', async () => {
      const { runRealtimeSelection } = await import('../../request/strategy-runner.js');
      const { ensureGuornSession } = await import('../../request/ensure-session.js');
      const { GuornStrategyClient } = await import('../../request/guorn-strategy-client.js');
      
      vi.mocked(ensureGuornSession).mockResolvedValue({ sessionFile: '/test/session.json' });
      
      const mockClient = {
        buildPostUrl: vi.fn((url) => url),
        request: vi.fn().mockResolvedValue({ status: 'error' }),
      };
      vi.mocked(GuornStrategyClient).mockImplementation(() => mockClient);
      
      await expect(runRealtimeSelection({})).rejects.toThrow('Realtime selection failed');
    });

    it('should save result to file', async () => {
      const { runRealtimeSelection } = await import('../../request/strategy-runner.js');
      const { ensureGuornSession } = await import('../../request/ensure-session.js');
      const { GuornStrategyClient } = await import('../../request/guorn-strategy-client.js');
      
      vi.mocked(ensureGuornSession).mockResolvedValue({ sessionFile: '/test/session.json' });
      
      const mockClient = {
        buildPostUrl: vi.fn((url) => url),
        request: vi.fn().mockResolvedValue({ status: 'ok', data: { stocks: [{ symbol: 'AAPL' }] } }),
      };
      vi.mocked(GuornStrategyClient).mockImplementation(() => mockClient);
      
      const result = await runRealtimeSelection({});
      
      expect(fs.writeFileSync).toHaveBeenCalled();
      expect(result.resultPath).toBeDefined();
    });
  });

  describe('runHistoricalSelection', () => {
    it('should run historical selection', async () => {
      const { runHistoricalSelection } = await import('../../request/strategy-runner.js');
      const { ensureGuornSession } = await import('../../request/ensure-session.js');
      const { GuornStrategyClient } = await import('../../request/guorn-strategy-client.js');
      
      vi.mocked(ensureGuornSession).mockResolvedValue({ sessionFile: '/test/session.json' });
      
      const mockClient = {
        buildPostUrl: vi.fn((url) => url),
        request: vi.fn().mockResolvedValue({ status: 'ok', data: { stocks: [] } }),
      };
      vi.mocked(GuornStrategyClient).mockImplementation(() => mockClient);
      
      const result = await runHistoricalSelection({
        strategyConfig: {},
        date: '2024-01-01'
      });
      
      expect(result.date).toBe('2024-01-01');
      expect(result.stocks).toEqual([]);
    });

    it('should throw error when historical selection fails', async () => {
      const { runHistoricalSelection } = await import('../../request/strategy-runner.js');
      const { ensureGuornSession } = await import('../../request/ensure-session.js');
      const { GuornStrategyClient } = await import('../../request/guorn-strategy-client.js');
      
      vi.mocked(ensureGuornSession).mockResolvedValue({ sessionFile: '/test/session.json' });
      
      const mockClient = {
        buildPostUrl: vi.fn((url) => url),
        request: vi.fn().mockResolvedValue({ status: 'error' }),
      };
      vi.mocked(GuornStrategyClient).mockImplementation(() => mockClient);
      
      await expect(runHistoricalSelection({ date: '2024-01-01' })).rejects.toThrow('Historical selection failed');
    });

    it('should handle missing date', async () => {
      const { runHistoricalSelection } = await import('../../request/strategy-runner.js');
      const { ensureGuornSession } = await import('../../request/ensure-session.js');
      const { GuornStrategyClient } = await import('../../request/guorn-strategy-client.js');
      
      vi.mocked(ensureGuornSession).mockResolvedValue({ sessionFile: '/test/session.json' });
      
      const mockClient = {
        buildPostUrl: vi.fn((url) => url),
        request: vi.fn().mockResolvedValue({ status: 'ok', data: { stocks: [] } }),
      };
      vi.mocked(GuornStrategyClient).mockImplementation(() => mockClient);
      
      const result = await runHistoricalSelection({ strategyConfig: {} });
      
      expect(result.stocks).toEqual([]);
    });
  });
});