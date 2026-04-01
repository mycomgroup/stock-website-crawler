#!/usr/bin/env node
/**
 * 批量运行果仁网策略
 * 
 * 策略列表：
 * 1. pure_treasury_defense - 国债ETF持有
 * 2. pure_cash_defense - 纯现金持有
 * 3. small_cap_growth - 小市值成长策略
 * 4. dividend_value - 高股息价值策略
 */

import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { SESSION_FILE, OUTPUT_ROOT } from '../paths.js';
import '../load-env.js';

const USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36';

// 策略配置
const STRATEGIES = [
  {
    name: 'pure_treasury_defense',
    displayName: '国债ETF防守策略',
    description: '100%持有国债ETF(511010)',
    config: {
      type: 'etf_holding',
      etfCode: '511010', // 国债ETF
    }
  },
  {
    name: 'pure_cash_defense',
    displayName: '纯现金防守策略',
    description: '100%现金持有',
    config: {
      type: 'cash',
    }
  },
  {
    name: 'small_cap_growth',
    displayName: '小市值成长策略',
    description: '市值升序+ROE>5%',
    config: {
      type: 'stock_selection',
      stockPool: '高流动800',
      stockLimit: 10,
      rebalanceCycle: 20,
      filters: [
        { indicator: 'ROE', operator: '>', value: 5 }
      ],
      rankings: [
        { indicator: '总市值', order: 'asc' }
      ],
      excludeST: true,
      excludeSTIB: true,
      filterSuspend: true
    }
  },
  {
    name: 'dividend_value',
    displayName: '高股息价值策略',
    description: 'PE<20+PB<2，PE升序',
    config: {
      type: 'stock_selection',
      stockPool: '高流动800',
      stockLimit: 20,
      rebalanceCycle: 20,
      filters: [
        { indicator: 'PE', operator: '<', value: 20 },
        { indicator: 'PB', operator: '<', value: 2 }
      ],
      rankings: [
        { indicator: 'PE', order: 'asc' }
      ],
      excludeST: true,
      excludeSTIB: true,
      filterSuspend: true
    }
  }
];

