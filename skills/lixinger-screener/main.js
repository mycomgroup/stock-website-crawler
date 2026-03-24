// main.js - Core logic for lixinger-screener skill
import { readFileSync, existsSync, mkdirSync, writeFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import OpenAI from 'openai';
import { chromium } from 'playwright';

const __dirname = dirname(fileURLToPath(import.meta.url));

const CATALOG = JSON.parse(readFileSync(join(__dirname, 'metrics-catalog.json'), 'utf8'));

/**
 * Validates required environment variables.
 * @returns {{ valid: boolean, missing: string[] }}
 */
export function validateEnv() {
  const required = ['LLM_API_KEY', 'LIXINGER_USERNAME', 'LIXINGER_PASSWORD'];
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
  const apiKey = process.env.LLM_API_KEY;
  const baseURL = process.env.LLM_BASE_URL || undefined;
  const model = process.env.LLM_MODEL || 'gpt-4o';

  const client = new OpenAI({ apiKey, ...(baseURL ? { baseURL } : {}) });

  const systemPrompt = `你是一个股票筛选条件解析助手。用户会用自然语言描述筛选条件，你需要将其转换为结构化的 JSON 对象。

可用的筛选指标（metrics-catalog）如下：
${JSON.stringify(catalog, null, 2)}

请将用户的筛选条件转换为以下格式的 JSON 对象，只返回 JSON，不要有任何其他文字：
{
  "filters": [
    { "field": "<displayName from catalog>", "operator": "<大于|小于|介于>", "value": <number or [min, max]> }
  ]
}

规则：
- field 必须使用 metrics-catalog 中的 displayName 字段值
- operator 只能是 "大于"、"小于" 或 "介于"
- value 为数字；当 operator 为 "介于" 时，value 为 [最小值, 最大值] 数组
- 只返回 JSON，不要有 markdown 代码块或其他说明文字`;

  let responseText;
  try {
    const completion = await client.chat.completions.create({
      model,
      messages: [
        { role: 'system', content: systemPrompt },
        { role: 'user', content: userQuery },
      ],
      temperature: 0,
    });
    responseText = completion.choices[0]?.message?.content?.trim() ?? '';
  } catch (err) {
    const examples = catalog.slice(0, 3).map(e => e.displayName).join('、');
    throw new Error(`LLM 请求失败：${err.message}。可用指标示例：${examples}`);
  }

  // Strip markdown code fences if present
  const cleaned = responseText.replace(/^```(?:json)?\s*/i, '').replace(/\s*```$/, '').trim();

  let parsed;
  try {
    parsed = JSON.parse(cleaned);
  } catch {
    const examples = catalog.slice(0, 3).map(e => e.displayName).join('、');
    throw new Error(
      `LLM 返回的内容无法解析为 JSON。\n原始内容：${responseText}\n可用指标示例：${examples}`
    );
  }

  if (!parsed || !Array.isArray(parsed.filters)) {
    const examples = catalog.slice(0, 3).map(e => e.displayName).join('、');
    throw new Error(
      `LLM 返回的 JSON 格式不正确，缺少 filters 数组。可用指标示例：${examples}`
    );
  }

  return parsed;
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

// Session management constants
const SESSION_FILE = join(__dirname, '.session.json');
const LIXINGER_URL = 'https://www.lixinger.com';
const LOGIN_URL = 'https://www.lixinger.com/login';
const SCREENER_URL = 'https://www.lixinger.com/analytics/screener/company-fundamental/cn';
const PAGE_TIMEOUT = 30_000;

/**
 * Loads existing session or creates a new one via login.
 * @param {import('playwright').Browser} browser
 * @returns {Promise<import('playwright').BrowserContext>}
 */
export async function loadOrCreateSession(browser) {
  // Try loading existing session
  if (existsSync(SESSION_FILE)) {
    const context = await browser.newContext({ storageState: SESSION_FILE });
    const page = await context.newPage();
    try {
      await page.goto(SCREENER_URL, { timeout: PAGE_TIMEOUT, waitUntil: 'domcontentloaded' });
      const url = page.url();
      if (!url.includes('/login')) {
        // Session is still valid
        await page.close();
        return context;
      }
    } catch {
      // Navigation failed; fall through to re-login
    } finally {
      await page.close();
    }
    // Session invalid — close and re-login
    await context.close();
  }

  // Fresh login
  const username = process.env.LIXINGER_USERNAME;
  const password = process.env.LIXINGER_PASSWORD;
  if (!username || !password) {
    throw new Error('LIXINGER_USERNAME 和 LIXINGER_PASSWORD 环境变量未配置');
  }

  const context = await browser.newContext();
  const page = await context.newPage();

  try {
    await page.goto(LOGIN_URL, { timeout: PAGE_TIMEOUT, waitUntil: 'domcontentloaded' });

    // Fill credentials — lixinger login form uses phone/email + password inputs
    await page.fill('input[type="text"], input[type="email"], input[type="tel"]', username, { timeout: PAGE_TIMEOUT });
    await page.fill('input[type="password"]', password, { timeout: PAGE_TIMEOUT });
    await page.click('button[type="submit"]', { timeout: PAGE_TIMEOUT });

    // Wait for navigation away from login page
    await page.waitForURL(url => !url.includes('/login'), { timeout: PAGE_TIMEOUT });

    const finalUrl = page.url();
    if (finalUrl.includes('/login')) {
      throw new Error('登录失败：登录后仍停留在登录页面，请检查账号密码');
    }
  } catch (err) {
    await page.close();
    await context.close();
    throw new Error(`登录失败：${err.message}`);
  }

  await page.close();

  // Persist session
  await context.storageState({ path: SESSION_FILE });

  return context;
}

/**
 * Navigates to screener page and applies filters.
 * @param {import('playwright').Page} page
 * @param {Array<{field: string, operator: string, value: number|number[]}>} filters
 * @returns {Promise<void>}
 */
export async function applyFilters(page, filters) {
  // Navigate to screener page
  await page.goto(SCREENER_URL, { timeout: PAGE_TIMEOUT, waitUntil: 'domcontentloaded' });

  // Wait for the page to be interactive
  await page.waitForLoadState('networkidle', { timeout: PAGE_TIMEOUT }).catch(() => {
    // networkidle may not fire on SPA pages; continue anyway
  });

  // Clear existing filters: look for "清除" / "重置" / "清空" button or close tags on existing conditions
  try {
    const clearBtn = page.locator(
      'button:has-text("清除"), button:has-text("重置"), button:has-text("清空条件"), [class*="clear"]:has-text("清")'
    ).first();
    if (await clearBtn.isVisible({ timeout: 3000 })) {
      await clearBtn.click({ timeout: PAGE_TIMEOUT });
      await page.waitForTimeout(500);
    }
  } catch {
    // No clear button found; proceed
  }

  // Remove any existing filter tags (×/close buttons on condition chips)
  try {
    const closeBtns = page.locator('[class*="tag"] [class*="close"], [class*="filter"] [class*="remove"], [class*="condition"] [class*="delete"]');
    const count = await closeBtns.count();
    for (let i = count - 1; i >= 0; i--) {
      await closeBtns.nth(i).click({ timeout: 5000 }).catch(() => {});
      await page.waitForTimeout(200);
    }
  } catch {
    // Ignore errors when removing existing tags
  }

  // Apply each filter in sequence
  for (const filter of filters) {
    try {
      // Step 1: Click "添加条件" button to open the metric selector
      const addBtn = page.locator(
        'button:has-text("添加条件"), button:has-text("添加筛选"), button:has-text("添加指标"), [class*="add"]:has-text("添加")'
      ).first();
      await addBtn.waitFor({ state: 'visible', timeout: PAGE_TIMEOUT });
      await addBtn.click({ timeout: PAGE_TIMEOUT });
      await page.waitForTimeout(300);

      // Step 2: Find and click the field by its displayName
      // Try direct text match first, then search input
      const fieldLocator = page.locator(
        `[class*="metric"]:has-text("${filter.field}"), [class*="indicator"]:has-text("${filter.field}"), [class*="item"]:has-text("${filter.field}")`
      ).first();

      let fieldFound = false;
      try {
        await fieldLocator.waitFor({ state: 'visible', timeout: 5000 });
        fieldFound = true;
      } catch {
        // Try searching via an input box in the selector panel
        const searchInput = page.locator(
          '[class*="search"] input, [placeholder*="搜索"], [placeholder*="查找"]'
        ).first();
        if (await searchInput.isVisible({ timeout: 3000 })) {
          await searchInput.fill(filter.field, { timeout: PAGE_TIMEOUT });
          await page.waitForTimeout(300);
          try {
            await fieldLocator.waitFor({ state: 'visible', timeout: 5000 });
            fieldFound = true;
          } catch {
            // Still not found after search
          }
        }
      }

      if (!fieldFound) {
        // Close the selector panel if open
        await page.keyboard.press('Escape').catch(() => {});
        throw new Error(`页面中找不到字段 "${filter.field}"，请检查 metrics-catalog.json`);
      }

      await fieldLocator.click({ timeout: PAGE_TIMEOUT });
      await page.waitForTimeout(300);

      // Step 3: Set the operator
      // Look for operator selector (大于/小于/介于 dropdown or radio buttons)
      const operatorLocator = page.locator(
        `[class*="operator"] :has-text("${filter.operator}"), [class*="select"] :has-text("${filter.operator}"), button:has-text("${filter.operator}")`
      ).first();

      try {
        await operatorLocator.waitFor({ state: 'visible', timeout: PAGE_TIMEOUT });
        await operatorLocator.click({ timeout: PAGE_TIMEOUT });
        await page.waitForTimeout(200);
      } catch {
        // Operator selector may already default to the right value; continue
      }

      // Step 4: Enter the value(s)
      if (filter.operator === '介于' && Array.isArray(filter.value)) {
        // Two inputs: min and max
        const inputs = page.locator('[class*="value"] input, [class*="filter"] input[type="number"], [class*="condition"] input');
        const inputCount = await inputs.count();
        if (inputCount >= 2) {
          await inputs.nth(0).fill(String(filter.value[0]), { timeout: PAGE_TIMEOUT });
          await inputs.nth(1).fill(String(filter.value[1]), { timeout: PAGE_TIMEOUT });
        } else if (inputCount === 1) {
          await inputs.nth(0).fill(String(filter.value[0]), { timeout: PAGE_TIMEOUT });
        }
      } else {
        const valueInput = page.locator(
          '[class*="value"] input, [class*="filter"] input[type="number"], [class*="condition"] input'
        ).first();
        await valueInput.waitFor({ state: 'visible', timeout: PAGE_TIMEOUT });
        await valueInput.fill(String(filter.value), { timeout: PAGE_TIMEOUT });
      }

      await page.waitForTimeout(200);

      // Step 5: Confirm / apply the filter (look for 确定/确认/应用 button)
      const confirmBtn = page.locator(
        'button:has-text("确定"), button:has-text("确认"), button:has-text("应用"), button:has-text("添加")'
      ).last();
      try {
        if (await confirmBtn.isVisible({ timeout: 3000 })) {
          await confirmBtn.click({ timeout: PAGE_TIMEOUT });
          await page.waitForTimeout(300);
        }
      } catch {
        // No confirm button; filter may apply automatically
      }
    } catch (err) {
      if (err.message.includes('找不到字段')) {
        throw err;
      }
      if (err.name === 'TimeoutError' || err.message.toLowerCase().includes('timeout')) {
        throw new Error(`页面操作超时（${PAGE_TIMEOUT / 1000} 秒）：${err.message}`);
      }
      throw err;
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
  const outputDir = join(__dirname, '..', '..', 'output');
  mkdirSync(outputDir, { recursive: true });
  const filename = `screener-${Date.now()}.csv`;
  const filePath = join(outputDir, filename);
  writeFileSync(filePath, csvContent, 'utf8');
  console.log(filePath);
  return filePath;
}

/**
 * Main orchestration function.
 * @param {{ query: string, headless?: boolean, limit?: number }} options
 * @returns {Promise<string>} - path to the output CSV file
 */
export async function main(options) {
  const catalog = CATALOG;

  // Phase 1: Validate environment
  const envResult = validateEnv();
  if (!envResult.valid) {
    throw new Error(`缺少必要的环境变量：${envResult.missing.join('、')}`);
  }

  // Phase 1: LLM conversion
  const screenerQuery = await queryToScreenerQuery(options.query, catalog);

  // Phase 1: Validate screener query fields
  const queryResult = validateScreenerQuery(screenerQuery, catalog);
  if (!queryResult.valid) {
    throw new Error(queryResult.errors.join('\n'));
  }

  // Phase 2: Playwright browser automation
  const browser = await chromium.launch({ headless: options.headless ?? true });
  let rows;
  try {
    const context = await loadOrCreateSession(browser);
    const page = await context.newPage();
    await applyFilters(page, screenerQuery.filters);
    rows = await scrapeAllPages(page);
  } finally {
    await browser.close();
  }

  // Phase 3: CSV output
  const limitedRows = applyLimit(rows, options.limit);
  const csvContent = formatCsv(limitedRows);
  const filePath = writeCsvFile(csvContent);

  return filePath;
}
