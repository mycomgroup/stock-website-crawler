// main.js - Core logic for lixinger-screener skill
import { existsSync, mkdirSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { chromium } from 'playwright';
import {
  CHROME_USER_DATA_DIR,
  OUTPUT_ROOT,
  SESSION_FILE as SHARED_SESSION_FILE
} from '../load-env.js';
import {
  conditionCatalogExists,
  loadBrowserMetricsCatalog,
  loadConditionCatalog,
  loadJson,
  resolveCatalogPath
} from '../shared/catalog.js';
import { queryToUnifiedInput, validateUnifiedQuery } from '../shared/natural-language.js';
import {
  buildBrowserFiltersFromUnifiedInput,
  inputNeedsConditionCatalog,
  mergeUnifiedInputs,
  normalizeUnifiedInput
} from '../shared/unified-input.js';
import LoginHandler from '../../../stock-crawler/src/login-handler.js';

const CATALOG = loadBrowserMetricsCatalog();
const CONDITION_CATALOG_HINT_PATTERN = /统计值|分位点|上市日期|上市时间|上市年数|上市以来|10年|20年/;
const BROWSER_CATALOG_HINT_PATTERN = /市盈率\(TTM\)|市销率\(TTM\)|市现率\(TTM\)|股息率\(TTM\)|净资产收益率\(TTM\)|总资产收益率\(TTM\)|净利润率\(TTM\)|毛利率\(TTM\)|营业利润率\(TTM\)|营业收入\(TTM\)|净利润\(TTM\)|营业收入增长率\(YOY\)|净利润增长率\(YOY\)|营业收入增长率\(3年复合\)|净利润增长率\(3年复合\)|流动比率|速动比率|利息保障倍数|市值\/自由现金流/;

/**
 * Validates required environment variables.
 * @param {{ requireLlm?: boolean }} options
 * @returns {{ valid: boolean, missing: string[] }}
 */
export function validateEnv(options = {}) {
  const required = ['LIXINGER_USERNAME', 'LIXINGER_PASSWORD'];
  if (options.requireLlm) {
    required.push('LLM_API_KEY');
  }
  const missing = required.filter(v => !process.env[v]);
  return { valid: missing.length === 0, missing };
}

/**
 * Converts natural language query to ScreenerQuery using LLM.
 * @param {string} userQuery - Natural language query
 * @param {Array} catalog - metrics-catalog entries
 * @returns {Promise<{filters: Array<{field: string, operator: string, value: number|number[]}>}>}
 */
export async function queryToScreenerQuery(userQuery, catalog) {
  const parsed = await queryToUnifiedInput(userQuery, catalog);
  const queryResult = validateUnifiedQuery(parsed, catalog);
  if (!queryResult.valid) {
    throw new Error(queryResult.errors.join('\n'));
  }
  return { filters: buildBrowserFiltersFromUnifiedInput(parsed, { metrics: catalog }) };
}

/**
 * Validates that all fields in a ScreenerQuery exist in the catalog.
 * @param {{ filters: Array<{field: string, operator: string, value: any}> }} query
 * @param {Array<{displayName: string}>} catalog
 * @returns {{ valid: boolean, errors: string[] }}
 */
export function validateScreenerQuery(query, catalog) {
  const validNames = new Set(catalog.map(entry => entry.displayName));
  const errors = [];

  for (const filter of query.filters) {
    if (!validNames.has(filter.field)) {
      // Find similar fields: catalog entries whose displayName includes any word from the invalid field name
      const words = filter.field.split(/[\s()（）,，、\/]+/).filter(w => w.length > 0);
      const similar = catalog
        .filter(entry => words.some(word => entry.displayName.includes(word)))
        .map(entry => entry.displayName);

      if (similar.length > 0) {
        errors.push(`字段 "${filter.field}" 不在 metrics-catalog 中。相近字段：${similar.join('、')}`);
      } else {
        errors.push(`字段 "${filter.field}" 不在 metrics-catalog 中`);
      }
    }
  }

  return { valid: errors.length === 0, errors };
}

function loadInputFile(inputFile) {
  if (!inputFile) return {};
  return loadJson(inputFile);
}

function loadDefaultConditionCatalog(options) {
  const defaultCatalogPath = resolveCatalogPath(options.catalogPath, options.cwd);
  if (options.catalogPath || conditionCatalogExists(defaultCatalogPath)) {
    return loadConditionCatalog(defaultCatalogPath);
  }
  return null;
}

function loadRichCatalogIfNeeded(options, input) {
  if (!inputNeedsConditionCatalog(input)) {
    return null;
  }

  const catalogPath = resolveCatalogPath(options.catalogPath, options.cwd);
  return loadConditionCatalog(catalogPath);
}

export function buildBrowserQueryCatalogCandidates(userQuery, options = {}, richCatalog = null) {
  const queryText = String(userQuery || '');
  const defaultConditionCatalog = richCatalog || loadDefaultConditionCatalog(options);
  const browserCandidate = {
    name: 'browser-metrics-catalog',
    catalog: CATALOG,
    richCatalog: null
  };
  const conditionCandidate = defaultConditionCatalog
    ? {
        name: 'condition-catalog',
        catalog: defaultConditionCatalog.metrics,
        richCatalog: defaultConditionCatalog
      }
    : null;

  if (!conditionCandidate) {
    return [browserCandidate];
  }

  if (CONDITION_CATALOG_HINT_PATTERN.test(queryText) && !BROWSER_CATALOG_HINT_PATTERN.test(queryText)) {
    return [conditionCandidate, browserCandidate];
  }

  return [browserCandidate, conditionCandidate];
}

export async function parseBrowserNaturalLanguageQuery(
  userQuery,
  options = {},
  richCatalog = null,
  parseQuery = queryToUnifiedInput
) {
  const candidates = buildBrowserQueryCatalogCandidates(userQuery, options, richCatalog);
  const failures = [];

  for (const candidate of candidates) {
    try {
      const parsed = await parseQuery(userQuery, candidate.catalog);
      const validation = validateUnifiedQuery(parsed, candidate.catalog);
      if (validation.valid) {
        return {
          parsed,
          richCatalog: candidate.richCatalog
        };
      }

      failures.push(
        `${candidate.name}: ${validation.errors.join('；') || '校验失败'}`
      );
    } catch (error) {
      failures.push(`${candidate.name}: ${error.message}`);
    }
  }

  throw new Error(
    `无法解析筛选条件 "${userQuery}"。\n${failures.join('\n')}`
  );
}

async function resolveBrowserInput(options) {
  const inputFileData = loadInputFile(options.inputFile);
  let unifiedInput = normalizeUnifiedInput(inputFileData);
  let richCatalog = loadRichCatalogIfNeeded(options, unifiedInput);

  const naturalLanguageQueries = [inputFileData.query, options.query].filter(Boolean);

  if (naturalLanguageQueries.length > 0) {
    for (const userQuery of naturalLanguageQueries) {
      const resolved = await parseBrowserNaturalLanguageQuery(userQuery, options, richCatalog);
      if (resolved.richCatalog && !richCatalog) {
        richCatalog = resolved.richCatalog;
      }
      unifiedInput = mergeUnifiedInputs(unifiedInput, resolved.parsed);
    }
  }

  if (!unifiedInput.conditions?.length) {
    throw new Error('缺少筛选条件。请提供 --query 或 --input-file');
  }

  return {
    unifiedInput,
    richCatalog
  };
}

// Session management constants
const SESSION_FILE = SHARED_SESSION_FILE;
const SCREENER_URL = 'https://www.lixinger.com/analytics/screener/company-fundamental/cn';
const PAGE_TIMEOUT = 30_000;
const CHROME_USER_DATA = CHROME_USER_DATA_DIR;
const USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36';

function buildCookieHeader(setCookies) {
  return setCookies.map(value => value.split(';')[0]).join('; ');
}

function cookieHeaderToPlaywrightCookies(cookieHeader) {
  return cookieHeader
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
}

async function loginByRequest(username, password, refererUrl) {
  const response = await fetch('https://www.lixinger.com/api/account/sign-in/by-account', {
    method: 'POST',
    headers: {
      accept: 'application/json, text/plain, */*',
      'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
      'content-type': 'application/json;charset=UTF-8',
      referer: refererUrl,
      'user-agent': USER_AGENT
    },
    body: JSON.stringify({ accountName: username, password })
  });

  if (!response.ok) {
    const text = await response.text().catch(() => '');
    throw new Error(`登录接口失败 ${response.status}: ${text.slice(0, 500)}`);
  }

  const setCookies = response.headers.getSetCookie ? response.headers.getSetCookie() : [];
  const cookie = buildCookieHeader(setCookies);
  if (!cookie) {
    throw new Error('登录接口返回成功，但未返回 cookie');
  }
  return cookie;
}

async function waitForScreenerReady(page) {
  await page.waitForLoadState('networkidle', { timeout: PAGE_TIMEOUT }).catch(() => {});

  const readySelectors = [
    'li.field div.plus-btn[title]',
    'div.plus-btn[title]',
    'a.nav-link:has-text("基本指标")',
    'tr svg.fa-xmark'
  ];

  for (const selector of readySelectors) {
    const locator = page.locator(selector).first();
    if (await locator.count()) {
      await locator.waitFor({ state: 'visible', timeout: 8000 }).catch(() => {});
      if (await locator.isVisible().catch(() => false)) {
        return;
      }
    }
  }

  throw new Error('筛选页面未准备好：未找到字段列表或条件表格');
}

async function openScreenerPage(page, targetUrl) {
  await page.goto(targetUrl, { timeout: PAGE_TIMEOUT, waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(2000);
  await waitForScreenerReady(page);
}

/**
 * Validates login state by calling a lightweight API endpoint instead of
 * loading the full screener page. This avoids opening extra browser tabs
 * and avoids long timeouts when the page is slow to load.
 */
async function validateContext(context) {
  const page = await context.newPage();
  try {
    const response = await page.goto(
      'https://www.lixinger.com/api/user/info',
      { timeout: 10_000, waitUntil: 'domcontentloaded' }
    ).catch(() => null);
    if (!response) return false;
    const text = await page.evaluate(() => document.body?.innerText || '').catch(() => '');
    try {
      const json = JSON.parse(text);
      // Logged-in response has a user object; not-logged-in returns code 401 or empty data
      return json?.data?._id != null || json?.code === 1;
    } catch {
      return false;
    }
  } catch {
    return false;
  } finally {
    await page.close().catch(() => {});
  }
}

async function createAuthenticatedContext(browser, cookieHeader) {
  const context = await browser.newContext({
    locale: 'zh-CN',
    viewport: { width: 1600, height: 1400 },
    userAgent: USER_AGENT
  });
  await context.addCookies(cookieHeaderToPlaywrightCookies(cookieHeader));
  await context.storageState({ path: SESSION_FILE });
  return context;
}

/**
 * Loads existing session or creates a new one via login.
 * @param {import('playwright').Browser} browser
 * @param {{ targetUrl?: string, profileDir?: string, headless?: boolean }} options
 * @returns {Promise<import('playwright').BrowserContext>}
 */
export async function loadOrCreateSession(browser, options = {}) {
  const targetUrl = options.targetUrl || SCREENER_URL;

  // Try loading existing session from storage state
  if (existsSync(SESSION_FILE)) {
    const context = await browser.newContext({
      storageState: SESSION_FILE,
      locale: 'zh-CN',
      viewport: { width: 1600, height: 1400 },
      userAgent: USER_AGENT
    });
    if (await validateContext(context)) {
      console.log('✓ 使用已保存的浏览器会话');
      return context;
    }
    await context.close().catch(() => {});
    console.log('已保存的会话已失效，重新登录...');
  }

  // Try using a specified browser profile (only when explicitly provided via --profile-dir)
  if (options.profileDir) {
    try {
      console.log(`尝试使用浏览器 profile: ${options.profileDir}`);
      const context = await chromium.launchPersistentContext(options.profileDir, {
        viewport: null,
        userAgent: USER_AGENT,
        headless: false,
        channel: 'chrome'
      }).catch(() => chromium.launchPersistentContext(options.profileDir, {
        viewport: null,
        userAgent: USER_AGENT,
        headless: false
      }));

      if (await validateContext(context)) {
        console.log('✓ 使用指定浏览器 profile 成功，已登录状态');
        return context;
      }

      console.log('指定 profile 未保持登录，继续尝试自动登录...');
      await context.close().catch(() => {});
    } catch (err) {
      console.log('使用指定浏览器 profile 失败:', err.message);
    }
  }

  // Fallback 1: Login via request API and inject cookies
  const username = process.env.LIXINGER_USERNAME;
  const password = process.env.LIXINGER_PASSWORD;
  if (!username || !password) {
    throw new Error('LIXINGER_USERNAME 和 LIXINGER_PASSWORD 环境变量未配置');
  }

  try {
    console.log('尝试通过登录接口写入浏览器会话...');
    const cookieHeader = await loginByRequest(username, password, targetUrl);
    const context = await createAuthenticatedContext(browser, cookieHeader);
    console.log('✓ 已通过登录接口创建浏览器会话');
    return context;
  } catch (error) {
    console.log('登录接口方式失败，继续尝试 UI 自动登录:', error.message);
  }

  // Fallback 2: Fresh UI login with username/password
  console.log('尝试通过浏览器表单自动登录...');
  const context = await browser.newContext();
  const page = await context.newPage();
  const loginHandler = new LoginHandler();

  try {
    await page.goto(targetUrl, { timeout: PAGE_TIMEOUT, waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(2000);

    if (await loginHandler.needsLogin(page)) {
      const success = await loginHandler.login(page, { username, password });
      if (!success) {
        throw new Error('登录表单提交后仍未通过登录校验');
      }
    }

    await openScreenerPage(page, targetUrl);
    await context.storageState({ path: SESSION_FILE });
    console.log('✓ 已通过浏览器表单自动登录');
    await page.close().catch(() => {});
    return context;
  } catch (err) {
    await page.close().catch(() => {});
    await context.close().catch(() => {});
    throw new Error(`登录失败：${err.message}`);
  }
}

/**
 * Navigates to screener page and applies filters.
 * @param {import('playwright').Page} page
 * @param {Array<{
 *   field: string,
 *   category?: string|null,
 *   dateModeLabel?: string,
 *   dateModeApi?: string,
 *   subCondition?: string,
 *   operator: string,
 *   value: number|number[]
 * }>} filters
 * @param {{ targetUrl?: string }} options
 * @returns {Promise<void>}
 */
export async function applyFilters(page, filters, options = {}) {
  const targetUrl = options.targetUrl || SCREENER_URL;
  await openScreenerPage(page, targetUrl);

  const rowLocator = page.locator('tr').filter({ has: page.locator('svg.fa-xmark') });

  const clickTab = async tabName => {
    // Only click tabs that are inside the screener field panel, not site navigation
    const tab = page.locator(
      `.field-list a.nav-link:has-text("${tabName}"), ` +
      `.screener-field a.nav-link:has-text("${tabName}"), ` +
      `.condition-panel a.nav-link:has-text("${tabName}"), ` +
      `ul.nav-tabs a.nav-link:has-text("${tabName}"), ` +
      `.tab-content ~ ul a.nav-link:has-text("${tabName}")`
    ).first();
    // Fallback: find a nav-link that is near a plus-btn (i.e. inside the field panel)
    const fallback = page.locator(`a.nav-link:has-text("${tabName}")`).filter({
      has: page.locator('xpath=ancestor::*[.//div[@class and contains(@class,"plus-btn")]]')
    }).first();

    let target = null;
    if (await tab.count()) {
      target = tab;
    } else if (await fallback.count()) {
      target = fallback;
    } else {
      // Last resort: find any nav-link with this exact text that is visible
      const all = page.locator(`a.nav-link`);
      const count = await all.count();
      for (let i = 0; i < count; i++) {
        const el = all.nth(i);
        const text = (await el.textContent().catch(() => '')).trim();
        if (text === tabName && await el.isVisible().catch(() => false)) {
          target = el;
          break;
        }
      }
    }

    if (!target) return false;
    await target.click({ force: true });
    await page.waitForTimeout(800);
    return true;
  };

  // Only list tabs that are inside the screener field panel (contain plus-btn fields)
  const listTabNames = async () => {
    return page.evaluate(() => {
      // Find all nav-link elements
      const allLinks = [...document.querySelectorAll('a.nav-link')];
      // A screener tab is one whose ancestor contains li.field or div.plus-btn elements
      const screenerTabs = allLinks.filter(link => {
        let el = link.parentElement;
        // Walk up max 5 levels looking for a container that has plus-btn children
        for (let i = 0; i < 5; i++) {
          if (!el) break;
          if (el.querySelector('li.field, div.plus-btn[title]')) return true;
          el = el.parentElement;
        }
        return false;
      });
      // If we found screener-specific tabs, use those; otherwise fall back to all nav-links
      const source = screenerTabs.length > 0 ? screenerTabs : allLinks;
      return source
        .map(el => el.textContent?.trim() || '')
        .filter(Boolean);
    }).catch(() => []);
  };

  const extractVisibleFieldTitles = async () => page.evaluate(() => {
    const isVisible = element => {
      const style = window.getComputedStyle(element);
      return style.display !== 'none' && style.visibility !== 'hidden' && element.offsetParent !== null;
    };

    return [...document.querySelectorAll('li.field div.plus-btn[title], div.plus-btn[title]')]
      .filter(element => isVisible(element))
      .map(element => element.getAttribute('title'))
      .filter(Boolean);
  });

  const findFieldButton = async filter => {
    const triedTabs = [];
    const candidateTabs = [];
    if (filter.category) candidateTabs.push(filter.category);
    for (const tabName of await listTabNames()) {
      if (!candidateTabs.includes(tabName)) {
        candidateTabs.push(tabName);
      }
    }

    for (const tabName of candidateTabs) {
      triedTabs.push(tabName);
      await clickTab(tabName).catch(() => {});
      const locator = page.locator(`div.plus-btn[title="${filter.field}"]`).first();
      if (await locator.count()) {
        const visible = await locator.isVisible().catch(() => false);
        if (visible) {
          return locator;
        }
      }
    }

    const visibleTitles = await extractVisibleFieldTitles();
    throw new Error(
      `页面中找不到字段 "${filter.field}"` +
      `${filter.category ? `（期望分类：${filter.category}）` : ''}。` +
      `${triedTabs.length ? `已尝试分类：${triedTabs.join('、')}。` : ''}` +
      `${visibleTitles.length ? `当前可见字段示例：${visibleTitles.slice(0, 20).join('、')}` : ''}`
    );
  };

  const clearExistingRows = async () => {
    while (await rowLocator.count()) {
      await rowLocator.first().locator('svg.fa-xmark').click({ force: true }).catch(() => {});
      await page.waitForTimeout(300);
    }
  };

  const waitForNewRow = async previousCount => {
    for (let index = 0; index < 40; index += 1) {
      if (await rowLocator.count() > previousCount) {
        return rowLocator.nth(previousCount);
      }
      await page.waitForTimeout(250);
    }
    throw new Error('新增筛选条件后未出现新的条件行');
  };

  const selectByLabelOrValue = async (selectLocator, preferredLabel, preferredValue, description) => {
    const attempts = [];

    if (preferredLabel) {
      attempts.push({ label: preferredLabel });
    }
    if (preferredValue && preferredValue !== preferredLabel) {
      attempts.push({ value: preferredValue });
    }

    for (const option of attempts) {
      try {
        await selectLocator.selectOption(option);
        return true;
      } catch {
        // Try the next option shape.
      }
    }

    const available = await selectLocator.locator('option').evaluateAll(elements =>
      elements.map(element => ({
        label: element.textContent?.trim() || '',
        value: element.getAttribute('value') || ''
      }))
    ).catch(() => []);

    throw new Error(
      `${description} 不支持 "${preferredLabel || preferredValue}"。` +
      `${available.length ? `可选项：${available.map(item => item.label || item.value).join('、')}` : ''}`
    );
  };

  const applyRowDateMode = async (row, filter) => {
    if (!filter.dateModeLabel && !filter.dateModeApi) {
      return;
    }

    const dateCell = row.locator('td').nth(2);
    const select = dateCell.locator('select').first();
    if (await select.count()) {
      await selectByLabelOrValue(select, filter.dateModeLabel, filter.dateModeApi, `字段 "${filter.field}" 的日期模式`);
      await page.waitForTimeout(200);
      return;
    }

    const currentText = await dateCell.innerText().catch(() => '');
    const expected = filter.dateModeLabel || filter.dateModeApi;
    if (!currentText.includes(expected)) {
      throw new Error(`字段 "${filter.field}" 不支持设置日期模式 "${expected}"`);
    }
  };

  const applyRowSubCondition = async (row, filter) => {
    if (!filter.subCondition) {
      return;
    }

    const subConditionCell = row.locator('td').nth(3);
    const select = subConditionCell.locator('select').first();
    if (await select.count()) {
      await selectByLabelOrValue(select, filter.subCondition, null, `字段 "${filter.field}" 的子条件`);
      await page.waitForTimeout(200);
      return;
    }

    const label = subConditionCell.locator('label').filter({ hasText: filter.subCondition }).first();
    if (await label.count()) {
      await label.click({ force: true }).catch(async () => {
        const inputId = await label.getAttribute('for');
        if (inputId) {
          await subConditionCell.locator(`#${inputId}`).click({ force: true });
        } else {
          throw new Error(`字段 "${filter.field}" 的子条件 "${filter.subCondition}" 无法点击`);
        }
      });
      await page.waitForTimeout(200);
      return;
    }

    const currentText = await subConditionCell.innerText().catch(() => '');
    if (!currentText.includes(filter.subCondition)) {
      throw new Error(`字段 "${filter.field}" 不支持子条件 "${filter.subCondition}"`);
    }
  };

  const fillRowValues = async (row, filter) => {
    const inputs = row.locator('input');
    const inputCount = await inputs.count();
    if (!inputCount) {
      throw new Error(`字段 "${filter.field}" 的条件行中未找到输入框`);
    }

    const fillInput = async (index, value) => {
      if (index >= inputCount) return;
      await inputs.nth(index).fill(value == null ? '' : String(value), { timeout: PAGE_TIMEOUT });
    };

    if (filter.operator === '介于' && Array.isArray(filter.value)) {
      await fillInput(0, filter.value[0]);
      await fillInput(1, filter.value[1]);
      return;
    }

    if (filter.operator === '大于') {
      await fillInput(0, filter.value);
      if (inputCount > 1) await fillInput(1, '');
      return;
    }

    if (filter.operator === '小于') {
      if (inputCount > 1) {
        await fillInput(0, '');
        await fillInput(1, filter.value);
      } else {
        await fillInput(0, filter.value);
      }
      return;
    }

    throw new Error(`不支持的操作符：${filter.operator}`);
  };

  await clearExistingRows();

  for (const filter of filters) {
    try {
      const countBefore = await rowLocator.count();
      const fieldButton = await findFieldButton(filter);
      await fieldButton.click({ force: true });
      await page.waitForTimeout(500);
      const row = await waitForNewRow(countBefore);
      await applyRowDateMode(row, filter);
      await applyRowSubCondition(row, filter);
      await fillRowValues(row, filter);
      await page.waitForTimeout(300);
    } catch (err) {
      if (err.message.includes('页面中找不到字段')) {
        throw err;
      }
      if (err.name === 'TimeoutError' || err.message.toLowerCase().includes('timeout')) {
        throw new Error(`页面操作超时（${PAGE_TIMEOUT / 1000} 秒）：${err.message}`);
      }
      throw err;
    }
  }

  const runButtonSelectors = [
    'button:has-text("开始筛选")',
    'button:has-text("筛选")',
    'button:has-text("查询")',
    'button:has-text("查看结果")'
  ];

  for (const selector of runButtonSelectors) {
    const button = page.locator(selector).first();
    if (await button.count()) {
      const visible = await button.isVisible().catch(() => false);
      if (visible) {
        await button.click({ force: true }).catch(() => {});
        await page.waitForTimeout(1500);
        await page.waitForLoadState('networkidle', { timeout: PAGE_TIMEOUT }).catch(() => {});
        break;
      }
    }
  }
}

/**
 * Merges multiple pages of table rows into a single array.
 * @param {Array<Array<Object>>} pages - Array of page data arrays
 * @returns {Array<Object>} - Merged rows
 */
export function mergePages(pages) {
  return pages.flat();
}

/**
 * Scrapes all pages of results from the screener table.
 * @param {import('playwright').Page} page
 * @returns {Promise<Array<{[columnName: string]: string}>>}
 */
export async function scrapeAllPages(page) {
  // Wait for the results table to appear
  try {
    await page.waitForSelector(
      'table, [class*="table"], [class*="list-table"], [class*="result"]',
      { timeout: PAGE_TIMEOUT }
    );
  } catch {
    // Table may not appear if no results; return empty
    return [];
  }

  const pages = [];

  // eslint-disable-next-line no-constant-condition
  while (true) {
    // Extract table data from current page
    const rows = await page.evaluate(() => {
      // Try standard <table> first
      const table = document.querySelector('table');
      if (table) {
        const headers = [];
        const headerCells = table.querySelectorAll('thead th, thead td, tr:first-child th');
        headerCells.forEach(cell => headers.push(cell.innerText.trim()));

        if (headers.length === 0) return [];

        const dataRows = [];
        const bodyRows = table.querySelectorAll('tbody tr');
        bodyRows.forEach(row => {
          const cells = row.querySelectorAll('td');
          if (cells.length === 0) return;
          const obj = {};
          cells.forEach((cell, i) => {
            const key = headers[i] ?? `col${i}`;
            obj[key] = cell.innerText.trim();
          });
          dataRows.push(obj);
        });
        return dataRows;
      }

      // Fallback: look for class-based table structures
      const tableEl =
        document.querySelector('[class*="table"]') ||
        document.querySelector('[class*="list"]');
      if (!tableEl) return [];

      const headerCells = tableEl.querySelectorAll('[class*="header"] [class*="cell"], [class*="th"], th');
      const headers = [];
      headerCells.forEach(cell => headers.push(cell.innerText.trim()));

      if (headers.length === 0) return [];

      const dataRows = [];
      const rowEls = tableEl.querySelectorAll('[class*="row"]:not([class*="header"])');
      rowEls.forEach(row => {
        const cells = row.querySelectorAll('[class*="cell"], td');
        if (cells.length === 0) return;
        const obj = {};
        cells.forEach((cell, i) => {
          const key = headers[i] ?? `col${i}`;
          obj[key] = cell.innerText.trim();
        });
        dataRows.push(obj);
      });
      return dataRows;
    });

    pages.push(rows);

    // Check for a "下一页" (next page) button that is not disabled
    const nextBtn = page.locator(
      'button:has-text("下一页"), [class*="next"]:has-text("下一页"), [class*="pagination"] [class*="next"], li[class*="next"] a'
    ).first();

    let hasNext = false;
    try {
      const visible = await nextBtn.isVisible({ timeout: 2000 });
      if (visible) {
        const disabled = await nextBtn.isDisabled({ timeout: 2000 });
        const ariaDisabled = await nextBtn.getAttribute('aria-disabled').catch(() => null);
        const classAttr = await nextBtn.getAttribute('class').catch(() => '');
        hasNext = !disabled && ariaDisabled !== 'true' && !classAttr.includes('disabled');
      }
    } catch {
      hasNext = false;
    }

    if (!hasNext) break;

    await nextBtn.click({ timeout: PAGE_TIMEOUT });
    // Wait for the table to refresh after page navigation
    await page.waitForTimeout(1000);
    try {
      await page.waitForLoadState('networkidle', { timeout: PAGE_TIMEOUT });
    } catch {
      // networkidle may not fire; continue
    }
  }

  return mergePages(pages);
}

/**
 * Applies a limit to the rows array.
 * @param {Array<Object>} rows
 * @param {number|null|undefined} limit - positive integer or null/undefined for no limit
 * @returns {Array<Object>}
 */
export function applyLimit(rows, limit) {
  if (typeof limit === 'number' && Number.isInteger(limit) && limit > 0) {
    return rows.slice(0, limit);
  }
  return rows;
}

/**
 * Escapes a single cell value per RFC 4180.
 * @param {string} value
 * @returns {string}
 */
function escapeCsvValue(value) {
  const str = String(value ?? '');
  if (str.includes(',') || str.includes('"') || str.includes('\n') || str.includes('\r')) {
    return '"' + str.replace(/"/g, '""') + '"';
  }
  return str;
}

/**
 * Formats table rows as CSV string (RFC 4180).
 * @param {Array<{[key: string]: string}>} rows
 * @returns {string}
 */
export function formatCsv(rows) {
  if (!rows || rows.length === 0) return '';

  const headers = Object.keys(rows[0]);
  const lines = [
    headers.map(escapeCsvValue).join(','),
    ...rows.map(row => headers.map(h => escapeCsvValue(row[h])).join(',')),
  ];
  return lines.join('\n');
}

/**
 * Writes CSV content to output/screener-{timestamp}.csv
 * @param {string} csvContent
 * @returns {string} - full file path
 */
export function writeCsvFile(csvContent) {
  const outputDir = OUTPUT_ROOT;
  mkdirSync(outputDir, { recursive: true });
  const filename = `screener-${Date.now()}.csv`;
  const filePath = join(outputDir, filename);
  writeFileSync(filePath, csvContent, 'utf8');
  console.log(filePath);
  return filePath;
}

/**
 * Main orchestration function.
 * @param {{ query?: string, inputFile?: string, catalogPath?: string, cwd?: string, headless?: boolean, limit?: number }} options
 * @returns {Promise<string>} - path to the output CSV file
 */
export async function main(options) {
  const needsLlm = Boolean(options.query || options.inputFile);
  const envResult = validateEnv({ requireLlm: needsLlm && Boolean(options.query) });
  if (!envResult.valid) {
    throw new Error(`缺少必要的环境变量：${envResult.missing.join('、')}`);
  }
  const { unifiedInput, richCatalog } = await resolveBrowserInput(options);
  const targetUrl = options.url || unifiedInput.url || SCREENER_URL;
  const screenerQuery = {
    filters: buildBrowserFiltersFromUnifiedInput(unifiedInput, richCatalog)
  };

  // Phase 2: Playwright browser automation
  const browser = await chromium.launch({ headless: options.headless ?? true });
  let context = null;
  let rows;
  try {
    context = await loadOrCreateSession(browser, {
      targetUrl,
      profileDir: options.profileDir,
      headless: options.headless
    });
    const page = await context.newPage();
    await applyFilters(page, screenerQuery.filters, { targetUrl });
    rows = await scrapeAllPages(page);
    await page.close().catch(() => {});
  } finally {
    await context?.close().catch(() => {});
    await browser.close().catch(() => {});
  }

  // Phase 3: CSV output
  const limitedRows = applyLimit(rows, options.limit);
  const csvContent = formatCsv(limitedRows);
  const filePath = writeCsvFile(csvContent);

  return filePath;
}
