import { test, mock } from 'node:test';
import assert from 'node:assert';
import {
  validateEnv,
  validateScreenerQuery,
  buildBrowserQueryCatalogCandidates,
  parseBrowserNaturalLanguageQuery,
  mergePages,
  applyLimit,
  formatCsv,
  writeCsvFile
} from '../browser/main.js';

const mockCatalog = [
  { name: 'pe_ttm', displayName: '市盈率(TTM)', category: '估值', unit: '倍', operators: ['大于', '小于', '介于'] },
  { name: 'pb', displayName: '市净率', category: '估值', unit: '倍', operators: ['大于', '小于', '介于'] },
  { name: 'roe_ttm', displayName: '净资产收益率(TTM)', category: '盈利能力', unit: '%', operators: ['大于', '小于', '介于'] }
];

const mockConditionCatalog = {
  metrics: [
    { metric: 'PE-TTM(扣非)统计值', category: '估值', unit: '倍', selectors: [{ defaultLabel: '10年', options: [{ label: '10年', value: '10y' }] }] }
  ]
};

test.describe('validateEnv', () => {
  test('returns valid when all required env vars are set', () => {
    const originalUsername = process.env.LIXINGER_USERNAME;
    const originalPassword = process.env.LIXINGER_PASSWORD;
    process.env.LIXINGER_USERNAME = 'test_user';
    process.env.LIXINGER_PASSWORD = 'test_pass';
    
    const result = validateEnv();
    assert.strictEqual(result.valid, true);
    assert.deepStrictEqual(result.missing, []);
    
    process.env.LIXINGER_USERNAME = originalUsername;
    process.env.LIXINGER_PASSWORD = originalPassword;
  });

  test('returns invalid when LIXINGER_USERNAME is missing', () => {
    const originalUsername = process.env.LIXINGER_USERNAME;
    delete process.env.LIXINGER_USERNAME;
    
    const result = validateEnv();
    assert.strictEqual(result.valid, false);
    assert.deepStrictEqual(result.missing, ['LIXINGER_USERNAME']);
    
    if (originalUsername !== undefined) process.env.LIXINGER_USERNAME = originalUsername;
  });

  test('returns invalid when LIXINGER_PASSWORD is missing', () => {
    const originalPassword = process.env.LIXINGER_PASSWORD;
    delete process.env.LIXINGER_PASSWORD;
    
    const result = validateEnv();
    assert.strictEqual(result.valid, false);
    assert.deepStrictEqual(result.missing, ['LIXINGER_PASSWORD']);
    
    if (originalPassword !== undefined) process.env.LIXINGER_PASSWORD = originalPassword;
  });

  test('returns invalid when both required env vars are missing', () => {
    const originalUsername = process.env.LIXINGER_USERNAME;
    const originalPassword = process.env.LIXINGER_PASSWORD;
    delete process.env.LIXINGER_USERNAME;
    delete process.env.LIXINGER_PASSWORD;
    
    const result = validateEnv();
    assert.strictEqual(result.valid, false);
    assert.deepStrictEqual(result.missing.sort(), ['LIXINGER_PASSWORD', 'LIXINGER_USERNAME'].sort());
    
    if (originalUsername !== undefined) process.env.LIXINGER_USERNAME = originalUsername;
    if (originalPassword !== undefined) process.env.LIXINGER_PASSWORD = originalPassword;
  });

  test('requires LLM_API_KEY when requireLlm option is true', () => {
    const originalApiKey = process.env.LLM_API_KEY;
    const originalUsername = process.env.LIXINGER_USERNAME;
    const originalPassword = process.env.LIXINGER_PASSWORD;
    process.env.LIXINGER_USERNAME = 'test_user';
    process.env.LIXINGER_PASSWORD = 'test_pass';
    delete process.env.LLM_API_KEY;
    
    const result = validateEnv({ requireLlm: true });
    assert.strictEqual(result.valid, false);
    assert.deepStrictEqual(result.missing, ['LLM_API_KEY']);
    
    if (originalApiKey !== undefined) process.env.LLM_API_KEY = originalApiKey;
    if (originalUsername !== undefined) process.env.LIXINGER_USERNAME = originalUsername;
    if (originalPassword !== undefined) process.env.LIXINGER_PASSWORD = originalPassword;
  });

  test('returns valid when all env vars including LLM_API_KEY are set', () => {
    const originalUsername = process.env.LIXINGER_USERNAME;
    const originalPassword = process.env.LIXINGER_PASSWORD;
    const originalApiKey = process.env.LLM_API_KEY;
    process.env.LIXINGER_USERNAME = 'test_user';
    process.env.LIXINGER_PASSWORD = 'test_pass';
    process.env.LLM_API_KEY = 'test_key';
    
    const result = validateEnv({ requireLlm: true });
    assert.strictEqual(result.valid, true);
    assert.deepStrictEqual(result.missing, []);
    
    if (originalUsername !== undefined) process.env.LIXINGER_USERNAME = originalUsername;
    if (originalPassword !== undefined) process.env.LIXINGER_PASSWORD = originalPassword;
    if (originalApiKey !== undefined) process.env.LLM_API_KEY = originalApiKey;
  });

  test('handles empty options object', () => {
    const originalUsername = process.env.LIXINGER_USERNAME;
    const originalPassword = process.env.LIXINGER_PASSWORD;
    process.env.LIXINGER_USERNAME = 'test_user';
    process.env.LIXINGER_PASSWORD = 'test_pass';
    
    const result = validateEnv({});
    assert.strictEqual(result.valid, true);
    
    if (originalUsername !== undefined) process.env.LIXINGER_USERNAME = originalUsername;
    if (originalPassword !== undefined) process.env.LIXINGER_PASSWORD = originalPassword;
  });

  test('handles undefined options', () => {
    const originalUsername = process.env.LIXINGER_USERNAME;
    const originalPassword = process.env.LIXINGER_PASSWORD;
    process.env.LIXINGER_USERNAME = 'test_user';
    process.env.LIXINGER_PASSWORD = 'test_pass';
    
    const result = validateEnv(undefined);
    assert.strictEqual(result.valid, true);
    
    if (originalUsername !== undefined) process.env.LIXINGER_USERNAME = originalUsername;
    if (originalPassword !== undefined) process.env.LIXINGER_PASSWORD = originalPassword;
  });
});

