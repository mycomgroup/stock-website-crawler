#!/usr/bin/env node
/**
 * RiceQuant Notebook 全面测试套件
 * 
 * 测试范围：
 * 1. Session 管理测试
 * 2. Notebook 创建/删除测试
 * 3. 代码执行测试
 * 4. 边界情况测试
 * 5. 错误处理测试
 * 6. 性能测试
 */

import { runNotebookTest } from './request/test-ricequant-notebook.js';
import { RiceQuantNotebookClient } from './request/ricequant-notebook-client.js';
import { ensureRiceQuantNotebookSession } from './request/ensure-ricequant-notebook-session.js';
import fs from 'node:fs';
import path from 'node:path';

const TEST_SUITE = {
  SESSION: {
    name: 'Session 管理测试',
    tests: []
  },
  NOTEBOOK: {
    name: 'Notebook 创建/删除测试',
    tests: []
  },
  EXECUTION: {
    name: '代码执行测试',
    tests: []
  },
  BOUNDARY: {
    name: '边界情况测试',
    tests: []
  },
  ERROR: {
    name: '错误处理测试',
    tests: []
  }
};

const results = {
  total: 0,
  passed: 0,
  failed: 0,
  skipped: 0,
  tests: []
};

function log(message, type = 'info') {
  const colors = {
    info: '\x1b[36m',
    success: '\x1b[32m',
    error: '\x1b[31m',
    warning: '\x1b[33m',
    reset: '\x1b[0m'
  };
  console.log(`${colors[type]}${message}${colors.reset}`);
}

function logTest(category, testName, status, duration, details = {}) {
  const statusIcon = status === 'passed' ? '✓' : status === 'failed' ? '✗' : '○';
  const statusColor = status === 'passed' ? 'success' : status === 'failed' ? 'error' : 'warning';
  
  log(`  ${statusIcon} ${testName} (${duration}ms)`, statusColor);
  
  if (details.error) {
    log(`    错误: ${details.error}`, 'error');
  }
  if (details.output) {
    log(`    输出: ${details.output}`, 'info');
  }
  
  results.total++;
  if (status === 'passed') results.passed++;
  else if (status === 'failed') results.failed++;
  else results.skipped++;
  
  results.tests.push({
    category,
    name: testName,
    status,
    duration,
    ...details
  });
}

// ==================== Session 管理测试 ====================

TEST_SUITE.SESSION.tests = [
  {
    name: '检查现有 session 文件',
    async run() {
      const sessionFile = './data/session.json';
      const exists = fs.existsSync(sessionFile);
      
      if (exists) {
        const stats = fs.statSync(sessionFile);
        const sizeKB = Math.round(stats.size / 1024);
        return {
          passed: true,
          details: { output: `文件存在，大小: ${sizeKB}KB` }
        };
      } else {
        return {
          passed: true,
          details: { output: '文件不存在（首次运行）' }
        };
      }
    }
  },
  {
    name: '验证 session 有效性',
    async run() {
      try {
        const notebookUrl = process.env.RICEQUANT_NOTEBOOK_URL;
        if (!notebookUrl) {
          return {
            passed: false,
            details: { error: '缺少 RICEQUANT_NOTEBOOK_URL 环境变量' }
          };
        }
        
        const result = await ensureRiceQuantNotebookSession({
          notebookUrl,
          headless: true
        });
        
        return {
          passed: result.refreshed !== undefined,
          details: { 
            output: `Session 状态: ${result.refreshed ? '新建' : '复用'}` 
          }
        };
      } catch (error) {
        return {
          passed: false,
          details: { error: error.message }
        };
      }
    }
  },
  {
    name: '测试 session 过期检测',
    async run() {
      const sessionFile = './data/session.json';
      
      if (!fs.existsSync(sessionFile)) {
        return {
          passed: true,
          details: { output: '无 session 文件，跳过测试' }
        };
      }
      
      const sessionData = JSON.parse(fs.readFileSync(sessionFile, 'utf8'));
      const capturedAt = new Date(sessionData.capturedAt);
      const now = new Date();
      const hoursSinceCapture = (now - capturedAt) / (1000 * 60 * 60);
      const daysSinceCapture = Math.floor(hoursSinceCapture / 24);
      
      const isExpired = hoursSinceCapture > 24 * 7;
      
      return {
        passed: true,
        details: { 
          output: `Session 年龄: ${daysSinceCapture}天 (${isExpired ? '已过期' : '有效'})` 
        }
      };
    }
  },
  {
    name: '测试 cookies 完整性',
    async run() {
      const sessionFile = './data/session.json';
      
      if (!fs.existsSync(sessionFile)) {
        return {
          passed: true,
          details: { output: '无 session 文件，跳过测试' }
        };
      }
      
      const sessionData = JSON.parse(fs.readFileSync(sessionFile, 'utf8'));
      const cookies = sessionData.cookies || [];
      const requiredCookies = ['session', 'RQSESSION'];
      
      const hasRequired = requiredCookies.some(name => 
        cookies.some(c => c.name === name)
      );
      
      return {
        passed: cookies.length >= 2 && hasRequired,
        details: { 
          output: `Cookies 数量: ${cookies.length}, 包含必需: ${hasRequired}` 
        }
      };
    }
  }
];

