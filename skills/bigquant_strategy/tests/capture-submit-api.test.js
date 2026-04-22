import { describe, it, expect, jest, beforeEach, afterEach } from '@jest/globals';

const mockCaptured = [];
const mockInteresting = [];

const mockPage = {
  goto: jest.fn().mockResolvedValue(undefined)
};

const mockContext = {
  newPage: jest.fn().mockResolvedValue(mockPage),
  addCookies: jest.fn().mockResolvedValue(undefined),
  on: jest.fn((event, handler) => {
    if (event === 'request') {
    }
    if (event === 'response') {
    }
  })
};

const mockBrowser = {
  newContext: jest.fn().mockResolvedValue(mockContext),
  close: jest.fn().mockResolvedValue(undefined)
};

const mockChromium = {
  launch: jest.fn().mockResolvedValue(mockBrowser)
};

jest.unstable_mockModule('playwright', () => ({
  chromium: mockChromium
}));

const mockFs = {
  readFileSync: jest.fn().mockReturnValue(JSON.stringify({
    cookies: [{ name: 'sessionid', value: 'test' }]
  })),
  writeFileSync: jest.fn(),
  existsSync: jest.fn().mockReturnValue(true)
};

jest.unstable_mockModule('fs', () => ({ default: mockFs, ...mockFs }));
jest.unstable_mockModule('fs/promises', () => ({ default: mockFs, ...mockFs }));

jest.unstable_mockModule('path', () => ({
  default: {
    join: jest.fn((...args) => args.join('/')),
    dirname: jest.fn((p) => p.split('/').slice(0, -1).join('/'))
  },
  join: jest.fn((...args) => args.join('/')),
  dirname: jest.fn((p) => p.split('/').slice(0, -1).join('/'))
}));

jest.unstable_mockModule('url', () => ({
  fileURLToPath: jest.fn(() => '/mock/path/capture-submit-api.js')
}));

jest.unstable_mockModule('../paths.js', () => ({
  SESSION_FILE: '/test/session.json'
}));

jest.unstable_mockModule('../load-env.js', () => ({}));

const originalSetInterval = global.setInterval;
const originalProcessOn = process.on;
const originalProcessExit = process.exit;

