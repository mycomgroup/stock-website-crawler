import { jest } from '@jest/globals';

const mockLaunch = jest.fn();
const mockAddInitScript = jest.fn();
const mockSetExtraHTTPHeaders = jest.fn();
const mockMouseMove = jest.fn();
const mockEvaluate = jest.fn();
const mockPage = {
  addInitScript: mockAddInitScript,
  setExtraHTTPHeaders: mockSetExtraHTTPHeaders,
  mouse: {
    move: mockMouseMove
  },
  evaluate: mockEvaluate
};

jest.unstable_mockModule('playwright', () => ({
  chromium: {
    launch: mockLaunch
  }
}));

const mockReadFile = jest.fn();
const mockWriteFile = jest.fn();
const mockMkdir = jest.fn();
const mockUnlink = jest.fn();

jest.unstable_mockModule('fs/promises', () => ({
  default: {
    readFile: mockReadFile,
    writeFile: mockWriteFile,
    mkdir: mockMkdir,
    unlink: mockUnlink
  },
  readFile: mockReadFile,
  writeFile: mockWriteFile,
  mkdir: mockMkdir,
  unlink: mockUnlink
}));

jest.unstable_mockModule('path', () => ({
  default: {
    dirname: jest.fn((p) => p.split('/').slice(0, -1).join('/'))
  },
  dirname: jest.fn((p) => p.split('/').slice(0, -1).join('/'))
}));

const mockFetch = jest.fn();
global.fetch = mockFetch;

beforeAll(() => {
  jest.spyOn(console, 'log').mockImplementation(() => {});
  jest.spyOn(console, 'error').mockImplementation(() => {});
});

afterAll(() => {
  console.log.mockRestore();
  console.error.mockRestore();
});

beforeEach(() => {
  jest.clearAllMocks();
});

const { AntiDetection, SessionManager, RateLimiter } = await import('../lib/anti-detection.js');

