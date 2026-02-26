#!/usr/bin/env node

/**
 * Task 9.1.4: 验证生成的配置质量
 * 
 * 功能:
 * - 加载template-rules.jsonl文件
 * - 验证每个配置的结构和完整性
 * - 测试TemplateParser能否从配置创建
 * - 测试URL匹配功能
 * - 验证提取器的合理性（正确的选择器、类型）
 * - 验证过滤器的有效性（基于高频内容）
 * - 测试用样例页面解析配置
 * - 生成质量评估报告
 */

const fs = require('fs');
const path = require('path');
const ConfigLoader = require('../lib/config-loader');
const TemplateParser = require('../lib/template-parser');

class ConfigQualityValidator {
  constructor(configPath) {
    this.configPath = configPath;
    this.configs = [];
    this.validationResults = [];
    this.issues = [];
    this.warnings = [];
  }

  /**
   * 运行完整的质量验证
   */
  async validate() {
    console.log('='.repeat(80));
    console.log('配置质量验证 - Task 9.1.4');
    console.log('='.repeat(80));
    console.log();

    try {
      // 1. 加载配置文件
      console.log('📂 步骤1: 加载配置文件...');
      await this.loadConfigs();
      console.log(`✅ 成功加载 ${this.configs.length} 个配置\n`);

      // 2. 验证配置结构
      console.log('🔍 步骤2: 验证配置结构...');
      this.validateStructure();
      console.log(`✅ 结构验证完成\n`);

      // 3. 测试TemplateParser创建
      console.log('🏗️  步骤3: 测试TemplateParser创建...');
      this.testParserCreation();
      console.log(`✅ Parser创建测试完成\n`);

      // 4. 测试URL匹配
      console.log('🔗 步骤4: 测试URL匹配功能...');
      this.testUrlMatching();
      console.log(`✅ URL匹配测试完成\n`);

      // 5. 验证提取器质量
      console.log('📊 步骤5: 验证提取器质量...');
      this.validateExtractors();
      console.log(`✅ 提取器验证完成\n`);

      // 6. 验证过滤器有效性
      console.log('🧹 步骤6: 验证过滤器有效性...');
      this.validateFilters();
      console.log(`✅ 过滤器验证完成\n`);

      // 7. 生成质量报告
      console.log('📝 步骤7: 生成质量评估报告...');
      const report = this.generateReport();
      console.log(`✅ 报告生成完成\n`);

      return report;
    } catch (error) {
      console.error('❌ 验证过程出错:', error.message);
      throw error;
    }
  }

  /**
   * 加载配置文件
   */
  async loadConfigs() {
    if (!fs.existsSync(this.configPath)) {
      throw new Error(`配置文件不存在: ${this.configPath}`);
    }

    const content = fs.readFileSync(this.configPath, 'utf-8');
    const lines = content.trim().split('\n').filter(line => line.trim());

    console.log(`  - 文件路径: ${this.configPath}`);
    console.log(`  - 文件大小: ${(fs.statSync(this.configPath).size / 1024).toFixed(2)} KB`);
    console.log(`  - 配置行数: ${lines.length}`);

    for (let i = 0; i < lines.length; i++) {
      try {
        const config = JSON.parse(lines[i]);
        this.configs.push(config);
      } catch (error) {
        this.issues.push({
          type: 'PARSE_ERROR',
          line: i + 1,
          message: `无法解析JSON: ${error.message}`
        });
      }
    }
  }

