#!/usr/bin/env node
/**
 * 捕获 algorithms/add 的真实 POST 参数
 * 在浏览器里点击"新建策略"按钮
 */
import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import '../load-env.js';
import { SESSION_FILE, OUTPUT_ROOT } from '../paths.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function captureAddApi() {
  const session = JSON.parse(fs.readFileSync(SESSION_FILE, 'utf8'));
  const browser = await chromium.launch({ headless: false, slowMo: 300 });
  const context = await browser.newContext({
    viewport: { width: 1400, height: 900 },
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36'
  });
  await context.addCookies(session.cookies || []);
  const page = await context.newPage();

  const addCalls = [];
  page.on('request', req => {
    if (req.url().includes('algorithms/add') && req.method() === 'POST') {
      console.log('\n★ ADD request!');
      console.log('  URL:', req.url());
      console.log('  Body:', req.postData());
      addCalls.push({ url: req.url(), postData: req.postData(), headers: req.headers() });
    }
  });
  page.on('response', async resp => {
    if (resp.url().includes('algorithms/add')) {
      const t = await resp.text().catch(() => '');
      console.log('  Response:', t.slice(0, 200));
      const entry = addCalls.find(c => c.url === resp.url() && !c.response);
      if (entry) entry.response = t.slice(0, 500);
    }
  });

  await page.goto('https://quant.10jqka.com.cn/view/study-index.html', { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(3000);

  console.log('页面已加载，点击新建策略...');

  // 点击新建策略
  const clicked = await page.evaluate(() => {
    const btns = Array.from(document.querySelectorAll('button, span, a, [class*="btn"]'));
    for (const btn of btns) {
      const t = btn.textContent.trim();
      if (t === '+新建策略' || t === '新建策略' || t.includes('新建策略')) {
        btn.click();
        return t;
      }
    }
    return null;
  });
  console.log('点击:', clicked);
  await page.waitForTimeout(3000);

  // 截图看弹窗
  await page.screenshot({ path: path.join(OUTPUT_ROOT, 'add-dialog.png') });

  // 分析弹窗
  const dialogInfo = await page.evaluate(() => {
    const inputs = Array.from(document.querySelectorAll('input')).map(i => ({
      type: i.type, placeholder: i.placeholder, name: i.name, value: i.value
    }));
    const btns = Array.from(document.querySelectorAll('button')).map(b => b.textContent.trim()).filter(t => t);
    const modals = Array.from(document.querySelectorAll('[class*="modal"], [class*="dialog"], [class*="popup"]'))
      .map(m => ({ class: m.className.slice(0, 60), visible: m.offsetWidth > 0 }));
    return { inputs, btns: btns.slice(0, 15), modals };
  });
  console.log('弹窗信息:', JSON.stringify(dialogInfo, null, 2));

  // 弹窗只有 radio 选择类型 + 确认按钮，直接点确认
  console.log('点击确认按钮...');
  const confirmClicked = await page.evaluate(() => {
    // 找 popbox-btn-ok 或 确定 按钮
    const okBtn = document.querySelector('.popbox-btn-ok, .plugin-dialog-btn');
    if (okBtn) { okBtn.click(); return okBtn.textContent.trim(); }
    const btns = Array.from(document.querySelectorAll('button'));
    for (const btn of btns) {
      const t = btn.textContent.trim();
      if (t === '确定' || t === '确认' || t === '创建' || t === 'OK') {
        btn.click(); return t;
      }
    }
    return null;
  });
  console.log('确认按钮:', confirmClicked);
  await page.waitForTimeout(8000);

  await page.screenshot({ path: path.join(OUTPUT_ROOT, 'add-after-confirm.png') });

  console.log(`\n捕获到 ${addCalls.length} 个 add 请求`);
  addCalls.forEach(c => {
    console.log('\nURL:', c.url);
    console.log('Body:', c.postData);
    console.log('Response:', c.response?.slice(0, 200));
  });

  const outputPath = path.join(OUTPUT_ROOT, 'add-api-capture.json');
  fs.writeFileSync(outputPath, JSON.stringify(addCalls, null, 2));
  console.log('\n保存:', outputPath);

  await page.waitForTimeout(5000);
  await browser.close();
  return addCalls;
}

captureAddApi().then(calls => {
  if (calls.length > 0) console.log('\n✓ 成功捕获 add 参数');
  else console.log('\n⚠ 未捕获到 add 请求');
}).catch(err => {
  console.error('✗ 失败:', err.message);
  process.exit(1);
});
