#!/usr/bin/env node

/**
 * URL Pattern Analyzer - Enhanced Runner
 * 
 * 通过项目名自动运行skill，并生成详细的Markdown统计报告
 * 
 * 使用方式:
 *   node run-skill.js <projectName> [options]
 * 
 * 示例:
 *   node run-skill.js lixinger-crawler
 *   node run-skill.js lixinger-crawler --min-group-size 10 --max-patterns 20
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

/**
 * 解析命令行参数
 */
function parseArgs() {
  const args = process.argv.slice(2);
  
  if (args.length === 0 || args.includes('--help') || args.includes('-h')) {
    showHelp();
    process.exit(0);
  }
  
  const config = {
    projectName: args[0],
    minGroupSize: 5,
    maxPatterns: null,
    sampleCount: 5,
    generateMarkdown: true,
    // 细分控制参数
    refineMaxValues: 8,
    refineMinCount: 10,
    refineMinGroups: 2,
    // 严格模式参数
    strictTopN: 0,
    strictMatchRatio: 0.8
  };
  
  // 解析选项
  for (let i = 1; i < args.length; i++) {
    const arg = args[i];
    
    if (arg === '--min-group-size' && i + 1 < args.length) {
      config.minGroupSize = parseInt(args[++i], 10);
    } else if (arg === '--max-patterns' && i + 1 < args.length) {
      config.maxPatterns = parseInt(args[++i], 10);
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
    } else if (arg === '--no-markdown') {
      config.generateMarkdown = false;
    }
  }
  
  return config;
}

/**
 * 显示帮助信息
 */
function showHelp() {
  console.log(`
URL Pattern Analyzer - Enhanced Runner

通过项目名自动运行skill，并生成详细的Markdown统计报告

使用方式:
  node run-skill.js <projectName> [options]

参数:
  projectName            项目名称（如: lixinger-crawler）

基础选项:
  --min-group-size <n>   最小分组大小（默认5）
  --max-patterns <n>     最大模式数量（默认无限制）
  --sample-count <n>     每个模式的示例URL数量（默认5）
  --no-markdown          不生成Markdown报告

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
  node run-skill.js lixinger-crawler

  # 自定义基础参数
  node run-skill.js lixinger-crawler --min-group-size 10 --max-patterns 20

  # 更激进的细分（生成更多细粒度的模式）
  node run-skill.js lixinger-crawler --refine-max-values 10 --refine-min-count 5

  # 更保守的细分（生成更少粗粒度的模式）
  node run-skill.js lixinger-crawler --refine-max-values 5 --refine-min-count 20

  # 组合使用
  node run-skill.js lixinger-crawler --min-group-size 15 --refine-max-values 6 --refine-min-count 15

参数调优建议:
  
  如果模式太多（过度细分）:
    - 增加 min-group-size (如 10 -> 15)
    - 减少 refine-max-values (如 8 -> 5)
    - 增加 refine-min-count (如 10 -> 15)
    - 增加 refine-min-groups (如 2 -> 3)
  
  如果模式太少（细分不足）:
    - 减少 min-group-size (如 10 -> 5)
    - 增加 refine-max-values (如 8 -> 12)
    - 减少 refine-min-count (如 10 -> 5)
    - 减少 refine-min-groups (如 2 -> 1)
  
  如果某些模式混合了不同类型的URL:
    - 增加 refine-max-values 允许更多值被细分
    - 减少 refine-min-count 允许更小的组被单独分出来

输出:
  - JSON报告: stock-crawler/output/{projectName}/url-patterns.json
  - Markdown报告: stock-crawler/output/{projectName}/url-patterns.md
  - 统计报告: stock-crawler/output/{projectName}/url-patterns-stats.md
  `);
}

/**
 * 查找项目的links文件
 */
function findLinksFile(projectName) {
  const baseDir = path.resolve(__dirname, '../../stock-crawler/output');
  const projectDir = path.join(baseDir, projectName);
  const linksFile = path.join(projectDir, 'links.txt');
  
  if (!fs.existsSync(linksFile)) {
    throw new Error(`Links file not found: ${linksFile}`);
  }
  
  return linksFile;
}

/**
 * 生成输出文件路径
 */
function getOutputPaths(projectName) {
  const baseDir = path.resolve(__dirname, '../../stock-crawler/output');
  const projectDir = path.join(baseDir, projectName);
  
  return {
    json: path.join(projectDir, 'url-patterns.json'),
    markdown: path.join(projectDir, 'url-patterns.md'),
    stats: path.join(projectDir, 'url-patterns-stats.md')
  };
}

/**
 * 运行main.js
 */
