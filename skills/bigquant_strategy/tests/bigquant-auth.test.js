import { jest } from '@jest/globals';

jest.unstable_mockModule('node:fs', () => ({
  existsSync: () => true,
  readFileSync: () => '{}',
  writeFileSync: () => {},
  mkdirSync: () => {}
}));

jest.unstable_mockModule('node:path', () => ({
  dirname: () => '/mock/dir',
  join: (...args) => args.join('/')
}));

jest.unstable_mockModule('../paths.js', () => ({
  SESSION_FILE: '/tmp/bigquant-test-session.json'
}));

const createMockJwt = (exp, userId) => {
  const header = Buffer.from(JSON.stringify({ alg: 'HS256' })).toString('base64');
  const payload = Buffer.from(JSON.stringify({ exp, user: { id: userId }, sub: userId })).toString('base64');
  return `${header}.${payload}.signature`;
};

const { isSessionValid, extractUserId } = await import('../request/bigquant-auth.js');

describe('bigquant-auth', () => {
  describe('isSessionValid', () => {
    it('returns true for valid session with valid JWT', () => {
      const futureExp = Math.floor(Date.now() / 1000) + 3600;
      const jwt = createMockJwt(futureExp, 'user-123');
      
      const result = isSessionValid({ cookies: [{ name: 'bigjwt', value: jwt }] });
      
      expect(result).toBe(true);
    });

    it('returns false for session without cookies', () => {
      const result = isSessionValid({});
      expect(result).toBe(false);
    });

    it('returns false for session without JWT cookie', () => {
      const result = isSessionValid({ cookies: [{ name: 'other', value: 'val' }] });
      expect(result).toBe(false);
    });

    it('returns false for expired JWT', () => {
      const pastExp = Math.floor(Date.now() / 1000) - 100;
      const jwt = createMockJwt(pastExp, 'user-123');
      
      const result = isSessionValid({ cookies: [{ name: 'bigjwt', value: jwt }] });
      expect(result).toBe(false);
    });

    it('returns false for malformed JWT', () => {
      const result = isSessionValid({ cookies: [{ name: 'bigjwt', value: 'invalid.jwt' }] });
      expect(result).toBe(false);
    });
  });

  describe('extractUserId', () => {
    it('extracts userId from session.userId', () => {
      const result = extractUserId({ userId: 'direct-user-id', cookies: [] });
      expect(result).toBe('direct-user-id');
    });

    it('extracts userId from JWT payload', () => {
      const futureExp = Math.floor(Date.now() / 1000) + 3600;
      const jwt = createMockJwt(futureExp, 'jwt-user-id');
      
      const result = extractUserId({ cookies: [{ name: 'bigjwt', value: jwt }] });
      expect(result).toBe('jwt-user-id');
    });

    it('extracts userId from biguid cookie', () => {
      const result = extractUserId({ cookies: [{ name: 'biguid', value: 'cookie-user-id' }] });
      expect(result).toBe('cookie-user-id');
    });

    it('returns null for empty session', () => {
      const result = extractUserId({});
      expect(result).toBeNull();
    });
  });
});