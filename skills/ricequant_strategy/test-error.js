#!/usr/bin/env node
/**
 * RiceQuant Notebook 错误场景测试
 * 
 * 专门测试各种错误场景：
 * 1. 语法错误
 * 2. 运行时错误
 * 3. 网络错误
 * 4. 权限错误
 * 5. 资源错误
 */

import { runNotebookTest } from './request/test-ricequant-notebook.js';
import { RiceQuantNotebookClient } from './request/ricequant-notebook-client.js';
import { ensureRiceQuantNotebookSession } from './request/ensure-ricequant-notebook-session.js';

const ERROR_SCENARIOS = [
  {
    category: 'Python 语法错误',
    tests: [
      {
        name: '缺少括号',
        code: 'print("missing parenthesis"',
        expectedError: 'SyntaxError',
        description: '测试语法错误捕获'
      },
      {
        name: '缺少引号',
        code: 'print("missing quote)',
        expectedError: 'SyntaxError',
        description: '测试字符串语法错误'
      },
      {
        name: '错误缩进',
        code: `
if True:
x = 1
`,
        expectedError: 'IndentationError',
        description: '测试缩进错误'
      },
      {
        name: '无效语法',
        code: 'if if else',
        expectedError: 'SyntaxError',
        description: '测试无效语法'
      },
      {
        name: '未定义变量',
        code: 'print(undefined_variable)',
        expectedError: 'NameError',
        description: '测试未定义变量错误'
      }
    ]
  },
  {
    category: 'Python 运行时错误',
    tests: [
      {
        name: '除零错误',
        code: 'x = 10 / 0',
        expectedError: 'ZeroDivisionError',
        description: '测试除零错误'
      },
      {
        name: '类型错误',
        code: 'x = "string" + 10',
        expectedError: 'TypeError',
        description: '测试类型错误'
      },
      {
        name: '索引错误',
        code: 'x = [1, 2, 3][10]',
        expectedError: 'IndexError',
        description: '测试索引越界错误'
      },
      {
        name: '键错误',
        code: 'x = {"a": 1}["b"]',
        expectedError: 'KeyError',
        description: '测试字典键错误'
      },
      {
        name: '属性错误',
        code: 'x = 123.append(4)',
        expectedError: 'AttributeError',
        description: '测试属性错误'
      },
      {
        name: '值错误',
        code: 'int("not a number")',
        expectedError: 'ValueError',
        description: '测试值转换错误'
      },
      {
        name: '导入错误',
        code: 'import nonexistent_module',
        expectedError: 'ModuleNotFoundError',
        description: '测试模块导入错误'
      },
      {
        name: '文件错误',
        code: 'open("/nonexistent/file.txt")',
        expectedError: 'FileNotFoundError',
        description: '测试文件不存在错误'
      }
    ]
  },
  {
    category: '自定义异常',
    tests: [
      {
        name: '抛出异常',
        code: `
raise Exception("自定义错误消息")
`,
        expectedError: 'Exception',
        description: '测试自定义异常'
      },
      {
        name: '断言错误',
        code: 'assert False, "断言失败"',
        expectedError: 'AssertionError',
        description: '测试断言错误'
      },
      {
        name: '自定义异常类',
        code: `
class MyError(Exception):
    pass

raise MyError("自定义异常类")
`,
        expectedError: 'MyError',
        description: '测试自定义异常类'
      }
    ]
  },
  {
    category: '错误恢复测试',
    tests: [
      {
        name: 'Try-Except 捕获',
        code: `
try:
    x = 10 / 0
except ZeroDivisionError:
    print("成功捕获除零错误")
    x = 0
print(f"结果: {x}")
`,
        expectedError: null,
        description: '测试错误捕获和恢复'
      },
      {
        name: '多重异常捕获',
        code: `
errors = []
for test in [
    lambda: 10/0,
    lambda: "a" + 1,
    lambda: [1][5]
]:
    try:
        test()
    except Exception as e:
        errors.append(type(e).__name__)

print(f"捕获的错误: {', '.join(errors)}")
`,
        expectedError: null,
        description: '测试多重异常捕获'
      },
      {
        name: 'Finally 执行',
        code: `
result = None
try:
    result = 10 / 0
except ZeroDivisionError:
    result = "error"
finally:
    print("Finally 块已执行")
print(f"结果: {result}")
`,
        expectedError: null,
        description: '测试Finally块执行'
      }
    ]
  },
  {
    category: '系统和环境错误',
    tests: [
      {
        name: '键盘中断',
        code: `
try:
    raise KeyboardInterrupt()
except KeyboardInterrupt:
    print("成功捕获键盘中断")
`,
        expectedError: null,
        description: '测试键盘中断处理'
      },
      {
        name: '系统退出',
        code: `
import sys
try:
    sys.exit(1)
except SystemExit:
    print("成功捕获系统退出")
`,
        expectedError: null,
        description: '测试系统退出处理'
      },
      {
        name: '内存错误',
        code: `
try:
    # 尝试分配超大内存
    big = [0] * (10**10)
except MemoryError:
    print("成功捕获内存错误")
except Exception as e:
    print(f"其他错误: {type(e).__name__}")
`,
        expectedError: null,
        description: '测试内存错误处理'
      }
    ]
  },
  {
    category: 'API 和网络错误',
    tests: [
      {
        name: '无效 Notebook URL',
        async test() {
          try {
            await runNotebookTest({
              notebookUrl: 'https://invalid-url-12345.com',
              cellSource: 'print("test")',
              timeoutMs: 5000
            });
            return { passed: false, error: '应该失败但没有' };
          } catch (error) {
            return { passed: true, output: '成功捕获无效URL错误' };
          }
        },
        description: '测试无效URL错误'
      },
      {
        name: '超时错误',
        code: `
import time
while True:
    time.sleep(1)
`,
        timeout: 3000,
        expectedError: 'timeout',
        description: '测试执行超时'
      },
      {
        name: '不存在的策略文件',
        async test() {
          try {
            await runNotebookTest({
              strategy: '/nonexistent/file.py',
              timeoutMs: 5000
            });
            return { passed: false, error: '应该失败但没有' };
          } catch (error) {
            return { passed: true, output: '成功捕获文件不存在错误' };
          }
        },
        description: '测试文件不存在错误'
      }
    ]
  }
];

