#!/usr/bin/env node
/**
 * 分析 SPA JS 源码，找到回测运行的真实 API 调用
 */

import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import '../load-env.js';
import { SESSION_FILE, OUTPUT_ROOT } from '../paths.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function analyzeSpaJs() {
  console.log('='.repeat(60));
  console.log('分析 SPA JS 源码');
  console.log('='.repeat(60));

  const session = JSON.parse(fs.readFileSync(SESSION_FILE, 'utf8'));
  const cookies = session.cookies || [];

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1400, height: 900 },
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36'
  });
  await context.addCookies(cookies);
  const page = await context.newPage();

  // 收集所有 JS 文件 URL
  const jsFiles = [];
  page.on('response', async resp => {
    const url = resp.url();
    if (url.includes('.js') && !url.includes('google') && !url.includes('analytics') && !url.includes('cbasspider')) {
      jsFiles.push(url);
    }
  });

  try {
    await page.goto('https://quant.10jqka.com.cn/view/study-index.html', {
      waitUntil: 'networkidle', timeout: 30000
    });
    await page.waitForTimeout(3000);

    console.log(`\n加载了 ${jsFiles.length} 个 JS 文件`);

    // 找主要的 app JS 文件（通常最大）
    const appJsFiles = jsFiles.filter(url =>
      url.includes('study-index') || url.includes('app.') || url.includes('chunk') || url.includes('vendor')
    );
    console.log('主要 JS 文件:', appJsFiles.slice(0, 5).map(u => u.split('/').pop()).join(', '));

    // 在页面上下文中搜索 backtest 相关的 API 调用
    console.log('\n在页面 JS 中搜索 backtest API...');

    const apiPatterns = await page.evaluate(async () => {
      // 获取所有已加载的 script 内容
      const scripts = Array.from(document.querySelectorAll('script[src]')).map(s => s.src);

      const results = {
        scripts: scripts.slice(0, 10),
        globalFunctions: [],
        vueComponents: [],
        ajaxCalls: []
      };

      // 搜索全局函数
      for (const key of Object.keys(window)) {
        if (typeof window[key] === 'function') {
          const str = window[key].toString();
          if (str.includes('backtest') || str.includes('run') || str.includes('algo')) {
            results.globalFunctions.push({ name: key, preview: str.slice(0, 100) });
          }
        }
      }

      // 搜索 Vue 实例
      const vueApp = document.querySelector('#app');
      if (vueApp && vueApp.__vue__) {
        const vm = vueApp.__vue__;
        const methods = Object.keys(vm.$options?.methods || {});
        results.vueComponents.push({
          type: 'root',
          methods: methods.filter(m => m.toLowerCase().includes('backtest') || m.toLowerCase().includes('run') || m.toLowerCase().includes('algo'))
        });
      }

      // 搜索所有 Vue 组件
      const allVueEls = document.querySelectorAll('[data-v-]');
      const vueInstances = new Set();
      allVueEls.forEach(el => {
        let vm = el.__vue__;
        while (vm) {
          if (!vueInstances.has(vm)) {
            vueInstances.add(vm);
            const methods = Object.keys(vm.$options?.methods || {});
            const backtestMethods = methods.filter(m =>
              m.toLowerCase().includes('backtest') || m.toLowerCase().includes('run') || m.toLowerCase().includes('algo')
            );
            if (backtestMethods.length > 0) {
              results.vueComponents.push({
                component: vm.$options?.name || 'unknown',
                methods: backtestMethods
              });
            }
          }
          vm = vm.$parent;
        }
      });

      return results;
    });

    console.log('全局函数:', apiPatterns.globalFunctions.map(f => f.name).join(', '));
    console.log('Vue 组件方法:', apiPatterns.vueComponents.map(c => `${c.component || c.type}: [${c.methods.join(', ')}]`).join('\n  '));

    // 直接获取 JS 文件内容并搜索
    console.log('\n下载并搜索 JS 文件...');

    const jsContent = {};
    for (const jsUrl of appJsFiles.slice(0, 3)) {
      try {
        const resp = await fetch(jsUrl);
        const text = await resp.text();
        jsContent[jsUrl.split('/').pop()] = text.length;

        // 搜索 backtest 相关代码
        const backtestMatches = [];
        const regex = /['"](\/platform\/backtest\/[^'"]+)['"]/g;
        let match;
        while ((match = regex.exec(text)) !== null) {
          backtestMatches.push(match[1]);
        }

        const runMatches = [];
        const runRegex = /['"](\/platform\/[^'"]*run[^'"]*)['"]/g;
        while ((match = runRegex.exec(text)) !== null) {
          runMatches.push(match[1]);
        }

        if (backtestMatches.length > 0 || runMatches.length > 0) {
          console.log(`\n${jsUrl.split('/').pop()} (${text.length} chars):`);
          console.log('  backtest URLs:', [...new Set(backtestMatches)].join(', '));
          console.log('  run URLs:', [...new Set(runMatches)].join(', '));
        }
      } catch (e) {
        console.log(`  获取失败: ${jsUrl.split('/').pop()}`);
      }
    }

    // 在页面上下文中搜索 JS 文件
    const jsSearchResult = await page.evaluate(async (jsUrls) => {
      const results = {};
      for (const url of jsUrls.slice(0, 5)) {
        try {
          const r = await fetch(url);
          const text = await r.text();

          // 搜索 backtest 相关 URL
          const backtestUrls = [];
          const regex1 = /['"]([^'"]*backtest[^'"]*)['"]/g;
          let m;
          while ((m = regex1.exec(text)) !== null) {
            if (m[1].startsWith('/platform/')) backtestUrls.push(m[1]);
          }

          // 搜索 run 相关 URL
          const runUrls = [];
          const regex2 = /['"]([^'"]*\/run[^'"]*)['"]/g;
          while ((m = regex2.exec(text)) !== null) {
            if (m[1].startsWith('/platform/')) runUrls.push(m[1]);
          }

          // 搜索 algo 相关 URL
          const algoUrls = [];
          const regex3 = /['"]([^'"]*\/algo[^'"]*)['"]/g;
          while ((m = regex3.exec(text)) !== null) {
            if (m[1].startsWith('/platform/')) algoUrls.push(m[1]);
          }

          const name = url.split('/').pop();
          results[name] = {
            size: text.length,
            backtestUrls: [...new Set(backtestUrls)],
            runUrls: [...new Set(runUrls)],
            algoUrls: [...new Set(algoUrls)]
          };
        } catch (e) {
          results[url.split('/').pop()] = { error: e.message };
        }
      }
      return results;
    }, appJsFiles);

    console.log('\nJS 文件分析结果:');
    for (const [name, info] of Object.entries(jsSearchResult)) {
      if (info.error) continue;
      if (info.backtestUrls.length > 0 || info.runUrls.length > 0 || info.algoUrls.length > 0) {
        console.log(`\n${name} (${info.size} chars):`);
        if (info.backtestUrls.length > 0) console.log('  backtest:', info.backtestUrls.join(', '));
        if (info.runUrls.length > 0) console.log('  run:', info.runUrls.join(', '));
        if (info.algoUrls.length > 0) console.log('  algo:', info.algoUrls.slice(0, 5).join(', '));
      }
    }

    // 保存
    const outputPath = path.join(OUTPUT_ROOT, 'spa-js-analysis.json');
    fs.writeFileSync(outputPath, JSON.stringify({ jsFiles, appJsFiles, apiPatterns, jsSearchResult, timestamp: Date.now() }, null, 2));
    console.log(`\n保存: ${outputPath}`);

    await browser.close();
    return jsSearchResult;

  } catch (err) {
    console.error('错误:', err.message);
    await browser.close();
    throw err;
  }
}

analyzeSpaJs().catch(err => {
  console.error('✗ 失败:', err.message);
  process.exit(1);
});
