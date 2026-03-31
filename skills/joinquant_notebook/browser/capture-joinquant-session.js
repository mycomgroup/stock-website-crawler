#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { chromium } from 'playwright';
import '../load-env.js';
import {
  CONTRACT_FILE,
  DEFAULT_NOTEBOOK_URL,
  RAW_CAPTURE_FILE,
  SESSION_FILE
} from '../paths.js';

const USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36';

function ensureDir(filePath) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
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

function redactHeaders(headers = {}) {
  return Object.fromEntries(
    Object.entries(headers).map(([key, value]) => (
      /cookie|authorization|token/i.test(key)
        ? [key, '<redacted>']
        : [key, value]
    ))
  );
}

function truncate(value, max = 4000) {
  if (value == null) return null;
  const text = typeof value === 'string' ? value : JSON.stringify(value);
  if (text.length <= max) return text;
  return `${text.slice(0, max)}...<truncated>`;
}

function buildCookieHeader(cookies = []) {
  return cookies.map(item => `${item.name}=${item.value}`).join('; ');
}

function normalizeCookies(cookies = []) {
  return cookies.map(cookie => ({
    name: cookie.name,
    value: cookie.value,
    domain: cookie.domain,
    path: cookie.path,
    expires: cookie.expires,
    httpOnly: cookie.httpOnly,
    secure: cookie.secure,
    sameSite: cookie.sameSite
  }));
}

async function clickFirst(page, selectors) {
  for (const selector of selectors) {
    const locator = page.locator(selector).first();
    if (await locator.count().catch(() => 0)) {
      const visible = await locator.isVisible().catch(() => false);
      if (visible) {
        await locator.click({ force: true }).catch(() => {});
        await page.waitForTimeout(500);
        return true;
      }
    }
  }
  return false;
}

async function fillFirst(page, selectors, value) {
  for (const selector of selectors) {
    const locator = page.locator(selector).first();
    if (await locator.count().catch(() => 0)) {
      const visible = await locator.isVisible().catch(() => false);
      if (visible) {
        await locator.fill(value, { timeout: 5000 }).catch(() => {});
        const current = await locator.inputValue().catch(() => '');
        if (current === value) {
          return true;
        }
      }
    }
  }
  return false;
}

async function ensureCheckboxChecked(page, selectors) {
  for (const selector of selectors) {
    const locator = page.locator(selector).first();
    if (!(await locator.count().catch(() => 0))) {
      continue;
    }
    const visible = await locator.isVisible().catch(() => false);
    if (!visible) {
      continue;
    }
    const checked = await locator.isChecked().catch(() => false);
    if (checked) {
      return true;
    }
    await locator.check({ force: true }).catch(async () => {
      await locator.click({ force: true }).catch(() => {});
    });
    await page.waitForTimeout(300);
    if (await locator.isChecked().catch(() => false)) {
      return true;
    }
  }
  return false;
}

function resolveDirectNotebookUrl(inputUrl) {
  const parsed = new URL(inputUrl);
  const notebookPath = parsed.searchParams.get('url');
  if (notebookPath?.startsWith('/')) {
    return new URL(notebookPath, parsed.origin).toString();
  }
  return inputUrl;
}

async function findJupyterFrame(page) {
  for (const frame of page.frames()) {
    const hasJupyter = await frame.evaluate(() => Boolean(window.Jupyter?.notebook)).catch(() => false);
    if (hasJupyter) {
      return frame;
    }
  }
  return null;
}

async function waitForNotebookReady(page) {
  const candidates = [
    '.notebook_app',
    '#notebook',
    '#site',
    '.jp-Notebook'
  ];

  for (let attempt = 0; attempt < 60; attempt += 1) {
    const frame = await findJupyterFrame(page);
    if (frame) {
      return frame;
    }

    for (const currentFrame of page.frames()) {
      for (const selector of candidates) {
        const locator = currentFrame.locator(selector).first();
        if (await locator.count().catch(() => 0)) {
          await locator.waitFor({ state: 'visible', timeout: 1000 }).catch(() => {});
        }
      }
    }

    await page.waitForTimeout(500);
  }

  return null;
}

