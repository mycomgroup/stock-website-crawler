#!/usr/bin/env node
/**
 * 测试URL正则匹配和后端渲染判断
 * 
 * 验证生成的URL模式能够正确匹配对应的URL
 */

const fs = require('fs');
const path = require('path');

async function testURLMatching() {
  console.log('=== 测试URL正则匹配 ===\n');
  
  // 1. 加载URL模式
  const patternsPath = path.join(__dirname, '../../../stock-crawler/output/lixinger-crawler/url-patterns.json');
  const patternsData = JSON.parse(fs.readFileSync(patternsPath, 'utf-8'));
  const patterns = patternsData.patterns;
  
  console.log(`加载了 ${patterns.length} 个URL模式\n`);
  
  // 2. 测试每个模式
  let totalTests = 0;
  let passedTests = 0;
  
  for (const pattern of patterns) {
    console.log(`\n测试模式: ${pattern.name}`);
    console.log(`路径模板: ${pattern.pathTemplate}`);
    console.log(`正则表达式: ${pattern.pattern}`);
    console.log(`样例URL数: ${pattern.samples.length}`);
    
    // 创建正则表达式对象
    const regex = new RegExp(pattern.pattern);
    
    // 测试样例URL
    let matched = 0;
    for (const url of pattern.samples) {
      totalTests++;
      if (regex.test(url)) {
        matched++;
        passedTests++;
      } else {
        console.log(`  ✗ 未匹配: ${url}`);
      }
    }
    
    const matchRate = (matched / pattern.samples.length * 100).toFixed(1);
    console.log(`  匹配率: ${matched}/${pattern.samples.length} (${matchRate}%)`);
    
    if (matched === pattern.samples.length) {
      console.log(`  ✓ 所有样例URL都匹配成功`);
    } else {
      console.log(`  ⚠ 有 ${pattern.samples.length - matched} 个样例URL未匹配`);
    }
  }
  
  // 3. 总结
  console.log('\n=== 测试总结 ===');
  console.log(`总测试数: ${totalTests}`);
  console.log(`通过测试: ${passedTests}`);
  console.log(`失败测试: ${totalTests - passedTests}`);
  console.log(`通过率: ${(passedTests / totalTests * 100).toFixed(1)}%`);
  
  if (passedTests === totalTests) {
    console.log('\n✓ 所有URL正则匹配测试通过！');
    return true;
  } else {
    console.log('\n⚠ 部分URL正则匹配测试失败');
    return false;
  }
}

// 运行测试
if (require.main === module) {
  testURLMatching()
    .then(success => {
      process.exit(success ? 0 : 1);
    })
    .catch(error => {
      console.error('测试失败:', error);
      process.exit(1);
    });
}

module.exports = { testURLMatching };
