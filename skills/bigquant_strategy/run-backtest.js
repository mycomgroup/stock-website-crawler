import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function runBacktest() {
  const sessionFile = path.join(__dirname, 'data/session.json');
  const session = JSON.parse(fs.readFileSync(sessionFile, 'utf8'));

  const strategyFile = process.argv[2];
  if (!strategyFile) {
    console.error('Usage: node run-backtest.js <strategy-file.py>');
    process.exit(1);
  }

  const code = fs.readFileSync(strategyFile, 'utf8');
  const strategyName = path.basename(strategyFile, '.py');
  console.log('Strategy:', strategyName);
  console.log('Code length:', code.length, 'characters');

  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext();
  await context.addCookies(session.cookies);

  // Grant clipboard permissions
  try {
    await context.grantPermissions(['clipboard-read', 'clipboard-write']);
  } catch (e) {
    console.log('Clipboard permissions not supported');
  }

  const page = await context.newPage();

  // Navigate to trading list page
  console.log('Navigating to Trading List page...');
  await page.goto('https://bigquant.com/trading/list', { waitUntil: 'networkidle' });
  await page.waitForTimeout(5000);

  // Take screenshot to see current state
  await page.screenshot({ path: path.join(__dirname, 'data/trading-list.png') });
  console.log('Screenshot saved to data/trading-list.png');

  // Look for "新建策略" or "创建策略" button
  console.log('Looking for create strategy button...');

  const createButtons = await page.$$('button:has-text("新建"), button:has-text("创建"), a:has-text("新建"), a:has-text("创建")');
  console.log('Found', createButtons.length, 'create buttons');

  for (const btn of createButtons) {
    try {
      const text = await btn.textContent();
      console.log('Button text:', text?.trim());
    } catch (e) {}
  }

  // Click the first create button if found
  if (createButtons.length > 0) {
    console.log('Clicking create button...');
    await createButtons[0].click();
    await page.waitForTimeout(3000);
    await page.screenshot({ path: path.join(__dirname, 'data/after-create-click.png') });
  }

  // Write code to clipboard
  await page.evaluate((c) => navigator.clipboard.writeText(c), code);
  console.log('Code copied to clipboard');

  // Look for code editor or textarea
  const textareas = await page.$$('textarea');
  const codeEditors = await page.$$('.CodeMirror, .monaco-editor, [class*="editor"]');

  console.log('Found', textareas.length, 'textareas');
  console.log('Found', codeEditors.length, 'code editors');

  if (textareas.length > 0) {
    console.log('Filling textarea with code...');
    await textareas[0].fill(code);
    await page.waitForTimeout(1000);
  } else if (codeEditors.length > 0) {
    console.log('Clicking code editor...');
    await codeEditors[0].click();
    await page.waitForTimeout(500);

    // Select all and paste
    await page.keyboard.down('Control');
    await page.keyboard.press('A');
    await page.keyboard.up('Control');
    await page.waitForTimeout(500);

    await page.keyboard.down('Control');
    await page.keyboard.press('V');
    await page.keyboard.up('Control');
    await page.waitForTimeout(1000);
  }

  // Fill strategy name if there's a name input
  const nameInputs = await page.$$('input[type="text"], input[name="name"], input[placeholder*="名称"], input[placeholder*="名字"]');
  if (nameInputs.length > 0) {
    console.log('Filling strategy name...');
    await nameInputs[0].fill(strategyName);
  }

  await page.screenshot({ path: path.join(__dirname, 'data/code-filled.png') });

  // Look for submit/run/backtest button
  console.log('Looking for run/backtest button...');
  const runButtons = await page.$$('button:has-text("运行"), button:has-text("回测"), button:has-text("提交"), button:has-text("保存")');
  console.log('Found', runButtons.length, 'run/save buttons');

  for (const btn of runButtons) {
    try {
      const text = await btn.textContent();
      console.log('Button:', text?.trim());
    } catch (e) {}
  }

  console.log('\n====================================');
  console.log('Please check the browser window.');
  console.log('If a form is displayed, please fill it and submit manually.');
  console.log('Browser will stay open for 5 minutes.');
  console.log('====================================\n');

  await page.waitForTimeout(300000);

  await browser.close();
}

runBacktest().catch(console.error);