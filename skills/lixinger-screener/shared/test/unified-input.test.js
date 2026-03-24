import { test } from 'node:test';
import assert from 'node:assert';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';
import {
  buildBrowserFiltersFromUnifiedInput,
  buildRequestPlanFromScreener,
  buildRequestPlanFromUnifiedInput,
  normalizeUnifiedInput
} from '../unified-input.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
const examplePath = resolve(__dirname, '..', '..', 'unified-input.example.json');

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
    },
    {
      category: '利润表',
      metric: '营业收入',
      displayLabelExample: '营业收入',
      formulaIdExample: 'q.ps.oi.t.dynamic~lq~y~0',
      requestIdExample: 'q.ps.oi.t.dynamic~lq~y~0',
      resultFieldKey: 'q.ps.oi.t.dynamic~lq~y~0',
      selectors: [],
      dateModes: [
        { label: '最新财报', value: 'latest_fs' },
        { label: '2024', value: '2024' }
      ],
      subConditionOptions: ['累积', 'TTM', 'TTM同比'],
      thresholds: {
        min: { inputType: 'number', unit: '亿', scale: 100000000 },
        max: { inputType: 'number', unit: '亿', scale: 100000000 }
      },
      notes: null,
      formulaIdTemplate: 'q.ps.oi.t.dynamic~lq~y~0',
      requestIdTemplate: 'q.ps.oi.t.dynamic~lq~y~0',
      format: 'yi',
      unit: '亿',
      apiScale: 100000000,
      specialRequestId: null
    },
    {
      category: '热度指标',
      metric: '过去20个交易日涨跌幅',
      displayLabelExample: '过去20个交易日涨跌幅',
      formulaIdExample: 'hm.vol.td_cr_20d.latest',
      requestIdExample: 'hm.vol.td_cr_20d',
      resultFieldKey: 'hm.vol.td_cr_20d',
      selectors: [],
      dateModes: [
        { label: '最新时间', value: 'latest_time' }
      ],
      subConditionOptions: [],
      thresholds: {
        min: { inputType: 'number', unit: '%', scale: 0.01 },
        max: { inputType: 'number', unit: '%', scale: 0.01 }
      },
      notes: null,
      formulaIdTemplate: 'hm.vol.td_cr_20d.latest',
      requestIdTemplate: 'hm.vol.td_cr_20d',
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

test('buildBrowserFiltersFromUnifiedInput preserves dateMode and subCondition for browser execution', () => {
  const filters = buildBrowserFiltersFromUnifiedInput({
    conditions: [
      {
        metric: '营业收入',
        category: '利润表',
        dateMode: '2024',
        subCondition: 'TTM',
        min: 10
      }
    ]
  }, catalog);

  assert.deepStrictEqual(filters, [
    {
      field: '营业收入',
      category: '利润表',
      dateModeLabel: '2024',
      dateModeApi: '2024',
      subCondition: 'TTM',
      operator: '大于',
      value: 10
    }
  ]);
});

test('buildBrowserFiltersFromUnifiedInput falls back to browser catalog for cashflow valuation fields', () => {
  const filters = buildBrowserFiltersFromUnifiedInput({
    conditions: [
      {
        metric: '市值/自由现金流',
        category: '基本指标',
        max: 20
      }
    ]
  });

  assert.deepStrictEqual(filters, [
    {
      field: '市值',
      category: '估值',
      operator: '小于',
      value: 20
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

test('buildRequestPlanFromUnifiedInput normalizes q metrics into screener ids', () => {
  const plan = buildRequestPlanFromUnifiedInput({
    areaCode: 'cn',
    conditions: [
      {
        metric: '营业收入',
        category: '利润表',
        subCondition: 'TTM',
        dateMode: '最新财报',
        min: 10
      }
    ],
    sort: {
      metric: '营业收入',
      category: '利润表',
      subCondition: 'TTM',
      dateMode: '最新财报',
      order: 'desc'
    }
  }, catalog);

  assert.deepStrictEqual(plan.body.filterList, [
    {
      id: 'q.ps.oi.ttm',
      value: 'all',
      date: 'latest',
      min: 1000000000
    }
  ]);
  assert.strictEqual(plan.body.sortName, 'fsm.latest.q.ps.oi.ttm');
  assert.strictEqual(plan.columnSpecs[0].resultFieldKey, 'fsm.latest.q.ps.oi.ttm');
});

test('buildRequestPlanFromUnifiedInput keeps hm sorts as hm ids', () => {
  const plan = buildRequestPlanFromUnifiedInput({
    areaCode: 'cn',
    conditions: [
      {
        metric: '过去20个交易日涨跌幅',
        category: '热度指标',
        max: -10
      }
    ],
    sort: {
      metric: '过去20个交易日涨跌幅',
      category: '热度指标',
      order: 'asc'
    }
  }, catalog);

  assert.deepStrictEqual(plan.body.filterList, [
    {
      id: 'hm.vol.td_cr_20d',
      value: 'all',
      date: 'latest',
      max: -0.1
    }
  ]);
  assert.strictEqual(plan.body.sortName, 'hm.vol.td_cr_20d');
});

test('buildRequestPlanFromScreener normalizes q filter ids and result paths', () => {
  const plan = buildRequestPlanFromScreener({
    areaCode: 'cn',
    ranges: { market: 'a' },
    filterList: [
      {
        id: 'q.m.fcf.t.dynamic~lq~ttm~0',
        min: 500000000,
        date: 'latest_fs'
      }
    ],
    sortName: 'fsm.latest.q.m.fcf.ttm'
  });

  assert.deepStrictEqual(plan.body.filterList, [
    {
      id: 'q.m.fcf.ttm',
      min: 500000000,
      value: 'all',
      date: 'latest'
    }
  ]);
  assert.strictEqual(plan.columnSpecs[0].resultFieldKey, 'fsm.latest.q.m.fcf.ttm');
});

test('buildRequestPlanFromScreener normalizes q subcondition-like request ids', () => {
  const plan = buildRequestPlanFromScreener({
    areaCode: 'cn',
    filterList: [
      {
        id: 'q.ps.oi.t.dynamic~lq~ttm~0',
        min: 1000000000,
        date: 'latest_fs'
      }
    ],
    sortName: 'fsm.latest.q.ps.oi.ttm_yoy'
  });

  assert.deepStrictEqual(plan.body.filterList, [
    {
      id: 'q.ps.oi.ttm',
      value: 'all',
      date: 'latest',
      min: 1000000000
    }
  ]);
  assert.strictEqual(plan.body.sortName, 'fsm.latest.q.ps.oi.ttm_yoy');
});

test('unified-input.example.json stays on the low-valuation high-dividend strategy', () => {
  const example = JSON.parse(readFileSync(examplePath, 'utf8'));

  assert.strictEqual(example.name, '低估值高股息示例');
  assert.ok(Array.isArray(example.conditions));
  assert.strictEqual(example.conditions.length, 4);
  assert.deepStrictEqual(example.conditions[0], {
    metric: 'PE-TTM(扣非)统计值',
    selectors: ['10年', '分位点%'],
    min: 0,
    max: 30
  });
});
