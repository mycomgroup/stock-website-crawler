import './load-env.js';
import { RiceQuantClient } from './request/ricequant-client.js';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const OUTPUT_DIR = path.join(__dirname, 'data');

async function runBacktest(codeFile, startDate, endDate, capital) {
  const code = fs.readFileSync(codeFile, 'utf8');
  const strategyName = path.basename(codeFile, '.py');
  
  console.log('\n' + '='.repeat(60));
  console.log('RiceQuant Backtest');
  console.log('='.repeat(60));
  console.log('Strategy:', strategyName);
  console.log('Period:', startDate, '-', endDate);
  console.log('Capital:', capital);
  console.log('='.repeat(60) + '\n');
  
  const client = new RiceQuantClient();
  const workspaceId = await client.getWorkspaceId();
  let strategyId = null;
  let backtestId = null;
  
  try {
    // Step 1: 检查登录
    console.log('1. Checking login...');
    const loginStatus = await client.checkLogin();
    if (loginStatus.code !== 0) {
      console.log('   ❌ Not logged in! Run: node auto-login.js');
      return null;
    }
    console.log('   ✓ Logged in');
    
    // Step 2: 创建策略
    console.log('\n2. Creating strategy...');
    const createResult = await client.request(
      `/api/strategy/v1/workspaces/${workspaceId}/strategies`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          title: `Backtest_${Date.now()}`,
          code: code,
          metadata: { strategy_type: 'general', wizard_option: null },
          config: {
            stock_init_cash: parseInt(capital),
            futures_init_cash: 0,
            bond_init_cash: 0,
            start_date: startDate,
            end_date: endDate,
            frequency: 'day',
            benchmark: '000300.XSHG'
          },
          account_type: 'stock',
          permission: 'write'
        })
      }
    );
    
    strategyId = createResult.strategy_id || createResult.id;
    if (!strategyId) {
      console.log('   ❌ Create failed:', JSON.stringify(createResult));
      return null;
    }
    console.log('   ✓ Created:', strategyId);
    
    // Step 3: 运行回测
    console.log('\n3. Starting backtest...');
    const runResult = await client.request(
      `/api/backtest/v1/workspaces/${workspaceId}/backtests`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          strategy_id: strategyId,
          code: Buffer.from(code).toString('base64'),
          config: {
            start_date: startDate,
            end_date: endDate,
            stock_init_cash: parseInt(capital),
            futures_init_cash: 0,
            bond_init_cash: 0,
            frequency: 'day',
            benchmark: '000300.XSHG',
            commission_multiplier: 1,
            dividend_reinvestment: false
          }
        })
      }
    );
    
    backtestId = typeof runResult === 'string' ? runResult.replace(/"/g, '') : (runResult.backtestId || runResult.backtest_id);
    if (!backtestId) {
      console.log('   ❌ Run failed:', JSON.stringify(runResult));
      return null;
    }
    console.log('   ✓ Started:', backtestId);
    
    // Step 4: 等待完成
    console.log('\n4. Waiting...');
    let status = 'running';
    let attempts = 0;
    
    while (status === 'running' && attempts < 60) {
      await new Promise(r => setTimeout(r, 3000));
      attempts++;
      
      const result = await client.request(
        `/api/backtest/v1/workspaces/${workspaceId}/backtests/${backtestId}`
      );
      status = result.status;
      
      process.stdout.write(`   [${attempts}] ${status} (${(result.progress * 100).toFixed(0)}%)\r`);
      
      if (status === 'error_exit' || status === 'failed') {
        console.log('\n   ❌ Backtest error');
        break;
      }
    }
    console.log('\n   ✓ Status:', status);
    
    // Step 5: 获取结果
    console.log('\n5. Fetching results...');
    
    const [info, risk] = await Promise.all([
      client.request(`/api/backtest/v1/workspaces/${workspaceId}/backtests/${backtestId}`),
      client.request(`/api/backtest/v1/workspaces/${workspaceId}/backtests/${backtestId}/risk`).catch(() => null)
    ]);
    
    // 获取日志
    const logs = await client.request(
      `/api/backtest/v1/workspaces/${workspaceId}/backtests/${backtestId}/logs`
    ).catch(() => null);
    
    if (logs && logs.logs) {
      console.log('\n   === LOGS ===');
      logs.logs.slice(-20).forEach(log => {
        console.log('   ', log);
      });
    }
    
    // 保存结果
    const timestamp = Date.now();
    const resultFile = path.join(OUTPUT_DIR, `result-${strategyName}-${timestamp}.json`);
    const resultData = {
      strategyId,
      backtestId,
      strategyName,
      startDate,
      endDate,
      capital,
      status,
      info,
      risk,
      timestamp: new Date().toISOString()
    };
    fs.writeFileSync(resultFile, JSON.stringify(resultData, null, 2));
    console.log('\n   Result saved:', resultFile);
    
    // 打印结果
    console.log('\n' + '='.repeat(60));
    console.log('RESULTS');
    console.log('='.repeat(60));
    
    if (risk) {
      console.log('Total Return:', ((risk.total_returns || 0) * 100).toFixed(2), '%');
      console.log('Annual Return:', ((risk.annual_returns || 0) * 100).toFixed(2), '%');
      console.log('Max Drawdown:', ((risk.max_drawdown || 0) * 100).toFixed(2), '%');
      console.log('Sharpe:', risk.sharpe || 'N/A');
      console.log('Alpha:', (risk.alpha || 0).toFixed(4));
      console.log('Beta:', (risk.beta || 0).toFixed(4));
    } else {
      console.log('(No risk data)');
    }
    
    if (info.exception) {
      console.log('\nException:', info.exception);
    }
    
    console.log('='.repeat(60));
    
    return resultData;
    
  } catch (e) {
    console.error('\n❌ Error:', e.message);
    return null;
  }
}

const args = process.argv.slice(2);

if (args.length < 1) {
  console.log('Usage: node test-backtest.js <codeFile> [startDate] [endDate] [capital]');
  console.log('Example: node test-backtest.js strategy.py 2023-01-01 2024-06-30 100000');
  process.exit(0);
}

runBacktest(
  args[0],
  args[1] || '2023-01-01',
  args[2] || '2024-06-30',
  args[3] || '100000'
);