import fs from 'fs';
import path from 'path';
import { chromium } from 'playwright';

const DEFAULT_AREA_CODE = 'cn';
const DEFAULT_PAGE_URL = `https://www.lixinger.com/analytics/screener/company-fundamental/${DEFAULT_AREA_CODE}`;
const DEFAULT_OUTPUT_DIR = path.resolve(process.cwd(), 'output/playwright/lixinger-screener');
const DEFAULT_CATALOG_PATH = path.join(DEFAULT_OUTPUT_DIR, 'condition-catalog.cn.json');
const DEFAULT_TEMPLATE_PATH = path.join(DEFAULT_OUTPUT_DIR, 'simple-input-template.cn.json');

const TAB_NAMES = [
  '基本指标',
  '热度指标',
  '资产负债表',
  '利润表',
  '现金流量表',
  '财务指标',
  '财报属性'
];

const SPECIAL_METRIC_ALIASES = {
  '上市日期': {
    requestId: 'pm.ipoDate',
    resultFieldKey: 'ipoDate',
    supportedSubConditionLabels: ['上市时间'],
    notes: '无公式 ID。当前脚本只支持“上市时间”。'
  }
};

const SELECTION_RANGES = [
  {
    key: 'market',
    label: '市场',
    type: 'single-select',
    options: [
      { label: 'AB股市场', value: '' },
      { label: 'A股市场', value: 'a' },
      { label: 'B股市场', value: 'b' }
    ]
  },
  {
    key: 'stockBourseTypes',
    label: '交易板块',
    type: 'multi-select',
    source: 'page-picker',
    note: '页面可选，当前目录未展开所有板块值。'
  },
  {
    key: 'industry',
    label: '行业',
    type: 'entity-select',
    source: 'page-picker',
    note: '页面可选，支持包含/排除。'
  },
  {
    key: 'index',
    label: '指数',
    type: 'entity-select',
    source: 'page-picker',
    note: '页面可选，支持交集/排除。'
  },
  {
    key: 'stockGroups',
    label: '我的关注',
    type: 'entity-select',
    source: 'page-picker',
    note: '页面可选，支持交集/排除。'
  },
  {
    key: 'mutualMarkets',
    label: '互联互通市场',
    type: 'multi-select',
    source: 'page-picker'
  },
  {
    key: 'multiMarketListedType',
    label: '多市场上市',
    type: 'multi-select',
    source: 'page-picker'
  },
  {
    key: 'province',
    label: '省份',
    type: 'entity-select',
    source: 'api/stock/provinces/list'
  },
  { key: 'excludeBlacklist', label: '排除屏蔽名单', type: 'boolean' },
  { key: 'excludeDelisted', label: '排除退市股', type: 'boolean' },
  { key: 'excludeSpecialTreatment', label: '排除ST', type: 'boolean' },
  { key: 'specialTreatmentOnly', label: '只含ST', type: 'boolean' }
];

function saveJson(filePath, data) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  fs.writeFileSync(filePath, JSON.stringify(data, null, 2));
}

function buildCookieHeader(setCookies) {
  return setCookies.map(value => value.split(';')[0]).join('; ');
}

function stripLatestSuffix(formulaId) {
  return formulaId?.endsWith('.latest')
    ? formulaId.slice(0, -('.latest'.length))
    : formulaId;
}

function requestIdToResultFieldKey(requestId) {
  return requestId ? requestId.replace(/^pm\./, '') : null;
}

function mapScaleByUnit(unit) {
  if (unit === '%') return 0.01;
  if (unit === '亿') return 100000000;
  return 1;
}

function buildTemplate(formulaId, selectors) {
  if (!formulaId) return null;
  let template = formulaId;
  selectors.forEach((selector, index) => {
    if (!selector.defaultValue) return;
    template = template.replace(selector.defaultValue, `{selector${index + 1}}`);
  });
  return template;
}

function inferFormatFromThreshold(threshold) {
  if (!threshold) return 'number';
  if (threshold.inputType === 'date') return 'date';
  if (threshold.unit === '%') return 'percentage';
  if (threshold.unit === '亿') return 'yi';
  return 'number';
}

