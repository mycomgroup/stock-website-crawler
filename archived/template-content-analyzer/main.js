#!/usr/bin/env node

/**
 * Template Content Analyzer - Main Entry Point
 * 
 * 分析markdown页面内容，识别模板内容和独特数据，生成模板配置文件
 * 
 * 使用方式:
 *   node main.js <urlPatternsFile> <pagesDir> <outputFile> [options]
 * 
 * 参数:
 *   urlPatternsFile  - url-patterns.json文件路径
 *   pagesDir         - pages目录路径
 *   outputFile       - 输出JSONL文件路径
 *   --template-threshold <n>  - 模板内容阈值（默认0.8）
 *   --unique-threshold <n>    - 独特内容阈值（默认0.2）
 *   --sample-urls <urls>      - 可选的样例URL（逗号分隔）
 *   --help                    - 显示帮助信息
 */

const fs = require('fs').promises;
const path = require('path');
const TemplateContentAnalyzer = require('./lib/content-analyzer');
const TemplateConfigGenerator = require('./lib/template-config-generator');

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
  if (args.length < 3) {
    console.error('错误: 缺少必需参数');
    console.error('使用 --help 查看帮助信息');
    process.exit(1);
  }
  
  const config = {
    urlPatternsFile: args[0],
    pagesDir: args[1],
    outputFile: args[2],
    frequencyThresholds: {
      template: 0.8,
      unique: 0.2
    },
    sampleUrls: []
  };
  
  // 解析选项
  for (let i = 3; i < args.length; i++) {
    const arg = args[i];
    
    if (arg === '--template-threshold' && i + 1 < args.length) {
      config.frequencyThresholds.template = parseFloat(args[++i]);
    } else if (arg === '--unique-threshold' && i + 1 < args.length) {
      config.frequencyThresholds.unique = parseFloat(args[++i]);
    } else if (arg === '--sample-urls' && i + 1 < args.length) {
      config.sampleUrls = args[++i].split(',').map(url => url.trim());
    }
  }
  
  return config;
}

/**
 * 显示帮助信息
 */
function showHelp() {
  console.log(`
Template Content Analyzer - 分析模板内容并生成配置文件

使用方式:
  node main.js <urlPatternsFile> <pagesDir> <outputFile> [options]

参数:
  urlPatternsFile        url-patterns.json文件路径
  pagesDir               pages目录路径
  outputFile             输出JSONL文件路径

选项:
  --template-threshold <n>  模板内容阈值（默认0.8）
  --unique-threshold <n>    独特内容阈值（默认0.2）
  --sample-urls <urls>      可选的样例URL（逗号分隔）
  --help, -h                显示此帮助信息

示例:
  # 基本使用
  node main.js url-patterns.json pages/ template-rules.jsonl

  # 自定义阈值
  node main.js url-patterns.json pages/ template-rules.jsonl --template-threshold 0.9 --unique-threshold 0.1

  # 提供样例URL进行验证
  node main.js url-patterns.json pages/ template-rules.jsonl --sample-urls "https://example.com/api/doc,https://example.com/api/index"

输出:
  - JSONL配置文件: 每行一个TemplateConfig对象
  - 包含extractors和filters配置
  - 可直接用于TemplateParser
  `);
}

/**
 * 加载URL模式文件
 */
async function loadURLPatterns(filePath) {
  try {
    const content = await fs.readFile(filePath, 'utf-8');
    const data = JSON.parse(content);
    
    // 支持两种格式：
    // 1. { patterns: [...] }
    // 2. [...]
    if (data.patterns && Array.isArray(data.patterns)) {
      return data.patterns;
    } else if (Array.isArray(data)) {
      return data;
    } else {
      throw new Error('Invalid URL patterns file format');
    }
  } catch (error) {
    throw new Error(`Failed to load URL patterns: ${error.message}`);
  }
}

/**
 * 匹配URL模式对应的markdown文件
 */
async function matchPagesToPattern(urlPattern, pagesDir, analyzer) {
  try {
    const matchedFiles = await analyzer.matchPagesToURLs(urlPattern, pagesDir);
    return matchedFiles;
  } catch (error) {
    console.warn(`  警告: 匹配文件失败 - ${error.message}`);
    return [];
  }
}

/**
 * 加载页面内容
 */
async function loadPages(filePaths, analyzer) {
  const pages = [];
  
  for await (const batch of analyzer.loadMarkdownPages(filePaths, { batchSize: 100 })) {
    batch.forEach(page => {
      pages.push(page.content);
    });
  }
  
  return pages;
}

/**
 * 分析单个模板
 */
