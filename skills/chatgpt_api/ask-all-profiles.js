#!/usr/bin/env node

import { chromium } from 'playwright';
import { readFileSync, writeFileSync, existsSync } from 'fs';

/**
 * 在所有 Chrome Profile 中提问并保存结果
 */
async function askAllProfiles(promptFile, outputDir) {
  // Read prompt
  const prompt = readFileSync(promptFile, 'utf-8').trim();
  console.log('📝 问题:');
  console.log(prompt);
  console.log('');

  // All profiles
  const profiles = [
    { name: 'Default', path: '/Users/yuping/Library/Application Support/Google/Chrome/Default' },
    { name: 'Profile-2', path: '/Users/yuping/Library/Application Support/Google/Chrome/Profile 2' },
    { name: 'Profile-3', path: '/Users/yuping/Library/Application Support/Google/Chrome/Profile 3' },
    { name: 'Profile-5', path: '/Users/yuping/Library/Application Support/Google/Chrome/Profile 5' },
    { name: 'Profile-6', path: '/Users/yuping/Library/Application Support/Google/Chrome/Profile 6' },
    { name: 'Profile-7', path: '/Users/yuping/Library/Application Support/Google/Chrome/Profile 7' },
    { name: 'Profile-8', path: '/Users/yuping/Library/Application Support/Google/Chrome/Profile 8' }
  ];

  const results = [];
  let successCount = 0;
  let failCount = 0;

  for (let i = 0; i < profiles.length; i++) {
    const profile = profiles[i];
    
    console.log('');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log(`📂 Profile ${i + 1}/${profiles.length}: ${profile.name}`);
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('');

    if (!existsSync(profile.path)) {
      console.log('⚠️  Profile 不存在，跳过');
      results.push({
        profile: profile.name,
        status: 'skipped',
        reason: 'Profile not found'
      });
      failCount++;
      continue;
    }

    let context = null;
    let page = null;

    try {
      console.log('🚀 启动浏览器...');
      
      context = await chromium.launchPersistentContext(profile.path, {
        headless: false,
        channel: 'chrome',
        args: [
          '--disable-blink-features=AutomationControlled',
          '--proxy-server=http://127.0.0.1:7897'
        ],
        viewport: { width: 1280, height: 800 },
        timeout: 60000
      });

      page = context.pages()[0] || await context.newPage();

      console.log('🌐 打开 ChatGPT...');
      await page.goto('https://chatgpt.com/', {
        waitUntil: 'domcontentloaded',
        timeout: 60000
      });

      console.log('⏳ 等待页面加载...');
      await page.waitForTimeout(5000);

      // Check if logged in
      const url = page.url();
      if (url.includes('/auth/')) {
        console.log('⚠️  未登录，跳过此 profile');
        results.push({
          profile: profile.name,
          status: 'skipped',
          reason: 'Not logged in'
        });
        failCount++;
        await context.close();
        continue;
      }

      console.log('✅ 已登录');

      // Get username if possible
      let username = 'Unknown';
      try {
        const userButton = await page.locator('button[id*="headlessui"]').first();
        const userText = await userButton.innerText().catch(() => '');
        if (userText) {
          username = userText.split('\n')[0] || 'Unknown';
        }
      } catch {
        // Ignore
      }

      console.log(`👤 用户: ${username}`);
      console.log('💬 发送消息...');

      // Find input
      const input = await page.waitForSelector('[contenteditable="true"]#prompt-textarea', {
        timeout: 10000
      });

      await input.click();
      await page.keyboard.type(prompt, { delay: 30 });
      await page.waitForTimeout(500);

      // Send
      const sendButton = await page.locator('button[data-testid="send-button"]').first();
      await sendButton.click();

      console.log('📤 已发送，等待回复...');

      // Wait for response
      await page.waitForTimeout(3000);
      
      // Wait for stop button to disappear
      await page.waitForSelector('button[data-testid="stop-button"]', {
        timeout: 5000,
        state: 'hidden'
      }).catch(() => {});

      await page.waitForTimeout(2000);

      // Get response
      const messages = await page.locator('[data-message-author-role="assistant"]').all();
      
      if (messages.length === 0) {
        throw new Error('未找到回复');
      }

      const lastMessage = messages[messages.length - 1];
      const responseText = await lastMessage.innerText();

      console.log('✅ 收到回复');
      console.log('');
      console.log('回复预览:');
      console.log(responseText.substring(0, 100) + '...');
      console.log('');

      // Save result
      const result = {
        profile: profile.name,
        username: username,
        status: 'success',
        prompt: prompt,
        response: responseText,
        timestamp: new Date().toISOString()
      };

      results.push(result);
      successCount++;

      // Save individual file
      const filename = `${outputDir}/response-${profile.name}.txt`;
      const content = `Profile: ${profile.name}
Username: ${username}
Timestamp: ${result.timestamp}

Question:
${prompt}

Answer:
${responseText}
`;
      writeFileSync(filename, content, 'utf-8');
      console.log(`💾 已保存到: ${filename}`);

      await context.close();

      // Wait between profiles
      if (i < profiles.length - 1) {
        console.log('⏳ 等待 3 秒后继续下一个 profile...');
        await new Promise(resolve => setTimeout(resolve, 3000));
      }

    } catch (error) {
      console.error('❌ 失败:', error.message);
      
      results.push({
        profile: profile.name,
        status: 'failed',
        error: error.message
      });
      failCount++;

      if (context) {
        await context.close().catch(() => {});
      }
    }
  }

  // Save summary
  console.log('');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('📊 总结');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('');
  console.log(`总 Profiles: ${profiles.length}`);
  console.log(`成功: ${successCount}`);
  console.log(`失败/跳过: ${failCount}`);
  console.log('');

  const summaryFile = `${outputDir}/summary.json`;
  writeFileSync(summaryFile, JSON.stringify(results, null, 2), 'utf-8');
  console.log(`💾 总结已保存到: ${summaryFile}`);
  console.log('');

  // Print results
  console.log('详细结果:');
  results.forEach((r, i) => {
    const icon = r.status === 'success' ? '✅' : '❌';
    console.log(`  ${i + 1}. ${icon} ${r.profile} - ${r.status}`);
    if (r.username) {
      console.log(`     用户: ${r.username}`);
    }
    if (r.reason) {
      console.log(`     原因: ${r.reason}`);
    }
    if (r.error) {
      console.log(`     错误: ${r.error}`);
    }
  });
  console.log('');
}

// Parse args
const promptFile = process.argv[2] || 'examples/example-prompt.txt';
const outputDir = process.argv[3] || 'examples';

console.log('🚀 在所有 Chrome Profiles 中提问');
console.log('');
console.log(`📄 问题文件: ${promptFile}`);
console.log(`📁 输出目录: ${outputDir}`);
console.log('');

askAllProfiles(promptFile, outputDir).catch(error => {
  console.error('❌ 执行失败:', error);
  process.exit(1);
});
