import { chromium } from 'playwright';
import '../load-env.js';
import { SESSION_FILE } from '../paths.js';
import fs from 'fs';

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

function saveSession(session) {
  const dir = './data';
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  fs.writeFileSync(SESSION_FILE, JSON.stringify(session, null, 2));
  console.log(`Session saved to ${SESSION_FILE}`);
}

function getScreenshotPath(name) {
  const dir = './data';
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  return `${dir}/${name}`;
}

export async function captureBigQuantSession(credentials, options = {}) {
  const headed = options.headed || false;
  
  console.log('Launching browser for BigQuant...');
  
  const browser = await chromium.launch({ headless: !headed });
  const context = await browser.newContext({
    viewport: { width: 1280, height: 720 }
  });
  
  const page = await context.newPage();
  
  try {
    console.log('1. Navigating to bigquant.com...');
    await page.goto('https://bigquant.com', { waitUntil: 'networkidle' });
    await page.waitForTimeout(5000);
    
    await page.screenshot({ path: getScreenshotPath('01-homepage.png') });
    
    console.log('2. Clicking login button...');
    const loginBtn = await page.$('button:has-text("登录")');
    
    if (!loginBtn) {
      throw new Error('Login button not found');
    }
    
    await loginBtn.click();
    console.log('   ✓ Login modal opened');
    await page.waitForTimeout(5000);
    
    await page.screenshot({ path: getScreenshotPath('02-login-modal.png') });
    
    console.log('3. Switching to password login mode...');
    const passwordTab = await page.$('text=密码登录');
    
    if (!passwordTab) {
      await page.screenshot({ path: getScreenshotPath('03-no-password-tab.png') });
      throw new Error('Password login tab not found');
    }
    
    await passwordTab.click();
    console.log('   ✓ Switched to password login');
    await page.waitForTimeout(5000);
    
    await page.screenshot({ path: getScreenshotPath('03-password-mode.png') });
    
    console.log('4. Finding input fields...');
    const usernameInput = await page.$('input[placeholder="请输入用户名"]');
    const passwordInput = await page.$('input[placeholder="请输入登录密码"]');
    
    if (!usernameInput || !passwordInput) {
      await page.screenshot({ path: getScreenshotPath('04-no-inputs.png') });
      throw new Error('Username or password input not found');
    }
    
    console.log('   ✓ Input fields found');
    
    console.log('5. Filling credentials...');
    await usernameInput.click();
    await usernameInput.fill(credentials.username);
    console.log('   ✓ Username filled:', credentials.username);
    
    await page.waitForTimeout(5000);
    
    await passwordInput.click();
    await passwordInput.fill(credentials.password);
    console.log('   ✓ Password filled');
    
    await page.screenshot({ path: getScreenshotPath('05-filled.png') });
    
    console.log('6. Submitting login...');
    await page.waitForTimeout(3000);
    
    // 使用更精确的选择器和force点击
    const loginButtonInModal = await page.$('.ant-modal-content button:has-text("登录")');
    
    if (loginButtonInModal) {
      await loginButtonInModal.click({ force: true });
      console.log('   ✓ Login button clicked (force)');
    } else {
      // 尝试按Enter
      await page.keyboard.press('Enter');
      console.log('   ✓ Enter key pressed');
    }
    
    await page.waitForTimeout(10000);
    
    await page.screenshot({ path: getScreenshotPath('06-after-login.png') });
    
    const currentUrl = page.url();
    console.log('   Current URL:', currentUrl);
    
    if (currentUrl.includes('login')) {
      console.log('   ⚠ Still on login page, checking for errors...');
      await page.screenshot({ path: getScreenshotPath('07-login-failed.png') });
    } else {
      console.log('   ✓ Login successful!');
    }
    
    console.log('7. Capturing cookies...');
    const cookies = await context.cookies();
    console.log(`   ✓ Captured ${cookies.length} cookies`);
    
    return {
      cookies,
      timestamp: Date.now()
    };
    
  } catch (error) {
    console.error('\n✗ Error:', error.message);
    await page.screenshot({ path: getScreenshotPath('error.png'), fullPage: true });
    throw error;
  } finally {
    try {
      await browser.close();
    } catch (e) {
      console.error('Browser close error:', e.message);
    }
  }
}

const args = parseArgs(process.argv.slice(2));

if (args.help) {
  console.log('Usage: node capture-session.js [--headed]');
  console.log('Options:');
  console.log('  --headed    Run in headed mode (visible browser)');
  console.log('  --help      Show this help message');
  process.exit(0);
}

captureBigQuantSession({
  username: process.env.BIGQUANT_USERNAME,
  password: process.env.BIGQUANT_PASSWORD
}, { headed: args.headed }).then(session => {
  saveSession(session);
  console.log('\n✓ Session captured successfully');
  console.log(`  Cookies: ${session.cookies.length}`);
  console.log('\nNext steps:');
  console.log('  1. Run: npm run test:session');
  console.log('  2. Run: npm run list');
}).catch(err => {
  console.error('\n✗ Failed:', err.message);
  console.log('\nTry manual capture instead:');
  console.log('  npm run manual-capture');
  process.exit(1);
});