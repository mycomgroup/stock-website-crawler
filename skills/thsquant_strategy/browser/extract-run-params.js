#!/usr/bin/env node
/**
 * 从 JS 源码中提取 backtest/run 的真实参数
 */

import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import '../load-env.js';
import { SESSION_FILE, OUTPUT_ROOT } from '../paths.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function extractRunParams() {
  console.log('='.repeat(60));
  console.log('从 JS 源码提取 backtest/run 参数');
  console.log('='.repeat(60));

  const session = JSON.parse(fs.readFileSync(SESSION_FILE, 'utf8'));
  const cookies = session.cookies || [];

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36'
  });
  await context.addCookies(cookies);
  const page = await context.newPage();

  const jsFiles = [];
  page.on('response', async resp => {
    const url = resp.url();
    if (url.includes('study-index.js') || url.includes('app.') && url.endsWith('.js')) {
      jsFiles.push(url);
    }
  });

  try {
    await page.goto('https://quant.10jqka.com.cn/view/study-index.html', {
      waitUntil: 'networkidle', timeout: 30000
    });

    console.log('JS 文件:', jsFiles);

    // 获取 study-index.js 内容并分析
    const analysis = await page.evaluate(async (jsUrls) => {
      const results = {};

      for (const url of jsUrls) {
        try {
          const r = await fetch(url);
          const text = await r.text();

          // 找到 backtest/run 附近的代码（前后 500 字符）
          const runIdx = text.indexOf('/platform/backtest/run/');
          if (runIdx === -1) continue;

          const contexts = [];
          let searchFrom = 0;
          while (true) {
            const idx = text.indexOf('/platform/backtest/run/', searchFrom);
            if (idx === -1) break;
            contexts.push(text.slice(Math.max(0, idx - 400), idx + 400));
            searchFrom = idx + 1;
          }

          // 找到 gettradedays 附近的代码（回测配置参数）
          const tradedaysIdx = text.indexOf('/platform/backtest/gettradedays/');
          const tradedaysContext = tradedaysIdx !== -1 ?
            text.slice(Math.max(0, tradedaysIdx - 300), tradedaysIdx + 300) : null;

          // 找到 queryinfo 附近的代码
          const queryinfoIdx = text.indexOf('/platform/backtest/queryinfo/');
          const queryinfoContext = queryinfoIdx !== -1 ?
            text.slice(Math.max(0, queryinfoIdx - 300), queryinfoIdx + 300) : null;

          results[url.split('/').pop()] = {
            runContexts: contexts,
            tradedaysContext,
            queryinfoContext
          };
        } catch (e) {
          results[url] = { error: e.message };
        }
      }
      return results;
    }, jsFiles);

    // 打印分析结果
    for (const [name, info] of Object.entries(analysis)) {
      if (info.error) continue;
      console.log(`\n=== ${name} ===`);

      if (info.runContexts) {
        console.log(`\n找到 ${info.runContexts.length} 处 backtest/run 调用:`);
        info.runContexts.forEach((ctx, i) => {
          console.log(`\n--- 调用 ${i + 1} ---`);
          console.log(ctx);
        });
      }

      if (info.tradedaysContext) {
        console.log('\n--- gettradedays 上下文 ---');
        console.log(info.tradedaysContext);
      }
    }

    // 保存
    const outputPath = path.join(OUTPUT_ROOT, 'run-params-analysis.json');
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

extractRunParams().catch(err => {
  console.error('✗ 失败:', err.message);
  process.exit(1);
});
