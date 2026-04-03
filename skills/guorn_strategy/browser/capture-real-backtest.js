#!/usr/bin/env node
/**
 * 通过 scrat.utility.ajaxDispatch 直接发送回测请求
 * 先用 getTestConfig({}) 填充参数，再调用 ajaxDispatch
 */
import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { DATA_ROOT, SESSION_FILE } from '../paths.js';

async function captureRealBacktest() {
  const session = JSON.parse(fs.readFileSync(SESSION_FILE, 'utf8'));
  const captured = [];

  const browser = await chromium.launch({ headless: true });
  const ctx = await browser.newContext({
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
  });
  await ctx.addCookies(session.cookies);
  const page = await ctx.newPage();

  page.on('request', req => {
    if (req.method() !== 'GET' && !req.url().includes('google') && !req.url().includes('analytics') && !req.url().includes('baidu')) {
      captured.push({ method: req.method(), url: req.url(), body: req.postData(), headers: req.headers() });
      console.log('[REQ]', req.method(), req.url().replace('https://guorn.com', ''));
    }
  });

  page.on('response', async resp => {
    if (resp.request().method() !== 'GET' && !resp.url().includes('google') && !resp.url().includes('analytics') && !resp.url().includes('baidu')) {
      const entry = captured.findLast(r => r.url === resp.url());
      if (entry) {
        entry.status = resp.status();
        try { entry.response = await resp.text(); } catch {}
        console.log('[RESP]', resp.status(), resp.url().replace('https://guorn.com', ''), '->', entry.response?.slice(0, 300));
      }
    }
  });

  console.log('Loading strategy page...');
  await page.goto('https://guorn.com/stock');
  await page.waitForTimeout(5000);

  // 方法1：用 getTestConfig 填充参数（传入空对象）
  const testConfigResult = await page.evaluate(() => {
    try {
      const ctrl = scrat.docController;
      const proto = Object.getPrototypeOf(ctrl);
      const t = {};
      proto.getTestConfig.call(ctrl, t);
      return { success: true, config: t };
    } catch(e) { return { error: e.message }; }
  });
  console.log('getTestConfig with empty obj:', JSON.stringify(testConfigResult, null, 2));

  // 方法2：直接用 getCurrentStrategy 的 tabs.back_test 构造 payload
  console.log('\nTrying direct ajaxDispatch with getCurrentStrategy data...');
  const ajaxResult = await page.evaluate(() => {
    return new Promise((resolve) => {
      try {
        const ctrl = scrat.docController;
        const strategy = ctrl.getCurrentStrategy();
        const bt = strategy.tabs.back_test;
        
        // 构造 payload，合并顶层策略字段和 back_test 字段
        const payload = {
          filters: strategy.filters || [],
          ranks: strategy.ranks || [],
          pool: strategy.pool || '',
          exclude_st: strategy.exclude_st || '0',
          exclude_STIB: strategy.exclude_STIB || 1,
          filter_suspend: strategy.filter_suspend || false,
          industry_type: strategy.industry_type || 0,
          timing: strategy.timing || { indicators: [], position: '0', threshold: ['-1', '-1'] },
          // back_test 参数
          start: bt.start,
          end: bt.end,
          reference: bt.reference || '000300',
          count: bt.count || '10',
          period: bt.period || 5,
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
          // calc_id
          calc_id: scrat.navPara.userProfile.uid + '.' + Date.now().toString()
        };
        
        console.log('Payload:', JSON.stringify(payload));
        
        // 直接调用 ajaxDispatch
        scrat.utility.ajaxDispatch('POST', 'stock/runtest', false, payload, function(resp) {
          resolve({ success: true, response: resp });
        });
        
        // 超时保护
        setTimeout(() => resolve({ timeout: true }), 30000);
      } catch(e) {
        resolve({ error: e.message });
      }
    });
  });
  
  console.log('ajaxDispatch result:', JSON.stringify(ajaxResult, null, 2));

  // 等待请求完成
  await page.waitForTimeout(5000);

  console.log('\nCaptured requests:', captured.length);
  for (const r of captured) {
    console.log('---');
    console.log('URL:', r.url.replace('https://guorn.com', ''));
    console.log('Status:', r.status);
    console.log('Body:', r.body?.slice(0, 800));
    console.log('Response:', r.response?.slice(0, 500));
  }

  fs.mkdirSync(DATA_ROOT, { recursive: true });
  fs.writeFileSync(
    path.join(DATA_ROOT, 'captured-real-backtest.json'),
    JSON.stringify({ testConfigResult, ajaxResult, captured }, null, 2)
  );
  console.log('\nSaved to data/captured-real-backtest.json');

  await browser.close();
}

captureRealBacktest().catch(console.error);
