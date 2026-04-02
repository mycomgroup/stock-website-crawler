#!/usr/bin/env node
/**
 * 在 SPA 编辑器里点击回测，拦截真实 POST 参数 v2
 * 先导航到策略列表，点击策略进入编辑器，再点击回测
 */

import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import '../load-env.js';
import { SESSION_FILE, OUTPUT_ROOT } from '../paths.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const TARGET_ALGO_ID = '67c935e607887b957629ad72'; // PSY交易策略

async function captureV2() {
  console.log('='.repeat(60));
  console.log('SPA 回测参数捕获 v2');
  console.log('='.repeat(60));

  const session = JSON.parse(fs.readFileSync(SESSION_FILE, 'utf8'));
  const cookies = session.cookies || [];

  const browser = await chromium.launch({
    headless: false,
    slowMo: 300,
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
      if (!p.includes('message') && !p.includes('checknew') && !p.includes('getauth') && !p.includes('newhelp')) {
        console.log(`→ POST ${p}`);
        if (entry.postData) console.log(`  ${entry.postData.slice(0, 150)}`);
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
          entry.responseRaw = text.slice(0, 600);
          const m = text.match(/\((.+)\)/s);
          try { entry.responseJson = JSON.parse(m ? m[1] : text); } catch (e) {}
          const p = entry.url.replace('https://quant.10jqka.com.cn', '');
          if (!p.includes('message') && !p.includes('checknew') && !p.includes('getauth') && !p.includes('newhelp')) {
            console.log(`  ← ${text.slice(0, 120)}`);
          }
        } catch (e) {}
      }
    }
  });

  try {
    // 1. 打开策略列表
    console.log('\n1. 打开策略列表...');
    await page.goto('https://quant.10jqka.com.cn/view/study-index.html', {
      waitUntil: 'networkidle', timeout: 30000
    });
    await page.waitForTimeout(3000);

    // 验证登录
    const userId = await page.evaluate(async () => {
      const r = await fetch('/platform/user/getauthdata', {
        method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: 'isajax=1'
      });
      const d = await r.json();
      return d.errorcode === 0 ? d.result.user_id : null;
    });
    if (!userId) { console.log('✗ Session 过期'); await browser.close(); return null; }
    console.log(`✓ 已登录 user_id=${userId}`);

    await page.screenshot({ path: path.join(OUTPUT_ROOT, 'v2-step1.png') });

    // 2. 找到策略列表中的 PSY 策略并点击
    console.log('\n2. 查找并点击 PSY 策略...');

    // 等待策略列表渲染
    await page.waitForTimeout(2000);

    // 截图看当前状态
    await page.screenshot({ path: path.join(OUTPUT_ROOT, 'v2-step2-before.png') });

    // 分析页面 DOM
    const domInfo = await page.evaluate(() => {
      // 查找所有包含策略名称的元素
      const allText = Array.from(document.querySelectorAll('*'))
        .filter(el => el.children.length === 0 && el.textContent.trim().length > 0 && el.textContent.trim().length < 50)
        .map(el => ({ text: el.textContent.trim(), tag: el.tagName, class: el.className.slice(0, 60) }))
        .filter(el => el.text.includes('PSY') || el.text.includes('策略') || el.text.includes('MACD') || el.text.includes('SAR'));

      return { strategyTexts: allText.slice(0, 20) };
    });

    console.log('策略相关文本:', domInfo.strategyTexts.map(t => `"${t.text}" [${t.tag}]`).join('\n  '));

    // 尝试点击 PSY 策略
    const clicked = await page.evaluate((algoId) => {
      // 方法1: 查找包含 PSY 的元素
      const psyEls = Array.from(document.querySelectorAll('*'))
        .filter(el => el.textContent.trim() === 'PSY交易策略' && el.children.length === 0);
      if (psyEls.length > 0) {
        psyEls[0].click();
        return { method: 'text-match', text: psyEls[0].textContent };
      }

      // 方法2: 查找 data-id 属性
      const dataEl = document.querySelector(`[data-id="${algoId}"], [data-algo-id="${algoId}"]`);
      if (dataEl) {
        dataEl.click();
        return { method: 'data-id' };
      }

      // 方法3: 查找 href 包含 algo_id 的链接
      const links = Array.from(document.querySelectorAll('a'))
        .filter(a => a.href.includes(algoId));
      if (links.length > 0) {
        links[0].click();
        return { method: 'href', href: links[0].href };
      }

      return { method: 'none' };
    }, TARGET_ALGO_ID);

    console.log('点击结果:', clicked);
    await page.waitForTimeout(4000);
    await page.screenshot({ path: path.join(OUTPUT_ROOT, 'v2-step2-after.png') });

    // 3. 分析当前页面（应该是编辑器了）
    console.log('\n3. 分析编辑器页面...');
    const editorInfo = await page.evaluate(() => {
      const buttons = Array.from(document.querySelectorAll('button, [class*="btn"], [role="button"]'))
        .map(el => ({ text: el.textContent.trim().slice(0, 40), class: el.className.slice(0, 80), visible: el.offsetWidth > 0 && el.offsetHeight > 0 }))
        .filter(b => b.text.length > 0 && b.visible);

      const iframes = Array.from(document.querySelectorAll('iframe')).map(f => ({ src: f.src, id: f.id }));
      const hasMonaco = !!(window.monaco?.editor);

      return { buttons: buttons.slice(0, 30), iframes, hasMonaco, url: location.href, hash: location.hash };
    });

    console.log('URL:', editorInfo.url);
    console.log('Hash:', editorInfo.hash);
    console.log('Monaco:', editorInfo.hasMonaco);
    console.log('Iframes:', editorInfo.iframes.map(f => f.src.slice(0, 80)).join('\n  '));
    console.log('按钮:', editorInfo.buttons.map(b => `"${b.text}"`).join(', '));

    // 4. 检查所有 frame
    const frames = page.frames();
    console.log(`\n4. 检查 ${frames.length} 个 frame...`);

    let runBtnClicked = false;
    for (const frame of frames) {
      const fUrl = frame.url();
      if (!fUrl || fUrl === 'about:blank') continue;
      console.log(`\n  Frame: ${fUrl.slice(0, 100)}`);

      try {
        const fInfo = await frame.evaluate(() => {
          const buttons = Array.from(document.querySelectorAll('button, [class*="run"], [class*="backtest"], [class*="btn"]'))
            .map(el => ({ text: el.textContent.trim().slice(0, 40), class: el.className.slice(0, 80), visible: el.offsetWidth > 0 && el.offsetHeight > 0 }))
            .filter(b => b.text.length > 0 && b.visible);

          const hasMonaco = !!(window.monaco?.editor);
          const editorCount = window.monaco?.editor?.getEditors?.()?.length || 0;

          return { buttons: buttons.slice(0, 20), hasMonaco, editorCount, url: location.href };
        });

        console.log(`  Monaco: ${fInfo.hasMonaco} (${fInfo.editorCount} editors)`);
        console.log(`  按钮: ${fInfo.buttons.map(b => `"${b.text}"`).join(', ')}`);

        // 找运行/回测按钮
        const runBtn = fInfo.buttons.find(b =>
          b.text.includes('回测') || b.text.includes('运行') || b.text.includes('Run') || b.text.includes('Backtest') || b.text.includes('执行')
        );

        if (runBtn) {
          console.log(`\n  ★ 找到运行按钮: "${runBtn.text}"`);
          runBtnClicked = true;

          // 点击
          await frame.evaluate((text) => {
            const btns = Array.from(document.querySelectorAll('button, [class*="run"], [class*="backtest"]'));
            for (const btn of btns) {
              if (btn.textContent.trim().includes(text) && btn.offsetWidth > 0) {
                btn.click();
                return true;
              }
            }
            return false;
          }, runBtn.text);

          console.log('  已点击，等待请求...');
          await page.waitForTimeout(10000);
          await page.screenshot({ path: path.join(OUTPUT_ROOT, 'v2-after-run.png') });
          break;
        }
      } catch (e) {
        console.log(`  Frame 错误: ${e.message}`);
      }
    }

    // 5. 如果没找到，尝试主页面
    if (!runBtnClicked) {
      console.log('\n5. 尝试主页面运行按钮...');
      const runBtns = editorInfo.buttons.filter(b =>
        b.text.includes('回测') || b.text.includes('运行') || b.text.includes('Run')
      );
      console.log('候选按钮:', runBtns.map(b => `"${b.text}"`).join(', '));

      for (const btn of runBtns) {
        try {
          await page.click(`button:has-text("${btn.text}")`);
          console.log(`点击: "${btn.text}"`);
          await page.waitForTimeout(10000);
          runBtnClicked = true;
          break;
        } catch (e) {}
      }
    }

    // 6. 等待并分析
    await page.waitForTimeout(5000);
    await page.screenshot({ path: path.join(OUTPUT_ROOT, 'v2-final.png') });

    const backtestReqs = captured.filter(c => {
      const p = c.url.replace('https://quant.10jqka.com.cn', '');
      return p.includes('backtest') || p.includes('run/') || p.includes('algo');
    });

    console.log(`\n捕获 ${captured.length} 个 POST 请求`);
    console.log(`回测相关: ${backtestReqs.length} 个`);

    if (backtestReqs.length > 0) {
      console.log('\n★ 回测请求详情:');
      backtestReqs.forEach(r => {
        const p = r.url.replace('https://quant.10jqka.com.cn', '');
        console.log(`\n  ${p}`);
        console.log(`  body: ${r.postData}`);
        if (r.responseJson) {
          console.log(`  errorcode: ${r.responseJson.errorcode}`);
          if (r.responseJson.result) console.log(`  result: ${JSON.stringify(r.responseJson.result).slice(0, 150)}`);
        }
      });
    }

    // 保存
    const outputPath = path.join(OUTPUT_ROOT, 'spa-v2-capture.json');
    fs.writeFileSync(outputPath, JSON.stringify({ captured, backtestReqs, editorInfo, timestamp: Date.now() }, null, 2));
    console.log(`\n保存: ${outputPath}`);

    fs.writeFileSync(SESSION_FILE, JSON.stringify({ cookies: await context.cookies(), timestamp: Date.now() }, null, 2));

    await page.waitForTimeout(5000);
    await browser.close();
    return backtestReqs;

  } catch (err) {
    console.error('错误:', err.message);
    try { await page.screenshot({ path: path.join(OUTPUT_ROOT, 'v2-error.png') }); } catch (e) {}
    try { fs.writeFileSync(SESSION_FILE, JSON.stringify({ cookies: await context.cookies(), timestamp: Date.now() }, null, 2)); } catch (e) {}
    await browser.close();
    throw err;
  }
}

captureV2().then(reqs => {
  if (reqs?.length > 0) {
    console.log(`\n✓ 捕获到 ${reqs.length} 个回测请求`);
  } else {
    console.log('\n⚠ 未捕获到回测请求');
  }
}).catch(err => {
  console.error('✗ 失败:', err.message);
  process.exit(1);
});
