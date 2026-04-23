#!/usr/bin/env node
/**
 * 并行提交所有用户策略回测
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { JoinQuantStrategyClient } from './request/joinquant-strategy-client.js';
import { ensureJoinQuantSession } from './request/ensure-session.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// 用户新建的策略列表
const USER_STRATEGIES = [
  {
    name: 'User_Attr_C_Pure_RFScore',
    algorithmId: 'dacacfad48acfd35c72a4a0f6517c519',
    desc: '纯RFScore7质量因子（剥离PB过滤）',
    purpose: '验证RFScore7单独贡献',
    codeFile: 'attribution_c_pure_rfscore.py'
  },
  {
    name: 'User_Attr_D_No_Risk_Control',
    algorithmId: '5c9e4225112d5504433a6231dea8e0a3',
    desc: '无动态风控（始终满仓20只）',
    purpose: '验证动态风控贡献',
    codeFile: 'attribution_d_no_risk_control.py'
  },
  {
    name: 'User_Attr_E_PB20_Loose',
    algorithmId: '50a2ce8b72bc5046cd4b9495379935a6',
    desc: 'PB20%宽松版（vs PB10%严格版）',
    purpose: '验证PB严格度是否过拟合',
    codeFile: 'attribution_e_pb20_loose.py'
  }
];

const BACKTEST_CONFIG = {
  startTime: '2020-01-01',
  endTime: '2025-12-31',
  baseCapital: '1000000',
  frequency: 'day'
};

async function submitBacktest(client, strategy) {
  console.log(`\n提交: ${strategy.name}`);
  
  try {
    const context = await client.getStrategyContext(strategy.algorithmId);
    const code = fs.readFileSync(path.join(__dirname, strategy.codeFile), 'utf8');
    
    const buildResult = await client.runBacktest(
      strategy.algorithmId, 
      code, 
      BACKTEST_CONFIG, 
      context
    );
    
    const backtestId = buildResult.backtestId;
    console.log(`✓ ${strategy.name}`);
    console.log(`  回测ID: ${backtestId}`);
    console.log(`  链接: https://www.joinquant.com/algorithm/backtest?backtestId=${backtestId}`);
    
    return {
      success: true,
      name: strategy.name,
      backtestId: backtestId,
      algorithmId: strategy.algorithmId
    };
  } catch (err) {
    console.error(`✗ ${strategy.name} 提交失败:`, err.message);
    return {
      success: false,
      name: strategy.name,
      error: err.message
    };
  }
}

async function main() {
  console.log('='.repeat(70));
  console.log('并行提交用户策略回测');
  console.log('='.repeat(70));
  
  console.log('\n策略列表:');
  USER_STRATEGIES.forEach((s, i) => {
    console.log(`  ${i + 1}. ${s.name} (${s.algorithmId})`);
  });
  
  console.log('\n检查登录状态...');
  await ensureJoinQuantSession({ headed: false, headless: true });
  
  const client = new JoinQuantStrategyClient();
  
  console.log('\n并行提交所有回测...\n');
  
  // 并行提交所有回测
  const results = await Promise.all(
    USER_STRATEGIES.map(s => submitBacktest(client, s))
  );
  
  console.log('\n' + '='.repeat(70));
  console.log('提交结果');
  console.log('='.repeat(70));
  
  results.forEach((r, i) => {
    if (r.success) {
      console.log(`${i + 1}. ✓ ${r.name}`);
      console.log(`   回测ID: ${r.backtestId}`);
      console.log(`   链接: https://www.joinquant.com/algorithm/backtest?backtestId=${r.backtestId}`);
    } else {
      console.log(`${i + 1}. ✗ ${r.name} - ${r.error}`);
    }
  });
  
  // 保存结果
  const outputPath = path.join(__dirname, 'output', `parallel-submit-${Date.now()}.json`);
  fs.mkdirSync(path.dirname(outputPath), { recursive: true });
  fs.writeFileSync(outputPath, JSON.stringify(results, null, 2));
  console.log(`\n结果已保存: ${outputPath}`);
  
  console.log('\n' + '='.repeat(70));
  console.log('所有回测已提交！');
  console.log('='.repeat(70));
  console.log('\n请访问以下链接查看结果:');
  results.filter(r => r.success).forEach(r => {
    console.log(`  ${r.name}:`);
    console.log(`    https://www.joinquant.com/algorithm/backtest?backtestId=${r.backtestId}`);
  });
}

main().catch(err => {
  console.error('提交失败:', err);
  process.exit(1);
});
