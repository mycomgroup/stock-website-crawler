#!/usr/bin/env node
/**
 * THSQuant 平台探索工具
 * 探索页面结构，找到策略编辑的正确路径
 */

import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import '../load-env.js';
import { SESSION_FILE, OUTPUT_ROOT } from '../paths.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function explorePlatform() {
  // 加载session
  let cookies = [];
  if (fs.existsSync(SESSION_FILE)) {
    const session = JSON.parse(fs.readFileSync(SESSION_FILE, 'utf8'));
    cookies = session.cookies || [];
  }

  console.log('启动浏览器探索THSQuant平台...');

  const browser = await chromium.launch({
    headless: false,
    args: ['--disable-blink-features=AutomationControlled']
  });

  const context = await browser.newContext({
    viewport: { width: 1400, height: 900 },
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
  });

  if (cookies.length > 0) {
    await context.addCookies(cookies);
  }

  const page = await context.newPage();

  // 监控所有请求
  const apiCalls = [];
  page.on('request', req => {
    const url = req.url();
    if (url.includes('quant.10jqka.com.cn') && !url.includes('.css') && !url.includes('.js')) {
      apiCalls.push({
        url: url.split('?')[0],
        method: req.method(),
        time: Date.now()
      });
    }
  });

  try {
    // 1. 首页
    console.log('\n1. 访问首页...');
    await page.goto('https://quant.10jqka.com.cn/view/study-index.html', {
      waitUntil: 'networkidle'
    });
    await page.waitForTimeout(3000);

    // 截图首页
    const homePath = path.join(OUTPUT_ROOT, 'explore-home.png');
    await page.screenshot({ path: homePath });
    console.log(`截图: ${homePath}`);

    // 检查页面元素
    console.log('\n页面主要元素:');
    const buttons = await page.$$('button');
    const links = await page.$$('a');
    console.log(`- Buttons: ${buttons.length}`);
    console.log(`- Links: ${links.length}`);

    // 打印主要导航
    const navTexts = await page.$$eval('nav a, .nav a, [class*="menu"] a', els =>
      els.map(e => e.textContent?.trim()).filter(t => t)
    );
    console.log('- 导航:', navTexts.slice(0, 10).join(', '));

    // 检查登录状态
    const isLogin = await page.$('.header-usr-logined, .user-info, [class*="logged"]');
    console.log(`- 登录状态: ${isLogin ? '已登录' : '未登录'}`);

    // 2. 策略列表页面
    console.log('\n2. 寻找策略管理页面...');
    await page.goto('https://quant.10jqka.com.cn/view/study-index.html#/strategy/list', {
      waitUntil: 'networkidle'
    });
    await page.waitForTimeout(3000);

    const listPath = path.join(OUTPUT_ROOT, 'explore-strategy-list.png');
    await page.screenshot({ path: listPath });
    console.log(`截图: ${listPath}`);

    // 3. 新建策略页面
    console.log('\n3. 尝试新建策略页面...');
    await page.goto('https://quant.10jqka.com.cn/view/study-index.html#/strategy/new', {
      waitUntil: 'networkidle'
    });
    await page.waitForTimeout(5000);

    const newPath = path.join(OUTPUT_ROOT, 'explore-strategy-new.png');
    await page.screenshot({ path: newPath });
    console.log(`截图: ${newPath}`);

    // 打印页面标题和URL
    console.log('\n当前页面:');
    console.log(`- URL: ${page.url()}`);
    const title = await page.title();
    console.log(`- Title: ${title}`);

    // 寻找输入区域
    console.log('\n寻找编辑器元素...');
    const textareaCount = await page.$$('textarea').then(els => els.length);
    const inputCount = await page.$$('input[type="text"], input:not([type])').then(els => els.length);
    const editorCount = await page.$$('[class*="editor"], [class*="code"]').then(els => els.length);

    console.log(`- textarea: ${textareaCount}`);
    console.log(`- input: ${inputCount}`);
    console.log(`- editor区域: ${editorCount}`);

    // 检查iframe
    const frames = page.frames();
    console.log(`- frames: ${frames.length}`);
    if (frames.length > 1) {
      for (let i = 0; i < frames.length; i++) {
        const frame = frames[i];
        try {
          const frameUrl = frame.url();
          console.log(`  Frame ${i}: ${frameUrl}`);
        } catch (e) {}
      }
    }

    // 4. 回测页面
    console.log('\n4. 尝试回测页面...');
    await page.goto('https://quant.10jqka.com.cn/view/study-index.html#/backtest', {
      waitUntil: 'networkidle'
    });
    await page.waitForTimeout(3000);

    const backtestPath = path.join(OUTPUT_ROOT, 'explore-backtest.png');
    await page.screenshot({ path: backtestPath });
    console.log(`截图: ${backtestPath}`);

    // 保存API调用记录
    const apiPath = path.join(OUTPUT_ROOT, 'explore-api-calls.json');
    fs.writeFileSync(apiPath, JSON.stringify(apiCalls, null, 2));
    console.log(`\nAPI调用记录: ${apiPath}`);
    console.log(`共 ${apiCalls.length} 个请求`);

    // 打印唯一API端点
    const uniqueApis = [...new Set(apiCalls.map(c => c.url))];
    console.log('\n发现的API端点:');
    uniqueApis.forEach(url => console.log(`  ${url}`));

    // 保存cookies
    const finalCookies = await context.cookies();
    fs.writeFileSync(SESSION_FILE, JSON.stringify({
      cookies: finalCookies,
      timestamp: Date.now(),
      url: page.url()
    }, null, 2));

    console.log('\n探索完成，浏览器保持打开60秒供手动检查...');
    await page.waitForTimeout(60000);

    await browser.close();

  } catch (error) {
    console.error('错误:', error.message);
    await browser.close();
    throw error;
  }
}

explorePlatform().catch(e => {
  console.error('失败:', e.message);
  process.exit(1);
});