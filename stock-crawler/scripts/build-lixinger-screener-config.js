import fs from 'fs';
import path from 'path';

const DEFAULT_OUTPUT_DIR = path.resolve(process.cwd(), 'output/playwright/lixinger-screener');
const DEFAULT_CATALOG_PATH = path.join(DEFAULT_OUTPUT_DIR, 'condition-catalog.cn.json');
const DEFAULT_TEMPLATE_PATH = path.join(DEFAULT_OUTPUT_DIR, 'simple-input-template.cn.json');
const DEFAULT_OUTPUT_PATH = path.join(DEFAULT_OUTPUT_DIR, 'condition-config.cn.json');

function loadJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, 'utf8'));
}

function saveJson(filePath, data) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  fs.writeFileSync(filePath, JSON.stringify(data, null, 2));
}

function simplifySelectionRange(range) {
  const simplified = {
    key: range.key,
    label: range.label,
    type: range.type
  };

  if (range.options?.length) {
    simplified.options = range.options.map(option => ({
      label: option.label,
      value: option.value
    }));
  }

  if (range.source) {
    simplified.source = range.source;
  }

  if (range.note) {
    simplified.note = range.note;
  }

  return simplified;
}

function simplifyMetric(metric) {
  return {
    metric: metric.metric,
    displayLabelExample: metric.displayLabelExample,
    formulaIdTemplate: metric.formulaIdTemplate,
    requestIdTemplate: metric.requestIdTemplate,
    resultFieldKey: metric.resultFieldKey,
    selectors: (metric.selectors || []).map(selector => ({
      name: selector.name,
      defaultLabel: selector.defaultLabel,
      options: selector.options.map(option => option.label)
    })),
    dateModes: (metric.dateModes || []).map(mode => ({
      label: mode.label,
      value: mode.value
    })),
    subConditionOptions: metric.subConditionOptions || [],
    input: {
      format: metric.format,
      unit: metric.unit,
      minType: metric.thresholds?.min?.inputType || null,
      maxType: metric.thresholds?.max?.inputType || null,
      apiScale: metric.apiScale
    },
    notes: metric.notes || undefined
  };
}

function buildMetricCategories(metrics) {
  const categories = {};
  for (const metric of metrics) {
    if (!categories[metric.category]) {
      categories[metric.category] = [];
    }
    categories[metric.category].push(simplifyMetric(metric));
  }
  return categories;
}

function buildSimpleInputSchema() {
  return {
    name: '自定义筛选名称',
    areaCode: 'cn',
    pageSize: 100,
    sort: {
      metric: '指标名',
      category: '可选，遇到重名指标时建议填写',
      selectors: ['可选选择器1', '可选选择器2'],
      order: 'desc'
    },
    ranges: {
      market: 'a',
      stockBourseTypes: [],
      mutualMarkets: {
        selectedMutualMarkets: [],
        selectType: 'include'
      },
      multiMarketListedType: {
        selectedMultiMarketListedTypes: [],
        selectType: 'include'
      },
      excludeBlacklist: false,
      excludeDelisted: false,
      excludeSpecialTreatment: false,
      specialTreatmentOnly: false
    },
    conditions: [
      {
        metric: 'PE-TTM(扣非)统计值',
        category: '基本指标',
        selectors: ['10年', '分位点%'],
        min: 0,
        max: 30
      },
      {
        metric: '上市日期',
        category: '基本指标',
        subCondition: '上市时间',
        max: '2015-01-01'
      }
    ]
  };
}

function main() {
  const catalog = loadJson(DEFAULT_CATALOG_PATH);
  const template = loadJson(DEFAULT_TEMPLATE_PATH);

  const output = {
    generatedAt: new Date().toISOString(),
    basedOnCatalogGeneratedAt: catalog.generatedAt,
    sourceUrl: catalog.sourceUrl,
    areaCode: catalog.areaCode,
    notes: [
      '这个文件是给人手工填写或程序生成 simple-input 用的，更偏规则化和可读性。',
      '百分比沿用页面输入习惯，例如 30 表示 30%，脚本会自动转换为 0.3。',
      '市值沿用“亿”作为输入单位，例如 100 表示 100 亿。',
      '遇到同名指标时，建议同时填写 category 以避免歧义。'
    ],
    simpleInputSchema: buildSimpleInputSchema(),
    simpleInputExample: template,
    selectionRanges: (catalog.selectionRanges || []).map(simplifySelectionRange),
    metricCategories: buildMetricCategories(catalog.metrics || [])
  };

  saveJson(DEFAULT_OUTPUT_PATH, output);

  process.stdout.write(`${JSON.stringify({
    outputPath: DEFAULT_OUTPUT_PATH,
    categoryCount: Object.keys(output.metricCategories).length,
    metricCount: catalog.metrics.length
  }, null, 2)}\n`);
}

main();
