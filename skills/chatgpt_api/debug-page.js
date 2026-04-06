#!/usr/bin/env node

import { ChatGPTBrowserClient } from './browser/chatgpt-browser-client.js';
import { PATHS } from './paths.js';

async function debug() {
  console.log('🔍 调试页面元素');
  console.log('');

  const client = new ChatGPTBrowserClient({
    headless: false,
    sessionPath: PATHS.sessionFile
  });

  try {
    await client.launch();

    console.log('');
    console.log('📊 页面信息:');
    console.log('URL:', client.page.url());
    console.log('');

    // Get page title
    const title = await client.page.title();
    console.log('标题:', title);
    console.log('');

    // Check for textareas
    console.log('🔍 查找 textarea 元素...');
    const textareas = await client.page.locator('textarea').all();
    console.log(`找到 ${textareas.length} 个 textarea`);
    
    for (let i = 0; i < textareas.length; i++) {
      const ta = textareas[i];
      const id = await ta.getAttribute('id').catch(() => null);
      const placeholder = await ta.getAttribute('placeholder').catch(() => null);
      const dataId = await ta.getAttribute('data-id').catch(() => null);
      const isVisible = await ta.isVisible().catch(() => false);
      
      console.log(`  ${i + 1}. id="${id}" placeholder="${placeholder}" data-id="${dataId}" visible=${isVisible}`);
    }

    console.log('');
    console.log('🔍 查找 button 元素...');
    const buttons = await client.page.locator('button').all();
    console.log(`找到 ${buttons.length} 个 button`);
    
    // Show first 10 buttons
    for (let i = 0; i < Math.min(10, buttons.length); i++) {
      const btn = buttons[i];
      const text = await btn.innerText().catch(() => '');
      const testId = await btn.getAttribute('data-testid').catch(() => null);
      const isVisible = await btn.isVisible().catch(() => false);
      
      if (text || testId) {
        console.log(`  ${i + 1}. text="${text.substring(0, 30)}" data-testid="${testId}" visible=${isVisible}`);
      }
    }

    console.log('');
    console.log('💡 浏览器保持打开，你可以手动检查页面');
    console.log('💡 按 Ctrl+C 退出');
    console.log('');

    // Keep alive
    await new Promise(() => {});

  } catch (error) {
    console.error('');
    console.error('❌ 调试失败:', error.message);
    console.error('');
    await client.close();
    process.exit(1);
  }
}

debug();
