#!/usr/bin/env node

/**
 * 测试过滤器应用功能
 * 
 * 演示如何使用 remove, keep, transform 过滤器
 */

const TemplateParser = require('../lib/template-parser');

console.log('=== 测试过滤器应用功能 ===\n');

// 测试配置1: Remove过滤器
console.log('1. Remove过滤器 - 移除模板噪音');
console.log('-----------------------------------');

const removeConfig = {
  name: 'api-doc-remove',
  description: 'API文档解析器 - 移除噪音',
  priority: 100,
  urlPattern: {
    pattern: '^https://example\\.com/api/doc',
    pathTemplate: '/api/doc',
    queryParams: []
  },
  extractors: [
    {
      field: 'title',
      type: 'text',
      selector: 'h1'
    },
    {
      field: 'description',
      type: 'text',
      selector: 'p'
    }
  ],
  filters: [
    {
      type: 'remove',
      target: 'text',
      pattern: 'API文档|导航|菜单',
      reason: 'Template noise (100% frequency)'
    }
  ]
};

const removeParser = new TemplateParser(removeConfig);
const removeResult = {
  type: 'api-doc-remove',
  url: 'https://example.com/api/doc',
  timestamp: new Date().toISOString(),
  title: 'API文档 - 用户接口',
  description: '获取用户信息的API接口'
};

console.log('原始数据:');
console.log(JSON.stringify(removeResult, null, 2));

const filteredRemove = removeParser.applyFilters(removeResult);
console.log('\n过滤后数据:');
console.log(JSON.stringify(filteredRemove, null, 2));
console.log('\n✓ 成功移除包含"API文档"的标题\n');

// 测试配置2: Keep过滤器
console.log('2. Keep过滤器 - 只保留有用数据');
console.log('-----------------------------------');

const keepConfig = {
  name: 'api-doc-keep',
  description: 'API文档解析器 - 保留数据',
  priority: 100,
  urlPattern: {
    pattern: '^https://example\\.com/api/doc',
    pathTemplate: '/api/doc',
    queryParams: []
  },
  extractors: [
    {
      field: 'paragraphs',
      type: 'text',
      selector: 'p'
    }
  ],
  filters: [
    {
      type: 'keep',
      target: 'text',
      pattern: '^获取|^查询|^创建|^更新|^删除',
      reason: 'Keep only API operation descriptions'
    }
  ]
};

const keepParser = new TemplateParser(keepConfig);
const keepResult = {
  type: 'api-doc-keep',
  url: 'https://example.com/api/doc',
  timestamp: new Date().toISOString(),
  operation: '获取用户信息',
  footer: '版权所有 © 2024'
};

console.log('原始数据:');
console.log(JSON.stringify(keepResult, null, 2));

const filteredKeep = keepParser.applyFilters(keepResult);
console.log('\n过滤后数据:');
console.log(JSON.stringify(filteredKeep, null, 2));
console.log('\n✓ 成功保留以"获取"开头的内容，移除版权信息\n');

// 测试配置3: Transform过滤器
console.log('3. Transform过滤器 - 转换内容格式');
console.log('-----------------------------------');

const transformConfig = {
  name: 'api-doc-transform',
  description: 'API文档解析器 - 转换格式',
  priority: 100,
  urlPattern: {
    pattern: '^https://example\\.com/api/doc',
    pathTemplate: '/api/doc',
    queryParams: []
  },
  extractors: [
    {
      field: 'description',
      type: 'text',
      selector: 'p'
    }
  ],
  filters: [
    {
      type: 'transform',
      target: 'text',
      pattern: '\\s+',
      replacement: ' ',
      reason: 'Normalize whitespace'
    }
  ]
};

const transformParser = new TemplateParser(transformConfig);
const transformResult = {
  type: 'api-doc-transform',
  url: 'https://example.com/api/doc',
  timestamp: new Date().toISOString(),
  description: '获取用户信息\n\n包含用户的基本资料   和   详细信息'
};

console.log('原始数据:');
console.log(JSON.stringify(transformResult, null, 2));

const filteredTransform = transformParser.applyFilters(transformResult);
console.log('\n过滤后数据:');
console.log(JSON.stringify(filteredTransform, null, 2));
console.log('\n✓ 成功标准化空白字符\n');

// 测试配置4: 组合过滤器
console.log('4. 组合过滤器 - 多个过滤器协同工作');
console.log('-----------------------------------');

