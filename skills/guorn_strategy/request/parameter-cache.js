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

  /**
   * Resolves an indicator ID from a friendly name or qualified name.
   * Supports:
   * 1. Raw ID: 0.M...
   * 2. UI Name: 市盈率
   * 3. Qualified Name / Middle Name: 股票每日指标_市盈率
   * 4. Synonyms: PE -> 市盈率
   * 5. English names: pe_ttm -> 市盈率
   */
  resolveId(nameOrId) {
    if (!nameOrId) return null;

    // 1. Check if it's already a raw ID
    if (/^0\.[M|D]\./.test(nameOrId)) {
      return nameOrId;
    }

    // 2. English to Chinese mapping (for autoresearch configs)
    const englishToChinese = {
      'pe_ttm': '市盈率',
      'pe': '市盈率',
      'pb': '市净率',
      'roe': '净资产收益率',
      'roa': '总资产收益率',
      'ps': '市销率',
      'pcf': '市现率',
      'gross_profit_margin': '销售毛利率',
      'net_profit_margin': '销售净利率',
      'debt_to_asset': '资产负债率',
      'debt_to_equity': '负债资产率',
      'current_ratio': '流动比率',
      'quick_ratio': '速动比率',
      'turnover_rate': '当日换手率',
      'market_cap': '总市值',
      'circulating_market_cap': '流通市值',
      // Additional mappings for autoresearch
      'dividend_yield': '股息率',
      'dividend_yield_ttm': '股息率TTM',
      'revenue_growth': '营业收入增长',
      'profit_growth': '净利润增长',
      'operating_profit_growth': '营业利润增长',
      'eps': '每股收益',
      'eps_growth': '净利润增长',
      'net_profit_margin': '销售净利率',
      'gross_profit_margin': '销售毛利率',
      'operating_profit_margin': '营业利润率',
      'roe_ex': '扣非净资产收益率',
      'pb_ex_goodwill': '扣除商誉市净率',
      'pe_static': '静态市盈率',
      'pe_dynamic': '动态市盈率',
      'pe_ex': '扣非市盈率',
      'turnover_5d': '5日换手率',
      'turnover_20d': '20日换手率',
    };
    
    const chineseName = englishToChinese[nameOrId.toLowerCase()];
    if (chineseName) {
      nameOrId = chineseName;
    }

    // 3. Load mapping if not already in cache (optimized for resolution)
    if (!this.mappingData) {
      try {
        const mappingPath = path.join(path.dirname(this.cacheFile), '..', 'indicator_mapping.json');
        if (fs.existsSync(mappingPath)) {
          this.mappingData = JSON.parse(fs.readFileSync(mappingPath, 'utf8'));
        }
      } catch (e) {
        console.warn('Mapping data not available:', e.message);
      }
    }

    if (this.mappingData && this.mappingData.indicators) {
      const indicators = this.mappingData.indicators;
      
      // 3.1 Exact name match
      let match = indicators.find(i => i.name === nameOrId);
      if (match) return match.id;

      // 3.2 Middle name match (qualified name)
      match = indicators.find(i => i.middle_name === nameOrId);
      if (match) return match.id;

      // 3.3 Synonym match (Basic PE/ROE/etc)
      const synonyms = {
        'PE': '市盈率',
        'PB': '市净率',
        'ROE': '净资产收益率',
        'PS': '市销率',
        'MCAP': '总市值'
      };
      const resolvedName = synonyms[nameOrId.toUpperCase()];
      if (resolvedName) {
        match = indicators.find(i => i.name === resolvedName);
        if (match) return match.id;
      }
    }

    // 4. Fallback to cache.indicators
    const cached = this.getIndicator(nameOrId);
    if (cached && (cached.expr || cached.id)) {
      return cached.expr || cached.id;
    }

    return nameOrId; // Return original if not resolvable
  }

  /**
   * Resolves a stock pool ID from a name.
   */
  resolvePoolId(nameOrId) {
    if (!nameOrId) return nameOrId;
    if (nameOrId.startsWith('1.P.')) return nameOrId;

    if (!this.cache || !this.cache.stockPools) return nameOrId;

    const allPools = [
      ...this.cache.stockPools.userPools,
      ...this.cache.stockPools.systemPools
    ];

    const match = allPools.find(p => p.name === nameOrId);
    return match ? match.id : nameOrId;
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