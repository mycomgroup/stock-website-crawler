import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';

/**
 * Browser Manager - 管理Playwright浏览器实例
 * 负责浏览器的启动、页面创建、导航和关闭
 */
class BrowserManager {
  constructor() {
    this.browser = null;
    this.context = null;
    this.storageStatePath = null;
  }

  /**
   * 启动浏览器
   * @param {Object} options - 浏览器选项
   * @param {boolean} options.headless - 是否无头模式，默认true
   * @param {number} options.timeout - 默认超时时间（毫秒），默认30000
   * @param {string} options.storageStatePath - Cookie存储路径，用于保持登录状态
   * @param {string} options.userDataDir - Chrome用户数据目录，用于复用当前浏览器的登录状态
   * @returns {Promise<void>}
   */
  async launch(options = {}) {
    const {
      headless = true,
      timeout = 30000,
      storageStatePath = null,
      userDataDir = null,
      ignoreHTTPSErrors = false
    } = options;
    
    this.storageStatePath = storageStatePath;
    
    // If userDataDir is provided, use persistent context to reuse browser profile
    if (userDataDir) {
      const persistentOptions = {
        headless,
        timeout,
        channel: 'chrome',
        viewport: { width: 1920, height: 1080 },
        userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        locale: 'en-US',
        ignoreHTTPSErrors,
        args: [
          '--disable-blink-features=AutomationControlled',
          '--disable-features=IsolateOrigins,site-per-process',
          '--no-sandbox',
          '--disable-setuid-sandbox'
        ]
      };

      try {
        this.context = await chromium.launchPersistentContext(userDataDir, persistentOptions);
        this.browser = this.context.browser();
        this.defaultTimeout = timeout;
        return;
      } catch (error) {
        console.warn('Failed to launch with user data dir, falling back to regular mode:', error.message);
        // Fall through to regular launch
      }
    }
    
    // Regular launch mode
    const launchOptions = {
      headless,
      timeout
    };
    
    // Try to use system Chrome if available, fallback to Chromium
    try {
      launchOptions.channel = 'chrome';
      this.browser = await chromium.launch(launchOptions);
    } catch (error) {
      // If Chrome channel fails, try without it (use bundled Chromium)
      delete launchOptions.channel;
      this.browser = await chromium.launch(launchOptions);
    }
    
    // Create a browser context with persistent storage
    const contextOptions = {
      viewport: { width: 1920, height: 1080 },
      userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
      locale: 'en-US',
      ignoreHTTPSErrors
    };
    
    // Load saved cookies/storage if exists
    if (this.storageStatePath && fs.existsSync(this.storageStatePath)) {
      try {
        contextOptions.storageState = this.storageStatePath;
      } catch (error) {
        // If loading fails, continue without saved state
        console.warn('Failed to load storage state:', error.message);
      }
    }
    
    this.context = await this.browser.newContext(contextOptions);
    
    this.defaultTimeout = timeout;
  }

  /**
   * 保存浏览器状态（cookies等）以便下次复用
   * @returns {Promise<void>}
   */
  async saveStorageState() {
    if (this.context && this.storageStatePath) {
      try {
        // Ensure directory exists
        const dir = path.dirname(this.storageStatePath);
        if (!fs.existsSync(dir)) {
          fs.mkdirSync(dir, { recursive: true });
        }
        
        await this.context.storageState({ path: this.storageStatePath });
      } catch (error) {
        console.warn('Failed to save storage state:', error.message);
      }
    }
  }

  /**
   * 创建新页面
   * @returns {Promise<Page>} Playwright页面对象
   * @throws {Error} 如果浏览器未启动
   */
  async newPage() {
    if (!this.context) {
      throw new Error('Browser not launched. Call launch() first.');
    }
    
    const page = await this.context.newPage();
    return page;
  }

  /**
   * 导航到URL
   * @param {Page} page - 页面对象
   * @param {string} url - 目标URL
   * @param {number} timeout - 超时时间（毫秒），可选
   * @returns {Promise<Response>} 页面响应对象
   * @throws {Error} 如果导航失败或超时
   */
  async goto(page, url, timeout) {
    const actualTimeout = timeout || this.defaultTimeout;
    
    try {
      const response = await page.goto(url, {
        timeout: actualTimeout,
        waitUntil: 'domcontentloaded'
      });
      
      return response;
    } catch (error) {
      throw new Error(`Failed to navigate to ${url}: ${error.message}`);
    }
  }

  /**
   * 等待页面加载完成
   * @param {Page} page - 页面对象
   * @param {number} timeout - 超时时间（毫秒），可选
   * @returns {Promise<void>}
   * @throws {Error} 如果等待超时
   */
  async waitForLoad(page, timeout) {
    const actualTimeout = timeout || this.defaultTimeout;

    try {
      // 使用 load 而不是 networkidle，对于 SPA 更可靠
      await page.waitForLoadState('load', {
        timeout: actualTimeout
      });
    } catch (error) {
      // 如果 load 也超时，尝试 domcontentloaded
      try {
        await page.waitForLoadState('domcontentloaded', { timeout: 5000 });
      } catch (e) {
        // 忽略，页面可能已经加载
      }
    }
  }

  /**
   * 关闭浏览器
   * @returns {Promise<void>}
   */
  async close() {
    if (this.context) {
      await this.context.close();
      this.context = null;
    }
    if (this.browser) {
      await this.browser.close();
      this.browser = null;
    }
  }
}

export default BrowserManager;
