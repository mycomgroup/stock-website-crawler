import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { chromium } from 'playwright';

vi.mock('playwright', () => ({
  chromium: {
    launch: vi.fn(),
  },
}));

vi.mock('../paths.js', () => ({
  SESSION_FILE: '/test/sessions/thsquant.json',
  OUTPUT_ROOT: '/test/output',
}));

vi.mock('node:fs/promises', () => ({
  readFile: vi.fn(),
  writeFile: vi.fn(),
  mkdir: vi.fn(),
  unlink: vi.fn(),
  readdir: vi.fn(),
}));

vi.mock('node:path', () => ({
  dirname: vi.fn((p) => p.split('/').slice(0, -1).join('/')),
  join: vi.fn((...args) => args.join('/')),
}));

let AntiDetection, SessionManager, RateLimiter;

beforeAll(async () => {
  const module = await import('../lib/anti-detection.js');
  AntiDetection = module.AntiDetection;
  SessionManager = module.SessionManager;
  RateLimiter = module.RateLimiter;
});

describe('AntiDetection', () => {
  let mockBrowser;
  let mockPage;

  beforeEach(() => {
    vi.clearAllMocks();

    mockPage = {
      addInitScript: vi.fn().mockResolvedValue(undefined),
      setExtraHTTPHeaders: vi.fn().mockResolvedValue(undefined),
      mouse: {
        move: vi.fn().mockResolvedValue(undefined),
      },
      evaluate: vi.fn().mockResolvedValue(undefined),
    };

    mockBrowser = {
      newContext: vi.fn().mockResolvedValue({
        newPage: vi.fn().mockResolvedValue(mockPage),
      }),
      close: vi.fn().mockResolvedValue(undefined),
    };

    chromium.launch.mockResolvedValue(mockBrowser);
  });

  describe('setupBrowser', () => {
    it('launches browser with default args', async () => {
      const browser = await AntiDetection.setupBrowser();

      expect(chromium.launch).toHaveBeenCalledWith(
        expect.objectContaining({
          headless: true,
          args: expect.arrayContaining([
            '--disable-blink-features=AutomationControlled',
          ]),
        })
      );
      expect(browser).toBe(mockBrowser);
    });

    it('launches browser in headed mode', async () => {
      await AntiDetection.setupBrowser({ headless: false });

      expect(chromium.launch).toHaveBeenCalledWith(
        expect.objectContaining({
          headless: false,
        })
      );
    });

    it('includes custom args', async () => {
      await AntiDetection.setupBrowser({ args: ['--custom-arg'] });

      expect(chromium.launch).toHaveBeenCalledWith(
        expect.objectContaining({
          args: expect.arrayContaining(['--custom-arg']),
        })
      );
    });
  });

  describe('injectAntiDetection', () => {
    it('calls addInitScript on page', async () => {
      await AntiDetection.injectAntiDetection(mockPage);

      expect(mockPage.addInitScript).toHaveBeenCalled();
    });
  });

  describe('setRealisticHeaders', () => {
    it('sets default headers', async () => {
      await AntiDetection.setRealisticHeaders(mockPage);

      expect(mockPage.setExtraHTTPHeaders).toHaveBeenCalledWith(
        expect.objectContaining({
          'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        })
      );
    });

    it('includes custom headers', async () => {
      await AntiDetection.setRealisticHeaders(mockPage, { 'X-Custom': 'value' });

      expect(mockPage.setExtraHTTPHeaders).toHaveBeenCalledWith(
        expect.objectContaining({
          'X-Custom': 'value',
        })
      );
    });
  });

  describe('randomDelay', () => {
    it('delays execution', async () => {
      const start = Date.now();
      await AntiDetection.randomDelay(100, 200);
      const elapsed = Date.now() - start;

      expect(elapsed).toBeGreaterThanOrEqual(90);
    });
  });

  describe('getRandomUserAgent', () => {
    it('returns a valid user agent string', () => {
      const ua = AntiDetection.getRandomUserAgent();

      expect(ua).toContain('Mozilla');
      expect(ua).toContain('Chrome');
    });

    it('returns different user agents on multiple calls', () => {
      const results = new Set();
      for (let i = 0; i < 10; i++) {
        results.add(AntiDetection.getRandomUserAgent());
      }

      expect(results.size).toBeGreaterThan(1);
    });
  });

  describe('simulateHumanBehavior', () => {
    it('moves mouse', async () => {
      await AntiDetection.simulateHumanBehavior(mockPage);

      expect(mockPage.mouse.move).toHaveBeenCalled();
    });

    it('scrolls page', async () => {
      await AntiDetection.simulateHumanBehavior(mockPage);

      expect(mockPage.evaluate).toHaveBeenCalled();
    });
  });

  describe('fetchWithRetry', () => {
    it('returns successful response', async () => {
      const mockResponse = { ok: true, status: 200 };
      const fetchFn = vi.fn().mockResolvedValue(mockResponse);

      const result = await AntiDetection.fetchWithRetry(fetchFn);

      expect(result).toEqual(mockResponse);
      expect(fetchFn).toHaveBeenCalledTimes(1);
    });

    it('retries on 429 status', async () => {
      const mockResponse = { ok: false, status: 429 };
      const successResponse = { ok: true, status: 200 };
      const fetchFn = vi.fn()
        .mockResolvedValueOnce(mockResponse)
        .mockResolvedValueOnce(successResponse);

      const consoleSpy = vi.spyOn(console, 'log').mockImplementation(() => {});

      const result = await AntiDetection.fetchWithRetry(fetchFn, { retryDelay: 100 });

      expect(result).toEqual(successResponse);
      expect(fetchFn).toHaveBeenCalledTimes(2);

      consoleSpy.mockRestore();
    });

    it('throws after max retries', async () => {
      const mockResponse = { ok: false, status: 500, statusText: 'Server Error' };
      const fetchFn = vi.fn().mockResolvedValue(mockResponse);

      await expect(
        AntiDetection.fetchWithRetry(fetchFn, { maxRetries: 2, retryDelay: 100 })
      ).rejects.toThrow();

      expect(fetchFn).toHaveBeenCalledTimes(2);
    });

    it('retries on network error', async () => {
      const successResponse = { ok: true, status: 200 };
      const fetchFn = vi.fn()
        .mockRejectedValueOnce(new Error('Network error'))
        .mockResolvedValueOnce(successResponse);

      const consoleSpy = vi.spyOn(console, 'log').mockImplementation(() => {});

      const result = await AntiDetection.fetchWithRetry(fetchFn, { maxRetries: 3, retryDelay: 100 });

      expect(result).toEqual(successResponse);
      expect(fetchFn).toHaveBeenCalledTimes(2);

      consoleSpy.mockRestore();
    });
  });

  describe('createRealisticHeaders', () => {
    it('returns complete headers object', () => {
      const headers = AntiDetection.createRealisticHeaders();

      expect(headers['User-Agent']).toBeDefined();
      expect(headers['Accept']).toBe('application/json, text/plain, */*');
      expect(headers['Accept-Language']).toBe('zh-CN,zh;q=0.9,en;q=0.8');
    });

    it('includes custom headers', () => {
      const headers = AntiDetection.createRealisticHeaders({ 'X-Custom': 'value' });

      expect(headers['X-Custom']).toBe('value');
    });

    it('overrides default headers', () => {
      const headers = AntiDetection.createRealisticHeaders({ 'Accept': 'text/html' });

      expect(headers['Accept']).toBe('text/html');
    });
  });
});

describe('SessionManager', () => {
  let fsPromises;

  beforeEach(async () => {
    vi.clearAllMocks();
    fsPromises = await import('node:fs/promises');
  });

  describe('constructor', () => {
    it('initializes with default options', () => {
      const sm = new SessionManager('/test/session.json');

      expect(sm.sessionFile).toBe('/test/session.json');
      expect(sm.maxAge).toBe(7 * 24 * 60 * 60 * 1000);
    });

    it('accepts custom maxAge', () => {
      const sm = new SessionManager('/test/session.json', { maxAge: 1000 });

      expect(sm.maxAge).toBe(1000);
    });

    it('accepts validateUrl', () => {
      const sm = new SessionManager('/test/session.json', {
        validateUrl: 'https://test.com/validate'
      });

      expect(sm.validateUrl).toBe('https://test.com/validate');
    });
  });

  describe('load', () => {
    it('loads session from file', async () => {
      const mockSession = { cookies: [{ name: 'sid', value: 'test' }] };
      fsPromises.readFile.mockResolvedValue(JSON.stringify(mockSession));

      const sm = new SessionManager('/test/session.json');
      const result = await sm.load();

      expect(result).toEqual(mockSession);
    });

    it('returns null on file read error', async () => {
      fsPromises.readFile.mockRejectedValue(new Error('File not found'));

      const sm = new SessionManager('/test/session.json');
      const result = await sm.load();

      expect(result).toBeNull();
    });

    it('returns null on JSON parse error', async () => {
      fsPromises.readFile.mockResolvedValue('invalid json');

      const sm = new SessionManager('/test/session.json');
      const result = await sm.load();

      expect(result).toBeNull();
    });
  });

  describe('save', () => {
    it('saves session to file', async () => {
      fsPromises.writeFile.mockResolvedValue(undefined);
      fsPromises.mkdir.mockResolvedValue(undefined);

      const sm = new SessionManager('/dir/session.json');
      await sm.save({ cookies: [] });

      expect(fsPromises.writeFile).toHaveBeenCalled();
    });

    it('adds capturedAt timestamp', async () => {
      fsPromises.writeFile.mockResolvedValue(undefined);
      fsPromises.mkdir.mockResolvedValue(undefined);

      const sm = new SessionManager('/dir/session.json');
      await sm.save({ cookies: [] });

      const savedData = JSON.parse(fsPromises.writeFile.mock.calls[0][1]);
      expect(savedData.capturedAt).toBeDefined();
    });
  });

  describe('isValid', () => {
    it('returns false for null session', async () => {
      fsPromises.readFile.mockResolvedValue(null);

      const sm = new SessionManager('/test/session.json');
      const result = await sm.isValid();

      expect(result).toBe(false);
    });

    it('returns false for session without capturedAt', async () => {
      fsPromises.readFile.mockResolvedValue(JSON.stringify({ cookies: [] }));

      const sm = new SessionManager('/test/session.json');
      const result = await sm.isValid();

      expect(result).toBe(false);
    });

    it('returns false for expired session', async () => {
      const oldSession = {
        cookies: [{ name: 'sid', value: 'test' }],
        capturedAt: new Date(Date.now() - 10 * 24 * 60 * 60 * 1000).toISOString()
      };
      fsPromises.readFile.mockResolvedValue(JSON.stringify(oldSession));

      const consoleSpy = vi.spyOn(console, 'log').mockImplementation(() => {});

      const sm = new SessionManager('/test/session.json');
      const result = await sm.isValid();

      expect(result).toBe(false);

      consoleSpy.mockRestore();
    });

    it('returns true for valid session', async () => {
      const validSession = {
        cookies: [{ name: 'sid', value: 'test' }],
        capturedAt: new Date().toISOString()
      };
      fsPromises.readFile.mockResolvedValue(JSON.stringify(validSession));

      const sm = new SessionManager('/test/session.json');
      const result = await sm.isValid();

      expect(result).toBe(true);
    });
  });

  describe('clear', () => {
    it('deletes session file', async () => {
      fsPromises.unlink.mockResolvedValue(undefined);

      const sm = new SessionManager('/test/session.json');
      await sm.clear();

      expect(fsPromises.unlink).toHaveBeenCalledWith('/test/session.json');
    });

    it('handles file not found error', async () => {
      fsPromises.unlink.mockRejectedValue(new Error('ENOENT'));

      const sm = new SessionManager('/test/session.json');
      await sm.clear();
    });
  });
});

describe('RateLimiter', () => {
  let rateLimiter;

  beforeEach(() => {
    vi.clearAllMocks();
    rateLimiter = new RateLimiter();
  });

  describe('constructor', () => {
    it('initializes with default options', () => {
      expect(rateLimiter.minDelay).toBe(1000);
      expect(rateLimiter.maxDelay).toBe(3000);
      expect(rateLimiter.lastRequestTime).toBe(0);
    });

    it('accepts custom delays', () => {
      const customLimiter = new RateLimiter({ minDelay: 500, maxDelay: 1000 });

      expect(customLimiter.minDelay).toBe(500);
      expect(customLimiter.maxDelay).toBe(1000);
    });
  });

  describe('wait', () => {
    it('updates lastRequestTime after first call', async () => {
      await rateLimiter.wait();

      expect(rateLimiter.lastRequestTime).toBeGreaterThan(0);
    });

    it('waits between consecutive calls', async () => {
      await rateLimiter.wait();
      const firstTime = rateLimiter.lastRequestTime;

      await new Promise(r => setTimeout(r, 100));
      await rateLimiter.wait();

      expect(rateLimiter.lastRequestTime).toBeGreaterThan(firstTime);
    });
  });
});