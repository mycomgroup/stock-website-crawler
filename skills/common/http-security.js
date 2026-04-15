/**
 * HTTP Security Toolkit
 * Provides secure HTTP client with anti-detection features for request-based API clients
 */

export const USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36';
export const SEC_CH_UA = '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"';

export class RateLimiter {
  constructor(maxRequestsPerMinute = 10) {
    this.maxRequestsPerMinute = maxRequestsPerMinute;
    this.minInterval = 60000 / maxRequestsPerMinute;
    this.lastRequestTime = 0;
    this.requestQueue = [];
  }

  async waitForSlot() {
    const now = Date.now();
    const timeSinceLastRequest = now - this.lastRequestTime;
    
    if (timeSinceLastRequest < this.minInterval) {
      const waitTime = this.minInterval - timeSinceLastRequest;
      await new Promise(resolve => setTimeout(resolve, waitTime));
    }
    
    this.lastRequestTime = Date.now();
  }
}

export class SecureHttpClient {
  constructor(options = {}) {
    this.baseUrl = options.baseUrl || '';
    this.maxRequestsPerMinute = options.maxRequestsPerMinute || 10;
    this.sessionValidator = options.sessionValidator;
    this.rateLimiter = new RateLimiter(this.maxRequestsPerMinute);
    this.currentUserAgent = USER_AGENT;
    this.currentSecChUa = SEC_CH_UA;
  }

  rotateUserAgent() {
  }

  async randomDelay(min = 1000, max = 3000) {
    const delay = Math.random() * (max - min) + min;
    await new Promise(resolve => setTimeout(resolve, delay));
  }

  async request(url, options = {}) {
    const {
      method = 'GET',
      headers = {},
      body = null,
      timeout = 30000,
      maxRetries = 3
    } = options;

    const fullUrl = url.startsWith('http') ? url : `${this.baseUrl}${url}`;

    for (let attempt = 0; attempt < maxRetries; attempt++) {
      if (this.sessionValidator) {
        const isValid = await this.sessionValidator();
        if (!isValid) {
          throw new Error('Session validation failed');
        }
      }

      await this.rateLimiter.waitForSlot();

      if (attempt > 0) {
        await this.randomDelay(1000, 2000);
      }

      try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), timeout);

        const fetchOptions = {
          method,
          headers: {
            'User-Agent': this.currentUserAgent,
            'sec-ch-ua': this.currentSecChUa,
            ...headers
          },
          signal: controller.signal
        };

        if (body) {
          fetchOptions.body = body;
        }

        const response = await fetch(fullUrl, fetchOptions);
        clearTimeout(timeoutId);

        if (response.status === 429) {
          const retryAfter = response.headers.get('Retry-After');
          const waitTime = retryAfter ? parseInt(retryAfter, 10) * 1000 : 60000;
          console.log(`Rate limited (429), waiting ${waitTime}ms before retry...`);
          await new Promise(resolve => setTimeout(resolve, waitTime));
          this.rotateUserAgent();
          continue;
        }

        if (response.status === 503) {
          const waitTime = 60000 * Math.pow(2, attempt);
          console.log(`Service unavailable (503), waiting ${waitTime}ms before retry...`);
          await new Promise(resolve => setTimeout(resolve, waitTime));
          continue;
        }

        if (response.status >= 500) {
          const waitTime = 10000 * Math.pow(2, attempt);
          console.log(`Server error (${response.status}), waiting ${waitTime}ms before retry...`);
          await new Promise(resolve => setTimeout(resolve, waitTime));
          continue;
        }

        if (!response.ok) {
          throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const text = await response.text();
        return text;

      } catch (error) {
        if (error.name === 'AbortError') {
          throw new Error(`Request timed out after ${timeout}ms`);
        }

        if (attempt === maxRetries - 1) {
          throw error;
        }

        const waitTime = 5000 * Math.pow(2, attempt);
        console.log(`Request failed: ${error.message}, retrying in ${waitTime}ms... (${attempt + 1}/${maxRetries})`);
        await new Promise(resolve => setTimeout(resolve, waitTime));
      }
    }

    throw new Error(`Max retries (${maxRetries}) exceeded`);
  }
}

export default {
  SecureHttpClient,
  RateLimiter,
  USER_AGENT,
  SEC_CH_UA
};