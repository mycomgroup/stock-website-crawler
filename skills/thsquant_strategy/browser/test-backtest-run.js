#!/usr/bin/env node
/**
 * THSQuant 运行回测 API 测试
 * 基于捕获的信息尝试运行回测
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import '../load-env.js';
import { SESSION_FILE, OUTPUT_ROOT } from '../paths.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// 构建请求函数
async function testBacktestAPI() {
  console.log('\n' + '='.repeat(70));
  console.log('THSQuant 运行回测 API 测试');
  console.log('='.repeat(70));

  // 加载 session
  const session = JSON.parse(fs.readFileSync(SESSION_FILE, 'utf8'));
  const cookies = session.cookies || [];
  const cookieHeader = cookies.map(c => `${c.name}=${c.value}`).join('; ');

  const strategyId = '67c935e607887b957629ad72';

  // 通用请求函数
  async function request(url, body = {}) {
    const bodyStr = typeof body === 'string' ? body : new URLSearchParams(body).toString();

    console.log(`\n请求: ${url}`);
    console.log(`参数: ${bodyStr}`);

    try {
      const resp = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'Cookie': cookieHeader,
          'X-Requested-With': 'XMLHttpRequest'
        },
        body: bodyStr
      });

      const text = await resp.text();

      // 解析 JSONP
      const match = text.match(/\((.+)\)/s);
      if (match) {
        try {
          const json = JSON.parse(match[1]);
          console.log(`响应: errorcode=${json.errorcode}`);
          if (json.errormsg) console.log(`消息: ${json.errormsg}`);
          return json;
        } catch (e) {}
      }

      // 尝试直接解析 JSON
      try {
        const json = JSON.parse(text);
        console.log(`响应: errorcode=${json.errorcode}`);
        if (json.errormsg) console.log(`消息: ${json.errormsg}`);
        return json;
      } catch (e) {
        console.log(`响应: ${text.slice(0, 200)}`);
        return { raw: text };
      }
    } catch (e) {
      console.log(`错误: ${e.message}`);
      return { error: e.message };
    }
  }

  // 1. 测试策略信息 API
  console.log('\n--- 测试策略信息 API ---');
  const strategyInfo = await request(
    'https://quant.10jqka.com.cn/platform/algorithms/queryinfo/',
    { algoId: strategyId, datatype: 'jsonp', isajax: '1' }
  );

  // 2. 测试回测列表 API
  console.log('\n--- 测试回测列表 API ---');
  const backtestList = await request(
    'https://quant.10jqka.com.cn/platform/backtest/queryall/',
    { algo_id: strategyId, isajax: '1' }
  );

  // 3. 尝试运行回测 - 测试各种可能的 API
  console.log('\n--- 尝试运行回测 ---');

  // 测试 1: backtest/run
  const runResult1 = await request(
    'https://quant.10jqka.com.cn/platform/backtest/run/',
    {
      algo_id: strategyId,
      start_date: '2024-01-01',
      end_date: '2024-12-31',
      capital_base: '100000',
      frequency: 'DAILY',
      benchmark: '000300.SH',
      isajax: '1'
    }
  );

  // 测试 2: backtest/create
  const runResult2 = await request(
    'https://quant.10jqka.com.cn/platform/backtest/create/',
    {
      algo_id: strategyId,
      start_date: '2024-01-01',
      end_date: '2024-12-31',
      capital_base: '100000',
      frequency: 'DAILY',
      benchmark: '000300.SH',
      isajax: '1'
    }
  );

  // 测试 3: backtest/add
  const runResult3 = await request(
    'https://quant.10jqka.com.cn/platform/backtest/add/',
    {
      algo_id: strategyId,
      start_date: '2024-01-01',
      end_date: '2024-12-31',
      capital_base: '100000',
      frequency: 'DAILY',
      benchmark: '000300.SH',
      isajax: '1'
    }
  );

  // 测试 4: algorithms/backtest
  const runResult4 = await request(
    'https://quant.10jqka.com.cn/platform/algorithms/backtest/',
    {
      algo_id: strategyId,
      start_date: '2024-01-01',
      end_date: '2024-12-31',
      capital_base: '100000',
      frequency: 'DAILY',
      benchmark: '000300.SH',
      isajax: '1'
    }
  );

  // 4. 尝试使用用户 ID
  console.log('\n--- 使用用户 ID 测试 ---');
  const userId = '772028948';

  const runResult5 = await request(
    'https://quant.10jqka.com.cn/platform/backtest/run/',
    {
      user_id: userId,
      algo_id: strategyId,
      start_date: '2024-01-01',
      end_date: '2024-12-31',
      capital_base: '100000',
      frequency: 'DAILY',
      benchmark: '000300.SH',
      stock_market: 'STOCK',
      isajax: '1'
    }
  );

  // 5. 尝试 JSONP 格式
  console.log('\n--- JSONP 格式测试 ---');
  const runResult6 = await request(
    'https://quant.10jqka.com.cn/platform/backtest/run/?callback=jQuery_test&datatype=jsonp',
    {
      algo_id: strategyId,
      start_date: '2024-01-01',
      end_date: '2024-12-31',
      capital_base: '100000',
      frequency: 'DAILY',
      benchmark: '000300.SH',
      datatype: 'jsonp',
      isajax: '1'
    }
  );

  // 6. 尝试不同的参数名
  console.log('\n--- 尝试不同参数名 ---');
  const runResult7 = await request(
    'https://quant.10jqka.com.cn/platform/backtest/run/',
    {
      algoId: strategyId,
      startDate: '2024-01-01',
      endDate: '2024-12-31',
      capitalBase: '100000',
      frequency: 'DAILY',
      benchmark: '000300.SH',
      isajax: '1'
    }
  );

  // 保存结果
  const results = {
    strategyInfo,
    backtestList,
    runTests: [
      { api: 'backtest/run', result: runResult1 },
      { api: 'backtest/create', result: runResult2 },
      { api: 'backtest/add', result: runResult3 },
      { api: 'algorithms/backtest', result: runResult4 },
      { api: 'backtest/run with user_id', result: runResult5 },
      { api: 'backtest/run JSONP', result: runResult6 },
      { api: 'backtest/run camelCase', result: runResult7 }
    ],
    timestamp: Date.now()
  };

  const outputPath = path.join(OUTPUT_ROOT, 'backtest-run-tests.json');
  fs.writeFileSync(outputPath, JSON.stringify(results, null, 2));
  console.log(`\n保存到: ${outputPath}`);

  // 分析结果
  console.log('\n' + '='.repeat(70));
  console.log('测试结果分析');
  console.log('='.repeat(70));

  results.runTests.forEach((test, i) => {
    const status = test.result?.errorcode === 0 ? '✓ 成功' :
                   test.result?.errorcode ? `✗ errorcode=${test.result.errorcode}` :
                   '✗ 失败';
    console.log(`${i + 1}. ${test.api}: ${status}`);
    if (test.result?.errormsg) {
      console.log(`   消息: ${test.result.errormsg}`);
    }
  });
}

testBacktestAPI().catch(console.error);