#!/usr/bin/env node

import { chromium } from 'playwright';
import { readFileSync, writeFileSync } from 'fs';
import { join } from 'path';
import { PATHS } from './paths.js';
import { ENV } from './load-env.js';

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (!arg.startsWith('--')) {
      continue;
    }

    const key = arg.slice(2);
    const value = argv[i + 1];
    if (value && !value.startsWith('--')) {
      args[key] = value;
      i++;
    } else {
      args[key] = true;
    }
  }
  return args;
}

function cookieKey(cookie) {
  return `${cookie.domain}|${cookie.path || '/'}|${cookie.name}`;
}

function normalizeCookies(cookies = []) {
  return cookies.map((cookie) => ({
    name: cookie.name,
    value: cookie.value,
    domain: cookie.domain,
    path: cookie.path || '/',
    expires: cookie.expires ?? cookie.expirationDate ?? -1,
    httpOnly: Boolean(cookie.httpOnly),
    secure: Boolean(cookie.secure),
    sameSite: cookie.sameSite || 'Lax'
  }));
}

function diffCookies(before = [], after = []) {
  const beforeMap = new Map(before.map((cookie) => [cookieKey(cookie), cookie]));
  const afterMap = new Map(after.map((cookie) => [cookieKey(cookie), cookie]));

  const added = [];
  const removed = [];
  const changed = [];

  for (const [key, cookie] of afterMap.entries()) {
    if (!beforeMap.has(key)) {
      added.push(cookie);
      continue;
    }

    const previous = beforeMap.get(key);
    if (previous.value !== cookie.value) {
      changed.push({
        name: cookie.name,
        domain: cookie.domain,
        path: cookie.path,
        beforeValuePreview: `${previous.value}`.slice(0, 24),
        afterValuePreview: `${cookie.value}`.slice(0, 24)
      });
    }
  }

  for (const [key, cookie] of beforeMap.entries()) {
    if (!afterMap.has(key)) {
      removed.push(cookie);
    }
  }

  return { added, removed, changed };
}

async function safeAllHeaders(target) {
  if (typeof target.allHeaders === 'function') {
    try {
      return await target.allHeaders();
    } catch {
      return target.headers();
    }
  }

  return target.headers();
}

async function safeHeadersArray(target) {
  if (typeof target.headersArray === 'function') {
    try {
      return await target.headersArray();
    } catch {
      return null;
    }
  }

  return null;
}

async function snapshotPageState(page, label) {
  const state = await page.evaluate(() => {
    const localStorageData = {};
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      localStorageData[key] = localStorage.getItem(key);
    }

    const sessionStorageData = {};
    for (let i = 0; i < sessionStorage.length; i++) {
      const key = sessionStorage.key(i);
      sessionStorageData[key] = sessionStorage.getItem(key);
    }

    return {
      url: window.location.href,
      title: document.title,
      readyState: document.readyState,
      userAgent: navigator.userAgent,
      language: navigator.language,
      languages: navigator.languages,
      webdriver: navigator.webdriver,
      documentCookie: document.cookie,
      localStorage: localStorageData,
      sessionStorage: sessionStorageData
    };
  });

  return {
    label,
    capturedAt: new Date().toISOString(),
    ...state
  };
}

