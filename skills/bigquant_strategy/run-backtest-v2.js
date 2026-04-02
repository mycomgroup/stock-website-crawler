import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function listStrategies(page) {
  // Get all strategy rows
  const rows = await page.$$('tr, [class*="row"], [class*="item"]');
  const strategies = [];

  for (const row of rows) {
    try {
      const nameEl = await row.$('a[href*="/trading/"], [class*="name"], td:first-child');
      if (nameEl) {
        const name = await nameEl.textContent();
        const link = await nameEl.getAttribute('href');
        if (name?.trim() && !name.includes('运行')) {
          strategies.push({
            name: name.trim(),
            link: link || '',
            row
          });
        }
      }
    } catch (e) {}
  }

  return strategies;
}

async function runBacktest() {
  const sessionFile = path.join(__dirname, 'data/session.json');
  const session = JSON.parse(fs.readFileSync(sessionFile, 'utf8'));

  const strategyFile = process.argv[2];
  if (!strategyFile) {
    console.error('Usage: node run-backtest-v2.js <strategy-file.py>');
    process.exit(1);
  }

  const code = fs.readFileSync(strategyFile, 'utf8');
  const strategyName = path.basename(strategyFile, '.py');
  console.log('Strategy:', strategyName);
  console.log('Code length:', code.length, 'characters');

  const browser = await chromium.launch({ headless: false, slowMo: 100 });
  const context = await browser.newContext();
  await context.addCookies(session.cookies);

  try {
    await context.grantPermissions(['clipboard-read', 'clipboard-write']);
  } catch (e) {}

  const page = await context.newPage();

  // Step 1: Go to trading list
  console.log('\n[Step 1] Navigating to Trading List...');
  await page.goto('https://bigquant.com/trading/list', { waitUntil: 'networkidle' });
  await page.waitForTimeout(5000);

  await page.screenshot({ path: path.join(__dirname, 'data/step1-trading-list.png') });

  // Step 2: List existing strategies
  console.log('\n[Step 2] Listing existing strategies...');

  // Try to find strategy names from the table
  const strategyRows = await page.$$('tbody tr, [class*="table"] tr');
  console.log('Found', strategyRows.length, 'rows');

  // Get all strategy links
  const strategyLinks = await page.$$('a[href*="/trading/"]');
  console.log('Found', strategyLinks.length, 'strategy links');

  for (let i = 0; i < Math.min(10, strategyLinks.length); i++) {
    const link = strategyLinks[i];
    const text = await link.textContent();
    const href = await link.getAttribute('href');
    console.log(`  ${i + 1}. "${text?.trim()}" -> ${href}`);
  }

  // Step 3: If strategies exist, navigate to the first strategy detail page
  const detailLinks = await page.$$('a[href*="/trading/detail/"]');
  if (detailLinks.length > 0) {
    const firstHref = await detailLinks[0].getAttribute('href');
    const strategyText = await detailLinks[0].textContent();
    console.log('\n[Step 3] Navigating to first strategy:', strategyText?.trim());
    console.log('URL:', 'https://bigquant.com' + firstHref);

    // Navigate directly instead of clicking
    await page.goto('https://bigquant.com' + firstHref, { waitUntil: 'networkidle' });
    await page.waitForTimeout(5000);

    const currentUrl = page.url();
    console.log('Current URL:', currentUrl);

    await page.screenshot({ path: path.join(__dirname, 'data/step3-strategy-detail.png') });

    // Step 4: Look for edit button
    console.log('\n[Step 4] Looking for edit button...');
    const editButtons = await page.$$('button:has-text("编辑"), a:has-text("编辑")');
    console.log('Found', editButtons.length, 'edit buttons');

    if (editButtons.length > 0) {
      console.log('Clicking edit button...');
      await editButtons[0].click();
      await page.waitForTimeout(5000);

      await page.screenshot({ path: path.join(__dirname, 'data/step4-edit-page.png') });

      // Step 5: Replace code
      console.log('\n[Step 5] Replacing code...');
      await page.evaluate((c) => navigator.clipboard.writeText(c), code);

      // Find code editor
      const textareas = await page.$$('textarea');
      if (textareas.length > 0) {
        console.log('Found textarea, filling with code...');
        await textareas[0].click();
        await page.keyboard.down('Control');
        await page.keyboard.press('A');
        await page.keyboard.up('Control');
        await page.waitForTimeout(300);

        await page.keyboard.down('Control');
        await page.keyboard.press('V');
        await page.keyboard.up('Control');
        await page.waitForTimeout(2000);
      }

      await page.screenshot({ path: path.join(__dirname, 'data/step5-code-replaced.png') });

      // Step 6: Save and Run
      console.log('\n[Step 6] Saving and running...');
      const saveButtons = await page.$$('button:has-text("保存")');
      if (saveButtons.length > 0) {
        await saveButtons[0].click();
        await page.waitForTimeout(3000);
      }

      const runButtons = await page.$$('button:has-text("运行回测"), button:has-text("运行")');
      if (runButtons.length > 0) {
        console.log('Clicking run button...');
        await runButtons[0].click();
        await page.waitForTimeout(5000);
      }

      await page.screenshot({ path: path.join(__dirname, 'data/step6-running.png') });
    }
  } else {
    // No existing strategies - go to AIStudio
    console.log('\n[Step 3] No strategies found, going to AIStudio...');
    await page.goto('https://bigquant.com/aistudio', { waitUntil: 'networkidle' });
    await page.waitForTimeout(10000);

    // Use VS Code shortcuts
    console.log('Creating new file...');
    await page.keyboard.down('Control');
    await page.keyboard.press('N');
    await page.keyboard.up('Control');
    await page.waitForTimeout(2000);

    await page.keyboard.type(strategyName + '.py');
    await page.keyboard.press('Enter');
    await page.waitForTimeout(2000);

    await page.evaluate((c) => navigator.clipboard.writeText(c), code);

    await page.keyboard.down('Control');
    await page.keyboard.press('V');
    await page.keyboard.up('Control');
    await page.waitForTimeout(2000);

    await page.keyboard.down('Control');
    await page.keyboard.press('S');
    await page.keyboard.up('Control');
    await page.waitForTimeout(2000);

    await page.screenshot({ path: path.join(__dirname, 'data/step3-aistudio.png') });
  }

  console.log('\n====================================');
  console.log('Automation complete.');
  console.log('Please check the browser to complete backtest setup.');
  console.log('Browser will stay open for 5 minutes.');
  console.log('====================================\n');

  await page.waitForTimeout(300000);

  await browser.close();
}

runBacktest().catch(console.error);