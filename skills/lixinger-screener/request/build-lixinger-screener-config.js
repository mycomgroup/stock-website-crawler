import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import '../load-env.js';
import { LIXINGER_OUTPUT_DIR } from '../paths.js';

const REQUEST_DIR = path.dirname(fileURLToPath(import.meta.url));
const DEFAULT_OUTPUT_DIR = LIXINGER_OUTPUT_DIR;
const DEFAULT_CATALOG_PATH = path.join(DEFAULT_OUTPUT_DIR, 'condition-catalog.cn.json');
const DEFAULT_TEMPLATE_PATH = path.join(DEFAULT_OUTPUT_DIR, 'simple-input-template.cn.json');
const DEFAULT_CONDITION_CONFIG_PATH = path.join(DEFAULT_OUTPUT_DIR, 'condition-config.cn.json');
const DEFAULT_PROFILE_DIR = path.join(REQUEST_DIR, 'profiles');

const PAGE_PROFILE_PRESETS = {
  'company-cn': {
    name: 'company-fundamental-cn',
    pageType: 'company-fundamental',
    screenerKey: 'company-cn',
    apiType: 'company',
    areaCode: 'cn',
    defaultUrl: 'https://www.lixinger.com/analytics/screener/company-fundamental/cn',
    ranges: {
      market: 'a',
      stockBourseTypes: [],
      mutualMarkets: { selectedMutualMarkets: [], selectType: 'include' },
      multiMarketListedType: { selectedMultiMarketListedTypes: [], selectType: 'include' },
      excludeBlacklist: false,
      excludeDelisted: false,
      excludeBourseType: false,
      excludeSpecialTreatment: false,
      constituentsPerspectiveType: 'history',
      specialTreatmentOnly: false
    },
    industrySource: 'sw_2021',
    industryLevel: 'three',
    sortName: 'pm.latest.d_pe_ttm.y10.cvpos',
    sortOrder: 'desc',
    pageSize: 100
  },
  'company-hk': {
    name: 'company-fundamental-hk',
    pageType: 'company-fundamental',
    screenerKey: 'company-hk',
    apiType: 'company',
    areaCode: 'hk',
    defaultUrl: 'https://www.lixinger.com/analytics/screener/company-fundamental/hk',
    ranges: {
      stockBourseTypes: [],
      mutualMarkets: { selectedMutualMarkets: [], selectType: 'include' },
      multiMarketListedType: { selectedMultiMarketListedTypes: [], selectType: 'include' },
      excludeBlacklist: false,
      excludeDelisted: false,
      excludeBourseType: false,
      constituentsPerspectiveType: 'history'
    },
    industrySource: 'hsi',
    industryLevel: 'three',
    sortName: 'pm.latest.pe_ttm',
    sortOrder: 'desc',
    pageSize: 100
  },
  'company-us': {
    name: 'company-fundamental-us',
    pageType: 'company-fundamental',
    screenerKey: 'company-us',
    apiType: 'company',
    areaCode: 'us',
    defaultUrl: 'https://www.lixinger.com/analytics/screener/company-fundamental/us',
    ranges: {
      excludeBlacklist: false,
      excludeDelisted: false,
      constituentsPerspectiveType: 'history'
    },
    industrySource: null,
    industryLevel: null,
    sortName: 'pm.latest.pe_ttm',
    sortOrder: 'desc',
    pageSize: 100
  },
  'fund-cn': {
    name: 'fund-fundamental-cn',
    pageType: 'fund-fundamental',
    screenerKey: 'fund-cn',
    apiType: 'fund',
    areaCode: 'cn',
    defaultUrl: 'https://www.lixinger.com/analytics/screener/fund-fundamental/cn',
    ranges: {
      excludeDelisted: true,
      excludeAbnormalNav: false
    },
    sortName: 'pm.latest.hm.vol.td_cr_20d',
    sortOrder: 'desc',
    pageSize: 100
  },
  'index-cn': {
    name: 'index-fundamental-cn',
    pageType: 'index-fundamental',
    screenerKey: 'index-cn',
    apiType: 'ii',
    stockType: 'index',
    areaCode: 'cn',
    defaultUrl: 'https://www.lixinger.com/analytics/screener/index-fundamental/cn',
    ranges: {
      source: 'all',
      series: 'all',
      calculationMethod: 'all',
      keyword: ''
    },
    sortName: 'hm.o.followedNum',
    sortOrder: 'desc',
    pageSize: 100
  },
  'index-hk': {
    name: 'index-fundamental-hk',
    pageType: 'index-fundamental',
    screenerKey: 'index-hk',
    apiType: 'ii',
    stockType: 'index',
    areaCode: 'hk',
    defaultUrl: 'https://www.lixinger.com/analytics/screener/index-fundamental/hk',
    ranges: {
      source: 'all',
      keyword: ''
    },
    sortName: 'hm.o.followedNum',
    sortOrder: 'desc',
    pageSize: 100
  }
};

function loadJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, 'utf8'));
}

