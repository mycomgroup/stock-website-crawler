import fs from 'fs';
import path from 'path';
import '../load-env.js';
import { LIXINGER_OUTPUT_DIR } from '../paths.js';
import {
  DEFAULT_CONDITION_CATALOG_PATH,
  loadConditionCatalog,
  resolveCatalogPath
} from '../shared/catalog.js';
import { queryToUnifiedInput, validateUnifiedQuery } from '../shared/natural-language.js';
import {
  buildRequestPlanFromScreener as buildSharedRequestPlanFromScreener,
  buildRequestPlanFromUnifiedInput as buildSharedRequestPlanFromUnifiedInput,
  mergeUnifiedInputs,
  normalizeUnifiedInput
} from '../shared/unified-input.js';

// 默认筛选器：10年估值历史低位
// 扣非PE-TTM过去10年分位点30%以下，PB（不含商誉）过去10年分位点30%以下，股息率2%以上
const DEFAULT_URL = 'https://www.lixinger.com/analytics/screener/company-fundamental/cn?screener-id=587c4d21d6e94ed9d447b29d';
const DEFAULT_CATALOG_PATH = DEFAULT_CONDITION_CATALOG_PATH;

const DEFAULT_RANGES = {
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
};

const SPECIAL_METRIC_ALIASES = {
  '上市日期': {
    requestId: 'pm.ipoDate',
    resultFieldKey: 'ipoDate',
    supportedSubConditionLabels: ['上市时间'],
    notes: '当前脚本只支持“上市时间”这一种子条件。'
  }
};

function showHelp() {
  process.stdout.write(
    [
      '用法：node request/fetch-lixinger-screener.js [选项]',
      '',
      '常用方式：',
      '  1. 直接读取理杏仁已保存筛选器',
      '     --url <筛选器页面 URL>',
      '     --screener-id <筛选器 ID>',
      '',
      '  2. 直接使用抓包后的请求体',
      '     --request-body-file <request-body.json>',
      '',
      '  3. 使用统一参数文件生成请求体',
      '     --input-file <input.json>',
      '     --simple-input-file <simple-input.json>   # 兼容旧参数名',
      '     --catalog-file <condition-catalog.cn.json>',
      '',
      '  4. 直接输入自然语言',
      '     --query "<自然语言筛选条件>"',
      '     --catalog-file <condition-catalog.cn.json>',
      '',
      '常用选项：',
      '  --output <table-json|markdown|csv|raw>   输出格式，默认 table-json',
      '  --page-size <数字>                        每页数量',
      '  --page-index <数字>                       起始页，默认 0',
      '  --save-request-body <文件路径>            保存最终请求体',
      '  --catalog-file <文件路径>                 条件目录，默认 output/playwright/lixinger-screener/condition-catalog.cn.json',
      '  --help                                   显示帮助',
      '',
      '环境变量：',
      '  LIXINGER_USERNAME',
      '  LIXINGER_PASSWORD',
      '',
      '示例：',
      '  node request/fetch-lixinger-screener.js --url "https://www.lixinger.com/analytics/screener/company-fundamental/cn?screener-id=587c4d21d6e94ed9d447b29d" --output markdown',
      '  node request/fetch-lixinger-screener.js --input-file output/playwright/lixinger-screener/simple-input-template.cn.json --output csv',
      '  node request/fetch-lixinger-screener.js --query "PE-TTM(扣非)统计值10年分位点小于30%，股息率大于2%" --output markdown'
    ].join('\n') + '\n'
  );
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

function parseScreenerUrl(url) {
  const parsed = new URL(url);
  const parts = parsed.pathname.split('/').filter(Boolean);
  return {
    url,
    areaCode: parts[parts.length - 1] || 'cn',
    screenerId: parsed.searchParams.get('screener-id')
  };
}

function buildCookieHeader(setCookies) {
  return setCookies.map(value => value.split(';')[0]).join('; ');
}

function loadJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, 'utf8'));
}

function saveJson(filePath, data) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  fs.writeFileSync(filePath, JSON.stringify(data, null, 2));
}

