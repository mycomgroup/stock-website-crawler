#!/usr/bin/env node
/**
 * 从 JS 源码提取 backtest/run 的完整参数格式
 */

import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import '../load-env.js';
import { SESSION_FILE, OUTPUT_ROOT } from '../paths.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function extractRunParamsV2() {
  const session = JSON.parse(fs.readFileSync(SESSION_FILE, 'utf8'));
  const cookies = session.cookies || [];

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36'
  });
  await context.addCookies(cookies);
  const page = await context.newPage();

  const jsUrl = 'https://s.thsi.cn/cd/b2blh-supermind-php/dd7751651857392805c255281e32db71315f5e36/js/study-index.js';

  try {
    await page.goto('https://quant.10jqka.com.cn/view/study-index.html', {
      waitUntil: 'domcontentloaded', timeout: 30000
    });

    const analysis = await page.evaluate(async (url) => {
      const r = await fetch(url);
      const text = await r.text();

      const results = {
        runContexts: [],
        backtestRunContexts: [],
        paramPatterns: [],
        sectionPattern: null,
        frequencyPattern: null
      };

      // 找所有包含 backtest/run 的上下文（更大范围）
      let searchFrom = 0;
      while (true) {
        const idx = text.indexOf('"/platform/backtest/run/"', searchFrom);
        if (idx === -1) break;
        results.runContexts.push(text.slice(Math.max(0, idx - 1000), idx + 1000));
        searchFrom = idx + 1;
      }

      // 搜索 run 函数调用模式
      // 找 .run( 或 run: function 附近的代码
      const runFnPatterns = [
        /run\s*:\s*function[^}]{0,500}/g,
        /\.run\s*\([^)]{0,300}\)/g,
        /runBacktest[^}]{0,500}/g,
        /startBacktest[^}]{0,500}/g,
        /doBacktest[^}]{0,500}/g,
      ];

      for (const pattern of runFnPatterns) {
        const matches = text.match(pattern) || [];
        if (matches.length > 0) {
          results.paramPatterns.push(...matches.slice(0, 3));
        }
      }

      // 搜索 section 参数（回测日期格式）
      const sectionMatches = text.match(/section[^,;]{0,100}/g) || [];
      results.sectionPattern = sectionMatches.slice(0, 5);

      // 搜索 frequency 参数
      const freqMatches = text.match(/frequency[^,;]{0,100}/g) || [];
      results.frequencyPattern = freqMatches.slice(0, 5);

      // 搜索 capital_base 参数
      const capitalMatches = text.match(/capital_base[^,;]{0,100}/g) || [];
      results.capitalPattern = capitalMatches.slice(0, 5);

      // 搜索 benchmark 参数
      const benchmarkMatches = text.match(/benchmark[^,;]{0,100}/g) || [];
      results.benchmarkPattern = benchmarkMatches.slice(0, 5);

      // 搜索 algo_id 参数
      const algoIdMatches = text.match(/algo_id[^,;]{0,100}/g) || [];
      results.algoIdPattern = algoIdMatches.slice(0, 5);

      // 搜索 isajax 参数附近的代码（找完整的 POST body 构建）
      const isajaxMatches = [];
      let isajaxFrom = 0;
      while (true) {
        const idx = text.indexOf('isajax', isajaxFrom);
        if (idx === -1) break;
        // 找到包含 backtest 的 isajax 上下文
        const ctx = text.slice(Math.max(0, idx - 200), idx + 200);
        if (ctx.includes('backtest') || ctx.includes('run') || ctx.includes('algo_id')) {
          isajaxMatches.push(ctx);
        }
        isajaxFrom = idx + 1;
        if (isajaxMatches.length >= 5) break;
      }
      results.isajaxContexts = isajaxMatches;

      // 搜索 data: { 模式（jQuery AJAX data 参数）
      const dataObjMatches = [];
      const dataRegex = /data\s*:\s*\{[^}]{0,500}\}/g;
      let dataMatch;
      while ((dataMatch = dataRegex.exec(text)) !== null) {
        const ctx = dataMatch[0];
        if (ctx.includes('algo_id') || ctx.includes('backtest') || ctx.includes('section')) {
          dataObjMatches.push(ctx);
        }
        if (dataObjMatches.length >= 10) break;
      }
      results.dataObjects = dataObjMatches;

      return results;
    }, jsUrl);

    console.log('\n=== run 上下文 ===');
    analysis.runContexts.forEach((ctx, i) => {
      console.log(`\n--- 上下文 ${i + 1} ---`);
      console.log(ctx);
    });

    console.log('\n=== section 参数模式 ===');
    analysis.sectionPattern?.forEach(p => console.log(' ', p));

    console.log('\n=== frequency 参数模式 ===');
    analysis.frequencyPattern?.forEach(p => console.log(' ', p));

    console.log('\n=== capital_base 参数模式 ===');
    analysis.capitalPattern?.forEach(p => console.log(' ', p));

    console.log('\n=== algo_id 参数模式 ===');
    analysis.algoIdPattern?.forEach(p => console.log(' ', p));

    console.log('\n=== isajax 上下文 ===');
    analysis.isajaxContexts?.forEach((ctx, i) => {
      console.log(`\n--- ${i + 1} ---`);
      console.log(ctx);
    });

    console.log('\n=== data 对象 ===');
    analysis.dataObjects?.forEach((d, i) => {
      console.log(`\n--- ${i + 1} ---`);
      console.log(d);
    });

    const outputPath = path.join(OUTPUT_ROOT, 'run-params-v2.json');
    fs.writeFileSync(outputPath, JSON.stringify(analysis, null, 2));
    console.log(`\n保存: ${outputPath}`);

    await browser.close();
    return analysis;

  } catch (err) {
    console.error('错误:', err.message);
    await browser.close();
    throw err;
  }
}

extractRunParamsV2().catch(err => {
  console.error('✗ 失败:', err.message);
  process.exit(1);
});
