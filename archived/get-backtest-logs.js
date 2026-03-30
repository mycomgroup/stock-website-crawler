import './load-env.js';
import { RiceQuantClient } from './request/ricequant-client.js';
import { ensureRiceQuantSession } from './browser/session-manager.js';
import fs from 'node:fs';

const WORKSPACE_ID = '640c7f5851dc7e67377e085d';

async function getBacktestLogs() {
  try {
    const credentials = {
      username: process.env.RICEQUANT_USERNAME,
      password: process.env.RICEQUANT_PASSWORD
    };
    const cookies = await ensureRiceQuantSession(credentials);
    const client = new RiceQuantClient({ cookies });
    
    // 获取最新的回测列表
    console.log('Getting backtest list...');
    const backtestListUrl = `/api/backtest/v1/workspaces/${WORKSPACE_ID}/backtests?limit=5`;
    const backtestList = await client.request(backtestListUrl, { method: 'GET' });
    
    console.log('Recent backtests:');
    if (backtestList.backtests) {
      backtestList.backtests.forEach((bt, i) => {
        console.log(`  ${i + 1}. ID: ${bt.backtest_id}, Status: ${bt.status}, Created: ${bt.ctime}`);
      });
    }
    
    // 获取最新回测的详情和日志
    if (backtestList.backtests && backtestList.backtests.length > 0) {
      const latestBacktest = backtestList.backtests[0];
      const backtestId = latestBacktest.backtest_id;
      
      console.log(`\nGetting details for backtest ${backtestId}...`);
      
      // 获取回测详情
      const detailUrl = `/api/backtest/v1/workspaces/${WORKSPACE_ID}/backtests/${backtestId}`;
      const detail = await client.request(detailUrl, { method: 'GET' });
      
      console.log('\nBacktest detail:');
      console.log(JSON.stringify(detail, null, 2).substring(0, 1000));
      
      // 获取日志
      console.log('\nGetting logs...');
      const logsUrl = `/api/backtest/v1/workspaces/${WORKSPACE_ID}/backtests/${backtestId}/logs`;
      try {
        const logs = await client.request(logsUrl, { method: 'GET' });
        console.log('\nLogs:');
        console.log(JSON.stringify(logs, null, 2).substring(0, 2000));
        
        fs.writeFileSync('backtest-logs.json', JSON.stringify(logs, null, 2));
        console.log('\n✓ Logs saved to backtest-logs.json');
      } catch (e) {
        console.log('Error getting logs:', e.message);
      }
    }
    
  } catch (error) {
    console.error('Error:', error.message);
  }
}

getBacktestLogs();
