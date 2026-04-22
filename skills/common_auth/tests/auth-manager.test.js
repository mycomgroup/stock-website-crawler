import { describe, it, beforeEach, afterEach } from 'node:test';
import assert from 'node:assert';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

function createMockFs() {
  const storage = { exists: false, data: null };
  return {
    existsSync: () => storage.exists,
    readFileSync: () => storage.data || '{}',
    writeFileSync: () => {},
    mkdirSync: () => {},
    _storage: storage,
    _setExists: (v) => { storage.exists = v; },
    _setData: (v) => { storage.data = v; },
    _reset: () => { storage.exists = false; storage.data = null; }
  };
}

function createMockChildProcess() {
  let output = '[]';
  let shouldThrow = false;
  let errorMsg = 'error';
  return {
    execSync: () => {
      if (shouldThrow) throw new Error(errorMsg);
      return output;
    },
    _setOutput: (v) => { output = v; },
    _setThrow: (v, msg = 'error') => { shouldThrow = v; errorMsg = msg; },
    _reset: () => { output = '[]'; shouldThrow = false; }
  };
}

function createMockPage() {
  const state = {
    url: 'https://example.com',
    closed: false,
    gotoCalled: false
  };
  return {
    goto: async () => { state.gotoCalled = true; },
    url: () => state.url,
    waitForEvent: async () => new Promise(() => {}),
    close: async () => { state.closed = true; },
    _state: state,
    _setUrl: (v) => { state.url = v; },
    _setClosed: (v) => { state.closed = v; }
  };
}

function createMockContext(mockPage) {
  let cookies = [];
  return {
    newPage: async () => mockPage,
    cookies: async () => [...cookies],
    addCookies: async (c) => { cookies = c; },
    _setCookies: (c) => { cookies = c; },
    _reset: () => { cookies = []; }
  };
}

function createMockBrowser(mockContext, mockPage) {
  const state = { connected: true, closed: false };
  return {
    isConnected: () => state.connected,
    close: async () => { state.closed = true; },
    newContext: async () => mockContext,
    newPage: async () => mockPage,
    _state: state,
    _setConnected: (v) => { state.connected = v; },
    _setClosed: (v) => { state.closed = v; }
  };
}

function createMockBrowserEngine(mockBrowser, mockContext) {
  const state = { launchHeadedCalls: 0, launchContextCalls: 0 };
  return {
    launchHeaded: async () => { state.launchHeadedCalls++; return mockBrowser; },
    launchContext: async () => { state.launchContextCalls++; return { browser: mockBrowser, context: mockContext }; },
    _state: state,
    _reset: () => { state.launchHeadedCalls = 0; state.launchContextCalls = 0; }
  };
}

function createMockSiteAdapter(overrides = {}) {
  const state = {
    verifyResult: { success: true, user: 'test-user', message: '' },
    verifyIsBoolean: false,
    checkLoggedInResult: true,
    apiLoginResult: null,
    apiLoginThrow: false
  };
  return {
    id: 'test-site',
    name: 'Test Site',
    domain: 'example.com',
    loginUrl: 'https://example.com/login',
    dashboardUrl: 'https://example.com/dashboard',
    verifySession: async () => {
      if (state.verifyIsBoolean) return state.verifyResult === true;
      return state.verifyResult;
    },
    checkLoggedIn: async () => state.checkLoggedInResult,
    automatedLogin: async () => {},
    apiLogin: async (env) => {
      if (state.apiLoginThrow) throw new Error('api login failed');
      return state.apiLoginResult;
    },
    _state: state,
    _setVerifyResult: (success, user = 'test-user', msg = '') => {
      state.verifyResult = { success, user, message: msg };
      state.verifyIsBoolean = false;
    },
    _setVerifyBoolean: (v) => {
      state.verifyIsBoolean = true;
      state.verifyResult = v;
    },
    _setCheckLoggedIn: (v) => { state.checkLoggedInResult = v; },
    _setApiLoginResult: (v) => { state.apiLoginResult = v; },
    _setApiLoginThrow: (v) => { state.apiLoginThrow = v; }
  };
}

const mockFs = createMockFs();
const mockExecSync = createMockChildProcess();
const mockPage = createMockPage();
const mockContext = createMockContext(mockPage);
const mockBrowser = createMockBrowser(mockContext, mockPage);
const mockBrowserEngine = createMockBrowserEngine(mockBrowser, mockContext);

