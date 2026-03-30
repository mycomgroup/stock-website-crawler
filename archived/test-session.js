#!/usr/bin/env node
/**
 * 测试脚本：验证RiceQuant会话捕获
 * 用法: node test-session.js
 */
import './load-env.js';
import { ensureRiceQuantSession } from './browser/session-manager.js';
import { RiceQuantClient } from './request/ricequant-client.js';

async function testSession() {
  console.log('=== RiceQuant Session Test ===\n');
  
  try {
    // 1. 测试会话管理
    console.log('1. Testing session management...');
    const credentials = {
      username: process.env.RICEQUANT_USERNAME,
      password: process.env.RICEQUANT_PASSWORD
    };
    
    if (!credentials.username || !credentials.password) {
      console.error('Error: Missing credentials in .env file');
      console.log('Please set RICEQUANT_USERNAME and RICEQUANT_PASSWORD');
      process.exit(1);
    }
    
    console.log(`Username: ${credentials.username}`);
    const cookies = await ensureRiceQuantSession(credentials);
    console.log(`✓ Session captured successfully (${cookies.length} cookies)`);
    
    // 2. 测试客户端
    console.log('\n2. Testing RiceQuantClient...');
    const client = new RiceQuantClient({ cookies });
    
    // 3. 尝试列出策略
    console.log('\n3. Testing listStrategies...');
    try {
      const strategies = await client.listStrategies();
      console.log(`✓ Found ${strategies.length} strategies`);
      if (strategies.length > 0) {
        console.log('\nFirst 3 strategies:');
        strategies.slice(0, 3).forEach((s, i) => {
          console.log(`  ${i + 1}. ${s.id || s.strategyId}: ${s.name || s.title}`);
        });
      }
    } catch (e) {
      console.log(`✗ listStrategies failed: ${e.message}`);
      console.log('  This is expected if the API endpoint is different');
    }
    
    console.log('\n=== Test Complete ===');
    
  } catch (error) {
    console.error('\n✗ Test failed:', error.message);
    console.error(error.stack);
    process.exit(1);
  }
}

testSession();
