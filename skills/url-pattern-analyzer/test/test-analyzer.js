/**
 * URL Pattern Analyzer - 测试脚本
 */

const URLPatternAnalyzer = require('../lib/url-clusterer');

// 创建分析器实例
const analyzer = new URLPatternAnalyzer();

console.log('=== URL Pattern Analyzer 测试 ===\n');

// 测试1: 提取URL特征
console.log('测试1: 提取URL特征');
console.log('-------------------');

const testUrls = [
  'https://www.lixinger.com/open/api/doc?api-key=cn/company',
  'https://www.lixinger.com/open/api/doc?api-key=hk/index',
  'https://www.lixinger.com/analytics/company/dashboard',
  'https://www.lixinger.com/analytics/index/dashboard?type=cn'
];

testUrls.forEach(url => {
  console.log(`\nURL: ${url}`);
  const features = analyzer.extractFeatures(url);
  console.log('特征:', JSON.stringify(features, null, 2));
});

// 测试2: 计算URL相似度
console.log('\n\n测试2: 计算URL相似度');
console.log('-------------------');

const pairs = [
  [testUrls[0], testUrls[1]], // 相同路径，不同参数值
  [testUrls[0], testUrls[2]], // 不同路径
  [testUrls[2], testUrls[3]], // 相似路径，不同参数
];

pairs.forEach(([url1, url2]) => {
  const similarity = analyzer.calculateSimilarity(url1, url2);
  console.log(`\nURL1: ${url1}`);
  console.log(`URL2: ${url2}`);
  console.log(`相似度分数: ${similarity}`);
});

// 测试3: URL聚类
console.log('\n\n测试3: URL聚类');
console.log('-------------------');

const clusterTestUrls = [
  // API文档组 (应该聚在一起)
  'https://www.lixinger.com/open/api/doc?api-key=cn/company',
  'https://www.lixinger.com/open/api/doc?api-key=hk/index',
  'https://www.lixinger.com/open/api/doc?api-key=us/stock',
  'https://www.lixinger.com/open/api/doc?api-key=cn/index',
  
  // Dashboard组 (应该聚在一起)
  'https://www.lixinger.com/analytics/company/dashboard',
  'https://www.lixinger.com/analytics/index/dashboard',
  'https://www.lixinger.com/analytics/stock/dashboard',
  
  // 用户组 (应该聚在一起)
  'https://www.lixinger.com/user/profile',
  'https://www.lixinger.com/user/settings',
  
  // 独立URL (应该各自成簇)
  'https://www.lixinger.com/about',
  'https://www.lixinger.com/contact'
];

console.log(`\n输入URL数量: ${clusterTestUrls.length}`);
console.log('\n开始聚类...');

const clusters = analyzer.clusterURLs(clusterTestUrls);

console.log(`\n聚类结果: ${clusters.length} 个簇\n`);

clusters.forEach((cluster, index) => {
  console.log(`簇 ${index + 1} (${cluster.length} 个URL):`);
  cluster.forEach(url => {
    console.log(`  - ${url}`);
  });
  console.log('');
});

// 测试4: 生成正则表达式
console.log('\n\n测试4: 生成正则表达式');
console.log('-------------------');

console.log('\n为每个簇生成正则表达式模式:\n');

clusters.forEach((cluster, index) => {
  console.log(`簇 ${index + 1}:`);
  
  try {
    const pattern = analyzer.generatePattern(cluster);
    console.log(`  路径模板: ${pattern.pathTemplate}`);
    console.log(`  正则表达式: ${pattern.pattern}`);
    console.log(`  查询参数: [${pattern.queryParams.join(', ')}]`);
    
    // 验证正则表达式是否匹配所有URL
    const regex = new RegExp(pattern.pattern);
    const allMatch = cluster.every(url => regex.test(url));
    console.log(`  验证: ${allMatch ? '✓ 所有URL匹配' : '✗ 部分URL不匹配'}`);
  } catch (error) {
    console.log(`  错误: ${error.message}`);
  }
  
  console.log('');
});

console.log('\n=== 测试完成 ===');