test.describe('validateScreenerQuery', () => {
  test('returns valid for query with all fields in catalog', () => {
    const query = { filters: [{ field: '市盈率(TTM)', operator: '大于', value: 10 }] };
    const result = validateScreenerQuery(query, mockCatalog);
    assert.strictEqual(result.valid, true);
    assert.deepStrictEqual(result.errors, []);
  });

  test('returns invalid for query with field not in catalog', () => {
    const query = { filters: [{ field: '不存在的字段', operator: '大于', value: 10 }] };
    const result = validateScreenerQuery(query, mockCatalog);
    assert.strictEqual(result.valid, false);
    assert.strictEqual(result.errors.length, 1);
    assert.ok(result.errors[0].includes('不在 metrics-catalog 中'));
  });

  test('suggests similar fields when available', () => {
    const query = { filters: [{ field: '市盈率', operator: '大于', value: 10 }] };
    const result = validateScreenerQuery(query, mockCatalog);
    assert.strictEqual(result.valid, false);
    assert.ok(result.errors[0].includes('相近字段'));
    assert.ok(result.errors[0].includes('市盈率(TTM)'));
  });

  test('returns valid for empty filters array', () => {
    const query = { filters: [] };
    const result = validateScreenerQuery(query, mockCatalog);
    assert.strictEqual(result.valid, true);
    assert.deepStrictEqual(result.errors, []);
  });

  test('handles multiple filters with some invalid fields', () => {
    const query = {
      filters: [
        { field: '市盈率(TTM)', operator: '大于', value: 10 },
        { field: 'invalid_field', operator: '小于', value: 5 }
      ]
    };
    const result = validateScreenerQuery(query, mockCatalog);
    assert.strictEqual(result.valid, false);
    assert.strictEqual(result.errors.length, 1);
  });

  test('handles empty catalog', () => {
    const query = { filters: [{ field: '市盈率(TTM)', operator: '大于', value: 10 }] };
    const result = validateScreenerQuery(query, []);
    assert.strictEqual(result.valid, false);
    assert.strictEqual(result.errors.length, 1);
  });

  test('handles field with parentheses in name', () => {
    const query = { filters: [{ field: '净资产收益率(TTM)', operator: '大于', value: 15 }] };
    const result = validateScreenerQuery(query, mockCatalog);
    assert.strictEqual(result.valid, true);
  });

  test('handles filter with complex field name splitting', () => {
    const query = { filters: [{ field: '市盈率(TTM)收益率', operator: '大于', value: 10 }] };
    const result = validateScreenerQuery(query, mockCatalog);
    assert.strictEqual(result.valid, false);
    assert.ok(result.errors[0].includes('市盈率(TTM)'));
  });

  test('handles multiple invalid fields', () => {
    const query = {
      filters: [
        { field: 'invalid1', operator: '大于', value: 10 },
        { field: 'invalid2', operator: '小于', value: 5 }
      ]
    };
    const result = validateScreenerQuery(query, mockCatalog);
    assert.strictEqual(result.valid, false);
    assert.strictEqual(result.errors.length, 2);
  });
});

