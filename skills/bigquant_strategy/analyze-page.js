import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';

async function analyze() {
  const sessionFile = './data/session.json';
  const session = JSON.parse(fs.readFileSync(sessionFile, 'utf8'));

  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext();
  await context.addCookies(session.cookies);

  const page = await context.newPage();

  console.log('Navigating to BigQuant AIStudio...');
  await page.goto('https://bigquant.com/aistudio', { waitUntil: 'networkidle' });
  await page.waitForTimeout(10000);

  const url = page.url();
  console.log('Current URL:', url);

  // Save page HTML for analysis
  const html = await page.content();
  fs.writeFileSync('./data/aistudio-debug.html', html);
  console.log('HTML saved to data/aistudio-debug.html');

  // Take screenshot
  await page.screenshot({ path: './data/aistudio-analyze.png', fullPage: true });
  console.log('Screenshot saved');

  // Find all interactive elements
  const buttons = await page.$$('button');
  console.log('Found', buttons.length, 'buttons');

  const textareas = await page.$$('textarea');
  console.log('Found', textareas.length, 'textareas');

  const editors = await page.$$('.CodeMirror, .monaco-editor, [class*="editor"]');
  console.log('Found', editors.length, 'editor elements');

  // List button texts
  for (const btn of buttons.slice(0, 10)) {
    const text = await btn.textContent().catch(() => '');
    console.log('Button:', text?.trim()?.substring(0, 50));
  }

  // Keep browser open for 60 seconds for manual inspection
  console.log('\nBrowser will stay open for 60 seconds for manual inspection...');
  await page.waitForTimeout(60000);

  await browser.close();
}

analyze().catch(console.error);