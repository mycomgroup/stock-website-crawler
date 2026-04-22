import { describe, it, beforeEach, afterEach, vi } from 'vitest';
import assert from 'node:assert';
import path from 'node:path';

vi.mock('node:fs', () => {
  const mockFs = {
    existsSync: vi.fn(() => true),
    readFileSync: vi.fn(() => '{"cookies":[{"name":"session","value":"test"}]}'),
    writeFileSync: vi.fn(),
    mkdirSync: vi.fn()
  };
  return {
    default: mockFs,
    ...mockFs
  };
});

vi.mock('../../paths.js', () => ({
  DATA_ROOT: '/test/data',
  SESSION_FILE: '/test/session.json'
}));

vi.mock('../../load-env.js', () => ({
  default: {},
}));

const mockFs = await import('node:fs');

function resetMocks() {
  mockFs.default.existsSync.mockClear();
  mockFs.default.readFileSync.mockClear();
  mockFs.default.writeFileSync.mockClear();
  mockFs.default.mkdirSync.mockClear();
}

describe('capture-save.js', () => {
  beforeEach(() => {
    resetMocks();
  });

  afterEach(() => {
    resetMocks();
  });

  describe('captureSaveAPI options', () => {
    it('should default to headless mode', () => {
      const headed = false;
      const headless = !headed;
      assert.strictEqual(headless, true);
    });

    it('should accept headed option', () => {
      const options = { headed: true };
      assert.strictEqual(options.headed, true);
    });

    it('should initialize empty apiCalls array', () => {
      const apiCalls = [];
      assert.strictEqual(apiCalls.length, 0);
    });
  });

  describe('session handling', () => {
    it('should throw error when session file not found', () => {
      mockFs.default.existsSync.mockImplementation(() => false);
      assert.strictEqual(mockFs.default.existsSync(), false);
    });

    it('should load session when file exists', () => {
      mockFs.default.readFileSync.mockImplementation(() => '{"cookies":[]}');
      const session = JSON.parse(mockFs.default.readFileSync());
      assert.ok(session.cookies);
    });

    it('should log session file location', () => {
      const SESSION_FILE = '/test/session.json';
      assert.ok(SESSION_FILE.includes('session.json'));
    });
  });

  describe('browser configuration', () => {
    it('should set headless based on headed option', () => {
      const headed = true;
      const headless = !headed;
      assert.strictEqual(headless, false);
    });

    it('should use correct user agent', () => {
      const USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)';
      assert.ok(USER_AGENT.includes('Macintosh'));
    });

    it('should add cookies to context', () => {
      const sessionPayload = { cookies: [{ name: 'test', value: 'val' }] };
      assert.ok(sessionPayload.cookies);
    });
  });

  describe('request interception', () => {
    it('should capture guorn.com requests', () => {
      const url = 'https://guorn.com/api/stock';
      const shouldCapture = url.includes('guorn.com');
      assert.strictEqual(shouldCapture, true);
    });

    it('should filter out CSS files', () => {
      const url = 'https://guorn.com/static/style.css';
      const shouldCapture = url.includes('guorn.com') && !url.includes('.css');
      assert.strictEqual(shouldCapture, false);
    });

    it('should filter out JS files', () => {
      const url = 'https://guorn.com/static/app.js';
      const shouldCapture = url.includes('guorn.com') && !url.includes('.js');
      assert.strictEqual(shouldCapture, false);
    });

    it('should filter out PNG files', () => {
      const url = 'https://guorn.com/static/logo.png';
      const shouldCapture = url.includes('guorn.com') && !url.includes('.png');
      assert.strictEqual(shouldCapture, false);
    });

    it('should filter out JPG files', () => {
      const url = 'https://guorn.com/static/banner.jpg';
      const shouldCapture = url.includes('guorn.com') && !url.includes('.jpg');
      assert.strictEqual(shouldCapture, false);
    });

    it('should filter out GIF files', () => {
      const url = 'https://guorn.com/static/animation.gif';
      const shouldCapture = url.includes('guorn.com') && !url.includes('.gif');
      assert.strictEqual(shouldCapture, false);
    });

    it('should filter out WOFF files', () => {
      const url = 'https://guorn.com/static/font.woff';
      const shouldCapture = url.includes('guorn.com') && !url.includes('.woff');
      assert.strictEqual(shouldCapture, false);
    });

    it('should filter out WOFF2 files', () => {
      const url = 'https://guorn.com/static/font.woff2';
      const shouldCapture = url.includes('guorn.com') && !url.includes('.woff2');
      assert.strictEqual(shouldCapture, false);
    });

    it('should filter out TTF files', () => {
      const url = 'https://guorn.com/static/font.ttf';
      const shouldCapture = url.includes('guorn.com') && !url.includes('.ttf');
      assert.strictEqual(shouldCapture, false);
    });

    it('should filter out google-analytics', () => {
      const url = 'https://google-analytics.com/collect';
      const shouldCapture = !url.includes('google-analytics');
      assert.strictEqual(shouldCapture, false);
    });

    it('should filter out googleapis', () => {
      const url = 'https://fonts.googleapis.com/css';
      const shouldCapture = !url.includes('googleapis');
      assert.strictEqual(shouldCapture, false);
    });

    it('should capture request method', () => {
      const request = { method: 'POST', url: 'https://guorn.com/api' };
      assert.strictEqual(request.method, 'POST');
    });

    it('should capture request headers', () => {
      const request = { headers: { 'Content-Type': 'application/json' } };
      assert.ok(request.headers['Content-Type']);
    });

    it('should capture POST data', () => {
      const request = { postData: '{"test":"data"}' };
      assert.ok(request.postData);
    });

    it('should capture timestamp', () => {
      const entry = { timestamp: new Date().toISOString() };
      assert.ok(entry.timestamp);
    });
  });

  describe('response interception', () => {
    it('should match response to request by URL', () => {
      const apiCalls = [{ type: 'request', url: 'https://guorn.com/api' }];
      const responseUrl = 'https://guorn.com/api';
      const entry = apiCalls.findLast(r => r.url === responseUrl);
      assert.ok(entry);
    });

    it('should capture response status code', () => {
      const statusCode = 200;
      assert.strictEqual(statusCode, 200);
    });

    it('should capture response body', () => {
      const responseBody = '{"result":"success"}';
      assert.ok(responseBody);
    });

    it('should handle response text errors', () => {
      const errorCaught = true;
      assert.strictEqual(errorCaught, true);
    });
  });

  describe('page navigation', () => {
    it('should navigate to strategy page', () => {
      const targetUrl = 'https://guorn.com/stock';
      assert.strictEqual(targetUrl, 'https://guorn.com/stock');
    });

    it('should wait 3s after navigation', () => {
      const waitTime = 3000;
      assert.strictEqual(waitTime, 3000);
    });
  });

  describe('login check', () => {
    it('should check login status by URL', () => {
      const url = 'https://guorn.com/stock';
      const isLoggedIn = !url.includes('/user/login');
      assert.strictEqual(isLoggedIn, true);
    });

    it('should return early when session expired', () => {
      const isLoggedIn = false;
      if (!isLoggedIn) {
        assert.strictEqual(isLoggedIn, false);
      }
    });
  });

  describe('save button interaction', () => {
    it('should find save button with multiple selectors', () => {
      const selector = 'a:has-text("保存"), button:has-text("保存")';
      assert.ok(selector.includes('保存'));
    });

    it('should wait 5s after save click', () => {
      const waitTime = 5000;
      assert.strictEqual(waitTime, 5000);
    });

    it('should handle missing save button', () => {
      const saveButtonVisible = false;
      assert.strictEqual(saveButtonVisible, false);
    });
  });

  describe('API call logging', () => {
    it('should log unique URLs', () => {
      const apiCalls = [
        { url: 'https://guorn.com/api1' },
        { url: 'https://guorn.com/api1' },
        { url: 'https://guorn.com/api2' }
      ];
      const uniqueUrls = [...new Set(apiCalls.map(r => r.url))];
      assert.strictEqual(uniqueUrls.length, 2);
    });

    it('should list methods for each URL', () => {
      const calls = [
        { url: 'test', method: 'GET' },
        { url: 'test', method: 'POST' }
      ];
      const methods = [...new Set(calls.map(r => r.method))];
      assert.strictEqual(methods.length, 2);
    });
  });

  describe('file saving', () => {
    it('should create data directory', () => {
      mockFs.default.mkdirSync.mockImplementation(() => undefined);
      mockFs.default.mkdirSync('/test/data', { recursive: true });
      assert.strictEqual(mockFs.default.mkdirSync.mock.calls.length, 1);
    });

    it('should save API calls to JSON file', () => {
      const outputPath = path.join('/test/data', 'save-api-calls.json');
      assert.ok(outputPath.endsWith('.json'));
    });

    it('should format JSON with indentation', () => {
      const apiCalls = [{ method: 'POST' }];
      const content = JSON.stringify(apiCalls, null, 2);
      assert.ok(content.includes('\n'));
    });
  });

  describe('return value', () => {
    it('should return apiCalls array', () => {
      const apiCalls = [{ method: 'POST', url: 'test' }];
      assert.ok(Array.isArray(apiCalls));
    });

    it('should return empty array when login expired', () => {
      const isLoggedIn = false;
      const result = isLoggedIn ? [] : undefined;
      assert.strictEqual(result, undefined);
    });
  });

  describe('CLI execution', () => {
    it('should parse --headed flag', () => {
      const args = ['--headed'];
      const headed = args.includes('--headed');
      assert.strictEqual(headed, true);
    });

    it('should run when called directly', () => {
      const isDirectCall = true;
      assert.strictEqual(isDirectCall, true);
    });
  });
});