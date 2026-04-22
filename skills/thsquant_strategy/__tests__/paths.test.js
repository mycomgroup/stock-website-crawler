import { describe, it, expect } from 'vitest';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
import { OUTPUT_ROOT, SESSION_FILE, CONTRACT_FILE, RAW_CAPTURE_FILE } from '../paths.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const parentDir = dirname(__dirname);

describe('paths.js', () => {
  describe('OUTPUT_ROOT', () => {
    it('should be defined as a string', () => {
      expect(OUTPUT_ROOT).toBeDefined();
      expect(typeof OUTPUT_ROOT).toBe('string');
    });

    it('should point to data directory relative to paths.js', () => {
      expect(OUTPUT_ROOT).toBe(join(parentDir, 'data'));
    });

    it('should be an absolute path', () => {
      expect(OUTPUT_ROOT).toBe(require('node:path').resolve(OUTPUT_ROOT));
    });
  });

  describe('SESSION_FILE', () => {
    it('should be defined as a string', () => {
      expect(SESSION_FILE).toBeDefined();
      expect(typeof SESSION_FILE).toBe('string');
    });

    it('should be an absolute path', () => {
      expect(SESSION_FILE.startsWith('/')).toBe(true);
    });

    it('should point to thsquant.json session file', () => {
      expect(SESSION_FILE.endsWith('thsquant.json')).toBe(true);
    });

    it('should be located in .sessions directory', () => {
      expect(SESSION_FILE).toContain('.sessions');
    });
  });

  describe('CONTRACT_FILE', () => {
    it('should be defined as a string', () => {
      expect(CONTRACT_FILE).toBeDefined();
      expect(typeof CONTRACT_FILE).toBe('string');
    });

    it('should be located in OUTPUT_ROOT directory', () => {
      expect(CONTRACT_FILE).toBe(join(OUTPUT_ROOT, 'notebook-contract.json'));
    });

    it('should have notebook-contract.json as filename', () => {
      expect(CONTRACT_FILE.endsWith('notebook-contract.json')).toBe(true);
    });
  });

  describe('RAW_CAPTURE_FILE', () => {
    it('should be defined as a string', () => {
      expect(RAW_CAPTURE_FILE).toBeDefined();
      expect(typeof RAW_CAPTURE_FILE).toBe('string');
    });

    it('should be located in OUTPUT_ROOT directory', () => {
      expect(RAW_CAPTURE_FILE).toBe(join(OUTPUT_ROOT, 'raw-capture.json'));
    });

    it('should have raw-capture.json as filename', () => {
      expect(RAW_CAPTURE_FILE.endsWith('raw-capture.json')).toBe(true);
    });
  });

  describe('path relationships', () => {
    it('CONTRACT_FILE and RAW_CAPTURE_FILE should be in same directory', () => {
      const contractDir = dirname(CONTRACT_FILE);
      const rawCaptureDir = dirname(RAW_CAPTURE_FILE);
      expect(contractDir).toBe(rawCaptureDir);
    });

    it('CONTRACT_FILE and RAW_CAPTURE_FILE should be in OUTPUT_ROOT', () => {
      expect(dirname(CONTRACT_FILE)).toBe(OUTPUT_ROOT);
      expect(dirname(RAW_CAPTURE_FILE)).toBe(OUTPUT_ROOT);
    });
  });
});