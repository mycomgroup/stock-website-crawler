#!/usr/bin/env node
/**
 * 捕获回测运行的真实 POST 参数
 * 用已有 session 打开编辑器，自动点击运行回测，拦截真实请求
 */

import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import '../load-env.js';
import { SESSION_FILE, OUTPUT_ROOT } from '../paths.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// 用已知有回测历史的策略
const TEST_ALGO_ID = '67c935e607887b957629ad72'; // PSY交易策略

async function captureBacktestRunParams() {
  console.log('='.repeat(60));
  console.log('捕获回测运行真实参数');
  console.log('='.repeat(60));

  const session = JSON.parse(fs.readFileSync(SESSION_FILE, 'utf8'));
  const cookies = session.cookies || [];
  console.log(`加载 session: ${cookies.length} 个 cookie`);

  const browser = await chromium.launch({
    headless: true,
    args: ['--disable-blink-features=AutomationControlled', '--no-sandbox']
  });

  const context = await browser.newContext({
    viewport: { width: 1400, height: 900 },
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36'
  });

  await context.addCookies(cookies);
  const page = await context.newPage();

  // 拦截所有 platform API 请求
  const captured = [];
  page.on('request', req => {
    const url = req.url();
    if (url.includes('quant.10jqka.com.cn/platform/')) {
      const entry = {
        url: url.split('?')[0],
        fullUrl: url,
        method: req.method(),
        postData: req.postData(),
        time: Date.now()
      };
      captured.push(entry);
      if (req.method() === 'POST') {
        console.log(`→ POST ${entry.url.replace('https://quant.10jqka.com.cn', '')}`);
        if (entry.postData) console.log(`  body: ${entry.postData.slice(0, 120)}`);
      }
    }
  });

  page.on('response', async resp => {
    const url = resp.url();
    if (url.includes('quant.10jqka.com.cn/platform/')) {
      const entry = captured.find(c => c.fullUrl === url && !c.status);
      if (entry) {
        entry.status = resp.status();
        try {
          const text = await resp.text();
          entry.responseRaw = text.slice(0, 800);
          const jsonpMatch = text.match(/\((.+)\)/s);
          const jsonStr = jsonpMatch ? jsonpMatch[1] : text;
          try { entry.responseJson = JSON.parse(jsonStr); } catch (e) {}
        } catch (e) {}
      }
    }
  });

  try {
    // 1. 验证登录
    console.log('\n1. 验证登录状态...');
    await page.goto('https://quant.10jqka.com.cn/view/study-index.html', {
      waitUntil: 'domcontentloaded', timeout: 30000
    });
    await page.waitForTimeout(3000);

    const loginOk = await page.evaluate(async () => {
      const r = await fetch('/platform/user/getauthdata', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: 'isajax=1'
      });
      const d = await r.json();
      return d.errorcode === 0 ? d.result.user_id : null;
    });

    if (!loginOk) {
      console.log('✗ Session 已过期');
      await browser.close();
      return null;
    }
    console.log(`✓ 已登录，user_id: ${loginOk}`);

    // 2. 获取策略信息
    console.log(`\n2. 获取策略信息 (${TEST_ALGO_ID})...`);
    const algoInfo = await page.evaluate(async (algoId) => {
      const r = await fetch('/platform/algorithms/queryinfo/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded', 'X-Requested-With': 'XMLHttpRequest' },
        body: `algoId=${algoId}&isajax=1`
      });
      const text = await r.text();
      try { return JSON.parse(text); } catch (e) { return { raw: text.slice(0, 200) }; }
    }, TEST_ALGO_ID);

    console.log('策略:', algoInfo?.result?.algo_name, '| 语言:', algoInfo?.result?.language);
    const algoCode = algoInfo?.result?.algo_code || '';

    // 3. 打开编辑器页面，让平台 JS 加载完整
    console.log(`\n3. 打开编辑器页面...`);
    const editorUrl = `https://quant.10jqka.com.cn/platform/study/html/editor.html?algo_id=${TEST_ALGO_ID}`;
    await page.goto(editorUrl, { waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForTimeout(5000);

    // 4. 探测回测运行端点（在页面上下文中，带完整 cookie）
    console.log('\n4. 探测回测运行端点...');

    const endpointTests = await page.evaluate(async (params) => {
      const { algoId, userId, code } = params;
      const results = {};

      const endpoints = [
        '/platform/backtest/run/',
        '/platform/backtest/start/',
        '/platform/algorithms/backtest/',
        '/platform/algorithms/run/',
        '/platform/backtest/create/',
        '/platform/backtest/submit/',
        '/platform/backtest/add/',
      ];

      // 不同参数格式
      const paramSets = [
        `algo_id=${algoId}&section=2024-01-01--2024-12-31&capital_base=100000&frequency=DAILY&benchmark=000300.SH&isajax=1`,
        `algo_id=${algoId}&start_date=2024-01-01&end_date=2024-12-31&capital_base=100000&frequency=DAILY&benchmark=000300.SH&isajax=1`,
        `algo_id=${algoId}&user_id=${userId}&section=2024-01-01--2024-12-31&capital_base=100000&frequency=DAILY&benchmark=000300.SH&isajax=1`,
        `algo_id=${algoId}&section=2024-01-01--2024-12-31&capital_base=100000&frequency=DAILY&benchmark=000300.SH&stock_market=STOCK&isajax=1`,
        `algo_id=${algoId}&section=2024-01-01--2024-12-31&capital_base=100000&frequency=DAILY&benchmark=000300.SH&language=PYTHON&isajax=1`,
      ];

      for (const endpoint of endpoints) {
        results[endpoint] = [];
        for (let i = 0; i < paramSets.length; i++) {
          try {
            const r = await fetch(endpoint, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-Requested-With': 'XMLHttpRequest',
                'Accept': 'application/json, text/javascript, */*; q=0.01'
              },
              body: paramSets[i]
            });
            const text = await r.text();
            let data;
            try {
              const m = text.match(/\((.+)\)/s);
              data = m ? JSON.parse(m[1]) : JSON.parse(text);
            } catch (e) {
              data = { raw: text.slice(0, 100) };
            }
            const entry = { paramSet: i, errorcode: data.errorcode, errormsg: data.errormsg, result: data.result };
            results[endpoint].push(entry);
            if (data.errorcode === 0) break;
          } catch (e) {
            results[endpoint].push({ paramSet: i, error: e.message });
          }
        }
      }
      return results;
    }, { algoId: TEST_ALGO_ID, userId: loginOk, code: algoCode });

    console.log('\n端点探测结果:');
    let foundEndpoint = null;
    let foundParams = null;
    for (const [ep, tests] of Object.entries(endpointTests)) {
      for (const t of tests) {
        if (t.errorcode === 0) {
          console.log(`  ✓ ${ep} [params${t.paramSet}]: 成功! result=${JSON.stringify(t.result).slice(0, 100)}`);
          foundEndpoint = ep;
          foundParams = t.paramSet;
        } else if (t.errorcode !== undefined) {
          console.log(`  ✗ ${ep} [params${t.paramSet}]: ${t.errorcode} ${t.errormsg || ''}`);
        }
      }
    }

    // 5. 尝试通过 jQuery AJAX（平台内部方式）
    console.log('\n5. 尝试 jQuery AJAX 方式...');
    const jqResult = await page.evaluate(async (algoId) => {
      if (typeof jQuery === 'undefined') return { error: 'no jQuery' };
      return new Promise(resolve => {
        jQuery.ajax({
          url: '/platform/backtest/run/',
          type: 'POST',
          dataType: 'jsonp',
          data: {
            algo_id: algoId,
            section: '2024-01-01--2024-12-31',
            capital_base: 100000,
            frequency: 'DAILY',
            benchmark: '000300.SH',
            isajax: 1,
            datatype: 'jsonp'
          },
          success: d => resolve({ ok: true, data: d }),
          error: (xhr, s, e) => resolve({ error: e, status: s, responseText: xhr.responseText?.slice(0, 200) })
        });
        setTimeout(() => resolve({ timeout: true }), 8000);
      });
    }, TEST_ALGO_ID);
    console.log('jQuery 结果:', JSON.stringify(jqResult).slice(0, 200));

    // 6. 尝试找到平台内部的 backtest 函数
    console.log('\n6. 探索平台内部 backtest 函数...');
    const internalFns = await page.evaluate(() => {
      const fns = {};
      // 查找全局 backtest 相关函数
      for (const key of Object.keys(window)) {
        if (key.toLowerCase().includes('backtest') || key.toLowerCase().includes('run') || key.toLowerCase().includes('algo')) {
          try {
            const val = window[key];
            fns[key] = typeof val === 'function' ? 'function' : typeof val;
          } catch (e) {}
        }
      }
      // 查找 Vue 实例中的方法
      const app = document.querySelector('#app, [id*="app"]');
      if (app && app.__vue__) {
        const methods = Object.keys(app.__vue__.$options?.methods || {});
        fns._vueMethods = methods.filter(m => m.toLowerCase().includes('backtest') || m.toLowerCase().includes('run'));
      }
      return fns;
    });
    console.log('内部函数:', JSON.stringify(internalFns).slice(0, 300));

    // 保存结果
    const outputPath = path.join(OUTPUT_ROOT, 'backtest-run-params-capture.json');
    fs.writeFileSync(outputPath, JSON.stringify({
      captured: captured.filter(c => c.method === 'POST'),
      endpointTests,
      jqResult,
      internalFns,
      foundEndpoint,
      foundParams,
      algoInfo: algoInfo?.result ? {
        algo_id: algoInfo.result._id,
        algo_name: algoInfo.result.algo_name,
        language: algoInfo.result.language,
        stock_market: algoInfo.result.stock_market
      } : null,
      timestamp: Date.now()
    }, null, 2));
    console.log(`\n保存到: ${outputPath}`);

    await browser.close();
    return { foundEndpoint, endpointTests };

  } catch (err) {
    console.error('错误:', err.message);
    try { await page.screenshot({ path: path.join(OUTPUT_ROOT, 'capture-run-error.png') }); } catch (e) {}
    await browser.close();
    throw err;
  }
}

captureBacktestRunParams().then(result => {
  if (result?.foundEndpoint) {
    console.log(`\n✓ 找到有效端点: ${result.foundEndpoint}`);
  } else {
    console.log('\n⚠ 未找到有效端点，查看 data/backtest-run-params-capture.json');
  }
}).catch(err => {
  console.error('✗ 失败:', err.message);
  process.exit(1);
});
