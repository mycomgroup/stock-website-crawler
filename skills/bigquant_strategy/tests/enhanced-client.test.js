import { jest } from '@jest/globals';

jest.unstable_mockModule('../lib/anti-detection.js', () => ({
  AntiDetection: {
    createRealisticHeaders: jest.fn((headers) => ({
      'User-Agent': 'test-user-agent',
      'Accept': 'application/json, text/plain, */*',
      'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
      ...headers
    })),
    fetchWithRetry: jest.fn(),
    randomDelay: jest.fn()
  },
  SessionManager: jest.fn(),
  RateLimiter: jest.fn()
}));

const { AntiDetection, SessionManager, RateLimiter } = await import('../lib/anti-detection.js');
const { EnhancedBigQuantClient } = await import('../request/enhanced-client.js');

const mockSession = {
  cookies: [
    { name: 'session_id', value: 'test-session-123' },
    { name: 'csrf_token', value: 'test-csrf-456' }
  ],
  capturedAt: new Date().toISOString()
};

const createMockResponse = (data, options = {}) => {
  const response = {
    ok: options.ok !== undefined ? options.ok : true,
    status: options.status || 200,
    statusText: options.statusText || 'OK',
    json: jest.fn().mockResolvedValue(data)
  };
  return response;
};

describe('EnhancedBigQuantClient', () => {
  let client;
  let mockSessionManager;
  let mockLimiter;

  beforeEach(() => {
    jest.clearAllMocks();

    mockSessionManager = {
      isValid: jest.fn().mockResolvedValue(true),
      load: jest.fn().mockResolvedValue(mockSession),
      clear: jest.fn().mockResolvedValue(undefined),
      save: jest.fn().mockResolvedValue(undefined)
    };

    mockLimiter = {
      wait: jest.fn().mockResolvedValue(undefined)
    };

    SessionManager.mockImplementation(() => mockSessionManager);
    RateLimiter.mockImplementation(() => mockLimiter);

    global.fetch = jest.fn();

    client = new EnhancedBigQuantClient();
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  describe('constructor', () => {
    it('should initialize with default options', () => {
      expect(SessionManager).toHaveBeenCalledWith(
        expect.stringContaining('session.json'),
        expect.objectContaining({
          maxAge: 7 * 24 * 60 * 60 * 1000
        })
      );
      expect(RateLimiter).toHaveBeenCalledWith({
        minDelay: 1000,
        maxDelay: 3000
      });
      expect(client.session).toBeNull();
    });

    it('should initialize with custom options', () => {
      const customClient = new EnhancedBigQuantClient({
        baseURL: 'https://custom.bigquant.com',
        sessionMaxAge: 1000,
        minDelay: 500,
        maxDelay: 1000,
        maxRetries: 5,
        retryDelay: 3000
      });

      expect(customClient.baseURL).toBe('https://custom.bigquant.com');
      expect(customClient.retryOptions.maxRetries).toBe(5);
      expect(customClient.retryOptions.retryDelay).toBe(3000);
    });
  });

  describe('init', () => {
    it('should initialize successfully with valid session', async () => {
      await client.init();

      expect(mockSessionManager.isValid).toHaveBeenCalled();
      expect(mockSessionManager.load).toHaveBeenCalled();
      expect(client.session).toEqual(mockSession);
    });

    it('should throw error when no valid session', async () => {
      mockSessionManager.isValid.mockResolvedValue(false);

      await expect(client.init()).rejects.toThrow(
        'No valid session found. Please run anti-detection-capture.js first.'
      );
    });
  });

  describe('getHeaders', () => {
    it('should throw error when client not initialized', () => {
      expect(() => client.getHeaders()).toThrow('Client not initialized. Call init() first.');
    });

    it('should return headers with cookies', async () => {
      await client.init();

      const headers = client.getHeaders();

      expect(headers['Cookie']).toBe('session_id=test-session-123; csrf_token=test-csrf-456');
      expect(headers['Referer']).toBe('https://bigquant.com');
      expect(headers['Origin']).toBe('https://bigquant.com');
      expect(AntiDetection.createRealisticHeaders).toHaveBeenCalled();
    });

    it('should merge custom headers', async () => {
      await client.init();

      const headers = client.getHeaders({
        'X-Custom-Header': 'custom-value',
        'Authorization': 'Bearer token'
      });

      expect(headers['X-Custom-Header']).toBe('custom-value');
      expect(headers['Authorization']).toBe('Bearer token');
    });
  });

  describe('request', () => {
    beforeEach(async () => {
      await client.init();
    });

    it('should make GET request with full URL', async () => {
      const mockResponse = createMockResponse({ success: true });
      AntiDetection.fetchWithRetry.mockResolvedValue(mockResponse);

      const response = await client.request('https://external.api/data');

      expect(mockLimiter.wait).toHaveBeenCalled();
      expect(AntiDetection.fetchWithRetry).toHaveBeenCalled();
      expect(response).toBe(mockResponse);
    });

    it('should make request with relative endpoint', async () => {
      const mockResponse = createMockResponse({ data: 'test' });
      AntiDetection.fetchWithRetry.mockResolvedValue(mockResponse);

      await client.request('/api/test');

      const fetchFn = AntiDetection.fetchWithRetry.mock.calls[0][0];
      const fetchCallArg = await fetchFn();

      expect(fetch).toHaveBeenCalledWith(
        'https://bigquant.com/api/test',
        expect.objectContaining({
          headers: expect.any(Object)
        })
      );
    });

    it('should call limiter.wait before request', async () => {
      const mockResponse = createMockResponse({});
      AntiDetection.fetchWithRetry.mockResolvedValue(mockResponse);

      await client.request('/api/test');

      expect(mockLimiter.wait).toHaveBeenCalled();
    });

    it('should clear session and throw on 401 response', async () => {
      const mockResponse = createMockResponse({}, { status: 401 });
      AntiDetection.fetchWithRetry.mockResolvedValue(mockResponse);

      await expect(client.request('/api/test')).rejects.toThrow(
        'Session invalid. Please re-capture session.'
      );
      expect(mockSessionManager.clear).toHaveBeenCalled();
    });

    it('should clear session and throw on 403 response', async () => {
      const mockResponse = createMockResponse({}, { status: 403 });
      AntiDetection.fetchWithRetry.mockResolvedValue(mockResponse);

      await expect(client.request('/api/test')).rejects.toThrow(
        'Session invalid. Please re-capture session.'
      );
      expect(mockSessionManager.clear).toHaveBeenCalled();
    });

    it('should pass retry options to fetchWithRetry', async () => {
      const customClient = new EnhancedBigQuantClient({
        maxRetries: 5,
        retryDelay: 3000
      });
      await customClient.init();

      const mockResponse = createMockResponse({});
      AntiDetection.fetchWithRetry.mockResolvedValue(mockResponse);

      await customClient.request('/api/test');

      expect(AntiDetection.fetchWithRetry).toHaveBeenCalledWith(
        expect.any(Function),
        expect.objectContaining({
          maxRetries: 5,
          retryDelay: 3000,
          backoff: true
        })
      );
    });
  });

  describe('HTTP Methods', () => {
    beforeEach(async () => {
      await client.init();
    });

    describe('get', () => {
      it('should make GET request and return JSON', async () => {
        const mockData = { id: 1, name: 'test' };
        const mockResponse = createMockResponse(mockData);
        AntiDetection.fetchWithRetry.mockResolvedValue(mockResponse);

        const result = await client.get('/api/test');

        expect(result).toEqual(mockData);
        expect(mockResponse.json).toHaveBeenCalled();
      });

      it('should append query params to URL', async () => {
        const mockResponse = createMockResponse({});
        AntiDetection.fetchWithRetry.mockResolvedValue(mockResponse);

        await client.get('/api/test', { page: 1, limit: 10 });

        const fetchFn = AntiDetection.fetchWithRetry.mock.calls[0][0];
        await fetchFn();

        expect(fetch).toHaveBeenCalledWith(
          'https://bigquant.com/api/test?page=1&limit=10',
          expect.objectContaining({ method: 'GET' })
        );
      });

      it('should not append query string when params empty', async () => {
        const mockResponse = createMockResponse({});
        AntiDetection.fetchWithRetry.mockResolvedValue(mockResponse);

        await client.get('/api/test', {});

        const fetchFn = AntiDetection.fetchWithRetry.mock.calls[0][0];
        await fetchFn();

        expect(fetch).toHaveBeenCalledWith(
          'https://bigquant.com/api/test',
          expect.any(Object)
        );
      });
    });

    describe('post', () => {
      it('should make POST request with JSON body', async () => {
        const mockData = { result: 'created' };
        const mockResponse = createMockResponse(mockData);
        AntiDetection.fetchWithRetry.mockResolvedValue(mockResponse);

        const result = await client.post('/api/test', { name: 'test' });

        expect(result).toEqual(mockData);
        const fetchFn = AntiDetection.fetchWithRetry.mock.calls[0][0];
        await fetchFn();

        expect(fetch).toHaveBeenCalledWith(
          'https://bigquant.com/api/test',
          expect.objectContaining({
            method: 'POST',
            body: JSON.stringify({ name: 'test' })
          })
        );
      });

      it('should merge custom headers', async () => {
        const mockResponse = createMockResponse({});
        AntiDetection.fetchWithRetry.mockResolvedValue(mockResponse);

        await client.post('/api/test', { data: 1 }, { headers: { 'X-Custom': 'value' } });

        const fetchFn = AntiDetection.fetchWithRetry.mock.calls[0][0];
        await fetchFn();

        expect(fetch).toHaveBeenCalledWith(
          expect.any(String),
          expect.objectContaining({
            headers: expect.objectContaining({
              'X-Custom': 'value',
              'Content-Type': 'application/json'
            })
          })
        );
      });
    });

    describe('put', () => {
      it('should make PUT request with JSON body', async () => {
        const mockData = { result: 'updated' };
        const mockResponse = createMockResponse(mockData);
        AntiDetection.fetchWithRetry.mockResolvedValue(mockResponse);

        const result = await client.put('/api/test/1', { name: 'updated' });

        expect(result).toEqual(mockData);
        const fetchFn = AntiDetection.fetchWithRetry.mock.calls[0][0];
        await fetchFn();

        expect(fetch).toHaveBeenCalledWith(
          'https://bigquant.com/api/test/1',
          expect.objectContaining({
            method: 'PUT',
            body: JSON.stringify({ name: 'updated' })
          })
        );
      });
    });

    describe('delete', () => {
      it('should make DELETE request', async () => {
        const mockData = { result: 'deleted' };
        const mockResponse = createMockResponse(mockData);
        AntiDetection.fetchWithRetry.mockResolvedValue(mockResponse);

        const result = await client.delete('/api/test/1');

        expect(result).toEqual(mockData);
        const fetchFn = AntiDetection.fetchWithRetry.mock.calls[0][0];
        await fetchFn();

        expect(fetch).toHaveBeenCalledWith(
          'https://bigquant.com/api/test/1',
          expect.objectContaining({ method: 'DELETE' })
        );
      });
    });
  });

  describe('API Methods', () => {
    beforeEach(async () => {
      await client.init();
    });

    describe('getUserInfo', () => {
      it('should call GET /api/user/info', async () => {
        const mockData = { userId: 123, username: 'test' };
        const mockResponse = createMockResponse(mockData);
        AntiDetection.fetchWithRetry.mockResolvedValue(mockResponse);

        const result = await client.getUserInfo();

        expect(result).toEqual(mockData);
        const fetchFn = AntiDetection.fetchWithRetry.mock.calls[0][0];
        await fetchFn();

        expect(fetch).toHaveBeenCalledWith(
          'https://bigquant.com/api/user/info',
          expect.any(Object)
        );
      });
    });

    describe('getStrategies', () => {
      it('should call GET /api/strategies with params', async () => {
        const mockData = { strategies: [] };
        const mockResponse = createMockResponse(mockData);
        AntiDetection.fetchWithRetry.mockResolvedValue(mockResponse);

        const result = await client.getStrategies({ limit: 10, offset: 0 });

        expect(result).toEqual(mockData);
        const fetchFn = AntiDetection.fetchWithRetry.mock.calls[0][0];
        await fetchFn();

        expect(fetch).toHaveBeenCalledWith(
          expect.stringContaining('/api/strategies?'),
          expect.any(Object)
        );
      });
    });

    describe('createStrategy', () => {
      it('should call POST /api/strategies', async () => {
        const mockData = { id: 'strategy-1' };
        const mockResponse = createMockResponse(mockData);
        AntiDetection.fetchWithRetry.mockResolvedValue(mockResponse);

        const result = await client.createStrategy({ name: 'New Strategy' });

        expect(result).toEqual(mockData);
        const fetchFn = AntiDetection.fetchWithRetry.mock.calls[0][0];
        await fetchFn();

        expect(fetch).toHaveBeenCalledWith(
          'https://bigquant.com/api/strategies',
          expect.objectContaining({ method: 'POST' })
        );
      });
    });

    describe('updateStrategy', () => {
      it('should call PUT /api/strategies/:id', async () => {
        const mockData = { id: 'strategy-1', updated: true };
        const mockResponse = createMockResponse(mockData);
        AntiDetection.fetchWithRetry.mockResolvedValue(mockResponse);

        const result = await client.updateStrategy('strategy-1', { name: 'Updated' });

        expect(result).toEqual(mockData);
        const fetchFn = AntiDetection.fetchWithRetry.mock.calls[0][0];
        await fetchFn();

        expect(fetch).toHaveBeenCalledWith(
          'https://bigquant.com/api/strategies/strategy-1',
          expect.objectContaining({ method: 'PUT' })
        );
      });
    });

    describe('runBacktest', () => {
      it('should call POST /api/strategies/:id/backtest', async () => {
        const mockData = { backtestId: 'backtest-1' };
        const mockResponse = createMockResponse(mockData);
        AntiDetection.fetchWithRetry.mockResolvedValue(mockResponse);

        const result = await client.runBacktest('strategy-1', {
          startDate: '2023-01-01',
          endDate: '2023-12-31'
        });

        expect(result).toEqual(mockData);
        const fetchFn = AntiDetection.fetchWithRetry.mock.calls[0][0];
        await fetchFn();

        expect(fetch).toHaveBeenCalledWith(
          'https://bigquant.com/api/strategies/strategy-1/backtest',
          expect.objectContaining({ method: 'POST' })
        );
      });
    });

    describe('getBacktestResult', () => {
      it('should call GET /api/backtests/:id', async () => {
        const mockData = { status: 'completed' };
        const mockResponse = createMockResponse(mockData);
        AntiDetection.fetchWithRetry.mockResolvedValue(mockResponse);

        const result = await client.getBacktestResult('backtest-1');

        expect(result).toEqual(mockData);
        const fetchFn = AntiDetection.fetchWithRetry.mock.calls[0][0];
        await fetchFn();

        expect(fetch).toHaveBeenCalledWith(
          'https://bigquant.com/api/backtests/backtest-1',
          expect.any(Object)
        );
      });
    });
  });

  describe('pollBacktestResult', () => {
    beforeEach(async () => {
      await client.init();
    });

    it('should return result when status is completed', async () => {
      const mockData = { status: 'completed', result: 'data' };
      const mockResponse = createMockResponse(mockData);
      AntiDetection.fetchWithRetry.mockResolvedValue(mockResponse);

      const result = await client.pollBacktestResult('backtest-1');

      expect(result).toEqual(mockData);
    });

    it('should throw error when status is failed', async () => {
      const mockData = { status: 'failed', error: 'Something went wrong' };
      const mockResponse = createMockResponse(mockData);
      AntiDetection.fetchWithRetry.mockResolvedValue(mockResponse);

      await expect(client.pollBacktestResult('backtest-1')).rejects.toThrow(
        'Backtest failed: Something went wrong'
      );
    });

    it('should poll multiple times until completed', async () => {
      const runningResponse = createMockResponse({ status: 'running' });
      const completedResponse = createMockResponse({ status: 'completed', result: 'data' });

      AntiDetection.fetchWithRetry
        .mockResolvedValueOnce(runningResponse)
        .mockResolvedValueOnce(runningResponse)
        .mockResolvedValueOnce(completedResponse);

      const result = await client.pollBacktestResult('backtest-1', { pollInterval: 100 });

      expect(result.status).toBe('completed');
      expect(AntiDetection.fetchWithRetry).toHaveBeenCalledTimes(3);
    });

    it('should throw timeout error after max attempts', async () => {
      const mockResponse = createMockResponse({ status: 'running' });
      AntiDetection.fetchWithRetry.mockResolvedValue(mockResponse);

      await expect(
        client.pollBacktestResult('backtest-1', { maxAttempts: 2, pollInterval: 100 })
      ).rejects.toThrow('Backtest timeout');
    });

    it('should use default options when not provided', async () => {
      const runningResponse = createMockResponse({ status: 'running' });
      const completedResponse = createMockResponse({ status: 'completed' });

      AntiDetection.fetchWithRetry
        .mockResolvedValueOnce(runningResponse)
        .mockResolvedValueOnce(completedResponse);

      await client.pollBacktestResult('backtest-1', { pollInterval: 5000 });

      expect(AntiDetection.randomDelay).toHaveBeenCalledWith(5000, 7000);
    });
  });

  describe('batchRunBacktests', () => {
    beforeEach(async () => {
      await client.init();
    });

    it('should run multiple backtests and return results', async () => {
      const backtestResponse = createMockResponse({ backtestId: 'bt-1' });
      const completedResponse = createMockResponse({ status: 'completed', result: 'data' });

      AntiDetection.fetchWithRetry
        .mockResolvedValueOnce(backtestResponse)
        .mockResolvedValueOnce(completedResponse)
        .mockResolvedValueOnce(backtestResponse)
        .mockResolvedValueOnce(completedResponse);

      const backtests = [
        { name: 'Test 1', strategyId: 's1', config: {} },
        { name: 'Test 2', strategyId: 's2', config: {} }
      ];

      const results = await client.batchRunBacktests(backtests);

      expect(results).toHaveLength(2);
      expect(results[0].success).toBe(true);
      expect(results[1].success).toBe(true);
    });

    it('should handle failed backtests', async () => {
      const backtestResponse = createMockResponse({ backtestId: 'bt-1' });
      const failedResponse = createMockResponse({ status: 'failed', error: 'Test error' });

      AntiDetection.fetchWithRetry
        .mockResolvedValueOnce(backtestResponse)
        .mockResolvedValueOnce(failedResponse);

      const backtests = [{ name: 'Test 1', strategyId: 's1', config: {} }];

      const results = await client.batchRunBacktests(backtests);

      expect(results).toHaveLength(1);
      expect(results[0].success).toBe(false);
      expect(results[0].error).toBe('Backtest failed: Test error');
    });

    it('should handle exceptions during backtest', async () => {
      AntiDetection.fetchWithRetry.mockRejectedValue(new Error('Network error'));

      const backtests = [{ name: 'Test 1', strategyId: 's1', config: {} }];

      const results = await client.batchRunBacktests(backtests);

      expect(results).toHaveLength(1);
      expect(results[0].success).toBe(false);
      expect(results[0].error).toBe('Network error');
    });

    it('should add random delay between backtests', async () => {
      const backtestResponse = createMockResponse({ backtestId: 'bt-1' });
      const completedResponse = createMockResponse({ status: 'completed' });

      AntiDetection.fetchWithRetry
        .mockResolvedValueOnce(backtestResponse)
        .mockResolvedValueOnce(completedResponse)
        .mockResolvedValueOnce(backtestResponse)
        .mockResolvedValueOnce(completedResponse);

      const backtests = [
        { name: 'Test 1', strategyId: 's1', config: {} },
        { name: 'Test 2', strategyId: 's2', config: {} }
      ];

      await client.batchRunBacktests(backtests);

      expect(AntiDetection.randomDelay).toHaveBeenCalledWith(2000, 5000);
    });
  });

  describe('Error Handling', () => {
    it('should propagate errors from fetchWithRetry', async () => {
      await client.init();
      AntiDetection.fetchWithRetry.mockRejectedValue(new Error('Network error'));

      await expect(client.request('/api/test')).rejects.toThrow('Network error');
    });

    it('should handle JSON parsing errors', async () => {
      await client.init();
      const mockResponse = createMockResponse({});
      mockResponse.json.mockRejectedValue(new Error('Invalid JSON'));
      AntiDetection.fetchWithRetry.mockResolvedValue(mockResponse);

      await expect(client.get('/api/test')).rejects.toThrow('Invalid JSON');
    });
  });
});