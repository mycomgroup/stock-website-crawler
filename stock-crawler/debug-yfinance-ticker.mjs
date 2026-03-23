
import { chromium } from 'playwright';
import YfinanceApiParser from './src/parsers/yfinance-api-parser.js';
import fs from 'fs/promises';
import path from 'path';

async function main() {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  const parser = new YfinanceApiParser();
  const testUrl = 'https://www.aidoczh.com/yfinance/reference/api/yfinance.Ticker.html';
  const outputDir = './test-yfinance-output-debug';

  console.log(`Loading: ${testUrl}`);
  try {
    await page.goto(testUrl, { waitUntil: 'networkidle' });
    console.log('Page loaded');

    // Parse the page
    const result = await parser.parse(page, testUrl, {
      pagesDir: outputDir
    });

    console.log('\n=== Parse Result ===');
    console.log(`isClassPage: ${result.isClassPage}`);
    console.log(`apiMembers count: ${result.apiMembers?.length || 0}`);
    
    if (result.apiMembers && result.apiMembers.length > 0) {
      console.log('\nFirst 5 members:');
      result.apiMembers.slice(0, 5).forEach(m => {
        console.log(`- [${m.type}] ${m.name}`);
      });

      const balanceSheet = result.apiMembers.find(m => m.name.includes('balance_sheet') || m.name.includes('balancesheet'));
      console.log('\nBalance Sheet member check:');
      if (balanceSheet) {
        console.log(`Found: ${JSON.stringify(balanceSheet, null, 2)}`);
      } else {
        console.log('Not found');
      }
    }

    // Check if files were created
    try {
      const files = await fs.readdir(outputDir);
      console.log(`\nFiles created in ${outputDir}: ${files.length}`);
      console.log(files.slice(0, 10).join(', ') + (files.length > 10 ? '...' : ''));
    } catch (e) {
      console.log(`\nError reading output dir: ${e.message}`);
    }

  } catch (error) {
    console.error('Test failed:', error);
  } finally {
    await browser.close();
  }
}

main().catch(console.error);
