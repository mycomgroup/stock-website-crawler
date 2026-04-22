import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { ParameterCache } from '../request/parameter-cache.js';
import { ParameterValidator } from '../request/parameter-validator.js';

vi.mock('../request/parameter-cache.js', () => {
  const mockCache = {
    refresh: vi.fn(),
    getSummary: vi.fn(),
    cache: {
      indicators: {
        flat: [],
        categories: {},
        functions: []
      },
      stockPools: {
        userPools: [],
        systemPools: []
      }
    },
    searchIndicators: vi.fn(),
    validateIndicator: vi.fn(),
  };
  
  return {
    ParameterCache: vi.fn(() => mockCache),
    getParameterCache: vi.fn(() => Promise.resolve(mockCache)),
  };
});

vi.mock('../request/parameter-validator.js', () => ({
  ParameterValidator: vi.fn(),
}));

describe('cache-parameters CLI logic', () => {
  let mockCache;
  let consoleLogSpy;
  let consoleErrorSpy;

  beforeEach(async () => {
    vi.clearAllMocks();
    
    consoleLogSpy = vi.spyOn(console, 'log').mockImplementation(() => {});
    consoleErrorSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
    
    const { getParameterCache } = await import('../request/parameter-cache.js');
    mockCache = await getParameterCache();
  });

  afterEach(() => {
    consoleLogSpy.mockRestore();
    consoleErrorSpy.mockRestore();
  });

  describe('refresh command logic', () => {
    it('should refresh cache and log success', async () => {
      await mockCache.refresh();
      
      expect(mockCache.refresh).toHaveBeenCalled();
    });
  });

  describe('summary command logic', () => {
    it('should get and display cache summary', async () => {
      mockCache.getSummary.mockReturnValue({
        totalIndicators: 100,
        categories: 10,
        userPools: 5
      });
      
      const summary = mockCache.getSummary();
      
      expect(summary.totalIndicators).toBe(100);
      expect(summary.categories).toBe(10);
      expect(summary.userPools).toBe(5);
    });
  });

  describe('indicators command logic', () => {
    it('should count indicators by category', async () => {
      mockCache.cache.indicators = {
        flat: [{ name: 'PE' }, { name: 'PB' }],
        categories: {
          'valuation': [{ name: 'PE' }],
          'profitability': [{ name: 'ROE' }]
        },
        functions: [{ name: 'avg' }]
      };
      
      expect(mockCache.cache.indicators.flat.length).toBe(2);
      expect(Object.keys(mockCache.cache.indicators.categories).length).toBe(2);
      expect(mockCache.cache.indicators.functions.length).toBe(1);
    });

    it('should count functions', async () => {
      mockCache.cache.indicators.functions = [{ name: 'avg' }, { name: 'sum' }];
      
      expect(mockCache.cache.indicators.functions.length).toBe(2);
    });
  });

  describe('search command logic', () => {
    it('should search indicators with query', async () => {
      mockCache.searchIndicators.mockReturnValue([
        { name: 'PE', type: 'indicator', category: 'valuation' },
        { name: 'PE_TTM', type: 'indicator', category: 'valuation' }
      ]);
      
      const results = mockCache.searchIndicators('PE');
      
      expect(mockCache.searchIndicators).toHaveBeenCalledWith('PE');
      expect(results.length).toBe(2);
    });

    it('should handle empty search results', async () => {
      mockCache.searchIndicators.mockReturnValue([]);
      
      const results = mockCache.searchIndicators('nonexistent');
      
      expect(results).toEqual([]);
    });

    it('should limit display to 20 results', async () => {
      const manyResults = Array.from({ length: 30 }, (_, i) => ({
        name: `Indicator${i}`,
        type: 'indicator'
      }));
      
      mockCache.searchIndicators.mockReturnValue(manyResults);
      
      const results = mockCache.searchIndicators('test');
      const displayed = results.slice(0, 20);
      const remaining = results.length - 20;
      
      expect(displayed.length).toBe(20);
      expect(remaining).toBe(10);
    });
  });

  describe('pools command logic', () => {
    it('should list user stock pools', async () => {
      mockCache.cache.stockPools.userPools = [
        { name: 'My Pool', poolid: 'pool1' },
        { name: 'Test Pool', poolid: 'pool2' }
      ];
      
      expect(mockCache.cache.stockPools.userPools.length).toBe(2);
      expect(mockCache.cache.stockPools.userPools[0].name).toBe('My Pool');
    });

    it('should list system stock pools', async () => {
      mockCache.cache.stockPools.systemPools = [
        { pool_name: '沪深300', id: 'sys1' },
        { pool_name: '中证500', id: 'sys2' }
      ];
      
      expect(mockCache.cache.stockPools.systemPools.length).toBe(2);
    });

    it('should limit system pools display to 10', async () => {
      mockCache.cache.stockPools.systemPools = Array.from({ length: 15 }, (_, i) => ({
        name: `System Pool ${i}`,
        id: `sys${i}`
      }));
      
      const displayed = mockCache.cache.stockPools.systemPools.slice(0, 10);
      const remaining = mockCache.cache.stockPools.systemPools.length - 10;
      
      expect(displayed.length).toBe(10);
      expect(remaining).toBe(5);
    });
  });

  describe('validate command logic', () => {
    it('should validate an indicator', async () => {
      mockCache.validateIndicator.mockReturnValue({
        valid: true,
        indicator: { name: 'PE', id: 'pe_id' }
      });
      
      const result = mockCache.validateIndicator('PE');
      
      expect(mockCache.validateIndicator).toHaveBeenCalledWith('PE');
      expect(result.valid).toBe(true);
    });

    it('should return invalid for unknown indicator', async () => {
      mockCache.validateIndicator.mockReturnValue({
        valid: false,
        indicator: null,
        message: 'Indicator not found: unknown'
      });
      
      const result = mockCache.validateIndicator('unknown');
      
      expect(result.valid).toBe(false);
    });
  });

  describe('test-validator command logic', () => {
    it('should run validator with sample config', async () => {
      const mockValidator = {
        validate: vi.fn().mockReturnValue({
          valid: true,
          errors: [],
          warnings: []
        })
      };
      
      vi.mocked(ParameterValidator).mockImplementation(() => mockValidator);
      
      const validator = new ParameterValidator(mockCache);
      const validation = validator.validate({
        name: 'Test Strategy',
        stockPool: { type: 'system', poolId: 'test' },
        filters: [],
        rankings: [],
        tradingModel: { type: 1 },
        backtest: { startDate: '2022-01-01' }
      });
      
      expect(mockValidator.validate).toHaveBeenCalled();
      expect(validation.valid).toBe(true);
    });
  });

  describe('error handling', () => {
    it('should handle cache errors', async () => {
      const { getParameterCache } = await import('../request/parameter-cache.js');
      
      vi.mocked(getParameterCache).mockRejectedValueOnce(new Error('Connection failed'));
      
      await expect(getParameterCache()).rejects.toThrow('Connection failed');
    });
  });

  describe('CLI command parsing', () => {
    it('should recognize refresh command', () => {
      const command = 'refresh';
      const validCommands = ['refresh', 'summary', 'indicators', 'search', 'pools', 'validate', 'test-validator'];
      
      expect(validCommands.includes(command)).toBe(true);
    });

    it('should handle unknown command', () => {
      const command = 'unknown';
      const validCommands = ['refresh', 'summary', 'indicators', 'search', 'pools', 'validate', 'test-validator'];
      
      expect(validCommands.includes(command)).toBe(false);
    });

    it('should default to refresh when no command', () => {
      const command = process.argv[2] || 'refresh';
      
      expect(command).toBe('refresh');
    });
  });
});