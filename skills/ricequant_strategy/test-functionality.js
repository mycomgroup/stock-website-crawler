#!/usr/bin/env node
/**
 * 功能验证测试脚本
 * 
 * 测试内容：
 * 1. Session 管理
 * 2. 创建独立 notebook
 * 3. 执行代码
 * 4. 自动清理
 */

import { fileURLToPath } from 'node:url';
import { runNotebookTest } from './request/test-ricequant-notebook.js';

const tests = [
  {
    name: '基础连接测试',
    options: {
      cellSource: 'print("基础连接测试成功！")',
      timeoutMs: 30000,
      createNew: false,
      cleanup: false
    }
  },
  {
    name: '创建独立notebook测试',
    options: {
      cellSource: `
import datetime
print(f"测试时间: {datetime.datetime.now()}")
print("独立notebook创建成功！")
`,
      timeoutMs: 30000,
      createNew: true,
      cleanup: false
    }
  },
  {
    name: '自动清理测试',
    options: {
      cellSource: 'print("这个notebook将被自动清理")',
      timeoutMs: 30000,
      createNew: true,
      cleanup: true
    }
  }
];

async function runTests() {
  console.log('=== RiceQuant Notebook 功能验证测试 ===\n');
  
  const results = [];
  
  for (let i = 0; i < tests.length; i++) {
    const test = tests[i];
    console.log(`\n测试 ${i + 1}/${tests.length}: ${test.name}`);
    console.log('-'.repeat(60));
    
    try {
      const startTime = Date.now();
      const result = await runNotebookTest(test.options);
      const duration = Date.now() - startTime;
      
      console.log(`✓ 测试通过 (${duration}ms)`);
      console.log(`  Notebook: ${result.notebookPath}`);
      console.log(`  执行 cells: ${result.targetCellIndices.length}`);
      console.log(`  新建 notebook: ${result.newNotebookCreated ? '是' : '否'}`);
      console.log(`  自动清理: ${result.cleanupResult?.success ? '成功' : '否'}`);
      
      if (result.executions.length > 0 && result.executions[0].textOutput) {
        console.log(`  输出:\n${result.executions[0].textOutput.split('\n').map(line => '    ' + line).join('\n')}`);
      }
      
      results.push({
        name: test.name,
        status: 'passed',
        duration,
        notebookPath: result.notebookPath,
        newNotebookCreated: result.newNotebookCreated,
        cleanupSuccess: result.cleanupResult?.success
      });
      
    } catch (error) {
      console.log(`✗ 测试失败: ${error.message}`);
      results.push({
        name: test.name,
        status: 'failed',
        error: error.message
      });
    }
  }
  
  console.log('\n' + '='.repeat(60));
  console.log('测试汇总');
  console.log('='.repeat(60));
  
  const passed = results.filter(r => r.status === 'passed').length;
  const failed = results.filter(r => r.status === 'failed').length;
  
  console.log(`总计: ${results.length} 个测试`);
  console.log(`通过: ${passed} 个`);
  console.log(`失败: ${failed} 个`);
  
  if (failed > 0) {
    console.log('\n失败的测试:');
    results.filter(r => r.status === 'failed').forEach(r => {
      console.log(`  - ${r.name}: ${r.error}`);
    });
  }
  
  console.log('\n详细结果:');
  results.forEach((r, i) => {
    console.log(`  ${i + 1}. ${r.name}: ${r.status === 'passed' ? '✓ 通过' : '✗ 失败'}`);
    if (r.status === 'passed') {
      console.log(`     耗时: ${r.duration}ms`);
      console.log(`     新建: ${r.newNotebookCreated ? '是' : '否'}`);
      console.log(`     清理: ${r.cleanupSuccess ? '成功' : '否'}`);
    }
  });
  
  process.exit(failed > 0 ? 1 : 0);
}

runTests().catch(error => {
  console.error('测试执行失败:', error);
  process.exit(1);
});