import { test, describe } from 'node:test';
import assert from 'node:assert';
import {
  normalizeOperatorValueCondition,
  normalizeUnifiedInput,
  mergeUnifiedInputs,
  normalizeFilterList,
  normalizeSortName,
  lookupCatalogEntry,
  buildFormulaIdFromCondition,
  buildDisplayLabel,
  resolveUnifiedCondition,
  conditionToBrowserFilter,
  inputNeedsConditionCatalog,
  buildBrowserFiltersFromUnifiedInput,
  buildRequestPlanFromUnifiedInput,
  buildRequestPlanFromScreener
} from '../shared/unified-input.js';

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
    },
    {
      category: '基本指标',
      metric: '上市日期',
      displayLabelExample: '上市日期',
      formulaIdExample: 'pm.ipoDate.latest',
      requestIdExample: 'pm.ipoDate',
      resultFieldKey: 'ipoDate',
      selectors: [],
      dateModes: [],
      subConditionOptions: [],
      thresholds: {
        min: { inputType: 'date', unit: null },
        max: { inputType: 'date', unit: null }
      },
      notes: null,
      formulaIdTemplate: 'pm.ipoDate.latest',
      requestIdTemplate: 'pm.ipoDate',
      format: 'date',
      unit: null,
      apiScale: 1,
      specialRequestId: null
    },
    {
      category: '其他指标',
      metric: '无公式指标',
      displayLabelExample: '无公式指标',
      selectors: [],
      thresholds: {},
      notes: null
    }
  ]
};

describe('normalizeOperatorValueCondition', () => {
  test('大于操作符: operator=大于, value=10 -> min=10', () => {
    const result = normalizeOperatorValueCondition({ field: 'PE', operator: '大于', value: 10 });
    assert.strictEqual(result.min, 10);
    assert.strictEqual(result.max, undefined);
    assert.strictEqual(result.operator, '大于');
    assert.strictEqual(result.value, 10);
  });

  test('小于操作符: operator=小于, value=30 -> max=30', () => {
    const result = normalizeOperatorValueCondition({ field: 'PE', operator: '小于', value: 30 });
    assert.strictEqual(result.max, 30);
    assert.strictEqual(result.min, undefined);
    assert.strictEqual(result.operator, '小于');
    assert.strictEqual(result.value, 30);
  });

  test('介于操作符: operator=介于, value=[0, 30] -> min=0, max=30', () => {
    const result = normalizeOperatorValueCondition({ field: 'PE', operator: '介于', value: [0, 30] });
    assert.strictEqual(result.min, 0);
    assert.strictEqual(result.max, 30);
    assert.strictEqual(result.operator, '介于');
    assert.deepStrictEqual(result.value, [0, 30]);
  });

  test('介于操作符: value不是数组时抛出错误', () => {
    assert.throws(
      () => normalizeOperatorValueCondition({ field: 'PE', operator: '介于', value: 10 }),
      /requires a \[min, max\] array/
    );
  });

  test('介于操作符: value数组长度不等于2时抛出错误', () => {
    assert.throws(
      () => normalizeOperatorValueCondition({ field: 'PE', operator: '介于', value: [0] }),
      /requires a \[min, max\] array/
    );
  });

  test('不支持的操作符抛出错误', () => {
    assert.throws(
      () => normalizeOperatorValueCondition({ field: 'PE', operator: '等于', value: 10 }),
      /Unsupported operator "等于"/
    );
  });

  test('无min/max无operator: 原样返回', () => {
    const result = normalizeOperatorValueCondition({ field: 'PE', min: 0, max: 30 });
    assert.strictEqual(result.min, 0);
    assert.strictEqual(result.max, 30);
    assert.strictEqual(result.operator, undefined);
  });

  test('有min时不转换operator', () => {
    const result = normalizeOperatorValueCondition({ field: 'PE', operator: '大于', value: 10, min: 5 });
    assert.strictEqual(result.min, 5);
    assert.strictEqual(result.operator, '大于');
    assert.strictEqual(result.value, 10);
  });

  test('有max时不转换operator', () => {
    const result = normalizeOperatorValueCondition({ field: 'PE', operator: '小于', value: 30, max: 25 });
    assert.strictEqual(result.max, 25);
    assert.strictEqual(result.operator, '小于');
    assert.strictEqual(result.value, 30);
  });

  test('field自动转换为displayLabel', () => {
    const result = normalizeOperatorValueCondition({ field: 'PE-TTM', min: 0 });
    assert.strictEqual(result.displayLabel, 'PE-TTM');
    assert.strictEqual(result.field, 'PE-TTM');
  });

  test('已有displayLabel时不覆盖', () => {
    const result = normalizeOperatorValueCondition({ field: 'PE-TTM', displayLabel: 'PE-TTM(10年)', min: 0 });
    assert.strictEqual(result.displayLabel, 'PE-TTM(10年)');
  });

  test('空condition返回空对象', () => {
    const result = normalizeOperatorValueCondition({});
    assert.deepStrictEqual(result, {});
  });
});

