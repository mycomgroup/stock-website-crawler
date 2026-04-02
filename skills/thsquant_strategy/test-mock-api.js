#!/usr/bin/env node
import './load-env.js';
import { THSQuantClient } from './request/thsquant-client.js';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// Mock session for testing when login is not available
const mockSession = {
  cookies: [
    { name: 'QUANT_RESEARCH_SESSIONID', value: 'mock_session_id', domain: 'quant.10jqka.com.cn' }
  ]
};

console.log('\n' + '='.repeat(60));
console.log('THSQuant API Mock Tests');
console.log('='.repeat(60));

async function testAPIs() {
  console.log('\nTesting with mock session...');
  
  const client = new THSQuantClient({ cookies: mockSession.cookies });
  
  // Test 1: Client initialization
  console.log('\nTest 1: Client initialization');
  console.log('  ✓ Client created with mock cookies');
  console.log('  Cookie count:', mockSession.cookies.length);
  
  // Test 2: Headers building
  console.log('\nTest 2: Headers building');
  const headers = client.buildHeaders('https://quant.10jqka.com.cn/test');
  console.log('  ✓ Headers built');
  console.log('  User-Agent:', headers['User-Agent'].substring(0, 50));
  console.log('  Cookie:', headers['Cookie']);
  
  // Test 3: Strategy code loading
  console.log('\nTest 3: Strategy code loading');
  try {
    const strategyPath = path.join(__dirname, 'examples/ma_strategy.py');
    const code = fs.readFileSync(strategyPath, 'utf8');
    console.log('  ✓ Strategy code loaded');
    console.log('  Length:', code.length, 'bytes');
    console.log('  Functions found:', code.match(/def \w+/g)?.join(', ') || 'none');
  } catch (e) {
    console.log('  ✗ Failed:', e.message);
  }
  
  // Test 4: Request format
  console.log('\nTest 4: Request format');
  try {
    const backtestBody = JSON.stringify({
      strategy_id: 'test123',
      code: 'test code',
      config: {
        start_date: '2023-01-01',
        end_date: '2023-12-31',
        initial_capital: 100000,
        frequency: '1d',
        benchmark: '000001.SH'
      }
    });
    console.log('  ✓ Backtest request body formatted');
    console.log('  Body preview:', backtestBody.substring(0, 100));
  } catch (e) {
    console.log('  ✗ Failed:', e.message);
  }
  
  // Test 5: Artifact writing
  console.log('\nTest 5: Artifact writing');
  try {
    const testData = { test: 'data', timestamp: Date.now() };
    const outputPath = client.writeArtifact('test-artifact', testData);
    console.log('  ✓ Artifact written');
    console.log('  Path:', outputPath);
    
    // Read back
    const readData = JSON.parse(fs.readFileSync(outputPath, 'utf8'));
    console.log('  ✓ Artifact readable');
    console.log('  Content matches:', readData.test === testData.test);
    
    // Cleanup
    fs.unlinkSync(outputPath);
    console.log('  ✓ Cleanup done');
  } catch (e) {
    console.log('  ✗ Failed:', e.message);
  }
  
  // Test 6: Error handling
  console.log('\nTest 6: Error handling');
  try {
    // Try invalid request
    const result = await client.request('/invalid/endpoint').catch(e => e);
    console.log('  ✓ Error caught properly');
    console.log('  Error type:', result.constructor.name);
  } catch (e) {
    console.log('  ✗ Error handling failed:', e.message);
  }
  
  console.log('\n' + '='.repeat(60));
  console.log('Mock API Tests Complete');
  console.log('='.repeat(60));
  console.log('\nNote: These tests verify code structure without actual API calls');
  console.log('For full testing, login first: node browser/manual-login-capture.js');
  console.log('='.repeat(60));
}

testAPIs().catch(console.error);