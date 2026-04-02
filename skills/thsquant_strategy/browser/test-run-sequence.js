#!/usr/bin/env node
/**
 * 测试回测运行的正确调用序列
 * 先 update 代码，再 gettradedays，再 run
 */

import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import '../load-env.js';
import { SESSION_FILE, OUTPUT_ROOT } from '../paths.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const TARGET_ALGO_ID = '67c935e607887b957629ad72';

async function testRunSequence() {
  console.log('='.repeat(60));
  console.log('测试回测运行序列');
  console.log('='.repeat(60));

  const session = JSON.parse(fs.readFileSync(SESSION_FILE, 'utf8'));
  const cookies = session.cookies || [];

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36'
  });
  await context.addCookies(cookies);
  const page = await context.newPage();

  try {
    await page.goto('https://quant.10jqka.com.cn/view/study-index.html', {
      waitUntil: 'domcontentloaded', timeout: 30000
    });
    await page.waitForTimeout(2000);

    const results = await page.evaluate(async (algoId) => {
      const results = {};

      const post = async (url, body) => {
        const r = await fetch(url, {
          method: 'POST',
          headers: { 'Content-Type': 'application/x-www-form-urlencoded', 'X-Requested-With': 'XMLHttpRequest' },
          body
        });
        const text = await r.text();
        try {
          const m = text.match(/\((.+)\)/s);
          return JSON.parse(m ? m[1] : text);
        } catch (e) {
          return { raw: text.slice(0, 200) };
        }
      };

      // 1. 获取策略信息
      results.algoInfo = await post('/platform/algorithms/queryinfo/', `algoId=${algoId}&isajax=1`);

      // 2. 获取交易日列表
      results.tradeDays = await post('/platform/backtest/gettradedays/', `isajax=1`);

      // 3. 先 update 策略（保存代码）
      const code = results.algoInfo?.result?.algo_code || '';
      const algoName = results.algoInfo?.result?.algo_name || 'test';
      results.updateResult = await post('/platform/algorithms/update/', 
        `algo_id=${algoId}&algo_name=${encodeURIComponent(algoName)}&code=${encodeURIComponent(code)}&isajax=1`
      );

      // 4. 尝试 run（在 update 之后）
      const runTests = [];

      // 格式1: section 格式
      const r1 = await post('/platform/backtest/run/', 
        `algo_id=${algoId}&section=2024-01-01--2024-12-31&capital_base=100000&frequency=DAILY&benchmark=000300.SH&isajax=1`
      );
      runTests.push({ test: 'section-format', result: r1 });

      // 格式2: 带 stock_market
      const r2 = await post('/platform/backtest/run/', 
        `algo_id=${algoId}&section=2024-01-01--2024-12-31&capital_base=100000&frequency=DAILY&benchmark=000300.SH&stock_market=STOCK&isajax=1`
      );
      runTests.push({ test: 'with-stock_market', result: r2 });

      // 格式3: 带 datatype=jsonp
      const r3 = await post('/platform/backtest/run/', 
        `algo_id=${algoId}&section=2024-01-01--2024-12-31&capital_base=100000&frequency=DAILY&benchmark=000300.SH&datatype=jsonp&isajax=1`
      );
      runTests.push({ test: 'with-jsonp', result: r3 });

      // 格式4: 用 beginDate/endDate
      const r4 = await post('/platform/backtest/run/', 
        `algo_id=${algoId}&beginDate=2024-01-01&endDate=2024-12-31&capital_base=100000&frequency=DAILY&benchmark=000300.SH&isajax=1`
      );
      runTests.push({ test: 'beginDate-endDate', result: r4 });

      // 格式5: 用 start/end
      const r5 = await post('/platform/backtest/run/', 
        `algo_id=${algoId}&start=2024-01-01&end=2024-12-31&capital_base=100000&frequency=DAILY&benchmark=000300.SH&isajax=1`
      );
      runTests.push({ test: 'start-end', result: r5 });

      // 格式6: 用 date_range
      const r6 = await post('/platform/backtest/run/', 
        `algo_id=${algoId}&date_range=2024-01-01--2024-12-31&capital_base=100000&frequency=DAILY&benchmark=000300.SH&isajax=1`
      );
      runTests.push({ test: 'date_range', result: r6 });

      // 格式7: 用 time_range
      const r7 = await post('/platform/backtest/run/', 
        `algo_id=${algoId}&time_range=2024-01-01--2024-12-31&capital_base=100000&frequency=DAILY&benchmark=000300.SH&isajax=1`
      );
      runTests.push({ test: 'time_range', result: r7 });

      // 格式8: 用 period
      const r8 = await post('/platform/backtest/run/', 
        `algo_id=${algoId}&period=2024-01-01--2024-12-31&capital_base=100000&frequency=DAILY&benchmark=000300.SH&isajax=1`
      );
      runTests.push({ test: 'period', result: r8 });

      results.runTests = runTests;

      // 5. 检查 gettradedays 的响应格式
      results.tradeDaysDetail = await post('/platform/backtest/gettradedays/', 
        `algo_id=${algoId}&isajax=1`
      );

      return results;
    }, TARGET_ALGO_ID);

    console.log('\n=== 策略信息 ===');
    console.log('名称:', results.algoInfo?.result?.algo_name);
    console.log('语言:', results.algoInfo?.result?.language);

    console.log('\n=== 交易日列表 ===');
    console.log('errorcode:', results.tradeDays?.errorcode);
    if (results.tradeDays?.result) {
      console.log('result:', JSON.stringify(results.tradeDays.result).slice(0, 200));
    }

    console.log('\n=== 交易日列表（带 algo_id）===');
    console.log('errorcode:', results.tradeDaysDetail?.errorcode);
    if (results.tradeDaysDetail?.result) {
      console.log('result:', JSON.stringify(results.tradeDaysDetail.result).slice(0, 200));
    }

    console.log('\n=== update 结果 ===');
    console.log('errorcode:', results.updateResult?.errorcode, results.updateResult?.errormsg);

    console.log('\n=== run 测试结果 ===');
    results.runTests?.forEach(t => {
      const r = t.result;
      if (r.errorcode === 0) {
        console.log(`✓ ${t.test}: 成功! result=${JSON.stringify(r.result).slice(0, 100)}`);
      } else {
        console.log(`✗ ${t.test}: ${r.errorcode} ${r.errormsg || r.raw || ''}`);
      }
    });

    // 保存
    const outputPath = path.join(OUTPUT_ROOT, 'run-sequence-test.json');
    fs.writeFileSync(outputPath, JSON.stringify(results, null, 2));
    console.log(`\n保存: ${outputPath}`);

    await browser.close();
    return results;

  } catch (err) {
    console.error('错误:', err.message);
    await browser.close();
    throw err;
  }
}

testRunSequence().catch(err => {
  console.error('✗ 失败:', err.message);
  process.exit(1);
});
