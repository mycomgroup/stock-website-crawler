import { test } from 'node:test';
import assert from 'node:assert';
import { validateCatalogEntry } from '../browser/lib/catalog-validator.js';

test.describe('validateCatalogEntry - null input', () => {
  test('returns false for null', () => {
    assert.strictEqual(validateCatalogEntry(null), false);
  });
});

test.describe('validateCatalogEntry - non-object input', () => {
  test('returns false for string', () => {
    assert.strictEqual(validateCatalogEntry('string'), false);
  });

  test('returns false for number', () => {
    assert.strictEqual(validateCatalogEntry(123), false);
  });

  test('returns false for boolean true', () => {
    assert.strictEqual(validateCatalogEntry(true), false);
  });

  test('returns false for boolean false', () => {
    assert.strictEqual(validateCatalogEntry(false), false);
  });

  test('returns false for undefined', () => {
    assert.strictEqual(validateCatalogEntry(undefined), false);
  });

  test('returns false for Symbol', () => {
    assert.strictEqual(validateCatalogEntry(Symbol('test')), false);
  });

  test('returns false for function', () => {
    assert.strictEqual(validateCatalogEntry(() => {}), false);
  });

  test('returns false for BigInt', () => {
    assert.strictEqual(validateCatalogEntry(BigInt(123)), false);
  });
});

test.describe('validateCatalogEntry - array input', () => {
  test('returns false for empty array', () => {
    assert.strictEqual(validateCatalogEntry([]), false);
  });

  test('returns false for array with numbers', () => {
    assert.strictEqual(validateCatalogEntry([1, 2, 3]), false);
  });

  test('returns false for array with objects', () => {
    assert.strictEqual(validateCatalogEntry([{ name: 'a' }]), false);
  });

  test('returns false for array that looks like valid entry', () => {
    const fakeArray = [
      { name: 'pe_ttm', displayName: '市盈率', category: '估值', unit: '倍', operators: ['大于'] }
    ];
    assert.strictEqual(validateCatalogEntry(fakeArray), false);
  });

  test('returns false for array with strings', () => {
    assert.strictEqual(validateCatalogEntry(['name', 'displayName', 'category']), false);
  });
});

test.describe('validateCatalogEntry - missing required fields', () => {
  test('returns false when name is missing', () => {
    const entry = { displayName: '市盈率', category: '估值', unit: '倍', operators: ['大于'] };
    assert.strictEqual(validateCatalogEntry(entry), false);
  });

  test('returns false when displayName is missing', () => {
    const entry = { name: 'pe_ttm', category: '估值', unit: '倍', operators: ['大于'] };
    assert.strictEqual(validateCatalogEntry(entry), false);
  });

  test('returns false when category is missing', () => {
    const entry = { name: 'pe_ttm', displayName: '市盈率', unit: '倍', operators: ['大于'] };
    assert.strictEqual(validateCatalogEntry(entry), false);
  });

  test('returns false when unit is missing', () => {
    const entry = { name: 'pe_ttm', displayName: '市盈率', category: '估值', operators: ['大于'] };
    assert.strictEqual(validateCatalogEntry(entry), false);
  });

  test('returns false when operators is missing', () => {
    const entry = { name: 'pe_ttm', displayName: '市盈率', category: '估值', unit: '倍' };
    assert.strictEqual(validateCatalogEntry(entry), false);
  });

  test('returns false when all fields are missing', () => {
    assert.strictEqual(validateCatalogEntry({}), false);
  });

  test('returns false when only name present', () => {
    const entry = { name: 'pe_ttm' };
    assert.strictEqual(validateCatalogEntry(entry), false);
  });

  test('returns false when extra fields present but required missing', () => {
    const entry = { extraField: 'value', name: 'pe_ttm' };
    assert.strictEqual(validateCatalogEntry(entry), false);
  });

  test('returns false when 4 out of 5 fields present', () => {
    const entry = { name: 'pe_ttm', displayName: '市盈率', category: '估值', unit: '倍' };
    assert.strictEqual(validateCatalogEntry(entry), false);
  });

  test('returns false when 3 out of 5 fields present', () => {
    const entry = { name: 'pe_ttm', displayName: '市盈率', category: '估值' };
    assert.strictEqual(validateCatalogEntry(entry), false);
  });

  test('returns false when 2 out of 5 fields present', () => {
    const entry = { name: 'pe_ttm', displayName: '市盈率' };
    assert.strictEqual(validateCatalogEntry(entry), false);
  });

  test('returns false when 1 out of 5 fields present', () => {
    const entry = { name: 'pe_ttm' };
    assert.strictEqual(validateCatalogEntry(entry), false);
  });
});

