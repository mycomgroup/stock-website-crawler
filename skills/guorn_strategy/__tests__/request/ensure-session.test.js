import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import fs from 'node:fs';
import path from 'node:path';

vi.mock('node:fs');
vi.mock('node:path', () => ({
  default: {
    resolve: vi.fn((...args) => args.join('/')),
  },
  resolve: vi.fn((...args) => args.join('/')),
}));

vi.mock('../../request/guorn-strategy-client.js', () => ({
  GuornStrategyClient: vi.fn().mockImplementation(() => ({
    getUserProfile: vi.fn(),
  })),
}));

vi.mock('../../browser/capture-session.js', () => ({
  captureGuornSession: vi.fn(),
}));

vi.mock('../../paths.js', () => ({
  SESSION_FILE: '/test/sessions/guorn.json',
}));

vi.mock('../../load-env.js', () => {});

describe('ensure-session.js', () => {
  let consoleLogSpy;

  beforeEach(() => {
    vi.clearAllMocks();
    consoleLogSpy = vi.spyOn(console, 'log').mockImplementation(() => {});
    
    vi.mocked(fs.existsSync).mockReturnValue(true);
    vi.mocked(fs.readFileSync).mockReturnValue(JSON.stringify({
      cookies: [{ name: '_xsrf', value: 'test_token' }]
    }));
  });

  afterEach(() => {
    consoleLogSpy.mockRestore();
  });

  describe('ensureGuornSession', () => {
    it('should return existing session when valid', async () => {
      const { ensureGuornSession } = await import('../../request/ensure-session.js');
      const { GuornStrategyClient } = await import('../../request/guorn-strategy-client.js');
      
      vi.mocked(GuornStrategyClient).mockImplementation(() => ({
        getUserProfile: vi.fn().mockResolvedValue({ status: 'ok' }),
      }));
      
      const result = await ensureGuornSession();
      
      expect(result.sessionFile).toBeDefined();
      expect(result.refreshed).toBe(false);
    });

    it('should refresh session when forceRefresh is true', async () => {
      const { ensureGuornSession } = await import('../../request/ensure-session.js');
      const { captureGuornSession } = await import('../../browser/capture-session.js');
      
      vi.mocked(captureGuornSession).mockResolvedValue({
        cookies: [{ name: 'new_session', value: 'value' }]
      });
      
      const result = await ensureGuornSession({ forceRefresh: true });
      
      expect(result.refreshed).toBe(true);
      expect(captureGuornSession).toHaveBeenCalled();
    });

    it('should refresh session when session file does not exist', async () => {
      const { ensureGuornSession } = await import('../../request/ensure-session.js');
      const { captureGuornSession } = await import('../../browser/capture-session.js');
      
      vi.mocked(fs.existsSync).mockReturnValue(false);
      vi.mocked(captureGuornSession).mockResolvedValue({
        cookies: []
      });
      
      const result = await ensureGuornSession();
      
      expect(result.refreshed).toBe(true);
    });

    it('should refresh session when profile check fails', async () => {
      const { ensureGuornSession } = await import('../../request/ensure-session.js');
      const { GuornStrategyClient } = await import('../../request/guorn-strategy-client.js');
      const { captureGuornSession } = await import('../../browser/capture-session.js');
      
      vi.mocked(GuornStrategyClient).mockImplementation(() => ({
        getUserProfile: vi.fn().mockRejectedValue(new Error('Session expired')),
      }));
      
      vi.mocked(captureGuornSession).mockResolvedValue({
        cookies: []
      });
      
      const result = await ensureGuornSession();
      
      expect(result.refreshed).toBe(true);
    });

    it('should refresh session when profile status is not ok', async () => {
      const { ensureGuornSession } = await import('../../request/ensure-session.js');
      const { GuornStrategyClient } = await import('../../request/guorn-strategy-client.js');
      const { captureGuornSession } = await import('../../browser/capture-session.js');
      
      vi.mocked(GuornStrategyClient).mockImplementation(() => ({
        getUserProfile: vi.fn().mockResolvedValue({ status: 'error' }),
      }));
      
      vi.mocked(captureGuornSession).mockResolvedValue({
        cookies: []
      });
      
      const result = await ensureGuornSession();
      
      expect(result.refreshed).toBe(true);
    });

    it('should use custom session file path', async () => {
      const { ensureGuornSession } = await import('../../request/ensure-session.js');
      const { GuornStrategyClient } = await import('../../request/guorn-strategy-client.js');
      
      vi.mocked(GuornStrategyClient).mockImplementation(() => ({
        getUserProfile: vi.fn().mockResolvedValue({ status: 'ok' }),
      }));
      
      const result = await ensureGuornSession({ sessionFile: '/custom/session.json' });
      
      expect(path.resolve).toHaveBeenCalledWith('/custom/session.json');
    });

    it('should pass headed option to captureGuornSession', async () => {
      const { ensureGuornSession } = await import('../../request/ensure-session.js');
      const { captureGuornSession } = await import('../../browser/capture-session.js');
      
      vi.mocked(fs.existsSync).mockReturnValue(false);
      vi.mocked(captureGuornSession).mockResolvedValue({});
      
      await ensureGuornSession({ headed: true });
      
      expect(captureGuornSession).toHaveBeenCalledWith({ headed: true });
    });

    it('should handle error during session check', async () => {
      const { ensureGuornSession } = await import('../../request/ensure-session.js');
      const { GuornStrategyClient } = await import('../../request/guorn-strategy-client.js');
      const { captureGuornSession } = await import('../../browser/capture-session.js');
      
      vi.mocked(GuornStrategyClient).mockImplementation(() => ({
        getUserProfile: vi.fn().mockImplementation(() => {
          throw new Error('Network error');
        }),
      }));
      
      vi.mocked(captureGuornSession).mockResolvedValue({});
      
      const result = await ensureGuornSession();
      
      expect(result.refreshed).toBe(true);
    });

    it('should log session valid message', async () => {
      const { ensureGuornSession } = await import('../../request/ensure-session.js');
      const { GuornStrategyClient } = await import('../../request/guorn-strategy-client.js');
      
      vi.mocked(GuornStrategyClient).mockImplementation(() => ({
        getUserProfile: vi.fn().mockResolvedValue({ status: 'ok' }),
      }));
      
      await ensureGuornSession();
      
      expect(consoleLogSpy).toHaveBeenCalledWith('Session valid');
    });

    it('should log session invalid message on error', async () => {
      const { ensureGuornSession } = await import('../../request/ensure-session.js');
      const { GuornStrategyClient } = await import('../../request/guorn-strategy-client.js');
      const { captureGuornSession } = await import('../../browser/capture-session.js');
      
      vi.mocked(GuornStrategyClient).mockImplementation(() => ({
        getUserProfile: vi.fn().mockRejectedValue(new Error('Invalid')),
      }));
      
      vi.mocked(captureGuornSession).mockResolvedValue({});
      
      await ensureGuornSession();
      
      expect(consoleLogSpy).toHaveBeenCalledWith('Session invalid, refreshing...', 'Invalid');
    });

    it('should return capture result when session is refreshed', async () => {
      const { ensureGuornSession } = await import('../../request/ensure-session.js');
      const { captureGuornSession } = await import('../../browser/capture-session.js');
      
      vi.mocked(fs.existsSync).mockReturnValue(false);
      
      const captureResult = {
        cookies: [{ name: 'session', value: 'new' }],
        capturedAt: '2024-01-01T00:00:00Z'
      };
      vi.mocked(captureGuornSession).mockResolvedValue(captureResult);
      
      const result = await ensureGuornSession();
      
      expect(result.result).toEqual(captureResult);
    });
  });
});