function saveJson(filePath, data) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  fs.writeFileSync(filePath, JSON.stringify(data, null, 2));
}

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (!arg.startsWith('--')) continue;
    const key = arg.slice(2);
    const next = argv[i + 1];
    if (!next || next.startsWith('--')) {
      args[key] = true;
      continue;
    }
    args[key] = next;
    i += 1;
  }
  return args;
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

  if (range.source) simplified.source = range.source;
  if (range.note) simplified.note = range.note;
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
    if (!categories[metric.category]) categories[metric.category] = [];
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

function inferProfileKeyFromUrl(url) {
  if (!url) return null;
  const value = String(url).toLowerCase();
  if (value.includes('/company-fundamental/cn')) return 'company-cn';
  if (value.includes('/company-fundamental/hk')) return 'company-hk';
  if (value.includes('/company-fundamental/us')) return 'company-us';
  if (value.includes('/fund-fundamental/cn')) return 'fund-cn';
  if (value.includes('/index-fundamental/cn')) return 'index-cn';
  if (value.includes('/index-fundamental/hk')) return 'index-hk';
  return null;
}

function buildProfileOutput(profileKey) {
  const preset = PAGE_PROFILE_PRESETS[profileKey];
  if (!preset) {
    throw new Error(`Unknown profile key: ${profileKey}`);
  }
  return {
    ...preset,
    generatedAt: new Date().toISOString()
  };
}

function writeOneProfile(profileKey, outputFile) {
  const profile = buildProfileOutput(profileKey);
  saveJson(outputFile, profile);
  return { profileKey, outputFile };
}

function writeAllProfiles(outputDir) {
  fs.mkdirSync(outputDir, { recursive: true });
  const result = [];
  for (const profileKey of Object.keys(PAGE_PROFILE_PRESETS)) {
    const fileName = `${PAGE_PROFILE_PRESETS[profileKey].name}.profile.json`;
    const outputFile = path.join(outputDir, fileName);
    result.push(writeOneProfile(profileKey, outputFile));
  }
  return result;
}

function buildConditionConfig(catalogPath, templatePath, outputPath) {
  const catalog = loadJson(catalogPath);
  const template = loadJson(templatePath);
  const dynamicOptionsIndexPath = path.join(path.dirname(catalogPath), 'dynamic-options-index.cn.json');
  const dynamicOptionsIndex = fs.existsSync(dynamicOptionsIndexPath) ? loadJson(dynamicOptionsIndexPath) : null;

  const output = {
    generatedAt: new Date().toISOString(),
    basedOnCatalogGeneratedAt: catalog.generatedAt,
    sourceUrl: catalog.sourceUrl,
    areaCode: catalog.areaCode,
    notes: [
      '这个文件是给人手工填写或程序生成 simple-input 用的，更偏规则化和可读性。',
      '百分比沿用页面输入习惯，例如 30 表示 30%，脚本会自动转换为 0.3。',
      '市值沿用“亿”作为输入单位，例如 100 表示 100 亿。',
      '遇到同名指标时，建议同时填写 category 以避免歧义。',
      '动态可选项请优先查看 dynamic-options-index.cn.json，再按分类拆分文件查看。'
    ],
    simpleInputSchema: buildSimpleInputSchema(),
    simpleInputExample: template,
    selectionRanges: (catalog.selectionRanges || []).map(simplifySelectionRange),
    metricCategories: buildMetricCategories(catalog.metrics || []),
    dynamicOptionsIndex
  };

  saveJson(outputPath, output);
  return {
    outputPath,
    categoryCount: Object.keys(output.metricCategories).length,
    metricCount: catalog.metrics.length
  };
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  const mode = args.mode || 'condition-config';

  if (mode === 'profiles' || args['all-profiles']) {
    const outputDir = args['output-dir']
      ? path.resolve(process.cwd(), args['output-dir'])
      : DEFAULT_PROFILE_DIR;
    const profiles = writeAllProfiles(outputDir);
    process.stdout.write(`${JSON.stringify({ mode: 'profiles', count: profiles.length, profiles }, null, 2)}\n`);
    return;
  }

  if (mode === 'profile') {
    const profileKey = args['profile-key']
      || inferProfileKeyFromUrl(args.url)
      || inferProfileKeyFromUrl(args['target-url'])
      || 'company-cn';
    const defaultOutputFileName = `${PAGE_PROFILE_PRESETS[profileKey]?.name || profileKey}.profile.json`;
    const outputFile = args.output
      ? path.resolve(process.cwd(), args.output)
      : path.join(DEFAULT_PROFILE_DIR, defaultOutputFileName);
    const result = writeOneProfile(profileKey, outputFile);
    process.stdout.write(`${JSON.stringify({ mode: 'profile', ...result }, null, 2)}\n`);
    return;
  }

  const catalogPath = args.catalog
    ? path.resolve(process.cwd(), args.catalog)
    : DEFAULT_CATALOG_PATH;
  const templatePath = args.template
    ? path.resolve(process.cwd(), args.template)
    : DEFAULT_TEMPLATE_PATH;
  const outputPath = args.output
    ? path.resolve(process.cwd(), args.output)
    : DEFAULT_CONDITION_CONFIG_PATH;
  const result = buildConditionConfig(catalogPath, templatePath, outputPath);
  process.stdout.write(`${JSON.stringify({ mode: 'condition-config', ...result }, null, 2)}\n`);
}

main();
