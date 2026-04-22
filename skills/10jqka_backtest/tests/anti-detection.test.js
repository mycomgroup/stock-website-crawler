import { jest, describe, test, expect, beforeEach, afterEach } from '@jest/globals';
import fs from 'node:fs';
import path from 'node:path';
import { AntiDetection, SessionManager, RateLimiter } from '../lib/anti-detection.js';

describe('AntiDetection', () => {
  describe('setupBrowser', () => {
    test('should create browser with default options', async () => {
      const browser = await AntiDetection.setupBrowser();
      expect(browser).toBeDefined();
      await browser.close();
    }, 30000);

    test('should create browser with headless mode', async () => {
      const browser = await AntiDetection.setupBrowser({ headless: true });
      expect(browser).toBeDefined();
      await browser.close();
    }, 30000);

    test('should create browser with non-headless mode', async () => {
      const browser = await AntiDetection.setupBrowser({ headless: false });
      expect(browser).toBeDefined();
      await browser.close();
    }, 30000);

    test('should include required args', async () => {
      const browser = await AntiDetection.setupBrowser();
      expect(browser).toBeDefined();
      await browser.close();
    }, 30000);

    test('should accept custom args', async () => {
      const browser = await AntiDetection.setupBrowser({
        args: ['--custom-arg']
      });
      expect(browser).toBeDefined();
      await browser.close();
    }, 30000);
  });

  describe('injectAntiDetection', () => {
    test('should inject script successfully', async () => {
      const browser = await AntiDetection.setupBrowser({ headless: true });
      const page = await browser.newPage();
      
      await AntiDetection.injectAntiDetection(page);
      
      await page.goto('https://example.com');
      
      const webdriver = await page.evaluate(() => navigator.webdriver);
      expect(webdriver).toBeUndefined();
      
      await browser.close();
    }, 30000);

    test('should define chrome object', async () => {
      const browser = await AntiDetection.setupBrowser({ headless: true });
      const page = await browser.newPage();
      
      await AntiDetection.injectAntiDetection(page);
      await page.goto('https://example.com');
      
      const hasChrome = await page.evaluate(() => !!window.chrome);
      expect(hasChrome).toBe(true);
      
      await browser.close();
    }, 30000);

    test('should set plugins', async () => {
      const browser = await AntiDetection.setupBrowser({ headless: true });
      const page = await browser.newPage();
      
      await AntiDetection.injectAntiDetection(page);
      await page.goto('https://example.com');
      
      const plugins = await page.evaluate(() => navigator.plugins.length);
      expect(plugins).toBeGreaterThan(0);
      
      await browser.close();
    }, 30000);

    test('should set languages', async () => {
      const browser = await AntiDetection.setupBrowser({ headless: true });
      const page = await browser.newPage();
      
      await AntiDetection.injectAntiDetection(page);
      await page.goto('https://example.com');
      
      const languages = await page.evaluate(() => navigator.languages);
      expect(languages).toContain('zh-CN');
      expect(languages).toContain('zh');
      
      await browser.close();
    }, 30000);

    test('should set hardwareConcurrency', async () => {
      const browser = await AntiDetection.setupBrowser({ headless: true });
      const page = await browser.newPage();
      
      await AntiDetection.injectAntiDetection(page);
      await page.goto('https://example.com');
      
      const concurrency = await page.evaluate(() => navigator.hardwareConcurrency);
      expect(concurrency).toBe(8);
      
      await browser.close();
    }, 30000);

    test('should set deviceMemory', async () => {
      const browser = await AntiDetection.setupBrowser({ headless: true });
      const page = await browser.newPage();
      
      await AntiDetection.injectAntiDetection(page);
      await page.goto('https://example.com');
      
      const memory = await page.evaluate(() => navigator.deviceMemory);
      expect(memory).toBe(8);
      
      await browser.close();
    }, 30000);

    test('should set timezone offset', async () => {
      const browser = await AntiDetection.setupBrowser({ headless: true });
      const page = await browser.newPage();
      
      await AntiDetection.injectAntiDetection(page);
      await page.goto('https://example.com');
      
      const offset = await page.evaluate(() => new Date().getTimezoneOffset());
      expect(offset).toBe(-480);
      
      await browser.close();
    }, 30000);
  });

  describe('setRealisticHeaders', () => {
    test('should set default headers', async () => {
      const browser = await AntiDetection.setupBrowser({ headless: true });
      const page = await browser.newPage();
      
      await AntiDetection.setRealisticHeaders(page);
      
      const headers = await page.evaluate(() => ({
        acceptLanguage: navigator.language
      }));
      
      await browser.close();
    }, 30000);

    test('should merge custom headers', async () => {
      const browser = await AntiDetection.setupBrowser({ headless: true });
      const page = await browser.newPage();
      
      await AntiDetection.setRealisticHeaders(page, {
        'Custom-Header': 'custom-value'
      });
      
      await browser.close();
    }, 30000);
  });

  describe('randomDelay', () => {
    test('should delay for random time within range', async () => {
      const start = Date.now();
      await AntiDetection.randomDelay(100, 200);
      const elapsed = Date.now() - start;
      
      expect(elapsed).toBeGreaterThanOrEqual(100);
      expect(elapsed).toBeLessThanOrEqual(200 + 50);
    });

    test('should accept custom min and max', async () => {
      const start = Date.now();
      await AntiDetection.randomDelay(50, 100);
      const elapsed = Date.now() - start;
      
      expect(elapsed).toBeGreaterThanOrEqual(50);
    });

    test('should handle equal min and max', async () => {
      const start = Date.now();
      await AntiDetection.randomDelay(100, 100);
      const elapsed = Date.now() - start;
      
      expect(elapsed).toBeGreaterThanOrEqual(100);
    });
  });

  describe('getRandomUserAgent', () => {
    test('should return a valid user agent string', () => {
      const ua = AntiDetection.getRandomUserAgent();
      expect(ua).toContain('Mozilla');
      expect(ua).toContain('Chrome');
    });

    test('should return different user agents on multiple calls', () => {
      const results = new Set();
      for (let i = 0; i < 20; i++) {
        results.add(AntiDetection.getRandomUserAgent());
      }
      expect(results.size).toBeGreaterThan(1);
    });

    test('should return user agent from predefined list', () => {
      const ua = AntiDetection.getRandomUserAgent();
      const userAgents = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
      ];
      expect(userAgents).toContain(ua);
    });
  });

  describe('simulateHumanBehavior', () => {
    test('should simulate mouse movement and scrolling', async () => {
      const browser = await AntiDetection.setupBrowser({ headless: true });
      const page = await browser.newPage();
      
      await page.goto('https://example.com');
      await AntiDetection.simulateHumanBehavior(page);
      
      await browser.close();
    }, 30000);

    test('should complete without errors', async () => {
      const browser = await AntiDetection.setupBrowser({ headless: true });
      const page = await browser.newPage();
      
      await page.goto('https://example.com');
      
      await expect(AntiDetection.simulateHumanBehavior(page))
        .resolves.not.toThrow();
      
      await browser.close();
    }, 30000);
  });

  describe('fetchWithRetry', () => {
    test('should return response on success', async () => {
      const mockFetch = jest.fn(() => Promise.resolve({
        ok: true,
        status: 200
      }));
      
      const result = await AntiDetection.fetchWithRetry(mockFetch);
      expect(result.ok).toBe(true);
      expect(mockFetch).toHaveBeenCalledTimes(1);
    });

    test('should retry on 429 status', async () => {
      const mockFetch = jest.fn()
        .mockResolvedValueOnce({ ok: false, status: 429 })
        .mockResolvedValueOnce({ ok: true, status: 200 });
      
      const result = await AntiDetection.fetchWithRetry(mockFetch, {
        retryDelay: 100
      });
      
      expect(result.ok).toBe(true);
      expect(mockFetch).toHaveBeenCalledTimes(2);
    });

    test('should retry on error', async () => {
      const mockFetch = jest.fn()
        .mockRejectedValueOnce(new Error('Network error'))
        .mockResolvedValueOnce({ ok: true, status: 200 });
      
      const result = await AntiDetection.fetchWithRetry(mockFetch, {
        retryDelay: 100,
        maxRetries: 2
      });
      
      expect(result.ok).toBe(true);
      expect(mockFetch).toHaveBeenCalledTimes(2);
    });

    test('should throw after max retries', async () => {
      const mockFetch = jest.fn()
        .mockRejectedValue(new Error('Network error'));
      
      await expect(AntiDetection.fetchWithRetry(mockFetch, {
        retryDelay: 100,
        maxRetries: 3
      })).rejects.toThrow('Network error');
      
      expect(mockFetch).toHaveBeenCalledTimes(3);
    });

    test('should throw on non-429 error status', async () => {
      const mockFetch = jest.fn(() => Promise.resolve({
        ok: false,
        status: 500,
        statusText: 'Internal Server Error'
      }));
      
      await expect(AntiDetection.fetchWithRetry(mockFetch))
        .rejects.toThrow('HTTP 500');
    });

    test('should use backoff strategy', async () => {
      const mockFetch = jest.fn()
        .mockRejectedValueOnce(new Error('Error'))
        .mockRejectedValueOnce(new Error('Error'))
        .mockResolvedValueOnce({ ok: true });
      
      const start = Date.now();
      await AntiDetection.fetchWithRetry(mockFetch, {
        retryDelay: 100,
        backoff: true,
        maxRetries: 3
      });
      const elapsed = Date.now() - start;
      
      expect(mockFetch).toHaveBeenCalledTimes(3);
      expect(elapsed).toBeGreaterThan(100);
    });
  });

  describe('createRealisticHeaders', () => {
    test('should create headers with all required fields', () => {
      const headers = AntiDetection.createRealisticHeaders();
      
      expect(headers).toHaveProperty('User-Agent');
      expect(headers).toHaveProperty('Accept');
      expect(headers).toHaveProperty('Accept-Language');
      expect(headers).toHaveProperty('Accept-Encoding');
      expect(headers).toHaveProperty('Connection');
      expect(headers).toHaveProperty('Sec-Fetch-Dest');
      expect(headers).toHaveProperty('Sec-Fetch-Mode');
      expect(headers).toHaveProperty('Sec-Fetch-Site');
      expect(headers).toHaveProperty('Sec-Ch-Ua');
      expect(headers).toHaveProperty('Sec-Ch-Ua-Mobile');
      expect(headers).toHaveProperty('Sec-Ch-Ua-Platform');
    });

    test('should merge custom headers', () => {
      const headers = AntiDetection.createRealisticHeaders({
        'X-Custom': 'custom-value'
      });
      
      expect(headers['X-Custom']).toBe('custom-value');
    });

    test('should override default headers with custom', () => {
      const headers = AntiDetection.createRealisticHeaders({
        'Accept': 'custom-accept'
      });
      
      expect(headers['Accept']).toBe('custom-accept');
    });

    test('should set correct Accept-Language', () => {
      const headers = AntiDetection.createRealisticHeaders();
      expect(headers['Accept-Language']).toBe('zh-CN,zh;q=0.9,en;q=0.8');
    });

    test('should set correct Sec-Ch-Ua-Mobile', () => {
      const headers = AntiDetection.createRealisticHeaders();
      expect(headers['Sec-Ch-Ua-Mobile']).toBe('?0');
    });
  });
});

