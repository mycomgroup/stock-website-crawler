#!/usr/bin/env node

import { chromium } from 'playwright';
import { existsSync } from 'fs';

/**
 * 使用现有的 Chrome Profile
 */
async function useChromeProfile(profilePath, message) {
  console.log('🚀 使用 Chrome Profile...');
  console.log(`📂 Profile: ${profilePath}`);
  
  if (!existsSync(profilePath)) {
    console.error('❌ Profile 不存在:', profilePath);
    process.exit(1);
  }

  // Launch with existing profile
  const context = await chromium.launchPersistentContext(profilePath, {
    headless: false,
    channel: 'chrome',
    args: [
      '--disable-blink-features=AutomationControlled',
      '--proxy-server=http://127.0.0.1:7897'
    ],
    viewport: { width: 1280, height: 800 }
  });

  const page = context.pages()[0] || await context.newPage();

  try {
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
      console.log('⚠️  未登录，请在浏览器中登录');
      console.log('💡 登录后按回车继续...');
      await new Promise(resolve => process.stdin.once('data', resolve));
      await page.reload({ waitUntil: 'domcontentloaded' });
      await page.waitForTimeout(3000);
    }

    console.log('✅ 已登录');

    if (message) {
      console.log(`💬 发送消息: ${message}`);

      // Find input
      const input = await page.waitForSelector('[contenteditable="true"]#prompt-textarea', {
        timeout: 10000
      });

      await input.click();
      await page.keyboard.type(message, { delay: 30 });
      await page.waitForTimeout(500);

      // Send
      const sendButton = await page.locator('button[data-testid="send-button"]').first();
      await sendButton.click();

      console.log('📤 消息已发送');
      console.log('⏳ 等待回复...');

      // Wait for response
      await page.waitForTimeout(3000);
      await page.waitForSelector('button[data-testid="stop-button"]', {
        timeout: 5000,
        state: 'hidden'
      }).catch(() => {});

      await page.waitForTimeout(2000);

      // Get response
      const messages = await page.locator('[data-message-author-role="assistant"]').all();
      if (messages.length > 0) {
        const lastMessage = messages[messages.length - 1];
        const responseText = await lastMessage.innerText();

        console.log('');
        console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
        console.log('💬 ChatGPT 回复:');
        console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
        console.log('');
        console.log(responseText);
        console.log('');
        console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
        console.log('');
      }
    }

    console.log('');
    console.log('💡 浏览器保持打开，你可以继续手动操作');
    console.log('💡 按 Ctrl+C 退出');
    console.log('');

    // Keep alive
    await new Promise(() => {});

  } catch (error) {
    console.error('❌ 失败:', error.message);
    await context.close();
    process.exit(1);
  }
}

// Parse args
const args = process.argv.slice(2);
const profilePath = args[0];
const message = args[1];

if (!profilePath) {
  console.log('用法: node use-chrome-profile.js <profile路径> [消息]');
  console.log('');
  console.log('示例:');
  console.log('  node use-chrome-profile.js "/Users/yuping/Library/Application Support/Google/Chrome/Default"');
  console.log('  node use-chrome-profile.js "/Users/yuping/Library/Application Support/Google/Chrome/Profile 7" "你好"');
  console.log('');
  console.log('你的 Chrome Profiles:');
  console.log('  Default: /Users/yuping/Library/Application Support/Google/Chrome/Default');
  console.log('  Profile 2: /Users/yuping/Library/Application Support/Google/Chrome/Profile 2');
  console.log('  Profile 3: /Users/yuping/Library/Application Support/Google/Chrome/Profile 3');
  console.log('  Profile 5: /Users/yuping/Library/Application Support/Google/Chrome/Profile 5');
  console.log('  Profile 6: /Users/yuping/Library/Application Support/Google/Chrome/Profile 6');
  console.log('  Profile 7: /Users/yuping/Library/Application Support/Google/Chrome/Profile 7');
  console.log('  Profile 8: /Users/yuping/Library/Application Support/Google/Chrome/Profile 8');
  process.exit(1);
}

useChromeProfile(profilePath, message);
