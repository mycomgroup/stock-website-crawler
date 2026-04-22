import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import fs from 'node:fs';
import path from 'node:path';

vi.mock('node:fs');
vi.mock('node:path', async (importOriginal) => {
  const actual = await importOriginal()
  return {
    ...actual,
    join: vi.fn((...args) => args.join('/')),
  }
});

vi.mock('../paths.js', () => ({
  DATA_ROOT: '/test/data',
}));

vi.mock('../../request/guorn-strategy-client.js', () => ({
  GuornStrategyClient: vi.fn().mockImplementation(() => ({
    getStockMeta: vi.fn(),
    getStockPoolList: vi.fn(),
    getHotPoolList: vi.fn(),
    getUserProfile: vi.fn(),
    request: vi.fn()
  }))
}));

describe('parameter-cache.js', () => {
  let cache;
  let mockClient;
  let consoleLogSpy;
  let consoleWarnSpy;
  let consoleErrorSpy;

  beforeEach(async () => {
    vi.clearAllMocks();
    vi.useFakeTimers();
    
    consoleLogSpy = vi.spyOn(console, 'log').mockImplementation(() => {});
    consoleWarnSpy = vi.spyOn(console, 'warn').mockImplementation(() => {});
    consoleErrorSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
    
    vi.mocked(fs.existsSync).mockReturnValue(false);
    vi.mocked(fs.readFileSync).mockReturnValue('');
    vi.mocked(fs.mkdirSync).mockImplementation(() => {});
    vi.mocked(fs.writeFileSync).mockImplementation(() => {});
    
    const { ParameterCache } = await import('../../request/parameter-cache.js');
    mockClient = {
      getStockMeta: vi.fn().mockResolvedValue({
        data: {
          function: { measures: [{ name: 'func_group', values: [{ name: 'func1', expr: 'expr1' }] }] },
          measure: { category1: [{ name: 'ind1', expr: 'expr_ind1' }] }
        }
      }),
      getStockPoolList: vi.fn().mockResolvedValue({
        data: { pool_list: [{ id: 'pool1', name: 'Pool One' }] }
      }),
      getHotPoolList: vi.fn().mockResolvedValue({
        data: { hot_pool_list: [{ id: 'hotpool1', name: 'Hot Pool' }] }
      }),
      getUserProfile: vi.fn().mockResolvedValue({
        data: { name: 'Test User' }
      }),
      request: vi.fn().mockResolvedValue({
        data: { privilege: 'test' }
      })
    };
    
    cache = new ParameterCache({ client: mockClient });
  });

  afterEach(() => {
    vi.useRealTimers();
    consoleLogSpy.mockRestore();
    consoleWarnSpy.mockRestore();
    consoleErrorSpy.mockRestore();
  });

  describe('ParameterCache constructor', () => {
    it('should initialize with default client', async () => {
      const { ParameterCache } = await import('../../request/parameter-cache.js');
      const cache = new ParameterCache();
      
      expect(cache.client).toBeDefined();
      expect(cache.cacheFile).toBeDefined();
      expect(cache.cache).toBeNull();
    });

    it('should use provided client and cacheFile', async () => {
      const { ParameterCache } = await import('../../request/parameter-cache.js');
      const customCacheFile = '/custom/cache.json';
      const cache = new ParameterCache({
        client: mockClient,
        cacheFile: customCacheFile
      });
      
      expect(cache.client).toBe(mockClient);
      expect(cache.cacheFile).toBe(customCacheFile);
    });
  });

  describe('load', () => {
    it('should return cached data if cache is fresh', async () => {
      vi.mocked(fs.existsSync).mockReturnValue(true);
      vi.mocked(fs.readFileSync).mockReturnValue(JSON.stringify({
        timestamp: new Date(Date.now() - 1000).toISOString(),
        indicators: { flat: [] },
        stockPools: { userPools: [], systemPools: [] }
      }));
      
      const result = await cache.load();
      
      expect(result).toBeDefined();
      expect(mockClient.getStockMeta).not.toHaveBeenCalled();
    });

    it('should refresh cache if expired', async () => {
      vi.mocked(fs.existsSync).mockReturnValue(true);
      const expiredTime = Date.now() - (25 * 60 * 60 * 1000);
      vi.mocked(fs.readFileSync).mockReturnValue(JSON.stringify({
        timestamp: new Date(expiredTime).toISOString(),
        indicators: { flat: [] }
      }));
      
      await cache.load();
      
      expect(mockClient.getStockMeta).toHaveBeenCalled();
    });

    it('should refresh cache if file does not exist', async () => {
      vi.mocked(fs.existsSync).mockReturnValue(false);
      
      await cache.load();
      
      expect(mockClient.getStockMeta).toHaveBeenCalled();
    });

    it('should handle corrupted cache file', async () => {
      vi.mocked(fs.existsSync).mockReturnValue(true);
      vi.mocked(fs.readFileSync).mockReturnValue('invalid json');
      
      await cache.load();
      
      expect(mockClient.getStockMeta).toHaveBeenCalled();
      expect(consoleWarnSpy).toHaveBeenCalled();
    });

    it('should log cache age on successful load', async () => {
      vi.mocked(fs.existsSync).mockReturnValue(true);
      const ageMinutes = 30;
      vi.mocked(fs.readFileSync).mockReturnValue(JSON.stringify({
        timestamp: new Date(Date.now() - (ageMinutes * 60 * 1000)).toISOString(),
        indicators: { flat: [] }
      }));
      
      await cache.load();
      
      expect(consoleLogSpy).toHaveBeenCalledWith(expect.stringContaining('minutes old'));
    });
  });

  describe('refresh', () => {
    it('should fetch all required data', async () => {
      await cache.refresh();
      
      expect(mockClient.getStockMeta).toHaveBeenCalledWith('stock');
      expect(mockClient.getStockPoolList).toHaveBeenCalledWith('stock');
      expect(mockClient.getHotPoolList).toHaveBeenCalledWith('stock');
      expect(mockClient.getUserProfile).toHaveBeenCalled();
      expect(mockClient.request).toHaveBeenCalledWith('/user/privilege?filename=stockScreen&op=Show');
    });

    it('should build cache object with all sections', async () => {
      const result = await cache.refresh();
      
      expect(result.timestamp).toBeDefined();
      expect(result.indicators).toBeDefined();
      expect(result.stockPools).toBeDefined();
      expect(result.profile).toBeDefined();
      expect(result.privilege).toBeDefined();
      expect(result.tradingModels).toBeDefined();
      expect(result.benchmarks).toBeDefined();
      expect(result.transactionCosts).toBeDefined();
    });

    it('should save cache to file', async () => {
      await cache.refresh();
      
      expect(fs.mkdirSync).toHaveBeenCalled();
      expect(fs.writeFileSync).toHaveBeenCalled();
    });

    it('should handle refresh error', async () => {
      mockClient.getStockMeta.mockRejectedValue(new Error('Network error'));
      
      await expect(cache.refresh()).rejects.toThrow('Network error');
      expect(consoleErrorSpy).toHaveBeenCalled();
    });

    it('should include default trading models', async () => {
      const result = await cache.refresh();
      
      expect(result.tradingModels).toEqual([
        { id: 1, name: '模型Ⅰ--定期轮动' },
        { id: 2, name: '模型Ⅱ--条件触发' }
      ]);
    });

    it('should include default benchmarks', async () => {
      const result = await cache.refresh();
      
      expect(result.benchmarks).toContain('沪深300');
      expect(result.benchmarks).toContain('中证500');
      expect(result.benchmarks).toContain('中证800');
    });

    it('should include transaction costs', async () => {
      const result = await cache.refresh();
      
      expect(result.transactionCosts).toBeDefined();
      expect(result.transactionCosts.length).toBeGreaterThan(0);
      expect(result.transactionCosts[0]).toHaveProperty('value');
      expect(result.transactionCosts[0]).toHaveProperty('label');
    });
  });

  describe('parseIndicators', () => {
    it('should parse function measures', async () => {
      const data = {
        function: {
          measures: [
            {
              name: 'group1',
              values: [
                { name: 'func1', expr: 'expr1', desc: 'desc1' },
                { name: 'func2', expr: 'expr2' }
              ]
            }
          ]
        }
      };
      
      const result = cache.parseIndicators(data);
      
      expect(result.functions.length).toBe(2);
      expect(result.functions[0].type).toBe('function');
      expect(result.functions[0].group).toBe('group1');
    });

    it('should parse measure categories', async () => {
      const data = {
        measure: {
          category1: [
            { name: 'ind1', expr: 'expr1', desc: 'desc1' }
          ],
          category2: [
            { name: 'ind2', expr: 'expr2' }
          ]
        }
      };
      
      const result = cache.parseIndicators(data);
      
      expect(result.categories.category1).toBeDefined();
      expect(result.categories.category2).toBeDefined();
      expect(result.flat.length).toBe(2);
    });

    it('should handle missing data', () => {
      const result = cache.parseIndicators(null);
      
      expect(result).toEqual({
        functions: [],
        categories: {},
        flat: []
      });
    });

    it('should handle empty data', () => {
      const result = cache.parseIndicators({});
      
      expect(result.functions).toEqual([]);
      expect(result.categories).toEqual({});
    });

    it('should use default desc if not provided', () => {
      const data = {
        function: {
          measures: [{
            name: 'group',
            values: [{ name: 'func', expr: 'expr' }]
          }]
        }
      };
      
      const result = cache.parseIndicators(data);
      
      expect(result.functions[0].desc).toBe('');
    });
  });

  describe('parseStockPools', () => {
    it('should parse user and system pools', () => {
      const poolsResponse = {
        data: {
          pool_list: [
            { id: 'pool1', name: 'User Pool 1' },
            { id: 'pool2', name: 'User Pool 2' }
          ]
        }
      };
      const hotPoolsResponse = {
        data: {
          hot_pool_list: [
            { id: 'hot1', name: 'Hot Pool 1' }
          ]
        }
      };
      
      const result = cache.parseStockPools([poolsResponse, hotPoolsResponse]);
      
      expect(result.userPools.length).toBe(2);
      expect(result.systemPools.length).toBe(1);
    });

    it('should handle missing pool_list', () => {
      const result = cache.parseStockPools([
        { data: {} },
        { data: {} }
      ]);
      
      expect(result.userPools).toEqual([]);
      expect(result.systemPools).toEqual([]);
    });

    it('should handle null data', () => {
      const result = cache.parseStockPools([
        { data: null },
        { data: null }
      ]);
      
      expect(result.userPools).toEqual([]);
      expect(result.systemPools).toEqual([]);
    });
  });

  describe('getIndicator', () => {
    beforeEach(async () => {
      cache.cache = {
        indicators: {
          flat: [
            { name: '市盈率', expr: '0.M.股票每日指标_市盈率.0' },
            { name: '市净率', expr: '0.M.股票每日指标_市净率.0' }
          ]
        }
      };
    });

    it('should find indicator by name', () => {
      const result = cache.getIndicator('市盈率');
      
      expect(result).toBeDefined();
      expect(result.name).toBe('市盈率');
    });

    it('should find indicator by expr', () => {
      const result = cache.getIndicator('0.M.股票每日指标_市盈率.0');
      
      expect(result).toBeDefined();
    });

    it('should return null if not found', () => {
      const result = cache.getIndicator('unknown');
      
      expect(result).toBeFalsy();
    });

    it('should return null if cache is null', () => {
      cache.cache = null;
      
      const result = cache.getIndicator('市盈率');
      
      expect(result).toBeFalsy();
    });
  });

  describe('resolveId', () => {
    beforeEach(async () => {
      await cache.refresh();
      vi.mocked(fs.existsSync).mockReturnValue(true);
      vi.mocked(fs.readFileSync).mockReturnValue(JSON.stringify({
        indicators: [
          { name: '市盈率', id: '0.M.股票每日指标_市盈率.0', middle_name: '股票每日指标_市盈率' },
          { name: '市净率', id: '0.M.股票每日指标_市净率.0', middle_name: '股票每日指标_市净率' },
          { name: '净资产收益率', id: '0.M.股票每日指标_净资产收益率.0', middle_name: '股票每日指标_净资产收益率' }
        ]
      }));
      cache.mappingData = null;
    });

    it('should return raw ID unchanged', () => {
      const result = cache.resolveId('0.M.股票每日指标_测试.0');
      
      expect(result).toBe('0.M.股票每日指标_测试.0');
    });

    it('should return D. prefixed ID unchanged', () => {
      const result = cache.resolveId('0.D.测试指标.0');
      
      expect(result).toBe('0.D.测试指标.0');
    });

    it('should map English name to Chinese', async () => {
      vi.mocked(fs.readFileSync).mockReturnValue(JSON.stringify({
        indicators: [
          { name: '市盈率', id: '0.M.股票每日指标_市盈率.0' }
        ]
      }));
      
      const result = cache.resolveId('pe_ttm');
      
      expect(result).toBe('0.M.股票每日指标_市盈率.0');
    });

    it('should map lowercase English name', async () => {
      vi.mocked(fs.readFileSync).mockReturnValue(JSON.stringify({
        indicators: [
          { name: '市盈率', id: '0.M.股票每日指标_市盈率.0' }
        ]
      }));
      
      const result = cache.resolveId('PE');
      
      expect(result).toBe('0.M.股票每日指标_市盈率.0');
    });

    it('should handle null/undefined input', () => {
      expect(cache.resolveId(null)).toBeNull();
      expect(cache.resolveId(undefined)).toBeNull();
      expect(cache.resolveId('')).toBeNull();
    });

    it('should resolve via mapping file', async () => {
      vi.mocked(fs.existsSync).mockReturnValue(true);
      vi.mocked(fs.readFileSync).mockReturnValue(JSON.stringify({
        indicators: [
          { name: '测试指标', id: '0.M.测试指标.0', middle_name: '测试_指标' }
        ]
      }));
      cache.mappingData = null;
      
      const result = cache.resolveId('测试指标');
      
      expect(result).toBe('0.M.测试指标.0');
    });

    it('should resolve via middle_name', async () => {
      vi.mocked(fs.readFileSync).mockReturnValue(JSON.stringify({
        indicators: [
          { name: '测试指标', id: '0.M.测试指标.0', middle_name: '股票每日指标_测试' }
        ]
      }));
      cache.mappingData = null;
      
      const result = cache.resolveId('股票每日指标_测试');
      
      expect(result).toBe('0.M.测试指标.0');
    });

    it('should handle synonym mapping (PE -> 市盈率)', async () => {
      vi.mocked(fs.readFileSync).mockReturnValue(JSON.stringify({
        indicators: [
          { name: '市盈率', id: '0.M.股票每日指标_市盈率.0' }
        ]
      }));
      cache.mappingData = null;
      
      const result = cache.resolveId('PE');
      
      expect(result).toBe('0.M.股票每日指标_市盈率.0');
    });

    it('should fallback to cache.indicators', () => {
      cache.cache = {
        indicators: {
          flat: [{ name: 'fallback', expr: 'fallback_expr' }]
        }
      };
      
      const result = cache.resolveId('fallback');
      
      expect(result).toBe('fallback_expr');
    });

    it('should return original name if not resolvable', () => {
      cache.cache = { indicators: { flat: [] } };
      cache.mappingData = { indicators: [] };
      
      const result = cache.resolveId('unknown_indicator');
      
      expect(result).toBe('unknown_indicator');
    });

    it('should load mapping file only once', async () => {
      vi.mocked(fs.existsSync).mockReturnValue(true);
      vi.mocked(fs.readFileSync).mockReturnValue(JSON.stringify({ indicators: [] }));
      cache.mappingData = null;
      
      await cache.resolveId('test1');
      await cache.resolveId('test2');
      
      const readCalls = vi.mocked(fs.readFileSync).mock.calls.filter(
        call => call[0].includes('indicator_mapping.json')
      );
      expect(readCalls.length).toBe(1);
    });

    it('should handle missing mapping file gracefully', async () => {
      vi.mocked(fs.existsSync).mockReturnValue(false);
      cache.mappingData = null;
      cache.cache = {
        indicators: {
          flat: [{ name: 'cached', expr: 'cached_expr' }]
        }
      };
      
      const result = cache.resolveId('cached');
      
      expect(consoleWarnSpy).not.toHaveBeenCalled();
      expect(result).toBe('cached_expr');
    });
  });

  describe('resolvePoolId', () => {
    beforeEach(() => {
      cache.cache = {
        stockPools: {
          userPools: [{ id: '1.P.pool1', name: 'User Pool' }],
          systemPools: [{ id: '1.P.hotpool1', name: 'Hot Pool' }]
        }
      };
    });

    it('should return pool ID unchanged if already prefixed', () => {
      const result = cache.resolvePoolId('1.P.pool123');
      
      expect(result).toBe('1.P.pool123');
    });

    it('should resolve pool name to ID', () => {
      const result = cache.resolvePoolId('User Pool');
      
      expect(result).toBe('1.P.pool1');
    });

    it('should search both user and system pools', () => {
      const result = cache.resolvePoolId('Hot Pool');
      
      expect(result).toBe('1.P.hotpool1');
    });

    it('should return original name if not found', () => {
      const result = cache.resolvePoolId('Unknown Pool');
      
      expect(result).toBe('Unknown Pool');
    });

    it('should handle null/undefined input', () => {
      expect(cache.resolvePoolId(null)).toBeNull();
      expect(cache.resolvePoolId(undefined)).toBeUndefined();
    });

    it('should handle missing cache', () => {
      cache.cache = null;
      
      const result = cache.resolvePoolId('User Pool');
      
      expect(result).toBe('User Pool');
    });
  });

  describe('getIndicatorsByCategory', () => {
    beforeEach(() => {
      cache.cache = {
        indicators: {
          categories: {
            valuation: [{ name: 'PE' }, { name: 'PB' }],
            growth: [{ name: 'RevenueGrowth' }]
          }
        }
      };
    });

    it('should return indicators for category', () => {
      const result = cache.getIndicatorsByCategory('valuation');
      
      expect(result.length).toBe(2);
    });

    it('should return empty array for unknown category', () => {
      const result = cache.getIndicatorsByCategory('unknown');
      
      expect(result).toEqual([]);
    });

    it('should return empty array if cache is null', () => {
      cache.cache = null;
      
      const result = cache.getIndicatorsByCategory('valuation');
      
      expect(result).toEqual([]);
    });
  });

  describe('getStockPool', () => {
    beforeEach(() => {
      cache.cache = {
        stockPools: {
          userPools: [{ id: 'pool1', poolid: 'poolid1', name: 'Pool One' }],
          systemPools: [{ id: 'hotpool1', name: 'Hot Pool' }]
        }
      };
    });

    it('should find pool by id', () => {
      const result = cache.getStockPool('pool1');
      
      expect(result).toBeDefined();
      expect(result.name).toBe('Pool One');
    });

    it('should find pool by poolid', () => {
      const result = cache.getStockPool('poolid1');
      
      expect(result).toBeDefined();
    });

    it('should search both user and system pools', () => {
      const result = cache.getStockPool('hotpool1');
      
      expect(result).toBeDefined();
    });

    it('should return null if not found', () => {
      const result = cache.getStockPool('unknown');
      
      expect(result).toBeFalsy();
    });

    it('should return null if cache is null', () => {
      cache.cache = null;
      
      const result = cache.getStockPool('pool1');
      
      expect(result).toBeFalsy();
    });
  });

  describe('validateIndicator', () => {
    beforeEach(() => {
      cache.cache = {
        indicators: {
          flat: [{ name: 'PE', expr: 'pe_expr' }]
        }
      };
    });

    it('should return valid result for existing indicator', () => {
      const result = cache.validateIndicator('PE');
      
      expect(result.valid).toBe(true);
      expect(result.indicator).toBeDefined();
      expect(result.message).toContain('Found indicator');
    });

    it('should return invalid result for unknown indicator', () => {
      const result = cache.validateIndicator('Unknown');
      
      expect(result.valid).toBe(false);
      expect(result.indicator).toBeFalsy();
      expect(result.message).toContain('not found');
    });
  });

  describe('searchIndicators', () => {
    beforeEach(() => {
      cache.cache = {
        indicators: {
          flat: [
            { name: '市盈率', expr: 'pe_expr', desc: 'price earnings ratio' },
            { name: '市净率', expr: 'pb_expr', desc: 'price book ratio' },
            { name: '动量', expr: 'momentum', desc: 'momentum indicator' }
          ]
        }
      };
    });

    it('should search by name', () => {
      const result = cache.searchIndicators('市盈');
      
      expect(result.length).toBe(1);
      expect(result[0].name).toBe('市盈率');
    });

    it('should search by expr', () => {
      const result = cache.searchIndicators('pe_expr');
      
      expect(result.length).toBe(1);
    });

    it('should search by desc', () => {
      const result = cache.searchIndicators('ratio');
      
      expect(result.length).toBe(2);
    });

    it('should be case-insensitive', () => {
      const result = cache.searchIndicators('RATIO');
      
      expect(result.length).toBe(2);
    });

    it('should return empty array if cache is null', () => {
      cache.cache = null;
      
      const result = cache.searchIndicators('test');
      
      expect(result).toEqual([]);
    });

    it('should handle indicators without desc', () => {
      cache.cache = {
        indicators: {
          flat: [
            { name: 'test', expr: 'test_expr' }
          ]
        }
      };
      
      const result = cache.searchIndicators('test');
      
      expect(result.length).toBe(1);
    });
  });

  describe('getSummary', () => {
    beforeEach(() => {
      cache.cache = {
        timestamp: '2024-01-01',
        indicators: {
          flat: [{ name: 'ind1' }, { name: 'ind2' }],
          functions: [{ name: 'func1' }],
          categories: { cat1: [], cat2: [] }
        },
        stockPools: {
          userPools: [{ id: 'pool1' }],
          systemPools: [{ id: 'hot1' }, { id: 'hot2' }]
        },
        profile: { name: 'Test User' }
      };
    });

    it('should return summary with all fields', () => {
      const result = cache.getSummary();
      
      expect(result.timestamp).toBe('2024-01-01');
      expect(result.totalIndicators).toBe(2);
      expect(result.functionCount).toBe(1);
      expect(result.categories).toEqual(['cat1', 'cat2']);
      expect(result.userPools).toBe(1);
      expect(result.systemPools).toBe(2);
      expect(result.userName).toBe('Test User');
    });

    it('should handle missing profile name', () => {
      cache.cache.profile = {};
      
      const result = cache.getSummary();
      
      expect(result.userName).toBe('Unknown');
    });

    it('should return null if cache is null', () => {
      cache.cache = null;
      
      const result = cache.getSummary();
      
      expect(result).toBeFalsy();
    });
  });

  describe('getParameterCache', () => {
    it('should create and load cache', async () => {
      vi.mocked(fs.existsSync).mockReturnValue(true);
      vi.mocked(fs.readFileSync).mockReturnValue(JSON.stringify({
        timestamp: new Date().toISOString(),
        indicators: { flat: [] }
      }));
      
      const { getParameterCache } = await import('../../request/parameter-cache.js');
      const result = await getParameterCache({ client: mockClient });
      
      expect(result).toBeDefined();
      expect(result.cache).toBeDefined();
    });
  });
});