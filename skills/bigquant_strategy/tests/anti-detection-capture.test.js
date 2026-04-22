import { describe, it, expect, jest, beforeEach, afterEach } from '@jest/globals';

const mockBrowser = {
  newContext: jest.fn(),
  close: jest.fn().mockResolvedValue(undefined)
};

const mockContext = {
  newPage: jest.fn(),
  cookies: jest.fn().mockResolvedValue([]),
  addCookies: jest.fn().mockResolvedValue(undefined)
};

const mockPage = {
  goto: jest.fn().mockResolvedValue(undefined),
  waitForFunction: jest.fn().mockResolvedValue(undefined),
  evaluate: jest.fn().mockResolvedValue('Mozilla/5.0'),
  addInitScript: jest.fn().mockResolvedValue(undefined),
  setExtraHTTPHeaders: jest.fn().mockResolvedValue(undefined),
  mouse: {
    move: jest.fn().mockResolvedValue(undefined)
  }
};

const mockAntiDetection = {
  setupBrowser: jest.fn().mockResolvedValue(mockBrowser),
  injectAntiDetection: jest.fn().mockResolvedValue(undefined),
  setRealisticHeaders: jest.fn().mockResolvedValue(undefined),
  simulateHumanBehavior: jest.fn().mockResolvedValue(undefined),
  randomDelay: jest.fn().mockResolvedValue(undefined),
  getRandomUserAgent: jest.fn().mockReturnValue('Mozilla/5.0 Test')
};

const mockSessionManager = {
  isValid: jest.fn().mockResolvedValue(false),
  load: jest.fn().mockResolvedValue(null),
  save: jest.fn().mockResolvedValue(undefined)
};

jest.unstable_mockModule('../lib/anti-detection.js', () => ({
  AntiDetection: mockAntiDetection,
  SessionManager: jest.fn(() => mockSessionManager)
}));

jest.unstable_mockModule('path', () => ({
  default: {
    join: jest.fn((...args) => args.join('/')),
    dirname: jest.fn((p) => p.split('/').slice(0, -1).join('/'))
  },
  join: jest.fn((...args) => args.join('/')),
  dirname: jest.fn((p) => p.split('/').slice(0, -1).join('/'))
}));

jest.unstable_mockModule('url', () => ({
  fileURLToPath: jest.fn(() => '/mock/path/anti-detection-capture.js')
}));

let antiDetectionCapture;