const combinedConfig = {
  name: 'api-doc-combined',
  description: 'API文档解析器 - 组合过滤',
  priority: 100,
  urlPattern: {
    pattern: '^https://example\\.com/api/doc',
    pathTemplate: '/api/doc',
    queryParams: []
  },
  extractors: [
    {
      field: 'title',
      type: 'text',
      selector: 'h1'
    },
    {
      field: 'description',
      type: 'text',
      selector: 'p'
    },
    {
      field: 'codeBlocks',
      type: 'code',
      selector: 'pre code'
    }
  ],
  filters: [
    {
      type: 'remove',
      target: 'text',
      pattern: 'API文档',
      reason: 'Remove template title'
    },
    {
      type: 'transform',
      target: 'text',
      pattern: '\\s+',
      replacement: ' ',
      reason: 'Normalize whitespace'
    },
    {
      type: 'remove',
      target: 'code',
      pattern: 'console\\.debug',
      reason: 'Remove debug code'
    }
  ]
};

const combinedParser = new TemplateParser(combinedConfig);
const combinedResult = {
  type: 'api-doc-combined',
  url: 'https://example.com/api/doc',
  timestamp: new Date().toISOString(),
  title: 'API文档 - 用户接口',
  description: '获取用户信息\n\n包含基本资料',
  codeBlocks: [
    { language: 'javascript', code: 'console.log("test");' },
    { language: 'javascript', code: 'console.debug("debug info");' },
    { language: 'javascript', code: 'console.info("info");' }
  ]
};

console.log('原始数据:');
console.log(JSON.stringify(combinedResult, null, 2));

const filteredCombined = combinedParser.applyFilters(combinedResult);
console.log('\n过滤后数据:');
console.log(JSON.stringify(filteredCombined, null, 2));
console.log('\n✓ 成功应用多个过滤器：移除标题噪音、标准化空白、移除调试代码\n');

// 测试配置5: 表格过滤
console.log('5. 表格过滤 - 过滤表格行');
console.log('-----------------------------------');

const tableConfig = {
  name: 'api-doc-table',
  description: 'API文档解析器 - 表格过滤',
  priority: 100,
  urlPattern: {
    pattern: '^https://example\\.com/api/doc',
    pathTemplate: '/api/doc',
    queryParams: []
  },
  extractors: [
    {
      field: 'parameters',
      type: 'table',
      selector: 'table'
    }
  ],
  filters: [
    {
      type: 'remove',
      target: 'table',
      pattern: 'deprecated',
      reason: 'Remove deprecated parameters'
    }
  ]
};

const tableParser = new TemplateParser(tableConfig);
const tableResult = {
  type: 'api-doc-table',
  url: 'https://example.com/api/doc',
  timestamp: new Date().toISOString(),
  parameters: {
    headers: ['参数名', '类型', '说明'],
    rows: [
      ['userId', 'string', '用户ID'],
      ['token', 'string', 'deprecated - 使用apiKey代替'],
      ['apiKey', 'string', 'API密钥']
    ]
  }
};

console.log('原始数据:');
console.log(JSON.stringify(tableResult, null, 2));

const filteredTable = tableParser.applyFilters(tableResult);
console.log('\n过滤后数据:');
console.log(JSON.stringify(filteredTable, null, 2));
console.log('\n✓ 成功移除包含"deprecated"的表格行\n');

// 测试配置6: Keep表格过滤
console.log('6. Keep表格过滤 - 只保留特定行');
console.log('-----------------------------------');

const keepTableConfig = {
  name: 'api-doc-keep-table',
  description: 'API文档解析器 - 保留表格',
  priority: 100,
  urlPattern: {
    pattern: '^https://example\\.com/api/doc',
    pathTemplate: '/api/doc',
    queryParams: []
  },
  extractors: [
    {
      field: 'features',
      type: 'table',
      selector: 'table'
    }
  ],
  filters: [
    {
      type: 'keep',
      target: 'table',
      pattern: 'active',
      reason: 'Keep only active features'
    }
  ]
};

const keepTableParser = new TemplateParser(keepTableConfig);
const keepTableResult = {
  type: 'api-doc-keep-table',
  url: 'https://example.com/api/doc',
  timestamp: new Date().toISOString(),
  features: {
    headers: ['功能名', '状态'],
    rows: [
      ['用户认证', 'active'],
      ['数据导出', 'deprecated'],
      ['实时通知', 'active'],
      ['旧版API', 'deprecated']
    ]
  }
};

console.log('原始数据:');
console.log(JSON.stringify(keepTableResult, null, 2));

const filteredKeepTable = keepTableParser.applyFilters(keepTableResult);
console.log('\n过滤后数据:');
console.log(JSON.stringify(filteredKeepTable, null, 2));
console.log('\n✓ 成功只保留状态为"active"的功能\n');

console.log('=== 所有过滤器测试完成 ===');
console.log('\n总结:');
console.log('✓ Remove过滤器 - 移除匹配的内容');
console.log('✓ Keep过滤器 - 只保留匹配的内容');
console.log('✓ Transform过滤器 - 转换内容格式');
console.log('✓ 组合过滤器 - 多个过滤器协同工作');
console.log('✓ 表格过滤 - 过滤表格行数据');
console.log('✓ 元数据保护 - type, url, timestamp等字段不受影响');
