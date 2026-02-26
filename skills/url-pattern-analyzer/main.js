/**
 * URL Pattern Analyzer - Main Entry Point
 * 
 * 分析links.txt中的URL，识别URL模式并生成报告
 * 
 * 使用方式:
 *   node main.js <linksFile> <outputFile> [options]
 * 
 * 参数:
 *   linksFile   - links.txt文件路径
 *   outputFile  - 输出JSON文件路径
 *   --min-group-size <n>        - 最小分组大小（默认5）
 *   --sample-count <n>          - 每个模式的示例URL数量（默认5）
 *   --refine-max-values <n>     - 半固定段最大唯一值数量（默认8）
 *   --refine-min-count <n>      - 半固定段每个值的最小出现次数（默认10）
 *   --refine-min-groups <n>     - 半固定段最少需要几个大组才细分（默认2）
 *   --markdown                  - 同时生成Markdown报告
 *   --help                      - 显示帮助信息
 */

const LinksReader = require('./lib/links-reader');
const URLPatternAnalyzer = require('./lib/url-clusterer');
const ReportGenerator = require('./lib/report-generator');
const path = require('path');
const fs = require('fs').promises;

/**
 * 解析命令行参数
 */
function parseArgs() {
  const args = process.argv.slice(2);
  
  // 显示帮助
  if (args.includes('--help') || args.includes('-h')) {
    showHelp();
    process.exit(0);
  }
  
  // 检查必需参数
  if (args.length < 2) {
    console.error('错误: 缺少必需参数');
    console.error('使用 --help 查看帮助信息');
    process.exit(1);
  }
  
  const config = {
    linksFile: args[0],
    outputFile: args[1],
    minGroupSize: 5,
    sampleCount: 5,
    generateMarkdown: false,
    // 细分控制参数
    refineMaxValues: 8,      // 半固定段最大唯一值数量
    refineMinCount: 10,      // 每个值最小出现次数
    refineMinGroups: 2,      // 最少需要几个大组才细分
    // 严格模式参数
    strictTopN: 0,           // 对前N个最大簇应用严格规则（0=不启用）
    strictMatchRatio: 0.8    // 严格模式下的匹配比例
  };
  
  // 解析选项
  for (let i = 2; i < args.length; i++) {
    const arg = args[i];
    
    if (arg === '--min-group-size' && i + 1 < args.length) {
      config.minGroupSize = parseInt(args[++i], 10);
    } else if (arg === '--sample-count' && i + 1 < args.length) {
      config.sampleCount = parseInt(args[++i], 10);
    } else if (arg === '--refine-max-values' && i + 1 < args.length) {
      config.refineMaxValues = parseInt(args[++i], 10);
    } else if (arg === '--refine-min-count' && i + 1 < args.length) {
      config.refineMinCount = parseInt(args[++i], 10);
    } else if (arg === '--refine-min-groups' && i + 1 < args.length) {
      config.refineMinGroups = parseInt(args[++i], 10);
    } else if (arg === '--strict-top-n' && i + 1 < args.length) {
      config.strictTopN = parseInt(args[++i], 10);
    } else if (arg === '--strict-match-ratio' && i + 1 < args.length) {
      config.strictMatchRatio = parseFloat(args[++i]);
    } else if (arg === '--markdown') {
      config.generateMarkdown = true;
    }
  }
  
  return config;
}

/**
 * 显示帮助信息
 */
