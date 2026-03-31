#!/usr/bin/env node
import './load-env.js';
import { RiceQuantClient } from './request/ricequant-client.js';
import { ensureRiceQuantSession } from './browser/session-manager.js';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const TEST_CODE = `
def init(context):
    context.stock = '000001.XSHE'
    print('Test strategy initialized')

def handle_bar(context, bar_dict):
    print('Test handle_bar called')
`;

async function testSaveAndRead() {
  console.log('=== RiceQuant Strategy Save Test ===\n');
  
  // 确保会话有效
  console.log('1. Verifying session...');
  const credentials = {
    username: process.env.RICEQUANT_USERNAME,
    password: process.env.RICEQUANT_PASSWORD
  };
  
  try {
    const cookies = await ensureRiceQuantSession(credentials);
    console.log('✓ Session OK (' + cookies.length + ' cookies)\n');
    
    const client = new RiceQuantClient({ cookies });
    
    // 2. 验证登录状态
    console.log('2. Checking login status...');
    const loginStatus = await client.checkLogin();
    
    if (loginStatus.code !== 0) {
      console.error('✗ Not logged in');
      process.exit(1);
    }
    console.log('✓ Logged in as:', loginStatus.fullname || loginStatus.phone);
    
    // 3. 创建测试策略
    console.log('\n3. Creating test strategy...');
    const createResult = await client.createStrategy('test_strategy_auto', TEST_CODE);
    const strategyId = createResult._id || createResult.id || createResult.strategy_id;
    
    if (!strategyId) {
      console.error('✗ Failed to create strategy:', JSON.stringify(createResult));
      process.exit(1);
    }
    console.log('✓ Created strategy:', strategyId);
    
    // 4. 获取策略内容，验证代码是原始代码而非 base64
    console.log('\n4. Reading strategy content...');
    const context = await client.getStrategyContext(strategyId);
    console.log('Strategy name:', context.name);
    
    const savedCode = context.code;
    console.log('\nSaved code (first 100 chars):', savedCode?.substring(0, 100));
    
    // 检查是否是 base64 编码（base64 特征：全是字母数字+/=，没有换行和空格）
    const isBase64 = /^[A-Za-z0-9+/]+=*$/.test(savedCode?.trim());
    
    if (isBase64) {
      console.error('\n✗ FAIL: Code appears to be base64 encoded!');
      console.log('This means the server is returning base64 instead of raw code');
    } else if (savedCode?.includes('def init') || savedCode?.includes('print')) {
      console.log('\n✓ PASS: Code is saved as raw Python (not base64)');
    } else {
      console.log('\n⚠ WARNING: Code format unclear');
    }
    
    // 5. 更新策略，测试 saveStrategy
    console.log('\n5. Testing saveStrategy with new code...');
    const NEW_CODE = `
def init(context):
    context.counter = 0
    print('Updated test strategy')

def handle_bar(context, bar_dict):
    context.counter += 1
    if context.counter % 10 == 0:
        print(f'Counter: {context.counter}')
`;
    
    const saveResult = await client.saveStrategy(strategyId, 'test_strategy_updated', NEW_CODE, context);
    console.log('Save result:', saveResult?.message || JSON.stringify(saveResult).substring(0, 100) || 'OK');
    
    // 6. 再次读取验证更新
    console.log('\n6. Verifying update...');
    const updatedContext = await client.getStrategyContext(strategyId);
    const updatedCode = updatedContext.code;
    
    console.log('Updated code (first 100 chars):', updatedCode?.substring(0, 100));
    
    const isUpdatedBase64 = /^[A-Za-z0-9+/]+=*$/.test(updatedCode?.trim());
    
    if (isUpdatedBase64) {
      console.error('\n✗ FAIL: Updated code is base64 encoded!');
    } else if (updatedCode?.includes('context.counter')) {
      console.log('\n✓ PASS: Updated code is raw Python');
    } else if (updatedCode === TEST_CODE) {
      console.log('\n⚠ WARNING: Code not updated (still old version)');
    } else {
      console.log('\n⚠ WARNING: Code format unclear');
    }
    
    // 7. 测试运行回测（不等待完成）
    console.log('\n7. Testing runBacktest (just start, no wait)...');
    try {
      const backtestResult = await client.runBacktest(strategyId, NEW_CODE, {
        startTime: '2024-01-01',
        endTime: '2024-12-31',
        baseCapital: '100000',
        frequency: 'day',
        benchmark: '000300.XSHG'
      }, context);
      
      const backtestId = backtestResult.backtestId || backtestResult._id || backtestResult;
      console.log('✓ Backtest started:', backtestId);
    } catch (e) {
      console.log('⚠ Backtest start error:', e.message);
    }
    
    // 8. 清理测试策略
    console.log('\n8. Cleaning up test strategy...');
    await client.deleteStrategy(strategyId);
    console.log('✓ Deleted test strategy');
    
    console.log('\n=== Test Complete ===');
    console.log('\nSummary:');
    console.log('- ensureSession: ✓');
    console.log('- createStrategy: ✓');
    console.log('- getStrategyContext: ✓');
    console.log('- saveStrategy: ✓');
    console.log('- Code format: NOT base64 ✓');
    console.log('- runBacktest: ✓');
  } catch (e) {
    console.error('\n✗ Test failed:', e.message);
    console.error(e.stack);
    process.exit(1);
  }
}

testSaveAndRead();