test.describe('buildBrowserQueryCatalogCandidates', () => {
  test('returns browser catalog first for browser-style queries', () => {
    const candidates = buildBrowserQueryCatalogCandidates('市盈率(TTM)大于10%');
    assert.strictEqual(candidates[0].name, 'browser-metrics-catalog');
    assert.ok(candidates[0].catalog.length > 0);
    assert.strictEqual(candidates[0].richCatalog, null);
  });

  test('returns only browser candidate when no condition catalog', () => {
    const candidates = buildBrowserQueryCatalogCandidates('some query', {});
    assert.strictEqual(candidates.length, 1);
    assert.strictEqual(candidates[0].name, 'browser-metrics-catalog');
  });

  test('returns condition catalog first for percentile queries', () => {
    const candidates = buildBrowserQueryCatalogCandidates('PE-TTM(扣非)统计值10年分位点小于30%', { catalogPath: '../data/condition-catalog.json' }, mockConditionCatalog);
    assert.strictEqual(candidates[0].name, 'condition-catalog');
    assert.strictEqual(candidates[1].name, 'browser-metrics-catalog');
  });

  test('returns condition catalog first for上市日期 queries', () => {
    const candidates = buildBrowserQueryCatalogCandidates('上市日期大于2010年', { catalogPath: '../data/condition-catalog.json' }, mockConditionCatalog);
    assert.strictEqual(candidates[0].name, 'condition-catalog');
  });

  test('returns browser catalog first for TTM metrics queries', () => {
    const candidates = buildBrowserQueryCatalogCandidates('净资产收益率(TTM)大于15%', { catalogPath: '../data/condition-catalog.json' }, mockConditionCatalog);
    assert.strictEqual(candidates[0].name, 'browser-metrics-catalog');
  });

  test('handles empty query string', () => {
    const candidates = buildBrowserQueryCatalogCandidates('');
    assert.strictEqual(candidates.length, 1);
    assert.strictEqual(candidates[0].name, 'browser-metrics-catalog');
  });

  test('handles null query', () => {
    const candidates = buildBrowserQueryCatalogCandidates(null);
    assert.strictEqual(candidates.length, 1);
    assert.strictEqual(candidates[0].name, 'browser-metrics-catalog');
  });

  test('handles undefined query', () => {
    const candidates = buildBrowserQueryCatalogCandidates(undefined);
    assert.strictEqual(candidates.length, 1);
    assert.strictEqual(candidates[0].name, 'browser-metrics-catalog');
  });

  test('preserves richCatalog from condition catalog', () => {
    const candidates = buildBrowserQueryCatalogCandidates('some query', { catalogPath: '../data/condition-catalog.json' }, mockConditionCatalog);
    assert.strictEqual(candidates[1].richCatalog, mockConditionCatalog);
  });

  test('handles 10年 keyword', () => {
    const candidates = buildBrowserQueryCatalogCandidates('10年分位点小于30%', { catalogPath: '../data/condition-catalog.json' }, mockConditionCatalog);
    assert.strictEqual(candidates[0].name, 'condition-catalog');
  });

  test('handles 20年 keyword', () => {
    const candidates = buildBrowserQueryCatalogCandidates('20年分位点小于30%', { catalogPath: '../data/condition-catalog.json' }, mockConditionCatalog);
    assert.strictEqual(candidates[0].name, 'condition-catalog');
  });

  test('handles上市年数 keyword', () => {
    const candidates = buildBrowserQueryCatalogCandidates('上市年数大于5', { catalogPath: '../data/condition-catalog.json' }, mockConditionCatalog);
    assert.strictEqual(candidates[0].name, 'condition-catalog');
  });

  test('handles上市时间 keyword', () => {
    const candidates = buildBrowserQueryCatalogCandidates('上市时间大于2010', { catalogPath: '../data/condition-catalog.json' }, mockConditionCatalog);
    assert.strictEqual(candidates[0].name, 'condition-catalog');
  });

  test('handles上市以来 keyword', () => {
    const candidates = buildBrowserQueryCatalogCandidates('上市以来涨幅大于50%', { catalogPath: '../data/condition-catalog.json' }, mockConditionCatalog);
    assert.strictEqual(candidates[0].name, 'condition-catalog');
  });
});

