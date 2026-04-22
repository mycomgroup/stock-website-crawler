import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import fs from 'node:fs';
import path from 'node:path';

vi.mock('node:fs');
vi.mock('node:path', () => ({
  ...vi.importActual('node:path'),
  basename: vi.fn((p, ext) => {
    const name = p.split('/').pop();
    return ext ? name.replace(ext, '') : name;
  }),
  extname: vi.fn((p) => {
    const match = p.match(/\.[^.]+$/);
    return match ? match[0] : '';
  })
}));

vi.mock('../load-env.js', () => {});
vi.mock('../paths.js', () => ({
  OUTPUT_ROOT: '/tmp/thsquant-test-output',
  SESSION_FILE: '/tmp/thsquant-test-session.json'
}));

const mockClient = {
  checkLogin: vi.fn(),
  createStrategy: vi.fn(),
  getStrategyInfo: vi.fn(),
  saveStrategy: vi.fn(),
  runBacktest: vi.fn(),
  waitForBacktest: vi.fn(),
  getFullReport: vi.fn(),
  writeArtifact: vi.fn()
};

vi.mock('../request/thsquant-client.js', () => ({
  THSQuantClient: vi.fn(() => mockClient)
}));

const mockWithAutoRelogin = vi.fn((credentials, fn) => fn([]));
vi.mock('../browser/session-manager.js', () => ({
  withAutoRelogin: mockWithAutoRelogin
}));

let runStrategyWorkflow;

beforeAll(async () => {
  ({ runStrategyWorkflow } = await import('../request/strategy-runner.js'));
});

beforeEach(() => {
  vi.clearAllMocks();
  fs.existsSync.mockReturnValue(true);
  fs.readFileSync.mockReturnValue('print("hello")');
  fs.mkdirSync.mockReturnValue();
  fs.writeFileSync.mockReturnValue();

  mockClient.checkLogin.mockResolvedValue({ logged: true, userId: 'user-123' });
  mockClient.createStrategy.mockResolvedValue({ success: true, algoId: 'new-algo-123' });
  mockClient.getStrategyInfo.mockResolvedValue({ algo_name: 'Existing Strategy' });
  mockClient.saveStrategy.mockResolvedValue({ success: true, message: 'Saved' });
  mockClient.runBacktest.mockResolvedValue({ backtestId: 'backtest-456' });
  mockClient.waitForBacktest.mockResolvedValue({ success: true });
  mockClient.getFullReport.mockResolvedValue({
    detail: { performance: { yield: 0.15, annual_yield: 0.12, max_drawdown: 0.08 } },
    performance: { sharpe_ratio: 1.5 },
    tradeLog: [{ id: 1 }],
    backtestLog: [{ id: 1 }],
    dailyGains: [],
    specificInfo: {}
  });
  mockClient.writeArtifact.mockReturnValue('/tmp/output/result.json');

  process.env.THSQUANT_USERNAME = 'testuser';
  process.env.THSQUANT_PASSWORD = 'testpass';

  vi.spyOn(Date, 'now').mockReturnValue(1700000000000);
});

afterEach(() => {
  vi.restoreAllMocks();
  delete process.env.THSQUANT_USERNAME;
  delete process.env.THSQUANT_PASSWORD;
});