function normalizeSortName(sortName) {
  if (!sortName) return 'pm.latest.d_pe_ttm.y10.cvpos';
  if (sortName.startsWith('priceMetrics.latest.pm.')) {
    return sortName.replace(/^priceMetrics\.latest\.pm\./, 'pm.latest.');
  }
  if (sortName.startsWith('priceMetrics.latest.')) {
    return sortName.replace(/^priceMetrics\.latest\./, '');
  }
  return sortName;
}

function normalizeFilterList(filterList = []) {
  return filterList.map(item => {
    const next = { ...item };
    if (!Object.prototype.hasOwnProperty.call(next, 'value')) {
      next.value = 'all';
    }
    if (!next.date && next.id?.startsWith('pm.') && !/Date$/.test(next.id)) {
      next.date = 'latest';
    }
    return next;
  });
}

function defaultRanges(overrides = {}) {
  return {
    ...DEFAULT_RANGES,
    ...overrides,
    mutualMarkets: overrides.mutualMarkets || DEFAULT_RANGES.mutualMarkets,
    multiMarketListedType: overrides.multiMarketListedType || DEFAULT_RANGES.multiMarketListedType
  };
}

function mapScaleByUnit(unit) {
  if (unit === '%') return 0.01;
  if (unit === '亿') return 100000000;
  return 1;
}

function formatNumber(value, digits = 2) {
  if (value == null || Number.isNaN(value)) return '';
  return new Intl.NumberFormat('zh-CN', {
    minimumFractionDigits: digits,
    maximumFractionDigits: digits
  }).format(value);
}

function formatDateToChina(dateValue) {
  if (!dateValue) return '';
  const date = new Date(dateValue);
  if (Number.isNaN(date.getTime())) return String(dateValue);
  const formatter = new Intl.DateTimeFormat('en-CA', {
    timeZone: 'Asia/Shanghai',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  });
  return formatter.format(date);
}

function inferCnLatestQuarter(referenceDateString) {
  const date = referenceDateString ? new Date(referenceDateString) : new Date();
  const formatter = new Intl.DateTimeFormat('en-CA', {
    timeZone: 'Asia/Shanghai',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  });
  const today = formatter.format(date);
  const [yearText, monthText, dayText] = today.split('-');
  const year = Number(yearText);
  const monthDay = `${monthText}-${dayText}`;

  if (monthDay <= '04-30') {
    return `${year - 1}-09-30`;
  }
  if (monthDay <= '08-31') {
    return `${year}-03-31`;
  }
  if (monthDay <= '10-31') {
    return `${year}-06-30`;
  }
  return `${year}-09-30`;
}

function stripLatestSuffix(formulaId) {
  return formulaId.endsWith('.latest')
    ? formulaId.slice(0, -('.latest'.length))
    : formulaId;
}

function requestIdToResultFieldKey(requestId) {
  return requestId.replace(/^pm\./, '');
}

function guessThresholdKind(unit, inputType) {
  if (inputType === 'date') return 'date';
  if (unit === '%') return 'percentage';
  if (unit === '亿') return 'yi';
  return 'number';
}

function lookupCatalogEntry(catalog, condition) {
  if (!catalog?.metrics?.length) return null;

  if (condition.metric) {
    let candidates = catalog.metrics.filter(item => item.metric === condition.metric);
    if (condition.category) {
      candidates = candidates.filter(item => item.category === condition.category);
    }
    const preferred = candidates.find(item => item.category === '基本指标');
    return preferred || candidates[0] || null;
  }

  if (condition.formulaId) {
    const requestId = stripLatestSuffix(condition.formulaId);
    return catalog.metrics.find(item =>
      item.formulaIdExample === condition.formulaId ||
      item.requestIdExample === requestId ||
      item.specialRequestId === requestId
    ) || null;
  }

  return null;
}

function resolveSelectorChoice(selector, desiredLabel, metricName) {
  const option = selector.options.find(item => item.label === desiredLabel);
  if (!option) {
    throw new Error(
      `Unknown selector label "${desiredLabel}" for metric "${metricName}". ` +
      `Available options: ${selector.options.map(item => item.label).join(', ')}`
    );
  }
  return option;
}

