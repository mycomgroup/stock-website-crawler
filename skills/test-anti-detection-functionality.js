#!/usr/bin/env node

/**
 * 详细测试 anti-detection.js 的功能
 */

import { AntiDetection, SessionManager, RateLimiter } from './bigquant_strategy/lib/anti-detection.js';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import { mkdtemp, rm } from 'fs/promises';
import { tmpdir } from 'os';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

console.log('🧪 Detailed Functionality Tests\n');
console.log('━'.repeat(60));
console.log();

let passCount = 0;
let failCount = 0;

async function test(name, fn) {
  process.stdout.write(`${name}... `);
  try {
    await fn();
    console.log('✅ PASS');
    passCount++;
    return true;
  } catch (error) {
    console.log(`❌ FAIL: ${error.message}`);
    failCount++;
    return false;
  }
}

// 测试 AntiDetection 类
console.log('📦 Testing AntiDetection class:\n');

await test('getRandomUserAgent()', () => {
  const ua = AntiDetection.getRandomUserAgent();
  if (!ua || typeof ua !== 'string') {
    throw new Error('Invalid user agent');
  }
  if (!ua.includes('Mozilla')) {
    throw new Error('User agent does not look realistic');
  }
});

await test('createRealisticHeaders()', () => {
  const headers = AntiDetection.createRealisticHeaders();
  if (!headers || typeof headers !== 'object') {
    throw new Error('Invalid headers');
  }
  if (!headers['User-Agent']) {
    throw new Error('Missing User-Agent header');
  }
  if (!headers['Accept-Language']) {
    throw new Error('Missing Accept-Language header');
  }
  if (!headers['Sec-Ch-Ua']) {
    throw new Error('Missing Sec-Ch-Ua header');
  }
});

await test('createRealisticHeaders() with custom headers', () => {
  const headers = AntiDetection.createRealisticHeaders({
    'Cookie': 'test=123',
    'Referer': 'https://example.com'
  });
  if (headers['Cookie'] !== 'test=123') {
    throw new Error('Custom Cookie not preserved');
  }
  if (headers['Referer'] !== 'https://example.com') {
    throw new Error('Custom Referer not preserved');
  }
  if (!headers['User-Agent']) {
    throw new Error('Default headers not added');
  }
});

await test('randomDelay()', async () => {
  const start = Date.now();
  await AntiDetection.randomDelay(100, 200);
  const elapsed = Date.now() - start;
  if (elapsed < 100 || elapsed > 300) {
    throw new Error(`Delay ${elapsed}ms not in expected range 100-200ms`);
  }
});

await test('fetchWithRetry() - success', async () => {
  let callCount = 0;
  const mockFetch = async () => {
    callCount++;
    return { ok: true, json: async () => ({ success: true }) };
  };
  
  const result = await AntiDetection.fetchWithRetry(mockFetch, {
    maxRetries: 3,
    retryDelay: 10
  });
  
  if (!result.ok) {
    throw new Error('Request failed');
  }
  if (callCount !== 1) {
    throw new Error(`Expected 1 call, got ${callCount}`);
  }
});

await test('fetchWithRetry() - retry on failure', async () => {
  let callCount = 0;
  const mockFetch = async () => {
    callCount++;
    if (callCount < 3) {
      throw new Error('Network error');
    }
    return { ok: true, json: async () => ({ success: true }) };
  };
  
  const result = await AntiDetection.fetchWithRetry(mockFetch, {
    maxRetries: 3,
    retryDelay: 10,
    backoff: false
  });
  
  if (!result.ok) {
    throw new Error('Request failed after retries');
  }
  if (callCount !== 3) {
    throw new Error(`Expected 3 calls, got ${callCount}`);
  }
});

console.log();
console.log('📦 Testing SessionManager class:\n');

await test('SessionManager - save and load', async () => {
  const tmpDir = await mkdtemp(join(tmpdir(), 'test-session-'));
  const sessionFile = join(tmpDir, 'session.json');
  
  try {
    const manager = new SessionManager(sessionFile);
    
    const testSession = {
      cookies: [
        { name: 'session', value: 'abc123' },
        { name: 'token', value: 'xyz789' }
      ],
      userAgent: 'Test User Agent'
    };
    
    await manager.save(testSession);
    const loaded = await manager.load();
    
    if (!loaded) {
      throw new Error('Failed to load session');
    }
    if (loaded.cookies.length !== 2) {
      throw new Error('Cookies not preserved');
    }
    if (loaded.userAgent !== 'Test User Agent') {
      throw new Error('User agent not preserved');
    }
    if (!loaded.capturedAt) {
      throw new Error('capturedAt not added');
    }
  } finally {
    await rm(tmpDir, { recursive: true, force: true });
  }
});

