/**
 * 测试 hao123 导航站链接的解析效果
 */
import { chromium } from 'playwright';
import ParserManager from '../stock-crawler/src/parsers/parser-manager.js';
import MarkdownGenerator from '../stock-crawler/src/parsers/markdown-generator.js';

// 限制测试数量，避免耗时过长
const MAX_LINKS = 30;
const TIMEOUT = 20000;
const SKIP_BAIDU_SEARCH = true; // 跳过百度搜索结果页

async function main() {
  const browser = await chromium.launch({ headless: true });
  const parserManager = new ParserManager();
  const markdownGenerator = new MarkdownGenerator();

  console.log('=== hao123 链接解析测试 ===\n');

  // 第一步：获取 hao123 首页的链接
  console.log('正在获取 hao123 首页链接...\n');

  let page;
  try {
    page = await browser.newPage();
    await page.goto('https://www.hao123.com/', { waitUntil: 'domcontentloaded', timeout: 30000 });
    await page.waitForTimeout(3000);

    // 提取所有链接
    const links = await page.evaluate(() => {
      const results = [];
      const seen = new Set();

      // 提取主要链接区域
      const linkEls = document.querySelectorAll('a[href^="http"]');
      linkEls.forEach(el => {
        const href = el.href;
        const text = el.textContent.trim();

        // 过滤掉 hao123 自身链接和无效链接
        if (href && !href.includes('hao123.com') && !seen.has(href) && text.length > 0 && text.length < 50) {
          seen.add(href);
          results.push({ href, text });
        }
      });

      return results;
    });

    await page.close();

    // 过滤掉百度搜索结果页
    let filteredLinks = links;
    if (SKIP_BAIDU_SEARCH) {
      filteredLinks = links.filter(l =>
        !l.href.includes('baidu.com/s?') &&
        !l.href.includes('baidu.com/s?wd') &&
        !l.href.includes('tn=50000')
      );
    }

    console.log(`找到 ${links.length} 个链接，过滤后 ${filteredLinks.length} 个，选取前 ${MAX_LINKS} 个进行测试\n`);

    // 第二步：测试每个链接
    const testLinks = filteredLinks.slice(0, MAX_LINKS);
    const results = [];

    for (let i = 0; i < testLinks.length; i++) {
      const link = testLinks[i];
      console.log(`\n${'='.repeat(60)}`);
      console.log(`[${i + 1}/${testLinks.length}] ${link.text}`);
      console.log(`URL: ${link.href}`);
      console.log('='.repeat(60));

      let testPage;
      try {
        testPage = await browser.newPage();

        await testPage.goto(link.href, { waitUntil: 'domcontentloaded', timeout: TIMEOUT });
        await testPage.waitForTimeout(2000);

        // 使用异步选择器（支持内容检测）
        const parser = await parserManager.selectParserAsync(testPage, link.href);
        console.log(`解析器: ${parser.constructor.name}`);

        const result = await parserManager.parse(testPage, link.href, {});
        console.log(`\n--- 解析结果 ---`);
        console.log(`类型: ${result.type}${result.subtype ? ` (${result.subtype})` : ''}`);
        console.log(`标题: ${result.title?.substring(0, 50) || '(无)'}`);

        // 显示内容检测结果（如果有）
        if (result.pageFeatures) {
          console.log(`页面特征: ${result.pageFeatures.suggestedType} (置信度: ${result.pageFeatures.confidence})`);
          if (result.pageFeatures.signals?.length > 0) {
            console.log(`特征信号: ${result.pageFeatures.signals.join(', ')}`);
          }
        }

        // 根据类型显示关键信息
        const summary = getSummary(result);
        if (summary) {
          console.log(summary);
        }

        // 生成 Markdown
        const markdown = markdownGenerator.generate(result);
        console.log(`\nMarkdown 长度: ${markdown.length} 字符`);

        results.push({
          url: link.href,
          text: link.text,
          parser: parser.constructor.name,
          type: result.type,
          title: result.title,
          markdownLength: markdown.length,
          success: true
        });

      } catch (error) {
        console.error(`\n错误: ${error.message}`);
        results.push({
          url: link.href,
          text: link.text,
          parser: 'Error',
          success: false,
          error: error.message
        });
      } finally {
        if (testPage) {
          await testPage.close();
        }
      }
    }

    // 输出汇总
    console.log('\n\n' + '='.repeat(60));
    console.log('=== 测试汇总 ===');
    console.log('='.repeat(60));

    const successCount = results.filter(r => r.success).length;
    console.log(`\n成功: ${successCount}/${results.length}`);

    // 按解析器统计
    const parserStats = {};
    results.forEach(r => {
      if (!parserStats[r.parser]) {
        parserStats[r.parser] = { total: 0, success: 0 };
      }
      parserStats[r.parser].total++;
      if (r.success) parserStats[r.parser].success++;
    });

    console.log('\n解析器使用统计:');
    Object.entries(parserStats)
      .sort((a, b) => b[1].total - a[1].total)
      .forEach(([parser, stats]) => {
        console.log(`  ${parser}: ${stats.success}/${stats.total} 成功`);
      });

    // 按类型统计
    const typeStats = {};
    results.filter(r => r.success).forEach(r => {
      if (!typeStats[r.type]) typeStats[r.type] = 0;
      typeStats[r.type]++;
    });

    console.log('\n页面类型统计:');
    Object.entries(typeStats)
      .sort((a, b) => b[1] - a[1])
      .forEach(([type, count]) => {
        console.log(`  ${type}: ${count} 个`);
      });

    // 显示详细结果
    console.log('\n详细结果:');
    results.forEach((r, i) => {
      const status = r.success ? '✓' : '✗';
      console.log(`  ${status} [${i + 1}] ${r.text?.substring(0, 20)} - ${r.parser} -> ${r.type || 'error'}`);
    });

  } catch (error) {
    console.error('主流程错误:', error.message);
  } finally {
    await browser.close();
  }
}

