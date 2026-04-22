/**
 * 浏览器防封工具包
 * 提供统一的反检测、请求随机化、Session管理等功能
 */

import { chromium } from 'playwright';

/**
 * 反检测工具类
 */
export class AntiDetection {
  /**
   * 设置反检测浏览器
   * @param {Object} options - 浏览器配置选项
   * @returns {Promise<Browser>}
   */
  static async setupBrowser(options = {}) {
    const defaultArgs = [
      '--disable-blink-features=AutomationControlled',
      '--disable-dev-shm-usage',
      '--disable-setuid-sandbox',
      '--no-sandbox',
      '--disable-web-security',
      '--disable-features=IsolateOrigins,site-per-process',
      '--disable-site-isolation-trials',
      '--disable-features=BlockInsecurePrivateNetworkRequests'
    ];

    const browser = await chromium.launch({
      headless: options.headless !== false,
      args: [...defaultArgs, ...(options.args || [])],
      ...options
    });

    return browser;
  }

  /**
   * 注入反检测脚本到页面
   * @param {Page} page - Playwright页面对象
   */
  static async injectAntiDetection(page) {
    await page.addInitScript(() => {
      // 移除 webdriver 标记
      Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined,
        configurable: true
      });

      // 模拟真实浏览器插件
      Object.defineProperty(navigator, 'plugins', {
        get: () => [
          { name: 'Chrome PDF Plugin' },
          { name: 'Chrome PDF Viewer' },
          { name: 'Native Client' }
        ],
        configurable: true
      });

      // 模拟 Chrome 对象
      window.chrome = {
        runtime: {},
        loadTimes: function() {},
        csi: function() {},
        app: {}
      };

      // 模拟权限查询
      const originalQuery = window.navigator.permissions.query;
      window.navigator.permissions.query = (parameters) => (
        parameters.name === 'notifications' ?
          Promise.resolve({ state: Notification.permission }) :
          originalQuery(parameters)
      );

      // 覆盖 navigator.languages
      Object.defineProperty(navigator, 'languages', {
        get: () => ['zh-CN', 'zh', 'en-US', 'en'],
        configurable: true
      });

      // 模拟真实的 hardwareConcurrency
      Object.defineProperty(navigator, 'hardwareConcurrency', {
        get: () => 8,
        configurable: true
      });

      // 模拟真实的 deviceMemory
      Object.defineProperty(navigator, 'deviceMemory', {
        get: () => 8,
        configurable: true
      });

      // 覆盖 Date.prototype.getTimezoneOffset
      const originalGetTimezoneOffset = Date.prototype.getTimezoneOffset;
      Date.prototype.getTimezoneOffset = function() {
        return -480; // UTC+8 (中国时区)
      };
    });
  }

  /**
   * 设置真实的浏览器headers
   * @param {Page} page - Playwright页面对象
   * @param {Object} customHeaders - 自定义headers
   */
  static async setRealisticHeaders(page, customHeaders = {}) {
    const defaultHeaders = {
      'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
      'Accept-Encoding': 'gzip, deflate, br',
      'Connection': 'keep-alive',
      'Sec-Fetch-Dest': 'document',
      'Sec-Fetch-Mode': 'navigate',
      'Sec-Fetch-Site': 'none',
      'Sec-Fetch-User': '?1',
      'Upgrade-Insecure-Requests': '1',
      'User-Agent': this.getRandomUserAgent()
    };

    await page.setExtraHTTPHeaders({
      ...defaultHeaders,
      ...customHeaders
    });
  }

  /**
   * 随机延迟
   * @param {number} min - 最小延迟(ms)
   * @param {number} max - 最大延迟(ms)
   * @returns {Promise<void>}
   */
  static async randomDelay(min = 1000, max = 3000) {
    const delay = Math.random() * (max - min) + min;
    await new Promise(resolve => setTimeout(resolve, delay));
  }

  /**
   * 获取随机User-Agent
   * @returns {string}
   */
  static getRandomUserAgent() {
    const userAgents = [
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
      'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    ];
    return userAgents[Math.floor(Math.random() * userAgents.length)];
  }

  /**
   * 模拟人类鼠标移动
   * @param {Page} page - Playwright页面对象
   */
  static async simulateHumanBehavior(page) {
    // 随机移动鼠标
    const x = Math.random() * 500 + 100;
    const y = Math.random() * 500 + 100;
    await page.mouse.move(x, y, { steps: 10 });
    
    // 随机滚动
    await page.evaluate(() => {
      window.scrollBy(0, Math.random() * 200);
    });
    
    await this.randomDelay(500, 1500);
  }

  /**
   * 带重试的HTTP请求
   * @param {Function} fetchFn - 请求函数
   * @param {Object} options - 选项
   * @returns {Promise<Response>}
   */
  static async fetchWithRetry(fetchFn, options = {}) {
    const {
      maxRetries = 3,
      retryDelay = 1000,
      backoff = true
    } = options;

    let lastError = null;
    
    for (let i = 0; i < maxRetries; i++) {
      try {
        const response = await fetchFn();
        
        if (response.ok) {
          return response;
        }
        
        if (response.status === 429) {
          const delay = backoff ? retryDelay * Math.pow(2, i) : retryDelay;
          console.log(`Rate limited, waiting ${delay}ms before retry...`);
          await this.randomDelay(delay, delay + 2000);
          lastError = new Error(`HTTP ${response.status}: ${response.statusText}`);
          continue;
        }
        
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      } catch (error) {
        lastError = error;
        if (i === maxRetries - 1) {
          throw error;
        }
        
        const delay = backoff ? retryDelay * Math.pow(2, i) : retryDelay;
        console.log(`Request failed, retrying in ${delay}ms... (${i + 1}/${maxRetries})`);
        await this.randomDelay(delay, delay + 1000);
      }
    }
    
    if (lastError) {
      throw lastError;
    }
    
    throw new Error('Max retries exceeded without a successful response');
  }

  /**
   * 创建真实的HTTP请求headers
   * @param {Object} customHeaders - 自定义headers
   * @returns {Object}
   */
  static createRealisticHeaders(customHeaders = {}) {
    return {
      'User-Agent': this.getRandomUserAgent(),
      'Accept': 'application/json, text/plain, */*',
      'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
      'Accept-Encoding': 'gzip, deflate, br',
      'Connection': 'keep-alive',
      'Sec-Fetch-Dest': 'empty',
      'Sec-Fetch-Mode': 'cors',
      'Sec-Fetch-Site': 'same-origin',
      'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
      'Sec-Ch-Ua-Mobile': '?0',
      'Sec-Ch-Ua-Platform': '"macOS"',
      ...customHeaders
    };
  }
}

