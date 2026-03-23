import { chromium } from 'playwright';
import MassiveApiParser from '../stock-crawler/src/parsers/massive-api-parser.js';
import MarkdownGenerator from '../stock-crawler/src/markdown-generator.js';

async function test() {
  const browser = await chromium.launch({ headless: true });
  const parser = new MassiveApiParser();
  const mdGenerator = new MarkdownGenerator();

  // 使用实际存在的 URL
  const testUrls = [
    'https://massive.com/docs/rest/forex/currency-conversion',
    'https://massive.com/docs/websocket/stocks',
    'https://massive.com/docs/rest/options/contracts/all-contracts',
    'https://massive.com/docs/rest/futures/schedules/all-schedules'
  ];

  for (const url of testUrls) {
    console.log('\n' + '='.repeat(60));
    console.log('URL:', url);

    const page = await browser.newPage();
    try {
      await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 });
      await parser.waitForContent(page);

      const data = await parser.parse(page, url);

      console.log('Title:', data.title);
      console.log('Description:', data.description?.substring(0, 80) || '(none)');
      console.log('Endpoint:', data.endpoint);
      console.log('Params:', data.parameters?.length || 0);
      console.log('Response Attrs:', data.responseAttributes?.length || 0);
      console.log('Code Examples:', data.codeExamples?.length || 0);

      // 显示前几个参数
      if (data.parameters?.length > 0) {
        console.log('First params:', data.parameters.slice(0, 3).map(p => p.name).join(', '));
      }
      if (data.responseAttributes?.length > 0) {
        console.log('First attrs:', data.responseAttributes.slice(0, 3).map(p => p.name).join(', '));
      }

    } catch (e) {
      console.error('Error:', e.message);
    }
    await page.close();
  }

  await browser.close();
}

test();