// ==================== Notebook 创建/删除测试 ====================

TEST_SUITE.NOTEBOOK.tests = [
  {
    name: '创建独立 notebook',
    async run() {
      try {
        const result = await runNotebookTest({
          cellSource: 'print("测试创建独立 notebook")',
          createNew: true,
          cleanup: false,
          timeoutMs: 30000
        });
        
        return {
          passed: result.newNotebookCreated === true,
          details: { 
            output: `Notebook: ${result.notebookPath}` 
          }
        };
      } catch (error) {
        return {
          passed: false,
          details: { error: error.message }
        };
      }
    }
  },
  {
    name: '创建并自动清理 notebook',
    async run() {
      try {
        const result = await runNotebookTest({
          cellSource: 'print("测试自动清理")',
          createNew: true,
          cleanup: true,
          timeoutMs: 30000
        });
        
        const cleanupSuccess = result.cleanupResult?.success === true;
        
        return {
          passed: result.newNotebookCreated && cleanupSuccess,
          details: { 
            output: `创建: ${result.newNotebookCreated}, 清理: ${cleanupSuccess}` 
          }
        };
      } catch (error) {
        return {
          passed: false,
          details: { error: error.message }
        };
      }
    }
  },
  {
    name: '生成唯一 notebook 名称',
    async run() {
      const notebookUrl = process.env.RICEQUANT_NOTEBOOK_URL;
      const client = new RiceQuantNotebookClient({ notebookUrl });
      
      const name1 = client.generateUniqueNotebookName('test');
      const name2 = client.generateUniqueNotebookName('test');
      
      const isUnique = name1 !== name2;
      const isValidFormat = /^test_\d+_[a-z0-9]+\.ipynb$/.test(name1);
      
      return {
        passed: isUnique && isValidFormat,
        details: { 
          output: `名称1: ${name1}, 名称2: ${name2}` 
        }
      };
    }
  }
];

// ==================== 代码执行测试 ====================

TEST_SUITE.EXECUTION.tests = [
  {
    name: '简单 print 语句',
    async run() {
      try {
        const result = await runNotebookTest({
          cellSource: 'print("Hello, RiceQuant!")',
          timeoutMs: 30000
        });
        
        const output = result.executions[0]?.textOutput || '';
        
        return {
          passed: output.includes('Hello, RiceQuant!'),
          details: { output: `输出: ${output.trim()}` }
        };
      } catch (error) {
        return {
          passed: false,
          details: { error: error.message }
        };
      }
    }
  },
  {
    name: '多行代码执行',
    async run() {
      const code = `
import datetime
date = datetime.datetime.now()
print(f"当前时间: {date}")
print("多行代码测试成功")
`;
      try {
        const result = await runNotebookTest({
          cellSource: code,
          timeoutMs: 30000
        });
        
        const output = result.executions[0]?.textOutput || '';
        
        return {
          passed: output.includes('当前时间') && output.includes('测试成功'),
          details: { output: `输出: ${output.trim()}` }
        };
      } catch (error) {
        return {
          passed: false,
          details: { error: error.message }
        };
      }
    }
  },
  {
    name: '计算任务',
    async run() {
      const code = `
result = 0
for i in range(100):
    result += i
print(f"计算结果: {result}")
`;
      try {
        const result = await runNotebookTest({
          cellSource: code,
          timeoutMs: 30000
        });
        
        const output = result.executions[0]?.textOutput || '';
        
        return {
          passed: output.includes('计算结果: 4950'),
          details: { output: `输出: ${output.trim()}` }
        };
      } catch (error) {
        return {
          passed: false,
          details: { error: error.message }
        };
      }
    }
  },
  {
    name: '执行策略文件',
    async run() {
      try {
        const result = await runNotebookTest({
          strategy: 'examples/simple_backtest.py',
          timeoutMs: 60000
        });
        
        const output = result.executions[0]?.textOutput || '';
        
        return {
          passed: result.executions.length > 0,
          details: { output: `执行了 ${result.executions.length} 个 cell` }
        };
      } catch (error) {
        return {
          passed: false,
          details: { error: error.message }
        };
      }
    }
  }
];

