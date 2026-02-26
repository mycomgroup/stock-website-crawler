#!/usr/bin/env node
/**
 * URL模式分析脚本
 * 
 * 从links.txt文件中分析URL模式，生成url-patterns.json和url-patterns.md报告
 * 
 * 使用方法:
 *   node scripts/analyze-url-patterns.js [options]
 * 
 * 选项:
 *   --input, -i <path>      输入的links.txt文件路径 (默认: stock-crawler/output/lixinger-crawler/links.txt)
 *   --output, -o <path>     输出目录 (默认: stock-crawler/output/lixinger-crawler)
 *   --min-group <number>    最小分组大小 (默认: 5)
 *   --samples <number>      每个模式的示例URL数量 (默认: 5)
 *   --help, -h              显示帮助信息
 */

const LinksReader = require('../lib/links-reader');
const URLPatternAnalyzer = require('../lib/url-clusterer');
const ReportGenerator = require('../lib/report-generator');
const path = require('path');
const fs = require('fs').promises;

// 解析命令行参数
function parseArgs() {
  const args = process.argv.slice(2);
  const options = {
    input: 'stock-crawler/output/lixinger-crawler/links.txt',
    output: 'stock-crawler/output/lixinger-crawler',
    minGroup: 5,
    samples: 5
  };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    
    if (arg === '--help' || arg === '-h') {
      printHelp();
      process.exit(0);
    } else if (arg === '--input' || arg === '-i') {
      options.input = args[++i];
    } else if (arg === '--output' || arg === '-o') {
      options.output = args[++i];
    } else if (arg === '--min-group') {
      options.minGroup = parseInt(args[++i], 10);
    } else if (arg === '--samples') {
      options.samples = parseInt(args[++i], 10);
    }
  }

  return options;
}

function printHelp() {
  console.log(`
URL模式分析脚本

使用方法:
  node scripts/analyze-url-patterns.js [options]

选项:
  --input, -i <path>      输入的links.txt文件路径
                          (默认: stock-crawler/output/lixinger-crawler/links.txt)
  --output, -o <path>     输出目录
                          (默认: stock-crawler/output/lixinger-crawler)
  --min-group <number>    最小分组大小 (默认: 5)
  --samples <number>      每个模式的示例URL数量 (默认: 5)
  --help, -h              显示帮助信息

示例:
  # 使用默认设置
  node scripts/analyze-url-patterns.js

  # 指定输入和输出
  node scripts/analyze-url-patterns.js -i data/links.txt -o output

  # 自定义参数
  node scripts/analyze-url-patterns.js --min-group 10 --samples 3
`);
}

// 显示进度条
function showProgress(current, total, label = '') {
  const percentage = Math.floor((current / total) * 100);
  const barLength = 40;
  const filledLength = Math.floor((barLength * current) / total);
  const bar = '█'.repeat(filledLength) + '░'.repeat(barLength - filledLength);
  
  process.stdout.write(`\r${label} [${bar}] ${percentage}% (${current}/${total})`);
  
  if (current === total) {
    process.stdout.write('\n');
  }
}

