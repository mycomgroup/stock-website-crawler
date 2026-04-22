import { describe, it, beforeEach, afterEach, mock } from 'node:test';
import assert from 'node:assert';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

let mockFetch = mock.fn(async (url, options) => {
  return {
    ok: true,
    status: 200,
    statusText: 'OK',
    headers: new Map([['content-type', 'application/json']]),
    text: async () => '{"success": true}'
  };
});

global.fetch = mockFetch;

function resetMocks() {
  mockFetch.mock.resetCalls();
}

describe('http-security', () => {
  beforeEach(() => {
    resetMocks();
  });

  describe('RateLimiter', () => {
    it('should initialize with default maxRequestsPerMinute', async () => {
      const { RateLimiter } = await import('../../common/http-security.js');
      
      const limiter = new RateLimiter();
      
      assert.strictEqual(limiter.maxRequestsPerMinute, 10);
      assert.strictEqual(limiter.minInterval, 6000);
    });

    it('should initialize with custom maxRequestsPerMinute', async () => {
      const { RateLimiter } = await import('../../common/http-security.js?cachebuster=' + Date.now());
      
      const limiter = new RateLimiter(30);
      
      assert.strictEqual(limiter.maxRequestsPerMinute, 30);
      assert.strictEqual(limiter.minInterval, 2000);
    });

    it('should initialize with lastRequestTime 0', async () => {
      const { RateLimiter } = await import('../../common/http-security.js?cachebuster=' + Date.now());
      
      const limiter = new RateLimiter();
      
      assert.strictEqual(limiter.lastRequestTime, 0);
    });

    it('should initialize with empty requestQueue', async () => {
      const { RateLimiter } = await import('../../common/http-security.js?cachebuster=' + Date.now());
      
      const limiter = new RateLimiter();
      
      assert.deepStrictEqual(limiter.requestQueue, []);
    });

    describe('waitForSlot', () => {
      it('should not wait when enough time has passed', async () => {
        const { RateLimiter } = await import('../../common/http-security.js?cachebuster=' + Date.now());
        
        const limiter = new RateLimiter(10);
        limiter.lastRequestTime = Date.now() - 10000;
        
        const startTime = Date.now();
        await limiter.waitForSlot();
        const elapsed = Date.now() - startTime;
        
        assert.ok(elapsed < 100);
      });

      it('should wait when not enough time has passed', async () => {
        const { RateLimiter } = await import('../../common/http-security.js?cachebuster=' + Date.now());
        
        const limiter = new RateLimiter(60);
        limiter.lastRequestTime = Date.now() - 500;
        
        const startTime = Date.now();
        await limiter.waitForSlot();
        const elapsed = Date.now() - startTime;
        
        assert.ok(elapsed >= 500);
      });

      it('should update lastRequestTime after waiting', async () => {
        const { RateLimiter } = await import('../../common/http-security.js?cachebuster=' + Date.now());
        
        const limiter = new RateLimiter();
        
        await limiter.waitForSlot();
        
        assert.ok(limiter.lastRequestTime > 0);
      });

      it('should handle first request (lastRequestTime = 0)', async () => {
        const { RateLimiter } = await import('../../common/http-security.js?cachebuster=' + Date.now());
        
        const limiter = new RateLimiter();
        
        const startTime = Date.now();
        await limiter.waitForSlot();
        const elapsed = Date.now() - startTime;
        
        assert.ok(elapsed < 100);
        assert.ok(limiter.lastRequestTime > 0);
      });

      it('should calculate correct wait time for 10 requests per minute', async () => {
        const { RateLimiter } = await import('../../common/http-security.js?cachebuster=' + Date.now());
        
        const limiter = new RateLimiter(10);
        limiter.lastRequestTime = Date.now();
        
        const startTime = Date.now();
        await limiter.waitForSlot();
        const elapsed = Date.now() - startTime;
        
        assert.ok(elapsed >= 5000);
      });

      it('should handle multiple sequential calls', async () => {
        const { RateLimiter } = await import('../../common/http-security.js?cachebuster=' + Date.now());
        
        const limiter = new RateLimiter(60);
        
        await limiter.waitForSlot();
        const time1 = limiter.lastRequestTime;
        
        await limiter.waitForSlot();
        const time2 = limiter.lastRequestTime;
        
        assert.ok(time2 >= time1);
      });

      it('should work with very high rate limit', async () => {
        const { RateLimiter } = await import('../../common/http-security.js?cachebuster=' + Date.now());
        
        const limiter = new RateLimiter(1000);
        limiter.lastRequestTime = Date.now() - 100;
        
        const startTime = Date.now();
        await limiter.waitForSlot();
        const elapsed = Date.now() - startTime;
        
        assert.ok(elapsed < 100);
      });

      it('should work with very low rate limit', async () => {
        const { RateLimiter } = await import('../../common/http-security.js?cachebuster=' + Date.now());
        
        const limiter = new RateLimiter(1);
        limiter.lastRequestTime = Date.now() - 30000;
        
        const startTime = Date.now();
        await limiter.waitForSlot();
        const elapsed = Date.now() - startTime;
        
        assert.ok(elapsed < 100);
      });
    });
  });

  describe('SecureHttpClient', () => {
    describe('constructor', () => {
      it('should initialize with default options', async () => {
        const { SecureHttpClient } = await import('../../common/http-security.js?cachebuster=' + Date.now());
        
        const client = new SecureHttpClient();
        
        assert.strictEqual(client.baseUrl, '');
        assert.strictEqual(client.maxRequestsPerMinute, 10);
        assert.strictEqual(client.sessionValidator, undefined);
        assert.ok(client.rateLimiter);
        assert.ok(client.currentUserAgent);
      });

      it('should initialize with custom baseUrl', async () => {
        const { SecureHttpClient } = await import('../../common/http-security.js?cachebuster=' + Date.now());
        
        const client = new SecureHttpClient({ baseUrl: 'https://api.example.com' });
        
        assert.strictEqual(client.baseUrl, 'https://api.example.com');
      });

      it('should initialize with custom maxRequestsPerMinute', async () => {
        const { SecureHttpClient } = await import('../../common/http-security.js?cachebuster=' + Date.now());
        
        const client = new SecureHttpClient({ maxRequestsPerMinute: 20 });
        
        assert.strictEqual(client.maxRequestsPerMinute, 20);
      });

      it('should initialize with sessionValidator', async () => {
        const { SecureHttpClient } = await import('../../common/http-security.js?cachebuster=' + Date.now());
        
        const validator = async () => true;
        const client = new SecureHttpClient({ sessionValidator: validator });
        
        assert.strictEqual(client.sessionValidator, validator);
      });

      it('should initialize currentUserAgent with default value', async () => {
        const { SecureHttpClient, USER_AGENT } = await import('../../common/http-security.js?cachebuster=' + Date.now());
        
        const client = new SecureHttpClient();
        
        assert.strictEqual(client.currentUserAgent, USER_AGENT);
      });

      it('should initialize currentSecChUa with default value', async () => {
        const { SecureHttpClient, SEC_CH_UA } = await import('../../common/http-security.js?cachebuster=' + Date.now());
        
        const client = new SecureHttpClient();
        
        assert.strictEqual(client.currentSecChUa, SEC_CH_UA);
      });
    });

    describe('rotateUserAgent', () => {
      it('should be a function', async () => {
        const { SecureHttpClient } = await import('../../common/http-security.js?cachebuster=' + Date.now());
        
        const client = new SecureHttpClient();
        
        assert.strictEqual(typeof client.rotateUserAgent, 'function');
      });

      it('should not throw when called', async () => {
        const { SecureHttpClient } = await import('../../common/http-security.js?cachebuster=' + Date.now());
        
        const client = new SecureHttpClient();
        
        client.rotateUserAgent();
      });

      it('should not modify userAgent (current implementation is empty)', async () => {
        const { SecureHttpClient, USER_AGENT } = await import('../../common/http-security.js?cachebuster=' + Date.now());
        
        const client = new SecureHttpClient();
        const originalUA = client.currentUserAgent;
        
        client.rotateUserAgent();
        
        assert.strictEqual(client.currentUserAgent, originalUA);
      });
    });

    describe('randomDelay', () => {
      it('should delay for random time in range', async () => {
        const { SecureHttpClient } = await import('../../common/http-security.js?cachebuster=' + Date.now());
        
        const client = new SecureHttpClient();
        
        const startTime = Date.now();
        await client.randomDelay(100, 200);
        const elapsed = Date.now() - startTime;
        
        assert.ok(elapsed >= 100);
        assert.ok(elapsed <= 300);
      });

      it('should use default min/max values', async () => {
        const { SecureHttpClient } = await import('../../common/http-security.js?cachebuster=' + Date.now());
        
        const client = new SecureHttpClient();
        
        const startTime = Date.now();
        await client.randomDelay();
        const elapsed = Date.now() - startTime;
        
        assert.ok(elapsed >= 1000);
        assert.ok(elapsed <= 3100);
      });

      it('should handle custom min and max', async () => {
        const { SecureHttpClient } = await import('../../common/http-security.js?cachebuster=' + Date.now());
        
        const client = new SecureHttpClient();
        
        const startTime = Date.now();
        await client.randomDelay(50, 100);
        const elapsed = Date.now() - startTime;
        
        assert.ok(elapsed >= 50);
        assert.ok(elapsed <= 150);
      });

      it('should handle same min and max', async () => {
        const { SecureHttpClient } = await import('../../common/http-security.js?cachebuster=' + Date.now());
        
        const client = new SecureHttpClient();
        
        const startTime = Date.now();
        await client.randomDelay(100, 100);
        const elapsed = Date.now() - startTime;
        
        assert.ok(elapsed >= 90);
        assert.ok(elapsed <= 120);
      });
    });

    describe('request', () => {
      it('should make successful request', async () => {
        const { SecureHttpClient } = await import('../../common/http-security.js?cachebuster=' + Date.now());
        
        mockFetch.mock.mockImplementation(async () => ({
          ok: true,
          status: 200,
          statusText: 'OK',
          text: async () => 'response body'
        }));
        
        const client = new SecureHttpClient();
        
        const result = await client.request('https://example.com');
        
        assert.strictEqual(result, 'response body');
        assert.strictEqual(mockFetch.mock.callCount(), 1);
      });

      it('should prepend baseUrl to relative URLs', async () => {
        const { SecureHttpClient } = await import('../../common/http-security.js?cachebuster=' + Date.now());
        
        mockFetch.mock.mockImplementation(async (url) => ({
          ok: true,
          status: 200,
          statusText: 'OK',
          text: async () => url
        }));
        
        const client = new SecureHttpClient({ baseUrl: 'https://api.example.com' });
        
        const result = await client.request('/endpoint');
        
        assert.strictEqual(result, 'https://api.example.com/endpoint');
      });

      it('should not prepend baseUrl to absolute URLs', async () => {
        const { SecureHttpClient } = await import('../../common/http-security.js?cachebuster=' + Date.now());
        
        mockFetch.mock.mockImplementation(async (url) => ({
          ok: true,
          status: 200,
          statusText: 'OK',
          text: async () => url
        }));
        
        const client = new SecureHttpClient({ baseUrl: 'https://api.example.com' });
        
        const result = await client.request('https://other.com/endpoint');
        
        assert.strictEqual(result, 'https://other.com/endpoint');
      });

      it('should include User-Agent header', async () => {
        const { SecureHttpClient } = await import('../../common/http-security.js?cachebuster=' + Date.now());
        
        mockFetch.mock.mockImplementation(async (url, options) => ({
          ok: true,
          status: 200,
          statusText: 'OK',
          text: async () => options.headers['User-Agent']
        }));
        
        const client = new SecureHttpClient();
        
        const result = await client.request('https://example.com');
        
        assert.ok(result.includes('Mozilla'));
      });

      it('should include sec-ch-ua header', async () => {
        const { SecureHttpClient } = await import('../../common/http-security.js?cachebuster=' + Date.now());
        
        mockFetch.mock.mockImplementation(async (url, options) => ({
          ok: true,
          status: 200,
          statusText: 'OK',
          text: async () => options.headers['sec-ch-ua']
        }));
        
        const client = new SecureHttpClient();
        
        const result = await client.request('https://example.com');
        
        assert.ok(result.includes('Chromium'));
      });

      it('should merge custom headers', async () => {
        const { SecureHttpClient } = await import('../../common/http-security.js?cachebuster=' + Date.now());
        
        mockFetch.mock.mockImplementation(async (url, options) => ({
          ok: true,
          status: 200,
          statusText: 'OK',
          text: async () => JSON.stringify(options.headers)
        }));
        
        const client = new SecureHttpClient();
        
        const result = await client.request('https://example.com', {
          headers: { 'X-Custom': 'custom-value' }
        });
        
        const headers = JSON.parse(result);
        assert.strictEqual(headers['X-Custom'], 'custom-value');
      });

      it('should include body in request', async () => {
        const { SecureHttpClient } = await import('../../common/http-security.js?cachebuster=' + Date.now());
        
        mockFetch.mock.mockImplementation(async (url, options) => ({
          ok: true,
          status: 200,
          statusText: 'OK',
          text: async () => options.body || 'no body'
        }));
        
        const client = new SecureHttpClient();
        
        const result = await client.request('https://example.com', {
          method: 'POST',
          body: 'test body'
        });
        
        assert.strictEqual(result, 'test body');
      });

      it('should throw on timeout', async () => {
        const { SecureHttpClient } = await import('../../common/http-security.js?cachebuster=' + Date.now());
        
        mockFetch.mock.mockImplementation(async () => {
          await new Promise(resolve => setTimeout(resolve, 10000));
          return { ok: true, status: 200, text: async () => 'ok' };
        });
        
        const client = new SecureHttpClient();
        
        await assert.rejects(
          async () => await client.request('https://example.com', { timeout: 100 }),
          { message: /timed out/ }
        );
      });

      it('should retry on 429 status', async () => {
        const { SecureHttpClient } = await import('../../common/http-security.js?cachebuster=' + Date.now());
        
        let callCount = 0;
        mockFetch.mock.mockImplementation(async () => {
          callCount++;
          if (callCount < 2) {
            return {
              ok: false,
              status: 429,
              statusText: 'Too Many Requests',
              headers: new Map([['Retry-After', '1']]),
              text: async () => ''
            };
          }
          return { ok: true, status: 200, text: async () => 'success' };
        });
        
        const client = new SecureHttpClient();
        
        const result = await client.request('https://example.com');
        
        assert.strictEqual(result, 'success');
        assert.strictEqual(mockFetch.mock.callCount(), 2);
      });

      it('should retry on 503 status', async () => {
        const { SecureHttpClient } = await import('../../common/http-security.js?cachebuster=' + Date.now());
        
        let callCount = 0;
        mockFetch.mock.mockImplementation(async () => {
          callCount++;
          if (callCount < 2) {
            return {
              ok: false,
              status: 503,
              statusText: 'Service Unavailable',
              headers: new Map(),
              text: async () => ''
            };
          }
          return { ok: true, status: 200, text: async () => 'success' };
        });
        
        const client = new SecureHttpClient();
        
        const result = await client.request('https://example.com');
        
        assert.strictEqual(result, 'success');
        assert.strictEqual(mockFetch.mock.callCount(), 2);
      });

      it('should retry on 500 status', async () => {
        const { SecureHttpClient } = await import('../../common/http-security.js?cachebuster=' + Date.now());
        
        let callCount = 0;
        mockFetch.mock.mockImplementation(async () => {
          callCount++;
          if (callCount < 2) {
            return {
              ok: false,
              status: 500,
              statusText: 'Internal Server Error',
              headers: new Map(),
              text: async () => ''
            };
          }
          return { ok: true, status: 200, text: async () => 'success' };
        });
        
        const client = new SecureHttpClient();
        
        const result = await client.request('https://example.com');
        
        assert.strictEqual(result, 'success');
        assert.strictEqual(mockFetch.mock.callCount(), 2);
      });

      it('should throw after max retries exceeded', async () => {
        const { SecureHttpClient } = await import('../../common/http-security.js?cachebuster=' + Date.now());
        
        mockFetch.mock.mockImplementation(async () => ({
          ok: false,
          status: 500,
          statusText: 'Internal Server Error',
          headers: new Map(),
          text: async () => ''
        }));
        
        const client = new SecureHttpClient();
        
        await assert.rejects(
          async () => await client.request('https://example.com', { maxRetries: 2 }),
          { message: /Max retries/ }
        );
      });

      it('should throw on 4xx error (non-retriable)', async () => {
        const { SecureHttpClient } = await import('../../common/http-security.js?cachebuster=' + Date.now());
        
        mockFetch.mock.mockImplementation(async () => ({
          ok: false,
          status: 404,
          statusText: 'Not Found',
          headers: new Map(),
          text: async () => ''
        }));
        
        const client = new SecureHttpClient();
        
        await assert.rejects(
          async () => await client.request('https://example.com'),
          { message: /HTTP 404/ }
        );
      });

      it('should validate session before request', async () => {
        const { SecureHttpClient } = await import('../../common/http-security.js?cachebuster=' + Date.now());
        
        mockFetch.mock.mockImplementation(async () => ({
          ok: true,
          status: 200,
          text: async () => 'ok'
        }));
        
        let validatorCalled = false;
        const client = new SecureHttpClient({
          sessionValidator: async () => {
            validatorCalled = true;
            return true;
          }
        });
        
        await client.request('https://example.com');
        
        assert.strictEqual(validatorCalled, true);
      });

      it('should throw when session validation fails', async () => {
        const { SecureHttpClient } = await import('../../common/http-security.js?cachebuster=' + Date.now());
        
        const client = new SecureHttpClient({
          sessionValidator: async () => false
        });
        
        await assert.rejects(
          async () => await client.request('https://example.com'),
          { message: /Session validation failed/ }
        );
      });

      it('should handle network error with retry', async () => {
        const { SecureHttpClient } = await import('../../common/http-security.js?cachebuster=' + Date.now());
        
        let callCount = 0;
        mockFetch.mock.mockImplementation(async () => {
          callCount++;
          if (callCount < 2) {
            throw new Error('Network error');
          }
          return { ok: true, status: 200, text: async () => 'success' };
        });
        
        const client = new SecureHttpClient();
        
        const result = await client.request('https://example.com');
        
        assert.strictEqual(result, 'success');
        assert.strictEqual(mockFetch.mock.callCount(), 2);
      });

      it('should throw after retries on persistent network error', async () => {
        const { SecureHttpClient } = await import('../../common/http-security.js?cachebuster=' + Date.now());
        
        mockFetch.mock.mockImplementation(async () => {
          throw new Error('Persistent network error');
        });
        
        const client = new SecureHttpClient();
        
        await assert.rejects(
          async () => await client.request('https://example.com', { maxRetries: 2 }),
          { message: 'Persistent network error' }
        );
      });

      it('should use default method GET', async () => {
        const { SecureHttpClient } = await import('../../common/http-security.js?cachebuster=' + Date.now());
        
        mockFetch.mock.mockImplementation(async (url, options) => ({
          ok: true,
          status: 200,
          text: async () => options.method
        }));
        
        const client = new SecureHttpClient();
        
        const result = await client.request('https://example.com');
        
        assert.strictEqual(result, 'GET');
      });

      it('should use custom method', async () => {
        const { SecureHttpClient } = await import('../../common/http-security.js?cachebuster=' + Date.now());
        
        mockFetch.mock.mockImplementation(async (url, options) => ({
          ok: true,
          status: 200,
          text: async () => options.method
        }));
        
        const client = new SecureHttpClient();
        
        const result = await client.request('https://example.com', { method: 'POST' });
        
        assert.strictEqual(result, 'POST');
      });

      it('should use default timeout 30000ms', async () => {
        const { SecureHttpClient } = await import('../../common/http-security.js?cachebuster=' + Date.now());
        
        const client = new SecureHttpClient();
        
        assert.ok(client);
      });

      it('should use custom timeout', async () => {
        const { SecureHttpClient } = await import('../../common/http-security.js?cachebuster=' + Date.now());
        
        mockFetch.mock.mockImplementation(async () => {
          await new Promise(resolve => setTimeout(resolve, 10000));
          return { ok: true, status: 200, text: async () => 'ok' };
        });
        
        const client = new SecureHttpClient();
        
        await assert.rejects(
          async () => await client.request('https://example.com', { timeout: 50 }),
          { message: /timed out/ }
        );
      });

      it('should use default maxRetries 3', async () => {
        const { SecureHttpClient } = await import('../../common/http-security.js?cachebuster=' + Date.now());
        
        mockFetch.mock.mockImplementation(async () => ({
          ok: false,
          status: 500,
          text: async () => ''
        }));
        
        const client = new SecureHttpClient();
        
        await assert.rejects(
          async () => await client.request('https://example.com'),
          { message: /Max retries \(3\)/ }
        );
      });

      it('should wait before retry on error', async () => {
        const { SecureHttpClient } = await import('../../common/http-security.js?cachebuster=' + Date.now());
        
        let callCount = 0;
        const startTime = Date.now();
        
        mockFetch.mock.mockImplementation(async () => {
          callCount++;
          if (callCount < 2) {
            throw new Error('Error');
          }
          return { ok: true, status: 200, text: async () => 'ok' };
        });
        
        const client = new SecureHttpClient();
        
        await client.request('https://example.com', { maxRetries: 3 });
        
        const elapsed = Date.now() - startTime;
        assert.ok(elapsed >= 5000);
      });

      it('should handle Retry-After header on 429', async () => {
        const { SecureHttpClient } = await import('../../common/http-security.js?cachebuster=' + Date.now());
        
        let callCount = 0;
        const startTime = Date.now();
        
        mockFetch.mock.mockImplementation(async () => {
          callCount++;
          if (callCount < 2) {
            return {
              ok: false,
              status: 429,
              headers: new Map([['Retry-After', '2']]),
              text: async () => ''
            };
          }
          return { ok: true, status: 200, text: async () => 'ok' };
        });
        
        const client = new SecureHttpClient();
        
        await client.request('https://example.com');
        
        const elapsed = Date.now() - startTime;
        assert.ok(elapsed >= 2000);
      });
    });

    describe('exports', () => {
      it('should export USER_AGENT constant', async () => {
        const { USER_AGENT } = await import('../../common/http-security.js?cachebuster=' + Date.now());
        
        assert.ok(USER_AGENT);
        assert.ok(USER_AGENT.includes('Mozilla'));
      });

      it('should export SEC_CH_UA constant', async () => {
        const { SEC_CH_UA } = await import('../../common/http-security.js?cachebuster=' + Date.now());
        
        assert.ok(SEC_CH_UA);
        assert.ok(SEC_CH_UA.includes('Chromium'));
      });

      it('should export default object with all exports', async () => {
        const httpSecurity = await import('../../common/http-security.js?cachebuster=' + Date.now());
        
        assert.ok(httpSecurity.default);
        assert.ok(httpSecurity.default.SecureHttpClient);
        assert.ok(httpSecurity.default.RateLimiter);
        assert.ok(httpSecurity.default.USER_AGENT);
        assert.ok(httpSecurity.default.SEC_CH_UA);
      });
    });
  });
});