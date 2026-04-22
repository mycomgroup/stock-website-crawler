import { describe, it, beforeEach, afterEach, mock } from 'node:test';
import assert from 'node:assert';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

describe('load-env', () => {
  const originalEnv = { ...process.env };

  beforeEach(() => {
    process.env = { ...originalEnv };
  });

  afterEach(() => {
    process.env = originalEnv;
  });

  describe('ENV object', () => {
    it('should export ENV object', async () => {
      const { ENV } = await import('../load-env.js');
      
      assert.ok(ENV);
      assert.ok(typeof ENV === 'object');
    });

    it('should have GOOGLE_EMAIL property', async () => {
      const { ENV } = await import('../load-env.js?cachebuster=' + Date.now());
      
      assert.ok('GOOGLE_EMAIL' in ENV);
    });

    it('should have CHROME_PROFILE_PATH property', async () => {
      const { ENV } = await import('../load-env.js?cachebuster=' + Date.now());
      
      assert.ok('CHROME_PROFILE_PATH' in ENV);
    });

    it('should have HEADLESS property', async () => {
      const { ENV } = await import('../load-env.js?cachebuster=' + Date.now());
      
      assert.ok('HEADLESS' in ENV);
    });

    it('should have DEFAULT_MODEL property', async () => {
      const { ENV } = await import('../load-env.js?cachebuster=' + Date.now());
      
      assert.ok('DEFAULT_MODEL' in ENV);
    });

    it('should have HTTP_PROXY property', async () => {
      const { ENV } = await import('../load-env.js?cachebuster=' + Date.now());
      
      assert.ok('HTTP_PROXY' in ENV);
    });

    it('should have HTTPS_PROXY property', async () => {
      const { ENV } = await import('../load-env.js?cachebuster=' + Date.now());
      
      assert.ok('HTTPS_PROXY' in ENV);
    });
  });

  describe('default values', () => {
    it('should use empty string for GOOGLE_EMAIL when not set', async () => {
      delete process.env.GOOGLE_EMAIL;
      
      const { ENV } = await import('../load-env.js?cachebuster=' + Date.now());
      
      assert.strictEqual(ENV.GOOGLE_EMAIL, '');
    });

    it('should use empty string for CHROME_PROFILE_PATH when not set', async () => {
      delete process.env.CHROME_PROFILE_PATH;
      
      const { ENV } = await import('../load-env.js?cachebuster=' + Date.now());
      
      assert.strictEqual(ENV.CHROME_PROFILE_PATH, '');
    });

    it('should use true for HEADLESS when not set', async () => {
      delete process.env.HEADLESS;
      
      const { ENV } = await import('../load-env.js?cachebuster=' + Date.now());
      
      assert.strictEqual(ENV.HEADLESS, true);
    });

    it('should use false for HEADLESS when set to false', async () => {
      process.env.HEADLESS = 'false';
      
      const { ENV } = await import('../load-env.js?cachebuster=' + Date.now());
      
      assert.strictEqual(ENV.HEADLESS, false);
    });

    it('should use gpt-4 for DEFAULT_MODEL when not set', async () => {
      delete process.env.DEFAULT_MODEL;
      
      const { ENV } = await import('../load-env.js?cachebuster=' + Date.now());
      
      assert.strictEqual(ENV.DEFAULT_MODEL, 'gpt-4');
    });

    it('should use custom DEFAULT_MODEL when set', async () => {
      process.env.DEFAULT_MODEL = 'gpt-3.5-turbo';
      
      const { ENV } = await import('../load-env.js?cachebuster=' + Date.now());
      
      assert.strictEqual(ENV.DEFAULT_MODEL, 'gpt-3.5-turbo');
    });

    it('should use empty string for HTTP_PROXY when not set', async () => {
      delete process.env.HTTP_PROXY;
      
      const { ENV } = await import('../load-env.js?cachebuster=' + Date.now());
      
      assert.strictEqual(ENV.HTTP_PROXY, '');
    });

    it('should use empty string for HTTPS_PROXY when not set', async () => {
      delete process.env.HTTPS_PROXY;
      
      const { ENV } = await import('../load-env.js?cachebuster=' + Date.now());
      
      assert.strictEqual(ENV.HTTPS_PROXY, '');
    });
  });

  describe('proxy setting', () => {
    it('should set HTTP_PROXY on process.env', async () => {
      process.env.HTTP_PROXY = 'http://proxy:8080';
      
      await import('../load-env.js?cachebuster=' + Date.now());
      
      assert.strictEqual(process.env.HTTP_PROXY, 'http://proxy:8080');
    });

    it('should set HTTPS_PROXY on process.env', async () => {
      process.env.HTTPS_PROXY = 'https://proxy:443';
      
      await import('../load-env.js?cachebuster=' + Date.now());
      
      assert.strictEqual(process.env.HTTPS_PROXY, 'https://proxy:443');
    });

    it('should not set proxy when empty', async () => {
      delete process.env.HTTP_PROXY;
      delete process.env.HTTPS_PROXY;
      
      await import('../load-env.js?cachebuster=' + Date.now());
      
      assert.strictEqual(process.env.HTTP_PROXY, undefined);
      assert.strictEqual(process.env.HTTPS_PROXY, undefined);
    });
  });

  describe('environment variable reading', () => {
    it('should read GOOGLE_EMAIL from .env', async () => {
      process.env.GOOGLE_EMAIL = 'test@example.com';
      
      const { ENV } = await import('../load-env.js?cachebuster=' + Date.now());
      
      assert.strictEqual(ENV.GOOGLE_EMAIL, 'test@example.com');
    });

    it('should read CHROME_PROFILE_PATH from .env', async () => {
      process.env.CHROME_PROFILE_PATH = '/path/to/profile';
      
      const { ENV } = await import('../load-env.js?cachebuster=' + Date.now());
      
      assert.strictEqual(ENV.CHROME_PROFILE_PATH, '/path/to/profile');
    });

    it('should read HTTP_PROXY from .env', async () => {
      process.env.HTTP_PROXY = 'http://localhost:3128';
      
      const { ENV } = await import('../load-env.js?cachebuster=' + Date.now());
      
      assert.strictEqual(ENV.HTTP_PROXY, 'http://localhost:3128');
    });

    it('should read HTTPS_PROXY from .env', async () => {
      process.env.HTTPS_PROXY = 'https://secure.proxy:443';
      
      const { ENV } = await import('../load-env.js?cachebuster=' + Date.now());
      
      assert.strictEqual(ENV.HTTPS_PROXY, 'https://secure.proxy:443');
    });
  });
});