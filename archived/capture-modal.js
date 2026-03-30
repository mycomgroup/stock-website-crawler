import { chromium } from 'playwright';
import fs from 'node:fs';

async function captureFullModal() {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();
  
  await page.goto('https://www.ricequant.com/login', { waitUntil: 'networkidle' });
  await page.waitForTimeout(3000);
  
  // 点击登录按钮
  const loginBtn = await page.$('button:has-text("登录")');
  if (loginBtn) await loginBtn.click();
  await page.waitForTimeout(2000);
  
  // 切换到密码登录
  const passwordOption = await page.locator('text=密码登录').first();
  if (await passwordOption.count() > 0) {
    await passwordOption.click();
    await page.waitForTimeout(1000);
  }
  
  // 获取模态框完整内容
  const modalHTML = await page.evaluate(() => {
    const dialog = document.querySelector('.el-dialog.user-status');
    if (dialog) {
      return dialog.innerHTML;
    }
    return 'No dialog found';
  });
  
  fs.writeFileSync('modal-full.html', modalHTML);
  console.log('✓ Saved modal-full.html');
  
  // 列出模态框内的所有按钮
  const buttons = await page.$$('.el-dialog.user-status button');
  console.log(`\nButtons in modal: ${buttons.length}`);
  for (let i = 0; i < buttons.length; i++) {
    const text = await buttons[i].textContent();
    const visible = await buttons[i].isVisible();
    const className = await buttons[i].getAttribute('class');
    console.log(`  ${i}: "${text?.trim()}" (${className}) visible=${visible}`);
  }
  
  await browser.close();
}

captureFullModal();
