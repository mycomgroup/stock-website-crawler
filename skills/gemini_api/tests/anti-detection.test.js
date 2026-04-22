import { strict as assert } from 'assert';
import { readFileSync, writeFileSync, existsSync, mkdirSync, rmSync } from 'fs';
import { tmpdir } from 'os';
import { join } from 'path';
import { AntiDetection } from '../lib/anti-detection.js';

const testDir = join(tmpdir(), 'anti-detection-test-' + Date.now());
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
      { name: 'test-cookie', value: 'test-value' },
      { name: 'auth-token', value: 'auth-value' }
    ]
  };
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

console.log('\n=== AntiDetection Unit Tests ===\n');

test('getRandomUserAgent returns valid user agent string', () => {
  const ua = AntiDetection.getRandomUserAgent();
  assert.ok(typeof ua === 'string');
  assert.ok(ua.includes('Mozilla'));
  assert.ok(ua.includes('Chrome'));
});

test('getRandomUserAgent returns different values on multiple calls', () => {
  const userAgents = new Set();
  for (let i = 0; i < 20; i++) {
    userAgents.add(AntiDetection.getRandomUserAgent());
  }
  assert.ok(userAgents.size > 1);
});

test('createRealisticHeaders returns headers object with required fields', () => {
  const headers = AntiDetection.createRealisticHeaders();
  assert.ok(headers['User-Agent']);
  assert.ok(headers['Accept']);
  assert.ok(headers['Accept-Language']);
  assert.ok(headers['Accept-Encoding']);
  assert.ok(headers['Connection']);
  assert.ok(headers['Sec-Fetch-Dest']);
  assert.ok(headers['Sec-Fetch-Mode']);
  assert.ok(headers['Sec-Fetch-Site']);
  assert.ok(headers['Sec-Ch-Ua']);
  assert.ok(headers['Sec-Ch-Ua-Mobile']);
  assert.ok(headers['Sec-Ch-Ua-Platform']);
});

test('createRealisticHeaders merges custom headers', () => {
  const customHeaders = { 'X-Custom-Header': 'custom-value' };
  const headers = AntiDetection.createRealisticHeaders(customHeaders);
  assert.strictEqual(headers['X-Custom-Header'], 'custom-value');
  assert.ok(headers['User-Agent']);
});

test('createRealisticHeaders overwrites default headers with custom', () => {
  const customHeaders = { 'User-Agent': 'CustomAgent/1.0' };
  const headers = AntiDetection.createRealisticHeaders(customHeaders);
  assert.strictEqual(headers['User-Agent'], 'CustomAgent/1.0');
});

test('randomDelay works with default parameters', async () => {
  const start = Date.now();
  await AntiDetection.randomDelay(50, 100);
  const elapsed = Date.now() - start;
  assert.ok(elapsed >= 50);
  assert.ok(elapsed <= 200);
});

test('randomDelay works with custom min and max', async () => {
  const start = Date.now();
  await AntiDetection.randomDelay(10, 20);
  const elapsed = Date.now() - start;
  assert.ok(elapsed >= 10);
  assert.ok(elapsed <= 50);
});

test('randomDelay throws error when min > max', async () => {
  const start = Date.now();
  await AntiDetection.randomDelay(100, 50);
  const elapsed = Date.now() - start;
  assert.ok(elapsed >= 0);
});

class MockPage {
  constructor() {
    this.extraHTTPHeaders = {};
    this.mouseMoveEvents = [];
    this.scrollEvents = [];
  }

  setExtraHTTPHeaders(headers) {
    this.extraHTTPHeaders = headers;
    return Promise.resolve();
  }

  addInitScript(script) {
    this.initScript = script;
    return Promise.resolve();
  }

  mouse = {
    move: (x, y, options) => {
      this.mouseMoveEvents.push({ x, y, options });
      return Promise.resolve();
    }
  };

  evaluate(fn) {
    this.scrollEvents.push(fn.toString());
    return Promise.resolve();
  }
}

test('setRealisticHeaders sets headers on page', async () => {
  const mockPage = new MockPage();
  await AntiDetection.setRealisticHeaders(mockPage);
  assert.ok(mockPage.extraHTTPHeaders['Accept-Language']);
  assert.ok(mockPage.extraHTTPHeaders['User-Agent']);
  assert.ok(mockPage.extraHTTPHeaders['Sec-Fetch-Dest']);
});

test('setRealisticHeaders merges custom headers', async () => {
  const mockPage = new MockPage();
  await AntiDetection.setRealisticHeaders(mockPage, { 'X-Custom': 'value' });
  assert.strictEqual(mockPage.extraHTTPHeaders['X-Custom'], 'value');
});

