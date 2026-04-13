import { chromium } from 'playwright';
import path from 'node:path';
import fs from 'node:fs';

export class BrowserEngine {
  constructor(options = {}) {
    this.headless = options.headless !== false;
    this.userDataDir = options.userDataDir || path.join(process.cwd(), 'tmp/browser_context');
  }

  async launchHeaded() {
    return await chromium.launch({ 
      headless: false,
      args: ['--disable-blink-features=AutomationControlled']
    });
  }

  async launchContext(cookies = []) {
    const browser = await chromium.launch({ 
      headless: this.headless,
      args: ['--disable-blink-features=AutomationControlled']
    });
    
    const context = await browser.newContext({
      viewport: { width: 1280, height: 800 },
      userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    });

    if (cookies && cookies.length > 0) {
      await context.addCookies(cookies);
    }

    return { browser, context };
  }

  async close(browser) {
    if (browser) await browser.close();
  }
}
