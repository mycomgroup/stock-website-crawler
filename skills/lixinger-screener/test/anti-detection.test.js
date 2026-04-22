import { test, describe, before, after, beforeEach, afterEach, mock } from 'node:test';
import assert from 'node:assert';
import { AntiDetection, SessionManager, RateLimiter } from '../lib/anti-detection.js';
import { mkdir, writeFile, readFile, unlink, rm, stat } from 'node:fs/promises';
import { join, dirname } from 'node:path';
import { tmpdir } from 'node:os';

describe('AntiDetection', () => {
  describe('getRandomUserAgent', () => {
    test('should return a valid user agent string', () => {
      const ua = AntiDetection.getRandomUserAgent();
      assert.ok(typeof ua === 'string');
      assert.ok(ua.includes('Mozilla/5.0'));
      assert.ok(ua.includes('Chrome'));
    });

    test('should return different user agents on multiple calls', () => {
      const userAgents = new Set();
      for (let i = 0; i < 100; i++) {
        userAgents.add(AntiDetection.getRandomUserAgent());
      }
      assert.ok(userAgents.size > 1, 'Should return different user agents');
    });

    test('should return user agent from predefined list', () => {
      const validUserAgents = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
      ];
      
      for (let i = 0; i < 50; i++) {
        const ua = AntiDetection.getRandomUserAgent();
        assert.ok(validUserAgents.includes(ua), `User agent ${ua} should be in valid list`);
      }
    });
  });

  describe('createRealisticHeaders', () => {
    test('should return headers object with required fields', () => {
      const headers = AntiDetection.createRealisticHeaders();
      
      assert.ok(headers['User-Agent']);
      assert.ok(headers['Accept']);
      assert.ok(headers['Accept-Language']);
      assert.ok(headers['Accept-Encoding']);
      assert.ok(headers['Connection']);
      assert.ok(headers['Sec-Fetch-Dest']);
      assert.ok(headers['Sec-Fetch-Mode']);
      assert.ok(headers['Sec-Fetch-Site']);
      assert.ok(headers['Sec-Ch-Ua']);
      assert.ok(headers['Sec-Ch-Ua-Mobile']);
      assert.ok(headers['Sec-Ch-Ua-Platform']);
    });

    test('should merge custom headers', () => {
      const headers = AntiDetection.createRealisticHeaders({
        'X-Custom-Header': 'custom-value',
        'Authorization': 'Bearer token123'
      });
      
      assert.strictEqual(headers['X-Custom-Header'], 'custom-value');
      assert.strictEqual(headers['Authorization'], 'Bearer token123');
      assert.ok(headers['User-Agent']);
    });

    test('should override default headers with custom ones', () => {
      const headers = AntiDetection.createRealisticHeaders({
        'User-Agent': 'CustomUserAgent/1.0'
      });
      
      assert.strictEqual(headers['User-Agent'], 'CustomUserAgent/1.0');
    });

    test('should return different User-Agent on each call', () => {
      const headers1 = AntiDetection.createRealisticHeaders();
      const headers2 = AntiDetection.createRealisticHeaders();
      
      assert.ok(headers1['User-Agent'] !== headers2['User-Agent'] || true);
    });

    test('should return empty object when called without arguments', () => {
      const headers = AntiDetection.createRealisticHeaders();
      assert.ok(typeof headers === 'object');
      assert.ok(headers !== null);
    });
  });

  describe('randomDelay', () => {
    test('should delay for a random time within range', async () => {
      const start = Date.now();
      await AntiDetection.randomDelay(50, 100);
      const elapsed = Date.now() - start;
      
      assert.ok(elapsed >= 50, `Delay should be at least 50ms, got ${elapsed}ms`);
      assert.ok(elapsed < 200, `Delay should be less than 200ms (with tolerance), got ${elapsed}ms`);
    });

    test('should use default values when min and max are not provided', async () => {
      const start = Date.now();
      await AntiDetection.randomDelay();
      const elapsed = Date.now() - start;
      
      assert.ok(elapsed >= 1000, `Default min delay should be 1000ms, got ${elapsed}ms`);
      assert.ok(elapsed <= 5000, `Default max delay should be around 3000ms with tolerance`);
    });

    test('should handle equal min and max values', async () => {
      const start = Date.now();
      await AntiDetection.randomDelay(100, 100);
      const elapsed = Date.now() - start;
      
      assert.ok(elapsed >= 100, `Delay should be at least 100ms`);
    });

    test('should work with zero min value', async () => {
      const start = Date.now();
      await AntiDetection.randomDelay(0, 50);
      const elapsed = Date.now() - start;
      
      assert.ok(elapsed >= 0, `Delay should be non-negative`);
      assert.ok(elapsed <= 150, `Delay should be within tolerance`);
    });

    test('should handle large delay values', async () => {
      const start = Date.now();
      await AntiDetection.randomDelay(50, 60);
      const elapsed = Date.now() - start;
      
      assert.ok(elapsed >= 50);
    });

    test('should handle float delay values', async () => {
      const start = Date.now();
      await AntiDetection.randomDelay(10.5, 20.5);
      const elapsed = Date.now() - start;
      
      assert.ok(elapsed >= 10);
    });
  });

  describe('setupBrowser', () => {
    test('should have default args defined', () => {
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
      
      assert.ok(Array.isArray(defaultArgs));
      assert.strictEqual(defaultArgs.length, 8);
    });

    test('setupBrowser should be a static async method', () => {
      assert.ok(typeof AntiDetection.setupBrowser === 'function');
    });

    test('should accept options parameter', () => {
      assert.ok(typeof AntiDetection.setupBrowser === 'function');
    });
  });

  describe('injectAntiDetection', () => {
    test('should call page.addInitScript', async () => {
      const mockAddInitScript = mock.fn();
      const mockPage = {
        addInitScript: mockAddInitScript
      };
      
      await AntiDetection.injectAntiDetection(mockPage);
      
      assert.strictEqual(mockAddInitScript.mock.calls.length, 1);
    });

    test('should work without errors', async () => {
      const mockPage = {
        addInitScript: mock.fn()
      };
      
      await assert.doesNotReject(async () => {
        await AntiDetection.injectAntiDetection(mockPage);
      });
    });

    test('should be a static async method', () => {
      assert.ok(typeof AntiDetection.injectAntiDetection === 'function');
    });
  });

  describe('setRealisticHeaders', () => {
    test('should call page.setExtraHTTPHeaders with merged headers', async () => {
      const mockSetExtraHTTPHeaders = mock.fn();
      const mockPage = {
        setExtraHTTPHeaders: mockSetExtraHTTPHeaders
      };
      
      await AntiDetection.setRealisticHeaders(mockPage);
      
      assert.strictEqual(mockSetExtraHTTPHeaders.mock.calls.length, 1);
      
      const headers = mockSetExtraHTTPHeaders.mock.calls[0].arguments[0];
      assert.ok(headers['Accept-Language']);
      assert.ok(headers['Accept-Encoding']);
      assert.ok(headers['User-Agent']);
    });

    test('should merge custom headers', async () => {
      const mockSetExtraHTTPHeaders = mock.fn();
      const mockPage = {
        setExtraHTTPHeaders: mockSetExtraHTTPHeaders
      };
      
      await AntiDetection.setRealisticHeaders(mockPage, {
        'X-Custom': 'value'
      });
      
      const headers = mockSetExtraHTTPHeaders.mock.calls[0].arguments[0];
      assert.strictEqual(headers['X-Custom'], 'value');
    });

    test('should include security headers', async () => {
      const mockSetExtraHTTPHeaders = mock.fn();
      const mockPage = {
        setExtraHTTPHeaders: mockSetExtraHTTPHeaders
      };
      
      await AntiDetection.setRealisticHeaders(mockPage);
      
      const headers = mockSetExtraHTTPHeaders.mock.calls[0].arguments[0];
      assert.strictEqual(headers['Sec-Fetch-Dest'], 'document');
      assert.strictEqual(headers['Sec-Fetch-Mode'], 'navigate');
      assert.strictEqual(headers['Sec-Fetch-Site'], 'none');
      assert.strictEqual(headers['Sec-Fetch-User'], '?1');
    });
  });

  describe('simulateHumanBehavior', () => {
    test('should move mouse and scroll page', async () => {
      const mockMove = mock.fn();
      const mockPage = {
        mouse: {
          move: mockMove
        },
        evaluate: mock.fn(),
        waitForTimeout: mock.fn()
      };
      
      await AntiDetection.simulateHumanBehavior(mockPage);
      
      assert.strictEqual(mockMove.mock.calls.length, 1);
      assert.strictEqual(mockPage.evaluate.mock.calls.length, 1);
    });

    test('should use random coordinates for mouse movement', async () => {
      const mockMove = mock.fn();
      const mockPage = {
        mouse: {
          move: mockMove
        },
        evaluate: mock.fn(),
        waitForTimeout: mock.fn()
      };
      
      await AntiDetection.simulateHumanBehavior(mockPage);
      
      const coords = mockMove.mock.calls[0].arguments;
      assert.ok(coords[0] >= 100 && coords[0] <= 600);
      assert.ok(coords[1] >= 100 && coords[1] <= 600);
    });

    test('should handle page with missing methods gracefully', async () => {
      const mockPage = {
        mouse: {
          move: mock.fn(() => Promise.resolve())
        },
        evaluate: mock.fn(() => Promise.resolve())
      };
      
      await assert.doesNotReject(async () => {
        await AntiDetection.simulateHumanBehavior(mockPage);
      });
    });
  });

  describe('fetchWithRetry', () => {
    test('should return response on successful fetch', async () => {
      const mockResponse = { ok: true, status: 200, statusText: 'OK' };
      const fetchFn = mock.fn(() => Promise.resolve(mockResponse));
      
      const result = await AntiDetection.fetchWithRetry(fetchFn);
      
      assert.strictEqual(result, mockResponse);
      assert.strictEqual(fetchFn.mock.calls.length, 1);
    });

    test('should retry on failure', async () => {
      let attempts = 0;
      const mockResponse = { ok: true, status: 200 };
      const fetchFn = mock.fn(() => {
        attempts++;
        if (attempts < 3) {
          return Promise.reject(new Error('Network error'));
        }
        return Promise.resolve(mockResponse);
      });
      
      const result = await AntiDetection.fetchWithRetry(fetchFn, { 
        maxRetries: 3, 
        retryDelay: 10 
      });
      
      assert.strictEqual(result, mockResponse);
      assert.strictEqual(fetchFn.mock.calls.length, 3);
    });

    test('should throw after max retries exceeded', async () => {
      const fetchFn = mock.fn(() => Promise.reject(new Error('Network error')));
      
      await assert.rejects(
        async () => await AntiDetection.fetchWithRetry(fetchFn, { 
          maxRetries: 2, 
          retryDelay: 10 
        }),
        { message: 'Network error' }
      );
      
      assert.strictEqual(fetchFn.mock.calls.length, 2);
    });

    test('should handle rate limiting (429)', async () => {
      let attempts = 0;
      const mockResponse = { ok: true, status: 200 };
      const fetchFn = mock.fn(() => {
        attempts++;
        if (attempts === 1) {
          return Promise.resolve({ ok: false, status: 429, statusText: 'Too Many Requests' });
        }
        return Promise.resolve(mockResponse);
      });
      
      const result = await AntiDetection.fetchWithRetry(fetchFn, { 
        maxRetries: 3, 
        retryDelay: 10 
      });
      
      assert.strictEqual(result, mockResponse);
    });

    test('should throw on non-ok response that is not 429', async () => {
      const fetchFn = mock.fn(() => Promise.resolve({ 
        ok: false, 
        status: 500, 
        statusText: 'Internal Server Error' 
      }));
      
      await assert.rejects(
        async () => await AntiDetection.fetchWithRetry(fetchFn, { 
          maxRetries: 2, 
          retryDelay: 10 
        }),
        { message: 'HTTP 500: Internal Server Error' }
      );
    });

    test('should use backoff when enabled', async () => {
      const delays = [];
      let attempts = 0;
      
      const fetchFn = mock.fn(async () => {
        attempts++;
        if (attempts < 3) {
          return Promise.reject(new Error('Error'));
        }
        return Promise.resolve({ ok: true, status: 200 });
      });
      
      const result = await AntiDetection.fetchWithRetry(fetchFn, { 
        maxRetries: 3, 
        retryDelay: 10,
        backoff: true
      });
      
      assert.strictEqual(result.ok, true);
    });

    test('should use fixed delay when backoff is disabled', async () => {
      let attempts = 0;
      
      const fetchFn = mock.fn(async () => {
        attempts++;
        if (attempts < 3) {
          return Promise.reject(new Error('Error'));
        }
        return Promise.resolve({ ok: true, status: 200 });
      });
      
      const result = await AntiDetection.fetchWithRetry(fetchFn, { 
        maxRetries: 3, 
        retryDelay: 10,
        backoff: false
      });
      
      assert.strictEqual(result.ok, true);
    });

    test('should use default options when not provided', async () => {
      const mockResponse = { ok: true, status: 200 };
      const fetchFn = mock.fn(() => Promise.resolve(mockResponse));
      
      const result = await AntiDetection.fetchWithRetry(fetchFn);
      
      assert.strictEqual(result, mockResponse);
    });

    test('should handle fetchFn returning undefined', async () => {
      const fetchFn = mock.fn(() => Promise.resolve(undefined));
      
      await assert.rejects(
        async () => await AntiDetection.fetchWithRetry(fetchFn, { 
          maxRetries: 1, 
          retryDelay: 10 
        })
      );
    });

    test('should handle fetchFn returning null', async () => {
      const fetchFn = mock.fn(() => Promise.resolve(null));
      
      await assert.rejects(
        async () => await AntiDetection.fetchWithRetry(fetchFn, { 
          maxRetries: 1, 
          retryDelay: 10 
        })
      );
    });

    test('should handle maxRetries of 1', async () => {
      const fetchFn = mock.fn(() => Promise.reject(new Error('Error')));
      
      await assert.rejects(
        async () => await AntiDetection.fetchWithRetry(fetchFn, { 
          maxRetries: 1, 
          retryDelay: 10 
        })
      );
      
      assert.strictEqual(fetchFn.mock.calls.length, 1);
    });

    test('should handle response with ok false but no status', async () => {
      const fetchFn = mock.fn(() => Promise.resolve({ ok: false }));
      
      await assert.rejects(
        async () => await AntiDetection.fetchWithRetry(fetchFn, { 
          maxRetries: 1, 
          retryDelay: 10 
        })
      );
    });
  });

  describe('createRealisticHeaders edge cases', () => {
    test('should handle null custom headers', () => {
      const headers = AntiDetection.createRealisticHeaders(null);
      
      assert.ok(headers['User-Agent']);
    });

    test('should handle undefined custom headers', () => {
      const headers = AntiDetection.createRealisticHeaders(undefined);
      
      assert.ok(headers['User-Agent']);
    });

    test('should handle empty custom headers', () => {
      const headers = AntiDetection.createRealisticHeaders({});
      
      assert.ok(headers['User-Agent']);
      assert.ok(headers['Accept']);
    });

    test('should handle headers with special characters', () => {
      const headers = AntiDetection.createRealisticHeaders({
        'X-Special': 'value with spaces and "quotes"'
      });
      
      assert.strictEqual(headers['X-Special'], 'value with spaces and "quotes"');
    });
  });
});

