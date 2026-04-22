import { describe, it, beforeEach, mock } from 'node:test';
import assert from 'node:assert';

describe('AntiDetection - static methods', () => {
  describe('getRandomUserAgent', () => {
    it('should return valid user agent string', async () => {
      const { AntiDetection } = await import('../lib/anti-detection.js');
      
      const ua = AntiDetection.getRandomUserAgent();
      
      assert.ok(ua.includes('Mozilla'));
      assert.ok(ua.includes('Chrome'));
    });

    it('should return different user agents on multiple calls', async () => {
      const { AntiDetection } = await import('../lib/anti-detection.js?cachebuster=' + Date.now());
      
      const uas = new Set();
      for (let i = 0; i < 50; i++) {
        uas.add(AntiDetection.getRandomUserAgent());
      }
      
      assert.ok(uas.size > 1);
    });

    it('should return Chrome user agents', async () => {
      const { AntiDetection } = await import('../lib/anti-detection.js?cachebuster=' + Date.now());
      
      for (let i = 0; i < 10; i++) {
        const ua = AntiDetection.getRandomUserAgent();
        assert.ok(ua.includes('Chrome'));
      }
    });

    it('should contain valid version numbers', async () => {
      const { AntiDetection } = await import('../lib/anti-detection.js?cachebuster=' + Date.now());
      
      const ua = AntiDetection.getRandomUserAgent();
      assert.ok(/\d+\.\d+\.\d+\.\d+/.test(ua));
    });
  });

  describe('createRealisticHeaders', () => {
    it('should return headers object', async () => {
      const { AntiDetection } = await import('../lib/anti-detection.js?cachebuster=' + Date.now());
      
      const headers = AntiDetection.createRealisticHeaders();
      
      assert.ok(headers['User-Agent']);
      assert.ok(headers['Accept']);
      assert.ok(headers['Accept-Language']);
    });

    it('should merge custom headers', async () => {
      const { AntiDetection } = await import('../lib/anti-detection.js?cachebuster=' + Date.now());
      
      const headers = AntiDetection.createRealisticHeaders({ 'X-Custom': 'value' });
      
      assert.strictEqual(headers['X-Custom'], 'value');
    });

    it('should override default headers with custom', async () => {
      const { AntiDetection } = await import('../lib/anti-detection.js?cachebuster=' + Date.now());
      
      const headers = AntiDetection.createRealisticHeaders({ 'User-Agent': 'CustomUA' });
      
      assert.strictEqual(headers['User-Agent'], 'CustomUA');
    });

    it('should include sec-ch-ua headers', async () => {
      const { AntiDetection } = await import('../lib/anti-detection.js?cachebuster=' + Date.now());
      
      const headers = AntiDetection.createRealisticHeaders();
      
      assert.ok(headers['Sec-Ch-Ua']);
      assert.ok(headers['Sec-Ch-Ua-Mobile']);
      assert.ok(headers['Sec-Ch-Ua-Platform']);
    });

    it('should include connection headers', async () => {
      const { AntiDetection } = await import('../lib/anti-detection.js?cachebuster=' + Date.now());
      
      const headers = AntiDetection.createRealisticHeaders();
      
      assert.ok(headers['Connection']);
      assert.ok(headers['Accept-Encoding']);
    });
  });

  describe('randomDelay', () => {
    it('should delay for random time in range', async () => {
      const { AntiDetection } = await import('../lib/anti-detection.js?cachebuster=' + Date.now());
      
      const startTime = Date.now();
      await AntiDetection.randomDelay(50, 100);
      const elapsed = Date.now() - startTime;
      
      assert.ok(elapsed >= 50);
      assert.ok(elapsed <= 150);
    });

    it('should use default range 1000-3000', async () => {
      const { AntiDetection } = await import('../lib/anti-detection.js?cachebuster=' + Date.now());
      
      const startTime = Date.now();
      await AntiDetection.randomDelay();
      const elapsed = Date.now() - startTime;
      
      assert.ok(elapsed >= 1000);
      assert.ok(elapsed <= 3100);
    });

    it('should handle same min and max', async () => {
      const { AntiDetection } = await import('../lib/anti-detection.js?cachebuster=' + Date.now());
      
      const startTime = Date.now();
      await AntiDetection.randomDelay(50, 50);
      const elapsed = Date.now() - startTime;
      
      assert.ok(elapsed >= 40);
      assert.ok(elapsed <= 70);
    });

    it('should handle zero delay', async () => {
      const { AntiDetection } = await import('../lib/anti-detection.js?cachebuster=' + Date.now());
      
      const startTime = Date.now();
      await AntiDetection.randomDelay(0, 0);
      const elapsed = Date.now() - startTime;
      
      assert.ok(elapsed < 20);
    });
  });
});

describe('RateLimiter (anti-detection)', () => {
  describe('constructor', () => {
    it('should initialize with default values', async () => {
      const { RateLimiter } = await import('../lib/anti-detection.js?cachebuster=' + Date.now());
      
      const limiter = new RateLimiter();
      
      assert.strictEqual(limiter.minDelay, 1000);
      assert.strictEqual(limiter.maxDelay, 3000);
      assert.strictEqual(limiter.lastRequestTime, 0);
    });

    it('should accept custom delays', async () => {
      const { RateLimiter } = await import('../lib/anti-detection.js?cachebuster=' + Date.now());
      
      const limiter = new RateLimiter({ minDelay: 500, maxDelay: 1000 });
      
      assert.strictEqual(limiter.minDelay, 500);
      assert.strictEqual(limiter.maxDelay, 1000);
    });

    it('should handle zero delays', async () => {
      const { RateLimiter } = await import('../lib/anti-detection.js?cachebuster=' + Date.now());
      
      const limiter = new RateLimiter({ minDelay: 0, maxDelay: 0 });
      
      assert.strictEqual(limiter.minDelay, 0);
      assert.strictEqual(limiter.maxDelay, 0);
    });
  });

  describe('wait', () => {
    it('should wait for delay time', async () => {
      const { RateLimiter } = await import('../lib/anti-detection.js?cachebuster=' + Date.now());
      
      const limiter = new RateLimiter({ minDelay: 50, maxDelay: 50 });
      
      const startTime = Date.now();
      await limiter.wait();
      const elapsed = Date.now() - startTime;
      
      assert.ok(elapsed >= 50);
    });

    it('should update lastRequestTime', async () => {
      const { RateLimiter } = await import('../lib/anti-detection.js?cachebuster=' + Date.now());
      
      const limiter = new RateLimiter({ minDelay: 10, maxDelay: 10 });
      
      await limiter.wait();
      
      assert.ok(limiter.lastRequestTime > 0);
    });

    it('should not wait if enough time passed', async () => {
      const { RateLimiter } = await import('../lib/anti-detection.js?cachebuster=' + Date.now());
      
      const limiter = new RateLimiter({ minDelay: 100, maxDelay: 100 });
      limiter.lastRequestTime = Date.now() - 1000;
      
      const startTime = Date.now();
      await limiter.wait();
      const elapsed = Date.now() - startTime;
      
      assert.ok(elapsed < 100);
    });

    it('should handle multiple sequential calls', async () => {
      const { RateLimiter } = await import('../lib/anti-detection.js?cachebuster=' + Date.now());
      
      const limiter = new RateLimiter({ minDelay: 10, maxDelay: 10 });
      
      await limiter.wait();
      const time1 = limiter.lastRequestTime;
      
      await limiter.wait();
      const time2 = limiter.lastRequestTime;
      
      assert.ok(time2 >= time1);
    });
  });
});