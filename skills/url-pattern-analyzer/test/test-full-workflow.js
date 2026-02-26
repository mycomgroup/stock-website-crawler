/**
 * 完整工作流测试 - 使用真实数据
 * 
 * 测试从读取links.txt到生成报告的完整流程
 */

const LinksReader = require('../lib/links-reader');
const URLPatternAnalyzer = require('../lib/url-clusterer');
const ReportGenerator = require('../lib/report-generator');
const path = require('path');
const fs = require('fs').promises;

async function testFullWorkflow() {
  console.log('=== 完整工作流测试 ===\n');
  
  // 检查是否有真实的links.txt文件
  const linksPath = path.join(__dirname, '../../../stock-crawler/output/lixinger-crawler/links.txt');
  const hasRealData = await fs.access(linksPath).then(() => true).catch(() => false);
  
  if (!hasRealData) {
    console.log('⚠ 未找到真实数据文件，使用测试数据');
    await testWithMockData();
    return;
  }
  
  console.log('✓ 找到真实数据文件，开始分析...\n');
  
  try {
    // 步骤1: 读取links.txt
    console.log('步骤1: 读取links.txt');
    console.log('-------------------');
    const reader = new LinksReader();
    const records = await reader.readLinksFile(linksPath);
    console.log(`✓ 读取了 ${records.length} 条记录`);
    
    // 获取统计信息
    const stats = reader.getStatistics(records);
    console.log(`  统计信息:`);
    console.log(`    - 总记录数: ${stats.total}`);
    console.log(`    - 有错误的: ${stats.withErrors}`);
    console.log(`    - 缺少URL的: ${stats.withoutUrl}`);
    console.log(`    - 按状态分布:`);
    Object.entries(stats.byStatus).forEach(([status, count]) => {
      console.log(`      - ${status}: ${count}`);
    });
    
    // 步骤2: 提取URL（只要fetched且无错误的）
    console.log('\n步骤2: 提取URL');
    console.log('-------------------');
    const urlStrings = reader.extractURLs(records, { 
      status: 'fetched', 
      excludeErrors: true 
    });
    console.log(`✓ 提取了 ${urlStrings.length} 个有效URL`);
    
    // 步骤3: URL聚类
    console.log('\n步骤3: URL聚类分析');
    console.log('-------------------');
    const analyzer = new URLPatternAnalyzer();
    const startTime = Date.now();
    const clusters = analyzer.clusterURLs(urlStrings);
    const duration = Date.now() - startTime;
    
    console.log(`✓ 聚类完成，用时 ${duration}ms`);
    console.log(`  识别出 ${clusters.length} 个URL模式`);
    console.log(`  前10个模式的URL数量:`);
    clusters.slice(0, 10).forEach((cluster, i) => {
      console.log(`    ${i + 1}. ${cluster.length} 个URL`);
    });
    
    // 步骤4: 生成报告
    console.log('\n步骤4: 生成报告');
    console.log('-------------------');
    const generator = new ReportGenerator();
    
    // 生成JSON报告
    const jsonReport = generator.generateJSONReport(clusters, { sampleCount: 5 });
    console.log(`✓ JSON报告生成成功`);
    console.log(`  总URL数: ${jsonReport.summary.totalUrls}`);
    console.log(`  模式数量: ${jsonReport.summary.patternCount}`);
    
    // 生成Markdown报告
    const markdown = generator.generateMarkdownReport(clusters, { sampleCount: 5 });
    console.log(`✓ Markdown报告生成成功`);
    console.log(`  报告长度: ${markdown.length} 字符`);
    
    // 步骤5: 保存报告
    console.log('\n步骤5: 保存报告');
    console.log('-------------------');
    const outputDir = path.join(__dirname, '../../../stock-crawler/output/lixinger-crawler');
    
    const jsonPath = path.join(outputDir, 'url-patterns.json');
    await generator.saveJSONReport(jsonReport, jsonPath);
    
    const mdPath = path.join(outputDir, 'url-patterns.md');
    await generator.saveMarkdownReport(markdown, mdPath);
    
    // 显示报告摘要
    console.log('\n=== 报告摘要 ===');
    console.log(`总URL数: ${jsonReport.summary.totalUrls}`);
    console.log(`模式数量: ${jsonReport.summary.patternCount}`);
    console.log(`\n前5个最大的模式:`);
    jsonReport.patterns.slice(0, 5).forEach((pattern, i) => {
      console.log(`${i + 1}. ${pattern.name}`);
      console.log(`   - 路径: ${pattern.pathTemplate}`);
      console.log(`   - URL数: ${pattern.urlCount} (${((pattern.urlCount / jsonReport.summary.totalUrls) * 100).toFixed(1)}%)`);
      console.log(`   - 参数: ${pattern.queryParams.join(', ') || '无'}`);
    });
    
    console.log('\n✓ 完整工作流测试成功！');
    console.log(`\n报告文件:`);
    console.log(`  - ${jsonPath}`);
    console.log(`  - ${mdPath}`);
    
  } catch (error) {
    console.error('✗ 测试失败:', error.message);
    console.error(error.stack);
    process.exit(1);
  }
}

async function testWithMockData() {
  console.log('使用模拟数据进行测试...\n');
  
  // 创建模拟数据
  const mockUrls = [
    // API文档组 (大组)
    ...Array.from({ length: 20 }, (_, i) => 
      `https://www.lixinger.com/open/api/doc?api-key=cn/api${i}`
    ),
    // Dashboard组 (中组)
    ...Array.from({ length: 10 }, (_, i) => 
      `https://www.lixinger.com/analytics/company${i}/dashboard`
    ),
    // 分析页面组 (小组)
    ...Array.from({ length: 5 }, (_, i) => 
      `https://www.lixinger.com/analytics/stock/detail?id=${i}`
    ),
    // 单个页面
    'https://www.lixinger.com/about',
    'https://www.lixinger.com/contact',
    'https://www.lixinger.com/help'
  ];
  
  console.log(`创建了 ${mockUrls.length} 个模拟URL\n`);
  
  // 聚类
  const analyzer = new URLPatternAnalyzer();
  const clusters = analyzer.clusterURLs(mockUrls);
  console.log(`聚类结果: ${clusters.length} 个模式\n`);
  
  // 生成报告
  const generator = new ReportGenerator();
  const jsonReport = generator.generateJSONReport(clusters, { sampleCount: 3 });
  const markdown = generator.generateMarkdownReport(clusters, { sampleCount: 3 });
  
  // 保存到测试输出目录
  const outputDir = path.join(__dirname, '../output');
  await generator.saveJSONReport(jsonReport, path.join(outputDir, 'mock-url-patterns.json'));
  await generator.saveMarkdownReport(markdown, path.join(outputDir, 'mock-url-patterns.md'));
  
  console.log('\n✓ 模拟数据测试完成！');
  console.log(`\n报告摘要:`);
  console.log(`  总URL数: ${jsonReport.summary.totalUrls}`);
  console.log(`  模式数量: ${jsonReport.summary.patternCount}`);
  jsonReport.patterns.forEach((pattern, i) => {
    console.log(`  ${i + 1}. ${pattern.name}: ${pattern.urlCount} 个URL`);
  });
}

// 运行测试
testFullWorkflow().catch(error => {
  console.error('测试运行失败:', error);
  process.exit(1);
});
