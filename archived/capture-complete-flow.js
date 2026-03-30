import { chromium } from 'playwright';
import fs from 'node:fs';

async function captureCompleteFlow() {
  console.log('=== Capturing Complete RiceQuant Flow ===\n');
  
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext();
  const page = await context.newPage();
  
  // 捕获所有请求
  const apiRequests = [];
  page.on('request', request => {
    const url = request.url();
    if (url.includes('ricequant.com/api') && !url.includes('isLogin.do')) {
      apiRequests.push({
        method: request.method(),
        url: url,
        postData: request.postData(),
        timestamp: Date.now()
      });
    }
  });
  
  // 捕获响应
  page.on('response', async response => {
    const url = response.url();
    if (url.includes('ricequant.com/api') && !url.includes('isLogin.do') && !url.includes('rqmessager')) {
      try {
        const body = await response.text();
        const preview = body.substring(0, 300).replace(/\n/g, ' ');
        console.log(`[${response.status()}] ${url.split('ricequant.com')[1]}`);
        console.log(`  ${preview}`);
        console.log('');
      } catch (e) {}
    }
  });
  
  try {
    // 登录
    console.log('1. Login...');
    await page.goto('https://www.ricequant.com/login', { waitUntil: 'networkidle' });
    await page.waitForTimeout(3000);
    
    const loginBtn = await page.$('button:has-text("登录")');
    if (loginBtn) await loginBtn.click();
    await page.waitForTimeout(2000);
    
    const passwordOption = await page.locator('text=密码登录').first();
    if (await passwordOption.count() > 0) {
      await passwordOption.click();
      await page.waitForTimeout(1000);
    }
    
    await page.waitForSelector('input[type="password"]', { timeout: 5000, state: 'visible' });
    const usernameInput = await page.$('input[placeholder="国内手机号或邮箱"]');
    const passwordInput = await page.$('input[type="password"][placeholder*="密码"]');
    await usernameInput.fill('13311390323');
    await passwordInput.fill('3228552');
    
    const loginSubmitBtn = await page.$('.el-dialog.user-status button.btn--submit');
    if (loginSubmitBtn) await loginSubmitBtn.click();
    
    console.log('Waiting for login...');
    await page.waitForTimeout(8000);
    
    // 清除登录相关的请求
    apiRequests.length = 0;
    
    // 导航到量化页面
    console.log('\n2. Navigating to quant page...');
    await page.goto('https://www.ricequant.com/quant/strategys', { waitUntil: 'networkidle' });
    await page.waitForTimeout(5000);
    
    // 截图
    await page.screenshot({ path: 'quant-page.png' });
    
    // 查找并点击新建按钮
    console.log('\n3. Clicking "New" button...');
    const newBtn = await page.$('button:has-text("新建")');
    if (newBtn) {
      await newBtn.click();
      await page.waitForTimeout(3000);
    }
    
    // 截图
    await page.screenshot({ path: 'after-click-new.png' });
    
    // 检查是否有策略编辑器出现
    console.log('\n4. Looking for code editor...');
    const editor = await page.$('.ace_editor, .CodeMirror, [class*="editor"], [class*="code"]');
    if (editor) {
      console.log('✓ Found code editor');
      
      // 读取策略代码
      const strategyCode = fs.readFileSync('strategy_rfscore_v2.py', 'utf8');
      console.log(`Strategy code length: ${strategyCode.length} chars`);
      
      // 尝试粘贴代码
      console.log('\n5. Trying to paste strategy code...');
      
      // 查找代码输入框
      const textarea = await page.$('textarea, .ace_text-input');
      if (textarea) {
        // 使用JavaScript直接设置内容
        await page.evaluate((code) => {
          // 尝试Ace编辑器
          if (window.ace) {
            const editors = document.querySelectorAll('.ace_editor');
            if (editors.length > 0) {
              const editor = ace.edit(editors[0]);
              editor.setValue(code);
              return true;
            }
          }
          return false;
        }, strategyCode);
        console.log('✓ Code pasted');
      }
    } else {
      console.log('✗ No code editor found');
    }
    
    await page.waitForTimeout(2000);
    
    // 列出所有API请求
    console.log('\n6. All captured API requests:');
    apiRequests.forEach((req, i) => {
      console.log(`  ${i + 1}. ${req.method} ${req.url.split('ricequant.com')[1]}`);
      if (req.postData) {
        const preview = req.postData.substring(0, 200);
        console.log(`     POST: ${preview}`);
      }
    });
    
    // 保存
    fs.writeFileSync('complete-flow.json', JSON.stringify(apiRequests, null, 2));
    console.log('\n✓ Saved to complete-flow.json');
    
  } catch (error) {
    console.error('Error:', error.message);
  } finally {
    await browser.close();
  }
}

captureCompleteFlow();
