#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { chromium } from 'playwright';
import { GuornStrategyClient } from './guorn-strategy-client.js';
import { ensureGuornSession } from './ensure-session.js';
import { DATA_ROOT, OUTPUT_ROOT, SESSION_FILE } from '../paths.js';

/**
 * 通过浏览器 JS 执行回测
 * 果仁网回测必须通过 scrat.utility.ajaxDispatch 调用，直接 HTTP POST 会返回 Server Error
 *
 * 账号限制：level=1 普通账号回测时间窗口约 1 年内
 */
async function runBacktestViaBrowser(config, sessionFile) {
  const session = JSON.parse(fs.readFileSync(sessionFile, 'utf8'));

  const browser = await chromium.launch({ headless: true });
  const ctx = await browser.newContext({
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
  });
  await ctx.addCookies(session.cookies);
  const page = await ctx.newPage();

  try {
    await page.goto('https://guorn.com/stock');
    await page.waitForTimeout(5000);
    await page.waitForFunction(() => typeof window.scrat !== 'undefined' && window.scrat.utility, { timeout: 15000 });

    // 发送回测请求
    await page.evaluate((cfg) => {
      const strategy = scrat.docController.getCurrentStrategy();
      const bt = strategy.tabs.back_test;
      const toSlashDate = d => d.replace(/-/g, '/');

      const payload = {
        filters: cfg.filters || strategy.filters || [],
        ranks: cfg.ranks || strategy.ranks || [],
        pool: cfg.pool || strategy.pool || '',
        exclude_st: cfg.exclude_st || strategy.exclude_st || '0',
        exclude_STIB: cfg.exclude_STIB ?? strategy.exclude_STIB ?? 1,
        filter_suspend: cfg.filter_suspend ?? strategy.filter_suspend ?? false,
        industry_type: cfg.industry_type || strategy.industry_type || 0,
        timing: cfg.timing || strategy.timing || { indicators: [], position: '0', threshold: ['-1', '-1'] },
        start: toSlashDate(cfg.start || cfg.startTime || bt.start),
        end: toSlashDate(cfg.end || cfg.endTime || bt.end),
        reference: cfg.reference || bt.reference || '000300',
        count: String(cfg.count || bt.count || '10'),
        period: cfg.period || bt.period || 5,
        price: cfg.price || bt.price || 'close',
        trade_cost: cfg.trade_cost ?? bt.trade_cost ?? 0.002,
        position_limit: cfg.position_limit ?? bt.position_limit ?? 1,
        backup_num: cfg.backup_num || bt.backup_num || '0',
        backup_fund: cfg.backup_fund || bt.backup_fund || '',
        ideal_position: cfg.ideal_position ?? bt.ideal_position ?? 0.1,
        min_position: cfg.min_position ?? bt.min_position ?? 0.01,
        position_bias: cfg.position_bias ?? bt.position_bias ?? 0.3,
        model: cfg.model ?? bt.model ?? 0,
        weight: cfg.weight || bt.weight || '',
        trading_strategy: cfg.trading_strategy || bt.trading_strategy || { buy_options: [], sell_options: [], hold_options: [] },
        hedge: cfg.hedge ?? bt.hedge ?? false,
        always_tradable: cfg.always_tradable ?? bt.always_tradable ?? 0,
        ideal_count: cfg.ideal_count || bt.ideal_count || 10,
        max_count: cfg.max_count || bt.max_count || 15,
        calc_id: scrat.navPara.userProfile.uid + '.' + Date.now().toString()
      };

      window.__backtestResult = null;
      window.__backtestDone = false;

      // skipCheck=true 确保回调被调用
      scrat.utility.ajaxDispatch('POST', 'stock/runtest', false, payload, function(resp) {
        window.__backtestResult = resp;
        window.__backtestDone = true;
      }, true);
    }, config);

    // 轮询等待结果（最多 90 秒）
    let result = null;
    for (let i = 0; i < 90; i++) {
      await page.waitForTimeout(1000);
      const done = await page.evaluate(() => window.__backtestDone);
      if (done) {
        result = await page.evaluate(() => window.__backtestResult);
        break;
      }
    }

    if (!result) {
      throw new Error('Backtest timed out after 90 seconds');
    }

    return result;
  } finally {
    await browser.close();
  }
}