// ==================== 边界情况测试 ====================

TEST_SUITE.BOUNDARY.tests = [
  {
    name: '空代码执行',
    async run() {
      try {
        const result = await runNotebookTest({
          cellSource: '',
          timeoutMs: 30000
        });
        
        return {
          passed: true,
          details: { output: '空代码执行成功' }
        };
      } catch (error) {
        return {
          passed: false,
          details: { error: error.message }
        };
      }
    }
  },
  {
    name: '超长代码执行',
    async run() {
      const longCode = 'print("' + 'A'.repeat(10000) + '")';
      
      try {
        const result = await runNotebookTest({
          cellSource: longCode,
          timeoutMs: 60000
        });
        
        return {
          passed: true,
          details: { output: '超长代码执行成功' }
        };
      } catch (error) {
        return {
          passed: false,
          details: { error: error.message }
        };
      }
    }
  },
  {
    name: 'Unicode 字符处理',
    async run() {
      const code = `
print("中文测试：你好世界")
print("Emoji测试：😀🎉")
print("特殊字符：@#￥%……&*（）")
`;
      try {
        const result = await runNotebookTest({
          cellSource: code,
          timeoutMs: 30000
        });
        
        const output = result.executions[0]?.textOutput || '';
        
        return {
          passed: output.includes('中文') || output.includes('Emoji'),
          details: { output: `输出: ${output.trim()}` }
        };
      } catch (error) {
        return {
          passed: false,
          details: { error: error.message }
        };
      }
    }
  },
  {
    name: '超时设置测试',
    async run() {
      const code = `
import time
start = time.time()
time.sleep(2)
end = time.time()
print(f"耗时: {end-start:.2f}秒")
`;
      try {
        const result = await runNotebookTest({
          cellSource: code,
          timeoutMs: 10000
        });
        
        const output = result.executions[0]?.textOutput || '';
        
        return {
          passed: output.includes('耗时'),
          details: { output: `输出: ${output.trim()}` }
        };
      } catch (error) {
        return {
          passed: false,
          details: { error: error.message }
        };
      }
    }
  },
  {
    name: '内存使用测试',
    async run() {
      const code = `
import sys
data = [i for i in range(100000)]
print(f"列表长度: {len(data)}")
print(f"内存占用: {sys.getsizeof(data)} bytes")
`;
      try {
        const result = await runNotebookTest({
          cellSource: code,
          timeoutMs: 30000
        });
        
        const output = result.executions[0]?.textOutput || '';
        
        return {
          passed: output.includes('列表长度: 100000'),
          details: { output: `输出: ${output.trim()}` }
        };
      } catch (error) {
        return {
          passed: false,
          details: { error: error.message }
        };
      }
    }
  }
];

// ==================== 错误处理测试 ====================

