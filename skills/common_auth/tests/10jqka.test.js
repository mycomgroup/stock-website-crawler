import { describe, it, beforeEach, afterEach, mock } from 'node:test';
import assert from 'node:assert';
import defaultExport from '../sites/10jqka.js';

const createMockPage = () => ({
  $: mock.fn(),
  waitForSelector: mock.fn(async () => ({
    contentFrame: mock.fn(async () => ({
      click: mock.fn(),
      fill: mock.fn(),
      waitForFunction: mock.fn(),
      $: mock.fn()
    }))
  })),
  waitForFunction: mock.fn(),
  url: mock.fn(() => 'https://backtest.10jqka.com.cn/')
});

const createMockResponse = (data, options = {}) => ({
  ok: options.ok ?? true,
  status: options.status ?? 200,
  json: mock.fn(async () => data)
});

describe('10jqka site adapter', () => {
  let originalFetch;

  beforeEach(() => {
    originalFetch = global.fetch;
  });

  afterEach(() => {
    global.fetch = originalFetch;
  });

  describe('basic properties', () => {
    it('should have correct id', () => {
      assert.strictEqual(defaultExport.id, '10jqka');
    });

    it('should have correct name', () => {
      assert.strictEqual(defaultExport.name, '问财回测/同花顺');
    });

    it('should have correct domain', () => {
      assert.strictEqual(defaultExport.domain, '.10jqka.com.cn');
    });

    it('should have correct loginUrl', () => {
      assert.strictEqual(defaultExport.loginUrl, 'https://backtest.10jqka.com.cn/backtest/app.html#/strategybacktest');
    });

    it('should have correct dashboardUrl', () => {
      assert.strictEqual(defaultExport.dashboardUrl, 'https://backtest.10jqka.com.cn/backtest/app.html#/strategybacktest');
    });
  });

  describe('verifySession', () => {
    it('should return failure when errorcode is -401', async () => {
      global.fetch = mock.fn(async () => createMockResponse({
        errorcode: -401,
        message: 'Unauthorized'
      }));

      const result = await defaultExport.verifySession([{ name: 'session', value: 'abc' }]);

      assert.strictEqual(result.success, false);
      assert.strictEqual(result.message, '未授权或 Cookie 已失效');
    });

    it('should return success when no errorcode -401', async () => {
      global.fetch = mock.fn(async () => createMockResponse({
        errorcode: 0,
        data: 'success'
      }));

      const result = await defaultExport.verifySession([{ name: 'session', value: 'abc' }]);

      assert.strictEqual(result.success, true);
      assert.strictEqual(result.user, '已登录');
    });

    it('should return success when response has other error codes', async () => {
      global.fetch = mock.fn(async () => createMockResponse({
        errorcode: -500,
        message: 'Server error'
      }));

      const result = await defaultExport.verifySession([{ name: 'session', value: 'abc' }]);

      assert.strictEqual(result.success, true);
    });

    it('should handle JSON parse error gracefully', async () => {
      global.fetch = mock.fn(async () => ({
        ok: true,
        json: mock.fn(async () => {
          throw new SyntaxError('Invalid JSON');
        })
      }));

      const result = await defaultExport.verifySession([{ name: 'session', value: 'abc' }]);

      assert.strictEqual(result.success, true);
    });

    it('should send POST request with correct body', async () => {
      let capturedBody;
      global.fetch = mock.fn(async (url, options) => {
        capturedBody = options.body;
        return createMockResponse({ errorcode: 0 });
      });

      await defaultExport.verifySession([{ name: 's', value: 'v' }]);

      assert.strictEqual(capturedBody, JSON.stringify({ query: '测试' }));
    });

    it('should send correct headers', async () => {
      let capturedHeaders;
      global.fetch = mock.fn(async (url, options) => {
        capturedHeaders = options.headers;
        return createMockResponse({ errorcode: 0 });
      });

      await defaultExport.verifySession([{ name: 's', value: 'v' }]);

      assert.ok(capturedHeaders.Cookie);
      assert.strictEqual(capturedHeaders['Content-Type'], 'application/json');
    });
  });

  describe('checkLoggedIn', () => {
    it('should return false when login link is present', async () => {
      const mockPage = createMockPage();
      mockPage.$ = mock.fn(async () => ({}));

      const result = await defaultExport.checkLoggedIn(mockPage);

      assert.strictEqual(result, false);
    });

    it('should return true when login link is not present', async () => {
      const mockPage = createMockPage();
      mockPage.$ = mock.fn(async () => null);

      const result = await defaultExport.checkLoggedIn(mockPage);

      assert.strictEqual(result, true);
    });

    it('should use text selector for login link', async () => {
      const mockPage = createMockPage();
      let capturedSelector;
      mockPage.$ = mock.fn(async (selector) => {
        capturedSelector = selector;
        return null;
      });

      await defaultExport.checkLoggedIn(mockPage);

      assert.ok(capturedSelector.includes('登录'));
    });
  });

  describe('automatedLogin', () => {
    it('should throw error when credentials are missing', async () => {
      const mockPage = createMockPage();

      await assert.rejects(
        defaultExport.automatedLogin(mockPage, {}),
        { message: '未发现同花顺账号凭证 (THSQUANT_USERNAME/PASSWORD)' }
      );
    });

    it('should throw error when only username is provided', async () => {
      const mockPage = createMockPage();

      await assert.rejects(
        defaultExport.automatedLogin(mockPage, { THSQUANT_USERNAME: 'user' }),
        { message: '未发现同花顺账号凭证 (THSQUANT_USERNAME/PASSWORD)' }
      );
    });

    it('should use alternative credential keys', async () => {
      const mockPage = createMockPage();
      let filledUsername;
      let filledPassword;

      const mockFrame = {
        click: mock.fn(),
        fill: mock.fn(async (selector, value) => {
          if (selector.includes('uname')) filledUsername = value;
          if (selector.includes('passwd')) filledPassword = value;
        }),
        $: mock.fn(async () => ({ click: mock.fn() }))
      };

      mockPage.$ = mock.fn(async () => ({ click: mock.fn() }));
      mockPage.waitForSelector = mock.fn(async () => ({
        contentFrame: mock.fn(async () => mockFrame)
      }));
      mockPage.waitForFunction = mock.fn(async () => {});

      await defaultExport.automatedLogin(mockPage, {
        THS_USER: 'altuser',
        THS_PASS: 'altpass'
      });

      assert.strictEqual(filledUsername, 'altuser');
      assert.strictEqual(filledPassword, 'altpass');
    });

    it('should click login link if present', async () => {
      const mockPage = createMockPage();
      const mockLoginLink = { click: mock.fn() };
      mockPage.$ = mock.fn(async () => mockLoginLink);

      const mockFrame = {
        click: mock.fn(),
        fill: mock.fn(),
        $: mock.fn(async () => ({ click: mock.fn() }))
      };

      mockPage.waitForSelector = mock.fn(async () => ({
        contentFrame: mock.fn(async () => mockFrame)
      }));
      mockPage.waitForFunction = mock.fn(async () => {});

      await defaultExport.automatedLogin(mockPage, {
        THSQUANT_USERNAME: 'user',
        THSQUANT_PASSWORD: 'pass'
      });

      assert.strictEqual(mockLoginLink.click.mock.calls.length, 1);
    });

    it('should fill iframe inputs', async () => {
      const mockPage = createMockPage();
      let filledInputs = [];

      const mockFrame = {
        click: mock.fn(),
        fill: mock.fn(async (selector, value) => {
          filledInputs.push({ selector, value });
        }),
        $: mock.fn(async () => ({ click: mock.fn() }))
      };

      mockPage.$ = mock.fn(async () => null);
      mockPage.waitForSelector = mock.fn(async () => ({
        contentFrame: mock.fn(async () => mockFrame)
      }));
      mockPage.waitForFunction = mock.fn(async () => {});

      await defaultExport.automatedLogin(mockPage, {
        THSQUANT_USERNAME: 'testuser',
        THSQUANT_PASSWORD: 'testpass'
      });

      assert.strictEqual(filledInputs.length, 2);
      assert.ok(filledInputs[0].selector.includes('uname'));
      assert.strictEqual(filledInputs[0].value, 'testuser');
      assert.ok(filledInputs[1].selector.includes('passwd'));
      assert.strictEqual(filledInputs[1].value, 'testpass');
    });

    it('should click submit button in iframe', async () => {
      const mockPage = createMockPage();
      const mockSubmitBtn = { click: mock.fn() };

      const mockFrame = {
        click: mock.fn(),
        fill: mock.fn(),
        $: mock.fn(async () => mockSubmitBtn)
      };

      mockPage.$ = mock.fn(async () => null);
      mockPage.waitForSelector = mock.fn(async () => ({
        contentFrame: mock.fn(async () => mockFrame)
      }));
      mockPage.waitForFunction = mock.fn(async () => {});

      await defaultExport.automatedLogin(mockPage, {
        THSQUANT_USERNAME: 'user',
        THSQUANT_PASSWORD: 'pass'
      });

      assert.strictEqual(mockSubmitBtn.click.mock.calls.length, 1);
    });

    it('should wait for iframe to disappear', async () => {
      const mockPage = createMockPage();
      let waitForFunctionCalled = false;

      const mockFrame = {
        click: mock.fn(),
        fill: mock.fn(),
        $: mock.fn(async () => ({ click: mock.fn() }))
      };

      mockPage.$ = mock.fn(async () => null);
      mockPage.waitForSelector = mock.fn(async () => ({
        contentFrame: mock.fn(async () => mockFrame)
      }));
      mockPage.waitForFunction = mock.fn(async () => {
        waitForFunctionCalled = true;
      });

      await defaultExport.automatedLogin(mockPage, {
        THSQUANT_USERNAME: 'user',
        THSQUANT_PASSWORD: 'pass'
      });

      assert.strictEqual(waitForFunctionCalled, true);
    });
  });
});