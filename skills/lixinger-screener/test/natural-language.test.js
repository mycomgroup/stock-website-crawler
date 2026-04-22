import { test, describe, beforeEach, afterEach } from 'node:test';
import assert from 'node:assert';
import {
  validateLlmEnv,
  validateUnifiedQuery
} from '../shared/natural-language.js';

const sampleConditionCatalog = [
  {
    metric: 'PE-TTM',
    displayLabelExample: 'PE-TTM',
    category: '基本指标',
    selectors: []
  },
  {
    metric: 'PE-TTM统计值',
    displayLabelExample: 'PE-TTM统计值(1年)·分位点%',
    category: '基本指标',
    selectors: [
      {
        name: 'selector1',
        defaultLabel: '1年',
        defaultValue: 'y1',
        options: [
          { label: '1年', value: 'y1' },
          { label: '3年', value: 'y3' }
        ]
      },
      {
        name: 'selector2',
        defaultLabel: '分位点%',
        defaultValue: 'cvpos',
        options: [
          { label: '分位点%', value: 'cvpos' },
          { label: '20%分位点值', value: 'q2v' }
        ]
      }
    ]
  }
];

const sampleBrowserCatalog = [
  {
    displayName: '市盈率(TTM)',
    name: 'pe_ttm',
    category: '估值',
    unit: '倍',
    operators: ['大于', '小于', '介于']
  },
  {
    displayName: '市净率',
    name: 'pb',
    category: '估值',
    unit: '倍',
    operators: ['大于', '小于', '介于']
  }
];

describe('validateLlmEnv', () => {
  let originalApiKey;
  let originalBaseUrl;

  beforeEach(() => {
    originalApiKey = process.env.LLM_API_KEY;
    originalBaseUrl = process.env.LLM_BASE_URL;
  });

  afterEach(() => {
    if (originalApiKey !== undefined) {
      process.env.LLM_API_KEY = originalApiKey;
    } else {
      delete process.env.LLM_API_KEY;
    }
    if (originalBaseUrl !== undefined) {
      process.env.LLM_BASE_URL = originalBaseUrl;
    } else {
      delete process.env.LLM_BASE_URL;
    }
  });

  test('should return valid when LLM_API_KEY is set', () => {
    process.env.LLM_API_KEY = 'test-key';
    const result = validateLlmEnv();
    assert.strictEqual(result.valid, true);
    assert.deepStrictEqual(result.missing, []);
  });

  test('should return invalid when LLM_API_KEY is missing', () => {
    delete process.env.LLM_API_KEY;
    const result = validateLlmEnv();
    assert.strictEqual(result.valid, false);
    assert.deepStrictEqual(result.missing, ['LLM_API_KEY']);
  });

  test('should return invalid when LLM_API_KEY is empty string', () => {
    process.env.LLM_API_KEY = '';
    const result = validateLlmEnv();
    assert.strictEqual(result.valid, false);
    assert.deepStrictEqual(result.missing, ['LLM_API_KEY']);
  });

  test('should not require LLM_BASE_URL', () => {
    process.env.LLM_API_KEY = 'test-key';
    delete process.env.LLM_BASE_URL;
    const result = validateLlmEnv();
    assert.strictEqual(result.valid, true);
  });

  test('should work with both LLM_API_KEY and LLM_BASE_URL set', () => {
    process.env.LLM_API_KEY = 'test-key';
    process.env.LLM_BASE_URL = 'https://api.example.com';
    const result = validateLlmEnv();
    assert.strictEqual(result.valid, true);
  });

  test('should only check for LLM_API_KEY in missing array', () => {
    delete process.env.LLM_API_KEY;
    const result = validateLlmEnv();
    assert.ok(result.missing.includes('LLM_API_KEY'));
    assert.strictEqual(result.missing.length, 1);
  });
});

