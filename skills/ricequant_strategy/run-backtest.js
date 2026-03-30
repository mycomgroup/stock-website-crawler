import './load-env.js';
import { RiceQuantClient } from './request/ricequant-client.js';
import { ensureRiceQuantSession } from './browser/session-manager.js';
import fs from 'node:fs';

const WORKSPACE_ID = '640c7f5851dc7e67377e085d';

async function createAndRunBacktest() {
  console.log('=== RiceQuant Create Strategy & Run Backtest ===\n');
  
  try {
    // 1. 确保会话
    console.log('1. Ensuring session...');
    const credentials = {
      username: process.env.RICEQUANT_USERNAME,
      password: process.env.RICEQUANT_PASSWORD
    };
    const cookies = await ensureRiceQuantSession(credentials);
    console.log(`✓ Session ready (${cookies.length} cookies)`);
    
    const client = new RiceQuantClient({ cookies });
    
    // 2. 读取策略代码
    console.log('\n2. Loading strategy code...');
    const strategyCode = fs.readFileSync('strategy_rfscore_v2.py', 'utf8');
    console.log(`✓ Strategy loaded (${strategyCode.length} chars)`);
    
    // 3. 创建新策略
    console.log('\n3. Creating new strategy...');
    const createUrl = `/api/strategy/v1/workspaces/${WORKSPACE_ID}/strategies`;
    
    const strategyData = {
      title: 'RFScore Pure Offensive',
      code: strategyCode,
      metadata: {
        strategy_type: 'general',
        wizard_option: null
      },
      config: {
        stock_init_cash: 1000000,
        futures_init_cash: 0,
        bond_init_cash: 0,
        start_date: '2022-01-01',
        end_date: '2025-03-28',
        frequency: 'day',
        commission_multiplier: 1,
        benchmark: '000300.XSHG',
        dividend_reinvestment: false,
        enable_profiler: false,
        enable_short_sell: false,
        margin_multiplier: 1,
        matching_type: 'current_bar',
        slippage: 0,
        slippage_model: 'PriceRatioSlippage',
        volume_limit: false,
        volume_percent: 0.25
      },
      account_type: 'stock',
      permission: 'write'
    };
    
    try {
      const createResult = await client.request(createUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(strategyData)
      });
      
      console.log('✓ Strategy created');
      console.log('Result:', JSON.stringify(createResult).substring(0, 300));
      
      const strategyId = createResult.strategy_id || createResult.id;
      console.log(`Strategy ID: ${strategyId}`);
      
      // 4. 运行回测
      console.log('\n4. Running backtest...');
      const backtestUrl = `/api/backtest/v1/workspaces/${WORKSPACE_ID}/backtests`;
      
      const backtestData = {
        strategy_id: strategyId,
        config: {
          start_date: '2022-01-01',
          end_date: '2025-03-28',
          stock_init_cash: 1000000,
          futures_init_cash: 0,
          bond_init_cash: 0,
          frequency: 'day',
          benchmark: '000300.XSHG',
          commission_multiplier: 1,
          dividend_reinvestment: false,
          enable_profiler: false,
          enable_short_sell: false,
          margin_multiplier: 1,
          matching_type: 'current_bar',
          slippage: 0,
          slippage_model: 'PriceRatioSlippage',
          volume_limit: false,
          volume_percent: 0.25
        }
      };
      
      const backtestResult = await client.request(backtestUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(backtestData)
      });
      
      console.log('✓ Backtest started');
      console.log('Backtest result:', JSON.stringify(backtestResult).substring(0, 300));
      
      // 处理返回的回测ID
      let backtestId;
      if (typeof backtestResult === 'string') {
        backtestId = backtestResult.replace(/"/g, '');  // 移除引号
      } else {
        backtestId = backtestResult.backtest_id || backtestResult.id || backtestResult;
      }
      console.log(`Backtest ID: ${backtestId}`);
      
      // 5. 轮询等待回测完成
      console.log('\n5. Waiting for backtest to complete...');
      let isComplete = false;
      let attempts = 0;
      const maxAttempts = 120; // 最多等待10分钟
      
      while (!isComplete && attempts < maxAttempts) {
        await new Promise(resolve => setTimeout(resolve, 5000));
        attempts++;
        
        try {
          const statusUrl = `/api/backtest/v1/workspaces/${WORKSPACE_ID}/backtests/${backtestId}`;
          const status = await client.request(statusUrl, { method: 'GET' });
          
          const backtestStatus = status.status || status.backtest?.status || 'unknown';
          const progress = status.progress || status.backtest?.progress || 0;
          
          console.log(`  [${attempts}/${maxAttempts}] Status: ${backtestStatus}, Progress: ${progress}%`);
          
          if (backtestStatus === 'finished' || backtestStatus === 'completed' || backtestStatus === 'success') {
            isComplete = true;
            console.log('\n✓ Backtest completed!');
          } else if (backtestStatus === 'failed' || backtestStatus === 'error') {
            throw new Error(`Backtest failed: ${JSON.stringify(status)}`);
          }
        } catch (err) {
          console.log(`  [${attempts}] Error checking status: ${err.message}`);
        }
      }
      
      if (!isComplete) {
        console.log('\n⚠ Backtest did not complete within timeout');
      }
      
      // 6. 获取回测结果
      console.log('\n6. Fetching backtest results...');
      try {
        const resultUrl = `/api/backtest/v1/workspaces/${WORKSPACE_ID}/backtests/${backtestId}`;
        const result = await client.request(resultUrl, { method: 'GET' });
        
        fs.writeFileSync('backtest-result.json', JSON.stringify(result, null, 2));
        console.log('✓ Result saved to backtest-result.json');
        console.log('\nResult summary:');
        console.log(JSON.stringify(result, null, 2).substring(0, 1000));
      } catch (err) {
        console.log('Error fetching result:', err.message);
      }
      
    } catch (err) {
      console.log('Error creating strategy:', err.message);
      if (err.message.includes('400')) {
        console.log('\nTrying alternative approach...');
        
        // 列出现有策略
        const strategies = await client.listStrategies();
        console.log(`\nExisting strategies: ${strategies.length}`);
        strategies.forEach((s, i) => {
          console.log(`  ${i + 1}. ${s.id} - ${s.name}`);
        });
      }
    }
    
  } catch (error) {
    console.error('\n✗ Error:', error.message);
    console.error(error.stack);
  }
}

createAndRunBacktest();
