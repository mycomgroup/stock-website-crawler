import { jest } from '@jest/globals';

jest.unstable_mockModule('node:fs', () => ({
  existsSync: () => true,
  readFileSync: () => '{}',
  writeFileSync: () => {},
  mkdirSync: () => {},
  default: { existsSync: () => true, readFileSync: () => '{}', writeFileSync: () => {}, mkdirSync: () => {} }
}));

jest.unstable_mockModule('node:path', () => ({
  dirname: () => '/mock/dir',
  join: (...args) => args.join('/'),
  default: { dirname: () => '/mock/dir', join: (...args) => args.join('/') }
}));

jest.unstable_mockModule('../../common/http-security.js', () => ({
  USER_AGENT: 'test-user-agent',
  SEC_CH_UA: 'test-sec-ch-ua',
  SecureHttpClient: class MockSecureHttpClient {
    constructor(options) {
      this.baseUrl = options.baseUrl || '';
      this.maxRequestsPerMinute = options.maxRequestsPerMinute || 10;
    }
    async request(url, options) {
      this._lastRequest = { url, options };
      return '{}';
    }
  }
}), { virtual: true });

jest.unstable_mockModule('../request/bigquant-auth.js', () => ({
  extractUserId: (session) => session.userId || null
}));

jest.unstable_mockModule('../load-env.js', () => ({}));
jest.unstable_mockModule('../paths.js', () => ({
  OUTPUT_ROOT: '/mocked/output/root'
}), { virtual: true });

const { BigQuantClient } = await import('../request/bigquant-client.js');

describe('BigQuantClient', () => {
  let client;
  let mockSession;

  beforeEach(() => {
    jest.clearAllMocks();

    mockSession = {
      cookies: [
        { name: 'bigjwt', value: 'test-jwt-token', domain: '.bigquant.com' },
        { name: 'sessionid', value: 'test-session-id', domain: 'bigquant.com' }
      ],
      userId: 'test-user-123'
    };

    client = new BigQuantClient(mockSession);
  });

  describe('constructor', () => {
    it('should initialize with session data', () => {
      expect(client.session).toBe(mockSession);
      expect(client.userId).toBe('test-user-123');
      expect(client.outputRoot).toBe('/mocked/output/root');
    });

    it('should use custom options when provided', () => {
      const customClient = new BigQuantClient(mockSession, {
        studioId: 'custom-studio-id',
        outputRoot: '/custom/output',
        resourceSpecId: 'custom-resource-id'
      });

      expect(customClient.studioId).toBe('custom-studio-id');
      expect(customClient.outputRoot).toBe('/custom/output');
    });

    it('should filter cookies by domain containing bigquant.com', () => {
      expect(client.cookieHeader).toContain('bigjwt');
      expect(client.cookieHeader).toContain('sessionid');
    });
  });

  describe('buildHeaders', () => {
    it('should return headers with default values', () => {
      const headers = client.buildHeaders();

      expect(headers).toHaveProperty('User-Agent');
      expect(headers).toHaveProperty('Accept');
      expect(headers).toHaveProperty('Content-Type');
      expect(headers).toHaveProperty('Cookie');
    });

    it('should merge extra headers', () => {
      const headers = client.buildHeaders({ 'X-Custom-Header': 'custom-value' });
      expect(headers['X-Custom-Header']).toBe('custom-value');
    });
  });

  describe('buildNotebook', () => {
    it('should build notebook with single line code', () => {
      const code = 'print("hello")';
      const notebook = client.buildNotebook(code);

      expect(notebook.metadata.kernelspec.name).toBe('python3');
      expect(notebook.nbformat).toBe(4);
      expect(notebook.cells).toHaveLength(1);
      expect(notebook.cells[0].cell_type).toBe('code');
    });

    it('should build notebook with multi-line code', () => {
      const code = 'line1\nline2\nline3';
      const notebook = client.buildNotebook(code);

      expect(notebook.cells[0].source).toEqual(['line1\n', 'line2\n', 'line3']);
    });

    it('should build notebook with empty code', () => {
      const code = '';
      const notebook = client.buildNotebook(code);

      expect(notebook.cells[0].source).toEqual(['']);
    });

    it('should have correct notebook structure', () => {
      const notebook = client.buildNotebook('test');

      expect(notebook).toHaveProperty('metadata');
      expect(notebook).toHaveProperty('nbformat', 4);
      expect(notebook).toHaveProperty('nbformat_minor', 4);
      expect(notebook.cells[0]).toHaveProperty('execution_count', null);
      expect(notebook.cells[0]).toHaveProperty('metadata');
      expect(notebook.cells[0]).toHaveProperty('outputs');
    });
  });

  describe('sleep', () => {
    beforeEach(() => {
      jest.useFakeTimers();
    });

    afterEach(() => {
      jest.useRealTimers();
    });

    it('should resolve after specified time', async () => {
      const sleepPromise = client.sleep(1000);
      jest.advanceTimersByTime(1000);
      await expect(sleepPromise).resolves.toBeUndefined();
    });
  });

  describe('request', () => {
    it('should handle full URL without prepending origin', async () => {
      client.secureClient.request = jest.fn().mockResolvedValue('{}');

      await client.request('GET', 'https://other.com/api/test');

      expect(client.secureClient.request).toHaveBeenCalledWith(
        'https://other.com/api/test',
        expect.any(Object)
      );
    });
  });

  describe('getLogs', () => {
    it('should return empty array when no logs', async () => {
      client.secureClient.request = jest.fn().mockResolvedValue('{}');

      const result = await client.getLogs('run-123');

      expect(result).toEqual([]);
    });
  });

  describe('getNotebookOutputs', () => {
    it('should return empty array when no code', async () => {
      client.secureClient.request = jest.fn().mockResolvedValue(JSON.stringify({ data: {} }));

      const result = await client.getNotebookOutputs('task-123');

      expect(result).toEqual([]);
    });

    it('should return empty array when code is invalid JSON', async () => {
      client.secureClient.request = jest.fn().mockResolvedValue(JSON.stringify({
        data: { data: { code: 'invalid json' } }
      }));

      const result = await client.getNotebookOutputs('task-123');

      expect(result).toEqual([]);
    });
  });

  describe('activateStudio', () => {
    it('should handle undefined response data', async () => {
      client.secureClient.request = jest.fn().mockResolvedValue('{}');

      const result = await client.activateStudio();

      expect(result).toBeUndefined();
    });

    it('should handle activation failure gracefully', async () => {
      client.secureClient.request = jest.fn().mockRejectedValue(new Error('Studio already active'));

      const result = await client.activateStudio();

      expect(result).toBeUndefined();
    });
  });

  describe('writeArtifact', () => {
    it('should return file path', () => {
      const result = client.writeArtifact('test', {}, 'json');

      expect(result).toContain('test-');
      expect(result).toContain('.json');
    });
  });
});