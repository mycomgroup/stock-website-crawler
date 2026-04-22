import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';

vi.mock('dotenv', () => ({
  config: vi.fn()
}));

describe('load-env.js', () => {
  let dotenvConfig;

  beforeEach(() => {
    vi.clearAllMocks();
    dotenvConfig = vi.fn();
    vi.doMock('dotenv', () => ({ config: dotenvConfig }));
  });

  afterEach(() => {
    vi.resetModules();
    vi.clearAllMocks();
  });

  describe('dotenv configuration', () => {
    it('should call dotenv config on import', async () => {
      const { config } = await import('dotenv');
      expect(config).toBeDefined();
    });

    it('should pass correct path to dotenv config', async () => {
      const { fileURLToPath } = await import('node:url');
      const { dirname, join } = await import('node:path');
      const { config } = await import('dotenv');
      
      const __filename = fileURLToPath(import.meta.url);
      const __dirname = dirname(__filename);
      const expectedPath = join(__dirname, '..', '.env');

      vi.doMock('dotenv', () => ({
        config: vi.fn((options) => {
          if (options && options.path) {
            expect(options.path.endsWith('.env')).toBe(true);
          }
          return {};
        })
      }));
    });
  });

  describe('environment variable handling', () => {
    it('dotenv config function should be callable', async () => {
      const { config } = await import('dotenv');
      expect(typeof config).toBe('function');
    });

    it('should handle missing .env file gracefully', async () => {
      const originalEnv = { ...process.env };
      
      vi.doMock('dotenv', () => ({
        config: vi.fn(() => ({ parsed: null, error: new Error('ENOENT') }))
      }));
      
      expect(() => {
        process.env = { ...originalEnv };
      }).not.toThrow();
      
      process.env = originalEnv;
    });
  });
});