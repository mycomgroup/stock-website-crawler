#!/usr/bin/env node
/**
 * 测试 HAR 提取功能
 */

import { AutoExtractWorkflow } from './auto-extract-workflow.js';
import fs from 'fs';

async function runTests() {
  console.log('开始测试 HAR 提取功能...\n');

  const testCases = [
    {
      name: 'jsonplaceholder',
      url: 'https://jsonplaceholder.typicode.com/posts',
      description: '测试简单的 REST API'
    }
  ];

  const workflow = new AutoExtractWorkflow({
    outputDir: 'output/test-har-extraction',
    formats: ['python', 'node', 'curl'],
    validate: false, // 跳过验证以加快测试
    waitTime: 2000
  });

  const results = [];

  for (const testCase of testCases) {
    console.log(`\n${'='.repeat(60)}`);
    console.log(`测试: ${testCase.name}`);
    console.log(`描述: ${testCase.description}`);
    console.log(`${'='.repeat(60)}\n`);

    try {
      const result = await workflow.run(testCase.url, testCase.name);
      
      // 验证输出
      const checks = {
        harExists: fs.existsSync(result.harPath),
        apisJsonExists: fs.existsSync(`${result.apisDir}/apis.json`),
        readmeExists: fs.existsSync(`${result.apisDir}/README.md`),
        pythonDirExists: fs.existsSync(`${result.apisDir}/python`),
        nodeDirExists: fs.existsSync(`${result.apisDir}/node`),
        curlDirExists: fs.existsSync(`${result.apisDir}/curl`)
      };

      const allPassed = Object.values(checks).every(v => v);

      results.push({
        name: testCase.name,
        success: allPassed,
        checks
      });

      console.log(`\n检查结果:`);
      Object.entries(checks).forEach(([key, value]) => {
        console.log(`  ${value ? '✅' : '❌'} ${key}`);
      });

    } catch (error) {
      console.error(`❌ 测试失败: ${error.message}`);
      results.push({
        name: testCase.name,
        success: false,
        error: error.message
      });
    }
  }

  // 总结
  console.log(`\n${'='.repeat(60)}`);
  console.log('测试总结');
  console.log(`${'='.repeat(60)}\n`);

  const passed = results.filter(r => r.success).length;
  const failed = results.filter(r => !r.success).length;

  console.log(`总计: ${results.length}`);
  console.log(`通过: ${passed}`);
  console.log(`失败: ${failed}`);

  results.forEach(result => {
    const status = result.success ? '✅' : '❌';
    console.log(`\n${status} ${result.name}`);
    if (result.error) {
      console.log(`   错误: ${result.error}`);
    }
  });

  console.log();

  return results;
}

// 运行测试
if (import.meta.url === `file://${process.argv[1]}`) {
  runTests().catch(error => {
    console.error('测试失败:', error);
    process.exit(1);
  });
}

export { runTests };
