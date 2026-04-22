import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

describe('paths.js', () => {
  let paths;

  beforeEach(async () => {
    vi.resetModules();
    paths = await import('../paths.js');
  });

  afterEach(() => {
    vi.clearAllMocks();
  });

  it('should export SKILL_ROOT as the directory of paths.js', () => {
    const __dirname = dirname(fileURLToPath(import.meta.url));
    const expectedDir = resolve(__dirname, '..');
    expect(paths.SKILL_ROOT).toBe(expectedDir);
  });

  it('should export BROWSER_ROOT as SKILL_ROOT/browser', () => {
    expect(paths.BROWSER_ROOT).toBe(resolve(paths.SKILL_ROOT, 'browser'));
  });

  it('should export REQUEST_ROOT as SKILL_ROOT/request', () => {
    expect(paths.REQUEST_ROOT).toBe(resolve(paths.SKILL_ROOT, 'request'));
  });

  it('should export DATA_ROOT as SKILL_ROOT/data', () => {
    expect(paths.DATA_ROOT).toBe(resolve(paths.SKILL_ROOT, 'data'));
  });

  it('should export OUTPUT_ROOT as SKILL_ROOT/output', () => {
    expect(paths.OUTPUT_ROOT).toBe(resolve(paths.SKILL_ROOT, 'output'));
  });

  it('should export SESSION_FILE with expected path', () => {
    expect(typeof paths.SESSION_FILE).toBe('string');
    expect(paths.SESSION_FILE).toMatch(/\.json$/);
    expect(paths.SESSION_FILE).toContain('.sessions');
  });

  it('should export DEFAULT_STRATEGY_URL as guorn.com URL', () => {
    expect(paths.DEFAULT_STRATEGY_URL).toBe('https://guorn.com/stock');
  });

  it('all exported constants should be strings', () => {
    const exports = ['SKILL_ROOT', 'BROWSER_ROOT', 'REQUEST_ROOT', 'DATA_ROOT', 'OUTPUT_ROOT', 'SESSION_FILE', 'DEFAULT_STRATEGY_URL'];
    for (const exp of exports) {
      expect(typeof paths[exp]).toBe('string');
    }
  });

  it('SKILL_ROOT should be absolute path', () => {
    expect(paths.SKILL_ROOT).toMatch(/^\/|^[A-Z]:\\/);
  });

  it('BROWSER_ROOT should start with SKILL_ROOT', () => {
    expect(paths.BROWSER_ROOT.startsWith(paths.SKILL_ROOT)).toBe(true);
  });

  it('REQUEST_ROOT should start with SKILL_ROOT', () => {
    expect(paths.REQUEST_ROOT.startsWith(paths.SKILL_ROOT)).toBe(true);
  });

  it('DATA_ROOT should start with SKILL_ROOT', () => {
    expect(paths.DATA_ROOT.startsWith(paths.SKILL_ROOT)).toBe(true);
  });

  it('OUTPUT_ROOT should start with SKILL_ROOT', () => {
    expect(paths.OUTPUT_ROOT.startsWith(paths.SKILL_ROOT)).toBe(true);
  });

  it('should export exactly 7 constants', () => {
    const exportKeys = Object.keys(paths);
    expect(exportKeys.length).toBe(7);
  });
});