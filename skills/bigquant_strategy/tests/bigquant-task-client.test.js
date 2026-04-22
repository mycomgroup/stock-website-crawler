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
    async request(method, endpoint, body) {
      if (endpoint.includes('resourcespecs')) {
        return { data: [{ id: 'spec-1' }] };
      }
      return { data: { id: 'task-id', username: 'testuser' } };
    }
    writeArtifact(name, data) { return '/mock/output/file.json'; }
  }
}));

jest.unstable_mockModule('../load-env.js', () => ({}));

const { BigQuantTaskClient } = await import('../request/bigquant-task-client.js');

describe('BigQuantTaskClient', () => {
  let client;

  beforeEach(() => {
    jest.clearAllMocks();
    client = new BigQuantTaskClient({ studioId: 'test-studio-id' });
  });

  describe('constructor', () => {
    it('should set studioId from options', () => {
      expect(client.studioId).toBe('test-studio-id');
    });
  });

  describe('checkLogin', () => {
    it('should call checkLogin method', async () => {
      const result = await client.checkLogin();
      expect(result).toBeDefined();
      expect(result).toHaveProperty('loggedIn');
    });
  });

  describe('getResourceSpecs', () => {
    it('should request resource specs', async () => {
      const result = await client.getResourceSpecs();
      expect(result).toBeDefined();
    });
  });

  describe('createTask', () => {
    it('should create task', async () => {
      const result = await client.createTask('test-task', 'print("hello")');
      expect(result.taskId).toBe('task-id');
    });
  });

  describe('updateTaskCode', () => {
    it('should update task code', async () => {
      const result = await client.updateTaskCode('task-123', 'new code');
      expect(result).toBeDefined();
    });
  });

  describe('updateTaskName', () => {
    it('should update task name', async () => {
      const result = await client.updateTaskName('task-123', 'new-name');
      expect(result).toBeDefined();
    });
  });

  describe('runTask', () => {
    it('should create taskrun', async () => {
      const result = await client.runTask('task-123');
      expect(result.taskrunId).toBe('task-id');
    });
  });

  describe('getTaskRunById', () => {
    it('should get taskrun by id', async () => {
      const result = await client.getTaskRunById('run-123');
      expect(result).toBeDefined();
    });
  });

  describe('getTaskRuns', () => {
    it('should get task runs', async () => {
      const result = await client.getTaskRuns('task-123');
      expect(result).toBeDefined();
    });
  });

  describe('createNotebookJSON', () => {
    it('should create valid notebook JSON', () => {
      const notebook = client.createNotebookJSON('print("hello")');
      expect(notebook.nbformat).toBe(4);
      expect(notebook.cells).toHaveLength(1);
    });

    it('should split multi-line code', () => {
      const notebook = client.createNotebookJSON('line1\nline2');
      expect(notebook.cells[0].source).toEqual(['line1\n', 'line2']);
    });
  });

  describe('getTaskWebUrl', () => {
    it('should generate web URL', async () => {
      const url = await client.getTaskWebUrl('task-456');
      expect(url).toContain('bigquant.com');
      expect(url).toContain('task-456');
    });
  });

  describe('runStrategy', () => {
    it('should run complete workflow', async () => {
      const result = await client.runStrategy('test-strategy', 'print("test")');
      expect(result.taskId).toBeDefined();
      expect(result.webUrl).toBeDefined();
    });
  });
});