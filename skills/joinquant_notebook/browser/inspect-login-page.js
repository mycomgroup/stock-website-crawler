#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { chromium } from 'playwright';
import '../load-env.js';
import { DATA_ROOT, DEFAULT_NOTEBOOK_URL } from '../paths.js';

const outputFile = path.join(DATA_ROOT, 'login-page-inspect.json');
fs.mkdirSync(DATA_ROOT, { recursive: true });

const browser = await chromium.launch({ headless: true, channel: 'chrome' }).catch(() => chromium.launch({ headless: true }));
const context = await browser.newContext({ locale: 'zh-CN' });
const page = await context.newPage();
await page.goto(DEFAULT_NOTEBOOK_URL, { waitUntil: 'domcontentloaded', timeout: 60000 });
await page.waitForTimeout(3000);
const result = await page.evaluate(() => {
  const getText = element => (element.innerText || element.textContent || '').trim();
  return {
    url: location.href,
    title: document.title,
    inputs: [...document.querySelectorAll('input, textarea, select')].map((el, index) => ({
      index,
      tag: el.tagName,
      type: el.getAttribute('type'),
      name: el.getAttribute('name'),
      id: el.id || null,
      placeholder: el.getAttribute('placeholder'),
      className: el.className,
      value: el.value,
      visible: !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length)
    })),
    buttons: [...document.querySelectorAll('button, a, input[type="button"], input[type="submit"]')].map((el, index) => ({
      index,
      tag: el.tagName,
      text: getText(el) || el.getAttribute('value') || '',
      id: el.id || null,
      name: el.getAttribute('name'),
      href: el.getAttribute('href'),
      className: el.className,
      visible: !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length)
    })).filter(item => item.text || item.href),
    iframes: [...document.querySelectorAll('iframe')].map((el, index) => ({
      index,
      id: el.id || null,
      name: el.getAttribute('name'),
      src: el.getAttribute('src'),
      className: el.className,
      visible: !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length)
    }))
  };
});
fs.writeFileSync(outputFile, JSON.stringify(result, null, 2));
console.log(JSON.stringify({ outputFile, ...result }, null, 2));
await browser.close();