test.describe('validateCatalogEntry - field values null/undefined', () => {
  test('returns false when name is null', () => {
    const entry = { name: null, displayName: '市盈率', category: '估值', unit: '倍', operators: ['大于'] };
    assert.strictEqual(validateCatalogEntry(entry), false);
  });

  test('returns false when name is undefined', () => {
    const entry = { displayName: '市盈率', category: '估值', unit: '倍', operators: ['大于'] };
    assert.strictEqual(validateCatalogEntry(entry), false);
  });

  test('returns false when displayName is null', () => {
    const entry = { name: 'pe_ttm', displayName: null, category: '估值', unit: '倍', operators: ['大于'] };
    assert.strictEqual(validateCatalogEntry(entry), false);
  });

  test('returns false when displayName is undefined', () => {
    const entry = { name: 'pe_ttm', category: '估值', unit: '倍', operators: ['大于'] };
    assert.strictEqual(validateCatalogEntry(entry), false);
  });

  test('returns false when category is null', () => {
    const entry = { name: 'pe_ttm', displayName: '市盈率', category: null, unit: '倍', operators: ['大于'] };
    assert.strictEqual(validateCatalogEntry(entry), false);
  });

  test('returns false when category is undefined', () => {
    const entry = { name: 'pe_ttm', displayName: '市盈率', unit: '倍', operators: ['大于'] };
    assert.strictEqual(validateCatalogEntry(entry), false);
  });

  test('returns false when unit is null', () => {
    const entry = { name: 'pe_ttm', displayName: '市盈率', category: '估值', unit: null, operators: ['大于'] };
    assert.strictEqual(validateCatalogEntry(entry), false);
  });

  test('returns false when unit is undefined', () => {
    const entry = { name: 'pe_ttm', displayName: '市盈率', category: '估值', operators: ['大于'] };
    assert.strictEqual(validateCatalogEntry(entry), false);
  });

  test('returns false when operators is null', () => {
    const entry = { name: 'pe_ttm', displayName: '市盈率', category: '估值', unit: '倍', operators: null };
    assert.strictEqual(validateCatalogEntry(entry), false);
  });

  test('returns false when operators is undefined', () => {
    const entry = { name: 'pe_ttm', displayName: '市盈率', category: '估值', unit: '倍' };
    assert.strictEqual(validateCatalogEntry(entry), false);
  });

  test('returns false when multiple fields are null', () => {
    const entry = { name: null, displayName: null, category: '估值', unit: '倍', operators: ['大于'] };
    assert.strictEqual(validateCatalogEntry(entry), false);
  });

  test('returns false when all fields are null', () => {
    const entry = { name: null, displayName: null, category: null, unit: null, operators: null };
    assert.strictEqual(validateCatalogEntry(entry), false);
  });
});

