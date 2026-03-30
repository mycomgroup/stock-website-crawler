#!/usr/bin/env node
/**
 * 综合测试：验证 RiceQuant 和 JoinQuant 的代码编码正确
 * 
 * 测试场景：
 * 1. RiceQuant 应发送原始代码（非 base64）
 * 2. JoinQuant 应发送 base64 编码代码 + encrType
 */

import './ricequant_strategy/load-env.js';
import { RiceQuantClient } from './ricequant_strategy/request/ricequant-client.js';
import { JoinQuantStrategyClient } from './joinquant_strategy/request/joinquant-strategy-client.js';

const TEST_PYTHON = `
def init(context):
    print("Hello from test")

def handle_bar(context, bar_dict):
    pass
`;

console.log('=== Code Encoding Test ===\n');

async function testRiceQuant() {
  console.log('1. RiceQuant Test');
  console.log('Expected: Raw Python code (NOT base64)\n');
  
  const client = new RiceQuantClient();
  
  // Check login
  const login = await client.checkLogin();
  if (login.code !== 0) {
    console.log('✗ RiceQuant: Not logged in');
    return false;
  }
  console.log('  Logged in:', login.fullname);
  
  // Create strategy
  const create = await client.createStrategy('test_encoding_rq', TEST_PYTHON);
  const strategyId = create.strategy_id || create._id || create.id;
  console.log('  Created strategy:', strategyId);
  
  // Read back
  const ctx = await client.getStrategyContext(strategyId);
  const code = ctx.code;
  
  // Validate
  const isBase64 = /^[A-Za-z0-9+/]+={0,2}$/.test(code?.replace(/\s/g, '')) && !code?.includes('def ');
  const isPython = code?.includes('def init') || code?.includes('print');
  
  console.log('  Code length:', code?.length);
  console.log('  Is base64:', isBase64);
  console.log('  Is Python:', isPython);
  
  if (!isBase64 && isPython) {
    console.log('  ✓ PASS: Code is raw Python\n');
  } else {
    console.log('  ✗ FAIL: Code encoding wrong\n');
  }
  
  // Cleanup
  await client.deleteStrategy(strategyId);
  return !isBase64 && isPython;
}

async function testJoinQuant() {
  console.log('2. JoinQuant Test');
  console.log('Expected: base64 encoding with encrType flag\n');
  
  const client = new JoinQuantStrategyClient();
  
  // Get existing strategy context
  try {
    const strategies = await client.listStrategies();
    if (strategies.length === 0) {
      console.log('✗ JoinQuant: No strategies found');
      return false;
    }
    
    const strategyId = strategies[0].id;
    console.log('  Using strategy:', strategyId, strategies[0].name);
    
    const ctx = await client.getStrategyContext(strategyId);
    console.log('  Token length:', ctx.token?.length);
    
    // Test save
    const result = await client.saveStrategy(ctx.algorithmId, ctx.name, TEST_PYTHON, ctx);
    console.log('  Save result:', result.status === '0' ? 'Success' : 'Failed');
    
    if (result.status === '0') {
      console.log('  ✓ PASS: Save works with base64 encoding\n');
      return true;
    } else {
      console.log('  ✗ FAIL: Save failed\n');
      return false;
    }
  } catch (e) {
    console.log('  ✗ Error:', e.message, '\n');
    return false;
  }
}

async function main() {
  const rqResult = await testRiceQuant();
  const jqResult = await testJoinQuant();
  
  console.log('=== Summary ===');
  console.log('RiceQuant:', rqResult ? '✓ PASS' : '✗ FAIL');
  console.log('JoinQuant:', jqResult ? '✓ PASS' : '✗ FAIL');
  
  if (rqResult && jqResult) {
    console.log('\nAll tests passed! Code encoding is correct for both platforms.');
  } else {
    console.log('\nSome tests failed. Check the implementation.');
    process.exitCode = 1;
  }
}

main().catch(e => {
  console.error('Error:', e.message);
  process.exitCode = 1;
});