async function main() {
  const options = parseArgs();
  
  console.log('=== URL模式分析器 ===\n');
  console.log('配置:');
  console.log(`  输入文件: ${options.input}`);
  console.log(`  输出目录: ${options.output}`);
  console.log(`  最小分组: ${options.minGroup}`);
  console.log(`  示例数量: ${options.samples}\n`);

  try {
    // 步骤1: 检查输入文件
    console.log('步骤1: 检查输入文件');
    console.log('-------------------');
    const inputPath = path.resolve(options.input);
    
    try {
      await fs.access(inputPath);
      console.log(`✓ 找到输入文件: ${inputPath}\n`);
    } catch (error) {
      console.error(`✗ 输入文件不存在: ${inputPath}`);
      process.exit(1);
    }

    // 步骤2: 读取links.txt
    console.log('步骤2: 读取links.txt');
    console.log('-------------------');
    const reader = new LinksReader();
    const records = await reader.readLinksFile(inputPath);
    console.log(`✓ 读取了 ${records.length} 条记录`);
    
    // 获取统计信息
    const stats = reader.getStatistics(records);
    console.log(`\n  统计信息:`);
    console.log(`    - 总记录数: ${stats.total}`);
    console.log(`    - 有错误的: ${stats.withErrors}`);
    console.log(`    - 缺少URL的: ${stats.withoutUrl}`);
    console.log(`    - 按状态分布:`);
    Object.entries(stats.byStatus).forEach(([status, count]) => {
      console.log(`      - ${status}: ${count}`);
    });

    // 步骤3: 提取有效URL
    console.log('\n步骤3: 提取有效URL');
    console.log('-------------------');
    const urlStrings = reader.extractURLs(records, { 
      status: 'fetched', 
      excludeErrors: true 
    });
    console.log(`✓ 提取了 ${urlStrings.length} 个有效URL\n`);

    if (urlStrings.length === 0) {
      console.error('✗ 没有找到有效的URL，无法继续分析');
      process.exit(1);
    }

    // 步骤4: URL聚类分析
    console.log('步骤4: URL聚类分析');
    console.log('-------------------');
    const analyzer = new URLPatternAnalyzer();
    const startTime = Date.now();
    
    console.log('正在分析URL模式...');
    const clusters = analyzer.clusterURLs(urlStrings);
    const duration = Date.now() - startTime;
    
    console.log(`✓ 聚类完成，用时 ${duration}ms`);
    console.log(`  识别出 ${clusters.length} 个URL模式`);
    
    // 过滤小组
    const filteredClusters = clusters.filter(cluster => cluster.length >= options.minGroup);
    console.log(`  过滤后保留 ${filteredClusters.length} 个模式 (>= ${options.minGroup} URLs)\n`);

    if (filteredClusters.length === 0) {
      console.warn('⚠ 没有符合最小分组大小的模式，降低 --min-group 参数重试');
      process.exit(0);
    }

    // 显示前10个模式
    console.log('  前10个最大的模式:');
    filteredClusters.slice(0, 10).forEach((cluster, i) => {
      console.log(`    ${i + 1}. ${cluster.length} 个URL`);
    });

    // 步骤5: 生成报告
    console.log('\n步骤5: 生成报告');
    console.log('-------------------');
    const generator = new ReportGenerator();
    
    // 生成JSON报告
    console.log('正在生成JSON报告...');
    const jsonReport = generator.generateJSONReport(filteredClusters, { 
      sampleCount: options.samples 
    });
    console.log(`✓ JSON报告生成成功`);
    
    // 生成Markdown报告
    console.log('正在生成Markdown报告...');
    const markdown = generator.generateMarkdownReport(filteredClusters, { 
      sampleCount: options.samples 
    });
    console.log(`✓ Markdown报告生成成功\n`);

    // 步骤6: 保存报告
    console.log('步骤6: 保存报告');
    console.log('-------------------');
    const outputDir = path.resolve(options.output);
    
    // 确保输出目录存在
    await fs.mkdir(outputDir, { recursive: true });
    
    const jsonPath = path.join(outputDir, 'url-patterns.json');
    const mdPath = path.join(outputDir, 'url-patterns.md');
    
    await generator.saveJSONReport(jsonReport, jsonPath);
    console.log(`✓ JSON报告已保存: ${jsonPath}`);
    
    await generator.saveMarkdownReport(markdown, mdPath);
    console.log(`✓ Markdown报告已保存: ${mdPath}\n`);

    // 步骤7: 显示报告摘要
    console.log('=== 分析结果摘要 ===');
    console.log(`总URL数: ${jsonReport.summary.totalUrls}`);
    console.log(`模式数量: ${jsonReport.summary.patternCount}`);
    console.log(`\n前5个最大的模式:`);
    
    jsonReport.patterns.slice(0, 5).forEach((pattern, i) => {
      const percentage = ((pattern.urlCount / jsonReport.summary.totalUrls) * 100).toFixed(1);
      console.log(`\n${i + 1}. ${pattern.name}`);
      console.log(`   路径: ${pattern.pathTemplate}`);
      console.log(`   URL数: ${pattern.urlCount} (${percentage}%)`);
      console.log(`   参数: ${pattern.queryParams.join(', ') || '无'}`);
      console.log(`   示例: ${pattern.samples[0]}`);
    });

    console.log('\n✓ 分析完成！');
    console.log(`\n输出文件:`);
    console.log(`  - ${jsonPath}`);
    console.log(`  - ${mdPath}`);

  } catch (error) {
    console.error('\n✗ 分析失败:', error.message);
    console.error(error.stack);
    process.exit(1);
  }
}

// 运行脚本
if (require.main === module) {
  main().catch(error => {
    console.error('脚本运行失败:', error);
    process.exit(1);
  });
}

module.exports = { main, parseArgs };
