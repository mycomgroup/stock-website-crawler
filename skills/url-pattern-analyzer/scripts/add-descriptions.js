#!/usr/bin/env node

/**
 * 为URL模式添加中文描述
 * 
 * 用法:
 *   node add-descriptions.js <input-json> [output-json]
 * 
 * 示例:
 *   node add-descriptions.js url-patterns.json url-patterns-with-desc.json
 */

const fs = require('fs');
const path = require('path');

// 中文映射表
const TRANSLATIONS = {
  // 市场/交易所
  'sh': '上海',
  'sz': '深圳',
  'hk': '香港',
  'nasdaq': '纳斯达克',
  'nyse': '纽约',
  'csi': '中证',
  'sw': '申万',
  'sw_2021': '申万2021',
  'lxr': '理杏仁',
  
  // 资产类型
  'company': '公司',
  'fund': '基金',
  'index': '指数',
  'industry': '行业',
  'bond': '债券',
  'macro': '宏观',
  
  // 页面类型
  'detail': '详情页',
  'dashboard': '看板',
  'list': '列表',
  'profile': '个人资料',
  'analytics': '分析',
  
  // 数据类型
  'fundamental': '基本面',
  'valuation': '估值',
  'shareholders': '股东',
  'capital-flow': '资金流向',
  'constituents': '成分股',
  'followed-users': '关注用户',
  'memo': '备忘录',
  'content': '内容',
  'fees': '费用',
  'pledge': '质押',
  'employee': '员工',
  
  // 基本面指标
  'peg': 'PEG估值',
  'dcf': 'DCF估值',
  'costs': '成本分析',
  'safety': '安全性分析',
  'profit': '盈利能力',
  'growth': '成长性',
  'cashflow': '现金流',
  'operation-capability': '运营能力',
  'custom-chart': '自定义图表',
  
  // 其他
  'mutual-market': '互联互通',
  'chart-maker': '图表制作',
  'open-api': '开放API',
  'user': '用户',
  'wiki': '百科',
  'marketing': '营销',
  'payment': '支付',
  'interest-rates': '利率',
  'price-index': '价格指数',
  'fund-collection': '基金公司',
  'fund-manager': '基金经理',
  'jjgs': '基金公司',
  'fm': '基金经理',
  'jj': '基金',
  'post': '帖子',
  'discussions': '讨论',
  'companies': '公司列表',
  'account': '账户',
  'notifications': '通知',
  'place-order': '下单',
  'my-followed': '我的关注',
  'center': '中心',
  'user-data': '用户数据',
  'model': '模型',
  'primary': '主要指标',
  'fitting': '拟合分析',
  'doc': '文档',
  'token': '令牌',
  'orders': '订单',
  'my-apis': '我的API',
  'receipts': '收据',
  'bs': '资产负债表',
  'ps': '利润表',
  'cfs': '现金流量表',
  'm': '主要指标'
};

/**
 * 根据URL路径和样本生成中文描述
 */
function generateDescription(pattern) {
  const { name, pathTemplate, samples, urlCount } = pattern;
  
  // 解析路径段
  const segments = pathTemplate.split('/').filter(s => s && !s.startsWith('{'));
  
  // 构建描述
  let description = '';
  let market = '';
  let assetType = '';
  let pageType = '';
  let dataType = '';
  
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
  
  // 识别页面类型
  if (segments.includes('detail')) pageType = '详情';
  else if (segments.includes('dashboard')) pageType = '看板';
  else if (segments.includes('list')) pageType = '列表';
  
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
    if (name.includes('mutual-market')) dataType = '互联互通资金流';
    else dataType = '资金流向';
  } else if (segments.includes('constituents')) {
    dataType = '成分股';
  } else if (segments.includes('followed-users')) {
    dataType = '关注用户';
  } else if (segments.includes('content')) {
    if (name.includes('memo')) dataType = '备忘录';
    else dataType = '内容';
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
    if (name.includes('center')) dataType = '个人中心';
    else dataType = '个人资料';
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
  if (market && assetType && dataType) {
    description = `${market}${assetType}${dataType}`;
  } else if (market && assetType && pageType) {
    description = `${market}${assetType}${pageType}`;
  } else if (assetType && dataType) {
    description = `${assetType}${dataType}`;
  } else if (assetType && pageType) {
    description = `${assetType}${pageType}`;
  } else if (dataType) {
    description = dataType;
  } else if (market && assetType) {
    description = `${market}${assetType}`;
  } else {
    // 兜底：使用name的翻译
    const words = name.split('-');
    const translated = words.map(w => TRANSLATIONS[w] || w).join('');
    description = translated || name;
  }
  
  return description;
}

/**
 * 主函数
 */
function main() {
  const args = process.argv.slice(2);
  
  if (args.length < 1) {
    console.error('用法: node add-descriptions.js <input-json> [output-json]');
    console.error('示例: node add-descriptions.js url-patterns.json url-patterns-with-desc.json');
    process.exit(1);
  }
  
  const inputFile = args[0];
  const outputFile = args[1] || inputFile.replace('.json', '-with-desc.json');
  
  // 读取输入文件
  if (!fs.existsSync(inputFile)) {
    console.error(`错误: 文件不存在: ${inputFile}`);
    process.exit(1);
  }
  
  console.log(`读取文件: ${inputFile}`);
  const data = JSON.parse(fs.readFileSync(inputFile, 'utf-8'));
  
  // 为每个模式添加描述
  let addedCount = 0;
  let updatedCount = 0;
  
  data.patterns.forEach(pattern => {
    const description = generateDescription(pattern);
    
    if (!pattern.description) {
      pattern.description = description;
      addedCount++;
    } else if (pattern.description !== description) {
      pattern.description = description;
      updatedCount++;
    }
  });
  
  // 保存输出文件
  fs.writeFileSync(outputFile, JSON.stringify(data, null, 2), 'utf-8');
  
  console.log(`\n✓ 处理完成！`);
  console.log(`  - 新增描述: ${addedCount} 个`);
  console.log(`  - 更新描述: ${updatedCount} 个`);
  console.log(`  - 总模式数: ${data.patterns.length} 个`);
  console.log(`\n输出文件: ${outputFile}`);
  
  // 显示前10个示例
  console.log(`\n前10个模式的描述:`);
  data.patterns.slice(0, 10).forEach((p, i) => {
    console.log(`${i + 1}. ${p.name}`);
    console.log(`   ${p.description} (${p.urlCount}个URL)`);
  });
}

// 运行
if (require.main === module) {
  main();
}

module.exports = { generateDescription };
