import { chromium } from 'playwright';
import readline from 'node:readline';

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

function question(query) {
  return new Promise(resolve => rl.question(query, resolve));
}

async function manualLogin() {
  console.log('=== RiceQuant Manual Login Helper ===\n');
  console.log('This tool will open a browser for you to login manually.');
  console.log('After you complete the login, press Enter to capture the session.\n');
  
  const browser = await chromium.launch({ 
    headless: false,
    args: ['--start-maximized']
  });
  
  const context = await browser.newContext({
    viewport: { width: 1280, height: 720 }
  });
  
  const page = await context.newPage();
  
  try {
    // 直接访问登录页面
    console.log('Opening login page...');
    await page.goto('https://www.ricequant.com/login', { waitUntil: 'networkidle' });
    
    console.log('\n✓ Browser opened. Please login manually.');
    console.log('  URL: https://www.ricequant.com/login\n');
    
    // 等待用户完成登录
    await question('Press Enter after you have logged in...');
    
    // 额外等待确保页面稳定
    await page.waitForTimeout(2000);
    
    // 获取当前URL
    const currentUrl = page.url();
    console.log(`\nCurrent URL: ${currentUrl}`);
    
    // 获取cookies
    const cookies = await context.cookies();
    console.log(`\nCaptured ${cookies.length} cookies:`);
    
    const sessionData = {
      url: currentUrl,
      cookies: cookies.map(c => ({
        name: c.name,
        value: c.value.substring(0, 20) + (c.value.length > 20 ? '...' : ''),
        domain: c.domain,
        path: c.path
      })),
      fullCookies: cookies,
      timestamp: Date.now()
    };
    
    console.log('\nCookie Details:');
    sessionData.cookies.forEach((c, i) => {
      console.log(`  ${i + 1}. ${c.name} (${c.domain})`);
    });
    
    // 尝试从页面提取token
    console.log('\nTrying to extract tokens from page...');
    try {
      const tokens = await page.evaluate(() => {
        const results = {};
        
        // 检查localStorage
        if (window.localStorage) {
          for (let i = 0; i < localStorage.length; i++) {
            const key = localStorage.key(i);
            const value = localStorage.getItem(key);
            if (key.toLowerCase().includes('token') || 
                key.toLowerCase().includes('session') ||
                key.toLowerCase().includes('auth')) {
              results[`localStorage.${key}`] = value;
            }
          }
        }
        
        // 检查sessionStorage
        if (window.sessionStorage) {
          for (let i = 0; i < sessionStorage.length; i++) {
            const key = sessionStorage.key(i);
            const value = sessionStorage.getItem(key);
            if (key.toLowerCase().includes('token') || 
                key.toLowerCase().includes('session') ||
                key.toLowerCase().includes('auth')) {
              results[`sessionStorage.${key}`] = value;
            }
          }
        }
        
        // 检查全局变量
        if (window.__INITIAL_STATE__) {
          results['__INITIAL_STATE__'] = JSON.stringify(window.__INITIAL_STATE__).substring(0, 100);
        }
        
        return results;
      });
      
      if (Object.keys(tokens).length > 0) {
        console.log('\nTokens found:');
        Object.entries(tokens).forEach(([key, value]) => {
          console.log(`  ${key}: ${value.substring(0, 50)}${value.length > 50 ? '...' : ''}`);
        });
        sessionData.tokens = tokens;
      } else {
        console.log('  No tokens found in storage');
      }
    } catch (e) {
      console.log('  Error extracting tokens:', e.message);
    }
    
    // 保存会话文件
    const fs = await import('node:fs');
    const path = await import('node:path');
    const { SESSION_FILE, OUTPUT_ROOT } = await import('../paths.js');
    
    const sessionFile = path.resolve(SESSION_FILE);
    const outputRoot = path.resolve(OUTPUT_ROOT);
    
    // 确保目录存在
    fs.mkdirSync(path.dirname(sessionFile), { recursive: true });
    fs.mkdirSync(outputRoot, { recursive: true });
    
    // 保存完整会话
    fs.writeFileSync(sessionFile, JSON.stringify({
      cookies: cookies,
      timestamp: Date.now()
    }, null, 2));
    
    console.log(`\n✓ Session saved to: ${sessionFile}`);
    
    // 保存调试信息
    const debugFile = path.join(outputRoot, `login-debug-${Date.now()}.json`);
    fs.writeFileSync(debugFile, JSON.stringify(sessionData, null, 2));
    console.log(`✓ Debug info saved to: ${debugFile}`);
    
    return sessionData;
    
  } catch (error) {
    console.error('\n✗ Error:', error.message);
    throw error;
  } finally {
    await browser.close();
    rl.close();
  }
}

manualLogin().then(() => {
  console.log('\n✓ Login capture complete!');
  process.exit(0);
}).catch(err => {
  console.error('\n✗ Failed:', err.message);
  process.exit(1);
});
