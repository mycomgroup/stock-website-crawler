import { describe, it, beforeEach, afterEach, mock } from 'node:test';
import assert from 'node:assert';
import defaultExport from '../sites/lixinger.js';

const createMockPage = () => ({
  $: mock.fn(),
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
  waitForURL: mock.fn(),
  waitForLoadState: mock.fn(),
  keyboard: { press: mock.fn() },
  url: mock.fn(() => 'https://www.lixinger.com/analytics/screener/company-fundamental/cn')
});

const createMockResponse = (data, options = {}) => {
  const headers = new Map();
  const setCookie = options.setCookie || [];
  return {
    ok: options.ok ?? true,
    status: options.status ?? 200,
    json: mock.fn(async () => data),
    text: mock.fn(async () => typeof data === 'string' ? data : JSON.stringify(data)),
    headers: {
      getSetCookie: mock.fn(() => setCookie)
    }
  };
};

describe('lixinger site adapter', () => {
  let originalFetch;

  beforeEach(() => {
    originalFetch = global.fetch;
  });

  afterEach(() => {
    global.fetch = originalFetch;
  });

  describe('basic properties', () => {
    it('should have correct id', () => {
      assert.strictEqual(defaultExport.id, 'lixinger');
    });

    it('should have correct name', () => {
      assert.strictEqual(defaultExport.name, '理杏仁');
    });

    it('should have correct domain', () => {
      assert.strictEqual(defaultExport.domain, '.lixinger.com');
    });

    it('should have correct loginUrl', () => {
      assert.strictEqual(defaultExport.loginUrl, 'https://www.lixinger.com/login');
    });

    it('should have correct dashboardUrl', () => {
      assert.strictEqual(defaultExport.dashboardUrl, 'https://www.lixinger.com/analytics/screener/company-fundamental/cn');
    });

    it('should have correct loginApi', () => {
      assert.strictEqual(defaultExport.loginApi, 'https://www.lixinger.com/api/account/sign-in/by-account');
    });
  });

  describe('verifySession', () => {
    it('should return success when API returns valid data', async () => {
      global.fetch = mock.fn(async () => createMockResponse({
        priceMetricsDate: '2024-01-15'
      }));

      const result = await defaultExport.verifySession([{ name: 'session', value: 'abc123' }]);

      assert.strictEqual(result.success, true);
      assert.strictEqual(result.user, '理杏仁用户');
    });

    it('should return failure when priceMetricsDate is missing', async () => {
      global.fetch = mock.fn(async () => createMockResponse({
        someOtherField: 'value'
      }));

      const result = await defaultExport.verifySession([{ name: 'session', value: 'abc123' }]);

      assert.strictEqual(result.success, false);
      assert.strictEqual(result.message, '未返回有效数据');
    });

    it('should return failure when HTTP status is not ok', async () => {
      global.fetch = mock.fn(async () => createMockResponse({}, { ok: false, status: 401 }));

      const result = await defaultExport.verifySession([{ name: 'session', value: 'abc123' }]);

      assert.strictEqual(result.success, false);
      assert.strictEqual(result.message, 'HTTP 401');
    });

    it('should handle network errors', async () => {
      global.fetch = mock.fn(async () => { throw new Error('Network timeout'); });

      const result = await defaultExport.verifySession([{ name: 'session', value: 'abc123' }]);

      assert.strictEqual(result.success, false);
      assert.strictEqual(result.message, 'Network timeout');
    });

    it('should send POST request with correct body', async () => {
      let capturedBody;
      global.fetch = mock.fn(async (url, options) => {
        capturedBody = options.body;
        return createMockResponse({ priceMetricsDate: '2024-01-15' });
      });

      await defaultExport.verifySession([{ name: 's', value: 'v' }]);

      assert.strictEqual(capturedBody, JSON.stringify({ areaCode: 'cn' }));
    });

    it('should send correct headers', async () => {
      let capturedHeaders;
      global.fetch = mock.fn(async (url, options) => {
        capturedHeaders = options.headers;
        return createMockResponse({ priceMetricsDate: '2024-01-15' });
      });

      await defaultExport.verifySession([{ name: 's', value: 'v' }]);

      assert.strictEqual(capturedHeaders.Cookie, 's=v');
      assert.strictEqual(capturedHeaders['Content-Type'], 'application/json');
    });
  });

  describe('checkLoggedIn', () => {
    it('should return true when URL does not contain /login', async () => {
      const mockPage = createMockPage();
      mockPage.url = mock.fn(() => 'https://www.lixinger.com/analytics/stock');

      const result = await defaultExport.checkLoggedIn(mockPage);

      assert.strictEqual(result, true);
    });

    it('should return false when URL contains /login', async () => {
      const mockPage = createMockPage();
      mockPage.url = mock.fn(() => 'https://www.lixinger.com/login');

      const result = await defaultExport.checkLoggedIn(mockPage);

      assert.strictEqual(result, false);
    });

    it('should return false when URL contains /user/login', async () => {
      const mockPage = createMockPage();
      mockPage.url = mock.fn(() => 'https://www.lixinger.com/user/login');

      const result = await defaultExport.checkLoggedIn(mockPage);

      assert.strictEqual(result, false);
    });
  });

  describe('buildCookieFromHeader', () => {
    it('should return null for empty array', () => {
      const result = defaultExport.buildCookieFromHeader([]);
      assert.strictEqual(result, null);
    });

    it('should return null for null input', () => {
      const result = defaultExport.buildCookieFromHeader(null);
      assert.strictEqual(result, null);
    });

    it('should return null for undefined input', () => {
      const result = defaultExport.buildCookieFromHeader(undefined);
      assert.strictEqual(result, null);
    });

    it('should parse single cookie correctly', () => {
      const result = defaultExport.buildCookieFromHeader(['session=abc123; Path=/; Secure']);

      assert.strictEqual(result.length, 1);
      assert.deepStrictEqual(result[0], {
        name: 'session',
        value: 'abc123',
        domain: '.lixinger.com',
        path: '/',
        secure: true,
        sameSite: 'Lax'
      });
    });

    it('should parse multiple cookies correctly', () => {
      const result = defaultExport.buildCookieFromHeader([
        'session=abc123; Path=/; Secure',
        'token=xyz789; Path=/; HttpOnly'
      ]);

      assert.strictEqual(result.length, 2);
      assert.strictEqual(result[0].name, 'session');
      assert.strictEqual(result[0].value, 'abc123');
      assert.strictEqual(result[1].name, 'token');
      assert.strictEqual(result[1].value, 'xyz789');
    });

    it('should handle cookies with equals in value', () => {
      const result = defaultExport.buildCookieFromHeader(['data=key=value; Path=/']);

      assert.strictEqual(result.length, 1);
      assert.strictEqual(result[0].name, 'data');
      assert.strictEqual(result[0].value, 'key=value');
    });

    it('should filter empty cookies', () => {
      const result = defaultExport.buildCookieFromHeader(['; Path=/', 'session=abc']);

      assert.strictEqual(result.length, 1);
      assert.strictEqual(result[0].name, 'session');
    });

    it('should return null when all cookies are empty', () => {
      const result = defaultExport.buildCookieFromHeader(['; Path=/', '; Secure']);

      assert.strictEqual(result, null);
    });
  });

  describe('apiLogin', () => {
    it('should throw error when credentials are missing', async () => {
      await assert.rejects(
        defaultExport.apiLogin({}),
        { message: '未发现理杏仁账号凭证' }
      );
    });

    it('should throw error when password is missing', async () => {
      await assert.rejects(
        defaultExport.apiLogin({ LIXINGER_USERNAME: 'user' }),
        { message: '未发现理杏仁账号凭证' }
      );
    });

    it('should return cookies on successful login', async () => {
      global.fetch = mock.fn(async () => createMockResponse({}, {
        setCookie: ['session=abc123; Path=/; Secure', 'token=xyz; Path=/']
      }));

      const result = await defaultExport.apiLogin({
        LIXINGER_USERNAME: 'user',
        LIXINGER_PASSWORD: 'pass'
      });

      assert.strictEqual(result.length, 2);
      assert.strictEqual(result[0].name, 'session');
      assert.strictEqual(result[1].name, 'token');
    });

    it('should throw error when HTTP response is not ok', async () => {
      global.fetch = mock.fn(async () => createMockResponse('Error message', {
        ok: false,
        status: 401
      }));

      await assert.rejects(
        defaultExport.apiLogin({
          LIXINGER_USERNAME: 'user',
          LIXINGER_PASSWORD: 'pass'
        }),
        Error
      );
    });

    it('should throw error when no cookies returned', async () => {
      global.fetch = mock.fn(async () => createMockResponse({}, { setCookie: [] }));

      await assert.rejects(
        defaultExport.apiLogin({
          LIXINGER_USERNAME: 'user',
          LIXINGER_PASSWORD: 'pass'
        }),
        { message: 'API 登录成功但未返回 Cookie' }
      );
    });

    it('should use alternative credential keys', async () => {
      let capturedBody;
      global.fetch = mock.fn(async (url, options) => {
        capturedBody = options.body;
        return createMockResponse({}, { setCookie: ['session=abc'] });
      });

      await defaultExport.apiLogin({
        LIXINGER_USER: 'altuser',
        LIXINGER_PASS: 'altpass'
      });

      assert.deepStrictEqual(JSON.parse(capturedBody), {
        accountName: 'altuser',
        password: 'altpass'
      });
    });

    it('should send correct request body', async () => {
      let capturedBody;
      global.fetch = mock.fn(async (url, options) => {
        capturedBody = options.body;
        return createMockResponse({}, { setCookie: ['session=abc'] });
      });

      await defaultExport.apiLogin({
        LIXINGER_USERNAME: 'testuser',
        LIXINGER_PASSWORD: 'testpass'
      });

      assert.deepStrictEqual(JSON.parse(capturedBody), {
        accountName: 'testuser',
        password: 'testpass'
      });
    });

    it('should send correct headers', async () => {
      let capturedHeaders;
      global.fetch = mock.fn(async (url, options) => {
        capturedHeaders = options.headers;
        return createMockResponse({}, { setCookie: ['session=abc'] });
      });

      await defaultExport.apiLogin({
        LIXINGER_USERNAME: 'user',
        LIXINGER_PASSWORD: 'pass'
      });

      assert.strictEqual(capturedHeaders['content-type'], 'application/json;charset=UTF-8');
      assert.strictEqual(capturedHeaders.referer, 'https://www.lixinger.com/');
    });

    it('should handle text response on error', async () => {
      global.fetch = mock.fn(async () => ({
        ok: false,
        status: 500,
        text: mock.fn(async () => 'Internal Server Error'),
        headers: { getSetCookie: mock.fn(() => []) }
      }));

      await assert.rejects(
        defaultExport.apiLogin({
          LIXINGER_USERNAME: 'user',
          LIXINGER_PASSWORD: 'pass'
        }),
        Error
      );
    });
  });

  describe('automatedLogin', () => {
    it('should call apiLogin when page is null', async () => {
      global.fetch = mock.fn(async () => createMockResponse({}, {
        setCookie: ['session=abc']
      }));

      const result = await defaultExport.automatedLogin(null, {
        LIXINGER_USERNAME: 'user',
        LIXINGER_PASSWORD: 'pass'
      });

      assert.strictEqual(result.length, 1);
      assert.strictEqual(result[0].name, 'session');
    });

    it('should call apiLogin when page is undefined', async () => {
      global.fetch = mock.fn(async () => createMockResponse({}, {
        setCookie: ['session=abc']
      }));

      const result = await defaultExport.automatedLogin(undefined, {
        LIXINGER_USERNAME: 'user',
        LIXINGER_PASSWORD: 'pass'
      });

      assert.strictEqual(result.length, 1);
    });

    it('should throw error when credentials are missing for browser login', async () => {
      const mockPage = createMockPage();

      await assert.rejects(
        defaultExport.automatedLogin(mockPage, {}),
        { message: '未发现理杏仁账号凭证' }
      );
    });

    it('should throw error when username input not found', async () => {
      const mockPage = createMockPage();
      mockPage.locator = mock.fn(() => ({
        first: mock.fn(() => ({
          isVisible: mock.fn(async () => false),
          fill: mock.fn()
        }))
      }));

      await assert.rejects(
        defaultExport.automatedLogin(mockPage, {
          LIXINGER_USERNAME: 'user',
          LIXINGER_PASSWORD: 'pass'
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
        }))
      }));

      await assert.rejects(
        defaultExport.automatedLogin(mockPage, {
          LIXINGER_USERNAME: 'user',
          LIXINGER_PASSWORD: 'pass'
        }),
        { message: '无法找到密码输入框' }
      );
    });

    it('should throw error when browser login fails', async () => {
      const mockPage = createMockPage();
      mockPage.url = mock.fn(() => 'https://www.lixinger.com/login');

      mockPage.locator = mock.fn((selector) => ({
        first: mock.fn(() => ({
          isVisible: mock.fn(async () => true),
          fill: mock.fn(),
          click: mock.fn()
        })),
        isVisible: mock.fn(async () => true),
        click: mock.fn()
      }));

      await assert.rejects(
        defaultExport.automatedLogin(mockPage, {
          LIXINGER_USERNAME: 'user',
          LIXINGER_PASSWORD: 'pass'
        }),
        { message: '浏览器登录失败，请检查用户名密码或网络连接' }
      );
    });
  });
});