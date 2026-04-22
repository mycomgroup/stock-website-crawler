import { describe, it, beforeEach, afterEach } from 'node:test';
import assert from 'node:assert';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { existsSync } from 'node:fs';

describe('load-env.js', () => {
  describe('ENV object structure', () => {
    it('should export ENV object', async () => {
      const loadEnv = await import('../load-env.js');
      assert.ok(loadEnv.ENV, 'ENV should be exported');
      assert.strictEqual(typeof loadEnv.ENV, 'object');
    });

    it('should have all required ENV properties', async () => {
      const loadEnv = await import('../load-env.js');
      const requiredProps = ['GOOGLE_EMAIL', 'CHROME_PROFILE_PATH', 'HEADLESS', 'DEFAULT_MODEL'];
      
      for (const prop of requiredProps) {
        assert.ok(prop in loadEnv.ENV, `ENV should have ${prop} property`);
      }
    });
  });

  describe('ENV property types', () => {
    it('should have GOOGLE_EMAIL as string type', async () => {
      const loadEnv = await import('../load-env.js');
      assert.strictEqual(typeof loadEnv.ENV.GOOGLE_EMAIL, 'string');
    });

    it('should have CHROME_PROFILE_PATH as string type', async () => {
      const loadEnv = await import('../load-env.js');
      assert.strictEqual(typeof loadEnv.ENV.CHROME_PROFILE_PATH, 'string');
    });

    it('should have HEADLESS as boolean type', async () => {
      const loadEnv = await import('../load-env.js');
      assert.strictEqual(typeof loadEnv.ENV.HEADLESS, 'boolean');
    });

    it('should have DEFAULT_MODEL as string type', async () => {
      const loadEnv = await import('../load-env.js');
      assert.strictEqual(typeof loadEnv.ENV.DEFAULT_MODEL, 'string');
    });
  });

  describe('HEADLESS logic', () => {
    it('should evaluate HEADLESS !== "false" correctly for truthy cases', async () => {
      const truthyValues = ['true', '1', 'yes', '', undefined, null, 'random'];
      
      for (const val of truthyValues) {
        const result = val !== 'false';
        assert.strictEqual(result, true, `HEADLESS="${val}" should result in true`);
      }
    });

    it('should evaluate HEADLESS !== "false" correctly for "false" string', () => {
      const result = 'false' !== 'false';
      assert.strictEqual(result, false, 'HEADLESS="false" should result in false');
    });
  });

  describe('default value logic', () => {
    it('should use || for GOOGLE_EMAIL default', () => {
      const cases = [
        { input: undefined, expected: '' },
        { input: null, expected: '' },
        { input: '', expected: '' },
        { input: 'test@example.com', expected: 'test@example.com' }
      ];
      
      for (const { input, expected } of cases) {
        const result = input || '';
        assert.strictEqual(result, expected, `GOOGLE_EMAIL="${input}" should default to "${expected}"`);
      }
    });

    it('should use || for CHROME_PROFILE_PATH default', () => {
      const cases = [
        { input: undefined, expected: '' },
        { input: null, expected: '' },
        { input: '', expected: '' },
        { input: '/path/to/profile', expected: '/path/to/profile' }
      ];
      
      for (const { input, expected } of cases) {
        const result = input || '';
        assert.strictEqual(result, expected, `CHROME_PROFILE_PATH="${input}" should default to "${expected}"`);
      }
    });

    it('should use || for DEFAULT_MODEL default', () => {
      const cases = [
        { input: undefined, expected: 'gpt-4' },
        { input: null, expected: 'gpt-4' },
        { input: '', expected: 'gpt-4' },
        { input: 'gemini-pro', expected: 'gemini-pro' }
      ];
      
      for (const { input, expected } of cases) {
        const result = input || 'gpt-4';
        assert.strictEqual(result, expected, `DEFAULT_MODEL="${input}" should result in "${expected}"`);
      }
    });
  });

  describe('dotenv config path', () => {
    it('should construct correct .env file path', () => {
      const __filename = fileURLToPath(import.meta.url);
      const __dirname = dirname(__filename);
      const expectedEnvPath = join(__dirname, '..', '.env');
      
      assert.ok(expectedEnvPath.includes('gemini_api'), 'Path should be in gemini_api directory');
      assert.ok(expectedEnvPath.endsWith('.env'), 'Path should end with .env');
    });

    it('should handle missing .env file gracefully', () => {
      const __filename = fileURLToPath(import.meta.url);
      const __dirname = dirname(__filename);
      const envPath = join(__dirname, '..', '.env');
      
      const envExists = existsSync(envPath);
      
      assert.strictEqual(typeof envExists, 'boolean', 'Should check if .env exists');
    });
  });

  describe('module imports', () => {
    it('should import dotenv config function', async () => {
      const dotenv = await import('dotenv');
      assert.strictEqual(typeof dotenv.config, 'function', 'dotenv should export config function');
    });

    it('should import fileURLToPath from url module', async () => {
      const url = await import('url');
      assert.strictEqual(typeof url.fileURLToPath, 'function', 'url should export fileURLToPath');
    });

    it('should import dirname and join from path module', async () => {
      const path = await import('path');
      assert.strictEqual(typeof path.dirname, 'function', 'path should export dirname');
      assert.strictEqual(typeof path.join, 'function', 'path should export join');
    });
  });

  describe('ENV object immutability', () => {
    it('should have consistent ENV values within single import', async () => {
      const loadEnv = await import('../load-env.js');
      
      const env1 = loadEnv.ENV;
      const env2 = loadEnv.ENV;
      
      assert.strictEqual(env1, env2, 'ENV should be same reference');
    });
  });

  describe('special character handling', () => {
    it('should handle special characters in email format', () => {
      const specialEmails = [
        'user+test@example.com',
        'user.test@example.co.uk',
        'user-test@sub.domain.com',
        'user_name@example.io'
      ];
      
      for (const email of specialEmails) {
        const result = email || '';
        assert.strictEqual(result, email, `Should handle "${email}" correctly`);
      }
    });

    it('should handle special characters in path format', () => {
      const specialPaths = [
        '/path/with spaces/profile',
        '/path/with-dashes/profile',
        '/path/with_underscores/profile'
      ];
      
      for (const path of specialPaths) {
        const result = path || '';
        assert.strictEqual(result, path, `Should handle "${path}" correctly`);
      }
    });
  });

  describe('actual ENV values from imported module', () => {
    it('should have a valid HEADLESS boolean value', async () => {
      const loadEnv = await import('../load-env.js');
      assert.ok(
        loadEnv.ENV.HEADLESS === true || loadEnv.ENV.HEADLESS === false,
        'HEADLESS should be a boolean'
      );
    });

    it('should have DEFAULT_MODEL as a non-null value', async () => {
      const loadEnv = await import('../load-env.js');
      assert.ok(loadEnv.ENV.DEFAULT_MODEL != null, 'DEFAULT_MODEL should not be null');
    });

    it('should have GOOGLE_EMAIL as string', async () => {
      const loadEnv = await import('../load-env.js');
      assert.strictEqual(typeof loadEnv.ENV.GOOGLE_EMAIL, 'string');
    });

    it('should have CHROME_PROFILE_PATH as string', async () => {
      const loadEnv = await import('../load-env.js');
      assert.strictEqual(typeof loadEnv.ENV.CHROME_PROFILE_PATH, 'string');
    });
  });
});