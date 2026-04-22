import { describe, it, beforeEach, afterEach } from 'node:test';
import assert from 'node:assert';
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';

describe('loadJson', () => {
  let loadJson;
  let testDir;
  let testFile;

  beforeEach(async () => {
    testDir = path.join(os.tmpdir(), `wizard-test-${Date.now()}`);
    fs.mkdirSync(testDir, { recursive: true });
    testFile = path.join(testDir, 'test.json');
    
    const { loadJson: lj } = await import('../request/wizard-client.js?' + Date.now());
    loadJson = lj;
  });

  afterEach(() => {
    fs.rmSync(testDir, { recursive: true, force: true });
  });

  it('should return null when file does not exist', () => {
    const result = loadJson('/nonexistent/path/file.json');
    assert.strictEqual(result, null);
  });

  it('should return parsed JSON when file exists and is valid', () => {
    const testData = { foo: 'bar', num: 42 };
    fs.writeFileSync(testFile, JSON.stringify(testData));
    
    const result = loadJson(testFile);
    assert.deepStrictEqual(result, testData);
  });

  it('should return null when JSON parsing fails', () => {
    fs.writeFileSync(testFile, 'invalid json {{{');
    
    const result = loadJson(testFile);
    assert.strictEqual(result, null);
  });

  it('should handle nested JSON correctly', () => {
    const testData = { nested: { deep: { value: 123 } }, array: [1, 2, 3] };
    fs.writeFileSync(testFile, JSON.stringify(testData));
    
    const result = loadJson(testFile);
    assert.deepStrictEqual(result.nested.deep.value, 123);
    assert.deepStrictEqual(result.array, [1, 2, 3]);
  });
});

describe('saveJson', () => {
  let saveJson;
  let testDir;

  beforeEach(async () => {
    testDir = path.join(os.tmpdir(), `wizard-test-${Date.now()}`);
    
    const { saveJson: sj } = await import('../request/wizard-client.js?' + Date.now());
    saveJson = sj;
  });

  afterEach(() => {
    fs.rmSync(testDir, { recursive: true, force: true });
  });

  it('should save JSON data to file', () => {
    const testFile = path.join(testDir, 'output.json');
    const testData = { foo: 'bar', nested: { a: 1 } };
    
    saveJson(testFile, testData);
    
    const content = fs.readFileSync(testFile, 'utf8');
    const parsed = JSON.parse(content);
    assert.deepStrictEqual(parsed, testData);
  });

  it('should create parent directory with recursive option', () => {
    const deepFile = path.join(testDir, 'deep', 'nested', 'path', 'file.json');
    
    saveJson(deepFile, { test: 1 });
    
    assert.ok(fs.existsSync(deepFile));
  });

  it('should format JSON with 2-space indentation', () => {
    const testFile = path.join(testDir, 'formatted.json');
    
    saveJson(testFile, { a: 1, b: { c: 2 } });
    
    const content = fs.readFileSync(testFile, 'utf8');
    assert.ok(content.includes('  "a":'));
    assert.ok(content.includes('    "c":'));
  });

  it('should overwrite existing file', () => {
    const testFile = path.join(testDir, 'overwrite.json');
    
    saveJson(testFile, { version: 1 });
    saveJson(testFile, { version: 2 });
    
    const content = fs.readFileSync(testFile, 'utf8');
    const parsed = JSON.parse(content);
    assert.strictEqual(parsed.version, 2);
  });
});

