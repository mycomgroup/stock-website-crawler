import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function runBigQuantStrategy() {
  const sessionFile = path.join(__dirname, 'data/session.json');
  const session = JSON.parse(fs.readFileSync(sessionFile, 'utf8'));

  const strategyFile = process.argv[2];
  if (!strategyFile) {
    console.error('Usage: node run-vscode-v3.js <strategy-file.py>');
    process.exit(1);
  }

  const code = fs.readFileSync(strategyFile, 'utf8');
  console.log('Strategy file:', strategyFile);
  console.log('Code length:', code.length, 'characters');

  const browser = await chromium.launch({ headless: false, slowMo: 50 });
  const context = await browser.newContext();
  await context.addCookies(session.cookies);

  // Grant clipboard permissions
  // Note: clipboardReadWrite may not be supported in all browsers
  try {
    await context.grantPermissions(['clipboard-read', 'clipboard-write']);
  } catch (e) {
    console.log('Clipboard permissions not supported, continuing anyway...');
  }

  const page = await context.newPage();

  console.log('Navigating to BigQuant AIStudio...');
  await page.goto('https://bigquant.com/aistudio', { waitUntil: 'networkidle' });
  await page.waitForTimeout(10000); // Wait longer for VS Code to load

  const url = page.url();
  console.log('Current URL:', url);

  // Take screenshot to see current state
  await page.screenshot({ path: path.join(__dirname, 'data/vscode-state.png'), fullPage: true });
  console.log('Screenshot saved to data/vscode-state.png');

  if (url.includes('login')) {
    console.log('Session expired, please login manually');
    await page.waitForTimeout(60000);
    await browser.close();
    return;
  }

  // Write code to clipboard
  await page.evaluate((codeContent) => {
    return navigator.clipboard.writeText(codeContent);
  }, code);
  console.log('Code copied to clipboard');

  // Wait for page to be interactive
  await page.waitForTimeout(5000);

  // Try multiple methods to interact with the editor
  console.log('Trying to interact with the editor...');

  // Method 1: Try to find any clickable element that might be an editor
  const clickableAreas = await page.$$('[role="textbox"], .editor-container, .monaco-editor, .view-lines');
  console.log('Found', clickableAreas.length, 'potential editor areas');

  // Method 2: Use keyboard shortcuts directly
  // First, let's try to create a new file
  console.log('Creating new file with Ctrl+N...');
  await page.keyboard.down('Control');
  await page.keyboard.press('N');
  await page.keyboard.up('Control');
  await page.waitForTimeout(2000);

  // Type filename
  console.log('Typing filename...');
  await page.keyboard.type('backtest_strategy.py');
  await page.keyboard.press('Enter');
  await page.waitForTimeout(3000);

  await page.screenshot({ path: path.join(__dirname, 'data/after-new-file.png') });

  // Now paste the code
  console.log('Pasting code with Ctrl+V...');
  await page.keyboard.down('Control');
  await page.keyboard.press('V');
  await page.keyboard.up('Control');
  await page.waitForTimeout(3000);

  await page.screenshot({ path: path.join(__dirname, 'data/after-paste.png') });

  // Save the file
  console.log('Saving file with Ctrl+S...');
  await page.keyboard.down('Control');
  await page.keyboard.press('S');
  await page.keyboard.up('Control');
  await page.waitForTimeout(2000);

  await page.screenshot({ path: path.join(__dirname, 'data/after-save.png') });

  // Look for run button - search for Chinese "运行" or play icon
  console.log('Looking for run button...');

  // Take a screenshot of current state
  await page.screenshot({ path: path.join(__dirname, 'data/before-run.png'), fullPage: true });

  // Get all buttons
  const allButtons = await page.$$('button');
  console.log('Found', allButtons.length, 'buttons on the page');

  // Try to find and click run-related buttons
  for (const btn of allButtons) {
    try {
      const text = await btn.textContent();
      const title = await btn.getAttribute('title');
      const className = await btn.getAttribute('class');

      if (text?.includes('运行') || text?.includes('Run') ||
          title?.includes('运行') || title?.includes('Run') ||
          className?.includes('run')) {
        console.log('Found potential run button:', text?.substring(0, 30), '|', title?.substring(0, 30));
      }
    } catch (e) {}
  }

  // Look in the activity bar (left sidebar) and status bar
  console.log('Checking activity bar and status bar...');

  // Click on the activity bar items
  const activityBarItems = await page.$$('.activitybar .action-item, [class*="activity-bar"] button');
  console.log('Found', activityBarItems.length, 'activity bar items');

  // Try keyboard shortcut for running (F5 or Ctrl+F5)
  console.log('Trying F5 to run...');
  await page.keyboard.press('F5');
  await page.waitForTimeout(3000);

  await page.screenshot({ path: path.join(__dirname, 'data/after-f5.png') });

  console.log('\n====================================');
  console.log('Automation steps completed.');
  console.log('Please check the browser window and complete any manual steps.');
  console.log('The browser will stay open for 5 minutes.');
  console.log('Press Ctrl+C to close earlier.');
  console.log('====================================\n');

  // Keep browser open
  await page.waitForTimeout(300000);

  await browser.close();
}

runBigQuantStrategy().catch(console.error);