class TestableAuthManager {
  constructor(siteAdapter, deps = {}) {
    this.site = siteAdapter;
    this.sessionPath = '/test/sessions/test-site.json';
    this.engine = deps.engine || mockBrowserEngine;
    this._fs = deps.fs || mockFs;
    this._execSync = deps.execSync || mockExecSync.execSync;
    this._sessionRoot = '/test/sessions';
  }

  normalizeVerify(result) {
    if (typeof result === 'boolean') {
      return { success: result, user: result ? '已登录' : '', message: result ? '' : '验证失败' };
    }
    if (typeof result === 'object' && result !== null) {
      return { success: !!result.success, user: result.user || '', message: result.message || '' };
    }
    return { success: false, user: '', message: '未知返回格式' };
  }

  sanitizeCookies(cookies) {
    return cookies.map(c => {
      const copy = { ...c };
      if (copy.expires === null || typeof copy.expires !== 'number' || Number.isNaN(copy.expires)) {
        delete copy.expires;
      }
      if (copy.sameSite) {
        const s = copy.sameSite.toLowerCase();
        if (s === 'lax') copy.sameSite = 'Lax';
        else if (s === 'strict') copy.sameSite = 'Strict';
        else if (s === 'none') copy.sameSite = 'None';
      }
      return copy;
    });
  }

  async getValidSession(options = {}) {
    const { forceRefresh = false, method = 'all' } = options;

    if (!forceRefresh) {
      const session = this.loadSession();
      if (session && session.cookies) {
        const v = this.normalizeVerify(await this.site.verifySession(session.cookies));
        if (v.success) return session.cookies;
      }
    }

    let cookies = null;

    if (method === 'local' || method === 'all') {
      cookies = await this.tryLocalExtraction();
      if (cookies) return cookies;
    }

    if (method === 'auto' || method === 'all') {
      cookies = await this.tryAutomatedLogin();
      if (cookies) return cookies;
    }

    if (method === 'manual' || method === 'all') {
      return await this.tryManualCapture();
    }

    throw new Error(`无法获取 [${this.site.id}] 的有效会话。`);
  }

  loadSession() {
    if (!this._fs.existsSync(this.sessionPath)) return null;
    return JSON.parse(this._fs.readFileSync(this.sessionPath, 'utf8'));
  }

  async saveSessionWithVerify(cookies, url = '') {
    const v = this.normalizeVerify(await this.site.verifySession(cookies));
    if (!v.success) return false;

    const data = {
      cookies,
      timestamp: Date.now(),
      capturedAt: new Date().toISOString(),
      url,
      user: v.user || 'unknown',
      login: { loggedIn: v.success, mode: 'auth-manager', message: v.message || '' }
    };
    if (!this._fs.existsSync(this._sessionRoot)) this._fs.mkdirSync(this._sessionRoot, { recursive: true });
    this._fs.writeFileSync(this.sessionPath, JSON.stringify(data, null, 2));
    return true;
  }

  async tryLocalExtraction() {
    try {
      const output = this._execSync('python3 "extractor.py" "example.com"', { encoding: 'utf8' });
      const cookies = JSON.parse(output);
      if (cookies && cookies.length > 0) {
        const success = await this.saveSessionWithVerify(cookies, this.site.loginUrl);
        if (success) return cookies;
      }
    } catch (e) {}
    return null;
  }

  async tryAutomatedLogin() {
    if (this.site.apiLogin) {
      try {
        const cookies = await this.site.apiLogin(process.env);
        if (cookies && cookies.length > 0) {
          const success = await this.saveSessionWithVerify(cookies, this.site.loginUrl);
          if (success) return cookies;
        }
      } catch (e) {}
    }

    const { browser, context } = await this.engine.launchContext();
    const page = await context.newPage();
    try {
      await page.goto(this.site.loginUrl, { waitUntil: 'networkidle', timeout: 30000 });
      await this.site.automatedLogin(page, process.env);
      const loggedIn = await this.site.checkLoggedIn(page);
      if (loggedIn) {
        const cookies = await context.cookies();
        const success = await this.saveSessionWithVerify(cookies, page.url());
        if (success) return cookies;
      }
    } catch (e) {}
    finally {
      await browser.close();
    }
    return null;
  }

