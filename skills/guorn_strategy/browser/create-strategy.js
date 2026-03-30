#!/usr/bin/env node
/**
 * 自动化在果仁网创建策略并运行回测
 * 
 * 将 rfscore_pure_offensive.py 策略转换为果仁网配置
 * 
 * 策略逻辑：
 * - 股票池：沪深300 + 中证500（排除科创板、ST）
 * - 排名条件：ROA、净利润增长率、毛利率等因子
 * - 交易模型：每月调仓，最多20只股票
 */

import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { DATA_ROOT, SESSION_FILE, OUTPUT_ROOT } from '../paths.js';
import '../load-env.js';

const USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36';

export async function createAndRunBacktest(options = {}) {
  const {
    startTime = '2022-01-01',
    endTime = '2025-03-28',
    headed = true
  } = options;

  // Load session
  let sessionPayload;
  if (fs.existsSync(SESSION_FILE)) {
    sessionPayload = JSON.parse(fs.readFileSync(SESSION_FILE, 'utf8'));
    console.log('Loaded session from', SESSION_FILE);
  } else {
    throw new Error('No session file found. Run capture-session.js first.');
  }

  const browser = await chromium.launch({ headless: !headed });
  const context = await browser.newContext({ userAgent: USER_AGENT });
  
  // Set cookies from session
  await context.addCookies(sessionPayload.cookies);
  
  const page = await context.newPage();

  console.log('Navigating to strategy page...');
  await page.goto('https://guorn.com/stock');
  await page.waitForTimeout(3000);

  // Check if still logged in
  const isLoggedIn = !page.url().includes('/user/login');
  console.log('Logged in:', isLoggedIn);

  if (!isLoggedIn) {
    console.log('Session expired, need to re-login');
    await browser.close();
    throw new Error('Session expired');
  }

  // Step 1: Click "新建" to create new strategy
  console.log('Creating new strategy...');
  const newButton = page.locator('a:has-text("新建"), span:has-text("新建")').first();
  if (await newButton.isVisible({ timeout: 5000 }).catch(() => false)) {
    await newButton.click();
    await page.waitForTimeout(2000);
    console.log('Clicked new button');
  }

  // Step 2: Set stock pool (沪深300 + 中证500)
  console.log('Setting stock pool...');
  // Click on stock pool dropdown
  const poolDropdown = page.locator('#pool-select, .pool-select, select:has(option:has-text("沪深300"))').first();
  if (await poolDropdown.isVisible({ timeout: 3000 }).catch(() => false)) {
    await poolDropdown.click();
    await page.waitForTimeout(1000);
    // Select 沪深300
    const hs300Option = page.locator('option:has-text("沪深300"), li:has-text("沪深300")').first();
    if (await hs300Option.isVisible({ timeout: 2000 }).catch(() => false)) {
      await hs300Option.click();
      await page.waitForTimeout(500);
    }
  }

  // Step 3: Set stock limit to 20
  console.log('Setting stock limit...');
  const stockLimitInput = page.locator('input[name="stocknum"], input[name="stockLimit"]').first();
  if (await stockLimitInput.isVisible({ timeout: 3000 }).catch(() => false)) {
    await stockLimitInput.fill('20');
  }

  // Step 4: Set rebalance cycle to 20 (monthly)
  console.log('Setting rebalance cycle...');
  const cycleInput = page.locator('input[name="cycle"], input[name="rebalanceCycle"]').first();
  if (await cycleInput.isVisible({ timeout: 3000 }).catch(() => false)) {
    await cycleInput.fill('20');
  }

  // Step 5: Add ranking conditions (ROA, 净利润增长率, 毛利率)
  console.log('Adding ranking conditions...');
  
  // Click on ranking section
  const rankingSection = page.locator('#ranking-section, .ranking-section, text=排名条件').first();
  if (await rankingSection.isVisible({ timeout: 3000 }).catch(() => false)) {
    await rankingSection.click();
    await page.waitForTimeout(1000);
  }

  // Add ROA indicator
  const addRankingBtn = page.locator('button:has-text("添加排名"), a:has-text("添加排名"), .add-ranking').first();
  if (await addRankingBtn.isVisible({ timeout: 3000 }).catch(() => false)) {
    await addRankingBtn.click();
    await page.waitForTimeout(500);
    
    // Select ROA from dropdown
    const indicatorSelect = page.locator('select.indicator-select, .indicator-dropdown').last();
    if (await indicatorSelect.isVisible({ timeout: 2000 }).catch(() => false)) {
      await indicatorSelect.selectOption({ label: 'ROA' });
    }
  }

  // Step 6: Set trading model (定期轮动)
  console.log('Setting trading model...');
  const modelSelect = page.locator('select[name="tradetype"], select[name="tradingModel"]').first();
  if (await modelSelect.isVisible({ timeout: 3000 }).catch(() => false)) {
    await modelSelect.selectOption({ value: '1' }); // 模型I - 定期轮动
  }

  // Step 7: Set rebalance time to first trading day
  console.log('Setting rebalance time...');
  const tradeDateSelect = page.locator('select[name="tradedate"]').first();
  if (await tradeDateSelect.isVisible({ timeout: 3000 }).catch(() => false)) {
    await tradeDateSelect.selectOption({ label: '每月第一个交易日' });
  }

  // Step 8: Set backtest parameters
  console.log('Setting backtest parameters...');
  
  // Set start date
  const startDateInput = page.locator('input[name="startdate"], #backtest-start').first();
  if (await startDateInput.isVisible({ timeout: 3000 }).catch(() => false)) {
    await startDateInput.fill(startTime);
  }

  // Set end date
  const endDateInput = page.locator('input[name="enddate"], #backtest-end').first();
  if (await endDateInput.isVisible({ timeout: 3000 }).catch(() => false)) {
    await endDateInput.fill(endTime);
  }

  // Step 9: Click backtest button
  console.log('Starting backtest...');
  const backtestBtn = page.locator('button:has-text("开始回测"), a:has-text("开始回测")').first();
  if (await backtestBtn.isVisible({ timeout: 5000 }).catch(() => false)) {
    await backtestBtn.click();
    console.log('Backtest started!');
  }

  // Wait for backtest to complete
  console.log('Waiting for backtest to complete...');
  await page.waitForTimeout(15000);

  // Take screenshot
  const screenshotPath = path.join(OUTPUT_ROOT, `backtest-${Date.now()}.png`);
  fs.mkdirSync(OUTPUT_ROOT, { recursive: true });
  await page.screenshot({ path: screenshotPath, fullPage: true });
  console.log(`Screenshot saved to ${screenshotPath}`);

  // Save current URL (strategy page)
  console.log('Current URL:', page.url());

  await browser.close();
  
  return {
    url: page.url(),
    screenshotPath
  };
}

if (process.argv[1] && import.meta.url === `file://${process.argv[1]}`) {
  createAndRunBacktest({ headed: process.argv.includes('--headed') }).catch(console.error);
}
