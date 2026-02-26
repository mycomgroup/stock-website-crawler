#!/usr/bin/env node

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
 *   --min-group-size <n>  - 最小分组大小（默认5）
 *   --sample-count <n>    - 每个模式的示例URL数量（默认5）
 *   --markdown            - 同时生成Markdown报告
 *   --help                - 显示帮助信息
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
    generateMarkdown: false
  };
  
  // 解析选项
  for (let i = 2; i < args.length; i++) {
    const arg = args[i];
    
    if (arg === '--min-group-size' && i + 1 < args.length) {
      config.minGroupSize = parseInt(args[++i], 10);
    } else if (arg === '--sample-count' && i + 1 < args.length) {
      config.sampleCount = parseInt(args[++i], 10);
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

选项:
  --min-group-size <n>   最小分组大小（默认5）
  --sample-count <n>     每个模式的示例URL数量（默认5）
  --markdown             同时生成Markdown报告
  --help, -h             显示此帮助信息

示例:
  # 基本使用
  node main.js links.txt url-patterns.json

  # 生成Markdown报告
  node main.js links.txt url-patterns.json --markdown

  # 自定义参数
  node main.js links.txt url-patterns.json --min-group-size 10 --sample-count 3

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
    
    // 步骤2: 提取URL（只要fetched且无错误的）
    console.log('\n步骤2: 提取有效URL');
    console.log('-------------------');
    const urlStrings = reader.extractURLs(records, { 
      status: 'fetched', 
      excludeErrors: true 
    });
    console.log(`✓ 提取了 ${urlStrings.length} 个有效URL`);
    
    if (urlStrings.length === 0) {
      console.error('错误: 没有找到有效的URL');
      process.exit(1);
    }
    
    // 步骤3: URL聚类
    console.log('\n步骤3: URL聚类分析');
    console.log('-------------------');
    const analyzer = new URLPatternAnalyzer();
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
