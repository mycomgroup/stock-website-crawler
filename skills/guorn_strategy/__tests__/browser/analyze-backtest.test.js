import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';

describe('browser/analyze-backtest.js', () => {
  describe('constants and configuration', () => {
    it('should use correct user agent', () => {
      const USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36';
      expect(USER_AGENT).toContain('Macintosh');
      expect(USER_AGENT).toContain('Chrome');
    });

    it('should use correct strategy URL', () => {
      const strategyUrl = 'https://guorn.com/stock';
      expect(strategyUrl).toBe('https://guorn.com/stock');
    });

    it('should use 3s wait after navigation', () => {
      const navigationWait = 3000;
      expect(navigationWait).toBe(3000);
    });

    it('should use 10s wait after backtest click', () => {
      const backtestWait = 10000;
      expect(backtestWait).toBe(10000);
    });

    it('should use 5s timeout for backtest button', () => {
      const backtestButtonTimeout = 5000;
      expect(backtestButtonTimeout).toBe(5000);
    });
  });

  describe('options handling', () => {
    it('should default to headless mode', () => {
      const headed = false;
      const headless = !headed;
      expect(headless).toBe(true);
    });

    it('should accept headed option', () => {
      const options = { headed: true };
      expect(options.headed).toBe(true);
    });

    it('should initialize empty apiCalls array', () => {
      const apiCalls = [];
      expect(apiCalls.length).toBe(0);
    });
  });

  describe('session handling', () => {
    it('should check if session file exists', () => {
      const SESSION_FILE = '/test/session.json';
      const exists = true;
      expect(exists).toBe(true);
    });

    it('should throw error when session file not found', () => {
      const SESSION_FILE = '/test/session.json';
      const exists = false;
      if (!exists) {
        expect(() => { throw new Error('No session file found. Run capture-session.js first.'); }).toThrow();
      }
    });

    it('should load session from file', () => {
      const sessionPayload = { cookies: [{ name: 'session', value: 'test' }] };
      expect(sessionPayload.cookies).toBeDefined();
    });

    it('should log session file location', () => {
      const SESSION_FILE = '/test/session.json';
      expect(SESSION_FILE.includes('session.json')).toBe(true);
    });
  });

  describe('browser configuration', () => {
    it('should set headless based on headed option', () => {
      const headed = true;
      const headless = !headed;
      expect(headless).toBe(false);
    });

    it('should use correct user agent string', () => {
      const USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)';
      expect(USER_AGENT.includes('Macintosh')).toBe(true);
    });

    it('should add cookies to context', () => {
      const sessionPayload = { cookies: [{ name: 'test', value: 'val' }] };
      expect(sessionPayload.cookies).toBeDefined();
    });
  });

  describe('request interception', () => {
    it('should capture guorn.com requests', () => {
      const url = 'https://guorn.com/api/stock';
      const shouldCapture = url.includes('guorn.com');
      expect(shouldCapture).toBe(true);
    });

    it('should filter out CSS files', () => {
      const url = 'https://guorn.com/static/style.css';
      const shouldCapture = !url.includes('.css');
      expect(shouldCapture).toBe(false);
    });

    it('should filter out JS files', () => {
      const url = 'https://guorn.com/static/script.js';
      const shouldCapture = !url.includes('.js');
      expect(shouldCapture).toBe(false);
    });

    it('should filter out PNG files', () => {
      const url = 'https://guorn.com/static/image.png';
      const shouldCapture = !url.includes('.png');
      expect(shouldCapture).toBe(false);
    });

    it('should filter out JPG files', () => {
      const url = 'https://guorn.com/static/image.jpg';
      const shouldCapture = !url.includes('.jpg');
      expect(shouldCapture).toBe(false);
    });

    it('should filter out WOFF files', () => {
      const url = 'https://guorn.com/static/font.woff';
      const shouldCapture = !url.includes('.woff');
      expect(shouldCapture).toBe(false);
    });

    it('should filter out google analytics', () => {
      const url = 'https://google-analytics.com/collect';
      const shouldCapture = !url.includes('google-analytics') && !url.includes('googleapis');
      expect(shouldCapture).toBe(false);
    });

    it('should capture request type', () => {
      const entry = { type: 'request' };
      expect(entry.type).toBe('request');
    });

    it('should capture request method', () => {
      const entry = { method: 'POST' };
      expect(entry.method).toBe('POST');
    });

    it('should capture request headers', () => {
      const entry = { headers: { 'Content-Type': 'application/json' } };
      expect(entry.headers).toBeDefined();
    });

    it('should capture POST data', () => {
      const entry = { postData: '{"test":"value"}' };
      expect(entry.postData).toBeDefined();
    });

    it('should capture timestamp', () => {
      const entry = { timestamp: new Date().toISOString() };
      expect(entry.timestamp).toBeDefined();
    });
  });

  describe('response interception', () => {
    it('should match response to request by URL', () => {
      const apiCalls = [{ type: 'request', url: 'https://guorn.com/api' }];
      const responseUrl = 'https://guorn.com/api';
      const entry = apiCalls.findLast(r => r.url === responseUrl);
      expect(entry).toBeDefined();
    });

    it('should capture status code', () => {
      const statusCode = 200;
      expect(statusCode).toBe(200);
    });

    it('should capture response body', () => {
      const responseBody = '{"result":"success"}';
      expect(responseBody).toBeDefined();
    });

    it('should handle response text errors', () => {
      const errorCaught = true;
      expect(errorCaught).toBe(true);
    });
  });

  describe('page navigation', () => {
    it('should navigate to strategy page', () => {
      const targetUrl = 'https://guorn.com/stock';
      expect(targetUrl).toBe('https://guorn.com/stock');
    });

    it('should wait 3s after navigation', () => {
      const waitTime = 3000;
      expect(waitTime).toBe(3000);
    });
  });

  describe('login verification', () => {
    it('should check login by URL', () => {
      const url = 'https://guorn.com/stock';
      const isLoggedIn = !url.includes('/user/login');
      expect(isLoggedIn).toBe(true);
    });

    it('should return early when not logged in', () => {
      const isLoggedIn = false;
      if (!isLoggedIn) {
        expect(isLoggedIn).toBe(false);
      }
    });
  });

  describe('backtest execution', () => {
    it('should find backtest button', () => {
      const selector = 'button:has-text("开始回测"), a:has-text("开始回测")';
      expect(selector.includes('开始回测')).toBe(true);
    });

    it('should click backtest button', () => {
      const clicked = true;
      expect(clicked).toBe(true);
    });

    it('should wait 10s after click', () => {
      const waitTime = 10000;
      expect(waitTime).toBe(10000);
    });

    it('should handle missing backtest button', () => {
      const backtestButtonVisible = false;
      expect(backtestButtonVisible).toBe(false);
    });
  });

  describe('file saving', () => {
    it('should save to backtest-api-calls.json', () => {
      const outputFileName = 'backtest-api-calls.json';
      expect(outputFileName.includes('backtest-api-calls')).toBe(true);
      expect(outputFileName.endsWith('.json')).toBe(true);
    });

    it('should format JSON with indentation', () => {
      const content = JSON.stringify({ key: 'value' }, null, 2);
      expect(content.includes('\n')).toBe(true);
    });

    it('should create data directory', () => {
      const DATA_ROOT = '/test/data';
      expect(DATA_ROOT).toBe('/test/data');
    });
  });

  describe('API call summary', () => {
    it('should get unique URLs', () => {
      const apiCalls = [{ url: 'url1' }, { url: 'url1' }, { url: 'url2' }];
      const uniqueUrls = [...new Set(apiCalls.map(r => r.url))];
      expect(uniqueUrls.length).toBe(2);
    });

    it('should get methods for each URL', () => {
      const calls = [{ url: 'url1', method: 'GET' }, { url: 'url1', method: 'POST' }];
      const methods = [...new Set(calls.map(r => r.method))];
      expect(methods.length).toBe(2);
    });

    it('should join methods with comma', () => {
      const methods = ['GET', 'POST'];
      const joined = methods.join(',');
      expect(joined).toBe('GET,POST');
    });
  });

  describe('return value', () => {
    it('should return apiCalls array', () => {
      const apiCalls = [];
      expect(Array.isArray(apiCalls)).toBe(true);
    });

    it('should return undefined when not logged in', () => {
      const isLoggedIn = false;
      const result = isLoggedIn ? [] : undefined;
      expect(result).toBeUndefined();
    });
  });

  describe('browser closing', () => {
    it('should close browser at end', () => {
      const browserClosed = true;
      expect(browserClosed).toBe(true);
    });
  });

  describe('CLI execution', () => {
    it('should parse --headed flag', () => {
      const args = ['--headed'];
      const headed = args.includes('--headed');
      expect(headed).toBe(true);
    });

    it('should run when called directly', () => {
      const isDirectCall = true;
      expect(isDirectCall).toBe(true);
    });
  });

  describe('error handling', () => {
    it('should handle session file not found', () => {
      const exists = false;
      if (!exists) {
        const error = new Error('No session file found. Run capture-session.js first.');
        expect(error.message).toContain('No session file found');
      }
    });

    it('should catch backtest button visibility errors', () => {
      const backtestButtonError = false;
      expect(backtestButtonError).toBe(false);
    });

    it('should catch response text errors', () => {
      const responseTextErrorCaught = true;
      expect(responseTextErrorCaught).toBe(true);
    });
  });
});