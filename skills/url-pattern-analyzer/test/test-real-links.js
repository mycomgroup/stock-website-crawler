/**
 * 测试使用真实的links.txt文件
 */

const LinksReader = require('../lib/links-reader');
const path = require('path');

async function testRealLinks() {
  const reader = new LinksReader();
  
  console.log('=== 测试真实links.txt文件 ===\n');
  
  // 真实文件路径
  const linksFile = path.join(__dirname, '../../../stock-crawler/output/lixinger-crawler/links.txt');
  
  console.log(`读取文件: ${linksFile}\n`);
  
  try {
    // 读取文件
    console.log('正在读取文件...');
    const records = await reader.readLinksFile(linksFile);
    console.log(`✓ 成功读取 ${records.length} 条记录\n`);
    
    // 获取统计信息
    console.log('统计信息:');
    console.log('-------------------');
    const stats = reader.getStatistics(records);
    console.log(`总记录数: ${stats.total}`);
    console.log(`按状态统计:`);
    Object.entries(stats.byStatus).forEach(([status, count]) => {
      console.log(`  ${status}: ${count}`);
    });
    console.log(`有错误的记录: ${stats.withErrors}`);
    console.log(`缺少URL的记录: ${stats.withoutUrl}`);
    
    // 提取URL
    console.log('\nURL提取:');
    console.log('-------------------');
    const allUrls = reader.extractURLs(records);
    console.log(`所有URL: ${allUrls.length} 个`);
    
    const fetchedUrls = reader.extractURLs(records, { status: 'fetched' });
    console.log(`fetched状态的URL: ${fetchedUrls.length} 个`);
    
    const noErrorUrls = reader.extractURLs(records, { excludeErrors: true });
    console.log(`无错误的URL: ${noErrorUrls.length} 个`);
    
    const fetchedNoErrorUrls = reader.extractURLs(records, { 
      status: 'fetched', 
      excludeErrors: true 
    });
    console.log(`fetched且无错误的URL: ${fetchedNoErrorUrls.length} 个`);
    
    // 显示前5个URL示例
    console.log('\n前5个URL示例:');
    console.log('-------------------');
    fetchedNoErrorUrls.slice(0, 5).forEach((url, index) => {
      console.log(`${index + 1}. ${url}`);
    });
    
    console.log('\n✓ 测试完成！');
    
  } catch (error) {
    console.error(`✗ 测试失败: ${error.message}`);
    process.exit(1);
  }
}

testRealLinks();