describe('mergeUnifiedInputs', () => {
  test('合并两个空的input', () => {
    const result = mergeUnifiedInputs({}, {});
    assert.deepStrictEqual(result.conditions, []);
  });

  test('合并baseInput和空的extraInput', () => {
    const result = mergeUnifiedInputs(
      { conditions: [{ field: 'PE', min: 0 }] },
      {}
    );
    assert.strictEqual(result.conditions.length, 1);
    assert.strictEqual(result.conditions[0].field, 'PE');
  });

  test('合并空的baseInput和extraInput', () => {
    const result = mergeUnifiedInputs(
      {},
      { conditions: [{ field: 'PB', max: 3 }] }
    );
    assert.strictEqual(result.conditions.length, 1);
    assert.strictEqual(result.conditions[0].field, 'PB');
  });

  test('合并两个有conditions的input', () => {
    const result = mergeUnifiedInputs(
      { conditions: [{ field: 'PE', min: 0 }], areaCode: 'cn' },
      { conditions: [{ field: 'PB', max: 3 }], sortName: 'pe' }
    );
    assert.strictEqual(result.conditions.length, 2);
    assert.strictEqual(result.conditions[0].field, 'PE');
    assert.strictEqual(result.conditions[1].field, 'PB');
    assert.strictEqual(result.areaCode, 'cn');
    assert.strictEqual(result.sortName, 'pe');
  });

  test('extraInput覆盖baseInput的同名属性', () => {
    const result = mergeUnifiedInputs(
      { areaCode: 'cn', pageSize: 50 },
      { areaCode: 'us', pageIndex: 1 }
    );
    assert.strictEqual(result.areaCode, 'us');
    assert.strictEqual(result.pageSize, 50);
    assert.strictEqual(result.pageIndex, 1);
  });

  test('conditions为undefined时正常处理', () => {
    const result = mergeUnifiedInputs(
      { conditions: undefined },
      { conditions: undefined }
    );
    assert.deepStrictEqual(result.conditions, []);
  });

  test('自动normalize conditions', () => {
    const result = mergeUnifiedInputs(
      { conditions: [{ field: 'PE', operator: '大于', value: 10 }] },
      {}
    );
    assert.strictEqual(result.conditions[0].min, 10);
    assert.strictEqual(result.conditions[0].displayLabel, 'PE');
  });
});

