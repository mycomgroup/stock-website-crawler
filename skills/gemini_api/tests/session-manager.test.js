import { strict as assert } from 'assert';
import { readFileSync, writeFileSync, existsSync, mkdirSync, rmSync } from 'fs';
import { tmpdir } from 'os';
import { join } from 'path';

const testDir = join(tmpdir(), 'session-manager-test-' + Date.now());
const sessionFile = join(testDir, 'session.json');

function setupTestDir() {
  if (!existsSync(testDir)) {
    mkdirSync(testDir, { recursive: true });
  }
}

function cleanupTestDir() {
  if (existsSync(testDir)) {
    rmSync(testDir, { recursive: true, force: true });
  }
}

function createSessionData(daysAgo = 0) {
  const capturedAt = new Date(Date.now() - daysAgo * 24 * 60 * 60 * 1000);
  return {
    capturedAt: capturedAt.toISOString(),
    cookies: [
      { name: '__Secure-next-auth.session-token', value: 'test-token' },
      { name: '__Secure-next-auth.callback-url', value: 'https://example.com' },
      { name: '_cfuvid', value: 'cfuvid-value' },
      { name: 'cf_clearance', value: 'cf-clearance-value' },
      { name: 'other-cookie', value: 'other-value' }
    ],
    userAgent: 'TestAgent/1.0'
  };
}

class TestableSessionManager {
  constructor(sessionFilePath) {
    this.sessionData = null;
    this.sessionFile = sessionFilePath;
    this._validateResult = true;
    this._captureResult = null;
  }

  loadSession() {
    if (!existsSync(this.sessionFile)) {
      console.log('⚠️  未找到 session 文件，需要先登录');
      return null;
    }

    try {
      const content = readFileSync(this.sessionFile, 'utf-8');
      this.sessionData = JSON.parse(content);
      
      const capturedAt = new Date(this.sessionData.capturedAt);
      const daysAgo = Math.floor((Date.now() - capturedAt.getTime()) / (1000 * 60 * 60 * 24));
      
      console.log(`📂 加载 session (捕获于 ${daysAgo} 天前)`);
      
      return this.sessionData;
    } catch (error) {
      console.error('❌ 加载 session 失败:', error.message);
      return null;
    }
  }

  getCookies() {
    if (!this.sessionData) {
      this.loadSession();
    }

    if (!this.sessionData) {
      throw new Error('No session data available. Please login first.');
    }

    const cookieString = this.sessionData.cookies
      .map(cookie => `${cookie.name}=${cookie.value}`)
      .join('; ');

    return cookieString;
  }

  getCookie(name) {
    if (!this.sessionData) {
      this.loadSession();
    }

    if (!this.sessionData) {
      return null;
    }

    const cookie = this.sessionData.cookies.find(c => c.name === name);
    return cookie ? cookie.value : null;
  }

  getAuthCookies() {
    return {
      sessionToken: this.getCookie('__Secure-next-auth.session-token'),
      callbackUrl: this.getCookie('__Secure-next-auth.callback-url'),
      cfuvid: this.getCookie('_cfuvid'),
      cfClearance: this.getCookie('cf_clearance')
    };
  }

  async validateSession() {
    if (!this.sessionData) {
      this.loadSession();
    }

    if (!this.sessionData) {
      return false;
    }

    const capturedAt = new Date(this.sessionData.capturedAt);
    const daysAgo = Math.floor((Date.now() - capturedAt.getTime()) / (1000 * 60 * 60 * 24));
    
    if (daysAgo > 30) {
      console.log('⚠️  Session 已过期（超过 30 天）');
      return false;
    }

    return this._validateResult;
  }

  async refreshSession(options = {}) {
    console.log('🔄 刷新 session...');
    if (this._captureResult) {
      this.sessionData = this._captureResult;
      return this.sessionData;
    }
    this.sessionData = createSessionData(0);
    return this.sessionData;
  }

  async ensureValidSession(options = {}) {
    if (!this.sessionData) {
      this.loadSession();
    }

    if (!this.sessionData) {
      console.log('🔐 首次使用，需要登录');
      return await this.refreshSession(options);
    }

    const isValid = await this.validateSession();
    
    if (!isValid) {
      console.log('🔄 Session 已失效，需要重新登录');
      return await this.refreshSession(options);
    }

    return this.sessionData;
  }

  getUserAgent() {
    if (!this.sessionData) {
      this.loadSession();
    }

    return this.sessionData?.userAgent || 
           'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36';
  }
}

let testsPassed = 0;
let testsFailed = 0;

function test(name, fn) {
  try {
    fn();
    console.log(`✅ ${name}`);
    testsPassed++;
  } catch (error) {
    console.log(`❌ ${name}`);
    console.log(`   Error: ${error.message}`);
    testsFailed++;
  }
}

async function testAsync(name, fn) {
  try {
    await fn();
    console.log(`✅ ${name}`);
    testsPassed++;
  } catch (error) {
    console.log(`❌ ${name}`);
    console.log(`   Error: ${error.message}`);
    testsFailed++;
  }
}

