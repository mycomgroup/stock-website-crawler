import { describe, it, beforeEach, afterEach, mock } from 'node:test';
import assert from 'node:assert';
import defaultExport from '../sites/joinquant.js';

const createMockPage = () => ({
  locator: mock.fn(() => ({
    count: mock.fn(async () => 1),
    click: mock.fn(),
    fill: mock.fn(),
    check: mock.fn()
  })),
  waitForTimeout: mock.fn(),
  waitForURL: mock.fn(async () => {}),
  waitForLoadState: mock.fn(async () => {}),
  url: mock.fn(() => 'https://www.joinquant.com/algorithm/index/list')
});

const createMockResponse = (data, options = {}) => ({
  ok: options.ok ?? true,
  status: options.status ?? 200,
  text: mock.fn(async () => data),
  json: mock.fn(async () => data)
});

describe('joinquant site adapter', () => {
  let originalFetch;

  beforeEach(() => {
    originalFetch = global.fetch;
  });

  afterEach(() => {
    global.fetch = originalFetch;
  });

  describe('basic properties', () => {
    it('should have correct id', () => {
      assert.strictEqual(defaultExport.id, 'joinquant');
    });

    it('should have correct name', () => {
      assert.strictEqual(defaultExport.name, '聚宽');
    });

    it('should have correct domain', () => {
      assert.strictEqual(defaultExport.domain, '.joinquant.com');
    });

    it('should have correct loginUrl', () => {
      assert.strictEqual(defaultExport.loginUrl, 'https://www.joinquant.com/user/login');
    });

    it('should have correct dashboardUrl', () => {
      assert.strictEqual(defaultExport.dashboardUrl, 'https://www.joinquant.com/algorithm/index/list');
    });
  });

  describe('verifySession', () => {
    it('should return success when page contains logout text', async () => {
      global.fetch = mock.fn(async () => createMockResponse(
        '<html><body>退出</body></html>',
        { ok: true }
      ));

      const result = await defaultExport.verifySession([{ name: 'session', value: 'abc' }]);

      assert.strictEqual(result.success, true);
      assert.strictEqual(result.user, 'JoinQuant User');
    });

    it('should return success when page contains algorithmId', async () => {
      global.fetch = mock.fn(async () => createMockResponse(
        '<html><body>algorithmId: 12345</body></html>',
        { ok: true }
      ));

      const result = await defaultExport.verifySession([{ name: 'session', value: 'abc' }]);

      assert.strictEqual(result.success, true);
    });

    it('should return failure when page contains login text only', async () => {
      global.fetch = mock.fn(async () => createMockResponse(
        '<html><body>登录</body></html>',
        { ok: true }
      ));

      const result = await defaultExport.verifySession([{ name: 'session', value: 'abc' }]);

      assert.strictEqual(result.success, false);
      assert.strictEqual(result.message, '页面判定为未登录状态');
    });

    it('should return failure when HTTP status is not ok', async () => {
      global.fetch = mock.fn(async () => createMockResponse('', { 
        ok: false, 
        status: 401 
      }));

      const result = await defaultExport.verifySession([{ name: 'session', value: 'abc' }]);

      assert.strictEqual(result.success, false);
      assert.strictEqual(result.message, 'HTTP 401');
    });

    it('should handle network errors', async () => {
      global.fetch = mock.fn(async () => { 
        throw new Error('Network failed'); 
      });

      const result = await defaultExport.verifySession([{ name: 'session', value: 'abc' }]);

      assert.strictEqual(result.success, false);
      assert.strictEqual(result.message, 'Network failed');
    });

    it('should return failure when no recognizable features', async () => {
      global.fetch = mock.fn(async () => createMockResponse(
        '<html><body>Some random content</body></html>',
        { ok: true }
      ));

      const result = await defaultExport.verifySession([{ name: 'session', value: 'abc' }]);

      assert.strictEqual(result.success, false);
      assert.strictEqual(result.message, '无法识别登录特征');
    });

    it('should send correct headers', async () => {
      let capturedHeaders;
      global.fetch = mock.fn(async (url, options) => {
        capturedHeaders = options.headers;
        return createMockResponse('<html><body>退出</body></html>');
      });

      await defaultExport.verifySession([{ name: 's', value: 'v' }]);

      assert.ok(capturedHeaders.Cookie);
      assert.ok(capturedHeaders['User-Agent'].includes('Mozilla'));
      assert.strictEqual(capturedHeaders.Referer, 'https://www.joinquant.com/');
    });
  });

  describe('checkLoggedIn', () => {
    it('should return true when URL does not contain /user/login', async () => {
      const mockPage = createMockPage();
      mockPage.url = mock.fn(() => 'https://www.joinquant.com/algorithm/index');

      const result = await defaultExport.checkLoggedIn(mockPage);

      assert.strictEqual(result, true);
    });

    it('should return false when URL contains /user/login', async () => {
      const mockPage = createMockPage();
      mockPage.url = mock.fn(() => 'https://www.joinquant.com/user/login');

      const result = await defaultExport.checkLoggedIn(mockPage);

      assert.strictEqual(result, false);
    });
  });

  describe('automatedLogin', () => {
    it('should throw error when credentials are missing', async () => {
      const mockPage = createMockPage();

      await assert.rejects(
        defaultExport.automatedLogin(mockPage, {}),
        { message: '未发现聚宽账号凭证' }
      );
    });

    it('should throw error when only username is provided', async () => {
      const mockPage = createMockPage();

      await assert.rejects(
        defaultExport.automatedLogin(mockPage, { JOINQUANT_USERNAME: 'user' }),
        { message: '未发现聚宽账号凭证' }
      );
    });

    it('should use alternative credential keys', async () => {
      const mockPage = createMockPage();
      let filledValues = [];

      mockPage.locator = mock.fn((selector) => ({
        count: mock.fn(async () => 1),
        click: mock.fn(),
        fill: mock.fn(async (v) => { filledValues.push(v); }),
        check: mock.fn()
      }));

      await defaultExport.automatedLogin(mockPage, {
        JOINQUANT_USER: 'altuser',
        JOINQUANT_PASS: 'altpass'
      });

      assert.ok(filledValues.includes('altuser'));
      assert.ok(filledValues.includes('altpass'));
    });

    it('should throw error when username input not found', async () => {
      const mockPage = createMockPage();

      mockPage.locator = mock.fn(() => ({
        count: mock.fn(async () => 0),
        click: mock.fn(),
        fill: mock.fn()
      }));

      await assert.rejects(
        defaultExport.automatedLogin(mockPage, {
          JOINQUANT_USERNAME: 'user',
          JOINQUANT_PASSWORD: 'pass'
        }),
        { message: '未找到用户名或密码输入框' }
      );
    });

    it('should click password login tab', async () => {
      const mockPage = createMockPage();
      let clickedSelectors = [];

      mockPage.locator = mock.fn((selector) => ({
        count: mock.fn(async () => 1),
        click: mock.fn(async () => { clickedSelectors.push(selector); }),
        fill: mock.fn(),
        check: mock.fn()
      }));

      await defaultExport.automatedLogin(mockPage, {
        JOINQUANT_USERNAME: 'user',
        JOINQUANT_PASSWORD: 'pass'
      });

      assert.ok(clickedSelectors.some(s => s.includes('密码登录')));
    });

    it('should check agreement checkbox', async () => {
      const mockPage = createMockPage();
      let checkedSelectors = [];

      mockPage.locator = mock.fn((selector) => ({
        count: mock.fn(async () => 1),
        click: mock.fn(),
        fill: mock.fn(),
        check: mock.fn(async () => { checkedSelectors.push(selector); })
      }));

      await defaultExport.automatedLogin(mockPage, {
        JOINQUANT_USERNAME: 'user',
        JOINQUANT_PASSWORD: 'pass'
      });

      assert.ok(checkedSelectors.some(s => s.includes('checkbox')));
    });

    it('should click submit button when found', async () => {
      const mockPage = createMockPage();
      let clickedSelectors = [];

      mockPage.locator = mock.fn((selector) => ({
        count: mock.fn(async () => selector.includes('btnPwdSubmit') ? 1 : 0),
        click: mock.fn(async () => { clickedSelectors.push(selector); }),
        fill: mock.fn(),
        check: mock.fn()
      }));

      await defaultExport.automatedLogin(mockPage, {
        JOINQUANT_USERNAME: 'user',
        JOINQUANT_PASSWORD: 'pass'
      });

      assert.ok(clickedSelectors.some(s => s.includes('btnPwdSubmit')));
    });

    it('should clear inputs before filling', async () => {
      const mockPage = createMockPage();
      let fillCalls = [];

      mockPage.locator = mock.fn((selector) => ({
        count: mock.fn(async () => 1),
        click: mock.fn(),
        fill: mock.fn(async (v) => { fillCalls.push({ selector, value: v }); }),
        check: mock.fn()
      }));

      await defaultExport.automatedLogin(mockPage, {
        JOINQUANT_USERNAME: 'user',
        JOINQUANT_PASSWORD: 'pass'
      });

      const usernameFills = fillCalls.filter(c => c.selector.includes('username'));
      assert.ok(usernameFills.some(c => c.value === ''));
      assert.ok(usernameFills.some(c => c.value === 'user'));
    });
  });
});