describe('normalizeFilterList', () => {
  test('空数组返回空数组', () => {
    const result = normalizeFilterList([]);
    assert.deepStrictEqual(result, []);
  });

  test('undefined返回空数组', () => {
    const result = normalizeFilterList(undefined);
    assert.deepStrictEqual(result, []);
  });

  test('null返回空数组', () => {
    const result = normalizeFilterList(null);
    assert.deepStrictEqual(result, []);
  });

  test('移除.latest后缀', () => {
    const result = normalizeFilterList([{ id: 'pm.pe_ttm.y1.cvpos.latest', min: 0 }]);
    assert.strictEqual(result[0].id, 'pm.pe_ttm.y1.cvpos');
  });

  test('规范化q指标id', () => {
    const result = normalizeFilterList([
      { id: 'q.ps.oi.t.dynamic~lq~ttm~0', min: 100 }
    ]);
    assert.strictEqual(result[0].id, 'q.ps.oi.ttm');
  });

  test('添加默认value=all', () => {
    const result = normalizeFilterList([{ id: 'pm.pe_ttm.y1.cvpos', min: 0 }]);
    assert.strictEqual(result[0].value, 'all');
  });

  test('保留已有value', () => {
    const result = normalizeFilterList([{ id: 'pm.pe_ttm.y1.cvpos', value: 'custom' }]);
    assert.strictEqual(result[0].value, 'custom');
  });

  test('规范化date字段: latest_fs -> latest', () => {
    const result = normalizeFilterList([
      { id: 'q.ps.oi.t.dynamic~lq~y~0', date: 'latest_fs' }
    ]);
    assert.strictEqual(result[0].date, 'latest');
  });

  test('规范化date字段: latest_time -> latest', () => {
    const result = normalizeFilterList([
      { id: 'hm.vol.td_cr_20d', date: 'latest_time' }
    ]);
    assert.strictEqual(result[0].date, 'latest');
  });

  test('Date结尾的id不自动添加date字段', () => {
    const result = normalizeFilterList([
      { id: 'pm.ipoDate' }
    ]);
    assert.strictEqual(result[0].date, undefined);
  });

  test('Date结尾的id已有date字段时保留原值', () => {
    const result = normalizeFilterList([
      { id: 'pm.ipoDate', date: '2024' }
    ]);
    assert.strictEqual(result[0].date, '2024');
  });

  test('pm前缀自动添加date=latest', () => {
    const result = normalizeFilterList([{ id: 'pm.pe_ttm.y1.cvpos' }]);
    assert.strictEqual(result[0].date, 'latest');
  });

  test('hm前缀自动添加date=latest', () => {
    const result = normalizeFilterList([{ id: 'hm.vol.td_cr_20d' }]);
    assert.strictEqual(result[0].date, 'latest');
  });

  test('q前缀自动添加date=latest', () => {
    const result = normalizeFilterList([{ id: 'q.ps.oi.ttm' }]);
    assert.strictEqual(result[0].date, 'latest');
  });

  test('保留min/max等属性', () => {
    const result = normalizeFilterList([
      { id: 'pm.pe_ttm.y1.cvpos', min: 0, max: 30 }
    ]);
    assert.strictEqual(result[0].min, 0);
    assert.strictEqual(result[0].max, 30);
  });
});

describe('normalizeSortName', () => {
  test('空值返回默认值', () => {
    const result = normalizeSortName(null);
    assert.strictEqual(result, 'pm.latest.d_pe_ttm.y10.cvpos');
  });

  test('undefined返回默认值', () => {
    const result = normalizeSortName(undefined);
    assert.strictEqual(result, 'pm.latest.d_pe_ttm.y10.cvpos');
  });

  test('空字符串返回默认值', () => {
    const result = normalizeSortName('');
    assert.strictEqual(result, 'pm.latest.d_pe_ttm.y10.cvpos');
  });

  test('转换priceMetrics.latest.pm前缀', () => {
    const result = normalizeSortName('priceMetrics.latest.pm.pe_ttm.y1.cvpos');
    assert.strictEqual(result, 'pm.latest.pe_ttm.y1.cvpos');
  });

  test('转换priceMetrics.latest前缀', () => {
    const result = normalizeSortName('priceMetrics.latest.hm.vol.td_cr_20d');
    assert.strictEqual(result, 'hm.vol.td_cr_20d');
  });

  test('保持其他格式不变', () => {
    const result = normalizeSortName('fsm.latest.q.ps.oi.ttm');
    assert.strictEqual(result, 'fsm.latest.q.ps.oi.ttm');
  });
});

