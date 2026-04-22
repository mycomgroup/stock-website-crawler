import { describe, it, beforeEach, afterEach, mock } from 'node:test';
import assert from 'node:assert';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const mockProxyAgent = mock.fn(function(url) {
  this.url = url;
});

const mockUndiciFetch = mock.fn(async (url, options) => {
  return {
    ok: true,
    status: 200,
    text: async () => 'response body'
  };
});

const mockNativeFetch = mock.fn(async (url, options) => {
  return {
    ok: true,
    status: 200,
    text: async () => 'native fetch response'
  };
});

let mockEnv = {
  HTTP_PROXY: '',
  HTTPS_PROXY: ''
};

mock.module('undici', {
  namedExports: {
    ProxyAgent: mockProxyAgent,
    fetch: mockUndiciFetch
  }
});

mock.module(path.join(__dirname, '../load-env.js'), {
  namedExports: {
    ENV: mockEnv
  }
});

global.fetch = mockNativeFetch;

function resetMocks() {
  mockProxyAgent.mock.resetCalls();
  mockUndiciFetch.mock.resetCalls();
  mockNativeFetch.mock.resetCalls();
}

describe('proxy-fetch', () => {
  beforeEach(() => {
    resetMocks();
    mockEnv.HTTP_PROXY = '';
    mockEnv.HTTPS_PROXY = '';
  });

  describe('createProxyFetch', () => {
    it('should return native fetch when no proxy configured', async () => {
      mockEnv.HTTP_PROXY = '';
      mockEnv.HTTPS_PROXY = '';
      
      const { createProxyFetch } = await import('../request/proxy-fetch.js');
      const fetchFn = createProxyFetch();
      
      assert.strictEqual(fetchFn, mockNativeFetch);
      assert.strictEqual(mockProxyAgent.mock.callCount(), 0);
    });

    it('should return proxy fetch when HTTP_PROXY configured', async () => {
      mockEnv.HTTP_PROXY = 'http://proxy.example.com:8080';
      mockEnv.HTTPS_PROXY = '';
      
      const { createProxyFetch } = await import('../request/proxy-fetch.js?cachebuster=' + Date.now());
      const fetchFn = createProxyFetch();
      
      assert.strictEqual(typeof fetchFn, 'function');
      assert.strictEqual(mockProxyAgent.mock.callCount(), 1);
      assert.strictEqual(mockProxyAgent.mock.calls[0].arguments[0], 'http://proxy.example.com:8080');
    });

    it('should return proxy fetch when HTTPS_PROXY configured', async () => {
      mockEnv.HTTP_PROXY = '';
      mockEnv.HTTPS_PROXY = 'https://secure-proxy.example.com:443';
      
      const { createProxyFetch } = await import('../request/proxy-fetch.js?cachebuster=' + Date.now());
      const fetchFn = createProxyFetch();
      
      assert.strictEqual(typeof fetchFn, 'function');
      assert.strictEqual(mockProxyAgent.mock.callCount(), 1);
      assert.strictEqual(mockProxyAgent.mock.calls[0].arguments[0], 'https://secure-proxy.example.com:443');
    });

    it('should prefer HTTPS_PROXY over HTTP_PROXY', async () => {
      mockEnv.HTTP_PROXY = 'http://proxy.example.com:8080';
      mockEnv.HTTPS_PROXY = 'https://secure-proxy.example.com:443';
      
      const { createProxyFetch } = await import('../request/proxy-fetch.js?cachebuster=' + Date.now());
      const fetchFn = createProxyFetch();
      
      assert.strictEqual(typeof fetchFn, 'function');
      assert.strictEqual(mockProxyAgent.mock.callCount(), 1);
      assert.strictEqual(mockProxyAgent.mock.calls[0].arguments[0], 'https://secure-proxy.example.com:443');
    });

    it('should create ProxyAgent with correct proxy URL', async () => {
      const proxyUrl = 'http://localhost:3128';
      mockEnv.HTTP_PROXY = proxyUrl;
      
      const { createProxyFetch } = await import('../request/proxy-fetch.js?cachebuster=' + Date.now());
      createProxyFetch();
      
      assert.strictEqual(mockProxyAgent.mock.calls[0].arguments[0], proxyUrl);
    });

    it('should return a function that passes dispatcher to undiciFetch', async () => {
      mockEnv.HTTPS_PROXY = 'http://proxy.test:8080';
      
      const { createProxyFetch } = await import('../request/proxy-fetch.js?cachebuster=' + Date.now());
      const fetchFn = createProxyFetch();
      
      mockUndiciFetch.mock.mockImplementation(async (url, options) => ({
        ok: true,
        status: 200
      }));
      
      await fetchFn('https://api.example.com/data', { method: 'GET' });
      
      assert.strictEqual(mockUndiciFetch.mock.callCount(), 1);
      const callArgs = mockUndiciFetch.mock.calls[0].arguments;
      assert.strictEqual(callArgs[0], 'https://api.example.com/data');
      assert.ok(callArgs[1].dispatcher);
    });

    it('should merge options with dispatcher', async () => {
      mockEnv.HTTPS_PROXY = 'http://proxy.test:8080';
      
      const { createProxyFetch } = await import('../request/proxy-fetch.js?cachebuster=' + Date.now());
      const fetchFn = createProxyFetch();
      
      const customOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: '{"test": true}'
      };
      
      await fetchFn('https://api.example.com/post', customOptions);
      
      const optionsArg = mockUndiciFetch.mock.calls[0].arguments[1];
      assert.strictEqual(optionsArg.method, 'POST');
      assert.deepStrictEqual(optionsArg.headers, { 'Content-Type': 'application/json' });
      assert.strictEqual(optionsArg.body, '{"test": true}');
      assert.ok(optionsArg.dispatcher);
    });

    it('should handle empty proxy strings', async () => {
      mockEnv.HTTP_PROXY = '';
      mockEnv.HTTPS_PROXY = '';
      
      const { createProxyFetch } = await import('../request/proxy-fetch.js?cachebuster=' + Date.now());
      const fetchFn = createProxyFetch();
      
      assert.strictEqual(fetchFn, mockNativeFetch);
    });

    it('should handle proxy URL with authentication', async () => {
      mockEnv.HTTP_PROXY = 'http://user:password@proxy.example.com:8080';
      
      const { createProxyFetch } = await import('../request/proxy-fetch.js?cachebuster=' + Date.now());
      createProxyFetch();
      
      assert.strictEqual(mockProxyAgent.mock.calls[0].arguments[0], 'http://user:password@proxy.example.com:8080');
    });

    it('should handle SOCKS proxy URLs', async () => {
      mockEnv.HTTP_PROXY = 'socks5://proxy.example.com:1080';
      
      const { createProxyFetch } = await import('../request/proxy-fetch.js?cachebuster=' + Date.now());
      createProxyFetch();
      
      assert.strictEqual(mockProxyAgent.mock.calls[0].arguments[0], 'socks5://proxy.example.com:1080');
    });
  });

  describe('proxyFetch export', () => {
    it('should be a function', async () => {
      mockEnv.HTTP_PROXY = '';
      mockEnv.HTTPS_PROXY = '';
      
      const { proxyFetch } = await import('../request/proxy-fetch.js?cachebuster=' + Date.now());
      
      assert.strictEqual(typeof proxyFetch, 'function');
    });

    it('should be the result of createProxyFetch', async () => {
      mockEnv.HTTP_PROXY = '';
      mockEnv.HTTPS_PROXY = '';
      
      const module = await import('../request/proxy-fetch.js?cachebuster=' + Date.now());
      
      assert.strictEqual(typeof module.proxyFetch, 'function');
    });

    it('should work as a fetch function', async () => {
      mockEnv.HTTP_PROXY = '';
      mockEnv.HTTPS_PROXY = '';
      
      const { proxyFetch } = await import('../request/proxy-fetch.js?cachebuster=' + Date.now());
      
      const result = await proxyFetch('https://example.com');
      
      assert.strictEqual(mockNativeFetch.mock.callCount(), 1);
      assert.strictEqual(mockNativeFetch.mock.calls[0].arguments[0], 'https://example.com');
    });
  });
});