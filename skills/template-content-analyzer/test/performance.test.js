/**
 * 性能测试 - 模板内容分析器
 * 
 * 测试目标：分析100个页面应在30秒内完成
 */

const TemplateContentAnalyzer = require('../lib/content-analyzer');
const fs = require('fs').promises;
const path = require('path');

/**
 * 生成测试数据
 * @param {number} count - 页面数量
 * @returns {Array<string>} 页面内容数组
 */
function generateTestPages(count) {
  const pages = [];
  
  for (let i = 0; i < count; i++) {
    const page = `
# API文档 - 测试页面 ${i}

## 简介

这是一个测试API的文档页面。

## 请求URL

\`\`\`
https://api.example.com/v1/test/${i}
\`\`\`

## 请求参数

| 参数名 | 必选 | 类型 | 说明 |
|--------|------|------|------|
| id | 是 | string | 唯一标识符 ${i} |
| name | 否 | string | 名称 |
| type | 否 | string | 类型 |

## 返回示例

\`\`\`json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": "${i}",
    "name": "Test ${i}",
    "value": ${i * 100}
  }
}
\`\`\`

## 返回参数说明

| 参数名 | 类型 | 说明 |
|--------|------|------|
| code | int | 状态码 |
| message | string | 消息 |
| data | object | 数据对象 |

## 备注

- 这是模板内容，每个页面都有
- 请注意参数的必填性
- 返回值可能为null

## 示例代码

\`\`\`javascript
fetch('https://api.example.com/v1/test/${i}')
  .then(res => res.json())
  .then(data => console.log(data));
\`\`\`

## 错误码说明

- 0: 成功
- 1: 参数错误
- 2: 权限不足
- 3: 资源不存在

## 更新日志

- 2024-01-${(i % 28) + 1}: 创建API
`;
    
    pages.push(page);
  }
  
  return pages;
}

/**
 * 格式化时间
 * @param {number} ms - 毫秒数
 * @returns {string} 格式化的时间字符串
 */
function formatTime(ms) {
  if (ms < 1000) {
    return `${ms.toFixed(0)}ms`;
  } else {
    return `${(ms / 1000).toFixed(2)}s`;
  }
}

/**
 * 运行性能测试
 */
async function runPerformanceTest() {
  console.log('=== 模板内容分析器 - 性能测试 ===\n');
  
  const testCases = [
    { name: '小规模测试', pageCount: 10, target: 3000 },
    { name: '中规模测试', pageCount: 50, target: 15000 },
    { name: '大规模测试', pageCount: 100, target: 30000 },
    { name: '超大规模测试', pageCount: 200, target: 60000 }
  ];
  
  const results = [];
  
  for (const testCase of testCases) {
    console.log(`\n测试: ${testCase.name}`);
    console.log(`  页面数量: ${testCase.pageCount}`);
    console.log(`  目标时间: ${formatTime(testCase.target)}`);
    console.log('  ---');
    
    // 生成测试数据
    console.log('  生成测试数据...');
    const pages = generateTestPages(testCase.pageCount);
    console.log(`  ✓ 生成了 ${pages.length} 个页面`);
    
    // 创建分析器实例
    const analyzer = new TemplateContentAnalyzer();
    
    // 测试1: 不使用优化
    console.log('\n  测试1: 不使用优化');
    const start1 = Date.now();
    const result1 = analyzer.analyzeTemplate(pages, {
      thresholds: { template: 0.8, unique: 0.2 },
      parallel: 1 // 禁用并行处理
    });
    const duration1 = Date.now() - start1;
    console.log(`    用时: ${formatTime(duration1)}`);
    console.log(`    总内容块: ${result1.stats.totalBlocks}`);
    console.log(`    模板内容: ${result1.stats.templateBlocks}`);
    console.log(`    独特内容: ${result1.stats.uniqueBlocks}`);
    
    // 清除缓存
    analyzer.clearCache();
    
    // 测试2: 使用优化（并行处理）
    console.log('\n  测试2: 使用优化（并行处理）');
    const start2 = Date.now();
    const result2 = analyzer.analyzeTemplate(pages, {
      thresholds: { template: 0.8, unique: 0.2 },
      parallel: 4 // 启用并行处理
    });
    const duration2 = Date.now() - start2;
    console.log(`    用时: ${formatTime(duration2)}`);
    console.log(`    总内容块: ${result2.stats.totalBlocks}`);
    console.log(`    模板内容: ${result2.stats.templateBlocks}`);
    console.log(`    独特内容: ${result2.stats.uniqueBlocks}`);
    
    // 计算性能提升
    const improvement = ((duration1 - duration2) / duration1 * 100).toFixed(1);
    const speedup = (duration1 / duration2).toFixed(2);
    
    console.log(`\n  性能对比:`);
    console.log(`    提升: ${improvement}%`);
    console.log(`    加速比: ${speedup}x`);
    console.log(`    是否达标: ${duration2 <= testCase.target ? '✓ 是' : '✗ 否'}`);
    
    // 记录结果
    results.push({
      name: testCase.name,
      pageCount: testCase.pageCount,
      target: testCase.target,
      withoutOptimization: duration1,
      withOptimization: duration2,
      improvement: parseFloat(improvement),
      speedup: parseFloat(speedup),
      passed: duration2 <= testCase.target
    });
  }
  
  // 生成总结报告
  console.log('\n\n=== 性能测试总结 ===\n');
  console.log('| 测试名称 | 页面数 | 目标时间 | 无优化 | 有优化 | 提升 | 加速比 | 结果 |');
  console.log('|----------|--------|----------|--------|--------|------|--------|------|');
  
  results.forEach(result => {
    const passed = result.passed ? '✓ 通过' : '✗ 未通过';
    console.log(
      `| ${result.name} | ${result.pageCount} | ${formatTime(result.target)} | ` +
      `${formatTime(result.withoutOptimization)} | ${formatTime(result.withOptimization)} | ` +
      `${result.improvement}% | ${result.speedup}x | ${passed} |`
    );
  });
  
  // 统计通过率
  const passedCount = results.filter(r => r.passed).length;
  const passRate = (passedCount / results.length * 100).toFixed(1);
  
  console.log(`\n通过率: ${passedCount}/${results.length} (${passRate}%)`);
  
  // 保存结果到文件
  const reportPath = path.join(__dirname, '../performance-test-report.json');
  await fs.writeFile(reportPath, JSON.stringify({
    timestamp: new Date().toISOString(),
    results,
    summary: {
      totalTests: results.length,
      passed: passedCount,
      failed: results.length - passedCount,
      passRate: parseFloat(passRate)
    }
  }, null, 2), 'utf-8');
  
  console.log(`\n性能测试报告已保存: ${reportPath}`);
  
  // 返回是否全部通过
  return passedCount === results.length;
}

// 运行测试
if (require.main === module) {
  runPerformanceTest()
    .then(allPassed => {
      if (allPassed) {
        console.log('\n✓ 所有性能测试通过！');
        process.exit(0);
      } else {
        console.log('\n✗ 部分性能测试未通过');
        process.exit(1);
      }
    })
    .catch(error => {
      console.error('\n✗ 性能测试失败:', error);
      process.exit(1);
    });
}

module.exports = { runPerformanceTest, generateTestPages };
