import { describe, it, beforeEach, afterEach, mock } from 'node:test';
import assert from 'node:assert';
import defaultExport from '../sites/ricequant.js';

const createMockPage = () => ({
  $: mock.fn(),
  locator: mock.fn(() => ({
    count: mock.fn(async () => 1),
    click: mock.fn(),
    fill: mock.fn()
  })),
  waitForTimeout: mock.fn(),
  click: mock.fn(),
  url: mock.fn(() => 'https://www.ricequant.com/algorithms')
});

const createMockResponse = (data, options = {}) => ({
  ok: options.ok ?? true,
  status: options.status ?? 200,
  json: mock.fn(async () => data)
});

describe('ricequant site adapter', () => {
  let originalFetch;

  beforeEach(() => {
    originalFetch = global.fetch;
  });

  afterEach(() => {
    global.fetch = originalFetch;
  });

  describe('basic properties', () => {
    it('should have correct id', () => {
      assert.strictEqual(defaultExport.id, 'ricequant');
    });

    it('should have correct name', () => {
      assert.strictEqual(defaultExport.name, '米筐');
    });

    it('should have correct domain', () => {
      assert.strictEqual(defaultExport.domain, '.ricequant.com');
    });

    it('should have correct loginUrl', () => {
      assert.strictEqual(defaultExport.loginUrl, 'https://www.ricequant.com/login');
    });

    it('should have correct dashboardUrl', () => {
      assert.strictEqual(defaultExport.dashboardUrl, 'https://www.ricequant.com/algorithms');
    });
  });

  describe('verifySession', () => {
    it('should return success when API returns userId', async () => {
      global.fetch = mock.fn(async () => createMockResponse({
        code: 0,
        userId: 12345,
        fullname: 'Test User'
      }));

      const result = await defaultExport.verifySession([{ name: 'session', value: 'abc' }]);

      assert.strictEqual(result.success, true);
      assert.strictEqual(result.user, 'Test User');
    });

    it('should return success when API returns user_id', async () => {
      global.fetch = mock.fn(async () => createMockResponse({
        code: 0,
        user_id: 67890,
        username: 'testuser'
      }));

      const result = await defaultExport.verifySession([{ name: 'session', value: 'abc' }]);

      assert.strictEqual(result.success, true);
      assert.strictEqual(result.user, 'testuser');
    });

    it('should return failure when code is not 0', async () => {
      global.fetch = mock.fn(async () => createMockResponse({
        code: 1,
        message: '未登录'
      }));

      const result = await defaultExport.verifySession([{ name: 'session', value: 'abc' }]);

      assert.strictEqual(result.success, false);
      assert.strictEqual(result.message, '未登录');
    });

    it('should return failure when userId/user_id missing', async () => {
      global.fetch = mock.fn(async () => createMockResponse({
        code: 0
      }));

      const result = await defaultExport.verifySession([{ name: 'session', value: 'abc' }]);

      assert.strictEqual(result.success, false);
    });

    it('should return failure when HTTP status is not ok', async () => {
      global.fetch = mock.fn(async () => createMockResponse({}, { 
        ok: false, 
        status: 500 
      }));

      const result = await defaultExport.verifySession([{ name: 'session', value: 'abc' }]);

      assert.strictEqual(result.success, false);
    });

    it('should handle network errors', async () => {
      global.fetch = mock.fn(async () => { 
        throw new Error('Connection timeout'); 
      });

      const result = await defaultExport.verifySession([{ name: 'session', value: 'abc' }]);

      assert.strictEqual(result.success, false);
      assert.strictEqual(result.message, 'Connection timeout');
    });

    it('should send POST request', async () => {
      let capturedMethod;
      global.fetch = mock.fn(async (url, options) => {
        capturedMethod = options.method;
        return createMockResponse({ code: 0, userId: 1 });
      });

      await defaultExport.verifySession([{ name: 's', value: 'v' }]);

      assert.strictEqual(capturedMethod, 'POST');
    });

    it('should send correct headers', async () => {
      let capturedHeaders;
      global.fetch = mock.fn(async (url, options) => {
        capturedHeaders = options.headers;
        return createMockResponse({ code: 0, userId: 1 });
      });

      await defaultExport.verifySession([{ name: 's', value: 'v' }]);

      assert.ok(capturedHeaders.Cookie);
      assert.ok(capturedHeaders['User-Agent'].includes('Mozilla'));
      assert.strictEqual(capturedHeaders['X-Requested-With'], 'XMLHttpRequest');
    });

    it('should use fullname as user first', async () => {
      global.fetch = mock.fn(async () => createMockResponse({
        code: 0,
        userId: 123,
        fullname: 'Full Name',
        username: 'username'
      }));

      const result = await defaultExport.verifySession([{ name: 'session', value: 'abc' }]);

      assert.strictEqual(result.user, 'Full Name');
    });

    it('should use username when fullname missing', async () => {
      global.fetch = mock.fn(async () => createMockResponse({
        code: 0,
        userId: 123,
        username: 'username'
      }));

      const result = await defaultExport.verifySession([{ name: 'session', value: 'abc' }]);

      assert.strictEqual(result.user, 'username');
    });

    it('should use userId when fullname/username missing', async () => {
      global.fetch = mock.fn(async () => createMockResponse({
        code: 0,
        userId: 123
      }));

      const result = await defaultExport.verifySession([{ name: 'session', value: 'abc' }]);

      assert.strictEqual(result.user, 123);
    });
  });

  describe('checkLoggedIn', () => {
    it('should return false when URL contains /login', async () => {
      const mockPage = createMockPage();
      mockPage.url = mock.fn(() => 'https://www.ricequant.com/login');

      const result = await defaultExport.checkLoggedIn(mockPage);

      assert.strictEqual(result, false);
    });

    it('should return true when login button not present and user info present', async () => {
      const mockPage = createMockPage();
      mockPage.$ = mock.fn(async (selector) => {
        if (selector.includes('登录')) return null;
        if (selector.includes('user')) return {};
        return null;
      });

      const result = await defaultExport.checkLoggedIn(mockPage);

      assert.strictEqual(result, true);
    });

    it('should return false when login button present', async () => {
      const mockPage = createMockPage();
      mockPage.$ = mock.fn(async (selector) => {
        if (selector.includes('登录')) return {};
        return null;
      });

      const result = await defaultExport.checkLoggedIn(mockPage);

      assert.strictEqual(result, false);
    });

    it('should fallback to URL check on error', async () => {
      const mockPage = createMockPage();
      mockPage.$ = mock.fn(async () => { throw new Error('Error'); });
      mockPage.url = mock.fn(() => 'https://www.ricequant.com/algorithms');

      const result = await defaultExport.checkLoggedIn(mockPage);

      assert.strictEqual(result, true);
    });
  });

  describe('automatedLogin', () => {
    it('should throw error when credentials are missing', async () => {
      const mockPage = createMockPage();

      await assert.rejects(
        defaultExport.automatedLogin(mockPage, {}),
        { message: '未发现米筐账号凭证' }
      );
    });

    it('should throw error when only username is provided', async () => {
      const mockPage = createMockPage();

      await assert.rejects(
        defaultExport.automatedLogin(mockPage, { RICEQUANT_USERNAME: 'user' }),
        { message: '未发现米筐账号凭证' }
      );
    });

    it('should use alternative credential keys', async () => {
      const mockPage = createMockPage();
      let filledValues = [];

      mockPage.locator = mock.fn(() => ({
        count: mock.fn(async () => 1),
        click: mock.fn(),
        fill: mock.fn(async (v) => { filledValues.push(v); })
      }));

      mockPage.$ = mock.fn(async () => null);
      mockPage.click = mock.fn();

      await defaultExport.automatedLogin(mockPage, {
        RICEQUANT_USER: 'altuser',
        RICEQUANT_PASS: 'altpass'
      });

      assert.ok(filledValues.includes('altuser'));
      assert.ok(filledValues.includes('altpass'));
    });

    it('should click login button if present', async () => {
      const mockPage = createMockPage();
      const mockLoginBtn = { click: mock.fn() };
      mockPage.$ = mock.fn(async () => mockLoginBtn);

      mockPage.locator = mock.fn(() => ({
        count: mock.fn(async () => 1),
        click: mock.fn(),
        fill: mock.fn()
      }));

      await defaultExport.automatedLogin(mockPage, {
        RICEQUANT_USERNAME: 'user',
        RICEQUANT_PASSWORD: 'pass'
      });

      assert.strictEqual(mockLoginBtn.click.mock.calls.length, 1);
    });

    it('should click password login tab', async () => {
      const mockPage = createMockPage();
      let clickedTexts = [];

      mockPage.click = mock.fn(async (text) => { clickedTexts.push(text); });
      mockPage.$ = mock.fn(async () => null);

      mockPage.locator = mock.fn(() => ({
        count: mock.fn(async () => 1),
        click: mock.fn(),
        fill: mock.fn()
      }));

      await defaultExport.automatedLogin(mockPage, {
        RICEQUANT_USERNAME: 'user',
        RICEQUANT_PASSWORD: 'pass'
      });

      assert.ok(clickedTexts.some(t => t.includes('密码登录')));
    });

    it('should throw error when inputs not found', async () => {
      const mockPage = createMockPage();

      mockPage.locator = mock.fn(() => ({
        count: mock.fn(async () => 0),
        click: mock.fn(),
        fill: mock.fn()
      }));

      mockPage.$ = mock.fn(async () => null);
      mockPage.click = mock.fn();

      await assert.rejects(
        defaultExport.automatedLogin(mockPage, {
          RICEQUANT_USERNAME: 'user',
          RICEQUANT_PASSWORD: 'pass'
        }),
        { message: '未找到用户名或密码输入框' }
      );
    });

    it('should click submit button', async () => {
      const mockPage = createMockPage();
      let clickedSelectors = [];

      mockPage.locator = mock.fn(() => ({
        count: mock.fn(async () => 1),
        click: mock.fn(async (s) => { clickedSelectors.push(s); }),
        fill: mock.fn()
      }));

      mockPage.$ = mock.fn(async () => null);
      mockPage.click = mock.fn();

      await defaultExport.automatedLogin(mockPage, {
        RICEQUANT_USERNAME: 'user',
        RICEQUANT_PASSWORD: 'pass'
      });

      assert.ok(clickedSelectors.some(s => s.includes('btn--submit')));
    });

    it('should fill username first then password', async () => {
      const mockPage = createMockPage();
      let fillOrder = [];

      mockPage.locator = mock.fn((selector) => ({
        count: mock.fn(async () => 1),
        click: mock.fn(),
        fill: mock.fn(async (v) => { fillOrder.push({ selector, value: v }); })
      }));

      mockPage.$ = mock.fn(async () => null);
      mockPage.click = mock.fn();

      await defaultExport.automatedLogin(mockPage, {
        RICEQUANT_USERNAME: 'user',
        RICEQUANT_PASSWORD: 'pass'
      });

      const usernameFill = fillOrder.find(f => f.selector.includes('手机号'));
      const passwordFill = fillOrder.find(f => f.selector.includes('password'));

      assert.ok(usernameFill);
      assert.ok(passwordFill);
      assert.strictEqual(usernameFill.value, 'user');
      assert.strictEqual(passwordFill.value, 'pass');
    });
  });
});