describe('WizardClient', () => {
  let WizardClient;
  let originalFetch;
  let fetchCalls;

  beforeEach(async () => {
    fetchCalls = [];
    originalFetch = global.fetch;
    
    global.fetch = async (url, options) => {
      fetchCalls.push({ url, options });
      
      if (url.includes('/workspaces')) {
        return {
          ok: true,
          status: 200,
          text: async () => JSON.stringify({ data: [{ id: 'workspace-123' }] })
        };
      }
      
      if (url.includes('/isLogin')) {
        return {
          ok: true,
          status: 200,
          text: async () => JSON.stringify({ isLogin: true })
        };
      }
      
      if (url.includes('/strategies') && !url.includes('/strategies/')) {
        return {
          ok: true,
          status: 200,
          text: async () => JSON.stringify([
            { _id: 'strat-1', title: 'Code Strategy', metadata: { strategy_type: 'code' }, last_modified: '2024-01-01' },
            { _id: 'strat-2', title: 'Wizard Strategy', metadata: { strategy_type: 'wizard' }, last_modified: '2024-01-02' }
          ])
        };
      }
      
      if (url.includes('/strategies/strat-')) {
        if (options?.method === 'DELETE') {
          return { ok: true, status: 200, text: async () => '' };
        }
        return {
          ok: true,
          status: 200,
          text: async () => JSON.stringify({ _id: 'strat-1', code: 'test code' })
        };
      }
      
      if (url.includes('/backtests/') && !url.includes('/risk') && !url.includes('/logs')) {
        if (url.includes('/backtests/bt-')) {
          return {
            ok: true,
            status: 200,
            text: async () => JSON.stringify({ backtestId: 'bt-1', status: 'finished', progress: 1, summary: { returns: 0.5 } })
          };
        }
        return {
          ok: true,
          status: 200,
          text: async () => JSON.stringify({ backtestId: 'bt-new' })
        };
      }
      
      if (url.includes('/risk')) {
        return {
          ok: true,
          status: 200,
          text: async () => JSON.stringify({ sharpe: 1.5, max_drawdown: 0.1 })
        };
      }
      
      if (url.includes('/logs')) {
        return {
          ok: true,
          status: 200,
          text: async () => JSON.stringify({ logs: ['log1', 'log2'] })
        };
      }
      
      if (options?.method === 'POST' && url.includes('/strategies')) {
        return {
          ok: true,
          status: 200,
          text: async () => JSON.stringify({ _id: 'new-strategy-1' })
        };
      }
      
      if (options?.method === 'POST' && url.includes('/backtests')) {
        return {
          ok: true,
          status: 200,
          text: async () => '"bt-123"'
        };
      }
      
      return {
        ok: true,
        status: 200,
        text: async () => JSON.stringify({ success: true })
      };
    };
    
    const module = await import('../request/wizard-client.js?' + Date.now());
    WizardClient = module.WizardClient;
  });

  afterEach(() => {
    global.fetch = originalFetch;
  });

  describe('constructor', () => {
    it('should initialize with default options', () => {
      const client = new WizardClient({ sessionPayload: {} });
      
      assert.strictEqual(client.origin, 'https://www.ricequant.com');
      assert.deepStrictEqual(client.cookieJar, []);
      assert.strictEqual(client.workspaceId, null);
    });

    it('should use provided cookies', () => {
      const cookies = [{ name: 'session', value: 'abc123' }];
      const client = new WizardClient({ sessionPayload: {}, cookies });
      
      assert.deepStrictEqual(client.cookieJar, cookies);
    });

    it('should use provided sessionPayload', () => {
      const payload = { cookies: [{ name: 'test', value: 'val' }] };
      const client = new WizardClient({ sessionPayload: payload });
      
      assert.deepStrictEqual(client.sessionPayload, payload);
      assert.strictEqual(client.cookieJar.length, 1);
    });

    it('should use custom session file path', () => {
      const client = new WizardClient({ sessionPayload: {}, sessionFile: '/custom/path.json' });
      
      assert.strictEqual(client.sessionFile, '/custom/path.json');
    });

    it('should prioritize cookies over sessionPayload cookies', () => {
      const cookies = [{ name: 'custom', value: 'xyz' }];
      const payload = { cookies: [{ name: 'session', value: 'abc' }] };
      const client = new WizardClient({ sessionPayload: payload, cookies });
      
      assert.strictEqual(client.cookieJar.length, 1);
      assert.strictEqual(client.cookieJar[0].name, 'custom');
    });
  });

  describe('buildHeaders', () => {
    it('should build headers with default values', () => {
      const client = new WizardClient({ 
        sessionPayload: {}, 
        cookies: [{ name: 'test', value: '123' }] 
      });
      
      const headers = client.buildHeaders('https://example.com/api');
      
      assert.ok(headers['User-Agent'].includes('Chrome'));
      assert.strictEqual(headers['Accept'], 'application/json, text/plain, */*');
      assert.strictEqual(headers['Referer'], 'https://example.com/api');
      assert.strictEqual(headers['Origin'], 'https://www.ricequant.com');
      assert.strictEqual(headers['Cookie'], 'test=123');
    });

    it('should build cookie header from multiple cookies', () => {
      const client = new WizardClient({
        sessionPayload: {},
        cookies: [
          { name: 'session', value: 'abc' },
          { name: 'token', value: 'xyz' }
        ]
      });
      
      const headers = client.buildHeaders('https://example.com');
      
      assert.strictEqual(headers['Cookie'], 'session=abc; token=xyz');
    });

    it('should override headers with provided values', () => {
      const client = new WizardClient({ sessionPayload: {} });
      
      const headers = client.buildHeaders('https://example.com', {
        'X-Custom': 'custom-value',
        'Accept': 'text/html'
      });
      
      assert.strictEqual(headers['X-Custom'], 'custom-value');
      assert.strictEqual(headers['Accept'], 'text/html');
    });

    it('should include sec-fetch headers', () => {
      const client = new WizardClient({ sessionPayload: {} });
      
      const headers = client.buildHeaders('https://example.com');
      
      assert.ok(headers['sec-fetch-dest']);
      assert.ok(headers['sec-fetch-mode']);
      assert.ok(headers['sec-fetch-site']);
    });
  });

  describe('request', () => {
    it('should make GET request and parse JSON response', async () => {
      const client = new WizardClient({ sessionPayload: {} });
      
      const result = await client.request('/api/test');
      
      assert.ok(result);
      assert.strictEqual(fetchCalls.length, 1);
      assert.ok(fetchCalls[0].url.startsWith('https://www.ricequant.com/api/test'));
    });

    it('should make request with full URL', async () => {
      const client = new WizardClient({ sessionPayload: {} });
      
      await client.request('https://other.com/api');
      
      assert.strictEqual(fetchCalls[0].url, 'https://other.com/api');
    });

    it('should make POST request with body', async () => {
      const client = new WizardClient({ sessionPayload: {} });
      
      await client.request('/api/test', {
        method: 'POST',
        body: '{"key":"value"}'
      });
      
      assert.strictEqual(fetchCalls[0].options.method, 'POST');
      assert.strictEqual(fetchCalls[0].options.body, '{"key":"value"}');
    });

    it('should throw on non-ok response', async () => {
      global.fetch = async () => ({
        ok: false,
        status: 404,
        text: async () => 'Not Found'
      });
      
      const client = new WizardClient({ sessionPayload: {} });
      
      await assert.rejects(
        async () => await client.request('/api/notfound'),
        /Request failed 404/
      );
    });

    it('should return text when response is not valid JSON', async () => {
      global.fetch = async () => ({
        ok: true,
        text: async () => 'plain text'
      });
      
      const client = new WizardClient({ sessionPayload: {} });
      
      const result = await client.request('/api/test');
      
      assert.strictEqual(result, 'plain text');
    });
  });

  describe('getWorkspaceId', () => {
    it('should return workspaceId from API', async () => {
      const client = new WizardClient({ sessionPayload: {} });
      
      const id = await client.getWorkspaceId();
      
      assert.strictEqual(id, 'workspace-123');
    });

    it('should cache workspaceId', async () => {
      const client = new WizardClient({ sessionPayload: {} });
      
      await client.getWorkspaceId();
      fetchCalls.length = 0;
      await client.getWorkspaceId();
      
      assert.strictEqual(fetchCalls.length, 0);
    });

    it('should throw when no workspace found', async () => {
      global.fetch = async () => ({
        ok: true,
        text: async () => JSON.stringify({ data: [] })
      });
      
      const client = new WizardClient({ sessionPayload: {} });
      
      await assert.rejects(
        async () => await client.getWorkspaceId(),
        /No workspace found/
      );
    });
  });

  describe('checkLogin', () => {
    it('should call login check API', async () => {
      const client = new WizardClient({ sessionPayload: {} });
      
      const result = await client.checkLogin();
      
      assert.strictEqual(result.isLogin, true);
      assert.ok(fetchCalls[0].url.includes('isLogin'));
      assert.strictEqual(fetchCalls[0].options.method, 'POST');
    });
  });

  describe('listStrategies', () => {
    it('should list all strategies without type filter', async () => {
      const client = new WizardClient({ sessionPayload: {} });
      
      const strategies = await client.listStrategies();
      
      assert.strictEqual(strategies.length, 2);
      assert.strictEqual(strategies[0].id, 'strat-1');
      assert.strictEqual(strategies[1].id, 'strat-2');
    });

    it('should filter strategies by type=wizard', async () => {
      const client = new WizardClient({ sessionPayload: {} });
      
      const strategies = await client.listStrategies({ type: 'wizard' });
      
      assert.strictEqual(strategies.length, 1);
      assert.strictEqual(strategies[0].type, 'wizard');
    });

    it('should filter strategies by type=code', async () => {
      const client = new WizardClient({ sessionPayload: {} });
      
      const strategies = await client.listStrategies({ type: 'code' });
      
      assert.strictEqual(strategies.length, 1);
      assert.strictEqual(strategies[0].type, 'code');
    });

    it('should handle strategy_id field', async () => {
      global.fetch = async () => ({
        ok: true,
        text: async () => JSON.stringify([
          { strategy_id: 'sid-3', title: 'Test', metadata: {}, last_modified: '2024-01-01' }
        ])
      });
      
      const client = new WizardClient({ sessionPayload: {} });
      client.workspaceId = 'ws-1';
      
      const strategies = await client.listStrategies();
      
      assert.strictEqual(strategies[0].id, 'sid-3');
    });

    it('should include wizardOption in result', async () => {
      global.fetch = async () => ({
        ok: true,
        text: async () => JSON.stringify([
          { 
            _id: 'strat-1', 
            title: 'Test', 
            metadata: { strategy_type: 'wizard', wizard_option: { max_holding_num: 10 } }, 
            last_modified: '2024-01-01' 
          }
        ])
      });
      
      const client = new WizardClient({ sessionPayload: {} });
      client.workspaceId = 'ws-1';
      
      const strategies = await client.listStrategies();
      
      assert.deepStrictEqual(strategies[0].wizardOption, { max_holding_num: 10 });
    });

    it('should handle non-array response', async () => {
      global.fetch = async () => ({
        ok: true,
        text: async () => JSON.stringify({ error: 'not array' })
      });
      
      const client = new WizardClient({ sessionPayload: {} });
      client.workspaceId = 'ws-1';
      
      const strategies = await client.listStrategies();
      
      assert.deepStrictEqual(strategies, []);
    });
  });

  describe('getStrategy', () => {
    it('should get strategy by ID', async () => {
      const client = new WizardClient({ sessionPayload: {} });
      client.workspaceId = 'ws-1';
      
      const strategy = await client.getStrategy('strat-1');
      
      assert.strictEqual(strategy._id, 'strat-1');
      assert.ok(fetchCalls[0].url.includes('strat-1'));
      assert.ok(fetchCalls[0].url.includes('code=true'));
    });
  });

  describe('createWizardStrategy', () => {
    it('should create wizard strategy with correct body', async () => {
      const client = new WizardClient({ sessionPayload: {} });
      const config = {
        name: 'Test Strategy',
        universe: ['000300.XSHG'],
        filters: [],
        sorting: [],
        backtest: {}
      };
      
      const result = await client.createWizardStrategy(config);
      
      assert.strictEqual(result.strategyId, 'new-strategy-1');
      assert.strictEqual(result.title, 'Test Strategy');
      
      const body = JSON.parse(fetchCalls[1].options.body);
      assert.strictEqual(body.title, 'Test Strategy');
      assert.strictEqual(body.metadata.strategy_type, 'wizard');
      assert.strictEqual(fetchCalls[1].options.method, 'POST');
    });

    it('should generate code and wizardOption', async () => {
      const client = new WizardClient({ sessionPayload: {} });
      const config = {
        name: 'Test',
        universe: ['000300.XSHG'],
        maxHoldingNum: 15,
        filters: [
          { operator: 'greater_than', factor: { type: 'fundamental', name: 'pe_ratio' }, rhs: 10 }
        ]
      };
      
      const result = await client.createWizardStrategy(config);
      
      assert.ok(result.wizardOption);
      assert.strictEqual(result.wizardOption.max_holding_num, 15);
      assert.strictEqual(result.wizardOption.filters.length, 1);
      
      const body = JSON.parse(fetchCalls[1].options.body);
      assert.ok(body.code.includes('MAX_HOLDING_NUM'));
      assert.ok(body.code.includes('FILTERS'));
    });
  });

  describe('updateWizardStrategy', () => {
    it('should update wizard strategy', async () => {
      global.fetch = async (url, options) => {
        if (options?.method === 'PATCH') {
          return { ok: true, text: async () => JSON.stringify({ success: true }) };
        }
        return { ok: true, text: async () => JSON.stringify({ data: [{ id: 'ws-1' }] }) };
      };
      
      const client = new WizardClient({ sessionPayload: {} });
      const config = { name: 'Updated', universe: ['000300.XSHG'] };
      
      const result = await client.updateWizardStrategy('strat-1', config);
      
      assert.deepStrictEqual(result, { success: true });
      assert.strictEqual(fetchCalls[1].options.method, 'PATCH');
    });

    it('should return success on error', async () => {
      global.fetch = async (url, options) => {
        if (options?.method === 'PATCH') {
          return { ok: false, status: 500, text: async () => 'Error' };
        }
        return { ok: true, text: async () => JSON.stringify({ data: [{ id: 'ws-1' }] }) };
      };
      
      const client = new WizardClient({ sessionPayload: {} });
      const config = { name: 'Test', universe: ['000300.XSHG'] };
      
      const result = await client.updateWizardStrategy('strat-1', config);
      
      assert.deepStrictEqual(result, { success: true });
    });
  });

  describe('deleteStrategy', () => {
    it('should delete strategy successfully', async () => {
      const client = new WizardClient({ sessionPayload: {} });
      client.workspaceId = 'ws-1';
      
      const result = await client.deleteStrategy('strat-1');
      
      assert.strictEqual(result, true);
      assert.strictEqual(fetchCalls[0].options.method, 'DELETE');
    });

    it('should return false on delete failure', async () => {
      global.fetch = async () => ({ ok: false, status: 404, text: async () => 'Not found' });
      
      const client = new WizardClient({ sessionPayload: {} });
      client.workspaceId = 'ws-1';
      
      const result = await client.deleteStrategy('strat-1');
      
      assert.strictEqual(result, false);
    });
  });

  describe('runBacktest', () => {
    it('should run backtest with default config', async () => {
      const client = new WizardClient({ sessionPayload: {} });
      client.workspaceId = 'ws-1';
      
      const result = await client.runBacktest('strat-1', {});
      
      assert.strictEqual(result.backtestId, 'bt-123');
    });

    it('should run backtest with custom config', async () => {
      const client = new WizardClient({ sessionPayload: {} });
      client.workspaceId = 'ws-1';
      
      const backtestConfig = {
        start: '2022-01-01',
        end: '2023-12-31',
        capital: '500000',
        frequency: 'minute',
        benchmark: '000905.XSHG'
      };
      
      await client.runBacktest('strat-1', backtestConfig);
      
      const body = JSON.parse(fetchCalls[0].options.body);
      assert.strictEqual(body.config.start_date, '2022-01-01');
      assert.strictEqual(body.config.end_date, '2023-12-31');
      assert.strictEqual(body.config.stock_init_cash, 500000);
      assert.strictEqual(body.config.frequency, 'minute');
      assert.strictEqual(body.config.benchmark, '000905.XSHG');
    });

    it('should parse backtestId from string response', async () => {
      global.fetch = async () => ({
        ok: true,
        text: async () => '"bt-string-id"'
      });
      
      const client = new WizardClient({ sessionPayload: {} });
      client.workspaceId = 'ws-1';
      
      const result = await client.runBacktest('strat-1', {});
      
      assert.strictEqual(result.backtestId, 'bt-string-id');
    });

    it('should parse backtestId from object response', async () => {
      global.fetch = async () => ({
        ok: true,
        text: async () => JSON.stringify({ _id: 'bt-obj-id' })
      });
      
      const client = new WizardClient({ sessionPayload: {} });
      client.workspaceId = 'ws-1';
      
      const result = await client.runBacktest('strat-1', {});
      
      assert.strictEqual(result.backtestId, 'bt-obj-id');
    });
  });

  describe('getBacktestResult', () => {
    it('should get backtest result', async () => {
      const client = new WizardClient({ sessionPayload: {} });
      client.workspaceId = 'ws-1';
      
      const result = await client.getBacktestResult('bt-1');
      
      assert.strictEqual(result.status, 'finished');
    });
  });

  describe('getBacktestRisk', () => {
    it('should get backtest risk data', async () => {
      const client = new WizardClient({ sessionPayload: {} });
      client.workspaceId = 'ws-1';
      
      const result = await client.getBacktestRisk('bt-1');
      
      assert.strictEqual(result.sharpe, 1.5);
    });

    it('should return null on error', async () => {
      global.fetch = async () => ({ ok: false, status: 404, text: async () => 'Not found' });
      
      const client = new WizardClient({ sessionPayload: {} });
      client.workspaceId = 'ws-1';
      
      const result = await client.getBacktestRisk('bt-1');
      
      assert.strictEqual(result, null);
    });
  });

  describe('getBacktestLogs', () => {
    it('should get backtest logs', async () => {
      const client = new WizardClient({ sessionPayload: {} });
      client.workspaceId = 'ws-1';
      
      const result = await client.getBacktestLogs('bt-1');
      
      assert.deepStrictEqual(result.logs, ['log1', 'log2']);
    });

    it('should return empty logs on error', async () => {
      global.fetch = async () => ({ ok: false, status: 500, text: async () => 'Error' });
      
      const client = new WizardClient({ sessionPayload: {} });
      client.workspaceId = 'ws-1';
      
      const result = await client.getBacktestLogs('bt-1');
      
      assert.deepStrictEqual(result, { logs: [] });
    });
  });

  describe('waitForBacktest', () => {
    it('should return finished on normal_exit status', async () => {
      global.fetch = async () => ({
        ok: true,
        text: async () => JSON.stringify({ status: 'normal_exit', progress: 1 })
      });
      
      const client = new WizardClient({ sessionPayload: {} });
      client.workspaceId = 'ws-1';
      
      const result = await client.waitForBacktest('bt-1', { maxAttempts: 1 });
      
      assert.strictEqual(result.status, 'finished');
    });

    it('should return finished on finished status', async () => {
      global.fetch = async () => ({
        ok: true,
        text: async () => JSON.stringify({ status: 'finished' })
      });
      
      const client = new WizardClient({ sessionPayload: {} });
      client.workspaceId = 'ws-1';
      
      const result = await client.waitForBacktest('bt-1', { maxAttempts: 1 });
      
      assert.strictEqual(result.status, 'finished');
    });

    it('should return finished on progress 1', async () => {
      global.fetch = async () => ({
        ok: true,
        text: async () => JSON.stringify({ status: 'running', progress: 1 })
      });
      
      const client = new WizardClient({ sessionPayload: {} });
      client.workspaceId = 'ws-1';
      
      const result = await client.waitForBacktest('bt-1', { maxAttempts: 1 });
      
      assert.strictEqual(result.status, 'finished');
    });

    it('should return finished on progress 100', async () => {
      global.fetch = async () => ({
        ok: true,
        text: async () => JSON.stringify({ status: 'running', progress: 100 })
      });
      
      const client = new WizardClient({ sessionPayload: {} });
      client.workspaceId = 'ws-1';
      
      const result = await client.waitForBacktest('bt-1', { maxAttempts: 1 });
      
      assert.strictEqual(result.status, 'finished');
    });

    it('should return error on error_exit status', async () => {
      global.fetch = async () => ({
        ok: true,
        text: async () => JSON.stringify({ status: 'error_exit', exception: 'Test error' })
      });
      
      const client = new WizardClient({ sessionPayload: {} });
      client.workspaceId = 'ws-1';
      
      const result = await client.waitForBacktest('bt-1', { maxAttempts: 1 });
      
      assert.strictEqual(result.status, 'error');
      assert.strictEqual(result.exception, 'Test error');
    });

    it('should return error on cancelled status', async () => {
      global.fetch = async () => ({
        ok: true,
        text: async () => JSON.stringify({ status: 'cancelled' })
      });
      
      const client = new WizardClient({ sessionPayload: {} });
      client.workspaceId = 'ws-1';
      
      const result = await client.waitForBacktest('bt-1', { maxAttempts: 1 });
      
      assert.strictEqual(result.status, 'error');
    });

    it('should return error on failed status', async () => {
      global.fetch = async () => ({
        ok: true,
        text: async () => JSON.stringify({ status: 'failed' })
      });
      
      const client = new WizardClient({ sessionPayload: {} });
      client.workspaceId = 'ws-1';
      
      const result = await client.waitForBacktest('bt-1', { maxAttempts: 1 });
      
      assert.strictEqual(result.status, 'error');
    });

    it('should return timeout after maxAttempts', async () => {
      global.fetch = async () => ({
        ok: true,
        text: async () => JSON.stringify({ status: 'running', progress: 0.5 })
      });
      
      const client = new WizardClient({ sessionPayload: {} });
      client.workspaceId = 'ws-1';
      
      const result = await client.waitForBacktest('bt-1', { maxAttempts: 2, interval: 1 });
      
      assert.strictEqual(result.status, 'timeout');
    });
  });

  describe('getFullReport', () => {
    it('should get all backtest data in parallel', async () => {
      const client = new WizardClient({ sessionPayload: {} });
      client.workspaceId = 'ws-1';
      
      const report = await client.getFullReport('bt-1');
      
      assert.strictEqual(report.backtestId, 'bt-1');
      assert.strictEqual(report.risk.sharpe, 1.5);
      assert.deepStrictEqual(report.logs, ['log1', 'log2']);
    });

    it('should use result.summary when risk is null', async () => {
      global.fetch = async (url) => {
        if (url.includes('/risk')) {
          return { ok: false, status: 404, text: async () => 'Not found' };
        }
        if (url.includes('/logs')) {
          return { ok: true, text: async () => JSON.stringify({ logs: [] }) };
        }
        return {
          ok: true,
          text: async () => JSON.stringify({ 
            backtestId: 'bt-1', 
            summary: { returns: 0.5 },
            risk: { sharpe: 1.0 }
          })
        };
      };
      
      const client = new WizardClient({ sessionPayload: {} });
      client.workspaceId = 'ws-1';
      
      const report = await client.getFullReport('bt-1');
      
      assert.strictEqual(report.risk.sharpe, 1.0);
      assert.deepStrictEqual(report.summary, { returns: 0.5 });
    });
  });

  describe('buildWizardOption', () => {
    it('should build option with defaults', () => {
      const client = new WizardClient({ sessionPayload: {} });
      
      const option = client.buildWizardOption({ name: 'Test' });
      
      assert.strictEqual(option.template_name, 'single_period');
      assert.deepStrictEqual(option.universe, ['000300.XSHG']);
      assert.deepStrictEqual(option.industries, ['*']);
      assert.deepStrictEqual(option.board, ['*']);
      assert.strictEqual(option.st_option, 'exclude');
      assert.strictEqual(option.max_holding_num, 10);
      assert.strictEqual(option.rebalance_interval, 5);
    });

    it('should use provided config values', () => {
      const client = new WizardClient({ sessionPayload: {} });
      
      const option = client.buildWizardOption({
        name: 'Test',
        template: 'three_periods',
        universe: ['000905.XSHG'],
        industries: ['金融'],
        board: ['主板'],
        stOption: 'include',
        maxHoldingNum: 20,
        rebalanceInterval: 10,
        maxHoldingPercent: 0.3
      });
      
      assert.strictEqual(option.template_name, 'three_periods');
      assert.deepStrictEqual(option.universe, ['000905.XSHG']);
      assert.deepStrictEqual(option.industries, ['金融']);
      assert.deepStrictEqual(option.board, ['主板']);
      assert.strictEqual(option.st_option, 'include');
      assert.strictEqual(option.max_holding_num, 20);
      assert.strictEqual(option.rebalance_interval, 10);
      assert.strictEqual(option.three_periods.max_holding_percent, 0.3);
    });

    it('should switch to three_periods when buy provided', () => {
      const client = new WizardClient({ sessionPayload: {} });
      
      const option = client.buildWizardOption({
        name: 'Test',
        buy: { filters: [] }
      });
      
      assert.strictEqual(option.template_name, 'three_periods');
    });

    it('should switch to three_periods when sell provided', () => {
      const client = new WizardClient({ sessionPayload: {} });
      
      const option = client.buildWizardOption({
        name: 'Test',
        sell: { filters: [] }
      });
      
      assert.strictEqual(option.template_name, 'three_periods');
    });

    it('should build filters, sorting, and risk', () => {
      const client = new WizardClient({ sessionPayload: {} });
      
      const option = client.buildWizardOption({
        name: 'Test',
        filters: [
          { operator: 'greater_than', factor: { type: 'fundamental', name: 'pe_ratio' }, rhs: 10 }
        ],
        sorting: [
          { factor: { type: 'fundamental', name: 'pe_ratio' }, ascending: true, weight: 0.5 }
        ],
        risk: {
          marketEnterSignals: ['sig1'],
          marketPanicSignals: ['sig2'],
          pnl: ['p1']
        }
      });
      
      assert.strictEqual(option.filters.length, 1);
      assert.strictEqual(option.sorting.length, 1);
      assert.deepStrictEqual(option.risk.market_enter_signals, ['sig1']);
    });

    it('should build buy and sell sections', () => {
      const client = new WizardClient({ sessionPayload: {} });
      
      const option = client.buildWizardOption({
        name: 'Test',
        buy: {
          filters: [{ operator: 'greater_than', factor: { type: 'fundamental', name: 'roe' }, rhs: 0.1 }],
          rebalanceInterval: 3
        },
        sell: {
          filters: [{ operator: 'less_than', factor: { type: 'fundamental', name: 'pe_ratio' }, rhs: 5 }],
          rebalanceInterval: 2
        }
      });
      
      assert.strictEqual(option.buy.filters.length, 1);
      assert.strictEqual(option.buy.rebalance_interval, 3);
      assert.strictEqual(option.sell.filters.length, 1);
      assert.strictEqual(option.sell.rebalance_interval, 2);
    });
  });

  describe('buildFilters', () => {
    it('should build filter with factor object', () => {
      const client = new WizardClient({ sessionPayload: {} });
      
      const filters = client.buildFilters([
        { operator: 'greater_than', factor: { type: 'fundamental', name: 'pe_ratio' }, rhs: 10 }
      ]);
      
      assert.strictEqual(filters[0].operator, 'greater_than');
      assert.strictEqual(filters[0].lhs.type, 'fundamental');
      assert.strictEqual(filters[0].lhs.name, 'pe_ratio');
      assert.strictEqual(filters[0].rhs, 10);
    });

    it('should build filter with simplified format', () => {
      const client = new WizardClient({ sessionPayload: {} });
      
      const filters = client.buildFilters([
        { operator: 'less_than', name: 'pb_ratio', value: 2 }
      ]);
      
      assert.strictEqual(filters[0].lhs.name, 'pb_ratio');
      assert.strictEqual(filters[0].lhs.type, 'fundamental');
      assert.strictEqual(filters[0].rhs, 2);
    });

    it('should preserve factor parameters', () => {
      const client = new WizardClient({ sessionPayload: {} });
      
      const filters = client.buildFilters([
        { 
          operator: 'greater_than', 
          factor: { type: 'fundamental', name: 'ma', parameters: { window: 20 } }, 
          rhs: 100 
        }
      ]);
      
      assert.deepStrictEqual(filters[0].lhs.parameters, { window: 20 });
    });

    it('should handle empty array', () => {
      const client = new WizardClient({ sessionPayload: {} });
      
      const filters = client.buildFilters([]);
      
      assert.deepStrictEqual(filters, []);
    });
  });

  describe('buildSorting', () => {
    it('should build sorting with factor object', () => {
      const client = new WizardClient({ sessionPayload: {} });
      
      const sorting = client.buildSorting([
        { factor: { type: 'fundamental', name: 'pe_ratio' }, ascending: true, weight: 0.5 }
      ]);
      
      assert.strictEqual(sorting[0].factor.type, 'fundamental');
      assert.strictEqual(sorting[0].factor.name, 'pe_ratio');
      assert.strictEqual(sorting[0].ascending, true);
      assert.strictEqual(sorting[0].weight, 0.5);
    });

    it('should build sorting with simplified format', () => {
      const client = new WizardClient({ sessionPayload: {} });
      
      const sorting = client.buildSorting([
        { name: 'market_cap', ascending: false }
      ]);
      
      assert.strictEqual(sorting[0].factor.name, 'market_cap');
      assert.strictEqual(sorting[0].ascending, false);
      assert.strictEqual(sorting[0].weight, 1);
    });

    it('should default ascending to true', () => {
      const client = new WizardClient({ sessionPayload: {} });
      
      const sorting = client.buildSorting([
        { factor: { type: 'fundamental', name: 'pe_ratio' } }
      ]);
      
      assert.strictEqual(sorting[0].ascending, true);
    });

    it('should handle empty array', () => {
      const client = new WizardClient({ sessionPayload: {} });
      
      const sorting = client.buildSorting([]);
      
      assert.deepStrictEqual(sorting, []);
    });
  });

  describe('buildRisk', () => {
    it('should build risk with all fields', () => {
      const client = new WizardClient({ sessionPayload: {} });
      
      const risk = client.buildRisk({
        marketEnterSignals: ['s1', 's2'],
        marketPanicSignals: ['s3'],
        pnl: ['p1']
      });
      
      assert.deepStrictEqual(risk.market_enter_signals, ['s1', 's2']);
      assert.deepStrictEqual(risk.market_panic_signals, ['s3']);
      assert.deepStrictEqual(risk.pnl, ['p1']);
    });

    it('should default to empty arrays', () => {
      const client = new WizardClient({ sessionPayload: {} });
      
      const risk = client.buildRisk({});
      
      assert.deepStrictEqual(risk.market_enter_signals, []);
      assert.deepStrictEqual(risk.market_panic_signals, []);
      assert.deepStrictEqual(risk.pnl, []);
    });
  });

  describe('buildBacktestConfig', () => {
    it('should build config with defaults', () => {
      const client = new WizardClient({ sessionPayload: {} });
      
      const config = client.buildBacktestConfig();
      
      assert.strictEqual(config.stock_init_cash, 100000);
      assert.strictEqual(config.start_date, '2020-01-01');
      assert.strictEqual(config.end_date, '2025-03-28');
      assert.strictEqual(config.frequency, 'day');
      assert.strictEqual(config.benchmark, '000300.XSHG');
    });

    it('should build config with custom values', () => {
      const client = new WizardClient({ sessionPayload: {} });
      
      const config = client.buildBacktestConfig({
        start: '2022-01-01',
        end: '2023-12-31',
        capital: '500000',
        frequency: 'minute',
        benchmark: '000905.XSHG'
      });
      
      assert.strictEqual(config.stock_init_cash, 500000);
      assert.strictEqual(config.start_date, '2022-01-01');
      assert.strictEqual(config.end_date, '2023-12-31');
      assert.strictEqual(config.frequency, 'minute');
      assert.strictEqual(config.benchmark, '000905.XSHG');
    });
  });

  describe('generateWizardCode', () => {
    it('should generate single period code by default', () => {
      const client = new WizardClient({ sessionPayload: {} });
      
      const code = client.generateWizardCode({
        name: 'Test',
        universe: ['000300.XSHG'],
        maxHoldingNum: 15,
        rebalanceInterval: 10
      });
      
      assert.ok(code.includes('MAX_HOLDING_NUM = 15'));
      assert.ok(code.includes('REBALANCE_INTERVAL = 10'));
      assert.ok(code.includes('def init(context)'));
      assert.ok(code.includes('def rebalance_first_part'));
      assert.ok(code.includes('def rebalance_second_part'));
      assert.ok(!code.includes('BUY_FILTERS'));
    });

    it('should generate three periods code when template is three_periods', () => {
      const client = new WizardClient({ sessionPayload: {} });
      
      const code = client.generateWizardCode({
        name: 'Test',
        template: 'three_periods'
      });
      
      assert.ok(code.includes('BUY_REBALANCE_INTERVAL'));
      assert.ok(code.includes('SELL_REBALANCE_INTERVAL'));
      assert.ok(code.includes('BUY_FILTERS'));
      assert.ok(code.includes('SELL_FILTERS'));
      assert.ok(code.includes('def sell_rebalance'));
      assert.ok(code.includes('def buy_rebalance'));
    });

    it('should generate three periods code when buy provided', () => {
      const client = new WizardClient({ sessionPayload: {} });
      
      const code = client.generateWizardCode({
        name: 'Test',
        buy: { filters: [] }
      });
      
      assert.ok(code.includes('BUY_FILTERS'));
    });

    it('should generate three periods code when sell provided', () => {
      const client = new WizardClient({ sessionPayload: {} });
      
      const code = client.generateWizardCode({
        name: 'Test',
        sell: { filters: [] }
      });
      
      assert.ok(code.includes('SELL_FILTERS'));
    });
  });

  describe('_buildFilterCodeLines', () => {
    it('should build filter code lines', () => {
      const client = new WizardClient({ sessionPayload: {} });
      
      const lines = client._buildFilterCodeLines([
        { operator: 'greater_than', factor: { type: 'fundamental', name: 'pe_ratio' }, rhs: 10 }
      ]);
      
      assert.ok(lines.includes("'operator': 'greater_than'"));
      assert.ok(lines.includes("'name': 'pe_ratio'"));
      assert.ok(lines.includes("'rhs': 10"));
    });

    it('should handle simplified format', () => {
      const client = new WizardClient({ sessionPayload: {} });
      
      const lines = client._buildFilterCodeLines([
        { operator: 'less_than', name: 'pb_ratio', value: 2 }
      ]);
      
      assert.ok(lines.includes("'name': 'pb_ratio'"));
    });

    it('should handle in_range with array', () => {
      const client = new WizardClient({ sessionPayload: {} });
      
      const lines = client._buildFilterCodeLines([
        { operator: 'in_range', factor: { name: 'pe_ratio' }, rhs: [5, 20] }
      ]);
      
      assert.ok(lines.includes('[5,20]'));
    });

    it('should return empty string for empty array', () => {
      const client = new WizardClient({ sessionPayload: {} });
      
      const lines = client._buildFilterCodeLines([]);
      
      assert.strictEqual(lines, '');
    });
  });

  describe('_buildSortingCodeLines', () => {
    it('should build sorting code lines', () => {
      const client = new WizardClient({ sessionPayload: {} });
      
      const lines = client._buildSortingCodeLines([
        { factor: { type: 'fundamental', name: 'pe_ratio' }, ascending: true, weight: 0.5 }
      ]);
      
      assert.ok(lines.includes("'name': 'pe_ratio'"));
      assert.ok(lines.includes("'ascending': True"));
      assert.ok(lines.includes("'weight': 0.5"));
    });

    it('should handle ascending: false', () => {
      const client = new WizardClient({ sessionPayload: {} });
      
      const lines = client._buildSortingCodeLines([
        { factor: { name: 'market_cap' }, ascending: false }
      ]);
      
      assert.ok(lines.includes("'ascending': False"));
    });

    it('should default ascending to True', () => {
      const client = new WizardClient({ sessionPayload: {} });
      
      const lines = client._buildSortingCodeLines([
        { factor: { name: 'pe_ratio' } }
      ]);
      
      assert.ok(lines.includes("'ascending': True"));
    });
  });

  describe('_commonCodeHeader', () => {
    it('should generate header with config values', () => {
      const client = new WizardClient({ sessionPayload: {} });
      
      const header = client._commonCodeHeader({
        universe: ['000905.XSHG'],
        industries: ['金融'],
        board: ['主板'],
        stOption: 'include',
        risk: { profitTaking: 0.2, stopLoss: -0.1 }
      });
      
      assert.ok(header.includes('import numpy as np'));
      assert.ok(header.includes('UNIVERSE = ["000905.XSHG"]'));
      assert.ok(header.includes('INDUSTRIES = ["金融"]'));
      assert.ok(header.includes('BOARDS = ["主板"]'));
      assert.ok(header.includes("ST_OPTION = 'include'"));
      assert.ok(header.includes('SINGLE_PROFIT_TAKEN = 0.2'));
      assert.ok(header.includes('SINGLE_STOP_LOSS = -0.1'));
    });

    it('should use defaults when not provided', () => {
      const client = new WizardClient({ sessionPayload: {} });
      
      const header = client._commonCodeHeader({});
      
      assert.ok(header.includes('UNIVERSE = ["000300.XSHG"]'));
      assert.ok(header.includes('INDUSTRIES = ["*"]'));
      assert.ok(header.includes('BOARDS = ["*"]'));
      assert.ok(header.includes("ST_OPTION = 'exclude'"));
      assert.ok(header.includes('SINGLE_PROFIT_TAKEN = None'));
      assert.ok(header.includes('SINGLE_STOP_LOSS = None'));
    });
  });

  describe('_generateSinglePeriodCode', () => {
    it('should generate complete single period code', () => {
      const client = new WizardClient({ sessionPayload: {} });
      
      const code = client._generateSinglePeriodCode({
        universe: ['000300.XSHG'],
        maxHoldingNum: 10,
        rebalanceInterval: 5,
        filters: [
          { operator: 'greater_than', factor: { type: 'fundamental', name: 'pe_ratio' }, rhs: 5 }
        ],
        sorting: [
          { factor: { type: 'fundamental', name: 'pe_ratio' }, ascending: true }
        ]
      });
      
      assert.ok(code.includes('import numpy as np'));
      assert.ok(code.includes('import pandas as pd'));
      assert.ok(code.includes('def init(context)'));
      assert.ok(code.includes('def handle_bar'));
      assert.ok(code.includes('FILTERS = ['));
      assert.ok(code.includes('SORTING_RULES = ['));
    });
  });

  describe('_generateThreePeriodsCode', () => {
    it('should generate complete three periods code', () => {
      const client = new WizardClient({ sessionPayload: {} });
      
      const code = client._generateThreePeriodsCode({
        universe: ['000300.XSHG'],
        maxHoldingNum: 10,
        maxHoldingPercent: 0.2,
        rebalanceInterval: 5,
        buy: {
          rebalanceInterval: 1,
          filters: []
        },
        sell: {
          rebalanceInterval: 1,
          filters: []
        }
      });
      
      assert.ok(code.includes('MAX_HOLDING_PERCENT = 0.2'));
      assert.ok(code.includes('BUY_REBALANCE_INTERVAL = 1'));
      assert.ok(code.includes('SELL_REBALANCE_INTERVAL = 1'));
      assert.ok(code.includes('BUY_FILTERS = ['));
      assert.ok(code.includes('SELL_FILTERS = ['));
      assert.ok(code.includes('def sell_rebalance'));
      assert.ok(code.includes('def buy_rebalance'));
    });
  });

  describe('saveReport', () => {
    it('should save report to file and return path', async () => {
      const testDir = path.join(os.tmpdir(), `wizard-report-test-${Date.now()}`);
      fs.mkdirSync(testDir, { recursive: true });
      
      const { WizardClient: WC, saveJson } = await import('../request/wizard-client.js?' + Date.now());
      
      const client = new WC();
      const report = { backtestId: 'bt-test-1', status: 'finished' };
      
      const filePath = client.saveReport('bt-test-1', report);
      
      assert.ok(filePath.includes('report-bt-test-1'));
      assert.ok(filePath.endsWith('.json'));
      
      fs.rmSync(testDir, { recursive: true, force: true });
    });
  });
});