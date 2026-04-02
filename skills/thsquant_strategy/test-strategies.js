#!/usr/bin/env node
import './load-env.js';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const examplesDir = path.join(__dirname, 'examples');

console.log('\n' + '='.repeat(60));
console.log('THSQuant Strategy Syntax Tests');
console.log('='.repeat(60));

// Test strategy files for syntax and structure
const strategyFiles = fs.readdirSync(examplesDir).filter(f => f.endsWith('.py'));

console.log('\nFound', strategyFiles.length, 'strategy files');

for (const file of strategyFiles) {
  console.log('\n' + '-'.repeat(60));
  console.log('Testing:', file);
  console.log('-'.repeat(60));
  
  const filePath = path.join(examplesDir, file);
  const code = fs.readFileSync(filePath, 'utf8');
  
  // Test 1: File exists and readable
  console.log('  ✓ File exists and readable');
  console.log('    Size:', code.length, 'bytes');
  
  // Test 2: Python syntax check (basic)
  console.log('\n  Syntax checks:');
  
  // Check for required functions
  const requiredFuncs = ['initialize', 'handle_data'];
  const optionalFuncs = ['rebalance', 'before_trading_start', 'after_trading_end'];
  
  for (const func of requiredFuncs) {
    if (code.includes(`def ${func}`)) {
      console.log(`    ✓ Required function: ${func}`);
    } else {
      console.log(`    ✗ Missing required function: ${func}`);
    }
  }
  
  for (const func of optionalFuncs) {
    if (code.includes(`def ${func}`)) {
      console.log(`    ✓ Optional function: ${func}`);
    }
  }
  
  // Check for common patterns
  console.log('\n  Pattern checks:');
  
  const patterns = [
    { name: 'context parameter', pattern: /def \w+\(context/ },
    { name: 'global variable', pattern: /g\.\w+/ },
    { name: 'order function', pattern: /order|order_target/ },
    { name: 'logging', pattern: /log\.|print\(/ },
    { name: 'data access', pattern: /data\[|attribute_history/ }
  ];
  
  for (const { name, pattern } of patterns) {
    if (pattern.test(code)) {
      console.log(`    ✓ ${name}`);
    }
  }
  
  // Check for potential issues
  console.log('\n  Issue checks:');
  
  const issues = [
    { name: 'Tabs vs Spaces', test: code.includes('\t') },
    { name: 'Unbalanced parentheses', test: (code.match(/\(/g)?.length || 0) !== (code.match(/\)/g)?.length || 0) },
    { name: 'Missing imports', test: code.includes('import ') || code.includes('from ') }
  ];
  
  for (const { name, test } of issues) {
    if (test) {
      console.log(`    ⚠ ${name}`);
    }
  }
  
  // Extract function definitions
  console.log('\n  Functions defined:');
  const funcs = code.match(/def \w+\([^)]*\)/g) || [];
  funcs.forEach(f => console.log(`    ${f}`));
}

console.log('\n' + '='.repeat(60));
console.log('Strategy Syntax Tests Complete');
console.log('='.repeat(60));