function runAnalysis(linksFile, outputFile, config) {
  const mainScript = path.join(__dirname, 'main.js');
  
  let cmd = `node "${mainScript}" "${linksFile}" "${outputFile}"`;
  cmd += ` --min-group-size ${config.minGroupSize}`;
  cmd += ` --sample-count ${config.sampleCount}`;
  cmd += ` --refine-max-values ${config.refineMaxValues}`;
  cmd += ` --refine-min-count ${config.refineMinCount}`;
  cmd += ` --refine-min-groups ${config.refineMinGroups}`;
  cmd += ` --strict-top-n ${config.strictTopN}`;
  cmd += ` --strict-match-ratio ${config.strictMatchRatio}`;
  
  if (config.generateMarkdown) {
    cmd += ' --markdown';
  }
  
  console.log('Running analysis...');
  console.log(`Command: ${cmd}\n`);
  
  try {
    const output = execSync(cmd, { encoding: 'utf-8', maxBuffer: 10 * 1024 * 1024 });
    console.log(output);
    return true;
  } catch (error) {
    console.error('Analysis failed:', error.message);
    return false;
  }
}

/**
 * 生成统计报告
 */
function generateStatsReport(jsonFile, statsFile, config) {
  console.log('\nGenerating statistics report...');
  
  // 读取JSON结果
  const data = JSON.parse(fs.readFileSync(jsonFile, 'utf-8'));
  
  // 应用maxPatterns限制
  let patterns = data.patterns || [];
  if (config.maxPatterns && patterns.length > config.maxPatterns) {
    patterns = patterns.slice(0, config.maxPatterns);
  }
  
  // 计算统计信息
  const stats = calculateStats(data, patterns);
  
  // 生成Markdown报告
  const markdown = generateMarkdownStats(data, patterns, stats, config);
  
  // 保存报告
  fs.writeFileSync(statsFile, markdown, 'utf-8');
  console.log(`✓ Statistics report saved: ${statsFile}`);
}

/**
 * 计算统计信息
 */
function calculateStats(data, patterns) {
  const totalUrls = data.summary?.totalUrls || 0;
  const coveredUrls = patterns.reduce((sum, p) => sum + p.urlCount, 0);
  const coverageRate = totalUrls > 0 ? (coveredUrls / totalUrls * 100).toFixed(2) : 0;
  
  const urlCounts = patterns.map(p => p.urlCount);
  const avgUrlsPerPattern = urlCounts.length > 0 
    ? (urlCounts.reduce((a, b) => a + b, 0) / urlCounts.length).toFixed(2)
    : 0;
  
  const maxUrls = Math.max(...urlCounts, 0);
  const minUrls = Math.min(...urlCounts, Infinity);
  
  return {
    totalUrls,
    coveredUrls,
    coverageRate,
    avgUrlsPerPattern,
    maxUrls,
    minUrls,
    patternCount: patterns.length
  };
}

/**
 * 生成Markdown统计报告（中文版）
 */
