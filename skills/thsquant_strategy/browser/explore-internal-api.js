#!/usr/bin/env node
/**
 * THSQuant 平台内部API探索工具
 * 通过注入JavaScript探索平台内部结构和API
 */

import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import '../load-env.js';
import { SESSION_FILE, OUTPUT_ROOT } from '../paths.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function exploreInternalAPIs() {
  console.log('\n' + '='.repeat(70));
  console.log('THSQuant 平台内部API探索');
  console.log('='.repeat(70));

  // 加载session
  let cookies = [];
  if (fs.existsSync(SESSION_FILE)) {
    const session = JSON.parse(fs.readFileSync(SESSION_FILE, 'utf8'));
    cookies = session.cookies || [];
  }

  console.log('\n启动浏览器...');
  const browser = await chromium.launch({
    headless: false,
    args: ['--disable-blink-features=AutomationControlled']
  });

  const context = await browser.newContext({
    viewport: { width: 1400, height: 900 },
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
  });

  if (cookies.length > 0) await context.addCookies(cookies);
  const page = await context.newPage();

  try {
    console.log('\n打开 THSQuant 平台...');
    await page.goto('https://quant.10jqka.com.cn/view/study-index.html', {
      waitUntil: 'networkidle'
    });
    await page.waitForTimeout(5000);

    // 1. 探索全局对象
    console.log('\n' + '='.repeat(70));
    console.log('1. 探索全局window对象');
    console.log('='.repeat(70));

    const globalObjects = await page.evaluate(() => {
      const results = {};

      // 检查关键全局对象
      const keys = Object.keys(window).filter(k =>
        k.includes('api') || k.includes('API') ||
        k.includes('quant') || k.includes('Quant') ||
        k.includes('strategy') || k.includes('backtest') ||
        k.includes('mindgo') || k.includes('Mindgo') ||
        k.includes('http') || k.includes('request')
      );
      results.specialKeys = keys;

      // 检查常见框架
      results.hasVue = !!(window.Vue || window.__VUE__);
      results.hasReact = !!(window.React || window.__REACT_DEVTOOLS_GLOBAL_HOOK__);
      results.hasAxios = !!window.axios;
      results.hasJQuery = !!window.jQuery;
      results.hasFetch = !!window.fetch;

      // 检查mindgo相关
      results.mindgoKeys = Object.keys(window).filter(k =>
        k.toLowerCase().includes('mind') || k.toLowerCase().includes('ths')
      );

      return results;
    });

    console.log('特殊全局变量:', globalObjects.specialKeys);
    console.log('Vue:', globalObjects.hasVue);
    console.log('React:', globalObjects.hasReact);
    console.log('Axios:', globalObjects.hasAxios);
    console.log('jQuery:', globalObjects.hasJQuery);
    console.log('Mindgo相关:', globalObjects.mindgoKeys);

    // 2. 探索LocalStorage和SessionStorage
    console.log('\n' + '='.repeat(70));
    console.log('2. 探索LocalStorage');
    console.log('='.repeat(70));

    const storage = await page.evaluate(() => {
      const ls = {};
      for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i);
        try {
          ls[key] = localStorage.getItem(key);
        } catch (e) {
          ls[key] = '[无法读取]';
        }
      }

      const ss = {};
      for (let i = 0; i < sessionStorage.length; i++) {
        const key = sessionStorage.key(i);
        try {
          ss[key] = sessionStorage.getItem(key);
        } catch (e) {
          ss[key] = '[无法读取]';
        }
      }

      return { localStorage: ls, sessionStorage: ss };
    });

    console.log('LocalStorage keys:', Object.keys(storage.localStorage));
    Object.entries(storage.localStorage).forEach(([k, v]) => {
      console.log(`  ${k}: ${String(v).substring(0, 60)}`);
    });

    // 3. 探索网络请求方法
    console.log('\n' + '='.repeat(70));
    console.log('3. 探索网络请求方法');
    console.log('='.repeat(70));

    const networkInfo = await page.evaluate(() => {
      const info = {};

      // 检查fetch
      if (window.fetch) {
        info.fetchExists = true;
        // 尝试获取fetch的源码来分析
        info.fetchStr = window.fetch.toString().substring(0, 200);
      }

      // 检查XMLHttpRequest
      if (window.XMLHttpRequest) {
        info.xhrExists = true;
      }

      // 检查是否有自定义请求库
      const requestLibs = Object.keys(window).filter(k =>
        k.toLowerCase().includes('request') ||
        k.toLowerCase().includes('http') ||
        k.toLowerCase().includes('ajax')
      );
      info.requestLibs = requestLibs;

      // 检查axios实例
      if (window.axios) {
        info.axiosDefaults = window.axios.defaults;
        info.axiosInterceptors = !!window.axios.interceptors;
      }

      return info;
    });

    console.log('Fetch存在:', networkInfo.fetchExists);
    console.log('XHR存在:', networkInfo.xhrExists);
    console.log('请求库:', networkInfo.requestLibs);
    if (networkInfo.axiosDefaults) {
      console.log('Axios baseURL:', networkInfo.axiosDefaults.baseURL);
    }

    // 4. 尝试触发策略列表API
    console.log('\n' + '='.repeat(70));
    console.log('4. 尝试调用平台API');
    console.log('='.repeat(70));

    // 导航到策略页面
    await page.goto('https://quant.10jqka.com.cn/view/study-index.html#/strategy/list', {
      waitUntil: 'networkidle'
    });
    await page.waitForTimeout(3000);

    // 尝试通过JS调用API
    const apiTestResult = await page.evaluate(async () => {
      const results = {};

      // 尝试调用getauthdata
      try {
        const resp = await fetch('/platform/user/getauthdata', {
          method: 'POST',
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
          body: 'isajax=1'
        });
        const text = await resp.text();
        results.getauthdata = text.substring(0, 200);
      } catch (e) {
        results.getauthdata = 'Error: ' + e.message;
      }

      // 尝试策略列表API
      const strategyEndpoints = [
        '/platform/strategy/list',
        '/platform/strategy/mylist',
        '/platform/backtest/list',
        '/api/strategy/list',
        '/api/strategy/my',
        '/platform/research/strategylist'
      ];

      for (const endpoint of strategyEndpoints) {
        try {
          const resp = await fetch(endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: 'isajax=1'
          });
          const text = await resp.text();
          results[endpoint] = {
            status: resp.status,
            response: text.substring(0, 200)
          };
        } catch (e) {
          results[endpoint] = 'Error: ' + e.message;
        }
      }

      return results;
    });

    console.log('\nAPI测试结果:');
    Object.entries(apiTestResult).forEach(([key, value]) => {
      if (typeof value === 'string') {
        console.log(`  ${key}: ${value.substring(0, 100)}`);
      } else {
        console.log(`  ${key}: status=${value.status}, ${value.response.substring(0, 80)}`);
      }
    });

    // 5. 查找Vue/React应用实例
    console.log('\n' + '='.repeat(70));
    console.log('5. 查找前端应用实例');
    console.log('='.repeat(70));

    const appInstance = await page.evaluate(() => {
      const info = {};

      // 查找Vue实例
      const vueElements = document.querySelectorAll('[data-v-]');
      info.vueComponents = vueElements.length;

      // 尝试找到Vue应用
      const app = document.querySelector('#app');
      if (app && app.__vue__) {
        info.hasVueInstance = true;
        info.vueData = Object.keys(app.__vue__.$data || {});
        info.vueMethods = Object.keys(app.__vue__.$options.methods || {});
      }

      // 查找React fiber
      const root = document.getElementById('root');
      if (root) {
        const fiberKey = Object.keys(root).find(k => k.startsWith('__reactFiber'));
        info.hasReactFiber = !!fiberKey;
      }

      // 查找所有有特殊属性的元素
      const specialElements = document.querySelectorAll('[class*="strategy"], [class*="backtest"], [id*="editor"]');
      info.specialElements = Array.from(specialElements).slice(0, 5).map(el => ({
        tag: el.tagName,
        class: el.className,
        id: el.id
      }));

      return info;
    });

    console.log('Vue组件数:', appInstance.vueComponents);
    console.log('Vue实例:', appInstance.hasVueInstance);
    if (appInstance.vueData) {
      console.log('Vue data:', appInstance.vueData);
    }
    if (appInstance.vueMethods) {
      console.log('Vue methods:', appInstance.vueMethods);
    }
    console.log('React Fiber:', appInstance.hasReactFiber);
    if (appInstance.specialElements) {
      console.log('特殊元素:', appInstance.specialElements);
    }

    // 6. 探索iframe内容
    console.log('\n' + '='.repeat(70));
    console.log('6. 探索iframe');
    console.log('='.repeat(70));

    const frames = page.frames();
    console.log(`发现 ${frames.length} 个frame`);

    for (let i = 0; i < frames.length; i++) {
      const frame = frames[i];
      try {
        const frameUrl = frame.url();
        console.log(`\nFrame ${i}: ${frameUrl}`);

        if (frameUrl !== 'about:blank') {
          // 探索iframe内部
          const frameInfo = await frame.evaluate(() => {
            return {
              title: document.title,
              hasEditor: !!document.querySelector('textarea, .editor, [class*="CodeMirror"]'),
              scripts: Array.from(document.querySelectorAll('script')).map(s => s.src).filter(s => s).slice(0, 3)
            };
          });
          console.log('  Title:', frameInfo.title);
          console.log('  编辑器:', frameInfo.hasEditor);
          console.log('  Scripts:', frameInfo.scripts);
        }
      } catch (e) {
        console.log(`  Error: ${e.message}`);
      }
    }

    // 保存分析结果
    const analysisResult = {
      globalObjects,
      storage,
      networkInfo,
      apiTestResult,
      appInstance,
      timestamp: Date.now()
    };

    const resultPath = path.join(OUTPUT_ROOT, 'internal-api-analysis.json');
    fs.writeFileSync(resultPath, JSON.stringify(analysisResult, null, 2));
    console.log(`\n分析结果保存: ${resultPath}`);

    // 保存session
    fs.writeFileSync(SESSION_FILE, JSON.stringify({
      cookies: await context.cookies(),
      timestamp: Date.now()
    }, null, 2));

    console.log('\n浏览器保持打开30秒...');
    await page.waitForTimeout(30000);

    await browser.close();

    return analysisResult;

  } catch (error) {
    console.error('\n错误:', error.message);
    await browser.close();
    throw error;
  }
}

exploreInternalAPIs().then(result => {
  console.log('\n' + '='.repeat(70));
  console.log('✓ 探索完成');
  console.log('='.repeat(70));
}).catch(err => {
  console.error('\n✗ 失败:', err.message);
  process.exit(1);
});