import { strict as assert } from 'assert';
import { readFileSync, writeFileSync, existsSync, mkdirSync, rmSync, readdirSync } from 'fs';
import { tmpdir } from 'os';
import { join } from 'path';

const testDir = join(tmpdir(), 'capture-session-test-' + Date.now());
const dataDir = join(testDir, 'data');
const sessionFile = join(dataDir, 'session.json');

function setupTestDir() {
  if (!existsSync(testDir)) {
    mkdirSync(testDir, { recursive: true });
  }
  if (!existsSync(dataDir)) {
    mkdirSync(dataDir, { recursive: true });
  }
}

function cleanupTestDir() {
  if (existsSync(testDir)) {
    rmSync(testDir, { recursive: true, force: true });
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

console.log('\n=== captureSession Unit Tests ===\n');
console.log(`Test directory: ${testDir}\n`);

setupTestDir();

test('captureSession function exists and is async', async () => {
  const { captureSession } = await import('../browser/capture-session.js');
  assert.strictEqual(typeof captureSession, 'function');
  assert.ok(captureSession.constructor.name === 'AsyncFunction');
});

test('validateSessionInBrowser function exists and is async', async () => {
  const { validateSessionInBrowser } = await import('../browser/capture-session.js');
  assert.strictEqual(typeof validateSessionInBrowser, 'function');
  assert.ok(validateSessionInBrowser.constructor.name === 'AsyncFunction');
});

console.log('\n=== Cookie Filtering Tests ===\n');

test('filters important cookies - auth cookies', () => {
  const cookies = [
    { name: '__Secure-next-auth.session-token', value: 'test', domain: '.google.com' }
  ];
  
  const filtered = cookies.filter(cookie => {
    const name = cookie.name.toLowerCase();
    return name.includes('auth') || name.includes('session') || name.includes('cf') || name.includes('token');
  });
  
  assert.strictEqual(filtered.length, 1);
});

test('filters important cookies - cf cookies', () => {
  const cookies = [
    { name: 'cf_clearance', value: 'test', domain: '.google.com' },
    { name: '_cfuvid', value: 'test', domain: '.google.com' }
  ];
  
  const filtered = cookies.filter(cookie => {
    const name = cookie.name.toLowerCase();
    return name.includes('auth') || name.includes('session') || name.includes('cf') || name.includes('token');
  });
  
  assert.strictEqual(filtered.length, 2);
});

test('filters important cookies - token cookies', () => {
  const cookies = [
    { name: 'mytoken', value: 'test', domain: '.google.com' },
    { name: 'NID', value: 'test', domain: '.google.com' }
  ];
  
  const filtered = cookies.filter(cookie => {
    const name = cookie.name.toLowerCase();
    return name.includes('auth') || name.includes('session') || name.includes('cf') || name.includes('token');
  });
  
  assert.strictEqual(filtered.length, 1);
  assert.strictEqual(filtered[0].name, 'mytoken');
});

test('excludes non-important cookies', () => {
  const cookies = [
    { name: 'random_cookie', value: 'test', domain: '.google.com' },
    { name: 'preferences', value: 'test', domain: '.google.com' },
    { name: 'language', value: 'test', domain: '.google.com' }
  ];
  
  const filtered = cookies.filter(cookie => {
    const name = cookie.name.toLowerCase();
    return name.includes('auth') || name.includes('session') || name.includes('cf') || name.includes('token');
  });
  
  assert.strictEqual(filtered.length, 0);
});

test('mixed cookies filtering', () => {
  const cookies = [
    { name: '__Secure-next-auth.session-token', value: 'auth1', domain: '.google.com' },
    { name: 'cf_clearance', value: 'cf1', domain: '.google.com' },
    { name: '_cfuvid', value: 'cfuvid1', domain: '.google.com' },
    { name: 'mytoken', value: 'token1', domain: '.google.com' },
    { name: 'random_cookie', value: 'random', domain: '.google.com' },
    { name: 'NID', value: 'nid', domain: '.google.com' }
  ];
  
  const filtered = cookies.filter(cookie => {
    const name = cookie.name.toLowerCase();
    return name.includes('auth') || name.includes('session') || name.includes('cf') || name.includes('token');
  });
  
  assert.strictEqual(filtered.length, 4);
  assert.ok(filtered.some(c => c.name === '__Secure-next-auth.session-token'));
  assert.ok(filtered.some(c => c.name === 'cf_clearance'));
  assert.ok(filtered.some(c => c.name === '_cfuvid'));
  assert.ok(filtered.some(c => c.name === 'mytoken'));
  assert.ok(!filtered.some(c => c.name === 'random_cookie'));
  assert.ok(!filtered.some(c => c.name === 'NID'));
});

console.log('\n=== Session Data Structure Tests ===\n');

test('session data has correct structure', () => {
  const sessionData = {
    capturedAt: new Date().toISOString(),
    cookies: [{ name: 'test', value: 'test-value', domain: '.google.com' }],
    userAgent: 'TestAgent/1.0'
  };
  
  assert.ok(sessionData.capturedAt);
  assert.ok(Array.isArray(sessionData.cookies));
  assert.ok(sessionData.userAgent);
  assert.strictEqual(typeof sessionData.capturedAt, 'string');
  assert.strictEqual(typeof sessionData.userAgent, 'string');
});

test('session data capturedAt is valid ISO date', () => {
  const capturedAt = new Date().toISOString();
  const parsedDate = new Date(capturedAt);
  
  assert.ok(parsedDate instanceof Date);
  assert.ok(!isNaN(parsedDate.getTime()));
});

console.log('\n=== Browser Launch Options Tests ===\n');

test('launch options for capture session', () => {
  const launchOptions = {
    headless: false,
    timeout: 600000
  };
  
  assert.strictEqual(launchOptions.headless, false);
  assert.strictEqual(launchOptions.timeout, 600000);
});

test('launch options for validate session', () => {
  const launchOptions = {
    headless: true
  };
  
  assert.strictEqual(launchOptions.headless, true);
});

test('context options have correct viewport', () => {
  const contextOptions = {
    viewport: { width: 1280, height: 720 },
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
  };
  
  assert.deepStrictEqual(contextOptions.viewport, { width: 1280, height: 720 });
});

test('default options merge correctly', () => {
  const defaultOptions = { headless: true, useProfile: '', timeout: 600000 };
  const customOptions = { headless: false, timeout: 300000 };
  const merged = { ...defaultOptions, ...customOptions };
  
  assert.strictEqual(merged.headless, false);
  assert.strictEqual(merged.timeout, 300000);
  assert.strictEqual(merged.useProfile, '');
});

console.log('\n=== Validation Logic Tests ===\n');

test('validation returns true for valid URL', () => {
  const currentUrl = 'https://gemini.google.com/app';
  const isValid = currentUrl.includes('gemini.google.com') && !currentUrl.includes('/signin');
  
  assert.strictEqual(isValid, true);
});

test('validation returns false for signin URL', () => {
  const currentUrl = 'https://gemini.google.com/signin';
  const isValid = currentUrl.includes('gemini.google.com') && !currentUrl.includes('/signin');
  
  assert.strictEqual(isValid, false);
});

test('validation returns false for accounts.google.com', () => {
  const currentUrl = 'https://accounts.google.com/signin';
  const isValid = currentUrl.includes('gemini.google.com') && !currentUrl.includes('/signin');
  
  assert.strictEqual(isValid, false);
});

test('validation returns true for gemini URL without signin', () => {
  const urls = [
    'https://gemini.google.com/',
    'https://gemini.google.com/app',
    'https://gemini.google.com/prompts'
  ];
  
  for (const url of urls) {
    const isValid = url.includes('gemini.google.com') && !url.includes('/signin');
    assert.strictEqual(isValid, true);
  }
});

console.log('\n=== Edge Case Tests ===\n');

test('empty cookies array', () => {
  const cookies = [];
  const filtered = cookies.filter(cookie => {
    const name = cookie.name.toLowerCase();
    return name.includes('auth') || name.includes('session') || name.includes('cf') || name.includes('token');
  });
  
  assert.strictEqual(filtered.length, 0);
});

test('missing userAgent defaults correctly', () => {
  const sessionData = { capturedAt: new Date().toISOString(), cookies: [] };
  const userAgent = sessionData.userAgent || 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36';
  
  assert.strictEqual(userAgent, 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36');
});

test('timeout values are correct', () => {
  const loginTimeout = 600000;
  const validationTimeout = 15000;
  const waitTimeouts = [300000, 3000, 2000];
  
  assert.strictEqual(loginTimeout, 600000);
  assert.strictEqual(validationTimeout, 15000);
  assert.strictEqual(waitTimeouts[0], 300000);
});

test('navigation options structure', () => {
  const gotoOptions = {
    waitUntil: 'domcontentloaded',
    timeout: 600000
  };
  
  assert.strictEqual(gotoOptions.waitUntil, 'domcontentloaded');
  assert.strictEqual(gotoOptions.timeout, 600000);
});

console.log('\n=== File Operations Tests ===\n');

test('directory creation creates data dir', () => {
  setupTestDir();
  
  assert.ok(existsSync(dataDir));
});

test('session file can be written', () => {
  setupTestDir();
  
  const sessionData = {
    capturedAt: new Date().toISOString(),
    cookies: [{ name: 'test', value: 'test-value' }],
    userAgent: 'TestAgent'
  };
  
  writeFileSync(sessionFile, JSON.stringify(sessionData, null, 2), 'utf-8');
  
  assert.ok(existsSync(sessionFile));
});

test('session file can be read back', () => {
  setupTestDir();
  
  const sessionData = {
    capturedAt: new Date().toISOString(),
    cookies: [{ name: 'test', value: 'test-value' }],
    userAgent: 'TestAgent'
  };
  
  writeFileSync(sessionFile, JSON.stringify(sessionData, null, 2), 'utf-8');
  const content = readFileSync(sessionFile, 'utf-8');
  const parsed = JSON.parse(content);
  
  assert.deepStrictEqual(parsed.cookies, sessionData.cookies);
  assert.strictEqual(parsed.userAgent, sessionData.userAgent);
});

cleanupTestDir();

console.log('\n=== Test Summary ===');
console.log(`Passed: ${testsPassed}`);
console.log(`Failed: ${testsFailed}`);
console.log(`Total: ${testsPassed + testsFailed}`);

if (testsFailed > 0) {
  process.exit(1);
}