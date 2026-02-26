/**
 * 性能测试 - URL模式分析器
 * 
 * 测试目标：分析1000个URL应在10秒内完成
 */

const URLPatternAnalyzer = require('../lib/url-clusterer');
const fs = require('fs').promises;
const path = require('path');

/**
 * 生成测试URL
 * @param {number} count - URL数量
 * @returns {Array<string>} URL数组
 */
function generateTestURLs(count) {
  const urls = [];
  const patterns = [
    { base: 'https://www.example.com/api/doc', param: 'api-key', values: 50 },
    { base: 'https://www.example.com/analytics/company/dashboard', param: 'id', values: 30 },
    { base: 'https://www.example.com/analytics/index/dashboard', param: 'id', values: 30 },
    { base: 'https://www.example.com/open/data', param: 'type', values: 20 },
    { base: 'https://www.example.com/user/profile', param: 'uid', values: 10 }
  ];
  
  let urlIndex = 0;
  
  // 生成每个模式的URL
  for (const pattern of patterns) {
    const urlsPerPattern = Math.floor(count / patterns.length);
    
    for (let i = 0; i < urlsPerPattern && urlIndex < count; i++) {
      const value = pattern.values > 0 ? i % pattern.values : i;
      const url = `${pattern.base}?${pattern.param}=${value}`;
      urls.push(url);
      urlIndex++;
    }
  }
  
  // 填充剩余的URL
  while (urlIndex < count) {
    const patternIndex = urlIndex % patterns.length;
    const pattern = patterns[patternIndex];
    const value = urlIndex % (pattern.values || 100);
    const url = `${pattern.base}?${pattern.param}=${value}`;
    urls.push(url);
    urlIndex++;
  }
  
  return urls;
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
  console.log('=== URL模式分析器 - 性能测试 ===\n');
  
  const testCases = [
    { name: '小规模测试', urlCount: 100, target: 1000 },
    { name: '中规模测试', urlCount: 500, target: 5000 },
    { name: '大规模测试', urlCount: 1000, target: 10000 },
    { name: '超大规模测试', urlCount: 5000, target: 50000 }
  ];
  
  const results = [];
  
  for (const testCase of testCases) {
    console.log(`\n测试: ${testCase.name}`);
    console.log(`  URL数量: ${testCase.urlCount}`);
    console.log(`  目标时间: ${formatTime(testCase.target)}`);
    console.log('  ---');
    
    // 生成测试数据
    console.log('  生成测试数据...');
    const urls = generateTestURLs(testCase.urlCount);
    console.log(`  ✓ 生成了 ${urls.length} 个URL`);
    
    // 创建分析器实例
    const analyzer = new URLPatternAnalyzer();
    
    // 测试1: 不使用优化（小批次）
    console.log('\n  测试1: 不使用优化（小批次）');
    const start1 = Date.now();
    const clusters1 = analyzer.clusterURLs(urls, { batchSize: 100 });
    const duration1 = Date.now() - start1;
    console.log(`    用时: ${formatTime(duration1)}`);
    console.log(`    识别模式数: ${clusters1.length}`);
    console.log(`    最大簇大小: ${clusters1[0]?.length || 0}`);
    
    // 清除缓存
    analyzer.clearCache();
    
    // 测试2: 使用优化（大批次）
    console.log('\n  测试2: 使用优化（大批次）');
    const start2 = Date.now();
    const clusters2 = analyzer.clusterURLs(urls, { batchSize: 1000 });
    const duration2 = Date.now() - start2;
    console.log(`    用时: ${formatTime(duration2)}`);
    console.log(`    识别模式数: ${clusters2.length}`);
    console.log(`    最大簇大小: ${clusters2[0]?.length || 0}`);
    
    // 计算性能提升
    const improvement = ((duration1 - duration2) / duration1 * 100).toFixed(1);
    const speedup = (duration1 / duration2).toFixed(2);
    
    console.log(`\n  性能对比:`);
    console.log(`    提升: ${improvement}%`);
    console.log(`    加速比: ${speedup}x`);
    console.log(`    是否达标: ${duration2 <= testCase.target ? '✓ 是' : '✗ 否'}`);
    
    // 测试3: 测试缓存效果
    console.log('\n  测试3: 测试缓存效果（重复分析）');
    const start3 = Date.now();
    const clusters3 = analyzer.clusterURLs(urls, { batchSize: 1000 });
    const duration3 = Date.now() - start3;
    console.log(`    用时: ${formatTime(duration3)}`);
    console.log(`    缓存加速比: ${(duration2 / duration3).toFixed(2)}x`);
    
    // 记录结果
    results.push({
      name: testCase.name,
      urlCount: testCase.urlCount,
      target: testCase.target,
      smallBatch: duration1,
      largeBatch: duration2,
      withCache: duration3,
      improvement: parseFloat(improvement),
      speedup: parseFloat(speedup),
      cacheSpeedup: parseFloat((duration2 / duration3).toFixed(2)),
      passed: duration2 <= testCase.target
    });
  }
  
  // 生成总结报告
  console.log('\n\n=== 性能测试总结 ===\n');
  console.log('| 测试名称 | URL数 | 目标时间 | 小批次 | 大批次 | 缓存 | 提升 | 加速比 | 缓存加速 | 结果 |');
  console.log('|----------|-------|----------|--------|--------|------|------|--------|----------|------|');
  
  results.forEach(result => {
    const passed = result.passed ? '✓ 通过' : '✗ 未通过';
    console.log(
      `| ${result.name} | ${result.urlCount} | ${formatTime(result.target)} | ` +
      `${formatTime(result.smallBatch)} | ${formatTime(result.largeBatch)} | ` +
      `${formatTime(result.withCache)} | ${result.improvement}% | ` +
      `${result.speedup}x | ${result.cacheSpeedup}x | ${passed} |`
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

module.exports = { runPerformanceTest, generateTestURLs };