test.describe('validateCatalogEntry - empty string fields', () => {
  test('returns false when name is empty string', () => {
    const entry = { name: '', displayName: '市盈率', category: '估值', unit: '倍', operators: ['大于'] };
    assert.strictEqual(validateCatalogEntry(entry), false);
  });

  test('returns false when name is whitespace only (spaces)', () => {
    const entry = { name: '   ', displayName: '市盈率', category: '估值', unit: '倍', operators: ['大于'] };
    assert.strictEqual(validateCatalogEntry(entry), false);
  });

  test('returns false when name is whitespace only (tabs)', () => {
    const entry = { name: '\t\t', displayName: '市盈率', category: '估值', unit: '倍', operators: ['大于'] };
    assert.strictEqual(validateCatalogEntry(entry), false);
  });

  test('returns false when displayName is empty string', () => {
    const entry = { name: 'pe_ttm', displayName: '', category: '估值', unit: '倍', operators: ['大于'] };
    assert.strictEqual(validateCatalogEntry(entry), false);
  });

  test('returns false when displayName is whitespace only', () => {
    const entry = { name: 'pe_ttm', displayName: '  ', category: '估值', unit: '倍', operators: ['大于'] };
    assert.strictEqual(validateCatalogEntry(entry), false);
  });

  test('returns false when category is empty string', () => {
    const entry = { name: 'pe_ttm', displayName: '市盈率', category: '', unit: '倍', operators: ['大于'] };
    assert.strictEqual(validateCatalogEntry(entry), false);
  });

  test('returns false when category is whitespace only', () => {
    const entry = { name: 'pe_ttm', displayName: '市盈率', category: '\t', unit: '倍', operators: ['大于'] };
    assert.strictEqual(validateCatalogEntry(entry), false);
  });

  test('returns false when unit is empty string', () => {
    const entry = { name: 'pe_ttm', displayName: '市盈率', category: '估值', unit: '', operators: ['大于'] };
    assert.strictEqual(validateCatalogEntry(entry), false);
  });

  test('returns false when unit is whitespace only', () => {
    const entry = { name: 'pe_ttm', displayName: '市盈率', category: '估值', unit: '\n', operators: ['大于'] };
    assert.strictEqual(validateCatalogEntry(entry), false);
  });

  test('returns false when unit is newlines only', () => {
    const entry = { name: 'pe_ttm', displayName: '市盈率', category: '估值', unit: '\n\r\n', operators: ['大于'] };
    assert.strictEqual(validateCatalogEntry(entry), false);
  });

  test('returns false when multiple string fields are empty', () => {
    const entry = { name: '', displayName: '', category: '估值', unit: '倍', operators: ['大于'] };
    assert.strictEqual(validateCatalogEntry(entry), false);
  });

  test('returns true when string field has valid whitespace-trimmable content', () => {
    const entry = { name: ' pe_ttm ', displayName: '市盈率', category: '估值', unit: '倍', operators: ['大于'] };
    assert.strictEqual(validateCatalogEntry(entry), true);
  });
});