async function captureHeaders() {
  const args = parseArgs(process.argv.slice(2));
  const message = args.message || '请只回复OK';
  const outputFile = args.output || join(PATHS.data, `browser-network-diagnosis-${Date.now()}.json`);

  console.log('🔍 捕获浏览器真实请求头和状态...');
  console.log(`📝 诊断消息: ${message}`);

  const sessionData = JSON.parse(readFileSync(PATHS.sessionFile, 'utf-8'));
  const initialSessionCookies = normalizeCookies(sessionData.cookies || []);

  const launchOptions = {
    headless: args.headless ? true : false,
    args: [
      '--disable-blink-features=AutomationControlled',
      ENV.HTTP_PROXY || ENV.HTTPS_PROXY ? `--proxy-server=${ENV.HTTPS_PROXY || ENV.HTTP_PROXY}` : null
    ].filter(Boolean)
  };

  const browser = await chromium.launch(launchOptions);
  const context = await browser.newContext({
    viewport: { width: 1280, height: 800 },
    userAgent: sessionData.userAgent,
    locale: 'zh-CN',
    timezoneId: 'Asia/Shanghai'
  });

  await context.addCookies(initialSessionCookies);

  const page = await context.newPage();
  const networkLog = [];

  page.on('request', async (request) => {
    const url = request.url();
    if (!url.includes('/backend-api/')) {
      return;
    }

    networkLog.push({
      type: 'request',
      capturedAt: new Date().toISOString(),
      url,
      method: request.method(),
      resourceType: request.resourceType(),
      headers: await safeAllHeaders(request),
      headersArray: await safeHeadersArray(request),
      postData: request.postData() || null
    });
  });

  page.on('response', async (response) => {
    const url = response.url();
    if (!url.includes('/backend-api/')) {
      return;
    }

    networkLog.push({
      type: 'response',
      capturedAt: new Date().toISOString(),
      url,
      status: response.status(),
      statusText: response.statusText(),
      headers: await safeAllHeaders(response),
      headersArray: await safeHeadersArray(response)
    });
  });

  try {
    console.log('🌐 打开 ChatGPT 页面...');
    await page.goto('https://chatgpt.com/', {
      waitUntil: 'domcontentloaded',
      timeout: 60000
    });

    console.log('⏳ 等待页面稳定...');
    await page.waitForTimeout(3000);

    const stateAfterLoad = await snapshotPageState(page, 'after-load');
    const cookiesAfterLoad = normalizeCookies(await context.cookies());
    console.log(`📍 当前页面: ${stateAfterLoad.url}`);

    console.log('🔎 查找输入框...');
    const textarea = await page.waitForSelector(
      'textarea[placeholder*="Message"], textarea[data-id="root"], #prompt-textarea',
      { timeout: 15000 }
    );

    console.log('⌨️ 输入诊断消息...');
    await textarea.click();
    await textarea.fill('');
    await textarea.type(message, { delay: 30 });
    await page.waitForTimeout(500);

    const conversationResponsePromise = page.waitForResponse(
      (response) =>
        response.url().includes('/backend-api/conversation') &&
        response.request().method() === 'POST',
      { timeout: 60000 }
    ).catch(() => null);

    console.log('📤 点击发送...');
    const sendButton = page.locator('button[data-testid="send-button"]').first();
    await sendButton.click();

    console.log('⏳ 等待 conversation 响应...');
    const conversationResponse = await conversationResponsePromise;

    // Give the page a moment to settle so cookies/storage can update.
    console.log('📦 抓取发送后的 cookies 和存储状态...');
    await page.waitForTimeout(5000);

    const stateAfterSend = await snapshotPageState(page, 'after-send');
    const cookiesAfterSend = normalizeCookies(await context.cookies());

    const relevantLog = networkLog.filter((entry) =>
      entry.url.includes('/backend-api/conversation') ||
      entry.url.includes('/backend-api/sentinel/') ||
      entry.url.includes('/backend-api/models') ||
      entry.url.includes('/backend-api/accounts/')
    );

    const report = {
      capturedAt: new Date().toISOString(),
      message,
      pageTitle: await page.title(),
      pageUrl: page.url(),
      conversationResponse: conversationResponse
        ? {
            status: conversationResponse.status(),
            statusText: conversationResponse.statusText(),
            url: conversationResponse.url()
          }
        : null,
      sessionFileCookieNames: initialSessionCookies.map((cookie) => cookie.name),
      cookies: {
        sessionFile: initialSessionCookies,
        afterLoad: cookiesAfterLoad,
        afterSend: cookiesAfterSend,
        deltaFromSessionToLoad: diffCookies(initialSessionCookies, cookiesAfterLoad),
        deltaFromSessionToSend: diffCookies(initialSessionCookies, cookiesAfterSend)
      },
      states: {
        afterLoad: stateAfterLoad,
        afterSend: stateAfterSend
      },
      networkLog: relevantLog
    };

    writeFileSync(outputFile, JSON.stringify(report, null, 2), 'utf-8');

    const addedCookieNames = report.cookies.deltaFromSessionToSend.added.map((cookie) => cookie.name);
    const changedCookieNames = report.cookies.deltaFromSessionToSend.changed.map((cookie) => cookie.name);
    const localStorageKeys = Object.keys(stateAfterSend.localStorage || {});
    const sessionStorageKeys = Object.keys(stateAfterSend.sessionStorage || {});

    console.log('');
    console.log(`💾 诊断结果已保存到: ${outputFile}`);
    console.log(`📦 请求日志条数: ${relevantLog.length}`);
    console.log(`🍪 新增 cookies: ${addedCookieNames.length > 0 ? addedCookieNames.join(', ') : '无'}`);
    console.log(`🔁 变化 cookies: ${changedCookieNames.length > 0 ? changedCookieNames.join(', ') : '无'}`);
    console.log(`🗂️  localStorage keys: ${localStorageKeys.length > 0 ? localStorageKeys.join(', ') : '无'}`);
    console.log(`🗂️  sessionStorage keys: ${sessionStorageKeys.length > 0 ? sessionStorageKeys.join(', ') : '无'}`);

  } finally {
    await browser.close();
  }
}

captureHeaders().catch((error) => {
  console.error('❌ 捕获失败:', error);
  process.exit(1);
});
