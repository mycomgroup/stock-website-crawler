#!/usr/bin/env node

/**
 * Test script to verify pages directory timestamp feature
 * 测试脚本：验证pages目录时间戳功能
 */

import Logger from '../stock-crawler/src/logger.js';
import fs from 'fs';
import path from 'path';

console.log('Testing pages directory timestamp feature...\n');

// Create a test logger
const testLogDir = './test-logs';
const logger = new Logger(testLogDir);

// Get the timestamp
const timestamp = logger.getTimestamp();
console.log(`✓ Logger timestamp: ${timestamp}`);
console.log(`✓ Log file: ${logger.getLogFile()}`);

// Simulate pages directory creation
const testProjectDir = './test-output';
const pagesDir = `${testProjectDir}/pages-${timestamp}`;

console.log(`✓ Pages directory would be: ${pagesDir}`);

// Verify timestamp format (YYYYMMDD-HHmmss)
const timestampRegex = /^\d{8}-\d{6}$/;
if (timestampRegex.test(timestamp)) {
  console.log('✓ Timestamp format is correct (YYYYMMDD-HHmmss)');
} else {
  console.error('✗ Timestamp format is incorrect');
  process.exit(1);
}

// Verify log file name matches pages directory suffix
const logFileName = path.basename(logger.getLogFile());
const expectedLogName = `crawler-${timestamp}.log`;
if (logFileName === expectedLogName) {
  console.log('✓ Log file name matches expected format');
} else {
  console.error(`✗ Log file name mismatch: ${logFileName} vs ${expectedLogName}`);
  process.exit(1);
}

// Clean up test directories
if (fs.existsSync(testLogDir)) {
  fs.rmSync(testLogDir, { recursive: true, force: true });
}

console.log('\n✓ All tests passed!');
console.log('\nExample output structure:');
console.log('  output/lixinger-crawler/');
console.log(`    ├── pages-${timestamp}/`);
console.log('    └── logs/');
console.log(`        └── crawler-${timestamp}.log`);
