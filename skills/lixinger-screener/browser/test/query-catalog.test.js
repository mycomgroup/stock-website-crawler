import { test } from 'node:test';
import assert from 'node:assert';
import {
  buildBrowserQueryCatalogCandidates,
  parseBrowserNaturalLanguageQuery
} from '../main.js';

test('browser-style growth queries prefer the browser metrics catalog first', () => {
  const candidates = buildBrowserQueryCatalogCandidates('营业收入增长率(YOY)大于10%');

  assert.strictEqual(candidates[0].name, 'browser-metrics-catalog');
  assert.strictEqual(candidates[1].name, 'condition-catalog');
});

test('historical percentile queries prefer the condition catalog first', () => {
  const candidates = buildBrowserQueryCatalogCandidates('PE-TTM(扣非)统计值10年分位点小于30%');

  assert.strictEqual(candidates[0].name, 'condition-catalog');
  assert.strictEqual(candidates[1].name, 'browser-metrics-catalog');
});

test('parseBrowserNaturalLanguageQuery falls back from browser catalog to condition catalog', async () => {
  const attemptedCatalogs = [];

  const result = await parseBrowserNaturalLanguageQuery(
    '资产负债率小于50%',
    {},
    null,
    async (_query, catalog) => {
      const isBrowserCatalog = Object.prototype.hasOwnProperty.call(catalog[0] || {}, 'displayName');
      attemptedCatalogs.push(isBrowserCatalog ? 'browser' : 'condition');

      if (isBrowserCatalog) {
        return {
          conditions: [
            { field: '不存在的浏览器字段', operator: '小于', value: 50 }
          ]
        };
      }

      const metric = catalog.find(item => item.metric === '资产负债率') || catalog[0];
      return {
        conditions: [
          { metric: metric.metric, category: metric.category, operator: '小于', value: 50 }
        ]
      };
    }
  );

  assert.deepStrictEqual(attemptedCatalogs, ['browser', 'condition']);
  assert.ok(result.richCatalog, 'fallback to condition catalog should preserve rich catalog');
  assert.strictEqual(result.parsed.conditions[0].metric, '资产负债率');
});

test('parseBrowserNaturalLanguageQuery can resolve condition-style queries without touching browser catalog', async () => {
  const attemptedCatalogs = [];

  const result = await parseBrowserNaturalLanguageQuery(
    'PE-TTM(扣非)统计值10年分位点小于30%',
    {},
    null,
    async (_query, catalog) => {
      const isBrowserCatalog = Object.prototype.hasOwnProperty.call(catalog[0] || {}, 'displayName');
      attemptedCatalogs.push(isBrowserCatalog ? 'browser' : 'condition');

      if (isBrowserCatalog) {
        throw new Error('browser catalog should not be attempted first for percentile queries');
      }

      const metric = catalog.find(item => item.metric === 'PE-TTM(扣非)统计值') || catalog[0];
      return {
        conditions: [
          {
            metric: metric.metric,
            category: metric.category,
            selectors: ['10年', '分位点%'],
            operator: '小于',
            value: 30
          }
        ]
      };
    }
  );

  assert.deepStrictEqual(attemptedCatalogs, ['condition']);
  assert.ok(result.richCatalog, 'condition-first parsing should expose the rich catalog');
  assert.strictEqual(result.parsed.conditions[0].metric, 'PE-TTM(扣非)统计值');
});
