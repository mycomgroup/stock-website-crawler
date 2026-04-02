#!/usr/bin/env node
/**
 * THSQuant 回测 API 探测器
 * 使用浏览器自动化捕获真实的回测 API 参数
 */

import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import '../load-env.js';
import { SESSION_FILE, OUTPUT_ROOT } from '../paths.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function exploreBacktestAPI() {
  console.log('\n' + '='.repeat(70));
  console.log('THSQuant 回测 API 探测器');
  console.log('='.repeat(70));

  // 加载 session
  const session = JSON.parse(fs.readFileSync(SESSION_FILE, 'utf8'));
  const cookies = session.cookies || [];
  console.log(`\n加载 ${cookies.length} 个 cookies`);

  // API 收集器
  const apiCalls = [];

  console.log('\n启动浏览器...');
  const browser = await chromium.launch({
    headless: false,
    args: ['--disable-blink-features=AutomationControlled']
  });

  const context = await browser.newContext({ viewport: { width: 1400, height: 900 } });
  await context.addCookies(cookies);
  const page = await context.newPage();

  // 监听所有请求
  page.on('request', request => {
    const url = request.url();
    const method = request.method();
    const postData = request.postData() || '';

    if (method === 'POST' || (method === 'GET' && url.includes('platform'))) {
      const call = {
        id: apiCalls.length,
        url,
        method,
        postData,
        time: Date.now()
      };
      apiCalls.push(call);

      // 打印重要请求
      if (url.includes('/platform/')) {
        const endpoint = url.split('/platform/')[1]?.split('?')[0] || url;
        console.log(`\n[${apiCalls.length}] ${method} ${endpoint}`);

        if (postData && method === 'POST') {
          try {
            const params = new URLSearchParams(postData);
            const important = {};
            for (const [k, v] of params) {
              if (!['isajax', 'datatype', 'callback'].includes(k)) {
                important[k] = v.length > 100 ? v.slice(0, 100) + '...' : v;
              }
            }
            if (Object.keys(important).length > 0) {
              console.log('  参数:', JSON.stringify(important, null, 2));
            }
          } catch (e) {
            if (postData.length < 200) {
              console.log('  Body:', postData);
            }
          }
        }
      }
    }
  });

  // 监听响应
  page.on('response', async response => {
    const url = response.url();
    const req = response.request();
    const call = apiCalls.find(c => c.url === url && !c.response);

    if (call) {
      call.status = response.status();
      try {
        const text = await response.text();

        // 解析 JSONP
        const match = text.match(/\((.+)\)/s);
        if (match) {
          try {
            call.responseJson = JSON.parse(match[1]);
          } catch (e) {}
        }

        // 打印关键响应
        if (call.responseJson) {
          const json = call.responseJson;
          if (json.errorcode !== undefined) {
            console.log(`  响应: errorcode=${json.errorcode}`);
            if (json.errormsg) {
              console.log(`  消息: ${json.errormsg}`);
            }
            if (json.result && typeof json.result === 'object') {
              const keys = Object.keys(json.result).slice(0, 5);
              if (keys.length > 0) {
                console.log(`  result: ${keys.join(', ')}`);
              }
            }
          }
        }
      } catch (e) {}
    }
  });

  try {
    // 1. 打开策略研究主页
    console.log('\n步骤1: 打开策略研究主页...');
    await page.goto('https://quant.10jqka.com.cn/view/study-index.html', {
      waitUntil: 'domcontentloaded',
      timeout: 30000
    });
    await page.waitForTimeout(5000);

    // 截图
    await page.screenshot({ path: path.join(OUTPUT_ROOT, 'study-index.png') });

    // 2. 检查登录
    console.log('\n步骤2: 检查登录状态...');
    const loginStatus = await page.evaluate(async () => {
      try {
        const resp = await fetch('/platform/user/getauthdata', {
          method: 'POST',
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
          body: 'isajax=1'
        });
        return await resp.json();
      } catch (e) {
        return { errorcode: -1 };
      }
    });

    if (loginStatus.errorcode !== 0) {
      console.log('✗ 未登录');
      await browser.close();
      return { success: false, reason: 'not_logged_in' };
    }
    console.log(`✓ 已登录 (用户ID: ${loginStatus.result?.user_id})`);

    // 3. 获取策略列表
    console.log('\n步骤3: 获取策略列表...');
    const strategies = await page.evaluate(async () => {
      try {
        const resp = await fetch('/platform/algorithms/queryall2/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
          body: 'isajax=1&datatype=jsonp'
        });
        const text = await resp.text();
        const match = text.match(/\((.+)\)/s);
        if (match) {
          const json = JSON.parse(match[1]);
          return json.result?.strategys || [];
        }
        return [];
      } catch (e) {
        return [];
      }
    });

    console.log(`找到 ${strategies.length} 个策略`);
    if (strategies.length > 0) {
      console.log('第一个策略:');
      console.log(`  ID: ${strategies[0].algo_id}`);
      console.log(`  名称: ${strategies[0].algo_name}`);
    }

    // 4. 打开第一个策略的编辑页面
    const strategyId = strategies[0]?.algo_id || '67c935e607887b957629ad72';
    console.log(`\n步骤4: 打开策略编辑页面 (${strategyId})...`);

    const editorUrl = `https://quant.10jqka.com.cn/platform/study/html/editor.html?algo_id=${strategyId}`;
    await page.goto(editorUrl, { waitUntil: 'domcontentloaded', timeout: 30000 });
    await page.waitForTimeout(8000);

    // 截图编辑器页面
    await page.screenshot({ path: path.join(OUTPUT_ROOT, 'editor-page.png') });

    // 5. 分析页面内容
    console.log('\n步骤5: 分析页面内容...');
    const pageInfo = await page.evaluate(() => {
      // 查找所有按钮
      const buttons = Array.from(document.querySelectorAll('button, a, [role="button"], input[type="button"]'))
        .filter(el => el.textContent?.trim() || el.value || el.id || el.className)
        .slice(0, 30)
        .map(el => ({
          text: (el.textContent || el.value || '').trim().slice(0, 30),
          tag: el.tagName,
          id: el.id,
          className: el.className?.toString().slice(0, 50),
          type: el.type
        }));

      // 查找表单
      const forms = Array.from(document.querySelectorAll('form')).map(f => ({
        action: f.action,
        id: f.id,
        className: f.className
      }));

      // 查找输入框
      const inputs = Array.from(document.querySelectorAll('input, select')).map(i => ({
        name: i.name,
        id: i.id,
        type: i.type,
        placeholder: i.placeholder,
        value: i.value?.slice(0, 50)
      }));

      // 检查全局变量
      const globals = {
        hasMonaco: typeof window.monaco !== 'undefined',
        hasCodeMirror: typeof window.CodeMirror !== 'undefined',
        hasJQuery: typeof window.jQuery !== 'undefined',
      };

      return { buttons, forms, inputs, globals };
    });

    console.log('\n页面按钮:');
    pageInfo.buttons.forEach(b => {
      if (b.text) console.log(`  ${b.tag}: "${b.text}" class="${b.className?.slice(0, 30)}"`);
    });

    console.log('\n页面输入框:');
    pageInfo.inputs.forEach(i => {
      if (i.name || i.id) console.log(`  ${i.type}: name="${i.name}" id="${i.id}" value="${i.value}"`);
    });

    console.log('\n全局变量:', pageInfo.globals);

    // 6. 尝试找到回测相关的元素
    console.log('\n步骤6: 查找回测相关元素...');

    // 使用多种方式查找
    const backtestElements = await page.evaluate(() => {
      const results = [];

      // 按文本查找
      const textPatterns = ['回测', '运行', '测试', 'backtest', 'run'];
      textPatterns.forEach(pattern => {
        const elements = document.querySelectorAll(`button, a, [role="button"], span, div`);
        elements.forEach(el => {
          const text = el.textContent || '';
          if (text.toLowerCase().includes(pattern.toLowerCase()) && text.length < 20) {
            results.push({
              type: 'text',
              pattern,
              text: text.trim(),
              tag: el.tagName,
              id: el.id,
              className: el.className?.toString().slice(0, 50)
            });
          }
        });
      });

      // 按类名查找
      const classPatterns = ['backtest', 'run', 'test', 'btn'];
      classPatterns.forEach(pattern => {
        const elements = document.querySelectorAll(`[class*="${pattern}"]`);
        elements.forEach(el => {
          if (!results.find(r => r.element === el)) {
            results.push({
              type: 'class',
              pattern,
              tag: el.tagName,
              id: el.id,
              className: el.className?.toString().slice(0, 50)
            });
          }
        });
      });

      return results;
    });

    console.log('找到回测相关元素:');
    backtestElements.slice(0, 10).forEach((el, i) => {
      console.log(`  ${i + 1}. ${el.type}: "${el.text || el.className}"`);
    });

    // 7. 尝试点击回测按钮
    console.log('\n步骤7: 尝试触发回测...');

    for (const el of backtestElements.slice(0, 5)) {
      try {
        let locator;
        if (el.text) {
          locator = page.locator(`text="${el.text}"`).first();
        } else if (el.id) {
          locator = page.locator(`#${el.id}`);
        } else if (el.className) {
          locator = page.locator(`.${el.className.split(' ')[0]}`).first();
        }

        if (locator && await locator.isVisible()) {
          console.log(`点击: ${el.text || el.className}`);
          await locator.click();
          await page.waitForTimeout(5000);
          break;
        }
      } catch (e) {
        continue;
      }
    }

    // 截图最终状态
    await page.screenshot({ path: path.join(OUTPUT_ROOT, 'final-state.png') });

    // 8. 保存 session
    const newCookies = await context.cookies();
    fs.writeFileSync(SESSION_FILE, JSON.stringify({
      cookies: newCookies,
      timestamp: Date.now()
    }, null, 2));

    // 保持浏览器打开一段时间让用户查看
    console.log('\n浏览器将在 30 秒后关闭...');
    await page.waitForTimeout(30000);

    await browser.close();

    // 9. 分析并保存结果
    console.log('\n' + '='.repeat(70));
    console.log('分析结果');
    console.log('='.repeat(70));

    // 找出回测相关的 API
    const backtestApis = apiCalls.filter(c =>
      c.url.includes('backtest') ||
      c.url.includes('run') ||
      (c.postData && (c.postData.includes('backtest') || c.postData.includes('run')))
    );

    const algoApis = apiCalls.filter(c =>
      c.url.includes('algo') || c.url.includes('algorithm')
    );

    console.log(`\n总 POST 请求: ${apiCalls.length} 个`);
    console.log(`回测相关: ${backtestApis.length} 个`);
    console.log(`策略相关: ${algoApis.length} 个`);

    const result = {
      strategies: strategies.slice(0, 3),
      pageInfo,
      backtestElements,
      totalCalls: apiCalls.length,
      backtestApis,
      algoApis,
      allCalls: apiCalls,
      timestamp: Date.now()
    };

    const outputPath = path.join(OUTPUT_ROOT, 'backtest-api-exploration.json');
    fs.writeFileSync(outputPath, JSON.stringify(result, null, 2));
    console.log(`\n保存到: ${outputPath}`);

    return result;

  } catch (error) {
    console.error('\n错误:', error.message);
    await page.screenshot({ path: path.join(OUTPUT_ROOT, 'error.png') });

    const result = {
      totalCalls: apiCalls.length,
      allCalls: apiCalls,
      error: error.message,
      timestamp: Date.now()
    };
    fs.writeFileSync(path.join(OUTPUT_ROOT, 'exploration-error.json'), JSON.stringify(result, null, 2));

    await browser.close();
    throw error;
  }
}

exploreBacktestAPI()
  .then(result => {
    if (result.backtestApis?.length > 0) {
      console.log('\n✓ 成功捕获回测 API!');
    } else {
      console.log('\n⚠ 未捕获到回测 API');
    }
  })
  .catch(console.error);