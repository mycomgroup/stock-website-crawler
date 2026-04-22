import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import fs from 'node:fs';
import path from 'node:path';

vi.mock('node:fs');
vi.mock('node:path', () => ({
  default: {
    join: vi.fn((...args) => args.join('/')),
  },
  join: vi.fn((...args) => args.join('/')),
}));

vi.mock('playwright', () => ({
  chromium: {
    launch: vi.fn(),
  },
}));

vi.mock('../../paths.js', () => ({
  DATA_ROOT: '/test/data',
  SESSION_FILE: '/test/sessions/guorn.json',
}));

vi.mock('../../load-env.js', () => {});

describe('analyze-login.js', () => {
  let mockBrowser;
  let mockContext;
  let mockPage;
  let consoleLogSpy;
  let originalEnv;

  beforeEach(async () => {
    vi.resetModules();
    vi.clearAllMocks();
    
    mockPage = {
      goto: vi.fn(),
      waitForTimeout: vi.fn(),
      locator: vi.fn().mockReturnValue({
        filter: vi.fn().mockReturnValue({
          all: vi.fn().mockResolvedValue([])
        }),
        first: vi.fn().mockReturnValue({
          isVisible: vi.fn().mockResolvedValue(true),
          fill: vi.fn(),
          click: vi.fn(),
        }),
      }),
      url: vi.fn().mockReturnValue('https://guorn.com/stock'),
      on: vi.fn(),
    };
    
    mockContext = {
      newPage: vi.fn(() => mockPage),
      cookies: vi.fn().mockResolvedValue([]),
    };
    
    mockBrowser = {
      newContext: vi.fn(() => mockContext),
      close: vi.fn(),
    };
    
    const { chromium } = await import('playwright');
    vi.mocked(chromium.launch).mockResolvedValue(mockBrowser);
    
    vi.mocked(fs.mkdirSync).mockImplementation(() => {});
    vi.mocked(fs.writeFileSync).mockImplementation(() => {});
    
    consoleLogSpy = vi.spyOn(console, 'log').mockImplementation(() => {});
    
    originalEnv = { ...process.env };
    process.env.GUORN_USERNAME = 'test_user';
    process.env.GUORN_PASSWORD = 'test_password';
  });

  afterEach(() => {
    consoleLogSpy.mockRestore();
    process.env = originalEnv;
  });

  describe('analyzeGuornLoginAPI', () => {
    it('should throw error when credentials missing', async () => {
      process.env.GUORN_USERNAME = undefined;
      process.env.GUORN_PASSWORD = undefined;
      
      const { analyzeGuornLoginAPI } = await import('../../browser/analyze-login.js');
      
      await expect(analyzeGuornLoginAPI()).rejects.toThrow('Missing GUORN_USERNAME or GUORN_PASSWORD');
    });

    it('should launch browser with headless mode', async () => {
      const { analyzeGuornLoginAPI } = await import('../../browser/analyze-login.js');
      const { chromium } = await import('playwright');
      
      await analyzeGuornLoginAPI({ headed: false });
      
      expect(chromium.launch).toHaveBeenCalledWith({ headless: true });
    });

    it('should launch headed browser when headed is true', async () => {
      const { analyzeGuornLoginAPI } = await import('../../browser/analyze-login.js');
      const { chromium } = await import('playwright');
      
      await analyzeGuornLoginAPI({ headed: true });
      
      expect(chromium.launch).toHaveBeenCalledWith({ headless: false });
    });

    it('should navigate to login page', async () => {
      const { analyzeGuornLoginAPI } = await import('../../browser/analyze-login.js');
      
      await analyzeGuornLoginAPI();
      
      expect(mockPage.goto).toHaveBeenCalledWith('https://guorn.com/user/login');
    });

    it('should intercept request events', async () => {
      const { analyzeGuornLoginAPI } = await import('../../browser/analyze-login.js');
      
      await analyzeGuornLoginAPI();
      
      expect(mockPage.on).toHaveBeenCalledWith('request', expect.any(Function));
    });

    it('should intercept response events', async () => {
      const { analyzeGuornLoginAPI } = await import('../../browser/analyze-login.js');
      
      await analyzeGuornLoginAPI();
      
      expect(mockPage.on).toHaveBeenCalledWith('response', expect.any(Function));
    });

    it('should filter out static assets', async () => {
      const apiCalls = [];
      
      mockPage.on.mockImplementation((event, handler) => {
        if (event === 'request') {
          handler({
            url: () => 'https://guorn.com/user/login',
            method: () => 'POST',
            headers: () => {},
            postData: () => '{}',
          });
          handler({
            url: () => 'https://guorn.com/static.js',
            method: () => 'GET',
            headers: () => {},
            postData: () => null,
          });
          handler({
            url: () => 'https://guorn.com/fonts.woff2',
            method: () => 'GET',
            headers: () => {},
            postData: () => null,
          });
          handler({
            url: () => 'https://google-analytics.com/collect',
            method: () => 'POST',
            headers: () => {},
            postData: () => '{}',
          });
        }
      });
      
      const { analyzeGuornLoginAPI } = await import('../../browser/analyze-login.js');
      
      const result = await analyzeGuornLoginAPI();
      
      expect(result.apiCalls.find(c => c.url.includes('user/login'))).toBeDefined();
      expect(result.apiCalls.find(c => c.url.includes('.js'))).toBeUndefined();
      expect(result.apiCalls.find(c => c.url.includes('.woff2'))).toBeUndefined();
      expect(result.apiCalls.find(c => c.url.includes('google-analytics'))).toBeUndefined();
    });

    it('should capture response body for login API', async () => {
      const apiCalls = [];
      let responseHandler;
      
      mockPage.on.mockImplementation((event, handler) => {
        if (event === 'request') {
          handler({
            url: () => 'https://guorn.com/user/login',
            method: () => 'POST',
            headers: () => {},
            postData: () => '{"account":"test"}',
          });
          apiCalls.push({
            type: 'request',
            url: 'https://guorn.com/user/login',
            method: 'POST',
          });
        }
        if (event === 'response') {
          responseHandler = handler;
        }
      });
      
      const mockResponse = {
        url: () => 'https://guorn.com/user/login',
        request: () => ({ method: () => 'POST' }),
        text: vi.fn().mockResolvedValue('{"status":"ok"}'),
      };
      
      const { analyzeGuornLoginAPI } = await import('../../browser/analyze-login.js');
      
      const resultPromise = analyzeGuornLoginAPI();
      
      if (responseHandler) {
        responseHandler(mockResponse);
      }
      
      const result = await resultPromise;
      
      expect(mockResponse.text).toHaveBeenCalled();
    });

    it('should handle password login tab', async () => {
      const mockTab = {
        isVisible: vi.fn().mockResolvedValue(true),
        click: vi.fn(),
      };
      
      mockPage.locator.mockReturnValue({
        filter: vi.fn().mockReturnValue({
          all: vi.fn().mockResolvedValue([mockTab])
        }),
      });
      
      const { analyzeGuornLoginAPI } = await import('../../browser/analyze-login.js');
      
      await analyzeGuornLoginAPI();
      
      expect(mockTab.click).toHaveBeenCalled();
    });

    it('should handle missing phone input field', async () => {
      mockPage.locator.mockImplementation((selector) => {
        if (selector.includes('input')) {
          return {
            first: vi.fn().mockReturnValue({
              isVisible: vi.fn().mockRejectedValue(new Error('Not found')),
            }),
          };
        }
        return {
          filter: vi.fn().mockReturnValue({ all: vi.fn().mockResolvedValue([]) }),
        };
      });
      
      const { analyzeGuornLoginAPI } = await import('../../browser/analyze-login.js');
      
      await expect(analyzeGuornLoginAPI()).rejects.toThrow('Could not find phone input field');
    });

    it('should fill phone input with username', async () => {
      const mockInput = {
        isVisible: vi.fn().mockResolvedValue(true),
        fill: vi.fn(),
      };
      
      mockPage.locator.mockImplementation((selector) => {
        if (selector.includes('input') && !selector.includes('password')) {
          return { first: vi.fn().mockReturnValue(mockInput) };
        }
        return {
          filter: vi.fn().mockReturnValue({ all: vi.fn().mockResolvedValue([]) }),
          first: vi.fn().mockReturnValue({
            isVisible: vi.fn().mockResolvedValue(true),
            fill: vi.fn(),
          }),
        };
      });
      
      const { analyzeGuornLoginAPI } = await import('../../browser/analyze-login.js');
      
      await analyzeGuornLoginAPI();
      
      expect(mockInput.fill).toHaveBeenCalledWith('test_user');
    });

    it('should fill password input', async () => {
      const mockPasswordInput = {
        fill: vi.fn(),
      };
      
      mockPage.locator.mockImplementation((selector) => {
        if (selector.includes('password')) {
          return { first: vi.fn().mockReturnValue(mockPasswordInput) };
        }
        return {
          filter: vi.fn().mockReturnValue({ all: vi.fn().mockResolvedValue([]) }),
          first: vi.fn().mockReturnValue({
            isVisible: vi.fn().mockResolvedValue(true),
            fill: vi.fn(),
          }),
        };
      });
      
      const { analyzeGuornLoginAPI } = await import('../../browser/analyze-login.js');
      
      await analyzeGuornLoginAPI();
      
      expect(mockPasswordInput.fill).toHaveBeenCalledWith('test_password');
    });

    it('should click login button', async () => {
      const mockButton = {
        click: vi.fn(),
      };
      
      mockPage.locator.mockImplementation((selector) => {
        if (selector.includes('button') || selector.includes('submit')) {
          return { first: vi.fn().mockReturnValue(mockButton) };
        }
        return {
          filter: vi.fn().mockReturnValue({ all: vi.fn().mockResolvedValue([]) }),
          first: vi.fn().mockReturnValue({
            isVisible: vi.fn().mockResolvedValue(true),
            fill: vi.fn(),
          }),
        };
      });
      
      const { analyzeGuornLoginAPI } = await import('../../browser/analyze-login.js');
      
      await analyzeGuornLoginAPI();
      
      expect(mockButton.click).toHaveBeenCalled();
    });

    it('should save API calls to login-api-calls.json', async () => {
      const { analyzeGuornLoginAPI } = await import('../../browser/analyze-login.js');
      
      await analyzeGuornLoginAPI();
      
      expect(fs.writeFileSync).toHaveBeenCalled();
      const calls = vi.mocked(fs.writeFileSync).mock.calls;
      const apiCallsCall = calls.find(c => c[0].includes('login-api-calls.json'));
      expect(apiCallsCall).toBeDefined();
    });

    it('should save session cookies', async () => {
      const { analyzeGuornLoginAPI } = await import('../../browser/analyze-login.js');
      
      await analyzeGuornLoginAPI();
      
      expect(mockContext.cookies).toHaveBeenCalled();
      expect(fs.writeFileSync).toHaveBeenCalled();
    });

    it('should close browser', async () => {
      const { analyzeGuornLoginAPI } = await import('../../browser/analyze-login.js');
      
      await analyzeGuornLoginAPI();
      
      expect(mockBrowser.close).toHaveBeenCalled();
    });

    it('should return isLoggedIn status', async () => {
      mockPage.url.mockReturnValue('https://guorn.com/dashboard');
      
      const { analyzeGuornLoginAPI } = await import('../../browser/analyze-login.js');
      
      const result = await analyzeGuornLoginAPI();
      
      expect(result.isLoggedIn).toBe(true);
    });

    it('should return isLoggedIn false when still on login page', async () => {
      mockPage.url.mockReturnValue('https://guorn.com/user/login');
      
      const { analyzeGuornLoginAPI } = await import('../../browser/analyze-login.js');
      
      const result = await analyzeGuornLoginAPI();
      
      expect(result.isLoggedIn).toBe(false);
    });

    it('should log login success status', async () => {
      mockPage.url.mockReturnValue('https://guorn.com/stock');
      
      const { analyzeGuornLoginAPI } = await import('../../browser/analyze-login.js');
      
      await analyzeGuornLoginAPI();
      
      expect(consoleLogSpy).toHaveBeenCalledWith('Login successful:', true);
    });
  });
});