test.describe('parseBrowserNaturalLanguageQuery', () => {
  test('returns parsed result when first candidate succeeds', async () => {
    const mockParsed = { conditions: [{ field: '市盈率(TTM)', operator: '大于', value: 10 }] };
    
    const mockValidate = { valid: true, errors: [] };
    
    const result = await parseBrowserNaturalLanguageQuery(
      '市盈率大于10',
      {},
      null,
      async () => mockParsed,
      (parsed) => mockValidate
    );
    
    assert.deepStrictEqual(result.parsed, mockParsed);
    assert.strictEqual(result.richCatalog, null);
  });

  test('throws error when all candidates fail', async () => {
    const mockParsed = { conditions: [{ field: 'invalid', operator: '大于', value: 10 }] };
    const mockValidate = { valid: false, errors: ['字段不存在'] };
    
    await assert.rejects(
      async () => parseBrowserNaturalLanguageQuery(
        'invalid query',
        {},
        null,
        async () => mockParsed,
        (parsed) => mockValidate
      ),
      { message: /无法解析筛选条件/ }
    );
  });

  test('returns richCatalog when condition catalog succeeds', async () => {
    const mockParsed = { conditions: [{ metric: 'PE-TTM(扣非)统计值', operator: '小于', value: 30 }] };
    const mockValidate = { valid: true, errors: [] };
    
    let callCount = 0;
    const conditionalParseQuery = async (_query, catalog) => {
      callCount += 1;
      const isConditionCatalog = catalog.some(item => 'metric' in item);
      if (isConditionCatalog) {
        return mockParsed;
      }
      return { conditions: [{ field: 'invalid', operator: '大于', value: 10 }] };
    };
    
    const conditionalValidate = (parsed, catalog) => {
      const isConditionCatalog = catalog.some(item => 'metric' in item);
      if (isConditionCatalog) {
        return { valid: true, errors: [] };
      }
      return { valid: false, errors: ['browser catalog failed'] };
    };
    
    const result = await parseBrowserNaturalLanguageQuery(
      'PE-TTM(扣非)统计值10年分位点小于30%',
      { catalogPath: '../data/condition-catalog.json' },
      mockConditionCatalog,
      conditionalParseQuery,
      conditionalValidate
    );
    
    assert.deepStrictEqual(result.parsed, mockParsed);
    assert.strictEqual(result.richCatalog, mockConditionCatalog);
  });

  test('falls back to next candidate when first fails', async () => {
    let attemptCount = 0;
    
    const fallbackParseQuery = async () => {
      attemptCount += 1;
      if (attemptCount === 1) {
        return { conditions: [{ field: 'invalid_field', operator: '大于', value: 10 }] };
      }
      return { conditions: [{ metric: 'some_metric', operator: '大于', value: 10 }] };
    };
    
    const fallbackValidate = (parsed, catalog) => {
      const isConditionCatalog = catalog.some(item => 'metric' in item);
      if (isConditionCatalog && attemptCount > 1) {
        return { valid: true, errors: [] };
      }
      return { valid: false, errors: ['validation failed'] };
    };
    
    await parseBrowserNaturalLanguageQuery(
      'some query',
      { catalogPath: '../data/condition-catalog.json' },
      mockConditionCatalog,
      fallbackParseQuery,
      fallbackValidate
    );
    
    assert.ok(attemptCount >= 2);
  });

  test('handles parse error gracefully', async () => {
    await assert.rejects(
      async () => parseBrowserNaturalLanguageQuery(
        'invalid query',
        {},
        null,
        async () => { throw new Error('LLM 解析失败'); }
      ),
      { message: /无法解析筛选条件/ }
    );
  });

  test('accumulates error messages from all candidates', async () => {
    const errorParse = async () => { throw new Error('parse error'); };
    
    await assert.rejects(
      async () => parseBrowserNaturalLanguageQuery(
        'invalid query',
        {},
        null,
        errorParse
      ),
      (err) => {
        assert.ok(err.message.includes('无法解析筛选条件'));
        assert.ok(err.message.includes('parse error'));
        return true;
      }
    );
  });
});