function buildFormulaIdFromCondition(entry, condition) {
  if (condition.formulaId) {
    return condition.formulaId;
  }

  if (entry?.formulaIdTemplate) {
    let formulaId = entry.formulaIdTemplate;
    const selectors = condition.selectors || [];
    for (let index = 0; index < entry.selectors.length; index += 1) {
      const selector = entry.selectors[index];
      const desiredLabel = selectors[index] || selector.defaultLabel;
      const option = resolveSelectorChoice(selector, desiredLabel, entry.metric);
      formulaId = formulaId.replace(`{selector${index + 1}}`, option.value);
    }
    return formulaId;
  }

  return entry?.formulaIdExample || null;
}

function buildDisplayLabel(entry, condition) {
  if (condition.displayLabel) {
    return condition.displayLabel;
  }

  let label = entry.displayLabelExample || entry.metric;
  const selectors = condition.selectors || [];

  for (let index = 0; index < (entry.selectors || []).length; index += 1) {
    const selector = entry.selectors[index];
    const desiredLabel = selectors[index] || selector.defaultLabel;
    resolveSelectorChoice(selector, desiredLabel, entry.metric);
    if (selector.defaultLabel && desiredLabel && selector.defaultLabel !== desiredLabel) {
      label = label.replace(selector.defaultLabel, desiredLabel);
    }
  }

  return label;
}

function resolveSimpleCondition(entry, condition) {
  const alias = condition.metric ? SPECIAL_METRIC_ALIASES[condition.metric] : null;

  if (alias) {
    const subCondition = condition.subCondition || alias.supportedSubConditionLabels?.[0] || null;
    if (subCondition && alias.supportedSubConditionLabels && !alias.supportedSubConditionLabels.includes(subCondition)) {
      throw new Error(
        `Metric "${condition.metric}" currently supports only: ${alias.supportedSubConditionLabels.join(', ')}`
      );
    }

    return {
      filter: {
        id: alias.requestId,
        value: 'all',
        min: condition.min,
        max: condition.max
      },
      columnSpec: {
        metric: condition.metric,
        displayLabel: condition.metric,
        requestId: alias.requestId,
        resultFieldKey: alias.resultFieldKey,
        format: 'date',
        unit: null
      }
    };
  }

  if (!entry) {
    throw new Error(`Unable to resolve condition: ${JSON.stringify(condition)}`);
  }

  const formulaId = buildFormulaIdFromCondition(entry, condition);
  if (!formulaId) {
    throw new Error(`Metric "${entry.metric}" does not expose a formula ID.`);
  }

  const requestId = stripLatestSuffix(formulaId);
  const primaryThreshold = entry.thresholds?.min || entry.thresholds?.max || {};
  const scale = mapScaleByUnit(primaryThreshold.unit);
  const kind = guessThresholdKind(primaryThreshold.unit, primaryThreshold.inputType);

  const filter = {
    id: requestId,
    value: 'all'
  };

  if (!/Date$/.test(requestId)) {
    filter.date = condition.dateModeApi || 'latest';
  }

  if (condition.min != null) {
    filter.min = kind === 'date' ? condition.min : Number(condition.min) * scale;
  }
  if (condition.max != null) {
    filter.max = kind === 'date' ? condition.max : Number(condition.max) * scale;
  }

  return {
    filter,
    columnSpec: {
      metric: entry.metric,
      displayLabel: buildDisplayLabel(entry, condition),
      requestId,
      resultFieldKey: requestIdToResultFieldKey(requestId),
      format: kind,
      unit: primaryThreshold.unit || null
    }
  };
}

function buildRequestPlanFromScreener(config, options) {
  const body = {
    areaCode: config.areaCode || options.areaCode || 'cn',
    ranges: defaultRanges(config.ranges),
    filterList: normalizeFilterList(config.filterList),
    customFilterList: config.customFilterList || [],
    industrySource: config.industrySource || 'sw_2021',
    industryLevel: config.industryLevel || 'three',
    sortName: normalizeSortName(config.sortName),
    sortOrder: config.sortOrder || 'desc',
    pageIndex: Number(options.pageIndex || 0),
    pageSize: Number(options.pageSize || 100)
  };

  const columnSpecs = body.filterList.map(item => ({
    metric: item.id,
    displayLabel: item.id,
    requestId: item.id,
    resultFieldKey: requestIdToResultFieldKey(item.id),
    format: item.id.endsWith('Date') ? 'date' : 'number',
    unit: null
  }));

  return {
    body,
    columnSpecs,
    summary: {
      screenerName: config.name || null
    }
  };
}

