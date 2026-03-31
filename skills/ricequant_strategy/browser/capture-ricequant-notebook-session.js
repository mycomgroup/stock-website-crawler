#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { chromium } from 'playwright';
import '../load-env.js';
import {
  CONTRACT_FILE,
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
  console.log(`当前 URL: ${currentUrl}`);

  if (currentUrl.includes('/research') && !currentUrl.includes('/login')) {
    console.log('✓ 已登录（research页面）');
    return { loggedIn: true, mode: 'existing-session' };
  }

  if (currentUrl.includes('/hub/') && !currentUrl.includes('/login')) {
    console.log('✓ 已登录（hub页面）');
    return { loggedIn: true, mode: 'cookie-session' };
  }

  if (hasExistingCookies && currentUrl.includes('/login')) {
    console.log('尝试使用已有 cookies 自动登录...');
    await page.waitForTimeout(3000);
    currentUrl = page.url();
    if (!currentUrl.includes('/login')) {
      console.log('✓ Cookies 自动登录成功');
      return { loggedIn: true, mode: 'cookie-auto-login' };
    }
    console.log('✗ Cookies 自动登录失败，需要手动登录');
  }

  if (!currentUrl.includes('/login')) {
    console.log('查找登录入口...');
    await clickFirst(page, [
      'a[href*="/login"]',
      'button:has-text("登录")',
      'a:has-text("登录")'
    ]);
    await page.waitForTimeout(1000);
    currentUrl = page.url();
  }

  console.log('切换到密码登录模式...');
  await clickFirst(page, [
    'text=密码登录',
    'text=账号密码登录',
    '[role="tab"]:has-text("密码")'
  ]);

  const usernameSelectors = [
    'input[name="username"]',
    'input[placeholder*="手机"]',
    'input[placeholder*="邮箱"]',
    'input[type="text"]'
  ];
  
  const passwordSelectors = [
    'input[name="password"]',
    'input[name="pwd"]',
    'input[type="password"]'
  ];

  let usernameInput = null;
  let passwordInput = null;

  for (const selector of usernameSelectors) {
    const locator = page.locator(selector).first();
    if (await locator.count().catch(() => 0) && await locator.isVisible().catch(() => false)) {
      usernameInput = locator;
      break;
    }
  }

  for (const selector of passwordSelectors) {
    const locator = page.locator(selector).first();
    if (await locator.count().catch(() => 0) && await locator.isVisible().catch(() => false)) {
      passwordInput = locator;
      break;
    }
  }

  if (!usernameInput || !passwordInput) {
    throw new Error('未找到登录输入框，无法自动填写账号密码');
  }

  console.log('填写登录信息...');
  await usernameInput.fill('');
  await usernameInput.fill(username);
  await passwordInput.fill('');
  await passwordInput.fill(password);

  await page.waitForTimeout(300);

  console.log('提交登录...');
  const submitSelectors = [
    'button.login-submit',
    'button.btn--submit',
    'button:has-text("登")',
    'button:has-text("登录")'
  ];

  let submitted = false;
  for (const selector of submitSelectors) {
    const locator = page.locator(selector).first();
    if (await locator.count().catch(() => 0) && await locator.isVisible().catch(() => false)) {
      await locator.click({ force: true });
      submitted = true;
      break;
    }
  }

  if (!submitted) {
    await passwordInput.press('Enter').catch(() => {});
  }

  console.log('等待登录完成...');
  await Promise.race([
    page.waitForURL(url => !url.includes('/login'), { timeout: 15000 }).catch(() => null),
    page.waitForLoadState('networkidle', { timeout: 15000 }).catch(() => null),
    page.waitForTimeout(5000)
  ]);

  await page.waitForTimeout(1500);

  const success = !page.url().includes('/login');
  if (success) {
    console.log('✓ 登录成功');
  } else {
    console.log('✗ 登录失败');
  }

  return {
    loggedIn: success,
    mode: 'form-login',
    urlAfterSubmit: page.url()
  };
}

