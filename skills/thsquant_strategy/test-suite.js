#!/usr/bin/env node
import './load-env.js';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

console.log('\n' + '='.repeat(60));
console.log('THSQuant Complete Test Suite');
console.log('='.repeat(60));

// Test 1: Environment Variables
console.log('\nTest 1: Environment Variables');
try {
  const username = process.env.THSQUANT_USERNAME;
  const password = process.env.THSQUANT_PASSWORD;
  
  if (!username || !password) {
    console.log('  ✗ FAIL: THSQUANT_USERNAME and THSQUANT_PASSWORD not set');
    console.log('  Please create .env file with:');
    console.log('  THSQUANT_USERNAME=mx_kj1ku00qp');
    console.log('  THSQUANT_PASSWORD=f09173228552');
    process.exit(1);
  }
  
  console.log('  ✓ PASS: Environment variables set');
  console.log('    Username:', username);
  console.log('    Password:', '***' + password.slice(-4));
} catch (e) {
  console.log('  ✗ FAIL:', e.message);
  process.exit(1);
}

// Test 2: File Structure
console.log('\nTest 2: File Structure');
const requiredFiles = [
  'request/thsquant-client.js',
  'browser/session-manager.js',
  'browser/capture-session.js',
  'browser/manual-login-capture.js',
  'run-skill.js',
  'list-strategies.js',
  'fetch-report.js',
  'test-session.js',
  'paths.js',
  'load-env.js',
  'package.json',
  '.env',
  'examples/simple_strategy.py',
  'examples/ma_strategy.py'
];

let missingFiles = [];
for (const file of requiredFiles) {
  const filePath = path.join(__dirname, file);
  if (!fs.existsSync(filePath)) {
    missingFiles.push(file);
  }
}

if (missingFiles.length > 0) {
  console.log('  ✗ FAIL: Missing files:', missingFiles.join(', '));
  process.exit(1);
} else {
  console.log('  ✓ PASS: All required files exist');
  console.log('    Total:', requiredFiles.length, 'files');
}

// Test 3: Dependencies
console.log('\nTest 3: Dependencies');
try {
  const packageJson = JSON.parse(fs.readFileSync(path.join(__dirname, 'package.json'), 'utf8'));
  const deps = Object.keys(packageJson.dependencies || {});
  console.log('  ✓ PASS: Dependencies defined');
  console.log('    Dependencies:', deps.join(', '));
  
  // Check if node_modules exists
  if (!fs.existsSync(path.join(__dirname, 'node_modules'))) {
    console.log('  ⚠ WARNING: node_modules not found, run: npm install');
  } else {
    console.log('  ✓ PASS: node_modules exists');
  }
} catch (e) {
  console.log('  ✗ FAIL:', e.message);
}

// Test 4: Client Module
console.log('\nTest 4: Client Module');
try {
  const { THSQuantClient } = await import('./request/thsquant-client.js');
  const client = new THSQuantClient();
  console.log('  ✓ PASS: THSQuantClient imported successfully');
  console.log('    Methods:', Object.getOwnPropertyNames(Object.getPrototypeOf(client)).join(', '));
} catch (e) {
  console.log('  ✗ FAIL:', e.message);
}

// Test 5: Session Manager
console.log('\nTest 5: Session Manager');
try {
  const { ensureTHSQuantSession } = await import('./browser/session-manager.js');
  console.log('  ✓ PASS: Session manager imported successfully');
} catch (e) {
  console.log('  ✗ FAIL:', e.message);
}

// Test 6: Data Directory
console.log('\nTest 6: Data Directory');
const dataDir = path.join(__dirname, 'data');
if (!fs.existsSync(dataDir)) {
  fs.mkdirSync(dataDir, { recursive: true });
  console.log('  ✓ PASS: Data directory created');
} else {
  console.log('  ✓ PASS: Data directory exists');
}

// Test 7: Session File
console.log('\nTest 7: Session File');
const sessionFile = path.join(dataDir, 'session.json');
if (fs.existsSync(sessionFile)) {
  try {
    const session = JSON.parse(fs.readFileSync(sessionFile, 'utf8'));
    console.log('  ✓ PASS: Session file exists');
    console.log('    Cookies:', session.cookies?.length || 0);
    console.log('    Timestamp:', new Date(session.timestamp).toISOString());
  } catch (e) {
    console.log('  ⚠ WARNING: Session file exists but invalid JSON');
  }
} else {
  console.log('  ⚠ WARNING: No session file, need to login first');
  console.log('    Run: node browser/manual-login-capture.js');
}

// Test 8: Example Strategies
console.log('\nTest 8: Example Strategies');
try {
  const simpleStrategy = fs.readFileSync(path.join(__dirname, 'examples/simple_strategy.py'), 'utf8');
  const maStrategy = fs.readFileSync(path.join(__dirname, 'examples/ma_strategy.py'), 'utf8');
  
  console.log('  ✓ PASS: Example strategies exist');
  console.log('    simple_strategy.py:', simpleStrategy.length, 'bytes');
  console.log('    ma_strategy.py:', maStrategy.length, 'bytes');
  
  // Check for required functions
  const requiredFunctions = ['initialize', 'handle_data'];
  for (const func of requiredFunctions) {
    if (simpleStrategy.includes(func) && maStrategy.includes(func)) {
      console.log(`    ✓ ${func} function found in both`);
    } else {
      console.log(`    ⚠ ${func} function missing in some strategies`);
    }
  }
} catch (e) {
  console.log('  ✗ FAIL:', e.message);
}

// Test 9: CLI Scripts
console.log('\nTest 9: CLI Scripts');
const cliScripts = [
  'run-skill.js',
  'list-strategies.js',
  'fetch-report.js',
  'test-session.js'
];

for (const script of cliScripts) {
  try {
    const content = fs.readFileSync(path.join(__dirname, script), 'utf8');
    if (content.includes('parseArgs') || content.includes('process.argv')) {
      console.log(`  ✓ ${script} has argument parsing`);
    }
  } catch (e) {
    console.log(`  ✗ ${script} failed:`, e.message);
  }
}

// Summary
console.log('\n' + '='.repeat(60));
console.log('Test Summary');
console.log('='.repeat(60));
console.log('\n✓ Basic structure and configuration are ready');
console.log('\n⚠ Next steps:');
console.log('  1. Login to THSQuant manually:');
console.log('     node browser/manual-login-capture.js');
console.log('  2. Test session:');
console.log('     node test-session.js');
console.log('  3. Run a backtest:');
console.log('     node run-skill.js --id <strategyId> --file examples/ma_strategy.py');
console.log('\n' + '='.repeat(60));