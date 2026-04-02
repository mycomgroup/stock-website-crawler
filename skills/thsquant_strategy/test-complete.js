#!/usr/bin/env node
import './load-env.js';
import { THSQuantClient } from './request/thsquant-client.js';
import { ensureTHSQuantSession } from './browser/session-manager.js';

console.log('\n' + '='.repeat(60));
console.log('THSQuant Strategy Runner - Complete Test');
console.log('='.repeat(60));

async function testCompleteWorkflow() {
  try {
    // 1. Test session
    console.log('\n1. Testing session...');
    const credentials = {
      username: process.env.THSQUANT_USERNAME,
      password: process.env.THSQUANT_PASSWORD
    };
    
    if (!credentials.username || !credentials.password) {
      throw new Error('THSQUANT_USERNAME and THSQUANT_PASSWORD must be set in .env');
    }
    
    console.log('   Username:', credentials.username);
    console.log('   Password:', '***' + credentials.password.slice(-4));
    
    const cookies = await ensureTHSQuantSession(credentials);
    console.log('   ✓ Session loaded:', cookies.length, 'cookies');
    
    // 2. Test client
    console.log('\n2. Testing THSQuant client...');
    const client = new THSQuantClient({ cookies });
    
    // Try to check login status
    console.log('   Checking login...');
    const loginResult = await client.checkLogin();
    console.log('   Login result:', JSON.stringify(loginResult).substring(0, 100));
    
    // 3. Test API endpoints
    console.log('\n3. Testing API endpoints...');
    
    // Try various possible endpoints
    const endpoints = [
      '/platform/user/getauthdata',
      '/platform/strategy/list',
      '/platform/strategy/mylist',
      '/platform/backtest/list',
      '/api/user/info',
      '/api/strategy/list'
    ];
    
    for (const endpoint of endpoints) {
      try {
        console.log(`\n   Trying: ${endpoint}`);
        const result = await client.request(endpoint, {
          method: 'POST',
          body: 'isajax=1'
        });
        
        if (result.errorcode === 0) {
          console.log('   ✓ Success:', JSON.stringify(result).substring(0, 100));
        } else {
          console.log('   Response:', result.errormsg || JSON.stringify(result).substring(0, 100));
        }
      } catch (e) {
        console.log('   ✗ Failed:', e.message.substring(0, 50));
      }
    }
    
    console.log('\n' + '='.repeat(60));
    console.log('Test completed');
    console.log('='.repeat(60));
    
    return true;
    
  } catch (e) {
    console.error('\n✗ Test failed:', e.message);
    console.error(e.stack);
    return false;
  }
}

testCompleteWorkflow();