#!/usr/bin/env node
/**
 * 页面模板分析脚本
 * 
 * 分析指定URL模式的页面内容，识别模板内容和独特数据，生成分析报告
 * 
 * 使用方法:
 *   node scripts/analyze-page-template.js [options]
 * 
 * 选项:
 *   --patterns, -p <path>   URL模式文件路径 (默认: stock-crawler/output/lixinger-crawler/url-patterns.json)
 *   --pages, -d <path>      页面目录路径 (默认: stock-crawler/output/lixinger-crawler/pages)
 *   --output, -o <path>     输出目录 (默认: stock-crawler/output/lixinger-crawler)
 *   --pattern-name, -n <name>  只分析指定名称的模式 (可选)
 *   --template-threshold <number>  模板内容阈值 (默认: 0.8)
 *   --unique-threshold <number>    独特内容阈值 (默认: 0.2)
 *   --help, -h              显示帮助信息
 */

const TemplateContentAnalyzer = require('../lib/content-analyzer');
const ConfigLoader = require('../lib/config-loader');
const fs = require('fs').promises;
const path = require('path');

// 解析命令行参数
function parseArgs() {
  const args = process.argv.slice(2);
  const options = {
    patterns: 'stock-crawler/output/lixinger-crawler/url-patterns.json',
    pages: 'stock-crawler/output/lixinger-crawler/pages',
    output: 'stock-crawler/output/lixinger-crawler',
    patternName: null,
    templateThreshold: 0.8,
    uniqueThreshold: 0.2
  };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    
    if (arg === '--help' || arg === '-h') {
      printHelp();
      process.exit(0);
    } else if (arg === '--patterns' || arg === '-p') {
      options.patterns = args[++i];
    } else if (arg === '--pages' || arg === '-d') {
      options.pages = args[++i];
    } else if (arg === '--output' || arg === '-o') {
      options.output = args[++i];
    } else if (arg === '--pattern-name' || arg === '-n') {
      options.patternName = args[++i];
    } else if (arg === '--template-threshold') {
      options.templateThreshold = parseFloat(args[++i]);
    } else if (arg === '--unique-threshold') {
      options.uniqueThreshold = parseFloat(args[++i]);
    }
  }

  return options;
}

