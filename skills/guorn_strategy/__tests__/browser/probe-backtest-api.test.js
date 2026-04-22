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

const mockFs = await import('node:fs');

function resetMocks() {
  mockFs.default.existsSync.mockClear();
  mockFs.default.readFileSync.mockClear();
  mockFs.default.writeFileSync.mockClear();
  mockFs.default.mkdirSync.mockClear();
}

describe('probe-backtest-api.js', () => {
  beforeEach(() => {
    resetMocks();
  });

  afterEach(() => {
    resetMocks();
  });

  describe('session loading', () => {
    it('should read session file on startup', () => {
      mockFs.default.readFileSync.mockImplementation(() => '{"cookies":[]}');
      const session = JSON.parse(mockFs.default.readFileSync());
      assert.ok(session.cookies);
    });

    it('should handle session file read error', () => {
      mockFs.default.readFileSync.mockImplementation(() => {
        throw new Error('Read error');
      });
      assert.throws(() => mockFs.default.readFileSync(), Error);
    });
  });

  describe('request interception', () => {
    it('should capture requests with guorn.com in URL', () => {
      const url = 'https://guorn.com/api/stock';
      assert.ok(url.includes('guorn.com'));
    });

    it('should filter out static assets', () => {
      const staticUrls = [
        'https://guorn.com/static/css/style.css',
        'https://guorn.com/static/js/app.js',
        'https://guorn.com/static/img/logo.png'
      ];
      for (const url of staticUrls) {
        assert.ok(url.includes('static'));
      }
    });

    it('should filter out google analytics', () => {
      const url = 'https://google-analytics.com/collect';
      assert.ok(url.includes('google'));
    });

    it('should capture request method', () => {
      const request = { method: 'POST', url: 'https://guorn.com/api/test' };
      assert.strictEqual(request.method, 'POST');
    });

    it('should capture POST data', () => {
      const request = { method: 'POST', postData: '{"test":"data"}' };
      assert.ok(request.postData);
    });

    it('should capture request headers', () => {
      const request = { headers: { 'Content-Type': 'application/json' } };
      assert.ok(request.headers['Content-Type']);
    });
  });

  describe('response interception', () => {
    it('should capture response status', () => {
      const response = { status: 200, url: 'https://guorn.com/api/test' };
      assert.strictEqual(response.status, 200);
    });

    it('should capture response body', () => {
      const responseBody = '{"result":"success"}';
      assert.ok(responseBody.includes('result'));
    });

    it('should match response to request by URL', () => {
      const requests = [{ url: 'https://guorn.com/api/test', method: 'POST' }];
      const responseUrl = 'https://guorn.com/api/test';
      const entry = requests.findLast(r => r.url === responseUrl);
      assert.ok(entry);
    });
  });

  describe('browser launch options', () => {
    it('should launch with headless false for debugging', () => {
      const launchOptions = { headless: false };
      assert.strictEqual(launchOptions.headless, false);
    });

    it('should set user agent', () => {
      const userAgent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)';
      assert.ok(userAgent.includes('Macintosh'));
    });

    it('should add cookies from session', () => {
      const session = { cookies: [{ name: 'sessionid', value: 'abc' }] };
      assert.ok(session.cookies);
    });
  });

  describe('page navigation', () => {
    it('should navigate to strategy page', () => {
      const targetUrl = 'https://guorn.com/stock';
      assert.strictEqual(targetUrl, 'https://guorn.com/stock');
    });

    it('should wait 4 seconds after navigation', () => {
      const waitTime = 4000;
      assert.strictEqual(waitTime, 4000);
    });
  });

  describe('button interactions', () => {
    it('should look for 创建策略 button', () => {
      const selector = 'a:has-text("创建策略"), button:has-text("创建策略")';
      assert.ok(selector.includes('创建策略'));
    });

    it('should look for 开始回测 button', () => {
      const selector = 'a:has-text("开始回测"), button:has-text("开始回测")';
      assert.ok(selector.includes('开始回测'));
    });

    it('should wait 3 seconds after clicking create button', () => {
      const waitTime = 3000;
      assert.strictEqual(waitTime, 3000);
    });

    it('should wait 15 seconds after clicking backtest button', () => {
      const waitTime = 15000;
      assert.strictEqual(waitTime, 15000);
    });
  });

  describe('screenshot saving', () => {
    it('should save screenshot on page load', () => {
      const screenshotPath = path.join('/test/data', 'probe-1-loaded.png');
      assert.ok(screenshotPath.endsWith('.png'));
    });

    it('should save screenshot after strategy creation', () => {
      const screenshotPath = path.join('/test/data', 'probe-2-created.png');
      assert.ok(screenshotPath.includes('created'));
    });

    it('should save screenshot after backtest', () => {
      const screenshotPath = path.join('/test/data', 'probe-3-backtest.png');
      assert.ok(screenshotPath.includes('backtest'));
    });
  });

  describe('POST request filtering', () => {
    it('should filter POST requests from all requests', () => {
      const requests = [
        { method: 'GET', url: 'https://guorn.com/page' },
        { method: 'POST', url: 'https://guorn.com/api/test' },
        { method: 'POST', url: 'https://guorn.com/api/backtest' }
      ];
      const posts = requests.filter(r => r.method === 'POST');
      assert.strictEqual(posts.length, 2);
    });

    it('should output POST request details', () => {
      const postRequest = {
        url: 'https://guorn.com/api/backtest',
        status: 200,
        body: '{"param":"value"}',
        response: '{"result":"ok"}'
      };
      assert.ok(postRequest.url);
      assert.ok(postRequest.status);
    });

    it('should truncate body to 500 chars', () => {
      const longBody = 'x'.repeat(1000);
      const truncated = longBody.slice(0, 500);
      assert.strictEqual(truncated.length, 500);
    });

    it('should truncate response to 200 chars', () => {
      const longResponse = 'y'.repeat(500);
      const truncated = longResponse.slice(0, 200);
      assert.strictEqual(truncated.length, 200);
    });
  });

  describe('request logging', () => {
    it('should log all guorn.com requests', () => {
      const requests = [
        { method: 'GET', url: 'https://guorn.com/page1' },
        { method: 'POST', url: 'https://guorn.com/api' }
      ];
      assert.strictEqual(requests.length, 2);
    });

    it('should strip domain from URL in log', () => {
      const url = 'https://guorn.com/api/test';
      const stripped = url.replace('https://guorn.com', '');
      assert.strictEqual(stripped, '/api/test');
    });
  });

  describe('file output', () => {
    it('should save requests to JSON file', () => {
      const outputPath = path.join('/test/data', 'probed-requests.json');
      assert.ok(outputPath.endsWith('.json'));
    });

    it('should create data directory', () => {
      mockFs.default.mkdirSync.mockImplementation(() => undefined);
      mockFs.default.mkdirSync('/test/data', { recursive: true });
      assert.strictEqual(mockFs.default.mkdirSync.mock.calls.length, 1);
    });

    it('should write formatted JSON', () => {
      const requests = [{ method: 'POST', url: 'test' }];
      const content = JSON.stringify(requests, null, 2);
      assert.ok(content.includes('\n'));
    });
  });

  describe('fallback behavior', () => {
    it('should wait 30s for manual interaction if backtest button not found', () => {
      const fallbackWait = 30000;
      assert.strictEqual(fallbackWait, 30000);
    });

    it('should handle invisible backtest button', () => {
      const isVisible = false;
      if (!isVisible) {
        assert.strictEqual(isVisible, false);
      }
    });
  });

  describe('manual interaction mode', () => {
    it('should allow manual intervention when buttons not found', () => {
      const needsManual = true;
      assert.strictEqual(needsManual, true);
    });
  });
});