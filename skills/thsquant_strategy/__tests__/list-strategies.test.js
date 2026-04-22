import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';

const mockCheckLogin = vi.fn();
const mockListStrategies = vi.fn();
const mockEnsureTHSQuantSession = vi.fn();

vi.mock('../load-env.js', () => ({}));

vi.mock('../request/thsquant-client.js', () => ({
  THSQuantClient: vi.fn().mockImplementation(() => ({
    checkLogin: mockCheckLogin,
    listStrategies: mockListStrategies
  }))
}));

vi.mock('../browser/session-manager.js', () => ({
  ensureTHSQuantSession: mockEnsureTHSQuantSession
}));

describe('list-strategies.js', () => {
  let mockConsoleLog;
  let mockConsoleError;
  let originalConsoleLog;
  let originalConsoleError;

  beforeEach(async () => {
    vi.resetModules();
    
    originalConsoleLog = console.log;
    originalConsoleError = console.error;
    mockConsoleLog = vi.fn();
    mockConsoleError = vi.fn();
    console.log = mockConsoleLog;
    console.error = mockConsoleError;

    mockCheckLogin.mockReset();
    mockListStrategies.mockReset();
    mockEnsureTHSQuantSession.mockReset();
  });

  afterEach(() => {
    console.log = originalConsoleLog;
    console.error = originalConsoleError;
    vi.clearAllMocks();
  });

  describe('listStrategies function', () => {
    it('should successfully list strategies', async () => {
      const mockCookies = [{ name: 'sid', value: 'test-sid' }];
      
      mockEnsureTHSQuantSession.mockResolvedValue(mockCookies);
      mockCheckLogin.mockResolvedValue({ code: 0, logged: true, userId: 'user-123' });
      mockListStrategies.mockResolvedValue([
        { id: 'algo-1', name: 'Strategy One' },
        { id: 'algo-2', name: 'Strategy Two' }
      ]);

      process.env.THSQUANT_USERNAME = 'testuser';
      process.env.THSQUANT_PASSWORD = 'testpass';

      await import('../list-strategies.js');
      
      expect(mockEnsureTHSQuantSession).toHaveBeenCalled();
      expect(mockCheckLogin).toHaveBeenCalled();
      expect(mockListStrategies).toHaveBeenCalled();

      delete process.env.THSQUANT_USERNAME;
      delete process.env.THSQUANT_PASSWORD;
    });

    it('should handle login failure (code -1)', async () => {
      const mockCookies = [{ name: 'sid', value: 'test-sid' }];
      
      mockEnsureTHSQuantSession.mockResolvedValue(mockCookies);
      mockCheckLogin.mockResolvedValue({ code: -1, logged: false });

      process.env.THSQUANT_USERNAME = 'testuser';
      process.env.THSQUANT_PASSWORD = 'testpass';

      await import('../list-strategies.js');
      
      expect(mockListStrategies).not.toHaveBeenCalled();
      expect(mockConsoleError).toHaveBeenCalledWith('Error: Not logged in');

      delete process.env.THSQUANT_USERNAME;
      delete process.env.THSQUANT_PASSWORD;
    });

    it('should handle empty strategy list', async () => {
      const mockCookies = [{ name: 'sid', value: 'test-sid' }];
      
      mockEnsureTHSQuantSession.mockResolvedValue(mockCookies);
      mockCheckLogin.mockResolvedValue({ code: 0, logged: true });
      mockListStrategies.mockResolvedValue([]);

      process.env.THSQUANT_USERNAME = 'testuser';
      process.env.THSQUANT_PASSWORD = 'testpass';

      await import('../list-strategies.js');
      
      expect(mockListStrategies).toHaveBeenCalled();
      expect(mockConsoleLog).toHaveBeenCalledWith('No strategies found');

      delete process.env.THSQUANT_USERNAME;
      delete process.env.THSQUANT_PASSWORD;
    });

    it('should handle errors during strategy fetch', async () => {
      mockEnsureTHSQuantSession.mockRejectedValue(new Error('Network error'));

      process.env.THSQUANT_USERNAME = 'testuser';
      process.env.THSQUANT_PASSWORD = 'testpass';

      await import('../list-strategies.js');
      
      expect(mockConsoleError).toHaveBeenCalledWith('Error:', 'Network error');

      delete process.env.THSQUANT_USERNAME;
      delete process.env.THSQUANT_PASSWORD;
    });

    it('should handle missing credentials', async () => {
      mockEnsureTHSQuantSession.mockRejectedValue(new Error('Missing credentials'));

      delete process.env.THSQUANT_USERNAME;
      delete process.env.THSQUANT_PASSWORD;

      await import('../list-strategies.js');
      
      expect(mockConsoleError).toHaveBeenCalled();
    });

    it('should use correct credentials from environment', async () => {
      const mockCookies = [{ name: 'sid', value: 'test-sid' }];
      
      mockEnsureTHSQuantSession.mockResolvedValue(mockCookies);
      mockCheckLogin.mockResolvedValue({ code: 0, logged: true });
      mockListStrategies.mockResolvedValue([]);

      process.env.THSQUANT_USERNAME = 'myuser';
      process.env.THSQUANT_PASSWORD = 'mypass';

      await import('../list-strategies.js');

      expect(mockEnsureTHSQuantSession).toHaveBeenCalledWith({
        username: 'myuser',
        password: 'mypass'
      });

      delete process.env.THSQUANT_USERNAME;
      delete process.env.THSQUANT_PASSWORD;
    });

    it('should display strategy information with correct format', async () => {
      const mockCookies = [{ name: 'sid', value: 'test-sid' }];
      
      mockEnsureTHSQuantSession.mockResolvedValue(mockCookies);
      mockCheckLogin.mockResolvedValue({ code: 0, logged: true });
      mockListStrategies.mockResolvedValue([
        { id: 'algo-1', name: 'Test Strategy' },
        { id: 'algo-2', name: 'Another Strategy' }
      ]);

      process.env.THSQUANT_USERNAME = 'testuser';
      process.env.THSQUANT_PASSWORD = 'testpass';

      await import('../list-strategies.js');

      expect(mockConsoleLog).toHaveBeenCalledWith('Fetching THSQuant strategies...\n');
      expect(mockConsoleLog).toHaveBeenCalledWith('Found 2 strategies:\n');
      expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('ID'));
      expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('Name'));

      delete process.env.THSQUANT_USERNAME;
      delete process.env.THSQUANT_PASSWORD;
    });

    it('should handle strategies with missing id or name', async () => {
      const mockCookies = [{ name: 'sid', value: 'test-sid' }];
      
      mockEnsureTHSQuantSession.mockResolvedValue(mockCookies);
      mockCheckLogin.mockResolvedValue({ code: 0, logged: true });
      mockListStrategies.mockResolvedValue([
        { id: null, name: 'No ID Strategy' },
        { id: 'has-id', name: null }
      ]);

      process.env.THSQUANT_USERNAME = 'testuser';
      process.env.THSQUANT_PASSWORD = 'testpass';

      await import('../list-strategies.js');

      expect(mockListStrategies).toHaveBeenCalled();
      expect(mockConsoleLog).toHaveBeenCalledWith('Found 2 strategies:\n');

      delete process.env.THSQUANT_USERNAME;
      delete process.env.THSQUANT_PASSWORD;
    });
  });
});