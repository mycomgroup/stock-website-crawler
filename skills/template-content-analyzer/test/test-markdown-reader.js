/**
 * 测试markdown文件读取器 - 使用真实数据
 */

const TemplateContentAnalyzer = require('../lib/content-analyzer');
const path = require('path');

async function testMarkdownReader() {
  console.log('\n=== 测试Markdown文件读取器 ===\n');
  
  const analyzer = new TemplateContentAnalyzer();
  
  // 测试1: 匹配URL模式到文件
  console.log('测试1: 匹配URL模式到文件...');
  const urlPattern = {
    name: 'open-api',
    pathTemplate: '/open/api/{param2}',
    pattern: '^https://www\\.lixinger\\.com/open/api/([^/]+)(\\?.*)?$'
  };
  
  const pagesDir = path.join(__dirname, '../../../stock-crawler/output/lixinger-crawler/pages');
  
  try {
    const matchedFiles = await analyzer.matchPagesToURLs(urlPattern, pagesDir);
    console.log(`✓ 找到 ${matchedFiles.length} 个匹配的文件`);
    
    if (matchedFiles.length > 0) {
      console.log('  示例文件:');
      matchedFiles.slice(0, 3).forEach(file => {
        console.log(`    - ${path.basename(file)}`);
      });
    }
  } catch (error) {
    console.error('✗ 匹配失败:', error.message);
  }
  
  // 测试2: 批量加载页面（流式处理）
  console.log('\n测试2: 批量加载页面（流式处理）...');
  
  try {
    const urlPattern2 = {
      name: 'fund',
      pathTemplate: '/cn/fund',
      pattern: '^https://www\\.lixinger\\.com/.*fund.*$'
    };
    
    const matchedFiles2 = await analyzer.matchPagesToURLs(urlPattern2, pagesDir);
    
    if (matchedFiles2.length > 0) {
      console.log(`✓ 找到 ${matchedFiles2.length} 个基金相关文件`);
      
      // 使用流式处理加载前10个文件
      const testFiles = matchedFiles2.slice(0, 10);
      let batchCount = 0;
      let totalSize = 0;
      
      for await (const batch of analyzer.loadMarkdownPages(testFiles, { batchSize: 3 })) {
        batchCount++;
        batch.forEach(page => {
          totalSize += page.size;
        });
        console.log(`  批次 ${batchCount}: 加载了 ${batch.length} 个文件`);
      }
      
      console.log(`✓ 总共处理 ${batchCount} 个批次，总大小: ${(totalSize / 1024).toFixed(2)} KB`);
    } else {
      console.log('  未找到匹配的文件，跳过加载测试');
    }
  } catch (error) {
    console.error('✗ 加载失败:', error.message);
  }
  
  // 测试3: 分析页面内容
  console.log('\n测试3: 分析页面内容...');
  
  try {
    const urlPattern3 = {
      name: 'csv',
      pathTemplate: '/csv',
      pattern: '^https://www\\.lixinger\\.com/.*csv.*$'
    };
    
    const matchedFiles3 = await analyzer.matchPagesToURLs(urlPattern3, pagesDir);
    
    if (matchedFiles3.length >= 2) {
      console.log(`✓ 找到 ${matchedFiles3.length} 个CSV相关文件`);
      
      // 加载前几个文件并分析
      const pages = [];
      for await (const batch of analyzer.loadMarkdownPages(matchedFiles3.slice(0, 3), { batchSize: 10 })) {
        batch.forEach(page => pages.push(page.content));
      }
      
      if (pages.length > 0) {
        const result = analyzer.analyzeTemplate(pages);
        console.log(`✓ 分析结果:`);
        console.log(`  - 总页面数: ${result.stats.totalPages}`);
        console.log(`  - 总内容块: ${result.stats.totalBlocks}`);
        console.log(`  - 模板内容: ${result.stats.templateBlocks}`);
        console.log(`  - 独特内容: ${result.stats.uniqueBlocks}`);
        console.log(`  - 混合内容: ${result.stats.mixedBlocks}`);
      }
    } else {
      console.log('  未找到足够的文件，跳过分析测试');
    }
  } catch (error) {
    console.error('✗ 分析失败:', error.message);
  }
  
  console.log('\n=== 测试完成 ===\n');
}

// 运行测试
testMarkdownReader().catch(error => {
  console.error('测试失败:', error);
  process.exit(1);
});
