import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';

vi.mock('playwright', () => ({
  chromium: {
    launch: vi.fn(),
  },
}));

vi.mock('../paths.js', () => ({
  SESSION_FILE: '/test/sessions/thsquant.json',
  OUTPUT_ROOT: '/test/output',
}));

import { chromium } from 'playwright';

const { captureTHSQuantSession } = await import('../browser/capture-session.js');

describe('capture-session.js', () => {
  let mockBrowser;
  let mockContext;
  let mockPage;
  let consoleLogSpy;
  let consoleErrorSpy;

  beforeEach(() => {
    vi.clearAllMocks();
    
    mockPage = {
      goto: vi.fn().mockResolvedValue(undefined),
      url: vi.fn().mockReturnValue('https://quant.10jqka.com.cn/view/study-index.html'),
      waitForTimeout: vi.fn().mockResolvedValue(undefined),
      waitForSelector: vi.fn().mockResolvedValue(undefined),
      $: vi.fn().mockResolvedValue(null),
      keyboard: {
        press: vi.fn().mockResolvedValue(undefined),
      },
      waitForNavigation: vi.fn().mockResolvedValue(undefined),
    };

    mockContext = {
      newPage: vi.fn().mockResolvedValue(mockPage),
      cookies: vi.fn().mockResolvedValue([{ name: 'sid', value: 'test123' }]),
    };

    mockBrowser = {
      newContext: vi.fn().mockResolvedValue(mockContext),
      close: vi.fn().mockResolvedValue(undefined),
    };

    vi.mocked(chromium.launch).mockResolvedValue(mockBrowser);

    consoleLogSpy = vi.spyOn(console, 'log').mockImplementation(() => {});
    consoleErrorSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
  });

  afterEach(() => {
    consoleLogSpy.mockRestore();
    consoleErrorSpy.mockRestore();
  });

  describe('captureTHSQuantSession', () => {
    it('should launch browser in headless mode by default', async () => {
      mockPage.url.mockReturnValue('https://quant.10jqka.com.cn/view/dashboard');

      await captureTHSQuantSession({ username: 'user', password: 'pass' });

      expect(chromium.launch).toHaveBeenCalledWith({
        headless: true,
        args: ['--disable-blink-features=AutomationControlled'],
      });
    });

    it('should launch browser in headed mode when specified', async () => {
      mockPage.url.mockReturnValue('https://quant.10jqka.com.cn/view/dashboard');

      await captureTHSQuantSession({ username: 'user', password: 'pass' }, { headed: true });

      expect(chromium.launch).toHaveBeenCalledWith({
        headless: false,
        args: ['--disable-blink-features=AutomationControlled'],
      });
    });

    it('should navigate to the login page', async () => {
      mockPage.url.mockReturnValue('https://quant.10jqka.com.cn/view/dashboard');

      await captureTHSQuantSession({ username: 'user', password: 'pass' });

      expect(mockPage.goto).toHaveBeenCalledWith(
        'https://quant.10jqka.com.cn/view/study-index.html',
        {
          waitUntil: 'networkidle',
          timeout: 30000,
        }
      );
    });

    it('should capture session when already logged in', async () => {
      mockPage.url.mockReturnValue('https://quant.10jqka.com.cn/view/dashboard');
      mockContext.cookies.mockResolvedValue([
        { name: 'sid', value: 'session_id' },
        { name: 'token', value: 'auth_token' },
      ]);

      const result = await captureTHSQuantSession({ username: 'user', password: 'pass' });

      expect(result).toEqual({
        cookies: [
          { name: 'sid', value: 'session_id' },
          { name: 'token', value: 'auth_token' },
        ],
        timestamp: expect.any(Number),
        url: 'https://quant.10jqka.com.cn/view/dashboard',
      });
      expect(mockBrowser.close).toHaveBeenCalled();
    });

    it('should detect login page and attempt login', async () => {
      mockPage.url
        .mockReturnValueOnce('https://quant.10jqka.com.cn/view/login')
        .mockReturnValueOnce('https://quant.10jqka.com.cn/view/login')
        .mockReturnValueOnce('https://quant.10jqka.com.cn/view/dashboard');

      const mockUsernameInput = {
        fill: vi.fn().mockResolvedValue(undefined),
      };
      const mockPasswordInput = {
        fill: vi.fn().mockResolvedValue(undefined),
      };
      const mockLoginButton = {
        click: vi.fn().mockResolvedValue(undefined),
      };

      mockPage.$.mockImplementation((selector) => {
        if (selector.includes('text') || selector.includes('username') || selector.includes('phone')) {
          return Promise.resolve(mockUsernameInput);
        }
        if (selector.includes('password')) {
          return Promise.resolve(mockPasswordInput);
        }
        if (selector.includes('submit') || selector.includes('login')) {
          return Promise.resolve(mockLoginButton);
        }
        return Promise.resolve(null);
      });

      mockContext.cookies.mockResolvedValue([{ name: 'sid', value: 'new_session' }]);

      const result = await captureTHSQuantSession(
        { username: 'testuser', password: 'testpass' },
        { headed: false }
      );

      expect(mockUsernameInput.fill).toHaveBeenCalledWith('testuser');
      expect(mockPasswordInput.fill).toHaveBeenCalledWith('testpass');
      expect(mockLoginButton.click).toHaveBeenCalled();
      expect(result.cookies).toEqual([{ name: 'sid', value: 'new_session' }]);
    });

    it('should press Enter if no login button found', async () => {
      mockPage.url.mockReturnValue('https://quant.10jqka.com.cn/view/login');

      const mockUsernameInput = {
        fill: vi.fn().mockResolvedValue(undefined),
      };
      const mockPasswordInput = {
        fill: vi.fn().mockResolvedValue(undefined),
      };

      let selectorCallCount = 0;
      mockPage.$.mockImplementation((selector) => {
        selectorCallCount++;
        if (selector.includes('text') || selector.includes('username') || selector.includes('phone')) {
          return Promise.resolve(mockUsernameInput);
        }
        if (selector.includes('password')) {
          return Promise.resolve(mockPasswordInput);
        }
        return Promise.resolve(null);
      });

      mockContext.cookies.mockResolvedValue([{ name: 'sid', value: 'session' }]);

      await captureTHSQuantSession({ username: 'user', password: 'pass' });

      expect(mockPage.keyboard.press).toHaveBeenCalledWith('Enter');
    });

    it('should handle navigation timeout gracefully', async () => {
      mockPage.url.mockReturnValue('https://quant.10jqka.com.cn/view/login');
      mockPage.waitForNavigation.mockRejectedValue(new Error('Navigation timeout'));

      const mockUsernameInput = {
        fill: vi.fn().mockResolvedValue(undefined),
      };
      const mockPasswordInput = {
        fill: vi.fn().mockResolvedValue(undefined),
      };

      mockPage.$.mockImplementation((selector) => {
        if (selector.includes('text') || selector.includes('username') || selector.includes('phone')) {
          return Promise.resolve(mockUsernameInput);
        }
        if (selector.includes('password')) {
          return Promise.resolve(mockPasswordInput);
        }
        return Promise.resolve(null);
      });

      mockContext.cookies.mockResolvedValue([{ name: 'sid', value: 'session' }]);

      const result = await captureTHSQuantSession({ username: 'user', password: 'pass' });

      expect(result).toHaveProperty('cookies');
      expect(mockBrowser.close).toHaveBeenCalled();
    });

    it('should handle waitForSelector timeout gracefully', async () => {
      mockPage.url.mockReturnValue('https://quant.10jqka.com.cn/view/login');
      mockPage.waitForSelector.mockRejectedValue(new Error('Selector timeout'));

      mockContext.cookies.mockResolvedValue([{ name: 'sid', value: 'session' }]);

      const result = await captureTHSQuantSession({ username: 'user', password: 'pass' });

      expect(result).toHaveProperty('cookies');
    });

    it('should throw error when navigation fails', async () => {
      mockPage.goto.mockRejectedValue(new Error('Network error'));

      await expect(
        captureTHSQuantSession({ username: 'user', password: 'pass' })
      ).rejects.toThrow('Network error');

      expect(mockBrowser.close).toHaveBeenCalled();
    });

    it('should create context with correct viewport', async () => {
      mockPage.url.mockReturnValue('https://quant.10jqka.com.cn/view/dashboard');

      await captureTHSQuantSession({ username: 'user', password: 'pass' });

      expect(mockBrowser.newContext).toHaveBeenCalledWith({
        viewport: { width: 1280, height: 800 },
        userAgent: expect.stringContaining('Mozilla'),
      });
    });

    it('should handle browser close on error', async () => {
      mockPage.goto.mockRejectedValue(new Error('Failed'));

      await expect(
        captureTHSQuantSession({ username: 'user', password: 'pass' })
      ).rejects.toThrow('Failed');

      expect(mockBrowser.close).toHaveBeenCalled();
    });

    it('should detect signin in URL as login page', async () => {
      mockPage.url.mockReturnValue('https://quant.10jqka.com.cn/view/signin');

      const mockUsernameInput = { fill: vi.fn().mockResolvedValue(undefined) };
      const mockPasswordInput = { fill: vi.fn().mockResolvedValue(undefined) };

      mockPage.$.mockImplementation((selector) => {
        if (selector.includes('text') || selector.includes('username') || selector.includes('phone')) {
          return Promise.resolve(mockUsernameInput);
        }
        if (selector.includes('password')) {
          return Promise.resolve(mockPasswordInput);
        }
        return Promise.resolve(null);
      });

      mockContext.cookies.mockResolvedValue([{ name: 'sid', value: 'session' }]);

      const result = await captureTHSQuantSession({ username: 'user', password: 'pass' });

      expect(consoleLogSpy).toHaveBeenCalledWith('Need to login...');
    });

    it('should handle missing username input gracefully', async () => {
      mockPage.url.mockReturnValue('https://quant.10jqka.com.cn/view/login');

      mockPage.$.mockImplementation((selector) => {
        if (selector.includes('password')) {
          return Promise.resolve({ fill: vi.fn().mockResolvedValue(undefined) });
        }
        return Promise.resolve(null);
      });

      mockContext.cookies.mockResolvedValue([{ name: 'sid', value: 'session' }]);

      const result = await captureTHSQuantSession({ username: 'user', password: 'pass' });

      expect(result).toHaveProperty('cookies');
    });

    it('should handle missing password input gracefully', async () => {
      mockPage.url.mockReturnValue('https://quant.10jqka.com.cn/view/login');

      mockPage.$.mockImplementation((selector) => {
        if (selector.includes('text') || selector.includes('username') || selector.includes('phone')) {
          return Promise.resolve({ fill: vi.fn().mockResolvedValue(undefined) });
        }
        return Promise.resolve(null);
      });

      mockContext.cookies.mockResolvedValue([{ name: 'sid', value: 'session' }]);

      const result = await captureTHSQuantSession({ username: 'user', password: 'pass' });

      expect(result).toHaveProperty('cookies');
    });

    it('should log error message on failure', async () => {
      mockPage.goto.mockRejectedValue(new Error('Navigation failed'));

      await expect(
        captureTHSQuantSession({ username: 'user', password: 'pass' })
      ).rejects.toThrow('Navigation failed');

      expect(consoleErrorSpy).toHaveBeenCalledWith('Error during login:', 'Navigation failed');
    });

    it('should include timestamp in session data', async () => {
      mockPage.url.mockReturnValue('https://quant.10jqka.com.cn/view/dashboard');
      mockContext.cookies.mockResolvedValue([{ name: 'sid', value: 'test' }]);

      const beforeTime = Date.now();
      const result = await captureTHSQuantSession({ username: 'user', password: 'pass' });
      const afterTime = Date.now();

      expect(result.timestamp).toBeGreaterThanOrEqual(beforeTime);
      expect(result.timestamp).toBeLessThanOrEqual(afterTime);
    });

    it('should capture all cookies from context', async () => {
      mockPage.url.mockReturnValue('https://quant.10jqka.com.cn/view/dashboard');
      const allCookies = [
        { name: 'sid', value: 'session_id' },
        { name: 'token', value: 'token_value' },
        { name: 'ths_user', value: 'user_info' },
      ];
      mockContext.cookies.mockResolvedValue(allCookies);

      const result = await captureTHSQuantSession({ username: 'user', password: 'pass' });

      expect(result.cookies).toEqual(allCookies);
    });
  });
});