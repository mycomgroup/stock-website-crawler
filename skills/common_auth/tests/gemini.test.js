import { describe, it, beforeEach, afterEach, mock } from 'node:test';
import assert from 'node:assert';
import defaultExport from '../sites/gemini.js';

const createMockPage = () => ({
  $: mock.fn(),
  waitForTimeout: mock.fn(),
  url: mock.fn(() => 'https://gemini.google.com/app')
});

const createMockResponse = (data, options = {}) => ({
  ok: options.ok ?? true,
  status: options.status ?? 200,
  json: mock.fn(async () => data),
  text: mock.fn(async () => typeof data === 'string' ? data : JSON.stringify(data))
});

describe('gemini site adapter', () => {
  let originalFetch;

  beforeEach(() => {
    originalFetch = global.fetch;
  });

  afterEach(() => {
    global.fetch = originalFetch;
  });

  describe('basic properties', () => {
    it('should have correct id', () => {
      assert.strictEqual(defaultExport.id, 'gemini');
    });

    it('should have correct name', () => {
      assert.strictEqual(defaultExport.name, 'Gemini');
    });

    it('should have correct domain', () => {
      assert.strictEqual(defaultExport.domain, '.google.com');
    });

    it('should have correct loginUrl', () => {
      assert.strictEqual(defaultExport.loginUrl, 'https://gemini.google.com/');
    });

    it('should have correct dashboardUrl', () => {
      assert.strictEqual(defaultExport.dashboardUrl, 'https://gemini.google.com/app');
    });
  });

  describe('verifySession', () => {
    it('should return true when API returns email', async () => {
      global.fetch = mock.fn(async () => createMockResponse({
        email: 'test@gmail.com'
      }));

      const result = await defaultExport.verifySession([{ name: 'session', value: 'abc123' }]);

      assert.strictEqual(result, true);
    });

    it('should return true when API returns id', async () => {
      global.fetch = mock.fn(async () => createMockResponse({
        id: 'user123'
      }));

      const result = await defaultExport.verifySession([{ name: 'session', value: 'abc123' }]);

      assert.strictEqual(result, true);
    });

    it('should return true when API returns user_id', async () => {
      global.fetch = mock.fn(async () => createMockResponse({
        user_id: 'user456'
      }));

      const result = await defaultExport.verifySession([{ name: 'session', value: 'abc123' }]);

      assert.strictEqual(result, true);
    });

    it('should return false when no user identifier in response', async () => {
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

    it('should fallback to HTML check on API error', async () => {
      let callCount = 0;
      global.fetch = mock.fn(async () => {
        callCount++;
        if (callCount === 1) {
          throw new Error('API error');
        }
        return createMockResponse('<html><body class="signed-in">Content</body></html>', { status: 200 });
      });

      const result = await defaultExport.verifySession([{ name: 'session', value: 'abc123' }]);

      assert.strictEqual(result, true);
    });

    it('should fallback and detect Gemini in HTML', async () => {
      let callCount = 0;
      global.fetch = mock.fn(async () => {
        callCount++;
        if (callCount === 1) {
          throw new Error('API error');
        }
        return createMockResponse('<html><title>Gemini</title></html>', { status: 200 });
      });

      const result = await defaultExport.verifySession([{ name: 'session', value: 'abc123' }]);

      assert.strictEqual(result, true);
    });

    it('should return false when both API and fallback fail', async () => {
      global.fetch = mock.fn(async () => { throw new Error('Network error'); });

      const result = await defaultExport.verifySession([{ name: 'session', value: 'abc123' }]);

      assert.strictEqual(result, false);
    });

    it('should return false when fallback HTML does not contain signed-in or Gemini', async () => {
      let callCount = 0;
      global.fetch = mock.fn(async () => {
        callCount++;
        if (callCount === 1) {
          throw new Error('API error');
        }
        return createMockResponse('<html><body>Please sign in</body></html>', { status: 200 });
      });

      const result = await defaultExport.verifySession([{ name: 'session', value: 'abc123' }]);

      assert.strictEqual(result, false);
    });

    it('should send correct headers to API', async () => {
      let capturedHeaders;
      global.fetch = mock.fn(async (url, options) => {
        if (url.includes('/api/user/info')) {
          capturedHeaders = options.headers;
        }
        return createMockResponse({ email: 'test@gmail.com' });
      });

      await defaultExport.verifySession([{ name: 's', value: 'v' }]);

      assert.strictEqual(capturedHeaders.Cookie, 's=v');
      assert.ok(capturedHeaders['User-Agent'].includes('Mozilla'));
    });

    it('should handle null response from API', async () => {
      global.fetch = mock.fn(async () => createMockResponse(null));

      const result = await defaultExport.verifySession([{ name: 'session', value: 'abc123' }]);

      assert.strictEqual(result, false);
    });

    it('should handle empty object response from API', async () => {
      global.fetch = mock.fn(async () => createMockResponse({}));

      const result = await defaultExport.verifySession([{ name: 'session', value: 'abc123' }]);

      assert.strictEqual(result, false);
    });
  });

  describe('checkLoggedIn', () => {
    it('should return true when chat input is present and no sign in button', async () => {
      const mockPage = createMockPage();
      mockPage.$ = mock.fn(async (selector) => {
        if (selector.includes('textarea')) return {};
        return null;
      });

      const result = await defaultExport.checkLoggedIn(mockPage);

      assert.strictEqual(result, true);
    });

    it('should return false when sign in button is present', async () => {
      const mockPage = createMockPage();
      mockPage.$ = mock.fn(async () => ({}));

      const result = await defaultExport.checkLoggedIn(mockPage);

      assert.strictEqual(result, false);
    });

    it('should return false when URL contains /signin', async () => {
      const mockPage = createMockPage();
      mockPage.url = mock.fn(() => 'https://gemini.google.com/signin');
      mockPage.$ = mock.fn(async () => { throw new Error('Not found'); });

      const result = await defaultExport.checkLoggedIn(mockPage);

      assert.strictEqual(result, false);
    });

    it('should return false when URL contains accounts.google.com', async () => {
      const mockPage = createMockPage();
      mockPage.url = mock.fn(() => 'https://accounts.google.com/signin');
      mockPage.$ = mock.fn(async () => { throw new Error('Not found'); });

      const result = await defaultExport.checkLoggedIn(mockPage);

      assert.strictEqual(result, false);
    });

    it('should return true when URL is dashboard and no errors', async () => {
      const mockPage = createMockPage();
      mockPage.$ = mock.fn(async (selector) => {
        if (selector.includes('textarea') || selector.includes('chat-input')) return {};
        return null;
      });

      const result = await defaultExport.checkLoggedIn(mockPage);

      assert.strictEqual(result, true);
    });

    it('should return false when chat input exists but sign in button also exists', async () => {
      const mockPage = createMockPage();
      mockPage.$ = mock.fn(async () => ({}));

      const result = await defaultExport.checkLoggedIn(mockPage);

      assert.strictEqual(result, false);
    });

    it('should handle element selector errors gracefully', async () => {
      const mockPage = createMockPage();
      mockPage.$ = mock.fn(async () => { throw new Error('Selector error'); });
      mockPage.url = mock.fn(() => 'https://gemini.google.com/app');

      const result = await defaultExport.checkLoggedIn(mockPage);

      assert.strictEqual(result, true);
    });
  });

  describe('automatedLogin', () => {
    it('should throw error when credentials are missing', async () => {
      const mockPage = createMockPage();

      await assert.rejects(
        defaultExport.automatedLogin(mockPage, {}),
        { message: '未发现 Google/Gemini 号凭证' }
      );
    });

    it('should throw error when only username is provided', async () => {
      const mockPage = createMockPage();

      await assert.rejects(
        defaultExport.automatedLogin(mockPage, { GEMINI_USERNAME: 'user' }),
        { message: '未发现 Google/Gemini 号凭证' }
      );
    });

    it('should use alternative credential keys (GOOGLE_EMAIL/GOOGLE_PASSWORD)', async () => {
      const mockPage = createMockPage();
      let filledEmail;
      let filledPassword;

      mockPage.$ = mock.fn(async (selector) => {
        if (selector.includes('email')) {
          return {
            fill: mock.fn(async (v) => { filledEmail = v; })
          };
        }
        if (selector.includes('password')) {
          return {
            fill: mock.fn(async (v) => { filledPassword = v; })
          };
        }
        if (selector.includes('Next') || selector.includes('submit')) {
          return { click: mock.fn() };
        }
        return null;
      });

      await defaultExport.automatedLogin(mockPage, {
        GOOGLE_EMAIL: 'altuser@gmail.com',
        GOOGLE_PASSWORD: 'altpass'
      });

      assert.strictEqual(filledEmail, 'altuser@gmail.com');
      assert.strictEqual(filledPassword, 'altpass');
    });

    it('should click sign in button if present', async () => {
      const mockPage = createMockPage();
      const mockSignInBtn = { click: mock.fn() };

      mockPage.$ = mock.fn(async (selector) => {
        if (selector.includes('Sign in')) return mockSignInBtn;
        return null;
      });

      await defaultExport.automatedLogin(mockPage, {
        GEMINI_USERNAME: 'user@gmail.com',
        GEMINI_PASSWORD: 'password'
      });

      assert.strictEqual(mockSignInBtn.click.mock.calls.length, 1);
    });

    it('should fill email and click next button', async () => {
      const mockPage = createMockPage();
      const mockEmailInput = { fill: mock.fn() };
      const mockNextBtn = { click: mock.fn() };

      mockPage.$ = mock.fn(async (selector) => {
        if (selector.includes('email')) return mockEmailInput;
        if (selector.includes('Next') || selector.includes('submit')) return mockNextBtn;
        return null;
      });

      await defaultExport.automatedLogin(mockPage, {
        GEMINI_USERNAME: 'user@gmail.com',
        GEMINI_PASSWORD: 'password'
      });

      assert.strictEqual(mockEmailInput.fill.mock.calls.length, 1);
      assert.strictEqual(mockEmailInput.fill.mock.calls[0][0], 'user@gmail.com');
      assert.ok(mockNextBtn.click.mock.calls.length >= 1);
    });

    it('should fill password and click next button', async () => {
      const mockPage = createMockPage();
      const mockPasswordInput = { fill: mock.fn() };
      const mockNextBtn = { click: mock.fn() };

      mockPage.$ = mock.fn(async (selector) => {
        if (selector.includes('password')) return mockPasswordInput;
        if (selector.includes('Next') || selector.includes('submit')) return mockNextBtn;
        return null;
      });

      await defaultExport.automatedLogin(mockPage, {
        GEMINI_USERNAME: 'user@gmail.com',
        GEMINI_PASSWORD: 'mypassword'
      });

      assert.strictEqual(mockPasswordInput.fill.mock.calls.length, 1);
      assert.strictEqual(mockPasswordInput.fill.mock.calls[0][0], 'mypassword');
      assert.ok(mockNextBtn.click.mock.calls.length >= 1);
    });

    it('should work without sign in button', async () => {
      const mockPage = createMockPage();
      const mockEmailInput = { fill: mock.fn() };
      const mockPasswordInput = { fill: mock.fn() };

      mockPage.$ = mock.fn(async (selector) => {
        if (selector.includes('email')) return mockEmailInput;
        if (selector.includes('password')) return mockPasswordInput;
        return null;
      });

      await defaultExport.automatedLogin(mockPage, {
        GEMINI_USERNAME: 'user@gmail.com',
        GEMINI_PASSWORD: 'password'
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
        GEMINI_USERNAME: 'user@gmail.com',
        GEMINI_PASSWORD: 'password'
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
        GEMINI_USERNAME: 'user@gmail.com',
        GEMINI_PASSWORD: 'password'
      });

      assert.strictEqual(mockEmailInput.fill.mock.calls.length, 1);
    });

    it('should call waitForTimeout multiple times', async () => {
      const mockPage = createMockPage();

      mockPage.$ = mock.fn(async () => ({ fill: mock.fn(), click: mock.fn() }));

      await defaultExport.automatedLogin(mockPage, {
        GEMINI_USERNAME: 'user@gmail.com',
        GEMINI_PASSWORD: 'password'
      });

      assert.ok(mockPage.waitForTimeout.mock.calls.length >= 1);
    });

    it('should handle anchor tag sign in button', async () => {
      const mockPage = createMockPage();
      const mockSignInLink = { click: mock.fn() };

      mockPage.$ = mock.fn(async (selector) => {
        if (selector.includes('Sign in') && selector.includes('a:')) return mockSignInLink;
        return null;
      });

      await defaultExport.automatedLogin(mockPage, {
        GEMINI_USERNAME: 'user@gmail.com',
        GEMINI_PASSWORD: 'password'
      });

      assert.strictEqual(mockSignInLink.click.mock.calls.length, 1);
    });
  });
});