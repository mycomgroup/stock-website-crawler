#!/usr/bin/env node
/**
 * RiceQuant 手动登录助手
 * 
 * 使用方法：
 * 1. 运行此脚本
 * 2. 在打开的浏览器中手动登录 RiceQuant
 * 3. 登录成功后，按 Ctrl+C 停止脚本
 * 4. Session 会自动保存
 */

import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import readline from 'readline';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const SESSION_FILE = path.join(__dirname, 'data', 'session.json');

async function main() {
  console.log('\n' + '='.repeat(60));
  console.log('RiceQuant 登录助手');
  console.log('='.repeat(60));
  console.log('\n步骤：');
  console.log('1. 浏览器窗口将打开');
  console.log('2. 请手动登录 RiceQuant');
  console.log('3. 登录成功后，按回车键保存 session');
  console.log('='.repeat(60) + '\n');
  
  const browser = await chromium.launch({ 
    headless: false,
    slowMo: 50
  });
  
  const context = await browser.newContext({
    viewport: { width: 1400, height: 900 }
  });
  
  const page = await context.newPage();
  
  try {
    // 打开 RiceQuant
    await page.goto('https://www.ricequant.com', { waitUntil: 'networkidle' });
    
    console.log('浏览器已打开！');
    console.log('请在浏览器中完成登录，然后回到这里按回车键...\n');
    
    // 等待用户按回车
    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout
    });
    
    await new Promise(resolve => {
      rl.question('登录完成后按回车继续...', () => {
        rl.close();
        resolve();
      });
    });
    
    // 保存 cookies
    const cookies = await context.cookies();
    
    console.log('\n捕获到的 Cookies:');
    cookies.forEach(c => console.log(`  ${c.name}: ${c.value.substring(0, 50)}...`));
    
    // 检查是否有登录 cookie
    const hasRqjwt = cookies.some(c => c.name === 'rqjwt');
    const hasSid = cookies.some(c => c.name === 'sid');
    
    if (hasRqjwt || hasSid) {
      // 保存 session
      const sessionData = {
        cookies,
        timestamp: Date.now(),
        capturedAt: new Date().toISOString()
      };
      
      const dataDir = path.dirname(SESSION_FILE);
      if (!fs.existsSync(dataDir)) {
        fs.mkdirSync(dataDir, { recursive: true });
      }
      
      fs.writeFileSync(SESSION_FILE, JSON.stringify(sessionData, null, 2));
      console.log('\n✓ Session 已保存到:', SESSION_FILE);
      
      if (hasRqjwt) {
        console.log('✓ 检测到 rqjwt cookie，登录应该成功！');
      }
    } else {
      console.log('\n⚠ 未检测到登录 cookie，请确保已完成登录');
    }
    
  } catch (e) {
    console.error('错误:', e.message);
  } finally {
    await browser.close();
    console.log('\n完成！');
  }
}

main().catch(console.error);