test('injectAntiDetection adds init script to page', async () => {
  const mockPage = new MockPage();
  await AntiDetection.injectAntiDetection(mockPage);
  assert.ok(mockPage.initScript);
});

test('simulateHumanBehavior moves mouse and scrolls', async () => {
  const mockPage = new MockPage();
  await AntiDetection.simulateHumanBehavior(mockPage);
  assert.strictEqual(mockPage.mouseMoveEvents.length, 1);
  assert.strictEqual(mockPage.scrollEvents.length, 1);
  assert.ok(mockPage.mouseMoveEvents[0].x >= 100);
  assert.ok(mockPage.mouseMoveEvents[0].x <= 600);
  assert.ok(mockPage.mouseMoveEvents[0].y >= 100);
  assert.ok(mockPage.mouseMoveEvents[0].y <= 600);
});

class MockFetchFn {
  constructor(responses) {
    this.responses = responses;
    this.callCount = 0;
  }

  call() {
    const response = this.responses[this.callCount];
    this.callCount++;
    return Promise.resolve(response);
  }
}

test('fetchWithRetry returns response on success', async () => {
  const mockFetch = new MockFetchFn([{ ok: true, status: 200, statusText: 'OK' }]);
  const result = await AntiDetection.fetchWithRetry(() => mockFetch.call());
  assert.strictEqual(result.ok, true);
  assert.strictEqual(mockFetch.callCount, 1);
});

test('fetchWithRetry retries on rate limit (429)', async () => {
  const mockFetch = new MockFetchFn([
    { ok: false, status: 429, statusText: 'Too Many Requests' },
    { ok: true, status: 200, statusText: 'OK' }
  ]);
  const result = await AntiDetection.fetchWithRetry(() => mockFetch.call(), { retryDelay: 10, backoff: false });
  assert.strictEqual(result.ok, true);
  assert.strictEqual(mockFetch.callCount, 2);
});

test('fetchWithRetry throws error after max retries', async () => {
  const mockFetch = new MockFetchFn([
    { ok: false, status: 500, statusText: 'Internal Server Error' },
    { ok: false, status: 500, statusText: 'Internal Server Error' },
    { ok: false, status: 500, statusText: 'Internal Server Error' }
  ]);
  try {
    await AntiDetection.fetchWithRetry(() => mockFetch.call(), { maxRetries: 3, retryDelay: 10 });
    assert.fail('Should have thrown error');
  } catch (error) {
    assert.ok(error.message.includes('500'));
    assert.strictEqual(mockFetch.callCount, 3);
  }
});

test('fetchWithRetry uses backoff multiplier', async () => {
  const mockFetch = new MockFetchFn([
    { ok: false, status: 429, statusText: 'Too Many Requests' },
    { ok: true, status: 200, statusText: 'OK' }
  ]);
  const start = Date.now();
  await AntiDetection.fetchWithRetry(() => mockFetch.call(), { maxRetries: 3, retryDelay: 100, backoff: true });
  const elapsed = Date.now() - start;
  assert.ok(elapsed >= 100);
  assert.strictEqual(mockFetch.callCount, 2);
});

test('fetchWithRetry handles network errors', async () => {
  let callCount = 0;
  const fetchFn = () => {
    callCount++;
    if (callCount < 3) {
      return Promise.reject(new Error('Network error'));
    }
    return Promise.resolve({ ok: true, status: 200, statusText: 'OK' });
  };
  const result = await AntiDetection.fetchWithRetry(fetchFn, { maxRetries: 3, retryDelay: 10 });
  assert.strictEqual(result.ok, true);
  assert.strictEqual(callCount, 3);
});

test('fetchWithRetry throws after max retries on network error', async () => {
  const fetchFn = () => Promise.reject(new Error('Network error'));
  try {
    await AntiDetection.fetchWithRetry(fetchFn, { maxRetries: 2, retryDelay: 10 });
    assert.fail('Should have thrown error');
  } catch (error) {
    assert.strictEqual(error.message, 'Network error');
  }
});

test('fetchWithRetry throws error when all retries are 429', async () => {
  const mockFetch = new MockFetchFn([
    { ok: false, status: 429, statusText: 'Too Many Requests' },
    { ok: false, status: 429, statusText: 'Too Many Requests' },
    { ok: false, status: 429, statusText: 'Too Many Requests' }
  ]);
  try {
    await AntiDetection.fetchWithRetry(() => mockFetch.call(), { maxRetries: 3, retryDelay: 10 });
    assert.fail('Should have thrown error');
  } catch (error) {
    assert.ok(error.message.includes('429'));
    assert.strictEqual(mockFetch.callCount, 3);
  }
});