test.describe('mergePages', () => {
  test('merges multiple pages into single array', () => {
    const pages = [
      [{ name: 'a', value: '1' }, { name: 'b', value: '2' }],
      [{ name: 'c', value: '3' }]
    ];
    const result = mergePages(pages);
    assert.strictEqual(result.length, 3);
    assert.strictEqual(result[0].name, 'a');
    assert.strictEqual(result[2].name, 'c');
  });

  test('returns empty array for empty input', () => {
    const result = mergePages([]);
    assert.deepStrictEqual(result, []);
  });

  test('returns same array for single page', () => {
    const page = [{ name: 'a', value: '1' }];
    const result = mergePages([page]);
    assert.deepStrictEqual(result, page);
  });

  test('handles pages with empty arrays', () => {
    const pages = [[], [{ name: 'a', value: '1' }], []];
    const result = mergePages(pages);
    assert.strictEqual(result.length, 1);
  });

  test('handles all empty pages', () => {
    const pages = [[]];
    const result = mergePages(pages);
    assert.deepStrictEqual(result, []);
  });

  test('preserves row order from each page', () => {
    const pages = [
      [{ id: 1 }, { id: 2 }],
      [{ id: 3 }, { id: 4 }]
    ];
    const result = mergePages(pages);
    assert.deepStrictEqual(result.map(r => r.id), [1, 2, 3, 4]);
  });

  test('handles deeply nested object values', () => {
    const pages = [
      [{ data: { nested: 'value' } }]
    ];
    const result = mergePages(pages);
    assert.strictEqual(result[0].data.nested, 'value');
  });

  test('handles pages with varying row counts', () => {
    const pages = [
      [{ id: 1 }],
      [{ id: 2 }, { id: 3 }, { id: 4 }],
      [{ id: 5 }]
    ];
    const result = mergePages(pages);
    assert.strictEqual(result.length, 5);
  });
});

test.describe('applyLimit', () => {
  test('returns first N rows when limit is positive integer', () => {
    const rows = [{ name: 'a' }, { name: 'b' }, { name: 'c' }];
    const result = applyLimit(rows, 2);
    assert.strictEqual(result.length, 2);
    assert.strictEqual(result[0].name, 'a');
    assert.strictEqual(result[1].name, 'b');
  });

  test('returns all rows when limit is null', () => {
    const rows = [{ name: 'a' }, { name: 'b' }];
    const result = applyLimit(rows, null);
    assert.deepStrictEqual(result, rows);
  });

  test('returns all rows when limit is undefined', () => {
    const rows = [{ name: 'a' }, { name: 'b' }];
    const result = applyLimit(rows, undefined);
    assert.deepStrictEqual(result, rows);
  });

  test('returns all rows when limit is zero', () => {
    const rows = [{ name: 'a' }, { name: 'b' }];
    const result = applyLimit(rows, 0);
    assert.deepStrictEqual(result, rows);
  });

  test('returns all rows when limit is negative', () => {
    const rows = [{ name: 'a' }, { name: 'b' }];
    const result = applyLimit(rows, -5);
    assert.deepStrictEqual(result, rows);
  });

  test('returns all rows when limit is non-integer', () => {
    const rows = [{ name: 'a' }, { name: 'b' }];
    const result = applyLimit(rows, 1.5);
    assert.deepStrictEqual(result, rows);
  });

  test('returns all rows when limit exceeds row count', () => {
    const rows = [{ name: 'a' }];
    const result = applyLimit(rows, 100);
    assert.strictEqual(result.length, 1);
  });

  test('returns empty array when input is empty', () => {
    const result = applyLimit([], 5);
    assert.deepStrictEqual(result, []);
  });

  test('handles limit of 1', () => {
    const rows = [{ name: 'a' }, { name: 'b' }];
    const result = applyLimit(rows, 1);
    assert.strictEqual(result.length, 1);
    assert.strictEqual(result[0].name, 'a');
  });

  test('handles string limit as invalid', () => {
    const rows = [{ name: 'a' }, { name: 'b' }];
    const result = applyLimit(rows, '5');
    assert.deepStrictEqual(result, rows);
  });

  test('handles NaN limit', () => {
    const rows = [{ name: 'a' }, { name: 'b' }];
    const result = applyLimit(rows, NaN);
    assert.deepStrictEqual(result, rows);
  });

  test('handles Infinity limit', () => {
    const rows = [{ name: 'a' }, { name: 'b' }];
    const result = applyLimit(rows, Infinity);
    assert.deepStrictEqual(result, rows);
  });

  test('handles large positive integer limit', () => {
    const rows = [{ name: 'a' }];
    const result = applyLimit(rows, 1000000);
    assert.strictEqual(result.length, 1);
  });

  test('handles very large row array', () => {
    const rows = Array.from({ length: 10000 }, (_, i) => ({ id: i }));
    const result = applyLimit(rows, 100);
    assert.strictEqual(result.length, 100);
    assert.strictEqual(result[0].id, 0);
    assert.strictEqual(result[99].id, 99);
  });
});

