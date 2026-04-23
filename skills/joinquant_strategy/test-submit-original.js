#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { JoinQuantStrategyClient } from './request/joinquant-strategy-client.js';
import { ensureJoinQuantSession } from './request/ensure-session.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const STRATEGY = {
  name: 'A_原版_Release_V1_测试',
  file: path.join(__dirname, '../../strategies/rfscore_offensive/rfscore7_pb10_release_v1.py'),
};

const BACKTEST_CONFIG = {
  startTime: '2024-01-01',
  endTime: '2025-01-01',
  baseCapital: '1000000',
  frequency: 'day'
};

async function main() {
  console.log('提交原始版本测试（1年回测）\n');
  
  await ensureJoinQuantSession({ headed: false, headless: true });
  const client = new JoinQuantStrategyClient();
  
  const algorithmId = '801d56e162b037ed1a6e0ba5d26ff092';
  const context = await client.getStrategyContext(algorithmId);
  
  const code = fs.readFileSync(STRATEGY.file, 'utf8');
  console.log('上传策略...');
  await client.saveStrategy(algorithmId, 'RFScore7_Original_Test', code, context);
  
  console.log('运行回测: ' + BACKTEST_CONFIG.startTime + ' ~ ' + BACKTEST_CONFIG.endTime);
  const buildResult = await client.runBacktest(algorithmId, '', BACKTEST_CONFIG, context);
  const backtestId = buildResult.backtestId;
  console.log('回测ID: ' + backtestId);
  
  console.log('等待回测完成...');
  let retries = 0;
  const maxRetries = 60;
  
  while (retries < maxRetries) {
    await new Promise(resolve => setTimeout(resolve, 2000));
    const result = await client.getBacktestResult(backtestId, context);
    
    if (result && result.results) {
      const r = result.results;
      console.log('\n回测完成!');
      console.log('年化收益: ' + (r.annualized_returns * 100).toFixed(2) + '%');
      console.log('夏普比率: ' + r.sharpe.toFixed(3));
      console.log('最大回撤: ' + (r.max_drawdown * 100).toFixed(2) + '%');
      return;
    }
    
    retries++;
    if (retries % 15 === 0) {
      console.log('等待中... ' + Math.floor(retries * 2 / 60) + '分钟');
    }
  }
  
  console.log('超时，获取日志...');
  const log = await client.getLog(backtestId);
  const logArr = log.data?.logArr || [];
  console.log(logArr.slice(-30).join('\n'));
}

main().catch(console.error);
