#!/usr/bin/env node
/**
 * 通过浏览器 JS 执行果仁网回测
 * 直接调用页面内的 scrat.utility.ajaxDispatch
 */
import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { DATA_ROOT, SESSION_FILE, OUTPUT_ROOT } from '../paths.js';

async function runBacktestViaJS(options = {}) {
  const {
    startDate = '2022-01-01',
    endDate = '2024-01-01',
    poolId = '1.P.113051162378342',  // 高流动800
    rankIndicator = '0.F.ROA.0',     // ROA
    count = 10,
    period = 20
  } = options;

  const session = JSON.parse(fs.readFileSync(SESSION_FILE, 'utf8'));

  const browser = await chromium.launch({ headless: true });
  const ctx = await browser.newContext({
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
  });
  await ctx.addCookies(session.cookies);
  const page = await ctx.newPage();

  console.log('Loading strategy page...');
  await page.goto('https://guorn.com/stock');
  await page.waitForTimeout(5000);

  // 等待 scrat 对象加载
  await page.waitForFunction(() => typeof window.scrat !== 'undefined' && window.scrat.utility, { timeout: 10000 });
  console.log('scrat loaded');

  // 先获取当前策略配置，了解正确的参数格式
  const strategyConfig = await page.evaluate(() => {
    try {
      return scrat.docController.getCurrentStrategy();
    } catch(e) {
      return { error: e.message };
    }
  });
  console.log('Current strategy config:', JSON.stringify(strategyConfig, null, 2).slice(0, 500));

  // 通过 scrat.utility.ajaxDispatch 调用，使用正确的参数格式
  // 用 Promise 等待回调（与 capture-real-backtest.js 相同的成功方式）
  const result = await page.evaluate(({ startDate, endDate, poolId, rankIndicator, count, period }) => {
    return new Promise((resolve) => {
      // 获取当前策略配置作为基础
      const strategy = scrat.docController.getCurrentStrategy();
      const bt = strategy.tabs.back_test;

      // 构造 payload（日期用斜杠格式，与 getCurrentStrategy 一致）
      const toSlashDate = d => d.replace(/-/g, '/');
      const payload = {
        filters: strategy.filters || [],
        ranks: rankIndicator
          ? [{ id: rankIndicator, weight: 1.0, asc: false, industry: 0 }]
          : (strategy.ranks || []),
        pool: poolId || strategy.pool || '',
        exclude_st: strategy.exclude_st || '0',
        exclude_STIB: strategy.exclude_STIB || 1,
        filter_suspend: strategy.filter_suspend || false,
        industry_type: strategy.industry_type || 0,
        timing: strategy.timing || { indicators: [], position: '0', threshold: ['-1', '-1'] },
        // 回测参数
        start: toSlashDate(startDate),
        end: toSlashDate(endDate),
        reference: bt.reference || '000300',
        count: String(count || bt.count || '10'),
        period: period || bt.period || 5,
        price: bt.price || 'close',
        trade_cost: bt.trade_cost || 0.002,
        position_limit: bt.position_limit || 1,
        backup_num: bt.backup_num || '0',
        backup_fund: bt.backup_fund || '',
        ideal_position: bt.ideal_position || 0.1,
        min_position: bt.min_position || 0.01,
        position_bias: bt.position_bias || 0.3,
        model: bt.model || 0,
        weight: bt.weight || '',
        trading_strategy: bt.trading_strategy || { buy_options: [], sell_options: [], hold_options: [] },
        hedge: bt.hedge || false,
        always_tradable: bt.always_tradable || 0,
        ideal_count: bt.ideal_count || 10,
        max_count: bt.max_count || 15,
        calc_id: scrat.navPara.userProfile.uid + '.' + Date.now().toString()
      };

      // 第 6 个参数 true = skipCheck（跳过 checkResponseOK，直接调用回调）
      scrat.utility.ajaxDispatch('POST', 'stock/runtest', false, payload, function(resp) {
        resolve(resp);
      }, true);

      setTimeout(() => resolve({ status: 'timeout' }), 90000);
    });
  }, { startDate, endDate, poolId, rankIndicator, count, period });

  await browser.close();
  return result;
}

async function main() {
  try {
    console.log('Running backtest via browser JS...');
    const result = await runBacktestViaJS({
      startDate: '2025-04-02',
      endDate: '2026-04-02',
      poolId: '',
      rankIndicator: '0.M.股票每日指标_中性ROA.0',
      count: 10,
      period: 20
    });

    console.log('Result status:', result.status);
    if (result.status === 'ok' && result.data) {
      const d = result.data;
      if (d.trade_summary) {
        console.log('Trade summary:', JSON.stringify(d.trade_summary, null, 2));
      }
      if (d.summary) {
        console.log('Summary rows:', d.summary?.sheet_data?.row_size);
      }
    } else {
      console.log('Full result:', JSON.stringify(result, null, 2).slice(0, 500));
    }

    fs.mkdirSync(DATA_ROOT, { recursive: true });
    const outFile = path.join(DATA_ROOT, `backtest-result-${Date.now()}.json`);
    fs.writeFileSync(outFile, JSON.stringify(result, null, 2));
    console.log('Saved to:', outFile);
  } catch (e) {
    console.error('Error:', e.message);
  }
}

main();
