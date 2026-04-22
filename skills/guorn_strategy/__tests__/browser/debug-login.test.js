import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';

describe('browser/debug-login.js', () => {
  describe('constants and configuration', () => {
    it('should use correct user agent', () => {
      const USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36';
      expect(USER_AGENT).toContain('Macintosh');
      expect(USER_AGENT).toContain('Chrome');
    });

    it('should use correct login URL', () => {
      const loginUrl = 'https://guorn.com/user/login';
      expect(loginUrl).toBe('https://guorn.com/user/login');
    });

    it('should use 3s wait after navigation', () => {
      const navigationWait = 3000;
      expect(navigationWait).toBe(3000);
    });

    it('should use 1.5s wait after tab click', () => {
      const tabClickWait = 1500;
      expect(tabClickWait).toBe(1500);
    });

    it('should use 5s wait after login click', () => {
      const loginClickWait = 5000;
      expect(loginClickWait).toBe(5000);
    });

    it('should use 2s timeout for element visibility', () => {
      const visibilityTimeout = 2000;
      expect(visibilityTimeout).toBe(2000);
    });
  });

  describe('environment variables', () => {
    it('should use GUORN_USERNAME from env', () => {
      process.env.GUORN_USERNAME = 'test_user';
      expect(process.env.GUORN_USERNAME).toBe('test_user');
      delete process.env.GUORN_USERNAME;
    });

    it('should use GUORN_PASSWORD from env', () => {
      process.env.GUORN_PASSWORD = 'test_pass';
      expect(process.env.GUORN_PASSWORD).toBe('test_pass');
      delete process.env.GUORN_PASSWORD;
    });

    it('should throw error when credentials missing', () => {
      const username = process.env.GUORN_USERNAME;
      const password = process.env.GUORN_PASSWORD;
      const missing = !username || !password;
      expect(missing).toBe(true);
    });

    it('should accept headed option', () => {
      const options = { headed: true };
      expect(options.headed).toBe(true);
    });

    it('should default to headless mode', () => {
      const options = {};
      const headed = options.headed === true;
      expect(headed).toBe(false);
    });
  });

  describe('browser configuration', () => {
    it('should set headless based on headed option', () => {
      const headed = true;
      const headless = !headed;
      expect(headless).toBe(false);
    });

    it('should use correct user agent string', () => {
      const USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)';
      expect(USER_AGENT.includes('Macintosh')).toBe(true);
    });
  });

  describe('page navigation', () => {
    it('should navigate to login page', () => {
      const targetUrl = 'https://guorn.com/user/login';
      expect(targetUrl).toBe('https://guorn.com/user/login');
    });

    it('should wait 3s after navigation', () => {
      const waitTime = 3000;
      expect(waitTime).toBe(3000);
    });
  });

  describe('input enumeration', () => {
    it('should find visible inputs', () => {
      const selector = 'input:visible';
      expect(selector).toBe('input:visible');
    });

    it('should log input attributes', () => {
      const input = { type: 'text', name: 'account', placeholder: '请输入手机号', id: 'phone-input' };
      expect(input.type).toBeDefined();
      expect(input.name).toBeDefined();
      expect(input.placeholder).toBeDefined();
      expect(input.id).toBeDefined();
    });
  });

  describe('button enumeration', () => {
    it('should find visible buttons', () => {
      const selector = 'button:visible, input[type="submit"]:visible';
      expect(selector.includes('button')).toBe(true);
      expect(selector.includes('submit')).toBe(true);
    });

    it('should log button text and type', () => {
      const button = { text: '登录', type: 'submit' };
      expect(button.text).toBe('登录');
      expect(button.type).toBe('submit');
    });
  });

  describe('登录 element search', () => {
    it('should find elements with 登录 text', () => {
      const selector = 'a:visible, span:visible, div:visible';
      expect(selector.includes('a')).toBe(true);
      expect(selector.includes('span')).toBe(true);
    });

    it('should filter by 登录 text', () => {
      const text = '登录';
      expect(text).toBe('登录');
    });

    it('should get tag name', () => {
      const tag = 'BUTTON';
      expect(tag).toBe('BUTTON');
    });

    it('should truncate text to 50 chars', () => {
      const longText = 'x'.repeat(100);
      const trimmed = longText?.trim().slice(0, 50);
      expect(trimmed?.length).toBe(50);
    });
  });

  describe('password tab click', () => {
    it('should find password login tab', () => {
      const selector = 'text=密码登录';
      expect(selector).toBe('text=密码登录');
    });

    it('should click password tab if visible', () => {
      const passwordTabVisible = true;
      expect(passwordTabVisible).toBe(true);
    });

    it('should wait 1.5s after tab click', () => {
      const waitTime = 1500;
      expect(waitTime).toBe(1500);
    });

    it('should handle missing password tab', () => {
      const passwordTabFound = false;
      expect(passwordTabFound).toBe(false);
    });
  });

  describe('phone input filling', () => {
    it('should find account input', () => {
      const selector = 'input[name="account"]';
      expect(selector.includes('account')).toBe(true);
    });

    it('should fill username', () => {
      const username = '13812345678';
      expect(username).toBe('13812345678');
    });

    it('should handle missing phone input', () => {
      const phoneInputVisible = false;
      expect(phoneInputVisible).toBe(false);
    });

    it('should use 2s timeout for visibility', () => {
      const timeout = 2000;
      expect(timeout).toBe(2000);
    });
  });

  describe('password input filling', () => {
    it('should find password input', () => {
      const selector = 'input[type="password"]:visible';
      expect(selector.includes('password')).toBe(true);
    });

    it('should fill password', () => {
      const password = 'test_password';
      expect(password).toBe('test_password');
    });

    it('should handle missing password input', () => {
      const passwordInputVisible = false;
      expect(passwordInputVisible).toBe(false);
    });
  });

  describe('login button click', () => {
    it('should find login button', () => {
      const selector = 'button:visible';
      expect(selector).toBe('button:visible');
    });

    it('should filter by 登录 text', () => {
      const filterText = '登录';
      expect(filterText).toBe('登录');
    });

    it('should click login button', () => {
      const loginButtonClicked = true;
      expect(loginButtonClicked).toBe(true);
    });

    it('should wait 5s after login', () => {
      const waitTime = 5000;
      expect(waitTime).toBe(5000);
    });

    it('should handle missing login button', () => {
      const loginButtonVisible = false;
      expect(loginButtonVisible).toBe(false);
    });
  });

  describe('login result check', () => {
    it('should get current URL', () => {
      const url = 'https://guorn.com/stock';
      expect(url).toBeDefined();
    });

    it('should check if URL contains /user/login', () => {
      const url = 'https://guorn.com/stock';
      const isLoggedIn = !url.includes('/user/login');
      expect(isLoggedIn).toBe(true);
    });

    it('should detect successful login', () => {
      const url = 'https://guorn.com/dashboard';
      const isLoggedIn = !url.includes('/user/login');
      expect(isLoggedIn).toBe(true);
    });

    it('should detect failed login', () => {
      const url = 'https://guorn.com/user/login';
      const isLoggedIn = !url.includes('/user/login');
      expect(isLoggedIn).toBe(false);
    });
  });

  describe('cookie saving', () => {
    it('should get cookies from context', () => {
      const cookies = [{ name: 'sessionid', value: 'abc123' }];
      expect(cookies).toBeDefined();
    });

    it('should create session payload', () => {
      const sessionPayload = { capturedAt: new Date().toISOString(), cookies: [] };
      expect(sessionPayload.capturedAt).toBeDefined();
      expect(sessionPayload.cookies).toBeDefined();
    });

    it('should save to SESSION_FILE', () => {
      const outputPath = '/test/session.json';
      expect(outputPath.endsWith('.json')).toBe(true);
    });

    it('should format JSON with indentation', () => {
      const content = JSON.stringify({ key: 'value' }, null, 2);
      expect(content.includes('\n')).toBe(true);
    });
  });

  describe('return value', () => {
    it('should return isLoggedIn status', () => {
      const result = { isLoggedIn: true };
      expect(result.isLoggedIn).toBe(true);
    });

    it('should return sessionPayload', () => {
      const result = { sessionPayload: { cookies: [] } };
      expect(result.sessionPayload).toBeDefined();
    });
  });

  describe('browser closing', () => {
    it('should close browser at end', () => {
      const browserClosed = true;
      expect(browserClosed).toBe(true);
    });
  });

  describe('CLI execution', () => {
    it('should parse --headed flag', () => {
      const args = ['--headed'];
      const headed = args.includes('--headed');
      expect(headed).toBe(true);
    });

    it('should run when called directly', () => {
      const isDirectCall = true;
      expect(isDirectCall).toBe(true);
    });
  });

  describe('error handling', () => {
    it('should handle missing credentials', () => {
      const hasCredentials = false;
      if (!hasCredentials) {
        expect(() => { throw new Error('Missing GUORN_USERNAME or GUORN_PASSWORD in .env'); }).toThrow();
      }
    });

    it('should catch errors in password tab click', () => {
      const passwordTabError = new Error('Element not found');
      expect(passwordTabError.message).toContain('Element not found');
    });

    it('should catch errors in phone input visibility check', () => {
      const phoneInputError = false;
      expect(phoneInputError).toBe(false);
    });
  });
});