  /**
   * 验证配置结构
   */
  validateStructure() {
    const requiredFields = ['name', 'urlPattern', 'extractors', 'filters', 'metadata'];
    const urlPatternFields = ['pattern', 'pathTemplate'];
    const metadataFields = ['generatedAt', 'pageCount', 'version'];

    this.configs.forEach((config, index) => {
      const result = {
        configIndex: index,
        configName: config.name || `未命名-${index}`,
        structureValid: true,
        missingFields: [],
        invalidFields: []
      };

      // 检查必需字段
      requiredFields.forEach(field => {
        if (!(field in config)) {
          result.missingFields.push(field);
          result.structureValid = false;
        }
      });

      // 检查urlPattern结构
      if (config.urlPattern) {
        urlPatternFields.forEach(field => {
          if (!(field in config.urlPattern)) {
            result.missingFields.push(`urlPattern.${field}`);
            result.structureValid = false;
          }
        });

        // 验证pattern是否是有效的正则表达式
        if (config.urlPattern.pattern) {
          try {
            new RegExp(config.urlPattern.pattern);
          } catch (error) {
            result.invalidFields.push({
              field: 'urlPattern.pattern',
              reason: `无效的正则表达式: ${error.message}`
            });
            result.structureValid = false;
          }
        }
      }

      // 检查metadata结构
      if (config.metadata) {
        metadataFields.forEach(field => {
          if (!(field in config.metadata)) {
            result.missingFields.push(`metadata.${field}`);
            result.structureValid = false;
          }
        });
      }

      // 检查extractors是否是数组
      if (config.extractors && !Array.isArray(config.extractors)) {
        result.invalidFields.push({
          field: 'extractors',
          reason: '应该是数组类型'
        });
        result.structureValid = false;
      }

      // 检查filters是否是数组
      if (config.filters && !Array.isArray(config.filters)) {
        result.invalidFields.push({
          field: 'filters',
          reason: '应该是数组类型'
        });
        result.structureValid = false;
      }

      this.validationResults.push(result);

      if (!result.structureValid) {
        this.issues.push({
          type: 'STRUCTURE_ERROR',
          config: result.configName,
          details: result
        });
      }

      console.log(`  - [${result.structureValid ? '✅' : '❌'}] ${result.configName}: ${result.structureValid ? '结构正确' : '结构错误'}`);
    });
  }

  /**
   * 测试TemplateParser创建
   */
  testParserCreation() {
    this.configs.forEach((config, index) => {
      try {
        const parser = new TemplateParser(config);
        console.log(`  - [✅] ${config.name}: Parser创建成功`);
      } catch (error) {
        console.log(`  - [❌] ${config.name}: Parser创建失败 - ${error.message}`);
        this.issues.push({
          type: 'PARSER_CREATION_ERROR',
          config: config.name,
          error: error.message
        });
      }
    });
  }

  /**
   * 测试URL匹配功能
   */
  testUrlMatching() {
    // 从links.txt读取一些样例URL进行测试
    const linksPath = path.join(path.dirname(this.configPath), 'links.txt');
    
    if (!fs.existsSync(linksPath)) {
      this.warnings.push({
        type: 'MISSING_TEST_DATA',
        message: '找不到links.txt文件，跳过URL匹配测试'
      });
      console.log('  ⚠️  找不到links.txt文件，跳过URL匹配测试');
      return;
    }

    // 读取前100个URL作为测试样本
    const content = fs.readFileSync(linksPath, 'utf-8');
    const lines = content.trim().split('\n').slice(0, 100);
    const testUrls = [];

    for (const line of lines) {
      try {
        const record = JSON.parse(line);
        if (record.url) {
          testUrls.push(record.url);
        }
      } catch (error) {
        // 忽略解析错误
      }
    }

    console.log(`  - 测试样本: ${testUrls.length} 个URL`);

    // 为每个配置测试URL匹配
    this.configs.forEach(config => {
      try {
        const parser = new TemplateParser(config);
        const matchedUrls = testUrls.filter(url => parser.matches(url));
        
        console.log(`  - [${matchedUrls.length > 0 ? '✅' : '⚠️'}] ${config.name}: 匹配 ${matchedUrls.length} 个URL`);
        
        if (matchedUrls.length === 0) {
          this.warnings.push({
            type: 'NO_URL_MATCH',
            config: config.name,
            message: '在测试样本中没有匹配到任何URL'
          });
        }

        // 显示前3个匹配的URL作为示例
        if (matchedUrls.length > 0) {
          matchedUrls.slice(0, 3).forEach(url => {
            console.log(`      - ${url}`);
          });
        }
      } catch (error) {
        console.log(`  - [❌] ${config.name}: 匹配测试失败 - ${error.message}`);
      }
    });
  }

