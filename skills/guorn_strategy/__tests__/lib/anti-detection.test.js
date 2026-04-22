import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { chromium } from 'playwright';

vi.mock('playwright', () => ({
  chromium: {
    launch: vi.fn(),
  },
}));

vi.mock('fs/promises', () => ({
  default: {
    readFile: vi.fn(),
    writeFile: vi.fn(),
    mkdir: vi.fn(),
    unlink: vi.fn(),
  },
  readFile: vi.fn(),
  writeFile: vi.fn(),
  mkdir: vi.fn(),
  unlink: vi.fn(),
}));

vi.mock('path', () => ({
  default: {
    dirname: vi.fn((p) => p.split('/').slice(0, -1).join('/')),
  },
  dirname: vi.fn((p) => p.split('/').slice(0, -1).join('/')),
}));

describe('lib/anti-detection.js', () => {
  let antiDetection;
  let SessionManager;
  let RateLimiter;

  beforeEach(async () => {
    vi.clearAllMocks();
    vi.resetModules();
    const module = await import('../../lib/anti-detection.js');
    antiDetection = module.AntiDetection;
    SessionManager = module.SessionManager;
    RateLimiter = module.RateLimiter;
  });

  afterEach(() => {
    vi.clearAllMocks();
    vi.useRealTimers();
  });

  describe('AntiDetection class', () => {
    describe('setupBrowser', () => {
      it('should return browser with default args', async () => {
        const mockBrowser = { close: vi.fn() };
        vi.mocked(chromium.launch).mockResolvedValue(mockBrowser);
        
        const result = await antiDetection.setupBrowser();
        
        expect(chromium.launch).toHaveBeenCalledWith(expect.objectContaining({
          headless: true
        }));
        expect(result).toBe(mockBrowser);
      });

      it('should respect headless=false option', async () => {
        const mockBrowser = {};
        vi.mocked(chromium.launch).mockResolvedValue(mockBrowser);
        
        await antiDetection.setupBrowser({ headless: false });
        
        expect(chromium.launch).toHaveBeenCalledWith(expect.objectContaining({ headless: false }));
      });

      it('should merge custom args with default args', async () => {
        const mockBrowser = {};
        vi.mocked(chromium.launch).mockResolvedValue(mockBrowser);
        
        await antiDetection.setupBrowser({ args: ['--custom-arg'] });
        
        const callArgs = vi.mocked(chromium.launch).mock.calls[0][0];
        expect(callArgs.args).toContain('--custom-arg');
      });
    });

    describe('injectAntiDetection', () => {
      it('should call addInitScript on page', async () => {
        const page = { addInitScript: vi.fn() };
        
        await antiDetection.injectAntiDetection(page);
        
        expect(page.addInitScript).toHaveBeenCalledTimes(1);
        expect(page.addInitScript).toHaveBeenCalledWith(expect.any(Function));
      });

      it('should define anti-detection script as function', async () => {
        let capturedScript = null;
        const page = {
          addInitScript: vi.fn((fn) => {
            capturedScript = fn.toString();
          })
        };
        
        await antiDetection.injectAntiDetection(page);
        
        expect(capturedScript).toContain('navigator');
        expect(capturedScript).toContain('webdriver');
        expect(capturedScript).toContain('chrome');
      });
    });

    describe('setRealisticHeaders', () => {
      it('should set default headers on page', async () => {
        const page = { setExtraHTTPHeaders: vi.fn() };
        
        await antiDetection.setRealisticHeaders(page);
        
        expect(page.setExtraHTTPHeaders).toHaveBeenCalledTimes(1);
        expect(page.setExtraHTTPHeaders).toHaveBeenCalledWith(expect.objectContaining({
          'Accept-Language': expect.any(String),
          'User-Agent': expect.any(String)
        }));
      });

      it('should merge custom headers with defaults', async () => {
        const page = { setExtraHTTPHeaders: vi.fn() };
        
        await antiDetection.setRealisticHeaders(page, { 'Custom-Header': 'custom-value' });
        
        expect(page.setExtraHTTPHeaders).toHaveBeenCalledWith(expect.objectContaining({
          'Custom-Header': 'custom-value',
          'Accept-Language': expect.any(String)
        }));
      });

      it('should override default headers with custom headers', async () => {
        const page = { setExtraHTTPHeaders: vi.fn() };
        
        await antiDetection.setRealisticHeaders(page, { 'Accept-Language': 'en-US' });
        
        expect(page.setExtraHTTPHeaders).toHaveBeenCalledWith(expect.objectContaining({
          'Accept-Language': 'en-US'
        }));
      });
    });

    describe('randomDelay', () => {
      it('should delay between min and max', async () => {
        const start = Date.now();
        await antiDetection.randomDelay(50, 100);
        const elapsed = Date.now() - start;
        
        expect(elapsed).toBeGreaterThanOrEqual(50);
        expect(elapsed).toBeLessThanOrEqual(150);
      });

      it('should handle zero delay', async () => {
        const start = Date.now();
        await antiDetection.randomDelay(0, 0);
        const elapsed = Date.now() - start;
        expect(elapsed).toBeLessThan(50);
      });
    });

    describe('getRandomUserAgent', () => {
      it('should return a valid Chrome user agent string', () => {
        const ua = antiDetection.getRandomUserAgent();
        expect(ua).toContain('Mozilla/5.0');
        expect(ua).toContain('Chrome');
        expect(ua).toContain('Safari');
      });

      it('should return one of the predefined user agents', () => {
        const userAgents = ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', 'Mozilla/5.0 (X11; Linux x86_64)'];
        
        for (let i = 0; i < 20; i++) {
          const ua = antiDetection.getRandomUserAgent();
          const found = userAgents.some(prefix => ua.includes(prefix));
          expect(found).toBe(true);
        }
      });

      it('should return different user agents on multiple calls', () => {
        const uas = new Set();
        for (let i = 0; i < 30; i++) {
          uas.add(antiDetection.getRandomUserAgent());
        }
        expect(uas.size).toBeGreaterThanOrEqual(2);
      });
    });

    describe('simulateHumanBehavior', () => {
      it('should move mouse randomly', async () => {
        const page = {
          mouse: { move: vi.fn() },
          evaluate: vi.fn(),
        };
        
        await antiDetection.simulateHumanBehavior(page);
        
        expect(page.mouse.move).toHaveBeenCalledTimes(1);
      });

      it('should scroll randomly', async () => {
        const page = {
          mouse: { move: vi.fn() },
          evaluate: vi.fn(),
        };
        
        await antiDetection.simulateHumanBehavior(page);
        
        expect(page.evaluate).toHaveBeenCalledTimes(1);
      });
    });

    describe('fetchWithRetry', () => {
      it('should return response on first successful attempt', async () => {
        const mockResponse = { ok: true, status: 200 };
        const fetchFn = vi.fn().mockResolvedValue(mockResponse);
        
        const result = await antiDetection.fetchWithRetry(fetchFn);
        
        expect(result).toBe(mockResponse);
        expect(fetchFn).toHaveBeenCalledTimes(1);
      });

      it('should throw after max retries', async () => {
        const fetchFn = vi.fn().mockRejectedValue(new Error('Persistent error'));
        
        await expect(antiDetection.fetchWithRetry(fetchFn, { maxRetries: 2, retryDelay: 10 }))
          .rejects.toThrow('Persistent error');
        
        expect(fetchFn).toHaveBeenCalledTimes(2);
      });

      it('should handle 429 rate limit response', async () => {
        let attempts = 0;
        const fetchFn = vi.fn().mockImplementation(async () => {
          attempts++;
          if (attempts < 2) return { ok: false, status: 429, statusText: 'Too Many Requests' };
          return { ok: true, status: 200 };
        });
        
        const result = await antiDetection.fetchWithRetry(fetchFn, { maxRetries: 3, retryDelay: 10 });
        
        expect(result.ok).toBe(true);
        expect(fetchFn).toHaveBeenCalledTimes(2);
      });

      it('should throw on non-OK response', async () => {
        const fetchFn = vi.fn().mockResolvedValue({ ok: false, status: 500, statusText: 'Server Error' });
        
        await expect(antiDetection.fetchWithRetry(fetchFn, { maxRetries: 1 }))
          .rejects.toThrow('HTTP 500');
      });
    });

    describe('createRealisticHeaders', () => {
      it('should return headers object with required fields', () => {
        const headers = antiDetection.createRealisticHeaders();
        
        expect(headers['User-Agent']).toBeDefined();
        expect(headers['Accept']).toBeDefined();
        expect(headers['Accept-Language']).toBeDefined();
        expect(headers['Accept-Encoding']).toBeDefined();
        expect(headers['Connection']).toBeDefined();
        expect(headers['Sec-Fetch-Dest']).toBeDefined();
        expect(headers['Sec-Fetch-Mode']).toBeDefined();
        expect(headers['Sec-Fetch-Site']).toBeDefined();
        expect(headers['Sec-Ch-Ua']).toBeDefined();
        expect(headers['Sec-Ch-Ua-Mobile']).toBeDefined();
        expect(headers['Sec-Ch-Ua-Platform']).toBeDefined();
      });

      it('should merge custom headers', () => {
        const headers = antiDetection.createRealisticHeaders({ 'X-Custom-Header': 'value' });
        expect(headers['X-Custom-Header']).toBe('value');
      });

      it('should override default headers with custom headers', () => {
        const headers = antiDetection.createRealisticHeaders({ 'Accept': 'text/html' });
        expect(headers['Accept']).toBe('text/html');
      });

      it('should include Chinese locale in Accept-Language', () => {
        const headers = antiDetection.createRealisticHeaders();
        expect(headers['Accept-Language']).toContain('zh-CN');
      });
    });
  });

  describe('SessionManager class', () => {
    describe('constructor', () => {
      it('should initialize with session file', () => {
        const sm = new SessionManager('/path/to/session.json');
        expect(sm.sessionFile).toBe('/path/to/session.json');
        expect(sm.maxAge).toBe(7 * 24 * 60 * 60 * 1000);
      });

      it('should accept custom maxAge', () => {
        const sm = new SessionManager('/path/to/session.json', { maxAge: 1000 });
        expect(sm.maxAge).toBe(1000);
      });

      it('should accept validateUrl option', () => {
        const sm = new SessionManager('/path/to/session.json', { validateUrl: 'https://example.com/validate' });
        expect(sm.validateUrl).toBe('https://example.com/validate');
      });
    });

    describe('load', () => {
      it('should return null if session file does not exist', async () => {
        const fs = await import('fs/promises');
        vi.mocked(fs.readFile).mockRejectedValue(new Error('ENOENT'));
        
        const sm = new SessionManager('/nonexistent/session.json');
        const result = await sm.load();
        
        expect(result).toBeNull();
      });

      it('should return parsed JSON if file exists', async () => {
        const fs = await import('fs/promises');
        const sessionData = { cookies: [{ name: 'test', value: 'val' }] };
        vi.mocked(fs.readFile).mockResolvedValue(JSON.stringify(sessionData));
        
        const sm = new SessionManager('/path/to/session.json');
        const result = await sm.load();
        
        expect(result).toEqual(sessionData);
      });

      it('should return null if JSON parse fails', async () => {
        const fs = await import('fs/promises');
        vi.mocked(fs.readFile).mockResolvedValue('invalid json');
        
        const sm = new SessionManager('/path/to/session.json');
        const result = await sm.load();
        
        expect(result).toBeNull();
      });
    });

    describe('save', () => {
      it('should save session with capturedAt timestamp', async () => {
        const fs = await import('fs/promises');
        const path = await import('path');
        let savedContent = null;
        vi.mocked(fs.mkdir).mockResolvedValue(undefined);
        vi.mocked(fs.writeFile).mockImplementation(async (file, content) => { savedContent = content; });
        vi.mocked(path.dirname).mockReturnValue('/path/to');
        
        const sm = new SessionManager('/path/to/session.json');
        await sm.save({ cookies: [] });
        
        const parsed = JSON.parse(savedContent);
        expect(parsed.capturedAt).toBeDefined();
        expect(new Date(parsed.capturedAt)).toBeInstanceOf(Date);
      });

      it('should create directory if it does not exist', async () => {
        const fs = await import('fs/promises');
        const path = await import('path');
        vi.mocked(fs.mkdir).mockResolvedValue(undefined);
        vi.mocked(fs.writeFile).mockResolvedValue(undefined);
        vi.mocked(path.dirname).mockReturnValue('/new/dir');
        
        const sm = new SessionManager('/new/dir/session.json');
        await sm.save({ cookies: [] });
        
        expect(fs.mkdir).toHaveBeenCalledWith('/new/dir', { recursive: true });
      });

      it('should format JSON with 2-space indentation', async () => {
        const fs = await import('fs/promises');
        const path = await import('path');
        let savedContent = null;
        vi.mocked(fs.mkdir).mockResolvedValue(undefined);
        vi.mocked(fs.writeFile).mockImplementation(async (file, content) => { savedContent = content; });
        vi.mocked(path.dirname).mockReturnValue('/path');
        
        const sm = new SessionManager('/path/session.json');
        await sm.save({ cookies: [] });
        
        expect(savedContent).toContain('  "cookies"');
      });
    });

    describe('isValid', () => {
      it('should return false if session is null', async () => {
        const sm = new SessionManager('/path/session.json');
        vi.spyOn(sm, 'load').mockResolvedValue(null);
        
        const result = await sm.isValid();
        expect(result).toBe(false);
      });

      it('should return false if capturedAt is missing', async () => {
        const sm = new SessionManager('/path/session.json');
        vi.spyOn(sm, 'load').mockResolvedValue({ cookies: [] });
        
        const result = await sm.isValid();
        expect(result).toBe(false);
      });

      it('should return false if session is too old', async () => {
        const sm = new SessionManager('/path/session.json', { maxAge: 100 });
        vi.spyOn(sm, 'load').mockResolvedValue({ cookies: [], capturedAt: new Date(Date.now() - 200).toISOString() });
        
        const result = await sm.isValid();
        expect(result).toBe(false);
      });

      it('should return true if session is fresh', async () => {
        const sm = new SessionManager('/path/session.json', { maxAge: 60000 });
        vi.spyOn(sm, 'load').mockResolvedValue({ cookies: [], capturedAt: new Date().toISOString() });
        
        const result = await sm.isValid();
        expect(result).toBe(true);
      });
    });

    describe('clear', () => {
      it('should delete session file', async () => {
        const fs = await import('fs/promises');
        vi.mocked(fs.unlink).mockResolvedValue(undefined);
        
        const sm = new SessionManager('/path/session.json');
        await sm.clear();
        
        expect(fs.unlink).toHaveBeenCalledWith('/path/session.json');
      });

      it('should not throw if file does not exist', async () => {
        const fs = await import('fs/promises');
        vi.mocked(fs.unlink).mockRejectedValue(new Error('ENOENT'));
        
        const sm = new SessionManager('/path/session.json');
        await expect(sm.clear()).resolves.toBeUndefined();
      });
    });
  });

  describe('RateLimiter class', () => {
    describe('constructor', () => {
      it('should initialize with default delays', () => {
        const rl = new RateLimiter();
        expect(rl.minDelay).toBe(1000);
        expect(rl.maxDelay).toBe(3000);
        expect(rl.lastRequestTime).toBe(0);
      });

      it('should accept custom delays', () => {
        const rl = new RateLimiter({ minDelay: 500, maxDelay: 1000 });
        expect(rl.minDelay).toBe(500);
        expect(rl.maxDelay).toBe(1000);
      });
    });

    describe('wait', () => {
      it('should update lastRequestTime after wait', async () => {
        const rl = new RateLimiter({ minDelay: 10, maxDelay: 20 });
        await rl.wait();
        expect(rl.lastRequestTime).toBeGreaterThan(0);
      });

      it('should not wait if enough time has passed', async () => {
        const rl = new RateLimiter({ minDelay: 50, maxDelay: 100 });
        rl.lastRequestTime = Date.now() - 200;
        
        const start = Date.now();
        await rl.wait();
        const elapsed = Date.now() - start;
        
        expect(elapsed).toBeLessThan(50);
      });
    });
  });

  describe('default export', () => {
    it('should export all classes', async () => {
      const module = await import('../../lib/anti-detection.js');
      expect(module.default.AntiDetection).toBe(antiDetection);
      expect(module.default.SessionManager).toBe(SessionManager);
      expect(module.default.RateLimiter).toBe(RateLimiter);
    });
  });
});