function generateMarkdownStats(data, patterns, stats, config) {
  const lines = [];
  
  // 标题
  lines.push('# URL模式分析 - 统计报告');
  lines.push('');
  lines.push(`**生成时间**: ${new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' })}`);
  lines.push(`**项目名称**: ${config.projectName}`);
  lines.push('');
  
  // 总体统计
  lines.push('## 总体统计');
  lines.push('');
  lines.push('| 指标 | 数值 |');
  lines.push('|------|------|');
  lines.push(`| 总URL数量 | ${stats.totalUrls.toLocaleString()} |`);
  lines.push(`| 识别的模式数量 | ${stats.patternCount} |`);
  lines.push(`| 已分类URL数量 | ${stats.coveredUrls.toLocaleString()} |`);
  lines.push(`| 覆盖率 | ${stats.coverageRate}% |`);
  lines.push(`| 平均每个模式的URL数 | ${stats.avgUrlsPerPattern} |`);
  lines.push(`| 最大模式的URL数 | ${stats.maxUrls.toLocaleString()} |`);
  lines.push(`| 最小模式的URL数 | ${stats.minUrls.toLocaleString()} |`);
  lines.push('');
  
  // 配置参数
  lines.push('## 配置参数');
  lines.push('');
  lines.push('| 参数 | 值 |');
  lines.push('|------|-----|');
  lines.push(`| 最小分组大小 | ${config.minGroupSize} |`);
  lines.push(`| 最大模式数量 | ${config.maxPatterns || '不限制'} |`);
  lines.push(`| 示例URL数量 | ${config.sampleCount} |`);
  lines.push('');
  
  // 模式分布
  lines.push('## 模式分布');
  lines.push('');
  lines.push('| 排名 | 模式名称 | URL数量 | 占比 | 路径模板 |');
  lines.push('|------|----------|---------|------|----------|');
  
  patterns.forEach((pattern, index) => {
    const percentage = stats.totalUrls > 0 
      ? ((pattern.urlCount / stats.totalUrls) * 100).toFixed(2)
      : 0;
    lines.push(`| ${index + 1} | ${pattern.name} | ${pattern.urlCount.toLocaleString()} | ${percentage}% | \`${pattern.pathTemplate}\` |`);
  });
  lines.push('');
  
  // Top 10 详细信息
  lines.push('## Top 10 模式详情');
  lines.push('');
  
  patterns.slice(0, 10).forEach((pattern, index) => {
    lines.push(`### ${index + 1}. ${pattern.name}`);
    lines.push('');
    lines.push(`- **URL数量**: ${pattern.urlCount.toLocaleString()}`);
    lines.push(`- **路径模板**: \`${pattern.pathTemplate}\``);
    lines.push(`- **正则表达式**: \`${pattern.pattern}\``);
    lines.push(`- **查询参数**: ${pattern.queryParams.length > 0 ? pattern.queryParams.join(', ') : '无'}`);
    lines.push('');
    
    if (pattern.samples && pattern.samples.length > 0) {
      lines.push('**示例URL**:');
      pattern.samples.slice(0, 3).forEach((url, i) => {
        lines.push(`${i + 1}. ${url}`);
      });
      lines.push('');
    }
  });
  
  // 质量评估
  lines.push('## 质量评估');
  lines.push('');
  
  if (stats.coverageRate >= 90) {
    lines.push('✅ **优秀**: 覆盖率 > 90%，模式定义良好。');
  } else if (stats.coverageRate >= 70) {
    lines.push('⚠️ **良好**: 覆盖率 70-90%，可考虑调整minGroupSize参数。');
  } else {
    lines.push('❌ **较差**: 覆盖率 < 70%，很多URL未被分类。');
  }
  lines.push('');
  
  // 建议
  lines.push('## 优化建议');
  lines.push('');
  
  if (stats.patternCount > 50) {
    lines.push(`- 考虑增加 \`minGroupSize\` 参数（当前: ${config.minGroupSize}）以减少模式数量`);
  }
  
  if (stats.coverageRate < 70) {
    lines.push(`- 考虑降低 \`minGroupSize\` 参数（当前: ${config.minGroupSize}）以提高覆盖率`);
  }
  
  if (stats.avgUrlsPerPattern < 10) {
    lines.push('- 许多模式的URL数量较少，考虑过滤或合并相似模式');
  }
  
  if (stats.patternCount < 5 && stats.totalUrls > 1000) {
    lines.push('- 模式数量较少，可能分类过于粗糙，考虑降低minGroupSize');
  }
  
  lines.push('');
  lines.push('---');
  lines.push('');
  lines.push('*由 URL Pattern Analyzer v1.0.0 生成*');
  
  return lines.join('\n');
}

/**
 * 主函数
 */
async function main() {
  try {
    // 解析参数
    const config = parseArgs();
    
    console.log('=== URL Pattern Analyzer - Enhanced Runner ===\n');
    console.log(`Project: ${config.projectName}`);
    console.log(`Min Group Size: ${config.minGroupSize}`);
    console.log(`Max Patterns: ${config.maxPatterns || 'Unlimited'}`);
    console.log(`Sample Count: ${config.sampleCount}`);
    console.log('');
    
    // 查找links文件
    console.log('Step 1: Locating links file...');
    const linksFile = findLinksFile(config.projectName);
    console.log(`✓ Found: ${linksFile}\n`);
    
    // 生成输出路径
    const outputPaths = getOutputPaths(config.projectName);
    
    // 运行分析
    console.log('Step 2: Running analysis...');
    const success = runAnalysis(linksFile, outputPaths.json, config);
    
    if (!success) {
      console.error('\n✗ Analysis failed');
      process.exit(1);
    }
    
    // 生成统计报告
    console.log('\nStep 3: Generating statistics report...');
    generateStatsReport(outputPaths.json, outputPaths.stats, config);
    
    // 完成
    console.log('\n=== Analysis Complete ===');
    console.log('\nOutput files:');
    console.log(`  - JSON: ${outputPaths.json}`);
    if (config.generateMarkdown) {
      console.log(`  - Markdown: ${outputPaths.markdown}`);
    }
    console.log(`  - Statistics: ${outputPaths.stats}`);
    console.log('\n✓ All done!');
    
  } catch (error) {
    console.error('\n✗ Error:', error.message);
    process.exit(1);
  }
}

// 运行主函数
if (require.main === module) {
  main().catch(error => {
    console.error('Fatal error:', error);
    process.exit(1);
  });
}

module.exports = main;
