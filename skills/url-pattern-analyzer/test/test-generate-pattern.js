/**
 * 测试 generatePattern() 方法
 */

const URLPatternAnalyzer = require('../lib/url-clusterer');

const analyzer = new URLPatternAnalyzer();

console.log('=== generatePattern() 测试 ===\n');

// 测试1: API文档URL组（相同路径，不同参数值）
console.log('测试1: API文档URL组');
console.log('-------------------');
const apiDocUrls = [
  'https://www.lixinger.com/open/api/doc?api-key=cn/company',
  'https://www.lixinger.com/open/api/doc?api-key=hk/index',
  'https://www.lixinger.com/open/api/doc?api-key=us/stock',
  'https://www.lixinger.com/open/api/doc?api-key=cn/index'
];

console.log('输入URL:');
apiDocUrls.forEach(url => console.log(`  - ${url}`));

const pattern1 = analyzer.generatePattern(apiDocUrls);
console.log('\n生成的模式:');
console.log('  pattern:', pattern1.pattern);
console.log('  pathTemplate:', pattern1.pathTemplate);
console.log('  queryParams:', pattern1.queryParams);

// 验证正则表达式是否匹配所有URL
console.log('\n验证匹配:');
const regex1 = new RegExp(pattern1.pattern);
apiDocUrls.forEach(url => {
  const matches = regex1.test(url);
  console.log(`  ${matches ? '✓' : '✗'} ${url}`);
});

// 测试2: Dashboard URL组（路径中有变化段）
console.log('\n\n测试2: Dashboard URL组');
console.log('-------------------');
const dashboardUrls = [
  'https://www.lixinger.com/analytics/company/dashboard',
  'https://www.lixinger.com/analytics/index/dashboard',
  'https://www.lixinger.com/analytics/stock/dashboard'
];

console.log('输入URL:');
dashboardUrls.forEach(url => console.log(`  - ${url}`));

const pattern2 = analyzer.generatePattern(dashboardUrls);
console.log('\n生成的模式:');
console.log('  pattern:', pattern2.pattern);
console.log('  pathTemplate:', pattern2.pathTemplate);
console.log('  queryParams:', pattern2.queryParams);

// 验证正则表达式是否匹配所有URL
console.log('\n验证匹配:');
const regex2 = new RegExp(pattern2.pattern);
dashboardUrls.forEach(url => {
  const matches = regex2.test(url);
  console.log(`  ${matches ? '✓' : '✗'} ${url}`);
});

// 测试3: 单个URL
console.log('\n\n测试3: 单个URL');
console.log('-------------------');
const singleUrl = ['https://www.lixinger.com/about'];

console.log('输入URL:');
console.log(`  - ${singleUrl[0]}`);

const pattern3 = analyzer.generatePattern(singleUrl);
console.log('\n生成的模式:');
console.log('  pattern:', pattern3.pattern);
console.log('  pathTemplate:', pattern3.pathTemplate);
console.log('  queryParams:', pattern3.queryParams);

// 验证正则表达式是否匹配
console.log('\n验证匹配:');
const regex3 = new RegExp(pattern3.pattern);
const matches3 = regex3.test(singleUrl[0]);
console.log(`  ${matches3 ? '✓' : '✗'} ${singleUrl[0]}`);

// 测试4: 混合参数URL组
console.log('\n\n测试4: 混合参数URL组');
console.log('-------------------');
const mixedUrls = [
  'https://www.lixinger.com/analytics/index/dashboard?type=cn',
  'https://www.lixinger.com/analytics/stock/dashboard?type=us&view=detail',
  'https://www.lixinger.com/analytics/company/dashboard'
];

console.log('输入URL:');
mixedUrls.forEach(url => console.log(`  - ${url}`));

const pattern4 = analyzer.generatePattern(mixedUrls);
console.log('\n生成的模式:');
console.log('  pattern:', pattern4.pattern);
console.log('  pathTemplate:', pattern4.pathTemplate);
console.log('  queryParams:', pattern4.queryParams);

// 验证正则表达式是否匹配所有URL
console.log('\n验证匹配:');
const regex4 = new RegExp(pattern4.pattern);
mixedUrls.forEach(url => {
  const matches = regex4.test(url);
  console.log(`  ${matches ? '✓' : '✗'} ${url}`);
});

console.log('\n=== 测试完成 ===');
