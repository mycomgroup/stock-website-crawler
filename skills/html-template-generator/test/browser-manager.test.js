import { BrowserManager } from '../lib/browser-manager.js';

describe('BrowserManager', () => {
  let manager;

  afterEach(async () => {
    if (manager && manager.isRunning()) {
      await manager.close();
    }
  });

  test('should create manager with default config', () => {
    manager = new BrowserManager();
    
    expect(manager.userDataDir).toBe('../../stock-crawler/chrome_user_data');
    expect(manager.headless).toBe(true);
    expect(manager.channel).toBe('chrome');
    expect(manager.timeout).toBe(30000);
  });

  test('should create manager with custom config', () => {
    manager = new BrowserManager({
      userDataDir: '/custom/path',
      headless: false,
      channel: 'chromium',
      timeout: 60000
    });
    
    expect(manager.userDataDir).toBe('/custom/path');
    expect(manager.headless).toBe(false);
    expect(manager.channel).toBe('chromium');
    expect(manager.timeout).toBe(60000);
  });

  test('should return null browser before launch', () => {
    manager = new BrowserManager();
    expect(manager.getBrowser()).toBeNull();
    expect(manager.isRunning()).toBe(false);
  });

  test('should handle close when browser not launched', async () => {
    manager = new BrowserManager();
    await expect(manager.close()).resolves.not.toThrow();
  });

  // Note: Actual browser launch tests are skipped in unit tests
  // They should be tested in integration/e2e tests
  test.skip('should launch browser successfully', async () => {
    manager = new BrowserManager({ headless: true });
    const browser = await manager.launch();
    
    expect(browser).toBeDefined();
    expect(manager.getBrowser()).toBe(browser);
    expect(manager.isRunning()).toBe(true);
  });

  test.skip('should close browser successfully', async () => {
    manager = new BrowserManager({ headless: true });
    await manager.launch();
    await manager.close();
    
    expect(manager.getBrowser()).toBeNull();
    expect(manager.isRunning()).toBe(false);
  });
});
