/**
 * screener-runner.js
 * 通用筛选器运行核心，支持 company / fund / ii(index) 三种 API 类型。
 * 被各筛选器入口文件调用，不直接执行。
 *
 * 各筛选器对应关系：
 *   company-fundamental/cn  → apiType:'company', areaCode:'cn'
 *   fund-fundamental/cn     → apiType:'fund',    areaCode:'cn'
 *   index-fundamental/cn    → apiType:'ii',      areaCode:'cn',  stockType:'index'
 *   company-fundamental/hk  → apiType:'company', areaCode:'hk'
 *   company-fundamental/us  → apiType:'company', areaCode:'us'
 *   index-fundamental/hk    → apiType:'ii',      areaCode:'hk',  stockType:'index'
 */
import fs from 'fs';
import path from 'path';
import '../load-env.js';
import {
  DEFAULT_CONDITION_CATALOG_PATH,
  loadConditionCatalog,
  resolveCatalogPath
} from '../shared/catalog.js';
import { queryToUnifiedInput, validateUnifiedQuery } from '../shared/natural-language.js';
import {
  buildRequestPlanFromScreener,
  buildRequestPlanFromUnifiedInput,
  mergeUnifiedInputs,
  normalizeUnifiedInput
} from '../shared/unified-input.js';

// ─── API 端点映射 ────────────────────────────────────────────────────────────

const SCREENER_API = {
  company: 'https://www.lixinger.com/api/company/screener',
  fund:    'https://www.lixinger.com/api/fund/screener',
  ii:      'https://www.lixinger.com/api/ii/screener'
};

const SCREENER_DATES_API = {
  company: 'https://www.lixinger.com/api/company/screener/dates',
  fund:    null,  // 基金筛选器无 dates 接口
  ii:      'https://www.lixinger.com/api/ii/screener/dates'
};

// ─── 各筛选器的默认 ranges ────────────────────────────────────────────────────

