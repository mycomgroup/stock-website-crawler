import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';

const mockFetch = vi.spyOn(global, 'fetch', 'get');

let SecureHttpClient, RateLimiter, USER_AGENT, SEC_CH_UA;

beforeAll(async () => {
  const module = await import('../../common/http-security.js');
  SecureHttpClient = module.SecureHttpClient;
  RateLimiter = module.RateLimiter;
  USER_AGENT = module.USER_AGENT;
  SEC_CH_UA = module.SEC_CH_UA;
});

describe('Constants', () => {
  describe('USER_AGENT', () => {
    it('is defined as a string', () => {
      expect(USER_AGENT).toBeDefined();
      expect(typeof USER_AGENT).toBe('string');
    });

    it('contains Chrome identifier', () => {
      expect(USER_AGENT).toContain('Chrome');
    });

    it('contains Mozilla identifier', () => {
      expect(USER_AGENT).toContain('Mozilla');
    });
  });

  describe('SEC_CH_UA', () => {
    it('is defined as a string', () => {
      expect(SEC_CH_UA).toBeDefined();
      expect(typeof SEC_CH_UA).toBe('string');
    });

    it('contains Chromium identifier', () => {
      expect(SEC_CH_UA).toContain('Chromium');
    });
  });
});

describe('RateLimiter', () => {
  describe('constructor', () => {
    it('initializes with default maxRequestsPerMinute', () => {
      const limiter = new RateLimiter();

      expect(limiter.maxRequestsPerMinute).toBe(10);
      expect(limiter.minInterval).toBe(6000);
      expect(limiter.lastRequestTime).toBe(0);
    });

    it('accepts custom maxRequestsPerMinute', () => {
      const limiter = new RateLimiter(30);

      expect(limiter.maxRequestsPerMinute).toBe(30);
      expect(limiter.minInterval).toBe(2000);
    });

    it('handles maxRequestsPerMinute = 1', () => {
      const limiter = new RateLimiter(1);

      expect(limiter.minInterval).toBe(60000);
    });

    it('handles maxRequestsPerMinute = 60', () => {
      const limiter = new RateLimiter(60);

      expect(limiter.minInterval).toBe(1000);
    });
  });

  describe('waitForSlot', () => {
    it('updates lastRequestTime', async () => {
      const limiter = new RateLimiter(60);
      
      await limiter.waitForSlot();

      expect(limiter.lastRequestTime).toBeGreaterThan(0);
    });

    it('allows immediate request after wait period', async () => {
      const limiter = new RateLimiter(60);

      await limiter.waitForSlot();
      const waitTime = limiter.minInterval + 100;

      await new Promise(r => setTimeout(r, waitTime));

      const start = Date.now();
      await limiter.waitForSlot();
      const elapsed = Date.now() - start;

      expect(elapsed).toBeLessThan(100);
    });
  });
});

