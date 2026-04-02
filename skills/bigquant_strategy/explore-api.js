import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function exploreBigQuantAPI() {
  const sessionFile = path.join(__dirname, 'data/session.json');
  const session = JSON.parse(fs.readFileSync(sessionFile, 'utf8'));

  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext();
  await context.addCookies(session.cookies);

  const page = await context.newPage();

  // Capture all XHR/Fetch requests
  const requests = [];

  page.on('request', request => {
    const url = request.url();
    const method = request.method();
    const postData = request.postData();
    const headers = request.headers();

    // Only capture API calls
    if (!url.includes('.js') && !url.includes('.css') && !url.includes('.png') && !url.includes('.svg')) {
      const req = {
        timestamp: new Date().toISOString(),
        method,
        url,
        postData: postData ? postData.substring(0, 1000) : null,
        contentType: headers['content-type']
      };
      requests.push(req);
      console.log(`[${method}] ${url.substring(0, 100)}`);
    }
  });

  page.on('response', async response => {
    const url = response.url();
    const status = response.status();
    const headers = response.headers();

    if (!url.includes('.js') && !url.includes('.css') && !url.includes('.png') && !url.includes('.svg')) {
      try {
        const contentType = headers['content-type'] || '';
        let body = '';
        if (contentType.includes('json')) {
          body = await response.text();
          body = body.substring(0, 2000);
        }
        console.log(`  -> [${status}] ${body.substring(0, 200)}`);

        const req = requests.find(r => r.url === url && !r.response);
        if (req) {
          req.response = { status, body };
        }
      } catch (e) {}
    }
  });

  // Visit different pages to discover API endpoints
  const pages = [
    { name: 'Trading List', url: 'https://bigquant.com/trading/list' },
    { name: 'API Docs', url: 'https://bigquant.com/wiki' },
    { name: 'AIStudio', url: 'https://bigquant.com/aistudio' },
  ];

  for (const p of pages) {
    console.log(`\n=== Visiting ${p.name}: ${p.url} ===`);
    await page.goto(p.url, { waitUntil: 'networkidle' });
    await page.waitForTimeout(5000);

    // Try clicking on elements that might trigger API calls
    const buttons = await page.$$('button');
    console.log(`Found ${buttons.length} buttons`);

    // Look for specific API-related buttons
    for (const btn of buttons) {
      try {
        const text = await btn.textContent();
        if (text?.includes('运行') || text?.includes('回测') || text?.includes('API')) {
          console.log(`  Button: "${text?.trim()}"`);
        }
      } catch (e) {}
    }

    await page.screenshot({ path: path.join(__dirname, `data/api-explore-${p.name.toLowerCase().replace(' ', '-')}.png`) });
  }

  // Try to find BigQuant API documentation
  console.log('\n=== Searching for API documentation ===');

  // Check if there's an API page
  await page.goto('https://bigquant.com/api', { waitUntil: 'networkidle' }).catch(() => {});
  await page.waitForTimeout(3000);

  await page.goto('https://bigquant.com/doc/api', { waitUntil: 'networkidle' }).catch(() => {});
  await page.waitForTimeout(3000);

  // Save all captured requests
  const outputPath = path.join(__dirname, 'data/bigquant-api-discovery.json');
  fs.writeFileSync(outputPath, JSON.stringify(requests, null, 2));
  console.log(`\n=== Captured ${requests.length} requests ===`);
  console.log('Saved to:', outputPath);

  // Group by host and path
  const apiEndpoints = {};
  for (const req of requests) {
    try {
      const url = new URL(req.url);
      const key = `${url.hostname}${url.pathname}`;
      if (!apiEndpoints[key]) {
        apiEndpoints[key] = { methods: [], urls: [] };
      }
      if (!apiEndpoints[key].methods.includes(req.method)) {
        apiEndpoints[key].methods.push(req.method);
      }
      apiEndpoints[key].urls.push(req.url.substring(0, 150));
    } catch (e) {}
  }

  console.log('\n=== Unique API Endpoints ===');
  for (const [key, value] of Object.entries(apiEndpoints)) {
    if (key.includes('api') || key.includes('backtest') || key.includes('strategy') || key.includes('trading')) {
      console.log(`${value.methods.join(',')} ${key}`);
    }
  }

  console.log('\nBrowser will stay open for 60 seconds for manual exploration...');
  await page.waitForTimeout(60000);

  await browser.close();
}

exploreBigQuantAPI().catch(console.error);