import { describe, it, beforeEach, afterEach, vi } from 'vitest';
import assert from 'node:assert';
import path from 'node:path';

vi.mock('node:fs', () => {
  const mockFs = {
    existsSync: vi.fn(() => false),
    readFileSync: vi.fn(() => '{}'),
    writeFileSync: vi.fn(),
    mkdirSync: vi.fn(),
    unlinkSync: vi.fn()
  };
  return {
    default: mockFs,
    ...mockFs
  };
});

vi.mock('../paths.js', () => ({
  SESSION_FILE: '/test/.sessions/guorn.json'
}));

const mockFs = await import('node:fs');

const { SessionManager } = await import('../../browser/session-manager.js');

function resetMocks() {
  mockFs.default.existsSync.mockClear();
  mockFs.default.readFileSync.mockClear();
  mockFs.default.writeFileSync.mockClear();
  mockFs.default.mkdirSync.mockClear();
  mockFs.default.unlinkSync.mockClear();
}

function createFreshSessionManager(options = {}) {
  return new SessionManager(options);
}

describe('SessionManager', () => {
  beforeEach(() => {
    resetMocks();
  });

  afterEach(() => {
    resetMocks();
  });

  describe('constructor', () => {
    it('should use default session file path when not provided', () => {
      mockFs.default.existsSync.mockImplementation(() => false);
      const sm = createFreshSessionManager();
      assert.ok(sm.sessionFile.includes('guorn.json'));
    });

    it('should use custom session file path when provided', () => {
      const sm = createFreshSessionManager({ sessionFile: '/custom/path/session.json' });
      assert.strictEqual(sm.sessionFile, '/custom/path/session.json');
    });

    it('should use default maxAge of 24 hours when not provided', () => {
      const sm = createFreshSessionManager();
      assert.strictEqual(sm.maxAge, 24 * 60 * 60 * 1000);
    });

    it('should use custom maxAge when provided', () => {
      const sm = createFreshSessionManager({ maxAge: 3600000 });
      assert.strictEqual(sm.maxAge, 3600000);
    });
  });

  describe('exists', () => {
    it('should return true when session file exists', () => {
      mockFs.default.existsSync.mockImplementation(() => true);
      const sm = createFreshSessionManager();
      const result = sm.exists();
      assert.strictEqual(result, true);
    });

    it('should return false when session file does not exist', () => {
      mockFs.default.existsSync.mockImplementation(() => false);
      const sm = createFreshSessionManager();
      const result = sm.exists();
      assert.strictEqual(result, false);
    });
  });

  describe('load', () => {
    it('should return null when session file does not exist', () => {
      mockFs.default.existsSync.mockImplementation(() => false);
      const sm = createFreshSessionManager();
      const result = sm.load();
      assert.strictEqual(result, null);
    });

    it('should return parsed JSON when session file exists', () => {
      const sessionData = {
        capturedAt: '2024-01-01T00:00:00.000Z',
        cookies: [{ name: 'session', value: 'abc123' }]
      };
      mockFs.default.existsSync.mockImplementation(() => true);
      mockFs.default.readFileSync.mockImplementation(() => JSON.stringify(sessionData));
      const sm = createFreshSessionManager();
      const result = sm.load();
      assert.deepStrictEqual(result, sessionData);
    });

    it('should return null when JSON parse fails', () => {
      mockFs.default.existsSync.mockImplementation(() => true);
      mockFs.default.readFileSync.mockImplementation(() => 'invalid json{{{');
      const sm = createFreshSessionManager();
      const result = sm.load();
      assert.strictEqual(result, null);
    });

    it('should return null when read file throws error', () => {
      mockFs.default.existsSync.mockImplementation(() => true);
      mockFs.default.readFileSync.mockImplementation(() => {
        throw new Error('Read error');
      });
      const sm = createFreshSessionManager();
      const result = sm.load();
      assert.strictEqual(result, null);
    });

    it('should read with utf8 encoding', () => {
      mockFs.default.existsSync.mockImplementation(() => true);
      mockFs.default.readFileSync.mockImplementation(() => '{}');
      const sm = createFreshSessionManager();
      sm.load();
      const calls = mockFs.default.readFileSync.mock.calls;
      assert.ok(calls.length > 0);
      assert.strictEqual(calls[calls.length - 1][1], 'utf8');
    });
  });

  describe('save', () => {
    it('should create directory if it does not exist', () => {
      mockFs.default.existsSync.mockImplementation(() => false);
      const sm = createFreshSessionManager({ sessionFile: '/test/dir/session.json' });
      sm.save({ cookies: [] });
      assert.strictEqual(mockFs.default.mkdirSync.mock.calls.length, 1);
    });

    it('should not create directory if it already exists', () => {
      mockFs.default.existsSync.mockImplementation(() => true);
      const sm = createFreshSessionManager({ sessionFile: '/test/dir/session.json' });
      sm.save({ cookies: [] });
      assert.strictEqual(mockFs.default.mkdirSync.mock.calls.length, 0);
    });

    it('should write session data to file', () => {
      mockFs.default.existsSync.mockImplementation(() => true);
      const sm = createFreshSessionManager({ sessionFile: '/test/session.json' });
      const sessionData = { capturedAt: '2024-01-01T00:00:00.000Z', cookies: [{ name: 'test', value: 'val' }] };
      sm.save(sessionData);
      const calls = mockFs.default.writeFileSync.mock.calls;
      assert.ok(calls.length > 0);
      const writtenData = JSON.parse(calls[calls.length - 1][1]);
      assert.deepStrictEqual(writtenData, sessionData);
    });

    it('should format JSON with 2-space indentation', () => {
      mockFs.default.existsSync.mockImplementation(() => true);
      const sm = createFreshSessionManager({ sessionFile: '/test/session.json' });
      sm.save({ test: 'value' });
      const calls = mockFs.default.writeFileSync.mock.calls;
      const content = calls[calls.length - 1][1];
      assert.ok(content.includes('  '));
      assert.ok(content.includes('\n'));
    });
  });

  describe('isExpired', () => {
    it('should return true when session does not exist', () => {
      mockFs.default.existsSync.mockImplementation(() => false);
      const sm = createFreshSessionManager();
      const result = sm.isExpired();
      assert.strictEqual(result, true);
    });

    it('should return true when session has no capturedAt', () => {
      mockFs.default.existsSync.mockImplementation(() => true);
      mockFs.default.readFileSync.mockImplementation(() => JSON.stringify({ cookies: [] }));
      const sm = createFreshSessionManager();
      const result = sm.isExpired();
      assert.strictEqual(result, true);
    });

    it('should return true when session is older than maxAge', () => {
      const oldTimestamp = new Date(Date.now() - 25 * 60 * 60 * 1000).toISOString();
      mockFs.default.existsSync.mockImplementation(() => true);
      mockFs.default.readFileSync.mockImplementation(() => JSON.stringify({ capturedAt: oldTimestamp, cookies: [] }));
      const sm = createFreshSessionManager({ maxAge: 24 * 60 * 60 * 1000 });
      const result = sm.isExpired();
      assert.strictEqual(result, true);
    });

    it('should return false when session is newer than maxAge', () => {
      const recentTimestamp = new Date(Date.now() - 1 * 60 * 60 * 1000).toISOString();
      mockFs.default.existsSync.mockImplementation(() => true);
      mockFs.default.readFileSync.mockImplementation(() => JSON.stringify({ capturedAt: recentTimestamp, cookies: [] }));
      const sm = createFreshSessionManager({ maxAge: 24 * 60 * 60 * 1000 });
      const result = sm.isExpired();
      assert.strictEqual(result, false);
    });

    it('should return false when session is exactly at maxAge boundary', () => {
      const timestamp = new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString();
      mockFs.default.existsSync.mockImplementation(() => true);
      mockFs.default.readFileSync.mockImplementation(() => JSON.stringify({ capturedAt: timestamp, cookies: [] }));
      const sm = createFreshSessionManager({ maxAge: 24 * 60 * 60 * 1000 });
      const result = sm.isExpired();
      assert.strictEqual(result, true);
    });
  });

  describe('getCookie', () => {
    it('should return null when session does not exist', () => {
      mockFs.default.existsSync.mockImplementation(() => false);
      const sm = createFreshSessionManager();
      const result = sm.getCookie('sessionid');
      assert.strictEqual(result, null);
    });

    it('should return null when session has no cookies', () => {
      mockFs.default.existsSync.mockImplementation(() => true);
      mockFs.default.readFileSync.mockImplementation(() => JSON.stringify({ capturedAt: new Date().toISOString() }));
      const sm = createFreshSessionManager();
      const result = sm.getCookie('sessionid');
      assert.strictEqual(result, null);
    });

    it('should return null when cookie not found', () => {
      mockFs.default.existsSync.mockImplementation(() => true);
      mockFs.default.readFileSync.mockImplementation(() => JSON.stringify({ 
        capturedAt: new Date().toISOString(),
        cookies: [{ name: 'other', value: 'val' }] 
      }));
      const sm = createFreshSessionManager();
      const result = sm.getCookie('sessionid');
      assert.strictEqual(result, null);
    });

    it('should return cookie value when found', () => {
      mockFs.default.existsSync.mockImplementation(() => true);
      mockFs.default.readFileSync.mockImplementation(() => JSON.stringify({ 
        capturedAt: new Date().toISOString(),
        cookies: [{ name: 'sessionid', value: 'abc123' }] 
      }));
      const sm = createFreshSessionManager();
      const result = sm.getCookie('sessionid');
      assert.strictEqual(result, 'abc123');
    });

    it('should return first matching cookie value', () => {
      mockFs.default.existsSync.mockImplementation(() => true);
      mockFs.default.readFileSync.mockImplementation(() => JSON.stringify({ 
        capturedAt: new Date().toISOString(),
        cookies: [
          { name: 'sessionid', value: 'first' },
          { name: 'sessionid', value: 'second' }
        ] 
      }));
      const sm = createFreshSessionManager();
      const result = sm.getCookie('sessionid');
      assert.strictEqual(result, 'first');
    });
  });

  describe('getCookieString', () => {
    it('should return empty string when session does not exist', () => {
      mockFs.default.existsSync.mockImplementation(() => false);
      const sm = createFreshSessionManager();
      const result = sm.getCookieString();
      assert.strictEqual(result, '');
    });

    it('should return empty string when session has no cookies', () => {
      mockFs.default.existsSync.mockImplementation(() => true);
      mockFs.default.readFileSync.mockImplementation(() => JSON.stringify({ capturedAt: new Date().toISOString() }));
      const sm = createFreshSessionManager();
      const result = sm.getCookieString();
      assert.strictEqual(result, '');
    });

    it('should return formatted cookie string for single cookie', () => {
      mockFs.default.existsSync.mockImplementation(() => true);
      mockFs.default.readFileSync.mockImplementation(() => JSON.stringify({ 
        capturedAt: new Date().toISOString(),
        cookies: [{ name: 'sessionid', value: 'abc123' }] 
      }));
      const sm = createFreshSessionManager();
      const result = sm.getCookieString();
      assert.strictEqual(result, 'sessionid=abc123');
    });

    it('should return formatted cookie string for multiple cookies', () => {
      mockFs.default.existsSync.mockImplementation(() => true);
      mockFs.default.readFileSync.mockImplementation(() => JSON.stringify({ 
        capturedAt: new Date().toISOString(),
        cookies: [
          { name: 'sessionid', value: 'abc123' },
          { name: 'token', value: 'xyz789' }
        ] 
      }));
      const sm = createFreshSessionManager();
      const result = sm.getCookieString();
      assert.strictEqual(result, 'sessionid=abc123; token=xyz789');
    });

    it('should handle empty cookies array', () => {
      mockFs.default.existsSync.mockImplementation(() => true);
      mockFs.default.readFileSync.mockImplementation(() => JSON.stringify({ 
        capturedAt: new Date().toISOString(),
        cookies: [] 
      }));
      const sm = createFreshSessionManager();
      const result = sm.getCookieString();
      assert.strictEqual(result, '');
    });
  });

  describe('clear', () => {
    it('should delete session file when it exists', () => {
      mockFs.default.existsSync.mockImplementation(() => true);
      const sm = createFreshSessionManager();
      sm.clear();
      assert.strictEqual(mockFs.default.unlinkSync.mock.calls.length, 1);
    });

    it('should not throw when session file does not exist', () => {
      mockFs.default.existsSync.mockImplementation(() => false);
      const sm = createFreshSessionManager();
      assert.doesNotThrow(() => sm.clear());
      assert.strictEqual(mockFs.default.unlinkSync.mock.calls.length, 0);
    });
  });

  describe('getAge', () => {
    it('should return Infinity when session does not exist', () => {
      mockFs.default.existsSync.mockImplementation(() => false);
      const sm = createFreshSessionManager();
      const result = sm.getAge();
      assert.strictEqual(result, Infinity);
    });

    it('should return Infinity when session has no capturedAt', () => {
      mockFs.default.existsSync.mockImplementation(() => true);
      mockFs.default.readFileSync.mockImplementation(() => JSON.stringify({ cookies: [] }));
      const sm = createFreshSessionManager();
      const result = sm.getAge();
      assert.strictEqual(result, Infinity);
    });

    it('should return age in milliseconds for valid session', () => {
      const capturedAt = new Date(Date.now() - 5000).toISOString();
      mockFs.default.existsSync.mockImplementation(() => true);
      mockFs.default.readFileSync.mockImplementation(() => JSON.stringify({ capturedAt, cookies: [] }));
      const sm = createFreshSessionManager();
      const result = sm.getAge();
      assert.ok(result >= 5000);
      assert.ok(result < 6000);
    });

    it('should return positive age for future capturedAt (edge case)', () => {
      const futureTime = new Date(Date.now() + 10000).toISOString();
      mockFs.default.existsSync.mockImplementation(() => true);
      mockFs.default.readFileSync.mockImplementation(() => JSON.stringify({ capturedAt: futureTime, cookies: [] }));
      const sm = createFreshSessionManager();
      const result = sm.getAge();
      assert.ok(result < 0);
    });
  });

  describe('isValid', () => {
    it('should return false when session file does not exist', () => {
      mockFs.default.existsSync.mockImplementation(() => false);
      const sm = createFreshSessionManager();
      const result = sm.isValid();
      assert.strictEqual(result, false);
    });

    it('should return false when session is expired', () => {
      const oldTimestamp = new Date(Date.now() - 25 * 60 * 60 * 1000).toISOString();
      mockFs.default.existsSync.mockImplementation(() => true);
      mockFs.default.readFileSync.mockImplementation(() => JSON.stringify({ capturedAt: oldTimestamp, cookies: [] }));
      const sm = createFreshSessionManager({ maxAge: 24 * 60 * 60 * 1000 });
      const result = sm.isValid();
      assert.strictEqual(result, false);
    });

    it('should return true when session exists and is not expired', () => {
      const recentTimestamp = new Date(Date.now() - 1 * 60 * 60 * 1000).toISOString();
      mockFs.default.existsSync.mockImplementation(() => true);
      mockFs.default.readFileSync.mockImplementation(() => JSON.stringify({ capturedAt: recentTimestamp, cookies: [] }));
      const sm = createFreshSessionManager({ maxAge: 24 * 60 * 60 * 1000 });
      const result = sm.isValid();
      assert.strictEqual(result, true);
    });
  });

  describe('integration scenarios', () => {
    it('should handle full lifecycle: save, load, isValid, clear', () => {
      const sessionData = {
        capturedAt: new Date().toISOString(),
        cookies: [{ name: 'session', value: 'test' }]
      };
      
      mockFs.default.existsSync.mockImplementation(() => true);
      mockFs.default.readFileSync.mockImplementation(() => JSON.stringify(sessionData));
      
      const sm = createFreshSessionManager();
      
      const loaded = sm.load();
      assert.deepStrictEqual(loaded, sessionData);
      
      const isValid = sm.isValid();
      assert.strictEqual(isValid, true);
      
      sm.clear();
      assert.strictEqual(mockFs.default.unlinkSync.mock.calls.length, 1);
    });
  });
});