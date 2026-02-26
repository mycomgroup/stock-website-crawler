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
      
      // 生成中文描述
      const description = this._generateDescription({
        name,
        pathTemplate: patternInfo.pathTemplate,
        samples,
        urlCount: urlGroup.length
      });
      
      return {
        name,
        description,
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
  
  /**
   * 生成中文描述
   * @private
   * @param {Object} pattern - 模式对象
   * @returns {string} 中文描述
   */
  _generateDescription(pattern) {
    const { name, pathTemplate, samples } = pattern;
    
    // 解析路径段
    const segments = pathTemplate.split('/').filter(s => s && !s.startsWith('{'));
    
    let market = '', assetType = '', pageType = '', dataType = '', subType = '';
    
    // 识别市场
    if (pathTemplate.includes('/sh/')) market = '上海证券交易所';
    else if (pathTemplate.includes('/sz/')) market = '深圳证券交易所';
    else if (pathTemplate.includes('/hk/')) market = '香港交易所';
    else if (pathTemplate.includes('/nasdaq/')) market = '纳斯达克';
    else if (pathTemplate.includes('/nyse/')) market = '纽约证券交易所';
    else if (pathTemplate.includes('/csi/')) market = '中证指数';
    else if (pathTemplate.includes('/sw_2021/')) market = '申万2021行业';
    else if (pathTemplate.includes('/sw/')) market = '申万行业';
    
    // 识别资产类型
    if (segments.includes('company')) assetType = '公司';
    else if (segments.includes('fund')) {
      if (segments.includes('fund-collection')) assetType = '基金公司';
      else if (segments.includes('fund-manager')) assetType = '基金经理';
      else assetType = '基金';
    } else if (segments.includes('index')) assetType = '指数';
    else if (segments.includes('industry')) assetType = '行业';
    else if (segments.includes('bond')) assetType = '债券';
    
    // 识别页面类型
    if (segments.includes('detail')) pageType = '详情页';
    else if (segments.includes('dashboard')) pageType = '数据看板';
    else if (segments.includes('list')) pageType = '列表页';
    
    // 识别数据类型和子类型
    if (segments.includes('fundamental')) {
      dataType = '基本面数据';
      if (name.includes('peg')) subType = 'PEG估值指标';
      else if (name.includes('dcf')) subType = 'DCF现金流折现估值';
      else if (name.includes('costs')) subType = '成本分析';
      else if (name.includes('safety')) subType = '安全性指标';
      else if (name.includes('profit')) subType = '盈利能力分析';
      else if (name.includes('growth')) subType = '成长性指标';
      else if (name.includes('cashflow')) subType = '现金流分析';
      else if (name.includes('operation-capability')) subType = '运营能力指标';
      else if (name.includes('custom-chart')) subType = '自定义图表';
      else if (name.includes('valuation')) subType = '估值分析';
    } else if (segments.includes('valuation')) {
      dataType = '估值数据';
      if (name.includes('primary')) subType = '主要估值指标';
      else if (name.includes('fitting')) subType = '估值拟合分析';
    } else if (segments.includes('shareholders')) {
      dataType = '股东数据';
      if (name.includes('pledge')) subType = '股东质押信息';
      else if (name.includes('fund-collection')) subType = '基金公司持股';
    } else if (segments.includes('capital-flow')) {
      dataType = '资金流向数据';
      if (name.includes('mutual-market')) subType = '沪深港通资金流';
    } else if (segments.includes('constituents')) {
      dataType = '成分股数据';
    } else if (segments.includes('followed-users')) {
      dataType = '关注用户列表';
    } else if (segments.includes('content')) {
      dataType = '内容数据';
      if (name.includes('memo')) subType = '用户备忘录';
    } else if (segments.includes('fees')) {
      dataType = '费用信息';
    } else if (segments.includes('employee')) {
      dataType = '员工信息';
    } else if (name.includes('chart-maker')) {
      return '图表制作工具 - 用于创建和管理自定义数据图表';
    } else if (segments.includes('open') && segments.includes('api')) {
      if (name.includes('doc')) return '开放API文档 - API接口说明和使用指南';
      return '开放API服务 - 提供数据接口访问';
    } else if (segments.includes('fund-list')) {
      dataType = '基金列表';
    } else if (segments.includes('user')) {
      if (name.includes('companies')) return '用户关注的公司列表';
      else if (name.includes('discussions')) return '用户发表的讨论帖子';
      else if (name.includes('memo')) return '用户的个人备忘录';
      else if (name.includes('account')) return '用户账户设置';
      else if (name.includes('notifications')) return '用户通知消息';
      else return '用户相关页面';
    } else if (segments.includes('profile')) {
      if (name.includes('center')) {
        if (name.includes('user-data')) return '个人中心 - 用户数据管理';
        else if (name.includes('my-followed')) return '个人中心 - 我的关注';
        return '个人中心';
      }
      return '个人资料页';
    } else if (segments.includes('macro')) {
      dataType = '宏观经济数据';
      if (name.includes('interest-rates')) subType = '利率数据';
      else if (name.includes('price-index')) subType = '价格指数';
    } else if (segments.includes('wiki')) {
      return '百科知识库';
    } else if (segments.includes('marketing')) {
      return '营销推广页面';
    } else if (segments.includes('payment')) {
      if (name.includes('place-order')) return '支付下单页面';
      return '支付相关页面';
    } else if (segments.includes('feedback')) {
      return '用户反馈帖子';
    } else if (segments.includes('model')) {
      return '数据模型分析工具';
    }
    
    // 特殊处理财报类型
    if (name.includes('-bs')) {
      dataType = '财务报表';
      subType = '资产负债表';
    } else if (name.includes('-ps')) {
      dataType = '财务报表';
      subType = '利润表';
    } else if (name.includes('-cfs')) {
      dataType = '财务报表';
      subType = '现金流量表';
    } else if (name.includes('-m') && market) {
      dataType = '财务数据';
      subType = '主要财务指标';
    }
    
    // 组合描述
    let description = '';
    
    if (market && assetType && dataType && subType) {
      description = `${market}${assetType}${pageType || ''} - ${dataType}(${subType})`;
    } else if (market && assetType && dataType) {
      description = `${market}${assetType}${pageType || ''} - ${dataType}`;
    } else if (market && assetType && pageType) {
      description = `${market}${assetType}${pageType}`;
    } else if (market && assetType) {
      description = `${market}${assetType}详情页`;
    } else if (assetType && dataType && subType) {
      description = `${assetType}${pageType || ''} - ${dataType}(${subType})`;
    } else if (assetType && dataType) {
      description = `${assetType}${pageType || ''} - ${dataType}`;
    } else if (assetType && pageType) {
      description = `${assetType}${pageType}`;
    } else if (dataType && subType) {
      description = `${dataType} - ${subType}`;
    } else if (dataType) {
      description = dataType;
    } else {
      // 兜底：使用简单翻译
      const SIMPLE_TRANS = {
        'sh': '上海', 'sz': '深圳', 'hk': '香港', 'nasdaq': '纳斯达克', 'nyse': '纽约',
        'csi': '中证', 'sw': '申万', 'sw_2021': '申万2021',
        'company': '公司', 'fund': '基金', 'index': '指数', 'industry': '行业',
        'detail': '详情', 'dashboard': '看板', 'list': '列表',
        'jjgs': '基金公司', 'fm': '基金经理', 'jj': '基金'
      };
      const words = name.split('-');
      description = words.map(w => SIMPLE_TRANS[w] || w).join('');
    }
    
    return description || name;
  }
}

module.exports = ReportGenerator;
