import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function analyzeDetailPage() {
  const sessionFile = path.join(__dirname, 'data/session.json');
  const session = JSON.parse(fs.readFileSync(sessionFile, 'utf8'));

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  await context.addCookies(session.cookies);

  const page = await context.newPage();

  // Go directly to a strategy detail page
  const detailUrl = 'https://bigquant.com/trading/detail/d3ecb2af-c36e-4b43-88fb-9af4256e5aa6';
  console.log('Navigating to:', detailUrl);
  await page.goto(detailUrl, { waitUntil: 'networkidle' });
  await page.waitForTimeout(5000);

  // Save HTML
  const html = await page.content();
  fs.writeFileSync(path.join(__dirname, 'data/detail-page.html'), html);
  console.log('HTML saved to data/detail-page.html');

  // Screenshot
  await page.screenshot({ path: path.join(__dirname, 'data/detail-page.png'), fullPage: true });
  console.log('Screenshot saved to data/detail-page.png');

  // Find all buttons
  const buttons = await page.$$('button');
  console.log('\n=== Buttons ===');
  for (let i = 0; i < buttons.length; i++) {
    const text = await buttons[i].textContent();
    const className = await buttons[i].getAttribute('class');
    console.log(`${i + 1}. "${text?.trim()}" class="${className?.substring(0, 50)}"`);
  }

  // Find all links
  const links = await page.$$('a');
  console.log('\n=== Links (first 15) ===');
  for (let i = 0; i < Math.min(15, links.length); i++) {
    const text = await links[i].textContent();
    const href = await links[i].getAttribute('href');
    console.log(`${i + 1}. "${text?.trim()}" -> "${href}"`);
  }

  // Find action buttons specifically
  const actionKeywords = ['编辑', '修改', '运行', '回测', '保存', 'delete', 'edit', 'run', 'save'];
  console.log('\n=== Action elements ===');
  for (const keyword of actionKeywords) {
    const elements = await page.$$(`button:has-text("${keyword}"), a:has-text("${keyword}"), [class*="${keyword}"]`);
    if (elements.length > 0) {
      console.log(`"${keyword}": ${elements.length} elements`);
    }
  }

  await browser.close();
}

analyzeDetailPage().catch(console.error);