describe('SessionManager', () => {
  const testSessionFile = './tests/fixtures/test-session-manager.json';

  beforeEach(() => {
    if (!fs.existsSync('./tests/fixtures')) {
      fs.mkdirSync('./tests/fixtures', { recursive: true });
    }
  });

  afterEach(() => {
    if (fs.existsSync(testSessionFile)) {
      fs.unlinkSync(testSessionFile);
    }
  });

  describe('constructor', () => {
    test('should create instance with session file', () => {
      const manager = new SessionManager(testSessionFile);
      expect(manager.sessionFile).toBe(testSessionFile);
    });

    test('should use default maxAge', () => {
      const manager = new SessionManager(testSessionFile);
      expect(manager.maxAge).toBe(7 * 24 * 60 * 60 * 1000);
    });

    test('should accept custom maxAge', () => {
      const customMaxAge = 3 * 24 * 60 * 60 * 1000;
      const manager = new SessionManager(testSessionFile, { maxAge: customMaxAge });
      expect(manager.maxAge).toBe(customMaxAge);
    });

    test('should accept validateUrl', () => {
      const manager = new SessionManager(testSessionFile, {
        validateUrl: 'https://test.com'
      });
      expect(manager.validateUrl).toBe('https://test.com');
    });
  });

  describe('load', () => {
    test('should load session from file', async () => {
      const session = { cookies: [{ name: 'test', value: '123' }] };
      fs.writeFileSync(testSessionFile, JSON.stringify(session));
      
      const manager = new SessionManager(testSessionFile);
      const loaded = await manager.load();
      
      expect(loaded.cookies).toHaveLength(1);
    });

    test('should return null for non-existent file', async () => {
      const manager = new SessionManager('./tests/fixtures/non-existent.json');
      const loaded = await manager.load();
      
      expect(loaded).toBeNull();
    });

    test('should return null for invalid JSON', async () => {
      fs.writeFileSync(testSessionFile, 'invalid json');
      
      const manager = new SessionManager(testSessionFile);
      const loaded = await manager.load();
      
      expect(loaded).toBeNull();
    });
  });

  describe('save', () => {
    test('should save session to file', async () => {
      const manager = new SessionManager(testSessionFile);
      const session = { cookies: [{ name: 'test', value: '123' }] };
      
      await manager.save(session);
      
      expect(fs.existsSync(testSessionFile)).toBe(true);
      const saved = JSON.parse(fs.readFileSync(testSessionFile, 'utf8'));
      expect(saved.cookies).toHaveLength(1);
    });

    test('should add capturedAt timestamp', async () => {
      const manager = new SessionManager(testSessionFile);
      const session = { cookies: [] };
      
      await manager.save(session);
      
      const saved = JSON.parse(fs.readFileSync(testSessionFile, 'utf8'));
      expect(saved.capturedAt).toBeDefined();
    });

    test('should create directory if not exists', async () => {
      const newDir = './tests/fixtures/new-dir/session.json';
      const manager = new SessionManager(newDir);
      
      await manager.save({ cookies: [] });
      
      expect(fs.existsSync('./tests/fixtures/new-dir')).toBe(true);
      fs.rmSync('./tests/fixtures/new-dir', { recursive: true, force: true });
    });
  });

  describe('isValid', () => {
    test('should return false for non-existent session', async () => {
      const manager = new SessionManager('./tests/fixtures/non-existent.json');
      const valid = await manager.isValid();
      
      expect(valid).toBe(false);
    });

    test('should return false for session without capturedAt', async () => {
      fs.writeFileSync(testSessionFile, JSON.stringify({ cookies: [] }));
      
      const manager = new SessionManager(testSessionFile);
      const valid = await manager.isValid();
      
      expect(valid).toBe(false);
    });

    test('should return false for expired session', async () => {
      const oldDate = new Date(Date.now() - 10 * 24 * 60 * 60 * 1000).toISOString();
      fs.writeFileSync(testSessionFile, JSON.stringify({
        cookies: [{ name: 'test', value: '123' }],
        capturedAt: oldDate
      }));
      
      const manager = new SessionManager(testSessionFile);
      const valid = await manager.isValid();
      
      expect(valid).toBe(false);
    });

    test('should return true for valid session', async () => {
      const freshDate = new Date().toISOString();
      fs.writeFileSync(testSessionFile, JSON.stringify({
        cookies: [{ name: 'test', value: '123' }],
        capturedAt: freshDate
      }));
      
      const manager = new SessionManager(testSessionFile);
      const valid = await manager.isValid();
      
      expect(valid).toBe(true);
    });
  });

  describe('validateCookies', () => {
    test('should return true without validateUrl', async () => {
      const manager = new SessionManager(testSessionFile);
      const valid = await manager.validateCookies([{ name: 'test', value: '123' }]);
      
      expect(valid).toBe(true);
    });

    test('should validate cookies with validateUrl', async () => {
      const manager = new SessionManager(testSessionFile, {
        validateUrl: 'https://example.com'
      });
      
      const mockFetch = jest.fn(() => Promise.resolve({
        ok: true
      }));
      global.fetch = mockFetch;
      
      const valid = await manager.validateCookies([{ name: 'test', value: '123' }]);
      expect(valid).toBe(true);
      
      mockFetch.mockRestore();
    });

    test('should return false on validation error', async () => {
      const manager = new SessionManager(testSessionFile, {
        validateUrl: 'https://example.com'
      });
      
      const mockFetch = jest.fn(() => Promise.resolve({
        ok: false
      }));
      global.fetch = mockFetch;
      
      const valid = await manager.validateCookies([{ name: 'test', value: '123' }]);
      expect(valid).toBe(false);
      
      mockFetch.mockRestore();
    });

    test('should return false on fetch error', async () => {
      const manager = new SessionManager(testSessionFile, {
        validateUrl: 'https://example.com'
      });
      
      const mockFetch = jest.fn(() => Promise.reject(new Error('Network error')));
      global.fetch = mockFetch;
      
      const valid = await manager.validateCookies([{ name: 'test', value: '123' }]);
      expect(valid).toBe(false);
      
      mockFetch.mockRestore();
    });
  });

  describe('clear', () => {
    test('should delete session file', async () => {
      fs.writeFileSync(testSessionFile, JSON.stringify({ cookies: [] }));
      
      const manager = new SessionManager(testSessionFile);
      await manager.clear();
      
      expect(fs.existsSync(testSessionFile)).toBe(false);
    });

    test('should handle non-existent file', async () => {
      const manager = new SessionManager('./tests/fixtures/non-existent.json');
      
      await expect(manager.clear()).resolves.not.toThrow();
    });
  });
});

