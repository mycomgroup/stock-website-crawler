#!/usr/bin/env node

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const loadEnv = require('../load-env.js');

async function manualLogin() {
  const env = loadEnv();
  const notebookUrl = env.notebookUrl || 'https://www.ricequant.com/research';
  
  console.log('=== RiceQuant 手动登录 ===');
  console.log('请在浏览器中手动登录，登录成功后按回车继续');
  console.log(`Notebook URL: ${notebookUrl}`);
  
  const browser = await chromium.launch({ 
    headless: false,
    slowMo: 100
  });
  
  const context = await browser.newContext();
  const page = await context.newPage();
  
  console.log('访问 RiceQuant...');
  await page.goto(notebookUrl, { waitUntil: 'networkidle', timeout: 60000 });
  
  console.log('\n请在浏览器中完成以下操作:');
  console.log('1. 点击登录按钮');
  console.log('2. 输入账号密码');
  console.log('3. 点击登录');
  console.log('4. 登录成功后，按回车继续');
  
  await new Promise(resolve => {
    process.stdin.once('data', () => {
      resolve();
    });
  });
  
  console.log('\n保存 session...');
  
  const cookies = await context.cookies();
  
  const sessionData = {
    cookies: cookies,
    timestamp: new Date().toISOString(),
    notebookUrl: notebookUrl
  };
  
  const sessionFile = path.join(__dirname, '../data/session.json');
  fs.writeFileSync(sessionFile, JSON.stringify(sessionData, null, 2));
  
  console.log(`✓ Session 已保存: ${sessionFile}`);
  
  await browser.close();
  
  console.log('\n现在可以运行策略了:');
  console.log('node run-strategy.js --strategy examples/simple_backtest.py');
}

manualLogin().catch(console.error);