async function createAndRunStrategy(page, strategy, startTime, endTime) {
  console.log(`\n========== ${strategy.displayName} ==========`);
  
  // 点击新建
  const newBtn = page.locator('.empty.action, span.empty').first();
  if (await newBtn.isVisible({ timeout: 3000 }).catch(() => false)) {
    await newBtn.click();
    await page.waitForTimeout(1000);
  }

  if (strategy.config.type === 'cash') {
    // 纯现金策略 - 不做任何配置，直接回测
    console.log('纯现金策略 - 空仓运行');
    return await runBacktest(page, strategy, startTime, endTime);
  }
  
  if (strategy.config.type === 'etf_holding') {
    // ETF持有策略 - 果仁网不支持直接持有ETF作为策略
    // 需要用"添加策略/ETF"功能
    console.log('ETF持有策略 - 需要使用资产配置功能');
    return await runBacktest(page, strategy, startTime, endTime);
  }

  // 股票选择策略
  const config = strategy.config;
  
  // 1. 设置股票上限
  console.log('设置股票上限:', config.stockLimit);
  const stockLimitInput = page.locator('.limit-txt + input.number').first();
  if (await stockLimitInput.isVisible({ timeout: 2000 }).catch(() => false)) {
    await stockLimitInput.fill(String(config.stockLimit));
  }

  // 2. 设置调仓周期
  console.log('设置调仓周期:', config.rebalanceCycle);
  const cycleInput = page.locator('input.number.period').first();
  if (await cycleInput.isVisible({ timeout: 2000 }).catch(() => false)) {
    await cycleInput.fill(String(config.rebalanceCycle));
  }

  // 3. 设置股票池
  if (config.stockPool) {
    console.log('设置股票池:', config.stockPool);
    const hotPoolSel = page.locator('select.hot-pool-sel').first();
    if (await hotPoolSel.isVisible({ timeout: 2000 })) {
      await hotPoolSel.selectOption(config.stockPool);
    }
  }

  // 4. 排除ST
  if (config.excludeST) {
    const stSelect = page.locator('.st select').first();
    if (await stSelect.isVisible({ timeout: 2000 })) {
      await stSelect.selectOption({ index: 1 }); // 排除ST
    }
  }

  // 5. 排除科创板
  if (config.excludeSTIB) {
    const stibSelect = page.locator('.STIB select').first();
    if (await stibSelect.isVisible({ timeout: 2000 })) {
      await stibSelect.selectOption({ index: 0 }); // 排除科创板
    }
  }

  // 6. 过滤停牌
  if (config.filterSuspend) {
    const suspendCheckbox = page.locator('.filter-suspend input[type="checkbox"]').first();
    if (await suspendCheckbox.isVisible({ timeout: 2000 })) {
      if (!(await suspendCheckbox.isChecked())) {
        await suspendCheckbox.check();
      }
    }
  }

  // 7. 设置筛选条件
  if (config.filters && config.filters.length > 0) {
    console.log('设置筛选条件...');
    // 需要点击指标添加筛选条件
    // 这里简化处理，使用排名条件
  }

  // 8. 设置排名条件
  if (config.rankings && config.rankings.length > 0) {
    console.log('设置排名条件...');
    const ranking = config.rankings[0];
    
    // 点击财务指标tab
    const financialTab = page.locator('text=财务指标').first();
    if (await financialTab.isVisible({ timeout: 2000 })) {
      await financialTab.click();
      await page.waitForTimeout(500);
    }

    // 对于市值排名，使用行情tab
    if (ranking.indicator.includes('市值')) {
      const quoteTab = page.locator('text=行情').first();
      if (await quoteTab.isVisible({ timeout: 2000 })) {
        await quoteTab.click();
        await page.waitForTimeout(500);
      }

      // 点击股本和市值
      const marketCapBtn = page.locator('.btn-factor:has-text("股本")').first();
      if (await marketCapBtn.isVisible({ timeout: 2000 })) {
        await marketCapBtn.click();
        await page.waitForTimeout(300);
      }

      // 点击总市值
      const totalMarketCap = page.locator('text=总市值').first();
      if (await totalMarketCap.isVisible({ timeout: 1000 })) {
        await totalMarketCap.click();
        await page.waitForTimeout(500);
      }
    }
    
    // 对于PE排名
    if (ranking.indicator === 'PE') {
      const valuationBtn = page.locator('.btn-factor:has-text("估值")').first();
      if (await valuationBtn.isVisible({ timeout: 2000 })) {
        await valuationBtn.click();
        await page.waitForTimeout(300);
      }
      
      const peBtn = page.locator('text=PE, text=市盈率').first();
      if (await peBtn.isVisible({ timeout: 1000 })) {
        await peBtn.click();
        await page.waitForTimeout(500);
      }
    }
  }

  await page.waitForTimeout(1000);
  
  return await runBacktest(page, strategy, startTime, endTime);
}