const DEFAULT_RANGES_BY_TYPE = {
  // A股公司（原有逻辑）
  'company-cn': {
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
  // 港股公司
  'company-hk': {
    stockBourseTypes: [],
    mutualMarkets: { selectedMutualMarkets: [], selectType: 'include' },
    multiMarketListedType: { selectedMultiMarketListedTypes: [], selectType: 'include' },
    excludeBlacklist: false,
    excludeDelisted: false,
    excludeBourseType: false,
    constituentsPerspectiveType: 'history'
  },
  // 美股公司
  'company-us': {
    excludeBlacklist: false,
    excludeDelisted: false,
    constituentsPerspectiveType: 'history'
  },
  // A股基金
  'fund-cn': {
    excludeDelisted: true,
    excludeAbnormalNav: false
  },
  // A股指数
  'index-cn': {
    source: 'all',
    series: 'all',
    calculationMethod: 'all',
    keyword: ''
  },
  // 港股指数
  'index-hk': {
    source: 'all',
    keyword: ''
  }
};

// ─── 各筛选器的默认 industrySource/industryLevel ─────────────────────────────

const INDUSTRY_BY_TYPE = {
  'company-cn': { industrySource: 'sw_2021', industryLevel: 'three' },
  'company-hk': { industrySource: 'hsi', industryLevel: 'three' },
  'company-us': { industrySource: null, industryLevel: null },
  'fund-cn':    {},
  'index-cn':   {},
  'index-hk':   {}
};

const DEFAULT_SORT_BY_TYPE = {
  'company-cn': 'pm.latest.d_pe_ttm.y10.cvpos',
  'company-hk': 'pm.latest.pe_ttm',
  'company-us': 'pm.latest.pe_ttm',
  'fund-cn': 'pm.latest.hm.vol.td_cr_20d',
  'index-cn': 'hm.o.followedNum',
  'index-hk': 'hm.o.followedNum'
};

// ─── 行数据展开 ───────────────────────────────────────────────────────────────

function getNestedValue(data, dotKey) {
  const pmLatest = data?.pm?.latest || {};
  if (Object.prototype.hasOwnProperty.call(pmLatest, dotKey)) {
    return pmLatest[dotKey];
  }
  const parts = dotKey.split('.');
  let cur = data;
  for (const part of parts) {
    if (cur == null || typeof cur !== 'object') return undefined;
    cur = cur[part];
  }
  return cur;
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
  return new Intl.DateTimeFormat('en-CA', {
    timeZone: 'Asia/Shanghai',
    year: 'numeric', month: '2-digit', day: '2-digit'
  }).format(date);
}

function flattenTableRows(rows, columnSpecs, screenerKey) {
  const isFund = screenerKey === 'fund-cn';
  const isIndex = screenerKey === 'index-cn' || screenerKey === 'index-hk';

  const nameLabel = isFund ? '基金名称' : isIndex ? '指数名称' : '公司名称';
  const codeLabel = isFund ? '基金代码' : isIndex ? '指数代码' : '代码';

  return rows.map((row, index) => {
    const s = row.stock || {};
    const code = s.stockCode
      ? (s.exchange ? `${s.stockCode}.${s.exchange}` : s.stockCode)
      : '';

    const result = {
      '#': index + 1,
      [nameLabel]: s.name || s.shortName || '',
      [codeLabel]: code
    };

    if (!isFund && !isIndex) {
      result['行业'] = s.industry?.name || '';
    }
    if (isFund) {
      result['基金类型'] = s.fundSecondLevel || '';
      result['基金经理'] = Array.isArray(s.managers)
        ? s.managers.map(m => m.name || m).join('、')
        : '';
    }

    result['备注'] = '无备注';

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

    result['关注度'] = s.followedNum ?? '';
    return result;
  });
}

// ─── 输出格式化 ──────────────────────────────────────────────────────────────

function toCsv(rows) {
  if (!rows.length) return '';
  const headers = Object.keys(rows[0]);
  const escape = v => {
    if (v == null) return '';
    const t = String(v);
    return /[",\n]/.test(t) ? `"${t.replace(/"/g, '""')}"` : t;
  };
  return [headers.join(','), ...rows.map(r => headers.map(h => escape(r[h])).join(','))].join('\n');
}

function toMarkdownTable(rows) {
  if (!rows.length) return '| # |\n| --- |\n';
  const headers = Object.keys(rows[0]);
  const esc = v => String(v ?? '').replace(/\|/g, '\\|').replace(/\n/g, ' ');
  return [
    `| ${headers.join(' | ')} |`,
    `| ${headers.map(() => '---').join(' | ')} |`,
    ...rows.map(r => `| ${headers.map(h => esc(r[h])).join(' | ')} |`)
  ].join('\n');
}

// ─── HTTP 工具 ───────────────────────────────────────────────────────────────

function buildCookieHeader(setCookies) {
  return setCookies.map(v => v.split(';')[0]).join('; ');
}

function loadJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, 'utf8'));
}

function saveJson(filePath, data) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  fs.writeFileSync(filePath, JSON.stringify(data, null, 2));
}

function loadProfile(profilePath, cwd = process.cwd()) {
  if (!profilePath) return null;
  return loadJson(path.resolve(cwd, profilePath));
}

async function lixingerFetch(url, init = {}, refererUrl) {
  const headers = {
    accept: 'application/json, text/plain, */*',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    referer: refererUrl || 'https://www.lixinger.com/',
    ...(init.headers || {})
  };
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 20000);
  try {
    const response = await fetch(url, { ...init, headers, signal: controller.signal });
    if (!response.ok) {
      const text = await response.text().catch(() => '');
      throw new Error(`Request failed ${response.status} ${url}: ${text.slice(0, 500)}`);
    }
    return response;
  } finally {
    clearTimeout(timer);
  }
}

async function login(username, password) {
  const response = await lixingerFetch('https://www.lixinger.com/api/account/sign-in/by-account', {
    method: 'POST',
    headers: { 'content-type': 'application/json;charset=UTF-8' },
    body: JSON.stringify({ accountName: username, password })
  });
  const setCookies = response.headers.getSetCookie ? response.headers.getSetCookie() : [];
  const cookie = buildCookieHeader(setCookies);
  if (!cookie) throw new Error('Login succeeded but no cookie was returned');
  return cookie;
}

async function getScreenerConfig(cookie, screenerId) {
  const response = await lixingerFetch(`https://www.lixinger.com/api/ugd/screener/${screenerId}`, {
    headers: { cookie }
  });
  return response.json();
}

async function getScreenerDates(cookie, areaCode, apiType) {
  const datesUrl = SCREENER_DATES_API[apiType];
  if (!datesUrl) return {};
  const response = await lixingerFetch(datesUrl, {
    method: 'POST',
    headers: { cookie, 'content-type': 'application/json;charset=UTF-8' },
    body: JSON.stringify({ areaCode })
  });
  return response.json();
}

async function fetchScreenerRows(cookie, body, apiType, refererUrl) {
  const apiUrl = SCREENER_API[apiType] || SCREENER_API.company;
  const response = await lixingerFetch(apiUrl, {
    method: 'POST',
    headers: { cookie, 'content-type': 'application/json;charset=UTF-8' },
    body: JSON.stringify(body)
  }, refererUrl);
  return response.json();
}

async function fetchAllScreenerRows(cookie, body, apiType, refererUrl) {
  const firstPage = await fetchScreenerRows(cookie, body, apiType, refererUrl);
  const pageSize = Number(body.pageSize || firstPage.rows?.length || 100);
  const startPageIndex = Number(body.pageIndex || 0);
  const totalPages = Math.ceil((firstPage.total || 0) / pageSize);

  if (totalPages <= startPageIndex + 1) return firstPage;

  // 串行拉取剩余分页，避免并发过多触发限流
  const allRows = [...(firstPage.rows || [])];
  for (let pageIndex = startPageIndex + 1; pageIndex < totalPages; pageIndex += 1) {
    const page = await fetchScreenerRows(cookie, { ...body, pageIndex }, apiType, refererUrl);
    allRows.push(...(page.rows || []));
  }

  return { ...firstPage, rows: allRows };
}

// ─── 请求体构建 ───────────────────────────────────────────────────────────────

/**
 * 根据 screenerKey 构建请求体，合并 filterList 和各类型特有字段
 */
function buildRequestBody(
  screenerKey,
  areaCode,
  filterList,
  sortName,
  sortOrder,
  pageIndex,
  pageSize,
  rangesOverride,
  profile = null
) {
  const apiType = screenerKey.split('-')[0] === 'index' ? 'ii' : screenerKey.split('-')[0];
  const defaultRanges = profile?.ranges || DEFAULT_RANGES_BY_TYPE[screenerKey] || {};
  const ranges = { ...defaultRanges, ...(rangesOverride || {}) };
  const industry = profile?.industrySource !== undefined || profile?.industryLevel !== undefined
    ? {
        industrySource: profile?.industrySource,
        industryLevel: profile?.industryLevel
      }
    : (INDUSTRY_BY_TYPE[screenerKey] || {});
  const defaultSortName = profile?.sortName || DEFAULT_SORT_BY_TYPE[screenerKey] || '';
  const defaultSortOrder = profile?.sortOrder || 'desc';

  const body = {
    areaCode,
    ranges,
    filterList,
    customFilterList: [],
    sortName: sortName || defaultSortName,
    sortOrder: sortOrder || defaultSortOrder,
    pageIndex: Number(pageIndex ?? profile?.pageIndex ?? 0),
    pageSize: Number(pageSize ?? profile?.pageSize ?? 100)
  };

  // ii/screener 需要 stockType
  if (apiType === 'ii') {
    body.stockType = 'index';
  }

  // company 筛选器需要 industrySource/industryLevel
  if (industry.industrySource !== undefined) {
    body.industrySource = industry.industrySource;
    body.industryLevel = industry.industryLevel;
  }

  return body;
}

// ─── CLI 参数解析 ─────────────────────────────────────────────────────────────

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (!arg.startsWith('--')) continue;
    const key = arg.slice(2);
    const next = argv[i + 1];
    if (!next || next.startsWith('--')) { args[key] = true; continue; }
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

function inferCnLatestQuarter(referenceDateString) {
  const date = referenceDateString ? new Date(referenceDateString) : new Date();
  const today = new Intl.DateTimeFormat('en-CA', {
    timeZone: 'Asia/Shanghai', year: 'numeric', month: '2-digit', day: '2-digit'
  }).format(date);
  const [yearText, monthText, dayText] = today.split('-');
  const year = Number(yearText);
  const monthDay = `${monthText}-${dayText}`;
  if (monthDay <= '04-30') return `${year - 1}-09-30`;
  if (monthDay <= '08-31') return `${year}-03-31`;
  if (monthDay <= '10-31') return `${year}-06-30`;
  return `${year}-09-30`;
}

// ─── 主入口（供各入口文件调用）───────────────────────────────────────────────

/**
 * @param {object} config
 * @param {string} config.defaultUrl    - 该筛选器的默认 URL
 * @param {string} config.screenerKey   - 'company-cn'|'fund-cn'|'index-cn'|'company-hk'|'company-us'|'index-hk'
 * @param {string} [config.helpName]    - 帮助信息中显示的脚本名
 */
export async function runScreener(config) {
  const { defaultUrl, screenerKey, helpName = 'fetch-screener.js' } = config;

  // 从 screenerKey 推导 apiType 和 areaCode
  const [rawType, areaCodeFromKey] = screenerKey.split('-');

  const args = parseArgs(process.argv.slice(2));
  const profilePath = args['config-file'] || config.profilePath;
  const profile = config.profile || loadProfile(profilePath, config.cwd);
  const apiType = profile?.apiType || (rawType === 'index' ? 'ii' : rawType); // index → ii

  if (args.help || args.h) {
    process.stdout.write(
      `用法：node request/${helpName} [选项]\n\n` +
      `  --url <筛选器页面 URL>\n` +
      `  --screener-id <筛选器 ID>\n` +
      `  --request-body-file <request-body.json>\n` +
      `  --input-file <input.json>\n` +
      `  --query "<自然语言筛选条件>"\n` +
      `  --config-file <profile.json>\n` +
      `  --output <table-json|markdown|csv|raw>   默认 table-json\n` +
      `  --page-size <数字>\n` +
      `  --page-index <数字>\n` +
      `  --save-request-body <文件路径>\n` +
      `  --catalog-file <文件路径>\n` +
      `  --help\n`
    );
    return;
  }

  const username = process.env.LIXINGER_USERNAME;
  const password = process.env.LIXINGER_PASSWORD;
  if (!username || !password) throw new Error('Missing LIXINGER_USERNAME or LIXINGER_PASSWORD');

  const outputMode = args.output || 'table-json';
  const screenerUrl = args.url || defaultUrl || profile?.defaultUrl || '';
  const parsedUrl = screenerUrl ? parseScreenerUrl(screenerUrl) : { areaCode: null, screenerId: null };
  const areaCode = profile?.areaCode || parsedUrl.areaCode || areaCodeFromKey || 'cn';
  const screenerId = args['screener-id'] || parsedUrl.screenerId;
  let catalogPath = resolveCatalogPath(args['catalog-file'], process.cwd(), profile?.catalogPath);
  if (!fs.existsSync(catalogPath)) {
    console.warn(`[warn] catalog 文件不存在：${catalogPath}，回退到默认 A 股 catalog，请先运行对应的 catalog 生成脚本。`);
    catalogPath = DEFAULT_CONDITION_CATALOG_PATH;
  }
  const saveRequestBodyPath = args['save-request-body']
    ? path.resolve(process.cwd(), args['save-request-body'])
    : null;

  const cookie = await login(username, password);

  let requestPlan;
  let screenerConfig = null;

  if (args['request-body-file']) {
    requestPlan = {
      body: loadJson(path.resolve(process.cwd(), args['request-body-file'])),
      columnSpecs: [],
      summary: {}
    };
  } else if (args['input-file'] || args['simple-input-file'] || args.query) {
    const inputFilePath = args['input-file'] || args['simple-input-file'];
    const inputFile = inputFilePath ? loadJson(path.resolve(process.cwd(), inputFilePath)) : {};
    let unifiedInput = normalizeUnifiedInput(inputFile);
    const catalog = loadConditionCatalog(catalogPath);

    for (const query of [inputFile.query, args.query].filter(Boolean)) {
      const parsed = await queryToUnifiedInput(query, catalog.metrics);
      const validation = validateUnifiedQuery(parsed, catalog.metrics);
      if (!validation.valid) throw new Error(validation.errors.join('\n'));
      unifiedInput = mergeUnifiedInputs(unifiedInput, parsed);
    }

    if (!unifiedInput.conditions?.length) {
      throw new Error('Missing input conditions. Provide --input-file, --simple-input-file, or --query');
    }

    // 用 shared 的 buildRequestPlanFromUnifiedInput 生成 filterList/columnSpecs
    const basePlan = buildRequestPlanFromUnifiedInput(unifiedInput, catalog, {
      areaCode,
      pageIndex: args['page-index'] ?? profile?.pageIndex,
      pageSize: args['page-size'] ?? profile?.pageSize,
      defaultRanges: profile?.ranges,
      industrySource: profile?.industrySource,
      industryLevel: profile?.industryLevel,
      defaultSortName: profile?.sortName,
      defaultSortOrder: profile?.sortOrder
    });

    // 用本模块的 buildRequestBody 重新组装，加入各筛选器特有字段
    requestPlan = {
      ...basePlan,
      body: buildRequestBody(
        screenerKey,
        areaCode,
        basePlan.body.filterList,
        basePlan.body.sortName,
        basePlan.body.sortOrder,
        basePlan.body.pageIndex,
        basePlan.body.pageSize,
        unifiedInput.ranges,
        profile
      )
    };
  } else {
    if (!screenerId) {
      throw new Error('Missing screener id. Provide --screener-id, --url, --request-body-file, or --input-file');
    }
    screenerConfig = await getScreenerConfig(cookie, screenerId);

    // 用 shared 的 buildRequestPlanFromScreener 生成基础 plan
    const basePlan = buildRequestPlanFromScreener(screenerConfig, {
      areaCode,
      pageIndex: args['page-index'] ?? profile?.pageIndex,
      pageSize: args['page-size'] ?? profile?.pageSize,
      defaultRanges: profile?.ranges,
      industrySource: profile?.industrySource,
      industryLevel: profile?.industryLevel,
      defaultSortName: profile?.sortName,
      defaultSortOrder: profile?.sortOrder
    });

    // 重新组装请求体，加入各筛选器特有字段
    requestPlan = {
      ...basePlan,
      body: buildRequestBody(
        screenerKey,
        areaCode,
        basePlan.body.filterList,
        basePlan.body.sortName,
        basePlan.body.sortOrder,
        basePlan.body.pageIndex,
        basePlan.body.pageSize,
        screenerConfig.ranges,
        profile
      )
    };
  }

  if (saveRequestBodyPath) saveJson(saveRequestBodyPath, requestPlan.body);

  const [result, dates] = await Promise.all([
    fetchAllScreenerRows(cookie, requestPlan.body, apiType, screenerUrl),
    getScreenerDates(cookie, areaCode, apiType).catch(() => ({}))
  ]);

  const latestTime = formatDateToChina(dates.priceMetricsDate);
  const latestQuarter = areaCode === 'cn'
    ? inferCnLatestQuarter(dates.priceMetricsDate)
    : null;

  const tableRows = flattenTableRows(result.rows || [], requestPlan.columnSpecs, screenerKey);
  const screenerName = screenerConfig?.name || requestPlan.summary.screenerName || null;
  const screenerDescription = screenerConfig?.description || screenerConfig?.remark || null;

  if (outputMode === 'raw') {
    process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
    return;
  }

  if (outputMode === 'csv') {
    if (screenerName) process.stdout.write(`# 筛选器: ${screenerName}\n`);
    if (screenerDescription) process.stdout.write(`# 描述: ${screenerDescription}\n`);
    process.stdout.write(`${toCsv(tableRows)}\n`);
    return;
  }

  if (outputMode === 'markdown') {
    if (screenerName) process.stdout.write(`**${screenerName}**\n\n`);
    if (screenerDescription) process.stdout.write(`> ${screenerDescription}\n\n`);
    process.stdout.write(`我们为您找到了 ${result.total} 个结果\n`);
    process.stdout.write(`(最新时间: ${latestTime}${latestQuarter ? ` 最新季度: ${latestQuarter}` : ''})\n\n`);
    process.stdout.write(`${toMarkdownTable(tableRows)}\n`);
    return;
  }

  process.stdout.write(`${JSON.stringify({
    screenerId: screenerId || null,
    screenerName,
    screenerDescription,
    total: result.total,
    latestTime,
    latestQuarter,
    pageIndex: requestPlan.body.pageIndex,
    pageSize: requestPlan.body.pageSize,
    rows: tableRows
  }, null, 2)}\n`);
}
