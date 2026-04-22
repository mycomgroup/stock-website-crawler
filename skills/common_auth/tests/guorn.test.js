import { describe, it, beforeEach, afterEach, mock } from 'node:test';
import assert from 'node:assert';
import defaultExport from '../sites/guorn.js';

const createMockPage = () => ({
  locator: mock.fn(() => ({
    first: mock.fn(() => ({
      isVisible: mock.fn(async () => true),
      fill: mock.fn(),
      click: mock.fn()
    })),
    isVisible: mock.fn(async () => true),
    click: mock.fn(),
    fill: mock.fn(),
    all: mock.fn(async () => [])
  })),
  waitForTimeout: mock.fn(),
  url: mock.fn(() => 'https://guorn.com/')
});

const createMockResponse = (data, options = {}) => ({
  ok: options.ok ?? true,
  status: options.status ?? 200,
  json: mock.fn(async () => data)
});

describe('guorn site adapter', () => {
  let originalFetch;

  beforeEach(() => {
    originalFetch = global.fetch;
  });

  afterEach(() => {
    global.fetch = originalFetch;
  });

  describe('basic properties', () => {
    it('should have correct id', () => {
      assert.strictEqual(defaultExport.id, 'guorn');
    });

    it('should have correct name', () => {
      assert.strictEqual(defaultExport.name, '果仁网');
    });

    it('should have correct domain', () => {
      assert.strictEqual(defaultExport.domain, '.guorn.com');
    });

    it('should have correct loginUrl', () => {
      assert.strictEqual(defaultExport.loginUrl, 'https://guorn.com/user/login');
    });

    it('should have correct dashboardUrl', () => {
      assert.strictEqual(defaultExport.dashboardUrl, 'https://guorn.com/');
    });
  });

  describe('verifySession', () => {
    it('should return success when profile returns valid data', async () => {
      global.fetch = mock.fn(async () => createMockResponse({
        status: 'ok',
        data: { username: 'testuser' }
      }));

      const result = await defaultExport.verifySession([{ name: 'session', value: 'abc' }]);

      assert.strictEqual(result.success, true);
      assert.strictEqual(result.user, 'testuser');
    });

    it('should return failure when status is 401', async () => {
      global.fetch = mock.fn(async () => createMockResponse({}, { 
        ok: false, 
        status: 401 
      }));

      const result = await defaultExport.verifySession([{ name: 'session', value: 'abc' }]);

      assert.strictEqual(result.success, false);
      assert.strictEqual(result.message, 'Cookie 已过期');
    });

    it('should return failure when status is not ok', async () => {
      global.fetch = mock.fn(async () => createMockResponse({
        status: 'error',
        message: 'Unknown'
      }));

      const result = await defaultExport.verifySession([{ name: 'session', value: 'abc' }]);

      assert.strictEqual(result.success, false);
      assert.strictEqual(result.message, '无法识别用户信息');
    });

    it('should return failure when username is missing', async () => {
      global.fetch = mock.fn(async () => createMockResponse({
        status: 'ok',
        data: {}
      }));

      const result = await defaultExport.verifySession([{ name: 'session', value: 'abc' }]);

      assert.strictEqual(result.success, false);
      assert.strictEqual(result.message, '无法识别用户信息');
    });

    it('should handle network errors', async () => {
      global.fetch = mock.fn(async () => { 
        throw new Error('Connection timeout'); 
      });

      const result = await defaultExport.verifySession([{ name: 'session', value: 'abc' }]);

      assert.strictEqual(result.success, false);
      assert.ok(result.message.includes('网络错误'));
    });

    it('should handle JSON parse error', async () => {
      global.fetch = mock.fn(async () => ({
        ok: true,
        status: 200,
        json: mock.fn(async () => {
          throw new SyntaxError('Invalid JSON');
        })
      }));

      const result = await defaultExport.verifySession([{ name: 'session', value: 'abc' }]);

      assert.strictEqual(result.success, false);
      assert.strictEqual(result.message, '无法识别用户信息');
    });

    it('should send correct headers', async () => {
      let capturedHeaders;
      global.fetch = mock.fn(async (url, options) => {
        capturedHeaders = options.headers;
        return createMockResponse({ status: 'ok', data: { username: 'test' } });
      });

      await defaultExport.verifySession([{ name: 's', value: 'v' }]);

      assert.ok(capturedHeaders.Cookie);
      assert.strictEqual(capturedHeaders.Accept, 'application/json');
      assert.ok(capturedHeaders['User-Agent'].includes('Mozilla'));
    });
  });

  describe('checkLoggedIn', () => {
    it('should return true when URL does not contain /user/login', async () => {
      const mockPage = createMockPage();
      mockPage.url = mock.fn(() => 'https://guorn.com/dashboard');

      const result = await defaultExport.checkLoggedIn(mockPage);

      assert.strictEqual(result, true);
    });

    it('should return false when URL contains /user/login', async () => {
      const mockPage = createMockPage();
      mockPage.url = mock.fn(() => 'https://guorn.com/user/login');

      const result = await defaultExport.checkLoggedIn(mockPage);

      assert.strictEqual(result, false);
    });
  });

  describe('automatedLogin', () => {
    it('should throw error when credentials are missing', async () => {
      const mockPage = createMockPage();

      await assert.rejects(
        defaultExport.automatedLogin(mockPage, {}),
        { message: '未发现果仁网账号凭证' }
      );
    });

    it('should throw error when only username is provided', async () => {
      const mockPage = createMockPage();

      await assert.rejects(
        defaultExport.automatedLogin(mockPage, { GUORN_USERNAME: 'user' }),
        { message: '未发现果仁网账号凭证' }
      );
    });

    it('should use alternative credential keys', async () => {
      const mockPage = createMockPage();
      let filledValues = [];

      mockPage.locator = mock.fn(() => ({
        first: mock.fn(() => ({
          isVisible: mock.fn(async () => true),
          fill: mock.fn(async (v) => { filledValues.push(v); }),
          click: mock.fn()
        })),
        isVisible: mock.fn(async () => true),
        click: mock.fn(),
        fill: mock.fn(),
        all: mock.fn(async () => [])
      }));

      await defaultExport.automatedLogin(mockPage, {
        GUORN_USER: 'altuser',
        GUORN_PASS: 'altpass'
      });

      assert.ok(filledValues.includes('altuser'));
      assert.ok(filledValues.includes('altpass'));
    });

    it('should try multiple username selectors', async () => {
      const mockPage = createMockPage();
      let triedSelectors = [];

      mockPage.locator = mock.fn((selector) => {
        triedSelectors.push(selector);
        return {
          first: mock.fn(() => ({
            isVisible: mock.fn(async () => triedSelectors.length === 1),
            fill: mock.fn(),
            click: mock.fn()
          })),
          isVisible: mock.fn(async () => true),
          click: mock.fn(),
          fill: mock.fn()
        };
      });

      await defaultExport.automatedLogin(mockPage, {
        GUORN_USERNAME: 'user',
        GUORN_PASSWORD: 'pass'
      });

      assert.ok(triedSelectors.some(s => s.includes('login-Id') || s.includes('account')));
    });

    it('should throw error when username input not found', async () => {
      const mockPage = createMockPage();

      mockPage.locator = mock.fn(() => ({
        first: mock.fn(() => ({
          isVisible: mock.fn(async () => false),
          fill: mock.fn()
        })),
        all: mock.fn(async () => [])
      }));

      await assert.rejects(
        defaultExport.automatedLogin(mockPage, {
          GUORN_USERNAME: 'user',
          GUORN_PASSWORD: 'pass'
        }),
        { message: '无法找到用户名输入框' }
      );
    });

    it('should throw error when password input not found', async () => {
      const mockPage = createMockPage();
      let callCount = 0;

      mockPage.locator = mock.fn(() => ({
        first: mock.fn(() => ({
          isVisible: mock.fn(async () => {
            callCount++;
            return callCount === 1;
          }),
          fill: mock.fn()
        })),
        all: mock.fn(async () => [])
      }));

      await assert.rejects(
        defaultExport.automatedLogin(mockPage, {
          GUORN_USERNAME: 'user',
          GUORN_PASSWORD: 'pass'
        }),
        { message: '无法找到密码输入框' }
      );
    });

    it('should throw error when login button not found', async () => {
      const mockPage = createMockPage();
      let selectorCalls = 0;

      mockPage.locator = mock.fn(() => ({
        first: mock.fn(() => ({
          isVisible: mock.fn(async () => {
            selectorCalls++;
            return selectorCalls <= 2;
          }),
          fill: mock.fn(),
          click: mock.fn()
        })),
        all: mock.fn(async () => [])
      }));

      await assert.rejects(
        defaultExport.automatedLogin(mockPage, {
          GUORN_USERNAME: 'user',
          GUORN_PASSWORD: 'pass'
        }),
        { message: '无法找到登录按钮' }
      );
    });

    it('should return success object on successful login', async () => {
      const mockPage = createMockPage();
      mockPage.url = mock.fn(() => 'https://guorn.com/dashboard');

      const result = await defaultExport.automatedLogin(mockPage, {
        GUORN_USERNAME: 'user',
        GUORN_PASSWORD: 'pass'
      });

      assert.strictEqual(result.success, true);
    });

    it('should throw error when still on login page after submission', async () => {
      const mockPage = createMockPage();
      mockPage.url = mock.fn(() => 'https://guorn.com/user/login');

      await assert.rejects(
        defaultExport.automatedLogin(mockPage, {
          GUORN_USERNAME: 'user',
          GUORN_PASSWORD: 'pass'
        }),
        { message: '登录失败，请检查用户名密码或网络连接' }
      );
    });
  });
});