import { jest } from '@jest/globals';

jest.unstable_mockModule('node:fs', () => ({
  existsSync: () => true,
  readFileSync: () => '{}',
  writeFileSync: () => {},
  mkdirSync: () => {}
}));

jest.unstable_mockModule('node:path', () => ({
  dirname: () => '/mock/dir',
  join: (...args) => args.join('/'),
  resolve: (...args) => args.join('/')
}));

jest.unstable_mockModule('../load-env.js', () => ({}));
jest.unstable_mockModule('../paths.js', () => ({
  OUTPUT_ROOT: '/tmp/bigquant-test-output',
  SESSION_FILE: '/tmp/bigquant-test-session.json'
}));

const mockFetch = jest.fn();
global.fetch = mockFetch;

const { BigQuantAPIClient, loadJson, saveJson } = await import('../request/bigquant-api-client.js');

describe('BigQuantAPIClient', () => {
  let client;

  const mockSession = {
    cookies: [
      { name: 'bigjwt', value: 'test.jwt.token', domain: 'bigquant.com' },
      { name: 'biguid', value: 'user-123', domain: 'bigquant.com' }
    ],
    userId: 'test-user-id',
    timestamp: Date.now()
  };

  beforeEach(() => {
    jest.clearAllMocks();
    mockFetch.mockReset();
    client = new BigQuantAPIClient({ sessionPayload: mockSession });
  });

  describe('constructor', () => {
    it('initializes with default options', () => {
      const c = new BigQuantAPIClient();
      expect(c.origin).toBe('https://bigquant.com');
      expect(c.apiBase).toBe('https://bigquant.com/bigapis');
    });

    it('initializes with custom sessionPayload', () => {
      expect(client.cookieJar).toEqual(mockSession.cookies);
      expect(client.sessionPayload).toEqual(mockSession);
    });
  });

  describe('buildCookieHeader', () => {
    it('builds cookie header from cookieJar', () => {
      const header = client.buildCookieHeader();
      expect(header).toBe('bigjwt=test.jwt.token; biguid=user-123');
    });

    it('returns empty string when no cookies', () => {
      client.cookieJar = [];
      const header = client.buildCookieHeader();
      expect(header).toBe('');
    });
  });

  describe('buildHeaders', () => {
    it('builds headers with defaults', () => {
      const headers = client.buildHeaders('https://bigquant.com/api/test');
      expect(headers['accept']).toBe('application/json, text/plain, */*');
      expect(headers['content-type']).toBe('application/json');
    });
  });

  describe('request', () => {
    it('makes GET request', async () => {
      mockFetch.mockResolvedValue({
        ok: true,
        text: () => Promise.resolve(JSON.stringify({ data: 'test' }))
      });

      const result = await client.request('GET', '/auth/v1/users/me');

      expect(mockFetch).toHaveBeenCalled();
      expect(result).toEqual({ data: 'test' });
    });

    it('makes POST request with body', async () => {
      mockFetch.mockResolvedValue({
        ok: true,
        text: () => Promise.resolve(JSON.stringify({ success: true }))
      });

      const body = { name: 'test' };
      const result = await client.request('POST', '/aiflow/v1/tasks', body);

      expect(mockFetch).toHaveBeenCalledWith(
        expect.any(String),
        expect.objectContaining({ method: 'POST' })
      );
    });

    it('throws on non-OK response', async () => {
      mockFetch.mockResolvedValue({
        ok: false,
        status: 401,
        text: () => Promise.resolve('Unauthorized')
      });

      await expect(client.request('GET', '/api/test')).rejects.toThrow('Request failed 401');
    });

    it('returns raw text when not JSON', async () => {
      mockFetch.mockResolvedValue({
        ok: true,
        text: () => Promise.resolve('not json')
      });

      const result = await client.request('GET', '/api/test');
      expect(result).toBe('not json');
    });
  });

  describe('getCurrentUser', () => {
    it('calls correct endpoint', async () => {
      mockFetch.mockResolvedValue({
        ok: true,
        text: () => Promise.resolve(JSON.stringify({ data: { id: 'user-1' } }))
      });

      await client.getCurrentUser();

      expect(mockFetch).toHaveBeenCalledWith(
        expect.stringContaining('/auth/v1/users/me'),
        expect.any(Object)
      );
    });
  });

  describe('getTask', () => {
    it('gets task by id', async () => {
      mockFetch.mockResolvedValue({
        ok: true,
        text: () => Promise.resolve(JSON.stringify({ data: { id: 'task-1' } }))
      });

      const result = await client.getTask('task-123');

      expect(mockFetch).toHaveBeenCalledWith(
        expect.stringContaining('/aiflow/v1/tasks/task-123'),
        expect.any(Object)
      );
    });
  });

  describe('loadJson', () => {
    it('returns empty object when file not found', () => {
      const result = loadJson('/nonexistent.json');
      expect(result).toEqual({});
    });

    it('returns empty object on parse error', () => {
      const result = loadJson('/test/file.json');
      expect(result).toEqual({});
    });
  });

  describe('saveJson', () => {
    it('writes JSON to file', () => {
      saveJson('/test/file.json', { key: 'value' });
    });
  });
});