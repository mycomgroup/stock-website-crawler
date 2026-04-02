#!/usr/bin/env node
/**
 * THSQuant API 详细探索
 * 使用有效session探索所有可能的API端点
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import '../load-env.js';
import { SESSION_FILE, OUTPUT_ROOT } from '../paths.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function exploreAPIs() {
  console.log('\n' + '='.repeat(70));
  console.log('THSQuant API 详细探索');
  console.log('='.repeat(70));

  // 加载session
  const session = JSON.parse(fs.readFileSync(SESSION_FILE, 'utf8'));
  const cookies = session.cookies || [];
  const cookieHeader = cookies.map(c => `${c.name}=${c.value}`).join('; ');

  console.log(`\nSession: ${cookies.length} cookies`);

  const baseUrl = 'https://quant.10jqka.com.cn';

  // 可能的API端点列表
  const endpoints = [
    // 用户相关
    { path: '/platform/user/getauthdata', method: 'POST', body: 'isajax=1' },
    { path: '/platform/user/info', method: 'POST', body: 'isajax=1' },
    { path: '/platform/user/info/', method: 'POST', body: 'isajax=1' },

    // 策略相关 - 尝试各种可能的路径
    { path: '/platform/strategy/list', method: 'POST', body: 'isajax=1' },
    { path: '/platform/strategy/mylist', method: 'POST', body: 'isajax=1' },
    { path: '/platform/strategy/my', method: 'POST', body: 'isajax=1' },
    { path: '/platform/strategy/getMyStrategyList', method: 'POST', body: 'isajax=1' },
    { path: '/platform/research/strategylist', method: 'POST', body: 'isajax=1' },
    { path: '/platform/research/mystrategy', method: 'POST', body: 'isajax=1' },
    { path: '/platform/backtest/mystrategy', method: 'POST', body: 'isajax=1' },

    // 回测相关
    { path: '/platform/backtest/list', method: 'POST', body: 'isajax=1' },
    { path: '/platform/backtest/mylist', method: 'POST', body: 'isajax=1' },
    { path: '/platform/backtest/history', method: 'POST', body: 'isajax=1' },
    { path: '/platform/backtest/results', method: 'POST', body: 'isajax=1' },

    // 研究环境
    { path: '/platform/research/list', method: 'POST', body: 'isajax=1' },
    { path: '/platform/research/my', method: 'POST', body: 'isajax=1' },
    { path: '/platform/jupyter/list', method: 'POST', body: 'isajax=1' },

    // 因子
    { path: '/platform/factor/list', method: 'POST', body: 'isajax=1' },
    { path: '/platform/factor/my', method: 'POST', body: 'isajax=1' },
    { path: '/platform/sfactor/list', method: 'POST', body: 'isajax=1' },

    // 模拟交易
    { path: '/platform/simuaccount/getyybidlist', method: 'POST', body: 'isajax=1' },
    { path: '/platform/simupaper/queryall/', method: 'POST', body: 'isajax=1' },
    { path: '/platform/simutrade/list', method: 'POST', body: 'isajax=1' },

    // 其他可能的端点
    { path: '/platform/stock/pool', method: 'POST', body: 'isajax=1' },
    { path: '/platform/data/query', method: 'POST', body: 'isajax=1' },
    { path: '/platform/algo/list', method: 'POST', body: 'isajax=1' },
    { path: '/platform/algorithm/list', method: 'POST', body: 'isajax=1' },
  ];

  const results = {};
  const workingAPIs = [];

  console.log('\n测试API端点...\n');

  for (const ep of endpoints) {
    const url = `${baseUrl}${ep.path}`;
    console.log(`测试: ${ep.path}`);

    try {
      const response = await fetch(url, {
        method: ep.method,
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'Cookie': cookieHeader,
          'User-Agent': 'Mozilla/5.0',
          'X-Requested-With': 'XMLHttpRequest'
        },
        body: ep.body
      });

      const text = await response.text();
      let data;
      try {
        data = JSON.parse(text);
      } catch (e) {
        data = { rawText: text.substring(0, 200) };
      }

      const result = {
        status: response.status,
        errorcode: data.errorcode,
        errormsg: data.errormsg,
        hasResult: !!data.result,
        resultType: data.result ? (Array.isArray(data.result) ? 'array' : typeof data.result) : null
      };

      if (data.result) {
        if (Array.isArray(data.result)) {
          result.resultCount = data.result.length;
          result.sample = data.result.slice(0, 2);
        } else if (typeof data.result === 'object') {
          result.resultKeys = Object.keys(data.result);
        }
      }

      results[ep.path] = result;

      // 记录成功的API
      if (result.errorcode === 0 || result.hasResult) {
        workingAPIs.push({
          path: ep.path,
          ...result
        });
        console.log(`  ✓ 成功: errorcode=${result.errorcode}, hasResult=${result.hasResult}`);
      } else {
        console.log(`  - 无结果`);
      }

    } catch (error) {
      results[ep.path] = { error: error.message };
      console.log(`  ✗ Error: ${error.message}`);
    }
  }

  // 保存完整结果
  fs.writeFileSync(path.join(OUTPUT_ROOT, 'api-explore-results.json'), JSON.stringify(results, null, 2));

  // 打印工作API汇总
  console.log('\n' + '='.repeat(70));
  console.log('成功的API端点:');
  console.log('='.repeat(70));

  workingAPIs.forEach(api => {
    console.log(`\n${api.path}`);
    console.log(`  Status: ${api.status}`);
    console.log(`  Errorcode: ${api.errorcode}`);
    if (api.resultCount !== undefined) {
      console.log(`  结果数量: ${api.resultCount}`);
    }
    if (api.resultKeys) {
      console.log(`  结果字段: ${api.resultKeys.slice(0, 5).join(', ')}${api.resultKeys.length > 5 ? '...' : ''}`);
    }
  });

  console.log(`\n共发现 ${workingAPIs.length} 个可用API端点`);
  console.log(`\n完整结果已保存: ${OUTPUT_ROOT}/api-explore-results.json`);

  return workingAPIs;
}

exploreAPIs().catch(err => {
  console.error('\n✗ 失败:', err.message);
  process.exit(1);
});