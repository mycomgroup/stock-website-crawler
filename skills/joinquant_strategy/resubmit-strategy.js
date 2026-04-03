#!/usr/bin/env node
import fs from 'node:fs';
import { JoinQuantStrategyClient } from './request/joinquant-strategy-client.js';
import { ensureJoinQuantSession } from './request/ensure-session.js';

const STRATEGY_FILE = '/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy/rfscore7_pb10_optimized.py';
const ALGORITHM_ID = '309ebf2421687fcf4d41223fdec01f2c';

async function main() {
  console.log('重新提交优化策略\n');
  
  await ensureJoinQuantSession({ headed: false, headless: true });
  const client = new JoinQuantStrategyClient();
  
  const context = await client.getStrategyContext(ALGORITHM_ID);
  console.log('策略ID:', ALGORITHM_ID);
  
  const code = fs.readFileSync(STRATEGY_FILE, 'utf8');
  console.log('代码长度:', code.length);
  console.log('代码前100字符:', code.slice(0, 100));
  
  console.log('\n保存策略...');
  const result = await client.saveStrategy(
    ALGORITHM_ID,
    'RFScore7_PB10_Optimized_V2',
    code,
    context
  );
  
  console.log('保存结果:', JSON.stringify(result, null, 2));
  
  console.log('\n验证策略已保存:');
  const verify = await client.getStrategyContext(ALGORITHM_ID);
  console.log('策略名称:', verify.name);
  
  console.log('\n✓ 策略已保存');
  console.log('\n请在网页查看:');
  console.log(`https://www.joinquant.com/algorithm/index/edit?algorithmId=${ALGORITHM_ID}`);
}

main().catch(console.error);