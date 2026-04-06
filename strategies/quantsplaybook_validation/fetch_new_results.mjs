#!/usr/bin/env node
/**
 * 从 rq_strategy_mapping.json 获取新策略的回测结果并更新 Markdown
 */
import fs from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import { RiceQuantClient } from '../../skills/ricequant_strategy/request/ricequant-client.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const MAPPING_FILE = path.join(__dirname, 'rq_strategy_mapping.json');
const OUTPUT_FILE = path.join(__dirname, 'NEW_STRATEGY_RESULTS.md');

async function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function main() {
  const client = new RiceQuantClient();
  const loginStatus = await client.checkLogin();
  if (!loginStatus) {
    console.error('Not logged in.');
    process.exit(1);
  }
  console.log('Logged in as:', loginStatus.fullname || loginStatus.phone);

  const mapping = JSON.parse(fs.readFileSync(MAPPING_FILE, 'utf8'));
  const entries = Object.entries(mapping);
  console.log(`Fetching results for ${entries.length} strategies...`);

  const results = [];

  for (const [filename, data] of entries) {
    const { strategyId, backtestId } = data;
    if (!backtestId) {
      results.push({ filename, strategyId, backtestId, status: '❌ 无backtestId', totalRet: '-', annualRet: '-', sharpe: '-', maxDD: '-' });
      continue;
    }

    try {
      const result = await client.getBacktestResult(backtestId);
      const status = result.status;
      const metrics = result.summary || {};

      if (status === 'normal_exit' || status === 'done' || status === 'finished') {
        const totalRetVal = metrics.total_returns ?? 0;
        const annualRetVal = metrics.annualized_returns ?? 0;
        const sharpeVal = metrics.sharpe ?? 0;
        const maxDDVal = metrics.max_drawdown ?? 0;

        results.push({
          filename,
          strategyId,
          backtestId,
          status: '✅ 完成',
          totalRet: (totalRetVal * 100).toFixed(2) + '%',
          annualRet: (annualRetVal * 100).toFixed(2) + '%',
          sharpe: sharpeVal.toFixed(3),
          maxDD: (maxDDVal * 100).toFixed(2) + '%'
        });
        console.log(`✓ ${filename}: ret=${(totalRetVal * 100).toFixed(2)}%, sharpe=${sharpeVal.toFixed(3)}`);
      } else if (status === 'running') {
        results.push({ filename, strategyId, backtestId, status: '⏳ 运行中', totalRet: '-', annualRet: '-', sharpe: '-', maxDD: '-' });
        console.log(`⏳ ${filename}: running`);
      } else {
        results.push({ filename, strategyId, backtestId, status: `❌ ${status}`, totalRet: '-', annualRet: '-', sharpe: '-', maxDD: '-' });
        console.log(`❌ ${filename}: ${status}`);
      }
    } catch (e) {
      results.push({ filename, strategyId, backtestId, status: `⚠️ ${e.message.slice(0, 50)}`, totalRet: '-', annualRet: '-', sharpe: '-', maxDD: '-' });
      console.log(`⚠️ ${filename}: ${e.message.slice(0, 100)}`);
    }

    // 避免请求过快
    await sleep(500);
  }

  // 生成 Markdown
  let content = `# 新策略回测结果\n`;
  content += `> 更新时间: ${new Date().toLocaleString()}\n\n`;
  content += `| 策略文件 | StrategyID | BacktestID | 收益率 | 年化 | 夏普 | 最大回撤 | 状态 |\n`;
  content += `|----------|------------|------------|--------|------|------|----------|------|\n`;

  for (const r of results) {
    const isPositive = r.totalRet !== '-' && !r.totalRet.startsWith('-') && r.totalRet !== '0.00%';
    const retStr = isPositive ? `**${r.totalRet}**` : r.totalRet;
    const btLink = r.backtestId ? `[${r.backtestId}](https://www.ricequant.com/quant/backtest/${r.backtestId})` : '-';
    content += `| ${r.filename} | ${r.strategyId || '-'} | ${btLink} | ${retStr} | ${r.annualRet} | ${r.sharpe} | ${r.maxDD} | ${r.status} |\n`;
  }

  fs.writeFileSync(OUTPUT_FILE, content);
  console.log(`\nResults saved to ${OUTPUT_FILE}`);

  // 也更新 SUBMITTED_BACKTESTS.md（合并新策略）
  const existingContent = fs.existsSync(path.join(__dirname, 'SUBMITTED_BACKTESTS.md'))
    ? fs.readFileSync(path.join(__dirname, 'SUBMITTED_BACKTESTS.md'), 'utf8')
    : '';

  let newContent = existingContent + '\n\n## 新策略回测结果\n' + content.split('\n\n## 新策略回测结果\n')[1];

  fs.writeFileSync(path.join(__dirname, 'SUBMITTED_BACKTESTS.md'), newContent);
  console.log('Updated SUBMITTED_BACKTESTS.md');
}

main().catch(console.error);
