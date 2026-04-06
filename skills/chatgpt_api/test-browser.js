#!/usr/bin/env node

import { ChatGPTBrowserClient } from './browser/chatgpt-browser-client.js';
import { PATHS } from './paths.js';

async function test() {
  console.log('🧪 测试浏览器模式');
  console.log('');

  const client = new ChatGPTBrowserClient({
    headless: false,
    sessionPath: PATHS.sessionFile
  });

  try {
    // Launch
    await client.launch();

    // Send message
    console.log('');
    const response = await client.sendMessage('你好，请用中文简短回复');

    console.log('');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('💬 回复:');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('');
    console.log(response.content);
    console.log('');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('');
    console.log('✅ 测试成功！');
    console.log('');

    // Close
    await client.close();

  } catch (error) {
    console.error('');
    console.error('❌ 测试失败:', error.message);
    console.error('');
    await client.close();
    process.exit(1);
  }
}

test();
