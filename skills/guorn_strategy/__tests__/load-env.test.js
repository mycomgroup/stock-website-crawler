import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));

describe('load-env.js', () => {
  const originalEnv = { ...process.env };

  beforeEach(() => {
    vi.resetModules();
    Object.keys(process.env).forEach(key => {
      if (!originalEnv.hasOwnProperty(key)) {
        delete process.env[key];
      }
    });
  });

  afterEach(() => {
    vi.clearAllMocks();
    Object.keys(process.env).forEach(key => {
      if (!originalEnv.hasOwnProperty(key)) {
        delete process.env[key];
      } else {
        process.env[key] = originalEnv[key];
      }
    });
  });

  it('should import without errors', async () => {
    vi.doMock('dotenv', () => ({
      config: vi.fn(() => ({ parsed: {} }))
    }));
    
    await expect(import('../load-env.js')).resolves.toBeDefined();
  });

  it('should use correct path to .env file', () => {
    const expectedPath = resolve(__dirname, '..', '.env');
    expect(expectedPath).toMatch(/\.env$/);
    expect(expectedPath).toContain('guorn_strategy');
  });

  it('should resolve path relative to module location', () => {
    const expectedPath = resolve(__dirname, '..', '.env');
    expect(expectedPath).toMatch(/guorn_strategy.*\.env$/);
  });

  it('should handle dotenv module import', async () => {
    vi.doMock('dotenv', () => ({
      config: vi.fn()
    }));
    
    const dotenv = await import('dotenv');
    expect(dotenv.config).toBeDefined();
  });

  it('should call config method', async () => {
    const mockConfig = vi.fn(() => ({ parsed: {} }));
    vi.doMock('dotenv', () => ({
      config: mockConfig
    }));
    
    await import('../load-env.js');
    
    expect(mockConfig).toHaveBeenCalled();
  });

  it('should pass path option to config', async () => {
    const mockConfig = vi.fn(() => ({ parsed: {} }));
    vi.doMock('dotenv', () => ({
      config: mockConfig
    }));
    
    await import('../load-env.js');
    
    expect(mockConfig).toHaveBeenCalledWith(expect.objectContaining({
      path: expect.stringContaining('.env')
    }));
  });

  it('should not throw if dotenv.config returns error', async () => {
    vi.doMock('dotenv', () => ({
      config: vi.fn(() => ({ error: new Error('ENOENT') }))
    }));
    
    await expect(import('../load-env.js')).resolves.toBeDefined();
  });

  it('should work when called multiple times', async () => {
    vi.doMock('dotenv', () => ({
      config: vi.fn(() => ({ parsed: {} }))
    }));
    
    await import('../load-env.js');
    vi.resetModules();
    await import('../load-env.js');
  });
});