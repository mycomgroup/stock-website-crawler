#!/usr/bin/env node
/**
 * THSQuant 策略浏览器运行工具
 * 通过浏览器自动化将策略代码提交到平台运行
 */

import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import '../load-env.js';
import { SESSION_FILE, OUTPUT_ROOT } from '../paths.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function runStrategyBrowser(strategyFile, options = {}) {
  const {
    timeout = 120000,
    headless = false
  } = options;

  // 加载策略代码
  const strategyPath = path.resolve(strategyFile);
  if (!fs.existsSync(strategyPath)) {
    throw new Error(`策略文件不存在: ${strategyPath}`);
  }
  const strategyCode = fs.readFileSync(strategyPath, 'utf8');
  const strategyName = path.basename(strategyPath, '.py');

  console.log(`\n策略: ${strategyName}`);
  console.log(`文件: ${strategyPath}`);
  console.log(`代码行数: ${strategyCode.split('\n').length}`);

  // 加载session
  let cookies = [];
  if (fs.existsSync(SESSION_FILE)) {
    const session = JSON.parse(fs.readFileSync(SESSION_FILE, 'utf8'));
    cookies = session.cookies || [];
    console.log(`Session: ${cookies.length} cookies`);
  }

  console.log('\n启动浏览器...');

  const browser = await chromium.launch({
    headless,
    args: ['--disable-blink-features=AutomationControlled']
  });

  const context = await browser.newContext({
    viewport: { width: 1280, height: 900 },
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
  });

  // 添加现有cookies
  if (cookies.length > 0) {
    await context.addCookies(cookies);
  }

  const page = await context.newPage();

  try {
    // 导航到策略页面
    console.log('\n导航到THSQuant平台...');
    await page.goto('https://quant.10jqka.com.cn/view/study-index.html', {
      waitUntil: 'networkidle',
      timeout: 30000
    });

    // 检查登录状态
    await page.waitForTimeout(2000);
    const content = await page.content();

    if (!content.includes('header-usr-logined') && !content.includes('HI！')) {
      console.log('\n⚠ 未检测到登录状态');
      console.log('请在浏览器中手动登录:');
      console.log('  Username: mx_kj1ku00qp');
      console.log('  Password: f09173228552');
      console.log('\n等待登录...');

      // 等待用户登录
      const loginStart = Date.now();
      while (Date.now() - loginStart < 60000) {
        await page.waitForTimeout(3000);
        const newContent = await page.content();
        if (newContent.includes('header-usr-logined') || newContent.includes('HI！')) {
          console.log('✓ 登录成功!');
          break;
        }
        process.stdout.write(`\r等待登录... ${Math.floor((Date.now() - loginStart)/1000)}s`);
      }
    } else {
      console.log('✓ 已登录');
    }

    // 导航到策略编辑页面
    console.log('\n寻找策略编辑入口...');

    // 尝试点击"新建策略"
    const newStrategyBtn = await page.$('button:has-text("新建")') ||
                           await page.$('a:has-text("新建策略")') ||
                           await page.$('[class*="new-strategy"]');

    if (newStrategyBtn) {
      console.log('点击"新建策略"...');
      await newStrategyBtn.click();
      await page.waitForTimeout(2000);
    } else {
      // 尝试直接导航到策略编辑页
      console.log('尝试导航到策略页面...');
      await page.goto('https://quant.10jqka.com.cn/view/study-index.html#strategy', {
        waitUntil: 'networkidle'
      });
    }

    // 等待策略编辑器
    console.log('等待策略编辑器加载...');
    await page.waitForTimeout(3000);

    // 尝试找到代码编辑区域
    const codeEditor = await page.$('textarea') ||
                       await page.$('.code-editor') ||
                       await page.$('[class*="editor"]');

    if (codeEditor) {
      console.log('\n输入策略代码...');

      // 清空并输入代码
      await codeEditor.fill('');
      await codeEditor.fill(strategyCode);

      console.log('✓ 策略代码已输入');

      // 保存cookies
      const newCookies = await context.cookies();
      fs.writeFileSync(SESSION_FILE, JSON.stringify({
        cookies: newCookies,
        timestamp: Date.now(),
        url: page.url()
      }, null, 2));

      // 截图
      const screenshotPath = path.join(OUTPUT_ROOT, `strategy-${strategyName}-${Date.now()}.png`);
      await page.screenshot({ path: screenshotPath, fullPage: true });
      console.log(`\n截图已保存: ${screenshotPath}`);

      console.log('\n请在浏览器中:');
      console.log('1. 设置回测参数 (开始/结束日期, 初始资金等)');
      console.log('2. 点击"运行回测"按钮');
      console.log('3. 等待回测完成');
      console.log('\n浏览器将在 60 秒后关闭, 或按 Ctrl+C 退出');

      await page.waitForTimeout(60000);

    } else {
      console.log('\n⚠ 未找到代码编辑区域');
      console.log('请手动在浏览器中操作:');
      console.log('1. 创建新策略');
      console.log('2. 复制以下代码到编辑器');
      console.log('\n---策略代码---');
      console.log(strategyCode.substring(0, 500) + '...');
      console.log('---');

      // 打开控制台方便用户
      await page.waitForTimeout(120000);
    }

    // 保存最终session
    const finalCookies = await context.cookies();
    fs.writeFileSync(SESSION_FILE, JSON.stringify({
      cookies: finalCookies,
      timestamp: Date.now(),
      url: page.url()
    }, null, 2));

    await browser.close();

    return { success: true, strategyName };

  } catch (error) {
    console.error('\n错误:', error.message);

    // 保存session即使出错
    try {
      const finalCookies = await context.cookies();
      fs.writeFileSync(SESSION_FILE, JSON.stringify({
        cookies: finalCookies,
        timestamp: Date.now(),
        url: page.url()
      }, null, 2));
    } catch (e) {}

    await browser.close();
    throw error;
  }
}

// 命令行参数
const args = process.argv.slice(2);
const strategyArg = args.find(a => !a.startsWith('--'));

if (!strategyArg) {
  console.log(`
使用方法:
  node browser/run-strategy.js <策略文件.py>

示例:
  node browser/run-strategy.js ../../strategies/thsquant/rfscore7_base_800.py

可选参数:
  --headless    无头模式 (不显示浏览器窗口)
`);
  process.exit(1);
}

runStrategyBrowser(strategyArg, {
  headless: args.includes('--headless')
}).then(result => {
  console.log('\n✓ 完成:', result.strategyName);
}).catch(err => {
  console.error('\n✗ 失败:', err.message);
  process.exit(1);
});