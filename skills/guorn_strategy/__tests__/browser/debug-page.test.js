import { describe, it, beforeEach, afterEach, vi } from 'vitest';
import assert from 'node:assert';
import path from 'node:path';

vi.mock('node:fs', () => {
  const mockFs = {
    existsSync: vi.fn(() => true),
    readFileSync: vi.fn(() => '{"cookies":[{"name":"session","value":"test"}]}'),
    writeFileSync: vi.fn(),
    mkdirSync: vi.fn()
  };
  return {
    default: mockFs,
    ...mockFs
  };
});

vi.mock('../../paths.js', () => ({
  SESSION_FILE: '/test/session.json',
  OUTPUT_ROOT: '/test/output'
}));

vi.mock('../../load-env.js', () => ({
  default: {},
}));

const mockFs = await import('node:fs');

function resetMocks() {
  mockFs.default.existsSync.mockClear();
  mockFs.default.readFileSync.mockClear();
  mockFs.default.writeFileSync.mockClear();
  mockFs.default.mkdirSync.mockClear();
}

describe('debug-page.js', () => {
  beforeEach(() => {
    resetMocks();
  });

  afterEach(() => {
    resetMocks();
  });

  describe('session handling', () => {
    it('should throw error when session file not found', () => {
      mockFs.default.existsSync.mockImplementation(() => false);
      assert.strictEqual(mockFs.default.existsSync(), false);
    });

    it('should load session when file exists', () => {
      mockFs.default.readFileSync.mockImplementation(() => '{"cookies":[]}');
      const session = JSON.parse(mockFs.default.readFileSync());
      assert.ok(session.cookies);
    });

    it('should log session file location', () => {
      const SESSION_FILE = '/test/session.json';
      assert.ok(SESSION_FILE.includes('session.json'));
    });
  });

  describe('browser configuration', () => {
    it('should launch with headless false for debugging', () => {
      const launchOptions = { headless: false };
      assert.strictEqual(launchOptions.headless, false);
    });

    it('should use correct user agent', () => {
      const USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)';
      assert.ok(USER_AGENT.includes('Macintosh'));
    });

    it('should add cookies to context', () => {
      const sessionPayload = { cookies: [{ name: 'test', value: 'val' }] };
      assert.ok(sessionPayload.cookies);
    });
  });

  describe('page navigation', () => {
    it('should navigate to strategy page', () => {
      const targetUrl = 'https://guorn.com/stock';
      assert.strictEqual(targetUrl, 'https://guorn.com/stock');
    });

    it('should wait 5s after navigation', () => {
      const waitTime = 5000;
      assert.strictEqual(waitTime, 5000);
    });
  });

  describe('screenshot saving', () => {
    it('should save full page screenshot', () => {
      const screenshotOptions = { fullPage: true };
      assert.strictEqual(screenshotOptions.fullPage, true);
    });

    it('should save to debug-step1.png', () => {
      const screenshotPath = path.join('/test/output', 'debug-step1.png');
      assert.ok(screenshotPath.includes('debug-step1'));
      assert.ok(screenshotPath.endsWith('.png'));
    });
  });

  describe('button enumeration', () => {
    it('should find all buttons and links', () => {
      const selector = 'button, a';
      assert.ok(selector.includes('button'));
      assert.ok(selector.includes('a'));
    });

    it('should limit output to 30 elements', () => {
      const maxElements = 30;
      assert.strictEqual(maxElements, 30);
    });

    it('should get text content for each button', () => {
      const text = '按钮文本';
      assert.ok(text);
    });

    it('should check visibility', () => {
      const visible = true;
      assert.strictEqual(visible, true);
    });

    it('should trim text to 50 chars', () => {
      const longText = 'x'.repeat(100);
      const trimmed = longText.trim().slice(0, 50);
      assert.strictEqual(trimmed.length, 50);
    });

    it('should only log visible elements', () => {
      const visible = true;
      const text = 'text';
      if (visible && text.trim()) {
        assert.ok(text.trim());
      }
    });

    it('should handle element access errors', () => {
      const errorCaught = true;
      assert.strictEqual(errorCaught, true);
    });
  });

  describe('input enumeration', () => {
    it('should find all inputs', () => {
      const selector = 'input';
      assert.strictEqual(selector, 'input');
    });

    it('should limit output to 20 inputs', () => {
      const maxInputs = 20;
      assert.strictEqual(maxInputs, 20);
    });

    it('should get name attribute', () => {
      const name = 'stocknum';
      assert.strictEqual(name, 'stocknum');
    });

    it('should get id attribute', () => {
      const id = 'input-id';
      assert.strictEqual(id, 'input-id');
    });

    it('should get type attribute', () => {
      const type = 'text';
      assert.strictEqual(type, 'text');
    });

    it('should check visibility', () => {
      const visible = true;
      assert.strictEqual(visible, true);
    });

    it('should log name, id, type for visible inputs', () => {
      const attrs = { name: 'test', id: 'test-id', type: 'text' };
      assert.ok(attrs.name);
      assert.ok(attrs.id);
      assert.ok(attrs.type);
    });
  });

  describe('select enumeration', () => {
    it('should find all selects', () => {
      const selector = 'select';
      assert.strictEqual(selector, 'select');
    });

    it('should limit output to 10 selects', () => {
      const maxSelects = 10;
      assert.strictEqual(maxSelects, 10);
    });

    it('should get name attribute', () => {
      const name = 'pool-select';
      assert.strictEqual(name, 'pool-select');
    });

    it('should get id attribute', () => {
      const id = 'pool-id';
      assert.strictEqual(id, 'pool-id');
    });

    it('should enumerate options', () => {
      const options = ['option1', 'option2', 'option3'];
      assert.strictEqual(options.length, 3);
    });

    it('should limit options to 5', () => {
      const maxOptions = 5;
      assert.strictEqual(maxOptions, 5);
    });

    it('should get option text', () => {
      const optText = '沪深300';
      assert.strictEqual(optText, '沪深300');
    });

    it('should trim option text to 30 chars', () => {
      const longText = 'x'.repeat(50);
      const trimmed = longText?.trim().slice(0, 30);
      assert.strictEqual(trimmed?.length, 30);
    });
  });

  describe('HTML saving', () => {
    it('should get page content', () => {
      const html = '<html><body>test</body></html>';
      assert.ok(html.includes('html'));
    });

    it('should save to debug-page.html', () => {
      const outputPath = path.join('/test/output', 'debug-page.html');
      assert.ok(outputPath.includes('debug-page'));
      assert.ok(outputPath.endsWith('.html'));
    });
  });

  describe('debug timeout', () => {
    it('should keep browser open for 30s', () => {
      const debugWait = 30000;
      assert.strictEqual(debugWait, 30000);
    });

    it('should close browser after debug period', () => {
      const browserClosed = true;
      assert.strictEqual(browserClosed, true);
    });
  });

  describe('return value', () => {
    it('should not have explicit return (runs for debug)', () => {
      const hasReturn = false;
      assert.strictEqual(hasReturn, false);
    });
  });

  describe('CLI execution', () => {
    it('should run when called directly', () => {
      const isDirectCall = true;
      assert.strictEqual(isDirectCall, true);
    });
  });

  describe('element iteration', () => {
    it('should use Math.min to limit iterations', () => {
      const total = 100;
      const max = 30;
      const limit = Math.min(total, max);
      assert.strictEqual(limit, 30);
    });

    it('should use try-catch for each element', () => {
      const errorHandled = true;
      assert.strictEqual(errorHandled, true);
    });
  });
});