async function loginIfNeeded(page, username, password, hasExistingCookies) {
  await page.waitForTimeout(2000);
  let currentUrl = page.url();

  if (currentUrl.includes('/research') && !currentUrl.includes('/user/login/')) {
    return { loggedIn: true, mode: 'existing-session' };
  }

  if (currentUrl.includes('/hub/') && !currentUrl.includes('/login')) {
    return { loggedIn: true, mode: 'cookie-session' };
  }

  if (hasExistingCookies && currentUrl.includes('/user/login/')) {
    await page.waitForTimeout(3000);
    currentUrl = page.url();
    if (!currentUrl.includes('/user/login/')) {
      return { loggedIn: true, mode: 'cookie-auto-login' };
    }
  }

  if (!currentUrl.includes('/user/login/')) {
    await clickFirst(page, [
      'a[href*="/user/login/index?type=login"]',
      'button:has-text("登录")',
      'a:has-text("登录")'
    ]);
    await page.waitForTimeout(1000);
    currentUrl = page.url();
  }

  await clickFirst(page, [
    'text=密码登录',
    'text=账号密码登录',
    '[role="tab"]:has-text("密码")'
  ]);

  const usernameInput = page.locator('input[name="username"]').first();
  const passwordInput = page.locator('input[name="pwd"], input[name="password"], input[type="password"]').first();
  const submitButton = page.locator('button.login-submit.btnPwdSubmit, button:has-text("登")').first();

  if (!(await usernameInput.count()) || !(await passwordInput.count())) {
    throw new Error('未找到登录输入框，无法自动填写账号密码');
  }

  await usernameInput.fill('');
  await usernameInput.fill(username);
  await passwordInput.fill('');
  await passwordInput.fill(password);

  const acceptedAgreement = await ensureCheckboxChecked(page, [
    '#agreementBox',
    'input.agreement-box',
    'input[type="checkbox"]'
  ]);

  await page.waitForTimeout(300);

  if (await submitButton.count()) {
    await submitButton.click({ force: true });
  } else {
    await passwordInput.press('Enter').catch(() => {});
  }

  await Promise.race([
    page.waitForURL(url => !url.includes('/user/login/'), { timeout: 15000 }).catch(() => null),
    page.waitForLoadState('networkidle', { timeout: 15000 }).catch(() => null),
    page.waitForTimeout(5000)
  ]);

  await page.waitForTimeout(1500);

  const errorText = await page.locator(
    '.error:visible, .help-block:visible, .tips:visible, .toast:visible, .layui-layer-content:visible, .login-error:visible'
  ).allInnerTexts().catch(() => []);

  return {
    loggedIn: !page.url().includes('/user/login/'),
    mode: 'form-login',
    acceptedAgreement,
    urlAfterSubmit: page.url(),
    errorText: errorText.filter(Boolean).join(' | ') || null
  };
}

async function collectPageState(page, frame = null) {
  const targetFrame = frame || page.mainFrame();
  const frameState = await targetFrame.evaluate(() => {
    const csrfMeta = document.querySelector('meta[name="csrf-token"], meta[name="csrf_token"], meta[name="_csrf"], meta[name="x-csrf-token"]');
    const csrfInput = document.querySelector('input[name="csrfmiddlewaretoken"], input[name="_csrf"], input[name="csrf_token"]');
    const scripts = [...document.scripts].map(item => item.src).filter(Boolean).slice(0, 50);
    const notebook = window.Jupyter?.notebook || window.jupyterapp || null;
    const bodyDataset = document.body ? { ...document.body.dataset } : {};
    return {
      url: location.href,
      title: document.title,
      hasJupyter: Boolean(window.Jupyter?.notebook),
      bodyClassName: document.body?.className || '',
      bodyDataset,
      csrfMeta: csrfMeta?.getAttribute('content') || null,
      csrfInput: csrfInput?.value || null,
      scripts,
      notebook: notebook ? {
        notebookPath: notebook.notebook_path || notebook.notebookPath || null,
        baseUrl: notebook.base_url || notebook.baseUrl || null,
        kernelId: notebook.kernel?.id || null,
        sessionId: notebook.session?.session_id || notebook.session?.id || null,
        ncells: typeof notebook.ncells === 'function' ? notebook.ncells() : null
      } : null
    };
  }).catch(() => ({
    url: targetFrame.url(),
    title: null,
    hasJupyter: false,
    bodyClassName: '',
    bodyDataset: {},
    csrfMeta: null,
    csrfInput: null,
    scripts: [],
    notebook: null
  }));

  return {
    pageUrl: page.url(),
    pageTitle: await page.title().catch(() => null),
    frameCount: page.frames().length,
    targetFrameUrl: targetFrame.url(),
    ...frameState
  };
}

