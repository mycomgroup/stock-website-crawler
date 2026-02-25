/**
 * 测试分页抓取功能
 */
import { chromium } from 'playwright';
import GenericParser from '../src/parsers/generic-parser.js';

async function testPagination() {
  console.log('Testing pagination extraction...\n');
  
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext();
  const page = await context.newPage();
  
  try {
    // 访问一个有分页的测试页面
    const testUrl = 'https://www.lixinger.com/analytics/company/dashboard/rate-of-return-rank/us';
    console.log(`Navigating to: ${testUrl}`);
    
    await page.goto(testUrl, { waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForTimeout(3000);
    
    console.log('Page loaded, starting extraction...\n');
    
    const parser = new GenericParser();
    
    // 数据块回调
    const chunks = [];
    const onDataChunk = async (chunk) => {
      chunks.push(chunk);
      console.log(`Received chunk: type=${chunk.type}, table=${chunk.tableIndex + 1}, page=${chunk.page}, rows=${chunk.rows?.length || 0}`);
    };
    
    const result = await parser.parse(page, testUrl, { onDataChunk });
    
    console.log(`\n=== Extraction Complete ===`);
    console.log(`Total chunks received: ${chunks.length}`);
    console.log(`Total tables: ${result.tables.length}`);
    
    result.tables.forEach((table, index) => {
      console.log(`\nTable ${index + 1}:`);
      console.log(`  Headers: ${table.headers.length}`);
      console.log(`  Rows: ${table.rows.length}`);
      console.log(`  Total Pages: ${table.totalPages || 1}`);
      if (table.headers.length > 0) {
        console.log(`  First header: ${table.headers[0]}`);
      }
      if (table.rows.length > 0) {
        console.log(`  First row: ${table.rows[0].slice(0, 3).join(', ')}...`);
      }
    });
    
  } catch (error) {
    console.error('Error:', error.message);
    console.error(error.stack);
  } finally {
    await browser.close();
  }
}

testPagination().catch(console.error);
