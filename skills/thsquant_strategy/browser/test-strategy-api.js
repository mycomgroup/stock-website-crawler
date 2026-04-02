#!/usr/bin/env node
/**
 * THSQuant 策略API测试
 * 测试发现的真实API端点
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import '../load-env.js';
import { SESSION_FILE, OUTPUT_ROOT } from '../paths.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function testStrategyAPIs() {
  console.log('\n' + '='.repeat(70));
  console.log('THSQuant 策略API测试');
  console.log('='.repeat(70));

  // 加载session
  const session = JSON.parse(fs.readFileSync(SESSION_FILE, 'utf8'));
  const cookies = session.cookies || [];
  const cookieHeader = cookies.map(c => `${c.name}=${c.value}`).join('; ');

  console.log(`\nSession: ${cookies.length} cookies`);

  const baseUrl = 'https://quant.10jqka.com.cn';

  // 发现的真实API
  const endpoints = [
    { name: '算法/策略列表', path: '/platform/algorithms/queryall2/', method: 'POST' },
    { name: '用户认证', path: '/platform/user/getauthdata', method: 'POST' },
  ];

  console.log('\n测试策略API...\n');

  // 1. 获取策略列表
  console.log('1. 获取策略列表 (algorithms/queryall2/)...');
  try {
    const resp = await fetch(`${baseUrl}/platform/algorithms/queryall2/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': cookieHeader,
        'User-Agent': 'Mozilla/5.0',
        'X-Requested-With': 'XMLHttpRequest'
      },
      body: 'isajax=1&datatype=jsonp'
    });

    const text = await resp.text();
    console.log(`Status: ${resp.status}`);

    // 解析JSONP响应
    const jsonpMatch = text.match(/\((.+)\)/);
    if (jsonpMatch) {
      const data = JSON.parse(jsonpMatch[1]);
      console.log(`Errorcode: ${data.errorcode}`);
      console.log(`Errormsg: ${data.errormsg || '无'}`);

      if (data.result) {
        console.log(`\n策略列表:`);
        if (Array.isArray(data.result)) {
          data.result.forEach((item, i) => {
            console.log(`  ${i + 1}. ${item.name || item.title || '未命名'} (ID: ${item._id || item.id || '?'})`);
          });
        } else {
          console.log(JSON.stringify(data.result, null, 2).substring(0, 500));
        }
      }
    }
  } catch (e) {
    console.log(`Error: ${e.message}`);
  }

  // 2. 尝试创建策略
  console.log('\n\n2. 探索策略创建API...');

  const createEndpoints = [
    '/platform/algorithms/create/',
    '/platform/algorithms/add/',
    '/platform/algorithms/new/',
    '/platform/strategy/create/',
    '/platform/strategy/add/',
  ];

  for (const ep of createEndpoints) {
    try {
      const resp = await fetch(`${baseUrl}${ep}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'Cookie': cookieHeader,
          'User-Agent': 'Mozilla/5.0'
        },
        body: 'isajax=1'
      });

      const text = await resp.text();
      if (!text.includes('404') && !text.includes('Not Found')) {
        console.log(`\n${ep}: Status ${resp.status}`);
        console.log(`  Response: ${text.substring(0, 100)}`);
      }
    } catch (e) {}
  }

  // 3. 探索回测API
  console.log('\n\n3. 探索回测API...');

  const backtestEndpoints = [
    '/platform/backtest/create/',
    '/platform/backtest/run/',
    '/platform/backtest/start/',
    '/platform/algorithms/backtest/',
    '/platform/algorithms/run/',
  ];

  for (const ep of backtestEndpoints) {
    try {
      const resp = await fetch(`${baseUrl}${ep}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'Cookie': cookieHeader,
          'User-Agent': 'Mozilla/5.0'
        },
        body: 'isajax=1'
      });

      const text = await resp.text();
      if (!text.includes('404') && !text.includes('Not Found')) {
        console.log(`\n${ep}: Status ${resp.status}`);
        console.log(`  Response: ${text.substring(0, 100)}`);
      }
    } catch (e) {}
  }
}

testStrategyAPIs().catch(err => {
  console.error('\n✗ 失败:', err.message);
  process.exit(1);
});