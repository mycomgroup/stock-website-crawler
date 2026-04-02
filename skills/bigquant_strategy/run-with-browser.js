#!/usr/bin/env node
/**
 * BigQuant 策略完整执行 - 浏览器自动化方案
 *
 * 流程:
 * 1. 创建任务 (通过 HTTP API)
 * 2. 打开浏览器 (Playwright)
 * 3. 自动点击运行按钮
 * 4. 等待执行完成
 * 5. 获取执行结果
 */

import { chromium } from 'playwright';
import './load-env.js';
import { BigQuantTaskClient } from './request/bigquant-task-client.js';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg.startsWith('--')) {
      const key = arg.slice(2);
      const value = argv[i + 1];
      if (value && !value.startsWith('--')) {
        args[key] = value;
        i++;
      } else {
        args[key] = true;
      }
    }
  }
  return args;
}

async function runStrategyWithBrowser(args) {
  console.log('='.repeat(60));
  console.log('BigQuant Strategy Runner (Browser Automation)');
  console.log('='.repeat(60));

  // 读取策略代码
  let code = '';
  let name = 'strategy';

  if (args.strategy) {
    const strategyPath = path.resolve(args.strategy);
    if (!fs.existsSync(strategyPath)) {
      console.error('错误: 策略文件不存在:', strategyPath);
      process.exit(1);
    }
    code = fs.readFileSync(strategyPath, 'utf8');
    name = args.name || path.basename(strategyPath, '.py');
  } else {
    console.error('错误: 请指定 --strategy');
    process.exit(1);
  }

  // Step 1: 创建任务
  console.log('\n[Step 1] 创建任务...');

  const client = new BigQuantTaskClient();
  const result = await client.runStrategy(name, code, {
    startDate: args['start-date'] || '2023-01-01',
    endDate: args['end-date'] || '2023-12-31',
    capital: parseInt(args.capital) || 100000
  });

  console.log('Task ID:', result.taskId);
  console.log('Web URL:', result.webUrl);

  // Step 2: 浏览器自动化
  console.log('\n[Step 2] 启动浏览器自动化...');

  const sessionFile = path.join(__dirname, 'data/session.json');
  const session = JSON.parse(fs.readFileSync(sessionFile, 'utf8'));

  const browser = await chromium.launch({ headless: args.headless ? true : false });
  const context = await browser.newContext();
  await context.addCookies(session.cookies);

  const page = await context.newPage();

  // 打开任务页面
  console.log('打开任务页面...');
  await page.goto(result.webUrl, { waitUntil: 'networkidle', timeout: 60000 });

  // 等待页面加载
  await page.waitForTimeout(5000);

  console.log('页面已加载，查找运行按钮...');

  // 尝试多种方式找到运行按钮
  const runButtonSelectors = [
    // VS Code 运行按钮 (可能在不同位置)
    'button[aria-label*="Run"]',
    'button[title*="Run"]',
    'button[title*="运行"]',
    '.run-button',
    '.toolbar-item-run',
    // BigQuant 特定按钮
    'button.bigquant-run',
    '[class*="run-all"]',
    // 通用运行按钮
    'button:has-text("Run")',
    'button:has-text("运行")',
    'button:has-text("Run All")',
    'button:has-text("全部运行")',
    // VS Code 命令面板
    '[aria-label="Run Code"]',
  ];

  let runButton = null;
  for (const selector of runButtonSelectors) {
    try {
      runButton = await page.$(selector);
      if (runButton) {
        console.log('找到运行按钮:', selector);
        break;
      }
    } catch (e) {}
  }

  if (!runButton) {
    console.log('未找到可见的运行按钮，使用快捷键方式...');
  } else {
    console.log('找到运行按钮，尝试强制点击...');
    try {
      // 强制点击 (即使元素不完全可见)
      await runButton.dispatchEvent('click');
    } catch (e) {
      console.log('点击失败，使用快捷键...');
    }
  }

  // 使用 VS Code 快捷键运行
  // Ctrl+Shift+A 或 Ctrl+Enter 运行当前单元格
  console.log('尝试快捷键: Ctrl+Enter (运行当前单元格)');
  await page.keyboard.down('Control');
  await page.keyboard.press('Enter');
  await page.keyboard.up('Control');
  await page.waitForTimeout(2000);

  // 如果没有反应，尝试其他快捷键
  console.log('尝试快捷键: Ctrl+Shift+A (运行全部)');
  await page.keyboard.down('Control');
  await page.keyboard.down('Shift');
  await page.keyboard.press('KeyA');
  await page.keyboard.up('Shift');
  await page.keyboard.up('Control');
  await page.waitForTimeout(2000);

  // 尝试 F5 运行
  console.log('尝试快捷键: F5');
  await page.keyboard.press('F5');
  await page.waitForTimeout(3000);

  // 尝试通过 VS Code 命令面板运行
  console.log('尝试命令面板: Ctrl+Shift+P -> Run Task');
  await page.keyboard.down('Control');
  await page.keyboard.down('Shift');
  await page.keyboard.press('KeyP');
  await page.keyboard.up('Shift');
  await page.keyboard.up('Control');
  await page.waitForTimeout(2000);

  // 输入运行命令
  await page.keyboard.type('Run Task');
  await page.waitForTimeout(1000);
  await page.keyboard.press('Enter');
  await page.waitForTimeout(3000);

  // 保存调试截图
  const debugScreenshot = path.join(__dirname, `data/debug-${result.taskId}.png`);
  await page.screenshot({ path: debugScreenshot, fullPage: true });
  console.log('调试截图:', debugScreenshot);

  // Step 3: 监控执行状态
  console.log('\n[Step 3] 监控执行状态...');

  let lastState = null;
  const maxWait = parseInt(args.timeout) || 180000; // 3分钟
  const startTime = Date.now();

  while (Date.now() - startTime < maxWait) {
    const task = await client.getTask(result.taskId);
    const currentState = task.data?.last_run?.state || 'none';

    if (currentState !== lastState) {
      const timestamp = new Date().toLocaleTimeString();
      console.log(`[${timestamp}] 状态: ${currentState}`);
      lastState = currentState;
    }

    // 检查完成状态
    if (currentState === 'success') {
      console.log('\n✓ 任务执行成功！');

      // 尝试获取输出
      const taskDetail = await client.getTask(result.taskId);

      // 从 notebook 中提取输出
      if (taskDetail.data?.data?.code) {
        try {
          const notebook = JSON.parse(taskDetail.data.data.code);
          const outputs = [];

          for (const cell of notebook.cells || []) {
            if (cell.outputs?.length > 0) {
              outputs.push(...cell.outputs);
            }
          }

          if (outputs.length > 0) {
            console.log('\n=== 执行输出 ===');
            for (const output of outputs) {
              if (output.text) {
                console.log(output.text);
              }
              if (output.data?.['text/plain']) {
                console.log(output.data['text/plain']);
              }
            }
          }
        } catch (e) {
          console.log('解析输出失败:', e.message);
        }
      }

      break;
    }

    if (currentState === 'failed') {
      console.log('\n✗ 任务执行失败');

      // 尝试获取错误信息
      const taskDetail = await client.getTask(result.taskId);
      if (taskDetail.data?.last_run?.message) {
        console.log('错误:', taskDetail.data.last_run.message);
      }

      break;
    }

    await new Promise(r => setTimeout(r, 5000));
  }

  // 截图保存
  const screenshotPath = path.join(__dirname, `data/result-${result.taskId}.png`);
  await page.screenshot({ path: screenshotPath, fullPage: true });
  console.log('\n截图保存到:', screenshotPath);

  // Step 4: 关闭浏览器
  await browser.close();

  console.log('\n' + '='.repeat(60));
  console.log('执行完成');
  console.log('='.repeat(60));
  console.log('\nTask ID:', result.taskId);
  console.log('最终状态:', lastState);
  console.log('截图:', screenshotPath);

  return { taskId: result.taskId, state: lastState, screenshotPath };
}

const args = parseArgs(process.argv.slice(2));
runStrategyWithBrowser(args).catch(console.error);