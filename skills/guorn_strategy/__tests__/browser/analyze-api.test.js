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

describe('analyze-api.js', () => {
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

  describe('analyzeGuornAPI', () => {
    it('should throw error when credentials missing', async () => {
      process.env.GUORN_USERNAME = undefined;
      process.env.GUORN_PASSWORD = undefined;
      
      const { analyzeGuornAPI } = await import('../../browser/analyze-api.js');
      
      await expect(analyzeGuornAPI()).rejects.toThrow('Missing GUORN_USERNAME or GUORN_PASSWORD');
    });

    it('should launch browser with correct options', async () => {
      const { analyzeGuornAPI } = await import('../../browser/analyze-api.js');
      const { chromium } = await import('playwright');
      
      await analyzeGuornAPI({ headed: false });
      
      expect(chromium.launch).toHaveBeenCalledWith({ headless: true });
    });

    it('should launch headed browser when headed option is true', async () => {
      const { analyzeGuornAPI } = await import('../../browser/analyze-api.js');
      const { chromium } = await import('playwright');
      
      await analyzeGuornAPI({ headed: true });
      
      expect(chromium.launch).toHaveBeenCalledWith({ headless: false });
    });

    it('should navigate to login page', async () => {
      const { analyzeGuornAPI } = await import('../../browser/analyze-api.js');
      
      await analyzeGuornAPI();
      
      expect(mockPage.goto).toHaveBeenCalledWith('https://guorn.com/user/login');
    });

    it('should fill login form', async () => {
      const { analyzeGuornAPI } = await import('../../browser/analyze-api.js');
      
      await analyzeGuornAPI();
      
      expect(mockPage.locator).toHaveBeenCalled();
    });

    it('should intercept network requests', async () => {
      const { analyzeGuornAPI } = await import('../../browser/analyze-api.js');
      
      await analyzeGuornAPI();
      
      expect(mockPage.on).toHaveBeenCalledWith('request', expect.any(Function));
      expect(mockPage.on).toHaveBeenCalledWith('response', expect.any(Function));
    });

    it('should save API calls to file', async () => {
      const { analyzeGuornAPI } = await import('../../browser/analyze-api.js');
      
      await analyzeGuornAPI();
      
      expect(fs.writeFileSync).toHaveBeenCalled();
    });

    it('should save session to file', async () => {
      const { analyzeGuornAPI } = await import('../../browser/analyze-api.js');
      
      await analyzeGuornAPI();
      
      expect(mockContext.cookies).toHaveBeenCalled();
      expect(fs.writeFileSync).toHaveBeenCalled();
    });

    it('should close browser after completion', async () => {
      const { analyzeGuornAPI } = await import('../../browser/analyze-api.js');
      
      await analyzeGuornAPI();
      
      expect(mockBrowser.close).toHaveBeenCalled();
    });

    it('should return apiCalls and sessionPayload', async () => {
      const { analyzeGuornAPI } = await import('../../browser/analyze-api.js');
      
      const result = await analyzeGuornAPI();
      
      expect(result.apiCalls).toBeDefined();
      expect(result.sessionPayload).toBeDefined();
    });

    it('should handle password login tab click', async () => {
      const mockTab = {
        isVisible: vi.fn().mockResolvedValue(true),
        click: vi.fn(),
      };
      
      mockPage.locator.mockReturnValue({
        filter: vi.fn().mockReturnValue({
          all: vi.fn().mockResolvedValue([mockTab])
        }),
      });
      
      const { analyzeGuornAPI } = await import('../../browser/analyze-api.js');
      
      await analyzeGuornAPI();
      
      expect(mockTab.click).toHaveBeenCalled();
    });

    it('should handle missing phone input selectors gracefully', async () => {
      mockPage.locator.mockReturnValue({
        filter: vi.fn().mockReturnValue({
          all: vi.fn().mockResolvedValue([])
        }),
      });
      
      vi.spyOn(mockPage, 'locator').mockImplementation((selector) => {
        if (selector === 'input[type="password"]:visible') {
          return {
            first: vi.fn().mockReturnValue({
              fill: vi.fn(),
            }),
          };
        }
        return {
          first: vi.fn().mockReturnValue({
            isVisible: vi.fn().mockRejectedValue(new Error('Not found')),
          }),
        };
      });
      
      const { analyzeGuornAPI } = await import('../../browser/analyze-api.js');
      
      await expect(analyzeGuornAPI()).rejects.toThrow('Could not find phone input field');
    });

    it('should find visible input selector', async () => {
      const mockInput = {
        isVisible: vi.fn().mockResolvedValue(true),
        fill: vi.fn(),
      };
      
      mockPage.locator.mockImplementation((selector) => {
        if (selector.includes('input')) {
          return { first: vi.fn().mockReturnValue(mockInput) };
        }
        return {
          filter: vi.fn().mockReturnValue({ all: vi.fn().mockResolvedValue([]) }),
        };
      });
      
      const { analyzeGuornAPI } = await import('../../browser/analyze-api.js');
      
      await analyzeGuornAPI();
      
      expect(mockInput.fill).toHaveBeenCalledWith('test_user');
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
      
      const { analyzeGuornAPI } = await import('../../browser/analyze-api.js');
      
      await analyzeGuornAPI();
      
      expect(mockButton.click).toHaveBeenCalled();
    });

    it('should navigate to strategy page after login', async () => {
      const { analyzeGuornAPI } = await import('../../browser/analyze-api.js');
      
      await analyzeGuornAPI();
      
      expect(mockPage.goto).toHaveBeenCalledWith('https://guorn.com/stock');
    });

    it('should filter out non-API requests', async () => {
      const apiCalls = [];
      
      mockPage.on.mockImplementation((event, handler) => {
        if (event === 'request') {
          handler({
            url: () => 'https://guorn.com/api/data',
            method: () => 'POST',
            headers: () => {},
            postData: () => '{}',
          });
          handler({
            url: () => 'https://guorn.com/static.css',
            method: () => 'GET',
            headers: () => {},
            postData: () => null,
          });
        }
      });
      
      const { analyzeGuornAPI } = await import('../../browser/analyze-api.js');
      
      const result = await analyzeGuornAPI();
      
      const apiRequest = result.apiCalls.find(c => c.url.includes('api/data'));
      const cssRequest = result.apiCalls.find(c => c.url.includes('.css'));
      
      expect(apiRequest).toBeDefined();
      expect(cssRequest).toBeUndefined();
    });
  });
});