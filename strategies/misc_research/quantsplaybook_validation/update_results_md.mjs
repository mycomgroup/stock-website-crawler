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

  const results = [];
  console.log(`Fetching comprehensive results for ${backtests.length} strategies...`);

  for (const b of backtests) {
    try {
      // getBacktestResult 现在包含 extra_fields=summary
      const fullResult = await client.getBacktestResult(b.backtestId);
      const metrics = fullResult.summary || {};
      
      const totalRetVal = metrics.total_returns ?? 0;
      const annualRetVal = metrics.annualized_returns ?? 0;
      const sharpeVal = metrics.sharpe ?? 0;
      const maxDDVal = metrics.max_drawdown ?? 0;

      const totalRet = (totalRetVal * 100).toFixed(2) + '%';
      const annualRet = (annualRetVal * 100).toFixed(2) + '%';
      const sharpe = sharpeVal.toFixed(3);
      const maxDD = (maxDDVal * 100).toFixed(2) + '%';
      
      const status = fullResult.status === 'normal_exit' ? '✅ 已完成' : `⏳ ${fullResult.status}`;
      
      results.push({ 
        ...b, 
        status, 
        totalRet, 
        annualRet, 
        sharpe, 
        maxDD 
      });
    } catch (e) {
      results.push({ ...b, status: '❌ 错误', totalRet: '-', annualRet: '-', sharpe: '-', maxDD: '-' });
    }
  }

  let newContent = `# RiceQuant 3年回测 (2023-2026) 结果汇报\n`;
  newContent += `> 更新时间: ${new Date().toLocaleString()}\n\n`;
  newContent += `| 策略文件 | 收益率 | 年化 | 夏普 | 最大回撤 | 状态 | 回测ID |\n`;
  newContent += `|----------|--------|------|------|----------|------|---------|\n`;

  for (const r of results) {
    // 简单对比加粗 (收益 > 0)
    const isPositive = !r.totalRet.startsWith('-') && r.totalRet !== '0.00%';
    const retStr = isPositive ? `**${r.totalRet}**` : r.totalRet;
    const row = `| ${r.filename} | ${retStr} | ${r.annualRet} | ${r.sharpe} | ${r.maxDD} | ${r.status} | [${r.backtestId}](https://www.ricequant.com/quant/strategy/${r.strategyId}/backtest/${r.backtestId}) |\n`;
    newContent += row;
  }

  fs.writeFileSync(logFile, newContent);
  console.log(`\nSuccessfully updated ${logFile}`);
}

main().catch(console.error);
