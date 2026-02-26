import { chromium } from 'playwright';
import { resolve } from 'path';

/**
 * BrowserManager - Manages Playwright browser instances
 */
export class BrowserManager {
  /**
   * @param {Object} config - Configuration options
   * @param {string} config.userDataDir - Path to Chrome user data directory
   * @param {boolean} config.headless - Whether to run in headless mode (default: true)
   * @param {string} config.channel - Browser channel to use (default: 'chrome')
   * @param {number} config.timeout - Default timeout in milliseconds (default: 30000)
   */
  constructor(config = {}) {
    this.userDataDir = config.userDataDir || '../../stock-crawler/chrome_user_data';
    this.headless = config.headless !== false;
    this.channel = config.channel || 'chrome';
    this.timeout = config.timeout || 30000;
    this.browser = null;
  }

  /**
   * Launch browser with persistent context
   * @returns {Promise<BrowserContext>} Browser context
   */
  async launch() {
    try {
      const userDataDir = resolve(this.userDataDir);
      
      this.browser = await chromium.launchPersistentContext(userDataDir, {
        headless: this.headless,
        channel: this.channel,
        args: [
          '--no-sandbox',
          '--disable-setuid-sandbox',
          '--disable-dev-shm-usage',
          '--disable-blink-features=AutomationControlled'
        ],
        viewport: { width: 1920, height: 1080 }
      });

      return this.browser;
    } catch (error) {
      throw new Error(`Failed to launch browser: ${error.message}`);
    }
  }

  /**
   * Close browser
   */
  async close() {
    if (this.browser) {
      try {
        await this.browser.close();
        this.browser = null;
      } catch (error) {
        console.error('Error closing browser:', error.message);
      }
    }
  }

  /**
   * Get browser instance
   * @returns {BrowserContext|null} Browser context or null if not launched
   */
  getBrowser() {
    return this.browser;
  }

  /**
   * Check if browser is running
   * @returns {boolean} True if browser is running
   */
  isRunning() {
    return this.browser !== null;
  }
}
