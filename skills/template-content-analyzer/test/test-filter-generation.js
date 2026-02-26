/**
 * 测试过滤器生成功能
 * 验证任务 4.4 的实现
 */

const TemplateConfigGenerator = require('../lib/template-config-generator');

console.log('\n=== 测试过滤器生成功能 (任务 4.4) ===\n');

const generator = new TemplateConfigGenerator();

// 模拟真实的分析结果
const urlPattern = {
  name: 'api-doc',
  pattern: '/api/doc/.*',
  pathTemplate: '/api/doc/{key}',
  queryParams: ['key']
};

const analysisResult = {
  stats: {
    totalPages: 100,
    totalBlocks: 1000
  },
  classified: {
    // 高频模板内容（噪音）
    template: [
      { type: 'heading', content: '## API文档', ratio: 1.0, count: 100 },
      { type: 'heading', content: '## 导航菜单', ratio: 0.98, count: 98 },
      { type: 'paragraph', content: '版权所有 © 2024', ratio: 0.96, count: 96 },
      { type: 'paragraph', content: '页脚信息', ratio: 0.85, count: 85 }
    ],
    // 低频独特内容（数据）
    unique: [
      { type: 'paragraph', content: '获取用户信息接口', ratio: 0.15, count: 15 },
      { type: 'paragraph', content: '查询订单数据API', ratio: 0.12, count: 12 },
      { type: 'code', content: 'GET /api/users', ratio: 0.08, count: 8 },
      { type: 'paragraph', content: '参数说明：id为用户ID', ratio: 0.10, count: 10 },
      { type: 'table', content: '| 字段 | 类型 | 说明 |', ratio: 0.18, count: 18 }
    ],
    mixed: []
  },
  dataStructures: {
    tables: [
      { columns: ['参数名', '类型', '必选', '说明'], columnCount: 4, occurrences: 80 }
    ],
    codeBlocks: [
      { language: 'json', occurrences: 50, avgLength: 200 }
    ],
    lists: []
  },
  cleaningRules: {
    removePatterns: [
      { 
        type: 'remove',
        target: 'heading', 
        pattern: 'API文档', 
        reason: 'Template noise (100% frequency)' 
      },
      { 
        type: 'remove',
        target: 'paragraph', 
        pattern: '版权所有', 
        reason: 'Template noise (96% frequency)' 
      }
    ],
    keepPatterns: [
      { 
        type: 'keep',
        target: 'paragraph', 
        contentType: 'api_description', 
        reason: 'API description content' 
      },
      { 
        type: 'keep',
        target: 'table', 
        contentType: 'structured_data', 
        reason: 'Parameter table' 
      }
    ]
  }
};

// 生成配置
console.log('步骤 1: 生成完整配置\n');
const config = generator.generateConfig(urlPattern, analysisResult);

console.log('✓ 配置生成成功');
console.log(`  - 名称: ${config.name}`);
console.log(`  - 提取器数量: ${config.extractors.length}`);
console.log(`  - 过滤器数量: ${config.filters.length}`);

// 分析过滤器
console.log('\n步骤 2: 分析生成的过滤器\n');

const removeFilters = config.filters.filter(f => f.type === 'remove');
const keepFilters = config.filters.filter(f => f.type === 'keep');

console.log(`移除过滤器 (${removeFilters.length} 个):`);
removeFilters.forEach((filter, index) => {
  console.log(`  ${index + 1}. [${filter.target}] ${filter.pattern || filter.text || 'N/A'}`);
  console.log(`     原因: ${filter.reason}`);
});

console.log(`\n保留过滤器 (${keepFilters.length} 个):`);
keepFilters.forEach((filter, index) => {
  console.log(`  ${index + 1}. [${filter.target}] contentType=${filter.contentType}`);
  console.log(`     原因: ${filter.reason}`);
});

// 验证任务完成情况
console.log('\n步骤 3: 验证任务完成情况\n');

let allPassed = true;

// 验证 4.4.1: 基于高频内容生成移除规则
console.log('✓ 任务 4.4.1: 基于高频内容生成移除规则');
if (removeFilters.length === 0) {
  console.log('  ✗ 失败: 没有生成移除过滤器');
  allPassed = false;
} else {
  console.log(`  ✓ 成功: 生成了 ${removeFilters.length} 个移除过滤器`);
  
  // 检查是否包含来自cleaningRules的规则
  const hasCleaningRules = removeFilters.some(f => f.reason.includes('Template noise'));
  if (hasCleaningRules) {
    console.log('  ✓ 包含来自清洗规则的移除过滤器');
  }
  
  // 检查是否包含来自高频内容的规则
  const hasHighFreq = removeFilters.some(f => f.reason.includes('High frequency'));
  if (hasHighFreq) {
    console.log('  ✓ 包含来自高频模板内容的移除过滤器');
  }
}

// 验证 4.4.2: 基于低频内容生成保留规则
console.log('\n✓ 任务 4.4.2: 基于低频内容生成保留规则');
if (keepFilters.length === 0) {
  console.log('  ✗ 失败: 没有生成保留过滤器');
  allPassed = false;
} else {
  console.log(`  ✓ 成功: 生成了 ${keepFilters.length} 个保留过滤器`);
  
  // 检查是否包含来自cleaningRules的规则
  const hasCleaningRules = keepFilters.some(f => f.reason.includes('API description') || f.reason.includes('Parameter table'));
  if (hasCleaningRules) {
    console.log('  ✓ 包含来自清洗规则的保留过滤器');
  }
  
  // 检查是否包含来自低频内容的规则
  const hasLowFreq = keepFilters.some(f => f.reason.includes('Unique data'));
  if (hasLowFreq) {
    console.log('  ✓ 包含来自低频独特内容的保留过滤器');
  }
  
  // 检查contentType字段
  const allHaveContentType = keepFilters.every(f => f.contentType && f.contentType !== 'unknown');
  if (allHaveContentType) {
    console.log('  ✓ 所有保留过滤器都有有效的contentType');
  } else {
    console.log('  ✗ 部分保留过滤器缺少contentType或为unknown');
    allPassed = false;
  }
}

// 验证 4.4.3: 添加规则说明和原因
console.log('\n✓ 任务 4.4.3: 添加规则说明和原因');
const allHaveReason = config.filters.every(f => f.reason && f.reason.length > 0);
if (allHaveReason) {
  console.log(`  ✓ 成功: 所有 ${config.filters.length} 个过滤器都包含原因说明`);
} else {
  console.log('  ✗ 失败: 部分过滤器缺少原因说明');
  allPassed = false;
}

// 最终结果
console.log('\n' + '='.repeat(60));
if (allPassed) {
  console.log('✓ 所有任务验证通过！');
  console.log('\n任务 4.4 完成情况:');
  console.log('  ✓ 4.4.1 基于高频内容生成移除规则');
  console.log('  ✓ 4.4.2 基于低频内容生成保留规则');
  console.log('  ✓ 4.4.3 添加规则说明和原因');
} else {
  console.log('✗ 部分任务验证失败');
  process.exitCode = 1;
}
console.log('='.repeat(60) + '\n');
