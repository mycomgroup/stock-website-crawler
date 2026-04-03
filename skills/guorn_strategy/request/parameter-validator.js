export class ParameterValidator {
  constructor(cache) {
    this.cache = cache;
    this.errors = [];
    this.warnings = [];
  }

  validate(config) {
    this.errors = [];
    this.warnings = [];

    this.validateBasicInfo(config);
    this.validateStockPool(config);
    this.validateFilters(config);
    this.validateRankings(config);
    this.validateTradingModel(config);
    this.validateBacktest(config);

    return {
      valid: this.errors.length === 0,
      errors: this.errors,
      warnings: this.warnings
    };
  }

  validateBasicInfo(config) {
    if (!config.name || config.name.trim().length === 0) {
      this.errors.push({ field: 'name', message: 'Strategy name is required' });
    }

    if (config.name && config.name.length > 50) {
      this.warnings.push({ field: 'name', message: 'Strategy name should be less than 50 characters' });
    }
  }

  validateStockPool(config) {
    if (!config.stockPool) {
      this.errors.push({ field: 'stockPool', message: 'Stock pool configuration is required' });
      return;
    }

    const { type, poolId, stockLimit, rebalanceCycle } = config.stockPool;

    if (!['system', 'custom', 'static', 'dynamic'].includes(type)) {
      this.errors.push({ field: 'stockPool.type', message: `Invalid pool type: ${type}` });
    }

    if (!poolId) {
      this.errors.push({ field: 'stockPool.poolId', message: 'Pool ID is required' });
    } else if (this.cache) {
      const pool = this.cache.getStockPool(poolId);
      if (!pool) {
        this.warnings.push({ field: 'stockPool.poolId', message: `Pool not found in cache: ${poolId}` });
      }
    }

    if (stockLimit && (stockLimit < 1 || stockLimit > 100)) {
      this.warnings.push({ field: 'stockPool.stockLimit', message: 'Stock limit should be between 1 and 100' });
    }

    if (rebalanceCycle && (rebalanceCycle < 1 || rebalanceCycle > 250)) {
      this.warnings.push({ field: 'stockPool.rebalanceCycle', message: 'Rebalance cycle should be between 1 and 250 days' });
    }
  }

  validateFilters(config) {
    if (!config.filters || !Array.isArray(config.filters)) {
      return;
    }

    config.filters.forEach((filter, index) => {
      if (!filter.indicator) {
        this.errors.push({ field: `filters[${index}].indicator`, message: 'Indicator is required' });
      } else if (this.cache) {
        const validation = this.cache.validateIndicator(filter.indicator);
        if (!validation.valid) {
          this.warnings.push({ 
            field: `filters[${index}].indicator`, 
            message: `Unknown indicator: ${filter.indicator}` 
          });
        }
      }

      const validOperators = ['<', '<=', '>', '>=', '==', '!=', 'between', 'in', 'not_in'];
      if (!validOperators.includes(filter.operator)) {
        this.errors.push({ 
          field: `filters[${index}].operator`, 
          message: `Invalid operator: ${filter.operator}` 
        });
      }

      if (filter.value === undefined || filter.value === null) {
        this.errors.push({ field: `filters[${index}].value`, message: 'Value is required' });
      }
    });
  }

  validateRankings(config) {
    if (!config.rankings || !Array.isArray(config.rankings)) {
      return;
    }

    config.rankings.forEach((ranking, index) => {
      if (!ranking.indicator) {
        this.errors.push({ field: `rankings[${index}].indicator`, message: 'Indicator is required' });
      } else if (this.cache) {
        const validation = this.cache.validateIndicator(ranking.indicator);
        if (!validation.valid) {
          this.warnings.push({ 
            field: `rankings[${index}].indicator`, 
            message: `Unknown indicator: ${ranking.indicator}` 
          });
        }
      }

      if (!['asc', 'desc'].includes(ranking.order)) {
        this.errors.push({ 
          field: `rankings[${index}].order`, 
          message: `Invalid order: ${ranking.order}. Must be 'asc' or 'desc'` 
        });
      }

      if (ranking.weight !== undefined && (ranking.weight < 0 || ranking.weight > 1)) {
        this.warnings.push({ 
          field: `rankings[${index}].weight`, 
          message: 'Weight should be between 0 and 1' 
        });
      }
    });
  }

  validateTradingModel(config) {
    if (!config.tradingModel) {
      this.errors.push({ field: 'tradingModel', message: 'Trading model configuration is required' });
      return;
    }

    const { type, maxPosition, minPosition, positionWeight } = config.tradingModel;

    if (![1, 2].includes(type)) {
      this.errors.push({ field: 'tradingModel.type', message: `Invalid trading model type: ${type}` });
    }

    if (maxPosition && (maxPosition < 1 || maxPosition > 100)) {
      this.warnings.push({ field: 'tradingModel.maxPosition', message: 'Max position should be between 1 and 100' });
    }

    if (minPosition !== undefined && (minPosition < 0 || minPosition > 100)) {
      this.warnings.push({ field: 'tradingModel.minPosition', message: 'Min position should be between 0 and 100' });
    }

    if (maxPosition && minPosition && minPosition > maxPosition) {
      this.errors.push({ field: 'tradingModel.minPosition', message: 'Min position cannot be greater than max position' });
    }

    const validWeights = ['equal', 'circulation_market_cap', 'total_market_cap'];
    if (positionWeight && !validWeights.includes(positionWeight)) {
      this.warnings.push({ 
        field: 'tradingModel.positionWeight', 
        message: `Unknown position weight method: ${positionWeight}` 
      });
    }
  }

  validateBacktest(config) {
    if (!config.backtest) {
      return;
    }

    const { startDate, endDate, benchmark, transactionCost } = config.backtest;

    if (startDate && !this.isValidDate(startDate)) {
      this.errors.push({ field: 'backtest.startDate', message: `Invalid date format: ${startDate}` });
    }

    if (endDate && !this.isValidDate(endDate)) {
      this.errors.push({ field: 'backtest.endDate', message: `Invalid date format: ${endDate}` });
    }

    if (startDate && endDate && new Date(startDate) >= new Date(endDate)) {
      this.errors.push({ field: 'backtest.endDate', message: 'End date must be after start date' });
    }

    if (benchmark && this.cache) {
      const validBenchmarks = this.cache.cache?.benchmarks || [];
      if (!validBenchmarks.includes(benchmark)) {
        this.warnings.push({ field: 'backtest.benchmark', message: `Unknown benchmark: ${benchmark}` });
      }
    }

    if (transactionCost !== undefined && (transactionCost < 0 || transactionCost > 0.1)) {
      this.warnings.push({ field: 'backtest.transactionCost', message: 'Transaction cost should be between 0 and 0.1 (10%)' });
    }
  }

  isValidDate(dateString) {
    const regex = /^\d{4}-\d{2}-\d{2}$/;
    if (!regex.test(dateString)) return false;
    
    const date = new Date(dateString);
    return date instanceof Date && !isNaN(date);
  }

  suggestIndicators(query) {
    if (!this.cache) return [];
    return this.cache.searchIndicators(query);
  }

  getValidBenchmarks() {
    return this.cache?.cache?.benchmarks || [];
  }

  getValidTransactionCosts() {
    return this.cache?.cache?.transactionCosts || [];
  }
}