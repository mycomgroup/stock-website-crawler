/**
 * Debug script to test eodhd parser for UI noise filtering
 */
import { chromium } from 'playwright';
import EodhdApiParser from '../stock-crawler/src/parsers/eodhd-api-parser.js';

async function main() {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  const parser = new EodhdApiParser();
  const testUrl = 'https://eodhd.com/financial-apis/live-realtime-stocks-api/';

  console.log(`Loading: ${testUrl}`);
  await page.goto(testUrl, { waitUntil: 'domcontentloaded' });
  await page.waitForSelector('h1', { timeout: 15000 });
  await page.waitForTimeout(3000);
  console.log('Page loaded');

  // Parse the page
  const result = await parser.parse(page, testUrl, {});
  console.log('\n=== Parse Result ===');
  console.log(`type: ${result.type}`);
  console.log(`title: ${result.title}`);
  console.log(`description: ${result.description?.substring(0, 200)}...`);

  // Check for UI noise
  const hasSignUp = result.description?.toLowerCase().includes('sign up');
  const hasGetData = result.description?.toLowerCase().includes('get data') && result.description?.length < 50;
  const markdownHasUINoise = result.markdownContent?.includes('Sign up & Get Data');

  console.log('\n=== UI Noise Check ===');
  console.log(`Description has "sign up": ${hasSignUp}`);
  console.log(`Description has short "get data": ${hasGetData}`);
  console.log(`Markdown has "Sign up & Get Data": ${markdownHasUINoise}`);

  if (markdownHasUINoise) {
    const lines = result.markdownContent.split('\n');
    const noiseLines = lines.filter(l => l.includes('Sign up') || l.includes('Get Data'));
    console.log('\nLines with UI noise:');
    noiseLines.forEach(l => console.log(`  "${l}"`));
  }

  console.log('\n=== Markdown Content (first 1500 chars) ===');
  console.log(result.markdownContent?.substring(0, 1500));

  await browser.close();
}

main().catch(console.error);