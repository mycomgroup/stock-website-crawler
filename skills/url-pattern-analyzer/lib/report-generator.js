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
        pathTemplate: patternInfo.pathTemplate,
        pattern: patternInfo.pattern,
        queryParams: patternInfo.queryParams,
        urlCount: urlGroup.length,
        samples,
        description
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
    
    // 中文映射表
    const TRANSLATIONS = {
      // 市场/交易所
      'sh': '上海', 'sz': '深圳', 'hk': '香港',
      'nasdaq': '纳斯达克', 'nyse': '纽约',
      'csi': '中证', 'sw': '申万', 'sw_2021': '申万2021', 'lxr': '理杏仁',
      
      // 资产类型
      'company': '公司', 'fund': '基金', 'index': '指数',
      'industry': '行业', 'bond': '债券', 'macro': '宏观',
      
      // 页面类型
      'detail': '详情', 'dashboard': '看板', 'list': '列表',
      'profile': '资料', 'analytics': '分析',
      
      // 数据类型
      'fundamental': '基本面', 'valuation': '估值', 'shareholders': '股东',
      'capital-flow': '资金流向', 'constituents': '成分股',
      'followed-users': '关注用户', 'memo': '备忘录', 'content': '内容',
      'fees': '费用', 'pledge': '质押', 'employee': '员工',
      
      // 基本面指标
      'peg': 'PEG估值', 'dcf': 'DCF估值', 'costs': '成本分析',
      'safety': '安全性', 'profit': '盈利能力', 'growth': '成长性',
      'cashflow': '现金流', 'operation-capability': '运营能力',
      'custom-chart': '自定义图表',
      
      // 其他
      'mutual-market': '互联互通', 'chart-maker': '图表制作',
      'open': '开放', 'api': 'API', 'user': '用户', 'wiki': '百科',
      'marketing': '营销', 'payment': '支付', 'interest-rates': '利率',
      'price-index': '价格指数', 'fund-collection': '基金公司',
      'fund-manager': '基金经理', 'jjgs': '基金公司', 'fm': '基金经理',
      'jj': '基金', 'post': '帖子', 'discussions': '讨论',
      'companies': '公司列表', 'account': '账户', 'notifications': '通知',
      'place-order': '下单', 'my-followed': '我的关注', 'center': '中心',
      'user-data': '用户数据', 'model': '模型', 'primary': '主要指标',
      'fitting': '拟合', 'doc': '文档', 'token': '令牌', 'orders': '订单',
      'my-apis': '我的API', 'receipts': '收据',
      'bs': '资产负债表', 'ps': '利润表', 'cfs': '现金流量表', 'm': '主要指标'
    };
    
    // 解析路径段
    const segments = pathTemplate.split('/').filter(s => s && !s.startsWith('{'));
    
    let market = '', assetType = '', dataType = '';
    
    // 识别市场
    if (pathTemplate.includes('/sh/')) market = '上海';
    else if (pathTemplate.includes('/sz/')) market = '深圳';
    else if (pathTemplate.includes('/hk/')) market = '香港';
    else if (pathTemplate.includes('/nasdaq/')) market = '纳斯达克';
    else if (pathTemplate.includes('/nyse/')) market = '纽约';
    else if (pathTemplate.includes('/csi/')) market = '中证';
    else if (pathTemplate.includes('/sw_2021/')) market = '申万2021';
    else if (pathTemplate.includes('/sw/')) market = '申万';
    
    // 识别资产类型
    if (segments.includes('company')) assetType = '公司';
    else if (segments.includes('fund')) assetType = '基金';
    else if (segments.includes('index')) assetType = '指数';
    else if (segments.includes('industry')) assetType = '行业';
    else if (segments.includes('bond')) assetType = '债券';
    
    // 识别数据类型
    if (segments.includes('fundamental')) {
      if (name.includes('peg')) dataType = 'PEG估值';
      else if (name.includes('dcf')) dataType = 'DCF估值';
      else if (name.includes('costs')) dataType = '成本分析';
      else if (name.includes('safety')) dataType = '安全性';
      else if (name.includes('profit')) dataType = '盈利能力';
      else if (name.includes('growth')) dataType = '成长性';
      else if (name.includes('cashflow')) dataType = '现金流';
      else if (name.includes('operation-capability')) dataType = '运营能力';
      else if (name.includes('custom-chart')) dataType = '自定义图表';
      else if (name.includes('valuation')) dataType = '估值分析';
      else dataType = '基本面分析';
    } else if (segments.includes('valuation')) {
      if (name.includes('primary')) dataType = '估值主要指标';
      else if (name.includes('fitting')) dataType = '估值拟合';
      else dataType = '估值分析';
    } else if (segments.includes('shareholders')) {
      if (name.includes('pledge')) dataType = '股东质押';
      else if (name.includes('fund-collection')) dataType = '基金公司持股';
      else dataType = '股东信息';
    } else if (segments.includes('capital-flow')) {
      dataType = name.includes('mutual-market') ? '互联互通资金流' : '资金流向';
    } else if (segments.includes('constituents')) {
      dataType = '成分股';
    } else if (segments.includes('followed-users')) {
      dataType = '关注用户';
    } else if (segments.includes('content')) {
      dataType = name.includes('memo') ? '备忘录' : '内容';
    } else if (segments.includes('fees')) {
      dataType = '费用信息';
    } else if (segments.includes('employee')) {
      dataType = '员工信息';
    } else if (name.includes('chart-maker')) {
      dataType = '图表制作工具';
    } else if (segments.includes('open') && segments.includes('api')) {
      dataType = '开放API';
    } else if (segments.includes('fund-list')) {
      dataType = '基金列表';
    } else if (segments.includes('fund-manager')) {
      dataType = '基金经理';
    } else if (segments.includes('fund-collection')) {
      dataType = '基金公司';
    } else if (segments.includes('user')) {
      if (name.includes('companies')) dataType = '用户关注公司';
      else if (name.includes('discussions')) dataType = '用户讨论';
      else if (name.includes('memo')) dataType = '用户备忘录';
      else if (name.includes('account')) dataType = '账户设置';
      else if (name.includes('notifications')) dataType = '通知';
      else dataType = '用户';
    } else if (segments.includes('profile')) {
      dataType = name.includes('center') ? '个人中心' : '个人资料';
    } else if (segments.includes('macro')) {
      if (name.includes('interest-rates')) dataType = '利率数据';
      else if (name.includes('price-index')) dataType = '价格指数';
      else dataType = '宏观数据';
    } else if (segments.includes('wiki')) {
      dataType = '百科';
    } else if (segments.includes('marketing')) {
      dataType = '营销页面';
    } else if (segments.includes('payment')) {
      dataType = '支付';
    } else if (segments.includes('feedback')) {
      dataType = '反馈帖子';
    } else if (segments.includes('model')) {
      dataType = '模型';
    }
    
    // 特殊处理财报类型
    if (name.includes('-bs')) dataType = '资产负债表';
    else if (name.includes('-ps')) dataType = '利润表';
    else if (name.includes('-cfs')) dataType = '现金流量表';
    else if (name.includes('-m') && market) dataType = '主要指标';
    
    // 组合描述
    let description = '';
    if (market && assetType && dataType) {
      description = `${market}${assetType}${dataType}`;
    } else if (market && assetType) {
      description = `${market}${assetType}详情`;
    } else if (assetType && dataType) {
      description = `${assetType}${dataType}`;
    } else if (dataType) {
      description = dataType;
    } else {
      // 兜底：翻译name
      const words = name.split('-');
      description = words.map(w => TRANSLATIONS[w] || w).join('');
    }
    
    return description || name;
  }
}

module.exports = ReportGenerator;
