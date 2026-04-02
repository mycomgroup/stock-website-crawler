#!/usr/bin/env node
import './load-env.js';
import { THSQuantClient } from './request/thsquant-client.js';
import { ensureTHSQuantSession } from './browser/session-manager.js';

async function testSession() {
  try {
    console.log('Testing THSQuant session...\n');
    
    const credentials = {
      username: process.env.THSQUANT_USERNAME,
      password: process.env.THSQUANT_PASSWORD
    };
    
    if (!credentials.username || !credentials.password) {
      console.error('Error: THSQUANT_USERNAME and THSQUANT_PASSWORD must be set in .env');
      process.exit(1);
    }
    
    console.log('1. Checking environment variables...');
    console.log('   Username:', credentials.username);
    console.log('   Password:', credentials.password ? '***' + credentials.password.slice(-4) : 'N/A');
    
    console.log('\n2. Loading/creating session...');
    const cookies = await ensureTHSQuantSession(credentials);
    console.log('   Session loaded:', cookies.length, 'cookies');
    
    const client = new THSQuantClient({ cookies });
    
    console.log('\n3. Verifying login status...');
    const loginStatus = await client.checkLogin();
    
    if (loginStatus.code === 0 || loginStatus.code === 200) {
      console.log('   ✓ Login successful');
      console.log('   User info:', JSON.stringify(loginStatus.data || loginStatus).substring(0, 100));
    } else {
      console.log('   ✗ Login failed:', loginStatus.message || JSON.stringify(loginStatus));
      process.exit(1);
    }
    
    console.log('\n4. Testing strategy list...');
    const strategies = await client.listStrategies();
    console.log('   ✓ Found', strategies.length, 'strategies');
    
    console.log('\n✓ All tests passed! Session is valid.');
    
  } catch (e) {
    console.error('\n✗ Test failed:', e.message);
    console.error(e.stack);
    process.exit(1);
  }
}

testSession();