#!/usr/bin/env node
/**
 * 测试脚本：验证generate-template-config.js的功能
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

console.log('=== 测试 generate-template-config.js ===\n');

// 测试1: 显示帮助信息
console.log('测试1: 显示帮助信息');
console.log('-------------------');
try {
  const output = execSync('node skills/template-content-analyzer/scripts/generate-template-config.js --help', {
    encoding: 'utf-8'
  });
  console.log('✓ 帮助信息显示正常\n');
} catch (error) {
  console.error('✗ 帮助信息显示失败:', error.message);
  process.exit(1);
}

// 测试2: 检查命令行参数解析
console.log('测试2: 检查命令行参数解析');
console.log('-------------------');
try {
  const { parseArgs } = require('../scripts/generate-template-config.js');
  
  // 保存原始参数
  const originalArgv = process.argv;
  
  // 测试默认参数
  process.argv = ['node', 'script.js'];
  const defaultOptions = parseArgs();
  console.log('✓ 默认参数解析成功');
  console.log(`  patterns: ${defaultOptions.patterns}`);
  console.log(`  pages: ${defaultOptions.pages}`);
  console.log(`  output: ${defaultOptions.output}`);
  
  // 测试自定义参数
  process.argv = [
    'node', 'script.js',
    '--patterns', 'test/patterns.json',
    '--pages', 'test/pages',
    '--output', 'test/output.jsonl',
    '--pattern-name', 'test-pattern',
    '--template-threshold', '0.9',
    '--unique-threshold', '0.1',
    '--yes'
  ];
  const customOptions = parseArgs();
  console.log('✓ 自定义参数解析成功');
  console.log(`  patterns: ${customOptions.patterns}`);
  console.log(`  patternName: ${customOptions.patternName}`);
  console.log(`  templateThreshold: ${customOptions.templateThreshold}`);
  console.log(`  skipConfirm: ${customOptions.skipConfirm}`);
  
  // 恢复原始参数
  process.argv = originalArgv;
  
  console.log('');
} catch (error) {
  console.error('✗ 参数解析失败:', error.message);
  process.exit(1);
}

// 测试3: 验证脚本可执行性
console.log('测试3: 验证脚本可执行性');
console.log('-------------------');
try {
  const scriptPath = 'skills/template-content-analyzer/scripts/generate-template-config.js';
  const stats = fs.statSync(scriptPath);
  const isExecutable = (stats.mode & 0o111) !== 0;
  
  if (isExecutable) {
    console.log('✓ 脚本具有可执行权限');
  } else {
    console.log('⚠ 脚本没有可执行权限（可选）');
  }
  console.log('');
} catch (error) {
  console.error('✗ 检查脚本权限失败:', error.message);
  process.exit(1);
}

// 测试4: 检查依赖模块
console.log('测试4: 检查依赖模块');
console.log('-------------------');
try {
  const TemplateContentAnalyzer = require('../lib/content-analyzer');
  const ConfigLoader = require('../lib/config-loader');
  
  console.log('✓ TemplateContentAnalyzer 模块加载成功');
  console.log('✓ ConfigLoader 模块加载成功');
  console.log('');
} catch (error) {
  console.error('✗ 依赖模块加载失败:', error.message);
  process.exit(1);
}

// 测试5: 验证输入文件检查（使用真实数据）
console.log('测试5: 验证输入文件检查');
console.log('-------------------');
try {
  const patternsPath = 'stock-crawler/output/lixinger-crawler/url-patterns.json';
  const pagesDir = 'stock-crawler/output/lixinger-crawler/pages';
  
  if (fs.existsSync(patternsPath)) {
    console.log(`✓ 找到测试数据: ${patternsPath}`);
  } else {
    console.log(`⚠ 测试数据不存在: ${patternsPath}`);
  }
  
  if (fs.existsSync(pagesDir)) {
    console.log(`✓ 找到页面目录: ${pagesDir}`);
  } else {
    console.log(`⚠ 页面目录不存在: ${pagesDir}`);
  }
  
  console.log('');
} catch (error) {
  console.error('✗ 文件检查失败:', error.message);
  process.exit(1);
}

console.log('=== 所有测试通过 ===\n');
console.log('脚本功能验证完成！');
console.log('\n要运行完整的配置生成，请执行:');
console.log('  node skills/template-content-analyzer/scripts/generate-template-config.js -y');
console.log('\n或者只生成特定模式:');
console.log('  node skills/template-content-analyzer/scripts/generate-template-config.js -n rate-of-return-rank-us -y');
