#!/usr/bin/env node
/**
 * 自动化在果仁网创建 RFScore 策略并运行回测
 * 
 * 策略逻辑（基于 rfscore_pure_offensive.py）：
 * - 股票池：高流动800（近似沪深300+中证500）
 * - 排除：科创板、ST、停牌
 * - 排名：ROA、净利润增长率等
 * - 交易：每月调仓，最多20只
 */

import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { DATA_ROOT, SESSION_FILE, OUTPUT_ROOT } from '../paths.js';
import '../load-env.js';

const USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36';

export async function runRFCoreStrategy(options = {}) {
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
  await page.waitForTimeout(5000);

  // Check if still logged in
  const isLoggedIn = !page.url().includes('/user/login');
  console.log('Logged in:', isLoggedIn);

  if (!isLoggedIn) {
    console.log('Session expired, need to re-login');
    await browser.close();
    throw new Error('Session expired');
  }

  // Take initial screenshot
  fs.mkdirSync(OUTPUT_ROOT, { recursive: true });
  await page.screenshot({ path: path.join(OUTPUT_ROOT, 'step1-initial.png') });

  // Step 1: Click "新建" to create new strategy
  console.log('Step 1: Creating new strategy...');
  const newBtn = page.locator('.empty.action, span.empty').first();
  if (await newBtn.isVisible({ timeout: 5000 }).catch(() => false)) {
    await newBtn.click();
    await page.waitForTimeout(2000);
    console.log('Clicked new button');
  }

  await page.screenshot({ path: path.join(OUTPUT_ROOT, 'step2-new.png') });

  // Step 2: Set stock limit (股票上限)
  console.log('Step 2: Setting stock limit to 20...');
  try {
    const stockLimitInput = page.locator('.limit-txt + input.number, input.number.text').first();
    if (await stockLimitInput.isVisible({ timeout: 3000 })) {
      await stockLimitInput.click();
      await stockLimitInput.fill('20');
      console.log('Set stock limit to 20');
    }
  } catch (e) {
    console.log('Stock limit error:', e.message);
  }

  // Step 3: Set rebalance cycle (调仓周期)
  console.log('Step 3: Setting rebalance cycle to 20...');
  try {
    const cycleInput = page.locator('input.number.period').first();
    if (await cycleInput.isVisible({ timeout: 3000 })) {
      await cycleInput.click();
      await cycleInput.fill('20');
      console.log('Set rebalance cycle to 20');
    }
  } catch (e) {
    console.log('Rebalance cycle error:', e.message);
  }

  await page.screenshot({ path: path.join(OUTPUT_ROOT, 'step3-config.png') });

  // Step 4: Select stock pool
  console.log('Step 4: Setting stock pool...');
  try {
    const hotPoolSel = page.locator('select.hot-pool-sel').first();
    if (await hotPoolSel.isVisible({ timeout: 3000 })) {
      // 高流动800 is a good proxy for 沪深300+中证500
      await hotPoolSel.selectOption('高流动800');
      console.log('Selected stock pool: 高流动800');
    }
  } catch (e) {
    console.log('Stock pool error:', e.message);
  }

  // Step 5: 排除ST
  console.log('Step 5: Excluding ST stocks...');
  try {
    const stSelect = page.locator('.st select').first();
    if (await stSelect.isVisible({ timeout: 3000 })) {
      await stSelect.selectOption({ index: 1 }); // 排除ST
      console.log('Excluded ST stocks');
    }
  } catch (e) {
    console.log('ST exclusion error:', e.message);
  }

  // Step 6: 排除科创板
  console.log('Step 6: Excluding STIB stocks...');
  try {
    const stibSelect = page.locator('.STIB select').first();
    if (await stibSelect.isVisible({ timeout: 3000 })) {
      await stibSelect.selectOption({ index: 0 }); // 排除科创板
      console.log('Excluded STIB stocks');
    }
  } catch (e) {
    console.log('STIB exclusion error:', e.message);
  }

  // Step 7: 过滤停牌股票
  console.log('Step 7: Filtering suspended stocks...');
  try {
    const suspendCheckbox = page.locator('.filter-suspend input[type="checkbox"]').first();
    if (await suspendCheckbox.isVisible({ timeout: 3000 })) {
      if (!(await suspendCheckbox.isChecked())) {
        await suspendCheckbox.check();
        console.log('Checked filter suspended stocks');
      }
    }
  } catch (e) {
    console.log('Suspend filter error:', e.message);
  }

  await page.screenshot({ path: path.join(OUTPUT_ROOT, 'step4-pool.png') });

  // Step 8: Add ranking conditions - click on 财务指标
  console.log('Step 8: Adding ranking conditions...');
  try {
    // Click on 财务指标 tab
    const financialTab = page.locator('text=财务指标').first();
    if (await financialTab.isVisible({ timeout: 3000 })) {
      await financialTab.click();
      await page.waitForTimeout(500);
      console.log('Clicked 财务指标 tab');
    }

    // Find and expand 盈利能力 section
    const profitabilityBtn = page.locator('.btn-factor:has-text("盈利")').first();
    if (await profitabilityBtn.isVisible({ timeout: 3000 })) {
      await profitabilityBtn.click();
      await page.waitForTimeout(500);
      console.log('Expanded 盈利能力 section');
    }

    // Click on ROA to add it to ranking
    const roaBtn = page.locator('text=ROA, text=总资产收益率').first();
    if (await roaBtn.isVisible({ timeout: 2000 })) {
      await roaBtn.click();
      console.log('Added ROA to ranking');
      await page.waitForTimeout(500);
    }
  } catch (e) {
    console.log('Ranking conditions error:', e.message);
  }

  await page.screenshot({ path: path.join(OUTPUT_ROOT, 'step5-ranking.png') });

  // Step 9: Click on trading model tab
  console.log('Step 9: Setting trading model...');
  try {
    const tradingTab = page.locator('a.trading, text=交易模型').first();
    if (await tradingTab.isVisible({ timeout: 3000 })) {
      await tradingTab.click();
      await page.waitForTimeout(1000);
      console.log('Clicked trading model tab');
    }
  } catch (e) {
    console.log('Trading model tab error:', e.message);
  }

  await page.screenshot({ path: path.join(OUTPUT_ROOT, 'step6-trading.png') });

  // Step 10: Set backtest date range
  console.log('Step 10: Setting backtest date range...');
  try {
    // Find date inputs - they might be in the backtest section
    const dateInputs = await page.locator('input.datepicker, input[type="text"][placeholder*="日期"]').all();
    console.log('Found date inputs:', dateInputs.length);
    
    // Try to find start/end date by looking at their position or aria-label
    const allInputs = await page.locator('input[type="text"]').all();
    for (const input of allInputs) {
      const val = await input.inputValue();
      if (val && val.match(/^\d{4}-\d{2}-\d{2}$/)) {
        console.log('Found date input with value:', val);
      }
    }
  } catch (e) {
    console.log('Date range error:', e.message);
  }

  // Step 11: Click backtest button
  console.log('Step 11: Starting backtest...');
  try {
    const backtestBtn = page.locator('a:has-text("开始回测"), button:has-text("开始回测")').first();
    if (await backtestBtn.isVisible({ timeout: 5000 })) {
      await backtestBtn.click();
      console.log('Clicked backtest button!');
    }
  } catch (e) {
    console.log('Backtest button error:', e.message);
  }

  // Wait for backtest to complete
  console.log('Waiting for backtest to complete...');
  for (let i = 0; i < 24; i++) {
    await page.waitForTimeout(5000);
    
    // Check if results are visible
    const hasResults = await page.locator('.result-table, text=年化收益, #equity-curve').isVisible().catch(() => false);
    const hasLoading = await page.locator('.loading, text=计算中').isVisible().catch(() => false);
    
    if (hasResults) {
      console.log('Backtest completed!');
      break;
    }
    if (!hasLoading && i > 6) {
      console.log('Loading finished, checking for results...');
    }
    console.log(`Waiting... ${(i + 1) * 5}s`);
  }

  await page.screenshot({ path: path.join(OUTPUT_ROOT, 'step8-result.png'), fullPage: true });

  // Extract results
  const results = {
    url: page.url(),
    timestamp: new Date().toISOString()
  };

  // Try to extract metrics from page text
  try {
    const pageText = await page.locator('body').textContent();
    
    // Save page text for debugging
    fs.writeFileSync(path.join(OUTPUT_ROOT, 'page-text.txt'), pageText);
    
    // Extract key metrics using regex - improved patterns
    const extractMetric = (label) => {
      // Try different patterns
      const patterns = [
        new RegExp(label + '[：:\\s]*([\\d.\\-+%]+)'),
        new RegExp(label + '\\s*([\\d.\\-+%]+)'),
        new RegExp('([\\d.\\-+%]+)\\s*' + label)
      ];
      for (const pattern of patterns) {
        const match = pageText.match(pattern);
        if (match && match[1]) {
          return match[1];
        }
      }
      return null;
    };

    results.metrics = {
      annualReturn: extractMetric('年化收益'),
      totalReturn: extractMetric('总收益'),
      maxDrawdown: extractMetric('最大回撤'),
      sharpeRatio: extractMetric('夏普比率'),
      winRate: extractMetric('交易赢率'),
      turnoverRate: extractMetric('年换手率'),
      volatility: extractMetric('收益波动率'),
      infoRatio: extractMetric('信息比率')
    };

    console.log('Extracted metrics:', JSON.stringify(results.metrics));
  } catch (e) {
    console.log('Metric extraction error:', e.message);
  }

  // Save results
  const resultFile = path.join(OUTPUT_ROOT, `rfcore-backtest-${Date.now()}.json`);
  fs.writeFileSync(resultFile, JSON.stringify(results, null, 2));
  console.log(`Results saved to ${resultFile}`);

  // Keep browser open for a bit to see results
  if (headed) {
    console.log('Browser will close in 15 seconds...');
    await page.waitForTimeout(15000);
  }

  await browser.close();
  return results;
}

if (process.argv[1] && import.meta.url === `file://${process.argv[1]}`) {
  runRFCoreStrategy({ 
    headed: !process.argv.includes('--headless'),
    startTime: process.argv.find(a => a.startsWith('--start='))?.split('=')[1] || '2022-01-01',
    endTime: process.argv.find(a => a.startsWith('--end='))?.split('=')[1] || '2025-03-28'
  }).catch(console.error);
}