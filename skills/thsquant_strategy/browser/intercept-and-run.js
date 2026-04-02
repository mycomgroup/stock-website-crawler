#!/usr/bin/env node
/**
 * 打开浏览器，拦截所有请求，让用户手动点击回测
 * 捕获真实的回测运行 POST 参数
 */

import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import readline from 'node:readline';
import { fileURLToPath } from 'node:url';
import '../load-env.js';
import { SESSION_FILE, OUTPUT_ROOT } from '../paths.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function interceptAndRun() {
  console.log('='.repeat(60));
  console.log('拦截回测请求 - 请在浏览器中手动点击回测');
  console.log('='.repeat(60));

  const session = JSON.parse(fs.readFileSync(SESSION_FILE, 'utf8'));
  const cookies = session.cookies || [];

  const browser = await chromium.launch({
    headless: false,
    args: ['--disable-blink-features=AutomationControlled']
  });

  const context = await browser.newContext({
    viewport: { width: 1400, height: 900 },
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36'
  });

  await context.addCookies(cookies);
  const page = await context.newPage();

  // 拦截所有 platform POST
  const captured = [];
  page.on('request', req => {
    const url = req.url();
    if (url.includes('quant.10jqka.com.cn/platform/') && req.method() === 'POST') {
      const entry = { url: url.split('?')[0], fullUrl: url, postData: req.postData(), time: Date.now() };
      captured.push(entry);
      const p = entry.url.replace('https://quant.10jqka.com.cn', '');
      // 打印所有非常规请求
      if (!p.includes('message') && !p.includes('checknew') && !p.includes('getauth') && !p.includes('newhelp') && !p.includes('queryall2')) {
        console.log(`\n★ POST ${p}`);
        if (entry.postData) console.log(`  body: ${entry.postData}`);
      }
    }
  });

  page.on('response', async resp => {
    const url = resp.url();
    if (url.includes('quant.10jqka.com.cn/platform/') && resp.request().method() === 'POST') {
      const entry = captured.find(c => c.fullUrl === url && !c.status);
      if (entry) {
        entry.status = resp.status();
        try {
          const text = await resp.text();
          entry.responseRaw = text.slice(0, 800);
          const m = text.match(/\((.+)\)/s);
          try { entry.responseJson = JSON.parse(m ? m[1] : text); } catch (e) {}
          const p = entry.url.replace('https://quant.10jqka.com.cn', '');
          if (!p.includes('message') && !p.includes('checknew') && !p.includes('getauth') && !p.includes('newhelp') && !p.includes('queryall2')) {
            console.log(`  ← ${text.slice(0, 200)}`);
          }
        } catch (e) {}
      }
    }
  });

  try {
    // 打开策略列表
    console.log('\n打开策略列表...');
    await page.goto('https://quant.10jqka.com.cn/view/study-index.html', {
      waitUntil: 'networkidle', timeout: 30000
    });
    await page.waitForTimeout(3000);

    console.log('\n' + '='.repeat(60));
    console.log('请在浏览器中执行以下操作:');
    console.log('  1. 点击任意策略名称进入编辑器');
    console.log('  2. 点击"运行回测"按钮');
    console.log('  3. 等待回测开始');
    console.log('='.repeat(60));
    console.log('\n按 Enter 键保存捕获结果并退出...');

    // 等待用户按 Enter
    await new Promise(resolve => {
      const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
      rl.question('', () => { rl.close(); resolve(); });
    });

    // 分析捕获结果
    const backtestReqs = captured.filter(c => {
      const p = c.url.replace('https://quant.10jqka.com.cn', '');
      return p.includes('backtest') || p.includes('run/');
    });

    console.log(`\n捕获 ${captured.length} 个 POST 请求`);
    console.log(`回测相关: ${backtestReqs.length} 个`);

    if (backtestReqs.length > 0) {
      console.log('\n★ 回测请求详情:');
      backtestReqs.forEach(r => {
        const p = r.url.replace('https://quant.10jqka.com.cn', '');
        console.log(`\n  URL: ${p}`);
        console.log(`  body: ${r.postData}`);
        if (r.responseJson) {
          console.log(`  errorcode: ${r.responseJson.errorcode}`);
          if (r.responseJson.result) console.log(`  result: ${JSON.stringify(r.responseJson.result).slice(0, 200)}`);
        }
      });
    }

    // 打印所有非常规请求
    const allInteresting = captured.filter(c => {
      const p = c.url.replace('https://quant.10jqka.com.cn', '');
      return !p.includes('message') && !p.includes('checknew') && !p.includes('getauth') && !p.includes('newhelp');
    });

    console.log(`\n所有有趣的请求 (${allInteresting.length} 个):`);
    allInteresting.forEach(r => {
      const p = r.url.replace('https://quant.10jqka.com.cn', '');
      console.log(`  ${p}: ${r.postData?.slice(0, 80) || ''}`);
    });

    // 保存
    const outputPath = path.join(OUTPUT_ROOT, 'intercept-capture.json');
    fs.writeFileSync(outputPath, JSON.stringify({ captured, backtestReqs, allInteresting, timestamp: Date.now() }, null, 2));
    console.log(`\n保存: ${outputPath}`);

    fs.writeFileSync(SESSION_FILE, JSON.stringify({ cookies: await context.cookies(), timestamp: Date.now() }, null, 2));

    await browser.close();
    return backtestReqs;

  } catch (err) {
    console.error('错误:', err.message);
    try { fs.writeFileSync(SESSION_FILE, JSON.stringify({ cookies: await context.cookies(), timestamp: Date.now() }, null, 2)); } catch (e) {}
    await browser.close();
    throw err;
  }
}

interceptAndRun().then(reqs => {
  if (reqs?.length > 0) {
    console.log(`\n✓ 捕获到 ${reqs.length} 个回测请求`);
  } else {
    console.log('\n⚠ 未捕获到回测请求');
  }
}).catch(err => {
  console.error('✗ 失败:', err.message);
  process.exit(1);
});
