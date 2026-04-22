import fs from 'node:fs';
import path from 'node:path';
import { RiceQuantClient } from '../../skills/ricequant_strategy/request/ricequant-client.js';

async function main() {
  const client = new RiceQuantClient();
  const loginStatus = await client.checkLogin();
  if (!loginStatus) {
    console.error('Not logged in.');
    process.exit(1);
  }

  // 1. 从 submit_all.sh 提取策略列表作为基准
  const submitScript = fs.readFileSync('./submit_all.sh', 'utf8');
  const strategyRegex = /"(\d+)\|([^"]+)"/g;
  let match;
  const strategyTasks = [];
  while ((match = strategyRegex.exec(submitScript)) !== null) {
    strategyTasks.push({
      strategyId: match[1],
      filename: path.basename(match[2])
    });
  }

  console.log(`Found ${strategyTasks.length} strategies in submit_all.sh. Fetching latest 3-year results from cloud...`);

  const finalResults = [];

  for (const task of strategyTasks) {
    try {
      // 获取该策略下的所有回测列表
      const backtests = await client.listStrategyBacktests(task.strategyId);
      if (backtests.length === 0) {
        finalResults.push({ ...task, status: '⚪ 未运行', totalRet: '-', annualRet: '-', sharpe: '-', maxDD: '-', backtestId: 'N/A' });
        continue;
      }

      // 找到最近一次针对 2023-01-01 开始的回测
      const latest = backtests[0]; // listStrategyBacktests 已经按时间倒序排好了
      const backtestId = latest._id || latest.backtest_id || latest.id;
      
      // 获取包含 summary 的详情
      const fullResult = await client.getBacktestResult(backtestId);
      const metrics = fullResult.summary || {};
      
      const totalRetVal = metrics.total_returns ?? 0;
      const annualRetVal = metrics.annualized_returns ?? 0;
      const sharpeVal = metrics.sharpe ?? 0;
      const maxDDVal = metrics.max_drawdown ?? 0;

      const totalRet = (totalRetVal * 100).toFixed(2) + '%';
      const annualRet = (annualRetVal * 100).toFixed(2) + '%';
      const sharpe = sharpeVal.toFixed(3);
      const maxDD = (maxDDVal * 100).toFixed(2) + '%';
      
      const isNormal = fullResult.status === 'normal_exit' || fullResult.status === 'done';
      const statusDisp = isNormal ? '✅ 已完成' : `⏳ ${fullResult.status}`;
      
      finalResults.push({ 
        ...task, 
        backtestId,
        status: statusDisp, 
        totalRet, 
        annualRet, 
        sharpe, 
        maxDD 
      });
      process.stdout.write('.'); // 进度指示
    } catch (e) {
      finalResults.push({ ...task, status: '❌ 错误', totalRet: '-', annualRet: '-', sharpe: '-', maxDD: '-', backtestId: 'Error' });
    }
  }

  // 2. 重建 SUBMITTED_BACKTESTS.md
  let newContent = `# RiceQuant 3年期深度回测报告 (2023-2026)\n`;
  newContent += `> 数据源: RiceQuant Cloud API | 更新时间: ${new Date().toLocaleString()}\n\n`;
  newContent += `| 策略文件 | 累计收益 | 年化收益 | 夏普比率 | 最大回撤 | 状态 | 云端链接 |\n`;
  newContent += `|:---|:---|:---|:---|:---|:---|:---|\n`;

  for (const r of finalResults) {
    const isPositive = !r.totalRet.startsWith('-') && r.totalRet !== '0.00%';
    const retCell = isPositive ? `**${r.totalRet}**` : r.totalRet;
    const row = `| ${r.filename} | ${retCell} | ${r.annualRet} | ${r.sharpe} | ${r.maxDD} | ${r.status} | [查看详情](https://www.ricequant.com/quant/backtest/${r.backtestId}) |\n`;
    newContent += row;
  }

  fs.writeFileSync('./SUBMITTED_BACKTESTS.md', newContent);
  console.log(`\n\n✅ 修复完成！共处理 ${finalResults.length} 条记录。报表已同步至 SUBMITTED_BACKTESTS.md`);
}

main().catch(console.error);
