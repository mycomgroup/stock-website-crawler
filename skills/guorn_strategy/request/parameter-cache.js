import fs from 'node:fs';
import path from 'node:path';
import { GuornStrategyClient } from './guorn-strategy-client.js';
import { DATA_ROOT } from '../paths.js';

const CACHE_FILE = path.join(DATA_ROOT, 'parameters-cache.json');
const CACHE_DURATION = 24 * 60 * 60 * 1000;

export class ParameterCache {
  constructor(options = {}) {
    this.client = options.client || new GuornStrategyClient(options);
    this.cacheFile = options.cacheFile || CACHE_FILE;
    this.cache = null;
  }

  async load() {
    if (fs.existsSync(this.cacheFile)) {
      try {
        const data = JSON.parse(fs.readFileSync(this.cacheFile, 'utf8'));
        const age = Date.now() - new Date(data.timestamp).getTime();
        
        if (age < CACHE_DURATION) {
          this.cache = data;
          console.log(`Loaded cached parameters (${Math.round(age / 1000 / 60)} minutes old)`);
          return this.cache;
        }
      } catch (error) {
        console.warn('Failed to load cache:', error.message);
      }
    }
    
    return await this.refresh();
  }

  async refresh() {
    console.log('Refreshing parameters from guorn.com...');
    
    try {
      const [indicators, stockPools, profile, privilege] = await Promise.all([
        this.client.getStockMeta('stock'),
        Promise.all([
          this.client.getStockPoolList('stock'),
          this.client.getHotPoolList('stock')
        ]),
        this.client.getUserProfile(),
        this.client.request('/user/privilege?filename=stockScreen&op=Show')
      ]);

      const parsedIndicators = this.parseIndicators(indicators.data);
      const parsedStockPools = this.parseStockPools(stockPools);

      this.cache = {
        timestamp: new Date().toISOString(),
        indicators: parsedIndicators,
        stockPools: parsedStockPools,
        profile: profile.data,
        privilege: privilege.data,
        tradingModels: [
          { id: 1, name: '模型Ⅰ--定期轮动' },
          { id: 2, name: '模型Ⅱ--条件触发' }
        ],
        benchmarks: [
          '沪深300', '中证500', '中证800', '中证流通',
          '创业板指数', '上证指数', '上证50', '中证1000'
        ],
        transactionCosts: [
          { value: 0, label: '零' },
          { value: 0.001, label: '千分之一' },
          { value: 0.002, label: '千分之二' },
          { value: 0.0025, label: '千分之二点五' },
          { value: 0.003, label: '千分之三' },
          { value: 0.005, label: '千分之五' },
          { value: 0.008, label: '千分之八' },
          { value: 0.01, label: '千分之十' }
        ]
      };

      fs.mkdirSync(path.dirname(this.cacheFile), { recursive: true });
      fs.writeFileSync(this.cacheFile, JSON.stringify(this.cache, null, 2));
      
      console.log(`Cached ${parsedIndicators.flat.length} indicators`);
      console.log(`Cached ${parsedStockPools.userPools.length + parsedStockPools.systemPools.length} stock pools`);
      
      return this.cache;
    } catch (error) {
      console.error('Failed to refresh parameters:', error.message);
      throw error;
    }
  }

  parseIndicators(data) {
    const indicators = {
      functions: [],
      categories: {},
      flat: []
    };

    if (!data) return indicators;

    if (data.function && data.function.measures) {
      data.function.measures.forEach(group => {
        if (group.values && Array.isArray(group.values)) {
          group.values.forEach(v => {
            const item = {
              type: 'function',
              name: v.name,
              expr: v.expr,
              desc: v.desc || '',
              group: group.name || ''
            };
            indicators.functions.push(item);
            indicators.flat.push(item);
          });
        }
      });
    }

    if (data.measure) {
      Object.entries(data.measure).forEach(([category, items]) => {
        if (Array.isArray(items)) {
          indicators.categories[category] = items.map(item => ({
            type: 'indicator',
            category,
            name: item.name,
            expr: item.expr,
            desc: item.desc || ''
          }));
          indicators.flat.push(...indicators.categories[category]);
        }
      });
    }

    return indicators;
  }

  parseStockPools([poolsResponse, hotPoolsResponse]) {
    return {
      userPools: poolsResponse.data?.pool_list || [],
      systemPools: hotPoolsResponse.data?.hot_pool_list || []
    };
  }

  getIndicator(name) {
    if (!this.cache) return null;
    return this.cache.indicators.flat.find(i => 
      i.name === name || i.expr === name
    );
  }

  getIndicatorsByCategory(category) {
    if (!this.cache) return [];
    return this.cache.indicators.categories[category] || [];
  }

  getStockPool(poolId) {
    if (!this.cache) return null;
    
    const allPools = [
      ...this.cache.stockPools.userPools,
      ...this.cache.stockPools.systemPools
    ];
    
    return allPools.find(p => p.id === poolId || p.poolid === poolId);
  }

  validateIndicator(name) {
    const indicator = this.getIndicator(name);
    return {
      valid: !!indicator,
      indicator,
      message: indicator 
        ? `Found indicator: ${indicator.name} (${indicator.type})`
        : `Indicator not found: ${name}`
    };
  }

  searchIndicators(query) {
    if (!this.cache) return [];
    
    const lowerQuery = query.toLowerCase();
    return this.cache.indicators.flat.filter(i =>
      i.name.toLowerCase().includes(lowerQuery) ||
      i.expr.toLowerCase().includes(lowerQuery) ||
      (i.desc && i.desc.toLowerCase().includes(lowerQuery))
    );
  }

  getSummary() {
    if (!this.cache) return null;
    
    return {
      timestamp: this.cache.timestamp,
      totalIndicators: this.cache.indicators.flat.length,
      functionCount: this.cache.indicators.functions.length,
      categories: Object.keys(this.cache.indicators.categories),
      userPools: this.cache.stockPools.userPools.length,
      systemPools: this.cache.stockPools.systemPools.length,
      userName: this.cache.profile?.name || 'Unknown'
    };
  }
}

export async function getParameterCache(options = {}) {
  const cache = new ParameterCache(options);
  await cache.load();
  return cache;
}