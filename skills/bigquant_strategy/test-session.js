#!/usr/bin/env node
import './load-env.js';
import { BigQuantClient } from './request/bigquant-client.js';
import { ensureBigQuantSession } from './browser/session-manager.js';

async function testSession() {
  console.log('='.repeat(60));
  console.log('BigQuant Session Test');
  console.log('='.repeat(60));
  
  try {
    console.log('\n1. Testing session...');
    const credentials = {
      username: process.env.BIGQUANT_USERNAME,
      password: process.env.BIGQUANT_PASSWORD
    };
    
    if (!credentials.username || !credentials.password) {
      console.error('✗ Missing credentials in .env file');
      return false;
    }
    
    console.log('  Username:', credentials.username);
    
    const cookies = await ensureBigQuantSession(credentials);
    console.log('  ✓ Session OK (' + cookies.length + ' cookies)');
    
    console.log('\n2. Testing access to AIStudio...');
    const client = new BigQuantClient({ cookies });
    
    const loginStatus = await client.checkLogin();
    console.log('  Result:', JSON.stringify(loginStatus));
    
    if (!loginStatus.success) {
      console.log('  ✗ Session validation failed');
      console.log('  Run: npm run capture');
      return false;
    }
    
    console.log('  ✓ Access granted to:', loginStatus.url);
    
    console.log('\n3. Testing strategy list...');
    const strategies = await client.listStrategies();
    console.log(`  ✓ Found ${strategies.length} studio(s)`);
    strategies.forEach(s => {
      console.log(`    - ${s.name}: ${s.url}`);
    });
    
    console.log('\n' + '='.repeat(60));
    console.log('✓ All tests passed');
    console.log('='.repeat(60));
    console.log('\nNote: BigQuant uses web-based interface.');
    console.log('Visit: https://bigquant.com/aistudio');
    
    return true;
    
  } catch (e) {
    console.error('\n✗ Test failed:', e.message);
    console.error(e.stack);
    return false;
  }
}

testSession().then(success => {
  process.exit(success ? 0 : 1);
});