describe('lookupCatalogEntry', () => {
  test('通过metric查找', () => {
    const result = lookupCatalogEntry(catalog, { metric: 'PE-TTM统计值' });
    assert.strictEqual(result.metric, 'PE-TTM统计值');
  });

  test('通过metric和category查找', () => {
    const result = lookupCatalogEntry(catalog, { metric: 'PE-TTM统计值', category: '基本指标' });
    assert.strictEqual(result.metric, 'PE-TTM统计值');
    assert.strictEqual(result.category, '基本指标');
  });

  test('category过滤无匹配时返回null', () => {
    const result = lookupCatalogEntry(catalog, { metric: 'PE-TTM统计值', category: '不存在' });
    assert.strictEqual(result, null);
  });

  test('通过displayLabel查找', () => {
    const result = lookupCatalogEntry(catalog, { displayLabel: '营业收入' });
    assert.strictEqual(result.metric, '营业收入');
  });

  test('通过formulaId查找', () => {
    const result = lookupCatalogEntry(catalog, { formulaId: 'pm.pe_ttm.y1.cvpos.latest' });
    assert.strictEqual(result.metric, 'PE-TTM统计值');
  });

  test('通过formulaId(无.latest后缀)查找', () => {
    const result = lookupCatalogEntry(catalog, { formulaId: 'pm.pe_ttm.y1.cvpos' });
    assert.strictEqual(result.metric, 'PE-TTM统计值');
  });

  test('通过requestIdExample查找', () => {
    const result = lookupCatalogEntry(catalog, { formulaId: 'pm.pe_ttm.y1.cvpos' });
    assert.strictEqual(result.metric, 'PE-TTM统计值');
  });

  test('空catalog返回null', () => {
    const result = lookupCatalogEntry({ metrics: [] }, { metric: 'PE-TTM统计值' });
    assert.strictEqual(result, null);
  });

  test('无metrics属性的catalog返回null', () => {
    const result = lookupCatalogEntry({}, { metric: 'PE-TTM统计值' });
    assert.strictEqual(result, null);
  });

  test('数组格式catalog', () => {
    const arrayCatalog = catalog.metrics;
    const result = lookupCatalogEntry(arrayCatalog, { metric: 'PE-TTM统计值' });
    assert.strictEqual(result.metric, 'PE-TTM统计值');
  });

  test('无匹配条件返回null', () => {
    const result = lookupCatalogEntry(catalog, {});
    assert.strictEqual(result, null);
  });

  test('metric优先匹配基本指标类别', () => {
    const multiCategoryCatalog = {
      metrics: [
        { metric: 'ROE', category: '估值', displayLabelExample: 'ROE' },
        { metric: 'ROE', category: '基本指标', displayLabelExample: 'ROE' }
      ]
    };
    const result = lookupCatalogEntry(multiCategoryCatalog, { metric: 'ROE' });
    assert.strictEqual(result.category, '基本指标');
  });

  test('metric无基本指标类别时返回第一个匹配', () => {
    const singleCategoryCatalog = {
      metrics: [
        { metric: 'ROE', category: '估值', displayLabelExample: 'ROE' }
      ]
    };
    const result = lookupCatalogEntry(singleCategoryCatalog, { metric: 'ROE' });
    assert.strictEqual(result.category, '估值');
  });
});

describe('buildFormulaIdFromCondition', () => {
  test('condition已有formulaId直接返回', () => {
    const entry = catalog.metrics[0];
    const result = buildFormulaIdFromCondition(entry, { formulaId: 'custom.id' });
    assert.strictEqual(result, 'custom.id');
  });

  test('使用formulaIdTemplate生成', () => {
    const entry = catalog.metrics[0];
    const result = buildFormulaIdFromCondition(entry, { selectors: ['10年', '分位点%'] });
    assert.strictEqual(result, 'pm.pe_ttm.y10.cvpos.latest');
  });

  test('使用默认selector值', () => {
    const entry = catalog.metrics[0];
    const result = buildFormulaIdFromCondition(entry, {});
    assert.strictEqual(result, 'pm.pe_ttm.y1.cvpos.latest');
  });

  test('部分selector使用默认值', () => {
    const entry = catalog.metrics[0];
    const result = buildFormulaIdFromCondition(entry, { selectors: ['10年'] });
    assert.strictEqual(result, 'pm.pe_ttm.y10.cvpos.latest');
  });

  test('无formulaIdTemplate和formulaIdExample时返回null', () => {
    const entry = catalog.metrics[4];
    const result = buildFormulaIdFromCondition(entry, {});
    assert.strictEqual(result, null);
  });

  test('entry为null时返回null', () => {
    const result = buildFormulaIdFromCondition(null, {});
    assert.strictEqual(result, null);
  });

  test('entry为undefined时返回null', () => {
    const result = buildFormulaIdFromCondition(undefined, {});
    assert.strictEqual(result, null);
  });

  test('无效selector label抛出错误', () => {
    const entry = catalog.metrics[0];
    assert.throws(
      () => buildFormulaIdFromCondition(entry, { selectors: ['无效'] }),
      /Unknown selector label "无效"/
    );
  });

  test('使用formulaIdExample作为后备', () => {
    const entry = catalog.metrics[1];
    const result = buildFormulaIdFromCondition(entry, {});
    assert.strictEqual(result, 'q.ps.oi.t.dynamic~lq~y~0');
  });
});