function buildRequestPlanFromSimpleInput(simpleInput, catalog, options) {
  const filters = [];
  const columnSpecs = [];

  for (const condition of simpleInput.conditions || []) {
    const entry = lookupCatalogEntry(catalog, condition);
    const resolved = resolveSimpleCondition(entry, condition);
    filters.push(resolved.filter);
    columnSpecs.push(resolved.columnSpec);
  }

  const sortCondition = simpleInput.sort || simpleInput.conditions?.[0] || null;
  const sortEntry = sortCondition ? lookupCatalogEntry(catalog, sortCondition) : null;
  const resolvedSort = sortCondition ? resolveSimpleCondition(sortEntry, sortCondition) : null;

  const body = {
    areaCode: simpleInput.areaCode || options.areaCode || 'cn',
    ranges: defaultRanges(simpleInput.ranges),
    filterList: filters,
    customFilterList: [],
    industrySource: simpleInput.industrySource || 'sw_2021',
    industryLevel: simpleInput.industryLevel || 'three',
    sortName: simpleInput.sortName ||
      (resolvedSort ? `pm.latest.${requestIdToResultFieldKey(resolvedSort.filter.id)}` : null),
    sortOrder: simpleInput.sortOrder || simpleInput.sort?.order || 'desc',
    pageIndex: Number(simpleInput.pageIndex ?? options.pageIndex ?? 0),
    pageSize: Number(simpleInput.pageSize ?? options.pageSize ?? 100)
  };

  return {
    body,
    columnSpecs,
    summary: {
      screenerName: simpleInput.name || null
    }
  };
}

function getNestedValue(data, dotKey) {
  // 先尝试 pm.latest 扁平 key（原有逻辑）
  const pmLatest = data?.pm?.latest || {};
  if (Object.prototype.hasOwnProperty.call(pmLatest, dotKey)) {
    return pmLatest[dotKey];
  }
  // 再按点路径深层查找（如 hm.vol.td_cr_20d）
  const parts = dotKey.split('.');
  let cur = data;
  for (const part of parts) {
    if (cur == null || typeof cur !== 'object') return undefined;
    cur = cur[part];
  }
  return cur;
}

function flattenTableRows(rows, columnSpecs) {
  return rows.map((row, index) => {
    const result = {
      '#': index + 1,
      '公司名称': row.stock.name,
      '代码': `${row.stock.stockCode}.${row.stock.exchange}`,
      '行业': row.stock.industry?.name || '',
      '备注': '无备注'
    };

    for (const spec of columnSpecs) {
      const value = getNestedValue(row.data, spec.resultFieldKey);
      if (spec.format === 'percentage') {
        result[spec.displayLabel] = value == null ? '' : `${formatNumber(value * 100)}%`;
      } else if (spec.format === 'yi') {
        result[spec.displayLabel] = value == null ? '' : `${formatNumber(value / 100000000)}亿元`;
      } else if (spec.format === 'date') {
        result[spec.displayLabel] = formatDateToChina(value);
      } else {
        result[spec.displayLabel] = value == null ? '' : formatNumber(value);
      }
    }

    result['关注度'] = row.stock.followedNum ?? '';
    return result;
  });
}

