#!/usr/bin/env node
/**
 * THSQuant 批量策略提交和执行工具
 * 自动为多个策略创建、提交代码并运行回测
 */

import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import '../load-env.js';
import { SESSION_FILE, OUTPUT_ROOT } from '../paths.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const STRATEGIES_DIR = path.resolve(__dirname, '../../../strategies/thsquant');

// 回测配置
const BACKTEST_CONFIG = {
  startDate: '2023-01-01',
  endDate: '2024-12-31',
  initialCapital: 100000,
  frequency: '1d',
  benchmark: '000300.SH'
};

async function batchRunStrategies(strategyFiles) {
  console.log('\n' + '='.repeat(70));
  console.log('THSQuant 批量策略运行工具');
  console.log('='.repeat(70));

  // 读取所有策略
  const strategies = strategyFiles.map(file => {
    const filePath = path.resolve(file);
    if (!fs.existsSync(filePath)) {
      console.log(`⚠ 文件不存在: ${file}`);
      return null;
    }
    return {
      name: path.basename(filePath, '.py'),
      path: filePath,
      code: fs.readFileSync(filePath, 'utf8')
    };
  }).filter(s => s);

  console.log(`\n共 ${strategies.length} 个策略待运行:`);
  strategies.forEach((s, i) => {
    console.log(`  ${i + 1}. ${s.name} (${s.code.split('\n').length} 行)`);
  });

  // 加载现有session
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

  if (cookies.length > 0) {
    await context.addCookies(cookies);
  }

  const page = await context.newPage();

  // 监控API调用
  const apiLog = [];
  page.on('request', req => {
    const url = req.url();
    if (url.includes('quant.10jqka.com.cn/platform/')) {
      apiLog.push({
        url: url.split('?')[0],
        method: req.method(),
        time: Date.now()
      });
    }
  });

  const results = [];

  try {
    // 1. 打开平台
    console.log('\n打开 THSQuant 平台...');
    await page.goto('https://quant.10jqka.com.cn/view/study-index.html', {
      waitUntil: 'networkidle'
    });
    await page.waitForTimeout(3000);

    // 检查登录状态
    let loginDetected = false;
    const content = await page.content();
    if (content.includes('header-usr-logined') || content.includes('HI！')) {
      loginDetected = true;
      console.log('✓ 已登录');
    } else {
      console.log('\n请手动登录:');
      console.log('  Username: mx_kj1ku00qp');
      console.log('  Password: f09173228552');

      const loginStart = Date.now();
      while (!loginDetected && Date.now() - loginStart < 90000) {
        await page.waitForTimeout(3000);
        const newContent = await page.content();
        if (newContent.includes('header-usr-logined') || newContent.includes('HI！')) {
          loginDetected = true;
          console.log('\n✓ 登录成功!');
        }
        process.stdout.write(`\r等待登录... ${Math.floor((Date.now() - loginStart)/1000)}s`);
      }

      if (!loginDetected) {
        throw new Error('登录超时');
      }
    }

    // 保存session
    const newCookies = await context.cookies();
    fs.writeFileSync(SESSION_FILE, JSON.stringify({
      cookies: newCookies,
      timestamp: Date.now()
    }, null, 2));

    // 2. 遍历策略
    for (const strategy of strategies) {
      console.log('\n' + '-'.repeat(70));
      console.log(`处理策略: ${strategy.name}`);
      console.log('-'.repeat(70));

      try {
        // 导航到策略新建页面
        await page.goto('https://quant.10jqka.com.cn/view/study-index.html#/strategy/new', {
          waitUntil: 'networkidle'
        });
        await page.waitForTimeout(3000);

        // 尝试找到代码编辑器 (可能在iframe中)
        let editorFound = false;
        let codeInput = null;

        // 检查主页面
        const mainEditor = await page.$('textarea, .code-editor textarea, [class*="CodeMirror"]');
        if (mainEditor) {
          codeInput = mainEditor;
          editorFound = true;
          console.log('✓ 找到主页面编辑器');
        }

        // 检查iframe
        if (!editorFound) {
          const frames = page.frames();
          for (const frame of frames) {
            try {
              const frameEditor = await frame.$('textarea, .code-editor textarea, [class*="CodeMirror"]');
              if (frameEditor) {
                codeInput = frameEditor;
                editorFound = true;
                console.log('✓ 找到iframe编辑器');
                break;
              }
            } catch (e) {}
          }
        }

        // 尝试通过点击按钮进入编辑模式
        if (!editorFound) {
          console.log('尝试点击编辑按钮...');

          // 尝试各种可能的按钮
          const btnSelectors = [
            'button:has-text("新建策略")',
            'button:has-text("创建")',
            'a:has-text("新建")',
            '[class*="create"]',
            '[class*="new-strategy"]'
          ];

          for (const selector of btnSelectors) {
            try {
              const btn = await page.$(selector);
              if (btn) {
                await btn.click();
                await page.waitForTimeout(2000);
                console.log(`✓ 点击了按钮: ${selector}`);
                break;
              }
            } catch (e) {}
          }

          await page.waitForTimeout(3000);

          // 再次查找编辑器
          const frames = page.frames();
          for (const frame of frames) {
            try {
              const frameEditor = await frame.$('textarea');
              if (frameEditor) {
                codeInput = frameEditor;
                editorFound = true;
                break;
              }
            } catch (e) {}
          }
        }

        // 截图当前状态
        const screenshotPath = path.join(OUTPUT_ROOT, `batch-${strategy.name}-${Date.now()}.png`);
        await page.screenshot({ path: screenshotPath });

        if (editorFound && codeInput) {
          // 输入代码
          console.log('输入策略代码...');
          await codeInput.fill('');
          await codeInput.fill(strategy.code);
          await page.waitForTimeout(1000);
          console.log('✓ 代码已输入');

          // 尝试保存
          const saveBtn = await page.$('button:has-text("保存")');
          if (saveBtn) {
            await saveBtn.click();
            await page.waitForTimeout(2000);
            console.log('✓ 已保存');
          }

          // 尝试运行回测
          const runBtn = await page.$('button:has-text("运行"), button:has-text("回测")');
          if (runBtn) {
            console.log('点击运行回测...');
            await runBtn.click();
            await page.waitForTimeout(5000);
            console.log('✓ 回测已启动');

            // 等待回测结果
            console.log('等待回测结果 (最多30秒)...');
            await page.waitForTimeout(30000);

            // 截图结果
            const resultPath = path.join(OUTPUT_ROOT, `batch-${strategy.name}-result-${Date.now()}.png`);
            await page.screenshot({ path: resultPath });
            console.log(`✓ 结果截图: ${resultPath}`);
          }

          results.push({ name: strategy.name, status: 'submitted', screenshot });
        } else {
          // 手动模式 - 打印代码供用户复制
          console.log('\n⚠ 未找到编辑器，需要手动操作');
          console.log('请手动复制代码到编辑器并运行');

          // 使用剪贴板
          await page.evaluate(() => {
            navigator.clipboard.writeText(`STRATEGY_CODE_PLACEHOLDER`);
          });

          results.push({ name: strategy.name, status: 'manual_required' });
        }

      } catch (err) {
        console.log(`✗ 处理失败: ${err.message}`);
        results.push({ name: strategy.name, status: 'error', error: err.message });
      }

      // 策略间隔
      await page.waitForTimeout(2000);
    }

    // 保存API日志
    const apiPath = path.join(OUTPUT_ROOT, `batch-api-log-${Date.now()}.json`);
    fs.writeFileSync(apiPath, JSON.stringify(apiLog, null, 2));
    console.log(`\nAPI日志: ${apiPath}`);

    // 保存最终session
    const finalCookies = await context.cookies();
    fs.writeFileSync(SESSION_FILE, JSON.stringify({
      cookies: finalCookies,
      timestamp: Date.now()
    }, null, 2));

    // 打印结果汇总
    console.log('\n' + '='.repeat(70));
    console.log('运行结果汇总');
    console.log('='.repeat(70));
    results.forEach((r, i) => {
      console.log(`${i + 1}. ${r.name}: ${r.status}`);
    });

    console.log('\n浏览器保持打开60秒，可以查看结果...');
    await page.waitForTimeout(60000);

    await browser.close();

    return results;

  } catch (error) {
    console.error('\n错误:', error.message);

    try {
      const cookies = await context.cookies();
      fs.writeFileSync(SESSION_FILE, JSON.stringify({ cookies, timestamp: Date.now() }, null, 2));
    } catch (e) {}

    await browser.close();
    throw error;
  }
}

// 获取策略文件
const args = process.argv.slice(2);

let strategyFiles = [];
if (args.length > 0) {
  strategyFiles = args;
} else {
  // 默认运行所有策略
  strategyFiles = fs.readdirSync(STRATEGIES_DIR)
    .filter(f => f.endsWith('.py') && !f.includes('test'))
    .map(f => path.join(STRATEGIES_DIR, f));
}

batchRunStrategies(strategyFiles).then(results => {
  const success = results.filter(r => r.status === 'submitted').length;
  console.log(`\n✓ 完成: ${success}/${results.length} 个策略已提交`);
}).catch(err => {
  console.error('\n✗ 失败:', err.message);
  process.exit(1);
});