/**
 * Session管理器
 */
export class SessionManager {
  constructor(sessionFile, options = {}) {
    this.sessionFile = sessionFile;
    this.maxAge = options.maxAge || 7 * 24 * 60 * 60 * 1000; // 默认7天
    this.validateUrl = options.validateUrl;
  }

  /**
   * 加载session
   * @returns {Promise<Object|null>}
   */
  async load() {
    try {
      const fs = await import('fs/promises');
      const content = await fs.readFile(this.sessionFile, 'utf-8');
      return JSON.parse(content);
    } catch (error) {
      return null;
    }
  }

  /**
   * 保存session
   * @param {Object} session - Session数据
   */
  async save(session) {
    const fs = await import('fs/promises');
    const path = await import('path');
    
    // 确保目录存在
    const dir = path.dirname(this.sessionFile);
    await fs.mkdir(dir, { recursive: true });
    
    // 添加捕获时间
    session.capturedAt = new Date().toISOString();
    
    await fs.writeFile(
      this.sessionFile,
      JSON.stringify(session, null, 2),
      'utf-8'
    );
  }

  /**
   * 检查session是否有效
   * @returns {Promise<boolean>}
   */
  async isValid() {
    const session = await this.load();
    if (!session || !session.capturedAt) {
      return false;
    }

    // 检查年龄
    const age = Date.now() - new Date(session.capturedAt).getTime();
    if (age > this.maxAge) {
      console.log('Session expired due to age');
      return false;
    }

    // 如果提供了验证URL，验证cookies
    if (this.validateUrl && session.cookies) {
      return await this.validateCookies(session.cookies);
    }

    return true;
  }

  /**
   * 验证cookies是否有效
   * @param {Array} cookies - Cookie数组
   * @returns {Promise<boolean>}
   */
  async validateCookies(cookies) {
    if (!this.validateUrl) {
      return true;
    }

    try {
      const cookieString = cookies
        .map(c => `${c.name}=${c.value}`)
        .join('; ');

      const response = await fetch(this.validateUrl, {
        headers: {
          'Cookie': cookieString,
          ...AntiDetection.createRealisticHeaders()
        }
      });

      return response.ok;
    } catch (error) {
      console.error('Cookie validation failed:', error.message);
      return false;
    }
  }

  /**
   * 清除session
   */
  async clear() {
    try {
      const fs = await import('fs/promises');
      await fs.unlink(this.sessionFile);
    } catch (error) {
      // 文件不存在，忽略错误
    }
  }
}

/**
 * 请求限流器
 */
export class RateLimiter {
  constructor(options = {}) {
    this.minDelay = options.minDelay || 1000;
    this.maxDelay = options.maxDelay || 3000;
    this.lastRequestTime = 0;
  }

  /**
   * 等待直到可以发送下一个请求
   */
  async wait() {
    const now = Date.now();
    const timeSinceLastRequest = now - this.lastRequestTime;
    const delay = Math.random() * (this.maxDelay - this.minDelay) + this.minDelay;
    
    if (timeSinceLastRequest < delay) {
      await new Promise(resolve => 
        setTimeout(resolve, delay - timeSinceLastRequest)
      );
    }
    
    this.lastRequestTime = Date.now();
  }
}

export default {
  AntiDetection,
  SessionManager,
  RateLimiter
};
