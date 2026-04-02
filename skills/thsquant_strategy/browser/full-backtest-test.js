#!/usr/bin/env node
/**
 * 完整的回测运行参数测试
 * 包含策略代码等所有可能的参数
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import '../load-env.js';
import { SESSION_FILE, OUTPUT_ROOT } from '../paths.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function fullBacktestTest() {
  console.log('\n' + '='.repeat(70));
  console.log('完整回测参数测试');
  console.log('='.repeat(70));

  const session = JSON.parse(fs.readFileSync(SESSION_FILE, 'utf8'));
  const cookies = session.cookies || [];
  const cookieHeader = cookies.map(c => `${c.name}=${c.value}`).join('; ');

  const strategyId = '67c935e607887b957629ad72';
  const userId = '772028948';

  // 简单策略代码
  const simpleCode = `# 简单策略
def initialize(context):
    g.stock = "000001.XSHE"

def handle_bar(context, bar_dict):
    stock = g.stock
    if stock not in context.portfolio.positions:
        order_target_percent(stock, 1.0)
`;

  async function request(url, body = {}) {
    const bodyStr = typeof body === 'string' ? body : new URLSearchParams(body).toString();

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
        try { return JSON.parse(match[1]); } catch (e) {}
      }
      try { return JSON.parse(text); } catch (e) { return { raw: text.slice(0, 200) }; }
    } catch (e) {
      return { error: e.message };
    }
  }

  // 测试案例 - 包含策略代码
  const testCases = [
    // 1. 包含代码
    {
      algo_id: strategyId,
      user_id: userId,
      algo_code: simpleCode,
      start_date: '2024-01-01',
      end_date: '2024-12-31',
      capital_base: '100000',
      frequency: 'DAILY',
      benchmark: '000300.SH',
      stock_market: 'STOCK',
      language: 'PYTHON',
      isajax: '1'
    },

    // 2. 使用 code 参数
    {
      algo_id: strategyId,
      user_id: userId,
      code: simpleCode,
      start_date: '2024-01-01',
      end_date: '2024-12-31',
      capital_base: '100000',
      frequency: 'DAILY',
      benchmark: '000300.SH',
      isajax: '1'
    },

    // 3. 尝试 save + run 组合
    {
      algo_id: strategyId,
      algo_name: 'PSY交易策略',
      algo_code: simpleCode,
      stock_market: 'STOCK',
      start_date: '2024-01-01',
      end_date: '2024-12-31',
      capital_base: '100000',
      frequency: 'DAILY',
      benchmark: '000300.SH',
      run_backtest: '1',
      isajax: '1'
    },

    // 4. 更简单的代码
    {
      algo_id: strategyId,
      code: '# test',
      start_date: '2024-01-01',
      end_date: '2024-12-31',
      isajax: '1'
    },

    // 5. 包含所有可能的字段
    {
      algo_id: strategyId,
      user_id: userId,
      algo_name: 'PSY交易策略',
      algo_code: simpleCode,
      start_date: '2024-01-01',
      end_date: '2024-12-31',
      begin_date: '2024-01-01',
      end_date: '2024-12-31',
      capital_base: '100000',
      initial_capital: '100000',
      frequency: 'DAILY',
      freq: 'DAILY',
      benchmark: '000300.SH',
      stock_market: 'STOCK',
      language: 'PYTHON',
      run_type: 'BACKTEST',
      isajax: '1'
    }
  ];

  console.log('\n测试包含代码的参数...\n');

  for (let i = 0; i < testCases.length; i++) {
    const params = testCases[i];
    console.log(`--- 测试 ${i + 1} ---`);

    const result = await request(
      'https://quant.10jqka.com.cn/platform/backtest/run/',
      params
    );

    console.log(`状态: ${result.errorcode === 0 ? '✓ 成功' : `✗ errorcode=${result.errorcode}`}`);
    if (result.errormsg) console.log(`消息: ${result.errormsg}`);

    if (result.errorcode === 0) {
      console.log('\n★ 找到正确的参数组合！');
      console.log('参数:', JSON.stringify(params, null, 2));
      console.log('结果:', JSON.stringify(result, null, 2));
      break;
    }
  }

  // 尝试先保存策略，再运行回测
  console.log('\n\n--- 尝试保存策略 + 运行回测 ---');

  // 先尝试编辑/保存 API
  const editResult = await request(
    'https://quant.10jqka.com.cn/platform/algorithms/edit/',
    {
      algo_id: strategyId,
      user_id: userId,
      algo_name: 'PSY交易策略',
      algo_code: simpleCode,
      stock_market: 'STOCK',
      isajax: '1'
    }
  );

  console.log('保存结果:', editResult);

  // 再尝试运行回测
  const runResult = await request(
    'https://quant.10jqka.com.cn/platform/backtest/run/',
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
    }
  );

  console.log('运行结果:', runResult);

  // 检查最新回测状态
  const latestStatus = await request(
    'https://quant.10jqka.com.cn/platform/backtest/querylatest/',
    { algoId: strategyId, query: 'status', datatype: 'jsonp', isajax: '1' }
  );

  console.log('\n最新回测状态:', latestStatus);

  console.log('\n' + '='.repeat(70));
  console.log('结论：HTTP API 运行回测需要特殊参数或令牌');
  console.log('建议：使用浏览器自动化方式运行回测');
  console.log('='.repeat(70));
}

fullBacktestTest().catch(console.error);