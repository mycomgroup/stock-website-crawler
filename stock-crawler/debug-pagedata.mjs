// Debug script to check pageData structure
import XiaohongshuApifoxParser from './src/parsers/xiaohongshu-apifox-parser.js';
import { chromium } from 'playwright';

async function debug() {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  console.log('Loading page...');
  await page.goto('https://xiaohongshu.apifox.cn/doc-2810928', { waitUntil: 'networkidle' });

  const parser = new XiaohongshuApifoxParser();
  console.log('Parsing page...');

  const pageData = await parser.parse(page, 'https://xiaohongshu.apifox.cn/doc-2810928', {});

  console.log('=== Page Data Type ===');
  console.log('type:', pageData.type);
  console.log('subtype:', pageData.subtype);

  console.log('\n=== Main Content Length ===');
  console.log('mainContent length:', pageData.mainContent?.length || 0);

  console.log('\n=== Tables ===');
  console.log('tables count:', pageData.tables?.length || 0);

  if (pageData.tables && pageData.tables.length > 0) {
    console.log('\nFirst table has precedingContent:', pageData.tables[0].precedingContent?.length || 0);
    if (pageData.tables[0].precedingContent) {
      console.log('First table precedingContent:', JSON.stringify(pageData.tables[0].precedingContent, null, 2));
    }
  }

  if (pageData.mainContent && pageData.mainContent.length > 0) {
    const tableItems = pageData.mainContent.filter(item => item.type === 'table');
    console.log('\nTables in mainContent:', tableItems.length);
    if (tableItems.length > 0) {
      console.log('First mainContent table has precedingContent:', tableItems[0].precedingContent?.length || 0);
    }
  }

  await browser.close();
}

debug().catch(console.error);