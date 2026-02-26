#!/usr/bin/env node

/**
 * Template Content Analyzer - Enhanced Runner
 * 
 * 简化的运行脚本，自动处理文件路径和输出结构
 * 
 * 使用方式:
 *   node run-skill.js <projectName> [options]
 * 
 * 示例:
 *   node run-skill.js lixinger-crawler
 *   node run-skill.js lixinger-crawler --template-threshold 0.9
 */

const fs = require('fs').promises;
const path = require('path');
const { execSync } = require('child_process');

/**
 * 解析命令行参数
 */
function parseArgs() {
  const args = process.argv.slice(2);
  
  if (args.length === 0 || args.includes('--help') || args.includes('-h')) {
    showHelp();
    process.exit(args.length === 0 ? 1 : 0);
  }
  
  const config = {
    projectName: args[0],
    templateThreshold: 0.8,
    uniqueThreshold: 0.2,
    sampleUrls: []
  };
  
  // 解析选项
  for (let i = 1; i < args.length; i++) {
    const arg = args[i];
    
    if (arg === '--template-threshold' && i + 1 < args.length) {
      config.templateThreshold = parseFloat(args[++i]);
    } else if (arg === '--unique-threshold' && i + 1 < args.length) {
      config.uniqueThreshold = parseFloat(args[++i]);
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
Template Content Analyzer - Enhanced Runner

使用方式:
  node run-skill.js <projectName> [options]

参数:
  projectName               项目名称（对应output目录下的子目录）

选项:
  --template-threshold <n>  模板内容阈值（默认0.8）
  --unique-threshold <n>    独特内容阈值（默认0.2）
  --sample-urls <urls>      可选的样例URL（逗号分隔）
  --help, -h                显示此帮助信息

示例:
  # 基本使用
  node run-skill.js lixinger-crawler

  # 自定义阈值
  node run-skill.js lixinger-crawler --template-threshold 0.9

输出结构:
  output/<projectName>/
    ├── url-patterns.json          (输入：URL模式文件)
    ├── pages/                     (输入：markdown页面)
    └── templates/                 (输出：模板配置)
        ├── template-summary.json  (汇总文件)
        ├── analytics-chart-maker.json
        ├── detail-sz.json
        └── ...
  `);
}

/**
 * 查找项目目录
 */
async function findProjectDir(projectName) {
  // 尝试多个可能的位置
  const possiblePaths = [
    path.join(process.cwd(), 'output', projectName),
    path.join(process.cwd(), '..', 'output', projectName),
    path.join(process.cwd(), '..', '..', 'output', projectName),
    path.join(process.cwd(), 'stock-crawler', 'output', projectName),
    path.join(process.cwd(), '..', 'stock-crawler', 'output', projectName)
  ];
  
  for (const p of possiblePaths) {
    try {
      await fs.access(p);
      return p;
    } catch (error) {
      // 继续尝试下一个路径
    }
  }
  
  throw new Error(`找不到项目目录: ${projectName}\n尝试过的路径:\n${possiblePaths.map(p => `  - ${p}`).join('\n')}`);
}

/**
 * 加载URL模式
 */
async function loadURLPatterns(filePath) {
  const content = await fs.readFile(filePath, 'utf-8');
  const data = JSON.parse(content);
  
  if (data.patterns && Array.isArray(data.patterns)) {
    return data.patterns;
  } else if (Array.isArray(data)) {
    return data;
  } else {
    throw new Error('Invalid URL patterns file format');
  }
}

/**
 * 保存单个模板配置
 */
async function saveTemplateConfig(config, outputDir) {
  const filename = `${config.name}.json`;
  const filepath = path.join(outputDir, filename);
  await fs.writeFile(filepath, JSON.stringify(config, null, 2), 'utf-8');
  return filename;
}

/**
 * 生成汇总文件
 */
async function generateSummary(configs, outputDir, projectName) {
  const summary = {
    projectName,
    generatedAt: new Date().toISOString(),
    totalTemplates: configs.length,
    templates: configs.map(cfg => ({
      name: cfg.name,
      description: cfg.description || '',
      file: `${cfg.name}.json`,
      pageCount: cfg.metadata?.pageCount || 0,
      extractors: cfg.extractors.length,
      filters: cfg.filters.length,
      urlPattern: cfg.urlPattern || cfg.pathTemplate || ''
    })),
    statistics: {
      totalExtractors: configs.reduce((sum, cfg) => sum + cfg.extractors.length, 0),
      totalFilters: configs.reduce((sum, cfg) => sum + cfg.filters.length, 0),
      totalPages: configs.reduce((sum, cfg) => sum + (cfg.metadata?.pageCount || 0), 0),
      avgExtractorsPerTemplate: 0,
      avgFiltersPerTemplate: 0
    }
  };
  
  if (configs.length > 0) {
    summary.statistics.avgExtractorsPerTemplate = 
      (summary.statistics.totalExtractors / configs.length).toFixed(2);
    summary.statistics.avgFiltersPerTemplate = 
      (summary.statistics.totalFilters / configs.length).toFixed(2);
  }
  
  const filepath = path.join(outputDir, 'template-summary.json');
  await fs.writeFile(filepath, JSON.stringify(summary, null, 2), 'utf-8');
  
  return summary;
}

/**
 * 主函数
 */
async function main() {
  try {
    const config = parseArgs();
    
    console.log('=== Template Content Analyzer - Enhanced Runner ===\n');
    console.log(`Project: ${config.projectName}`);
    console.log(`Template Threshold: ${config.templateThreshold}`);
    console.log(`Unique Threshold: ${config.uniqueThreshold}`);
    console.log('');
    
    // Step 1: 定位项目目录
    console.log('Step 1: Locating project directory...');
    const projectDir = await findProjectDir(config.projectName);
    console.log(`✓ Found: ${projectDir}`);
    
    // Step 2: 检查必需文件
    console.log('\nStep 2: Checking required files...');
    const urlPatternsFile = path.join(projectDir, 'url-patterns.json');
    const pagesDir = path.join(projectDir, 'pages');
    
    try {
      await fs.access(urlPatternsFile);
      console.log(`✓ URL patterns file: ${urlPatternsFile}`);
    } catch (error) {
      throw new Error(`URL patterns file not found: ${urlPatternsFile}`);
    }
    
    try {
      await fs.access(pagesDir);
      console.log(`✓ Pages directory: ${pagesDir}`);
    } catch (error) {
      throw new Error(`Pages directory not found: ${pagesDir}`);
    }
    
    // Step 3: 创建输出目录
    console.log('\nStep 3: Creating output directory...');
    const templatesDir = path.join(projectDir, 'templates');
    await fs.mkdir(templatesDir, { recursive: true });
    console.log(`✓ Templates directory: ${templatesDir}`);
    
    // Step 4: 加载URL模式
    console.log('\nStep 4: Loading URL patterns...');
    const urlPatterns = await loadURLPatterns(urlPatternsFile);
    console.log(`✓ Loaded ${urlPatterns.length} URL patterns`);
    
    // Step 5: 运行分析
    console.log('\nStep 5: Running analysis...');
    console.log('This may take a while...\n');
    
    const TemplateContentAnalyzer = require('./lib/content-analyzer');
    const TemplateConfigGenerator = require('./lib/template-config-generator');
    
    const analyzer = new TemplateContentAnalyzer();
    const generator = new TemplateConfigGenerator();
    
    const configs = [];
    const results = {
      total: urlPatterns.length,
      success: 0,
      skipped: 0,
      failed: 0
    };
    
    for (let i = 0; i < urlPatterns.length; i++) {
      const urlPattern = urlPatterns[i];
      const progress = `[${i + 1}/${urlPatterns.length}]`;
      
      try {
        console.log(`${progress} Analyzing: ${urlPattern.name}`);
        
        // 匹配文件
        const matchedFiles = await analyzer.matchPagesToURLs(urlPattern, pagesDir);
        
        if (matchedFiles.length === 0) {
          console.log(`  ⚠ No matching files, skipped`);
          results.skipped++;
          continue;
        }
        
        console.log(`  Found ${matchedFiles.length} files`);
        
        // 加载页面
        const pages = [];
        for await (const batch of analyzer.loadMarkdownPages(matchedFiles, { batchSize: 100 })) {
          batch.forEach(page => pages.push(page.content));
        }
        
        if (pages.length === 0) {
          console.log(`  ⚠ No page content, skipped`);
          results.skipped++;
          continue;
        }
        
        // 分析模板
        const analysisResult = analyzer.analyzeTemplate(pages, {
          thresholds: {
            template: config.templateThreshold,
            unique: config.uniqueThreshold
          }
        });
        
        // 生成配置
        const templateConfig = generator.generateConfig(urlPattern, analysisResult);
        
        // 添加描述（如果有）
        if (urlPattern.description) {
          templateConfig.description = urlPattern.description;
        }
        
        configs.push(templateConfig);
        results.success++;
        
        console.log(`  ✓ Generated config: ${templateConfig.extractors.length} extractors, ${templateConfig.filters.length} filters`);
        
      } catch (error) {
        console.error(`  ✗ Failed: ${error.message}`);
        results.failed++;
      }
    }
    
    // Step 6: 保存配置文件
    console.log('\nStep 6: Saving template configs...');
    
    if (configs.length === 0) {
      console.error('✗ No configs generated');
      process.exit(1);
    }
    
    for (const cfg of configs) {
      const filename = await saveTemplateConfig(cfg, templatesDir);
      console.log(`  ✓ Saved: ${filename}`);
    }
    
    // Step 7: 生成汇总文件
    console.log('\nStep 7: Generating summary...');
    const summary = await generateSummary(configs, templatesDir, config.projectName);
    console.log(`✓ Summary saved: template-summary.json`);
    
    // 显示结果
    console.log('\n=== Analysis Complete ===\n');
    console.log(`Total patterns: ${results.total}`);
    console.log(`Success: ${results.success}`);
    console.log(`Skipped: ${results.skipped}`);
    console.log(`Failed: ${results.failed}`);
    
    console.log('\nStatistics:');
    console.log(`  - Total templates: ${summary.totalTemplates}`);
    console.log(`  - Total extractors: ${summary.statistics.totalExtractors}`);
    console.log(`  - Total filters: ${summary.statistics.totalFilters}`);
    console.log(`  - Total pages analyzed: ${summary.statistics.totalPages}`);
    console.log(`  - Avg extractors/template: ${summary.statistics.avgExtractorsPerTemplate}`);
    console.log(`  - Avg filters/template: ${summary.statistics.avgFiltersPerTemplate}`);
    
    console.log('\nOutput directory:');
    console.log(`  ${templatesDir}`);
    console.log('\nFiles generated:');
    console.log(`  - template-summary.json (汇总文件)`);
    console.log(`  - ${configs.length} template config files`);
    
    console.log('\n✓ All done!');
    
  } catch (error) {
    console.error('\n✗ Error:', error.message);
    if (process.env.DEBUG) {
      console.error(error.stack);
    }
    process.exit(1);
  }
}

// 运行
if (require.main === module) {
  main().catch(error => {
    console.error('Fatal error:', error);
    process.exit(1);
  });
}

module.exports = main;
