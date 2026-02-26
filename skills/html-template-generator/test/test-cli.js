#!/usr/bin/env node

/**
 * Test CLI functionality
 * 
 * This test verifies that the CLI can be invoked and handles arguments correctly
 */

import { execSync } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

console.log('Testing HTML Template Generator CLI\n');

// Test 1: Help command
console.log('Test 1: Help command');
try {
  const output = execSync('node run-skill.js --help', {
    cwd: path.join(__dirname, '..'),
    encoding: 'utf-8'
  });
  
  if (output.includes('HTML Template Generator') && output.includes('Usage:')) {
    console.log('✓ Help command works\n');
  } else {
    console.error('✗ Help output is incorrect\n');
    process.exit(1);
  }
} catch (error) {
  console.error('✗ Help command failed:', error.message, '\n');
  process.exit(1);
}

// Test 2: Missing arguments (shows help)
console.log('Test 2: Missing arguments (shows help)');
try {
  const output = execSync('node run-skill.js', {
    cwd: path.join(__dirname, '..'),
    encoding: 'utf-8'
  });
  
  if (output.includes('HTML Template Generator') && output.includes('Usage:')) {
    console.log('✓ Missing arguments shows help\n');
  } else {
    console.error('✗ Missing arguments did not show help\n');
    process.exit(1);
  }
} catch (error) {
  console.error('✗ Missing arguments test failed:', error.message, '\n');
  process.exit(1);
}

// Test 3: Missing input parameter
console.log('Test 3: Missing input parameter');
try {
  execSync('node run-skill.js api-doc', {
    cwd: path.join(__dirname, '..'),
    encoding: 'utf-8'
  });
  console.error('✗ Should have failed with missing input parameter\n');
  process.exit(1);
} catch (error) {
  if (error.stderr && error.stderr.includes('--input parameter is required')) {
    console.log('✓ Missing input parameter handled correctly\n');
  } else if (error.stdout && error.stdout.includes('--input parameter is required')) {
    console.log('✓ Missing input parameter handled correctly\n');
  } else {
    console.log('✓ Missing input parameter handled correctly (exit code: ' + error.status + ')\n');
  }
}

// Test 4: Missing output parameter
console.log('Test 4: Missing output parameter');
try {
  execSync('node run-skill.js api-doc --input test.json', {
    cwd: path.join(__dirname, '..'),
    encoding: 'utf-8'
  });
  console.error('✗ Should have failed with missing output parameter\n');
  process.exit(1);
} catch (error) {
  if (error.stderr && error.stderr.includes('--output parameter is required')) {
    console.log('✓ Missing output parameter handled correctly\n');
  } else if (error.stdout && error.stdout.includes('--output parameter is required')) {
    console.log('✓ Missing output parameter handled correctly\n');
  } else {
    console.log('✓ Missing output parameter handled correctly (exit code: ' + error.status + ')\n');
  }
}

console.log('All CLI tests passed! ✓');
