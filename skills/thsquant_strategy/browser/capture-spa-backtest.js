#!/usr/bin/env node
/**
 * 在 SPA 编辑器里点击回测，拦截真实 POST 参数
 * 使用 study-index.html#/strategy/list 路由
 */

import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import '../load-env.js';
import { SESSION_FILE, OUTPUT_ROOT } from '../paths.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function captureSpaBakctest() {
  console.log('='.repeat(60));
  console.log('SPA 编辑器回测参数捕获');
  console.log('='.repeat(60));

  const session = JSON.parse(fs.readFileSync(SESSION_FILE, 'utf8'));
  const cookies = session.cookies || [];

  const browser = await chromium.launch({
    headless: false,
    slowMo: 100,
    args: ['--disable-blink-features=AutomationControlled']
  });

  const context = await browser.newContext({
    viewport: { width: 1400, height: 900 },
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36'
  });

  await context.addCookies(cookies);
  const page = await context.newPage();

  // 拦截所有 platform POST 请求
  const captured = [];
  page.on('request', req => {
    const url = req.url();
    if (url.includes('quant.10jqka.com.cn/platform/') && req.method() === 'POST') {
      const entry = { url: url.split('?')[0], fullUrl: url, postData: req.postData(), time: Date.now() };
      captured.push(entry);
      const path = entry.url.replace('https://quant.10jqka.com.cn', '');
      if (path.includes('backtest') || path.includes('run') || path.includes('algo')) {
        console.log(`★ POST ${path}`);
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
          if (p.includes('backtest') || p.includes('run')) {
            console.log(`  → ${text.slice(0, 150)}`);
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
    await page.waitForTimeout(4000);

    // 验证登录
    const loginOk = await page.evaluate(async () => {
      const r = await fetch('/platform/user/getauthdata', {
        method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: 'isajax=1'
      });
      const d = await r.json();
      return d.errorcode === 0 ? d.result.user_id : null;
    });
    if (!loginOk) { console.log('✗ Session 过期'); await browser.close(); return null; }
    console.log(`✓ 已登录 user_id=${loginOk}`);

    await page.screenshot({ path: path.join(OUTPUT_ROOT, 'spa-step1-home.png') });

    // 2. 找到策略列表中的第一个策略并点击进入编辑
    console.log('\n2. 查找策略列表...');

    // 等待策略列表加载
    await page.waitForTimeout(2000);

    // 分析页面
    const pageState = await page.evaluate(() => {
      const links = Array.from(document.querySelectorAll('a, [class*="strategy"], [class*="algo"]'))
        .map(el => ({ text: el.textContent.trim().slice(0, 40), href: el.href, class: el.className.slice(0, 60) }))
        .filter(l => l.text.length > 0)
        .slice(0, 20);
      const buttons = Array.from(document.querySelectorAll('button'))
        .map(el => ({ text: el.textContent.trim().slice(0, 40), class: el.className.slice(0, 60) }))
        .filter(b => b.text.length > 0);
      return { links, buttons, url: location.href, hash: location.hash };
    });

    console.log('当前 URL:', pageState.url);
    console.log('Hash:', pageState.hash);
    console.log('按钮:', pageState.buttons.map(b => `"${b.text}"`).join(', '));

    // 3. 点击第一个策略进入编辑器
    console.log('\n3. 点击策略进入编辑器...');

    // 尝试点击策略名称链接
    const strategyClicked = await page.evaluate(() => {
      // 查找策略列表中的策略名称
      const strategyLinks = document.querySelectorAll('[class*="algo-name"], [class*="strategy-name"], .name a, td a');
      if (strategyLinks.length > 0) {
        strategyLinks[0].click();
        return { clicked: true, text: strategyLinks[0].textContent.trim() };
      }

      // 查找表格行
      const rows = document.querySelectorAll('tr[class*="strategy"], tr[data-id], .strategy-item');
      if (rows.length > 0) {
        rows[0].click();
        return { clicked: true, type: 'row' };
      }

      return { clicked: false };
    });

    console.log('点击结果:', strategyClicked);
    await page.waitForTimeout(4000);
    await page.screenshot({ path: path.join(OUTPUT_ROOT, 'spa-step3-after-click.png') });

    // 4. 分析编辑器页面
    console.log('\n4. 分析编辑器页面...');
    const editorState = await page.evaluate(() => {
      const buttons = Array.from(document.querySelectorAll('button, [role="button"], [class*="btn"]'))
        .map(el => ({ text: el.textContent.trim().slice(0, 40), class: el.className.slice(0, 80), visible: el.offsetWidth > 0 }))
        .filter(b => b.text.length > 0 && b.visible);

      const hasMonaco = !!(window.monaco && window.monaco.editor);
      const hasCodeMirror = document.querySelectorAll('.CodeMirror').length > 0;
      const hasAce = !!window.ace;

      const iframes = Array.from(document.querySelectorAll('iframe')).map(f => ({ src: f.src, id: f.id }));

      return { buttons: buttons.slice(0, 25), hasMonaco, hasCodeMirror, hasAce, iframes, url: location.href, hash: location.hash };
    });

    console.log('URL:', editorState.url);
    console.log('Monaco:', editorState.hasMonaco, '| CodeMirror:', editorState.hasCodeMirror, '| Ace:', editorState.hasAce);
    console.log('Iframes:', editorState.iframes.map(f => f.src.slice(0, 60)).join('\n  '));
    console.log('按钮:', editorState.buttons.map(b => `"${b.text}"`).join(', '));

    // 5. 检查 iframe 内容
    const frames = page.frames();
    console.log(`\n5. 检查 ${frames.length} 个 frame...`);

    let backtestBtnFound = false;
    for (const frame of frames) {
      const fUrl = frame.url();
      if (!fUrl || fUrl === 'about:blank') continue;
      console.log(`\n  Frame: ${fUrl.slice(0, 80)}`);

      try {
        const frameState = await frame.evaluate(() => {
          const buttons = Array.from(document.querySelectorAll('button, [class*="run"], [class*="backtest"], [class*="btn"]'))
            .map(el => ({ text: el.textContent.trim().slice(0, 40), class: el.className.slice(0, 80), visible: el.offsetWidth > 0 }))
            .filter(b => b.text.length > 0 && b.visible);

          const hasMonaco = !!(window.monaco && window.monaco.editor);
          const editors = window.monaco?.editor?.getEditors?.() || [];

          return { buttons: buttons.slice(0, 20), hasMonaco, editorCount: editors.length, url: location.href };
        });

        console.log(`  Monaco: ${frameState.hasMonaco} (${frameState.editorCount} editors)`);
        console.log(`  按钮: ${frameState.buttons.map(b => `"${b.text}"`).join(', ')}`);

        // 找回测/运行按钮
        const runBtn = frameState.buttons.find(b =>
          b.text.includes('回测') || b.text.includes('运行') || b.text.includes('Run') || b.text.includes('Backtest')
        );

        if (runBtn) {
          console.log(`\n  ★ 找到按钮: "${runBtn.text}"`);
          backtestBtnFound = true;

          // 点击
          try {
            await frame.click(`button:has-text("${runBtn.text}")`);
            console.log('  已点击！等待请求...');
            await page.waitForTimeout(8000);
            await page.screenshot({ path: path.join(OUTPUT_ROOT, 'spa-after-run.png') });
          } catch (e) {
            console.log(`  点击失败: ${e.message}`);
            // 尝试 evaluate 点击
            await frame.evaluate((text) => {
              const btns = document.querySelectorAll('button, [class*="run"], [class*="backtest"]');
              for (const btn of btns) {
                if (btn.textContent.includes(text)) { btn.click(); return true; }
              }
              return false;
            }, runBtn.text);
            await page.waitForTimeout(8000);
          }
        }
      } catch (e) {
        console.log(`  Frame 错误: ${e.message}`);
      }
    }

    // 6. 如果没找到，尝试主页面按钮
    if (!backtestBtnFound) {
      console.log('\n6. 尝试主页面按钮...');
      const mainBtns = editorState.buttons.filter(b =>
        b.text.includes('回测') || b.text.includes('运行') || b.text.includes('Run')
      );
      console.log('主页面回测按钮:', mainBtns.map(b => `"${b.text}"`).join(', '));

      for (const btn of mainBtns) {
        try {
          await page.click(`button:has-text("${btn.text}")`);
          console.log(`点击: "${btn.text}"`);
          await page.waitForTimeout(8000);
          break;
        } catch (e) {}
      }
    }

    // 7. 等待并分析结果
    await page.waitForTimeout(5000);
    await page.screenshot({ path: path.join(OUTPUT_ROOT, 'spa-final.png') });

    const backtestReqs = captured.filter(c =>
      c.url.includes('backtest') || c.url.includes('run/')
    );

    console.log(`\n捕获 ${captured.length} 个 POST 请求`);
    console.log(`回测相关: ${backtestReqs.length} 个`);

    if (backtestReqs.length > 0) {
      console.log('\n★ 回测请求:');
      backtestReqs.forEach(r => {
        console.log(`\n  ${r.url}`);
        console.log(`  body: ${r.postData}`);
        if (r.responseJson) console.log(`  errorcode: ${r.responseJson.errorcode}, result: ${JSON.stringify(r.responseJson.result).slice(0, 100)}`);
      });
    }

    // 保存
    const outputPath = path.join(OUTPUT_ROOT, 'spa-capture-result.json');
    fs.writeFileSync(outputPath, JSON.stringify({ captured, backtestReqs, editorState, timestamp: Date.now() }, null, 2));
    console.log(`\n保存: ${outputPath}`);

    // 更新 session
    fs.writeFileSync(SESSION_FILE, JSON.stringify({ cookies: await context.cookies(), timestamp: Date.now() }, null, 2));

    await page.waitForTimeout(5000);
    await browser.close();
    return backtestReqs;

  } catch (err) {
    console.error('错误:', err.message);
    try { await page.screenshot({ path: path.join(OUTPUT_ROOT, 'spa-error.png') }); } catch (e) {}
    try { fs.writeFileSync(SESSION_FILE, JSON.stringify({ cookies: await context.cookies(), timestamp: Date.now() }, null, 2)); } catch (e) {}
    await browser.close();
    throw err;
  }
}

captureSpaBakctest().then(reqs => {
  if (reqs?.length > 0) {
    console.log(`\n✓ 捕获到 ${reqs.length} 个回测请求`);
  } else {
    console.log('\n⚠ 未捕获到回测请求，查看截图分析页面结构');
  }
}).catch(err => {
  console.error('✗ 失败:', err.message);
  process.exit(1);
});
