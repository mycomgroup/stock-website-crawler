#!/usr/bin/env node
/**
 * THSQuant 纯API测试工具
 * 使用已保存的session测试所有发现的API端点
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import '../load-env.js';
import { SESSION_FILE, OUTPUT_ROOT } from '../paths.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function testAllAPIs() {
  console.log('\n' + '='.repeat(70));
  console.log('THSQuant API 端点测试');
  console.log('='.repeat(70));

  // 加载session
  if (!fs.existsSync(SESSION_FILE)) {
    console.log('\n✗ 没有找到session文件，请先登录');
    console.log('运行: node browser/manual-login-capture.js');
    process.exit(1);
  }

  const session = JSON.parse(fs.readFileSync(SESSION_FILE, 'utf8'));
  const cookies = session.cookies || [];

  // 构建cookie header
  const cookieHeader = cookies.map(c => `${c.name}=${c.value}`).join('; ');
  console.log(`\nSession: ${cookies.length} cookies`);
  console.log(`QUANT_RESEARCH_SESSIONID: ${cookies.find(c => c.name === 'QUANT_RESEARCH_SESSIONID')?.value || '未找到'}`);

  const baseUrl = 'https://quant.10jqka.com.cn';

  // 所有发现的API端点
  const endpoints = [
    // 用户相关
    { name: '用户认证', path: '/platform/user/getauthdata', method: 'POST' },

    // 策略相关
    { name: '策略列表', path: '/platform/strategy/list', method: 'POST' },
    { name: '我的策略', path: '/platform/strategy/mylist', method: 'POST' },
    { name: '研究策略列表', path: '/platform/research/strategylist', method: 'POST' },

    // 回测相关
    { name: '回测列表', path: '/platform/backtest/list', method: 'POST' },

    // 模拟交易
    { name: '模拟账户', path: '/platform/simuaccount/getyybidlist', method: 'POST' },
    { name: '模拟交易查询', path: '/platform/simupaper/queryall/', method: 'POST' },

    // 帮助文档
    { name: '帮助目录', path: '/platform/newhelp/directory', method: 'POST' },

    // 可能的其他端点
    { name: '因子研究', path: '/platform/factor/list', method: 'POST' },
    { name: '研究环境', path: '/platform/research/list', method: 'POST' },
  ];

  const results = {};

  console.log('\n测试API端点...\n');

  for (const endpoint of endpoints) {
    const url = `${baseUrl}${endpoint.path}`;
    console.log(`测试: ${endpoint.name} (${endpoint.path})`);

    try {
      const response = await fetch(url, {
        method: endpoint.method,
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'Cookie': cookieHeader,
          'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
          'X-Requested-With': 'XMLHttpRequest'
        },
        body: 'isajax=1'
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
        resultType: data.result ? typeof data.result : null
      };

      // 如果有结果，显示摘要
      if (data.result) {
        if (Array.isArray(data.result)) {
          result.resultCount = data.result.length;
          result.sample = data.result.slice(0, 2);
        } else if (typeof data.result === 'object') {
          result.resultKeys = Object.keys(data.result);
          result.sample = JSON.stringify(data.result).substring(0, 150);
        }
      }

      results[endpoint.path] = result;

      console.log(`  Status: ${result.status}, Errorcode: ${result.errorcode}`);
      if (result.errorcode === 0) {
        console.log(`  ✓ 成功! 有结果: ${result.hasResult}`);
        if (result.resultCount !== undefined) {
          console.log(`  结果数量: ${result.resultCount}`);
        }
        if (result.resultKeys) {
          console.log(`  结果字段: ${result.resultKeys.join(', ')}`);
        }
      } else {
        console.log(`  ✗ ${result.errormsg}`);
      }

    } catch (error) {
      results[endpoint.path] = { error: error.message };
      console.log(`  ✗ Error: ${error.message}`);
    }

    console.log();
  }

  // 保存结果
  const resultPath = path.join(OUTPUT_ROOT, 'api-test-results.json');
  fs.writeFileSync(resultPath, JSON.stringify(results, null, 2));
  console.log(`\n结果已保存: ${resultPath}`);

  // 统计
  const successful = Object.values(results).filter(r => r.errorcode === 0).length;
  const failed = Object.values(results).filter(r => r.errorcode === -1).length;

  console.log('\n' + '='.repeat(70));
  console.log('测试统计');
  console.log('='.repeat(70));
  console.log(`成功: ${successful}`);
  console.log(`失败(未登录): ${failed}`);
  console.log(`错误: ${Object.values(results).filter(r => r.error).length}`);

  // 如果有成功的API，显示详细信息
  if (successful > 0) {
    console.log('\n成功的API端点:');
    Object.entries(results).forEach(([path, result]) => {
      if (result.errorcode === 0) {
        console.log(`  ${path}`);
        if (result.resultCount !== undefined) {
          console.log(`    - 结果数量: ${result.resultCount}`);
        }
        if (result.resultKeys) {
          console.log(`    - 字段: ${result.resultKeys.join(', ')}`);
        }
      }
    });
  }

  return results;
}

testAllAPIs().catch(err => {
  console.error('\n✗ 失败:', err.message);
  process.exit(1);
});