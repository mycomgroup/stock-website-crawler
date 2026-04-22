import { describe, it, expect, jest, beforeEach, afterEach } from '@jest/globals';
import path from 'node:path';

const mockDirname = '/mock/dir';
jest.unstable_mockModule('node:url', () => ({
  fileURLToPath: jest.fn(() => '/mock/dir/paths.js')
}));

jest.unstable_mockModule('node:path', () => ({
  dirname: jest.fn(() => mockDirname),
  join: jest.fn((...args) => args.join('/'))
}));

const { OUTPUT_ROOT, SESSION_FILE, CONTRACT_FILE, RAW_CAPTURE_FILE } = await import('../paths.js');

describe('paths.js', () => {
  describe('OUTPUT_ROOT', () => {
    it('should be defined', () => {
      expect(OUTPUT_ROOT).toBeDefined();
    });

    it('should be a string', () => {
      expect(typeof OUTPUT_ROOT).toBe('string');
    });

    it('should contain "data" in path', () => {
      expect(OUTPUT_ROOT).toContain('data');
    });
  });

  describe('SESSION_FILE', () => {
    it('should be defined', () => {
      expect(SESSION_FILE).toBeDefined();
    });

    it('should be a string', () => {
      expect(typeof SESSION_FILE).toBe('string');
    });

    it('should contain session file name', () => {
      expect(SESSION_FILE).toContain('.json');
    });
  });

  describe('CONTRACT_FILE', () => {
    it('should be defined', () => {
      expect(CONTRACT_FILE).toBeDefined();
    });

    it('should be a string', () => {
      expect(typeof CONTRACT_FILE).toBe('string');
    });

    it('should contain notebook-contract.json', () => {
      expect(CONTRACT_FILE).toContain('notebook-contract.json');
    });
  });

  describe('RAW_CAPTURE_FILE', () => {
    it('should be defined', () => {
      expect(RAW_CAPTURE_FILE).toBeDefined();
    });

    it('should be a string', () => {
      expect(typeof RAW_CAPTURE_FILE).toBe('string');
    });

    it('should contain raw-capture.json', () => {
      expect(RAW_CAPTURE_FILE).toContain('raw-capture.json');
    });
  });

  describe('path consistency', () => {
    it('CONTRACT_FILE should be under OUTPUT_ROOT', () => {
      expect(CONTRACT_FILE).toContain('data');
    });

    it('RAW_CAPTURE_FILE should be under OUTPUT_ROOT', () => {
      expect(RAW_CAPTURE_FILE).toContain('data');
    });
  });
});