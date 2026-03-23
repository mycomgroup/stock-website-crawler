// Debug script to trace markdown generation
import XiaohongshuApifoxParser from '../stock-crawler/src/parsers/xiaohongshu-apifox-parser.js';
import MarkdownGenerator from '../stock-crawler/src/markdown-generator.js';
import { chromium } from 'playwright';

async function debug() {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  console.log('Loading page...');
  await page.goto('https://xiaohongshu.apifox.cn/doc-2810928', { waitUntil: 'networkidle' });

  const parser = new XiaohongshuApifoxParser();
  console.log('Parsing page...');

  const pageData = await parser.parse(page, 'https://xiaohongshu.apifox.cn/doc-2810928', {});

  console.log('\n=== Page Data Type ===');
  console.log('type:', pageData.type);

  console.log('\n=== Generating Markdown ===');
  const gen = new MarkdownGenerator();
  const markdown = gen.generate(pageData);

  // Check table section
  const tableSectionStart = markdown.indexOf('## 表格');
  if (tableSectionStart !== -1) {
    console.log('\n=== Table Section ===');
    console.log(markdown.substring(tableSectionStart, tableSectionStart + 1500));
  }

  await browser.close();
}

debug().catch(console.error);