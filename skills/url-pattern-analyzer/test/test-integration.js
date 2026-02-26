/**
 * 集成测试: LinksReader + URLPatternAnalyzer
 * 
 * 测试完整的工作流：读取links.txt -> 提取URL -> 聚类 -> 生成模式
 */

const LinksReader = require('../lib/links-reader');
const URLPatternAnalyzer = require('../lib/url-clusterer');
const path = require('path');

async function integrationTest() {
  console.log('=== 集成测试: 完整工作流 ===\n');
  
  const reader = new LinksReader();
  const analyzer = new URLPatternAnalyzer();
  
  // 真实文件路径
  const linksFile = path.join(__dirname, '../../../stock-crawler/output/lixinger-crawler/links.txt');
  
  try {
    // 步骤1: 读取links文件
    console.log('步骤1: 读取links.txt文件');
    console.log('-------------------');
    const records = await reader.readLinksFile(linksFile);
    console.log(`✓ 读取 ${records.length} 条记录\n`);
    
    // 步骤2: 提取fetched状态且无错误的URL
    console.log('步骤2: 提取有效URL');
    console.log('-------------------');
    const urls = reader.extractURLs(records, { 
      status: 'fetched', 
      excludeErrors: true 
    });
    console.log(`✓ 提取 ${urls.length} 个有效URL\n`);
    
    // 步骤3: URL聚类（使用前100个URL进行快速测试）
    console.log('步骤3: URL聚类分析');
    console.log('-------------------');
    const sampleSize = Math.min(100, urls.length);
    const sampleUrls = urls.slice(0, sampleSize);
    console.log(`使用前 ${sampleSize} 个URL进行聚类...\n`);
    
    const clusters = analyzer.clusterURLs(sampleUrls);
    console.log(`✓ 识别出 ${clusters.length} 个URL模式\n`);
    
    // 步骤4: 为每个簇生成正则表达式模式
    console.log('步骤4: 生成URL模式');
    console.log('-------------------');
    
    const patterns = [];
    
    clusters.forEach((cluster, index) => {
      console.log(`\n模式 ${index + 1} (${cluster.length} 个URL):`);
      
      try {
        const pattern = analyzer.generatePattern(cluster);
        patterns.push({
          name: `pattern-${index + 1}`,
          ...pattern,
          urlCount: cluster.length,
          samples: cluster.slice(0, 3) // 保存前3个URL作为示例
        });
        
        console.log(`  路径模板: ${pattern.pathTemplate}`);
        console.log(`  正则表达式: ${pattern.pattern}`);
        console.log(`  查询参数: [${pattern.queryParams.join(', ')}]`);
        console.log(`  示例URL:`);
        cluster.slice(0, 3).forEach(url => {
          console.log(`    - ${url}`);
        });
        
        // 验证正则表达式
        const regex = new RegExp(pattern.pattern);
        const allMatch = cluster.every(url => regex.test(url));
        console.log(`  验证: ${allMatch ? '✓ 所有URL匹配' : '✗ 部分URL不匹配'}`);
        
      } catch (error) {
        console.log(`  ✗ 生成模式失败: ${error.message}`);
      }
    });
    
    // 步骤5: 输出总结
    console.log('\n\n=== 测试总结 ===');
    console.log(`总URL数: ${urls.length}`);
    console.log(`测试样本: ${sampleSize}`);
    console.log(`识别模式: ${patterns.length}`);
    console.log(`平均每个模式: ${(sampleSize / patterns.length).toFixed(1)} 个URL`);
    
    // 显示最大的3个模式
    console.log('\n最大的3个URL模式:');
    const sortedPatterns = patterns.sort((a, b) => b.urlCount - a.urlCount);
    sortedPatterns.slice(0, 3).forEach((pattern, index) => {
      console.log(`\n${index + 1}. ${pattern.name} (${pattern.urlCount} 个URL)`);
      console.log(`   路径: ${pattern.pathTemplate}`);
      console.log(`   参数: [${pattern.queryParams.join(', ')}]`);
    });
    
    console.log('\n✓ 集成测试完成！');
    
  } catch (error) {
    console.error(`\n✗ 集成测试失败: ${error.message}`);
    console.error(error.stack);
    process.exit(1);
  }
}

integrationTest();
