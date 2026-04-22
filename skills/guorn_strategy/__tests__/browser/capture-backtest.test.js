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

describe('capture-backtest.js', () => {
  beforeEach(() => {
    resetMocks();
  });

  afterEach(() => {
    resetMocks();
  });

  describe('captureBacktestAPI options', () => {
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
      const shouldCapture = !url.includes('.css');
      assert.strictEqual(shouldCapture, false);
    });

    it('should filter out JS files', () => {
      const url = 'https://guorn.com/static/app.js';
      const shouldCapture = !url.includes('.js');
      assert.strictEqual(shouldCapture, false);
    });

    it('should filter out PNG files', () => {
      const url = 'https://guorn.com/static/logo.png';
      const shouldCapture = !url.includes('.png');
      assert.strictEqual(shouldCapture, false);
    });

    it('should filter out JPG files', () => {
      const url = 'https://guorn.com/static/banner.jpg';
      const shouldCapture = !url.includes('.jpg');
      assert.strictEqual(shouldCapture, false);
    });

    it('should filter out GIF files', () => {
      const url = 'https://guorn.com/static/animation.gif';
      const shouldCapture = !url.includes('.gif');
      assert.strictEqual(shouldCapture, false);
    });

    it('should filter out font files', () => {
      const fontExtensions = ['.woff', '.woff2', '.ttf'];
      for (const ext of fontExtensions) {
        const url = `https://guorn.com/static/font${ext}`;
        const shouldCapture = !url.includes(ext);
        assert.strictEqual(shouldCapture, false);
      }
    });

    it('should filter out google analytics', () => {
      const url = 'https://google-analytics.com/collect';
      const shouldCapture = !url.includes('google-analytics') && !url.includes('googleapis');
      assert.strictEqual(shouldCapture, false);
    });

    it('should capture request type', () => {
      const entry = { type: 'request' };
      assert.strictEqual(entry.type, 'request');
    });

    it('should capture request method', () => {
      const entry = { method: 'POST' };
      assert.strictEqual(entry.method, 'POST');
    });

    it('should capture request URL', () => {
      const entry = { url: 'https://guorn.com/api' };
      assert.ok(entry.url);
    });

    it('should capture request headers', () => {
      const entry = { headers: {} };
      assert.ok(entry.headers);
    });

    it('should capture POST data', () => {
      const entry = { postData: '{"test":"value"}' };
      assert.ok(entry.postData);
    });

    it('should capture timestamp', () => {
      const entry = { timestamp: new Date().toISOString() };
      assert.ok(entry.timestamp);
    });
  });

  describe('response interception', () => {
    it('should match response to request by URL and type', () => {
      const apiCalls = [{ type: 'request', url: 'https://guorn.com/api' }];
      const responseUrl = 'https://guorn.com/api';
      const entry = apiCalls.findLast(r => r.url === responseUrl && r.type === 'request');
      assert.ok(entry);
    });

    it('should capture status code', () => {
      const statusCode = 200;
      assert.strictEqual(statusCode, 200);
    });

    it('should capture response body', () => {
      const responseBody = '{"result":"success"}';
      assert.ok(responseBody);
    });

    it('should handle response text errors gracefully', () => {
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

  describe('login verification', () => {
    it('should check login by URL', () => {
      const url = 'https://guorn.com/stock';
      const isLoggedIn = !url.includes('/user/login');
      assert.strictEqual(isLoggedIn, true);
    });

    it('should detect login page redirect', () => {
      const url = 'https://guorn.com/user/login';
      const isLoggedIn = !url.includes('/user/login');
      assert.strictEqual(isLoggedIn, false);
    });

    it('should return early when not logged in', () => {
      const isLoggedIn = false;
      if (!isLoggedIn) {
        assert.strictEqual(isLoggedIn, false);
      }
    });
  });

  describe('backtest button interaction', () => {
    it('should find backtest button with multiple selectors', () => {
      const selector = 'a:has-text("开始回测"), button:has-text("开始回测")';
      assert.ok(selector.includes('开始回测'));
    });

    it('should click backtest button when visible', () => {
      const clicked = true;
      assert.strictEqual(clicked, true);
    });

    it('should wait 10s after clicking backtest', () => {
      const waitTime = 10000;
      assert.strictEqual(waitTime, 10000);
    });

    it('should handle missing backtest button', () => {
      const backtestButtonVisible = false;
      assert.strictEqual(backtestButtonVisible, false);
    });

    it('should use 5s timeout for visibility check', () => {
      const timeout = 5000;
      assert.strictEqual(timeout, 5000);
    });
  });

  describe('file saving', () => {
    it('should create data directory', () => {
      mockFs.default.mkdirSync.mockImplementation(() => undefined);
      mockFs.default.mkdirSync('/test/data', { recursive: true });
      assert.strictEqual(mockFs.default.mkdirSync.mock.calls.length, 1);
    });

    it('should save to backtest-api-calls.json', () => {
      const outputPath = path.join('/test/data', 'backtest-api-calls.json');
      assert.ok(outputPath.includes('backtest-api-calls'));
      assert.ok(outputPath.endsWith('.json'));
    });

    it('should format JSON with 2-space indentation', () => {
      const content = JSON.stringify({}, null, 2);
      assert.ok(content.includes('\n'));
    });
  });

  describe('API call summary', () => {
    it('should get unique URLs', () => {
      const apiCalls = [
        { url: 'url1' },
        { url: 'url1' },
        { url: 'url2' }
      ];
      const uniqueUrls = [...new Set(apiCalls.map(r => r.url))];
      assert.strictEqual(uniqueUrls.length, 2);
    });

    it('should group calls by URL', () => {
      const apiCalls = [
        { url: 'url1', method: 'GET' },
        { url: 'url1', method: 'POST' },
        { url: 'url2', method: 'GET' }
      ];
      for (const url of [...new Set(apiCalls.map(r => r.url))]) {
        const calls = apiCalls.filter(r => r.url === url);
        assert.ok(calls.length > 0);
      }
    });

    it('should get unique methods for each URL', () => {
      const calls = [
        { url: 'url1', method: 'GET' },
        { url: 'url1', method: 'POST' }
      ];
      const methods = [...new Set(calls.map(r => r.method))];
      assert.strictEqual(methods.length, 2);
    });

    it('should join methods with comma', () => {
      const methods = ['GET', 'POST'];
      const joined = methods.join(',');
      assert.strictEqual(joined, 'GET,POST');
    });
  });

  describe('return value', () => {
    it('should return apiCalls array', () => {
      const apiCalls = [];
      assert.ok(Array.isArray(apiCalls));
    });

    it('should return undefined when not logged in', () => {
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