describe('buildDisplayLabel', () => {
  test('condition已有displayLabel直接返回', () => {
    const entry = catalog.metrics[0];
    const result = buildDisplayLabel(entry, { displayLabel: '自定义标签' });
    assert.strictEqual(result, '自定义标签');
  });

  test('使用displayLabelExample', () => {
    const entry = catalog.metrics[0];
    const result = buildDisplayLabel(entry, {});
    assert.strictEqual(result, 'PE-TTM统计值(1年)·分位点%');
  });

  test('使用selectors替换默认label', () => {
    const entry = catalog.metrics[0];
    const result = buildDisplayLabel(entry, { selectors: ['10年', '分位点%'] });
    assert.strictEqual(result, 'PE-TTM统计值(10年)·分位点%');
  });

  test('无效selector label抛出错误', () => {
    const entry = catalog.metrics[0];
    assert.throws(
      () => buildDisplayLabel(entry, { selectors: ['无效'] }),
      /Unknown selector label "无效"/
    );
  });

  test('无displayLabelExample时使用metric', () => {
    const entry = { metric: 'ROE', selectors: [] };
    const result = buildDisplayLabel(entry, {});
    assert.strictEqual(result, 'ROE');
  });

  test('无displayLabelExample和metric时使用displayName', () => {
    const entry = { displayName: 'ROE指标', selectors: [] };
    const result = buildDisplayLabel(entry, {});
    assert.strictEqual(result, 'ROE指标');
  });
});

