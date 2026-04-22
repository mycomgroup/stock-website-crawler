import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';

vi.mock('../../request/parameter-cache.js', () => ({
  getParameterCache: vi.fn()
}));

describe('config-normalizer.js', () => {
  let mockCache;
  let consoleLogSpy;
  let consoleWarnSpy;
  
  beforeEach(async () => {
    vi.clearAllMocks();
    
    consoleLogSpy = vi.spyOn(console, 'log').mockImplementation(() => {});
    consoleWarnSpy = vi.spyOn(console, 'warn').mockImplementation(() => {});
    
    mockCache = {
      resolveId: vi.fn((name) => {
        const mapping = {
          'PE': '0.M.股票每日指标_市盈率.0',
          'PB': '0.M.股票每日指标_市净率.0',
          'ROE': '0.M.股票每日指标_净资产收益率.0',
          '市值': '0.M.股票每日指标_总市值.0'
        };
        return mapping[name] || name;
      }),
      resolvePoolId: vi.fn((name) => {
        const mapping = {
          '全A股': '',
          'hs300': '',
          'zz500': '',
          '自定义池': '1.P.custom'
        };
        return mapping[name] || name;
      }),
      cache: {
        indicators: { flat: [] },
        stockPools: { userPools: [], systemPools: [] }
      }
    };
    
    const { getParameterCache } = await import('../../request/parameter-cache.js');
    vi.mocked(getParameterCache).mockResolvedValue(mockCache);
  });
  
  afterEach(() => {
    consoleLogSpy.mockRestore();
    consoleWarnSpy.mockRestore();
  });

  describe('ConfigNormalizer constructor', () => {
    it('should initialize without cache', async () => {
      const { ConfigNormalizer } = await import('../../request/config-normalizer.js');
      const normalizer = new ConfigNormalizer();
      
      expect(normalizer.cache).toBeNull();
    });

    it('should initialize with provided cache', async () => {
      const { ConfigNormalizer } = await import('../../request/config-normalizer.js');
      const normalizer = new ConfigNormalizer({ cache: mockCache });
      
      expect(normalizer.cache).toBe(mockCache);
    });
  });

  describe('init', () => {
    it('should load cache if not provided', async () => {
      const { ConfigNormalizer } = await import('../../request/config-normalizer.js');
      const normalizer = new ConfigNormalizer();
      
      await normalizer.init();
      
      expect(normalizer.cache).toBeDefined();
    });

    it('should not reload cache if already provided', async () => {
      const { ConfigNormalizer, defaultNormalizer } = await import('../../request/config-normalizer.js');
      const normalizer = new ConfigNormalizer({ cache: mockCache });
      
      await normalizer.init();
      
      expect(normalizer.cache).toBe(mockCache);
    });
  });

  describe('normalize', () => {
    it('should normalize string filters', async () => {
      const { ConfigNormalizer } = await import('../../request/config-normalizer.js');
      const normalizer = new ConfigNormalizer({ cache: mockCache });
      
      const config = {
        filters: ['simple_filter']
      };
      
      const result = await normalizer.normalize(config);
      
      expect(result.filters).toEqual(['simple_filter']);
    });

    it('should normalize object filters with indicator field', async () => {
      const { ConfigNormalizer } = await import('../../request/config-normalizer.js');
      const normalizer = new ConfigNormalizer({ cache: mockCache });
      
      const config = {
        filters: [
          { indicator: 'PE', operator: '>', value: 10 }
        ]
      };
      
      const result = await normalizer.normalize(config);
      
      expect(result.filters[0].id).toBe('0.M.股票每日指标_市盈率.0');
      expect(result.filters[0].op).toBe('gt');
      expect(result.filters[0].val).toBe('10');
      expect(result.filters[0].type).toBe('meas');
    });

    it('should normalize object filters with factor field', async () => {
      const { ConfigNormalizer } = await import('../../request/config-normalizer.js');
      const normalizer = new ConfigNormalizer({ cache: mockCache });
      
      const config = {
        filters: [
          { factor: 'PB', op: '<', val: 5 }
        ]
      };
      
      const result = await normalizer.normalize(config);
      
      expect(result.filters[0].id).toBe('0.M.股票每日指标_市净率.0');
      expect(result.filters[0].op).toBe('lt');
    });

    it('should map operators correctly', async () => {
      const { ConfigNormalizer } = await import('../../request/config-normalizer.js');
      const normalizer = new ConfigNormalizer({ cache: mockCache });
      
      const config = {
        filters: [
          { indicator: 'PE', operator: '<', value: 10 },
          { indicator: 'PB', operator: '>', value: 5 },
          { indicator: 'ROE', operator: '<=', value: 20 },
          { indicator: '市值', operator: '>=', value: 100 }
        ]
      };
      
      const result = await normalizer.normalize(config);
      
      expect(result.filters[0].op).toBe('lt');
      expect(result.filters[1].op).toBe('gt');
      expect(result.filters[2].op).toBe('lte');
      expect(result.filters[3].op).toBe('gte');
    });

    it('should support already mapped operators', async () => {
      const { ConfigNormalizer } = await import('../../request/config-normalizer.js');
      const normalizer = new ConfigNormalizer({ cache: mockCache });
      
      const config = {
        filters: [
          { indicator: 'PE', operator: 'lt', value: 10 },
          { indicator: 'PB', operator: 'gte', value: 5 }
        ]
      };
      
      const result = await normalizer.normalize(config);
      
      expect(result.filters[0].op).toBe('lt');
      expect(result.filters[1].op).toBe('gte');
    });

    it('should default to gt for unknown operators', async () => {
      const { ConfigNormalizer } = await import('../../request/config-normalizer.js');
      const normalizer = new ConfigNormalizer({ cache: mockCache });
      
      const config = {
        filters: [
          { indicator: 'PE', operator: 'unknown', value: 10 }
        ]
      };
      
      const result = await normalizer.normalize(config);
      
      expect(result.filters[0].op).toBe('gt');
    });

    it('should use op field as alternative', async () => {
      const { ConfigNormalizer } = await import('../../request/config-normalizer.js');
      const normalizer = new ConfigNormalizer({ cache: mockCache });
      
      const config = {
        filters: [
          { indicator: 'PE', op: '<', value: 10 }
        ]
      };
      
      const result = await normalizer.normalize(config);
      
      expect(result.filters[0].op).toBe('lt');
    });

    it('should use val field as alternative', async () => {
      const { ConfigNormalizer } = await import('../../request/config-normalizer.js');
      const normalizer = new ConfigNormalizer({ cache: mockCache });
      
      const config = {
        filters: [
          { indicator: 'PE', operator: '>', val: 10 }
        ]
      };
      
      const result = await normalizer.normalize(config);
      
      expect(result.filters[0].val).toBe('10');
    });

    it('should handle filters with industry', async () => {
      const { ConfigNormalizer } = await import('../../request/config-normalizer.js');
      const normalizer = new ConfigNormalizer({ cache: mockCache });
      
      const config = {
        filters: [
          { indicator: 'PE', operator: '>', value: 10, industry: 1 }
        ]
      };
      
      const result = await normalizer.normalize(config);
      
      expect(result.filters[0].industry).toBe(1);
    });

    it('should normalize rankings with indicator field', async () => {
      const { ConfigNormalizer } = await import('../../request/config-normalizer.js');
      const normalizer = new ConfigNormalizer({ cache: mockCache });
      
      const config = {
        rankings: [
          { indicator: 'ROE', weight: 0.5, order: 'desc' }
        ]
      };
      
      const result = await normalizer.normalize(config);
      
      expect(result.ranks[0].id).toBe('0.M.股票每日指标_净资产收益率.0');
      expect(result.ranks[0].weight).toBe(0.5);
      expect(result.ranks[0].asc).toBe(false);
      expect(result.ranks[0].industry).toBe(0);
    });

    it('should normalize rankings with factor field', async () => {
      const { ConfigNormalizer } = await import('../../request/config-normalizer.js');
      const normalizer = new ConfigNormalizer({ cache: mockCache });
      
      const config = {
        rankings: [
          { factor: '市值', weight: 1 }
        ]
      };
      
      const result = await normalizer.normalize(config);
      
      expect(result.ranks[0].id).toBe('0.M.股票每日指标_总市值.0');
    });

    it('should determine asc correctly from order field', async () => {
      const { ConfigNormalizer } = await import('../../request/config-normalizer.js');
      const normalizer = new ConfigNormalizer({ cache: mockCache });
      
      const config = {
        rankings: [
          { indicator: 'ROE', order: 'asc' },
          { indicator: 'PE', order: 'desc' }
        ]
      };
      
      const result = await normalizer.normalize(config);
      
      expect(result.ranks[0].asc).toBe(true);
      expect(result.ranks[1].asc).toBe(false);
    });

    it('should determine asc correctly from asc field', async () => {
      const { ConfigNormalizer } = await import('../../request/config-normalizer.js');
      const normalizer = new ConfigNormalizer({ cache: mockCache });
      
      const config = {
        rankings: [
          { indicator: 'ROE', asc: true },
          { indicator: 'PE', asc: false }
        ]
      };
      
      const result = await normalizer.normalize(config);
      
      expect(result.ranks[0].asc).toBe(true);
      expect(result.ranks[1].asc).toBe(false);
    });

    it('should determine asc correctly from ascending field', async () => {
      const { ConfigNormalizer } = await import('../../request/config-normalizer.js');
      const normalizer = new ConfigNormalizer({ cache: mockCache });
      
      const config = {
        rankings: [
          { indicator: 'ROE', ascending: true }
        ]
      };
      
      const result = await normalizer.normalize(config);
      
      expect(result.ranks[0].asc).toBe(true);
    });

    it('should use default weight of 1', async () => {
      const { ConfigNormalizer } = await import('../../request/config-normalizer.js');
      const normalizer = new ConfigNormalizer({ cache: mockCache });
      
      const config = {
        rankings: [
          { indicator: 'ROE' }
        ]
      };
      
      const result = await normalizer.normalize(config);
      
      expect(result.ranks[0].weight).toBe(1.0);
    });

    it('should remove rankings field after normalization', async () => {
      const { ConfigNormalizer } = await import('../../request/config-normalizer.js');
      const normalizer = new ConfigNormalizer({ cache: mockCache });
      
      const config = {
        rankings: [{ indicator: 'ROE' }]
      };
      
      const result = await normalizer.normalize(config);
      
      expect(result.rankings).toBeUndefined();
      expect(result.ranks).toBeDefined();
    });

    it('should normalize pool - 全部A股', async () => {
      const { ConfigNormalizer } = await import('../../request/config-normalizer.js');
      const normalizer = new ConfigNormalizer({ cache: mockCache });
      
      const result = await normalizer.normalize({ pool: '全部A股' });
      
      expect(result.pool).toBe('');
    });

    it('should normalize pool - hs300', async () => {
      const { ConfigNormalizer } = await import('../../request/config-normalizer.js');
      const normalizer = new ConfigNormalizer({ cache: mockCache });
      
      const result = await normalizer.normalize({ pool: 'hs300' });
      
      expect(result.pool).toBe('');
    });

    it('should normalize pool - zz500', async () => {
      const { ConfigNormalizer } = await import('../../request/config-normalizer.js');
      const normalizer = new ConfigNormalizer({ cache: mockCache });
      
      const result = await normalizer.normalize({ pool: 'zz500' });
      
      expect(result.pool).toBe('');
    });

    it('should normalize pool - zz1000', async () => {
      const { ConfigNormalizer } = await import('../../request/config-normalizer.js');
      const normalizer = new ConfigNormalizer({ cache: mockCache });
      
      const result = await normalizer.normalize({ pool: 'zz1000' });
      
      expect(result.pool).toBe('');
    });

    it('should normalize pool - empty', async () => {
      const { ConfigNormalizer } = await import('../../request/config-normalizer.js');
      const normalizer = new ConfigNormalizer({ cache: mockCache });
      
      const result = await normalizer.normalize({ pool: '' });
      
      expect(result.pool).toBe('');
    });

    it('should normalize pool - null', async () => {
      const { ConfigNormalizer } = await import('../../request/config-normalizer.js');
      const normalizer = new ConfigNormalizer({ cache: mockCache });
      
      const result = await normalizer.normalize({ pool: null });
      
      expect(result.pool).toBe('');
    });

    it('should resolve custom pool ID', async () => {
      const { ConfigNormalizer } = await import('../../request/config-normalizer.js');
      const normalizer = new ConfigNormalizer({ cache: mockCache });
      
      const result = await normalizer.normalize({ pool: '自定义池' });
      
      expect(result.pool).toBe('1.P.custom');
    });

    it('should normalize period from rebalanceCycle', async () => {
      const { ConfigNormalizer } = await import('../../request/config-normalizer.js');
      const normalizer = new ConfigNormalizer({ cache: mockCache });
      
      const config = {
        rebalanceCycle: '每5天'
      };
      
      const result = await normalizer.normalize(config);
      
      expect(result.period).toBe(5);
    });

    it('should extract number from rebalanceCycle', async () => {
      const { ConfigNormalizer } = await import('../../request/config-normalizer.js');
      const normalizer = new ConfigNormalizer({ cache: mockCache });
      
      const config = {
        rebalanceCycle: '10日轮动'
      };
      
      const result = await normalizer.normalize(config);
      
      expect(result.period).toBe(10);
    });

    it('should use period field directly', async () => {
      const { ConfigNormalizer } = await import('../../request/config-normalizer.js');
      const normalizer = new ConfigNormalizer({ cache: mockCache });
      
      const result = await normalizer.normalize({ period: 20 });
      
      expect(result.period).toBe(20);
    });

    it('should use default period of 5', async () => {
      const { ConfigNormalizer } = await import('../../request/config-normalizer.js');
      const normalizer = new ConfigNormalizer({ cache: mockCache });
      
      const result = await normalizer.normalize({});
      
      expect(result.period).toBe(5);
    });

    it('should normalize benchmark - 沪深300', async () => {
      const { ConfigNormalizer } = await import('../../request/config-normalizer.js');
      const normalizer = new ConfigNormalizer({ cache: mockCache });
      
      const result = await normalizer.normalize({ benchmark: '沪深300' });
      
      expect(result.reference).toBe('000300');
    });

    it('should normalize benchmark - hs300', async () => {
      const { ConfigNormalizer } = await import('../../request/config-normalizer.js');
      const normalizer = new ConfigNormalizer({ cache: mockCache });
      
      const result = await normalizer.normalize({ benchmark: 'hs300' });
      
      expect(result.reference).toBe('000300');
    });

    it('should normalize benchmark - 中证500', async () => {
      const { ConfigNormalizer } = await import('../../request/config-normalizer.js');
      const normalizer = new ConfigNormalizer({ cache: mockCache });
      
      const result = await normalizer.normalize({ benchmark: '中证500' });
      
      expect(result.reference).toBe('000905');
    });

    it('should normalize benchmark - zz500', async () => {
      const { ConfigNormalizer } = await import('../../request/config-normalizer.js');
      const normalizer = new ConfigNormalizer({ cache: mockCache });
      
      const result = await normalizer.normalize({ benchmark: 'zz500' });
      
      expect(result.reference).toBe('000905');
    });

    it('should normalize benchmark - 中证800', async () => {
      const { ConfigNormalizer } = await import('../../request/config-normalizer.js');
      const normalizer = new ConfigNormalizer({ cache: mockCache });
      
      const result = await normalizer.normalize({ benchmark: '中证800' });
      
      expect(result.reference).toBe('000906');
    });

    it('should normalize benchmark - 中证1000', async () => {
      const { ConfigNormalizer } = await import('../../request/config-normalizer.js');
      const normalizer = new ConfigNormalizer({ cache: mockCache });
      
      const result = await normalizer.normalize({ benchmark: '中证1000' });
      
      expect(result.reference).toBe('000852');
    });

    it('should normalize benchmark - 创业板', async () => {
      const { ConfigNormalizer } = await import('../../request/config-normalizer.js');
      const normalizer = new ConfigNormalizer({ cache: mockCache });
      
      const result = await normalizer.normalize({ benchmark: '创业板' });
      
      expect(result.reference).toBe('399006');
    });

    it('should normalize benchmark - 上证指数', async () => {
      const { ConfigNormalizer } = await import('../../request/config-normalizer.js');
      const normalizer = new ConfigNormalizer({ cache: mockCache });
      
      const result = await normalizer.normalize({ benchmark: '上证指数' });
      
      expect(result.reference).toBe('000001');
    });

    it('should use reference field if benchmark not mapped', async () => {
      const { ConfigNormalizer } = await import('../../request/config-normalizer.js');
      const normalizer = new ConfigNormalizer({ cache: mockCache });
      
      const result = await normalizer.normalize({ reference: 'custom_ref' });
      
      expect(result.reference).toBe('custom_ref');
    });

    it('should use default reference of 000300', async () => {
      const { ConfigNormalizer } = await import('../../request/config-normalizer.js');
      const normalizer = new ConfigNormalizer({ cache: mockCache });
      
      const result = await normalizer.normalize({});
      
      expect(result.reference).toBe('000300');
    });

    it('should normalize model from tradingModel', async () => {
      const { ConfigNormalizer } = await import('../../request/config-normalizer.js');
      const normalizer = new ConfigNormalizer({ cache: mockCache });
      
      const result = await normalizer.normalize({ tradingModel: 1 });
      
      expect(result.model).toBe(1);
    });

    it('should use model field directly', async () => {
      const { ConfigNormalizer } = await import('../../request/config-normalizer.js');
      const normalizer = new ConfigNormalizer({ cache: mockCache });
      
      const result = await normalizer.normalize({ model: 2 });
      
      expect(result.model).toBe(2);
    });

    it('should default model to 0', async () => {
      const { ConfigNormalizer } = await import('../../request/config-normalizer.js');
      const normalizer = new ConfigNormalizer({ cache: mockCache });
      
      const result = await normalizer.normalize({});
      
      expect(result.model).toBe(0);
    });

    it('should handle complex config with all fields', async () => {
      const { ConfigNormalizer } = await import('../../request/config-normalizer.js');
      const normalizer = new ConfigNormalizer({ cache: mockCache });
      
      const config = {
        filters: [
          { indicator: 'PE', operator: '>', value: 10, industry: 1 },
          'simple_filter'
        ],
        rankings: [
          { factor: 'ROE', weight: 0.6, order: 'desc' },
          { indicator: '市值', weight: 0.4, asc: true }
        ],
        pool: '自定义池',
        rebalanceCycle: '每5天',
        benchmark: '中证500',
        tradingModel: 1
      };
      
      const result = await normalizer.normalize(config);
      
      expect(result.filters.length).toBe(2);
      expect(result.ranks.length).toBe(2);
      expect(result.pool).toBe('1.P.custom');
      expect(result.period).toBe(5);
      expect(result.reference).toBe('000905');
      expect(result.model).toBe(1);
    });

    it('should preserve other fields', async () => {
      const { ConfigNormalizer } = await import('../../request/config-normalizer.js');
      const normalizer = new ConfigNormalizer({ cache: mockCache });
      
      const config = {
        customField: 'customValue',
        anotherField: 123
      };
      
      const result = await normalizer.normalize(config);
      
      expect(result.customField).toBe('customValue');
      expect(result.anotherField).toBe(123);
    });

    it('should not modify original config', async () => {
      const { ConfigNormalizer } = await import('../../request/config-normalizer.js');
      const normalizer = new ConfigNormalizer({ cache: mockCache });
      
      const config = {
        filters: [{ indicator: 'PE', operator: '>', value: 10 }],
        rankings: [{ indicator: 'ROE' }]
      };
      
      const result = await normalizer.normalize(config);
      
      expect(config.filters[0].indicator).toBe('PE');
      expect(config.rankings).toBeDefined();
    });
  });

  describe('normalizeConfig (singleton)', () => {
    it('should use default normalizer', async () => {
      vi.clearAllMocks();
      const { getParameterCache } = await import('../../request/parameter-cache.js');
      vi.mocked(getParameterCache).mockResolvedValue(mockCache);
      
      const { normalizeConfig } = await import('../../request/config-normalizer.js');
      const result = await normalizeConfig({ benchmark: '沪深300' });
      
      expect(result.reference).toBe('000300');
    });

    it('should reuse default normalizer', async () => {
      vi.clearAllMocks();
      const { getParameterCache } = await import('../../request/parameter-cache.js');
      vi.mocked(getParameterCache).mockResolvedValue(mockCache);
      
      const module = await import('../../request/config-normalizer.js');
      await module.normalizeConfig({});
      await module.normalizeConfig({});
      
      expect(mockCache.resolveId).toHaveBeenCalled();
    });
  });
});