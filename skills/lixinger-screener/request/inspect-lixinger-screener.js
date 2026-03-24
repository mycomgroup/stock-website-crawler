import fs from 'fs';
import path from 'path';
import { chromium } from 'playwright';
import '../load-env.js';
import { LIXINGER_OUTPUT_DIR } from '../paths.js';
import LoginHandler from '../../../stock-crawler/src/login-handler.js';

const DEFAULT_URL = 'https://www.lixinger.com/analytics/screener/company-fundamental/cn?screener-id=587c4d21d6e94ed9d447b29d';
const OUTPUT_DIR = LIXINGER_OUTPUT_DIR;
const OUTPUT_FILE = path.join(OUTPUT_DIR, 'network-capture.json');
const STORAGE_STATE_FILE = '/tmp/lixinger-latest-storage-state.json';

function ensureDir(dir) {
  fs.mkdirSync(dir, { recursive: true });
}

function sanitizeHeaders(headers = {}) {
  const redacted = {};
  for (const [key, value] of Object.entries(headers)) {
    if (/cookie|authorization|token/i.test(key)) {
      redacted[key] = '<redacted>';
    } else {
      redacted[key] = value;
    }
  }
  return redacted;
}

function bodyPreview(body) {
  if (body == null) return null;
  const text = typeof body === 'string' ? body : JSON.stringify(body);
  if (text.length <= 4000) return text;
  return `${text.slice(0, 4000)}...<truncated>`;
}

function sanitizePostData(url, postData) {
  if (!postData) return null;
  if (url.includes('/api/account/sign-in/by-account')) {
    return '{"accountName":"<redacted>","password":"<redacted>"}';
  }
  return bodyPreview(postData);
}

function shouldRedactBody(url) {
  return [
    '/api/account/',
    '/api/user/',
    '/api/site/notifications/',
    '/api/ugd/settings-groups',
    '/api/stock/stocks/stock-collections'
  ].some(pattern => url.includes(pattern));
}

function sanitizeResponseBody(url, body) {
  if (!body) return null;
  if (shouldRedactBody(url)) {
    return '<redacted>';
  }
  return bodyPreview(body);
}

async function tryClick(page, selectors) {
  for (const selector of selectors) {
    const locator = page.locator(selector).first();
    if (await locator.count()) {
      await locator.click().catch(() => {});
      await page.waitForTimeout(1000);
      return true;
    }
  }
  return false;
}

async function ensureLoggedIn(page, username, password) {
  const loginHandler = new LoginHandler();

  await page.waitForTimeout(2000);

  if (!(await loginHandler.needsLogin(page))) {
    await tryClick(page, [
      'button:has-text("登录")',
      'a:has-text("登录")',
      'button:has-text("Sign in")',
      'a:has-text("Sign in")'
    ]);
    await page.waitForTimeout(1000);
  }

  await tryClick(page, [
    'text=密码登录',
    'text=账号密码登录',
    'text=手机密码登录',
    '[role="tab"]:has-text("密码")',
    'button:has-text("密码登录")'
  ]);

  if (!(await loginHandler.needsLogin(page))) {
    return true;
  }

  const success = await loginHandler.login(page, { username, password });
  await page.waitForTimeout(4000);
  return success;
}

function shouldTrack(url, resourceType) {
  if (resourceType === 'xhr' || resourceType === 'fetch') return true;
  return /lixinger\.com|resource\.lixinger\.com/.test(url) &&
    /(api|analytics|screener|company|fundamental|search|query)/i.test(url);
}

async function main() {
  const username = process.env.LIXINGER_USERNAME;
  const password = process.env.LIXINGER_PASSWORD;
  const targetUrl = process.env.LIXINGER_URL || DEFAULT_URL;
  const saveStorageState = process.env.LIXINGER_SAVE_STORAGE_STATE === '1';

  if (!username || !password) {
    throw new Error('Missing LIXINGER_USERNAME or LIXINGER_PASSWORD');
  }

  ensureDir(OUTPUT_DIR);

  const browser = await chromium.launch({
    headless: true,
    channel: 'chrome',
    args: [
      '--disable-blink-features=AutomationControlled',
      '--disable-features=IsolateOrigins,site-per-process',
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
    viewport: { width: 1440, height: 900 },
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    extraHTTPHeaders: {
      'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
    }
  });

  await context.addInitScript(() => {
    Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
    Object.defineProperty(navigator, 'languages', { get: () => ['zh-CN', 'zh', 'en-US', 'en'] });
    Object.defineProperty(navigator, 'plugins', {
      get: () => [{ name: 'Chrome PDF Plugin' }, { name: 'Chrome PDF Viewer' }]
    });
  });

  const page = await context.newPage();
  const captures = [];
  const pending = new Map();
  let counter = 0;

  page.on('request', request => {
    const resourceType = request.resourceType();
    const url = request.url();
    if (!shouldTrack(url, resourceType)) return;

    const id = ++counter;
    const record = {
      id,
      phase: 'request',
      resourceType,
      method: request.method(),
      url,
      headers: sanitizeHeaders(request.headers()),
      postData: sanitizePostData(url, request.postData())
    };
    pending.set(request, record);
    captures.push(record);
  });

  page.on('response', async response => {
    const request = response.request();
    const resourceType = request.resourceType();
    const url = response.url();
    if (!shouldTrack(url, resourceType)) return;

    const contentType = response.headers()['content-type'] || '';
    let preview = null;
    if (/json|text|javascript/.test(contentType)) {
      preview = sanitizeResponseBody(url, await response.text().catch(() => null));
    }

    const existing = pending.get(request);
    captures.push({
      id: existing?.id ?? ++counter,
      phase: 'response',
      resourceType,
      method: request.method(),
      url,
      status: response.status(),
      headers: sanitizeHeaders(response.headers()),
      contentType,
      body: preview
    });
  });

  let loginSuccess = false;
  let currentUrl = '';

  try {
    await page.goto(targetUrl, { waitUntil: 'domcontentloaded', timeout: 45000 });
    loginSuccess = await ensureLoggedIn(page, username, password);

    await page.goto(targetUrl, { waitUntil: 'domcontentloaded', timeout: 45000 });
    await page.waitForLoadState('networkidle', { timeout: 15000 }).catch(() => {});
    await page.waitForTimeout(5000);

    currentUrl = page.url();

    if (saveStorageState) {
      await context.storageState({ path: STORAGE_STATE_FILE });
    }
  } finally {
    const result = {
      targetUrl,
      currentUrl,
      loginSuccess,
      pageTitle: await page.title().catch(() => null),
      captureCount: captures.length,
      captures
    };

    fs.writeFileSync(OUTPUT_FILE, JSON.stringify(result, null, 2));
    await browser.close();
  }

  console.log(JSON.stringify({
    outputFile: OUTPUT_FILE,
    storageStateFile: saveStorageState ? STORAGE_STATE_FILE : null,
    targetUrl,
    currentUrl,
    loginSuccess,
    captureCount: captures.length
  }, null, 2));
}

main().catch(error => {
  console.error(error.stack || error.message);
  process.exit(1);
});