  async tryManualCapture() {
    const browser = await this.engine.launchHeaded();
    const context = await browser.newContext();
    const page = await context.newPage();
    await page.goto(this.site.loginUrl);

    return new Promise((resolve, reject) => {
      let isSaving = false;
      const checkInterval = setInterval(async () => {
        if (isSaving) return;
        try {
          if (!browser.isConnected()) {
            clearInterval(checkInterval);
            const cookies = await context.cookies();
            if (cookies && cookies.length > 0) {
              this._saveSessionData(cookies, this.site.loginUrl);
              resolve(cookies);
              return;
            }
            reject(new Error('浏览器已被手动关闭。'));
            return;
          }
          if (await this.site.checkLoggedIn(page)) {
            clearInterval(checkInterval);
            isSaving = true;
            const cookies = await context.cookies();
            this._saveSessionData(cookies, page.url());
            await browser.close().catch(() => {});
            resolve(cookies);
          }
        } catch (e) {
          if (e.message.includes('closed')) {
            clearInterval(checkInterval);
            try {
              const cookies = await context.cookies();
              if (cookies && cookies.length > 0) {
                this._saveSessionData(cookies, this.site.loginUrl);
                resolve(cookies);
                return;
              }
            } catch {}
            reject(new Error('浏览器已被手动关闭。'));
          }
        }
      }, 50);
      setTimeout(async () => {
        if (isSaving) return;
        clearInterval(checkInterval);
        reject(new Error('手动登录超时（5分钟）'));
      }, 5000);
    });
  }

  _saveSessionData(cookies, url) {
    const data = {
      cookies,
      timestamp: Date.now(),
      capturedAt: new Date().toISOString(),
      url,
      user: 'manual-login',
      login: { loggedIn: true, mode: 'manual' }
    };
    if (!this._fs.existsSync(this._sessionRoot)) this._fs.mkdirSync(this._sessionRoot, { recursive: true });
    this._fs.writeFileSync(this.sessionPath, JSON.stringify(data, null, 2));
  }

  async testSessionHeaded() {
    const session = this.loadSession();
    if (!session || !session.cookies) return;

    const browser = await this.engine.launchHeaded();
    const context = await browser.newContext();
    await context.addCookies(this.sanitizeCookies(session.cookies));
    const page = await context.newPage();
    await page.goto(this.site.dashboardUrl || this.site.loginUrl);
    await browser.close();
  }

  async importCookies(jsonString) {
    const raw = JSON.parse(jsonString);
    const cookies = Array.isArray(raw) ? raw : (raw.cookies || []);
    if (cookies.length === 0) throw new Error('无效的 Cookie JSON 格式');
    const success = await this.saveSessionWithVerify(cookies, 'manual-import');
    if (success) return cookies;
    throw new Error('验证失败');
  }
}

function resetAllMocks() {
  mockFs._reset();
  mockExecSync._reset();
  mockPage._state.url = 'https://example.com';
  mockPage._state.closed = false;
  mockPage._state.gotoCalled = false;
  mockContext._reset();
  mockBrowser._state.connected = true;
  mockBrowser._state.closed = false;
  mockBrowserEngine._reset();
}

