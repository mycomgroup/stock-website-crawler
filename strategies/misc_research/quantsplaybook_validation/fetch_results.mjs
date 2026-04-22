import fs from 'node:fs';
import { RiceQuantClient } from '../../skills/ricequant_strategy/request/ricequant-client.js';

async function main() {
  const client = new RiceQuantClient();
  const loginStatus = await client.checkLogin();
  if (!loginStatus) {
    console.error('Not logged in.');
    process.exit(1);
  }

  const logFile = './SUBMITTED_BACKTESTS.md';
  const content = fs.readFileSync(logFile, 'utf8');
  
  const regex = /\| ([^|]+) \| ([^|]+) \| ([^|]+) \|/g;
  let match;
  const backtests = [];
  while ((match = regex.exec(content)) !== null) {
    const filename = match[1].trim();
    const strategyId = match[2].trim();
    const backtestId = match[3].trim();
    if (backtestId && backtestId !== '回测ID' && backtestId !== '---------') {
      backtests.push({ filename, strategyId, backtestId });
    }
  }

  console.log(`Checking ${backtests.length} backtests...`);
  console.log('| 策略文件 | 收益率 | 年化 | 夏普 | 最大回撤 | 状态 |');
  console.log('|----------|--------|------|------|----------|------|');

  for (const b of backtests) {
    try {
      const result = await client.getBacktestResult(b.backtestId);
      const status = result.status;
      
      // RiceQuant use 'normal_exit' or 'done' for successful runs
      if (status === 'normal_exit' || status === 'done') {
        const risk = await client.getBacktestRisk(b.backtestId);
        if (risk && (risk.total_returns !== undefined)) {
          const totalRet = (risk.total_returns * 100).toFixed(2) + '%';
          const annualRet = (risk.annualized_returns * 100).toFixed(2) + '%';
          const sharpe = (risk.sharpe || 0).toFixed(3);
          const maxDD = (risk.max_drawdown * 100).toFixed(2) + '%';
          console.log(`| ${b.filename} | ${totalRet} | ${annualRet} | ${sharpe} | ${maxDD} | ✅ 完成 |`);
        } else {
          // Normal exit but no risk data usually means no trades or zero returns
          console.log(`| ${b.filename} | 0.00% | 0.00% | 0.000 | 0.00% | ⚪ 无交易 |`);
        }
      } else if (status === 'running') {
        console.log(`| ${b.filename} | - | - | - | - | ⏳ 运行中 |`);
      } else {
        console.log(`| ${b.filename} | - | - | - | - | ❌ ${status} |`);
      }
    } catch (e) {
      console.log(`| ${b.filename} | - | - | - | - | ⚠️ 错误 |`);
    }
  }
}

main().catch(console.error);
