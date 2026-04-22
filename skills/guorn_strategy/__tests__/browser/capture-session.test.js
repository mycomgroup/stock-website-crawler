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

describe('capture-session.js', () => {
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
        fill: vi.fn(),
        click: vi.fn(),
      }),
      url: vi.fn().mockReturnValue('https://guorn.com/stock'),
      screenshot: vi.fn(),
    };
    
    mockContext = {
      newPage: vi.fn(() => mockPage),
      cookies: vi.fn().mockResolvedValue([
        { name: '_xsrf', value: 'test_token' },
        { name: 'session', value: 'test_session' }
      ]),
    };
    
    mockBrowser = {
      newContext: vi.fn(() => mockContext),
      close: vi.fn(),
    };
    
    const { chromium } = await import('playwright');
    vi.mocked(chromium.launch).mockResolvedValue(mockBrowser);
    
    vi.mocked(fs.writeFileSync).mockImplementation(() => {});
    vi.mocked(fs.mkdirSync).mockImplementation(() => {});
    
    consoleLogSpy = vi.spyOn(console, 'log').mockImplementation(() => {});
    
    originalEnv = { ...process.env };
    process.env.GUORN_USERNAME = 'test_user';
    process.env.GUORN_PASSWORD = 'test_password';
  });

  afterEach(() => {
    consoleLogSpy.mockRestore();
    process.env = originalEnv;
  });

  describe('captureGuornSession', () => {
    it('should throw error when credentials missing', async () => {
      process.env.GUORN_USERNAME = undefined;
      process.env.GUORN_PASSWORD = undefined;
      
      const { captureGuornSession } = await import('../../browser/capture-session.js');
      
      await expect(captureGuornSession()).rejects.toThrow('Missing GUORN_USERNAME or GUORN_PASSWORD');
    });

    it('should launch browser with headless mode by default', async () => {
      const { captureGuornSession } = await import('../../browser/capture-session.js');
      const { chromium } = await import('playwright');
      
      await captureGuornSession();
      
      expect(chromium.launch).toHaveBeenCalledWith({ headless: true });
    });

    it('should launch headed browser when headed option is true', async () => {
      const { captureGuornSession } = await import('../../browser/capture-session.js');
      const { chromium } = await import('playwright');
      
      await captureGuornSession({ headed: true });
      
      expect(chromium.launch).toHaveBeenCalledWith({ headless: false });
    });

    it('should navigate to login page', async () => {
      const { captureGuornSession } = await import('../../browser/capture-session.js');
      
      await captureGuornSession();
      
      expect(mockPage.goto).toHaveBeenCalledWith('https://guorn.com/user/login');
    });

    it('should fill phone input', async () => {
      const { captureGuornSession } = await import('../../browser/capture-session.js');
      
      await captureGuornSession();
      
      expect(mockPage.locator).toHaveBeenCalledWith('#login-Id');
    });

    it('should fill password input', async () => {
      const { captureGuornSession } = await import('../../browser/capture-session.js');
      
      await captureGuornSession();
      
      expect(mockPage.locator).toHaveBeenCalledWith('#login-password');
    });

    it('should click login button', async () => {
      const { captureGuornSession } = await import('../../browser/capture-session.js');
      
      await captureGuornSession();
      
      expect(mockPage.locator).toHaveBeenCalledWith('button[type="submit"]:has-text("登录")');
    });

    it('should save session cookies when login successful', async () => {
      const { captureGuornSession } = await import('../../browser/capture-session.js');
      
      const result = await captureGuornSession();
      
      expect(fs.writeFileSync).toHaveBeenCalled();
      expect(result.cookies).toBeDefined();
    });

    it('should throw error when login fails', async () => {
      mockPage.url.mockReturnValue('https://guorn.com/user/login');
      
      const { captureGuornSession } = await import('../../browser/capture-session.js');
      
      await expect(captureGuornSession()).rejects.toThrow('Login failed');
    });

    it('should take screenshot when login fails', async () => {
      mockPage.url.mockReturnValue('https://guorn.com/user/login');
      
      const { captureGuornSession } = await import('../../browser/capture-session.js');
      
      try {
        await captureGuornSession();
      } catch (e) {
        expect(mockPage.screenshot).toHaveBeenCalled();
      }
    });

    it('should close browser when login fails', async () => {
      mockPage.url.mockReturnValue('https://guorn.com/user/login');
      
      const { captureGuornSession } = await import('../../browser/capture-session.js');
      
      try {
        await captureGuornSession();
      } catch (e) {
        expect(mockBrowser.close).toHaveBeenCalled();
      }
    });

    it('should close browser after successful login', async () => {
      const { captureGuornSession } = await import('../../browser/capture-session.js');
      
      await captureGuornSession();
      
      expect(mockBrowser.close).toHaveBeenCalled();
    });

    it('should return sessionPayload with capturedAt timestamp', async () => {
      const { captureGuornSession } = await import('../../browser/capture-session.js');
      
      const result = await captureGuornSession();
      
      expect(result.capturedAt).toBeDefined();
      expect(new Date(result.capturedAt)).toBeValidDate();
    });

    it('should return sessionPayload with cookies', async () => {
      const { captureGuornSession } = await import('../../browser/capture-session.js');
      
      const result = await captureGuornSession();
      
      expect(result.cookies).toEqual([
        { name: '_xsrf', value: 'test_token' },
        { name: 'session', value: 'test_session' }
      ]);
    });

    it('should log navigation message', async () => {
      const { captureGuornSession } = await import('../../browser/capture-session.js');
      
      await captureGuornSession();
      
      expect(consoleLogSpy).toHaveBeenCalledWith('Navigating to Guorn login page...');
    });

    it('should log login message', async () => {
      const { captureGuornSession } = await import('../../browser/capture-session.js');
      
      await captureGuornSession();
      
      expect(consoleLogSpy).toHaveBeenCalledWith('Logging in...');
    });

    it('should log current URL after login', async () => {
      const { captureGuornSession } = await import('../../browser/capture-session.js');
      
      await captureGuornSession();
      
      expect(consoleLogSpy).toHaveBeenCalledWith('Login attempted, current URL:', 'https://guorn.com/stock');
    });

    it('should log login success status', async () => {
      const { captureGuornSession } = await import('../../browser/capture-session.js');
      
      await captureGuornSession();
      
      expect(consoleLogSpy).toHaveBeenCalledWith('Login successful:', true);
    });

    it('should log session saved message', async () => {
      const { captureGuornSession } = await import('../../browser/capture-session.js');
      
      await captureGuornSession();
      
      expect(consoleLogSpy).toHaveBeenCalledWith(expect.stringContaining('Session saved to'));
    });

    it('should save session to SESSION_FILE path', async () => {
      const { captureGuornSession } = await import('../../browser/capture-session.js');
      
      await captureGuornSession();
      
      const calls = vi.mocked(fs.writeFileSync).mock.calls;
      expect(calls[0][0]).toContain('/test/sessions/guorn.json');
    });

    it('should format session JSON with proper indentation', async () => {
      const { captureGuornSession } = await import('../../browser/capture-session.js');
      
      await captureGuornSession();
      
      const calls = vi.mocked(fs.writeFileSync).mock.calls;
      const content = calls[0][1];
      expect(content).toContain('\n');
      expect(content).toContain('  ');
    });

    it('should wait for page load after navigation', async () => {
      const { captureGuornSession } = await import('../../browser/capture-session.js');
      
      await captureGuornSession();
      
      expect(mockPage.waitForTimeout).toHaveBeenCalledWith(3000);
    });

    it('should wait after login button click', async () => {
      const { captureGuornSession } = await import('../../browser/capture-session.js');
      
      await captureGuornSession();
      
      expect(mockPage.waitForTimeout).toHaveBeenCalledWith(5000);
    });
  });
});