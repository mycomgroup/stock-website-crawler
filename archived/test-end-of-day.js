// Test script to crawl Tiingo end-of-day page specifically
import { chromium } from 'playwright';
import TiingoApiParser from '../stock-crawler/src/parsers/tiingo-api-parser.js';
import MarkdownGenerator from '../stock-crawler/src/markdown-generator.js';
import fs from 'fs';
import path from 'path';

async function testEndOfDayPage() {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();

  const parser = new TiingoApiParser();
  const markdownGenerator = new MarkdownGenerator();

  const url = 'https://www.tiingo.com/documentation/end-of-day';

  console.log(`Testing: ${url}`);

  try {
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 });
    await parser.waitForContent(page);

    const pageData = await parser.parse(page, url);

    console.log('\n=== Page Info ===');
    console.log('Title:', pageData.title);
    console.log('Tables found:', pageData.tables?.length || 0);
    console.log('Tab contents found:', pageData.tabContents?.length || 0);

    if (pageData.tabContents && pageData.tabContents.length > 0) {
      console.log('\n=== Tab Contents ===');
      for (const tab of pageData.tabContents) {
        console.log(`\nTab: ${tab.name}`);
        console.log('Tables:', tab.tables?.length || 0);
        if (tab.tables && tab.tables.length > 0) {
          for (let i = 0; i < tab.tables.length; i++) {
            const table = tab.tables[i];
            console.log(`  Table ${i + 1}: ${table.length} rows, ${table[0]?.length || 0} cols`);
            console.log('  Headers:', table[0]);
          }
        }
      }
    }

    // Generate markdown
    const markdown = markdownGenerator.generate(pageData);

    // Save to test output
    const outputDir = './output/test-fix';
    if (!fs.existsSync(outputDir)) {
      fs.mkdirSync(outputDir, { recursive: true });
    }

    const outputPath = path.join(outputDir, 'end-of-day-test.md');
    fs.writeFileSync(outputPath, markdown);

    console.log(`\n=== Markdown saved to: ${outputPath} ===`);

    // Check if the Response tab is properly handled (should be skipped since table duplicates main content)
    // Use simpler pattern to capture Tab 内容 section
    const tabSectionStart = markdown.indexOf('### 2.1.1 Overview - Tab 内容');
    if (tabSectionStart !== -1) {
      console.log('\n=== Tab Section Check ===');
      // Get all text from the tab section to the end
      const sectionText = markdown.substring(tabSectionStart);

      // Check that Response tab is NOT present (since its table duplicates main content)
      const hasResponseTab = sectionText.includes('#### Response');
      if (hasResponseTab) {
        console.log('❌ Response tab is present (should be skipped since table duplicates main content)');
      } else {
        console.log('✅ Response tab correctly skipped (table duplicates main content)');
      }

      // Check that Request tab has properly formatted table
      const hasRequestTable = sectionText.includes('#### Request') && sectionText.includes('| Field Name | Parameter');
      if (hasRequestTable) {
        console.log('✅ Request tab has properly formatted Markdown table');
      } else {
        console.log('❌ Request tab table not found or not formatted');
        console.log('DEBUG: #### Request present:', sectionText.includes('#### Request'));
        console.log('DEBUG: | Field Name | Parameter present:', sectionText.includes('| Field Name | Parameter'));
      }

      // Check that Examples tab has code blocks
      const hasExamplesCode = sectionText.includes('#### Examples') && sectionText.includes('```text');
      if (hasExamplesCode) {
        console.log('✅ Examples tab has code blocks');
      } else {
        console.log('❌ Examples tab code blocks not found');
        console.log('DEBUG: #### Examples present:', sectionText.includes('#### Examples'));
        console.log('DEBUG: ```text present:', sectionText.includes('```text'));
      }
    } else {
      console.log('\n❌ Tab section not found in markdown');
    }

  } catch (error) {
    console.error('Error:', error.message);
  } finally {
    await browser.close();
  }
}

testEndOfDayPage();