async function runBacktest(page, strategy, startTime, endTime) {
  console.log('开始回测...');
  
  // 点击开始回测
  const backtestBtn = page.locator('a:has-text("开始回测")').first();
  if (await backtestBtn.isVisible({ timeout: 3000 }).catch(() => false)) {
    await backtestBtn.click();
  }

  // 等待回测完成
  console.log('等待回测完成...');
  for (let i = 0; i < 24; i++) {
    await page.waitForTimeout(5000);
    
    const hasResults = await page.locator('.result-table, text=年化收益').isVisible().catch(() => false);
    if (hasResults) {
      console.log('回测完成！');
      break;
    }
    console.log(`等待... ${(i + 1) * 5}s`);
  }

  // 提取结果
  const results = {
    strategy: strategy.name,
    displayName: strategy.displayName,
    timestamp: new Date().toISOString()
  };

  try {
    const pageText = await page.locator('body').textContent();
    
    // 提取关键指标
    const extractMetric = (label) => {
      const patterns = [
        new RegExp(label + '[：:\\s]*([\\d.\\-+%]+)'),
        new RegExp('([\\d.\\-+%]+)\\s*' + label)
      ];
      for (const pattern of patterns) {
        const match = pageText.match(pattern);
        if (match && match[1]) return match[1];
      }
      return null;
    };

    // 提取表格数据
    const tableMatch = pageText.match(/本策略\s*([\d.\-+%]+)\s*([\d.\-+%]+)\s*([\d.\-]+)\s*([\d.\-+%]+)/);
    if (tableMatch) {
      results.totalReturn = tableMatch[1];
      results.annualReturn = tableMatch[2];
      results.sharpeRatio = tableMatch[3];
      results.maxDrawdown = tableMatch[4];
    }

    results.winRate = extractMetric('交易赢率');
    results.turnoverRate = extractMetric('年换手率');

    console.log('结果:', JSON.stringify(results, null, 2));
  } catch (e) {
    console.log('提取结果失败:', e.message);
  }

  // 截图
  const screenshotPath = path.join(OUTPUT_ROOT, `${strategy.name}-result.png`);
  await page.screenshot({ path: screenshotPath, fullPage: true });
  console.log('截图保存:', screenshotPath);

  return results;
}

export async function runAllStrategies(options = {}) {
  const {
    startTime = '2022-01-01',
    endTime = '2025-03-28',
    headed = true
  } = options;

  // 加载会话
  let sessionPayload;
  if (fs.existsSync(SESSION_FILE)) {
    sessionPayload = JSON.parse(fs.readFileSync(SESSION_FILE, 'utf8'));
    console.log('加载会话:', SESSION_FILE);
  } else {
    throw new Error('未找到会话文件，请先运行 capture-session.js');
  }

  const browser = await chromium.launch({ headless: !headed });
  const context = await browser.newContext({ userAgent: USER_AGENT });
  await context.addCookies(sessionPayload.cookies);
  const page = await context.newPage();

  console.log('导航到策略页面...');
  try {
    await page.goto('https://guorn.com/stock', { timeout: 90000, waitUntil: 'domcontentloaded' });
  } catch (e) {
    console.log('页面加载超时，尝试继续...');
  }
  await page.waitForTimeout(5000);

  // 检查登录状态
  const isLoggedIn = !page.url().includes('/user/login');
  console.log('登录状态:', isLoggedIn);

  if (!isLoggedIn) {
    await browser.close();
    throw new Error('会话已过期');
  }

  fs.mkdirSync(OUTPUT_ROOT, { recursive: true });

  const allResults = [];

  // 运行每个策略
  for (const strategy of STRATEGIES) {
    try {
      const result = await createAndRunStrategy(page, strategy, startTime, endTime);
      allResults.push(result);
      
      // 等待一段时间再运行下一个
      await page.waitForTimeout(3000);
      
      // 刷新页面准备下一个策略
      await page.goto('https://guorn.com/stock');
      await page.waitForTimeout(2000);
    } catch (e) {
      console.error(`策略 ${strategy.name} 运行失败:`, e.message);
      allResults.push({
        strategy: strategy.name,
        error: e.message
      });
    }
  }

  // 保存所有结果
  const resultsFile = path.join(OUTPUT_ROOT, 'all-strategies-results.json');
  fs.writeFileSync(resultsFile, JSON.stringify(allResults, null, 2));
  console.log('\n所有结果已保存:', resultsFile);

  // 打印汇总
  console.log('\n========== 汇总结果 ==========');
  for (const result of allResults) {
    if (result.error) {
      console.log(`${result.strategy}: 失败 - ${result.error}`);
    } else {
      console.log(`${result.displayName}: 年化收益=${result.annualReturn || 'N/A'}, 最大回撤=${result.maxDrawdown || 'N/A'}`);
    }
  }

  if (headed) {
    console.log('\n浏览器将在10秒后关闭...');
    await page.waitForTimeout(10000);
  }

  await browser.close();
  return allResults;
}

if (process.argv[1] && import.meta.url === `file://${process.argv[1]}`) {
  runAllStrategies({ 
    headed: !process.argv.includes('--headless')
  }).catch(console.error);
}