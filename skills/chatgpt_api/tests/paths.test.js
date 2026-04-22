import { describe, it } from 'node:test';
import assert from 'node:assert';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

describe('paths', () => {
  describe('PATHS object', () => {
    it('should export PATHS object', async () => {
      const { PATHS } = await import('../paths.js');
      
      assert.ok(PATHS);
      assert.ok(typeof PATHS === 'object');
    });

    it('should have root property', async () => {
      const { PATHS } = await import('../paths.js?cachebuster=' + Date.now());
      
      assert.ok(PATHS.root);
      assert.ok(typeof PATHS.root === 'string');
    });

    it('should have data property', async () => {
      const { PATHS } = await import('../paths.js?cachebuster=' + Date.now());
      
      assert.ok(PATHS.data);
      assert.ok(typeof PATHS.data === 'string');
    });

    it('should have browser property', async () => {
      const { PATHS } = await import('../paths.js?cachebuster=' + Date.now());
      
      assert.ok(PATHS.browser);
      assert.ok(typeof PATHS.browser === 'string');
    });

    it('should have request property', async () => {
      const { PATHS } = await import('../paths.js?cachebuster=' + Date.now());
      
      assert.ok(PATHS.request);
      assert.ok(typeof PATHS.request === 'string');
    });

    it('should have examples property', async () => {
      const { PATHS } = await import('../paths.js?cachebuster=' + Date.now());
      
      assert.ok(PATHS.examples);
      assert.ok(typeof PATHS.examples === 'string');
    });

    it('should have sessionFile property', async () => {
      const { PATHS } = await import('../paths.js?cachebuster=' + Date.now());
      
      assert.ok(PATHS.sessionFile);
      assert.ok(typeof PATHS.sessionFile === 'string');
    });

    it('should have conversationsFile property', async () => {
      const { PATHS } = await import('../paths.js?cachebuster=' + Date.now());
      
      assert.ok(PATHS.conversationsFile);
      assert.ok(typeof PATHS.conversationsFile === 'string');
    });

    it('should have userDataDir property', async () => {
      const { PATHS } = await import('../paths.js?cachebuster=' + Date.now());
      
      assert.ok(PATHS.userDataDir);
      assert.ok(typeof PATHS.userDataDir === 'string');
    });

    it('should have correct path structure', async () => {
      const { PATHS } = await import('../paths.js?cachebuster=' + Date.now());
      
      assert.ok(PATHS.data.includes('data'));
      assert.ok(PATHS.browser.includes('browser'));
      assert.ok(PATHS.request.includes('request'));
    });

    it('should have absolute paths', async () => {
      const { PATHS } = await import('../paths.js?cachebuster=' + Date.now());
      
      assert.ok(path.isAbsolute(PATHS.root));
      assert.ok(path.isAbsolute(PATHS.data));
      assert.ok(path.isAbsolute(PATHS.browser));
      assert.ok(path.isAbsolute(PATHS.request));
    });

    it('should have consistent directory hierarchy', async () => {
      const { PATHS } = await import('../paths.js?cachebuster=' + Date.now());
      
      assert.ok(PATHS.data.startsWith(PATHS.root));
      assert.ok(PATHS.browser.startsWith(PATHS.root));
      assert.ok(PATHS.request.startsWith(PATHS.root));
    });
  });
});