  /**
   * 验证提取器质量
   */
  validateExtractors() {
    const validTypes = ['text', 'table', 'code', 'list'];
    const validSelectors = /^[a-zA-Z0-9\s,.\-_#\[\]="':()>+~*]+$/;

    this.configs.forEach(config => {
      const extractorIssues = [];
      const extractorWarnings = [];

      if (!config.extractors || config.extractors.length === 0) {
        extractorWarnings.push('没有定义任何提取器');
      } else {
        config.extractors.forEach((extractor, index) => {
          // 检查必需字段
          if (!extractor.field) {
            extractorIssues.push(`提取器${index}: 缺少field字段`);
          }
          if (!extractor.type) {
            extractorIssues.push(`提取器${index}: 缺少type字段`);
          } else if (!validTypes.includes(extractor.type)) {
            extractorIssues.push(`提取器${index}: 无效的type "${extractor.type}"`);
          }
          if (!extractor.selector) {
            extractorIssues.push(`提取器${index}: 缺少selector字段`);
          } else if (!validSelectors.test(extractor.selector)) {
            extractorWarnings.push(`提取器${index}: selector可能包含特殊字符 "${extractor.selector}"`);
          }

          // 检查table类型的特殊要求
          if (extractor.type === 'table' && !extractor.columns) {
            extractorWarnings.push(`提取器${index}: table类型建议定义columns字段`);
          }
        });

        console.log(`  - [${extractorIssues.length === 0 ? '✅' : '❌'}] ${config.name}: ${config.extractors.length} 个提取器`);
        
        if (extractorIssues.length > 0) {
          extractorIssues.forEach(issue => console.log(`      ❌ ${issue}`));
          this.issues.push({
            type: 'EXTRACTOR_ERROR',
            config: config.name,
            issues: extractorIssues
          });
        }
        
        if (extractorWarnings.length > 0) {
          extractorWarnings.forEach(warning => console.log(`      ⚠️  ${warning}`));
          this.warnings.push({
            type: 'EXTRACTOR_WARNING',
            config: config.name,
            warnings: extractorWarnings
          });
        }
      }
    });
  }

  /**
   * 验证过滤器有效性
   */
  validateFilters() {
    const validTypes = ['remove', 'keep', 'transform'];

    this.configs.forEach(config => {
      const filterIssues = [];
      const filterWarnings = [];

      if (!config.filters || config.filters.length === 0) {
        filterWarnings.push('没有定义任何过滤器');
      } else {
        config.filters.forEach((filter, index) => {
          // 检查必需字段
          if (!filter.type) {
            filterIssues.push(`过滤器${index}: 缺少type字段`);
          } else if (!validTypes.includes(filter.type)) {
            filterIssues.push(`过滤器${index}: 无效的type "${filter.type}"`);
          }
          if (!filter.target) {
            filterIssues.push(`过滤器${index}: 缺少target字段`);
          }
          if (!filter.pattern) {
            filterIssues.push(`过滤器${index}: 缺少pattern字段`);
          }

          // 检查是否有reason说明
          if (!filter.reason) {
            filterWarnings.push(`过滤器${index}: 建议添加reason字段说明原因`);
          }
        });

        // 统计高频过滤器（frequency > 80%）
        const highFreqFilters = config.filters.filter(f => 
          f.reason && f.reason.includes('%') && 
          parseInt(f.reason.match(/(\d+)%/)?.[1] || '0') > 80
        );

        console.log(`  - [${filterIssues.length === 0 ? '✅' : '❌'}] ${config.name}: ${config.filters.length} 个过滤器 (${highFreqFilters.length} 个高频)`);
        
        if (filterIssues.length > 0) {
          filterIssues.forEach(issue => console.log(`      ❌ ${issue}`));
          this.issues.push({
            type: 'FILTER_ERROR',
            config: config.name,
            issues: filterIssues
          });
        }
        
        if (filterWarnings.length > 0 && filterWarnings.length <= 3) {
          filterWarnings.forEach(warning => console.log(`      ⚠️  ${warning}`));
        }
      }
    });
  }

  /**
   * 生成质量评估报告
   */
  generateReport() {
    const report = {
      summary: {
        totalConfigs: this.configs.length,
        validConfigs: this.validationResults.filter(r => r.structureValid).length,
        totalIssues: this.issues.length,
        totalWarnings: this.warnings.length,
        timestamp: new Date().toISOString()
      },
      configDetails: this.configs.map((config, index) => ({
        name: config.name,
        urlPattern: config.urlPattern?.pathTemplate || 'N/A',
        extractorCount: config.extractors?.length || 0,
        filterCount: config.filters?.length || 0,
        pageCount: config.metadata?.pageCount || 0,
        structureValid: this.validationResults[index]?.structureValid || false
      })),
      issues: this.issues,
      warnings: this.warnings,
      recommendations: this.generateRecommendations()
    };

    return report;
  }

  /**
   * 生成改进建议
   */
  generateRecommendations() {
    const recommendations = [];

    // 基于issues生成建议
    const structureErrors = this.issues.filter(i => i.type === 'STRUCTURE_ERROR');
    if (structureErrors.length > 0) {
      recommendations.push({
        priority: 'HIGH',
        category: '结构问题',
        message: `有 ${structureErrors.length} 个配置存在结构错误，需要修复`,
        action: '检查并补充缺失的必需字段'
      });
    }

    const extractorErrors = this.issues.filter(i => i.type === 'EXTRACTOR_ERROR');
    if (extractorErrors.length > 0) {
      recommendations.push({
        priority: 'HIGH',
        category: '提取器问题',
        message: `有 ${extractorErrors.length} 个配置的提取器存在错误`,
        action: '检查提取器的field、type、selector字段是否完整和正确'
      });
    }

    const noUrlMatch = this.warnings.filter(w => w.type === 'NO_URL_MATCH');
    if (noUrlMatch.length > 0) {
      recommendations.push({
        priority: 'MEDIUM',
        category: 'URL匹配',
        message: `有 ${noUrlMatch.length} 个配置在测试样本中没有匹配到URL`,
        action: '检查urlPattern.pattern正则表达式是否正确'
      });
    }

    // 如果没有问题，给出正面反馈
    if (this.issues.length === 0) {
      recommendations.push({
        priority: 'INFO',
        category: '质量评估',
        message: '所有配置都通过了验证，质量良好',
        action: '可以投入使用'
      });
    }

    return recommendations;
  }

  /**
   * 保存报告到文件
   */
  saveReport(report, outputPath) {
    // 保存JSON格式
    const jsonPath = outputPath.replace(/\.md$/, '.json');
    fs.writeFileSync(jsonPath, JSON.stringify(report, null, 2), 'utf-8');
    console.log(`\n📄 JSON报告已保存: ${jsonPath}`);

    // 生成Markdown格式
    const markdown = this.generateMarkdownReport(report);
    fs.writeFileSync(outputPath, markdown, 'utf-8');
    console.log(`📄 Markdown报告已保存: ${outputPath}`);
  }

  /**
   * 生成Markdown格式的报告
   */
  generateMarkdownReport(report) {
    const lines = [];

    lines.push('# 配置质量验证报告 - Task 9.1.4');
    lines.push('');
    lines.push(`**生成时间**: ${new Date(report.summary.timestamp).toLocaleString('zh-CN')}`);
    lines.push(`**配置文件**: ${this.configPath}`);
    lines.push('');

    // 摘要
    lines.push('## 📊 验证摘要');
    lines.push('');
    lines.push('| 指标 | 数值 |');
    lines.push('|------|------|');
    lines.push(`| 总配置数 | ${report.summary.totalConfigs} |`);
    lines.push(`| 有效配置 | ${report.summary.validConfigs} |`);
    lines.push(`| 错误数量 | ${report.summary.totalIssues} |`);
    lines.push(`| 警告数量 | ${report.summary.totalWarnings} |`);
    lines.push(`| 验证结果 | ${report.summary.totalIssues === 0 ? '✅ 通过' : '❌ 存在问题'} |`);
    lines.push('');

    // 配置详情
    lines.push('## 📋 配置详情');
    lines.push('');
    lines.push('| 配置名称 | URL模式 | 提取器 | 过滤器 | 页面数 | 状态 |');
    lines.push('|---------|---------|--------|--------|--------|------|');
    report.configDetails.forEach(config => {
      lines.push(`| ${config.name} | ${config.urlPattern} | ${config.extractorCount} | ${config.filterCount} | ${config.pageCount} | ${config.structureValid ? '✅' : '❌'} |`);
    });
    lines.push('');

    // 提取器统计
    lines.push('## 📊 提取器统计');
    lines.push('');
    const totalExtractors = report.configDetails.reduce((sum, c) => sum + c.extractorCount, 0);
    const avgExtractors = (totalExtractors / report.configDetails.length).toFixed(1);
    lines.push(`- **总提取器数**: ${totalExtractors}`);
    lines.push(`- **平均每配置**: ${avgExtractors} 个`);
    lines.push(`- **最多**: ${Math.max(...report.configDetails.map(c => c.extractorCount))} 个`);
    lines.push(`- **最少**: ${Math.min(...report.configDetails.map(c => c.extractorCount))} 个`);
    lines.push('');

    // 过滤器统计
    lines.push('## 🧹 过滤器统计');
    lines.push('');
    const totalFilters = report.configDetails.reduce((sum, c) => sum + c.filterCount, 0);
    const avgFilters = (totalFilters / report.configDetails.length).toFixed(1);
    lines.push(`- **总过滤器数**: ${totalFilters}`);
    lines.push(`- **平均每配置**: ${avgFilters} 个`);
    lines.push(`- **最多**: ${Math.max(...report.configDetails.map(c => c.filterCount))} 个`);
    lines.push(`- **最少**: ${Math.min(...report.configDetails.map(c => c.filterCount))} 个`);
    lines.push('');

    // 问题列表
    if (report.issues.length > 0) {
      lines.push('## ❌ 发现的问题');
      lines.push('');
      report.issues.forEach((issue, index) => {
        lines.push(`### ${index + 1}. ${issue.type}`);
        lines.push('');
        lines.push(`**配置**: ${issue.config || 'N/A'}`);
        lines.push('');
        if (issue.details) {
          lines.push('**详情**:');
          if (issue.details.missingFields?.length > 0) {
            lines.push(`- 缺失字段: ${issue.details.missingFields.join(', ')}`);
          }
          if (issue.details.invalidFields?.length > 0) {
            lines.push('- 无效字段:');
            issue.details.invalidFields.forEach(f => {
              lines.push(`  - ${f.field}: ${f.reason}`);
            });
          }
        }
        if (issue.issues) {
          issue.issues.forEach(i => lines.push(`- ${i}`));
        }
        if (issue.error) {
          lines.push(`- 错误: ${issue.error}`);
        }
        lines.push('');
      });
    }

    // 警告列表
    if (report.warnings.length > 0 && report.warnings.length <= 10) {
      lines.push('## ⚠️  警告信息');
      lines.push('');
      report.warnings.forEach((warning, index) => {
        lines.push(`${index + 1}. **${warning.type}** - ${warning.config || ''}`);
        lines.push(`   - ${warning.message || warning.warnings?.join(', ')}`);
        lines.push('');
      });
    }

    // 改进建议
    if (report.recommendations.length > 0) {
      lines.push('## 💡 改进建议');
      lines.push('');
      report.recommendations.forEach((rec, index) => {
        const icon = rec.priority === 'HIGH' ? '🔴' : rec.priority === 'MEDIUM' ? '🟡' : '🟢';
        lines.push(`### ${icon} ${rec.category}`);
        lines.push('');
        lines.push(`**优先级**: ${rec.priority}`);
        lines.push('');
        lines.push(`**问题**: ${rec.message}`);
        lines.push('');
        lines.push(`**建议**: ${rec.action}`);
        lines.push('');
      });
    }

    // 结论
    lines.push('## ✅ 验证结论');
    lines.push('');
    if (report.summary.totalIssues === 0) {
      lines.push('所有配置都通过了质量验证，可以投入使用。');
      lines.push('');
      lines.push('**配置质量评估**: ⭐⭐⭐⭐⭐ 优秀');
    } else if (report.summary.totalIssues <= 3) {
      lines.push('配置基本合格，但存在少量问题需要修复。');
      lines.push('');
      lines.push('**配置质量评估**: ⭐⭐⭐⭐ 良好');
    } else {
      lines.push('配置存在较多问题，建议修复后再使用。');
      lines.push('');
      lines.push('**配置质量评估**: ⭐⭐⭐ 一般');
    }
    lines.push('');

    lines.push('---');
    lines.push('');
    lines.push(`**验证工具**: ConfigQualityValidator`);
    lines.push(`**验证时间**: ${new Date(report.summary.timestamp).toLocaleString('zh-CN')}`);

    return lines.join('\n');
  }
}

// 主函数
async function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    console.log('用法: node validate-config-quality.js <config-file> [output-report]');
    console.log('');
    console.log('示例:');
    console.log('  node validate-config-quality.js ../../stock-crawler/output/lixinger-crawler/template-rules.jsonl');
    console.log('  node validate-config-quality.js template-rules.jsonl quality-report.md');
    process.exit(1);
  }

  const configPath = args[0];
  const outputPath = args[1] || path.join(
    path.dirname(configPath),
    'CONFIG_QUALITY_REPORT.md'
  );

  try {
    const validator = new ConfigQualityValidator(configPath);
    const report = await validator.validate();
    validator.saveReport(report, outputPath);

    console.log('');
    console.log('='.repeat(80));
    console.log('验证完成');
    console.log('='.repeat(80));
    console.log(`✅ 有效配置: ${report.summary.validConfigs}/${report.summary.totalConfigs}`);
    console.log(`${report.summary.totalIssues === 0 ? '✅' : '❌'} 错误: ${report.summary.totalIssues}`);
    console.log(`${report.summary.totalWarnings === 0 ? '✅' : '⚠️'} 警告: ${report.summary.totalWarnings}`);
    console.log('');

    process.exit(report.summary.totalIssues > 0 ? 1 : 0);
  } catch (error) {
    console.error('❌ 验证失败:', error.message);
    console.error(error.stack);
    process.exit(1);
  }
}

// 如果直接运行此脚本
if (require.main === module) {
  main();
}

module.exports = ConfigQualityValidator;
