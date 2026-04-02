import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function createAndRunStrategy() {
  const sessionFile = path.join(__dirname, 'data/session.json');
  const session = JSON.parse(fs.readFileSync(sessionFile, 'utf8'));

  const strategyFile = process.argv[2];
  if (!strategyFile) {
    console.error('Usage: node create-strategy.js <strategy-file.py>');
    process.exit(1);
  }

  const code = fs.readFileSync(strategyFile, 'utf8');
  const strategyName = path.basename(strategyFile, '.py');
  console.log('Strategy:', strategyName);
  console.log('Code length:', code.length, 'characters');

  const browser = await chromium.launch({ headless: false, slowMo: 200 });
  const context = await browser.newContext();
  await context.addCookies(session.cookies);

  try {
    await context.grantPermissions(['clipboard-read', 'clipboard-write']);
  } catch (e) {}

  const page = await context.newPage();

  // Step 1: Go to AIStudio
  console.log('\n[Step 1] Navigating to BigQuant AIStudio...');
  await page.goto('https://bigquant.com/aistudio/landing', { waitUntil: 'networkidle' });
  await page.waitForTimeout(8000);

  await page.screenshot({ path: path.join(__dirname, 'data/create-step1.png') });

  // Check if there's a "新建策略" or similar button
  const createButtons = await page.$$('button:has-text("新建"), button:has-text("创建"), a:has-text("新建"), [class*="create"], [class*="new"]');
  console.log('Found', createButtons.length, 'create buttons');

  // Step 2: Click on "编写策略" or similar to enter editor
  console.log('\n[Step 2] Looking for strategy editor entry...');
  const editorLinks = await page.$$('a[href*="aistudio"]');
  for (const link of editorLinks) {
    const text = await link.textContent();
    const href = await link.getAttribute('href');
    console.log('Link:', text?.trim(), '->', href);
  }

  // Go directly to AIStudio editor
  await page.goto('https://bigquant.com/aistudio', { waitUntil: 'networkidle' });
  await page.waitForTimeout(10000);

  await page.screenshot({ path: path.join(__dirname, 'data/create-step2.png') });
  console.log('Current URL:', page.url());

  // Step 3: Create new file using VS Code keyboard shortcut
  console.log('\n[Step 3] Creating new Python file...');

  // Copy code to clipboard
  await page.evaluate((c) => navigator.clipboard.writeText(c), code);
  console.log('Code copied to clipboard');

  // Use Ctrl+N to create new file
  await page.keyboard.down('Control');
  await page.keyboard.press('N');
  await page.keyboard.up('Control');
  await page.waitForTimeout(3000);

  // Type filename
  await page.keyboard.type(strategyName + '.py');
  await page.keyboard.press('Enter');
  await page.waitForTimeout(3000);

  await page.screenshot({ path: path.join(__dirname, 'data/create-step3.png') });

  // Step 4: Paste code
  console.log('\n[Step 4] Pasting code...');
  await page.keyboard.down('Control');
  await page.keyboard.press('V');
  await page.keyboard.up('Control');
  await page.waitForTimeout(3000);

  // Step 5: Save file
  console.log('\n[Step 5] Saving file...');
  await page.keyboard.down('Control');
  await page.keyboard.press('S');
  await page.keyboard.up('Control');
  await page.waitForTimeout(3000);

  await page.screenshot({ path: path.join(__dirname, 'data/create-step5.png') });

  // Step 6: Run backtest - look for BigQuant specific run button
  console.log('\n[Step 6] Looking for backtest run button...');

  // Try keyboard shortcut for running
  await page.keyboard.press('F5');
  await page.waitForTimeout(5000);

  await page.screenshot({ path: path.join(__dirname, 'data/create-step6.png') });

  // Step 7: Wait for backtest dialog and fill parameters
  console.log('\n[Step 7] Looking for backtest configuration...');

  // Check for any dialogs
  const dialogs = await page.$$('.ant-modal, [role="dialog"], .dialog');
  console.log('Found', dialogs.length, 'potential dialogs');

  // Look for input fields (start date, end date, capital)
  const inputs = await page.$$('input[type="text"], input[type="date"], input[type="number"]');
  console.log('Found', inputs.length, 'input fields');

  // Fill backtest parameters if found
  if (inputs.length >= 3) {
    // Typical order: start date, end date, capital
    console.log('Filling backtest parameters...');

    // Start date
    await inputs[0].click();
    await inputs[0].fill('2021-01-01');

    // End date
    await inputs[1].click();
    await inputs[1].fill('2025-03-28');

    // Capital
    await inputs[2].click();
    await inputs[2].fill('100000');
  }

  await page.screenshot({ path: path.join(__dirname, 'data/create-step7.png') });

  // Look for submit button
  const submitButtons = await page.$$('button:has-text("确定"), button:has-text("运行"), button:has-text("开始"), button:has-text("提交")');
  if (submitButtons.length > 0) {
    console.log('Clicking submit button...');
    await submitButtons[0].click();
    await page.waitForTimeout(5000);
  }

  await page.screenshot({ path: path.join(__dirname, 'data/create-final.png') });

  console.log('\n====================================');
  console.log('Strategy creation complete!');
  console.log('Please check the browser to verify and run the backtest.');
  console.log('Browser will stay open for 5 minutes.');
  console.log('====================================\n');

  await page.waitForTimeout(300000);

  await browser.close();
}

createAndRunStrategy().catch(console.error);