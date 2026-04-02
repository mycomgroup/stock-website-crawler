#!/usr/bin/env node
/**
 * THSQuant 手动登录 + 策略运行工具
 * 打开浏览器等待用户手动登录，然后帮助提交策略代码
 */

import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import '../load-env.js';
import { SESSION_FILE, OUTPUT_ROOT } from '../paths.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function manualLoginAndRunStrategy(strategyFile) {
  // 读取策略代码
  const strategyPath = path.resolve(strategyFile);
  if (!fs.existsSync(strategyPath)) {
    throw new Error(`策略文件不存在: ${strategyPath}`);
  }
  const strategyCode = fs.readFileSync(strategyPath, 'utf8');
  const strategyName = path.basename(strategyPath, '.py');

  console.log('\n' + '='.repeat(60));
  console.log('THSQuant 策略运行工具');
  console.log('='.repeat(60));
  console.log(`\n策略: ${strategyName}`);
  console.log(`文件: ${strategyPath}`);
  console.log(`代码行数: ${strategyCode.split('\n').length}`);

  console.log('\n' + '='.repeat(60));
  console.log('登录信息:');
  console.log('  Username: mx_kj1ku00qp');
  console.log('  Password: f09173228552');
  console.log('='.repeat(60));

  console.log('\n启动浏览器...');

  const browser = await chromium.launch({
    headless: false,
    args: ['--disable-blink-features=AutomationControlled']
  });

  const context = await browser.newContext({
    viewport: { width: 1400, height: 900 },
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
  });

  const page = await context.newPage();

  // 监控登录API
  let loginDetected = false;
  page.on('response', async response => {
    const url = response.url();
    if (url.includes('/platform/user/getauthdata')) {
      try {
        const text = await response.text();
        if (text.includes('errorcode":0') || !text.includes('尚未登录')) {
          loginDetected = true;
          console.log('\n✓ 检测到登录成功!');
        }
      } catch (e) {}
    }
  });

  try {
    // 打开首页
    console.log('\n打开 THSQuant 平台...');
    await page.goto('https://quant.10jqka.com.cn/view/study-index.html', {
      waitUntil: 'networkidle'
    });

    console.log('\n' + '-'.repeat(60));
    console.log('请在浏览器中完成以下步骤:');
    console.log('-'.repeat(60));
    console.log('1. 点击右上角"登录"按钮');
    console.log('2. 输入账号密码:');
    console.log('   Username: mx_kj1ku00qp');
    console.log('   Password: f09173228552');
    console.log('3. 完成登录后，此脚本会自动检测');
    console.log('-'.repeat(60));

    // 等待登录
    const loginStart = Date.now();
    const loginTimeout = 120000; // 2分钟

    while (!loginDetected && Date.now() - loginStart < loginTimeout) {
      await page.waitForTimeout(2000);

      // 检查页面内容是否显示登录状态
      try {
        const content = await page.content();
        if (content.includes('header-usr-logined') ||
            content.includes('HI！') ||
            content.includes('mx_kj')) {
          loginDetected = true;
          console.log('\n✓ 检测到登录成功!');
        }
      } catch (e) {}

      if (!loginDetected) {
        const elapsed = Math.floor((Date.now() - loginStart) / 1000);
        process.stdout.write(`\r等待登录... ${elapsed}s / ${loginTimeout/1000}s`);
      }
    }

    if (!loginDetected) {
      console.log('\n\n⚠ 登录超时，请重试');
      await browser.close();
      return { success: false, reason: 'login_timeout' };
    }

    // 保存session
    console.log('\n保存 Session...');
    const cookies = await context.cookies();
    fs.writeFileSync(SESSION_FILE, JSON.stringify({
      cookies,
      timestamp: Date.now(),
      url: page.url()
    }, null, 2));
    console.log('✓ Session 已保存');

    // 截图
    const screenshotPath = path.join(OUTPUT_ROOT, `login-success-${Date.now()}.png`);
    await page.screenshot({ path: screenshotPath });
    console.log(`✓ 截图: ${screenshotPath}`);

    // 导航到策略页面
    console.log('\n导航到策略编辑页面...');
    await page.goto('https://quant.10jqka.com.cn/view/study-index.html#/strategy/new', {
      waitUntil: 'networkidle'
    });
    await page.waitForTimeout(3000);

    const editorScreenshot = path.join(OUTPUT_ROOT, `strategy-editor-${Date.now()}.png`);
    await page.screenshot({ path: editorScreenshot });
    console.log(`✓ 编辑器截图: ${editorScreenshot}`);

    // 显示策略代码供用户复制
    console.log('\n' + '='.repeat(60));
    console.log('请在浏览器中:');
    console.log('1. 点击"新建策略"或找到策略编辑入口');
    console.log('2. 将以下代码复制粘贴到编辑器:');
    console.log('='.repeat(60));
    console.log('\n--- 策略代码开始 ---\n');
    console.log(strategyCode);
    console.log('\n--- 策略代码结束 ---\n');

    console.log('='.repeat(60));
    console.log('浏览器将保持打开，请手动完成:');
    console.log('1. 粘贴代码到编辑器');
    console.log('2. 设置回测参数 (日期、资金等)');
    console.log('3. 点击"运行回测"');
    console.log('4. 查看回测结果');
    console.log('='.repeat(60));

    console.log('\n按 Ctrl+C 退出，或等待自动关闭 (5分钟)...');

    // 等待用户操作
    await page.waitForTimeout(300000);

    // 保存最终状态
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

    try {
      const cookies = await context.cookies();
      fs.writeFileSync(SESSION_FILE, JSON.stringify({
        cookies,
        timestamp: Date.now(),
        url: page.url()
      }, null, 2));
    } catch (e) {}

    await browser.close();
    throw error;
  }
}

// 命令行参数
const strategyArg = process.argv[2];

if (!strategyArg) {
  console.log(`
使用方法:
  node browser/manual-run-strategy.js <策略文件.py>

示例:
  node browser/manual-run-strategy.js ../../strategies/thsquant/rfscore7_base_800.py
`);
  process.exit(1);
}

manualLoginAndRunStrategy(strategyArg).then(result => {
  if (result.success) {
    console.log('\n✓ 完成:', result.strategyName);
  } else {
    console.log('\n✗ 失败:', result.reason);
  }
}).catch(err => {
  console.error('\n✗ 错误:', err.message);
  process.exit(1);
});