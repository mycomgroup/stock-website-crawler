/**
 * Test script for different page type parsers
 */
import { chromium } from 'playwright';
import ParserManager from './src/parsers/parser-manager.js';
import MarkdownGenerator from './src/parsers/markdown-generator.js';

const testUrls = [
  // 门户首页
  { url: 'https://www.qq.com/', type: 'portal', name: 'QQ门户首页' },
  // 搜索结果页
  { url: 'https://www.baidu.com/s?wd=苹果手机', type: 'search-result', name: '百度搜索结果' },
  // 文章页 - 使用新浪真实文章
  { url: 'https://news.sina.com.cn/w/2026-03-17/doc-inhrhpmt8211552.shtml', type: 'article', name: '新浪新闻文章' },
  // 列表页 - 使用网易新闻列表
  { url: 'https://news.163.com/international/', type: 'list-page', name: '网易国际新闻列表' },
];

async function main() {
  const browser = await chromium.launch({ headless: true });
  const parserManager = new ParserManager();
  const markdownGenerator = new MarkdownGenerator();

  console.log('=== 页面解析器测试 ===\n');

  for (const test of testUrls) {
    console.log(`\n${'='.repeat(60)}`);
    console.log(`测试: ${test.name}`);
    console.log(`URL: ${test.url}`);
    console.log(`预期类型: ${test.type}`);
    console.log('='.repeat(60));

    let page;
    try {
      page = await browser.newPage();

      // 选择解析器
      const parser = parserManager.selectParser(test.url);
      console.log(`\n解析器: ${parser.constructor.name}`);

      // 访问页面
      console.log('\n加载页面...');
      await page.goto(test.url, { waitUntil: 'domcontentloaded', timeout: 30000 });
      await page.waitForTimeout(3000);

      // 解析页面
      console.log('解析页面...');
      const result = await parserManager.parse(page, test.url, {});

      // 输出结果
      console.log('\n--- 解析结果 ---');
      console.log(`类型: ${result.type}`);
      console.log(`标题: ${result.title || '(无)'}`);

      if (result.type === 'portal') {
        console.log(`\n导航数量: ${result.navigation?.length || 0}`);
        console.log(`内容区块: ${result.contentBlocks?.length || 0}`);
        console.log(`热门话题: ${result.hotTopics?.length || 0}`);
        console.log(`频道数: ${result.channels?.length || 0}`);
        if (result.contentBlocks?.length > 0) {
          console.log('\n内容区块示例:');
          result.contentBlocks.slice(0, 2).forEach((block, i) => {
            console.log(`  ${i + 1}. ${block.title}: ${block.items?.length || 0} 条`);
          });
        }
      } else if (result.type === 'search-result') {
        console.log(`搜索词: ${result.query || '(无)'}`);
        console.log(`结果数: ${result.results?.length || 0}`);
        console.log(`相关搜索: ${result.relatedSearches?.length || 0}`);
        if (result.results?.length > 0) {
          console.log('\n前3条结果:');
          result.results.slice(0, 3).forEach((r, i) => {
            console.log(`  ${i + 1}. ${r.title?.substring(0, 50)}...`);
          });
        }
      } else if (result.type === 'article') {
        console.log(`发布时间: ${result.publishTime || '(无)'}`);
        console.log(`作者: ${result.author?.name || '(无)'}`);
        console.log(`内容长度: ${result.content?.length || 0} 字符`);
        console.log(`标签: ${result.tags?.join(', ') || '(无)'}`);
        if (result.content) {
          console.log(`\n内容摘要: ${result.content.substring(0, 200)}...`);
        }
      } else if (result.type === 'list-page') {
        console.log(`列表项数: ${result.items?.length || 0}`);
        console.log(`分页: ${result.pagination?.current || 1}/${result.pagination?.total || 1}`);
        if (result.items?.length > 0) {
          console.log('\n前5条列表项:');
          result.items.slice(0, 5).forEach((item, i) => {
            console.log(`  ${i + 1}. ${item.title?.substring(0, 50) || item.text?.substring(0, 50)}...`);
          });
        }
      } else if (result.type === 'generic') {
        console.log(`描述: ${result.description?.substring(0, 100) || '(无)'}`);
        console.log(`段落: ${result.paragraphs?.length || 0}`);
        console.log(`链接: ${result.links?.length || 0}`);
      }

      // 生成 Markdown
      const markdown = markdownGenerator.generate(result);
      console.log(`\nMarkdown 长度: ${markdown.length} 字符`);
      console.log(`\nMarkdown 预览 (前500字符):\n${markdown.substring(0, 500)}...`);

    } catch (error) {
      console.error(`\n错误: ${error.message}`);
    } finally {
      if (page) {
        await page.close();
      }
    }
  }

  await browser.close();
  console.log('\n\n=== 测试完成 ===');
}

main().catch(console.error);