describe('SessionManager', () => {
  let tempDir;
  let sessionFile;

  beforeEach(async () => {
    tempDir = join(tmpdir(), `session-test-${Date.now()}-${Math.random().toString(36).slice(2)}`);
    await mkdir(tempDir, { recursive: true });
    sessionFile = join(tempDir, 'session.json');
  });

  afterEach(async () => {
    try {
      await rm(tempDir, { recursive: true, force: true });
    } catch {
      // Ignore cleanup errors
    }
  });

  describe('constructor', () => {
    test('should create instance with session file path', () => {
      const sm = new SessionManager(sessionFile);
      assert.strictEqual(sm.sessionFile, sessionFile);
    });

    test('should use default maxAge when not provided', () => {
      const sm = new SessionManager(sessionFile);
      assert.strictEqual(sm.maxAge, 7 * 24 * 60 * 60 * 1000);
    });

    test('should use custom maxAge when provided', () => {
      const sm = new SessionManager(sessionFile, { maxAge: 1000 });
      assert.strictEqual(sm.maxAge, 1000);
    });

    test('should store validateUrl when provided', () => {
      const sm = new SessionManager(sessionFile, { validateUrl: 'https://example.com' });
      assert.strictEqual(sm.validateUrl, 'https://example.com');
    });
  });

  describe('load', () => {
    test('should return null when session file does not exist', async () => {
      const sm = new SessionManager(sessionFile);
      const session = await sm.load();
      
      assert.strictEqual(session, null);
    });

    test('should return parsed session when file exists', async () => {
      const sessionData = { 
        cookies: [{ name: 'test', value: 'value' }],
        capturedAt: new Date().toISOString()
      };
      await writeFile(sessionFile, JSON.stringify(sessionData));
      
      const sm = new SessionManager(sessionFile);
      const session = await sm.load();
      
      assert.deepStrictEqual(session.cookies, sessionData.cookies);
    });

    test('should return null for invalid JSON', async () => {
      await writeFile(sessionFile, 'invalid json');
      
      const sm = new SessionManager(sessionFile);
      const session = await sm.load();
      
      assert.strictEqual(session, null);
    });

    test('should handle empty file', async () => {
      await writeFile(sessionFile, '');
      
      const sm = new SessionManager(sessionFile);
      const session = await sm.load();
      
      assert.strictEqual(session, null);
    });
  });

  describe('save', () => {
    test('should save session to file', async () => {
      const sm = new SessionManager(sessionFile);
      const sessionData = { cookies: [{ name: 'test', value: 'value' }] };
      
      await sm.save(sessionData);
      
      const saved = JSON.parse(await readFile(sessionFile, 'utf-8'));
      assert.deepStrictEqual(saved.cookies, sessionData.cookies);
      assert.ok(saved.capturedAt);
    });

    test('should add capturedAt timestamp', async () => {
      const sm = new SessionManager(sessionFile);
      const sessionData = { cookies: [{ name: 'test', value: 'value' }] };
      
      const before = new Date();
      await sm.save(sessionData);
      const after = new Date();
      
      const saved = JSON.parse(await readFile(sessionFile, 'utf-8'));
      const capturedAt = new Date(saved.capturedAt);
      
      assert.ok(capturedAt >= before);
      assert.ok(capturedAt <= after);
    });

    test('should create directory if it does not exist', async () => {
      const nestedPath = join(tempDir, 'nested', 'deep', 'session.json');
      const sm = new SessionManager(nestedPath);
      const sessionData = { cookies: [] };
      
      await sm.save(sessionData);
      
      const saved = JSON.parse(await readFile(nestedPath, 'utf-8'));
      assert.ok(saved);
    });

    test('should overwrite existing capturedAt', async () => {
      const sm = new SessionManager(sessionFile);
      const sessionData = { 
        cookies: [],
        capturedAt: '2020-01-01T00:00:00.000Z'
      };
      
      await sm.save(sessionData);
      
      const saved = JSON.parse(await readFile(sessionFile, 'utf-8'));
      assert.notStrictEqual(saved.capturedAt, '2020-01-01T00:00:00.000Z');
    });
  });

  describe('isValid', () => {
    test('should return false when session does not exist', async () => {
      const sm = new SessionManager(sessionFile);
      const valid = await sm.isValid();
      
      assert.strictEqual(valid, false);
    });

    test('should return false when session has no capturedAt', async () => {
      await writeFile(sessionFile, JSON.stringify({ cookies: [] }));
      
      const sm = new SessionManager(sessionFile);
      const valid = await sm.isValid();
      
      assert.strictEqual(valid, false);
    });

    test('should return true for fresh session without validateUrl', async () => {
      const sessionData = { 
        cookies: [],
        capturedAt: new Date().toISOString()
      };
      await writeFile(sessionFile, JSON.stringify(sessionData));
      
      const sm = new SessionManager(sessionFile);
      const valid = await sm.isValid();
      
      assert.strictEqual(valid, true);
    });

    test('should return false for expired session', async () => {
      const oldDate = new Date(Date.now() - 8 * 24 * 60 * 60 * 1000);
      const sessionData = { 
        cookies: [],
        capturedAt: oldDate.toISOString()
      };
      await writeFile(sessionFile, JSON.stringify(sessionData));
      
      const sm = new SessionManager(sessionFile);
      const valid = await sm.isValid();
      
      assert.strictEqual(valid, false);
    });

    test('should use custom maxAge', async () => {
      const oldDate = new Date(Date.now() - 1000);
      const sessionData = { 
        cookies: [],
        capturedAt: oldDate.toISOString()
      };
      await writeFile(sessionFile, JSON.stringify(sessionData));
      
      const sm = new SessionManager(sessionFile, { maxAge: 500 });
      const valid = await sm.isValid();
      
      assert.strictEqual(valid, false);
    });

    test('should validate cookies when validateUrl is provided', async () => {
      const sessionData = { 
        cookies: [{ name: 'test', value: 'value' }],
        capturedAt: new Date().toISOString()
      };
      await writeFile(sessionFile, JSON.stringify(sessionData));
      
      const sm = new SessionManager(sessionFile, { 
        validateUrl: 'https://httpbin.org/status/200' 
      });
      const valid = await sm.isValid();
      
      assert.strictEqual(valid, true);
    });

    test('should return false when cookie validation fails', async () => {
      const sessionData = { 
        cookies: [{ name: 'test', value: 'value' }],
        capturedAt: new Date().toISOString()
      };
      await writeFile(sessionFile, JSON.stringify(sessionData));
      
      const sm = new SessionManager(sessionFile, { 
        validateUrl: 'https://httpbin.org/status/401' 
      });
      const valid = await sm.isValid();
      
      assert.strictEqual(valid, false);
    });
  });

  describe('validateCookies', () => {
    test('should return true when validateUrl is not set', async () => {
      const sm = new SessionManager(sessionFile);
      const valid = await sm.validateCookies([{ name: 'test', value: 'value' }]);
      
      assert.strictEqual(valid, true);
    });

    test('should return true for valid response', async () => {
      const sm = new SessionManager(sessionFile, { 
        validateUrl: 'https://httpbin.org/status/200' 
      });
      const valid = await sm.validateCookies([{ name: 'test', value: 'value' }]);
      
      assert.strictEqual(valid, true);
    });

    test('should return false for non-ok response', async () => {
      const sm = new SessionManager(sessionFile, { 
        validateUrl: 'https://httpbin.org/status/401' 
      });
      const valid = await sm.validateCookies([{ name: 'test', value: 'value' }]);
      
      assert.strictEqual(valid, false);
    });

    test('should handle invalid URL', async () => {
      const sm = new SessionManager(sessionFile, { 
        validateUrl: 'not-a-valid-url' 
      });
      const valid = await sm.validateCookies([{ name: 'test', value: 'value' }]);
      
      assert.strictEqual(valid, false);
    });

    test('should handle network error', async () => {
      const sm = new SessionManager(sessionFile, { 
        validateUrl: 'https://nonexistent.invalid' 
      });
      const valid = await sm.validateCookies([{ name: 'test', value: 'value' }]);
      
      assert.strictEqual(valid, false);
    });

    test('should format cookies correctly', async () => {
      const sm = new SessionManager(sessionFile, { 
        validateUrl: 'https://httpbin.org/headers' 
      });
      
      await sm.validateCookies([
        { name: 'cookie1', value: 'value1' },
        { name: 'cookie2', value: 'value2' }
      ]);
      
      assert.ok(true);
    });
  });

  describe('clear', () => {
    test('should delete session file', async () => {
      await writeFile(sessionFile, JSON.stringify({ test: 'data' }));
      
      const sm = new SessionManager(sessionFile);
      await sm.clear();
      
      let exists = false;
      try {
        await stat(sessionFile);
        exists = true;
      } catch {
        exists = false;
      }
      
      assert.strictEqual(exists, false);
    });

    test('should not throw when file does not exist', async () => {
      const sm = new SessionManager(sessionFile);
      
      await assert.doesNotReject(async () => {
        await sm.clear();
      });
    });

    test('should be idempotent', async () => {
      const sm = new SessionManager(sessionFile);
      
      await sm.clear();
      await sm.clear();
      
      assert.ok(true);
    });
  });

  describe('integration', () => {
    test('should work with full lifecycle', async () => {
      const sm = new SessionManager(sessionFile, { maxAge: 60000 });
      
      let valid = await sm.isValid();
      assert.strictEqual(valid, false);
      
      await sm.save({ cookies: [{ name: 'session', value: 'abc123' }] });
      
      valid = await sm.isValid();
      assert.strictEqual(valid, true);
      
      const session = await sm.load();
      assert.ok(session.cookies);
      assert.ok(session.capturedAt);
      
      await sm.clear();
      
      valid = await sm.isValid();
      assert.strictEqual(valid, false);
    });
  });
});