async function collectPageState(page, frame = null) {
  const targetFrame = frame || page.mainFrame();
  const frameState = await targetFrame.evaluate(() => {
    const csrfMeta = document.querySelector('meta[name="csrf-token"], meta[name="csrf_token"]');
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
      cell.set_text('print("hello from ricequant")');
    } else if (cell.code_mirror?.setValue) {
      cell.code_mirror.setValue('print("hello from ricequant")');
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

export async function captureRiceQuantNotebookSession(options = {}) {
  const args = normalizeCaptureOptions(options);
  const username = args.username || process.env.RICEQUANT_USERNAME;
  const password = args.password || process.env.RICEQUANT_PASSWORD;
  const notebookUrl = args.url || args.notebookUrl || process.env.RICEQUANT_NOTEBOOK_URL;
  const directNotebookUrl = resolveDirectNotebookUrl(notebookUrl);
  
  const headed = args.headed === true;
  const headless = args.headless !== false;
  const forceLogin = args.forceLogin === true || args['force-login'] === true;

  console.log('=== RiceQuant Notebook Session Capture ===');
  console.log(`模式: ${headed ? '有界面' : '无界面（headless）'}`);
  console.log(`Notebook URL: ${notebookUrl}`);

  if (!username || !password) {
    throw new Error('缺少 RICEQUANT_USERNAME 或 RICEQUANT_PASSWORD');
  }

  if (!notebookUrl) {
    throw new Error('缺少 RICEQUANT_NOTEBOOK_URL');
  }

  ensureDir(SESSION_FILE);
  ensureDir(CONTRACT_FILE);
  ensureDir(RAW_CAPTURE_FILE);

  const existingCookies = forceLogin ? null : loadExistingCookies();
  
  if (existingCookies && existingCookies.length > 0) {
    console.log(`✓ 发现已有 cookies (${existingCookies.length} 个)`);
  }

  console.log('启动浏览器...');
  const browser = await chromium.launch({
    headless: headless && !headed,
    channel: 'chrome'
  }).catch(() => {
    console.log('使用默认浏览器...');
    return chromium.launch({ headless: headless && !headed });
  });

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
    console.log('访问 RiceQuant 主页...');
    const ricequantUrl = 'https://www.ricequant.com';
    await page.goto(ricequantUrl, { waitUntil: 'domcontentloaded', timeout: 60000 });
    
    loginResult = await loginIfNeeded(page, username, password, Boolean(existingCookies?.length));
    
    if (!loginResult.loggedIn) {
      console.log('尝试直接访问登录页面...');
      await page.goto('https://www.ricequant.com/login', { waitUntil: 'domcontentloaded', timeout: 60000 });
      loginResult = await loginIfNeeded(page, username, password, Boolean(existingCookies?.length));
    }
    
    if (!loginResult.loggedIn) {
      throw new Error('登录失败');
    }
    
    console.log('访问 Notebook...');
    await page.waitForTimeout(2000);
    await page.goto(directNotebookUrl, { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForLoadState('networkidle', { timeout: 30000 }).catch(() => {});
    
    console.log('等待 Notebook 加载...');
    const notebookFrame = await waitForNotebookReady(page);
    await page.waitForTimeout(5000);

    console.log('收集页面状态...');
    pageState = await collectPageState(page, notebookFrame);
    actionResult = await triggerNotebookActions(notebookFrame);
    await page.waitForTimeout(12000);

    console.log('保存 session...');
    const cookies = await context.cookies();
    const cookieHeader = buildCookieHeader(cookies.filter(item => item.domain.includes('ricequant.com')));
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
    console.log(`✓ Session 已保存: ${SESSION_FILE}`);

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
  const result = await captureRiceQuantNotebookSession(process.argv.slice(2));
  process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  main().catch(error => {
    console.error(error.stack || error.message);
    process.exit(1);
  });
}