test.describe('formatCsv - RFC 4180', () => {
  test('returns empty string for null input', () => {
    assert.strictEqual(formatCsv(null), '');
  });

  test('returns empty string for undefined input', () => {
    assert.strictEqual(formatCsv(undefined), '');
  });

  test('returns empty string for empty array', () => {
    assert.strictEqual(formatCsv([]), '');
  });

  test('outputs header row from object keys', () => {
    const rows = [{ name: 'a', value: '1' }];
    const csv = formatCsv(rows);
    const lines = csv.split('\n');
    assert.strictEqual(lines[0], 'name,value');
  });

  test('outputs data rows following header', () => {
    const rows = [{ name: 'a', value: '1' }, { name: 'b', value: '2' }];
    const csv = formatCsv(rows);
    const lines = csv.split('\n');
    assert.strictEqual(lines.length, 3);
    assert.strictEqual(lines[1], 'a,1');
    assert.strictEqual(lines[2], 'b,2');
  });

  test('RFC 4180: escapes comma in value', () => {
    const rows = [{ col: 'hello,world' }];
    const csv = formatCsv(rows);
    const lines = csv.split('\n');
    assert.strictEqual(lines[1], '"hello,world"');
  });

  test('RFC 4180: escapes double quote by doubling', () => {
    const rows = [{ col: 'say "hi"' }];
    const csv = formatCsv(rows);
    const lines = csv.split('\n');
    assert.strictEqual(lines[1], '"say ""hi"""');
  });

  test('RFC 4180: escapes newline in value', () => {
    const rows = [{ col: 'line1\nline2' }];
    const csv = formatCsv(rows);
    assert.ok(csv.includes('"line1\nline2"'));
  });

  test('RFC 4180: escapes carriage return in value', () => {
    const rows = [{ col: 'line1\rline2' }];
    const csv = formatCsv(rows);
    assert.ok(csv.includes('"line1\rline2"'));
  });

  test('RFC 4180: escapes CRLF in value', () => {
    const rows = [{ col: 'line1\r\nline2' }];
    const csv = formatCsv(rows);
    assert.ok(csv.includes('"line1\r\nline2"'));
  });

  test('RFC 4180: does not escape plain value', () => {
    const rows = [{ col: 'hello' }];
    const csv = formatCsv(rows);
    const lines = csv.split('\n');
    assert.strictEqual(lines[1], 'hello');
  });

  test('RFC 4180: handles multiple special chars', () => {
    const rows = [{ col: 'a,b"c\nd' }];
    const csv = formatCsv(rows);
    assert.ok(csv.includes('"a,b""c\nd"'));
  });

  test('RFC 4180: handles empty string value', () => {
    const rows = [{ col: '' }];
    const csv = formatCsv(rows);
    const lines = csv.split('\n');
    assert.strictEqual(lines[1], '');
  });

  test('RFC 4180: handles null value as empty string', () => {
    const rows = [{ col: null }];
    const csv = formatCsv(rows);
    const lines = csv.split('\n');
    assert.strictEqual(lines[1], '');
  });

  test('RFC 4180: handles undefined value as empty string', () => {
    const rows = [{ col: undefined }];
    const csv = formatCsv(rows);
    const lines = csv.split('\n');
    assert.strictEqual(lines[1], '');
  });

  test('RFC 4180: handles number value by converting to string', () => {
    const rows = [{ col: 123 }];
    const csv = formatCsv(rows);
    const lines = csv.split('\n');
    assert.strictEqual(lines[1], '123');
  });

  test('RFC 4180: handles boolean value by converting to string', () => {
    const rows = [{ col: true }];
    const csv = formatCsv(rows);
    const lines = csv.split('\n');
    assert.strictEqual(lines[1], 'true');
  });

  test('RFC 4180: handles false boolean value', () => {
    const rows = [{ col: false }];
    const csv = formatCsv(rows);
    const lines = csv.split('\n');
    assert.strictEqual(lines[1], 'false');
  });

  test('RFC 4180: preserves field order from first row', () => {
    const rows = [{ b: '2', a: '1', c: '3' }];
    const csv = formatCsv(rows);
    const lines = csv.split('\n');
    assert.strictEqual(lines[0], 'b,a,c');
    assert.strictEqual(lines[1], '2,1,3');
  });

  test('RFC 4180: handles rows with different keys using first row keys', () => {
    const rows = [{ a: '1', b: '2' }, { a: '3', c: '4' }];
    const csv = formatCsv(rows);
    const lines = csv.split('\n');
    assert.strictEqual(lines[0], 'a,b');
    assert.strictEqual(lines[1], '1,2');
    assert.strictEqual(lines[2], '3,');
  });

  test('RFC 4180: escapes value starting with quote', () => {
    const rows = [{ col: '"quoted"' }];
    const csv = formatCsv(rows);
    const lines = csv.split('\n');
    assert.strictEqual(lines[1], '"quoted"');
  });

  test('RFC 4180: handles consecutive quotes', () => {
    const rows = [{ col: '""""' }];
    const csv = formatCsv(rows);
    const lines = csv.split('\n');
    assert.strictEqual(lines[1], '""""""');
  });

  test('RFC 4180: handles value with only comma', () => {
    const rows = [{ col: ',' }];
    const csv = formatCsv(rows);
    const lines = csv.split('\n');
    assert.strictEqual(lines[1], '","');
  });

  test('RFC 4180: handles Chinese characters', () => {
    const rows = [{ name: '股票名称', code: '000001' }];
    const csv = formatCsv(rows);
    const lines = csv.split('\n');
    assert.strictEqual(lines[1], '股票名称,000001');
  });

  test('RFC 4180: handles Chinese with special chars', () => {
    const rows = [{ desc: '市盈率(TTM)大于10%' }];
    const csv = formatCsv(rows);
    const lines = csv.split('\n');
    assert.strictEqual(lines[1], '市盈率(TTM)大于10%');
  });

  test('RFC 4180: handles large dataset', () => {
    const rows = [];
    for (let i = 0; i < 1000; i++) {
      rows.push({ id: String(i), name: `name_${i}` });
    }
    const csv = formatCsv(rows);
    const lines = csv.split('\n');
    assert.strictEqual(lines.length, 1001);
  });

  test('RFC 4180: handles single column', () => {
    const rows = [{ col: 'value1' }, { col: 'value2' }];
    const csv = formatCsv(rows);
    const lines = csv.split('\n');
    assert.strictEqual(lines[0], 'col');
    assert.strictEqual(lines[1], 'value1');
    assert.strictEqual(lines[2], 'value2');
  });

  test('RFC 4180: handles many columns', () => {
    const row = {};
    for (let i = 0; i < 50; i++) {
      row[`col${i}`] = `val${i}`;
    }
    const rows = [row];
    const csv = formatCsv(rows);
    const lines = csv.split('\n');
    assert.strictEqual(lines[0].split(',').length, 50);
  });

  test('RFC 4180: handles value with mixed quotes and commas', () => {
    const rows = [{ col: 'He said, "Hello, World!"' }];
    const csv = formatCsv(rows);
    assert.strictEqual(csv.split('\n')[1], '"He said, ""Hello, World!"""');
  });

  test('RFC 4180: handles negative number', () => {
    const rows = [{ col: -123.45 }];
    const csv = formatCsv(rows);
    const lines = csv.split('\n');
    assert.strictEqual(lines[1], '-123.45');
  });

  test('RFC 4180: handles zero', () => {
    const rows = [{ col: 0 }];
    const csv = formatCsv(rows);
    const lines = csv.split('\n');
    assert.strictEqual(lines[1], '0');
  });

  test('RFC 4180: handles special numeric values', () => {
    const rows = [{ col: NaN }, { col: Infinity }];
    const csv = formatCsv(rows);
    const lines = csv.split('\n');
    assert.strictEqual(lines[1], 'NaN');
    assert.strictEqual(lines[2], 'Infinity');
  });

  test('RFC 4180: handles object with Symbol key (ignored)', () => {
    const sym = Symbol('hidden');
    const rows = [{ a: '1', [sym]: 'hidden' }];
    const csv = formatCsv(rows);
    const lines = csv.split('\n');
    assert.strictEqual(lines[0], 'a');
    assert.strictEqual(lines[1], '1');
  });

  test('RFC 4180: handles tab character (no escaping required)', () => {
    const rows = [{ col: 'hello\tworld' }];
    const csv = formatCsv(rows);
    const lines = csv.split('\n');
    assert.strictEqual(lines[1], 'hello\tworld');
  });

  test('RFC 4180: handles multiple commas', () => {
    const rows = [{ col: 'a,b,c,d' }];
    const csv = formatCsv(rows);
    const lines = csv.split('\n');
    assert.strictEqual(lines[1], '"a,b,c,d"');
  });

  test('RFC 4180: handles empty rows array returns empty string', () => {
    assert.strictEqual(formatCsv([]), '');
  });
});

