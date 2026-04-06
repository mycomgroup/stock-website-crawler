import { chromium } from 'playwright';
import { existsSync } from 'fs';
import { ENV } from '../load-env.js';

/**
 * 基于 Playwright 的 ChatGPT 客户端
 * 使用真实浏览器操作，不会被 Cloudflare 阻止
 */
export class ChatGPTBrowserClient {
  constructor(options = {}) {
    this.headless = options.headless !== undefined ? options.headless : false;
    this.sessionPath = options.sessionPath || null;
    this.browser = null;
    this.context = null;
    this.page = null;
  }

  /**
   * 启动浏览器
   */
  async launch() {
    console.log('🚀 启动浏览器...');

    const launchOptions = {
      headless: this.headless,
      args: [
        '--disable-blink-features=AutomationControlled',
        `--proxy-server=${ENV.HTTP_PROXY || ENV.HTTPS_PROXY}`
      ].filter(Boolean)
    };

    if (this.sessionPath && existsSync(this.sessionPath)) {
      console.log(`📂 使用 session: ${this.sessionPath}`);
      
      // Load session from cookies
      const { readFileSync } = await import('fs');
      const sessionData = JSON.parse(readFileSync(this.sessionPath, 'utf-8'));
      
      this.browser = await chromium.launch(launchOptions);
      this.context = await this.browser.newContext({
        viewport: { width: 1280, height: 800 },
        userAgent: sessionData.userAgent || 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        locale: 'zh-CN',
        timezoneId: 'Asia/Shanghai'
      });

      // Convert cookies to Playwright format
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

      // Add cookies
      await this.context.addCookies(playwrightCookies);
      
      console.log(`🍪 已加载 ${playwrightCookies.length} 个 cookies`);
      
    } else {
      // No session, launch fresh browser
      this.browser = await chromium.launch(launchOptions);
      this.context = await this.browser.newContext({
        viewport: { width: 1280, height: 800 },
        userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        locale: 'zh-CN',
        timezoneId: 'Asia/Shanghai'
      });
    }

    this.page = await this.context.newPage();
    
    // Navigate to ChatGPT
    console.log('🌐 打开 ChatGPT...');
    await this.page.goto('https://chatgpt.com/', {
      waitUntil: 'domcontentloaded',
      timeout: 60000
    });

    // Wait longer for page to fully render
    console.log('⏳ 等待页面加载...');
    await this.page.waitForTimeout(5000);

    // Check if logged in
    const isLoggedIn = await this.checkLogin();
    if (!isLoggedIn) {
      console.log('');
      console.log('⚠️  检测到未登录');
      console.log('');
      console.log('请在打开的浏览器中完成登录，然后：');
      console.log('  1. 确保看到 ChatGPT 聊天界面');
      console.log('  2. 回到终端按回车继续');
      console.log('');
      console.log('💡 等待你的操作...');
      console.log('');
      
      // Wait for user input with timeout
      await Promise.race([
        new Promise(resolve => {
          process.stdin.once('data', () => {
            console.log('✅ 继续执行...');
            resolve();
          });
        }),
        new Promise(resolve => setTimeout(resolve, 300000)) // 5 minutes timeout
      ]);
      
      // Refresh page to check login status
      await this.page.reload({ waitUntil: 'networkidle' });
      await this.page.waitForTimeout(2000);
      
      // Check again
      const nowLoggedIn = await this.checkLogin();
      if (!nowLoggedIn) {
        throw new Error('仍未登录，请先登录 ChatGPT');
      }
    }

    console.log('✅ 浏览器已就绪');
  }

  /**
   * 检查是否已登录
   */
  async checkLogin() {
    const url = this.page.url();
    
    // If redirected to auth page, not logged in
    if (url.includes('/auth/')) {
      return false;
    }

    // Check for multiple possible selectors
    try {
      // Try to find the textarea (main chat interface)
      const hasTextarea = await this.page.locator('textarea[placeholder*="Message"], textarea[data-id="root"], textarea#prompt-textarea').first().isVisible({ timeout: 3000 }).catch(() => false);
      
      if (hasTextarea) {
        return true;
      }

      // Check for user menu (indicates logged in)
      const hasUserMenu = await this.page.locator('button[id*="headlessui"], div[class*="user"], button:has-text("zxcgas")').first().isVisible({ timeout: 3000 }).catch(() => false);
      
      if (hasUserMenu) {
        return true;
      }

      // Check if we're on the main chat page
      if (url === 'https://chatgpt.com/' || url.startsWith('https://chatgpt.com/?')) {
        // If on main page and no auth redirect, likely logged in
        return true;
      }

      return false;
    } catch (error) {
      console.log('检测登录状态时出错:', error.message);
      return false;
    }
  }

