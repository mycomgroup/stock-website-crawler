import { jest, describe, test, expect, beforeEach, afterEach } from '@jest/globals';
import fs from 'node:fs';
import path from 'node:path';

const testSessionFile = './tests/fixtures/test-session-data.json';

function loadSessionFromFile(filePath) {
  if (!fs.existsSync(filePath)) return null;
  try {
    return JSON.parse(fs.readFileSync(filePath, 'utf8'));
  } catch (e) {
    return null;
  }
}

function saveSessionToFile(filePath, cookies, url = '') {
  const sessionData = {
    cookies,
    timestamp: Date.now(),
    url
  };
  const dir = path.dirname(filePath);
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(filePath, JSON.stringify(sessionData, null, 2), 'utf8');
  return sessionData;
}

function isSessionValid(session) {
  if (!session || !session.cookies || session.cookies.length === 0) return false;
  
  const hasKeyCookie = session.cookies.some(c => 
    c.name.includes('v') || c.name.includes('SID') || c.name.includes('token')
  );
  
  if (!hasKeyCookie) return false;

  const SESSION_DURATION = 7 * 24 * 60 * 60 * 1000;
  const isExpired = Date.now() - (session.timestamp || 0) > SESSION_DURATION;
  
  return !isExpired;
}

describe('session-manager', () => {
  beforeEach(() => {
    if (!fs.existsSync('./tests/fixtures')) {
      fs.mkdirSync('./tests/fixtures', { recursive: true });
    }
    if (fs.existsSync(testSessionFile)) {
      fs.unlinkSync(testSessionFile);
    }
  });

  afterEach(() => {
    if (fs.existsSync(testSessionFile)) {
      fs.unlinkSync(testSessionFile);
    }
  });

  describe('loadSessionFromFile', () => {
    test('should load session from file', () => {
      const session = {
        cookies: [{ name: 'v', value: 'test123' }],
        timestamp: Date.now()
      };
      fs.writeFileSync(testSessionFile, JSON.stringify(session));
      
      const loaded = loadSessionFromFile(testSessionFile);
      expect(loaded.cookies).toHaveLength(1);
      expect(loaded.cookies[0].name).toBe('v');
    });

    test('should return null for non-existent file', () => {
      const loaded = loadSessionFromFile('./tests/fixtures/non-existent.json');
      expect(loaded).toBeNull();
    });

    test('should return null for invalid JSON', () => {
      fs.writeFileSync(testSessionFile, 'invalid json content');
      
      const loaded = loadSessionFromFile(testSessionFile);
      expect(loaded).toBeNull();
    });

    test('should return null for empty file', () => {
      fs.writeFileSync(testSessionFile, '');
      
      const loaded = loadSessionFromFile(testSessionFile);
      expect(loaded).toBeNull();
    });

    test('should handle malformed JSON', () => {
      fs.writeFileSync(testSessionFile, '{broken: json}');
      
      const loaded = loadSessionFromFile(testSessionFile);
      expect(loaded).toBeNull();
    });

    test('should load session with multiple cookies', () => {
      const session = {
        cookies: [
          { name: 'v', value: 'value1' },
          { name: 'SID', value: 'value2' },
          { name: 'token', value: 'value3' }
        ],
        timestamp: Date.now()
      };
      fs.writeFileSync(testSessionFile, JSON.stringify(session));
      
      const loaded = loadSessionFromFile(testSessionFile);
      expect(loaded.cookies).toHaveLength(3);
    });

    test('should preserve timestamp', () => {
      const timestamp = 1234567890;
      const session = {
        cookies: [],
        timestamp
      };
      fs.writeFileSync(testSessionFile, JSON.stringify(session));
      
      const loaded = loadSessionFromFile(testSessionFile);
      expect(loaded.timestamp).toBe(timestamp);
    });

    test('should preserve url', () => {
      const url = 'https://backtest.10jqka.com.cn/test';
      const session = {
        cookies: [],
        timestamp: Date.now(),
        url
      };
      fs.writeFileSync(testSessionFile, JSON.stringify(session));
      
      const loaded = loadSessionFromFile(testSessionFile);
      expect(loaded.url).toBe(url);
    });
  });

  describe('saveSessionToFile', () => {
    test('should save session with cookies', () => {
      const cookies = [
        { name: 'v', value: 'test123' },
        { name: 'SID', value: 'sid456' }
      ];
      
      const result = saveSessionToFile(testSessionFile, cookies);
      
      expect(result.cookies).toEqual(cookies);
      expect(result.timestamp).toBeDefined();
      expect(result.url).toBe('');
      expect(fs.existsSync(testSessionFile)).toBe(true);
    });

    test('should save session with url', () => {
      const cookies = [{ name: 'test', value: 'value' }];
      const url = 'https://example.com';
      
      const result = saveSessionToFile(testSessionFile, cookies, url);
      
      expect(result.url).toBe(url);
    });

    test('should add timestamp', () => {
      const cookies = [];
      const before = Date.now();
      
      const result = saveSessionToFile(testSessionFile, cookies);
      
      expect(result.timestamp).toBeGreaterThanOrEqual(before);
    });

    test('should create directory if not exists', () => {
      const newDir = './tests/fixtures/new-session-dir';
      const newFile = path.join(newDir, 'session.json');
      
      if (fs.existsSync(newDir)) {
        fs.rmSync(newDir, { recursive: true, force: true });
      }
      
      const cookies = [{ name: 'test', value: 'value' }];
      saveSessionToFile(newFile, cookies, 'https://example.com');
      
      expect(fs.existsSync(newDir)).toBe(true);
      expect(fs.existsSync(newFile)).toBe(true);
      
      fs.rmSync(newDir, { recursive: true, force: true });
    });

    test('should overwrite existing session', () => {
      const oldSession = {
        cookies: [{ name: 'old', value: 'old_value' }],
        timestamp: 1000
      };
      fs.writeFileSync(testSessionFile, JSON.stringify(oldSession));
      
      const newCookies = [{ name: 'new', value: 'new_value' }];
      const result = saveSessionToFile(testSessionFile, newCookies);
      
      expect(result.cookies[0].name).toBe('new');
      expect(result.timestamp).toBeGreaterThan(1000);
    });

    test('should handle empty cookies array', () => {
      const result = saveSessionToFile(testSessionFile, []);
      
      expect(result.cookies).toEqual([]);
      expect(result.timestamp).toBeDefined();
    });

    test('should handle complex cookie objects', () => {
      const cookies = [
        {
          name: 'complex',
          value: 'value',
          domain: '.10jqka.com.cn',
          path: '/',
          expires: 1234567890,
          secure: true,
          httpOnly: true
        }
      ];
      
      const result = saveSessionToFile(testSessionFile, cookies);
      
      expect(result.cookies[0]).toEqual(cookies[0]);
    });
  });

  describe('isSessionValid', () => {
    test('should return false for null session', () => {
      expect(isSessionValid(null)).toBe(false);
    });

    test('should return false for undefined session', () => {
      expect(isSessionValid(undefined)).toBe(false);
    });

    test('should return false for session without cookies', () => {
      expect(isSessionValid({ cookies: [] })).toBe(false);
    });

    test('should return false for session with empty cookies', () => {
      expect(isSessionValid({ cookies: [], timestamp: Date.now() })).toBe(false);
    });

    test('should return false for session without key cookies', () => {
      const session = {
        cookies: [{ name: 'unknown', value: 'value' }],
        timestamp: Date.now()
      };
      
      expect(isSessionValid(session)).toBe(false);
    });

    test('should return true for session with v cookie', () => {
      const session = {
        cookies: [{ name: 'v', value: 'test123' }],
        timestamp: Date.now()
      };
      
      expect(isSessionValid(session)).toBe(true);
    });

    test('should return true for session with SID cookie', () => {
      const session = {
        cookies: [{ name: 'SID', value: 'sid456' }],
        timestamp: Date.now()
      };
      
      expect(isSessionValid(session)).toBe(true);
    });

    test('should return true for session with token cookie', () => {
      const session = {
        cookies: [{ name: 'token', value: 'token789' }],
        timestamp: Date.now()
      };
      
      expect(isSessionValid(session)).toBe(true);
    });

    test('should return true for session with multiple cookies including key', () => {
      const session = {
        cookies: [
          { name: 'other', value: 'value1' },
          { name: 'v', value: 'value2' },
          { name: 'SID', value: 'value3' }
        ],
        timestamp: Date.now()
      };
      
      expect(isSessionValid(session)).toBe(true);
    });

    test('should return false for expired session', () => {
      const oldTimestamp = Date.now() - (8 * 24 * 60 * 60 * 1000);
      const session = {
        cookies: [{ name: 'v', value: 'test' }],
        timestamp: oldTimestamp
      };
      
      expect(isSessionValid(session)).toBe(false);
    });

    test('should return true for session within 7 days', () => {
      const recentTimestamp = Date.now() - (3 * 24 * 60 * 60 * 1000);
      const session = {
        cookies: [{ name: 'v', value: 'test' }],
        timestamp: recentTimestamp
      };
      
      expect(isSessionValid(session)).toBe(true);
    });

    test('should return true for fresh session', () => {
      const session = {
        cookies: [{ name: 'v', value: 'test' }],
        timestamp: Date.now()
      };
      
      expect(isSessionValid(session)).toBe(true);
    });

    test('should return false for session at exactly 7 days boundary', () => {
      const exactTimestamp = Date.now() - (7 * 24 * 60 * 60 * 1000 + 1);
      const session = {
        cookies: [{ name: 'v', value: 'test' }],
        timestamp: exactTimestamp
      };
      
      expect(isSessionValid(session)).toBe(false);
    });

    test('should return false for session with timestamp 0', () => {
      const session = {
        cookies: [{ name: 'v', value: 'test' }],
        timestamp: 0
      };
      
      expect(isSessionValid(session)).toBe(false);
    });

    test('should return false for session without timestamp', () => {
      const session = {
        cookies: [{ name: 'v', value: 'test' }]
      };
      
      expect(isSessionValid(session)).toBe(false);
    });

    test('should handle cookie name variations containing key substrings', () => {
      const validCookieNames = ['v', 'SID', 'SID_test', 'token', 'access_token', 'auth_token'];
      
      validCookieNames.forEach(cookieName => {
        const session = {
          cookies: [{ name: cookieName, value: 'test' }],
          timestamp: Date.now()
        };
        
        expect(isSessionValid(session)).toBe(true);
      });
    });
  });

  describe('integration', () => {
    test('should save and load session correctly', () => {
      const cookies = [
        { name: 'v', value: 'integration_test' },
        { name: 'SID', value: 'integration_sid' }
      ];
      const url = 'https://backtest.10jqka.com.cn';
      
      saveSessionToFile(testSessionFile, cookies, url);
      
      const loaded = loadSessionFromFile(testSessionFile);
      expect(loaded.cookies).toHaveLength(2);
      expect(loaded.url).toBe(url);
      expect(loaded.timestamp).toBeDefined();
    });

    test('should validate saved session', () => {
      const cookies = [{ name: 'v', value: 'test' }];
      
      saveSessionToFile(testSessionFile, cookies);
      
      const loaded = loadSessionFromFile(testSessionFile);
      expect(isSessionValid(loaded)).toBe(true);
    });

    test('should handle session lifecycle', () => {
      const cookies1 = [{ name: 'v', value: 'first' }];
      saveSessionToFile(testSessionFile, cookies1);
      
      const loaded1 = loadSessionFromFile(testSessionFile);
      expect(isSessionValid(loaded1)).toBe(true);
      
      const cookies2 = [{ name: 'SID', value: 'second' }];
      saveSessionToFile(testSessionFile, cookies2);
      
      const loaded2 = loadSessionFromFile(testSessionFile);
      expect(loaded2.cookies[0].name).toBe('SID');
    });
  });
});