test.describe('validateCatalogEntry - non-string fields', () => {
  test('returns false when name is number', () => {
    const entry = { name: 123, displayName: '市盈率', category: '估值', unit: '倍', operators: ['大于'] };
    assert.strictEqual(validateCatalogEntry(entry), false);
  });

  test('returns false when name is boolean', () => {
    const entry = { name: true, displayName: '市盈率', category: '估值', unit: '倍', operators: ['大于'] };
    assert.strictEqual(validateCatalogEntry(entry), false);
  });

  test('returns false when name is object', () => {
    const entry = { name: {}, displayName: '市盈率', category: '估值', unit: '倍', operators: ['大于'] };
    assert.strictEqual(validateCatalogEntry(entry), false);
  });

  test('returns false when name is array', () => {
    const entry = { name: [], displayName: '市盈率', category: '估值', unit: '倍', operators: ['大于'] };
    assert.strictEqual(validateCatalogEntry(entry), false);
  });

  test('returns false when displayName is number', () => {
    const entry = { name: 'pe_ttm', displayName: 456, category: '估值', unit: '倍', operators: ['大于'] };
    assert.strictEqual(validateCatalogEntry(entry), false);
  });

  test('returns false when displayName is boolean', () => {
    const entry = { name: 'pe_ttm', displayName: true, category: '估值', unit: '倍', operators: ['大于'] };
    assert.strictEqual(validateCatalogEntry(entry), false);
  });

  test('returns false when category is array', () => {
    const entry = { name: 'pe_ttm', displayName: '市盈率', category: [], unit: '倍', operators: ['大于'] };
    assert.strictEqual(validateCatalogEntry(entry), false);
  });

  test('returns false when category is number', () => {
    const entry = { name: 'pe_ttm', displayName: '市盈率', category: 1, unit: '倍', operators: ['大于'] };
    assert.strictEqual(validateCatalogEntry(entry), false);
  });

  test('returns false when unit is number', () => {
    const entry = { name: 'pe_ttm', displayName: '市盈率', category: '估值', unit: 100, operators: ['大于'] };
    assert.strictEqual(validateCatalogEntry(entry), false);
  });

  test('returns false when unit is boolean', () => {
    const entry = { name: 'pe_ttm', displayName: '市盈率', category: '估值', unit: false, operators: ['大于'] };
    assert.strictEqual(validateCatalogEntry(entry), false);
  });
});

test.describe('validateCatalogEntry - operators validation', () => {
  test('returns false when operators is empty array', () => {
    const entry = { name: 'pe_ttm', displayName: '市盈率', category: '估值', unit: '倍', operators: [] };
    assert.strictEqual(validateCatalogEntry(entry), false);
  });

  test('returns false when operators is string', () => {
    const entry = { name: 'pe_ttm', displayName: '市盈率', category: '估值', unit: '倍', operators: '大于' };
    assert.strictEqual(validateCatalogEntry(entry), false);
  });

  test('returns false when operators is object', () => {
    const entry = { name: 'pe_ttm', displayName: '市盈率', category: '估值', unit: '倍', operators: {} };
    assert.strictEqual(validateCatalogEntry(entry), false);
  });

  test('returns false when operators is number', () => {
    const entry = { name: 'pe_ttm', displayName: '市盈率', category: '估值', unit: '倍', operators: 3 };
    assert.strictEqual(validateCatalogEntry(entry), false);
  });

  test('returns false when operators is boolean', () => {
    const entry = { name: 'pe_ttm', displayName: '市盈率', category: '估值', unit: '倍', operators: true };
    assert.strictEqual(validateCatalogEntry(entry), false);
  });

  test('returns true when operators has one element', () => {
    const entry = { name: 'pe_ttm', displayName: '市盈率', category: '估值', unit: '倍', operators: ['大于'] };
    assert.strictEqual(validateCatalogEntry(entry), true);
  });

  test('returns true when operators has two elements', () => {
    const entry = { name: 'pe_ttm', displayName: '市盈率', category: '估值', unit: '倍', operators: ['大于', '小于'] };
    assert.strictEqual(validateCatalogEntry(entry), true);
  });

  test('returns true when operators has three elements', () => {
    const entry = { name: 'pe_ttm', displayName: '市盈率', category: '估值', unit: '倍', operators: ['大于', '小于', '介于'] };
    assert.strictEqual(validateCatalogEntry(entry), true);
  });

  test('returns true when operators has many elements', () => {
    const entry = { name: 'pe_ttm', displayName: '市盈率', category: '估值', unit: '倍', operators: ['大于', '小于', '介于', '等于', '不等于'] };
    assert.strictEqual(validateCatalogEntry(entry), true);
  });

  test('returns true when operators array contains empty strings', () => {
    const entry = { name: 'pe_ttm', displayName: '市盈率', category: '估值', unit: '倍', operators: ['', '大于'] };
    assert.strictEqual(validateCatalogEntry(entry), true);
  });

  test('returns true when operators array contains numbers', () => {
    const entry = { name: 'pe_ttm', displayName: '市盈率', category: '估值', unit: '倍', operators: [1, 2] };
    assert.strictEqual(validateCatalogEntry(entry), true);
  });

  test('returns true when operators array contains null values', () => {
    const entry = { name: 'pe_ttm', displayName: '市盈率', category: '估值', unit: '倍', operators: [null, '大于'] };
    assert.strictEqual(validateCatalogEntry(entry), true);
  });

  test('returns true when operators with duplicate values', () => {
    const entry = { name: 'pe_ttm', displayName: '市盈率', category: '估值', unit: '倍', operators: ['大于', '大于'] };
    assert.strictEqual(validateCatalogEntry(entry), true);
  });

  test('returns true when operators is array with single empty string', () => {
    const entry = { name: 'pe_ttm', displayName: '市盈率', category: '估值', unit: '倍', operators: [''] };
    assert.strictEqual(validateCatalogEntry(entry), true);
  });
});