describe('resolveUnifiedCondition', () => {
  test('特殊指标别名: 上市日期', () => {
    const result = resolveUnifiedCondition(null, { metric: '上市日期', min: '2020-01-01' });
    assert.strictEqual(result.filter.id, 'pm.ipoDate');
    assert.strictEqual(result.filter.value, 'all');
    assert.strictEqual(result.filter.min, '2020-01-01');
    assert.strictEqual(result.columnSpec.format, 'date');
    assert.strictEqual(result.columnSpec.resultFieldKey, 'ipoDate');
  });

  test('特殊指标别名: 上市日期不支持subCondition时抛出错误', () => {
    assert.throws(
      () => resolveUnifiedCondition(null, { metric: '上市日期', subCondition: '不支持' }),
      /currently supports only/
    );
  });

  test('特殊指标别名: 上市日期支持的subCondition', () => {
    const result = resolveUnifiedCondition(null, { metric: '上市日期', subCondition: '上市时间', min: '2020-01-01' });
    assert.strictEqual(result.filter.id, 'pm.ipoDate');
  });

  

  test('无entry且不是特殊别名时抛出错误', () => {
    assert.throws(
      () => resolveUnifiedCondition(null, { metric: '未知指标', min: 0 }),
      /Unable to resolve condition/
    );
  });

  test('metric无formulaId时抛出错误', () => {
    const entryWithoutFormula = {
      metric: '无公式',
      displayLabelExample: '无公式',
      selectors: [],
      thresholds: {}
    };
    assert.throws(
      () => resolveUnifiedCondition(entryWithoutFormula, { metric: '无公式', min: 0 }),
      /does not expose a formula ID/
    );
  });

  test('正确处理百分比单位', () => {
    const entry = catalog.metrics[0];
    const result = resolveUnifiedCondition(entry, { metric: 'PE-TTM统计值', selectors: ['1年', '分位点%'], min: 10, max: 30 });
    assert.strictEqual(result.filter.min, 0.1);
    assert.strictEqual(result.filter.max, 0.3);
    assert.strictEqual(result.columnSpec.unit, '%');
  });

  test('正确处理亿单位', () => {
    const entry = catalog.metrics[1];
    const result = resolveUnifiedCondition(entry, { metric: '营业收入', subCondition: 'TTM', min: 10 });
    assert.strictEqual(result.filter.min, 1000000000);
    assert.strictEqual(result.columnSpec.unit, '亿');
  });

  test('正确处理日期格式', () => {
    const entry = catalog.metrics[3];
    const result = resolveUnifiedCondition(entry, { metric: '上市日期', min: '2020-01-01', max: '2024-01-01' });
    assert.strictEqual(result.filter.min, '2020-01-01');
    assert.strictEqual(result.filter.max, '2024-01-01');
    assert.strictEqual(result.columnSpec.format, 'date');
  });

  test('处理dateMode', () => {
    const entry = catalog.metrics[1];
    const result = resolveUnifiedCondition(entry, { metric: '营业收入', dateMode: '最新财报', min: 10 });
    assert.strictEqual(result.filter.date, 'latest');
  });

  test('处理dateModeApi', () => {
    const entry = catalog.metrics[1];
    const result = resolveUnifiedCondition(entry, { metric: '营业收入', dateModeApi: 'latest_fs', min: 10 });
    assert.strictEqual(result.filter.date, 'latest');
  });

  test('处理无效dateMode抛出错误', () => {
    const entry = catalog.metrics[1];
    assert.throws(
      () => resolveUnifiedCondition(entry, { metric: '营业收入', dateMode: '无效' }),
      /Unknown date mode/
    );
  });

  test('处理无效subCondition抛出错误', () => {
    const entry = catalog.metrics[1];
    assert.throws(
      () => resolveUnifiedCondition(entry, { metric: '营业收入', subCondition: '无效' }),
      /Unknown subCondition/
    );
  });

  test('处理有效的subCondition', () => {
    const entry = catalog.metrics[1];
    const result = resolveUnifiedCondition(entry, { metric: '营业收入', subCondition: 'TTM', min: 10 });
    assert.strictEqual(result.filter.id, 'q.ps.oi.ttm');
  });
});

describe('conditionToBrowserFilter', () => {
  test('介于条件', () => {
    const result = conditionToBrowserFilter({ field: 'PE', min: 0, max: 30 });
    assert.strictEqual(result.operator, '介于');
    assert.deepStrictEqual(result.value, [0, 30]);
  });

  test('大于条件', () => {
    const result = conditionToBrowserFilter({ field: 'PE', min: 10 });
    assert.strictEqual(result.operator, '大于');
    assert.strictEqual(result.value, 10);
  });

  test('小于条件', () => {
    const result = conditionToBrowserFilter({ field: 'PE', max: 30 });
    assert.strictEqual(result.operator, '小于');
    assert.strictEqual(result.value, 30);
  });

  test('无min/max抛出错误', () => {
    assert.throws(
      () => conditionToBrowserFilter({ field: 'PE' }),
      /is missing min\/max or operator\/value/
    );
  });

  test('使用catalog查找entry', () => {
    const result = conditionToBrowserFilter({ metric: 'PE-TTM统计值', selectors: ['10年', '分位点%'], min: 0, max: 30 }, catalog);
    assert.strictEqual(result.field, 'PE-TTM统计值(10年)·分位点%');
    assert.strictEqual(result.category, '基本指标');
  });

  test('特殊指标别名: 市值/自由现金流', () => {
    const result = conditionToBrowserFilter({ metric: '市值/自由现金流', max: 20 });
    assert.strictEqual(result.field, '市值');
    assert.strictEqual(result.category, '估值');
  });

  test('无displayLabel且无catalog时使用browser catalog', () => {
    const result = conditionToBrowserFilter({ metric: '市值/自由现金流', max: 20 });
    assert.strictEqual(result.field, '市值');
    assert.strictEqual(result.category, '估值');
  });

  test('已有displayLabel时使用', () => {
    const result = conditionToBrowserFilter({ displayLabel: 'PE-TTM', min: 0, max: 30 });
    assert.strictEqual(result.field, 'PE-TTM');
  });

  test('field作为displayLabel', () => {
    const result = conditionToBrowserFilter({ field: 'PE-TTM', min: 0 });
    assert.strictEqual(result.field, 'PE-TTM');
  });

  test('处理dateMode', () => {
    const result = conditionToBrowserFilter({ metric: '营业收入', dateMode: '最新财报', min: 10 }, catalog);
    assert.strictEqual(result.dateModeLabel, '最新财报');
    assert.strictEqual(result.dateModeApi, 'latest_fs');
  });

  test('处理dateModeApi', () => {
    const result = conditionToBrowserFilter({ metric: '营业收入', dateModeApi: 'latest_fs', min: 10 }, catalog);
    assert.strictEqual(result.dateModeLabel, '最新财报');
    assert.strictEqual(result.dateModeApi, 'latest_fs');
  });

  test('处理subCondition', () => {
    const result = conditionToBrowserFilter({ metric: '营业收入', subCondition: 'TTM', min: 10 }, catalog);
    assert.strictEqual(result.subCondition, 'TTM');
  });
});

