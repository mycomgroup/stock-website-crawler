#!/usr/bin/env node
/**
 * RiceQuant Notebook 边界测试
 * 
 * 专门测试各种边界情况：
 * 1. 极限值测试
 * 2. 并发测试
 * 3. 资源限制测试
 * 4. 特殊字符测试
 */

import { runNotebookTest } from './request/test-ricequant-notebook.js';

const BOUNDARY_TESTS = [
  {
    category: '极限值测试',
    tests: [
      {
        name: '最小代码长度',
        code: 'x=1',
        expected: 'should_pass',
        description: '测试最短的代码片段'
      },
      {
        name: '最大单行长度',
        code: 'print("' + 'A'.repeat(100000) + '")',
        expected: 'should_pass',
        timeout: 60000,
        description: '测试超长单行代码'
      },
      {
        name: '最大变量数量',
        code: Array(10000).fill(0).map((_, i) => `var_${i} = ${i}`).join('\n') + '\nprint("done")',
        expected: 'should_pass',
        timeout: 60000,
        description: '测试大量变量定义'
      },
      {
        name: '深层嵌套循环',
        code: `
result = 0
for i in range(10):
    for j in range(10):
        for k in range(10):
            for l in range(10):
                result += 1
print(f"嵌套循环结果: {result}")
`,
        expected: 'should_pass',
        description: '测试深层嵌套'
      },
      {
        name: '递归深度',
        code: `
import sys
sys.setrecursionlimit(100)

def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

try:
    result = factorial(50)
    print(f"递归结果: {result}")
except RecursionError:
    print("捕获递归深度错误")
`,
        expected: 'should_pass',
        description: '测试递归深度限制'
      }
    ]
  },
  {
    category: '数据类型边界',
    tests: [
      {
        name: '最大整数',
        code: `
big_int = 10**100
print(f"最大整数: {big_int}")
print(f"位数: {len(str(big_int))}")
`,
        expected: 'should_pass',
        description: '测试超大整数'
      },
      {
        name: '浮点数精度',
        code: `
import sys
print(f"浮点数最大值: {sys.float_info.max}")
print(f"浮点数最小值: {sys.float_info.min}")
print(f"浮点数精度: {sys.float_info.epsilon}")

a = 0.1 + 0.2
print(f"0.1 + 0.2 = {a}")
print(f"精度误差: {abs(a - 0.3)}")
`,
        expected: 'should_pass',
        description: '测试浮点数精度边界'
      },
      {
        name: '字符串长度',
        code: `
long_str = "A" * 1000000
print(f"字符串长度: {len(long_str)}")
print(f"内存占用: {len(long_str.encode('utf-8'))} bytes")
`,
        expected: 'should_pass',
        timeout: 60000,
        description: '测试超长字符串'
      },
      {
        name: '列表大小',
        code: `
import sys
big_list = list(range(100000))
print(f"列表长度: {len(big_list)}")
print(f"内存占用: {sys.getsizeof(big_list)} bytes")
`,
        expected: 'should_pass',
        description: '测试大型列表'
      }
    ]
  },
  {
    category: '特殊字符测试',
    tests: [
      {
        name: '中文字符',
        code: `
print("中文测试")
print("标点符号：，。！？")
print("特殊汉字：龘𪚥")
`,
        expected: 'should_pass',
        description: '测试中文字符处理'
      },
      {
        name: 'Emoji 字符',
        code: `
print("Emoji: 😀 🎉 🚀 ❤️")
print("组合Emoji: 👨‍👩‍👧‍👦 🏳️‍🌈")
`,
        expected: 'should_pass',
        description: '测试Emoji字符'
      },
      {
        name: '控制字符',
        code: `
print("换行:\\n制表:\\t回车:\\r")
print("转义字符:\\\\ \\' \\\"")
`,
        expected: 'should_pass',
        description: '测试控制字符'
      },
      {
        name: 'Unicode 字符范围',
        code: `
print("Latin: Héllo Wörld")
print("Greek: Αλφα Βητα")
print("Cyrillic: Привет мир")
print("Japanese: こんにちは世界")
print("Korean: 안녕하세요")
print("Arabic: مرحبا بالعالم")
print("Hebrew: שלום עולם")
`,
        expected: 'should_pass',
        description: '测试多种语言Unicode'
      }
    ]
  },
  {
    category: '并发和资源测试',
    tests: [
      {
        name: '文件句柄限制',
        code: `
import os
files = []
try:
    for i in range(100):
        f = open(f'/tmp/test_{i}.txt', 'w')
        files.append(f)
    print(f"成功打开 {len(files)} 个文件")
finally:
    for f in files:
        f.close()
    print("文件句柄已清理")
`,
        expected: 'should_pass',
        description: '测试文件句柄管理'
      },
      {
        name: '内存分配',
        code: `
import sys
data = []
for i in range(10):
    chunk = [0] * 100000
    data.append(chunk)
    print(f"分配 {i+1}/10, 内存: {sys.getsizeof(data)} bytes")
print("内存分配测试完成")
`,
        expected: 'should_pass',
        description: '测试内存分配'
      },
      {
        name: 'CPU 密集计算',
        code: `
import time
start = time.time()
result = sum(i**2 for i in range(100000))
end = time.time()
print(f"计算结果: {result}")
print(f"耗时: {end-start:.3f}秒")
`,
        expected: 'should_pass',
        timeout: 60000,
        description: '测试CPU密集型任务'
      }
    ]
  },
  {
    category: '错误边界测试',
    tests: [
      {
        name: '内存错误捕获',
        code: `
try:
    # 尝试分配超大内存
    big = [0] * 10**9
except MemoryError:
    print("成功捕获内存错误")
except Exception as e:
    print(f"其他错误: {type(e).__name__}")
`,
        expected: 'should_pass',
        description: '测试内存错误处理'
      },
      {
        name: '栈溢出捕获',
        code: `
import sys
sys.setrecursionlimit(100)

def deep_recursion(n):
    if n == 0:
        return 0
    return deep_recursion(n - 1) + 1

try:
    result = deep_recursion(1000)
    print(f"结果: {result}")
except RecursionError:
    print("成功捕获栈溢出错误")
`,
        expected: 'should_pass',
        description: '测试栈溢出处理'
      },
      {
        name: '键盘中断模拟',
        code: `
try:
    # 模拟键盘中断
    raise KeyboardInterrupt()
except KeyboardInterrupt:
    print("成功捕获键盘中断")
`,
        expected: 'should_pass',
        description: '测试键盘中断处理'
      }
    ]
  }
];