test.describe('validateCatalogEntry - valid entries', () => {
  test('returns true for minimal valid entry', () => {
    const entry = {
      name: 'pe_ttm',
      displayName: '市盈率',
      category: '估值',
      unit: '倍',
      operators: ['大于']
    };
    assert.strictEqual(validateCatalogEntry(entry), true);
  });

  test('returns true for entry with all operators', () => {
    const entry = {
      name: 'pe_ttm',
      displayName: '市盈率(TTM)',
      category: '估值',
      unit: '倍',
      operators: ['大于', '小于', '介于']
    };
    assert.strictEqual(validateCatalogEntry(entry), true);
  });

  test('returns true for entry with extra fields', () => {
    const entry = {
      name: 'pe_ttm',
      displayName: '市盈率(TTM)',
      category: '估值',
      unit: '倍',
      operators: ['大于', '小于', '介于'],
      description: '额外字段',
      apiField: 'pe_ratio',
      deprecated: false
    };
    assert.strictEqual(validateCatalogEntry(entry), true);
  });

  test('returns true for entry with Chinese characters', () => {
    const entry = {
      name: '市盈率',
      displayName: '市盈率(TTM)',
      category: '估值指标',
      unit: '倍',
      operators: ['大于']
    };
    assert.strictEqual(validateCatalogEntry(entry), true);
  });

  test('returns true for entry with special characters in name', () => {
    const entry = {
      name: 'pe-ttm_ratio',
      displayName: '市盈率(TTM)',
      category: '估值',
      unit: '倍',
      operators: ['大于']
    };
    assert.strictEqual(validateCatalogEntry(entry), true);
  });

  test('returns true for entry with parentheses in displayName', () => {
    const entry = {
      name: 'roe_ttm',
      displayName: '净资产收益率(TTM)',
      category: '盈利能力',
      unit: '%',
      operators: ['大于', '小于']
    };
    assert.strictEqual(validateCatalogEntry(entry), true);
  });

  test('returns true for entry with underscore in name', () => {
    const entry = {
      name: 'pe_ttm_value',
      displayName: 'PE TTM',
      category: '估值',
      unit: '倍',
      operators: ['大于']
    };
    assert.strictEqual(validateCatalogEntry(entry), true);
  });

  test('returns true for entry with special unit', () => {
    const entry = {
      name: 'market_cap',
      displayName: '总市值',
      category: '规模',
      unit: '亿元',
      operators: ['大于']
    };
    assert.strictEqual(validateCatalogEntry(entry), true);
  });

  test('returns true for entry with percentage unit', () => {
    const entry = {
      name: 'roe',
      displayName: 'ROE',
      category: '盈利能力',
      unit: '%',
      operators: ['大于']
    };
    assert.strictEqual(validateCatalogEntry(entry), true);
  });

  test('returns true for entry with no unit', () => {
    const entry = {
      name: 'count',
      displayName: '数量',
      category: '其他',
      unit: '个',
      operators: ['大于']
    };
    assert.strictEqual(validateCatalogEntry(entry), true);
  });

  test('returns true for entry with long strings', () => {
    const entry = {
      name: 'very_long_metric_name_for_testing_purposes',
      displayName: '非常长的显示名称用于测试目的验证',
      category: '测试分类',
      unit: '测试单位',
      operators: ['大于']
    };
    assert.strictEqual(validateCatalogEntry(entry), true);
  });

  test('returns true for entry with single character strings', () => {
    const entry = {
      name: 'a',
      displayName: 'b',
      category: 'c',
      unit: 'd',
      operators: ['e']
    };
    assert.strictEqual(validateCatalogEntry(entry), true);
  });
});