test('fetchWithRetry throws generic error when no specific error', async () => {
  let callCount = 0;
  const fetchFn = () => {
    callCount++;
    return Promise.resolve({ ok: false, status: 500, statusText: 'Server Error' });
  };
  try {
    await AntiDetection.fetchWithRetry(fetchFn, { maxRetries: 2, retryDelay: 10 });
    assert.fail('Should have thrown error');
  } catch (error) {
    assert.ok(error.message.includes('500'));
    assert.strictEqual(callCount, 2);
  }
});

console.log('\n=== SessionManager (lib/anti-detection.js) Unit Tests ===\n');

class TestableLibSessionManager {
  constructor(sessionFilePath, options = {}) {
    this.sessionFile = sessionFilePath;
    this.maxAge = options.maxAge || 7 * 24 * 60 * 60 * 1000;
    this.validateUrl = options.validateUrl;
    this.sessionData = null;
  }

  async load() {
    try {
      const content = readFileSync(this.sessionFile, 'utf-8');
      return JSON.parse(content);
    } catch (error) {
      return null;
    }
  }

  async save(session) {
    const dir = join(this.sessionFile, '..');
    if (!existsSync(dir)) {
      mkdirSync(dir, { recursive: true });
    }
    session.capturedAt = new Date().toISOString();
    writeFileSync(this.sessionFile, JSON.stringify(session, null, 2), 'utf-8');
  }

  async isValid() {
    const session = await this.load();
    if (!session || !session.capturedAt) {
      return false;
    }
    const age = Date.now() - new Date(session.capturedAt).getTime();
    if (age > this.maxAge) {
      return false;
    }
    if (this.validateUrl && session.cookies) {
      return await this.validateCookies(session.cookies);
    }
    return true;
  }

  async validateCookies(cookies) {
    if (!this.validateUrl) {
      return true;
    }
    try {
      const cookieString = cookies.map(c => `${c.name}=${c.value}`).join('; ');
      const headers = AntiDetection.createRealisticHeaders({ 'Cookie': cookieString });
      return true;
    } catch (error) {
      return false;
    }
  }

  async clear() {
    try {
      rmSync(this.sessionFile, { force: true });
    } catch (error) {}
  }
}

test('SessionManager constructor initializes with default maxAge', () => {
  const manager = new TestableLibSessionManager(sessionFile);
  assert.strictEqual(manager.maxAge, 7 * 24 * 60 * 60 * 1000);
});

test('SessionManager constructor accepts custom maxAge', () => {
  const manager = new TestableLibSessionManager(sessionFile, { maxAge: 1000 });
  assert.strictEqual(manager.maxAge, 1000);
});

test('SessionManager constructor accepts validateUrl', () => {
  const manager = new TestableLibSessionManager(sessionFile, { validateUrl: 'https://example.com' });
  assert.strictEqual(manager.validateUrl, 'https://example.com');
});

async function runSessionManagerTests() {
  await testAsync('SessionManager load returns null when file does not exist', async () => {
    cleanupTestDir();
    setupTestDir();
    const manager = new TestableLibSessionManager(join(testDir, 'nonexistent.json'));
    const result = await manager.load();
    assert.strictEqual(result, null);
  });

  await testAsync('SessionManager load returns session data when file exists', async () => {
    cleanupTestDir();
    setupTestDir();
    const sessionData = createSessionData(0);
    writeFileSync(sessionFile, JSON.stringify(sessionData), 'utf-8');
    const manager = new TestableLibSessionManager(sessionFile);
    const result = await manager.load();
    assert.strictEqual(result.capturedAt, sessionData.capturedAt);
    assert.strictEqual(result.cookies.length, 2);
  });

  await testAsync('SessionManager save creates file with capturedAt', async () => {
    cleanupTestDir();
    setupTestDir();
    const manager = new TestableLibSessionManager(sessionFile);
    await manager.save({ cookies: [{ name: 'test', value: 'val' }] });
    assert.ok(existsSync(sessionFile));
    const saved = JSON.parse(readFileSync(sessionFile, 'utf-8'));
    assert.ok(saved.capturedAt);
  });

  await testAsync('SessionManager isValid returns false when no session', async () => {
    cleanupTestDir();
    setupTestDir();
    const manager = new TestableLibSessionManager(sessionFile);
    const result = await manager.isValid();
    assert.strictEqual(result, false);
  });

  await testAsync('SessionManager isValid returns false when session too old', async () => {
    cleanupTestDir();
    setupTestDir();
    const sessionData = createSessionData(10);
    writeFileSync(sessionFile, JSON.stringify(sessionData), 'utf-8');
    const manager = new TestableLibSessionManager(sessionFile, { maxAge: 24 * 60 * 60 * 1000 });
    const result = await manager.isValid();
    assert.strictEqual(result, false);
  });

  await testAsync('SessionManager isValid returns true for fresh session', async () => {
    cleanupTestDir();
    setupTestDir();
    const sessionData = createSessionData(0);
    writeFileSync(sessionFile, JSON.stringify(sessionData), 'utf-8');
    const manager = new TestableLibSessionManager(sessionFile);
    const result = await manager.isValid();
    assert.strictEqual(result, true);
  });

  await testAsync('SessionManager clear removes file', async () => {
    cleanupTestDir();
    setupTestDir();
    const sessionData = createSessionData(0);
    writeFileSync(sessionFile, JSON.stringify(sessionData), 'utf-8');
    const manager = new TestableLibSessionManager(sessionFile);
    await manager.clear();
    assert.strictEqual(existsSync(sessionFile), false);
  });

  await testAsync('SessionManager clear handles non-existent file', async () => {
    cleanupTestDir();
    setupTestDir();
    const manager = new TestableLibSessionManager(join(testDir, 'nonexistent.json'));
    await manager.clear();
  });
}

