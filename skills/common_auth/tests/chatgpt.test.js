import { describe, it, beforeEach, afterEach, mock } from 'node:test';
import assert from 'node:assert';
import defaultExport from '../sites/chatgpt.js';

const createMockPage = () => ({
  $: mock.fn(),
  waitForTimeout: mock.fn(),
  url: mock.fn(() => 'https://chatgpt.com/')
});

const createMockResponse = (data, options = {}) => ({
  ok: options.ok ?? true,
  status: options.status ?? 200,
  json: mock.fn(async () => data),
  text: mock.fn(async () => typeof data === 'string' ? data : JSON.stringify(data))
});

describe('chatgpt site adapter', () => {
  let originalFetch;

  beforeEach(() => {
    originalFetch = global.fetch;
  });

  afterEach(() => {
    global.fetch = originalFetch;
  });

  describe('basic properties', () => {
    it('should have correct id', () => {
      assert.strictEqual(defaultExport.id, 'chatgpt');
    });

    it('should have correct name', () => {
      assert.strictEqual(defaultExport.name, 'ChatGPT');
    });

    it('should have correct domain', () => {
      assert.strictEqual(defaultExport.domain, 'chatgpt.com');
    });

    it('should have correct loginUrl', () => {
      assert.strictEqual(defaultExport.loginUrl, 'https://chatgpt.com/auth/login');
    });

    it('should have correct dashboardUrl', () => {
      assert.strictEqual(defaultExport.dashboardUrl, 'https://chatgpt.com/');
    });
  });

  describe('verifySession', () => {
    it('should return true when API returns valid user data', async () => {
      global.fetch = mock.fn(async () => createMockResponse({
        id: 'user123',
        email: 'test@example.com'
      }));

      const result = await defaultExport.verifySession([{ name: 'session', value: 'abc123' }]);

      assert.strictEqual(result, true);
    });

    it('should return false when id is missing', async () => {
      global.fetch = mock.fn(async () => createMockResponse({
        email: 'test@example.com'
      }));

      const result = await defaultExport.verifySession([{ name: 'session', value: 'abc123' }]);

      assert.strictEqual(result, false);
    });

    it('should return false when email is missing', async () => {
      global.fetch = mock.fn(async () => createMockResponse({
        id: 'user123'
      }));

      const result = await defaultExport.verifySession([{ name: 'session', value: 'abc123' }]);

      assert.strictEqual(result, false);
    });

    it('should return false when both id and email are missing', async () => {
      global.fetch = mock.fn(async () => createMockResponse({
        name: 'Test User'
      }));

      const result = await defaultExport.verifySession([{ name: 'session', value: 'abc123' }]);

      assert.strictEqual(result, false);
    });

    it('should return false when HTTP status is not ok', async () => {
      global.fetch = mock.fn(async () => createMockResponse({}, { ok: false, status: 401 }));

      const result = await defaultExport.verifySession([{ name: 'session', value: 'abc123' }]);

      assert.strictEqual(result, false);
    });

    it('should return false on network error', async () => {
      global.fetch = mock.fn(async () => { throw new Error('Network error'); });

      const result = await defaultExport.verifySession([{ name: 'session', value: 'abc123' }]);

      assert.strictEqual(result, false);
    });

    it('should return false on JSON parse error', async () => {
      global.fetch = mock.fn(async () => ({
        ok: true,
        status: 200,
        json: mock.fn(async () => { throw new Error('Invalid JSON'); })
      }));

      const result = await defaultExport.verifySession([{ name: 'session', value: 'abc123' }]);

      assert.strictEqual(result, false);
    });

    it('should send correct headers', async () => {
      let capturedHeaders;
      global.fetch = mock.fn(async (url, options) => {
        capturedHeaders = options.headers;
        return createMockResponse({ id: '123', email: 'test@test.com' });
      });

      await defaultExport.verifySession([{ name: 's', value: 'v' }]);

      assert.strictEqual(capturedHeaders.Cookie, 's=v');
      assert.ok(capturedHeaders['User-Agent'].includes('Mozilla'));
    });

    it('should handle empty cookies array', async () => {
      global.fetch = mock.fn(async () => createMockResponse({
        id: 'user123',
        email: 'test@example.com'
      }));

      const result = await defaultExport.verifySession([]);

      assert.strictEqual(result, true);
    });
  });

  describe('checkLoggedIn', () => {
    it('should return false when URL contains /auth/login', async () => {
      const mockPage = createMockPage();
      mockPage.url = mock.fn(() => 'https://chatgpt.com/auth/login');

      const result = await defaultExport.checkLoggedIn(mockPage);

      assert.strictEqual(result, false);
    });

    it('should return false when URL contains /signup', async () => {
      const mockPage = createMockPage();
      mockPage.url = mock.fn(() => 'https://chatgpt.com/signup');

      const result = await defaultExport.checkLoggedIn(mockPage);

      assert.strictEqual(result, false);
    });

    it('should return true when chat input is present', async () => {
      const mockPage = createMockPage();
      mockPage.$ = mock.fn(async () => ({}));

      const result = await defaultExport.checkLoggedIn(mockPage);

      assert.strictEqual(result, true);
    });

    it('should return false when chat input is not present', async () => {
      const mockPage = createMockPage();
      mockPage.$ = mock.fn(async () => null);

      const result = await defaultExport.checkLoggedIn(mockPage);

      assert.strictEqual(result, false);
    });

    it('should return false when URL contains /auth and element not found', async () => {
      const mockPage = createMockPage();
      mockPage.url = mock.fn(() => 'https://chatgpt.com/auth/verify');
      mockPage.$ = mock.fn(async () => { throw new Error('Not found'); });

      const result = await defaultExport.checkLoggedIn(mockPage);

      assert.strictEqual(result, false);
    });

    it('should return true when URL is dashboard and no errors', async () => {
      const mockPage = createMockPage();
      mockPage.url = mock.fn(() => 'https://chatgpt.com/');
      mockPage.$ = mock.fn(async () => ({}));

      const result = await defaultExport.checkLoggedIn(mockPage);

      assert.strictEqual(result, true);
    });

    it('should detect chat input with data-testid', async () => {
      const mockPage = createMockPage();
      mockPage.$ = mock.fn(async (selector) => {
        if (selector.includes('chat-input')) return {};
        return null;
      });

      const result = await defaultExport.checkLoggedIn(mockPage);

      assert.strictEqual(result, true);
    });

    it('should detect chat input with textarea placeholder', async () => {
      const mockPage = createMockPage();
      mockPage.$ = mock.fn(async (selector) => {
        if (selector.includes('Message')) return {};
        return null;
      });

      const result = await defaultExport.checkLoggedIn(mockPage);

      assert.strictEqual(result, true);
    });
  });

  describe('automatedLogin', () => {
    it('should throw error when credentials are missing', async () => {
      const mockPage = createMockPage();

      await assert.rejects(
        defaultExport.automatedLogin(mockPage, {}),
        { message: '未发现 ChatGPT 账号凭证' }
      );
    });

    it('should throw error when only username is provided', async () => {
      const mockPage = createMockPage();

      await assert.rejects(
        defaultExport.automatedLogin(mockPage, { CHATGPT_USERNAME: 'user' }),
        { message: '未发现 ChatGPT 账号凭证' }
      );
    });

    it('should use alternative credential keys', async () => {
      const mockPage = createMockPage();
      let filledEmail;

      mockPage.$ = mock.fn(async (selector) => {
        if (selector.includes('email')) {
          return {
            fill: mock.fn(async (v) => { filledEmail = v; })
          };
        }
        if (selector.includes('password')) {
          return {
            fill: mock.fn()
          };
        }
        if (selector.includes('Continue') || selector.includes('submit')) {
          return { click: mock.fn() };
        }
        return null;
      });

      await defaultExport.automatedLogin(mockPage, {
        OPENAI_EMAIL: 'altuser@example.com',
        OPENAI_PASSWORD: 'altpass'
      });

      assert.strictEqual(filledEmail, 'altuser@example.com');
    });

    it('should click login button if present', async () => {
      const mockPage = createMockPage();
      const mockLoginBtn = { click: mock.fn() };

      mockPage.$ = mock.fn(async (selector) => {
        if (selector.includes('Log in') || selector.includes('登录')) {
          return mockLoginBtn;
        }
        return null;
      });

      await defaultExport.automatedLogin(mockPage, {
        CHATGPT_USERNAME: 'user@example.com',
        CHATGPT_PASSWORD: 'password'
      });

      assert.strictEqual(mockLoginBtn.click.mock.calls.length, 1);
    });

    it('should fill email and click continue button', async () => {
      const mockPage = createMockPage();
      const mockEmailInput = { fill: mock.fn() };
      const mockContinueBtn = { click: mock.fn() };

      mockPage.$ = mock.fn(async (selector) => {
        if (selector.includes('email')) return mockEmailInput;
        if (selector.includes('Continue') || selector.includes('submit')) return mockContinueBtn;
        return null;
      });

      await defaultExport.automatedLogin(mockPage, {
        CHATGPT_USERNAME: 'user@example.com',
        CHATGPT_PASSWORD: 'password'
      });

      assert.strictEqual(mockEmailInput.fill.mock.calls.length, 1);
      assert.strictEqual(mockEmailInput.fill.mock.calls[0][0], 'user@example.com');
      assert.ok(mockContinueBtn.click.mock.calls.length >= 1);
    });

    it('should fill password and click submit', async () => {
      const mockPage = createMockPage();
      const mockPasswordInput = { fill: mock.fn() };
      const mockSubmitBtn = { click: mock.fn() };

      mockPage.$ = mock.fn(async (selector) => {
        if (selector.includes('password')) return mockPasswordInput;
        if (selector.includes('Continue') || selector.includes('submit')) return mockSubmitBtn;
        return null;
      });

      await defaultExport.automatedLogin(mockPage, {
        CHATGPT_USERNAME: 'user@example.com',
        CHATGPT_PASSWORD: 'mypassword'
      });

      assert.strictEqual(mockPasswordInput.fill.mock.calls.length, 1);
      assert.strictEqual(mockPasswordInput.fill.mock.calls[0][0], 'mypassword');
      assert.ok(mockSubmitBtn.click.mock.calls.length >= 1);
    });

    it('should work without login button', async () => {
      const mockPage = createMockPage();
      const mockEmailInput = { fill: mock.fn() };
      const mockPasswordInput = { fill: mock.fn() };

      mockPage.$ = mock.fn(async (selector) => {
        if (selector.includes('email')) return mockEmailInput;
        if (selector.includes('password')) return mockPasswordInput;
        return null;
      });

      await defaultExport.automatedLogin(mockPage, {
        CHATGPT_USERNAME: 'user@example.com',
        CHATGPT_PASSWORD: 'password'
      });

      assert.strictEqual(mockEmailInput.fill.mock.calls.length, 1);
      assert.strictEqual(mockPasswordInput.fill.mock.calls.length, 1);
    });

    it('should work without email input', async () => {
      const mockPage = createMockPage();
      const mockPasswordInput = { fill: mock.fn() };

      mockPage.$ = mock.fn(async (selector) => {
        if (selector.includes('password')) return mockPasswordInput;
        return null;
      });

      await defaultExport.automatedLogin(mockPage, {
        CHATGPT_USERNAME: 'user@example.com',
        CHATGPT_PASSWORD: 'password'
      });

      assert.strictEqual(mockPasswordInput.fill.mock.calls.length, 1);
    });

    it('should work without password input', async () => {
      const mockPage = createMockPage();
      const mockEmailInput = { fill: mock.fn() };

      mockPage.$ = mock.fn(async (selector) => {
        if (selector.includes('email')) return mockEmailInput;
        return null;
      });

      await defaultExport.automatedLogin(mockPage, {
        CHATGPT_USERNAME: 'user@example.com',
        CHATGPT_PASSWORD: 'password'
      });

      assert.strictEqual(mockEmailInput.fill.mock.calls.length, 1);
    });

    it('should call waitForTimeout multiple times', async () => {
      const mockPage = createMockPage();

      mockPage.$ = mock.fn(async () => ({ fill: mock.fn(), click: mock.fn() }));

      await defaultExport.automatedLogin(mockPage, {
        CHATGPT_USERNAME: 'user@example.com',
        CHATGPT_PASSWORD: 'password'
      });

      assert.ok(mockPage.waitForTimeout.mock.calls.length >= 1);
    });
  });
});