describe('inputNeedsConditionCatalog', () => {
  test('有metric时返回true', () => {
    assert.strictEqual(inputNeedsConditionCatalog({ conditions: [{ metric: 'PE' }] }), true);
  });

  test('有category时返回true', () => {
    assert.strictEqual(inputNeedsConditionCatalog({ conditions: [{ category: '估值' }] }), true);
  });

  test('有formulaId时返回true', () => {
    assert.strictEqual(inputNeedsConditionCatalog({ conditions: [{ formulaId: 'pm.pe' }] }), true);
  });

  test('有selectors时返回true', () => {
    assert.strictEqual(inputNeedsConditionCatalog({ conditions: [{ selectors: ['10年'] }] }), true);
  });

  test('有subCondition时返回true', () => {
    assert.strictEqual(inputNeedsConditionCatalog({ conditions: [{ subCondition: 'TTM' }] }), true);
  });

  test('只有field/min/max时返回false', () => {
    assert.strictEqual(inputNeedsConditionCatalog({ conditions: [{ field: 'PE', min: 0, max: 30 }] }), false);
  });

  test('空conditions返回false', () => {
    assert.strictEqual(inputNeedsConditionCatalog({ conditions: [] }), false);
  });

  test('无conditions返回false', () => {
    assert.strictEqual(inputNeedsConditionCatalog({}), false);
  });

  test('使用filters别名', () => {
    assert.strictEqual(inputNeedsConditionCatalog({ filters: [{ metric: 'PE' }] }), true);
  });

  test('多个条件有一个需要catalog就返回true', () => {
    assert.strictEqual(
      inputNeedsConditionCatalog({
        conditions: [
          { field: 'PE', min: 0 },
          { metric: 'ROE' }
        ]
      }),
      true
    );
  });
});