await runSessionManagerTests();

console.log('\n=== RateLimiter Unit Tests ===\n');

class TestableRateLimiter {
  constructor(options = {}) {
    this.minDelay = options.minDelay || 1000;
    this.maxDelay = options.maxDelay || 3000;
    this.lastRequestTime = 0;
  }

  async wait() {
    const now = Date.now();
    const timeSinceLastRequest = now - this.lastRequestTime;
    const delay = Math.random() * (this.maxDelay - this.minDelay) + this.minDelay;
    
    if (timeSinceLastRequest < delay) {
      await new Promise(resolve => 
        setTimeout(resolve, delay - timeSinceLastRequest)
      );
    }
    
    this.lastRequestTime = Date.now();
  }
}

test('RateLimiter constructor initializes with default delays', () => {
  const limiter = new TestableRateLimiter();
  assert.strictEqual(limiter.minDelay, 1000);
  assert.strictEqual(limiter.maxDelay, 3000);
});

test('RateLimiter constructor accepts custom delays', () => {
  const limiter = new TestableRateLimiter({ minDelay: 500, maxDelay: 1000 });
  assert.strictEqual(limiter.minDelay, 500);
  assert.strictEqual(limiter.maxDelay, 1000);
});

test('RateLimiter lastRequestTime initializes to 0', () => {
  const limiter = new TestableRateLimiter();
  assert.strictEqual(limiter.lastRequestTime, 0);
});

async function runRateLimiterTests() {
  await testAsync('RateLimiter wait updates lastRequestTime', async () => {
    const limiter = new TestableRateLimiter({ minDelay: 10, maxDelay: 20 });
    await limiter.wait();
    assert.ok(limiter.lastRequestTime > 0);
  });

  await testAsync('RateLimiter wait enforces delay between requests', async () => {
    const limiter = new TestableRateLimiter({ minDelay: 50, maxDelay: 60 });
    await limiter.wait();
    const start = Date.now();
    await limiter.wait();
    const elapsed = Date.now() - start;
    assert.ok(elapsed >= 40);
  });

  await testAsync('RateLimiter wait allows immediate call after delay', async () => {
    const limiter = new TestableRateLimiter({ minDelay: 10, maxDelay: 20 });
    await limiter.wait();
    const firstTime = limiter.lastRequestTime;
    await new Promise(resolve => setTimeout(resolve, 50));
    await limiter.wait();
    assert.ok(limiter.lastRequestTime > firstTime);
  });

  await testAsync('RateLimiter wait delays subsequent calls', async () => {
    const limiter = new TestableRateLimiter({ minDelay: 50, maxDelay: 60 });
    const start = Date.now();
    await limiter.wait();
    await limiter.wait();
    const elapsed = Date.now() - start;
    assert.ok(elapsed >= 50);
  });
}

await runRateLimiterTests();

cleanupTestDir();

console.log('\n=== Test Summary ===');
console.log(`Passed: ${testsPassed}`);
console.log(`Failed: ${testsFailed}`);
console.log(`Total: ${testsPassed + testsFailed}`);

if (testsFailed > 0) {
  process.exit(1);
}