describe('runStrategyWorkflow', () => {
  describe('file validation', () => {
    it('throws error when codeFilePath is not provided', async () => {
      await expect(runStrategyWorkflow({})).rejects.toThrow('Strategy file not found');
    });

    it('throws error when file does not exist', async () => {
      fs.existsSync.mockReturnValue(false);

      await expect(
        runStrategyWorkflow({ codeFilePath: '/path/to/nonexistent.py' })
      ).rejects.toThrow('Strategy file not found: /path/to/nonexistent.py');
    });
  });

  describe('strategy name generation', () => {
    it('generates name from strategyName parameter', async () => {
      await runStrategyWorkflow({
        codeFilePath: '/test/strategy.py',
        strategyName: 'my-strategy',
        beginDate: '2023-01-01',
        endDate: '2023-12-31'
      });

      expect(mockClient.createStrategy).toHaveBeenCalled();
      const strategyName = mockClient.createStrategy.mock.calls[0][0];

      expect(strategyName).toContain('my-strategy');
    });

    it('generates name from filename when strategyName not provided', async () => {
      await runStrategyWorkflow({
        codeFilePath: '/test/myfile.py',
        beginDate: '2023-01-01',
        endDate: '2023-12-31'
      });

      const strategyName = mockClient.createStrategy.mock.calls[0][0];
      expect(strategyName).toContain('myfile');
    });
  });

  describe('create new strategy', () => {
    it('creates new strategy by default', async () => {
      const result = await runStrategyWorkflow({
        codeFilePath: '/test/strategy.py'
      });

      expect(mockClient.createStrategy).toHaveBeenCalled();
      expect(mockClient.getStrategyInfo).not.toHaveBeenCalled();
      expect(result.algoId).toBe('new-algo-123');
    });

    it('throws when strategy creation fails', async () => {
      mockClient.createStrategy.mockResolvedValue({
        success: false,
        message: 'Strategy name already exists'
      });

      await expect(
        runStrategyWorkflow({ codeFilePath: '/test/strategy.py' })
      ).rejects.toThrow('Failed to create strategy');
    });
  });

  describe('update existing strategy', () => {
    it('updates existing strategy when algoId provided and createNew is false', async () => {
      const result = await runStrategyWorkflow({
        codeFilePath: '/test/strategy.py',
        algoId: 'existing-algo-456',
        createNew: false
      });

      expect(mockClient.createStrategy).not.toHaveBeenCalled();
      expect(mockClient.getStrategyInfo).toHaveBeenCalledWith('existing-algo-456');
      expect(mockClient.saveStrategy).toHaveBeenCalled();
      expect(result.algoId).toBe('existing-algo-456');
    });
  });

  describe('backtest configuration', () => {
    it('uses default backtest configuration', async () => {
      await runStrategyWorkflow({
        codeFilePath: '/test/strategy.py'
      });

      expect(mockClient.runBacktest).toHaveBeenCalledWith(
        'new-algo-123',
        expect.objectContaining({
          beginDate: '2023-01-01',
          endDate: '2024-12-31',
          capitalBase: '100000',
          frequency: 'DAILY',
          benchmark: '000300.SH'
        })
      );
    });

    it('uses custom backtest configuration', async () => {
      await runStrategyWorkflow({
        codeFilePath: '/test/strategy.py',
        beginDate: '2022-01-01',
        endDate: '2023-12-31',
        capitalBase: '500000',
        frequency: 'MINUTE',
        benchmark: '000016.SH'
      });

      expect(mockClient.runBacktest).toHaveBeenCalledWith(
        'new-algo-123',
        expect.objectContaining({
          beginDate: '2022-01-01',
          endDate: '2023-12-31',
          capitalBase: '500000'
        })
      );
    });
  });

  describe('login check', () => {
    it('throws when not logged in', async () => {
      mockClient.checkLogin.mockResolvedValue({ logged: false, userId: null });

      await expect(
        runStrategyWorkflow({ codeFilePath: '/test/strategy.py' })
      ).rejects.toThrow('Not logged in');
    });
  });

  describe('backtest execution', () => {
    it('starts backtest and gets backtestId', async () => {
      const result = await runStrategyWorkflow({
        codeFilePath: '/test/strategy.py'
      });

      expect(mockClient.runBacktest).toHaveBeenCalled();
      expect(result.backtestId).toBe('backtest-456');
    });

    it('throws on backtest failure', async () => {
      mockClient.waitForBacktest.mockResolvedValue({
        success: false,
        error: 'Backtest timeout'
      });

      await expect(
        runStrategyWorkflow({ codeFilePath: '/test/strategy.py' })
      ).rejects.toThrow('Backtest failed');
    });
  });

  describe('result handling', () => {
    it('fetches full report after backtest', async () => {
      await runStrategyWorkflow({
        codeFilePath: '/test/strategy.py'
      });

      expect(mockClient.getFullReport).toHaveBeenCalledWith('backtest-456');
    });

    it('writes artifact with all data', async () => {
      await runStrategyWorkflow({
        codeFilePath: '/test/strategy.py'
      });

      expect(mockClient.writeArtifact).toHaveBeenCalled();
      const writeCall = mockClient.writeArtifact.mock.calls[0];
      expect(writeCall[1]).toHaveProperty('summary');
    });

    it('generates correct summary', async () => {
      mockClient.getFullReport.mockResolvedValue({
        detail: {
          performance: {
            yield: 0.25,
            annual_yield: 0.15,
            benchmark_yield: 0.10,
            max_drawdown: 0.12,
            sharpe_ratio: 1.8
          }
        },
        performance: { sharpe_ratio: 1.9 },
        tradeLog: [{ id: 1 }, { id: 2 }],
        backtestLog: [{ id: 1 }]
      });

      await runStrategyWorkflow({
        codeFilePath: '/test/strategy.py',
        beginDate: '2023-01-01',
        endDate: '2023-12-31',
        capitalBase: '500000'
      });

      const writeCall = mockClient.writeArtifact.mock.calls[0];
      const summary = writeCall[1].summary;

      expect(summary.backtestId).toBe('backtest-456');
      expect(summary.period).toBe('2023-01-01 ~ 2023-12-31');
      expect(summary.capitalBase).toBe(500000);
      expect(summary.totalReturn).toBe(0.25);
    });
  });

  describe('credentials', () => {
    it('passes credentials from environment', async () => {
      await runStrategyWorkflow({
        codeFilePath: '/test/strategy.py'
      });

      expect(mockWithAutoRelogin).toHaveBeenCalledWith(
        { username: 'testuser', password: 'testpass' },
        expect.any(Function)
      );
    });
  });

  describe('return value', () => {
    it('returns complete result object', async () => {
      const result = await runStrategyWorkflow({
        codeFilePath: '/test/strategy.py',
        strategyName: 'test-strategy',
        beginDate: '2023-01-01',
        endDate: '2023-12-31'
      });

      expect(result).toHaveProperty('backtestId');
      expect(result).toHaveProperty('algoId');
      expect(result).toHaveProperty('resultPath');
      expect(result).toHaveProperty('summary');
    });
  });
});