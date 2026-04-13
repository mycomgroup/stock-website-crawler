#!/usr/bin/env node

/**
 * 测试所有技能的 anti-detection.js 是否能正常导入和运行
 */

import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import { readdir, stat } from 'fs/promises';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const SKILLS_TO_TEST = [
  'bigquant_strategy',
  'thsquant_strategy',
  'guorn_strategy',
  'ricequant_strategy',
  'joinquant_strategy',
  'lixinger-screener',
  'chatgpt_api',
  'gemini_api',
  '10jqka_backtest',
  'html-template-generator'
];

console.log('🧪 Testing anti-detection.js in all skills...\n');
console.log('━'.repeat(60));
console.log();

let passCount = 0;
let failCount = 0;
const results = [];

for (const skill of SKILLS_TO_TEST) {
  const skillPath = join(__dirname, skill);
  const antiDetectionPath = join(skillPath, 'lib', 'anti-detection.js');
  
  process.stdout.write(`Testing ${skill}... `);
  
  try {
    // 测试1: 检查文件是否存在
    await stat(antiDetectionPath);
    
    // 测试2: 尝试导入模块
    const module = await import(`file://${antiDetectionPath}`);
    
    // 测试3: 检查导出的类
    const { AntiDetection, SessionManager, RateLimiter } = module;
    
    if (!AntiDetection) {
      throw new Error('AntiDetection class not found');
    }
    if (!SessionManager) {
      throw new Error('SessionManager class not found');
    }
    if (!RateLimiter) {
      throw new Error('RateLimiter class not found');
    }
    
    // 测试4: 检查关键方法
    const requiredMethods = [
      'setupBrowser',
      'injectAntiDetection',
      'setRealisticHeaders',
      'randomDelay',
      'getRandomUserAgent',
      'simulateHumanBehavior',
      'fetchWithRetry',
      'createRealisticHeaders'
    ];
    
    for (const method of requiredMethods) {
      if (typeof AntiDetection[method] !== 'function') {
        throw new Error(`Method ${method} not found or not a function`);
      }
    }
    
    // 测试5: 测试简单功能
    const ua = AntiDetection.getRandomUserAgent();
    if (!ua || typeof ua !== 'string') {
      throw new Error('getRandomUserAgent() failed');
    }
    
    const headers = AntiDetection.createRealisticHeaders();
    if (!headers || typeof headers !== 'object') {
      throw new Error('createRealisticHeaders() failed');
    }
    
    console.log('✅ PASS');
    passCount++;
    results.push({ skill, status: 'PASS', error: null });
    
  } catch (error) {
    console.log(`❌ FAIL: ${error.message}`);
    failCount++;
    results.push({ skill, status: 'FAIL', error: error.message });
  }
}

console.log();
console.log('━'.repeat(60));
console.log();
console.log('📊 Test Summary:');
console.log(`   Total:  ${SKILLS_TO_TEST.length}`);
console.log(`   ✅ Pass:  ${passCount}`);
console.log(`   ❌ Fail:  ${failCount}`);
console.log();

if (failCount > 0) {
  console.log('❌ Failed Skills:');
  results
    .filter(r => r.status === 'FAIL')
    .forEach(r => {
      console.log(`   - ${r.skill}: ${r.error}`);
    });
  console.log();
}

if (passCount === SKILLS_TO_TEST.length) {
  console.log('🎉 All tests passed!');
  console.log();
  console.log('✅ All skills have working anti-detection.js');
  console.log('✅ All required classes are exported');
  console.log('✅ All required methods are available');
  console.log('✅ Basic functionality works');
  process.exit(0);
} else {
  console.log('⚠️  Some tests failed. Please check the errors above.');
  process.exit(1);
}
