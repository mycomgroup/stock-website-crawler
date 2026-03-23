/**
 * 测试脚本：检查 EODHD 解析器提取的内容
 */
import { chromium } from 'playwright';
import EodhdApiParser from '../stock-crawler/src/parsers/eodhd-api-parser.js';

async function testParser() {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  const testUrl = 'https://eodhd.com/financial-apis/live-ohlcv-stocks-api';
  console.log(`正在访问: ${testUrl}`);

  await page.goto(testUrl, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await page.waitForTimeout(5000);

  const parser = new EodhdApiParser();
  const result = await parser.parse(page, testUrl);

  console.log('\n=== 解析结果 ===\n');
  console.log('标题:', result.title);
  console.log('描述:', result.description?.substring(0, 200));
  console.log('端点:', result.endpoint);
  console.log('参数数量:', result.parameters?.length || 0);
  console.log('章节数量:', result.sections?.length || 0);
  console.log('代码示例数量:', result.codeExamples?.length || 0);
  console.log('原始内容长度:', result.rawContent?.length || 0);
  console.log('Markdown 长度:', result.markdownContent?.length || 0);

  console.log('\n=== Markdown 内容 ===\n');
  console.log(result.markdownContent);

  console.log('\n=== 章节内容 ===');
  if (result.sections && result.sections.length > 0) {
    result.sections.forEach((s, i) => {
      console.log(`\n章节 ${i+1}: ${s.title}`);
      console.log(s.content?.substring(0, 300));
    });
  }

  await browser.close();
}

testParser().catch(console.error);