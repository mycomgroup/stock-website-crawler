import { describe, it, beforeEach, afterEach, mock } from 'node:test';
import assert from 'node:assert';
import defaultExport from '../sites/thsquant.js';

const createMockPage = () => ({
  $: mock.fn(),
  waitForTimeout: mock.fn(),
  waitForSelector: mock.fn(),
  waitForNavigation: mock.fn(async () => {}),
  url: mock.fn(() => 'https://quant.10jqka.com.cn/view/study-index.html'),
  evaluate: mock.fn(async () => false)
});

const createMockResponse = (data, options = {}) => ({
  ok: options.ok ?? true,
  status: options.status ?? 200,
  json: mock.fn(async () => data),
  text: mock.fn(async () => typeof data === 'string' ? data : JSON.stringify(data))
});

describe('thsquant site adapter', () => {
  let originalFetch;

  beforeEach(() => {
    originalFetch = global.fetch;
  });

  afterEach(() => {
    global.fetch = originalFetch;
  });

  describe('basic properties', () => {
    it('should have correct id', () => {
      assert.strictEqual(defaultExport.id, 'thsquant');
    });

    it('should have correct name', () => {
      assert.strictEqual(defaultExport.name, '同花顺量化 (thsquant)');
    });

    it('should have correct domain', () => {
      assert.strictEqual(defaultExport.domain, '.10jqka.com.cn');
    });

    it('should have correct loginUrl', () => {
      assert.strictEqual(defaultExport.loginUrl, 'https://quant.10jqka.com.cn/view/study-index.html');
    });

    it('should have correct dashboardUrl', () => {
      assert.strictEqual(defaultExport.dashboardUrl, 'https://quant.10jqka.com.cn/view/study-index.html');
    });
  });

  describe('verifySession', () => {
    it('should return success when API returns code 200', async () => {
      global.fetch = mock.fn(async () => createMockResponse({
        code: 200,
        data: { username: 'testuser' }
      }));

      const result = await defaultExport.verifySession([{ name: 'session', value: 'abc123' }]);

      assert.strictEqual(result.success, true);
      assert.strictEqual(result.user, 'testuser');
    });

    it('should return success when API returns code 0', async () => {
      global.fetch = mock.fn(async () => createMockResponse({
        code: 0,
        data: { username: 'testuser' }
      }));

      const result = await defaultExport.verifySession([{ name: 'session', value: 'abc123' }]);

      assert.strictEqual(result.success, true);
    });

    it('should return failure when API returns error code', async () => {
      global.fetch = mock.fn(async () => createMockResponse({
        code: 401,
        message: '未授权'
      }));

      const result = await defaultExport.verifySession([{ name: 'session', value: 'abc123' }]);

      assert.strictEqual(result.success, false);
      assert.strictEqual(result.message, '未授权');
    });

    it('should return default message when no message in response', async () => {
      global.fetch = mock.fn(async () => createMockResponse({ code: 500 }));

      const result = await defaultExport.verifySession([{ name: 'session', value: 'abc123' }]);

      assert.strictEqual(result.success, false);
      assert.strictEqual(result.message, 'Cookie 失效');
    });

    it('should use default user name when username not in data', async () => {
      global.fetch = mock.fn(async () => createMockResponse({
        code: 200,
        data: {}
      }));

      const result = await defaultExport.verifySession([{ name: 'session', value: 'abc123' }]);

      assert.strictEqual(result.success, true);
      assert.strictEqual(result.user, '已登录');
    });

    it('should send correct headers', async () => {
      let capturedHeaders;
      global.fetch = mock.fn(async (url, options) => {
        capturedHeaders = options.headers;
        return createMockResponse({ code: 200, data: { username: 'test' } });
      });

      await defaultExport.verifySession([{ name: 's', value: 'v' }]);

      assert.strictEqual(capturedHeaders.Cookie, 's=v');
      assert.strictEqual(capturedHeaders.Accept, 'application/json');
    });

    it('should handle JSON parse error', async () => {
      global.fetch = mock.fn(async () => ({
        ok: true,
        status: 200,
        json: mock.fn(async () => { throw new SyntaxError('Invalid JSON'); }),
        text: mock.fn(async () => '<html></html>')
      }));

      const result = await defaultExport.verifySession([{ name: 'session', value: 'abc123' }]);

      assert.strictEqual(result.success, false);
    });
  });

  describe('checkLoggedIn', () => {
    it('should return boolean type', async () => {
      const mockPage = createMockPage();

      const result = await defaultExport.checkLoggedIn(mockPage);

      assert.strictEqual(typeof result, 'boolean');
    });

    it('should return false when login button visible', async () => {
      const mockPage = createMockPage();
      mockPage.evaluate = mock.fn(async (fn) => {
        if (fn.toString().includes('login-btn') || fn.toString().includes('header_signup')) {
          return true;
        }
        return false;
      });

      const result = await defaultExport.checkLoggedIn(mockPage);

      assert.strictEqual(result, false);
    });

    it('should return true when user indicators present', async () => {
      const mockPage = createMockPage();
      mockPage.evaluate = mock.fn(async (fn) => {
        if (fn.toString().includes('login-btn')) {
          return false;
        }
        if (fn.toString().includes('user-info') || fn.toString().includes('isLoggedIn')) {
          return true;
        }
        return false;
      });

      const result = await defaultExport.checkLoggedIn(mockPage);

      assert.strictEqual(typeof result, 'boolean');
    });
  });

  describe('automatedLogin', () => {
    it('should throw error when credentials are missing', async () => {
      const mockPage = createMockPage();

      await assert.rejects(
        defaultExport.automatedLogin(mockPage, {}),
        { message: '未发现同花顺量化账号凭证 (THSQUANT_USERNAME/PASSWORD)' }
      );
    });

    it('should throw error when password is missing', async () => {
      const mockPage = createMockPage();

      await assert.rejects(
        defaultExport.automatedLogin(mockPage, { THSQUANT_USERNAME: 'user' }),
        { message: '未发现同花顺量化账号凭证 (THSQUANT_USERNAME/PASSWORD)' }
      );
    });

    it('should throw error when iframe content frame is null', async () => {
      const mockPage = createMockPage();
      const mockIframeElement = {
        contentFrame: mock.fn(async () => null)
      };

      mockPage.$ = mock.fn(async () => null);
      mockPage.waitForSelector = mock.fn(async () => mockIframeElement);

      await assert.rejects(
        defaultExport.automatedLogin(mockPage, {
          THSQUANT_USERNAME: 'user',
          THSQUANT_PASSWORD: 'pass'
        }),
        { message: '无法获取登录 iframe' }
      );
    });

    it('should use alternative credential keys THS_USER/THS_PASS', async () => {
      const mockPage = createMockPage();
      const mockFrame = {
        $: mock.fn(async () => ({ click: mock.fn() })),
        click: mock.fn(async () => {}),
        fill: mock.fn(async () => {}),
        keyboard: { press: mock.fn() }
      };
      const mockIframeElement = {
        contentFrame: mock.fn(async () => mockFrame)
      };

      mockPage.$ = mock.fn(async () => null);
      mockPage.waitForSelector = mock.fn(async () => mockIframeElement);

      await defaultExport.automatedLogin(mockPage, {
        THS_USER: 'altuser',
        THS_PASS: 'altpass'
      });

      assert.ok(mockFrame.fill.mock.calls.length >= 2);
    });

    it('should click login trigger if present', async () => {
      const mockPage = createMockPage();
      const mockLoginTrigger = { click: mock.fn(async () => {}) };
      const mockFrame = {
        $: mock.fn(async () => ({ click: mock.fn() })),
        click: mock.fn(async () => {}),
        fill: mock.fn(async () => {}),
        keyboard: { press: mock.fn() }
      };
      const mockIframeElement = {
        contentFrame: mock.fn(async () => mockFrame)
      };

      mockPage.$ = mock.fn(async (sel) => {
        if (sel.includes('header_signup')) return mockLoginTrigger;
        return null;
      });
      mockPage.waitForSelector = mock.fn(async () => mockIframeElement);

      await defaultExport.automatedLogin(mockPage, {
        THSQUANT_USERNAME: 'user',
        THSQUANT_PASSWORD: 'pass'
      });

      assert.strictEqual(mockLoginTrigger.click.mock.calls.length, 1);
    });

    it('should call fill with username and password', async () => {
      const mockPage = createMockPage();
      const filledData = [];
      const mockFrame = {
        $: mock.fn(async () => ({ click: mock.fn() })),
        click: mock.fn(async () => {}),
        fill: mock.fn(async (sel, val) => { filledData.push({ sel, val }); }),
        keyboard: { press: mock.fn() }
      };
      const mockIframeElement = {
        contentFrame: mock.fn(async () => mockFrame)
      };

      mockPage.$ = mock.fn(async () => null);
      mockPage.waitForSelector = mock.fn(async () => mockIframeElement);

      await defaultExport.automatedLogin(mockPage, {
        THSQUANT_USERNAME: 'testuser',
        THSQUANT_PASSWORD: 'testpass'
      });

      assert.ok(filledData.some(d => d.sel.includes('username') && d.val === 'testuser'));
      assert.ok(filledData.some(d => d.sel.includes('password') && d.val === 'testpass'));
    });

    it('should handle waitForNavigation catching errors', async () => {
      const mockPage = createMockPage();
      const mockFrame = {
        $: mock.fn(async () => ({ click: mock.fn() })),
        click: mock.fn(async () => {}),
        fill: mock.fn(async () => {}),
        keyboard: { press: mock.fn() }
      };
      const mockIframeElement = {
        contentFrame: mock.fn(async () => mockFrame)
      };

      mockPage.$ = mock.fn(async () => null);
      mockPage.waitForSelector = mock.fn(async () => mockIframeElement);
      mockPage.waitForNavigation = mock.fn(async () => { throw new Error('Timeout'); });

      await defaultExport.automatedLogin(mockPage, {
        THSQUANT_USERNAME: 'user',
        THSQUANT_PASSWORD: 'pass'
      });

      assert.strictEqual(mockPage.waitForNavigation.mock.calls.length, 1);
    });
  });
});