describe('queryToUnifiedInput - environment validation', () => {
  let originalApiKey;

  beforeEach(() => {
    originalApiKey = process.env.LLM_API_KEY;
  });

  afterEach(() => {
    if (originalApiKey !== undefined) {
      process.env.LLM_API_KEY = originalApiKey;
    } else {
      delete process.env.LLM_API_KEY;
    }
  });

  test('should throw error when LLM_API_KEY is missing', async () => {
    delete process.env.LLM_API_KEY;
    const { queryToUnifiedInput } = await import('../shared/natural-language.js');
    await assert.rejects(
      queryToUnifiedInput('test query', sampleConditionCatalog),
      /缺少必要的环境变量/
    );
  });

  test('should throw error for unsupported catalog format', async () => {
    process.env.LLM_API_KEY = 'test-key';
    const { queryToUnifiedInput } = await import('../shared/natural-language.js');
    const invalidCatalog = [{ unknown: 'format' }];
    
    await assert.rejects(
      queryToUnifiedInput('test query', invalidCatalog),
      /Unsupported catalog format/
    );
  });

  test('should throw error for empty catalog', async () => {
    process.env.LLM_API_KEY = 'test-key';
    const { queryToUnifiedInput } = await import('../shared/natural-language.js');
    
    await assert.rejects(
      queryToUnifiedInput('test query', []),
      /Unsupported catalog format/
    );
  });

  test('should throw error for null catalog', async () => {
    process.env.LLM_API_KEY = 'test-key';
    const { queryToUnifiedInput } = await import('../shared/natural-language.js');
    
    await assert.rejects(
      queryToUnifiedInput('test query', null),
      /Unsupported catalog format/
    );
  });

  test('should throw error for undefined catalog', async () => {
    process.env.LLM_API_KEY = 'test-key';
    const { queryToUnifiedInput } = await import('../shared/natural-language.js');
    
    await assert.rejects(
      queryToUnifiedInput('test query', undefined),
      /Unsupported catalog format/
    );
  });
});

