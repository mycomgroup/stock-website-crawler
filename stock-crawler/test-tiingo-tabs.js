// Test multiple Tiingo pages with tabs
import { chromium } from 'playwright';
import TiingoApiParser from './src/parsers/tiingo-api-parser.js';
import MarkdownGenerator from './src/markdown-generator.js';
import fs from 'fs';
import path from 'path';

async function testPages() {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();

  const parser = new TiingoApiParser();
  const markdownGenerator = new MarkdownGenerator();

  const urls = [
    'https://www.tiingo.com/documentation/end-of-day',
    'https://www.tiingo.com/documentation/general/overview',
    'https://www.tiingo.com/documentation/intraday'
  ];

  const outputDir = './output/test-fix';
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  let totalIssues = 0;

  for (const url of urls) {
    console.log(`\n=== Testing: ${url} ===`);
    
    try {
      await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 });
      await parser.waitForContent(page);
      const pageData = await parser.parse(page, url);
      const markdown = markdownGenerator.generate(pageData);
      
      // Check for raw text tables (a sign of the bug)
      const rawTablePattern = /#### [A-Za-z]+\n\n[A-Z][a-z]+ [A-Z][a-z]+\n[A-Z][a-z]+ [A-Z][a-z]+\n/;
      const hasRawTable = rawTablePattern.test(markdown);
      
      if (hasRawTable) {
        console.log('❌ Found raw text table (bug not fixed)');
        totalIssues++;
      } else {
        console.log('✅ No raw text tables found');
      }
      
      // Check for proper markdown tables
      const hasProperTable = /\| [^|]+ \| [^|]+ \|/.test(markdown);
      console.log(`   Has proper markdown tables: ${hasProperTable ? '✅' : 'N/A'}`);
      
      // Save output
      const filename = url.split('/').pop() || 'index';
      const outputPath = path.join(outputDir, `${filename}.md`);
      fs.writeFileSync(outputPath, markdown);
      console.log(`   Saved to: ${outputPath}`);
      
    } catch (error) {
      console.log(`❌ Error: ${error.message}`);
      totalIssues++;
    }
  }

  await browser.close();
  
  console.log(`\n=== Summary ===`);
  console.log(`Total issues: ${totalIssues}`);
  process.exit(totalIssues > 0 ? 1 : 0);
}

testPages();
