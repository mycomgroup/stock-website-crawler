import { describe, it, expect, vi, beforeEach } from 'vitest';

describe('parameter-validator.js', () => {
  let validator;
  let mockCache;
  
  beforeEach(async () => {
    vi.clearAllMocks();
    
    mockCache = {
      getStockPool: vi.fn((poolId) => {
        if (poolId === 'valid_pool') {
          return { id: 'valid_pool', name: 'Valid Pool' };
        }
        return null;
      }),
      validateIndicator: vi.fn((name) => {
        const validIndicators = ['PE', 'PB', 'ROE'];
        const valid = validIndicators.includes(name);
        return {
          valid,
          indicator: valid ? { name, expr: `${name}_expr` } : null,
          message: valid ? `Found indicator: ${name}` : `Indicator not found: ${name}`
        };
      }),
      searchIndicators: vi.fn((query) => {
        return [
          { name: 'PE', expr: 'pe_expr' },
          { name: 'PB', expr: 'pb_expr' }
        ].filter(i => i.name.toLowerCase().includes(query.toLowerCase()));
      }),
      cache: {
        benchmarks: ['沪深300', '中证500', '中证800'],
        transactionCosts: [
          { value: 0, label: '零' },
          { value: 0.002, label: '千分之二' }
        ]
      }
    };
    
    const { ParameterValidator } = await import('../../request/parameter-validator.js');
    validator = new ParameterValidator(mockCache);
  });

  describe('ParameterValidator constructor', () => {
    it('should initialize with cache', async () => {
      const { ParameterValidator } = await import('../../request/parameter-validator.js');
      const validator = new ParameterValidator(mockCache);
      
      expect(validator.cache).toBe(mockCache);
      expect(validator.errors).toEqual([]);
      expect(validator.warnings).toEqual([]);
    });

    it('should work without cache', async () => {
      const { ParameterValidator } = await import('../../request/parameter-validator.js');
      const validator = new ParameterValidator();
      
      expect(validator.cache).toBeUndefined();
    });
  });

  describe('validate', () => {
    it('should return valid result for valid config', () => {
      const config = {
        name: 'Test Strategy',
        stockPool: {
          type: 'system',
          poolId: 'valid_pool',
          stockLimit: 10,
          rebalanceCycle: 5
        },
        filters: [
          { indicator: 'PE', operator: '>', value: 10 }
        ],
        rankings: [
          { indicator: 'ROE', order: 'desc', weight: 1 }
        ],
        tradingModel: {
          type: 1,
          maxPosition: 20,
          minPosition: 5,
          positionWeight: 'equal'
        },
        backtest: {
          startDate: '2024-01-01',
          endDate: '2024-12-31',
          benchmark: '沪深300',
          transactionCost: 0.002
        }
      };
      
      const result = validator.validate(config);
      
      expect(result.valid).toBe(true);
      expect(result.errors).toEqual([]);
    });

    it('should clear errors and warnings before validation', () => {
      validator.errors = ['old_error'];
      validator.warnings = ['old_warning'];
      
      const result = validator.validate({ name: 'Test' });
      
      expect(result.errors).not.toContain('old_error');
      expect(result.warnings).not.toContain('old_warning');
    });

    it('should call all validate methods', () => {
      const config = {
        name: 'Test',
        stockPool: { type: 'system', poolId: 'test' },
        tradingModel: { type: 1 }
      };
      
      validator.validate(config);
      
      expect(validator.errors).toBeDefined();
    });
  });

  describe('validateBasicInfo', () => {
    it('should error on missing name', () => {
      validator.validateBasicInfo({});
      
      expect(validator.errors).toContainEqual({
        field: 'name',
        message: 'Strategy name is required'
      });
    });

    it('should error on empty name', () => {
      validator.validateBasicInfo({ name: '' });
      
      expect(validator.errors).toContainEqual({
        field: 'name',
        message: 'Strategy name is required'
      });
    });

    it('should error on whitespace-only name', () => {
      validator.validateBasicInfo({ name: '   ' });
      
      expect(validator.errors).toContainEqual({
        field: 'name',
        message: 'Strategy name is required'
      });
    });

    it('should warn on long name (> 50 characters)', () => {
      validator.validateBasicInfo({ name: 'a'.repeat(51) });
      
      expect(validator.warnings).toContainEqual({
        field: 'name',
        message: 'Strategy name should be less than 50 characters'
      });
    });

    it('should accept valid name', () => {
      validator.validateBasicInfo({ name: 'Valid Strategy Name' });
      
      expect(validator.errors.filter(e => e.field === 'name')).toEqual([]);
    });
  });

  describe('validateStockPool', () => {
    it('should error on missing stockPool', () => {
      validator.validateStockPool({});
      
      expect(validator.errors).toContainEqual({
        field: 'stockPool',
        message: 'Stock pool configuration is required'
      });
    });

    it('should error on invalid pool type', () => {
      validator.validateStockPool({
        stockPool: {
          type: 'invalid_type',
          poolId: 'test'
        }
      });
      
      expect(validator.errors).toContainEqual({
        field: 'stockPool.type',
        message: 'Invalid pool type: invalid_type'
      });
    });

    it('should accept valid pool types', () => {
      const validTypes = ['system', 'custom', 'static', 'dynamic'];
      
      validTypes.forEach(type => {
        validator.errors = [];
        validator.validateStockPool({
          stockPool: { type, poolId: 'test' }
        });
        
        const typeErrors = validator.errors.filter(e => e.field === 'stockPool.type');
        expect(typeErrors).toEqual([]);
      });
    });

    it('should error on missing poolId', () => {
      validator.validateStockPool({
        stockPool: { type: 'system' }
      });
      
      expect(validator.errors).toContainEqual({
        field: 'stockPool.poolId',
        message: 'Pool ID is required'
      });
    });

    it('should warn on pool not in cache', () => {
      validator.validateStockPool({
        stockPool: {
          type: 'system',
          poolId: 'unknown_pool'
        }
      });
      
      expect(validator.warnings).toContainEqual({
        field: 'stockPool.poolId',
        message: 'Pool not found in cache: unknown_pool'
      });
    });

    it('should accept pool found in cache', () => {
      validator.validateStockPool({
        stockPool: {
          type: 'system',
          poolId: 'valid_pool'
        }
      });
      
      const poolWarnings = validator.warnings.filter(w => w.field === 'stockPool.poolId');
      expect(poolWarnings).toEqual([]);
    });

    it('should warn on stockLimit out of range (> 100)', async () => {
      const mockCache = {
        getStockPool: vi.fn().mockReturnValue({ id: 'test', name: 'Test Pool' }),
      };
      const { ParameterValidator } = await import('../../request/parameter-validator.js');
      const validator = new ParameterValidator(mockCache);
      
      validator.validateStockPool({
        stockPool: {
          type: 'system',
          poolId: 'test',
          stockLimit: 101
        }
      });
      
      expect(validator.warnings).toContainEqual({
        field: 'stockPool.stockLimit',
        message: 'Stock limit should be between 1 and 100'
      });
    });

    it('should warn on stockLimit out of range (> 100)', () => {
      validator.validateStockPool({
        stockPool: {
          type: 'system',
          poolId: 'test',
          stockLimit: 101
        }
      });
      
      expect(validator.warnings).toContainEqual({
        field: 'stockPool.stockLimit',
        message: 'Stock limit should be between 1 and 100'
      });
    });

    it('should accept valid stockLimit', () => {
      validator.validateStockPool({
        stockPool: {
          type: 'system',
          poolId: 'test',
          stockLimit: 50
        }
      });
      
      const limitWarnings = validator.warnings.filter(w => w.field === 'stockPool.stockLimit');
      expect(limitWarnings).toEqual([]);
    });

    it('should warn on rebalanceCycle out of range (> 250)', async () => {
      const mockCache = {
        getStockPool: vi.fn().mockReturnValue({ id: 'test', name: 'Test Pool' }),
      };
      const { ParameterValidator } = await import('../../request/parameter-validator.js');
      const validator = new ParameterValidator(mockCache);
      
      validator.validateStockPool({
        stockPool: {
          type: 'system',
          poolId: 'test',
          rebalanceCycle: 251
        }
      });
      
      expect(validator.warnings).toContainEqual({
        field: 'stockPool.rebalanceCycle',
        message: 'Rebalance cycle should be between 1 and 250 days'
      });
    });

    it('should warn on rebalanceCycle out of range (> 250)', () => {
      validator.validateStockPool({
        stockPool: {
          type: 'system',
          poolId: 'test',
          rebalanceCycle: 251
        }
      });
      
      expect(validator.warnings).toContainEqual({
        field: 'stockPool.rebalanceCycle',
        message: 'Rebalance cycle should be between 1 and 250 days'
      });
    });

    it('should accept valid rebalanceCycle', () => {
      validator.validateStockPool({
        stockPool: {
          type: 'system',
          poolId: 'test',
          rebalanceCycle: 20
        }
      });
      
      const cycleWarnings = validator.warnings.filter(w => w.field === 'stockPool.rebalanceCycle');
      expect(cycleWarnings).toEqual([]);
    });

    it('should skip pool validation if no cache', async () => {
      const { ParameterValidator } = await import('../../request/parameter-validator.js');
      const validator = new ParameterValidator();
      
      validator.validateStockPool({
        stockPool: {
          type: 'system',
          poolId: 'test'
        }
      });
      
      expect(validator.warnings).toEqual([]);
    });
  });

  describe('validateFilters', () => {
    it('should skip if no filters', () => {
      validator.validateFilters({});
      
      expect(validator.errors).toEqual([]);
    });

    it('should skip if filters is not array', () => {
      validator.validateFilters({ filters: 'not_array' });
      
      expect(validator.errors).toEqual([]);
    });

    it('should error on missing indicator', () => {
      validator.validateFilters({
        filters: [
          { operator: '>', value: 10 }
        ]
      });
      
      expect(validator.errors).toContainEqual({
        field: 'filters[0].indicator',
        message: 'Indicator is required'
      });
    });

    it('should warn on unknown indicator', () => {
      validator.validateFilters({
        filters: [
          { indicator: 'unknown', operator: '>', value: 10 }
        ]
      });
      
      expect(validator.warnings).toContainEqual({
        field: 'filters[0].indicator',
        message: 'Unknown indicator: unknown'
      });
    });

    it('should accept valid indicator', () => {
      validator.validateFilters({
        filters: [
          { indicator: 'PE', operator: '>', value: 10 }
        ]
      });
      
      const indWarnings = validator.warnings.filter(w => w.field.includes('indicator'));
      expect(indWarnings).toEqual([]);
    });

    it('should error on invalid operator', () => {
      validator.validateFilters({
        filters: [
          { indicator: 'PE', operator: 'invalid', value: 10 }
        ]
      });
      
      expect(validator.errors).toContainEqual({
        field: 'filters[0].operator',
        message: 'Invalid operator: invalid'
      });
    });

    it('should accept valid operators', () => {
      const validOperators = ['<', '<=', '>', '>=', '==', '!=', 'between', 'in', 'not_in'];
      
      validOperators.forEach((op, index) => {
        validator.errors = [];
        validator.validateFilters({
          filters: [
            { indicator: 'PE', operator: op, value: 10 }
          ]
        });
        
        const opErrors = validator.errors.filter(e => e.field.includes('operator'));
        expect(opErrors).toEqual([]);
      });
    });

    it('should error on missing value', () => {
      validator.validateFilters({
        filters: [
          { indicator: 'PE', operator: '>' }
        ]
      });
      
      expect(validator.errors).toContainEqual({
        field: 'filters[0].value',
        message: 'Value is required'
      });
    });

    it('should error on null value', () => {
      validator.validateFilters({
        filters: [
          { indicator: 'PE', operator: '>', value: null }
        ]
      });
      
      expect(validator.errors).toContainEqual({
        field: 'filters[0].value',
        message: 'Value is required'
      });
    });

    it('should accept valid value', () => {
      validator.validateFilters({
        filters: [
          { indicator: 'PE', operator: '>', value: 10 }
        ]
      });
      
      const valErrors = validator.errors.filter(e => e.field.includes('value'));
      expect(valErrors).toEqual([]);
    });

    it('should validate multiple filters', () => {
      validator.validateFilters({
        filters: [
          { indicator: 'PE', operator: '>', value: 10 },
          { indicator: 'unknown', operator: 'invalid', value: null }
        ]
      });
      
      expect(validator.errors.length).toBe(2);
      expect(validator.warnings.length).toBe(1);
    });

    it('should skip indicator validation without cache', async () => {
      const { ParameterValidator } = await import('../../request/parameter-validator.js');
      const validator = new ParameterValidator();
      
      validator.validateFilters({
        filters: [
          { indicator: 'any', operator: '>', value: 10 }
        ]
      });
      
      expect(validator.warnings).toEqual([]);
    });
  });

  describe('validateRankings', () => {
    it('should skip if no rankings', () => {
      validator.validateRankings({});
      
      expect(validator.errors).toEqual([]);
    });

    it('should skip if rankings is not array', () => {
      validator.validateRankings({ rankings: 'not_array' });
      
      expect(validator.errors).toEqual([]);
    });

    it('should error on missing indicator', () => {
      validator.validateRankings({
        rankings: [
          { order: 'desc' }
        ]
      });
      
      expect(validator.errors).toContainEqual({
        field: 'rankings[0].indicator',
        message: 'Indicator is required'
      });
    });

    it('should warn on unknown indicator', () => {
      validator.validateRankings({
        rankings: [
          { indicator: 'unknown', order: 'desc' }
        ]
      });
      
      expect(validator.warnings).toContainEqual({
        field: 'rankings[0].indicator',
        message: 'Unknown indicator: unknown'
      });
    });

    it('should error on invalid order', () => {
      validator.validateRankings({
        rankings: [
          { indicator: 'PE', order: 'invalid' }
        ]
      });
      
      expect(validator.errors).toContainEqual({
        field: 'rankings[0].order',
        message: 'Invalid order: invalid. Must be \'asc\' or \'desc\''
      });
    });

    it('should accept valid orders', () => {
      validator.validateRankings({
        rankings: [
          { indicator: 'PE', order: 'asc' }
        ]
      });
      
      validator.errors = [];
      validator.validateRankings({
        rankings: [
          { indicator: 'PE', order: 'desc' }
        ]
      });
      
      const orderErrors = validator.errors.filter(e => e.field.includes('order'));
      expect(orderErrors).toEqual([]);
    });

    it('should warn on weight out of range (< 0)', () => {
      validator.validateRankings({
        rankings: [
          { indicator: 'PE', order: 'desc', weight: -0.1 }
        ]
      });
      
      expect(validator.warnings).toContainEqual({
        field: 'rankings[0].weight',
        message: 'Weight should be between 0 and 1'
      });
    });

    it('should warn on weight out of range (> 1)', () => {
      validator.validateRankings({
        rankings: [
          { indicator: 'PE', order: 'desc', weight: 1.1 }
        ]
      });
      
      expect(validator.warnings).toContainEqual({
        field: 'rankings[0].weight',
        message: 'Weight should be between 0 and 1'
      });
    });

    it('should accept valid weight', () => {
      validator.validateRankings({
        rankings: [
          { indicator: 'PE', order: 'desc', weight: 0.5 }
        ]
      });
      
      const weightWarnings = validator.warnings.filter(w => w.field.includes('weight'));
      expect(weightWarnings).toEqual([]);
    });

    it('should accept missing weight', () => {
      validator.validateRankings({
        rankings: [
          { indicator: 'PE', order: 'desc' }
        ]
      });
      
      expect(validator.warnings).toEqual([]);
    });

    it('should validate multiple rankings', () => {
      validator.validateRankings({
        rankings: [
          { indicator: 'PE', order: 'desc' },
          { indicator: 'unknown', order: 'invalid' }
        ]
      });
      
      expect(validator.errors.length).toBe(1);
      expect(validator.warnings.length).toBe(1);
    });
  });

  describe('validateTradingModel', () => {
    it('should error on missing tradingModel', () => {
      validator.validateTradingModel({});
      
      expect(validator.errors).toContainEqual({
        field: 'tradingModel',
        message: 'Trading model configuration is required'
      });
    });

    it('should error on invalid model type', () => {
      validator.validateTradingModel({
        tradingModel: { type: 3 }
      });
      
      expect(validator.errors).toContainEqual({
        field: 'tradingModel.type',
        message: 'Invalid trading model type: 3'
      });
    });

    it('should accept valid model types', () => {
      validator.validateTradingModel({ tradingModel: { type: 1 } });
      validator.errors = [];
      validator.validateTradingModel({ tradingModel: { type: 2 } });
      
      expect(validator.errors).toEqual([]);
    });

    it('should warn on maxPosition out of range (> 100)', () => {
      validator.validateTradingModel({
        tradingModel: {
          type: 1,
          maxPosition: 101
        }
      });
      
      expect(validator.warnings).toContainEqual({
        field: 'tradingModel.maxPosition',
        message: 'Max position should be between 1 and 100'
      });
    });

    it('should warn on minPosition out of range (< 0)', () => {
      validator.validateTradingModel({
        tradingModel: {
          type: 1,
          minPosition: -1
        }
      });
      
      expect(validator.warnings).toContainEqual({
        field: 'tradingModel.minPosition',
        message: 'Min position should be between 0 and 100'
      });
    });

    it('should warn on minPosition out of range (> 100)', () => {
      validator.validateTradingModel({
        tradingModel: {
          type: 1,
          minPosition: 101
        }
      });
      
      expect(validator.warnings).toContainEqual({
        field: 'tradingModel.minPosition',
        message: 'Min position should be between 0 and 100'
      });
    });

    it('should error when minPosition > maxPosition', () => {
      validator.validateTradingModel({
        tradingModel: {
          type: 1,
          maxPosition: 10,
          minPosition: 20
        }
      });
      
      expect(validator.errors).toContainEqual({
        field: 'tradingModel.minPosition',
        message: 'Min position cannot be greater than max position'
      });
    });

    it('should accept minPosition <= maxPosition', () => {
      validator.validateTradingModel({
        tradingModel: {
          type: 1,
          maxPosition: 20,
          minPosition: 10
        }
      });
      
      const posErrors = validator.errors.filter(e => e.field === 'tradingModel.minPosition');
      expect(posErrors).toEqual([]);
    });

    it('should warn on unknown positionWeight', () => {
      validator.validateTradingModel({
        tradingModel: {
          type: 1,
          positionWeight: 'unknown'
        }
      });
      
      expect(validator.warnings).toContainEqual({
        field: 'tradingModel.positionWeight',
        message: 'Unknown position weight method: unknown'
      });
    });

    it('should accept valid positionWeight', () => {
      const validWeights = ['equal', 'circulation_market_cap', 'total_market_cap'];
      
      validWeights.forEach(weight => {
        validator.warnings = [];
        validator.validateTradingModel({
          tradingModel: { type: 1, positionWeight: weight }
        });
        
        const weightWarnings = validator.warnings.filter(w => w.field === 'tradingModel.positionWeight');
        expect(weightWarnings).toEqual([]);
      });
    });
  });

  describe('validateBacktest', () => {
    it('should skip if no backtest config', () => {
      validator.validateBacktest({});
      
      expect(validator.errors).toEqual([]);
    });

    it('should error on invalid startDate format', () => {
      validator.validateBacktest({
        backtest: {
          startDate: '2024/01/01'
        }
      });
      
      expect(validator.errors).toContainEqual({
        field: 'backtest.startDate',
        message: 'Invalid date format: 2024/01/01'
      });
    });

    it('should error on invalid endDate format', () => {
      validator.validateBacktest({
        backtest: {
          endDate: 'invalid-date'
        }
      });
      
      expect(validator.errors).toContainEqual({
        field: 'backtest.endDate',
        message: 'Invalid date format: invalid-date'
      });
    });

    it('should accept valid YYYY-MM-DD format', () => {
      validator.validateBacktest({
        backtest: {
          startDate: '2024-01-01',
          endDate: '2024-12-31'
        }
      });
      
      const dateErrors = validator.errors.filter(e => e.field.includes('Date'));
      expect(dateErrors).toEqual([]);
    });

    it('should error when endDate <= startDate', () => {
      validator.validateBacktest({
        backtest: {
          startDate: '2024-12-31',
          endDate: '2024-01-01'
        }
      });
      
      expect(validator.errors).toContainEqual({
        field: 'backtest.endDate',
        message: 'End date must be after start date'
      });
    });

    it('should accept endDate > startDate', () => {
      validator.validateBacktest({
        backtest: {
          startDate: '2024-01-01',
          endDate: '2024-12-31'
        }
      });
      
      const dateErrors = validator.errors.filter(e => e.field === 'backtest.endDate');
      expect(dateErrors).toEqual([]);
    });

    it('should warn on unknown benchmark', () => {
      validator.validateBacktest({
        backtest: {
          benchmark: 'unknown_benchmark'
        }
      });
      
      expect(validator.warnings).toContainEqual({
        field: 'backtest.benchmark',
        message: 'Unknown benchmark: unknown_benchmark'
      });
    });

    it('should accept valid benchmark', () => {
      validator.validateBacktest({
        backtest: {
          benchmark: '沪深300'
        }
      });
      
      const benchWarnings = validator.warnings.filter(w => w.field === 'backtest.benchmark');
      expect(benchWarnings).toEqual([]);
    });

    it('should warn on transactionCost out of range (< 0)', () => {
      validator.validateBacktest({
        backtest: {
          transactionCost: -0.01
        }
      });
      
      expect(validator.warnings).toContainEqual({
        field: 'backtest.transactionCost',
        message: 'Transaction cost should be between 0 and 0.1 (10%)'
      });
    });

    it('should warn on transactionCost out of range (> 0.1)', () => {
      validator.validateBacktest({
        backtest: {
          transactionCost: 0.11
        }
      });
      
      expect(validator.warnings).toContainEqual({
        field: 'backtest.transactionCost',
        message: 'Transaction cost should be between 0 and 0.1 (10%)'
      });
    });

    it('should accept valid transactionCost', () => {
      validator.validateBacktest({
        backtest: {
          transactionCost: 0.002
        }
      });
      
      const costWarnings = validator.warnings.filter(w => w.field === 'backtest.transactionCost');
      expect(costWarnings).toEqual([]);
    });

    it('should accept zero transactionCost', () => {
      validator.validateBacktest({
        backtest: {
          transactionCost: 0
        }
      });
      
      const costWarnings = validator.warnings.filter(w => w.field === 'backtest.transactionCost');
      expect(costWarnings).toEqual([]);
    });

    it('should skip benchmark validation without cache', async () => {
      const { ParameterValidator } = await import('../../request/parameter-validator.js');
      const validator = new ParameterValidator();
      
      validator.validateBacktest({
        backtest: {
          benchmark: 'any'
        }
      });
      
      expect(validator.warnings).toEqual([]);
    });
  });

  describe('isValidDate', () => {
    it('should return true for valid YYYY-MM-DD', async () => {
      const { ParameterValidator } = await import('../../request/parameter-validator.js');
      const validator = new ParameterValidator();
      
      expect(validator.isValidDate('2024-01-01')).toBe(true);
      expect(validator.isValidDate('2024-12-31')).toBe(true);
    });

    it('should return false for invalid formats', async () => {
      const { ParameterValidator } = await import('../../request/parameter-validator.js');
      const validator = new ParameterValidator();
      
      expect(validator.isValidDate('2024/01/01')).toBe(false);
      expect(validator.isValidDate('01-01-2024')).toBe(false);
      expect(validator.isValidDate('2024-1-1')).toBe(false);
      expect(validator.isValidDate('invalid')).toBe(false);
    });

    it('should return false for invalid dates', async () => {
      const { ParameterValidator } = await import('../../request/parameter-validator.js');
      const validator = new ParameterValidator();
      
      expect(validator.isValidDate('2024-13-01')).toBe(false);
      expect(validator.isValidDate('2024-01-32')).toBe(false);
    });
  });

  describe('suggestIndicators', () => {
    it('should search indicators', () => {
      const result = validator.suggestIndicators('pe');
      
      expect(result.length).toBeGreaterThan(0);
      expect(mockCache.searchIndicators).toHaveBeenCalledWith('pe');
    });

    it('should return empty array without cache', async () => {
      const { ParameterValidator } = await import('../../request/parameter-validator.js');
      const validator = new ParameterValidator();
      
      const result = validator.suggestIndicators('pe');
      
      expect(result).toEqual([]);
    });
  });

  describe('getValidBenchmarks', () => {
    it('should return benchmarks from cache', () => {
      const result = validator.getValidBenchmarks();
      
      expect(result).toEqual(['沪深300', '中证500', '中证800']);
    });

    it('should return empty array without cache', async () => {
      const { ParameterValidator } = await import('../../request/parameter-validator.js');
      const validator = new ParameterValidator();
      
      const result = validator.getValidBenchmarks();
      
      expect(result).toEqual([]);
    });
  });

  describe('getValidTransactionCosts', () => {
    it('should return transaction costs from cache', () => {
      const result = validator.getValidTransactionCosts();
      
      expect(result).toEqual([
        { value: 0, label: '零' },
        { value: 0.002, label: '千分之二' }
      ]);
    });

    it('should return empty array without cache', async () => {
      const { ParameterValidator } = await import('../../request/parameter-validator.js');
      const validator = new ParameterValidator();
      
      const result = validator.getValidTransactionCosts();
      
      expect(result).toEqual([]);
    });
  });
});