/**
 * 主工作流：验证 session + 执行回测 + 保存结果
 */
export async function runStrategyWorkflow(options = {}) {
  const { strategyConfig, backtestConfig, headed, forceRefresh } = options;

  // 1. 确保 session 有效
  const { sessionFile } = await ensureGuornSession({ headed, forceRefresh });

  // 2. 获取用户信息
  const client = new GuornStrategyClient({ sessionFile });
  const profile = await client.getUserProfile();
  console.log(`User: ${profile.data?.username || 'Unknown'} (level=${profile.data?.level})`);

  // 3. 构造回测配置
  // strategyConfig 可以包含 filters/ranks/pool 等策略参数
  // backtestConfig 包含 startTime/endTime/transactionCost 等回测参数
  const config = {
    ...(strategyConfig || {}),
    start: backtestConfig?.startTime || backtestConfig?.start,
    end: backtestConfig?.endTime || backtestConfig?.end,
    trade_cost: backtestConfig?.transactionCost ?? backtestConfig?.trade_cost ?? 0.002,
    reference: backtestConfig?.benchmark === 'zz500' ? '000905'
      : backtestConfig?.benchmark === 'zz1000' ? '000852'
      : '000300',
  };

  console.log(`Running backtest: ${config.start} → ${config.end}`);

  // 4. 执行回测
  const result = await runBacktestViaBrowser(config, sessionFile);

  if (result.status !== 'ok') {
    throw new Error(`Backtest failed: ${JSON.stringify(result)}`);
  }

  // 5. 保存结果
  fs.mkdirSync(OUTPUT_ROOT, { recursive: true });
  const outFile = path.join(OUTPUT_ROOT, `backtest-${Date.now()}.json`);
  fs.writeFileSync(outFile, JSON.stringify(result, null, 2));
  console.log(`Result saved to: ${outFile}`);

  // 6. 提取摘要
  const data = result.data || {};
  const summary = data.trade_summary || {};

  return {
    status: 'ok',
    resultPath: outFile,
    summary: {
      annualReturn: summary.winsorize_annual,
      winRate: summary.win_ratio,
      informationRatio: summary.year_information_ratio,
      maxDrawdownDays: summary.maxdrop_day,
      avgHoldingDays: summary.avg_holding_days,
      sellCount: summary.sell_count,
      annualTurnover: summary.annual_turnover_rate,
      ...summary
    }
  };
}

/**
 * 实时选股（通过 /stock/screen）
 */
export async function runRealtimeSelection(options = {}) {
  const { strategyConfig, headed, forceRefresh } = options;

  await ensureGuornSession({ headed, forceRefresh });
  const client = new GuornStrategyClient();

  const url = client.buildPostUrl('/stock/screen');
  const result = await client.request(url, {
    method: 'POST',
    body: JSON.stringify(strategyConfig || {})
  });

  if (result.status !== 'ok') {
    throw new Error(`Realtime selection failed: ${JSON.stringify(result)}`);
  }

  fs.mkdirSync(OUTPUT_ROOT, { recursive: true });
  const outFile = path.join(OUTPUT_ROOT, `screen-${Date.now()}.json`);
  fs.writeFileSync(outFile, JSON.stringify(result, null, 2));

  return {
    resultPath: outFile,
    stocks: result.data?.stocks || result.data || []
  };
}

/**
 * 历史选股
 */
export async function runHistoricalSelection(options = {}) {
  const { strategyConfig, date, headed, forceRefresh } = options;

  await ensureGuornSession({ headed, forceRefresh });
  const client = new GuornStrategyClient();

  const payload = { ...(strategyConfig || {}), date };
  const url = client.buildPostUrl('/stock/screen');
  const result = await client.request(url, {
    method: 'POST',
    body: JSON.stringify(payload)
  });

  if (result.status !== 'ok') {
    throw new Error(`Historical selection failed: ${JSON.stringify(result)}`);
  }

  fs.mkdirSync(OUTPUT_ROOT, { recursive: true });
  const outFile = path.join(OUTPUT_ROOT, `screen-${date}-${Date.now()}.json`);
  fs.writeFileSync(outFile, JSON.stringify(result, null, 2));

  return {
    resultPath: outFile,
    date,
    stocks: result.data?.stocks || result.data || []
  };
}
