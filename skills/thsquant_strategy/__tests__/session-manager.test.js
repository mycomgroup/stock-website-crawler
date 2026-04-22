import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import fs from 'node:fs';
import path from 'node:path';

vi.mock('node:fs');
vi.mock('node:path', () => ({
  default: {
    dirname: vi.fn((p) => p.split('/').slice(0, -1).join('/')),
  },
  dirname: vi.fn((p) => p.split('/').slice(0, -1).join('/')),
}));

vi.mock('../browser/capture-session.js', () => ({
  captureTHSQuantSession: vi.fn(),
}));

vi.mock('../paths.js', () => ({
  SESSION_FILE: '/test/sessions/thsquant.json',
  OUTPUT_ROOT: '/test/output',
}));

const { captureTHSQuantSession } = await import('../browser/capture-session.js');

const sessionManager = await import('../browser/session-manager.js');

describe('session-manager.js', () => {
  let consoleLogSpy;
  let consoleErrorSpy;

  beforeEach(() => {
    vi.clearAllMocks();
    consoleLogSpy = vi.spyOn(console, 'log').mockImplementation(() => {});
    consoleErrorSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
  });

  afterEach(() => {
    consoleLogSpy.mockRestore();
    consoleErrorSpy.mockRestore();
  });

  describe('isSessionValid', () => {
    it('should return false for null session', () => {
      expect(sessionManager.isSessionValid(null)).toBe(false);
    });

    it('should return false for undefined session', () => {
      expect(sessionManager.isSessionValid(undefined)).toBe(false);
    });

    it('should return false for session without cookies property', () => {
      expect(sessionManager.isSessionValid({ timestamp: Date.now() })).toBe(false);
    });

    it('should return false for session with empty cookies array', () => {
      expect(sessionManager.isSessionValid({ cookies: [], timestamp: Date.now() })).toBe(false);
    });

    it('should return false when no valid cookie names (no sid, token, session, auth, ths)', () => {
      const session = {
        cookies: [{ name: 'other' }, { name: 'random' }],
        timestamp: Date.now(),
      };
      expect(sessionManager.isSessionValid(session)).toBe(false);
      expect(consoleLogSpy).toHaveBeenCalledWith('No valid session cookie found');
    });

    it('should return true for cookie with "sid" in name', () => {
      const session = {
        cookies: [{ name: 'my_sid_cookie' }],
        timestamp: Date.now(),
      };
      expect(sessionManager.isSessionValid(session)).toBe(true);
    });

    it('should return true for cookie with "token" in name', () => {
      const session = {
        cookies: [{ name: 'auth_token' }],
        timestamp: Date.now(),
      };
      expect(sessionManager.isSessionValid(session)).toBe(true);
    });

    it('should return true for cookie with "session" in name', () => {
      const session = {
        cookies: [{ name: 'session_id' }],
        timestamp: Date.now(),
      };
      expect(sessionManager.isSessionValid(session)).toBe(true);
    });

    it('should return true for cookie with "auth" in name', () => {
      const session = {
        cookies: [{ name: 'user_auth' }],
        timestamp: Date.now(),
      };
      expect(sessionManager.isSessionValid(session)).toBe(true);
    });

    it('should return true for cookie with "ths" in name', () => {
      const session = {
        cookies: [{ name: 'ths_session' }],
        timestamp: Date.now(),
      };
      expect(sessionManager.isSessionValid(session)).toBe(true);
    });

    it('should return false for expired session (> 7 days old)', () => {
      const EIGHT_DAYS = 8 * 24 * 60 * 60 * 1000;
      const session = {
        cookies: [{ name: 'sid' }],
        timestamp: Date.now() - EIGHT_DAYS,
      };
      expect(sessionManager.isSessionValid(session)).toBe(false);
      expect(consoleLogSpy).toHaveBeenCalledWith('Session expired (> 7 days old)');
    });

    it('should return true for session exactly 7 days old (boundary)', () => {
      const SEVEN_DAYS = 7 * 24 * 60 * 60 * 1000;
      const session = {
        cookies: [{ name: 'sid' }],
        timestamp: Date.now() - SEVEN_DAYS + 1000,
      };
      expect(sessionManager.isSessionValid(session)).toBe(true);
    });

    it('should return true for session with missing timestamp (defaults to 0, will be expired)', () => {
      const session = {
        cookies: [{ name: 'sid' }],
      };
      expect(sessionManager.isSessionValid(session)).toBe(false);
    });

    it('should return true for valid session with valid cookies and fresh timestamp', () => {
      const session = {
        cookies: [{ name: 'sid' }, { name: 'token' }],
        timestamp: Date.now(),
      };
      expect(sessionManager.isSessionValid(session)).toBe(true);
    });
  });

  describe('ensureTHSQuantSession', () => {
    it('should return existing cookies when valid session exists', async () => {
      const mockSession = {
        cookies: [{ name: 'sid', value: 'test123' }],
        timestamp: Date.now(),
      };
      
      vi.mocked(fs.existsSync).mockReturnValue(true);
      vi.mocked(fs.readFileSync).mockReturnValue(JSON.stringify(mockSession));

      const result = await sessionManager.ensureTHSQuantSession({ username: 'user', password: 'pass' });

      expect(result).toEqual(mockSession.cookies);
      expect(captureTHSQuantSession).not.toHaveBeenCalled();
    });

    it('should perform login when session is invalid', async () => {
      const mockCookies = [{ name: 'sid', value: 'new_session' }];
      vi.mocked(fs.existsSync).mockReturnValue(false);
      vi.mocked(captureTHSQuantSession).mockResolvedValue({ cookies: mockCookies, timestamp: Date.now() });

      const result = await sessionManager.ensureTHSQuantSession({ username: 'user', password: 'pass' });

      expect(captureTHSQuantSession).toHaveBeenCalledWith({ username: 'user', password: 'pass' });
      expect(result).toEqual(mockCookies);
    });

    it('should force refresh when forceRefresh is true', async () => {
      const mockSession = {
        cookies: [{ name: 'sid', value: 'old_session' }],
        timestamp: Date.now(),
      };
      const newCookies = [{ name: 'sid', value: 'new_session' }];
      
      vi.mocked(fs.existsSync).mockReturnValue(true);
      vi.mocked(fs.readFileSync).mockReturnValue(JSON.stringify(mockSession));
      vi.mocked(captureTHSQuantSession).mockResolvedValue({ cookies: newCookies, timestamp: Date.now() });

      const result = await sessionManager.ensureTHSQuantSession(
        { username: 'user', password: 'pass' },
        true
      );

      expect(captureTHSQuantSession).toHaveBeenCalled();
      expect(result).toEqual(newCookies);
    });

    it('should not check existing session when forceRefresh is true', async () => {
      const newCookies = [{ name: 'sid', value: 'new_session' }];
      vi.mocked(captureTHSQuantSession).mockResolvedValue({ cookies: newCookies, timestamp: Date.now() });

      await sessionManager.ensureTHSQuantSession(
        { username: 'user', password: 'pass' },
        true
      );

      expect(fs.existsSync).not.toHaveBeenCalled();
    });

    it('should throw error when credentials are missing', async () => {
      vi.mocked(fs.existsSync).mockReturnValue(false);

      await expect(sessionManager.ensureTHSQuantSession({})).rejects.toThrow(
        'Missing credentials. Please provide username and password.'
      );
    });

    it('should throw error when username is missing', async () => {
      vi.mocked(fs.existsSync).mockReturnValue(false);

      await expect(sessionManager.ensureTHSQuantSession({ password: 'pass' })).rejects.toThrow(
        'Missing credentials. Please provide username and password.'
      );
    });

    it('should throw error when password is missing', async () => {
      vi.mocked(fs.existsSync).mockReturnValue(false);

      await expect(sessionManager.ensureTHSQuantSession({ username: 'user' })).rejects.toThrow(
        'Missing credentials. Please provide username and password.'
      );
    });
  });

  describe('withAutoRelogin', () => {
    it('should call function with cookies and return result', async () => {
      const mockSession = {
        cookies: [{ name: 'sid', value: 'test123' }],
        timestamp: Date.now(),
      };
      vi.mocked(fs.existsSync).mockReturnValue(true);
      vi.mocked(fs.readFileSync).mockReturnValue(JSON.stringify(mockSession));

      const fn = vi.fn().mockResolvedValue({ success: true });
      const result = await sessionManager.withAutoRelogin({ username: 'user', password: 'pass' }, fn);

      expect(fn).toHaveBeenCalledWith(mockSession.cookies);
      expect(result).toEqual({ success: true });
    });

    it('should re-login on "Not logged in" error', async () => {
      const oldSession = {
        cookies: [{ name: 'sid', value: 'old' }],
        timestamp: Date.now(),
      };
      const newSession = {
        cookies: [{ name: 'sid', value: 'new' }],
        timestamp: Date.now(),
      };

      vi.mocked(fs.existsSync).mockReturnValue(true);
      vi.mocked(fs.readFileSync)
        .mockReturnValueOnce(JSON.stringify(oldSession))
        .mockReturnValueOnce(JSON.stringify(newSession));
      vi.mocked(captureTHSQuantSession).mockResolvedValue(newSession);

      let callCount = 0;
      const fn = vi.fn().mockImplementation(() => {
        callCount++;
        if (callCount === 1) {
          throw new Error('Not logged in');
        }
        return { success: true };
      });

      const result = await sessionManager.withAutoRelogin({ username: 'user', password: 'pass' }, fn);

      expect(fn).toHaveBeenCalledTimes(2);
      expect(result).toEqual({ success: true });
    });

    it('should re-login on "401" error', async () => {
      const mockSession = {
        cookies: [{ name: 'sid', value: 'test' }],
        timestamp: Date.now(),
      };
      vi.mocked(fs.existsSync).mockReturnValue(true);
      vi.mocked(fs.readFileSync).mockReturnValue(JSON.stringify(mockSession));
      vi.mocked(captureTHSQuantSession).mockResolvedValue(mockSession);

      let callCount = 0;
      const fn = vi.fn().mockImplementation(() => {
        callCount++;
        if (callCount === 1) {
          throw new Error('401 Unauthorized');
        }
        return { success: true };
      });

      const result = await sessionManager.withAutoRelogin({ username: 'user', password: 'pass' }, fn);
      expect(result).toEqual({ success: true });
    });

    it('should re-login on "403" error', async () => {
      const mockSession = {
        cookies: [{ name: 'sid', value: 'test' }],
        timestamp: Date.now(),
      };
      vi.mocked(fs.existsSync).mockReturnValue(true);
      vi.mocked(fs.readFileSync).mockReturnValue(JSON.stringify(mockSession));
      vi.mocked(captureTHSQuantSession).mockResolvedValue(mockSession);

      let callCount = 0;
      const fn = vi.fn().mockImplementation(() => {
        callCount++;
        if (callCount === 1) {
          throw new Error('403 Forbidden');
        }
        return { success: true };
      });

      const result = await sessionManager.withAutoRelogin({ username: 'user', password: 'pass' }, fn);
      expect(result).toEqual({ success: true });
    });

    it('should re-login on "Unauthorized" error', async () => {
      const mockSession = {
        cookies: [{ name: 'sid', value: 'test' }],
        timestamp: Date.now(),
      };
      vi.mocked(fs.existsSync).mockReturnValue(true);
      vi.mocked(fs.readFileSync).mockReturnValue(JSON.stringify(mockSession));
      vi.mocked(captureTHSQuantSession).mockResolvedValue(mockSession);

      let callCount = 0;
      const fn = vi.fn().mockImplementation(() => {
        callCount++;
        if (callCount === 1) {
          throw new Error('Unauthorized access');
        }
        return { success: true };
      });

      const result = await sessionManager.withAutoRelogin({ username: 'user', password: 'pass' }, fn);
      expect(result).toEqual({ success: true });
    });

    it('should re-login on "login" error message', async () => {
      const mockSession = {
        cookies: [{ name: 'sid', value: 'test' }],
        timestamp: Date.now(),
      };
      vi.mocked(fs.existsSync).mockReturnValue(true);
      vi.mocked(fs.readFileSync).mockReturnValue(JSON.stringify(mockSession));
      vi.mocked(captureTHSQuantSession).mockResolvedValue(mockSession);

      let callCount = 0;
      const fn = vi.fn().mockImplementation(() => {
        callCount++;
        if (callCount === 1) {
          throw new Error('Please login to continue');
        }
        return { success: true };
      });

      const result = await sessionManager.withAutoRelogin({ username: 'user', password: 'pass' }, fn);
      expect(result).toEqual({ success: true });
    });

    it('should re-login on "session" error message', async () => {
      const mockSession = {
        cookies: [{ name: 'sid', value: 'test' }],
        timestamp: Date.now(),
      };
      vi.mocked(fs.existsSync).mockReturnValue(true);
      vi.mocked(fs.readFileSync).mockReturnValue(JSON.stringify(mockSession));
      vi.mocked(captureTHSQuantSession).mockResolvedValue(mockSession);

      let callCount = 0;
      const fn = vi.fn().mockImplementation(() => {
        callCount++;
        if (callCount === 1) {
          throw new Error('session expired');
        }
        return { success: true };
      });

      const result = await sessionManager.withAutoRelogin({ username: 'user', password: 'pass' }, fn);
      expect(result).toEqual({ success: true });
    });

    it('should throw non-session errors', async () => {
      const mockSession = {
        cookies: [{ name: 'sid', value: 'test' }],
        timestamp: Date.now(),
      };
      vi.mocked(fs.existsSync).mockReturnValue(true);
      vi.mocked(fs.readFileSync).mockReturnValue(JSON.stringify(mockSession));

      const fn = vi.fn().mockRejectedValue(new Error('Network error'));

      await expect(
        sessionManager.withAutoRelogin({ username: 'user', password: 'pass' }, fn)
      ).rejects.toThrow('Network error');
    });

    it('should delete session file on session error', async () => {
      const mockSession = {
        cookies: [{ name: 'sid', value: 'test' }],
        timestamp: Date.now(),
      };
      vi.mocked(fs.existsSync).mockReturnValue(true);
      vi.mocked(fs.readFileSync).mockReturnValue(JSON.stringify(mockSession));
      vi.mocked(captureTHSQuantSession).mockResolvedValue(mockSession);

      let callCount = 0;
      const fn = vi.fn().mockImplementation(() => {
        callCount++;
        if (callCount === 1) {
          throw new Error('session expired');
        }
        return { success: true };
      });

      await sessionManager.withAutoRelogin({ username: 'user', password: 'pass' }, fn);
      expect(fs.unlinkSync).toHaveBeenCalledWith('/test/sessions/thsquant.json');
    });

    it('should not throw if session file deletion fails', async () => {
      const mockSession = {
        cookies: [{ name: 'sid', value: 'test' }],
        timestamp: Date.now(),
      };
      vi.mocked(fs.existsSync).mockReturnValue(true);
      vi.mocked(fs.readFileSync).mockReturnValue(JSON.stringify(mockSession));
      vi.mocked(captureTHSQuantSession).mockResolvedValue(mockSession);
      vi.mocked(fs.unlinkSync).mockImplementation(() => {
        throw new Error('File not found');
      });

      let callCount = 0;
      const fn = vi.fn().mockImplementation(() => {
        callCount++;
        if (callCount === 1) {
          throw new Error('session expired');
        }
        return { success: true };
      });

      const result = await sessionManager.withAutoRelogin({ username: 'user', password: 'pass' }, fn);
      expect(result).toEqual({ success: true });
    });
  });

  describe('saveJson helper (indirect test via doLogin)', () => {
    it('should save session to file after login', async () => {
      const mockSession = {
        cookies: [{ name: 'sid', value: 'test' }],
        timestamp: Date.now(),
      };
      vi.mocked(fs.existsSync).mockReturnValue(false);
      vi.mocked(captureTHSQuantSession).mockResolvedValue(mockSession);

      await sessionManager.ensureTHSQuantSession({ username: 'user', password: 'pass' });

      expect(fs.writeFileSync).toHaveBeenCalled();
      expect(fs.mkdirSync).toHaveBeenCalled();
    });
  });

  describe('loadJson helper (indirect test)', () => {
    it('should return null for non-existent file', async () => {
      vi.mocked(fs.existsSync).mockReturnValue(false);
      vi.mocked(captureTHSQuantSession).mockResolvedValue({
        cookies: [{ name: 'sid' }],
        timestamp: Date.now(),
      });

      await sessionManager.ensureTHSQuantSession({ username: 'user', password: 'pass' });

      expect(fs.existsSync).toHaveBeenCalledWith('/test/sessions/thsquant.json');
    });

    it('should return null for invalid JSON', async () => {
      vi.mocked(fs.existsSync).mockReturnValue(true);
      vi.mocked(fs.readFileSync).mockReturnValue('invalid json');
      vi.mocked(captureTHSQuantSession).mockResolvedValue({
        cookies: [{ name: 'sid' }],
        timestamp: Date.now(),
      });

      await sessionManager.ensureTHSQuantSession({ username: 'user', password: 'pass' });

      expect(captureTHSQuantSession).toHaveBeenCalled();
    });
  });
});