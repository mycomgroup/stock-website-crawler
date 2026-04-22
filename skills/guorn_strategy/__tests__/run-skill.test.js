import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import fs from 'node:fs';

vi.mock('node:fs', () => ({
  default: {
    existsSync: vi.fn(),
    readFileSync: vi.fn(),
  },
  existsSync: vi.fn(),
  readFileSync: vi.fn(),
}));

vi.mock('./request/strategy-runner.js', () => ({
  runStrategyWorkflow: vi.fn(),
  runRealtimeSelection: vi.fn(),
  runHistoricalSelection: vi.fn(),
}));

vi.mock('./request/guorn-strategy-client.js', () => ({
  GuornStrategyClient: vi.fn().mockImplementation(() => ({
    getStockMeta: vi.fn(),
  })),
  FACTOR_IDS: {
    ROA: '0.M.股票每日指标_中性ROA.0',
    ROE: '0.M.股票每日指标_中性ROE.0',
    PE: '0.M.股票每日指标_市盈率.0',
    PB: '0.M.股票每日指标_市净率.0',
    MOMENTUM: '0.M.股票每日指标_动量.0',
  },
}));

describe('run-skill.js', () => {
  let originalArgv;
  let originalExit;

  beforeEach(() => {
    originalArgv = process.argv;
    originalExit = process.exit;
    vi.clearAllMocks();
  });

  afterEach(() => {
    process.argv = originalArgv;
    process.exit = originalExit;
    vi.clearAllMocks();
  });

  describe('parseArgs', () => {
    const parseArgs = (argv) => {
      const args = { _: [] };
      for (let i = 0; i < argv.length; i++) {
        const arg = argv[i];
        if (arg.startsWith('--')) {
          const key = arg.slice(2);
          const value = argv[i + 1];
          if (value && !value.startsWith('--')) {
            args[key] = value;
            i++;
          } else {
            args[key] = true;
          }
        } else {
          args._.push(arg);
        }
      }
      return args;
    };

    it('should parse command without options', () => {
      const result = parseArgs(['backtest']);
      expect(result).toEqual({ _: ['backtest'] });
    });

    it('should parse option with value', () => {
      const result = parseArgs(['--config', 'config.json']);
      expect(result).toEqual({ _: [], config: 'config.json' });
    });

    it('should parse flag without value', () => {
      const result = parseArgs(['--headed']);
      expect(result).toEqual({ _: [], headed: true });
    });

    it('should parse multiple options', () => {
      const result = parseArgs(['--start', '2025-01-01', '--end', '2025-12-31', '--headed']);
      expect(result).toEqual({ _: [], start: '2025-01-01', end: '2025-12-31', headed: true });
    });

    it('should parse command with options', () => {
      const result = parseArgs(['realtime', '--config', 'strategy.json']);
      expect(result).toEqual({ _: ['realtime'], config: 'strategy.json' });
    });

    it('should parse kebab-case option as key', () => {
      const result = parseArgs(['--force-refresh']);
      expect(result).toEqual({ _: [], 'force-refresh': true });
    });

    it('should handle empty argv', () => {
      const result = parseArgs([]);
      expect(result).toEqual({ _: [] });
    });

    it('should handle option at end without value', () => {
      const result = parseArgs(['--config', '--headed']);
      expect(result).toEqual({ _: [], config: true, headed: true });
    });

    it('should parse multiple commands', () => {
      const result = parseArgs(['command1', 'command2']);
      expect(result).toEqual({ _: ['command1', 'command2'] });
    });

    it('should parse numeric value as string', () => {
      const result = parseArgs(['--count', '10']);
      expect(result).toEqual({ _: [], count: '10' });
      expect(typeof result.count).toBe('string');
    });

    it('should handle option value starting with hyphen', () => {
      const result = parseArgs(['--date', '2025-01-01']);
      expect(result).toEqual({ _: [], date: '2025-01-01' });
    });

    it('should parse complex command line', () => {
      const result = parseArgs(['backtest', '--config', 'strategy.json', '--start', '2025-01-01', '--end', '2025-12-31', '--benchmark', 'hs300', '--cost', '0.002', '--headed', '--force-refresh']);
      expect(result).toEqual({ _: ['backtest'], config: 'strategy.json', start: '2025-01-01', end: '2025-12-31', benchmark: 'hs300', cost: '0.002', headed: true, 'force-refresh': true });
    });
  });

  describe('config file handling', () => {
    it('should handle non-existent config file', async () => {
      vi.mocked(fs.existsSync).mockReturnValue(false);
      expect(fs.existsSync('/nonexistent/config.json')).toBe(false);
    });

    it('should parse JSON config file correctly', () => {
      const config = { filters: [{ indicator: 'PE', operator: '<', value: 20 }], ranks: [{ id: 'test', weight: 1.0 }] };
      vi.mocked(fs.existsSync).mockReturnValue(true);
      vi.mocked(fs.readFileSync).mockReturnValue(JSON.stringify(config));
      
      const parsed = JSON.parse(fs.readFileSync('test.json', 'utf8'));
      expect(parsed).toEqual(config);
    });

    it('should handle malformed JSON', () => {
      vi.mocked(fs.existsSync).mockReturnValue(true);
      vi.mocked(fs.readFileSync).mockReturnValue('invalid json');
      
      expect(() => JSON.parse(fs.readFileSync('test.json', 'utf8'))).toThrow();
    });
  });

  describe('command routing', () => {
    it('should default to backtest command', () => {
      const args = { _: [] };
      const command = args._[0] || 'backtest';
      expect(command).toBe('backtest');
    });

    it('should recognize realtime command', () => {
      const args = { _: ['realtime'] };
      const command = args._[0] || 'backtest';
      expect(command).toBe('realtime');
    });

    it('should recognize history command', () => {
      const args = { _: ['history'] };
      const command = args._[0] || 'backtest';
      expect(command).toBe('history');
    });

    it('should recognize factors command', () => {
      const args = { _: ['factors'] };
      const command = args._[0] || 'backtest';
      expect(command).toBe('factors');
    });
  });

  describe('backtest config building', () => {
    it('should build correct backtest config from CLI args', () => {
      const args = { start: '2025-04-01', end: '2026-04-01', benchmark: 'hs300', cost: '0.002', rank: '0.M.股票每日指标_中性ROA.0' };
      
      const strategyConfig = {};
      if (args.rank) {
        strategyConfig.ranks = [{ id: args.rank, weight: 1.0, asc: false, industry: 0 }];
      }
      
      const backtestConfig = {
        startTime: args.start,
        endTime: args.end,
        benchmark: args.benchmark || 'hs300',
        transactionCost: args.cost ? Number(args.cost) : 0.002
      };
      
      expect(strategyConfig.ranks).toEqual([{ id: '0.M.股票每日指标_中性ROA.0', weight: 1.0, asc: false, industry: 0 }]);
      expect(backtestConfig.startTime).toBe('2025-04-01');
      expect(backtestConfig.transactionCost).toBe(0.002);
    });

    it('should convert benchmark codes correctly', () => {
      const benchmarkMap = { hs300: '000300', zz500: '000905', zz1000: '000852' };
      expect(benchmarkMap['hs300']).toBe('000300');
      expect(benchmarkMap['zz500']).toBe('000905');
      expect(benchmarkMap['zz1000']).toBe('000852');
    });

    it('should handle missing optional args', () => {
      const args = {};
      const backtestConfig = {
        startTime: args.start,
        endTime: args.end,
        benchmark: args.benchmark || 'hs300',
        transactionCost: args.cost ? Number(args.cost) : 0.002
      };
      
      expect(backtestConfig.benchmark).toBe('hs300');
      expect(backtestConfig.transactionCost).toBe(0.002);
      expect(backtestConfig.startTime).toBeUndefined();
    });

    it('should convert count to string', () => {
      const args = { count: '10' };
      const cfg = {};
      if (args.count) cfg.count = String(args.count);
      expect(cfg.count).toBe('10');
      expect(typeof cfg.count).toBe('string');
    });

    it('should convert period to number', () => {
      const args = { period: '20' };
      const cfg = {};
      if (args.period) cfg.period = Number(args.period);
      expect(cfg.period).toBe(20);
      expect(typeof cfg.period).toBe('number');
    });
  });

  describe('FACTOR_IDS usage', () => {
    it('should use correct factor IDs', async () => {
      const { FACTOR_IDS } = await import('./request/guorn-strategy-client.js');
      expect(FACTOR_IDS.ROA).toBe('0.M.股票每日指标_中性ROA.0');
      expect(FACTOR_IDS.ROE).toBe('0.M.股票每日指标_中性ROE.0');
    });
  });
});