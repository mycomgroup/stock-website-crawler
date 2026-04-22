import { describe, it, beforeEach, afterEach, mock } from 'node:test';
import assert from 'node:assert';
import defaultExport from '../sites/bigquant.js';

const createMockPage = () => ({
  $: mock.fn(),
  locator: mock.fn(() => ({
    count: mock.fn(),
    click: mock.fn(),
    fill: mock.fn()
  })),
  waitForTimeout: mock.fn(),
  keyboard: { press: mock.fn() },
  url: mock.fn(() => 'https://bigquant.com/')
});

const createMockResponse = (data, options = {}) => ({
  ok: options.ok ?? true,
  status: options.status ?? 200,
  json: mock.fn(async () => data),
  text: mock.fn(async () => JSON.stringify(data))
});

describe('bigquant site adapter', () => {
  let originalFetch;

  beforeEach(() => {
    originalFetch = global.fetch;
  });

  afterEach(() => {
    global.fetch = originalFetch;
  });

  describe('basic properties', () => {
    it('should have correct id', () => {
      assert.strictEqual(defaultExport.id, 'bigquant');
    });

    it('should have correct name', () => {
      assert.strictEqual(defaultExport.name, 'BigQuant');
    });

    it('should have correct domain', () => {
      assert.strictEqual(defaultExport.domain, '.bigquant.com');
    });

    it('should have correct loginUrl', () => {
      assert.strictEqual(defaultExport.loginUrl, 'https://bigquant.com');
    });

    it('should have correct dashboardUrl', () => {
      assert.strictEqual(defaultExport.dashboardUrl, 'https://bigquant.com/');
    });
  });

  describe('verifySession', () => {
    it('should return success when API returns valid user data with username', async () => {
      global.fetch = mock.fn(async () => createMockResponse({
        code: 0,
        data: { username: 'testuser', id: 123 }
      }));

      const result = await defaultExport.verifySession([{ name: 'session', value: 'abc123' }]);

      assert.strictEqual(result.success, true);
      assert.strictEqual(result.user, 'testuser');
    });

    it('should return success when API returns valid user data with id only', async () => {
      global.fetch = mock.fn(async () => createMockResponse({
        code: 0,
        data: { id: 456 }
      }));

      const result = await defaultExport.verifySession([{ name: 'session', value: 'abc123' }]);

      assert.strictEqual(result.success, true);
      assert.strictEqual(result.user, 456);
    });

    it('should return failure when code is not 0', async () => {
      global.fetch = mock.fn(async () => createMockResponse({
        code: 1,
        message: 'Unauthorized'
      }));

      const result = await defaultExport.verifySession([{ name: 'session', value: 'abc123' }]);

      assert.strictEqual(result.success, false);
      assert.strictEqual(result.message, 'Unauthorized');
    });

    it('should return failure when data is missing', async () => {
      global.fetch = mock.fn(async () => createMockResponse({
        code: 0
      }));

      const result = await defaultExport.verifySession([{ name: 'session', value: 'abc123' }]);

      assert.strictEqual(result.success, false);
      assert.strictEqual(result.message, '未登录');
    });

    it('should return failure when HTTP status is not ok', async () => {
      global.fetch = mock.fn(async () => createMockResponse({}, { ok: false, status: 401 }));

      const result = await defaultExport.verifySession([{ name: 'session', value: 'abc123' }]);

      assert.strictEqual(result.success, false);
      assert.strictEqual(result.message, 'HTTP 401');
    });

    it('should handle network errors', async () => {
      global.fetch = mock.fn(async () => { throw new Error('Network error'); });

      const result = await defaultExport.verifySession([{ name: 'session', value: 'abc123' }]);

      assert.strictEqual(result.success, false);
      assert.strictEqual(result.message, 'Network error');
    });

    it('should send correct headers', async () => {
      let capturedHeaders;
      global.fetch = mock.fn(async (url, options) => {
        capturedHeaders = options.headers;
        return createMockResponse({ code: 0, data: { username: 'test' } });
      });

      await defaultExport.verifySession([
        { name: 'session', value: 'abc' },
        { name: 'token', value: 'def' }
      ]);

      assert.strictEqual(capturedHeaders.Cookie, 'session=abc; token=def');
      assert.ok(capturedHeaders['User-Agent'].includes('Mozilla'));
    });
  });

  describe('checkLoggedIn', () => {
    it('should return true when user avatar is present', async () => {
      const mockPage = createMockPage();
      mockPage.$ = mock.fn(async (selector) => {
        if (selector.includes('avatar')) return {};
        return null;
      });

      const result = await defaultExport.checkLoggedIn(mockPage);

      assert.strictEqual(result, true);
    });

    it('should return false when login button is present and no user indicator', async () => {
      const mockPage = createMockPage();
      mockPage.$ = mock.fn(async (selector) => {
        if (selector.includes('登录')) return {};
        return null;
      });

      const result = await defaultExport.checkLoggedIn(mockPage);

      assert.strictEqual(result, false);
    });

    it('should return true when no login button and no user indicator but URL is not login page', async () => {
      const mockPage = createMockPage();
      mockPage.$ = mock.fn(async () => null);
      mockPage.url = mock.fn(() => 'https://bigquant.com/dashboard');

      const result = await defaultExport.checkLoggedIn(mockPage);

      assert.strictEqual(result, true);
    });

    it('should return false when URL contains /login', async () => {
      const mockPage = createMockPage();
      mockPage.$ = mock.fn(async () => { throw new Error('Element not found'); });
      mockPage.url = mock.fn(() => 'https://bigquant.com/login');

      const result = await defaultExport.checkLoggedIn(mockPage);

      assert.strictEqual(result, false);
    });
  });

  describe('automatedLogin', () => {
    it('should throw error when credentials are missing', async () => {
      const mockPage = createMockPage();

      await assert.rejects(
        defaultExport.automatedLogin(mockPage, {}),
        { message: '未发现 BigQuant 账号凭证' }
      );
    });

    it('should throw error when only username is provided', async () => {
      const mockPage = createMockPage();

      await assert.rejects(
        defaultExport.automatedLogin(mockPage, { BIGQUANT_USERNAME: 'user' }),
        { message: '未发现 BigQuant 账号凭证' }
      );
    });

    it('should throw error when login button not found', async () => {
      const mockPage = createMockPage();
      mockPage.locator = mock.fn(() => ({
        count: mock.fn(async () => 0),
        click: mock.fn(),
        fill: mock.fn()
      }));

      await assert.rejects(
        defaultExport.automatedLogin(mockPage, {
          BIGQUANT_USERNAME: 'user',
          BIGQUANT_PASSWORD: 'pass'
        }),
        { message: '未找到登录按钮' }
      );
    });

    it('should throw error when password tab not found', async () => {
      const mockPage = createMockPage();
      const mockLoginBtn = { count: mock.fn(async () => 1), click: mock.fn() };
      const mockPasswordTab = { count: mock.fn(async () => 0), click: mock.fn() };

      mockPage.locator = mock.fn((selector) => {
        if (selector.includes('登录')) return mockLoginBtn;
        if (selector.includes('密码登录')) return mockPasswordTab;
        return { count: mock.fn(async () => 0) };
      });

      await assert.rejects(
        defaultExport.automatedLogin(mockPage, {
          BIGQUANT_USERNAME: 'user',
          BIGQUANT_PASSWORD: 'pass'
        }),
        { message: '未找到密码登录选项' }
      );
    });

    it('should throw error when input fields not found', async () => {
      const mockPage = createMockPage();
      const mockBtn = { count: mock.fn(async () => 1), click: mock.fn() };
      const mockInput = { count: mock.fn(async () => 0), click: mock.fn(), fill: mock.fn() };

      mockPage.locator = mock.fn(() => mockBtn);
      mockPage.$ = mock.fn(async () => null);

      await assert.rejects(
        defaultExport.automatedLogin(mockPage, {
          BIGQUANT_USERNAME: 'user',
          BIGQUANT_PASSWORD: 'pass'
        }),
        { message: '未找到用户名或密码输入框' }
      );
    });

    it('should use alternative credential keys', async () => {
      const mockPage = createMockPage();
      let filledUsername;
      let filledPassword;

      const mockLoginBtn = { count: mock.fn(async () => 1), click: mock.fn() };
      const mockPasswordTab = { count: mock.fn(async () => 1), click: mock.fn() };
      const mockUsernameInput = {
        count: mock.fn(async () => 1),
        click: mock.fn(),
        fill: mock.fn(async (v) => { filledUsername = v; })
      };
      const mockPasswordInput = {
        count: mock.fn(async () => 1),
        click: mock.fn(),
        fill: mock.fn(async (v) => { filledPassword = v; })
      };

      mockPage.locator = mock.fn((selector) => {
        if (selector.includes('登录') && !selector.includes('密码')) return mockLoginBtn;
        if (selector.includes('密码登录')) return mockPasswordTab;
        if (selector.includes('用户名')) return mockUsernameInput;
        if (selector.includes('登录密码')) return mockPasswordInput;
        return { count: mock.fn(async () => 0) };
      });
      mockPage.$ = mock.fn(async () => ({ click: mock.fn() }));

      await defaultExport.automatedLogin(mockPage, {
        BIGQUANT_USER: 'altuser',
        BIGQUANT_PASS: 'altpass'
      });

      assert.strictEqual(filledUsername, 'altuser');
      assert.strictEqual(filledPassword, 'altpass');
    });

    it('should click submit button when found', async () => {
      const mockPage = createMockPage();
      const mockSubmitBtn = { click: mock.fn() };

      const mockLoginBtn = { count: mock.fn(async () => 1), click: mock.fn() };
      const mockPasswordTab = { count: mock.fn(async () => 1), click: mock.fn() };
      const mockUsernameInput = { count: mock.fn(async () => 1), click: mock.fn(), fill: mock.fn() };
      const mockPasswordInput = { count: mock.fn(async () => 1), click: mock.fn(), fill: mock.fn() };

      mockPage.locator = mock.fn((selector) => {
        if (selector.includes('登录') && !selector.includes('密码')) return mockLoginBtn;
        if (selector.includes('密码登录')) return mockPasswordTab;
        if (selector.includes('用户名')) return mockUsernameInput;
        if (selector.includes('登录密码')) return mockPasswordInput;
        return { count: mock.fn(async () => 0) };
      });
      mockPage.$ = mock.fn(async (selector) => {
        if (selector.includes('.ant-modal-content')) return mockSubmitBtn;
        return null;
      });

      await defaultExport.automatedLogin(mockPage, {
        BIGQUANT_USERNAME: 'user',
        BIGQUANT_PASSWORD: 'pass'
      });

      assert.strictEqual(mockSubmitBtn.click.mock.calls.length, 1);
    });

    it('should press Enter when submit button not found', async () => {
      const mockPage = createMockPage();

      const mockLoginBtn = { count: mock.fn(async () => 1), click: mock.fn() };
      const mockPasswordTab = { count: mock.fn(async () => 1), click: mock.fn() };
      const mockUsernameInput = { count: mock.fn(async () => 1), click: mock.fn(), fill: mock.fn() };
      const mockPasswordInput = { count: mock.fn(async () => 1), click: mock.fn(), fill: mock.fn() };

      mockPage.locator = mock.fn((selector) => {
        if (selector.includes('登录') && !selector.includes('密码')) return mockLoginBtn;
        if (selector.includes('密码登录')) return mockPasswordTab;
        if (selector.includes('用户名')) return mockUsernameInput;
        if (selector.includes('登录密码')) return mockPasswordInput;
        return { count: mock.fn(async () => 0) };
      });
      mockPage.$ = mock.fn(async () => null);

      await defaultExport.automatedLogin(mockPage, {
        BIGQUANT_USERNAME: 'user',
        BIGQUANT_PASSWORD: 'pass'
      });

      assert.strictEqual(mockPage.keyboard.press.mock.calls.length, 1);
      assert.strictEqual(mockPage.keyboard.press.mock.calls[0][0], 'Enter');
    });
  });
});