async function triggerNotebookActions(frame) {
  if (!frame) {
    return { hasJupyter: false, reason: '未找到包含 Jupyter 的 frame' };
  }

  return frame.evaluate(async () => {
    const notebook = window.Jupyter?.notebook;
    if (!notebook) {
      return { hasJupyter: false, reason: 'frame 内未找到 Jupyter.notebook' };
    }

    const startCount = typeof notebook.ncells === 'function' ? notebook.ncells() : null;
    const cell = typeof notebook.insert_cell_at_bottom === 'function'
      ? notebook.insert_cell_at_bottom('code')
      : typeof notebook.insert_cell_below === 'function'
        ? notebook.insert_cell_below('code')
        : null;

    if (!cell) {
      return {
        hasJupyter: true,
        inserted: false,
        reason: '无法通过页面对象创建 cell'
      };
    }

    if (typeof cell.set_text === 'function') {
      cell.set_text('print("hello")');
    } else if (cell.code_mirror?.setValue) {
      cell.code_mirror.setValue('print("hello")');
    }

    const cellIndex = typeof notebook.find_cell_index === 'function'
      ? notebook.find_cell_index(cell)
      : startCount;

    if (typeof notebook.select === 'function' && Number.isInteger(cellIndex)) {
      notebook.select(cellIndex);
    }

    if (typeof notebook.save_notebook === 'function') {
      try {
        const result = notebook.save_notebook();
        if (result?.then) {
          await result.catch(() => {});
        }
      } catch {
      }
    }

    if (typeof notebook.execute_selected_cells === 'function') {
      try {
        notebook.execute_selected_cells();
      } catch {
      }
    } else if (typeof notebook.execute_cell_and_select_below === 'function') {
      try {
        notebook.execute_cell_and_select_below();
      } catch {
      }
    }

    await new Promise(resolve => setTimeout(resolve, 3000));

    if (typeof notebook.execute_all_cells === 'function') {
      try {
        notebook.execute_all_cells();
      } catch {
      }
    }

    return {
      hasJupyter: true,
      inserted: true,
      cellIndex,
      startCount,
      endCount: typeof notebook.ncells === 'function' ? notebook.ncells() : null,
      kernelId: notebook.kernel?.id || null,
      sessionId: notebook.session?.session_id || notebook.session?.id || null,
      notebookPath: notebook.notebook_path || notebook.notebookPath || null
    };
  });
}

function normalizeCaptureOptions(options = {}) {
  if (Array.isArray(options)) {
    return parseArgs(options);
  }
  return { ...options };
}

function loadExistingCookies() {
  try {
    if (!fs.existsSync(SESSION_FILE)) {
      return null;
    }
    const data = JSON.parse(fs.readFileSync(SESSION_FILE, 'utf8'));
    if (!data.cookies || !Array.isArray(data.cookies)) {
      return null;
    }
    const capturedAt = new Date(data.capturedAt);
    const now = new Date();
    const hoursSinceCapture = (now - capturedAt) / (1000 * 60 * 60);
    if (hoursSinceCapture > 24 * 7) {
      return null;
    }
    return data.cookies.filter(cookie => {
      if (cookie.expires && cookie.expires > 0 && cookie.expires < now.getTime() / 1000) {
        return false;
      }
      return true;
    });
  } catch {
    return null;
  }
}