TEST_SUITE.ERROR.tests = [
  {
    name: '语法错误处理',
    async run() {
      const code = 'print("missing parenthesis"';
      
      try {
        const result = await runNotebookTest({
          cellSource: code,
          timeoutMs: 30000
        });
        
        const outputs = result.executions[0]?.outputs || [];
        const hasError = outputs.some(o => o.output_type === 'error');
        
        return {
          passed: hasError,
          details: { output: '成功捕获语法错误' }
        };
      } catch (error) {
        return {
          passed: false,
          details: { error: error.message }
        };
      }
    }
  },
  {
    name: '运行时错误处理',
    async run() {
      const code = `
x = 10
y = 0
z = x / y
`;
      try {
        const result = await runNotebookTest({
          cellSource: code,
          timeoutMs: 30000
        });
        
        const outputs = result.executions[0]?.outputs || [];
        const hasError = outputs.some(o => 
          o.output_type === 'error' && o.ename === 'ZeroDivisionError'
        );
        
        return {
          passed: hasError,
          details: { output: '成功捕获除零错误' }
        };
      } catch (error) {
        return {
          passed: false,
          details: { error: error.message }
        };
      }
    }
  },
  {
    name: 'Import 错误处理',
    async run() {
      const code = 'import nonexistent_module';
      
      try {
        const result = await runNotebookTest({
          cellSource: code,
          timeoutMs: 30000
        });
        
        const outputs = result.executions[0]?.outputs || [];
        const hasError = outputs.some(o => 
          o.output_type === 'error' && o.ename === 'ModuleNotFoundError'
        );
        
        return {
          passed: hasError,
          details: { output: '成功捕获模块导入错误' }
        };
      } catch (error) {
        return {
          passed: false,
          details: { error: error.message }
        };
      }
    }
  },
  {
    name: '超时错误处理',
    async run() {
      const code = `
import time
while True:
    time.sleep(1)
`;
      try {
        const result = await runNotebookTest({
          cellSource: code,
          timeoutMs: 5000
        });
        
        return {
          passed: false,
          details: { error: '应该超时但没有' }
        };
      } catch (error) {
        const isTimeoutError = error.message.includes('超时') || 
                              error.message.includes('timeout');
        
        return {
          passed: isTimeoutError,
          details: { output: '成功捕获超时错误' }
        };
      }
    }
  },
  {
    name: '不存在的策略文件',
    async run() {
      try {
        const result = await runNotebookTest({
          strategy: 'nonexistent_file.py',
          timeoutMs: 30000
        });
        
        return {
          passed: false,
          details: { error: '应该失败但没有' }
        };
      } catch (error) {
        return {
          passed: error.message.includes('不存在') || error.message.includes('not found'),
          details: { output: '成功捕获文件不存在错误' }
        };
      }
    }
  },
  {
    name: '无效的 notebook URL',
    async run() {
      try {
        const result = await runNotebookTest({
          notebookUrl: 'https://invalid-url.com',
          cellSource: 'print("test")',
          timeoutMs: 10000
        });
        
        return {
          passed: false,
          details: { error: '应该失败但没有' }
        };
      } catch (error) {
        return {
          passed: true,
          details: { output: '成功捕获无效URL错误' }
        };
      }
    }
  }
];

// ==================== 运行测试套件 ====================

async function runTestSuite() {
  log('\n' + '='.repeat(60), 'info');
  log('RiceQuant Notebook 全面测试套件', 'info');
  log('='.repeat(60) + '\n', 'info');
  
  for (const [category, suite] of Object.entries(TEST_SUITE)) {
    log(`\n${suite.name}`, 'info');
    log('-'.repeat(60), 'info');
    
    for (const test of suite.tests) {
      const startTime = Date.now();
      
      try {
        const result = await test.run();
        const duration = Date.now() - startTime;
        
        logTest(category, test.name, result.passed ? 'passed' : 'failed', duration, result.details);
        
      } catch (error) {
        const duration = Date.now() - startTime;
        logTest(category, test.name, 'failed', duration, { error: error.message });
      }
      
      await new Promise(resolve => setTimeout(resolve, 500));
    }
  }
  
  log('\n' + '='.repeat(60), 'info');
  log('测试汇总', 'info');
  log('='.repeat(60), 'info');
  
  log(`\n总计: ${results.total} 个测试`, 'info');
  log(`通过: ${results.passed} 个`, 'success');
  log(`失败: ${results.failed} 个`, results.failed > 0 ? 'error' : 'info');
  log(`跳过: ${results.skipped} 个`, 'warning');
  
  const passRate = (results.passed / results.total * 100).toFixed(1);
  log(`\n通过率: ${passRate}%`, passRate >= 80 ? 'success' : passRate >= 60 ? 'warning' : 'error');
  
  if (results.failed > 0) {
    log('\n失败的测试:', 'error');
    results.tests
      .filter(t => t.status === 'failed')
      .forEach(t => {
        log(`  - [${t.category}] ${t.name}`, 'error');
        if (t.error) log(`    ${t.error}`, 'error');
      });
  }
  
  const reportFile = `./data/test-report-${Date.now()}.json`;
  fs.writeFileSync(reportFile, JSON.stringify(results, null, 2));
  log(`\n测试报告已保存: ${reportFile}`, 'info');
  
  process.exit(results.failed > 0 ? 1 : 0);
}

runTestSuite().catch(error => {
  log(`\n测试套件执行失败: ${error.message}`, 'error');
  console.error(error);
  process.exit(1);
});