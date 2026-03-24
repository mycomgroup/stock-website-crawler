import { test } from 'node:test';
import assert from 'node:assert';
import {
  buildBrowserFiltersFromUnifiedInput,
  buildRequestPlanFromUnifiedInput,
  normalizeUnifiedInput
} from '../unified-input.js';

const catalog = {
  metrics: [
    {
      category: '基本指标',
      metric: 'PE-TTM统计值',
      displayLabelExample: 'PE-TTM统计值(1年)·分位点%',
      formulaIdExample: 'pm.pe_ttm.y1.cvpos.latest',
      requestIdExample: 'pm.pe_ttm.y1.cvpos',
      resultFieldKey: 'pe_ttm.y1.cvpos',
      selectors: [
        {
          name: 'selector1',
          defaultLabel: '1年',
          defaultValue: 'y1',
          options: [
            { label: '1年', value: 'y1' },
            { label: '10年', value: 'y10' }
          ]
        },
        {
          name: 'selector2',
          defaultLabel: '分位点%',
          defaultValue: 'cvpos',
          options: [
            { label: '分位点%', value: 'cvpos' }
          ]
        }
      ],
      thresholds: {
        min: { inputType: 'number', unit: '%', scale: 0.01 },
        max: { inputType: 'number', unit: '%', scale: 0.01 }
      },
      notes: null,
      formulaIdTemplate: 'pm.pe_ttm.{selector1}.{selector2}.latest',
      requestIdTemplate: 'pm.pe_ttm.{selector1}.{selector2}',
      format: 'percentage',
      unit: '%',
      apiScale: 0.01,
      specialRequestId: null
    }
  ]
};

test('normalizeUnifiedInput converts operator/value into min/max', () => {
  const normalized = normalizeUnifiedInput({
    conditions: [
      { field: 'PE-TTM统计值(10年)·分位点%', operator: '介于', value: [0, 30] }
    ]
  });

  assert.deepStrictEqual(normalized.conditions[0], {
    field: 'PE-TTM统计值(10年)·分位点%',
    displayLabel: 'PE-TTM统计值(10年)·分位点%',
    operator: '介于',
    value: [0, 30],
    min: 0,
    max: 30
  });
});

test('buildBrowserFiltersFromUnifiedInput resolves metric selectors into browser field labels', () => {
  const filters = buildBrowserFiltersFromUnifiedInput({
    conditions: [
      { metric: 'PE-TTM统计值', selectors: ['10年', '分位点%'], min: 0, max: 30 }
    ]
  }, catalog);

  assert.deepStrictEqual(filters, [
    {
      field: 'PE-TTM统计值(10年)·分位点%',
      category: '基本指标',
      operator: '介于',
      value: [0, 30]
    }
  ]);
});

test('buildRequestPlanFromUnifiedInput reuses the same unified condition schema', () => {
  const plan = buildRequestPlanFromUnifiedInput({
    areaCode: 'cn',
    conditions: [
      { metric: 'PE-TTM统计值', selectors: ['10年', '分位点%'], min: 0, max: 30 }
    ]
  }, catalog);

  assert.deepStrictEqual(plan.body.filterList, [
    {
      id: 'pm.pe_ttm.y10.cvpos',
      value: 'all',
      date: 'latest',
      min: 0,
      max: 0.3
    }
  ]);
  assert.strictEqual(plan.columnSpecs[0].displayLabel, 'PE-TTM统计值(10年)·分位点%');
});
