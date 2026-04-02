import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function runBigQuantStrategy() {
  const sessionFile = path.join(__dirname, 'data/session.json');
  const session = JSON.parse(fs.readFileSync(sessionFile, 'utf8'));

  // Read strategy code
  const strategyFile = process.argv[2];
  if (!strategyFile) {
    console.error('Usage: node run-vscode-v2.js <strategy-file.py>');
    process.exit(1);
  }

  const code = fs.readFileSync(strategyFile, 'utf8');
  console.log('Strategy file:', strategyFile);
  console.log('Code length:', code.length, 'characters');

  const browser = await chromium.launch({ headless: false, slowMo: 100 });
  const context = await browser.newContext();
  await context.addCookies(session.cookies);

  const page = await context.newPage();

  console.log('Navigating to BigQuant AIStudio...');
  await page.goto('https://bigquant.com/aistudio', { waitUntil: 'networkidle' });
  await page.waitForTimeout(8000);

  const url = page.url();
  console.log('Current URL:', url);

  if (url.includes('login')) {
    console.log('Session expired, please login manually');
    await page.waitForTimeout(60000);
    await browser.close();
    return;
  }

  // Wait for VS Code to fully load
  console.log('Waiting for VS Code to load...');
  await page.waitForSelector('.monaco-editor', { timeout: 30000 });
  await page.waitForTimeout(5000);

  await page.screenshot({ path: path.join(__dirname, 'data/vscode-ready.png') });

  // Method 1: Try to find existing Python file tab or create new one
  console.log('Looking for Python file or creating new one...');

  // Check if there's already a Python file open
  const pythonTab = await page.$('.tab:has(.label-name:has-text(".py"))');
  if (pythonTab) {
    console.log('Found existing Python file tab, clicking it...');
    await pythonTab.click();
    await page.waitForTimeout(1000);
  } else {
    // Create new file using keyboard shortcut
    console.log('Creating new Python file...');
    await page.keyboard.down('Control');
    await page.keyboard.press('N');
    await page.keyboard.up('Control');
    await page.waitForTimeout(2000);

    // Type filename
    await page.keyboard.type('strategy_backtest.py');
    await page.keyboard.press('Enter');
    await page.waitForTimeout(2000);
  }

  await page.screenshot({ path: path.join(__dirname, 'data/file-ready.png') });

  // Method 2: Use clipboard to paste code (more reliable than typing)
  console.log('Setting up code in clipboard...');

  // Grant clipboard permissions
  await context.grantPermissions(['clipboardReadWrite', 'clipboardSanitizedWrite']);

  // Write to clipboard using page.evaluate
  await page.evaluate((codeContent) => {
    return navigator.clipboard.writeText(codeContent);
  }, code);

  console.log('Code copied to clipboard');

  // Focus on the editor
  const editor = await page.$('.monaco-editor.focused, .monaco-editor');
  if (editor) {
    await editor.click({ position: { x: 100, y: 100 } });
    await page.waitForTimeout(500);

    // Select all (Ctrl+A)
    await page.keyboard.down('Control');
    await page.keyboard.press('A');
    await page.keyboard.up('Control');
    await page.waitForTimeout(500);

    // Paste (Ctrl+V)
    console.log('Pasting code from clipboard...');
    await page.keyboard.down('Control');
    await page.keyboard.press('V');
    await page.keyboard.up('Control');
    await page.waitForTimeout(2000);
  }

  await page.screenshot({ path: path.join(__dirname, 'data/code-pasted.png') });

  // Save the file
  console.log('Saving file...');
  await page.keyboard.down('Control');
  await page.keyboard.press('S');
  await page.keyboard.up('Control');
  await page.waitForTimeout(2000);

  // Look for "运行" or "Run" button in the activity bar or status bar
  console.log('Looking for run button...');

  // Try clicking on the run icon in the sidebar
  const runButtons = await page.$$('button:has-text("运行"), [title*="运行"], [title*="Run"], .run-button, [class*="run"]');
  console.log('Found', runButtons.length, 'potential run buttons');

  for (const btn of runButtons) {
    try {
      const text = await btn.textContent();
      const title = await btn.getAttribute('title');
      console.log('Button:', text?.substring(0, 30), '| Title:', title?.substring(0, 30));
    } catch (e) {}
  }

  // Try opening command palette and searching for run command
  console.log('Opening command palette to find run command...');
  await page.keyboard.down('Control');
  await page.keyboard.down('Shift');
  await page.keyboard.press('P');
  await page.keyboard.up('Shift');
  await page.keyboard.up('Control');
  await page.waitForTimeout(1000);

  // Search for BigQuant specific run command
  await page.keyboard.type('BigQuant: Run');
  await page.waitForTimeout(1000);

  await page.screenshot({ path: path.join(__dirname, 'data/run-command-search.png') });

  // List available commands in the palette
  const commands = await page.$$('.quick-input-list .label-name, .monaco-list-row');
  console.log('Available commands:');
  for (const cmd of commands.slice(0, 10)) {
    try {
      const text = await cmd.textContent();
      console.log(' -', text?.trim());
    } catch (e) {}
  }

  // Press Enter to execute first command
  await page.keyboard.press('Enter');
  await page.waitForTimeout(3000);

  await page.screenshot({ path: path.join(__dirname, 'data/after-run.png') });

  console.log('\n====================================');
  console.log('Strategy code has been pasted and saved.');
  console.log('If backtest dialog opened, please complete it manually.');
  console.log('Press Ctrl+C to close the browser when done.');
  console.log('====================================\n');

  // Wait for user to complete
  await page.waitForTimeout(300000); // 5 minutes

  await browser.close();
}

runBigQuantStrategy().catch(console.error);