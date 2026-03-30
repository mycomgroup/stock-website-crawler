#!/usr/bin/env node
/**
 * RiceQuant Session Capture Script
 * 
 * Usage:
 *   1. Run this script: node capture-session.js
 *   2. A browser window will open
 *   3. Login to RiceQuant manually if needed
 *   4. Navigate to workspace/strategies page
 *   5. Press Ctrl+C or wait for timeout to save session
 */

import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const SESSION_FILE = path.join(__dirname, 'data', 'session.json');
const API_TRACES_FILE = path.join(__dirname, 'data', 'api_traces.json');

const TIMEOUT_MS = 120000; // 2 minutes

async function captureSession() {
  console.log('='.repeat(60));
  console.log('RiceQuant Session Capture');
  console.log('='.repeat(60));
  console.log('\nThis script will:');
  console.log('1. Open a browser window');
  console.log('2. Navigate to RiceQuant');
  console.log('3. Wait for you to login manually');
  console.log('4. Capture your session cookies');
  console.log('5. Save them for API use');
  console.log('\nTimeout:', TIMEOUT_MS / 1000, 'seconds');
  console.log('-'.repeat(60));
  
  const browser = await chromium.launch({ 
    headless: false,
    slowMo: 100
  });
  
  const context = await browser.newContext({
    viewport: { width: 1400, height: 900 }
  });
  
  const page = await context.newPage();
  
  // 收集 API 调用
  const apiCalls = [];
  
  page.on('request', request => {
    if (request.resourceType() === 'xhr' || request.resourceType() === 'fetch') {
      apiCalls.push({
        url: request.url(),
        method: request.method(),
        headers: request.headers()
      });
    }
  });
  
  page.on('response', async response => {
    const call = apiCalls.find(c => c.url === response.url());
    if (call) {
      call.status = response.status();
      try {
        call.body = await response.text();
      } catch (e) {}
    }
  });
  
  let sessionSaved = false;
  
  const saveSession = async () => {
    if (sessionSaved) return;
    sessionSaved = true;
    
    console.log('\n'.repeat(2));
    console.log('='.repeat(60));
    console.log('Saving session...');
    
    try {
      // 获取 cookies
      const cookies = await context.cookies();
      
      console.log('\nCookies captured:');
      cookies.forEach(c => console.log(`  ${c.name}: ${c.value.substring(0, 40)}...`));
      
      // 保存 session
      const dataDir = path.dirname(SESSION_FILE);
      if (!fs.existsSync(dataDir)) {
        fs.mkdirSync(dataDir, { recursive: true });
      }
      
      const sessionData = {
        cookies,
        timestamp: Date.now(),
        capturedAt: new Date().toISOString()
      };
      
      fs.writeFileSync(SESSION_FILE, JSON.stringify(sessionData, null, 2));
      console.log('\nSession saved to:', SESSION_FILE);
      
      // 保存 API traces
      fs.writeFileSync(API_TRACES_FILE, JSON.stringify(apiCalls, null, 2));
      console.log('API traces saved to:', API_TRACES_FILE);
      
      // 打印关键 API
      console.log('\n'.repeat(2));
      console.log('='.repeat(60));
      console.log('API Calls Captured:');
      console.log('-'.repeat(60));
      
      apiCalls.forEach((call, i) => {
        console.log(`\n${i + 1}. ${call.method} ${call.url}`);
        console.log(`   Status: ${call.status || 'N/A'}`);
        if (call.body) {
          try {
            const json = JSON.parse(call.body);
            console.log(`   Response: ${JSON.stringify(json).substring(0, 150)}`);
          } catch {
            console.log(`   Response: ${call.body.substring(0, 150)}`);
          }
        }
      });
      
    } catch (e) {
      console.error('Error saving session:', e.message);
    }
    
    console.log('\n'.repeat(2));
    console.log('='.repeat(60));
    console.log('Session capture complete!');
    console.log('You can now use the RiceQuant API.');
    console.log('='.repeat(60));
  };
  
  try {
    // 导航到 RiceQuant
    console.log('\nOpening browser...');
    await page.goto('https://www.ricequant.com', { waitUntil: 'networkidle' });
    
    console.log('\n' + '='.repeat(60));
    console.log('PLEASE LOGIN MANUALLY IN THE BROWSER WINDOW');
    console.log('After login, navigate to the workspace/strategies page');
    console.log('='.repeat(60));
    
    // 等待用户操作或超时
    await page.waitForTimeout(TIMEOUT_MS);
    
    // 超时后保存
    await saveSession();
    
  } catch (e) {
    console.error('Error:', e.message);
    await saveSession();
  } finally {
    await browser.close();
  }
}

// 处理 Ctrl+C
process.on('SIGINT', async () => {
  console.log('\n\nReceived SIGINT, saving session...');
  process.exit(0);
});

captureSession().catch(console.error);