describe('validateUnifiedQuery', () => {
  describe('with condition catalog', () => {
    test('should return valid for empty conditions', () => {
      const result = validateUnifiedQuery({ conditions: [] }, sampleConditionCatalog);
      assert.strictEqual(result.valid, true);
      assert.deepStrictEqual(result.errors, []);
    });

    test('should return valid for valid condition', () => {
      const input = {
        conditions: [
          { metric: 'PE-TTM', operator: '大于', value: 10 }
        ]
      };
      const result = validateUnifiedQuery(input, sampleConditionCatalog);
      assert.strictEqual(result.valid, true);
      assert.deepStrictEqual(result.errors, []);
    });

    test('should return invalid for unknown metric', () => {
      const input = {
        conditions: [
          { metric: 'UNKNOWN-METRIC', operator: '大于', value: 10 }
        ]
      };
      const result = validateUnifiedQuery(input, sampleConditionCatalog);
      assert.strictEqual(result.valid, false);
      assert.ok(result.errors.some(e => e.includes('UNKNOWN-METRIC') && e.includes('不在条件目录中')));
    });

    test('should return invalid for invalid selector option', () => {
      const input = {
        conditions: [
          { 
            metric: 'PE-TTM统计值', 
            selectors: ['1年', '无效选项'],
            operator: '大于', 
            value: 10 
          }
        ]
      };
      const result = validateUnifiedQuery(input, sampleConditionCatalog);
      assert.strictEqual(result.valid, false);
      assert.ok(result.errors.some(e => e.includes('不支持') && e.includes('无效选项')));
    });

    test('should return valid for correct selector options', () => {
      const input = {
        conditions: [
          { 
            metric: 'PE-TTM统计值', 
            selectors: ['1年', '分位点%'],
            operator: '大于', 
            value: 10 
          }
        ]
      };
      const result = validateUnifiedQuery(input, sampleConditionCatalog);
      assert.strictEqual(result.valid, true);
    });

    test('should return invalid for extra selector', () => {
      const input = {
        conditions: [
          { 
            metric: 'PE-TTM', 
            selectors: ['extra'],
            operator: '大于', 
            value: 10 
          }
        ]
      };
      const result = validateUnifiedQuery(input, sampleConditionCatalog);
      assert.strictEqual(result.valid, false);
      assert.ok(result.errors.some(e => e.includes('不支持第') && e.includes('selector')));
    });

    test('should handle input without conditions array', () => {
      const result = validateUnifiedQuery({}, sampleConditionCatalog);
      assert.strictEqual(result.valid, true);
    });

    test('should handle null input', () => {
      const result = validateUnifiedQuery(null, sampleConditionCatalog);
      assert.strictEqual(result.valid, true);
    });

    test('should handle undefined input', () => {
      const result = validateUnifiedQuery(undefined, sampleConditionCatalog);
      assert.strictEqual(result.valid, true);
    });

    test('should handle input with conditions not being array', () => {
      const result = validateUnifiedQuery({ conditions: 'not-array' }, sampleConditionCatalog);
      assert.strictEqual(result.valid, true);
    });

    test('should collect multiple errors', () => {
      const input = {
        conditions: [
          { metric: 'UNKNOWN-1', operator: '大于', value: 10 },
          { metric: 'UNKNOWN-2', operator: '小于', value: 20 }
        ]
      };
      const result = validateUnifiedQuery(input, sampleConditionCatalog);
      assert.strictEqual(result.valid, false);
      assert.strictEqual(result.errors.length, 2);
    });

    test('should handle condition without selectors property', () => {
      const input = {
        conditions: [
          { metric: 'PE-TTM统计值', operator: '大于', value: 10 }
        ]
      };
      const result = validateUnifiedQuery(input, sampleConditionCatalog);
      assert.strictEqual(result.valid, true);
    });

    test('should handle condition with empty selectors array', () => {
      const input = {
        conditions: [
          { metric: 'PE-TTM统计值', selectors: [], operator: '大于', value: 10 }
        ]
      };
      const result = validateUnifiedQuery(input, sampleConditionCatalog);
      assert.strictEqual(result.valid, true);
    });

    test('should handle entry without selectors', () => {
      const catalogWithoutSelectors = [
        { metric: 'TEST', displayLabelExample: 'Test', selectors: undefined }
      ];
      const input = {
        conditions: [
          { metric: 'TEST', selectors: ['any'], operator: '大于', value: 10 }
        ]
      };
      const result = validateUnifiedQuery(input, catalogWithoutSelectors);
      assert.strictEqual(result.valid, false);
    });

    test('should validate multiple selector positions', () => {
      const input = {
        conditions: [
          { 
            metric: 'PE-TTM统计值', 
            selectors: ['无效选项', '分位点%'],
            operator: '大于', 
            value: 10 
          }
        ]
      };
      const result = validateUnifiedQuery(input, sampleConditionCatalog);
      assert.strictEqual(result.valid, false);
      assert.ok(result.errors.some(e => e.includes('selector 1') && e.includes('无效选项')));
    });

    test('should handle selector with null options', () => {
      const catalogWithNullOptions = [
        { 
          metric: 'TEST', 
          displayLabelExample: 'Test',
          selectors: [{ name: 's1', options: null }]
        }
      ];
      const input = {
        conditions: [
          { metric: 'TEST', selectors: ['option1'], operator: '大于', value: 10 }
        ]
      };
      const result = validateUnifiedQuery(input, catalogWithNullOptions);
      assert.strictEqual(result.valid, false);
      assert.ok(result.errors.some(e => e.includes('不支持')));
    });

    test('should handle selector with undefined options', () => {
      const catalogWithUndefinedOptions = [
        { 
          metric: 'TEST', 
          displayLabelExample: 'Test',
          selectors: [{ name: 's1', options: undefined }]
        }
      ];
      const input = {
        conditions: [
          { metric: 'TEST', selectors: ['option1'], operator: '大于', value: 10 }
        ]
      };
      const result = validateUnifiedQuery(input, catalogWithUndefinedOptions);
      assert.strictEqual(result.valid, false);
      assert.ok(result.errors.some(e => e.includes('不支持')));
    });

    test('should handle selector with empty options array', () => {
      const catalogWithEmptyOptions = [
        { 
          metric: 'TEST', 
          displayLabelExample: 'Test',
          selectors: [{ name: 's1', options: [] }]
        }
      ];
      const input = {
        conditions: [
          { metric: 'TEST', selectors: ['option1'], operator: '大于', value: 10 }
        ]
      };
      const result = validateUnifiedQuery(input, catalogWithEmptyOptions);
      assert.strictEqual(result.valid, false);
      assert.ok(result.errors.some(e => e.includes('不支持')));
    });

    test('should validate first selector correctly when second is valid', () => {
      const input = {
        conditions: [
          { 
            metric: 'PE-TTM统计值', 
            selectors: ['无效', '分位点%'],
            operator: '大于', 
            value: 10 
          }
        ]
      };
      const result = validateUnifiedQuery(input, sampleConditionCatalog);
      assert.strictEqual(result.valid, false);
      assert.strictEqual(result.errors.length, 1);
    });

    test('should validate both selectors when both invalid', () => {
      const input = {
        conditions: [
          { 
            metric: 'PE-TTM统计值', 
            selectors: ['无效1', '无效2'],
            operator: '大于', 
            value: 10 
          }
        ]
      };
      const result = validateUnifiedQuery(input, sampleConditionCatalog);
      assert.strictEqual(result.valid, false);
      assert.strictEqual(result.errors.length, 2);
    });
  });

  describe('with browser catalog', () => {
    test('should return valid for valid field', () => {
      const input = {
        conditions: [
          { field: '市盈率(TTM)', operator: '大于', value: 10 }
        ]
      };
      const result = validateUnifiedQuery(input, sampleBrowserCatalog);
      assert.strictEqual(result.valid, true);
    });

    test('should return invalid for unknown field', () => {
      const input = {
        conditions: [
          { field: '未知字段', operator: '大于', value: 10 }
        ]
      };
      const result = validateUnifiedQuery(input, sampleBrowserCatalog);
      assert.strictEqual(result.valid, false);
      assert.ok(result.errors.some(e => e.includes('未知字段') && e.includes('不在 metrics-catalog 中')));
    });

    test('should accept displayLabel as field fallback', () => {
      const input = {
        conditions: [
          { displayLabel: '市盈率(TTM)', operator: '大于', value: 10 }
        ]
      };
      const result = validateUnifiedQuery(input, sampleBrowserCatalog);
      assert.strictEqual(result.valid, true);
    });

    test('should handle empty conditions', () => {
      const result = validateUnifiedQuery({ conditions: [] }, sampleBrowserCatalog);
      assert.strictEqual(result.valid, true);
    });

    test('should handle null input', () => {
      const result = validateUnifiedQuery(null, sampleBrowserCatalog);
      assert.strictEqual(result.valid, true);
    });

    test('should collect multiple errors for browser catalog', () => {
      const input = {
        conditions: [
          { field: '未知1', operator: '大于', value: 10 },
          { field: '未知2', operator: '小于', value: 20 }
        ]
      };
      const result = validateUnifiedQuery(input, sampleBrowserCatalog);
      assert.strictEqual(result.valid, false);
      assert.strictEqual(result.errors.length, 2);
    });

    test('should handle condition without field or displayLabel', () => {
      const input = {
        conditions: [
          { operator: '大于', value: 10 }
        ]
      };
      const result = validateUnifiedQuery(input, sampleBrowserCatalog);
      assert.strictEqual(result.valid, false);
      assert.ok(result.errors.some(e => e.includes('undefined') || e.includes('不在')));
    });

    test('should handle field that is null', () => {
      const input = {
        conditions: [
          { field: null, operator: '大于', value: 10 }
        ]
      };
      const result = validateUnifiedQuery(input, sampleBrowserCatalog);
      assert.strictEqual(result.valid, false);
    });

    test('should prefer field over displayLabel', () => {
      const input = {
        conditions: [
          { field: '市盈率(TTM)', displayLabel: '市净率', operator: '大于', value: 10 }
        ]
      };
      const result = validateUnifiedQuery(input, sampleBrowserCatalog);
      assert.strictEqual(result.valid, true);
    });

    test('should use displayLabel when field is empty string', () => {
      const input = {
        conditions: [
          { field: '', displayLabel: '市盈率(TTM)', operator: '大于', value: 10 }
        ]
      };
      const result = validateUnifiedQuery(input, sampleBrowserCatalog);
      assert.strictEqual(result.valid, true);
    });

    test('should handle multiple valid conditions', () => {
      const input = {
        conditions: [
          { field: '市盈率(TTM)', operator: '大于', value: 10 },
          { field: '市净率', operator: '小于', value: 5 }
        ]
      };
      const result = validateUnifiedQuery(input, sampleBrowserCatalog);
      assert.strictEqual(result.valid, true);
      assert.strictEqual(result.errors.length, 0);
    });
  });

  describe('with invalid catalog format', () => {
    test('should return error for unsupported catalog format', () => {
      const invalidCatalog = [{ unknown: 'format' }];
      const input = { conditions: [{ metric: 'test' }] };
      const result = validateUnifiedQuery(input, invalidCatalog);
      assert.strictEqual(result.valid, false);
      assert.ok(result.errors.some(e => e.includes('Unsupported catalog format')));
    });

    test('should handle null catalog', () => {
      const input = { conditions: [] };
      const result = validateUnifiedQuery(input, null);
      assert.strictEqual(result.valid, false);
      assert.ok(result.errors.some(e => e.includes('Unsupported catalog format')));
    });

    test('should handle undefined catalog', () => {
      const input = { conditions: [] };
      const result = validateUnifiedQuery(input, undefined);
      assert.strictEqual(result.valid, false);
      assert.ok(result.errors.some(e => e.includes('Unsupported catalog format')));
    });

    test('should handle empty array catalog', () => {
      const input = { conditions: [] };
      const result = validateUnifiedQuery(input, []);
      assert.strictEqual(result.valid, false);
      assert.ok(result.errors.some(e => e.includes('Unsupported catalog format')));
    });

    test('should handle catalog with null first entry', () => {
      const catalog = [null];
      const input = { conditions: [] };
      const result = validateUnifiedQuery(input, catalog);
      assert.strictEqual(result.valid, false);
      assert.ok(result.errors.some(e => e.includes('Unsupported catalog format')));
    });

    test('should handle catalog with undefined first entry', () => {
      const catalog = [undefined];
      const input = { conditions: [] };
      const result = validateUnifiedQuery(input, catalog);
      assert.strictEqual(result.valid, false);
      assert.ok(result.errors.some(e => e.includes('Unsupported catalog format')));
    });
  });
});