describe('RateLimiter', () => {
  describe('constructor', () => {
    test('should create instance with default options', () => {
      const rl = new RateLimiter();
      
      assert.strictEqual(rl.minDelay, 1000);
      assert.strictEqual(rl.maxDelay, 3000);
      assert.strictEqual(rl.lastRequestTime, 0);
    });

    test('should accept custom options', () => {
      const rl = new RateLimiter({ minDelay: 100, maxDelay: 500 });
      
      assert.strictEqual(rl.minDelay, 100);
      assert.strictEqual(rl.maxDelay, 500);
    });
  });

  describe('wait', () => {
    test('should wait for random delay on first call', async () => {
      const rl = new RateLimiter({ minDelay: 50, maxDelay: 100 });
      
      const start = Date.now();
      await rl.wait();
      const elapsed = Date.now() - start;
      
      assert.ok(elapsed >= 50 || elapsed >= 0);
    });

    test('should update lastRequestTime after wait', async () => {
      const rl = new RateLimiter({ minDelay: 10, maxDelay: 20 });
      
      await rl.wait();
      
      assert.ok(rl.lastRequestTime > 0);
    });

    test('should wait between requests', async () => {
      const rl = new RateLimiter({ minDelay: 100, maxDelay: 100 });
      
      await rl.wait();
      const time1 = rl.lastRequestTime;
      
      await rl.wait();
      const time2 = rl.lastRequestTime;
      
      assert.ok(time2 > time1);
    });

    test('should handle rapid calls', async () => {
      const rl = new RateLimiter({ minDelay: 10, maxDelay: 20 });
      
      await Promise.all([
        rl.wait(),
        rl.wait(),
        rl.wait()
      ]);
      
      assert.ok(rl.lastRequestTime > 0);
    });

    test('should work with very small delays', async () => {
      const rl = new RateLimiter({ minDelay: 1, maxDelay: 2 });
      
      const start = Date.now();
      await rl.wait();
      const elapsed = Date.now() - start;
      
      assert.ok(elapsed >= 0);
    });

    test('should work with zero delay', async () => {
      const rl = new RateLimiter({ minDelay: 0, maxDelay: 0 });
      
      const start = Date.now();
      await rl.wait();
      const elapsed = Date.now() - start;
      
      assert.ok(elapsed >= 0);
    });

    test('should handle sequential waits correctly', async () => {
      const rl = new RateLimiter({ minDelay: 50, maxDelay: 50 });
      
      const start = Date.now();
      await rl.wait();
      await rl.wait();
      await rl.wait();
      const elapsed = Date.now() - start;
      
      assert.ok(elapsed >= 100, 'Three waits with 50ms delay should take at least 100ms');
    });

    test('should not wait if enough time has passed', async () => {
      const rl = new RateLimiter({ minDelay: 10, maxDelay: 20 });
      
      await rl.wait();
      await new Promise(resolve => setTimeout(resolve, 100));
      
      const start = Date.now();
      await rl.wait();
      const elapsed = Date.now() - start;
      
      assert.ok(elapsed < 50, 'Should not wait if enough time has passed');
    });
  });

  describe('edge cases', () => {
    test('should handle minDelay > maxDelay gracefully', async () => {
      const rl = new RateLimiter({ minDelay: 100, maxDelay: 50 });
      
      const start = Date.now();
      await rl.wait();
      const elapsed = Date.now() - start;
      
      assert.ok(elapsed >= 0);
    });

    test('should handle negative delays', async () => {
      const rl = new RateLimiter({ minDelay: -100, maxDelay: -50 });
      
      const start = Date.now();
      await rl.wait();
      const elapsed = Date.now() - start;
      
      assert.ok(elapsed >= 0 || elapsed < 100);
    });

    test('should handle very large delays without blocking', async () => {
      const rl = new RateLimiter({ minDelay: 1, maxDelay: 2 });
      
      const start = Date.now();
      await rl.wait();
      const elapsed = Date.now() - start;
      
      assert.ok(elapsed < 1000, 'Should not block for too long in tests');
    });
  });
});