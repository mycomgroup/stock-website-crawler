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
  resolve: (...args) => args.join('/'),
  basename: (p, ext) => p.split('/').pop().replace(ext || '', '')
}));

jest.unstable_mockModule('node:url', () => ({
  fileURLToPath: () => '/mock/path'
}));

jest.unstable_mockModule('../request/bigquant-api-client.js', () => ({
  BigQuantAPIClient: class MockBigQuantAPIClient {
    constructor(options) {
      this.sessionPayload = options.sessionPayload || { userId: 'test-user-id' };
      this.studioId = options.studioId;
    }
    async request(method, endpoint, body) { return { data: { id: 'task-id' } }; }
    async createTask(data) { return { data: { id: 'task-id' } }; }
    async getTask(id) { return { data: { last_run: { state: 'success' } } }; }
    async getTaskResult(id) { return { data: {} }; }
    writeArtifact(name, data) { return '/mock/output/file.json'; }
  }
}));

jest.unstable_mockModule('../load-env.js', () => ({}));
jest.unstable_mockModule('../paths.js', () => ({ OUTPUT_ROOT: '/mock/output' }), { virtual: true });

describe('BigQuantNotebookClient', () => {
  let client;

  beforeEach(async () => {
    jest.clearAllMocks();
    const { BigQuantNotebookClient } = await import('../request/bigquant-notebook-client.js');
    client = new BigQuantNotebookClient({ studioId: 'test-studio-id' });
  });

  describe('constructor', () => {
    it('should set studioId from options', () => {
      expect(client.studioId).toBe('test-studio-id');
    });

    it('should set baseUrl from studioId', () => {
      expect(client.baseUrl).toBe('/aistudio/studios/test-studio-id/');
    });
  });

  describe('createNotebookJSON', () => {
    it('should create notebook from string cells', () => {
      const notebook = client.createNotebookJSON(['print("hello")', 'print("world")']);
      expect(notebook.cells).toHaveLength(2);
    });

    it('should handle cell objects', () => {
      const cellObj = { cell_type: 'markdown', source: ['# Title'] };
      const notebook = client.createNotebookJSON([cellObj]);
      expect(notebook.cells[0]).toEqual(cellObj);
    });

    it('should split multi-line strings correctly', () => {
      const notebook = client.createNotebookJSON(['line1\nline2\nline3']);
      expect(notebook.cells[0].source).toEqual(['line1\n', 'line2\n', 'line3']);
    });

    it('should create valid notebook structure', () => {
      const notebook = client.createNotebookJSON([]);
      expect(notebook.nbformat).toBe(4);
      expect(notebook.metadata.kernelspec.name).toBe('python3');
    });
  });

  describe('createTaskRun', () => {
    it('should create taskrun', async () => {
      const result = await client.createTaskRun('task-123');
      expect(result).toBeDefined();
    });
  });

  describe('getTaskRun', () => {
    it('should get taskrun by id', async () => {
      const result = await client.getTaskRun('run-123');
      expect(result).toBeDefined();
    });
  });

  describe('listTaskRuns', () => {
    it('should list taskruns for a task', async () => {
      const result = await client.listTaskRuns('task-123');
      expect(result).toBeDefined();
    });
  });

  describe('createAndRunBacktest', () => {
    it('should create task and taskrun', async () => {
      const result = await client.createAndRunBacktest({
        code: 'print("test")',
        name: 'test-backtest'
      });
      expect(result.taskId).toBe('task-id');
    });
  });

  describe('executeCode', () => {
    it('should execute code', async () => {
      const result = await client.executeCode('print("hello")');
      expect(result.taskId).toBe('task-id');
    });
  });

  describe('waitForResult', () => {
    beforeEach(() => {
      jest.useFakeTimers();
    });

    afterEach(() => {
      jest.useRealTimers();
    });

    it('should return success', async () => {
      const promise = client.waitForResult('task-123', 10000);
      await jest.runAllTimersAsync();
      const result = await promise;
      expect(result.success).toBe(true);
    });
  });

  describe('runBacktest', () => {
    it('should run backtest workflow', async () => {
      const result = await client.runBacktest('print("test")', {
        name: 'test-backtest'
      });
      expect(result.taskId).toBe('task-id');
      expect(result.webUrl).toBeDefined();
    });
  });
});