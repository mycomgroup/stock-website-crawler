import { chromium } from 'playwright';
import fs from 'node:fs';

async function exploreLoginModal() {
  console.log('=== Exploring RiceQuant Login Modal ===\n');
  
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext();
  const page = await context.newPage();
  
  try {
    console.log('Opening login page...');
    await page.goto('https://www.ricequant.com/login', { waitUntil: 'networkidle' });
    await page.waitForTimeout(3000);
    
    // 点击登录按钮
    const loginBtn = await page.$('button:has-text("登录")');
    if (loginBtn) {
      await loginBtn.click();
      console.log('✓ Clicked login button');
      await page.waitForTimeout(2000);
    }
    
    // 获取模态框内容
    console.log('\n1. All visible clickable elements:');
    const clickables = await page.$$('a, span, div[class*="tab"], button');
    for (const el of clickables) {
      const visible = await el.isVisible();
      if (visible) {
        const text = await el.textContent();
        const tag = await el.evaluate(e => e.tagName);
        const className = await el.getAttribute('class');
        if (text && text.trim() && text.trim().length < 30) {
          console.log(`  ${tag} [${className?.substring(0, 20)}]: "${text.trim()}"`);
        }
      }
    }
    
    // 查找密码登录相关文字
    console.log('\n2. Looking for password login option...');
    const passwordOption = await page.locator('text=密码登录').first();
    if (await passwordOption.count() > 0) {
      console.log('✓ Found "密码登录" option');
      await passwordOption.click();
      console.log('✓ Clicked password login option');
      await page.waitForTimeout(1000);
    } else {
      console.log('✗ "密码登录" not found, checking other options...');
      // 尝试其他方式
      const pwdOptions = ['密码', 'Password', '密码登录', '账号密码'];
      for (const opt of pwdOptions) {
        const found = await page.locator(`text=${opt}`).first();
        if (await found.count() > 0) {
          console.log(`✓ Found "${opt}"`);
          await found.click();
          await page.waitForTimeout(1000);
          break;
        }
      }
    }
    
    // 再次检查所有可见元素
    console.log('\n3. Visible elements after switch:');
    const afterSwitch = await page.$$('span, div');
    for (const el of afterSwitch) {
      const visible = await el.isVisible();
      if (visible) {
        const text = await el.textContent();
        if (text && text.trim() && text.trim().length < 20 && 
            (text.includes('密码') || text.includes('登录') || text.includes('手机'))) {
          console.log(`  "${text.trim()}"`);
        }
      }
    }
    
    // 检查所有可见的输入框
    console.log('\n4. Visible inputs:');
    const inputs = await page.$$('input');
    for (let i = 0; i < inputs.length; i++) {
      const visible = await inputs[i].isVisible();
      if (visible) {
        const type = await inputs[i].getAttribute('type');
        const placeholder = await inputs[i].getAttribute('placeholder');
        console.log(`  Input ${i}: type=${type}, placeholder=${placeholder}`);
      }
    }
    
    // 获取页面HTML结构中的模态框部分
    console.log('\n5. Checking modal HTML structure...');
    const modalHTML = await page.evaluate(() => {
      // 查找模态框
      const modals = document.querySelectorAll('[class*="modal"], [class*="dialog"], [class*="popup"], [role="dialog"]');
      return Array.from(modals).map(m => ({
        class: m.className.substring(0, 50),
        html: m.innerHTML.substring(0, 500)
      }));
    });
    
    if (modalHTML.length > 0) {
      fs.writeFileSync('modal-structure.json', JSON.stringify(modalHTML, null, 2));
      console.log('✓ Modal structure saved to modal-structure.json');
    }
    
    await page.screenshot({ path: 'login-modal-final.png', fullPage: true });
    console.log('✓ Screenshot saved to login-modal-final.png');
    
  } catch (error) {
    console.error('Error:', error.message);
  } finally {
    await browser.close();
  }
}

exploreLoginModal();
