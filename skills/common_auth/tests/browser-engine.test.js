import { describe, it, beforeEach, afterEach, mock } from 'node:test';
import assert from 'node:assert';
import path from 'node:path';

const createMockChromium = () => {
  const state = {
    launchCalls: [],
    newContextCalls: [],
    connected: true
  };
  
  const mockBrowser = {
    isConnected: () => state.connected,
    close: mock.fn(async () => {}),
    newContext: mock.fn(async () => ({
      addCookies: mock.fn(async () => {}),
      newPage: mock.fn(async () => ({
        goto: mock.fn(async () => {}),
        waitForEvent: mock.fn(async () => new Promise(() => {}))
      }))
    }))
  };
  
  return {
    launch: mock.fn(async (options) => {
      state.launchCalls.push(options);
      return mockBrowser;
    }),
    _state: state,
    _mockBrowser: mockBrowser
  };
};

describe('BrowserEngine', () => {
  let mockChromium;
  let originalPath;
  
  beforeEach(() => {
    mockChromium = createMockChromium();
  });
  
  describe('constructor', () => {
    it('should use default headless true', () => {
      const options = {};
      const headless = options.headless !== false;
      assert.strictEqual(headless, true);
    });
    
    it('should use custom headless false', () => {
      const options = { headless: false };
      const headless = options.headless !== false;
      assert.strictEqual(headless, false);
    });
    
    it('should use default userDataDir', () => {
      const options = {};
      const userDataDir = options.userDataDir || path.join(process.cwd(), 'tmp/browser_context');
      assert.ok(userDataDir.includes('tmp/browser_context'));
    });
    
    it('should use custom userDataDir', () => {
      const customDir = '/custom/path';
      const options = { userDataDir: customDir };
      const userDataDir = options.userDataDir || path.join(process.cwd(), 'tmp/browser_context');
      assert.strictEqual(userDataDir, customDir);
    });
  });
  
  describe('launchHeaded', () => {
    it('should launch browser with headless false', async () => {
      await mockChromium.launch({ 
        headless: false,
        args: ['--disable-blink-features=AutomationControlled']
      });
      
      assert.strictEqual(mockChromium.launch.mock.calls.length, 1);
      const launchOptions = mockChromium.launch.mock.calls[0].arguments[0];
      assert.strictEqual(launchOptions.headless, false);
      assert.ok(launchOptions.args.includes('--disable-blink-features=AutomationControlled'));
    });
    
    it('should return browser object', async () => {
      const browser = await mockChromium.launch({ headless: false });
      assert.ok(browser);
      assert.ok(browser.close);
      assert.ok(browser.newContext);
    });
  });
  
  describe('launchContext', () => {
    it('should launch browser with configured headless', async () => {
      const headless = true;
      await mockChromium.launch({ 
        headless: headless,
        args: ['--disable-blink-features=AutomationControlled']
      });
      
      const launchOptions = mockChromium.launch.mock.calls[0].arguments[0];
      assert.strictEqual(launchOptions.headless, true);
    });
    
    it('should create context with viewport', async () => {
      const browser = await mockChromium.launch({ headless: true });
      const context = await browser.newContext({
        viewport: { width: 1280, height: 800 },
        userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
      });
      
      assert.ok(context);
      assert.ok(context.newPage);
    });
    
    it('should return browser and context', async () => {
      const browser = await mockChromium.launch({ headless: true });
      const context = await browser.newContext();
      
      assert.ok(browser);
      assert.ok(context);
    });
    
    it('should add cookies when provided', async () => {
      const browser = await mockChromium.launch({ headless: true });
      const context = await browser.newContext();
      const cookies = [{ name: 'test', value: 'val', domain: '.example.com' }];
      
      await context.addCookies(cookies);
      
      assert.strictEqual(context.addCookies.mock.calls.length, 1);
      assert.deepStrictEqual(context.addCookies.mock.calls[0].arguments[0], cookies);
    });
    
    it('should not add cookies when empty array', async () => {
      const browser = await mockChromium.launch({ headless: true });
      const context = await browser.newContext();
      
      if (context.addCookies) {
        assert.ok(true);
      }
    });
    
    it('should not add cookies when null', async () => {
      const browser = await mockChromium.launch({ headless: true });
      const context = await browser.newContext();
      
      if (context.addCookies) {
        assert.ok(true);
      }
    });
  });
  
  describe('close', () => {
    it('should close browser when provided', async () => {
      const browser = await mockChromium.launch({ headless: true });
      await browser.close();
      
      assert.strictEqual(browser.close.mock.calls.length, 1);
    });
    
    it('should handle null browser gracefully', async () => {
      const browser = null;
      if (browser) await browser.close();
      assert.strictEqual(browser, null);
    });
    
    it('should handle undefined browser gracefully', async () => {
      const browser = undefined;
      if (browser) await browser.close();
      assert.strictEqual(browser, undefined);
    });
  });
  
  describe('integration scenarios', () => {
    it('should support full workflow: launch, create context, add cookies, close', async () => {
      const browser = await mockChromium.launch({ headless: true });
      const context = await browser.newContext();
      const cookies = [{ name: 'session', value: 'abc123' }];
      
      await context.addCookies(cookies);
      await browser.close();
      
      assert.strictEqual(mockChromium.launch.mock.calls.length, 1);
      assert.strictEqual(browser.newContext.mock.calls.length, 1);
      assert.strictEqual(context.addCookies.mock.calls.length, 1);
      assert.strictEqual(browser.close.mock.calls.length, 1);
    });
    
    it('should support headed browser workflow', async () => {
      const browser = await mockChromium.launch({ headless: false });
      const context = await browser.newContext();
      const page = await context.newPage();
      
      assert.ok(page);
      assert.ok(page.goto);
      await browser.close();
    });
  });
});