test.describe('validateCatalogEntry - edge cases', () => {
  test('returns false for Object.create(null) with missing fields', () => {
    const entry = Object.create(null);
    entry.name = 'pe_ttm';
    assert.strictEqual(validateCatalogEntry(entry), false);
  });

  test('returns true for Object.create(null) with all required fields', () => {
    const entry = Object.create(null);
    entry.name = 'pe_ttm';
    entry.displayName = '市盈率';
    entry.category = '估值';
    entry.unit = '倍';
    entry.operators = ['大于'];
    assert.strictEqual(validateCatalogEntry(entry), true);
  });

  test('returns false for frozen object with missing fields', () => {
    const entry = Object.freeze({ name: 'pe_ttm' });
    assert.strictEqual(validateCatalogEntry(entry), false);
  });

  test('returns true for frozen object with all required fields', () => {
    const entry = Object.freeze({
      name: 'pe_ttm',
      displayName: '市盈率',
      category: '估值',
      unit: '倍',
      operators: ['大于']
    });
    assert.strictEqual(validateCatalogEntry(entry), true);
  });

  test('returns false for sealed object with missing fields', () => {
    const entry = Object.seal({ name: 'pe_ttm' });
    assert.strictEqual(validateCatalogEntry(entry), false);
  });

  test('returns true for sealed object with all required fields', () => {
    const entry = Object.seal({
      name: 'pe_ttm',
      displayName: '市盈率',
      category: '估值',
      unit: '倍',
      operators: ['大于']
    });
    assert.strictEqual(validateCatalogEntry(entry), true);
  });

  test('returns true for entry with prototype properties', () => {
    function Base() {}
    Base.prototype.inherited = 'value';
    const entry = new Base();
    entry.name = 'pe_ttm';
    entry.displayName = '市盈率';
    entry.category = '估值';
    entry.unit = '倍';
    entry.operators = ['大于'];
    assert.strictEqual(validateCatalogEntry(entry), true);
  });

  test('returns true for entry with getter properties', () => {
    const entry = {
      get name() { return 'pe_ttm'; },
      displayName: '市盈率',
      category: '估值',
      unit: '倍',
      operators: ['大于']
    };
    assert.strictEqual(validateCatalogEntry(entry), true);
  });

  test('returns true for entry with setter properties (if get returns value)', () => {
    let _name = 'pe_ttm';
    const entry = {
      get name() { return _name; },
      set name(v) { _name = v; },
      displayName: '市盈率',
      category: '估值',
      unit: '倍',
      operators: ['大于']
    };
    assert.strictEqual(validateCatalogEntry(entry), true);
  });

  test('returns true for entry with Symbol properties and required fields', () => {
    const sym = Symbol('hidden');
    const entry = {
      name: 'pe_ttm',
      displayName: '市盈率',
      category: '估值',
      unit: '倍',
      operators: ['大于'],
      [sym]: 'hidden value'
    };
    assert.strictEqual(validateCatalogEntry(entry), true);
  });

  test('returns true for entry with numeric string operators', () => {
    const entry = {
      name: 'pe_ttm',
      displayName: '市盈率',
      category: '估值',
      unit: '倍',
      operators: ['1', '2']
    };
    assert.strictEqual(validateCatalogEntry(entry), true);
  });

  test('returns true for sparse array operators', () => {
    const operators = [];
    operators[0] = '大于';
    operators[2] = '小于';
    const entry = {
      name: 'pe_ttm',
      displayName: '市盈率',
      category: '估值',
      unit: '倍',
      operators: operators
    };
    assert.strictEqual(validateCatalogEntry(entry), true);
  });

  test('returns true for entry with very large operators array', () => {
    const operators = Array.from({ length: 100 }, (_, i) => `op${i}`);
    const entry = {
      name: 'pe_ttm',
      displayName: '市盈率',
      category: '估值',
      unit: '倍',
      operators: operators
    };
    assert.strictEqual(validateCatalogEntry(entry), true);
  });

  test('returns false for Date object', () => {
    assert.strictEqual(validateCatalogEntry(new Date()), false);
  });

  test('returns false for RegExp object', () => {
    assert.strictEqual(validateCatalogEntry(/test/), false);
  });

  test('returns false for Error object', () => {
    assert.strictEqual(validateCatalogEntry(new Error('test')), false);
  });

  test('returns false for Map object', () => {
    assert.strictEqual(validateCatalogEntry(new Map()), false);
  });

  test('returns false for Set object', () => {
    assert.strictEqual(validateCatalogEntry(new Set()), false);
  });

  test('returns false for WeakMap object', () => {
    assert.strictEqual(validateCatalogEntry(new WeakMap()), false);
  });

  test('returns false for WeakSet object', () => {
    assert.strictEqual(validateCatalogEntry(new WeakSet()), false);
  });

  test('returns false for Promise object', () => {
    assert.strictEqual(validateCatalogEntry(Promise.resolve()), false);
  });

  test('returns false for Int8Array', () => {
    assert.strictEqual(validateCatalogEntry(new Int8Array()), false);
  });

  test('returns false for ArrayBuffer', () => {
    assert.strictEqual(validateCatalogEntry(new ArrayBuffer(10)), false);
  });
});

