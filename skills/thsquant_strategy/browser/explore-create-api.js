#!/usr/bin/env node
/**
 * THSQuant 策略创建API探索
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import '../load-env.js';
import { SESSION_FILE, OUTPUT_ROOT } from '../paths.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function exploreCreateAPI() {
  // 加载session
  const session = JSON.parse(fs.readFileSync(SESSION_FILE, 'utf8'));
  const cookies = session.cookies || [];
  const cookieHeader = cookies.map(c => `${c.name}=${c.value}`).join('; ');

  const baseUrl = 'https://quant.10jqka.com.cn';

  // 首先获取用户ID
  const authResp = await fetch(`${baseUrl}/platform/user/getauthdata`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Cookie': cookieHeader
    },
    body: 'isajax=1'
  });
  const authData = await authResp.json();
  const userId = authData.result?.user_id;
  console.log('用户ID:', userId);

  // 尝试不同的参数组合
  const testCases = [
    // 格式1
    new URLSearchParams({
      isajax: '1',
      user_id: userId,
      algo_name: 'API测试策略',
      code: '# test',
      stock_market: 'STOCK'
    }).toString(),

    // 格式2 - JSON
    JSON.stringify({
      user_id: userId,
      algo_name: 'API测试策略',
      code: '# test',
      stock_market: 'STOCK'
    }),

    // 格式3
    new URLSearchParams({
      isajax: '1',
      userid: userId,
      name: 'API测试策略',
      code: '# test'
    }).toString(),

    // 格式4
    new URLSearchParams({
      isajax: '1',
      algo_name: 'API测试策略',
      code: '# test',
      stock_market: 'STOCK'
    }).toString(),
  ];

  console.log('\n测试创建策略API...\n');

  for (let i = 0; i < testCases.length; i++) {
    const body = testCases[i];
    console.log(`测试 ${i + 1}:`);
    console.log(`  Body: ${body.substring(0, 80)}...`);

    try {
      const resp = await fetch(`${baseUrl}/platform/algorithms/add/`, {
        method: 'POST',
        headers: {
          'Content-Type': i === 1 ? 'application/json' : 'application/x-www-form-urlencoded',
          'Cookie': cookieHeader,
          'User-Agent': 'Mozilla/5.0'
        },
        body
      });

      const text = await resp.text();
      console.log(`  Response: ${text.substring(0, 150)}`);

      // 检查是否成功
      if (text.includes('"errorcode":0')) {
        console.log('  ✓ 成功!');
      }
    } catch (e) {
      console.log(`  Error: ${e.message}`);
    }

    console.log();
  }

  // 尝试其他端点
  console.log('尝试其他创建端点...\n');

  const otherEndpoints = [
    '/platform/algorithms/create/',
    '/platform/algorithms/new/',
    '/platform/algorithms/save/',
  ];

  for (const ep of otherEndpoints) {
    const body = new URLSearchParams({
      isajax: '1',
      algo_name: 'API测试策略',
      code: '# test strategy'
    }).toString();

    try {
      const resp = await fetch(`${baseUrl}${ep}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'Cookie': cookieHeader
        },
        body
      });

      const text = await resp.text();
      console.log(`${ep}:`);
      console.log(`  Status: ${resp.status}`);
      console.log(`  Response: ${text.substring(0, 100)}`);
      console.log();
    } catch (e) {
      console.log(`${ep}: ${e.message}\n`);
    }
  }
}

exploreCreateAPI().catch(console.error);