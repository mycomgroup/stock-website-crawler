#!/usr/bin/env node
/**
 * 模板配置生成脚本
 * 
 * 根据URL模式和页面分析结果，生成JSONL格式的模板配置文件
 * 
 * 使用方法:
 *   node scripts/generate-template-config.js [options]
 * 
 * 选项:
 *   --patterns, -p <path>   URL模式文件路径 (默认: stock-crawler/output/lixinger-crawler/url-patterns.json)
 *   --pages, -d <path>      页面目录路径 (默认: stock-crawler/output/lixinger-crawler/pages)
 *   --output, -o <path>     输出文件路径 (默认: stock-crawler/output/lixinger-crawler/template-rules.jsonl)
 *   --pattern-name, -n <name>  只生成指定名称的模式配置 (可选)
 *   --template-threshold <number>  模板内容阈值 (默认: 0.8)
 *   --unique-threshold <number>    独特内容阈值 (默认: 0.2)
 *   --yes, -y               跳过确认提示
 *   --help, -h              显示帮助信息
 */

const TemplateContentAnalyzer = require('../lib/content-analyzer');
const ConfigLoader = require('../lib/config-loader');
const fs = require('fs').promises;
const path = require('path');
const readline = require('readline');

// 解析命令行参数
function parseArgs() {
  const args = process.argv.slice(2);
  const options = {
    patterns: 'stock-crawler/output/lixinger-crawler/url-patterns.json',
    pages: 'stock-crawler/output/lixinger-crawler/pages',
    output: 'stock-crawler/output/lixinger-crawler/template-rules.jsonl',
    patternName: null,
    templateThreshold: 0.8,
    uniqueThreshold: 0.2,
    skipConfirm: false
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
    } else if (arg === '--yes' || arg === '-y') {
      options.skipConfirm = true;
    }
  }

  return options;
}

