import { jest } from '@jest/globals';
import AlltickApiParser from '../src/parsers/alltick-api-parser.js';

describe('AlltickApiParser', () => {
  let parser;

  beforeEach(() => {
    parser = new AlltickApiParser();
  });

  test('should match alltick docs URLs', () => {
    expect(parser.matches('https://apis.alltick.co/')).toBe(true);
    expect(parser.matches('https://apis.alltick.co/zh/quickstart')).toBe(true);
    expect(parser.matches('https://example.com/docs')).toBe(false);
  });

  test('should generate stable filenames', () => {
    expect(parser.generateFilename('https://apis.alltick.co/')).toBe('overview');
    expect(parser.generateFilename('https://apis.alltick.co/zh/quickstart')).toBe('zh_quickstart');
  });

  test('should format markdown table safely', () => {
    const lines = [];
    parser._formatTable(lines, [
      ['Field', 'Description'],
      ['symbol', 'A|B line1\nline2']
    ]);

    const markdown = lines.join('\n');
    expect(markdown).toContain('| Field | Description |');
    expect(markdown).toContain('A\\|B line1<br>line2');
  });

  test('waitForContent should not throw on timeout', async () => {
    const page = {
      waitForLoadState: jest.fn().mockRejectedValue(new Error('timeout')),
      waitForSelector: jest.fn(),
      waitForTimeout: jest.fn()
    };

    await expect(parser.waitForContent(page)).resolves.not.toThrow();
  });
});
