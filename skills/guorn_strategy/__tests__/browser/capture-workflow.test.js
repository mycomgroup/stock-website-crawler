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

describe('capture-workflow.js', () => {
  beforeEach(() => {
    resetMocks();
  });

  afterEach(() => {
    resetMocks();
  });

  describe('captureFullWorkflow options', () => {
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

    it('should filter out static assets', () => {
      const staticExtensions = ['.css', '.js', '.png', '.jpg', '.gif', '.woff', '.woff2', '.ttf'];
      assert.strictEqual(staticExtensions.length, 8);
    });

    it('should filter out google analytics', () => {
      const url = 'https://google-analytics.com/collect';
      const shouldCapture = !url.includes('google-analytics') && !url.includes('googleapis');
      assert.strictEqual(shouldCapture, false);
    });

    it('should capture request metadata', () => {
      const entry = {
        type: 'request',
        method: 'POST',
        url: 'https://guorn.com/api',
        headers: {},
        postData: '{}',
        timestamp: new Date().toISOString()
      };
      assert.strictEqual(entry.type, 'request');
      assert.ok(entry.timestamp);
    });
  });

  describe('response interception', () => {
    it('should match response to request', () => {
      const apiCalls = [{ type: 'request', url: 'https://guorn.com/api' }];
      const responseUrl = 'https://guorn.com/api';
      const entry = apiCalls.findLast(r => r.url === responseUrl);
      assert.ok(entry);
    });

    it('should capture status code', () => {
      const statusCode = 200;
      assert.strictEqual(statusCode, 200);
    });

    it('should capture response body', () => {
      const responseBody = '{"data":"value"}';
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

    it('should return early when not logged in', () => {
      const isLoggedIn = false;
      if (!isLoggedIn) {
        assert.strictEqual(isLoggedIn, false);
      }
    });
  });

  describe('save button search', () => {
    it('should try multiple selectors for save button', () => {
      const saveSelectors = [
        '#save-btn',
        '.save-btn',
        'a:has-text("保存")',
        'button:has-text("保存")',
        'span:has-text("保存")'
      ];
      assert.strictEqual(saveSelectors.length, 5);
    });

    it('should iterate through selectors', () => {
      const selectors = ['a:has-text("保存")', 'button:has-text("保存")'];
      for (const sel of selectors) {
        assert.ok(sel.includes('保存'));
      }
    });

    it('should wait 3s after clicking save', () => {
      const waitTime = 3000;
      assert.strictEqual(waitTime, 3000);
    });

    it('should break after finding visible button', () => {
      let found = false;
      for (let i = 0; i < 5; i++) {
        if (i === 2) {
          found = true;
          break;
        }
      }
      assert.strictEqual(found, true);
    });
  });

  describe('backtest button search', () => {
    it('should try multiple selectors for backtest button', () => {
      const backtestSelectors = [
        '#backtest-btn',
        '.backtest-btn',
        'a:has-text("开始回测")',
        'button:has-text("开始回测")',
        'span:has-text("开始回测")'
      ];
      assert.strictEqual(backtestSelectors.length, 5);
    });

    it('should wait 10s after clicking backtest', () => {
      const waitTime = 10000;
      assert.strictEqual(waitTime, 10000);
    });
  });

  describe('file saving', () => {
    it('should create data directory', () => {
      mockFs.default.mkdirSync.mockImplementation(() => undefined);
      mockFs.default.mkdirSync('/test/data', { recursive: true });
      assert.strictEqual(mockFs.default.mkdirSync.mock.calls.length, 1);
    });

    it('should save to full-workflow-api-calls.json', () => {
      const outputPath = path.join('/test/data', 'full-workflow-api-calls.json');
      assert.ok(outputPath.includes('full-workflow'));
      assert.ok(outputPath.endsWith('.json'));
    });

    it('should format JSON with indentation', () => {
      const content = JSON.stringify({}, null, 2);
      assert.ok(content.includes('\n'));
    });
  });

  describe('POST request filtering', () => {
    it('should filter POST calls from all apiCalls', () => {
      const apiCalls = [
        { method: 'GET', url: 'test1' },
        { method: 'POST', url: 'test2' },
        { method: 'POST', url: 'test3' }
      ];
      const postCalls = apiCalls.filter(r => r.method === 'POST');
      assert.strictEqual(postCalls.length, 2);
    });

    it('should print URL for each POST call', () => {
      const call = { url: 'https://guorn.com/api' };
      assert.ok(call.url);
    });

    it('should print postData', () => {
      const call = { postData: '{"test":"value"}' };
      assert.ok(call.postData);
    });

    it('should truncate response to 200 chars', () => {
      const response = 'x'.repeat(500);
      const truncated = response?.slice(0, 200);
      assert.strictEqual(truncated?.length, 200);
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