function printHelp() {
  console.log(`
模板配置生成脚本

使用方法:
  node scripts/generate-template-config.js [options]

选项:
  --patterns, -p <path>   URL模式文件路径
                          (默认: stock-crawler/output/lixinger-crawler/url-patterns.json)
  --pages, -d <path>      页面目录路径
                          (默认: stock-crawler/output/lixinger-crawler/pages)
  --output, -o <path>     输出文件路径
                          (默认: stock-crawler/output/lixinger-crawler/template-rules.jsonl)
  --pattern-name, -n <name>  只生成指定名称的模式配置 (可选)
  --template-threshold <number>  模板内容阈值 (默认: 0.8)
  --unique-threshold <number>    独特内容阈值 (默认: 0.2)
  --yes, -y               跳过确认提示
  --help, -h              显示帮助信息

示例:
  # 生成所有模式的配置
  node scripts/generate-template-config.js

  # 只生成api-doc模式的配置
  node scripts/generate-template-config.js -n api-doc

  # 自定义输出路径
  node scripts/generate-template-config.js -o output/my-rules.jsonl

  # 跳过确认提示
  node scripts/generate-template-config.js -y

  # 自定义阈值
  node scripts/generate-template-config.js --template-threshold 0.9 --unique-threshold 0.1
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

// 交互式确认
async function confirm(question) {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });

  return new Promise((resolve) => {
    rl.question(question, (answer) => {
      rl.close();
      resolve(answer.toLowerCase() === 'y' || answer.toLowerCase() === 'yes');
    });
  });
}

async function main() {
  const options = parseArgs();
  
  console.log('=== 模板配置生成器 ===\n');
  console.log('配置:');
  console.log(`  URL模式文件: ${options.patterns}`);
  console.log(`  页面目录: ${options.pages}`);
  console.log(`  输出文件: ${options.output}`);
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
    const outputPath = path.resolve(options.output);
    
    try {
      await fs.access(patternsPath);
      console.log(`✓ 找到URL模式文件: ${patternsPath}`);
    } catch (error) {
      console.error(`✗ URL模式文件不存在: ${patternsPath}`);
      process.exit(1);
    }

    try {
      await fs.access(pagesDir);
      console.log(`✓ 找到页面目录: ${pagesDir}`);
    } catch (error) {
      console.error(`✗ 页面目录不存在: ${pagesDir}`);
      process.exit(1);
    }

    // 检查输出文件是否已存在
    let outputExists = false;
    try {
      await fs.access(outputPath);
      outputExists = true;
      console.log(`⚠ 输出文件已存在: ${outputPath}`);
    } catch (error) {
      console.log(`✓ 输出文件路径: ${outputPath}`);
    }
    console.log('');

    // 步骤2: 加载URL模式
    console.log('步骤2: 加载URL模式');
    console.log('-------------------');
    const patternsContent = await fs.readFile(patternsPath, 'utf-8');
    const patternsData = JSON.parse(patternsContent);
    const patterns = patternsData.patterns || [];
    
    console.log(`✓ 加载了 ${patterns.length} 个URL模式\n`);

    if (patterns.length === 0) {
      console.error('✗ 没有找到URL模式，无法继续生成');
      process.exit(1);
    }

    // 过滤模式（如果指定了pattern-name）
    let patternsToGenerate = patterns;
    if (options.patternName) {
      patternsToGenerate = patterns.filter(p => p.name === options.patternName);
      if (patternsToGenerate.length === 0) {
        console.error(`✗ 未找到名为 "${options.patternName}" 的模式`);
        console.log('\n可用的模式:');
        patterns.forEach(p => console.log(`  - ${p.name}`));
        process.exit(1);
      }
      console.log(`✓ 将生成模式: ${options.patternName}\n`);
    }

    // 步骤3: 显示生成计划
    console.log('步骤3: 生成计划');
    console.log('-------------------');
    console.log(`将生成 ${patternsToGenerate.length} 个模板配置:`);
    patternsToGenerate.forEach((pattern, index) => {
      console.log(`  ${index + 1}. ${pattern.name} (${pattern.urlCount} URLs)`);
    });
    console.log('');

    // 交互式确认
    if (!options.skipConfirm) {
      if (outputExists) {
        const shouldOverwrite = await confirm('输出文件已存在，是否覆盖？ (y/n): ');
        if (!shouldOverwrite) {
          console.log('操作已取消');
          process.exit(0);
        }
      }

      const shouldContinue = await confirm('是否继续生成配置？ (y/n): ');
      if (!shouldContinue) {
        console.log('操作已取消');
        process.exit(0);
      }
      console.log('');
    }

    // 步骤4: 分析并生成配置
    console.log('步骤4: 分析并生成配置');
    console.log('-------------------');
    const analyzer = new TemplateContentAnalyzer();
    const configs = [];
    const generationReport = {
      totalPatterns: patternsToGenerate.length,
      successCount: 0,
      failedCount: 0,
      skippedCount: 0,
      details: []
    };

    for (let i = 0; i < patternsToGenerate.length; i++) {
      const pattern = patternsToGenerate[i];
      console.log(`\n[${i + 1}/${patternsToGenerate.length}] 处理模式: ${pattern.name}`);
      console.log(`  路径模板: ${pattern.pathTemplate}`);
      console.log(`  URL数量: ${pattern.urlCount}`);

      const patternDetail = {
        name: pattern.name,
        pathTemplate: pattern.pathTemplate,
        urlCount: pattern.urlCount,
        status: 'pending',
        error: null
      };

      try {
        // 4.1 匹配页面文件
        console.log('  正在匹配页面文件...');
        const matchedFiles = await analyzer.matchPagesToURLs(pattern, pagesDir);
        console.log(`  ✓ 找到 ${matchedFiles.length} 个匹配的页面文件`);

        if (matchedFiles.length === 0) {
          console.log(`  ⚠ 跳过此模式（没有匹配的页面）`);
          patternDetail.status = 'skipped';
          patternDetail.error = 'No matching pages found';
          generationReport.skippedCount++;
          generationReport.details.push(patternDetail);
          continue;
        }

        patternDetail.matchedFiles = matchedFiles.length;

        // 4.2 加载页面内容
        console.log('  正在加载页面内容...');
        const pages = [];
        let loadedCount = 0;
        
        for await (const batch of analyzer.loadMarkdownPages(matchedFiles, { batchSize: 50 })) {
          pages.push(...batch.map(p => p.content));
          loadedCount += batch.length;
          showProgress(loadedCount, matchedFiles.length, '  加载进度');
        }

        console.log(`  ✓ 加载了 ${pages.length} 个页面`);

        // 4.3 执行模板分析
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

        patternDetail.analysisTime = duration;
        patternDetail.stats = analysisResult.stats;

        // 4.4 生成配置对象
        console.log('  正在生成配置...');
        const config = ConfigLoader.generateTemplateConfig(pattern, analysisResult);
        configs.push(config);

        console.log(`  ✓ 配置生成成功`);
        console.log(`    - 提取器数量: ${config.extractors.length}`);
        console.log(`    - 过滤器数量: ${config.filters.length}`);

        patternDetail.status = 'success';
        patternDetail.extractorsCount = config.extractors.length;
        patternDetail.filtersCount = config.filters.length;
        generationReport.successCount++;

      } catch (error) {
        console.error(`  ✗ 处理失败: ${error.message}`);
        patternDetail.status = 'failed';
        patternDetail.error = error.message;
        generationReport.failedCount++;
      }

      generationReport.details.push(patternDetail);
    }

    if (configs.length === 0) {
      console.log('\n⚠ 没有成功生成任何配置');
      process.exit(0);
    }

    // 步骤5: 保存配置文件
    console.log('\n步骤5: 保存配置文件');
    console.log('-------------------');
    
    // 确保输出目录存在
    const outputDir = path.dirname(outputPath);
    await fs.mkdir(outputDir, { recursive: true });

    // 保存为JSONL格式
    const jsonlContent = configs.map(config => JSON.stringify(config)).join('\n');
    await fs.writeFile(outputPath, jsonlContent, 'utf-8');
    
    console.log(`✓ 配置文件已保存: ${outputPath}`);
    console.log(`  包含 ${configs.length} 个模板配置\n`);

    // 步骤6: 生成报告
    console.log('步骤6: 生成报告');
    console.log('-------------------');
    
    const reportPath = outputPath.replace('.jsonl', '-report.json');
    const reportData = {
      generatedAt: new Date().toISOString(),
      options: {
        patterns: options.patterns,
        pages: options.pages,
        output: options.output,
        templateThreshold: options.templateThreshold,
        uniqueThreshold: options.uniqueThreshold
      },
      summary: {
        totalPatterns: generationReport.totalPatterns,
        successCount: generationReport.successCount,
        failedCount: generationReport.failedCount,
        skippedCount: generationReport.skippedCount,
        totalExtractors: configs.reduce((sum, c) => sum + c.extractors.length, 0),
        totalFilters: configs.reduce((sum, c) => sum + c.filters.length, 0)
      },
      details: generationReport.details
    };

    await fs.writeFile(reportPath, JSON.stringify(reportData, null, 2), 'utf-8');
    console.log(`✓ 生成报告已保存: ${reportPath}\n`);

    // 步骤7: 显示摘要
    console.log('=== 生成结果摘要 ===');
    console.log(`处理的模式数: ${generationReport.totalPatterns}`);
    console.log(`成功: ${generationReport.successCount}`);
    console.log(`失败: ${generationReport.failedCount}`);
    console.log(`跳过: ${generationReport.skippedCount}`);
    console.log('');

    if (generationReport.successCount > 0) {
      console.log('成功生成的配置:');
      generationReport.details
        .filter(d => d.status === 'success')
        .forEach((detail, index) => {
          console.log(`  ${index + 1}. ${detail.name}`);
          console.log(`     路径: ${detail.pathTemplate}`);
          console.log(`     页面数: ${detail.matchedFiles}`);
          console.log(`     提取器: ${detail.extractorsCount}`);
          console.log(`     过滤器: ${detail.filtersCount}`);
          console.log(`     分析时间: ${detail.analysisTime}ms`);
        });
      console.log('');
    }

    if (generationReport.failedCount > 0) {
      console.log('失败的模式:');
      generationReport.details
        .filter(d => d.status === 'failed')
        .forEach((detail, index) => {
          console.log(`  ${index + 1}. ${detail.name}: ${detail.error}`);
        });
      console.log('');
    }

    if (generationReport.skippedCount > 0) {
      console.log('跳过的模式:');
      generationReport.details
        .filter(d => d.status === 'skipped')
        .forEach((detail, index) => {
          console.log(`  ${index + 1}. ${detail.name}: ${detail.error}`);
        });
      console.log('');
    }

    console.log('✓ 配置生成完成！');
    console.log(`\n输出文件:`);
    console.log(`  - 配置文件: ${outputPath}`);
    console.log(`  - 生成报告: ${reportPath}`);

  } catch (error) {
    console.error('\n✗ 生成失败:', error.message);
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
