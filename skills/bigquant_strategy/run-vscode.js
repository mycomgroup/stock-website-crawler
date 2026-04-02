import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function runBigQuantStrategy() {
  const sessionFile = path.join(__dirname, 'data/session.json');
  const session = JSON.parse(fs.readFileSync(sessionFile, 'utf8'));

  // Read strategy code
  const strategyFile = process.argv[2] || '/Users/yuping/Downloads/git/stock-website-crawler/strategies/bigquant/pure_cash_defense.py';
  const code = fs.readFileSync(strategyFile, 'utf8');
  console.log('Strategy file:', strategyFile);
  console.log('Code length:', code.length, 'characters');

  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext();
  await context.addCookies(session.cookies);

  const page = await context.newPage();

  console.log('Navigating to BigQuant AIStudio...');
  await page.goto('https://bigquant.com/aistudio', { waitUntil: 'networkidle' });
  await page.waitForTimeout(5000);

  const url = page.url();
  console.log('Current URL:', url);

  if (url.includes('login')) {
    console.log('Session expired, please login manually');
    await page.waitForTimeout(60000);
    await browser.close();
    return;
  }

  // Wait for VS Code to load
  console.log('Waiting for VS Code to load...');
  await page.waitForTimeout(10000);

  // Take screenshot
  await page.screenshot({ path: path.join(__dirname, 'data/vscode-initial.png') });

  // Try to open command palette (Ctrl+Shift+P)
  console.log('Opening command palette...');
  await page.keyboard.down('Control');
  await page.keyboard.down('Shift');
  await page.keyboard.press('P');
  await page.keyboard.up('Shift');
  await page.keyboard.up('Control');
  await page.waitForTimeout(2000);

  await page.screenshot({ path: path.join(__dirname, 'data/command-palette.png') });

  // Type to search for "new file" command
  await page.keyboard.type('new file');
  await page.waitForTimeout(1000);

  // Press Enter to create new file
  await page.keyboard.press('Enter');
  await page.waitForTimeout(2000);

  // Type the filename
  await page.keyboard.type('strategy.py');
  await page.keyboard.press('Enter');
  await page.waitForTimeout(2000);

  await page.screenshot({ path: path.join(__dirname, 'data/new-file.png') });

  // Now paste the code - use clipboard
  console.log('Pasting code...');

  // Select all (Ctrl+A)
  await page.keyboard.down('Control');
  await page.keyboard.press('A');
  await page.keyboard.up('Control');
  await page.waitForTimeout(500);

  // We need to set clipboard content, but that's tricky
  // Instead, let's type the code directly (for small files)
  // For larger files, we'll need a different approach

  // First, let's try to find the active editor
  const monacoEditor = await page.$('.monaco-editor.focused');
  if (monacoEditor) {
    console.log('Found focused Monaco editor');

    // Click on the editor to focus
    await monacoEditor.click();
    await page.waitForTimeout(500);

    // Use Ctrl+A to select all
    await page.keyboard.down('Control');
    await page.keyboard.press('A');
    await page.keyboard.up('Control');
    await page.waitForTimeout(500);

    // Type the code (this will replace selection)
    console.log('Typing code (this may take a while for large files)...');

    // Split code into chunks and type
    const lines = code.split('\n');
    for (let i = 0; i < lines.length; i++) {
      await page.keyboard.type(lines[i]);
      await page.keyboard.press('Enter');
      if (i % 100 === 0) {
        console.log(`Typed ${i}/${lines.length} lines...`);
      }
    }
  }

  await page.screenshot({ path: path.join(__dirname, 'data/code-entered.png') });

  // Save the file (Ctrl+S)
  console.log('Saving file...');
  await page.keyboard.down('Control');
  await page.keyboard.press('S');
  await page.keyboard.up('Control');
  await page.waitForTimeout(2000);

  // Try to run the strategy
  // Look for run button or use command palette
  console.log('Trying to run strategy...');

  // Open command palette again
  await page.keyboard.down('Control');
  await page.keyboard.down('Shift');
  await page.keyboard.press('P');
  await page.keyboard.up('Shift');
  await page.keyboard.up('Control');
  await page.waitForTimeout(1000);

  // Search for run command
  await page.keyboard.type('run');
  await page.waitForTimeout(1000);

  await page.screenshot({ path: path.join(__dirname, 'data/run-command.png') });

  // Keep browser open for user to complete
  console.log('\nBrowser will stay open. Please complete the backtest manually.');
  console.log('Press Ctrl+C to close when done.');

  // Wait indefinitely
  await new Promise(() => {});
}

runBigQuantStrategy().catch(console.error);