describe('RateLimiter', () => {
  describe('constructor', () => {
    test('should create instance with default options', () => {
      const limiter = new RateLimiter();
      expect(limiter.minDelay).toBe(1000);
      expect(limiter.maxDelay).toBe(3000);
    });

    test('should create instance with custom delays', () => {
      const limiter = new RateLimiter({
        minDelay: 500,
        maxDelay: 2000
      });
      
      expect(limiter.minDelay).toBe(500);
      expect(limiter.maxDelay).toBe(2000);
    });
  });

  describe('wait', () => {
    test('should not wait on first request if lastRequestTime is 0', async () => {
      const limiter = new RateLimiter({ minDelay: 100, maxDelay: 150 });
      
      const start = Date.now();
      await limiter.wait();
      const elapsed = Date.now() - start;
      
      expect(elapsed).toBeLessThan(100);
    });

    test('should wait between requests', async () => {
      const limiter = new RateLimiter({ minDelay: 100, maxDelay: 150 });
      
      await limiter.wait();
      
      const start = Date.now();
      await limiter.wait();
      const elapsed = Date.now() - start;
      
      expect(elapsed).toBeGreaterThanOrEqual(100);
    });

    test('should not wait if enough time elapsed', async () => {
      const limiter = new RateLimiter({ minDelay: 100, maxDelay: 150 });
      
      await limiter.wait();
      await new Promise(resolve => setTimeout(resolve, 200));
      
      const start = Date.now();
      await limiter.wait();
      const elapsed = Date.now() - start;
      
      expect(elapsed).toBeLessThan(100);
    });

    test('should update lastRequestTime', async () => {
      const limiter = new RateLimiter();
      
      expect(limiter.lastRequestTime).toBe(0);
      
      await limiter.wait();
      
      expect(limiter.lastRequestTime).toBeGreaterThan(0);
    });
  });
});