function toCsv(rows) {
  if (!rows.length) return '';
  const headers = Object.keys(rows[0]);
  const escape = value => {
    if (value == null) return '';
    const text = String(value);
    if (/[",\n]/.test(text)) {
      return `"${text.replace(/"/g, '""')}"`;
    }
    return text;
  };

  const lines = [headers.join(',')];
  for (const row of rows) {
    lines.push(headers.map(header => escape(row[header])).join(','));
  }
  return lines.join('\n');
}

function toMarkdownTable(rows) {
  if (!rows.length) return '| # |\n| --- |\n';
  const headers = Object.keys(rows[0]);
  const escape = value => String(value ?? '').replace(/\|/g, '\\|').replace(/\n/g, ' ');
  const head = `| ${headers.join(' | ')} |`;
  const divider = `| ${headers.map(() => '---').join(' | ')} |`;
  const body = rows.map(row => `| ${headers.map(header => escape(row[header])).join(' | ')} |`);
  return [head, divider, ...body].join('\n');
}

async function lixingerFetch(url, init = {}) {
  const headers = {
    accept: 'application/json, text/plain, */*',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    referer: DEFAULT_URL,
    ...(init.headers || {})
  };

  const response = await fetch(url, {
    ...init,
    headers
  });

  if (!response.ok) {
    const text = await response.text().catch(() => '');
    throw new Error(`Request failed ${response.status} ${url}: ${text.slice(0, 500)}`);
  }

  return response;
}

async function login(username, password) {
  const response = await lixingerFetch('https://www.lixinger.com/api/account/sign-in/by-account', {
    method: 'POST',
    headers: {
      'content-type': 'application/json;charset=UTF-8'
    },
    body: JSON.stringify({
      accountName: username,
      password
    })
  });

  const setCookies = response.headers.getSetCookie ? response.headers.getSetCookie() : [];
  const cookie = buildCookieHeader(setCookies);
  if (!cookie) {
    throw new Error('Login succeeded but no cookie was returned');
  }
  return cookie;
}

async function getScreenerConfig(cookie, screenerId) {
  const response = await lixingerFetch(`https://www.lixinger.com/api/ugd/screener/${screenerId}`, {
    headers: { cookie }
  });
  return response.json();
}

async function getScreenerDates(cookie, areaCode) {
  const response = await lixingerFetch('https://www.lixinger.com/api/company/screener/dates', {
    method: 'POST',
    headers: {
      cookie,
      'content-type': 'application/json;charset=UTF-8'
    },
    body: JSON.stringify({ areaCode })
  });
  return response.json();
}

async function fetchScreenerRows(cookie, body) {
  const response = await lixingerFetch('https://www.lixinger.com/api/company/screener', {
    method: 'POST',
    headers: {
      cookie,
      'content-type': 'application/json;charset=UTF-8'
    },
    body: JSON.stringify(body)
  });
  return response.json();
}

async function fetchAllScreenerRows(cookie, body) {
  const firstPage = await fetchScreenerRows(cookie, body);
  const pageSize = Number(body.pageSize || firstPage.rows?.length || 100);
  const startPageIndex = Number(body.pageIndex || 0);
  const totalPages = Math.ceil((firstPage.total || 0) / pageSize);

  if (totalPages <= startPageIndex + 1) {
    return firstPage;
  }

  const remainingBodies = [];
  for (let pageIndex = startPageIndex + 1; pageIndex < totalPages; pageIndex += 1) {
    remainingBodies.push({ ...body, pageIndex });
  }

  const remainingPages = await Promise.all(
    remainingBodies.map(nextBody => fetchScreenerRows(cookie, nextBody))
  );

  return {
    ...firstPage,
    rows: [
      ...(firstPage.rows || []),
      ...remainingPages.flatMap(page => page.rows || [])
    ]
  };
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help || args.h) {
    showHelp();
    return;
  }

  const username = process.env.LIXINGER_USERNAME;
  const password = process.env.LIXINGER_PASSWORD;

  if (!username || !password) {
    throw new Error('Missing LIXINGER_USERNAME or LIXINGER_PASSWORD');
  }

  const outputMode = args.output || 'table-json';
  const screenerUrl = args.url || DEFAULT_URL;
  const parsedUrl = parseScreenerUrl(screenerUrl);
  const screenerId = args['screener-id'] || parsedUrl.screenerId;
  const catalogPath = resolveCatalogPath(args['catalog-file'], process.cwd());
  const saveRequestBodyPath = args['save-request-body']
    ? path.resolve(process.cwd(), args['save-request-body'])
    : null;

  const cookie = await login(username, password);

  let requestPlan;
  let screenerConfig = null;

  if (args['request-body-file']) {
    const filePath = path.resolve(process.cwd(), args['request-body-file']);
    requestPlan = {
      body: loadJson(filePath),
      columnSpecs: [],
      summary: {}
    };
  } else if (args['input-file'] || args['simple-input-file'] || args.query) {
    const inputFilePath = args['input-file'] || args['simple-input-file'];
    const inputFile = inputFilePath
      ? loadJson(path.resolve(process.cwd(), inputFilePath))
      : {};
    let unifiedInput = normalizeUnifiedInput(inputFile);
    const catalog = loadConditionCatalog(catalogPath);
    const naturalLanguageQueries = [inputFile.query, args.query].filter(Boolean);

    for (const query of naturalLanguageQueries) {
      const parsed = await queryToUnifiedInput(query, catalog.metrics);
      const validation = validateUnifiedQuery(parsed, catalog.metrics);
      if (!validation.valid) {
        throw new Error(validation.errors.join('\n'));
      }
      unifiedInput = mergeUnifiedInputs(unifiedInput, parsed);
    }

    if (!unifiedInput.conditions?.length) {
      throw new Error(
        'Missing input conditions. Provide --input-file, --simple-input-file, or --query'
      );
    }

    requestPlan = buildSharedRequestPlanFromUnifiedInput(unifiedInput, catalog, {
      areaCode: parsedUrl.areaCode,
      pageIndex: args['page-index'],
      pageSize: args['page-size']
    });
  } else {
    if (!screenerId) {
      throw new Error(
        'Missing screener id. Provide --screener-id, --url, --request-body-file, or --simple-input-file'
      );
    }
    screenerConfig = await getScreenerConfig(cookie, screenerId);
    requestPlan = buildSharedRequestPlanFromScreener(screenerConfig, {
      areaCode: parsedUrl.areaCode,
      pageIndex: args['page-index'],
      pageSize: args['page-size']
    });
  }

  if (saveRequestBodyPath) {
    saveJson(saveRequestBodyPath, requestPlan.body);
  }

  const [result, dates] = await Promise.all([
    fetchAllScreenerRows(cookie, requestPlan.body),
    getScreenerDates(cookie, requestPlan.body.areaCode)
  ]);

  const latestTime = formatDateToChina(dates.priceMetricsDate);
  const latestQuarter = requestPlan.body.areaCode === 'cn'
    ? inferCnLatestQuarter(dates.priceMetricsDate)
    : null;

  const tableRows = flattenTableRows(result.rows, requestPlan.columnSpecs);
  const screenerName = screenerConfig?.name || requestPlan.summary.screenerName || null;
  // 筛选器描述：从 API 返回的 description 或 remark 字段获取（理杏仁页面上展示的过滤条件说明）
  const screenerDescription = screenerConfig?.description || screenerConfig?.remark || null;

  const payload = {
    screenerId: screenerId || null,
    screenerName,
    screenerDescription,
    total: result.total,
    latestTime,
    latestQuarter,
    pageIndex: requestPlan.body.pageIndex,
    pageSize: requestPlan.body.pageSize,
    rows: tableRows
  };

  if (outputMode === 'raw') {
    process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
    return;
  }

  if (outputMode === 'csv') {
    if (screenerName) {
      process.stdout.write(`# 筛选器: ${screenerName}\n`);
    }
    if (screenerDescription) {
      process.stdout.write(`# 描述: ${screenerDescription}\n`);
    }
    process.stdout.write(`${toCsv(tableRows)}\n`);
    return;
  }

  if (outputMode === 'markdown') {
    if (screenerName) {
      process.stdout.write(`**${screenerName}**\n\n`);
    }
    if (screenerDescription) {
      process.stdout.write(`> ${screenerDescription}\n\n`);
    }
    process.stdout.write(`我们为您找到了 ${result.total} 个结果\n`);
    process.stdout.write(`(最新时间: ${latestTime}${latestQuarter ? ` 最新季度: ${latestQuarter}` : ''})\n\n`);
    process.stdout.write(`${toMarkdownTable(tableRows)}\n`);
    return;
  }

  process.stdout.write(`${JSON.stringify(payload, null, 2)}\n`);
}

main().catch(error => {
  console.error(error.stack || error.message);
  process.exit(1);
});
