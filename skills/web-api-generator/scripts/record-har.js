#!/usr/bin/env node
/**
 * 录制 HAR 文件
 * 使用 Playwright 访问页面并自动录制所有网络请求
 */

import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';

async function recordHAR(url, outputPath, options = {}) {
  const {
    waitTime = 3000,
    headless = true,
    userAgent = null
  } = options;

  console.log(`开始录制: ${url}`);
  
  const browser = await chromium.launch({ headless });
  
  const context = await browser.newContext({
    recordHar: {
      path: outputPath,
      mode: 'minimal'
    },
    userAgent: userAgent || undefined
  });
  
  const page = await context.newPage();
  
  try {
    // 访问页面
    console.log('正在访问页面...');
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 });
    
    console.log('页面加载完成，等待额外请求...');
    
    // 等待可能的异步请求
    await page.waitForTimeout(waitTime);
    
    // 尝试滚动页面触发懒加载
    await page.evaluate(() => {
      window.scrollTo(0, document.body.scrollHeight);
    });
    
    await page.waitForTimeout(1000);
    
    console.log(`HAR 已保存到: ${outputPath}`);
    
  } catch (error) {
    console.error(`录制失败: ${error.message}`);
    throw error;
  } finally {
    await context.close();
    await browser.close();
  }
}

// 批量录制
async function batchRecord(urls, outputDir) {
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }
  
  for (const { url, name } of urls) {
    const outputPath = path.join(outputDir, `${name}.har`);
    
    try {
      await recordHAR(url, outputPath);
      console.log(`✅ ${name} 完成\n`);
    } catch (error) {
      console.error(`❌ ${name} 失败: ${error.message}\n`);
    }
  }
}

// CLI 使用
if (import.meta.url === `file://${process.argv[1]}`) {
  const args = process.argv.slice(2);
  
  if (args.length < 2) {
    console.log(`
使用方法:
  node record-har.js <url> <output.har> [waitTime]

示例:
  node record-har.js https://example.com/api output/example.har
  node record-har.js https://example.com/api output/example.har 5000

参数:
  url       - 要访问的 URL
  output    - HAR 文件保存路径
  waitTime  - 等待时间（毫秒），默认 3000
    `);
    process.exit(1);
  }
  
  const [url, output, waitTime] = args;
  
  recordHAR(url, output, {
    waitTime: waitTime ? parseInt(waitTime) : 3000
  }).catch(error => {
    console.error('错误:', error);
    process.exit(1);
  });
}

export { recordHAR, batchRecord };
