import fs from 'node:fs';
import { getParameterCache } from './parameter-cache.js';

export class ConfigNormalizer {
  constructor(options = {}) {
    this.cache = options.cache || null;
  }

  async init() {
    if (!this.cache) {
      this.cache = await getParameterCache();
    }
  }

  /**
   * Normalizes a strategy configuration.
   * Processes filters, rankings, and other fields.
   */
  async normalize(config) {
    if (!this.cache) await this.init();

    const normalized = { ...config };

    // 1. Normalize Filters
    if (config.filters && Array.isArray(config.filters)) {
      normalized.filters = config.filters.map(filter => {
        if (typeof filter === 'string') return filter;
        
        // Support both "indicator" and "factor" field names
        const indicatorName = filter.indicator || filter.factor;
        const id = this.cache.resolveId(indicatorName);

        // Operator mapping: < -> lt, > -> gt, <= -> lte, >= -> gte
        const rawOp = filter.operator || filter.op || '>';
        const opMap = { '<': 'lt', '>': 'gt', '<=': 'lte', '>=': 'gte', 'lt': 'lt', 'gt': 'gt', 'lte': 'lte', 'gte': 'gte' };
        const op = opMap[rawOp] || 'gt';

        const val = String(filter.value !== undefined ? filter.value : filter.val);

        // Guorn filter object format: { id, op, val, type, industry }
        return { id, op, val, type: 'meas', industry: filter.industry || 0 };
      });
    }

    // 2. Normalize Rankings (ranks)
    if (config.rankings && Array.isArray(config.rankings)) {
      normalized.ranks = config.rankings.map(rank => {
        // Support both "indicator" and "factor" field names
        const indicatorName = rank.indicator || rank.factor;
        const id = this.cache.resolveId(indicatorName);
        return {
          id: id,
          weight: rank.weight || 1.0,
          asc: rank.order === 'asc' || rank.asc === true || rank.ascending === true,
          industry: rank.industry || 0
        };
      });
      delete normalized.rankings; // Remove high-level field
    }

    // 3. Normalize Pool
    if (config.pool === '全部A股' || !config.pool || config.pool === 'hs300' || config.pool === 'zz500' || config.pool === 'zz1000') {
      // Index constituents are not specified as pools in Guorn - use empty string for all A-shares
      normalized.pool = '';
    } else {
      normalized.pool = this.cache.resolvePoolId(config.pool);
    }

    // 4. Normalize Period (Rebalance Cycle)
    if (config.rebalanceCycle) {
      const match = config.rebalanceCycle.match(/(\d+)/);
      if (match) {
        normalized.period = parseInt(match[1], 10);
      }
    } else if (config.period) {
      normalized.period = config.period;
    } else {
      normalized.period = 5;
    }

    // 5. Normalize Benchmark (reference)
    const benchmarkMap = {
      '沪深300': '000300',
      'hs300': '000300',
      '中证500': '000905',
      'zz500': '000905',
      '中证800': '000906',
      'zz800': '000906',
      '中证1000': '000852',
      'zz1000': '000852',
      '创业板': '399006',
      '上证指数': '000001'
    };
    if (config.benchmark && benchmarkMap[config.benchmark]) {
      normalized.reference = benchmarkMap[config.benchmark];
    } else if (config.reference) {
      normalized.reference = config.reference;
    } else {
      normalized.reference = '000300';
    }

    normalized.model = config.model !== undefined ? config.model : (config.tradingModel || 0);

    return normalized;
  }
}

let defaultNormalizer = null;
export async function normalizeConfig(config, options = {}) {
  if (!defaultNormalizer) {
    defaultNormalizer = new ConfigNormalizer(options);
  }
  return await defaultNormalizer.normalize(config);
}