describe('边界情况和错误处理', () => {
  test('normalizeOperatorValueCondition: null input', () => {
    const result = normalizeOperatorValueCondition(null);
    assert.deepStrictEqual(result, {});
  });

  test('normalizeUnifiedInput: undefined input', () => {
    const result = normalizeUnifiedInput(undefined);
    assert.deepStrictEqual(result.conditions, []);
  });

  test('normalizeUnifiedInput: null input', () => {
    const result = normalizeUnifiedInput(null);
    assert.deepStrictEqual(result.conditions, []);
  });

  

  test('mergeUnifiedInputs: undefined inputs', () => {
    const result = mergeUnifiedInputs(undefined, undefined);
    assert.deepStrictEqual(result.conditions, []);
  });

  test('buildRequestPlanFromUnifiedInput: 空conditions', () => {
    const result = buildRequestPlanFromUnifiedInput({}, catalog);
    assert.deepStrictEqual(result.body.filterList, []);
    assert.deepStrictEqual(result.columnSpecs, []);
  });

  test('buildRequestPlanFromUnifiedInput: 默认值', () => {
    const result = buildRequestPlanFromUnifiedInput({}, catalog);
    assert.strictEqual(result.body.areaCode, 'cn');
    assert.strictEqual(result.body.pageSize, 100);
    assert.strictEqual(result.body.pageIndex, 0);
    assert.strictEqual(result.body.sortOrder, 'desc');
    assert.strictEqual(result.body.industrySource, 'sw_2021');
    assert.strictEqual(result.body.industryLevel, 'three');
  });

  test('buildRequestPlanFromUnifiedInput: 自定义值覆盖默认值', () => {
    const result = buildRequestPlanFromUnifiedInput(
      { areaCode: 'us', pageSize: 50, pageIndex: 1, sortOrder: 'asc' },
      catalog
    );
    assert.strictEqual(result.body.areaCode, 'us');
    assert.strictEqual(result.body.pageSize, 50);
    assert.strictEqual(result.body.pageIndex, 1);
    assert.strictEqual(result.body.sortOrder, 'asc');
  });

  test('buildRequestPlanFromScreener: 默认值', () => {
    const result = buildRequestPlanFromScreener({});
    assert.strictEqual(result.body.areaCode, 'cn');
    assert.strictEqual(result.body.pageSize, 100);
    assert.strictEqual(result.body.pageIndex, 0);
    assert.strictEqual(result.body.sortOrder, 'desc');
    assert.strictEqual(result.body.sortName, 'pm.latest.d_pe_ttm.y10.cvpos');
  });

  test('buildRequestPlanFromScreener: 自定义值', () => {
    const result = buildRequestPlanFromScreener({
      areaCode: 'hk',
      pageSize: 200,
      pageIndex: 2,
      sortOrder: 'asc',
      sortName: 'pm.pe_ttm.y1'
    });
    assert.strictEqual(result.body.areaCode, 'hk');
    assert.strictEqual(result.body.pageSize, 200);
    assert.strictEqual(result.body.pageIndex, 2);
    assert.strictEqual(result.body.sortOrder, 'asc');
    assert.strictEqual(result.body.sortName, 'pm.pe_ttm.y1');
  });

  test('buildBrowserFiltersFromUnifiedInput: 空conditions', () => {
    const result = buildBrowserFiltersFromUnifiedInput({});
    assert.deepStrictEqual(result, []);
  });

  test('normalizeFilterList: 保留其他属性', () => {
    const result = normalizeFilterList([{ id: 'pm.test', customProp: 'value' }]);
    assert.strictEqual(result[0].customProp, 'value');
  });

  test('conditionToBrowserFilter: 有category时保留', () => {
    const result = conditionToBrowserFilter({ field: 'PE', category: '估值', min: 0 });
    assert.strictEqual(result.category, '估值');
  });

  test('lookupCatalogEntry: 通过specialRequestId查找', () => {
    const specialCatalog = {
      metrics: [{
        metric: '特殊指标',
        displayLabelExample: '特殊指标',
        specialRequestId: 'special.id'
      }]
    };
    const result = lookupCatalogEntry(specialCatalog, { formulaId: 'special.id' });
    assert.strictEqual(result.metric, '特殊指标');
  });

  test('resolveUnifiedCondition: 使用condition中的formulaId', () => {
    const result = resolveUnifiedCondition(null, {
      metric: '上市日期',
      formulaId: 'custom.formula.id',
      min: '2020-01-01'
    });
    assert.strictEqual(result.columnSpec.requestId, 'pm.ipoDate');
  });

  test('buildFormulaIdFromCondition: 空selectors数组', () => {
    const entry = catalog.metrics[0];
    const result = buildFormulaIdFromCondition(entry, { selectors: [] });
    assert.strictEqual(result, 'pm.pe_ttm.y1.cvpos.latest');
  });

  test('normalizeFilterList: 处理多个filter', () => {
    const result = normalizeFilterList([
      { id: 'pm.pe_ttm.y1.cvpos.latest', min: 0 },
      { id: 'q.ps.oi.t.dynamic~lq~ttm~0', min: 100 }
    ]);
    assert.strictEqual(result.length, 2);
    assert.strictEqual(result[0].id, 'pm.pe_ttm.y1.cvpos');
    assert.strictEqual(result[1].id, 'q.ps.oi.ttm');
  });
});