function showHelp() {
  console.log(`
URL Pattern Analyzer - 分析URL模式并生成报告

使用方式:
  node main.js <linksFile> <outputFile> [options]

参数:
  linksFile              links.txt文件路径
  outputFile             输出JSON文件路径

基础选项:
  --min-group-size <n>   最小分组大小（默认5）
  --sample-count <n>     每个模式的示例URL数量（默认5）
  --markdown             同时生成Markdown报告

细分控制选项（用于控制URL模式的细分程度）:
  --refine-max-values <n>   半固定段最大唯一值数量（默认8）
                            如果某个路径段的唯一值 ≤ 此值，可能被细分
                            
  --refine-min-count <n>    半固定段每个值的最小出现次数（默认10）
                            只有出现次数 ≥ 此值的值才会被单独分组
                            
  --refine-min-groups <n>   最少需要几个大组才细分（默认2）
                            只有至少有N个值满足min-count时才细分

严格模式选项（对最大的簇应用更严格的细分规则）:
  --strict-top-n <n>        对前N个最大簇应用严格规则（默认0，不启用）
                            严格规则要求每个路径段要么全部固定，要么只有一个变量
                            
  --strict-match-ratio <f>  严格模式下的匹配比例（默认0.8，即80%）
                            整体固定比例 >= 此值时不再细分
  
  --help, -h             显示此帮助信息

示例:
  # 基本使用
  node main.js links.txt url-patterns.json

  # 生成Markdown报告
  node main.js links.txt url-patterns.json --markdown

  # 自定义分组参数
  node main.js links.txt url-patterns.json --min-group-size 10 --sample-count 3

  # 控制细分程度（更激进的细分）
  node main.js links.txt url-patterns.json --refine-max-values 10 --refine-min-count 5

  # 控制细分程度（更保守的细分）
  node main.js links.txt url-patterns.json --refine-max-values 5 --refine-min-count 20

参数调优建议:
  
  1. min-group-size: 控制最终保留的模式
     - 小型网站（<1000 URLs）: 3-5
     - 中型网站（1000-5000 URLs）: 5-10
     - 大型网站（>5000 URLs）: 10-20
  
  2. refine-max-values: 控制哪些段可以被细分
     - 值越小，细分越保守（只细分值很少的段）
     - 值越大，细分越激进（可以细分值较多的段）
     - 推荐范围: 5-15
  
  3. refine-min-count: 控制细分后的最小组大小
     - 值越大，只有大组才会被单独分出来
     - 值越小，小组也会被单独分出来
     - 推荐范围: 5-20
  
  4. refine-min-groups: 控制细分的触发条件
     - 值越大，需要更多大组才会细分
     - 值越小，更容易触发细分
     - 推荐范围: 2-5

输出:
  - JSON报告: 包含所有识别的URL模式
  - Markdown报告: 可读性更好的分析报告（可选）
  `);
}

/**
 * 主函数
 */
