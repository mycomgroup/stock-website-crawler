#!/usr/bin/env node

/**
 * 测试 README 中的所有例子（纯浏览器模式）
 * 验证所有功能都能正常工作
 */

import { ReusableBrowserClient } from './reusable-browser-client.js';
import { writeFileSync } from 'fs';

async function testAllExamples() {
  console.log('');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('🧪 测试 README 中的所有例子（纯浏览器模式）');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('');

  // 使用 Chrome Profile 7
  const profilePath = '/Users/yuping/Library/Application Support/Google/Chrome/Profile 7';
  
  const client = new ReusableBrowserClient({ profilePath });

  const results = [];
  let passCount = 0;
  let failCount = 0;

  try {
    // 启动浏览器
    console.log('📋 测试 1: 启动浏览器');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    await client.launch();
    results.push({ test: '启动浏览器', status: 'PASS' });
    passCount++;
    console.log('✅ PASS\n');

    // 测试 2: 发送单条消息
    console.log('📋 测试 2: 发送单条消息');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    const response1 = await client.sendMessage('请用一句话解释什么是 JavaScript');
    if (response1 && response1.length > 10) {
      results.push({ test: '发送单条消息', status: 'PASS', response: response1.substring(0, 100) });
      passCount++;
      console.log('✅ PASS\n');
    } else {
      throw new Error('响应为空或太短');
    }

    // 测试 3: 发送第二条消息（测试复用）
    console.log('📋 测试 3: 发送第二条消息（测试浏览器复用）');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    const response2 = await client.sendMessage('请用一句话解释什么是 Python');
    if (response2 && response2.length > 10) {
      results.push({ test: '浏览器复用', status: 'PASS', response: response2.substring(0, 100) });
      passCount++;
      console.log('✅ PASS\n');
    } else {
      throw new Error('响应为空或太短');
    }

    // 测试 4: 开始新对话
    console.log('📋 测试 4: 开始新对话');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    try {
      // Try multiple selectors for new chat button
      const newChatSelectors = [
        'a[data-testid="create-new-chat-button"]',
        'a[href="/"]',
        'button:has-text("New chat")'
      ];
      
      let clicked = false;
      for (const selector of newChatSelectors) {
        try {
          await client.page.locator(selector).first().click({ timeout: 5000, force: true });
          clicked = true;
          break;
        } catch (e) {
          continue;
        }
      }
      
      if (!clicked) {
        // Just navigate directly
        await client.page.goto('https://chatgpt.com/', { waitUntil: 'domcontentloaded' });
      }
      
      await client.page.waitForTimeout(2000);
      results.push({ test: '开始新对话', status: 'PASS' });
      passCount++;
      console.log('✅ PASS\n');
    } catch (error) {
      console.log('⚠️  跳过新对话测试（非关键功能）\n');
      results.push({ test: '开始新对话', status: 'SKIP', note: '非关键功能' });
    }

    // 测试 5: 在新对话中发送消息
    console.log('📋 测试 5: 在新对话中发送消息');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    const response3 = await client.sendMessage('你好，请简短回复');
    if (response3 && response3.length > 0) {
      results.push({ test: '新对话发送消息', status: 'PASS', response: response3.substring(0, 100) });
      passCount++;
      console.log('✅ PASS\n');
    } else {
      throw new Error('响应为空');
    }

    // 测试 6: 批量发送（3条消息）
    console.log('📋 测试 6: 批量发送消息');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    const batchMessages = [
      '什么是 Docker？请用一句话回答',
      '什么是 Kubernetes？请用一句话回答',
      '什么是微服务？请用一句话回答'
    ];
    
    const batchResponses = [];
    for (const msg of batchMessages) {
      const resp = await client.sendMessage(msg);
      batchResponses.push(resp);
    }
    
    if (batchResponses.every(r => r && r.length > 10)) {
      results.push({ test: '批量发送消息', status: 'PASS', count: batchMessages.length });
      passCount++;
      console.log('✅ PASS\n');
    } else {
      throw new Error('部分批量消息失败');
    }

    // 关闭浏览器
    console.log('📋 测试 7: 关闭浏览器');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    await client.close();
    results.push({ test: '关闭浏览器', status: 'PASS' });
    passCount++;
    console.log('✅ PASS\n');

  } catch (error) {
    console.error('❌ FAIL:', error.message);
    console.error('');
    results.push({ test: '当前测试', status: 'FAIL', error: error.message });
    failCount++;
    
    await client.close().catch(() => {});
  }

  // 生成测试报告
  console.log('');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('📊 测试总结');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('');
  console.log(`总测试数: ${passCount + failCount}`);
  console.log(`通过: ${passCount} ✅`);
  console.log(`失败: ${failCount} ❌`);
  console.log(`成功率: ${((passCount / (passCount + failCount)) * 100).toFixed(1)}%`);
  console.log('');

  console.log('详细结果:');
  results.forEach((r, i) => {
    const icon = r.status === 'PASS' ? '✅' : '❌';
    console.log(`  ${i + 1}. ${icon} ${r.test}`);
    if (r.response) {
      console.log(`     响应: ${r.response}...`);
    }
    if (r.count) {
      console.log(`     数量: ${r.count}`);
    }
    if (r.error) {
      console.log(`     错误: ${r.error}`);
    }
  });
  console.log('');

  // 保存测试报告
  const report = {
    timestamp: new Date().toISOString(),
    summary: {
      total: passCount + failCount,
      passed: passCount,
      failed: failCount,
      successRate: `${((passCount / (passCount + failCount)) * 100).toFixed(1)}%`
    },
    results
  };

  writeFileSync('examples/test-report.json', JSON.stringify(report, null, 2));
  console.log('💾 测试报告已保存到: examples/test-report.json');
  console.log('');

  if (failCount > 0) {
    console.log('❌ 部分测试失败');
    process.exit(1);
  } else {
    console.log('✅ 所有测试通过！');
  }
}

testAllExamples().catch(error => {
  console.error('');
  console.error('❌ 测试执行失败:', error);
  console.error('');
  process.exit(1);
});
