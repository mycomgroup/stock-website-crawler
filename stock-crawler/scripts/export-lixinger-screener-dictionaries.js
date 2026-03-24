import fs from 'fs';
import path from 'path';

const DEFAULT_AREA_CODE = 'cn';
const DEFAULT_PAGE_URL = `https://www.lixinger.com/analytics/screener/company-fundamental/${DEFAULT_AREA_CODE}`;
const DEFAULT_OUTPUT_DIR = path.resolve(process.cwd(), 'output/playwright/lixinger-screener');

function saveJson(filePath, data) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  fs.writeFileSync(filePath, JSON.stringify(data, null, 2));
}

function buildCookieHeader(setCookies) {
  return setCookies.map(value => value.split(';')[0]).join('; ');
}

async function login(username, password) {
  const response = await fetch('https://www.lixinger.com/api/account/sign-in/by-account', {
    method: 'POST',
    headers: {
      accept: 'application/json, text/plain, */*',
      'content-type': 'application/json;charset=UTF-8',
      referer: DEFAULT_PAGE_URL,
      'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    },
    body: JSON.stringify({ accountName: username, password })
  });

  if (!response.ok) {
    const text = await response.text().catch(() => '');
    throw new Error(`Login failed ${response.status}: ${text.slice(0, 500)}`);
  }

  const setCookies = response.headers.getSetCookie ? response.headers.getSetCookie() : [];
  return buildCookieHeader(setCookies);
}

async function fetchJson(url, { cookie, method = 'GET', body } = {}) {
  const response = await fetch(url, {
    method,
    headers: {
      accept: 'application/json, text/plain, */*',
      'content-type': 'application/json',
      cookie: cookie || '',
      referer: DEFAULT_PAGE_URL,
      'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    },
    body: body ? JSON.stringify(body) : undefined
  });

  const text = await response.text();
  if (!response.ok) {
    throw new Error(`Fetch failed ${response.status} ${url}: ${text.slice(0, 500)}`);
  }
  return JSON.parse(text);
}

function normalizeIndustry(records) {
  return records.map(item => ({
    id: item._id,
    code: item.stockCode,
    name: item.name,
    level: item.level,
    areaCode: item.areaCode,
    source: item.source,
    exchange: item.exchange,
    fsTableType: item.fsTableType || null,
    parentId: item.parent || null,
    tickerId: item.tickerId,
    pinyin: item.pinyin || null,
    followedNum: item.followedNum ?? null,
    stocksNum: item.stocksNum ?? null
  }));
}

function normalizeIndex(records) {
  return records.map(item => ({
    id: item._id,
    code: item.stockCode,
    name: item.name,
    fullName: item.fullName || null,
    areaCode: item.areaCode,
    source: item.source,
    exchange: item.exchange,
    market: item.market || null,
    fsTableType: item.fsTableType || null,
    tickerId: item.tickerId,
    pinyin: item.pinyin || null,
    followedNum: item.followedNum ?? null,
    stocksNum: item.stocksNum ?? null,
    totalReturnIndexId: item.totalReturnIndexId || null,
    constituentsMarkets: item.constituentsMarkets || []
  }));
}

async function main() {
  const username = process.env.LIXINGER_USERNAME;
  const password = process.env.LIXINGER_PASSWORD;
  const cookieFromEnv = process.env.LIXINGER_COOKIE;

  if (!cookieFromEnv && (!username || !password)) {
    throw new Error('Missing LIXINGER_USERNAME or LIXINGER_PASSWORD');
  }

  const cookie = cookieFromEnv || await login(username, password);

  const [industryRecords, indexRecords, provinces] = await Promise.all([
    fetchJson('https://www.lixinger.com/api/stock/stocks/stock-collections', {
      cookie,
      method: 'POST',
      body: { areaCode: DEFAULT_AREA_CODE, stockType: 'industry', fsTableType: null, sources: ['sw', 'sw_2021', 'cni'] }
    }),
    fetchJson('https://www.lixinger.com/api/stock/stocks/stock-collections', {
      cookie,
      method: 'POST',
      body: { stockType: 'index', fsTableType: null, excludeBlocked: true }
    }),
    fetchJson('https://www.lixinger.com/api/stock/provinces/list', { cookie })
  ]);

  const output = {
    generatedAt: new Date().toISOString(),
    sourceUrl: DEFAULT_PAGE_URL,
    areaCode: DEFAULT_AREA_CODE,
    stockBourseTypes: [
      { label: '沪市', value: 'sh' },
      { label: '沪市科创板', value: 'sh_kcb' },
      { label: '沪市主板', value: 'sh_main_board' },
      { label: '深圳', value: 'sz' },
      { label: '深圳创业板', value: 'sz_cyb' },
      { label: '深圳主板', value: 'sz_main_board' },
      { label: '北京', value: 'bj' }
    ],
    mutualMarkets: [
      { label: '陆股通', value: 'ha' }
    ],
    multiMarketListedTypes: [
      { label: 'AH市场上市', value: 'ah' },
      { label: 'AB市场上市', value: 'ab' }
    ],
    stockGroups: [
      { label: '全部关注', value: 'all' },
      { label: '默认组', value: 'default' }
    ],
    provinces: provinces.map(item => ({
      label: item.shortName,
      value: item.code,
      name: item.name
    })),
    industries: normalizeIndustry(industryRecords),
    indices: normalizeIndex(indexRecords)
  };

  saveJson(path.join(DEFAULT_OUTPUT_DIR, 'dynamic-stock-bourse-types.cn.json'), {
    generatedAt: output.generatedAt,
    sourceUrl: output.sourceUrl,
    items: output.stockBourseTypes
  });
  saveJson(path.join(DEFAULT_OUTPUT_DIR, 'dynamic-mutual-markets.cn.json'), {
    generatedAt: output.generatedAt,
    sourceUrl: output.sourceUrl,
    items: output.mutualMarkets
  });
  saveJson(path.join(DEFAULT_OUTPUT_DIR, 'dynamic-multi-market-listed-types.cn.json'), {
    generatedAt: output.generatedAt,
    sourceUrl: output.sourceUrl,
    items: output.multiMarketListedTypes
  });
  saveJson(path.join(DEFAULT_OUTPUT_DIR, 'dynamic-stock-groups.cn.json'), {
    generatedAt: output.generatedAt,
    sourceUrl: output.sourceUrl,
    items: output.stockGroups
  });
  saveJson(path.join(DEFAULT_OUTPUT_DIR, 'dynamic-provinces.cn.json'), {
    generatedAt: output.generatedAt,
    sourceUrl: output.sourceUrl,
    items: output.provinces
  });
  saveJson(path.join(DEFAULT_OUTPUT_DIR, 'dynamic-industries.cn.json'), {
    generatedAt: output.generatedAt,
    sourceUrl: output.sourceUrl,
    items: output.industries
  });
  saveJson(path.join(DEFAULT_OUTPUT_DIR, 'dynamic-indices.cn.json'), {
    generatedAt: output.generatedAt,
    sourceUrl: output.sourceUrl,
    items: output.indices
  });
  saveJson(path.join(DEFAULT_OUTPUT_DIR, 'dynamic-options-index.cn.json'), output);

  process.stdout.write(`${JSON.stringify({
    outputDir: DEFAULT_OUTPUT_DIR,
    counts: {
      stockBourseTypes: output.stockBourseTypes.length,
      mutualMarkets: output.mutualMarkets.length,
      multiMarketListedTypes: output.multiMarketListedTypes.length,
      stockGroups: output.stockGroups.length,
      provinces: output.provinces.length,
      industries: output.industries.length,
      indices: output.indices.length
    }
  }, null, 2)}\n`);
}

main().catch(error => {
  console.error(error.stack || error.message);
  process.exit(1);
});