test.describe('writeCsvFile', () => {
  test('writes CSV content and returns file path', async (t) => {
    const fs = await import('node:fs');
    const path = await import('node:path');
    
    t.mock.method(fs, 'mkdirSync', () => undefined);
    t.mock.method(fs, 'writeFileSync', () => undefined);
    t.mock.method(path, 'join', (_, filename) => `/mocked/output/${filename}`);
    
    const originalDateNow = Date.now;
    global.Date.now = () => 1234567890;
    
    const result = writeCsvFile('name,value\na,1');
    
    assert.strictEqual(result, '/mocked/output/screener-1234567890.csv');
    
    global.Date.now = originalDateNow;
  });

  test('creates output directory recursively', async (t) => {
    const fs = await import('node:fs');
    
    const mkdirCall = t.mock.method(fs, 'mkdirSync', (path, options) => {
      assert.ok(options.recursive);
      return undefined;
    });
    
    t.mock.method(fs, 'writeFileSync', () => undefined);
    
    writeCsvFile('test');
    
    assert.strictEqual(mkdirCall.mock.callCount(), 1);
  });

  test('writes content with utf8 encoding', async (t) => {
    const fs = await import('node:fs');
    
    t.mock.method(fs, 'mkdirSync', () => undefined);
    
    const writeCall = t.mock.method(fs, 'writeFileSync', (_, content, encoding) => {
      assert.strictEqual(content, 'test content');
      assert.strictEqual(encoding, 'utf8');
    });
    
    writeCsvFile('test content');
    
    assert.strictEqual(writeCall.mock.callCount(), 1);
  });

  test('handles empty CSV content', async (t) => {
    const fs = await import('node:fs');
    
    t.mock.method(fs, 'mkdirSync', () => undefined);
    
    const writeCall = t.mock.method(fs, 'writeFileSync', (_, content) => {
      assert.strictEqual(content, '');
    });
    
    writeCsvFile('');
    
    assert.strictEqual(writeCall.mock.callCount(), 1);
  });

  test('generates unique filename based on timestamp', async (t) => {
    const fs = await import('node:fs');
    const path = await import('node:path');
    
    t.mock.method(fs, 'mkdirSync', () => undefined);
    t.mock.method(fs, 'writeFileSync', () => undefined);
    
    let timestamps = [1000, 2000];
    let callIndex = 0;
    const originalDateNow = Date.now;
    global.Date.now = () => timestamps[callIndex++];
    
    const path1 = writeCsvFile('a');
    const path2 = writeCsvFile('b');
    
    assert.ok(path1.includes('screener-1000'));
    assert.ok(path2.includes('screener-2000'));
    
    global.Date.now = originalDateNow;
  });

  test('console logs the file path', async (t) => {
    const fs = await import('node:fs');
    const path = await import('node:path');
    
    t.mock.method(fs, 'mkdirSync', () => undefined);
    t.mock.method(fs, 'writeFileSync', () => undefined);
    t.mock.method(path, 'join', () => '/output/test.csv');
    
    const originalLog = console.log;
    let loggedPath = null;
    console.log = (path) => { loggedPath = path; };
    
    writeCsvFile('content');
    
    assert.strictEqual(loggedPath, '/output/test.csv');
    
    console.log = originalLog;
  });
});