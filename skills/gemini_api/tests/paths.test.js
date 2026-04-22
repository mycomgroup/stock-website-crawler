import { describe, it, beforeEach, afterEach, mock } from 'node:test';
import assert from 'node:assert';
import { join, dirname, basename, isAbsolute } from 'node:path';

describe('paths.js', () => {
  let originalMetaUrl;
  let paths;

  beforeEach(() => {
    originalMetaUrl = import.meta.url;
  });

  afterEach(() => {
    mock.restoreAll();
  });

  describe('PATHS object structure', () => {
    it('should export PATHS object', async () => {
      paths = await import('../paths.js');
      assert.ok(paths.PATHS, 'PATHS should be exported');
      assert.strictEqual(typeof paths.PATHS, 'object');
    });

    it('should have all required path properties', async () => {
      paths = await import('../paths.js');
      const requiredProps = [
        'root',
        'data',
        'browser',
        'request',
        'examples',
        'sessionFile',
        'conversationsFile',
        'userDataDir'
      ];
      
      for (const prop of requiredProps) {
        assert.ok(prop in paths.PATHS, `PATHS should have ${prop} property`);
      }
    });

    it('should have root pointing to gemini_api directory', async () => {
      paths = await import('../paths.js');
      const rootDir = basename(paths.PATHS.root);
      assert.strictEqual(rootDir, 'gemini_api', 'root should point to gemini_api directory');
    });
  });

  describe('directory paths', () => {
    it('should have data path as subdirectory of root', async () => {
      paths = await import('../paths.js');
      assert.strictEqual(paths.PATHS.data, join(paths.PATHS.root, 'data'));
    });

    it('should have browser path as subdirectory of root', async () => {
      paths = await import('../paths.js');
      assert.strictEqual(paths.PATHS.browser, join(paths.PATHS.root, 'browser'));
    });

    it('should have request path as subdirectory of root', async () => {
      paths = await import('../paths.js');
      assert.strictEqual(paths.PATHS.request, join(paths.PATHS.root, 'request'));
    });

    it('should have examples path as subdirectory of root', async () => {
      paths = await import('../paths.js');
      assert.strictEqual(paths.PATHS.examples, join(paths.PATHS.root, 'examples'));
    });
  });

  describe('file paths', () => {
    it('should have sessionFile as relative path from gemini_api', async () => {
      paths = await import('../paths.js');
      assert.ok(
        paths.PATHS.sessionFile.includes('.sessions') && paths.PATHS.sessionFile.includes('gemini.json'),
        'sessionFile should contain .sessions and gemini.json'
      );
    });

    it('should have conversationsFile as subdirectory of data', async () => {
      paths = await import('../paths.js');
      assert.strictEqual(
        paths.PATHS.conversationsFile, 
        join(paths.PATHS.data, 'conversations.json')
      );
    });

    it('should have userDataDir as subdirectory of data', async () => {
      paths = await import('../paths.js');
      assert.strictEqual(
        paths.PATHS.userDataDir, 
        join(paths.PATHS.data, 'browser-profile')
      );
    });
  });

  describe('path validation', () => {
    it('should have all string values', async () => {
      paths = await import('../paths.js');
      for (const [key, value] of Object.entries(paths.PATHS)) {
        assert.strictEqual(typeof value, 'string', `${key} should be a string`);
      }
    });

    it('should have non-empty string values', async () => {
      paths = await import('../paths.js');
      for (const [key, value] of Object.entries(paths.PATHS)) {
        assert.ok(value.length > 0, `${key} should not be empty`);
      }
    });

    it('should have valid path separators', async () => {
      paths = await import('../paths.js');
      for (const [key, value] of Object.entries(paths.PATHS)) {
        if (key !== 'root') {
          const parentDir = dirname(value);
          assert.ok(
            parentDir.length > 0,
            `${key} should have a valid parent directory`
          );
        }
      }
    });
  });
});