await test('SessionManager - isValid() with fresh session', async () => {
  const tmpDir = await mkdtemp(join(tmpdir(), 'test-session-'));
  const sessionFile = join(tmpDir, 'session.json');
  
  try {
    const manager = new SessionManager(sessionFile, {
      maxAge: 10000 // 10 seconds
    });
    
    await manager.save({ cookies: [] });
    const isValid = await manager.isValid();
    
    if (!isValid) {
      throw new Error('Fresh session should be valid');
    }
  } finally {
    await rm(tmpDir, { recursive: true, force: true });
  }
});

await test('SessionManager - isValid() with expired session', async () => {
  const tmpDir = await mkdtemp(join(tmpdir(), 'test-session-'));
  const sessionFile = join(tmpDir, 'session.json');
  
  try {
    const manager = new SessionManager(sessionFile, {
      maxAge: 100 // 100ms
    });
    
    await manager.save({ cookies: [] });
    
    // Wait for expiration
    await new Promise(resolve => setTimeout(resolve, 150));
    
    const isValid = await manager.isValid();
    
    if (isValid) {
      throw new Error('Expired session should be invalid');
    }
  } finally {
    await rm(tmpDir, { recursive: true, force: true });
  }
});

await test('SessionManager - clear()', async () => {
  const tmpDir = await mkdtemp(join(tmpdir(), 'test-session-'));
  const sessionFile = join(tmpDir, 'session.json');
  
  try {
    const manager = new SessionManager(sessionFile);
    
    await manager.save({ cookies: [] });
    await manager.clear();
    
    const loaded = await manager.load();
    if (loaded !== null) {
      throw new Error('Session should be null after clear');
    }
  } finally {
    await rm(tmpDir, { recursive: true, force: true });
  }
});

console.log();
console.log('📦 Testing RateLimiter class:\n');

await test('RateLimiter - basic delay', async () => {
  const limiter = new RateLimiter({
    minDelay: 100,
    maxDelay: 200
  });
  
  // First call should be immediate
  const start1 = Date.now();
  await limiter.wait();
  const elapsed1 = Date.now() - start1;
  
  if (elapsed1 > 50) {
    throw new Error(`First delay ${elapsed1}ms should be immediate`);
  }
  
  // Second call should respect the delay
  const start2 = Date.now();
  await limiter.wait();
  const elapsed2 = Date.now() - start2;
  
  if (elapsed2 < 100 || elapsed2 > 300) {
    throw new Error(`Second delay ${elapsed2}ms not in expected range 100-200ms`);
  }
});

await test('RateLimiter - multiple calls', async () => {
  const limiter = new RateLimiter({
    minDelay: 50,
    maxDelay: 100
  });
  
  const delays = [];
  
  for (let i = 0; i < 3; i++) {
    const start = Date.now();
    await limiter.wait();
    const elapsed = Date.now() - start;
    delays.push(elapsed);
  }
  
  // First call should be immediate or very short
  if (delays[0] > 150) {
    throw new Error(`First delay ${delays[0]}ms too long`);
  }
  
  // Subsequent calls should respect the delay
  for (let i = 1; i < delays.length; i++) {
    if (delays[i] < 50 || delays[i] > 200) {
      throw new Error(`Delay ${delays[i]}ms not in expected range`);
    }
  }
});

console.log();
console.log('━'.repeat(60));
console.log();
console.log('📊 Test Summary:');
console.log(`   Total:  ${passCount + failCount}`);
console.log(`   ✅ Pass:  ${passCount}`);
console.log(`   ❌ Fail:  ${failCount}`);
console.log();

if (failCount === 0) {
  console.log('🎉 All functionality tests passed!');
  console.log();
  console.log('✅ AntiDetection class works correctly');
  console.log('✅ SessionManager class works correctly');
  console.log('✅ RateLimiter class works correctly');
  console.log('✅ All methods produce expected results');
  console.log('✅ Error handling works as expected');
  process.exit(0);
} else {
  console.log('⚠️  Some tests failed. Please check the errors above.');
  process.exit(1);
}