/**
 * 根据页面类型生成摘要信息
 */
function getSummary(result) {
  const lines = [];

  if (result.type === 'portal') {
    lines.push(`导航数量: ${result.navigation?.length || 0}`);
    lines.push(`内容区块: ${result.contentBlocks?.length || 0}`);
    lines.push(`热门话题: ${result.hotTopics?.length || 0}`);
  } else if (result.type === 'search-result') {
    lines.push(`搜索词: ${result.query || '(无)'}`);
    lines.push(`结果数: ${result.results?.length || 0}`);
  } else if (result.type === 'article') {
    lines.push(`发布时间: ${result.publishTime || '(无)'}`);
    lines.push(`作者: ${result.author?.name || '(无)'}`);
    lines.push(`内容长度: ${result.content?.length || 0} 字符`);
  } else if (result.type === 'list-page') {
    lines.push(`列表项数: ${result.listItems?.length || 0}`);
  } else if (result.type === 'ecommerce-product') {
    lines.push(`价格: ${result.price?.current || '(无)'}`);
    lines.push(`品牌: ${result.brand || '(无)'}`);
  } else if (result.type === 'ecommerce-list') {
    lines.push(`商品数: ${result.products?.length || 0}`);
  } else if (result.type === 'generic') {
    lines.push(`描述: ${result.description?.substring(0, 50) || '(无)'}`);
    lines.push(`段落: ${result.paragraphs?.length || 0}`);
    lines.push(`链接: ${result.links?.length || 0}`);
    if (result.pageFeatures) {
      lines.push(`建议类型: ${result.pageFeatures.suggestedType}`);
    }
  } else {
    // API 文档类型
    if (result.endpoints) {
      lines.push(`API端点数: ${result.endpoints?.length || 0}`);
    }
    if (result.functions) {
      lines.push(`函数数: ${result.functions?.length || 0}`);
    }
  }

  return lines.length > 0 ? lines.join('\n') : null;
}

main().catch(console.error);