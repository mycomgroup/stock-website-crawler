import AliyunBailianMcpParser from './src/parsers/aliyun-bailian-mcp-parser.js';
import MarkdownGenerator from './src/parsers/markdown-generator.js';
import { chromium } from 'playwright';

async function test() {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  
  const parser = new AliyunBailianMcpParser();
  const mdGen = new MarkdownGenerator();
  
  console.log('Loading detail page...');
  await page.goto('https://bailian.console.aliyun.com/cn-beijing/?tab=mcp#/mcp-market/detail/code_interpreter_mcp', { waitUntil: 'domcontentloaded' });
  const detailData = await parser.parse(page, 'https://bailian.console.aliyun.com/cn-beijing/?tab=mcp#/mcp-market/detail/code_interpreter_mcp');
  const detailMd = mdGen.generate(detailData);
  console.log('--- DETAIL MD ---');
  console.log(detailMd);
  
  await browser.close();
}

test().catch(console.error);
