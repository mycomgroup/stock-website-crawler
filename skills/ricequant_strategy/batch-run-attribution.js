#!/usr/bin/env node
import fs from 'node:fs';

const STRATEGY_ID = '2416771';
const STRATEGIES = [
  {
    name: 'A_纯小市值',
    file: '/Users/fengzhi/Downloads/git/testlixingren/skills/ricequant_strategy/attribution_a_working.py',
    desc: '纯小市值因子：市值最小前20只，月度调仓'
  },
  {
    name: 'B_小市值事件',
    file: '/Users/fengzhi/Downloads/git/testlixingren/skills/ricequant_strategy/attribution_b_smallcap_event_rq.py',
    desc: '小市值+事件：市值5-15亿+首板低开，次日退出'
  },
  {
    name: 'C_纯事件',
    file: '/Users/fengzhi/Downloads/git/testlixingren/skills/ricequant_strategy/attribution_c_event_rq.py',
    desc: '纯事件：全市场首板低开，次日退出'
  }
];

const BACKTEST_CONFIG = {
  start: '2024-01-01',
  end: '2024-06-30',
  capital: '100000'
};

console.log('============================================================');
console.log('小市值因子 vs 事件策略归因分析 - 批量回测');
console.log('============================================================');
console.log('策略数量:', STRATEGIES.length);
console.log('回测期间:', BACKTEST_CONFIG.start, '~', BACKTEST_CONFIG.end);
console.log('初始资金:', BACKTEST_CONFIG.capital);
console.log('============================================================\n');

async function runBacktest(strategy) {
  const { execSync } = await import('child_process');
  
  console.log(`\n=== [${strategy.name}] ===`);
  console.log(`描述: ${strategy.desc}\n`);
  
  const cmd = `node run-skill.js --id ${STRATEGY_ID} --file ${strategy.file} --start ${BACKTEST_CONFIG.start} --end ${BACKTEST_CONFIG.end} --capital ${BACKTEST_CONFIG.capital}`;
  
  try {
    execSync(cmd, { 
      stdio: 'inherit',
      cwd: '/Users/fengzhi/Downloads/git/testlixingren/skills/ricequant_strategy'
    });
    console.log(`\n✓ ${strategy.name} 回测完成`);
  } catch (error) {
    console.error(`\n✗ ${strategy.name} 回测失败:`, error.message);
  }
}

async function main() {
  for (const strategy of STRATEGIES) {
    await runBacktest(strategy);
    await new Promise(resolve => setTimeout(resolve, 3000));
  }
  
  console.log('\n\n============================================================');
  console.log('所有策略回测完成！');
  console.log('============================================================');
  console.log('\n请查看上方的回测结果，或访问 RiceQuant 平台查看详细报告：');
  console.log('https://www.ricequant.com/quant/strategys');
}

main().catch(console.error);