#!/usr/bin/env node

import { getParameterCache } from '../request/parameter-cache.js';
import { ParameterValidator } from '../request/parameter-validator.js';

async function main() {
  const command = process.argv[2] || 'refresh';
  
  console.log('=== Guorn Parameter Cache Tool ===\n');
  
  try {
    const cache = await getParameterCache();
    
    switch (command) {
      case 'refresh':
        await cache.refresh();
        console.log('\n✓ Parameters cached successfully');
        break;
        
      case 'summary':
        const summary = cache.getSummary();
        console.log('Cache Summary:');
        console.log(JSON.stringify(summary, null, 2));
        break;
        
      case 'indicators':
        console.log(`Total Indicators: ${cache.cache.indicators.flat.length}`);
        console.log('\nBy Category:');
        Object.entries(cache.cache.indicators.categories).forEach(([cat, items]) => {
          console.log(`  ${cat}: ${items.length} indicators`);
        });
        console.log(`\nFunctions: ${cache.cache.indicators.functions.length}`);
        break;
        
      case 'search':
        const query = process.argv[3];
        if (!query) {
          console.error('Usage: node cache-parameters.js search <query>');
          process.exit(1);
        }
        const results = cache.searchIndicators(query);
        console.log(`Found ${results.length} indicators for "${query}":`);
        results.slice(0, 20).forEach(i => {
          console.log(`  - ${i.name} (${i.type}${i.category ? '/' + i.category : ''})`);
        });
        if (results.length > 20) {
          console.log(`  ... and ${results.length - 20} more`);
        }
        break;
        
      case 'pools':
        console.log('User Stock Pools:');
        cache.cache.stockPools.userPools.forEach(p => {
          console.log(`  - ${p.name || p.pool_name} (${p.id || p.poolid})`);
        });
        console.log(`\nSystem Stock Pools (${cache.cache.stockPools.systemPools.length} total):`);
        cache.cache.stockPools.systemPools.slice(0, 10).forEach(p => {
          console.log(`  - ${p.name || p.pool_name} (${p.id || p.poolid})`);
        });
        if (cache.cache.stockPools.systemPools.length > 10) {
          console.log(`  ... and ${cache.cache.stockPools.systemPools.length - 10} more`);
        }
        break;
        
      case 'validate':
        const indicator = process.argv[3];
        if (!indicator) {
          console.error('Usage: node cache-parameters.js validate <indicator>');
          process.exit(1);
        }
        const result = cache.validateIndicator(indicator);
        console.log(JSON.stringify(result, null, 2));
        break;
        
      case 'test-validator':
        const validator = new ParameterValidator(cache);
        const testConfig = {
          name: 'Test Strategy',
          stockPool: {
            type: 'system',
            poolId: 'test-pool',
            stockLimit: 10,
            rebalanceCycle: 20
          },
          filters: [
            { indicator: 'PE', operator: '<', value: 20, enabled: true }
          ],
          rankings: [
            { indicator: '总市值', order: 'asc', weight: 1.0, enabled: true }
          ],
          tradingModel: {
            type: 1,
            maxPosition: 10,
            minPosition: 5,
            positionWeight: 'equal'
          },
          backtest: {
            startDate: '2022-01-01',
            endDate: '2025-03-28',
            benchmark: '沪深300',
            transactionCost: 0.002
          }
        };
        
        const validation = validator.validate(testConfig);
        console.log('Validation Result:');
        console.log(JSON.stringify(validation, null, 2));
        break;
        
      default:
        console.log('Available commands:');
        console.log('  refresh       - Refresh parameter cache from guorn.com');
        console.log('  summary       - Show cache summary');
        console.log('  indicators    - List all indicators');
        console.log('  search <q>    - Search indicators');
        console.log('  pools         - List stock pools');
        console.log('  validate <i>  - Validate an indicator');
        console.log('  test-validator- Test validator with sample config');
    }
  } catch (error) {
    console.error('\n✗ Error:', error.message);
    process.exit(1);
  }
}

main();