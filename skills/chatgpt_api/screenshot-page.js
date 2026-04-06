#!/usr/bin/env node

import { ChatGPTBrowserClient } from './browser/chatgpt-browser-client.js';
import { PATHS } from './paths.js';

async function screenshot() {
  const client = new ChatGPTBrowserClient({
    headless: false,
    sessionPath: PATHS.sessionFile
  });

  try {
    await client.launch();
    
    // Wait a bit for page to load
    await client.page.waitForTimeout(3000);
    
    // Take screenshot
    await client.page.screenshot({ path: 'chatgpt-page.png', fullPage: true });
    console.log('✅ 截图已保存到 chatgpt-page.png');
    
    // Get HTML
    const html = await client.page.content();
    const { writeFileSync } = await import('fs');
    writeFileSync('chatgpt-page.html', html);
    console.log('✅ HTML 已保存到 chatgpt-page.html');
    
    await client.close();
    
  } catch (error) {
    console.error('❌ 失败:', error.message);
    await client.close();
    process.exit(1);
  }
}

screenshot();