async function runBoundaryTests() {
  console.log('\n' + '='.repeat(80));
  console.log('RiceQuant Notebook 边界测试套件');
  console.log('='.repeat(80) + '\n');
  
  const results = {
    total: 0,
    passed: 0,
    failed: 0,
    tests: []
  };
  
  for (const category of BOUNDARY_TESTS) {
    console.log(`\n${category.category}`);
    console.log('-'.repeat(80));
    
    for (const test of category.tests) {
      const startTime = Date.now();
      
      try {
        const result = await runNotebookTest({
          cellSource: test.code,
          timeoutMs: test.timeout || 30000
        });
        
        const duration = Date.now() - startTime;
        const output = result.executions[0]?.textOutput || '';
        
        const passed = result.executions.length > 0;
        
        console.log(`  ${passed ? '✓' : '✗'} ${test.name} (${duration}ms)`);
        console.log(`    描述: ${test.description}`);
        if (output) {
          console.log(`    输出: ${output.trim().split('\n')[0]}`);
        }
        
        results.total++;
        if (passed) results.passed++;
        else results.failed++;
        
        results.tests.push({
          category: category.category,
          name: test.name,
          description: test.description,
          status: passed ? 'passed' : 'failed',
          duration,
          output: output.trim()
        });
        
      } catch (error) {
        const duration = Date.now() - startTime;
        const expectedToFail = test.expected === 'should_fail';
        const passed = expectedToFail;
        
        console.log(`  ${passed ? '✓' : '✗'} ${test.name} (${duration}ms)`);
        console.log(`    描述: ${test.description}`);
        console.log(`    错误: ${error.message}`);
        
        results.total++;
        if (passed) results.passed++;
        else results.failed++;
        
        results.tests.push({
          category: category.category,
          name: test.name,
          description: test.description,
          status: passed ? 'passed' : 'failed',
          duration,
          error: error.message
        });
      }
      
      await new Promise(resolve => setTimeout(resolve, 300));
    }
  }
  
  console.log('\n' + '='.repeat(80));
  console.log('边界测试汇总');
  console.log('='.repeat(80));
  console.log(`\n总计: ${results.total} 个测试`);
  console.log(`通过: ${results.passed} 个`);
  console.log(`失败: ${results.failed} 个`);
  console.log(`通过率: ${(results.passed / results.total * 100).toFixed(1)}%`);
  
  if (results.failed > 0) {
    console.log('\n失败的测试:');
    results.tests.filter(t => t.status === 'failed').forEach(t => {
      console.log(`  - [${t.category}] ${t.name}`);
      console.log(`    ${t.description}`);
    });
  }
  
  const fs = await import('fs');
  const reportFile = `./data/boundary-test-report-${Date.now()}.json`;
  fs.writeFileSync(reportFile, JSON.stringify(results, null, 2));
  console.log(`\n测试报告: ${reportFile}`);
  
  process.exit(results.failed > 0 ? 1 : 0);
}

runBoundaryTests().catch(error => {
  console.error('测试执行失败:', error);
  process.exit(1);
});