async function runErrorTests() {
  console.log('\n' + '='.repeat(80));
  console.log('RiceQuant Notebook 错误场景测试');
  console.log('='.repeat(80) + '\n');
  
  const results = {
    total: 0,
    passed: 0,
    failed: 0,
    tests: []
  };
  
  for (const category of ERROR_SCENARIOS) {
    console.log(`\n${category.category}`);
    console.log('-'.repeat(80));
    
    for (const test of category.tests) {
      const startTime = Date.now();
      
      try {
        let result;
        
        if (test.test) {
          result = await test.test();
        } else {
          const runResult = await runNotebookTest({
            cellSource: test.code,
            timeoutMs: test.timeout || 30000
          });
          
          const outputs = runResult.executions[0]?.outputs || [];
          const errorOutput = outputs.find(o => o.output_type === 'error');
          
          if (test.expectedError) {
            const hasExpectedError = errorOutput && 
              (errorOutput.ename === test.expectedError || 
               errorOutput.ename.includes(test.expectedError));
            result = {
              passed: hasExpectedError,
              output: hasExpectedError ? 
                `成功捕获 ${errorOutput.ename}` : 
                `未捕获预期的 ${test.expectedError}`
            };
          } else {
            result = {
              passed: runResult.executions.length > 0,
              output: runResult.executions[0]?.textOutput || '执行成功'
            };
          }
        }
        
        const duration = Date.now() - startTime;
        
        console.log(`  ${result.passed ? '✓' : '✗'} ${test.name} (${duration}ms)`);
        console.log(`    描述: ${test.description}`);
        console.log(`    结果: ${result.output || result.error}`);
        
        results.total++;
        if (result.passed) results.passed++;
        else results.failed++;
        
        results.tests.push({
          category: category.category,
          name: test.name,
          description: test.description,
          status: result.passed ? 'passed' : 'failed',
          duration,
          output: result.output,
          error: result.error
        });
        
      } catch (error) {
        const duration = Date.now() - startTime;
        const passed = test.expectedError === 'timeout' && 
          (error.message.includes('超时') || error.message.includes('timeout'));
        
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
  console.log('错误场景测试汇总');
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
      if (t.error) console.log(`    错误: ${t.error}`);
    });
  }
  
  const fs = await import('fs');
  const reportFile = `./data/error-test-report-${Date.now()}.json`;
  fs.writeFileSync(reportFile, JSON.stringify(results, null, 2));
  console.log(`\n测试报告: ${reportFile}`);
  
  process.exit(results.failed > 0 ? 1 : 0);
}

runErrorTests().catch(error => {
  console.error('测试执行失败:', error);
  process.exit(1);
});