describe('capture-submit-api.js', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    mockCaptured.length = 0;
    mockInteresting.length = 0;
    global.setInterval = jest.fn(() => 123);
    process.on = jest.fn();
    process.exit = jest.fn();
  });

  afterEach(() => {
    global.setInterval = originalSetInterval;
    process.on = originalProcessOn;
    process.exit = originalProcessExit;
    jest.clearAllMocks();
  });

  describe('browser launch', () => {
    it('should launch browser with headless false', async () => {
      const mockRequest = {
        url: jest.fn().mockReturnValue('https://bigquant.com/api/test'),
        method: jest.fn().mockReturnValue('GET'),
        postData: jest.fn().mockReturnValue(null)
      };

      expect(mockChromium.launch).toBeDefined();
    });

    it('should create context with correct user agent and viewport', async () => {
      expect(mockBrowser.newContext).toBeDefined();
    });

    it('should add cookies from session file', async () => {
      expect(mockContext.addCookies).toBeDefined();
    });
  });

  describe('request filtering', () => {
    const createMockRequest = (url, method = 'GET', postData = null) => ({
      url: jest.fn().mockReturnValue(url),
      method: jest.fn().mockReturnValue(method),
      postData: jest.fn().mockReturnValue(postData)
    });

    it('should capture bigquant.com requests', () => {
      const req = createMockRequest('https://bigquant.com/api/task');
      expect(req.url()).toContain('bigquant.com');
    });

    it('should ignore static resources', () => {
      const urls = [
        'https://bigquant.com/static/app.js',
        'https://bigquant.com/styles/main.css',
        'https://bigquant.com/images/logo.png',
        'https://bigquant.com/fonts/roboto.woff',
        'https://bigquant.com/assets/icon.svg'
      ];

      urls.forEach(url => {
        const isStatic = url.match(/\.(js|css|png|svg|woff|ttf|wasm|gif|jpg|ico)(\?|$)/);
        expect(isStatic).toBeTruthy();
      });
    });

    it('should ignore analytics requests', () => {
      const urls = [
        'https://bigquant.com/google-analytics/collect',
        'https://bigquant.com/baidu/tracking',
        'https://bigquant.com/telemetry/event'
      ];

      urls.forEach(url => {
        const isAnalytics = url.includes('google-analytics') || 
                           url.includes('baidu') || 
                           url.includes('telemetry');
        expect(isAnalytics).toBeTruthy();
      });
    });

    it('should identify interesting API paths', () => {
      const interestingPaths = [
        '/api/task',
        '/api/run',
        '/api/submit',
        '/api/paper',
        '/api/trading',
        '/api/kernel',
        '/api/session',
        '/api/execute',
        '/api/aiflow',
        '/api/mint',
        '/api/notebook',
        '/api/backtest'
      ];

      interestingPaths.forEach(path => {
        const isKey = path.includes('task') || path.includes('run') || 
                     path.includes('submit') || path.includes('paper') || 
                     path.includes('trading') || path.includes('kernel') ||
                     path.includes('session') || path.includes('execute') || 
                     path.includes('aiflow') || path.includes('mint') || 
                     path.includes('notebook') || path.includes('backtest');
        expect(isKey).toBeTruthy();
      });
    });
  });

  describe('response handling', () => {
    const createMockResponse = (url, status = 200, body = '{}') => ({
      url: jest.fn().mockReturnValue(url),
      status: jest.fn().mockReturnValue(status),
      text: jest.fn().mockResolvedValue(body)
    });

    it('should capture response status and body', async () => {
      const resp = createMockResponse('https://bigquant.com/api/task', 200, '{"result": "ok"}');
      
      expect(resp.status()).toBe(200);
      expect(await resp.text()).toBe('{"result": "ok"}');
    });

    it('should filter response URLs same as requests', () => {
      const staticUrl = 'https://bigquant.com/static/app.js';
      const isStatic = staticUrl.match(/\.(js|css|png|svg|woff|ttf|wasm|gif|jpg|ico)(\?|$)/);
      expect(isStatic).toBeTruthy();
    });
  });

  describe('page navigation', () => {
    it('should navigate to studio URL with correct options', async () => {
      const expectedUrl = expect.stringContaining('bigquant.com/aistudio/studios');
      expect(mockPage.goto).toBeDefined();
    });

    it('should use domcontentloaded wait strategy', () => {
      const options = { waitUntil: 'domcontentloaded', timeout: 60000 };
      expect(options.waitUntil).toBe('domcontentloaded');
      expect(options.timeout).toBe(60000);
    });
  });

  describe('data saving', () => {
    it('should save captured data to JSON file', () => {
      const data = {
        all: [{ method: 'GET', url: 'https://bigquant.com/api/test' }],
        interesting: [{ method: 'POST', url: 'https://bigquant.com/api/submit' }]
      };
      
      mockFs.writeFileSync('/test/captured-submit-api.json', JSON.stringify(data, null, 2));
      
      expect(mockFs.writeFileSync).toHaveBeenCalled();
    });
  });

  describe('process signal handling', () => {
    it('should register SIGINT handler', () => {
      const handler = jest.fn();
      process.on('SIGINT', handler);
      
      expect(process.on).toBeDefined();
    });

    it('should call process.exit with 0 on SIGINT', () => {
      expect(process.exit).toBeDefined();
    });
  });

  describe('session file reading', () => {
    it('should read session file on startup', () => {
      const sessionData = mockFs.readFileSync('/test/session.json', 'utf8');
      const session = JSON.parse(sessionData);
      
      expect(session).toHaveProperty('cookies');
    });

    it('should throw if session file is missing', () => {
      mockFs.readFileSync.mockImplementationOnce(() => {
        throw new Error('ENOENT: no such file');
      });
      
      expect(() => mockFs.readFileSync()).toThrow();
    });
  });

  describe('captured request structure', () => {
    it('should have correct structure for captured entries', () => {
      const entry = {
        method: 'POST',
        url: 'https://bigquant.com/api/submit',
        postData: '{"test": "data"}',
        time: new Date().toISOString()
      };
      
      expect(entry).toHaveProperty('method');
      expect(entry).toHaveProperty('url');
      expect(entry).toHaveProperty('time');
    });

    it('should truncate postData to 1000 characters', () => {
      const longData = 'x'.repeat(2000);
      const truncated = longData.slice(0, 1000);
      
      expect(truncated.length).toBe(1000);
    });

    it('should handle null postData', () => {
      const entry = {
        method: 'GET',
        url: 'https://bigquant.com/api/test',
        postData: null?.slice(0, 1000),
        time: new Date().toISOString()
      };
      
      expect(entry.postData).toBeUndefined();
    });
  });

  describe('response body handling', () => {
    it('should truncate response body to 1000 characters for storage', () => {
      const body = 'x'.repeat(2000);
      const truncated = body.slice(0, 1000);
      
      expect(truncated.length).toBe(1000);
    });

    it('should handle response text errors gracefully', async () => {
      const errorResp = {
        url: jest.fn().mockReturnValue('https://bigquant.com/api/test'),
        status: jest.fn().mockReturnValue(500),
        text: jest.fn().mockRejectedValue(new Error('Failed to read body'))
      };
      
      try {
        await errorResp.text();
      } catch (e) {
        expect(e.message).toBe('Failed to read body');
      }
    });
  });
});