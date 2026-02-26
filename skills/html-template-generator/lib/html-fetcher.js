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
      
      // Wait a bit for any dynamic content to load
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
   * Set timeout for page loads
   * @param {number} timeout - Timeout in milliseconds
   */
  setTimeout(timeout) {
    this.timeout = timeout;
  }
}