console.log('\n=== SessionManager Unit Tests ===\n');
console.log(`Test directory: ${testDir}\n`);

setupTestDir();

test('constructor initializes sessionData as null', () => {
  const manager = new TestableSessionManager(sessionFile);
  assert.strictEqual(manager.sessionData, null);
});

test('loadSession returns null when session file does not exist', () => {
  cleanupTestDir();
  setupTestDir();
  
  const manager = new TestableSessionManager(join(testDir, 'nonexistent.json'));
  const result = manager.loadSession();
  
  assert.strictEqual(result, null);
  assert.strictEqual(manager.sessionData, null);
});

test('loadSession loads and parses session file correctly', () => {
  cleanupTestDir();
  setupTestDir();
  
  const sessionData = createSessionData(5);
  writeFileSync(sessionFile, JSON.stringify(sessionData), 'utf-8');
  
  const manager = new TestableSessionManager(sessionFile);
  const result = manager.loadSession();
  
  assert.strictEqual(result.capturedAt, sessionData.capturedAt);
  assert.strictEqual(result.cookies.length, 5);
  assert.strictEqual(result.userAgent, 'TestAgent/1.0');
});

test('loadSession handles JSON parse error', () => {
  cleanupTestDir();
  setupTestDir();
  
  writeFileSync(sessionFile, 'invalid json {{{', 'utf-8');
  
  const manager = new TestableSessionManager(sessionFile);
  const result = manager.loadSession();
  
  assert.strictEqual(result, null);
  assert.strictEqual(manager.sessionData, null);
});

test('loadSession calculates days ago correctly', () => {
  cleanupTestDir();
  setupTestDir();
  
  const sessionData = createSessionData(10);
  writeFileSync(sessionFile, JSON.stringify(sessionData), 'utf-8');
  
  const manager = new TestableSessionManager(sessionFile);
  manager.loadSession();
  
  assert.ok(manager.sessionData.capturedAt);
});

test('getCookies throws error when no session data', () => {
  cleanupTestDir();
  setupTestDir();
  
  const manager = new TestableSessionManager(sessionFile);
  
  assert.throws(
    () => manager.getCookies(),
    { message: 'No session data available. Please login first.' }
  );
});

test('getCookies returns cookie string correctly', () => {
  cleanupTestDir();
  setupTestDir();
  
  const sessionData = createSessionData();
  writeFileSync(sessionFile, JSON.stringify(sessionData), 'utf-8');
  
  const manager = new TestableSessionManager(sessionFile);
  manager.loadSession();
  const cookies = manager.getCookies();
  
  assert.strictEqual(cookies, '__Secure-next-auth.session-token=test-token; __Secure-next-auth.callback-url=https://example.com; _cfuvid=cfuvid-value; cf_clearance=cf-clearance-value; other-cookie=other-value');
});

test('getCookie returns value for existing cookie', () => {
  cleanupTestDir();
  setupTestDir();
  
  const sessionData = createSessionData();
  writeFileSync(sessionFile, JSON.stringify(sessionData), 'utf-8');
  
  const manager = new TestableSessionManager(sessionFile);
  manager.loadSession();
  const value = manager.getCookie('__Secure-next-auth.session-token');
  
  assert.strictEqual(value, 'test-token');
});

test('getCookie returns null for non-existing cookie', () => {
  cleanupTestDir();
  setupTestDir();
  
  const sessionData = createSessionData();
  writeFileSync(sessionFile, JSON.stringify(sessionData), 'utf-8');
  
  const manager = new TestableSessionManager(sessionFile);
  manager.loadSession();
  const value = manager.getCookie('non-existent');
  
  assert.strictEqual(value, null);
});

test('getCookie returns null when no session data', () => {
  cleanupTestDir();
  setupTestDir();
  
  const manager = new TestableSessionManager(sessionFile);
  const value = manager.getCookie('any-cookie');
  
  assert.strictEqual(value, null);
});

test('getAuthCookies returns all auth cookies', () => {
  cleanupTestDir();
  setupTestDir();
  
  const sessionData = createSessionData();
  writeFileSync(sessionFile, JSON.stringify(sessionData), 'utf-8');
  
  const manager = new TestableSessionManager(sessionFile);
  manager.loadSession();
  const authCookies = manager.getAuthCookies();
  
  assert.deepStrictEqual(authCookies, {
    sessionToken: 'test-token',
    callbackUrl: 'https://example.com',
    cfuvid: 'cfuvid-value',
    cfClearance: 'cf-clearance-value'
  });
});

test('getUserAgent returns user agent from session data', () => {
  cleanupTestDir();
  setupTestDir();
  
  const sessionData = createSessionData();
  writeFileSync(sessionFile, JSON.stringify(sessionData), 'utf-8');
  
  const manager = new TestableSessionManager(sessionFile);
  manager.loadSession();
  const ua = manager.getUserAgent();
  
  assert.strictEqual(ua, 'TestAgent/1.0');
});