function printHelp() {
  console.log(`
页面模板分析脚本

使用方法:
  node scripts/analyze-page-template.js [options]

选项:
  --patterns, -p <path>   URL模式文件路径
                          (默认: stock-crawler/output/lixinger-crawler/url-patterns.json)
  --pages, -d <path>      页面目录路径
                          (默认: stock-crawler/output/lixinger-crawler/pages)
  --output, -o <path>     输出目录
                          (默认: stock-crawler/output/lixinger-crawler)
  --pattern-name, -n <name>  只分析指定名称的模式 (可选)
  --template-threshold <number>  模板内容阈值 (默认: 0.8)
  --unique-threshold <number>    独特内容阈值 (默认: 0.2)
  --help, -h              显示帮助信息

示例:
  # 分析所有模式
  node scripts/analyze-page-template.js

  # 只分析api-doc模式
  node scripts/analyze-page-template.js -n api-doc

  # 自定义阈值
  node scripts/analyze-page-template.js --template-threshold 0.9 --unique-threshold 0.1

  # 指定输入和输出
  node scripts/analyze-page-template.js -p data/url-patterns.json -d data/pages -o output
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
  
  console.log('=== 页面模板分析器 ===\n');
  console.log('配置:');
  console.log(`  URL模式文件: ${options.patterns}`);
  console.log(`  页面目录: ${options.pages}`);
  console.log(`  输出目录: ${options.output}`);
  console.log(`  模板阈值: ${options.templateThreshold}`);
  console.log(`  独特阈值: ${options.uniqueThreshold}`);
  if (options.patternName) {
    console.log(`  指定模式: ${options.patternName}`);
  }
  console.log('');

  try {
    // 步骤1: 检查输入文件
    console.log('步骤1: 检查输入文件');
    console.log('-------------------');
    const patternsPath = path.resolve(options.patterns);
    const pagesDir = path.resolve(options.pages);
    
    try {
      await fs.access(patternsPath);
      console.log(`✓ 找到URL模式文件: ${patternsPath}`);
    } catch (error) {
      console.error(`✗ URL模式文件不存在: ${patternsPath}`);
      process.exit(1);
    }

    try {
      await fs.access(pagesDir);
      console.log(`✓ 找到页面目录: ${pagesDir}\n`);
    } catch (error) {
      console.error(`✗ 页面目录不存在: ${pagesDir}`);
      process.exit(1);
    }

    // 步骤2: 加载URL模式
    console.log('步骤2: 加载URL模式');
    console.log('-------------------');
    const patternsContent = await fs.readFile(patternsPath, 'utf-8');
    const patternsData = JSON.parse(patternsContent);
    const patterns = patternsData.patterns || [];
    
    console.log(`✓ 加载了 ${patterns.length} 个URL模式\n`);

    if (patterns.length === 0) {
      console.error('✗ 没有找到URL模式，无法继续分析');
      process.exit(1);
    }

    // 过滤模式（如果指定了pattern-name）
    let patternsToAnalyze = patterns;
    if (options.patternName) {
      patternsToAnalyze = patterns.filter(p => p.name === options.patternName);
      if (patternsToAnalyze.length === 0) {
        console.error(`✗ 未找到名为 "${options.patternName}" 的模式`);
        console.log('\n可用的模式:');
        patterns.forEach(p => console.log(`  - ${p.name}`));
        process.exit(1);
      }
      console.log(`✓ 将分析模式: ${options.patternName}\n`);
    }

    // 步骤3: 分析每个模式
    console.log('步骤3: 分析模板内容');
    console.log('-------------------');
    const analyzer = new TemplateContentAnalyzer();
    const allResults = [];

    for (let i = 0; i < patternsToAnalyze.length; i++) {
      const pattern = patternsToAnalyze[i];
      console.log(`\n[${i + 1}/${patternsToAnalyze.length}] 分析模式: ${pattern.name}`);
      console.log(`  路径模板: ${pattern.pathTemplate}`);
      console.log(`  URL数量: ${pattern.urlCount}`);

      // 3.1 匹配页面文件
      console.log('  正在匹配页面文件...');
      const matchedFiles = await analyzer.matchPagesToURLs(pattern, pagesDir);
      console.log(`  ✓ 找到 ${matchedFiles.length} 个匹配的页面文件`);

      if (matchedFiles.length === 0) {
        console.log(`  ⚠ 跳过此模式（没有匹配的页面）`);
        continue;
      }

      // 3.2 加载页面内容
      console.log('  正在加载页面内容...');
      const pages = [];
      let loadedCount = 0;
      
      for await (const batch of analyzer.loadMarkdownPages(matchedFiles, { batchSize: 50 })) {
        pages.push(...batch.map(p => p.content));
        loadedCount += batch.length;
        showProgress(loadedCount, matchedFiles.length, '  加载进度');
      }

      console.log(`  ✓ 加载了 ${pages.length} 个页面`);

      // 3.3 执行模板分析
      console.log('  正在分析模板内容...');
      const startTime = Date.now();
      const analysisResult = analyzer.analyzeTemplate(pages, {
        thresholds: {
          template: options.templateThreshold,
          unique: options.uniqueThreshold
        }
      });
      const duration = Date.now() - startTime;

      console.log(`  ✓ 分析完成，用时 ${duration}ms`);
      console.log(`    - 总内容块: ${analysisResult.stats.totalBlocks}`);
      console.log(`    - 模板内容: ${analysisResult.stats.templateBlocks}`);
      console.log(`    - 独特内容: ${analysisResult.stats.uniqueBlocks}`);
      console.log(`    - 混合内容: ${analysisResult.stats.mixedBlocks}`);

      // 保存结果
      allResults.push({
        pattern,
        analysisResult,
        pages
      });
    }

    if (allResults.length === 0) {
      console.log('\n⚠ 没有成功分析任何模式');
      process.exit(0);
    }

    // 步骤4: 生成报告
    console.log('\n步骤4: 生成分析报告');
    console.log('-------------------');
    const outputDir = path.resolve(options.output);
    await fs.mkdir(outputDir, { recursive: true });

    for (const result of allResults) {
      const { pattern, analysisResult, pages } = result;
      
      console.log(`\n正在生成 ${pattern.name} 的报告...`);

      // 4.1 生成JSON报告
      const jsonReport = analyzer.generateAnalysisJSON(analysisResult, pattern);
      const jsonPath = path.join(outputDir, `template-analysis-${pattern.name}.json`);
      await fs.writeFile(jsonPath, JSON.stringify(jsonReport, null, 2), 'utf-8');
      console.log(`  ✓ JSON报告: ${jsonPath}`);

      // 4.2 生成Markdown报告
      const markdownReport = analyzer.generateAnalysisMarkdown(analysisResult, pattern);
      const mdPath = path.join(outputDir, `template-analysis-${pattern.name}.md`);
      await fs.writeFile(mdPath, markdownReport, 'utf-8');
      console.log(`  ✓ Markdown报告: ${mdPath}`);

      // 4.3 生成清洗示例
      const cleaningExamples = analyzer.generateCleaningExamples(
        pages,
        analysisResult.cleaningRules,
        { maxExamples: 3 }
      );
      const examplesPath = path.join(outputDir, `cleaning-examples-${pattern.name}.json`);
      await fs.writeFile(examplesPath, JSON.stringify(cleaningExamples, null, 2), 'utf-8');
      console.log(`  ✓ 清洗示例: ${examplesPath}`);
    }

    // 步骤5: 生成配置文件（JSONL格式）
    console.log('\n步骤5: 生成模板配置文件');
    console.log('-------------------');
    
    const configs = [];

    for (const result of allResults) {
      const { pattern, analysisResult } = result;
      
      // 生成配置对象
      const config = ConfigLoader.generateTemplateConfig(pattern, analysisResult);
      configs.push(config);
    }

    // 保存为JSONL格式
    const configPath = path.join(outputDir, 'template-rules.jsonl');
    const jsonlContent = configs.map(config => JSON.stringify(config)).join('\n');
    await fs.writeFile(configPath, jsonlContent, 'utf-8');
    
    console.log(`✓ 配置文件已保存: ${configPath}`);
    console.log(`  包含 ${configs.length} 个模板配置\n`);

    // 步骤6: 显示摘要
    console.log('=== 分析结果摘要 ===');
    console.log(`分析的模式数: ${allResults.length}`);
    console.log('');

    allResults.forEach((result, index) => {
      const { pattern, analysisResult } = result;
      console.log(`${index + 1}. ${pattern.name}`);
      console.log(`   路径: ${pattern.pathTemplate}`);
      console.log(`   页面数: ${analysisResult.stats.totalPages}`);
      console.log(`   模板内容块: ${analysisResult.stats.templateBlocks}`);
      console.log(`   独特内容块: ${analysisResult.stats.uniqueBlocks}`);
      console.log(`   表格结构: ${analysisResult.stats.tableStructures}`);
      console.log(`   代码块类型: ${analysisResult.stats.codeBlockTypes}`);
      console.log('');
    });

    console.log('✓ 分析完成！');
    console.log(`\n输出文件:`);
    console.log(`  - 配置文件: ${configPath}`);
    allResults.forEach(result => {
      const pattern = result.pattern;
      console.log(`  - ${pattern.name} 报告: template-analysis-${pattern.name}.{json,md}`);
    });

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
