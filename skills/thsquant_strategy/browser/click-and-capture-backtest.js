#!/usr/bin/env node
/**
 * 在编辑器页面点击回测按钮，拦截真实的 POST 参数
 */

import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import '../load-env.js';
import { SESSION_FILE, OUTPUT_ROOT } from '../paths.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const TEST_ALGO_ID = '67c935e607887b957629ad72';

async function clickAndCapture() {
  console.log('='.repeat(60));
  console.log('点击回测按钮 + 拦截真实参数');
  console.log('='.repeat(60));

  const session = JSON.parse(fs.readFileSync(SESSION_FILE, 'utf8'));
  const cookies = session.cookies || [];

  const browser = await chromium.launch({
    headless: false, // 需要看到页面
    slowMo: 200,
    args: ['--disable-blink-features=AutomationControlled']
  });

  const context = await browser.newContext({
    viewport: { width: 1400, height: 900 },
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36'
  });

  await context.addCookies(cookies);
  const page = await context.newPage();

  // 拦截所有请求
  const captured = [];
  page.on('request', req => {
    const url = req.url();
    if (url.includes('quant.10jqka.com.cn/platform/') && req.method() === 'POST') {
      const entry = {
        url: url.split('?')[0],
        fullUrl: url,
        postData: req.postData(),
        time: Date.now()
      };
      captured.push(entry);
      // 重点关注 backtest 相关
      if (url.includes('backtest') || url.includes('run') || url.includes('algo')) {
        console.log(`\n★ POST ${url.replace('https://quant.10jqka.com.cn', '')}`);
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
          entry.responseRaw = text.slice(0, 500);
          const m = text.match(/\((.+)\)/s);
          try { entry.responseJson = JSON.parse(m ? m[1] : text); } catch (e) {}
          if (url.includes('backtest') || url.includes('run')) {
            console.log(`  → response: ${text.slice(0, 200)}`);
          }
        } catch (e) {}
      }
    }
  });

  try {
    // 1. 打开编辑器
    console.log('\n打开编辑器...');
    await page.goto(
      `https://quant.10jqka.com.cn/platform/study/html/editor.html?algo_id=${TEST_ALGO_ID}`,
      { waitUntil: 'networkidle', timeout: 30000 }
    );
    await page.waitForTimeout(5000);
    await page.screenshot({ path: path.join(OUTPUT_ROOT, 'click-editor-loaded.png') });

    // 2. 分析页面结构
    const pageAnalysis = await page.evaluate(() => {
      const allButtons = Array.from(document.querySelectorAll('button, a, [role="button"], [class*="btn"], [class*="run"], [class*="backtest"]'))
        .map(el => ({
          tag: el.tagName,
          text: el.textContent.trim().slice(0, 40),
          class: el.className.slice(0, 80),
          id: el.id,
          visible: el.offsetWidth > 0 && el.offsetHeight > 0
        }))
        .filter(b => b.text.length > 0 && b.visible);

      const iframes = Array.from(document.querySelectorAll('iframe')).map(f => ({
        src: f.src, id: f.id, name: f.name
      }));

      return { buttons: allButtons.slice(0, 30), iframes, title: document.title };
    });

    console.log('\n页面标题:', pageAnalysis.title);
    console.log('Iframes:', pageAnalysis.iframes.map(f => f.src.slice(0, 60)).join('\n  '));
    console.log('\n可见按钮:');
    pageAnalysis.buttons.forEach(b => console.log(`  [${b.tag}] "${b.text}" class="${b.class.slice(0, 50)}"`));

    // 3. 检查 iframe 内容
    const frames = page.frames();
    console.log(`\n共 ${frames.length} 个 frame`);

    for (const frame of frames) {
      const fUrl = frame.url();
      if (!fUrl || fUrl === 'about:blank') continue;
      console.log(`\nFrame: ${fUrl.slice(0, 80)}`);

      try {
        const frameAnalysis = await frame.evaluate(() => {
          const buttons = Array.from(document.querySelectorAll('button, [class*="run"], [class*="backtest"], [class*="btn"]'))
            .map(el => ({
              text: el.textContent.trim().slice(0, 40),
              class: el.className.slice(0, 80),
              visible: el.offsetWidth > 0 && el.offsetHeight > 0
            }))
            .filter(b => b.text.length > 0);
          return { buttons: buttons.slice(0, 20), title: document.title };
        });

        console.log('  Frame 按钮:', frameAnalysis.buttons.map(b => `"${b.text}"`).join(', '));

        // 找回测按钮
        const backtestBtn = frameAnalysis.buttons.find(b =>
          b.text.includes('回测') || b.text.includes('运行') || b.text.includes('Run') || b.text.includes('Backtest')
        );

        if (backtestBtn) {
          console.log(`\n  ★ 找到回测按钮: "${backtestBtn.text}"`);

          // 点击它
          await frame.click(`button:has-text("${backtestBtn.text}"), [class*="run"]:has-text("${backtestBtn.text}")`);
          console.log('  已点击，等待请求...');
          await page.waitForTimeout(5000);
          await page.screenshot({ path: path.join(OUTPUT_ROOT, 'click-after-backtest.png') });
        }
      } catch (e) {
        console.log(`  Frame 分析错误: ${e.message}`);
      }
    }

    // 4. 如果没找到 iframe 按钮，尝试主页面
    const backtestCaptured = captured.filter(c =>
      c.url.includes('backtest') || c.url.includes('run/')
    );

    if (backtestCaptured.length === 0) {
      console.log('\n尝试主页面点击...');

      // 尝试各种选择器
      const selectors = [
        'button:has-text("回测")',
        'button:has-text("运行")',
        '[class*="run-btn"]',
        '[class*="backtest-btn"]',
        '.run',
        '#run-btn',
        '[data-action="run"]',
        '[data-action="backtest"]'
      ];

      for (const sel of selectors) {
        try {
          const el = await page.$(sel);
          if (el && await el.isVisible()) {
            console.log(`点击: ${sel}`);
            await el.click();
            await page.waitForTimeout(5000);
            break;
          }
        } catch (e) {}
      }
    }

    // 5. 等待更多请求
    await page.waitForTimeout(8000);
    await page.screenshot({ path: path.join(OUTPUT_ROOT, 'click-final-state.png') });

    // 6. 分析捕获结果
    const backtestRequests = captured.filter(c =>
      c.url.includes('backtest') || c.url.includes('run/')
    );

    console.log(`\n捕获到 ${captured.length} 个 POST 请求`);
    console.log(`回测相关: ${backtestRequests.length} 个`);

    if (backtestRequests.length > 0) {
      console.log('\n★ 回测请求详情:');
      backtestRequests.forEach(r => {
        console.log(`\n  URL: ${r.url}`);
        console.log(`  Body: ${r.postData}`);
        if (r.responseJson) {
          console.log(`  Response: errorcode=${r.responseJson.errorcode}, result=${JSON.stringify(r.responseJson.result).slice(0, 100)}`);
        }
      });
    }

    // 保存
    const outputPath = path.join(OUTPUT_ROOT, 'click-capture-result.json');
    fs.writeFileSync(outputPath, JSON.stringify({
      allCaptured: captured,
      backtestRequests,
      pageAnalysis,
      timestamp: Date.now()
    }, null, 2));
    console.log(`\n保存: ${outputPath}`);

    // 保持打开 10 秒
    await page.waitForTimeout(10000);
    await browser.close();

    return backtestRequests;

  } catch (err) {
    console.error('错误:', err.message);
    try { await page.screenshot({ path: path.join(OUTPUT_ROOT, 'click-error.png') }); } catch (e) {}
    await browser.close();
    throw err;
  }
}

clickAndCapture().then(reqs => {
  if (reqs?.length > 0) {
    console.log(`\n✓ 成功捕获 ${reqs.length} 个回测请求`);
  } else {
    console.log('\n⚠ 未捕获到回测请求');
  }
}).catch(err => {
  console.error('✗ 失败:', err.message);
  process.exit(1);
});