async function analyzePattern(urlPattern, pagesDir, analyzer, generator, options) {
  console.log(`\n分析模板: ${urlPattern.name}`);
  console.log('-------------------');
  console.log(`  路径模板: ${urlPattern.pathTemplate}`);
  console.log(`  URL数量: ${urlPattern.urlCount || 0}`);
  
  // 1. 匹配markdown文件
  console.log(`  步骤1: 匹配markdown文件...`);
  const matchedFiles = await matchPagesToPattern(urlPattern, pagesDir, analyzer);
  
  if (matchedFiles.length === 0) {
    console.log(`  ⚠ 未找到匹配的文件，跳过此模板`);
    return null;
  }
  
  console.log(`  ✓ 找到 ${matchedFiles.length} 个匹配文件`);
  
  // 2. 加载页面内容
  console.log(`  步骤2: 加载页面内容...`);
  const pages = await loadPages(matchedFiles, analyzer);
  console.log(`  ✓ 加载了 ${pages.length} 个页面`);
  
  if (pages.length === 0) {
    console.log(`  ⚠ 页面内容为空，跳过此模板`);
    return null;
  }
  
  // 3. 分析模板
  console.log(`  步骤3: 分析模板内容...`);
  const startTime = Date.now();
  const analysisResult = analyzer.analyzeTemplate(pages, {
    thresholds: options.frequencyThresholds
  });
  const duration = Date.now() - startTime;
  
  console.log(`  ✓ 分析完成，用时 ${duration}ms`);
  console.log(`    - 总内容块: ${analysisResult.stats.totalBlocks}`);
  console.log(`    - 模板内容: ${analysisResult.stats.templateBlocks}`);
  console.log(`    - 独特内容: ${analysisResult.stats.uniqueBlocks}`);
  console.log(`    - 表格结构: ${analysisResult.stats.tableStructures}`);
  console.log(`    - 代码块类型: ${analysisResult.stats.codeBlockTypes}`);
  
  // 4. 生成配置
  console.log(`  步骤4: 生成配置...`);
  const config = generator.generateConfig(urlPattern, analysisResult);
  console.log(`  ✓ 配置生成成功`);
  console.log(`    - 提取器数量: ${config.extractors.length}`);
  console.log(`    - 过滤器数量: ${config.filters.length}`);
  
  return config;
}

/**
 * 主函数
 */
async function main() {
  try {
    // 解析参数
    const config = parseArgs();
    
    console.log('=== Template Content Analyzer ===\n');
    console.log(`URL模式文件: ${config.urlPatternsFile}`);
    console.log(`Pages目录: ${config.pagesDir}`);
    console.log(`输出文件: ${config.outputFile}`);
    console.log(`模板阈值: ${config.frequencyThresholds.template}`);
    console.log(`独特阈值: ${config.frequencyThresholds.unique}`);
    if (config.sampleUrls.length > 0) {
      console.log(`样例URL: ${config.sampleUrls.length} 个`);
    }
    console.log('');
    
    // 步骤1: 加载URL模式
    console.log('步骤1: 加载URL模式');
    console.log('-------------------');
    const urlPatterns = await loadURLPatterns(config.urlPatternsFile);
    console.log(`✓ 加载了 ${urlPatterns.length} 个URL模式`);
    
    if (urlPatterns.length === 0) {
      console.error('错误: 没有找到URL模式');
      process.exit(1);
    }
    
    // 步骤2: 初始化分析器和生成器
    console.log('\n步骤2: 初始化分析器');
    console.log('-------------------');
    const analyzer = new TemplateContentAnalyzer();
    const generator = new TemplateConfigGenerator();
    console.log('✓ 分析器初始化完成');
    
    // 步骤3: 分析每个模板
    console.log('\n步骤3: 分析模板');
    console.log('===================');
    
    const configs = [];
    const results = {
      total: urlPatterns.length,
      success: 0,
      skipped: 0,
      failed: 0
    };
    
    for (const urlPattern of urlPatterns) {
      try {
        const templateConfig = await analyzePattern(
          urlPattern,
          config.pagesDir,
          analyzer,
          generator,
          config
        );
        
        if (templateConfig) {
          configs.push(templateConfig);
          results.success++;
        } else {
          results.skipped++;
        }
      } catch (error) {
        console.error(`  ✗ 分析失败: ${error.message}`);
        results.failed++;
      }
    }
    
    // 步骤4: 保存配置
    console.log('\n步骤4: 保存配置');
    console.log('-------------------');
    
    if (configs.length === 0) {
      console.error('错误: 没有生成任何配置');
      process.exit(1);
    }
    
    await generator.saveAsJSONL(configs, config.outputFile);
    console.log(`✓ 配置已保存到: ${config.outputFile}`);
    
    // 显示摘要
    console.log('\n=== 分析完成 ===');
    console.log(`总模式数: ${results.total}`);
    console.log(`成功: ${results.success}`);
    console.log(`跳过: ${results.skipped}`);
    console.log(`失败: ${results.failed}`);
    
    if (configs.length > 0) {
      console.log(`\n生成的配置:`);
      configs.forEach((cfg, i) => {
        console.log(`${i + 1}. ${cfg.name}`);
        console.log(`   - 提取器: ${cfg.extractors.length}`);
        console.log(`   - 过滤器: ${cfg.filters.length}`);
        console.log(`   - 页面数: ${cfg.metadata.pageCount}`);
      });
    }
    
    // 统计信息
    const totalExtractors = configs.reduce((sum, cfg) => sum + cfg.extractors.length, 0);
    const totalFilters = configs.reduce((sum, cfg) => sum + cfg.filters.length, 0);
    
    console.log('\n✓ 分析成功完成！');
    console.log(`\n统计信息:`);
    console.log(`  - 配置数量: ${configs.length}`);
    console.log(`  - 总提取器: ${totalExtractors}`);
    console.log(`  - 总过滤器: ${totalFilters}`);
    console.log(`\n输出文件: ${config.outputFile}`);
    
    // 返回结果（供程序化调用）
    return {
      success: true,
      configFile: config.outputFile,
      configsGenerated: configs.length,
      totalExtractors,
      totalFilters,
      configs: configs.map(cfg => ({
        name: cfg.name,
        pageCount: cfg.metadata.pageCount,
        extractorsGenerated: cfg.extractors.length,
        filtersGenerated: cfg.filters.length
      }))
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
