#!/usr/bin/env node

/**
 * 测试虚拟表格提取功能
 * 
 * 用法:
 *   node scripts/test-virtual-table.js <url>
 * 
 * 示例:
 *   node scripts/test-virtual-table.js https://example.com/virtual-table-page
 */

import { chromium } from 'playwright';
import GenericParser from '../src/parsers/generic-parser.js';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

async function testVirtualTable(url) {
  console.log('='.repeat(80));
  console.log('虚拟表格提取功能测试');
  console.log('='.repeat(80));
  console.log(`测试URL: ${url}`);
  console.log('');

  let browser;
  let context;

  try {
    // 启动浏览器
    console.log('启动浏览器...');
    browser = await chromium.launch({
      headless: false, // 非无头模式，方便观察
      slowMo: 100 // 减慢操作速度，方便观察
    });

    context = await browser.newContext({
      viewport: { width: 1920, height: 1080 },
      userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    });

    const page = await context.newPage();

    // 导航到页面
    console.log('导航到页面...');
    await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForTimeout(2000);

    // 创建解析器
    const parser = new GenericParser();

    // 数据块回调
    let chunkCount = 0;
    const onDataChunk = (chunk) => {
      chunkCount++;
      console.log(`\n[数据块 ${chunkCount}]`);
      console.log(`  类型: ${chunk.type}`);
      
      if (chunk.type === 'table') {
        console.log(`  表格索引: ${chunk.tableIndex}`);
        console.log(`  页码: ${chunk.page}`);
        console.log(`  表头: ${chunk.headers.join(', ')}`);
        console.log(`  行数: ${chunk.rows.length}`);
        console.log(`  是否虚拟表格: ${chunk.isVirtual || false}`);
        console.log(`  首页: ${chunk.isFirstPage}, 末页: ${chunk.isLastPage}`);
        
        if (chunk.rows.length > 0) {
          console.log(`  第一行数据: ${chunk.rows[0].join(', ')}`);
        }
      }
    };

    // 解析页面
    console.log('\n开始解析页面...\n');
    const result = await parser.parse(page, url, {
      onDataChunk,
      filepath: 'test-virtual-table.md',
      pagesDir: path.join(__dirname, '../output/test')
    });

    // 输出结果统计
    console.log('\n' + '='.repeat(80));
    console.log('解析结果统计');
    console.log('='.repeat(80));
    console.log(`标题: ${result.title}`);
    console.log(`表格数量: ${result.tables.length}`);
    console.log(`图表数量: ${result.charts.length}`);
    console.log(`运行时图表数据: ${result.chartData ? result.chartData.length : 0}`);
    console.log(`数据块回调次数: ${chunkCount}`);
    console.log('');

    // 详细输出每个表格
    result.tables.forEach((table, index) => {
      console.log(`\n表格 ${index + 1}:`);
      console.log(`  索引: ${table.index}`);
      console.log(`  表头: ${table.headers.join(', ')}`);
      console.log(`  行数: ${table.rows.length}`);
      console.log(`  是否虚拟表格: ${table.isVirtual || false}`);
      console.log(`  总页数: ${table.totalPages || 1}`);
      
      if (table.rows.length > 0) {
        console.log(`  前3行数据:`);
        table.rows.slice(0, 3).forEach((row, i) => {
          console.log(`    ${i + 1}. ${row.join(' | ')}`);
        });
        
        if (table.rows.length > 3) {
          console.log(`    ... (共 ${table.rows.length} 行)`);
        }
      }
    });

    console.log('\n' + '='.repeat(80));
    console.log('测试完成！');
    console.log('='.repeat(80));

    // 等待用户观察
    console.log('\n按任意键关闭浏览器...');
    await new Promise(resolve => {
      process.stdin.once('data', resolve);
    });

  } catch (error) {
    console.error('\n测试失败:', error.message);
    console.error(error.stack);
  } finally {
    if (context) {
      await context.close();
    }
    if (browser) {
      await browser.close();
    }
  }
}

// 主函数
async function main() {
  const url = process.argv[2];

  if (!url) {
    console.error('错误: 请提供测试URL');
    console.error('用法: node scripts/test-virtual-table.js <url>');
    console.error('示例: node scripts/test-virtual-table.js https://example.com/page');
    process.exit(1);
  }

  await testVirtualTable(url);
}

main().catch(console.error);
