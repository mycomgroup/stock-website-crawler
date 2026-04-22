import { jest } from '@jest/globals';

jest.unstable_mockModule('node:fs', () => ({
  existsSync: () => true,
  mkdirSync: () => {},
  readFileSync: () => '{}',
  writeFileSync: () => {}
}));

jest.unstable_mockModule('node:fs/promises', () => ({
  readFile: async () => '{}',
  writeFile: async () => {},
  mkdir: async () => {},
  unlink: async () => {}
}));

jest.unstable_mockModule('node:path', () => ({
  dirname: (p) => p.split('/').slice(0, -1).join('/'),
  join: (...args) => args.join('/')
}));

jest.unstable_mockModule('../browser/capture-session.js', () => ({
  captureBigQuantSession: async () => ({
    cookies: [{ name: 'test', value: 'val' }]
  })
}));

jest.unstable_mockModule('../paths.js', () => ({
  SESSION_FILE: '/test/session.json',
  OUTPUT_ROOT: '/test/data'
}));

const { SessionManager } = await import('../lib/anti-detection.js');
const BrowserSessionManager = await import('../browser/session-manager.js').then(m => m.default || m.SessionManager || m);

describe('SessionManager', () => {
  describe('constructor', () => {
    it('should create session manager', () => {
      const manager = new SessionManager('/test/session.json');
      expect(manager.sessionFile).toBe('/test/session.json');
    });

    it('should use default maxAge', () => {
      const manager = new SessionManager('/test/session.json');
      expect(manager.maxAge).toBe(7 * 24 * 60 * 60 * 1000);
    });

    it('should use custom maxAge', () => {
      const manager = new SessionManager('/test/session.json', { maxAge: 1000 });
      expect(manager.maxAge).toBe(1000);
    });
  });

  describe('load', () => {
    it('should load session from file', async () => {
      const manager = new SessionManager('/test/session.json');
      const session = await manager.load();
      expect(session).toBeDefined();
    });
  });

describe('save', () => {
    it('should call save method', async () => {
      const manager = new SessionManager('/tmp/test-session.json');
      await manager.save({ cookies: [] });
    });
  });

  describe('isValid', () => {
    it('should check session validity', async () => {
      const manager = new SessionManager('/test/session.json');
      const valid = await manager.isValid();
      expect(typeof valid).toBe('boolean');
    });
  });

  describe('clear', () => {
    it('should clear session', async () => {
      const manager = new SessionManager('/test/session.json');
      await manager.clear();
    });
  });
});