export async function captureJoinQuantSession(options = {}) {
  const args = normalizeCaptureOptions(options);
  const username = args.username || process.env.JOINQUANT_USERNAME;
  const password = args.password || process.env.JOINQUANT_PASSWORD;
  const notebookUrl = args.url || args.notebookUrl || process.env.JOINQUANT_NOTEBOOK_URL || DEFAULT_NOTEBOOK_URL;
  const directNotebookUrl = resolveDirectNotebookUrl(notebookUrl);
  const headed = args.headed === true || args.headless === false || args.headless === 'false';
  const forceLogin = args.forceLogin === true || args['force-login'] === true;

  if (!username || !password) {
    throw new Error('缺少 JOINQUANT_USERNAME 或 JOINQUANT_PASSWORD');
  }

  const sessionDir = path.dirname(SESSION_FILE);
  if (sessionDir && sessionDir !== '.' && !fs.existsSync(sessionDir)) {
    fs.mkdirSync(sessionDir, { recursive: true });
  }
  const contractDir = path.dirname(CONTRACT_FILE);
  if (contractDir && contractDir !== '.' && !fs.existsSync(contractDir)) {
    fs.mkdirSync(contractDir, { recursive: true });
  }
  const rawDir = path.dirname(RAW_CAPTURE_FILE);
  if (rawDir && rawDir !== '.' && !fs.existsSync(rawDir)) {
    fs.mkdirSync(rawDir, { recursive: true });
  }

  const existingCookies = forceLogin ? null : loadExistingCookies();

  const browser = await chromium.launch({
    headless: !headed,
    channel: 'chrome'
  }).catch(() => chromium.launch({ headless: !headed }));

  const context = await browser.newContext({
    locale: 'zh-CN',
    viewport: { width: 1600, height: 1200 },
    userAgent: USER_AGENT,
    extraHTTPHeaders: {
      'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
    }
  });

  if (existingCookies && existingCookies.length > 0) {
    await context.addCookies(existingCookies);
  }

  const page = await context.newPage();
  const captures = [];
  const websockets = [];
  let counter = 0;

  page.on('request', request => {
    const resourceType = request.resourceType();
    if (!['xhr', 'fetch', 'document', 'script', 'websocket'].includes(resourceType)) {
      return;
    }
    captures.push({
      id: ++counter,
      phase: 'request',
      resourceType,
      method: request.method(),
      url: request.url(),
      headers: redactHeaders(request.headers()),
      postData: truncate(request.postData())
    });
  });

  page.on('response', async response => {
    const request = response.request();
    const resourceType = request.resourceType();
    if (!['xhr', 'fetch', 'document', 'script'].includes(resourceType)) {
      return;
    }
    const contentType = response.headers()['content-type'] || '';
    let body = null;
    if (/json|text|javascript/.test(contentType)) {
      body = truncate(await response.text().catch(() => null));
    }
    captures.push({
      id: ++counter,
      phase: 'response',
      resourceType,
      method: request.method(),
      url: response.url(),
      status: response.status(),
      headers: redactHeaders(response.headers()),
      contentType,
      body
    });
  });

  page.on('websocket', ws => {
    const item = {
      url: ws.url(),
      framesSent: [],
      framesReceived: []
    };
    websockets.push(item);
    ws.on('framesent', event => {
      item.framesSent.push(truncate(event.payload));
    });
    ws.on('framereceived', event => {
      item.framesReceived.push(truncate(event.payload));
    });
  });

  let loginResult = null;
  let pageState = null;
  let actionResult = null;

  try {
    const researchUrl = 'https://www.joinquant.com/research';
    await page.goto(researchUrl, { waitUntil: 'domcontentloaded', timeout: 60000 });
    loginResult = await loginIfNeeded(page, username, password, Boolean(existingCookies?.length));
    await page.waitForTimeout(2000);
    await page.goto(directNotebookUrl, { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForLoadState('networkidle', { timeout: 30000 }).catch(() => {});
    const notebookFrame = await waitForNotebookReady(page);
    await page.waitForTimeout(5000);

    pageState = await collectPageState(page, notebookFrame);
    actionResult = await triggerNotebookActions(notebookFrame);
    await page.waitForTimeout(12000);

    const cookies = await context.cookies();
    const cookieHeader = buildCookieHeader(cookies.filter(item => {
      const domain = item.domain.startsWith('.') ? item.domain.slice(1) : item.domain;
      return domain === 'joinquant.com' || domain.endsWith('.joinquant.com');
    }));
    const sessionPayload = {
      capturedAt: new Date().toISOString(),
      notebookUrl,
      directNotebookUrl,
      cookieHeader,
      cookies: normalizeCookies(cookies),
      pageState,
      actionResult,
      login: loginResult,
      reusedCookies: existingCookies?.length || 0
    };
    fs.writeFileSync(SESSION_FILE, JSON.stringify(sessionPayload, null, 2));

    const contractPayload = {
      capturedAt: sessionPayload.capturedAt,
      notebookUrl,
      directNotebookUrl,
      pageState,
      actionResult,
      requestUrls: [...new Set(captures.map(item => item.url))],
      likelyNotebookRequests: captures.filter(item => /research|notebook|api|kernel|session|contents|save|run|execute/i.test(item.url)),
      websockets
    };
    fs.writeFileSync(CONTRACT_FILE, JSON.stringify(contractPayload, null, 2));

    fs.writeFileSync(RAW_CAPTURE_FILE, JSON.stringify({
      capturedAt: sessionPayload.capturedAt,
      notebookUrl,
      directNotebookUrl,
      login: loginResult,
      pageState,
      actionResult,
      captures,
      websockets
    }, null, 2));

    return {
      sessionFile: SESSION_FILE,
      contractFile: CONTRACT_FILE,
      rawCaptureFile: RAW_CAPTURE_FILE,
      notebookUrl,
      directNotebookUrl,
      login: loginResult,
      pageState,
      actionResult
    };
  } finally {
    await context.close().catch(() => {});
    await browser.close().catch(() => {});
  }
}

async function main() {
  const result = await captureJoinQuantSession(process.argv.slice(2));
  process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  main().catch(error => {
    console.error(error.stack || error.message);
    process.exit(1);
  });
}
