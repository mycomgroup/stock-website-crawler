import fs from 'node:fs';
import path from 'node:path';
import { chromium } from 'playwright';
import { SESSION_FILE } from '../paths.js';
import { loadJson } from '../request/joinquant-strategy-client.js';

export const LIST_URL = 'https://www.joinquant.com/algorithm/index/list';
export const NEW_STOCK_STRATEGY_URL =
  'https://www.joinquant.com/algorithm/index/new?restore=0&type=stock&baseCapital=100000';

function ensureSessionCookies() {
  const sessionPayload = loadJson(SESSION_FILE);
  if (!sessionPayload.cookies || sessionPayload.cookies.length === 0) {
    throw new Error(`No cookies found in session file: ${SESSION_FILE}`);
  }
  return sessionPayload.cookies;
}

async function writeDebugArtifacts(page, runDir, debugPrefix, suffix) {
  if (!runDir || !debugPrefix) return {};

  const htmlFile = path.join(runDir, `${debugPrefix}_${suffix}.html`);
  fs.writeFileSync(htmlFile, await page.content(), 'utf8');

  const pngFile = path.join(runDir, `${debugPrefix}_${suffix}.png`);
  await page.screenshot({ path: pngFile, fullPage: true }).catch(() => {});

  return { htmlFile, pngFile };
}

export async function launchBrowserWithSession(options = {}) {
  const {
    headed = false,
    browserArgs,
    contextOptions
  } = options;

  const cookies = ensureSessionCookies();
  const browser = await chromium.launch({
    headless: !headed,
    ...(browserArgs ? { args: browserArgs } : {})
  });
  const context = await browser.newContext(contextOptions);
  await context.addCookies(cookies);
  const page = await context.newPage();
  return { browser, context, page };
}

export async function clickFirstVisible(page, selectors, timeout = 5000) {
  for (const selector of selectors) {
    const locator = page.locator(selector).first();
    try {
      if (await locator.count()) {
        await locator.click({ timeout });
        return selector;
      }
    } catch {
      // Try the next selector.
    }
  }
  return null;
}

export async function createNewStockStrategy(options = {}) {
  const {
    page,
    browserContext,
    runDir,
    debugPrefix,
    fallbackToList = true
  } = options;

  await page.goto(NEW_STOCK_STRATEGY_URL, {
    waitUntil: 'domcontentloaded',
    timeout: 30000
  });
  await page.waitForLoadState('networkidle', { timeout: 30000 }).catch(() => {});

  if (page.url().includes('/login/')) {
    throw new Error('JoinQuant session is not logged in when opening new stock strategy page');
  }

  let targetPage = page;
  let clickedSelector = 'direct:new_stock_strategy_url';
  let match = targetPage.url().match(/algorithmId=([^&]+)/);

  if (!match && fallbackToList) {
    await page.goto(LIST_URL, { waitUntil: 'domcontentloaded', timeout: 30000 });
    await page.waitForLoadState('networkidle', { timeout: 30000 }).catch(() => {});

    const popupPromise = browserContext
      ? browserContext.waitForEvent('page', { timeout: 3000 }).catch(() => null)
      : Promise.resolve(null);
    const openDropdown = await clickFirstVisible(page, [
      '#new-algo-button',
      'button:has-text("新建策略")',
      'a:has-text("新建策略")',
      'text=新建策略'
    ]);

    if (!openDropdown) {
      const { htmlFile } = await writeDebugArtifacts(page, runDir, debugPrefix, 'list_page');
      const suffix = htmlFile ? ` Debug saved to ${htmlFile}` : '';
      throw new Error(`Unable to find "新建策略" dropdown on list page.${suffix}`);
    }

    const stockLink = page
      .locator('#tacticsList a[href*="/algorithm/index/new?"][href*="type=stock"]')
      .first();
    await stockLink.waitFor({ state: 'visible', timeout: 10000 });
    await stockLink.click({ timeout: 10000 });

    const popup = await popupPromise;
    targetPage = popup || page;
    clickedSelector = 'fallback:#tacticsList stock link';
    await targetPage.waitForLoadState('domcontentloaded', { timeout: 30000 });
    await targetPage.waitForLoadState('networkidle', { timeout: 30000 }).catch(() => {});
    match = targetPage.url().match(/algorithmId=([^&]+)/);
  }

  if (!match) {
    const { htmlFile } = await writeDebugArtifacts(targetPage, runDir, debugPrefix, 'edit_page');
    const suffix = htmlFile ? ` Debug saved to ${htmlFile}` : '';
    throw new Error(`Failed to parse algorithmId from URL: ${targetPage.url()}.${suffix}`);
  }

  return {
    algorithmId: match[1],
    targetPage,
    clickedSelector
  };
}
