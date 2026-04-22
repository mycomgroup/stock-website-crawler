import { describe, it, beforeEach, mock } from 'node:test';
import assert from 'node:assert';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { basename, dirname, join, resolve } from 'node:path';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const PROFILE_DIR_PATTERNS = [
  /^Default$/,
  /^Profile \d+$/,
  /^Guest Profile$/,
  /^System Profile$/
];

function stripWrappingQuotes(value) {
  return value.replace(/^['"`""]+|['"`""]+$/g, '');
}

function expandHome(value) {
  if (!value.startsWith('~/')) {
    return value;
  }
  const home = process.env.HOME;
  return home ? join(home, value.slice(2)) : value;
}

function looksLikeProfileDir(pathname) {
  const base = basename(pathname);
  if (PROFILE_DIR_PATTERNS.some((pattern) => pattern.test(base))) {
    return true;
  }
  return false;
}

function looksLikeUserDataDir(pathname) {
  return pathname.includes('Local State');
}

describe('Chrome Profile - utility functions', () => {
  describe('stripWrappingQuotes', () => {
    it('should strip double quotes', () => {
      const result = stripWrappingQuotes('"test path"');
      assert.strictEqual(result, 'test path');
    });

    it('should strip single quotes', () => {
      const result = stripWrappingQuotes("'test path'");
      assert.strictEqual(result, 'test path');
    });

    it('should not modify unquoted strings', () => {
      const result = stripWrappingQuotes('test path');
      assert.strictEqual(result, 'test path');
    });

    it('should handle empty string', () => {
      const result = stripWrappingQuotes('');
      assert.strictEqual(result, '');
    });

    it('should handle nested quotes', () => {
      const result = stripWrappingQuotes('"\'test\'"');
      assert.strictEqual(result, "'test'");
    });
  });

  describe('expandHome', () => {
    it('should expand ~/ to home directory', () => {
      process.env.HOME = '/home/testuser';
      const result = expandHome '~/test');
      assert.strictEqual(result, '/home/testuser/test');
    });

    it('should not modify non-home paths', () => {
      const result = expandHome('/absolute/path');
      assert.strictEqual(result, '/absolute/path');
    });

    it('should handle missing HOME env', () => {
      delete process.env.HOME;
      const result = expandHome '~/test');
      assert.strictEqual(result, '~/test');
    });

    it('should handle relative paths without ~/', () => {
      const result = expandHome('relative/path');
      assert.strictEqual(result, 'relative/path');
    });
  });

  describe('PROFILE_DIR_PATTERNS', () => {
    it('should match Default', () => {
      assert.ok(PROFILE_DIR_PATTERNS.some(p => p.test('Default')));
    });

    it('should match Profile N', () => {
      assert.ok(PROFILE_DIR_PATTERNS.some(p => p.test('Profile 1')));
      assert.ok(PROFILE_DIR_PATTERNS.some(p => p.test('Profile 5')));
      assert.ok(PROFILE_DIR_PATTERNS.some(p => p.test('Profile 100')));
    });

    it('should match Guest Profile', () => {
      assert.ok(PROFILE_DIR_PATTERNS.some(p => p.test('Guest Profile')));
    });

    it('should match System Profile', () => {
      assert.ok(PROFILE_DIR_PATTERNS.some(p => p.test('System Profile')));
    });

    it('should not match random names', () => {
      assert.strictEqual(PROFILE_DIR_PATTERNS.some(p => p.test('Random')), false);
      assert.strictEqual(PROFILE_DIR_PATTERNS.some(p => p.test('Custom')), false);
    });
  });

  describe('looksLikeProfileDir', () => {
    it('should return true for Default', () => {
      assert.strictEqual(looksLikeProfileDir('/test/Default'), true);
    });

    it('should return true for Profile N', () => {
      assert.strictEqual(looksLikeProfileDir('/test/Profile 1'), true);
    });

    it('should return false for random paths', () => {
      assert.strictEqual(looksLikeProfileDir('/test/random'), false);
    });

    it('should return true for Guest Profile', () => {
      assert.strictEqual(looksLikeProfileDir('/test/Guest Profile'), true);
    });
  });

  describe('looksLikeUserDataDir', () => {
    it('should return true when contains Local State', () => {
      assert.strictEqual(looksLikeUserDataDir('/test/Local State'), true);
    });

    it('should return false otherwise', () => {
      assert.strictEqual(looksLikeUserDataDir('/test/Default'), false);
    });
  });

  describe('resolveChromeProfile', () => {
    it('should return null for null input', async () => {
      const { resolveChromeProfile } = await import('../browser/chrome-profile.js');
      assert.strictEqual(resolveChromeProfile(null), null);
    });

    it('should return null for empty string', async () => {
      const { resolveChromeProfile } = await import('../browser/chrome-profile.js?cachebuster=' + Date.now());
      assert.strictEqual(resolveChromeProfile(''), null);
    });

    it('should return null for undefined', async () => {
      const { resolveChromeProfile } = await import('../browser/chrome-profile.js?cachebuster=' + Date.now());
      assert.strictEqual(resolveChromeProfile(undefined), null);
    });
  });

  describe('formatResolvedChromeProfile', () => {
    it('should return 未指定 for null', async () => {
      const { formatResolvedChromeProfile } = await import('../browser/chrome-profile.js?cachebuster=' + Date.now());
      assert.strictEqual(formatResolvedChromeProfile(null), '未指定');
    });

    it('should return userDataDir when no profileDirectory', async () => {
      const { formatResolvedChromeProfile } = await import('../browser/chrome-profile.js?cachebuster=' + Date.now());
      const result = formatResolvedChromeProfile({ userDataDir: '/test/chrome' });
      assert.strictEqual(result, '/test/chrome');
    });

    it('should return formatted string with profile', async () => {
      const { formatResolvedChromeProfile } = await import('../browser/chrome-profile.js?cachebuster=' + Date.now());
      const result = formatResolvedChromeProfile({
        userDataDir: '/test/chrome',
        profileDirectory: 'Profile 1'
      });
      assert.ok(result.includes('/test/chrome'));
      assert.ok(result.includes('Profile 1'));
    });
  });

  describe('enhanceChromeProfileError', () => {
    it('should enhance in use error', async () => {
      const { enhanceChromeProfileError } = await import('../browser/chrome-profile.js?cachebuster=' + Date.now());
      
      const originalError = new Error('user data directory is already in use');
      const profileConfig = { userDataDir: '/test', profileDirectory: 'Profile 1' };
      
      const enhanced = enhanceChromeProfileError(originalError, profileConfig);
      
      assert.ok(enhanced.message.includes('正在被其他 Chrome 进程占用'));
    });

    it('should enhance ProcessSingleton error', async () => {
      const { enhanceChromeProfileError } = await import('../browser/chrome-profile.js?cachebuster=' + Date.now());
      
      const originalError = new Error('ProcessSingleton error');
      const profileConfig = { userDataDir: '/test' };
      
      const enhanced = enhanceChromeProfileError(originalError, profileConfig);
      
      assert.ok(enhanced.message.includes('正在被其他 Chrome 进程占用'));
    });

    it('should enhance SingletonLock error', async () => {
      const { enhanceChromeProfileError } = await import('../browser/chrome-profile.js?cachebuster=' + Date.now());
      
      const originalError = new Error('SingletonLock failed');
      const profileConfig = { userDataDir: '/test' };
      
      const enhanced = enhanceChromeProfileError(originalError, profileConfig);
      
      assert.ok(enhanced.message.includes('正在被其他 Chrome 进程占用'));
    });

    it('should return original error for other errors', async () => {
      const { enhanceChromeProfileError } = await import('../browser/chrome-profile.js?cachebuster=' + Date.now());
      
      const originalError = new Error('Random error');
      const profileConfig = { userDataDir: '/test' };
      
      const enhanced = enhanceChromeProfileError(originalError, profileConfig);
      
      assert.strictEqual(enhanced.message, 'Random error');
    });
  });
});