describe('anti-detection-capture.js', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    mockContext.newPage.mockResolvedValue(mockPage);
    mockBrowser.newContext.mockResolvedValue(mockContext);
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  describe('captureSessionWithAntiDetection', () => {
    it('should return existing session when valid', async () => {
      const existingSession = {
        cookies: [{ name: 'test', value: 'value' }],
        localStorage: {},
        userAgent: 'TestAgent'
      };
      
      mockSessionManager.isValid.mockResolvedValueOnce(true);
      mockSessionManager.load.mockResolvedValueOnce(existingSession);
      
      const { captureSessionWithAntiDetection } = await import('../browser/anti-detection-capture.js');
      const result = await captureSessionWithAntiDetection();
      
      expect(result).toEqual(existingSession);
    });

    it('should create browser with headless false for manual login', async () => {
      mockSessionManager.isValid.mockResolvedValueOnce(false);
      mockPage.waitForFunction.mockResolvedValueOnce(undefined);
      mockPage.evaluate.mockResolvedValueOnce('TestUserAgent');
      mockContext.cookies.mockResolvedValueOnce([{ name: 'sessionid', value: 'test' }]);
      
      const { captureSessionWithAntiDetection } = await import('../browser/anti-detection-capture.js');
      
      await captureSessionWithAntiDetection();
      
      expect(mockAntiDetection.setupBrowser).toHaveBeenCalledWith(
        expect.objectContaining({ headless: false })
      );
    });

    it('should inject anti-detection scripts', async () => {
      mockSessionManager.isValid.mockResolvedValueOnce(false);
      mockPage.waitForFunction.mockResolvedValueOnce(undefined);
      mockPage.evaluate.mockResolvedValueOnce('TestUserAgent');
      mockContext.cookies.mockResolvedValueOnce([{ name: 'sessionid', value: 'test' }]);
      
      const { captureSessionWithAntiDetection } = await import('../browser/anti-detection-capture.js');
      
      await captureSessionWithAntiDetection();
      
      expect(mockAntiDetection.injectAntiDetection).toHaveBeenCalled();
    });

    it('should set realistic headers with BigQuant URL', async () => {
      mockSessionManager.isValid.mockResolvedValueOnce(false);
      mockPage.waitForFunction.mockResolvedValueOnce(undefined);
      mockPage.evaluate.mockResolvedValueOnce('TestUserAgent');
      mockContext.cookies.mockResolvedValueOnce([{ name: 'sessionid', value: 'test' }]);
      
      const { captureSessionWithAntiDetection } = await import('../browser/anti-detection-capture.js');
      
      await captureSessionWithAntiDetection();
      
      expect(mockAntiDetection.setRealisticHeaders).toHaveBeenCalledWith(
        mockPage,
        expect.objectContaining({
          Referer: 'https://bigquant.com',
          Origin: 'https://bigquant.com'
        })
      );
    });

    it('should navigate to BigQuant homepage', async () => {
      mockSessionManager.isValid.mockResolvedValueOnce(false);
      mockPage.waitForFunction.mockResolvedValueOnce(undefined);
      mockPage.evaluate.mockResolvedValueOnce('TestUserAgent');
      mockContext.cookies.mockResolvedValueOnce([{ name: 'sessionid', value: 'test' }]);
      
      const { captureSessionWithAntiDetection } = await import('../browser/anti-detection-capture.js');
      
      await captureSessionWithAntiDetection();
      
      expect(mockPage.goto).toHaveBeenCalledWith(
        'https://bigquant.com',
        { waitUntil: 'networkidle' }
      );
    });

    it('should simulate human behavior', async () => {
      mockSessionManager.isValid.mockResolvedValueOnce(false);
      mockPage.waitForFunction.mockResolvedValueOnce(undefined);
      mockPage.evaluate.mockResolvedValueOnce('TestUserAgent');
      mockContext.cookies.mockResolvedValueOnce([{ name: 'sessionid', value: 'test' }]);
      
      const { captureSessionWithAntiDetection } = await import('../browser/anti-detection-capture.js');
      
      await captureSessionWithAntiDetection();
      
      expect(mockAntiDetection.simulateHumanBehavior).toHaveBeenCalled();
    });

    it('should capture cookies and localStorage', async () => {
      const expectedCookies = [{ name: 'sessionid', value: 'test123' }];
      const expectedLocalStorage = { token: 'abc' };
      
      mockSessionManager.isValid.mockResolvedValueOnce(false);
      mockPage.waitForFunction.mockResolvedValueOnce(undefined);
      mockContext.cookies.mockResolvedValueOnce(expectedCookies);
      mockPage.evaluate.mockImplementation((fn) => {
        if (typeof fn === 'string' && fn.includes('navigator')) {
          return Promise.resolve('TestUserAgent');
        }
        if (typeof fn === 'function') {
          return Promise.resolve(expectedLocalStorage);
        }
        return Promise.resolve('TestUserAgent');
      });
      
      const { captureSessionWithAntiDetection } = await import('../browser/anti-detection-capture.js');
      const result = await captureSessionWithAntiDetection();
      
      expect(result.cookies).toEqual(expectedCookies);
    });

    it('should save session after capture', async () => {
      mockSessionManager.isValid.mockResolvedValueOnce(false);
      mockPage.waitForFunction.mockResolvedValueOnce(undefined);
      mockPage.evaluate.mockResolvedValueOnce('TestUserAgent');
      mockContext.cookies.mockResolvedValueOnce([{ name: 'sessionid', value: 'test' }]);
      
      const { captureSessionWithAntiDetection } = await import('../browser/anti-detection-capture.js');
      
      await captureSessionWithAntiDetection();
      
      expect(mockSessionManager.save).toHaveBeenCalled();
    });

    it('should close browser after capture', async () => {
      mockSessionManager.isValid.mockResolvedValueOnce(false);
      mockPage.waitForFunction.mockResolvedValueOnce(undefined);
      mockPage.evaluate.mockResolvedValueOnce('TestUserAgent');
      mockContext.cookies.mockResolvedValueOnce([{ name: 'sessionid', value: 'test' }]);
      
      const { captureSessionWithAntiDetection } = await import('../browser/anti-detection-capture.js');
      
      await captureSessionWithAntiDetection();
      
      expect(mockBrowser.close).toHaveBeenCalled();
    });

    it('should close browser even on error', async () => {
      mockSessionManager.isValid.mockResolvedValueOnce(false);
      mockPage.goto.mockRejectedValueOnce(new Error('Navigation failed'));
      
      const { captureSessionWithAntiDetection } = await import('../browser/anti-detection-capture.js');
      
      await expect(captureSessionWithAntiDetection()).rejects.toThrow();
      expect(mockBrowser.close).toHaveBeenCalled();
    });

    it('should include capturedAt timestamp in session', async () => {
      mockSessionManager.isValid.mockResolvedValueOnce(false);
      mockPage.waitForFunction.mockResolvedValueOnce(undefined);
      mockPage.evaluate.mockResolvedValueOnce('TestUserAgent');
      mockContext.cookies.mockResolvedValueOnce([{ name: 'sessionid', value: 'test' }]);
      
      const { captureSessionWithAntiDetection } = await import('../browser/anti-detection-capture.js');
      const result = await captureSessionWithAntiDetection();
      
      expect(result.capturedAt).toBeDefined();
      expect(new Date(result.capturedAt)).toBeInstanceOf(Date);
    });
  });

  describe('createPageWithSession', () => {
    it('should throw error when no session found', async () => {
      mockSessionManager.load.mockResolvedValueOnce(null);
      
      const { createPageWithSession } = await import('../browser/anti-detection-capture.js');
      
      await expect(createPageWithSession(mockBrowser)).rejects.toThrow('No session found');
    });

    it('should create context with session user agent', async () => {
      const session = {
        cookies: [{ name: 'test', value: 'value' }],
        userAgent: 'CustomAgent/1.0'
      };
      
      mockSessionManager.load.mockResolvedValueOnce(session);
      mockBrowser.newContext.mockResolvedValueOnce(mockContext);
      mockContext.newPage.mockResolvedValueOnce(mockPage);
      
      const { createPageWithSession } = await import('../browser/anti-detection-capture.js');
      
      await createPageWithSession(mockBrowser);
      
      expect(mockBrowser.newContext).toHaveBeenCalledWith(
        expect.objectContaining({
          userAgent: 'CustomAgent/1.0'
        })
      );
    });

    it('should add cookies to context', async () => {
      const session = {
        cookies: [{ name: 'test', value: 'value' }],
        userAgent: 'Agent'
      };
      
      mockSessionManager.load.mockResolvedValueOnce(session);
      mockBrowser.newContext.mockResolvedValueOnce(mockContext);
      mockContext.newPage.mockResolvedValueOnce(mockPage);
      
      const { createPageWithSession } = await import('../browser/anti-detection-capture.js');
      
      await createPageWithSession(mockBrowser);
      
      expect(mockContext.addCookies).toHaveBeenCalledWith(session.cookies);
    });

    it('should restore localStorage if present', async () => {
      const session = {
        cookies: [{ name: 'test', value: 'value' }],
        localStorage: { token: 'abc123' },
        userAgent: 'Agent'
      };
      
      mockSessionManager.load.mockResolvedValueOnce(session);
      mockBrowser.newContext.mockResolvedValueOnce(mockContext);
      mockContext.newPage.mockResolvedValueOnce(mockPage);
      
      const { createPageWithSession } = await import('../browser/anti-detection-capture.js');
      
      await createPageWithSession(mockBrowser);
      
      expect(mockPage.addInitScript).toHaveBeenCalled();
    });

    it('should inject anti-detection on page', async () => {
      const session = {
        cookies: [{ name: 'test', value: 'value' }],
        userAgent: 'Agent'
      };
      
      mockSessionManager.load.mockResolvedValueOnce(session);
      mockBrowser.newContext.mockResolvedValueOnce(mockContext);
      mockContext.newPage.mockResolvedValueOnce(mockPage);
      
      const { createPageWithSession } = await import('../browser/anti-detection-capture.js');
      
      await createPageWithSession(mockBrowser);
      
      expect(mockAntiDetection.injectAntiDetection).toHaveBeenCalledWith(mockPage);
    });

    it('should return page and context', async () => {
      const session = {
        cookies: [{ name: 'test', value: 'value' }],
        userAgent: 'Agent'
      };
      
      mockSessionManager.load.mockResolvedValueOnce(session);
      mockBrowser.newContext.mockResolvedValueOnce(mockContext);
      mockContext.newPage.mockResolvedValueOnce(mockPage);
      
      const { createPageWithSession } = await import('../browser/anti-detection-capture.js');
      const result = await createPageWithSession(mockBrowser);
      
      expect(result).toHaveProperty('page');
      expect(result).toHaveProperty('context');
    });
  });

  describe('SESSION_FILE export', () => {
    it('should export SESSION_FILE path', async () => {
      const { SESSION_FILE } = await import('../browser/anti-detection-capture.js');
      
      expect(SESSION_FILE).toBeDefined();
      expect(typeof SESSION_FILE).toBe('string');
      expect(SESSION_FILE).toContain('session.json');
    });
  });
});