test.describe('validateCatalogEntry - combined edge cases', () => {
  test('returns false when operators empty array and other fields missing', () => {
    const entry = { operators: [] };
    assert.strictEqual(validateCatalogEntry(entry), false);
  });

  test('returns false when operators empty array but other fields valid', () => {
    const entry = { name: 'pe_ttm', displayName: '市盈率', category: '估值', unit: '倍', operators: [] };
    assert.strictEqual(validateCatalogEntry(entry), false);
  });

  test('returns true for minimal entry with spaces in strings', () => {
    const entry = { name: ' pe_ttm ', displayName: ' 市盈率 ', category: ' 估值 ', unit: ' 倍 ', operators: [' 大于 '] };
    assert.strictEqual(validateCatalogEntry(entry), true);
  });

  test('returns false when entry has only operators as valid field', () => {
    const entry = { operators: ['大于'] };
    assert.strictEqual(validateCatalogEntry(entry), false);
  });

  test('returns true for entry with escaped characters in displayName', () => {
    const entry = {
      name: 'pe_ttm',
      displayName: '市盈率\\n(TTM)',
      category: '估值',
      unit: '倍',
      operators: ['大于']
    };
    assert.strictEqual(validateCatalogEntry(entry), true);
  });

  test('returns true for entry with unicode characters', () => {
    const entry = {
      name: 'unicode_test',
      displayName: '测试\u4e2d\u6587',
      category: '分类\u8d28',
      unit: '单位\u5143',
      operators: ['大于']
    };
    assert.strictEqual(validateCatalogEntry(entry), true);
  });

  test('returns true for entry with emoji in displayName', () => {
    const entry = {
      name: 'emoji',
      displayName: '市盈率📈',
      category: '估值',
      unit: '倍',
      operators: ['大于']
    };
    assert.strictEqual(validateCatalogEntry(entry), true);
  });
});