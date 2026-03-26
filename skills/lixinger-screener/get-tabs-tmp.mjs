import { chromium } from 'playwright';
import { createRequire } from 'module';
import { fileURLToPath } from 'url';
import path from 'path';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// load env manually
import dotenv from 'dotenv';
dotenv.config({ path: '/Users/fengzhi/Downloads/git/testlixingren/skills/lixinger-screener/.env' });
dotenv.config({ path: '/Users/fengzhi/Downloads/git/testlixingren/skills/lixinger-screener/../.env' });

const username = process.env.LIXINGER_USERNAME;
const password = process.env.LIXINGER_PASSWORD;

async function login() {
  const r = await fetch('https://www.lixinger.com/api/account/sign-in/by-account', {
    method: 'POST',
    headers: { 'content-type': 'application/json;charset=UTF-8', 'user-agent': 'Mozilla/5.0' },
    body: JSON.stringify({ accountName: username, password })
  });
  const setCookies = r.headers.getSetCookie?.() ?? [];
  return setCookies.map(v => v.split(';')[0]).join('; ');
}

async function getTabsForUrl(page, url) {
  await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 45000 });
  await page.waitForTimeout(5000);
  const tabs = await page.evaluate(() =>
    [...document.querySelectorAll('a.nav-link')].map(a => a.textContent.trim()).filter(Boolean)
  );
  return tabs;
}

const cookie = await login();
const browser = await chromium.launch({ headless: true, channel: 'chrome', args: ['--no-sandbox'] })
  .catch(() => chromium.launch({ headless: true, args: ['--no-sandbox'] }));

const context = await browser.newContext({ locale: 'zh-CN', viewport: { width: 1600, height: 1000 }, userAgent: 'Mozilla/5.0' });
await context.addCookies(
  cookie.split(';').map(item => item.trim()).filter(Boolean).map(item => {
    const [name, ...rest] = item.split('=');
    return { name, value: rest.join('='), domain: '.lixinger.com', path: '/', secure: true, sameSite: 'Lax' };
  })
);
const page = await context.newPage();

const pages = [
  ['fund-cn', 'https://www.lixinger.com/analytics/screener/fund-fundamental/cn'],
  ['index-cn', 'https://www.lixinger.com/analytics/screener/index-fundamental/cn'],
  ['index-hk', 'https://www.lixinger.com/analytics/screener/index-fundamental/hk'],
  ['company-hk', 'https://www.lixinger.com/analytics/screener/company-fundamental/hk'],
  ['company-us', 'https://www.lixinger.com/analytics/screener/company-fundamental/us'],
];

const result = {};
for (const [key, url] of pages) {
  const tabs = await getTabsForUrl(page, url);
  result[key] = tabs;
  console.log(`[${key}] tabs(${tabs.length}):`, JSON.stringify(tabs));
}

await browser.close();
