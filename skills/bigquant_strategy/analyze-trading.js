import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function analyzeTradingPage() {
  const sessionFile = path.join(__dirname, 'data/session.json');
  const session = JSON.parse(fs.readFileSync(sessionFile, 'utf8'));

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  await context.addCookies(session.cookies);

  const page = await context.newPage();

  console.log('Navigating to Trading List page...');
  await page.goto('https://bigquant.com/trading/list', { waitUntil: 'networkidle' });
  await page.waitForTimeout(5000);

  // Save HTML
  const html = await page.content();
  fs.writeFileSync(path.join(__dirname, 'data/trading-list.html'), html);
  console.log('HTML saved to data/trading-list.html');

  // Take full screenshot
  await page.screenshot({ path: path.join(__dirname, 'data/trading-list-full.png'), fullPage: true });

  // Find all buttons with their details
  const buttons = await page.$$('button');
  console.log('\n=== Buttons ===');
  for (let i = 0; i < buttons.length; i++) {
    const btn = buttons[i];
    const text = await btn.textContent().catch(() => '');
    const className = await btn.getAttribute('class').catch(() => '');
    const onclick = await btn.getAttribute('onclick').catch(() => '');
    console.log(`${i + 1}. "${text?.trim()}" class="${className?.substring(0, 50)}" onclick="${onclick?.substring(0, 30)}"`);
  }

  // Find all links
  const links = await page.$$('a[href]');
  console.log('\n=== Links (first 20) ===');
  for (let i = 0; i < Math.min(20, links.length); i++) {
    const link = links[i];
    const text = await link.textContent().catch(() => '');
    const href = await link.getAttribute('href').catch(() => '');
    console.log(`${i + 1}. "${text?.trim()}" -> "${href}"`);
  }

  // Find strategy list items
  const strategyItems = await page.$$('[class*="strategy"], [class*="list-item"], tr, .item');
  console.log('\n=== Strategy items:', strategyItems.length, '===');

  // Check for create/new buttons specifically
  const newButtons = await page.$$('button:has-text("新建"), button:has-text("创建"), button:has-text("新策略")');
  console.log('\n=== New/Create buttons:', newButtons.length, '===');

  await browser.close();
}

analyzeTradingPage().catch(console.error);