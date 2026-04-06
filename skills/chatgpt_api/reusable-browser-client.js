#!/usr/bin/env node

import { chromium } from 'playwright';
import { readFileSync, existsSync } from 'fs';
import { PATHS } from './paths.js';
import readline from 'readline';

/**
 * 可复用的浏览器客户端
 * 启动一次浏览器，可以发送多条消息
 */
class ReusableBrowserClient {
  constructor(options = {}) {
    this.sessionPath = options.sessionPath || PATHS.sessionFile;
    this.profilePath = options.profilePath || null;
    this.browser = null;
    this.context = null;
    this.page = null;
  }

  async launch() {
    console.log('🚀 启动浏览器...');

    if (this.profilePath && existsSync(this.profilePath)) {
      // Use Chrome profile
      console.log(`📂 使用 Chrome Profile: ${this.profilePath}`);
      
      this.context = await chromium.launchPersistentContext(this.profilePath, {
        headless: false,
        channel: 'chrome',
        args: [
          '--disable-blink-features=AutomationControlled',
          '--proxy-server=http://127.0.0.1:7897'
        ],
        viewport: { width: 1280, height: 800 }
      });

      this.page = this.context.pages()[0] || await this.context.newPage();

    } else if (this.sessionPath && existsSync(this.sessionPath)) {
      // Use session cookies
      console.log(`📂 使用 Session: ${this.sessionPath}`);
      
      const sessionData = JSON.parse(readFileSync(this.sessionPath, 'utf-8'));
      
      this.browser = await chromium.launch({
        headless: false,
        args: ['--proxy-server=http://127.0.0.1:7897']
      });

      this.context = await this.browser.newContext({
        viewport: { width: 1280, height: 800 },
        userAgent: sessionData.userAgent,
        locale: 'zh-CN',
        timezoneId: 'Asia/Shanghai'
      });

      const playwrightCookies = sessionData.cookies.map(cookie => ({
        name: cookie.name,
        value: cookie.value,
        domain: cookie.domain,
        path: cookie.path || '/',
        expires: cookie.expirationDate ? cookie.expirationDate : -1,
        httpOnly: cookie.httpOnly || false,
        secure: cookie.secure || false,
        sameSite: cookie.sameSite || 'Lax'
      }));

      await this.context.addCookies(playwrightCookies);
      this.page = await this.context.newPage();

    } else {
      throw new Error('需要提供 sessionPath 或 profilePath');
    }

    // Navigate to ChatGPT
    console.log('🌐 打开 ChatGPT...');
    await this.page.goto('https://chatgpt.com/', {
      waitUntil: 'domcontentloaded',
      timeout: 60000
    });

    console.log('⏳ 等待页面加载...');
    await this.page.waitForTimeout(5000);

    console.log('✅ 浏览器已就绪');
  }

  async sendMessage(message) {
    console.log(`\n💬 发送: ${message.substring(0, 50)}${message.length > 50 ? '...' : ''}`);

    const input = await this.page.waitForSelector('[contenteditable="true"]#prompt-textarea', {
      timeout: 10000
    });

    await input.click();
    await this.page.keyboard.type(message, { delay: 30 });
    await this.page.waitForTimeout(500);

    const sendButton = await this.page.locator('button[data-testid="send-button"]').first();
    await sendButton.click();

    console.log('📤 已发送，等待回复...');

    // Wait for response
    await this.page.waitForTimeout(3000);
    await this.page.waitForSelector('button[data-testid="stop-button"]', {
      timeout: 5000,
      state: 'hidden'
    }).catch(() => {});

    await this.page.waitForTimeout(2000);

    // Get response
    const messages = await this.page.locator('[data-message-author-role="assistant"]').all();
    if (messages.length > 0) {
      const lastMessage = messages[messages.length - 1];
      const responseText = await lastMessage.innerText();

      console.log('✅ 收到回复:');
      console.log('');
      console.log(responseText);
      console.log('');

      return responseText;
    }

    return null;
  }

  async close() {
    if (this.browser) {
      await this.browser.close();
    } else if (this.context) {
      await this.context.close();
    }
  }

  async interactive() {
    console.log('');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('🎯 交互模式');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('');
    console.log('输入消息并按回车发送');
    console.log('输入 "exit" 或 "quit" 退出');
    console.log('输入 "new" 开始新对话');
    console.log('');

    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout,
      prompt: '💬 你: '
    });

    rl.prompt();

    rl.on('line', async (line) => {
      const input = line.trim();

      if (!input) {
        rl.prompt();
        return;
      }

      if (input === 'exit' || input === 'quit') {
        console.log('👋 再见！');
        await this.close();
        process.exit(0);
      }

      if (input === 'new') {
        console.log('🆕 开始新对话...');
        await this.page.locator('a[href="/"]').first().click();
        await this.page.waitForTimeout(1000);
        console.log('✅ 新对话已创建');
        rl.prompt();
        return;
      }

      try {
        await this.sendMessage(input);
      } catch (error) {
        console.error('❌ 发送失败:', error.message);
      }

      rl.prompt();
    });
  }
}

// CLI
async function main() {
  const args = process.argv.slice(2);
  
  let sessionPath = null;
  let profilePath = null;
  let interactive = false;
  let messages = [];

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--session') {
      sessionPath = args[++i];
    } else if (args[i] === '--profile') {
      profilePath = args[++i];
    } else if (args[i] === '--interactive' || args[i] === '-i') {
      interactive = true;
    } else if (args[i] === '--message' || args[i] === '-m') {
      messages.push(args[++i]);
    }
  }

  const client = new ReusableBrowserClient({ sessionPath, profilePath });

  try {
    await client.launch();

    if (messages.length > 0) {
      // Send messages
      for (const msg of messages) {
        await client.sendMessage(msg);
      }
    }

    if (interactive) {
      // Interactive mode
      await client.interactive();
    } else if (messages.length === 0) {
      // No messages, just keep browser open
      console.log('');
      console.log('💡 浏览器保持打开');
      console.log('💡 按 Ctrl+C 退出');
      console.log('');
      await new Promise(() => {});
    } else {
      // Close after sending messages
      await client.close();
    }

  } catch (error) {
    console.error('❌ 失败:', error.message);
    await client.close();
    process.exit(1);
  }
}

if (import.meta.url === `file://${process.argv[1]}`) {
  main();
}

export { ReusableBrowserClient };