async function login(username, password) {
  const response = await fetch('https://www.lixinger.com/api/account/sign-in/by-account', {
    method: 'POST',
    headers: {
      accept: 'application/json, text/plain, */*',
      'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
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

async function fetchProvinces(cookie) {
  const response = await fetch('https://www.lixinger.com/api/stock/provinces/list', {
    headers: {
      accept: 'application/json, text/plain, */*',
      'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
      cookie,
      referer: DEFAULT_PAGE_URL,
      'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    }
  });

  if (!response.ok) {
    return [];
  }
  return response.json();
}

async function createPage(cookie) {
  const browser = await chromium.launch({
    headless: true,
    channel: 'chrome',
    args: [
      '--disable-blink-features=AutomationControlled',
      '--no-sandbox',
      '--disable-setuid-sandbox'
    ]
  }).catch(() => chromium.launch({
    headless: true,
    args: [
      '--disable-blink-features=AutomationControlled',
      '--no-sandbox',
      '--disable-setuid-sandbox'
    ]
  }));

  const context = await browser.newContext({
    locale: 'zh-CN',
    viewport: { width: 1600, height: 1400 },
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
  });

  const cookies = cookie
    .split(';')
    .map(item => item.trim())
    .filter(Boolean)
    .map(item => {
      const [name, ...rest] = item.split('=');
      return {
        name,
        value: rest.join('='),
        domain: '.lixinger.com',
        path: '/',
        secure: true,
        sameSite: 'Lax'
      };
    });

  await context.addCookies(cookies);
  const page = await context.newPage();
  await page.goto(DEFAULT_PAGE_URL, { waitUntil: 'domcontentloaded', timeout: 45000 });
  await page.waitForTimeout(8000);

  return { browser, context, page };
}

async function reloadBasePage(page) {
  await page.goto(DEFAULT_PAGE_URL, { waitUntil: 'domcontentloaded', timeout: 45000 });
  await page.waitForTimeout(4000);
}

async function clickTab(page, tabName) {
  await page.locator(`a.nav-link:has-text("${tabName}")`).first().click({ force: true });
  await page.waitForTimeout(800);
}

async function extractVisibleFieldTitles(page) {
  return page.evaluate(() => {
    const isVisible = element => {
      const style = window.getComputedStyle(element);
      return style.display !== 'none' && style.visibility !== 'hidden' && element.offsetParent !== null;
    };

    return [...document.querySelectorAll('li.field div.plus-btn[title]')]
      .filter(element => isVisible(element))
      .map(element => element.getAttribute('title'))
      .filter(Boolean);
  });
}

async function addField(page, title) {
  await page.locator(`div.plus-btn[title="${title}"]`).first().click({ force: true });
  await page.waitForTimeout(500);
}

async function deleteCurrentField(page) {
  const deleteButton = page.locator('tr svg.fa-xmark').first();
  if (await deleteButton.count()) {
    await deleteButton.click({ force: true });
    await page.waitForTimeout(400);
  }
}

async function withTimeout(task, ms, label) {
  return Promise.race([
    task(),
    new Promise((_, reject) => {
      setTimeout(() => reject(new Error(`Timeout: ${label}`)), ms);
    })
  ]);
}

async function extractCurrentRowInfo(page, category, metricTitle) {
  return page.evaluate(({ category, metricTitle, specialAliases }) => {
    const row = [...document.querySelectorAll('tr')]
      .find(item => item.querySelector('svg.fa-xmark'));

    if (!row) return null;

    const cells = [...row.querySelectorAll('td')];
    const titleCell = cells[1];
    const dateCell = cells[2];
    const subConditionCell = cells[3];
    const minCell = cells[4];
    const maxCell = cells[5];

    const formulaId = titleCell.innerText.match(/ID: \[([^\]]+)\]/)?.[1] || null;
    const selectors = [...titleCell.querySelectorAll('select')].map((select, index) => ({
      name: `selector${index + 1}`,
      defaultLabel: select.selectedOptions[0]?.textContent.trim() || null,
      defaultValue: select.value || null,
      options: [...select.options].map(option => ({
        label: option.textContent.trim(),
        value: option.value
      }))
    }));

    const dateSelect = dateCell.querySelector('select');
    const dateModes = dateSelect
      ? [...dateSelect.options].map(option => ({
          label: option.textContent.trim(),
          value: option.value
        }))
      : [{ label: dateCell.innerText.trim() || '最新时间', value: 'latest_time' }];

    const subConditionOptions = [...subConditionCell.querySelectorAll('label, option')]
      .map(element => element.textContent.trim())
      .filter(Boolean);

    const parseThreshold = cell => {
      const input = cell.querySelector('input');
      const unit = cell.querySelector('.input-group-text')?.textContent.trim() || null;
      return {
        inputType: input?.getAttribute('type') || 'number',
        unit,
        scale: unit === '%' ? 0.01 : unit === '亿' ? 100000000 : 1
      };
    };

    const specialAlias = specialAliases[metricTitle] || null;
    const requestIdExample = formulaId
      ? formulaId.replace(/\.latest$/, '')
      : specialAlias?.requestId || null;
    const resultFieldKey = requestIdExample
      ? requestIdExample.replace(/^pm\./, '')
      : specialAlias?.resultFieldKey || null;

    return {
      category,
      metric: metricTitle,
      displayLabelExample: titleCell.querySelector('span[title]')?.textContent.trim() || metricTitle,
      formulaIdExample: formulaId,
      requestIdExample,
      resultFieldKey,
      selectors,
      dateModes,
      subConditionOptions,
      thresholds: {
        min: parseThreshold(minCell),
        max: parseThreshold(maxCell)
      },
      notes: specialAlias?.notes || null
    };
  }, {
    category,
    metricTitle,
    specialAliases: SPECIAL_METRIC_ALIASES
  });
}

function finalizeMetricEntry(entry) {
  const formulaIdTemplate = buildTemplate(entry.formulaIdExample, entry.selectors);
  const requestIdTemplate = formulaIdTemplate ? stripLatestSuffix(formulaIdTemplate) : entry.requestIdExample;
  const primaryThreshold = entry.thresholds.min.unit ? entry.thresholds.min : entry.thresholds.max;

  return {
    ...entry,
    formulaIdTemplate,
    requestIdTemplate,
    format: inferFormatFromThreshold(primaryThreshold),
    unit: primaryThreshold.unit || null,
    apiScale: mapScaleByUnit(primaryThreshold.unit),
    specialRequestId: !entry.formulaIdExample ? entry.requestIdExample : null
  };
}

function buildSimpleInputTemplate(catalog) {
  return {
    name: '10年估值历史低位_示例',
    areaCode: 'cn',
    pageSize: 100,
    sort: {
      metric: 'PE-TTM(扣非)统计值',
      selectors: ['10年', '分位点%'],
      order: 'desc'
    },
    ranges: {
      market: 'a',
      excludeBlacklist: false,
      excludeDelisted: false,
      excludeSpecialTreatment: false,
      specialTreatmentOnly: false
    },
    conditions: [
      {
        metric: 'PE-TTM(扣非)统计值',
        selectors: ['10年', '分位点%'],
        min: 0,
        max: 30
      },
      {
        metric: 'PB(不含商誉)统计值',
        selectors: ['10年', '分位点%'],
        min: 0,
        max: 30
      },
      {
        metric: '股息率',
        min: 2
      },
      {
        metric: '市值'
      },
      {
        metric: '上市日期',
        subCondition: '上市时间',
        max: '2015-01-01'
      }
    ],
    notes: [
      '百分比按页面输入习惯填写，例如 30 表示 30%。脚本会自动转换成 API 需要的小数 0.3。',
      '市值按“亿”填写，例如 100 表示 100 亿。脚本会自动转换成原始金额。',
      '更完整的可用条件请查看同目录下的 condition-catalog.cn.json。'
    ],
    catalogGeneratedAt: catalog.generatedAt
  };
}

async function main() {
  const username = process.env.LIXINGER_USERNAME;
  const password = process.env.LIXINGER_PASSWORD;

  if (!username || !password) {
    throw new Error('Missing LIXINGER_USERNAME or LIXINGER_PASSWORD');
  }

  const cookie = await login(username, password);
  const provinces = await fetchProvinces(cookie);
  const { browser, page } = await createPage(cookie);

  try {
    const metrics = [];

    for (const tabName of TAB_NAMES) {
      console.log(`TAB ${tabName}`);
      await clickTab(page, tabName);
      const titles = await extractVisibleFieldTitles(page);
      console.log(`FIELDS ${tabName} ${titles.length}`);

      for (const title of titles) {
        console.log(`  METRIC ${title}`);
        try {
          const rawEntry = await withTimeout(async () => {
            await addField(page, title);
            return extractCurrentRowInfo(page, tabName, title);
          }, 7000, `${tabName}/${title}/extract`);

          if (rawEntry) {
            metrics.push(finalizeMetricEntry(rawEntry));
          }
        } catch (error) {
          console.warn(`  SKIP ${title}: ${error.message}`);
        } finally {
          try {
            await withTimeout(() => deleteCurrentField(page), 3000, `${tabName}/${title}/delete`);
          } catch (error) {
            console.warn(`  RESET ${title}: ${error.message}`);
            await reloadBasePage(page);
            await clickTab(page, tabName);
          }
        }
      }
    }

    metrics.push({
      category: '自定义指标',
      metric: '自定义指标',
      displayLabelExample: '自定义指标',
      formulaIdExample: null,
      requestIdExample: null,
      requestIdTemplate: null,
      formulaIdTemplate: null,
      resultFieldKey: null,
      selectors: [],
      dateModes: [],
      subConditionOptions: [],
      thresholds: {
        min: { inputType: 'number', unit: null, scale: 1 },
        max: { inputType: 'number', unit: null, scale: 1 }
      },
      format: 'custom',
      unit: null,
      apiScale: 1,
      specialRequestId: null,
      notes: '需要页面内手工定义，当前目录不展开。'
    });

    const catalog = {
      generatedAt: new Date().toISOString(),
      page: 'company-fundamental',
      areaCode: DEFAULT_AREA_CODE,
      sourceUrl: DEFAULT_PAGE_URL,
      selectionRanges: SELECTION_RANGES.map(item => {
        if (item.key === 'province') {
          return {
            ...item,
            options: provinces.map(province => ({
              label: province.shortName,
              value: province.code
            }))
          };
        }
        return item;
      }),
      metrics
    };

    const template = buildSimpleInputTemplate(catalog);

    saveJson(DEFAULT_CATALOG_PATH, catalog);
    saveJson(DEFAULT_TEMPLATE_PATH, template);

    process.stdout.write(`${JSON.stringify({
      catalogPath: DEFAULT_CATALOG_PATH,
      templatePath: DEFAULT_TEMPLATE_PATH,
      metricCount: metrics.length,
      provinceCount: provinces.length
    }, null, 2)}\n`);
  } finally {
    await browser.close();
  }
}

main().catch(error => {
  console.error(error.stack || error.message);
  process.exit(1);
});
