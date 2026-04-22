import { jest } from '@jest/globals';

jest.unstable_mockModule('node:fs', () => ({
  existsSync: () => true,
  readFileSync: () => 'print("test code")',
  writeFileSync: () => {},
  mkdirSync: () => {}
}));

jest.unstable_mockModule('node:path', () => ({
  basename: (p, ext) => p.split('/').pop().replace(ext || '', ''),
  dirname: () => '/mock/dir',
  join: (...args) => args.join('/')
}));

jest.unstable_mockModule('../request/bigquant-auth.js', () => ({
  ensureSession: async () => ({
    cookies: [{ name: 'bigjwt', value: 'test-jwt', domain: '.bigquant.com' }],
    userId: 'test-user-id'
  })
}));

jest.unstable_mockModule('../request/bigquant-client.js', () => ({
  BigQuantClient: class MockBigQuantClient {
    constructor() {}
    async activateStudio() { return 'active'; }
    async sleep() { return; }
    buildNotebook(code) { return { cells: [], metadata: {}, nbformat: 4 }; }
    async createTask(name, notebook, config) { return 'task-123'; }
    async triggerTask(taskId) { return 'run-456'; }
    async waitForCompletion(taskId, timeoutMs) { return { success: true, state: 'completed' }; }
    async getNotebookOutputs(taskId) { return [{ output_type: 'stream', text: '总收益率: 15.5%\n年化收益率: 12.3%' }]; }
    async getLogs(runId) { return ['日志行1', '日志行2']; }
    writeArtifact(name, data) { return '/mock/result.json'; }
  }
}));

jest.unstable_mockModule('../load-env.js', () => ({}));
jest.unstable_mockModule('../../common/http-security.js', () => ({
  USER_AGENT: 'test-user-agent',
  SEC_CH_UA: 'test-sec-ch-ua',
  SecureHttpClient: class {}
}), { virtual: true });

jest.unstable_mockModule('../paths.js', () => ({
  OUTPUT_ROOT: '/mock/output'
}), { virtual: true });

const { runStrategyTest } = await import('../request/strategy-runner.js');

describe('strategy-runner', () => {
  describe('runStrategyTest', () => {
    it('should run complete strategy test workflow', async () => {
      const result = await runStrategyTest({
        cellSource: 'print("hello")',
        startDate: '2023-01-01',
        endDate: '2023-12-31',
        capital: 100000
      });

      expect(result.taskId).toBe('task-123');
      expect(result.runId).toBe('run-456');
      expect(result.success).toBe(true);
      expect(result.state).toBe('completed');
      expect(result.resultFile).toBe('/mock/result.json');
    });

    it('should return correct result structure', async () => {
      const result = await runStrategyTest({
        cellSource: 'test code'
      });

      expect(result).toHaveProperty('taskId');
      expect(result).toHaveProperty('runId');
      expect(result).toHaveProperty('taskName');
      expect(result).toHaveProperty('success');
      expect(result).toHaveProperty('state');
      expect(result).toHaveProperty('metrics');
      expect(result).toHaveProperty('executions');
      expect(result).toHaveProperty('textOutput');
      expect(result).toHaveProperty('outputs');
      expect(result).toHaveProperty('logs');
    });

    it('should handle cellSource string', async () => {
      const result = await runStrategyTest({
        cellSource: '# 测试策略\nprint("test")'
      });

      expect(result.taskName).toBeDefined();
    });

    it('should handle custom config options', async () => {
      const result = await runStrategyTest({
        cellSource: 'test',
        startDate: '2022-01-01',
        endDate: '2022-12-31',
        capital: 500000,
        benchmark: '000001.XSHG',
        frequency: 'minute'
      });

      expect(result.taskId).toBe('task-123');
    });

    it('should generate taskName with timestamp', async () => {
      const result = await runStrategyTest({
        cellSource: 'test'
      });

      expect(result.taskName).toMatch(/strategy_\d+/);
    });

    it('should use explicit taskName when provided', async () => {
      const result = await runStrategyTest({
        cellSource: 'test',
        taskName: 'explicit-task-name'
      });

      expect(result.taskName).toBe('explicit-task-name');
    });

    it('should return metrics object', async () => {
      const result = await runStrategyTest({ cellSource: 'test' });
      expect(result.metrics).toBeDefined();
    });

    it('should set ok status for normal output', async () => {
      const result = await runStrategyTest({ cellSource: 'test' });

      expect(result.executions[0].status).toBe('ok');
    });
  });
});