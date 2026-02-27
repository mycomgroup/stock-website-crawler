/**
 * HTMLFetcher - Fetches HTML content from URLs using Playwright
 */
export class HTMLFetcher {
  /**
   * @param {BrowserManager} browserManager - Browser manager instance
   * @param {number} timeout - Timeout in milliseconds (default: 30000)
   */
  constructor(browserManager, timeout = 30000) {
    this.browserManager = browserManager;
    this.timeout = timeout;
  }

  /**
   * Fetch HTML from multiple URLs
   * @param {string[]} urls - Array of URLs to fetch
   * @returns {Promise<Array<{url: string, html: string, title: string, timestamp: string}>>}
   */
  async fetchAll(urls) {
    const results = [];
    
    for (const url of urls) {
      try {
        console.log(`  Fetching: ${url}`);
        const content = await this.fetchOne(url);
        results.push(content);
      } catch (error) {
        console.error(`  ✗ Failed to fetch ${url}: ${error.message}`);
        // Continue with other URLs even if one fails
      }
    }
    
    return results;
  }

  /**
   * Fetch HTML from a single URL
   * @param {string} url - URL to fetch
   * @returns {Promise<{url: string, html: string, title: string, timestamp: string}>}
   */
  async fetchOne(url) {
    const browser = this.browserManager.getBrowser();
    
    if (!browser) {
      throw new Error('Browser not launched. Call browserManager.launch() first.');
    }

    const page = await browser.newPage();
    
    try {
      // Navigate to URL and wait for network to be idle
      await page.goto(url, { 
        waitUntil: 'networkidle',
        timeout: this.timeout 
      });
      
      // Wait for SPA to render - try multiple strategies
      await this._waitForSPAContent(page);
      
      // Scroll to load lazy content
      await this._scrollPage(page);
      
      // Final wait for any animations
      await page.waitForTimeout(1000);
      
      // Extract content
      const html = await page.content();
      const title = await page.title();
      const finalUrl = page.url();
      
      return {
        url: finalUrl,
        html,
        title,
        timestamp: new Date().toISOString()
      };
    } catch (error) {
      if (error.name === 'TimeoutError') {
        throw new Error(`Timeout loading ${url} after ${this.timeout}ms`);
      }
      throw new Error(`Failed to fetch ${url}: ${error.message}`);
    } finally {
      await page.close();
    }
  }

  /**
   * Wait for SPA content to load
   * @param {Page} page - Playwright page
   * @private
   */
  async _waitForSPAContent(page) {
    // Strategy 1: Wait for common content selectors
    const selectors = [
      'main',
      '[role="main"]',
      '.content',
      '.main-content',
      '#content',
      '.container',
      'article',
      '.data-booth' // 理杏仁特定
    ];
    
    for (const selector of selectors) {
      try {
        await page.waitForSelector(selector, { timeout: 3000, state: 'visible' });
        console.log(`  ✓ Found content: ${selector}`);
        break;
      } catch (e) {
        // Try next selector
      }
    }
    
    // Strategy 2: Wait for Vue/React to finish rendering
    await page.waitForTimeout(2000);
    
    // Strategy 3: Wait for no new DOM mutations
    try {
      await page.waitForFunction(() => {
        return new Promise((resolve) => {
          let timeout;
          const observer = new MutationObserver(() => {
            clearTimeout(timeout);
            timeout = setTimeout(() => {
              observer.disconnect();
              resolve(true);
            }, 500);
          });
          
          observer.observe(document.body, {
            childList: true,
            subtree: true
          });
          
          // Start initial timeout
          timeout = setTimeout(() => {
            observer.disconnect();
            resolve(true);
          }, 500);
        });
      }, { timeout: 5000 });
      console.log('  ✓ DOM stable');
    } catch (e) {
      // Continue anyway
    }
  }

  /**
   * Scroll page to trigger lazy loading
   * @param {Page} page - Playwright page
   * @private
   */
  async _scrollPage(page) {
    try {
      // Scroll to bottom
      await page.evaluate(() => {
        window.scrollTo(0, document.body.scrollHeight);
      });
      await page.waitForTimeout(500);
      
      // Scroll to middle
      await page.evaluate(() => {
        window.scrollTo(0, document.body.scrollHeight / 2);
      });
      await page.waitForTimeout(500);
      
      // Scroll back to top
      await page.evaluate(() => {
        window.scrollTo(0, 0);
      });
      await page.waitForTimeout(500);
      
      console.log('  ✓ Scrolled page');
    } catch (e) {
      // Scroll failed, continue anyway
    }
  }

  /**
   * Set timeout for page loads
   * @param {number} timeout - Timeout in milliseconds
   */
  setTimeout(timeout) {
    this.timeout = timeout;
  }
}