async function main() {
  try {
    // 解析参数
    const config = parseArgs();
    
    console.log('=== URL Pattern Analyzer ===\n');
    console.log(`输入文件: ${config.linksFile}`);
    console.log(`输出文件: ${config.outputFile}`);
    console.log(`最小分组: ${config.minGroupSize}`);
    console.log(`示例数量: ${config.sampleCount}`);
    console.log(`生成Markdown: ${config.generateMarkdown ? '是' : '否'}`);
    console.log('');
    
    // 步骤1: 读取links.txt
    console.log('步骤1: 读取links.txt');
    console.log('-------------------');
    const reader = new LinksReader();
    const records = await reader.readLinksFile(config.linksFile);
    console.log(`✓ 读取了 ${records.length} 条记录`);
    
    // 获取统计信息
    const stats = reader.getStatistics(records);
    console.log(`  统计信息:`);
    console.log(`    - 总记录数: ${stats.total}`);
    console.log(`    - 有错误的: ${stats.withErrors}`);
    console.log(`    - 缺少URL的: ${stats.withoutUrl}`);
    if (Object.keys(stats.byStatus).length > 0) {
      console.log(`    - 按状态分布:`);
      Object.entries(stats.byStatus).forEach(([status, count]) => {
        console.log(`      - ${status}: ${count}`);
      });
    }
    
    // 步骤2: 提取URL（默认所有URL，可通过参数控制）
    console.log('\n步骤2: 提取URL');
    console.log('-------------------');
    const urlStrings = reader.extractURLs(records, { 
      // 不限制status，分析所有URL
      excludeErrors: true 
    });
    console.log(`✓ 提取了 ${urlStrings.length} 个URL`);
    
    if (urlStrings.length === 0) {
      console.error('错误: 没有找到有效的URL');
      process.exit(1);
    }
    
    // 步骤3: URL聚类
    console.log('\n步骤3: URL聚类分析');
    console.log('-------------------');
    const analyzer = new URLPatternAnalyzer({
      refineMaxValues: config.refineMaxValues,
      refineMinCount: config.refineMinCount,
      refineMinGroups: config.refineMinGroups,
      strictTopN: config.strictTopN,
      strictMatchRatio: config.strictMatchRatio
    });
    const startTime = Date.now();
    const clusters = analyzer.clusterURLs(urlStrings);
    const duration = Date.now() - startTime;
    
    console.log(`✓ 聚类完成，用时 ${duration}ms`);
    console.log(`  识别出 ${clusters.length} 个URL模式`);
    
    // 过滤小组（如果设置了最小分组大小）
    const filteredClusters = clusters.filter(cluster => cluster.length >= config.minGroupSize);
    if (filteredClusters.length < clusters.length) {
      console.log(`  过滤后保留 ${filteredClusters.length} 个模式（最小分组: ${config.minGroupSize}）`);
    }
    
    // 显示前10个模式的URL数量
    console.log(`  前10个模式的URL数量:`);
    filteredClusters.slice(0, 10).forEach((cluster, i) => {
      console.log(`    ${i + 1}. ${cluster.length} 个URL`);
    });
    
    // 步骤4: 生成报告
    console.log('\n步骤4: 生成报告');
    console.log('-------------------');
    const generator = new ReportGenerator();
    
    // 生成JSON报告
    const jsonReport = generator.generateJSONReport(filteredClusters, { 
      sampleCount: config.sampleCount 
    });
    console.log(`✓ JSON报告生成成功`);
    console.log(`  总URL数: ${jsonReport.summary.totalUrls}`);
    console.log(`  模式数量: ${jsonReport.summary.patternCount}`);
    
    // 步骤5: 保存JSON报告
    console.log('\n步骤5: 保存报告');
    console.log('-------------------');
    await generator.saveJSONReport(jsonReport, config.outputFile);
    
    // 生成并保存Markdown报告（如果需要）
    if (config.generateMarkdown) {
      const markdown = generator.generateMarkdownReport(filteredClusters, { 
        sampleCount: config.sampleCount 
      });
      const mdPath = config.outputFile.replace(/\.json$/, '.md');
      await generator.saveMarkdownReport(markdown, mdPath);
    }
    
    // 显示报告摘要
    console.log('\n=== 分析完成 ===');
    console.log(`总URL数: ${jsonReport.summary.totalUrls}`);
    console.log(`模式数量: ${jsonReport.summary.patternCount}`);
    
    if (jsonReport.patterns.length > 0) {
      console.log(`\n前5个最大的模式:`);
      jsonReport.patterns.slice(0, 5).forEach((pattern, i) => {
        const percentage = ((pattern.urlCount / jsonReport.summary.totalUrls) * 100).toFixed(1);
        console.log(`${i + 1}. ${pattern.name}`);
        console.log(`   - 路径: ${pattern.pathTemplate}`);
        console.log(`   - URL数: ${pattern.urlCount} (${percentage}%)`);
        console.log(`   - 参数: ${pattern.queryParams.join(', ') || '无'}`);
      });
    }
    
    console.log('\n✓ 分析成功完成！');
    console.log(`\n输出文件:`);
    console.log(`  - ${config.outputFile}`);
    if (config.generateMarkdown) {
      console.log(`  - ${config.outputFile.replace(/\.json$/, '.md')}`);
    }
    
    // 返回结果（供程序化调用）
    return {
      success: true,
      patternsFile: config.outputFile,
      patternCount: jsonReport.summary.patternCount,
      totalUrls: jsonReport.summary.totalUrls,
      patterns: jsonReport.patterns
    };
    
  } catch (error) {
    console.error('\n✗ 分析失败:', error.message);
    if (process.env.DEBUG) {
      console.error(error.stack);
    }
    process.exit(1);
  }
}

// 如果直接运行此文件，执行主函数
if (require.main === module) {
  main().catch(error => {
    console.error('程序异常退出:', error);
    process.exit(1);
  });
}

// 导出主函数供其他模块调用
module.exports = main;
