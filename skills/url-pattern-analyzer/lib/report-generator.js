/**
 * Report Generator - 生成URL模式分析报告
 * 
 * 负责生成JSON和Markdown格式的分析报告
 */

const fs = require('fs').promises;
const path = require('path');

class ReportGenerator {
  /**
   * 生成JSON格式报告
   * @param {Array} clusters - URL聚类结果
   * @param {Object} options - 生成选项
   * @param {number} options.sampleCount - 每个模式的示例URL数量（默认5）
   * @returns {Object} JSON报告对象
   */
  generateJSONReport(clusters, options = {}) {
    const { sampleCount = 5 } = options;
    
    // 导入URLPatternAnalyzer用于生成模式
    const URLPatternAnalyzer = require('./url-clusterer');
    const analyzer = new URLPatternAnalyzer();
    
    // 生成每个簇的模式信息
    const patterns = clusters.map((urlGroup, index) => {
      // 生成正则表达式和模板
      const patternInfo = analyzer.generatePattern(urlGroup);
      
      // 生成模式名称（基于路径模板）
      const name = this._generatePatternName(patternInfo.pathTemplate, index);
      
      // 选择示例URL
      const samples = urlGroup.slice(0, sampleCount);
      
      return {
        name,
        pathTemplate: patternInfo.pathTemplate,
        pattern: patternInfo.pattern,
        queryParams: patternInfo.queryParams,
        urlCount: urlGroup.length,
        samples
      };
    });
    
    // 计算统计信息
    const totalUrls = clusters.reduce((sum, cluster) => sum + cluster.length, 0);
    const patternCount = patterns.length;
    
    // 生成完整报告
    const report = {
      summary: {
        totalUrls,
        patternCount,
        generatedAt: new Date().toISOString()
      },
      patterns
    };
    
    return report;
  }
  
  /**
   * 生成Markdown格式报告
   * @param {Array} clusters - URL聚类结果
   * @param {Object} options - 生成选项
   * @param {number} options.sampleCount - 每个模式的示例URL数量（默认5）
   * @returns {string} Markdown报告内容
   */
  generateMarkdownReport(clusters, options = {}) {
    const { sampleCount = 5 } = options;
    
    // 首先生成JSON报告以获取结构化数据
    const jsonReport = this.generateJSONReport(clusters, options);
    
    // 构建Markdown内容
    const lines = [];
    
    // 标题
    lines.push('# URL模式分析报告');
    lines.push('');
    
    // 生成时间
    lines.push(`**生成时间**: ${new Date(jsonReport.summary.generatedAt).toLocaleString('zh-CN')}`);
    lines.push('');
    
    // 统计信息
    lines.push('## 统计摘要');
    lines.push('');
    lines.push(`- **URL总数**: ${jsonReport.summary.totalUrls}`);
    lines.push(`- **模式数量**: ${jsonReport.summary.patternCount}`);
    lines.push(`- **平均每模式URL数**: ${Math.round(jsonReport.summary.totalUrls / jsonReport.summary.patternCount)}`);
    lines.push('');
    
    // 模式分布表格
    lines.push('## 模式分布');
    lines.push('');
    lines.push('| 序号 | 模式名称 | URL数量 | 占比 | 路径模板 |');
    lines.push('|------|----------|---------|------|----------|');
    
    jsonReport.patterns.forEach((pattern, index) => {
      const percentage = ((pattern.urlCount / jsonReport.summary.totalUrls) * 100).toFixed(1);
      lines.push(`| ${index + 1} | ${pattern.name} | ${pattern.urlCount} | ${percentage}% | \`${pattern.pathTemplate}\` |`);
    });
    lines.push('');
    
    // 详细模式信息
    lines.push('## 模式详情');
    lines.push('');
    
    jsonReport.patterns.forEach((pattern, index) => {
      lines.push(`### ${index + 1}. ${pattern.name}`);
      lines.push('');
      lines.push(`**路径模板**: \`${pattern.pathTemplate}\``);
      lines.push('');
      lines.push(`**正则表达式**: \`${pattern.pattern}\``);
      lines.push('');
      
      if (pattern.queryParams.length > 0) {
        lines.push(`**查询参数**: ${pattern.queryParams.map(p => `\`${p}\``).join(', ')}`);
        lines.push('');
      }
      
      lines.push(`**URL数量**: ${pattern.urlCount}`);
      lines.push('');
      lines.push('**示例URL**:');
      lines.push('');
      pattern.samples.forEach((url, i) => {
        lines.push(`${i + 1}. \`${url}\``);
      });
      lines.push('');
    });
    
    return lines.join('\n');
  }
  
  /**
   * 保存JSON报告到文件
   * @param {Object} report - JSON报告对象
   * @param {string} outputPath - 输出文件路径
   * @returns {Promise<void>}
   */
  async saveJSONReport(report, outputPath) {
    try {
      // 确保输出目录存在
      const dir = path.dirname(outputPath);
      await fs.mkdir(dir, { recursive: true });
      
      // 写入文件（格式化JSON）
      await fs.writeFile(
        outputPath,
        JSON.stringify(report, null, 2),
        'utf-8'
      );
      
      console.log(`✓ JSON报告已保存: ${outputPath}`);
    } catch (error) {
      throw new Error(`Failed to save JSON report: ${error.message}`);
    }
  }
  
  /**
   * 保存Markdown报告到文件
   * @param {string} markdown - Markdown内容
   * @param {string} outputPath - 输出文件路径
   * @returns {Promise<void>}
   */
  async saveMarkdownReport(markdown, outputPath) {
    try {
      // 确保输出目录存在
      const dir = path.dirname(outputPath);
      await fs.mkdir(dir, { recursive: true });
      
      // 写入文件
      await fs.writeFile(outputPath, markdown, 'utf-8');
      
      console.log(`✓ Markdown报告已保存: ${outputPath}`);
    } catch (error) {
      throw new Error(`Failed to save Markdown report: ${error.message}`);
    }
  }
  
  /**
   * 生成模式名称
   * @private
   * @param {string} pathTemplate - 路径模板
   * @param {number} index - 模式索引
   * @returns {string} 模式名称
   */
  _generatePatternName(pathTemplate, index) {
    // 从路径模板提取有意义的名称
    const segments = pathTemplate.split('/').filter(seg => seg && !seg.startsWith('{'));
    
    if (segments.length === 0) {
      return `pattern-${index + 1}`;
    }
    
    // 使用最后一个有意义的段作为名称
    const lastName = segments[segments.length - 1];
    
    // 如果有多个段，可以组合使用
    if (segments.length > 1) {
      return segments.slice(-2).join('-');
    }
    
    return lastName;
  }
}

module.exports = ReportGenerator;
