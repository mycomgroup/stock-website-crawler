/**
 * 测试 ReportGenerator 类
 */

const ReportGenerator = require('../lib/report-generator');
const URLPatternAnalyzer = require('../lib/url-clusterer');
const path = require('path');
const fs = require('fs').promises;

async function testReportGenerator() {
  const generator = new ReportGenerator();
  const analyzer = new URLPatternAnalyzer();
  let testsPassed = 0;
  let testsFailed = 0;
  
  console.log('=== ReportGenerator 测试 ===\n');
  
  // 准备测试数据
  const testUrls = [
    // API文档组
    'https://www.lixinger.com/open/api/doc?api-key=cn/company',
    'https://www.lixinger.com/open/api/doc?api-key=hk/index',
    'https://www.lixinger.com/open/api/doc?api-key=us/stock',
    'https://www.lixinger.com/open/api/doc?api-key=cn/index',
    // Dashboard组
    'https://www.lixinger.com/analytics/company/dashboard',
    'https://www.lixinger.com/analytics/index/dashboard',
    'https://www.lixinger.com/analytics/stock/dashboard',
    // 单个URL
    'https://www.lixinger.com/about'
  ];
  
  // 聚类URL
  const clusters = analyzer.clusterURLs(testUrls);
  console.log(`聚类结果: ${clusters.length} 个模式`);
  clusters.forEach((cluster, i) => {
    console.log(`  模式 ${i + 1}: ${cluster.length} 个URL`);
  });
  console.log('');
  
  // 测试1: 生成JSON报告
  console.log('测试1: 生成JSON报告');
  console.log('-------------------');
  try {
    const jsonReport = generator.generateJSONReport(clusters, { sampleCount: 3 });
    
    console.log('✓ JSON报告生成成功');
    console.log(`  总URL数: ${jsonReport.summary.totalUrls}`);
    console.log(`  模式数量: ${jsonReport.summary.patternCount}`);
    console.log(`  生成时间: ${jsonReport.summary.generatedAt}`);
    console.log(`  模式列表:`);
    
    jsonReport.patterns.forEach((pattern, i) => {
      console.log(`    ${i + 1}. ${pattern.name}`);
      console.log(`       - 路径模板: ${pattern.pathTemplate}`);
      console.log(`       - URL数量: ${pattern.urlCount}`);
      console.log(`       - 查询参数: ${pattern.queryParams.join(', ') || '无'}`);
      console.log(`       - 示例数量: ${pattern.samples.length}`);
    });
    
    // 验证报告结构
    if (jsonReport.summary &&
        jsonReport.summary.totalUrls === 8 &&
        jsonReport.summary.patternCount === clusters.length &&
        jsonReport.patterns &&
        jsonReport.patterns.length === clusters.length &&
        jsonReport.patterns[0].name &&
        jsonReport.patterns[0].pathTemplate &&
        jsonReport.patterns[0].pattern &&
        jsonReport.patterns[0].samples.length <= 3) {
      testsPassed++;
    } else {
      console.log('✗ JSON报告结构不符合预期');
      testsFailed++;
    }
  } catch (error) {
    console.log(`✗ 测试失败: ${error.message}`);
    testsFailed++;
  }
  
  // 测试2: 生成Markdown报告
  console.log('\n测试2: 生成Markdown报告');
  console.log('-------------------');
  try {
    const markdown = generator.generateMarkdownReport(clusters, { sampleCount: 3 });
    
    console.log('✓ Markdown报告生成成功');
    console.log(`  报告长度: ${markdown.length} 字符`);
    console.log(`  报告行数: ${markdown.split('\n').length} 行`);
    
    // 验证Markdown内容
    const hasTitle = markdown.includes('# URL模式分析报告');
    const hasSummary = markdown.includes('## 统计摘要');
    const hasPatterns = markdown.includes('## 模式详情');
    const hasTable = markdown.includes('| 序号 | 模式名称 | URL数量 | 占比 | 路径模板 |');
    
    console.log(`  包含标题: ${hasTitle ? '✓' : '✗'}`);
    console.log(`  包含统计摘要: ${hasSummary ? '✓' : '✗'}`);
    console.log(`  包含模式详情: ${hasPatterns ? '✓' : '✗'}`);
    console.log(`  包含分布表格: ${hasTable ? '✓' : '✗'}`);
    
    // 显示报告预览（前20行）
    console.log('\n  报告预览（前20行）:');
    const lines = markdown.split('\n');
    lines.slice(0, 20).forEach(line => {
      console.log(`    ${line}`);
    });
    if (lines.length > 20) {
      console.log(`    ... (还有 ${lines.length - 20} 行)`);
    }
    
    if (hasTitle && hasSummary && hasPatterns && hasTable) {
      testsPassed++;
    } else {
      console.log('✗ Markdown报告内容不完整');
      testsFailed++;
    }
  } catch (error) {
    console.log(`✗ 测试失败: ${error.message}`);
    testsFailed++;
  }
  
  // 测试3: 保存JSON报告到文件
  console.log('\n测试3: 保存JSON报告到文件');
  console.log('-------------------');
  try {
    const jsonReport = generator.generateJSONReport(clusters);
    const outputPath = path.join(__dirname, '../output/test-url-patterns.json');
    
    await generator.saveJSONReport(jsonReport, outputPath);
    
    // 验证文件是否存在
    const fileExists = await fs.access(outputPath).then(() => true).catch(() => false);
    
    if (fileExists) {
      // 读取文件验证内容
      const content = await fs.readFile(outputPath, 'utf-8');
      const parsed = JSON.parse(content);
      
      console.log(`✓ 文件已保存并验证: ${outputPath}`);
      console.log(`  文件大小: ${content.length} 字节`);
      console.log(`  包含 ${parsed.patterns.length} 个模式`);
      
      testsPassed++;
    } else {
      console.log('✗ 文件未成功保存');
      testsFailed++;
    }
  } catch (error) {
    console.log(`✗ 测试失败: ${error.message}`);
    testsFailed++;
  }
  
  // 测试4: 保存Markdown报告到文件
  console.log('\n测试4: 保存Markdown报告到文件');
  console.log('-------------------');
  try {
    const markdown = generator.generateMarkdownReport(clusters);
    const outputPath = path.join(__dirname, '../output/test-url-patterns.md');
    
    await generator.saveMarkdownReport(markdown, outputPath);
    
    // 验证文件是否存在
    const fileExists = await fs.access(outputPath).then(() => true).catch(() => false);
    
    if (fileExists) {
      // 读取文件验证内容
      const content = await fs.readFile(outputPath, 'utf-8');
      
      console.log(`✓ 文件已保存并验证: ${outputPath}`);
      console.log(`  文件大小: ${content.length} 字节`);
      console.log(`  行数: ${content.split('\n').length}`);
      
      testsPassed++;
    } else {
      console.log('✗ 文件未成功保存');
      testsFailed++;
    }
  } catch (error) {
    console.log(`✗ 测试失败: ${error.message}`);
    testsFailed++;
  }
  
  // 测试5: 自定义示例数量
  console.log('\n测试5: 自定义示例数量');
  console.log('-------------------');
  try {
    const jsonReport1 = generator.generateJSONReport(clusters, { sampleCount: 2 });
    const jsonReport2 = generator.generateJSONReport(clusters, { sampleCount: 10 });
    
    console.log(`✓ sampleCount=2: 第一个模式有 ${jsonReport1.patterns[0].samples.length} 个示例`);
    console.log(`✓ sampleCount=10: 第一个模式有 ${jsonReport2.patterns[0].samples.length} 个示例`);
    
    // 验证示例数量限制
    const maxSamples1 = Math.max(...jsonReport1.patterns.map(p => p.samples.length));
    const maxSamples2 = Math.max(...jsonReport2.patterns.map(p => p.samples.length));
    
    if (maxSamples1 <= 2 && maxSamples2 <= 10) {
      testsPassed++;
    } else {
      console.log(`✗ 示例数量限制不正确: ${maxSamples1}, ${maxSamples2}`);
      testsFailed++;
    }
  } catch (error) {
    console.log(`✗ 测试失败: ${error.message}`);
    testsFailed++;
  }
  
  // 总结
  console.log('\n=== 测试总结 ===');
  console.log(`通过: ${testsPassed}`);
  console.log(`失败: ${testsFailed}`);
  console.log(`总计: ${testsPassed + testsFailed}`);
  
  if (testsFailed === 0) {
    console.log('\n✓ 所有测试通过！');
  } else {
    console.log(`\n✗ ${testsFailed} 个测试失败`);
    process.exit(1);
  }
}

// 运行测试
testReportGenerator().catch(error => {
  console.error('测试运行失败:', error);
  process.exit(1);
});