describe('SecureHttpClient', () => {
  let client;

  beforeEach(() => {
    vi.clearAllMocks();
    client = new SecureHttpClient();
  });

  afterEach(() => {
    mockFetch.mockReset();
  });

  describe('constructor', () => {
    it('initializes with default options', () => {
      expect(client.baseUrl).toBe('');
      expect(client.maxRequestsPerMinute).toBe(10);
      expect(client.currentUserAgent).toBe(USER_AGENT);
      expect(client.currentSecChUa).toBe(SEC_CH_UA);
    });

    it('accepts custom baseUrl', () => {
      const customClient = new SecureHttpClient({ baseUrl: 'https://api.test.com' });

      expect(customClient.baseUrl).toBe('https://api.test.com');
    });

    it('accepts custom maxRequestsPerMinute', () => {
      const customClient = new SecureHttpClient({ maxRequestsPerMinute: 30 });

      expect(customClient.maxRequestsPerMinute).toBe(30);
    });

    it('accepts sessionValidator', () => {
      const validator = async () => true;
      const customClient = new SecureHttpClient({ sessionValidator: validator });

      expect(customClient.sessionValidator).toBe(validator);
    });
  });

  describe('rotateUserAgent', () => {
    it('exists as a method', () => {
      expect(client.rotateUserAgent).toBeDefined();
      expect(typeof client.rotateUserAgent).toBe('function');
    });

    it('can be called without error', () => {
      client.rotateUserAgent();
    });
  });

  describe('randomDelay', () => {
    it('delays execution with default range', async () => {
      const start = Date.now();
      await client.randomDelay();
      const elapsed = Date.now() - start;

      expect(elapsed).toBeGreaterThanOrEqual(900);
    });

    it('delays execution with custom range', async () => {
      const start = Date.now();
      await client.randomDelay(100, 200);
      const elapsed = Date.now() - start;

      expect(elapsed).toBeGreaterThanOrEqual(90);
    });
  });

  describe('request', () => {
    it('makes GET request with default options', async () => {
      mockFetch.mockResolvedValue({
        ok: true,
        status: 200,
        text: async () => 'response text'
      });

      const result = await client.request('https://test.com/api');

      expect(mockFetch).toHaveBeenCalledWith(
        'https://test.com/api',
        expect.objectContaining({
          method: 'GET',
        })
      );
      expect(result).toBe('response text');
    });

    it('makes POST request', async () => {
      mockFetch.mockResolvedValue({
        ok: true,
        status: 200,
        text: async () => 'ok'
      });

      await client.request('https://test.com/api', { method: 'POST', body: 'data' });

      expect(mockFetch).toHaveBeenCalledWith(
        expect.any(String),
        expect.objectContaining({
          method: 'POST',
          body: 'data',
        })
      );
    });

    it('prepends baseUrl to relative URL', async () => {
      const urlClient = new SecureHttpClient({ baseUrl: 'https://api.test.com' });
      mockFetch.mockResolvedValue({
        ok: true,
        status: 200,
        text: async () => 'ok'
      });

      await urlClient.request('/endpoint');

      expect(mockFetch).toHaveBeenCalledWith(
        'https://api.test.com/endpoint',
        expect.any(Object)
      );
    });

    it('uses full URL without baseUrl', async () => {
      const urlClient = new SecureHttpClient({ baseUrl: 'https://api.test.com' });
      mockFetch.mockResolvedValue({
        ok: true,
        status: 200,
        text: async () => 'ok'
      });

      await urlClient.request('https://other.com/api');

      expect(mockFetch).toHaveBeenCalledWith(
        'https://other.com/api',
        expect.any(Object)
      );
    });

    it('includes default headers', async () => {
      mockFetch.mockResolvedValue({
        ok: true,
        status: 200,
        text: async () => 'ok'
      });

      await client.request('https://test.com/api');

      expect(mockFetch).toHaveBeenCalledWith(
        expect.any(String),
        expect.objectContaining({
          headers: expect.objectContaining({
            'User-Agent': USER_AGENT,
            'sec-ch-ua': SEC_CH_UA,
          }),
        })
      );
    });

    it('includes custom headers', async () => {
      mockFetch.mockResolvedValue({
        ok: true,
        status: 200,
        text: async () => 'ok'
      });

      await client.request('https://test.com/api', {
        headers: { 'X-Custom': 'value' }
      });

      expect(mockFetch).toHaveBeenCalledWith(
        expect.any(String),
        expect.objectContaining({
          headers: expect.objectContaining({
            'X-Custom': 'value',
          }),
        })
      );
    });

    it('returns response text', async () => {
      mockFetch.mockResolvedValue({
        ok: true,
        status: 200,
        text: async () => 'response body'
      });

      const result = await client.request('https://test.com/api');

      expect(result).toBe('response body');
    });

    it('throws on non-ok response', async () => {
      mockFetch.mockResolvedValue({
        ok: false,
        status: 404,
        statusText: 'Not Found'
      });

      await expect(client.request('https://test.com/api')).rejects.toThrow('HTTP 404: Not Found');
    });

    it('handles 429 rate limiting with retry', async () => {
      mockFetch
        .mockResolvedValueOnce({
          ok: false,
          status: 429,
          headers: new Map([['Retry-After', '1']])
        })
        .mockResolvedValueOnce({
          ok: true,
          status: 200,
          text: async () => 'ok'
        });

      const consoleSpy = vi.spyOn(console, 'log').mockImplementation(() => {});

      const result = await client.request('https://test.com/api');

      expect(result).toBe('ok');
      expect(mockFetch).toHaveBeenCalledTimes(2);

      consoleSpy.mockRestore();
    });

    it('handles 503 service unavailable with retry', async () => {
      mockFetch
        .mockResolvedValueOnce({
          ok: false,
          status: 503
        })
        .mockResolvedValueOnce({
          ok: true,
          status: 200,
          text: async () => 'ok'
        });

      const consoleSpy = vi.spyOn(console, 'log').mockImplementation(() => {});

      const result = await client.request('https://test.com/api');

      expect(result).toBe('ok');
      expect(mockFetch).toHaveBeenCalledTimes(2);

      consoleSpy.mockRestore();
    });

    it('handles 500 server error with retry', async () => {
      mockFetch
        .mockResolvedValueOnce({
          ok: false,
          status: 500,
          statusText: 'Internal Server Error'
        })
        .mockResolvedValueOnce({
          ok: true,
          status: 200,
          text: async () => 'ok'
        });

      const consoleSpy = vi.spyOn(console, 'log').mockImplementation(() => {});

      const result = await client.request('https://test.com/api');

      expect(result).toBe('ok');

      consoleSpy.mockRestore();
    });

    it('retries on network error', async () => {
      mockFetch
        .mockRejectedValueOnce(new Error('Network error'))
        .mockResolvedValueOnce({
          ok: true,
          status: 200,
          text: async () => 'ok'
        });

      const consoleSpy = vi.spyOn(console, 'log').mockImplementation(() => {});

      const result = await client.request('https://test.com/api');

      expect(result).toBe('ok');
      expect(mockFetch).toHaveBeenCalledTimes(2);

      consoleSpy.mockRestore();
    });

    it('throws after max retries', async () => {
      mockFetch.mockResolvedValue({
        ok: false,
        status: 500,
        statusText: 'Error'
      });

      await expect(client.request('https://test.com/api')).rejects.toThrow();

      expect(mockFetch).toHaveBeenCalledTimes(3);
    });

    it('throws on timeout', async () => {
      mockFetch.mockImplementation(() => new Promise((resolve) => {
        setTimeout(() => resolve({
          ok: true,
          status: 200,
          text: async () => 'ok'
        }), 5000);
      }));

      await expect(
        client.request('https://test.com/api', { timeout: 100 })
      ).rejects.toThrow('Request timed out');
    });

    it('uses custom maxRetries', async () => {
      mockFetch.mockRejectedValue(new Error('Error'));

      await expect(
        client.request('https://test.com/api', { maxRetries: 1 })
      ).rejects.toThrow();

      expect(mockFetch).toHaveBeenCalledTimes(1);
    });

    it('calls sessionValidator before request', async () => {
      const validator = vi.fn().mockResolvedValue(true);
      const validatorClient = new SecureHttpClient({ sessionValidator: validator });
      mockFetch.mockResolvedValue({
        ok: true,
        status: 200,
        text: async () => 'ok'
      });

      await validatorClient.request('https://test.com/api');

      expect(validator).toHaveBeenCalled();
    });

    it('throws when sessionValidator returns false', async () => {
      const validator = vi.fn().mockResolvedValue(false);
      const validatorClient = new SecureHttpClient({ sessionValidator: validator });

      await expect(
        validatorClient.request('https://test.com/api')
      ).rejects.toThrow('Session validation failed');
    });
  });
});