/**
 * 演示过滤器生成功能
 * 展示任务 4.4 的实现效果
 */

const TemplateConfigGenerator = require('../lib/template-config-generator');

console.log('=== 过滤器生成功能演示 ===\n');

const generator = new TemplateConfigGenerator();

// 模拟分析结果
const urlPattern = {
  name: 'api-doc',
  pattern: '/api/doc/.*',
  pathTemplate: '/api/doc/{key}',
  queryParams: ['key']
};

const analysisResult = {
  stats: {
    totalPages: 163
  },
  classified: {
    template: [
      { type: 'heading', content: 'API文档 - 理杏仁', ratio: 1.0 },
      { type: 'heading', content: '导航菜单', ratio: 0.98 },
      { type: 'paragraph', content: '版权所有 © 2024', ratio: 0.97 },
      { type: 'paragraph', content: '联系我们', ratio: 0.96 },
      { type: 'heading', content: '页脚信息', ratio: 0.95 }
    ],
    unique: [
      { type: 'paragraph', content: '获取A股公司基本信息', ratio: 0.006 },
      { type: 'paragraph', content: '查询指数成分股数据', ratio: 0.012 },
      { type: 'code', content: 'GET /api/v1/company', ratio: 0.018 },
      { type: 'paragraph', content: '参数说明：symbol为股票代码', ratio: 0.015 }
    ],
    mixed: []
  },
  dataStructures: {
    tables: [
      { columns: ['参数名称', '必选', '类型', '说明'] }
    ],
    codeBlocks: [
      { language: 'json', count: 5 }
    ],
    lists: []
  },
  cleaningRules: {
    removePatterns: [
      { target: 'heading', pattern: '返回顶部', reason: 'Navigation element' }
    ],
    keepPatterns: [
      { target: 'paragraph', contentType: 'api_description', reason: 'API documentation' }
    ]
  }
};

// 生成配置
const config = generator.generateConfig(urlPattern, analysisResult);

console.log('生成的配置：\n');
console.log(JSON.stringify(config, null, 2));

console.log('\n=== 过滤器详情 ===\n');

// 统计过滤器
const removeFilters = config.filters.filter(f => f.type === 'remove');
const keepFilters = config.filters.filter(f => f.type === 'keep');

console.log(`移除过滤器数量: ${removeFilters.length}`);
console.log('移除过滤器列表:');
removeFilters.forEach((filter, index) => {
  console.log(`  ${index + 1}. [${filter.target}] ${filter.pattern}`);
  console.log(`     原因: ${filter.reason}`);
});

console.log(`\n保留过滤器数量: ${keepFilters.length}`);
console.log('保留过滤器列表:');
keepFilters.forEach((filter, index) => {
  console.log(`  ${index + 1}. [${filter.target}] ${filter.contentType}`);
  console.log(`     原因: ${filter.reason}`);
});

console.log('\n=== 功能验证 ===\n');

// 验证任务 4.4.1: 基于高频内容生成移除规则
const highFreqFilters = removeFilters.filter(f => f.reason.includes('High frequency'));
console.log(`✓ 4.4.1 基于高频内容生成移除规则: ${highFreqFilters.length} 个`);

// 验证任务 4.4.2: 基于低频内容生成保留规则
const uniqueFilters = keepFilters.filter(f => f.reason.includes('Unique data'));
console.log(`✓ 4.4.2 基于低频内容生成保留规则: ${uniqueFilters.length} 个`);

// 验证任务 4.4.3: 添加规则说明和原因
const allHaveReasons = config.filters.every(f => f.reason && f.reason.length > 0);
console.log(`✓ 4.4.3 所有过滤器都有说明和原因: ${allHaveReasons ? '是' : '否'}`);

console.log('\n=== 演示完成 ===\n');
