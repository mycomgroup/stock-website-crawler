#!/usr/bin/env node
/**
 * THSQuant 回测运行参数探测
 * 基于已有回测记录分析正确的参数格式
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import '../load-env.js';
import { SESSION_FILE, OUTPUT_ROOT } from '../paths.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function probeBacktestParams() {
  console.log('\n' + '='.repeat(70));
  console.log('THSQuant 回测运行参数探测');
  console.log('='.repeat(70));

  const session = JSON.parse(fs.readFileSync(SESSION_FILE, 'utf8'));
  const cookies = session.cookies || [];
  const cookieHeader = cookies.map(c => `${c.name}=${c.value}`).join('; ');

  const strategyId = '67c935e607887b957629ad72';
  const userId = '772028948';

  async function request(url, body = {}) {
    const bodyStr = typeof body === 'string' ? body : new URLSearchParams(body).toString();

    console.log(`\n请求: POST ${url.split('/platform/')[1]?.split('?')[0] || url}`);

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
      const match = text.match(/\((.+)\)/s);
      if (match) {
        try {
          return JSON.parse(match[1]);
        } catch (e) {}
      }
      try {
        return JSON.parse(text);
      } catch (e) {
        return { raw: text.slice(0, 200) };
      }
    } catch (e) {
      return { error: e.message };
    }
  }

  // 根据已有回测记录，尝试各种参数组合
  const testCases = [
    // 案例 1: 最小参数
    {
      algo_id: strategyId,
      isajax: '1'
    },

    // 案例 2: 使用已有回测的参数格式
    {
      algo_id: strategyId,
      user_id: userId,
      start_date: '2024-01-01',
      end_date: '2024-12-31',
      capital_base: '100000',
      frequency: 'DAILY',
      benchmark: '000300.SH',
      stock_market: 'STOCK',
      isajax: '1'
    },

    // 案例 3: 不带 user_id
    {
      algo_id: strategyId,
      start_date: '2024-01-01',
      end_date: '2024-12-31',
      capital_base: '100000',
      frequency: 'DAILY',
      benchmark: '000300.SH',
      stock_market: 'STOCK',
      isajax: '1'
    },

    // 案例 4: 添加 algo_name
    {
      algo_id: strategyId,
      algo_name: 'PSY交易策略',
      start_date: '2024-01-01',
      end_date: '2024-12-31',
      capital_base: '100000',
      frequency: 'DAILY',
      benchmark: '000300.SH',
      stock_market: 'STOCK',
      isajax: '1'
    },

    // 案例 5: 使用 section 格式
    {
      algo_id: strategyId,
      section: '2024-01-01--2024-12-31',
      capital_base: '100000',
      frequency: 'DAILY',
      benchmark: '000300.SH',
      stock_market: 'STOCK',
      isajax: '1'
    },

    // 案例 6: 更简单的格式
    {
      algo_id: strategyId,
      startDate: '2024-01-01',
      endDate: '2024-12-31',
      capitalBase: '100000',
      isajax: '1'
    },

    // 案例 7: 使用 JSON 格式
    {
      algo_id: strategyId,
      config: JSON.stringify({
        start_date: '2024-01-01',
        end_date: '2024-12-31',
        capital_base: 100000,
        frequency: 'DAILY',
        benchmark: '000300.SH'
      }),
      isajax: '1'
    },

    // 案例 8: 添加更多参数
    {
      algo_id: strategyId,
      user_id: userId,
      start_date: '2024-01-01',
      end_date: '2024-12-31',
      capital_base: '100000',
      frequency: 'DAILY',
      benchmark: '000300.SH',
      stock_market: 'STOCK',
      language: 'PYTHON',
      run_type: 'BACKTEST',
      isajax: '1'
    },

    // 案例 9: 使用 algoId
    {
      algoId: strategyId,
      userId: userId,
      startDate: '2024-01-01',
      endDate: '2024-12-31',
      capitalBase: '100000',
      frequency: 'DAILY',
      benchmark: '000300.SH',
      isajax: '1'
    },

    // 案例 10: 检查是否需要 code 参数
    {
      algo_id: strategyId,
      user_id: userId,
      start_date: '2024-01-01',
      end_date: '2024-12-31',
      capital_base: '100000',
      frequency: 'DAILY',
      benchmark: '000300.SH',
      stock_market: 'STOCK',
      language: 'PYTHON',
      isajax: '1'
    }
  ];

  console.log('\n开始测试参数组合...');

  const results = [];

  for (let i = 0; i < testCases.length; i++) {
    const params = testCases[i];
    console.log(`\n--- 测试案例 ${i + 1} ---`);
    console.log('参数:', JSON.stringify(params, null, 2));

    const result = await request(
      'https://quant.10jqka.com.cn/platform/backtest/run/',
      params
    );

    const status = result.errorcode === 0 ? '✓ 成功' :
                   result.errorcode ? `✗ errorcode=${result.errorcode}` : '? 未知';

    console.log(`状态: ${status}`);
    if (result.errormsg) console.log(`消息: ${result.errormsg}`);
    if (result.result) console.log(`结果: ${JSON.stringify(result.result).slice(0, 100)}`);

    results.push({
      case: i + 1,
      params,
      result
    });

    // 如果成功，停止并保存
    if (result.errorcode === 0 && result.result?.backtest_id) {
      console.log('\n★ 成功找到正确的参数组合！');
      break;
    }
  }

  // 尝试查询回测状态看看是否有新回测
  console.log('\n\n--- 检查是否有新回测 ---');
  const latestBacktest = await request(
    'https://quant.10jqka.com.cn/platform/backtest/querylatest/',
    { algoId: strategyId, query: 'status', datatype: 'jsonp', isajax: '1' }
  );

  console.log('最新回测状态:', latestBacktest);

  // 保存结果
  const output = {
    testResults: results,
    latestBacktest,
    timestamp: Date.now()
  };

  fs.writeFileSync(path.join(OUTPUT_ROOT, 'backtest-param-probe.json'), JSON.stringify(output, null, 2));

  console.log('\n' + '='.repeat(70));
  console.log('测试完成，结果已保存');
}

probeBacktestParams().catch(console.error);