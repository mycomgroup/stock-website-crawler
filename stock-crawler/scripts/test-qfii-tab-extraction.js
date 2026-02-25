#!/usr/bin/env node

/**
 * 测试QFII页面的Tab提取
 */

import { chromium } from 'playwright';
import GenericParser from '../src/parsers/generic-parser.js';
import path from 'path';
import fs from 'fs';

const url = 'https://www.lixinger.com/analytics/shareholders/qfii';
const outputDir = './output/test-qfii-tabs';

async function testQFIITabs() {
  console.log('🧪 测试QFII页面Tab提取\n');
  console.log(`URL: ${url}\n`);
  
  // 创建输出目录
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }
  
  const browser = await chromium.launchPersistentContext(
    './chrome_user_data_test',
    {
      headless: false,
      viewport: { width: 1280, height: 720 }
    }
  );
  
  const page = await browser.newPage();
  
  try {
    console.log('📄 加载页面...');
    await page.goto(url, { waitUntil: 'networkidle', timeout: 60000 });
    console.log('✅ 页面加载完成\n');
    
    // 等待内容加载
    await page.waitForTimeout(3000);
    
    console.log('🔍 开始提取Tab内容...\n');
    
    const parser = new GenericParser();
    const filepath = path.join(outputDir, 'qfii-tabs-test.md');
    
    let tabCount = 0;
    const onDataChunk = async (chunk) => {
      if (chunk.type === 'tab') {
        tabCount++;
        console.log(`  ✓ Tab ${tabCount}: ${chunk.name}`);
        if (chunk.data && chunk.data.tables) {
          console.log(`    - 表格数: ${chunk.data.tables.length}`);
          chunk.data.tables.forEach((table, i) => {
            console.log(`      表格 ${i + 1}: ${table.headers.length} 列, ${table.rows.length} 行`);
          });
        }
      }
    };
    
    const tabs = await parser.findAndProcessTabs(page, filepath, onDataChunk);
    
    console.log(`\n📊 提取结果:`);
    console.log(`  总Tab数: ${tabs.length}`);
    
    if (tabs.length > 0) {
      console.log(`\n  Tab列表:`);
      tabs.forEach((tab, i) => {
        console.log(`    ${i + 1}. ${tab.name}`);
        if (tab.tables && tab.tables.length > 0) {
          console.log(`       - ${tab.tables.length} 个表格`);
        }
      });
    } else {
      console.log(`\n  ⚠️  未找到Tab，可能需要进一步优化检测逻辑`);
    }
    
    console.log(`\n✅ 测试完成`);
    
  } catch (error) {
    console.error('❌ 错误:', error.message);
    console.error(error.stack);
  } finally {
    await browser.close();
  }
}

testQFIITabs().catch(console.error);
