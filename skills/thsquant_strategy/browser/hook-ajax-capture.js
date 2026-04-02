#!/usr/bin/env node
/**
 * Hook jQuery.ajax 来捕获回测运行的真实参数
 * 在页面加载时注入 hook，然后自动触发回测
 */

import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import '../load-env.js';
import { SESSION_FILE, OUTPUT_ROOT } from '../paths.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const TARGET_ALGO_ID = '67c935e607887b957629ad72';

async function hookAjaxCapture() {
  console.log('='.repeat(60));
  console.log('Hook jQuery.ajax 捕获回测参数');
  console.log('='.repeat(60));

  const session = JSON.parse(fs.readFileSync(SESSION_FILE, 'utf8'));
  const cookies = session.cookies || [];

  const browser = await chromium.launch({
    headless: false,
    slowMo: 200,
    args: ['--disable-blink-features=AutomationControlled']
  });

  const context = await browser.newContext({
    viewport: { width: 1400, height: 900 },
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36'
  });

  await context.addCookies(cookies);

  // 在每个页面加载时注入 hook
  await context.addInitScript(() => {
    window.__capturedAjax = [];

    // Hook fetch
    const origFetch = window.fetch;
    window.fetch = function(...args) {
      const url = typeof args[0] === 'string' ? args[0] : args[0]?.url || '';
      const opts = args[1] || {};
      if (url.includes('/platform/') && opts.method === 'POST') {
        const entry = { url, body: opts.body, time: Date.now(), type: 'fetch' };
        window.__capturedAjax.push(entry);
        if (url.includes('backtest') || url.includes('run')) {
          console.log('[HOOK fetch]', url, opts.body);
        }
      }
      return origFetch.apply(this, args);
    };

    // Hook XMLHttpRequest
    const origOpen = XMLHttpRequest.prototype.open;
    const origSend = XMLHttpRequest.prototype.send;

    XMLHttpRequest.prototype.open = function(method, url, ...rest) {
      this._hookUrl = url;
      this._hookMethod = method;
      return origOpen.apply(this, [method, url, ...rest]);
    };

    XMLHttpRequest.prototype.send = function(body) {
      if (this._hookUrl && this._hookUrl.includes('/platform/') && this._hookMethod === 'POST') {
        const entry = { url: this._hookUrl, body, time: Date.now(), type: 'xhr' };
        window.__capturedAjax.push(entry);
        if (this._hookUrl.includes('backtest') || this._hookUrl.includes('run')) {
          console.log('[HOOK XHR]', this._hookUrl, body);
        }
      }
      return origSend.apply(this, [body]);
    };
  });

  const page = await context.newPage();

  // 也用 Playwright 拦截
  const captured = [];
  page.on('request', req => {
    const url = req.url();
    if (url.includes('quant.10jqka.com.cn/platform/') && req.method() === 'POST') {
      const entry = { url: url.split('?')[0], fullUrl: url, postData: req.postData(), time: Date.now() };
      captured.push(entry);
      const p = entry.url.replace('https://quant.10jqka.com.cn', '');
      if (!p.includes('message') && !p.includes('checknew') && !p.includes('getauth') && !p.includes('newhelp') && !p.includes('queryall2')) {
        console.log(`\n★ POST ${p}`);
        if (entry.postData) console.log(`  ${entry.postData}`);
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
          if (!p.includes('message') && !p.includes('checknew') && !p.includes('getauth') && !p.includes('newhelp') && !p.includes('queryall2')) {
            console.log(`  ← ${text.slice(0, 150)}`);
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

    // 2. 找到 PSY 策略并双击进入编辑器
    console.log('\n2. 双击 PSY 策略进入编辑器...');

    // 先截图看当前状态
    await page.screenshot({ path: path.join(OUTPUT_ROOT, 'hook-step1.png') });

    // 尝试双击策略名称
    const dblClicked = await page.evaluate((algoId) => {
      const psyEls = Array.from(document.querySelectorAll('*'))
        .filter(el => el.textContent.trim() === 'PSY交易策略' && el.children.length === 0);
      if (psyEls.length > 0) {
        // 双击
        psyEls[0].dispatchEvent(new MouseEvent('dblclick', { bubbles: true }));
        psyEls[0].dispatchEvent(new MouseEvent('click', { bubbles: true }));
        return { found: true, tag: psyEls[0].tagName, class: psyEls[0].className };
      }
      return { found: false };
    }, TARGET_ALGO_ID);

    console.log('双击结果:', dblClicked);
    await page.waitForTimeout(3000);
    await page.screenshot({ path: path.join(OUTPUT_ROOT, 'hook-step2.png') });

    // 3. 检查是否进入了编辑器
    const editorState = await page.evaluate(() => {
      return {
        url: location.href,
        hash: location.hash,
        hasMonaco: !!(window.monaco?.editor),
        buttons: Array.from(document.querySelectorAll('button'))
          .map(b => b.textContent.trim().slice(0, 30))
          .filter(t => t.length > 0)
          .slice(0, 20)
      };
    });

    console.log('当前状态:', editorState.hash, '| Monaco:', editorState.hasMonaco);
    console.log('按钮:', editorState.buttons.join(', '));

    // 4. 如果没进入编辑器，尝试通过 Vue 路由跳转
    if (!editorState.hasMonaco && !editorState.hash.includes('editor')) {
      console.log('\n3. 尝试通过 Vue 路由跳转到编辑器...');

      // 尝试通过 Vue router 跳转
      const routerResult = await page.evaluate((algoId) => {
        // 找 Vue router
        const app = document.querySelector('#app');
        if (app && app.__vue__) {
          const vm = app.__vue__;
          if (vm.$router) {
            vm.$router.push({ name: 'editor', params: { id: algoId } });
            return { method: 'vue-router', routes: vm.$router.options?.routes?.map(r => r.path) };
          }
        }

        // 尝试直接修改 hash
        location.hash = `#/strategy/editor/${algoId}`;
        return { method: 'hash-change' };
      }, TARGET_ALGO_ID);

      console.log('路由跳转:', routerResult);
      await page.waitForTimeout(3000);
      await page.screenshot({ path: path.join(OUTPUT_ROOT, 'hook-step3.png') });
    }

    // 5. 分析所有 frame
    const frames = page.frames();
    console.log(`\n4. 检查 ${frames.length} 个 frame...`);

    for (const frame of frames) {
      const fUrl = frame.url();
      if (!fUrl || fUrl === 'about:blank') continue;

      try {
        const fInfo = await frame.evaluate(() => {
          const buttons = Array.from(document.querySelectorAll('button'))
            .map(b => ({ text: b.textContent.trim().slice(0, 30), visible: b.offsetWidth > 0 }))
            .filter(b => b.text.length > 0 && b.visible);
          const hasMonaco = !!(window.monaco?.editor);
          const editorCount = window.monaco?.editor?.getEditors?.()?.length || 0;
          return { buttons, hasMonaco, editorCount, url: location.href };
        });

        if (fInfo.hasMonaco || fInfo.buttons.some(b => b.text.includes('回测') || b.text.includes('运行'))) {
          console.log(`\n  ★ Frame: ${fUrl.slice(0, 80)}`);
          console.log(`  Monaco: ${fInfo.hasMonaco} (${fInfo.editorCount})`);
          console.log(`  按钮: ${fInfo.buttons.map(b => `"${b.text}"`).join(', ')}`);

          // 找运行按钮并点击
          const runBtn = fInfo.buttons.find(b => b.text.includes('回测') || b.text.includes('运行'));
          if (runBtn) {
            console.log(`\n  点击: "${runBtn.text}"`);
            await frame.evaluate((text) => {
              const btns = Array.from(document.querySelectorAll('button'));
              for (const btn of btns) {
                if (btn.textContent.trim().includes(text) && btn.offsetWidth > 0) {
                  btn.click();
                  return true;
                }
              }
              return false;
            }, runBtn.text);
            await page.waitForTimeout(8000);
          }
        }
      } catch (e) {}
    }

    // 6. 读取 hook 捕获的数据
    await page.waitForTimeout(3000);
    const hookData = await page.evaluate(() => window.__capturedAjax || []);
    console.log(`\nHook 捕获: ${hookData.length} 个请求`);

    const backtestHook = hookData.filter(h => h.url.includes('backtest') || h.url.includes('run'));
    if (backtestHook.length > 0) {
      console.log('\n★ Hook 捕获的回测请求:');
      backtestHook.forEach(h => {
        console.log(`  ${h.url}`);
        console.log(`  body: ${h.body}`);
      });
    }

    // 7. 分析 Playwright 捕获的请求
    const backtestReqs = captured.filter(c => {
      const p = c.url.replace('https://quant.10jqka.com.cn', '');
      return p.includes('backtest') || p.includes('run/');
    });

    console.log(`\nPlaywright 捕获: ${captured.length} 个 POST`);
    console.log(`回测相关: ${backtestReqs.length} 个`);

    if (backtestReqs.length > 0) {
      console.log('\n★ 回测请求:');
      backtestReqs.forEach(r => {
        console.log(`  ${r.url.replace('https://quant.10jqka.com.cn', '')}`);
        console.log(`  body: ${r.postData}`);
        if (r.responseJson) console.log(`  errorcode: ${r.responseJson.errorcode}`);
      });
    }

    // 保存
    const outputPath = path.join(OUTPUT_ROOT, 'hook-capture.json');
    fs.writeFileSync(outputPath, JSON.stringify({ captured, hookData, backtestReqs, editorState, timestamp: Date.now() }, null, 2));
    console.log(`\n保存: ${outputPath}`);

    fs.writeFileSync(SESSION_FILE, JSON.stringify({ cookies: await context.cookies(), timestamp: Date.now() }, null, 2));

    await page.waitForTimeout(5000);
    await browser.close();
    return backtestReqs;

  } catch (err) {
    console.error('错误:', err.message);
    try { await page.screenshot({ path: path.join(OUTPUT_ROOT, 'hook-error.png') }); } catch (e) {}
    try { fs.writeFileSync(SESSION_FILE, JSON.stringify({ cookies: await context.cookies(), timestamp: Date.now() }, null, 2)); } catch (e) {}
    await browser.close();
    throw err;
  }
}

hookAjaxCapture().then(reqs => {
  if (reqs?.length > 0) {
    console.log(`\n✓ 捕获到 ${reqs.length} 个回测请求`);
  } else {
    console.log('\n⚠ 未捕获到回测请求');
  }
}).catch(err => {
  console.error('✗ 失败:', err.message);
  process.exit(1);
});
