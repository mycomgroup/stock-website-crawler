import { jest } from '@jest/globals';
import TableOnlyParser from '../src/parsers/table-only-parser.js';

describe('TableOnlyParser', () => {
  let parser;

  beforeEach(() => {
    parser = new TableOnlyParser();
  });

  test('matches always returns true', () => {
    expect(parser.matches('https://example.com')).toBe(true);
  });

  test('getPriority returns 5', () => {
    expect(parser.getPriority()).toBe(5);
  });

  test('isTableOnlyPage returns false when page evaluation throws', async () => {
    const page = {
      evaluate: async () => {
        throw new Error('dom error');
      }
    };

    await expect(parser.isTableOnlyPage(page)).resolves.toBe(false);
  });

  test('parse falls back to generic parser when page is not table-only', async () => {
    parser.isTableOnlyPage = jest.fn(async () => false);
    parser.genericParser.parse = jest.fn(async () => ({ type: 'generic' }));

    const result = await parser.parse({}, 'https://example.com/page');

    expect(parser.genericParser.parse).toHaveBeenCalled();
    expect(result).toEqual({ type: 'generic' });
  });

  test('parse falls back to generic parser when no tables extracted', async () => {
    parser.isTableOnlyPage = jest.fn(async () => true);
    parser.extractTitle = jest.fn(async () => 'Title');
    parser.genericParser.extractTablesWithPaginationAndVirtual = jest.fn(async () => []);
    parser.genericParser.parse = jest.fn(async () => ({ type: 'generic' }));

    const result = await parser.parse({}, 'https://example.com/page');

    expect(parser.genericParser.parse).toHaveBeenCalled();
    expect(result).toEqual({ type: 'generic' });
  });

  test('parse returns table-only payload when tables are available', async () => {
    const tables = [{ headers: ['h1'], rows: [['v1']] }];
    parser.isTableOnlyPage = jest.fn(async () => true);
    parser.extractTitle = jest.fn(async () => '表格页');
    parser.genericParser.extractTablesWithPaginationAndVirtual = jest.fn(async () => tables);

    const result = await parser.parse({}, 'https://example.com/table');

    expect(result.type).toBe('table-only');
    expect(result.title).toBe('表格页');
    expect(result.tables).toEqual(tables);
    expect(result.apiData).toBe(0);
  });
});
