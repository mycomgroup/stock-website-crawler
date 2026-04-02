import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function captureNetworkRequests() {
  const sessionFile = path.join(__dirname, 'data/session.json');
  const session = JSON.parse(fs.readFileSync(sessionFile, 'utf8'));

  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext();
  await context.addCookies(session.cookies);

  const page = await context.newPage();

  // Capture all network requests
  const requests = [];

  page.on('request', request => {
    const url = request.url();
    const method = request.method();
    const postData = request.postData();

    // Filter for API calls
    if (url.includes('/api/') || url.includes('backtest') || url.includes('strategy') || url.includes('run')) {
      requests.push({
        timestamp: Date.now(),
        method,
        url,
        postData: postData?.substring(0, 500)
      });
      console.log(`[${method}] ${url}`);
      if (postData) {
        console.log(`  Body: ${postData.substring(0, 200)}...`);
      }
    }
  });

  page.on('response', async response => {
    const url = response.url();
    const status = response.status();

    if (url.includes('/api/') || url.includes('backtest') || url.includes('strategy') || url.includes('run')) {
      try {
        const body = await response.text();
        console.log(`  Response [${status}]: ${body.substring(0, 300)}...`);

        const req = requests.find(r => r.url === url);
        if (req) {
          req.responseStatus = status;
          req.responseBody = body.substring(0, 1000);
        }
      } catch (e) {
        console.log(`  Response [${status}]: (unable to read body)`);
      }
    }
  });

  console.log('Navigating to BigQuant AIStudio...');
  await page.goto('https://bigquant.com/aistudio', { waitUntil: 'networkidle' });
  await page.waitForTimeout(10000);

  console.log('\n=== Trying to find and click Run button ===');

  // Try pressing F5 or looking for run button
  await page.keyboard.press('F5');
  await page.waitForTimeout(5000);

  // Look for any dialogs or backtest UI
  const dialogs = await page.$$('.ant-modal, [role="dialog"]');
  console.log('Found', dialogs.length, 'dialogs');

  await page.screenshot({ path: path.join(__dirname, 'data/network-capture.png') });

  // Wait for user to manually interact and trigger API calls
  console.log('\n=== Please manually interact with the page to trigger API calls ===');
  console.log('Browser will stay open for 60 seconds...');
  await page.waitForTimeout(60000);

  // Save captured requests
  const outputPath = path.join(__dirname, 'data/captured-requests.json');
  fs.writeFileSync(outputPath, JSON.stringify(requests, null, 2));
  console.log(`\nCaptured ${requests.length} API requests`);
  console.log('Saved to:', outputPath);

  await browser.close();
}

captureNetworkRequests().catch(console.error);