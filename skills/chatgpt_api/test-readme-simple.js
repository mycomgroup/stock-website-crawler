#!/usr/bin/env node

/**
 * 简化版 README 例子测试（避免触发 rate limit）
 * 测试核心功能
 */

import { ReusableBrowserClient } from './reusable-browser-client.js';
import { writeFileSync } from 'fs';

async function testCoreFeatures() {
  console.log('');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('🧪 测试 README 核心功能（纯浏览器模式）');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('');

  const profilePath = '/Users/yuping/Library/Application Support/Google/Chrome/Profile 7';
  const client = new ReusableBrowserClient({ profilePath });

  const results = [];
  let passCount = 0;

  try {
    // 测试 1: 启动浏览器
    console.log('📋 测试 1: 启动浏览器');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    await client.launch();
    results.push({ test: '启动浏览器', status: 'PASS' });
    passCount++;
    console.log('✅ PASS\n');

    // 测试 2: 发送单条消息
    console.log('📋 测试 2: 发送单条消息');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    const response1 = await client.sendMessage('请用一句话解释什么是闭包');
    if (response1 && response1.length > 10) {
      results.push({ 
        test: '发送单条消息', 
        status: 'PASS', 
        response: response1.substring(0, 100) 
      });
      passCount++;
      console.log('✅ PASS\n');
    } else {
      throw new Error('响应为空或太短');
    }

    // 等待一下避免 rate limit
    console.log('⏳ 等待 5 秒避免 rate limit...\n');
    await new Promise(resolve => setTimeout(resolve, 5000));

    // 测试 3: 发送第二条消息（测试复用）
    console.log('📋 测试 3: 浏览器复用 - 发送第二条消息');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    const response2 = await client.sendMessage('请用一句话解释什么是异步编程');
    if (response2 && response2.length > 10) {
      results.push({ 
        test: '浏览器复用', 
        status: 'PASS', 
        response: response2.substring(0, 100) 
      });
      passCount++;
      console.log('✅ PASS\n');
    } else {
      throw new Error('响应为空或太短');
    }

    // 测试 4: 关闭浏览器
    console.log('📋 测试 4: 关闭浏览器');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    await client.close();
    results.push({ test: '关闭浏览器', status: 'PASS' });
    passCount++;
    console.log('✅ PASS\n');

  } catch (error) {
    console.error('❌ FAIL:', error.message);
    console.error('');
    results.push({ test: '当前测试', status: 'FAIL', error: error.message });
    
    await client.close().catch(() => {});
  }

  // 生成测试报告
  console.log('');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('📊 测试总结');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('');
  console.log(`总测试数: ${results.length}`);
  console.log(`通过: ${passCount} ✅`);
  console.log(`失败: ${results.length - passCount} ❌`);
  console.log(`成功率: ${((passCount / results.length) * 100).toFixed(1)}%`);
  console.log('');

  console.log('详细结果:');
  results.forEach((r, i) => {
    const icon = r.status === 'PASS' ? '✅' : '❌';
    console.log(`  ${i + 1}. ${icon} ${r.test}`);
    if (r.response) {
      console.log(`     响应: ${r.response}...`);
    }
    if (r.error) {
      console.log(`     错误: ${r.error}`);
    }
  });
  console.log('');

  // 保存测试报告
  const report = {
    timestamp: new Date().toISOString(),
    mode: 'browser',
    summary: {
      total: results.length,
      passed: passCount,
      failed: results.length - passCount,
      successRate: `${((passCount / results.length) * 100).toFixed(1)}%`
    },
    results
  };

  writeFileSync('examples/test-report-simple.json', JSON.stringify(report, null, 2));
  console.log('💾 测试报告已保存到: examples/test-report-simple.json');
  console.log('');

  if (passCount === results.length) {
    console.log('✅ 所有核心功能测试通过！');
    console.log('');
    console.log('已验证的功能:');
    console.log('  ✅ 启动浏览器（使用 Chrome Profile）');
    console.log('  ✅ 发送单条消息');
    console.log('  ✅ 浏览器复用（多条消息）');
    console.log('  ✅ 关闭浏览器');
    console.log('');
  } else {
    console.log('❌ 部分测试失败');
    process.exit(1);
  }
}

testCoreFeatures().catch(error => {
  console.error('');
  console.error('❌ 测试执行失败:', error);
  console.error('');
  process.exit(1);
});