test('getUserAgent returns default user agent when no session', () => {
  cleanupTestDir();
  setupTestDir();
  
  const manager = new TestableSessionManager(sessionFile);
  const ua = manager.getUserAgent();
  
  assert.ok(ua.includes('Chrome'));
});

async function runAsyncTests() {
  await testAsync('validateSession returns false when no session data', async () => {
    cleanupTestDir();
    setupTestDir();
    
    const manager = new TestableSessionManager(sessionFile);
    manager._validateResult = true;
    const result = await manager.validateSession();
    
    assert.strictEqual(result, false);
  });

  await testAsync('validateSession returns false when session too old (> 30 days)', async () => {
    cleanupTestDir();
    setupTestDir();
    
    const sessionData = createSessionData(35);
    writeFileSync(sessionFile, JSON.stringify(sessionData), 'utf-8');
    
    const manager = new TestableSessionManager(sessionFile);
    manager.loadSession();
    manager._validateResult = true;
    const result = await manager.validateSession();
    
    assert.strictEqual(result, false);
  });

  await testAsync('validateSession returns true for valid age', async () => {
    cleanupTestDir();
    setupTestDir();
    
    const sessionData = createSessionData(5);
    writeFileSync(sessionFile, JSON.stringify(sessionData), 'utf-8');
    
    const manager = new TestableSessionManager(sessionFile);
    manager.loadSession();
    manager._validateResult = true;
    const result = await manager.validateSession();
    
    assert.strictEqual(result, true);
  });

  await testAsync('validateSession returns false when browser validation fails', async () => {
    cleanupTestDir();
    setupTestDir();
    
    const sessionData = createSessionData(5);
    writeFileSync(sessionFile, JSON.stringify(sessionData), 'utf-8');
    
    const manager = new TestableSessionManager(sessionFile);
    manager.loadSession();
    manager._validateResult = false;
    const result = await manager.validateSession();
    
    assert.strictEqual(result, false);
  });

  await testAsync('refreshSession updates sessionData', async () => {
    cleanupTestDir();
    setupTestDir();
    
    const manager = new TestableSessionManager(sessionFile);
    manager._captureResult = createSessionData(0);
    manager._captureResult.userAgent = 'NewAgent/2.0';
    
    const result = await manager.refreshSession();
    
    assert.strictEqual(result.userAgent, 'NewAgent/2.0');
    assert.deepStrictEqual(manager.sessionData, result);
  });

  await testAsync('ensureValidSession loads existing valid session', async () => {
    cleanupTestDir();
    setupTestDir();
    
    const sessionData = createSessionData(1);
    writeFileSync(sessionFile, JSON.stringify(sessionData), 'utf-8');
    
    const manager = new TestableSessionManager(sessionFile);
    manager._validateResult = true;
    const result = await manager.ensureValidSession();
    
    assert.strictEqual(result.capturedAt, sessionData.capturedAt);
  });

  await testAsync('ensureValidSession creates new session when none exists', async () => {
    cleanupTestDir();
    setupTestDir();
    
    const manager = new TestableSessionManager(sessionFile);
    manager._captureResult = createSessionData(0);
    manager._captureResult.userAgent = 'FreshAgent/3.0';
    
    const result = await manager.ensureValidSession();
    
    assert.strictEqual(result.userAgent, 'FreshAgent/3.0');
  });

  await testAsync('ensureValidSession refreshes when session invalid', async () => {
    cleanupTestDir();
    setupTestDir();
    
    const sessionData = createSessionData(1);
    writeFileSync(sessionFile, JSON.stringify(sessionData), 'utf-8');
    
    const manager = new TestableSessionManager(sessionFile);
    manager._validateResult = false;
    manager._captureResult = createSessionData(0);
    manager._captureResult.userAgent = 'RefreshedAgent/4.0';
    
    const result = await manager.ensureValidSession();
    
    assert.strictEqual(result.userAgent, 'RefreshedAgent/4.0');
  });

  await testAsync('ensureValidSession refreshes when session expired (> 30 days)', async () => {
    cleanupTestDir();
    setupTestDir();
    
    const oldSession = createSessionData(35);
    writeFileSync(sessionFile, JSON.stringify(oldSession), 'utf-8');
    
    const manager = new TestableSessionManager(sessionFile);
    manager._captureResult = createSessionData(0);
    manager._captureResult.userAgent = 'NewAgent/5.0';
    
    const result = await manager.ensureValidSession();
    
    assert.strictEqual(result.userAgent, 'NewAgent/5.0');
  });
}

await runAsyncTests();

cleanupTestDir();

console.log('\n=== Test Summary ===');
console.log(`Passed: ${testsPassed}`);
console.log(`Failed: ${testsFailed}`);
console.log(`Total: ${testsPassed + testsFailed}`);

if (testsFailed > 0) {
  process.exit(1);
}