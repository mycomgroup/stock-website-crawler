/**
 * Debug script to test yfinance parser
 */
import { chromium } from 'playwright';
import ParserManager from './src/parsers/parser-manager.js';

async function main() {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  const testUrl = 'https://www.aidoczh.com/yfinance/reference/api/yfinance.Ticker.balance_sheet.html';

  console.log(`Loading: ${testUrl}`);
  await page.goto(testUrl, { waitUntil: 'networkidle' });
  console.log('Page loaded');

  // Test parser selection
  const parserManager = new ParserManager();
  const parser = parserManager.selectParser(testUrl);
  console.log(`Selected parser: ${parser.constructor.name}`);
  console.log(`Parser priority: ${parser.getPriority()}`);

  // Parse the page
  const result = await parser.parse(page, testUrl, {});
  console.log('\n=== Parse Result ===');
  console.log(`type: ${result.type}`);
  console.log(`title: ${result.title}`);
  console.log(`apiName: ${result.apiName}`);
  console.log(`suggestedFilename: ${result.suggestedFilename}`);
  console.log(`signature: ${result.signature}`);
  console.log(`parameters count: ${result.parameters?.length || 0}`);
  console.log(`returns count: ${result.returns?.length || 0}`);
  console.log(`attributes count: ${result.attributes?.length || 0}`);
  console.log(`tables count: ${result.tables?.length || 0}`);
  console.log(`codeExamples count: ${result.codeExamples?.length || 0}`);

  // Print first few parameters if any
  if (result.parameters && result.parameters.length > 0) {
    console.log('\nFirst 3 parameters:', JSON.stringify(result.parameters.slice(0, 3), null, 2));
  }

  // Print first few methods if any
  if (result.returns && result.returns.length > 0) {
    console.log('\nFirst 3 returns/methods:', JSON.stringify(result.returns.slice(0, 3), null, 2));
  }

  await browser.close();
}

main().catch(console.error);