import { test, describe, beforeEach, afterEach, mock } from 'node:test';
import assert from 'node:assert';
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import {
  loadJson,
  saveJson,
  loadConditionCatalog,
  loadConditionMetrics,
  loadBrowserMetricsCatalog,
  resolveCatalogPath,
  conditionCatalogExists,
  getConditionDisplayLabel,
  isConditionMetricEntry,
  isBrowserMetricEntry,
  DEFAULT_CONDITION_CATALOG_PATH,
  DEFAULT_BROWSER_METRICS_CATALOG_PATH
} from '../shared/catalog.js';

const sampleConditionCatalog = {
  generatedAt: '2026-03-24T02:30:37.952Z',
  page: 'company-fundamental',
  areaCode: 'cn',
  metrics: [
    {
      category: '基本指标',
      metric: 'PE-TTM',
      displayLabelExample: 'PE-TTM',
      formulaIdExample: 'pm.pe_ttm.latest',
      requestIdExample: 'pm.pe_ttm',
      resultFieldKey: 'pe_ttm',
      selectors: [],
      thresholds: { min: { inputType: 'number' }, max: { inputType: 'number' } }
    },
    {
      category: '基本指标',
      metric: 'PE-TTM统计值',
      displayLabelExample: 'PE-TTM统计值(1年)·分位点%',
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
  ]
};

const sampleBrowserMetricsCatalog = [
  {
    name: '市盈率(TTM)',
    displayName: '市盈率(TTM)',
    category: '估值',
    unit: '倍',
    operators: ['大于', '小于', '介于']
  },
  {
    name: '市净率',
    displayName: '市净率',
    category: '估值',
    unit: '倍',
    operators: ['大于', '小于', '介于']
  }
];

describe('loadJson', () => {
  let tempDir;
  let tempFile;

  beforeEach(() => {
    tempDir = fs.mkdtempSync(path.join(os.tmpdir(), 'catalog-test-'));
    tempFile = path.join(tempDir, 'test.json');
  });

  afterEach(() => {
    fs.rmSync(tempDir, { recursive: true, force: true });
  });

  test('should load and parse valid JSON file', () => {
    const data = { name: 'test', value: 123 };
    fs.writeFileSync(tempFile, JSON.stringify(data));
    const result = loadJson(tempFile);
    assert.deepStrictEqual(result, data);
  });

  test('should load JSON array', () => {
    const data = [1, 2, 3];
    fs.writeFileSync(tempFile, JSON.stringify(data));
    const result = loadJson(tempFile);
    assert.deepStrictEqual(result, data);
  });

  test('should throw for non-existent file', () => {
    assert.throws(
      () => loadJson(path.join(tempDir, 'nonexistent.json')),
      { code: 'ENOENT' }
    );
  });

  test('should throw for invalid JSON', () => {
    fs.writeFileSync(tempFile, 'not valid json {');
    assert.throws(
      () => loadJson(tempFile),
      { name: 'SyntaxError' }
    );
  });

  test('should load JSON with nested objects', () => {
    const data = { level1: { level2: { level3: 'deep' } } };
    fs.writeFileSync(tempFile, JSON.stringify(data));
    const result = loadJson(tempFile);
    assert.strictEqual(result.level1.level2.level3, 'deep');
  });

  test('should load JSON with special characters', () => {
    const data = { message: '中文测试 🎉 \n\t' };
    fs.writeFileSync(tempFile, JSON.stringify(data));
    const result = loadJson(tempFile);
    assert.strictEqual(result.message, data.message);
  });
});

describe('saveJson', () => {
  let tempDir;
  let tempFile;

  beforeEach(() => {
    tempDir = fs.mkdtempSync(path.join(os.tmpdir(), 'catalog-test-'));
    tempFile = path.join(tempDir, 'output.json');
  });

  afterEach(() => {
    fs.rmSync(tempDir, { recursive: true, force: true });
  });

  test('should save object to JSON file', () => {
    const data = { name: 'test', value: 123 };
    saveJson(tempFile, data);
    const content = fs.readFileSync(tempFile, 'utf8');
    assert.deepStrictEqual(JSON.parse(content), data);
  });

  test('should save array to JSON file', () => {
    const data = [1, 2, 3];
    saveJson(tempFile, data);
    const content = fs.readFileSync(tempFile, 'utf8');
    assert.deepStrictEqual(JSON.parse(content), data);
  });

  test('should format JSON with 2-space indentation', () => {
    const data = { a: 1 };
    saveJson(tempFile, data);
    const content = fs.readFileSync(tempFile, 'utf8');
    assert.strictEqual(content, '{\n  "a": 1\n}');
  });

  test('should create parent directories if they do not exist', () => {
    const nestedFile = path.join(tempDir, 'sub1', 'sub2', 'output.json');
    saveJson(nestedFile, { test: true });
    assert.ok(fs.existsSync(nestedFile));
  });

  test('should overwrite existing file', () => {
    fs.writeFileSync(tempFile, '{"old": true}');
    saveJson(tempFile, { new: true });
    const content = fs.readFileSync(tempFile, 'utf8');
    assert.deepStrictEqual(JSON.parse(content), { new: true });
  });

  test('should handle null values', () => {
    const data = { value: null };
    saveJson(tempFile, data);
    const result = JSON.parse(fs.readFileSync(tempFile, 'utf8'));
    assert.strictEqual(result.value, null);
  });

  test('should handle empty object', () => {
    saveJson(tempFile, {});
    const content = fs.readFileSync(tempFile, 'utf8');
    assert.strictEqual(content, '{}');
  });

  test('should handle empty array', () => {
    saveJson(tempFile, []);
    const content = fs.readFileSync(tempFile, 'utf8');
    assert.strictEqual(content, '[]');
  });
});

describe('loadConditionCatalog', () => {
  let tempDir;
  let tempFile;

  beforeEach(() => {
    tempDir = fs.mkdtempSync(path.join(os.tmpdir(), 'catalog-test-'));
    tempFile = path.join(tempDir, 'condition-catalog.json');
  });

  afterEach(() => {
    fs.rmSync(tempDir, { recursive: true, force: true });
  });

  test('should load catalog with default path', () => {
    const loadJsonMock = mock.fn(() => sampleConditionCatalog);
    mock.method(fs, 'readFileSync', () => JSON.stringify(sampleConditionCatalog));
    
    const result = loadConditionCatalog();
    assert.ok(result.metrics);
    mock.restoreAll();
  });

  test('should load catalog with custom path', () => {
    fs.writeFileSync(tempFile, JSON.stringify(sampleConditionCatalog));
    const result = loadConditionCatalog(tempFile);
    assert.deepStrictEqual(result, sampleConditionCatalog);
  });

  test('should throw for non-existent file', () => {
    assert.throws(
      () => loadConditionCatalog(path.join(tempDir, 'nonexistent.json')),
      { code: 'ENOENT' }
    );
  });
});

describe('loadConditionMetrics', () => {
  let tempDir;
  let tempFile;

  beforeEach(() => {
    tempDir = fs.mkdtempSync(path.join(os.tmpdir(), 'catalog-test-'));
    tempFile = path.join(tempDir, 'condition-catalog.json');
  });

  afterEach(() => {
    fs.rmSync(tempDir, { recursive: true, force: true });
  });

  test('should extract metrics array from catalog', () => {
    fs.writeFileSync(tempFile, JSON.stringify(sampleConditionCatalog));
    const result = loadConditionMetrics(tempFile);
    assert.strictEqual(result.length, 2);
    assert.strictEqual(result[0].metric, 'PE-TTM');
  });

  test('should throw for catalog without metrics', () => {
    fs.writeFileSync(tempFile, JSON.stringify({ page: 'test' }));
    assert.throws(
      () => loadConditionMetrics(tempFile),
      /Invalid condition catalog/
    );
  });

  test('should throw for catalog with non-array metrics', () => {
    fs.writeFileSync(tempFile, JSON.stringify({ metrics: 'not-an-array' }));
    assert.throws(
      () => loadConditionMetrics(tempFile),
      /Invalid condition catalog/
    );
  });

  test('should throw for null catalog', () => {
    fs.writeFileSync(tempFile, 'null');
    assert.throws(
      () => loadConditionMetrics(tempFile),
      /Invalid condition catalog/
    );
  });

  test('should return empty array if metrics is empty', () => {
    fs.writeFileSync(tempFile, JSON.stringify({ metrics: [] }));
    const result = loadConditionMetrics(tempFile);
    assert.deepStrictEqual(result, []);
  });
});

describe('loadBrowserMetricsCatalog', () => {
  let tempDir;
  let tempFile;

  beforeEach(() => {
    tempDir = fs.mkdtempSync(path.join(os.tmpdir(), 'catalog-test-'));
    tempFile = path.join(tempDir, 'metrics-catalog.json');
  });

  afterEach(() => {
    fs.rmSync(tempDir, { recursive: true, force: true });
  });

  test('should load browser metrics catalog array', () => {
    fs.writeFileSync(tempFile, JSON.stringify(sampleBrowserMetricsCatalog));
    const result = loadBrowserMetricsCatalog(tempFile);
    assert.strictEqual(result.length, 2);
    assert.strictEqual(result[0].displayName, '市盈率(TTM)');
  });

  test('should throw for non-array catalog', () => {
    fs.writeFileSync(tempFile, JSON.stringify({ notArray: true }));
    assert.throws(
      () => loadBrowserMetricsCatalog(tempFile),
      /Invalid browser metrics catalog/
    );
  });

  test('should throw for null catalog', () => {
    fs.writeFileSync(tempFile, 'null');
    assert.throws(
      () => loadBrowserMetricsCatalog(tempFile),
      /Invalid browser metrics catalog/
    );
  });

  test('should return empty array for empty array', () => {
    fs.writeFileSync(tempFile, '[]');
    const result = loadBrowserMetricsCatalog(tempFile);
    assert.deepStrictEqual(result, []);
  });
});

describe('resolveCatalogPath', () => {
  test('should return resolved catalogPath when provided', () => {
    const result = resolveCatalogPath('./custom.json', '/base/dir');
    assert.strictEqual(result, '/base/dir/custom.json');
  });

  test('should return absolute catalogPath as-is', () => {
    const result = resolveCatalogPath('/absolute/path.json', '/other/dir');
    assert.strictEqual(result, '/absolute/path.json');
  });

  test('should use profileCatalogPath when catalogPath is not provided (absolute)', () => {
    const result = resolveCatalogPath(null, '/base/dir', '/absolute/profile.json');
    assert.strictEqual(result, '/absolute/profile.json');
  });

  test('should resolve profileCatalogPath relative to LIXINGER_OUTPUT_DIR when relative', () => {
    const result = resolveCatalogPath(null, '/base/dir', 'relative/profile.json');
    assert.ok(result.includes('data/relative/profile.json'));
  });

  test('should return default path when no paths provided', () => {
    const result = resolveCatalogPath(null, '/base/dir', null);
    assert.strictEqual(result, DEFAULT_CONDITION_CATALOG_PATH);
  });

  test('should prioritize catalogPath over profileCatalogPath', () => {
    const result = resolveCatalogPath('./catalog.json', '/base/dir', '/profile.json');
    assert.strictEqual(result, '/base/dir/catalog.json');
  });

  test('should handle undefined parameters', () => {
    const result = resolveCatalogPath(undefined, undefined, undefined);
    assert.strictEqual(result, DEFAULT_CONDITION_CATALOG_PATH);
  });

  test('should handle empty string catalogPath', () => {
    const result = resolveCatalogPath('', '/base/dir', '/profile.json');
    assert.strictEqual(result, '/profile.json');
  });
});

describe('conditionCatalogExists', () => {
  let tempDir;
  let tempFile;

  beforeEach(() => {
    tempDir = fs.mkdtempSync(path.join(os.tmpdir(), 'catalog-test-'));
    tempFile = path.join(tempDir, 'exists.json');
    fs.writeFileSync(tempFile, '{}');
  });

  afterEach(() => {
    fs.rmSync(tempDir, { recursive: true, force: true });
  });

  test('should return true for existing file', () => {
    assert.strictEqual(conditionCatalogExists(tempFile), true);
  });

  test('should return false for non-existing file', () => {
    assert.strictEqual(conditionCatalogExists(path.join(tempDir, 'not-exist.json')), false);
  });

  test('should use default path when no argument provided', () => {
    const result = conditionCatalogExists();
    assert.strictEqual(typeof result, 'boolean');
  });

  test('should return false for directory path', () => {
    assert.strictEqual(conditionCatalogExists(tempDir), true);
  });
});

describe('getConditionDisplayLabel', () => {
  test('should return displayLabelExample when present', () => {
    const entry = { metric: 'PE-TTM', displayLabelExample: 'PE-TTM值' };
    assert.strictEqual(getConditionDisplayLabel(entry), 'PE-TTM值');
  });

  test('should return metric when displayLabelExample is missing', () => {
    const entry = { metric: 'PE-TTM' };
    assert.strictEqual(getConditionDisplayLabel(entry), 'PE-TTM');
  });

  test('should prefer displayLabelExample over metric', () => {
    const entry = { metric: 'PE-TTM', displayLabelExample: 'Custom Label' };
    assert.strictEqual(getConditionDisplayLabel(entry), 'Custom Label');
  });

  test('should return null for null entry', () => {
    assert.strictEqual(getConditionDisplayLabel(null), null);
  });

  test('should return null for undefined entry', () => {
    assert.strictEqual(getConditionDisplayLabel(undefined), null);
  });

  test('should return null for empty object', () => {
    assert.strictEqual(getConditionDisplayLabel({}), null);
  });

  test('should return null for entry without metric or displayLabelExample', () => {
    const entry = { category: 'test' };
    assert.strictEqual(getConditionDisplayLabel(entry), null);
  });

  test('should return metric when displayLabelExample is empty string', () => {
    const entry = { metric: 'PE-TTM', displayLabelExample: '' };
    assert.strictEqual(getConditionDisplayLabel(entry), 'PE-TTM');
  });

  test('should return null when both are missing', () => {
    const entry = { category: 'test', selectors: [] };
    assert.strictEqual(getConditionDisplayLabel(entry), null);
  });
});

describe('isConditionMetricEntry', () => {
  test('should return true for valid condition metric entry', () => {
    const entry = { metric: 'PE-TTM', displayLabelExample: 'PE-TTM值' };
    assert.strictEqual(isConditionMetricEntry(entry), true);
  });

  test('should return false for entry without metric', () => {
    const entry = { displayLabelExample: 'Test' };
    assert.strictEqual(isConditionMetricEntry(entry), false);
  });

  test('should return false for entry without displayLabelExample', () => {
    const entry = { metric: 'PE-TTM' };
    assert.strictEqual(isConditionMetricEntry(entry), false);
  });

  test('should return true when displayLabelExample is empty string', () => {
    const entry = { metric: 'PE-TTM', displayLabelExample: '' };
    assert.strictEqual(isConditionMetricEntry(entry), true);
  });

  test('should return false for null entry', () => {
    assert.strictEqual(isConditionMetricEntry(null), false);
  });

  test('should return false for undefined entry', () => {
    assert.strictEqual(isConditionMetricEntry(undefined), false);
  });

  test('should return false for empty object', () => {
    assert.strictEqual(isConditionMetricEntry({}), false);
  });

  test('should return false for browser metric entry', () => {
    const entry = { displayName: '市盈率', operators: ['大于', '小于'] };
    assert.strictEqual(isConditionMetricEntry(entry), false);
  });

  test('should return true for entry with additional properties', () => {
    const entry = { 
      metric: 'PE-TTM', 
      displayLabelExample: 'PE-TTM值',
      category: '基本指标',
      selectors: []
    };
    assert.strictEqual(isConditionMetricEntry(entry), true);
  });
});

describe('isBrowserMetricEntry', () => {
  test('should return true for valid browser metric entry', () => {
    const entry = { displayName: '市盈率', operators: ['大于', '小于', '介于'] };
    assert.strictEqual(isBrowserMetricEntry(entry), true);
  });

  test('should return false for entry without displayName', () => {
    const entry = { operators: ['大于', '小于'] };
    assert.strictEqual(isBrowserMetricEntry(entry), false);
  });

  test('should return false for entry without operators', () => {
    const entry = { displayName: '市盈率' };
    assert.strictEqual(isBrowserMetricEntry(entry), false);
  });

  test('should return false for entry with non-array operators', () => {
    const entry = { displayName: '市盈率', operators: 'not-array' };
    assert.strictEqual(isBrowserMetricEntry(entry), false);
  });

  test('should return false for entry with null operators', () => {
    const entry = { displayName: '市盈率', operators: null };
    assert.strictEqual(isBrowserMetricEntry(entry), false);
  });

  test('should return true for entry with empty operators array', () => {
    const entry = { displayName: '市盈率', operators: [] };
    assert.strictEqual(isBrowserMetricEntry(entry), true);
  });

  test('should return false for null entry', () => {
    assert.strictEqual(isBrowserMetricEntry(null), false);
  });

  test('should return false for undefined entry', () => {
    assert.strictEqual(isBrowserMetricEntry(undefined), false);
  });

  test('should return false for empty object', () => {
    assert.strictEqual(isBrowserMetricEntry({}), false);
  });

  test('should return false for condition metric entry', () => {
    const entry = { metric: 'PE-TTM', displayLabelExample: 'PE-TTM值' };
    assert.strictEqual(isBrowserMetricEntry(entry), false);
  });

  test('should return true for entry with additional properties', () => {
    const entry = { 
      displayName: '市盈率', 
      operators: ['大于'],
      name: 'pe',
      category: '估值',
      unit: '倍'
    };
    assert.strictEqual(isBrowserMetricEntry(entry), true);
  });
});

describe('DEFAULT_*_PATH constants', () => {
  test('DEFAULT_CONDITION_CATALOG_PATH should be a string', () => {
    assert.strictEqual(typeof DEFAULT_CONDITION_CATALOG_PATH, 'string');
  });

  test('DEFAULT_BROWSER_METRICS_CATALOG_PATH should be a string', () => {
    assert.strictEqual(typeof DEFAULT_BROWSER_METRICS_CATALOG_PATH, 'string');
  });

  test('DEFAULT_CONDITION_CATALOG_PATH should end with condition-catalog.cn.json', () => {
    assert.ok(DEFAULT_CONDITION_CATALOG_PATH.endsWith('condition-catalog.cn.json'));
  });

  test('DEFAULT_BROWSER_METRICS_CATALOG_PATH should end with metrics-catalog.json', () => {
    assert.ok(DEFAULT_BROWSER_METRICS_CATALOG_PATH.endsWith('metrics-catalog.json'));
  });
});