import './load-env.js';
import { RiceQuantClient } from './request/ricequant-client.js';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const SESSION_FILE = path.join(__dirname, 'data', 'session.json');

async function loginAndTest() {
  console.log('=== RiceQuant Login Test ===\n');
  
  const username = process.env.RICEQUANT_USERNAME;
  const password = process.env.RICEQUANT_PASSWORD;
  
  if (!username || !password) {
    console.error('Error: RICEQUANT_USERNAME and RICEQUANT_PASSWORD must be set in .env');
    process.exit(1);
  }
  
  console.log('Username:', username);
  
  const client = new RiceQuantClient();
  
  // 1. 检查当前登录状态
  console.log('\n1. Checking current login status...');
  let loginStatus = await client.checkLogin();
  console.log('Login status:', JSON.stringify(loginStatus));
  
  // 如果已登录，直接使用
  if (loginStatus.code === 0 || loginStatus.data?.isLoggedIn) {
    console.log('\nAlready logged in!');
  } else {
    // 2. 尝试登录
    console.log('\n2. Attempting login...');
    const loginResult = await client.login(username, password);
    console.log('Login result:', JSON.stringify(loginResult));
    
    if (loginResult.code !== 0 && loginResult.code !== '0') {
      console.error('\nLogin failed!');
      console.log('\nPossible reasons:');
      console.log('1. Wrong username/password');
      console.log('2. Need captcha verification');
      console.log('3. Account locked');
      console.log('\nPlease login manually in browser first:');
      console.log('  node browser/capture-api.js');
      return;
    }
    
    // 登录成功后，获取新的 cookies
    console.log('\nLogin successful!');
  }
  
  // 3. 获取 workspaces
  console.log('\n3. Getting workspaces...');
  try {
    const workspaces = await client.getWorkspaces();
    console.log('Workspaces:', JSON.stringify(workspaces, null, 2));
  } catch (e) {
    console.log('Error:', e.message);
  }
  
  // 4. 获取策略列表
  console.log('\n4. Getting strategies...');
  try {
    const strategies = await client.listStrategies();
    console.log(`Found ${strategies.length} strategies`);
    strategies.forEach(s => {
      console.log(`  - ${s.name || s.strategyName} (${s.id || s.strategyId})`);
    });
  } catch (e) {
    console.log('Error:', e.message);
  }
}

loginAndTest().catch(console.error);