#!/usr/bin/env node
import './load-env.js';

console.log('='.repeat(60));
console.log('BigQuant Comprehensive Test Suite');
console.log('='.repeat(60));
console.log('\nRunning tests...\n');

import { spawn } from 'child_process';

const tests = [
  { name: 'API Mock Test', file: 'test-api.js', required: true },
  { name: 'Session Test', file: 'test-session.js', required: true }
];

let passed = 0;
let failed = 0;

async function runTest(test) {
  console.log(`\n${'─'.repeat(60)}`);
  console.log(`Test: ${test.name}`);
  console.log('─'.repeat(60));
  
  return new Promise((resolve) => {
    const child = spawn('node', [test.file], {
      cwd: process.cwd(),
      stdio: 'inherit'
    });
    
    child.on('close', (code) => {
      if (code === 0) {
        console.log(`\n✓ ${test.name} passed`);
        passed++;
        resolve(true);
      } else {
        console.log(`\n✗ ${test.name} failed`);
        failed++;
        resolve(false);
      }
    });
    
    child.on('error', (err) => {
      console.log(`\n✗ ${test.name} error:`, err.message);
      failed++;
      resolve(false);
    });
  });
}

async function runAllTests() {
  for (const test of tests) {
    await runTest(test);
  }
  
  console.log('\n' + '='.repeat(60));
  console.log('Test Summary');
  console.log('='.repeat(60));
  console.log(`Passed: ${passed}/${tests.length}`);
  console.log(`Failed: ${failed}/${tests.length}`);
  console.log('='.repeat(60));
  
  if (failed > 0) {
    console.log('\nSome tests failed. Check the output above for details.');
    console.log('\nTroubleshooting:');
    console.log('  1. Run: npm run capture');
    console.log('  2. Check .env file has correct credentials');
    process.exit(1);
  } else {
    console.log('\n✓ All core tests passed!');
    console.log('\nNext steps:');
    console.log('  - Visit: https://bigquant.com/aistudio');
    console.log('  - Use web interface to create and run strategies');
    process.exit(0);
  }
}

runAllTests();