  /**
   * 发送消息
   */
  async sendMessage(message, options = {}) {
    const { waitForResponse = true, timeout = 120000 } = options;

    if (!this.page) {
      throw new Error('浏览器未启动，请先调用 launch()');
    }

    console.log(`💬 发送消息: ${message.substring(0, 50)}${message.length > 50 ? '...' : ''}`);

    // Find input element - ChatGPT uses contenteditable div, not textarea
    let inputElement = null;
    const selectors = [
      '[contenteditable="true"]#prompt-textarea',
      '[contenteditable="true"][aria-label*="ChatGPT"]',
      '[contenteditable="true"][role="textbox"]',
      'div#prompt-textarea',
      'textarea[name="prompt-textarea"]',
      'textarea[placeholder*="问"]',
      'textarea'
    ];

    for (const selector of selectors) {
      try {
        inputElement = await this.page.waitForSelector(selector, { timeout: 5000, state: 'visible' });
        if (inputElement) {
          console.log(`✓ 找到输入框: ${selector}`);
          break;
        }
      } catch (e) {
        console.log(`✗ 未找到: ${selector}`);
        continue;
      }
    }

    if (!inputElement) {
      throw new Error('未找到输入框，请确保已登录并在聊天页面');
    }

    // Click and type message
    await inputElement.click();
    await this.page.waitForTimeout(300);
    
    // For contenteditable, use keyboard input
    await inputElement.focus();
    await this.page.keyboard.type(message, { delay: 30 });

    // Wait a bit
    await this.page.waitForTimeout(500);

    // Find and click send button - try multiple selectors
    const sendSelectors = [
      'button[data-testid="send-button"]',
      'button[data-testid="fruitjuice-send-button"]',
      'button:has-text("Send")',
      'button svg[class*="icon"]'
    ];

    let sent = false;
    for (const selector of sendSelectors) {
      try {
        const button = await this.page.locator(selector).first();
        const isVisible = await button.isVisible({ timeout: 1000 }).catch(() => false);
        if (isVisible) {
          await button.click();
          console.log(`✓ 点击发送按钮: ${selector}`);
          sent = true;
          break;
        }
      } catch {
        continue;
      }
    }

    if (!sent) {
      // Try pressing Enter as fallback
      console.log('⚠️  未找到发送按钮，尝试按 Enter');
      await this.page.keyboard.press('Enter');
    }

    console.log('📤 消息已发送');

    if (!waitForResponse) {
      return { sent: true };
    }

    // Wait for response
    console.log('⏳ 等待回复...');

    try {
      // Wait for the response to appear and complete
      // Look for the stop button to disappear (means response is complete)
      await this.page.waitForSelector('button[data-testid="stop-button"], button:has-text("Stop")', {
        timeout: 5000,
        state: 'visible'
      }).catch(() => {
        // Stop button might not appear for quick responses
      });

      // Wait for stop button to disappear (response complete)
      await this.page.waitForSelector('button[data-testid="stop-button"], button:has-text("Stop")', {
        timeout: timeout,
        state: 'hidden'
      }).catch(() => {
        // Timeout or button never appeared
      });

      // Wait a bit more for rendering
      await this.page.waitForTimeout(2000);

      // Get the last assistant message - try multiple selectors
      const messageSelectors = [
        '[data-message-author-role="assistant"]',
        '[data-role="assistant"]',
        'div[class*="agent"]',
        'div[class*="markdown"]'
      ];

      let messages = [];
      for (const selector of messageSelectors) {
        messages = await this.page.locator(selector).all();
        if (messages.length > 0) {
          console.log(`✓ 找到 ${messages.length} 条回复消息: ${selector}`);
          break;
        }
      }
      
      if (messages.length === 0) {
        throw new Error('未找到回复消息');
      }

      const lastMessage = messages[messages.length - 1];
      const responseText = await lastMessage.innerText();

      console.log('✅ 收到回复');
      
      return {
        content: responseText,
        timestamp: new Date().toISOString()
      };

    } catch (error) {
      console.error('❌ 获取回复失败:', error.message);
      throw error;
    }
  }

  /**
   * 获取对话历史
   */
  async getConversationHistory() {
    if (!this.page) {
      throw new Error('浏览器未启动');
    }

    const messages = [];

    // Get all user messages
    const userMessages = await this.page.locator('[data-message-author-role="user"]').all();
    for (const msg of userMessages) {
      messages.push({
        role: 'user',
        content: await msg.innerText()
      });
    }

    // Get all assistant messages
    const assistantMessages = await this.page.locator('[data-message-author-role="assistant"]').all();
    for (const msg of assistantMessages) {
      messages.push({
        role: 'assistant',
        content: await msg.innerText()
      });
    }

    return messages;
  }

  /**
   * 开始新对话
   */
  async newChat() {
    if (!this.page) {
      throw new Error('浏览器未启动');
    }

    console.log('🆕 开始新对话...');

    // Click new chat button
    const newChatButton = await this.page.locator('a[href="/"]').first();
    await newChatButton.click();

    await this.page.waitForTimeout(1000);
    console.log('✅ 新对话已创建');
  }

  /**
   * 关闭浏览器
   */
  async close() {
    if (this.browser) {
      console.log('🔒 关闭浏览器...');
      await this.browser.close();
      this.browser = null;
      this.context = null;
      this.page = null;
    }
  }

  /**
   * 保持浏览器打开（用于交互式使用）
   */
  async keepAlive() {
    console.log('');
    console.log('🎯 浏览器保持打开状态');
    console.log('💡 你可以在浏览器中手动操作');
    console.log('💡 按 Ctrl+C 退出');
    console.log('');

    // Keep process alive
    await new Promise(() => {});
  }
}