describe('AntiDetection', () => {
  describe('setupBrowser', () => {
    it('should launch browser with default args', async () => {
      const mockBrowser = { close: jest.fn() };
      mockLaunch.mockResolvedValue(mockBrowser);

      const browser = await AntiDetection.setupBrowser();

      expect(mockLaunch).toHaveBeenCalledTimes(1);
      const launchOptions = mockLaunch.mock.calls[0][0];
      expect(launchOptions.headless).toBe(true);
      expect(launchOptions.args).toContain('--disable-blink-features=AutomationControlled');
      expect(launchOptions.args).toContain('--no-sandbox');
    });

    it('should respect headless: false option', async () => {
      const mockBrowser = { close: jest.fn() };
      mockLaunch.mockResolvedValue(mockBrowser);

      await AntiDetection.setupBrowser({ headless: false });

      const launchOptions = mockLaunch.mock.calls[0][0];
      expect(launchOptions.headless).toBe(false);
    });

    it('should merge custom args with default args', async () => {
      const mockBrowser = { close: jest.fn() };
      mockLaunch.mockResolvedValue(mockBrowser);

      await AntiDetection.setupBrowser({ args: ['--custom-arg'] });

      const launchOptions = mockLaunch.mock.calls[0][0];
      expect(launchOptions.args).toContain('--custom-arg');
      expect(launchOptions.args).toContain('--disable-blink-features=AutomationControlled');
      expect(launchOptions.args).toContain('--no-sandbox');
    });

    it('should pass through additional options', async () => {
      const mockBrowser = { close: jest.fn() };
      mockLaunch.mockResolvedValue(mockBrowser);

      await AntiDetection.setupBrowser({ slowMo: 100 });

      const launchOptions = mockLaunch.mock.calls[0][0];
      expect(launchOptions.slowMo).toBe(100);
    });
  });

  describe('injectAntiDetection', () => {
    it('should call addInitScript on page', async () => {
      await AntiDetection.injectAntiDetection(mockPage);

      expect(mockAddInitScript).toHaveBeenCalledTimes(1);
      expect(mockAddInitScript).toHaveBeenCalledWith(expect.any(Function));
    });

    it('should pass a valid function to addInitScript', async () => {
      await AntiDetection.injectAntiDetection(mockPage);

      const scriptFn = mockAddInitScript.mock.calls[0][0];
      expect(typeof scriptFn).toBe('function');
    });
  });

  describe('setRealisticHeaders', () => {
    it('should set default headers on page', async () => {
      await AntiDetection.setRealisticHeaders(mockPage);

      expect(mockSetExtraHTTPHeaders).toHaveBeenCalledTimes(1);
      const headers = mockSetExtraHTTPHeaders.mock.calls[0][0];
      expect(headers).toHaveProperty('Accept-Language');
      expect(headers).toHaveProperty('User-Agent');
      expect(headers['Accept-Language']).toBe('zh-CN,zh;q=0.9,en;q=0.8');
    });

    it('should merge custom headers with defaults', async () => {
      await AntiDetection.setRealisticHeaders(mockPage, { 'X-Custom': 'value' });

      const headers = mockSetExtraHTTPHeaders.mock.calls[0][0];
      expect(headers['X-Custom']).toBe('value');
      expect(headers).toHaveProperty('Accept-Language');
    });

    it('should override default headers with custom headers', async () => {
      await AntiDetection.setRealisticHeaders(mockPage, { 'Accept-Language': 'en-US' });

      const headers = mockSetExtraHTTPHeaders.mock.calls[0][0];
      expect(headers['Accept-Language']).toBe('en-US');
    });
  });

  describe('randomDelay', () => {
    it('should return a promise', () => {
      const result = AntiDetection.randomDelay(10, 20);
      expect(result).toBeInstanceOf(Promise);
    });

    it('should resolve after delay', async () => {
      jest.useFakeTimers();
      const delayPromise = AntiDetection.randomDelay(100, 100);
      jest.advanceTimersByTime(100);
      await expect(delayPromise).resolves.toBeUndefined();
      jest.useRealTimers();
    });
  });

  describe('getRandomUserAgent', () => {
    it('should return a string', () => {
      const ua = AntiDetection.getRandomUserAgent();
      expect(typeof ua).toBe('string');
    });

    it('should return valid Chrome user agent', () => {
      const ua = AntiDetection.getRandomUserAgent();
      expect(ua).toContain('Mozilla/5.0');
      expect(ua).toContain('Chrome');
    });

    it('should return one of the predefined user agents', () => {
      const userAgents = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
      ];
      const ua = AntiDetection.getRandomUserAgent();
      expect(userAgents).toContain(ua);
    });
  });

  describe('simulateHumanBehavior', () => {
    it('should move mouse with steps parameter', async () => {
      mockMouseMove.mockResolvedValue(undefined);
      mockEvaluate.mockResolvedValue(undefined);

      const promise = AntiDetection.simulateHumanBehavior(mockPage);
      
      await jest.runAllTimersAsync();
      await promise;

      expect(mockMouseMove).toHaveBeenCalledTimes(1);
      const moveCall = mockMouseMove.mock.calls[0];
      expect(moveCall[2]).toEqual({ steps: 10 });
    });

    it('should scroll page', async () => {
      mockMouseMove.mockResolvedValue(undefined);
      mockEvaluate.mockResolvedValue(undefined);

      const promise = AntiDetection.simulateHumanBehavior(mockPage);
      
      await jest.runAllTimersAsync();
      await promise;

      expect(mockEvaluate).toHaveBeenCalledTimes(1);
    });
  });

  describe('fetchWithRetry', () => {
    it('should return response on first success', async () => {
      const mockResponse = { ok: true, status: 200 };
      const fetchFn = jest.fn().mockResolvedValue(mockResponse);

      const result = await AntiDetection.fetchWithRetry(fetchFn);

      expect(fetchFn).toHaveBeenCalledTimes(1);
      expect(result).toBe(mockResponse);
    });

    it('should throw on non-OK response that is not 429', async () => {
      const errorResponse = { ok: false, status: 500, statusText: 'Internal Server Error' };
      const fetchFn = jest.fn().mockResolvedValue(errorResponse);

      await expect(AntiDetection.fetchWithRetry(fetchFn, { maxRetries: 1 }))
        .rejects.toThrow('HTTP 500: Internal Server Error');
    });

    it('should retry on failure with backoff', async () => {
      const mockResponse = { ok: true, status: 200 };
      const fetchFn = jest.fn()
        .mockRejectedValueOnce(new Error('Network error'))
        .mockResolvedValue(mockResponse);

      const promise = AntiDetection.fetchWithRetry(fetchFn, { maxRetries: 3, retryDelay: 100, backoff: true });
      
      await jest.runAllTimersAsync();
      await promise;

      expect(fetchFn).toHaveBeenCalledTimes(2);
    });

    it('should throw after max retries', async () => {
      const error = new Error('Network error');
      const fetchFn = jest.fn().mockRejectedValue(error);

      const promise = AntiDetection.fetchWithRetry(fetchFn, { maxRetries: 2, retryDelay: 10 });
      
      await jest.runAllTimersAsync();
      await expect(promise).rejects.toThrow('Network error');
      expect(fetchFn).toHaveBeenCalledTimes(2);
    });

    it('should handle 429 rate limiting', async () => {
      const mockResponse = { ok: true, status: 200 };
      const rateLimitedResponse = { ok: false, status: 429, statusText: 'Too Many Requests' };
      const fetchFn = jest.fn()
        .mockResolvedValueOnce(rateLimitedResponse)
        .mockResolvedValue(mockResponse);

      const promise = AntiDetection.fetchWithRetry(fetchFn, { maxRetries: 3, retryDelay: 100 });
      
      await jest.runAllTimersAsync();
      await promise;

      expect(fetchFn).toHaveBeenCalledTimes(2);
    });

    it('should not use exponential backoff when disabled', async () => {
      const mockResponse = { ok: true, status: 200 };
      const fetchFn = jest.fn()
        .mockRejectedValueOnce(new Error('Error'))
        .mockResolvedValue(mockResponse);

      const promise = AntiDetection.fetchWithRetry(fetchFn, { maxRetries: 3, retryDelay: 100, backoff: false });
      
      await jest.runAllTimersAsync();
      await promise;

      expect(fetchFn).toHaveBeenCalledTimes(2);
    });
  });

  describe('createRealisticHeaders', () => {
    it('should return headers object with all required properties', () => {
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

    it('should merge custom headers', () => {
      const headers = AntiDetection.createRealisticHeaders({ 'X-Custom': 'value' });

      expect(headers['X-Custom']).toBe('value');
    });

    it('should override default headers with custom', () => {
      const headers = AntiDetection.createRealisticHeaders({ 'Accept': 'text/html' });

      expect(headers['Accept']).toBe('text/html');
    });
  });
});

describe('SessionManager', () => {
  const testSessionFile = '/tmp/test-session.json';

  describe('constructor', () => {
    it('should use default maxAge when not provided', () => {
      const manager = new SessionManager(testSessionFile);
      expect(manager.maxAge).toBe(7 * 24 * 60 * 60 * 1000);
    });

    it('should use custom maxAge', () => {
      const manager = new SessionManager(testSessionFile, { maxAge: 1000 });
      expect(manager.maxAge).toBe(1000);
    });

    it('should store validateUrl', () => {
      const manager = new SessionManager(testSessionFile, { validateUrl: 'https://example.com' });
      expect(manager.validateUrl).toBe('https://example.com');
    });
  });

  describe('load', () => {
    it('should load and parse session from file', async () => {
      const sessionData = { token: 'abc123', cookies: [] };
      mockReadFile.mockResolvedValue(JSON.stringify(sessionData));

      const manager = new SessionManager(testSessionFile);
      const session = await manager.load();

      expect(session).toEqual(sessionData);
      expect(mockReadFile).toHaveBeenCalledWith(testSessionFile, 'utf-8');
    });

    it('should return null when file does not exist', async () => {
      mockReadFile.mockRejectedValue(new Error('ENOENT'));

      const manager = new SessionManager(testSessionFile);
      const session = await manager.load();

      expect(session).toBeNull();
    });

    it('should return null on JSON parse error', async () => {
      mockReadFile.mockResolvedValue('invalid json');

      const manager = new SessionManager(testSessionFile);
      const session = await manager.load();

      expect(session).toBeNull();
    });
  });

  describe('save', () => {
    it('should save session with capturedAt timestamp', async () => {
      mockMkdir.mockResolvedValue(undefined);
      mockWriteFile.mockResolvedValue(undefined);

      const manager = new SessionManager(testSessionFile);
      const session = { token: 'abc123' };
      await manager.save(session);

      expect(mockWriteFile).toHaveBeenCalled();
      const savedData = JSON.parse(mockWriteFile.mock.calls[0][1]);
      expect(savedData.token).toBe('abc123');
      expect(savedData.capturedAt).toBeDefined();
    });

    it('should create directory if not exists', async () => {
      mockMkdir.mockResolvedValue(undefined);
      mockWriteFile.mockResolvedValue(undefined);

      const manager = new SessionManager('/tmp/nested/dir/session.json');
      await manager.save({ token: 'test' });

      expect(mockMkdir).toHaveBeenCalledWith('/tmp/nested/dir', { recursive: true });
    });
  });

  describe('isValid', () => {
    it('should return false when no session', async () => {
      mockReadFile.mockRejectedValue(new Error('ENOENT'));

      const manager = new SessionManager(testSessionFile);
      const valid = await manager.isValid();

      expect(valid).toBe(false);
    });

    it('should return false when no capturedAt', async () => {
      mockReadFile.mockResolvedValue(JSON.stringify({ token: 'abc' }));

      const manager = new SessionManager(testSessionFile);
      const valid = await manager.isValid();

      expect(valid).toBe(false);
    });

    it('should return false when session is expired', async () => {
      const oldDate = new Date(Date.now() - 10 * 24 * 60 * 60 * 1000).toISOString();
      mockReadFile.mockResolvedValue(JSON.stringify({ capturedAt: oldDate }));

      const manager = new SessionManager(testSessionFile, { maxAge: 1000 });
      const valid = await manager.isValid();

      expect(valid).toBe(false);
    });

    it('should return true for valid session', async () => {
      const recentDate = new Date().toISOString();
      mockReadFile.mockResolvedValue(JSON.stringify({ capturedAt: recentDate }));

      const manager = new SessionManager(testSessionFile);
      const valid = await manager.isValid();

      expect(valid).toBe(true);
    });

    it('should validate cookies when validateUrl is provided', async () => {
      const recentDate = new Date().toISOString();
      const cookies = [{ name: 'session', value: 'abc123' }];
      mockReadFile.mockResolvedValue(JSON.stringify({ capturedAt: recentDate, cookies }));
      mockFetch.mockResolvedValue({ ok: true });

      const manager = new SessionManager(testSessionFile, { validateUrl: 'https://example.com' });
      const valid = await manager.isValid();

      expect(mockFetch).toHaveBeenCalledWith(
        'https://example.com',
        expect.objectContaining({
          headers: expect.objectContaining({
            'Cookie': 'session=abc123'
          })
        })
      );
    });

    it('should return false when cookie validation fails', async () => {
      const recentDate = new Date().toISOString();
      const cookies = [{ name: 'session', value: 'abc123' }];
      mockReadFile.mockResolvedValue(JSON.stringify({ capturedAt: recentDate, cookies }));
      mockFetch.mockResolvedValue({ ok: false });

      const manager = new SessionManager(testSessionFile, { validateUrl: 'https://example.com' });
      const valid = await manager.isValid();

      expect(valid).toBe(false);
    });
  });

  describe('validateCookies', () => {
    it('should return true when no validateUrl', async () => {
      const manager = new SessionManager(testSessionFile);
      const valid = await manager.validateCookies([]);

      expect(valid).toBe(true);
    });

    it('should return true for valid cookies', async () => {
      mockFetch.mockResolvedValue({ ok: true });

      const manager = new SessionManager(testSessionFile, { validateUrl: 'https://example.com' });
      const cookies = [{ name: 'session', value: 'abc123' }];
      const valid = await manager.validateCookies(cookies);

      expect(valid).toBe(true);
    });

    it('should return false for invalid cookies', async () => {
      mockFetch.mockResolvedValue({ ok: false });

      const manager = new SessionManager(testSessionFile, { validateUrl: 'https://example.com' });
      const cookies = [{ name: 'session', value: 'invalid' }];
      const valid = await manager.validateCookies(cookies);

      expect(valid).toBe(false);
    });

    it('should return false on fetch error', async () => {
      mockFetch.mockRejectedValue(new Error('Network error'));

      const manager = new SessionManager(testSessionFile, { validateUrl: 'https://example.com' });
      const cookies = [{ name: 'session', value: 'abc123' }];
      const valid = await manager.validateCookies(cookies);

      expect(valid).toBe(false);
    });

    it('should handle multiple cookies', async () => {
      mockFetch.mockResolvedValue({ ok: true });

      const manager = new SessionManager(testSessionFile, { validateUrl: 'https://example.com' });
      const cookies = [
        { name: 'session', value: 'abc123' },
        { name: 'token', value: 'xyz789' }
      ];
      await manager.validateCookies(cookies);

      expect(mockFetch).toHaveBeenCalledWith(
        'https://example.com',
        expect.objectContaining({
          headers: expect.objectContaining({
            'Cookie': 'session=abc123; token=xyz789'
          })
        })
      );
    });
  });

  describe('clear', () => {
    it('should delete session file', async () => {
      mockUnlink.mockResolvedValue(undefined);

      const manager = new SessionManager(testSessionFile);
      await manager.clear();

      expect(mockUnlink).toHaveBeenCalledWith(testSessionFile);
    });

    it('should ignore error when file does not exist', async () => {
      mockUnlink.mockRejectedValue(new Error('ENOENT'));

      const manager = new SessionManager(testSessionFile);
      await expect(manager.clear()).resolves.not.toThrow();
    });
  });
});

describe('RateLimiter', () => {
  describe('constructor', () => {
    it('should use default delays when not provided', () => {
      const limiter = new RateLimiter();
      expect(limiter.minDelay).toBe(1000);
      expect(limiter.maxDelay).toBe(3000);
    });

    it('should use custom delays', () => {
      const limiter = new RateLimiter({ minDelay: 500, maxDelay: 1000 });
      expect(limiter.minDelay).toBe(500);
      expect(limiter.maxDelay).toBe(1000);
    });

    it('should initialize lastRequestTime to 0', () => {
      const limiter = new RateLimiter();
      expect(limiter.lastRequestTime).toBe(0);
    });
  });

  describe('wait', () => {
    beforeEach(() => {
      jest.useFakeTimers();
    });

    afterEach(() => {
      jest.useRealTimers();
    });

    it('should wait when no previous request', async () => {
      jest.spyOn(Math, 'random').mockReturnValue(0);
      jest.setSystemTime(0);
      const limiter = new RateLimiter({ minDelay: 100, maxDelay: 100 });

      const promise = limiter.wait();
      await jest.runAllTimersAsync();
      await promise;

      expect(limiter.lastRequestTime).toBe(100);
    });

    it('should update lastRequestTime after wait', async () => {
      jest.spyOn(Math, 'random').mockReturnValue(0);
      const limiter = new RateLimiter({ minDelay: 100, maxDelay: 100 });

      const promise = limiter.wait();
      await jest.runAllTimersAsync();
      await promise;

      expect(limiter.lastRequestTime).toBeGreaterThan(0);
    });

    it('should not wait if enough time has passed since last request', async () => {
      jest.spyOn(Math, 'random').mockReturnValue(0);
      const limiter = new RateLimiter({ minDelay: 100, maxDelay: 100 });
      limiter.lastRequestTime = 0;

      jest.setSystemTime(10000);

      const promise = limiter.wait();
      await jest.runAllTimersAsync();
      await promise;

      expect(limiter.lastRequestTime).toBe(10000);
    });

    it('should wait remaining time if not enough time has passed', async () => {
      jest.spyOn(Math, 'random').mockReturnValue(0);
      const limiter = new RateLimiter({ minDelay: 1000, maxDelay: 1000 });
      limiter.lastRequestTime = 0;

      jest.setSystemTime(500);

      const promise = limiter.wait();
      await jest.advanceTimersByTimeAsync(500);
      await promise;

      expect(limiter.lastRequestTime).toBe(1000);
    });

    it('should calculate random delay within range', () => {
      const limiter = new RateLimiter({ minDelay: 1000, maxDelay: 3000 });

      for (let i = 0; i < 100; i++) {
        jest.spyOn(Math, 'random').mockReturnValue(i / 100);
        const delay = limiter.minDelay + (i / 100) * (limiter.maxDelay - limiter.minDelay);
        expect(delay).toBeGreaterThanOrEqual(1000);
        expect(delay).toBeLessThanOrEqual(3000);
      }
    });
  });

  describe('multiple requests', () => {
    beforeEach(() => {
      jest.useFakeTimers();
    });

    afterEach(() => {
      jest.useRealTimers();
    });

    it('should enforce rate limiting across multiple requests', async () => {
      jest.spyOn(Math, 'random').mockReturnValue(0);
      const limiter = new RateLimiter({ minDelay: 100, maxDelay: 100 });

      jest.setSystemTime(0);

      const promise1 = limiter.wait();
      await jest.runAllTimersAsync();
      await promise1;
      const time1 = limiter.lastRequestTime;

      jest.setSystemTime(time1 + 50);

      const promise2 = limiter.wait();
      await jest.runAllTimersAsync();
      await promise2;
      const time2 = limiter.lastRequestTime;

      expect(time2).toBeGreaterThan(time1);
    });
  });
});

describe('Integration Tests', () => {
  describe('AntiDetection and SessionManager integration', () => {
    it('should create realistic headers for session validation', async () => {
      const headers = AntiDetection.createRealisticHeaders();

      expect(headers['User-Agent']).toBeDefined();
      expect(headers['Accept-Language']).toBe('zh-CN,zh;q=0.9,en;q=0.8');

      mockFetch.mockResolvedValue({ ok: true });
      mockReadFile.mockResolvedValue(JSON.stringify({
        capturedAt: new Date().toISOString(),
        cookies: [{ name: 'test', value: '123' }]
      }));

      const manager = new SessionManager('/tmp/test-session.json', { validateUrl: 'https://example.com' });
      const valid = await manager.isValid();

      expect(typeof valid).toBe('boolean');
    });
  });
});