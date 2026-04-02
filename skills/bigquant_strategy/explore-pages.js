import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function exploreBigQuant() {
  const sessionFile = path.join(__dirname, 'data/session.json');
  const session = JSON.parse(fs.readFileSync(sessionFile, 'utf8'));

  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext();
  await context.addCookies(session.cookies);

  const page = await context.newPage();

  // Try different BigQuant pages
  const pages = [
    { name: 'Trading List', url: 'https://bigquant.com/trading/list' },
    { name: 'Strategy List', url: 'https://bigquant.com/strategy/list' },
    { name: 'AIStudio', url: 'https://bigquant.com/aistudio' },
  ];

  for (const p of pages) {
    console.log(`\nVisiting ${p.name}: ${p.url}`);
    await page.goto(p.url, { waitUntil: 'networkidle' });
    await page.waitForTimeout(5000);

    const url = page.url();
    const title = await page.title();
    console.log('URL:', url);
    console.log('Title:', title);

    // Take screenshot
    const screenshotPath = path.join(__dirname, `data/explore-${p.name.toLowerCase().replace(' ', '-')}.png`);
    await page.screenshot({ path: screenshotPath, fullPage: true });
    console.log('Screenshot:', screenshotPath);

    // Find all links
    const links = await page.$$('a[href]');
    console.log('Links found:', links.length);

    // Find all buttons
    const buttons = await page.$$('button');
    console.log('Buttons found:', buttons.length);
  }

  console.log('\n\nExploration complete. Browser will stay open for 60 seconds.');
  await page.waitForTimeout(60000);

  await browser.close();
}

exploreBigQuant().catch(console.error);