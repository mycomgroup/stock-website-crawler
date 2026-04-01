#!/usr/bin/env node
/**
 * 运行单个策略 - 小市值成长策略
 */

import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { SESSION_FILE, OUTPUT_ROOT } from '../paths.js';
import '../load-env.js';

const USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36';

async function runSmallCapStrategy() {
  // 加载会话
  const sessionPayload = JSON.parse(fs.readFileSync(SESSION_FILE, 'utf8'));
  
  const browser = await chromium.launch({ headless: false, slowMo: 500 });
  const context = await browser.newContext({ userAgent: USER_AGENT });
  await context.addCookies(sessionPayload.cookies);
  const page = await context.newPage();

  console.log('=== 小市值成长策略 ===');
  console.log('策略: 市值升序 + ROE>5%, 10只股票, 每月调仓');

  // 导航
  console.log('打开策略页面...');
  await page.goto('https://guorn.com/stock', { timeout: 30000, waitUntil: 'domcontentloaded' });
  console.log('DOM加载完成，等待页面稳定...');
  await page.waitForTimeout(10000);

  // 截图调试
  await page.screenshot({ path: path.join(OUTPUT_ROOT, 'debug-page.png') });
  console.log('截图保存: debug-page.png');

  // 尝试点击新建按钮
  console.log('尝试点击新建按钮...');
  const newBtn = page.locator('span:has-text("新建")').first();
  const isVisible = await newBtn.isVisible({ timeout: 5000 }).catch(() => false);
  
  if (!isVisible) {
    console.log('新建按钮不可见，可能已经是新策略页面');
  } else {
    await newBtn.click();
    await page.waitForTimeout(2000);
  }

  // 设置股票上限
  console.log('设置股票上限: 10');
  const stockLimitInput = page.locator('input[value="100"]').first();
  if (await stockLimitInput.isVisible({ timeout: 5000 }).catch(() => false)) {
    await stockLimitInput.fill('10');
  } else {
    console.log('股票上限输入框未找到');
  }

  // 设置股票池
  console.log('设置股票池: 高流动800');
  const hotPoolSel = page.locator('select.hot-pool-sel').first();
  await hotPoolSel.selectOption('高流动800');

  // 排除ST
  const stSelect = page.locator('.st select').first();
  await stSelect.selectOption({ index: 1 });

  // 排除科创板
  const stibSelect = page.locator('.STIB select').first();
  await stibSelect.selectOption({ index: 0 });

  // 过滤停牌
  const suspendCheckbox = page.locator('.filter-suspend input[type="checkbox"]').first();
  if (!(await suspendCheckbox.isChecked())) {
    await suspendCheckbox.check();
  }

  await page.waitForTimeout(1000);

  // 添加排名条件 - 总市值升序
  console.log('添加排名条件: 总市值升序');
  
  // 点击行情tab
  const quoteTab = page.locator('text=行情').first();
  await quoteTab.click();
  await page.waitForTimeout(500);

  // 点击股本和市值
  const marketCapBtn = page.locator('.btn-factor:has-text("股本")').first();
  await marketCapBtn.click();
  await page.waitForTimeout(300);

  // 点击总市值
  const totalMarketCap = page.locator('text=总市值').first();
  await totalMarketCap.click();
  await page.waitForTimeout(1000);

  // 点击开始回测
  console.log('开始回测...');
  const backtestBtn = page.locator('a:has-text("开始回测")').first();
  await backtestBtn.click();

  // 等待结果
  console.log('等待回测结果...');
  await page.waitForTimeout(120000);

  // 截图
  const screenshotPath = path.join(OUTPUT_ROOT, 'small_cap_growth-result.png');
  await page.screenshot({ path: screenshotPath, fullPage: true });
  console.log('截图保存:', screenshotPath);

  // 提取结果
  const pageText = await page.locator('body').textContent();
  const tableMatch = pageText.match(/本策略\s*([\d.\-+%]+)\s*([\d.\-+%]+)\s*([\d.\-]+)\s*([\d.\-+%]+)/);
  
  const results = {
    strategy: 'small_cap_growth',
    displayName: '小市值成长策略',
    timestamp: new Date().toISOString()
  };

  if (tableMatch) {
    results.totalReturn = tableMatch[1];
    results.annualReturn = tableMatch[2];
    results.sharpeRatio = tableMatch[3];
    results.maxDrawdown = tableMatch[4];
  }

  // 保存结果
  const resultFile = path.join(OUTPUT_ROOT, 'small_cap_growth-result.json');
  fs.writeFileSync(resultFile, JSON.stringify(results, null, 2));
  console.log('结果保存:', resultFile);
  console.log('结果:', JSON.stringify(results, null, 2));

  await browser.close();
  return results;
}

runSmallCapStrategy().catch(console.error);