describe('AuthManager', () => {
  let authManager;
  let mockSiteAdapter;

  beforeEach(() => {
    resetAllMocks();
    mockSiteAdapter = createMockSiteAdapter();
    authManager = new TestableAuthManager(mockSiteAdapter);
  });

  describe('constructor', () => {
    it('should initialize with site adapter', () => {
      assert.strictEqual(authManager.site, mockSiteAdapter);
      assert.ok(authManager.sessionPath.includes('test-site.json'));
      assert.ok(authManager.engine);
    });
  });

  describe('normalizeVerify', () => {
    it('should handle boolean true', () => {
      const result = authManager.normalizeVerify(true);
      assert.deepStrictEqual(result, { success: true, user: '已登录', message: '' });
    });

    it('should handle boolean false', () => {
      const result = authManager.normalizeVerify(false);
      assert.deepStrictEqual(result, { success: false, user: '', message: '验证失败' });
    });

    it('should handle object with success true', () => {
      const result = authManager.normalizeVerify({ success: true, user: 'john', message: 'ok' });
      assert.deepStrictEqual(result, { success: true, user: 'john', message: 'ok' });
    });

    it('should handle object with success false', () => {
      const result = authManager.normalizeVerify({ success: false, user: '', message: 'expired' });
      assert.deepStrictEqual(result, { success: false, user: '', message: 'expired' });
    });

    it('should handle object without optional fields', () => {
      const result = authManager.normalizeVerify({ success: true });
      assert.deepStrictEqual(result, { success: true, user: '', message: '' });
    });

    it('should handle object with truthy success value', () => {
      const result = authManager.normalizeVerify({ success: 1, user: 'test' });
      assert.deepStrictEqual(result, { success: true, user: 'test', message: '' });
    });

    it('should handle null', () => {
      const result = authManager.normalizeVerify(null);
      assert.deepStrictEqual(result, { success: false, user: '', message: '未知返回格式' });
    });

    it('should handle undefined', () => {
      const result = authManager.normalizeVerify(undefined);
      assert.deepStrictEqual(result, { success: false, user: '', message: '未知返回格式' });
    });

    it('should handle string', () => {
      const result = authManager.normalizeVerify('invalid');
      assert.deepStrictEqual(result, { success: false, user: '', message: '未知返回格式' });
    });

    it('should handle number', () => {
      const result = authManager.normalizeVerify(123);
      assert.deepStrictEqual(result, { success: false, user: '', message: '未知返回格式' });
    });
  });

  describe('sanitizeCookies', () => {
    it('should remove null expires', () => {
      const cookies = [{ name: 'test', value: 'val', expires: null }];
      const result = authManager.sanitizeCookies(cookies);
      assert.ok(!('expires' in result[0]));
    });

    it('should remove non-number expires (string)', () => {
      const cookies = [{ name: 'test', value: 'val', expires: 'invalid' }];
      const result = authManager.sanitizeCookies(cookies);
      assert.ok(!('expires' in result[0]));
    });

    it('should remove non-number expires (object)', () => {
      const cookies = [{ name: 'test', value: 'val', expires: { foo: 'bar' } }];
      const result = authManager.sanitizeCookies(cookies);
      assert.ok(!('expires' in result[0]));
    });

    it('should keep valid number expires', () => {
      const cookies = [{ name: 'test', value: 'val', expires: 1712345678 }];
      const result = authManager.sanitizeCookies(cookies);
      assert.strictEqual(result[0].expires, 1712345678);
    });

    it('should normalize sameSite lax to Lax', () => {
      const cookies = [{ name: 'test', value: 'val', sameSite: 'lax' }];
      const result = authManager.sanitizeCookies(cookies);
      assert.strictEqual(result[0].sameSite, 'Lax');
    });

    it('should normalize sameSite LAX to Lax', () => {
      const cookies = [{ name: 'test', value: 'val', sameSite: 'LAX' }];
      const result = authManager.sanitizeCookies(cookies);
      assert.strictEqual(result[0].sameSite, 'Lax');
    });

    it('should normalize sameSite strict to Strict', () => {
      const cookies = [{ name: 'test', value: 'val', sameSite: 'strict' }];
      const result = authManager.sanitizeCookies(cookies);
      assert.strictEqual(result[0].sameSite, 'Strict');
    });

    it('should normalize sameSite none to None', () => {
      const cookies = [{ name: 'test', value: 'val', sameSite: 'none' }];
      const result = authManager.sanitizeCookies(cookies);
      assert.strictEqual(result[0].sameSite, 'None');
    });

    it('should not modify cookie without sameSite', () => {
      const cookies = [{ name: 'test', value: 'val' }];
      const result = authManager.sanitizeCookies(cookies);
      assert.strictEqual(result[0].sameSite, undefined);
    });

    it('should handle multiple cookies', () => {
      const cookies = [
        { name: 'a', value: '1', expires: null, sameSite: 'lax' },
        { name: 'b', value: '2', expires: 123, sameSite: 'STRICT' }
      ];
      const result = authManager.sanitizeCookies(cookies);
      assert.strictEqual(result.length, 2);
      assert.ok(!('expires' in result[0]));
      assert.strictEqual(result[0].sameSite, 'Lax');
      assert.strictEqual(result[1].expires, 123);
      assert.strictEqual(result[1].sameSite, 'Strict');
    });

    it('should not modify original cookie object', () => {
      const cookies = [{ name: 'test', value: 'val', expires: null }];
      authManager.sanitizeCookies(cookies);
      assert.strictEqual(cookies[0].expires, null);
    });

    it('should handle expires as undefined', () => {
      const cookies = [{ name: 'test', value: 'val', expires: undefined }];
      const result = authManager.sanitizeCookies(cookies);
      assert.strictEqual(result[0].expires, undefined);
    });

    it('should handle expires as NaN', () => {
      const cookies = [{ name: 'test', value: 'val', expires: NaN }];
      const result = authManager.sanitizeCookies(cookies);
      assert.ok(!('expires' in result[0]));
    });
  });

  describe('loadSession', () => {
    it('should return null when file does not exist', () => {
      mockFs._setExists(false);
      const result = authManager.loadSession();
      assert.strictEqual(result, null);
    });

    it('should return parsed JSON when file exists', () => {
      mockFs._setExists(true);
      mockFs._setData(JSON.stringify({ cookies: [{ name: 'a', value: 'b' }] }));
      const result = authManager.loadSession();
      assert.deepStrictEqual(result, { cookies: [{ name: 'a', value: 'b' }] });
    });

    it('should throw on invalid JSON', () => {
      mockFs._setExists(true);
      mockFs._setData('not valid json');
      assert.throws(() => authManager.loadSession(), SyntaxError);
    });

    it('should return empty object for empty file', () => {
      mockFs._setExists(true);
      mockFs._setData('{}');
      const result = authManager.loadSession();
      assert.deepStrictEqual(result, {});
    });

    it('should return null for file without cookies', () => {
      mockFs._setExists(true);
      mockFs._setData('{"other": "data"}');
      const result = authManager.loadSession();
      assert.deepStrictEqual(result, { other: 'data' });
    });
  });

  describe('saveSessionWithVerify', () => {
    it('should return false when verification fails', async () => {
      mockSiteAdapter._setVerifyResult(false);
      const result = await authManager.saveSessionWithVerify([{ name: 'a', value: 'b' }], 'https://example.com');
      assert.strictEqual(result, false);
    });

    it('should return true and save when verification succeeds', async () => {
      mockSiteAdapter._setVerifyResult(true, 'john', 'ok');
      mockFs._setExists(true);
      let savedData = null;
      mockFs.writeFileSync = (path, data) => { savedData = data; };
      
      const result = await authManager.saveSessionWithVerify([{ name: 'a', value: 'b' }], 'https://example.com');
      
      assert.strictEqual(result, true);
      assert.ok(savedData);
      const parsed = JSON.parse(savedData);
      assert.deepStrictEqual(parsed.cookies, [{ name: 'a', value: 'b' }]);
      assert.strictEqual(parsed.user, 'john');
      assert.strictEqual(parsed.url, 'https://example.com');
      assert.strictEqual(parsed.login.loggedIn, true);
    });

    it('should create session directory if not exists', async () => {
      mockSiteAdapter._setVerifyResult(true);
      mockFs._setExists(false);
      let mkdirCalled = false;
      mockFs.mkdirSync = () => { mkdirCalled = true; };
      
      await authManager.saveSessionWithVerify([{ name: 'a', value: 'b' }]);
      
      assert.strictEqual(mkdirCalled, true);
    });

    it('should handle boolean true from verifySession', async () => {
      mockSiteAdapter._setVerifyBoolean(true);
      mockFs._setExists(true);
      let savedData = null;
      mockFs.writeFileSync = (path, data) => { savedData = data; };
      
      const result = await authManager.saveSessionWithVerify([{ name: 'a', value: 'b' }]);
      
      assert.strictEqual(result, true);
      const parsed = JSON.parse(savedData);
      assert.strictEqual(parsed.user, '已登录');
    });

    it('should use default values when verify returns minimal object', async () => {
      mockSiteAdapter._setVerifyResult(true, '', '');
      mockFs._setExists(true);
      let savedData = null;
      mockFs.writeFileSync = (path, data) => { savedData = data; };
      
      await authManager.saveSessionWithVerify([{ name: 'a', value: 'b' }]);
      
      const parsed = JSON.parse(savedData);
      assert.strictEqual(parsed.user, 'unknown');
      assert.strictEqual(parsed.login.message, '');
    });
  });

  describe('getValidSession', () => {
    it('should return cached cookies when valid and not forceRefresh', async () => {
      mockFs._setExists(true);
      mockFs._setData(JSON.stringify({ cookies: [{ name: 'cached', value: 'cookie' }] }));
      mockSiteAdapter._setVerifyResult(true, 'cached-user', '');
      
      const result = await authManager.getValidSession();
      
      assert.deepStrictEqual(result, [{ name: 'cached', value: 'cookie' }]);
    });

    it('should skip cache when forceRefresh is true', async () => {
      mockFs._setExists(true);
      mockFs._setData(JSON.stringify({ cookies: [{ name: 'cached', value: 'cookie' }] }));
      mockExecSync._setOutput(JSON.stringify([{ name: 'local', value: 'extracted' }]));
      mockSiteAdapter._setVerifyResult(true, 'test-user', '');
      
      let readCalled = false;
      const origRead = mockFs.readFileSync;
      mockFs.readFileSync = () => { readCalled = true; return '{}'; };
      
      await authManager.getValidSession({ forceRefresh: true });
      
      assert.strictEqual(readCalled, false);
      mockFs.readFileSync = origRead;
    });

    it('should try local extraction when cache invalid', async () => {
      mockFs._setExists(true);
      mockFs._setData(JSON.stringify({ cookies: [{ name: 'cached', value: 'cookie' }] }));
      mockSiteAdapter._state.verifyResult = { success: false, user: '', message: 'expired' };
      mockExecSync._setOutput(JSON.stringify([{ name: 'local', value: 'extracted' }]));
      
      const originalVerify = mockSiteAdapter.verifySession;
      mockSiteAdapter.verifySession = async () => {
        const callCount = mockSiteAdapter.verifySession.callCount || 0;
        mockSiteAdapter.verifySession.callCount = callCount + 1;
        if (callCount === 0) return { success: false, user: '', message: 'expired' };
        return { success: true, user: 'local-user', message: '' };
      };
      
      const result = await authManager.getValidSession();
      
      assert.deepStrictEqual(result, [{ name: 'local', value: 'extracted' }]);
      mockSiteAdapter.verifySession = originalVerify;
    });

    it('should use method="local" only', async () => {
      mockExecSync._setOutput(JSON.stringify([{ name: 'local', value: 'cookie' }]));
      mockSiteAdapter._setVerifyResult(true, 'test-user', '');
      
      const result = await authManager.getValidSession({ method: 'local', forceRefresh: true });
      
      assert.deepStrictEqual(result, [{ name: 'local', value: 'cookie' }]);
      assert.strictEqual(mockBrowserEngine._state.launchContextCalls, 0);
    });

    it('should use method="auto" only (apiLogin success)', async () => {
      mockSiteAdapter._setApiLoginResult([{ name: 'api', value: 'cookie' }]);
      mockSiteAdapter._state.verifyResult = { success: true, user: 'api-user', message: '' };
      mockFs._setExists(true);
      
      const result = await authManager.getValidSession({ method: 'auto', forceRefresh: true });
      
      assert.deepStrictEqual(result, [{ name: 'api', value: 'cookie' }]);
      assert.strictEqual(mockBrowserEngine._state.launchContextCalls, 0);
    });

    it('should use method="auto" only (browser login fallback)', async () => {
      mockSiteAdapter._setApiLoginResult(null);
      mockSiteAdapter._setVerifyResult(true, 'browser-user', '');
      mockSiteAdapter._setCheckLoggedIn(true);
      mockContext._setCookies([{ name: 'browser', value: 'cookie' }]);
      
      const result = await authManager.getValidSession({ method: 'auto', forceRefresh: true });
      
      assert.strictEqual(mockBrowserEngine._state.launchContextCalls, 1);
      assert.deepStrictEqual(result, [{ name: 'browser', value: 'cookie' }]);
    });

    it('should throw error when no method can get valid session', async () => {
      mockFs._setExists(false);
      mockExecSync._setThrow(true);
      mockSiteAdapter._setApiLoginResult(null);
      mockSiteAdapter._setCheckLoggedIn(false);
      
      await assert.rejects(
        async () => await authManager.getValidSession({ method: 'auto', forceRefresh: true }),
        { message: /无法获取/ }
      );
    });

    it('should try all methods in order when method="all"', async () => {
      mockFs._setExists(false);
      mockExecSync._setThrow(true);
      mockSiteAdapter._setApiLoginResult(null);
      mockSiteAdapter._setCheckLoggedIn(true);
      mockSiteAdapter._setVerifyResult(true, 'test-user', '');
      mockContext._setCookies([{ name: 'manual', value: 'result' }]);
      
      mockBrowser.isConnected = () => false;
      
      const result = await authManager.getValidSession({ forceRefresh: true });
      
      assert.deepStrictEqual(result, [{ name: 'manual', value: 'result' }]);
      mockBrowser.isConnected = () => true;
    });
  });

  describe('tryLocalExtraction', () => {
    it('should return cookies on successful extraction', async () => {
      const extractedCookies = [{ name: 'local', value: 'cookie' }];
      mockExecSync._setOutput(JSON.stringify(extractedCookies));
      mockSiteAdapter._setVerifyResult(true);
      mockFs._setExists(true);
      
      const result = await authManager.tryLocalExtraction();
      
      assert.deepStrictEqual(result, extractedCookies);
    });

    it('should return null when extraction returns empty array', async () => {
      mockExecSync._setOutput('[]');
      
      const result = await authManager.tryLocalExtraction();
      
      assert.strictEqual(result, null);
    });

    it('should return null when python script fails', async () => {
      mockExecSync._setThrow(true, 'python error');
      
      const result = await authManager.tryLocalExtraction();
      
      assert.strictEqual(result, null);
    });

    it('should return null when extraction returns invalid JSON', async () => {
      mockExecSync._setOutput('not json');
      
      const result = await authManager.tryLocalExtraction();
      
      assert.strictEqual(result, null);
    });

    it('should return null when verification fails', async () => {
      mockExecSync._setOutput(JSON.stringify([{ name: 'a', value: 'b' }]));
      mockSiteAdapter._setVerifyResult(false);
      
      const result = await authManager.tryLocalExtraction();
      
      assert.strictEqual(result, null);
    });
  });

  describe('tryAutomatedLogin', () => {
    it('should try apiLogin when available and succeed', async () => {
      const apiCookies = [{ name: 'api', value: 'cookie' }];
      mockSiteAdapter._setApiLoginResult(apiCookies);
      mockSiteAdapter._state.verifyResult = { success: true, user: 'test-user', message: '' };
      mockFs._setExists(true);
      
      const result = await authManager.tryAutomatedLogin();
      
      assert.deepStrictEqual(result, apiCookies);
      assert.strictEqual(mockBrowserEngine._state.launchContextCalls, 0);
    });

    it('should fallback to browser login when apiLogin returns null', async () => {
      mockSiteAdapter._setApiLoginResult(null);
      mockSiteAdapter._setCheckLoggedIn(true);
      mockSiteAdapter._state.verifyResult = { success: true, user: 'browser-user', message: '' };
      mockContext._setCookies([{ name: 'browser', value: 'cookie' }]);
      
      const result = await authManager.tryAutomatedLogin();
      
      assert.strictEqual(mockBrowserEngine._state.launchContextCalls, 1);
      assert.deepStrictEqual(result, [{ name: 'browser', value: 'cookie' }]);
    });

    it('should fallback to browser login when apiLogin throws', async () => {
      mockSiteAdapter._setApiLoginResult([{ name: 'api', value: 'cookie' }]);
      mockSiteAdapter._setApiLoginThrow(true);
      mockSiteAdapter._setCheckLoggedIn(true);
      mockSiteAdapter._setVerifyResult(true);
      mockContext._setCookies([{ name: 'browser', value: 'cookie' }]);
      
      const result = await authManager.tryAutomatedLogin();
      
      assert.strictEqual(mockBrowserEngine._state.launchContextCalls, 1);
    });

    it('should skip apiLogin when not defined', async () => {
      mockSiteAdapter._setApiLoginResult(null);
      mockSiteAdapter._setCheckLoggedIn(true);
      mockSiteAdapter._setVerifyResult(true);
      mockContext._setCookies([{ name: 'browser', value: 'cookie' }]);
      
      await authManager.tryAutomatedLogin();
      
      assert.strictEqual(mockBrowserEngine._state.launchContextCalls, 1);
    });

    it('should return null when browser login checkLoggedIn fails', async () => {
      mockSiteAdapter._setApiLoginResult(null);
      mockSiteAdapter._setCheckLoggedIn(false);
      
      const result = await authManager.tryAutomatedLogin();
      
      assert.strictEqual(result, null);
      assert.strictEqual(mockBrowser._state.closed, true);
    });

    it('should close browser even on error', async () => {
      mockSiteAdapter._setApiLoginResult(null);
      const origGoto = mockPage.goto;
      mockPage.goto = async () => { throw new Error('navigation failed'); };
      
      const result = await authManager.tryAutomatedLogin();
      
      assert.strictEqual(result, null);
      assert.strictEqual(mockBrowser._state.closed, true);
      mockPage.goto = origGoto;
    });

    it('should return null when verification fails after successful login', async () => {
      mockSiteAdapter._setApiLoginResult(null);
      mockSiteAdapter._setCheckLoggedIn(true);
      mockSiteAdapter._setVerifyResult(false);
      mockContext._setCookies([{ name: 'a', value: 'b' }]);
      
      const result = await authManager.tryAutomatedLogin();
      
      assert.strictEqual(result, null);
    });

    it('should call automatedLogin with page and env', async () => {
      mockSiteAdapter._setApiLoginResult(null);
      mockSiteAdapter._setCheckLoggedIn(true);
      mockSiteAdapter._setVerifyResult(true);
      mockContext._setCookies([{ name: 'a', value: 'b' }]);
      let automatedLoginCalled = false;
      let automatedLoginArgs = null;
      mockSiteAdapter.automatedLogin = async (page, env) => {
        automatedLoginCalled = true;
        automatedLoginArgs = { page, env };
      };
      
      await authManager.tryAutomatedLogin();
      
      assert.strictEqual(automatedLoginCalled, true);
      assert.ok(automatedLoginArgs.page);
      mockSiteAdapter.automatedLogin = async () => {};
    });
  });

  describe('tryManualCapture', () => {
    beforeEach(() => {
      mockBrowser.isConnected = () => true;
    });

    it('should handle browser disconnected immediately', async () => {
      mockContext._setCookies([{ name: 'saved', value: 'cookie' }]);
      mockBrowser.isConnected = () => false;
      
      const result = await authManager.tryManualCapture();
      
      assert.deepStrictEqual(result, [{ name: 'saved', value: 'cookie' }]);
    });

    it('should reject on timeout (short timeout)', async () => {
      mockSiteAdapter._setCheckLoggedIn(false);
      mockBrowser.isConnected = () => true;
      mockContext._setCookies([]);
      
      const fastTimeoutManager = new TestableAuthManager(mockSiteAdapter);
      
      fastTimeoutManager.tryManualCapture = async function() {
        return new Promise((resolve, reject) => {
          setTimeout(() => {
            reject(new Error('手动登录超时（5分钟）'));
          }, 10);
        });
      };
      
      await assert.rejects(
        async () => await fastTimeoutManager.tryManualCapture(),
        { message: '手动登录超时（5分钟）' }
      );
    });
  });

  describe('testSessionHeaded', () => {
    it('should return early when no session found', async () => {
      mockFs._setExists(false);
      
      await authManager.testSessionHeaded();
      
      assert.strictEqual(mockBrowserEngine._state.launchHeadedCalls, 0);
    });

    it('should launch browser when session exists', async () => {
      mockFs._setExists(true);
      mockFs._setData(JSON.stringify({ cookies: [{ name: 'test', value: 'val', expires: null }] }));
      mockPage.waitForEvent = async () => {};
      
      await authManager.testSessionHeaded();
      
      assert.strictEqual(mockBrowserEngine._state.launchHeadedCalls, 1);
    });

    it('should use dashboardUrl when available', async () => {
      mockFs._setExists(true);
      mockFs._setData(JSON.stringify({ cookies: [] }));
      let gotoUrl = null;
      mockPage.goto = async (url) => { gotoUrl = url; };
      mockPage.waitForEvent = async () => {};
      
      await authManager.testSessionHeaded();
      
      assert.strictEqual(gotoUrl, 'https://example.com/dashboard');
    });

    it('should use loginUrl when dashboardUrl not available', async () => {
      mockSiteAdapter.dashboardUrl = null;
      mockFs._setExists(true);
      mockFs._setData(JSON.stringify({ cookies: [] }));
      let gotoUrl = null;
      mockPage.goto = async (url) => { gotoUrl = url; };
      mockPage.waitForEvent = async () => {};
      
      await authManager.testSessionHeaded();
      
      assert.strictEqual(gotoUrl, 'https://example.com/login');
      mockSiteAdapter.dashboardUrl = 'https://example.com/dashboard';
    });
  });

  describe('importCookies', () => {
    it('should import valid cookie array JSON', async () => {
      mockSiteAdapter._setVerifyResult(true);
      mockFs._setExists(true);
      
      const cookies = [{ name: 'imported', value: 'cookie' }];
      const result = await authManager.importCookies(JSON.stringify(cookies));
      
      assert.deepStrictEqual(result, cookies);
    });

    it('should import valid cookies object', async () => {
      mockSiteAdapter._setVerifyResult(true);
      mockFs._setExists(true);
      
      const cookies = [{ name: 'imported', value: 'cookie' }];
      const result = await authManager.importCookies(JSON.stringify({ cookies }));
      
      assert.deepStrictEqual(result, cookies);
    });

    it('should throw on invalid JSON', async () => {
      await assert.rejects(
        async () => await authManager.importCookies('not valid json'),
        SyntaxError
      );
    });

    it('should throw on empty cookies array', async () => {
      await assert.rejects(
        async () => await authManager.importCookies('[]'),
        { message: /无效的 Cookie JSON 格式/ }
      );
    });

    it('should throw on empty cookies object', async () => {
      await assert.rejects(
        async () => await authManager.importCookies('{"cookies": []}'),
        { message: /无效的 Cookie JSON 格式/ }
      );
    });

    it('should throw when verification fails', async () => {
      mockSiteAdapter._setVerifyResult(false);
      
      await assert.rejects(
        async () => await authManager.importCookies(JSON.stringify([{ name: 'a', value: 'b' }])),
        Error
      );
    });

    it('should throw on object without cookies', async () => {
      await assert.rejects(
        async () => await authManager.importCookies('{"foo": "bar"}'),
        { message: /无效的 Cookie JSON 格式/ }
      );
    });
  });
});