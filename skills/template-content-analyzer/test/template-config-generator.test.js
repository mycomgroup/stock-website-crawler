/**
 * TemplateConfigGenerator 单元测试
 */

const TemplateConfigGenerator = require('../lib/template-config-generator');
const fs = require('fs').promises;
const path = require('path');
const os = require('os');

// 简单的测试框架
function test(description, fn) {
  try {
    fn();
    console.log(`✓ ${description}`);
  } catch (error) {
    console.error(`✗ ${description}`);
    console.error(`  ${error.message}`);
    process.exitCode = 1;
  }
}

async function testAsync(description, fn) {
  try {
    await fn();
    console.log(`✓ ${description}`);
  } catch (error) {
    console.error(`✗ ${description}`);
    console.error(`  ${error.message}`);
    process.exitCode = 1;
  }
}

function assertEquals(actual, expected, message) {
  if (JSON.stringify(actual) !== JSON.stringify(expected)) {
    throw new Error(message || `Expected ${JSON.stringify(expected)}, got ${JSON.stringify(actual)}`);
  }
}

function assertTrue(condition, message) {
  if (!condition) {
    throw new Error(message || 'Expected condition to be true');
  }
}

function assertGreaterThan(actual, expected, message) {
  if (actual <= expected) {
    throw new Error(message || `Expected ${actual} to be greater than ${expected}`);
  }
}

function assertLessThanOrEqual(actual, expected, message) {
  if (actual > expected) {
    throw new Error(message || `Expected ${actual} to be less than or equal to ${expected}`);
  }
}

// 测试套件
console.log('\n=== TemplateConfigGenerator 单元测试 ===\n');

const generator = new TemplateConfigGenerator();

// 测试1: generateConfig() - 生成完整配置对象
test('应该生成完整的配置对象', () => {
  const urlPattern = {
    name: 'test-pattern',
    pattern: '/test/.*',
    pathTemplate: '/test/{id}',
    queryParams: ['id']
  };

  const analysisResult = {
    stats: {
      totalPages: 10,
      totalBlocks: 100
    },
    classified: {
      template: [],
      unique: [],
      mixed: []
    },
    dataStructures: {
      tables: [],
      codeBlocks: [],
      lists: []
    },
    cleaningRules: {
      removePatterns: []
    }
  };

  const config = generator.generateConfig(urlPattern, analysisResult);

  assertTrue(config.name === 'test-pattern', '应该有name字段');
  assertTrue(config.description !== undefined, '应该有description字段');
  assertTrue(config.priority === 100, '应该有priority字段');
  assertTrue(config.urlPattern !== undefined, '应该有urlPattern字段');
  assertTrue(Array.isArray(config.extractors), '应该有extractors数组');
  assertTrue(Array.isArray(config.filters), '应该有filters数组');
  assertTrue(config.metadata !== undefined, '应该有metadata字段');
  assertTrue(config.metadata.generatedAt !== undefined, '应该有generatedAt');
  assertTrue(config.metadata.pageCount === 10, '应该有pageCount');
  assertTrue(config.metadata.version === '1.0.0', '应该有version');
});

// 测试2: generateConfig() - 包含URL模式详情
test('应该包含URL模式详情', () => {
  const urlPattern = {
    name: 'api-doc',
    pattern: '/api/doc/.*',
    pathTemplate: '/api/doc/{key}',
    queryParams: ['key', 'version']
  };

  const analysisResult = {
    stats: { totalPages: 5 },
    classified: { template: [], unique: [], mixed: [] },
    dataStructures: { tables: [], codeBlocks: [], lists: [] },
    cleaningRules: { removePatterns: [] }
  };

  const config = generator.generateConfig(urlPattern, analysisResult);

  assertEquals(config.urlPattern.pattern, '/api/doc/.*', 'pattern应该匹配');
  assertEquals(config.urlPattern.pathTemplate, '/api/doc/{key}', 'pathTemplate应该匹配');
  assertEquals(config.urlPattern.queryParams, ['key', 'version'], 'queryParams应该匹配');
});

// 测试3: generateExtractors() - 总是包含标题提取器
test('应该总是包含标题提取器', () => {
  const dataStructures = {
    tables: [],
    codeBlocks: [],
    lists: []
  };
  const classified = { template: [], unique: [], mixed: [] };

  const extractors = generator.generateExtractors(dataStructures, classified);

  assertGreaterThan(extractors.length, 0, '应该至少有一个提取器');
  assertEquals(extractors[0], {
    field: 'title',
    type: 'text',
    selector: 'h1, h2, title',
    required: true
  }, '第一个应该是标题提取器');
});

// 测试4: generateExtractors() - 生成表格提取器
test('应该生成表格提取器', () => {
  const dataStructures = {
    tables: [
      { columns: ['Name', 'Age', 'City'] },
      { columns: ['Product', 'Price'] }
    ],
    codeBlocks: [],
    lists: []
  };
  const classified = { template: [], unique: [], mixed: [] };

  const extractors = generator.generateExtractors(dataStructures, classified);

  const tableExtractors = extractors.filter(e => e.type === 'table');
  assertEquals(tableExtractors.length, 2, '应该有2个表格提取器');
  assertEquals(tableExtractors[0].field, 'mainTable', '第一个应该是mainTable');
  assertEquals(tableExtractors[0].columns, ['Name', 'Age', 'City'], '列名应该匹配');
  assertEquals(tableExtractors[1].field, 'table1', '第二个应该是table1');
  assertEquals(tableExtractors[1].columns, ['Product', 'Price'], '列名应该匹配');
});

// 测试5: generateExtractors() - 生成代码块提取器
test('应该生成代码块提取器', () => {
  const dataStructures = {
    tables: [],
    codeBlocks: [{ language: 'javascript', count: 5 }],
    lists: []
  };
  const classified = { template: [], unique: [], mixed: [] };

  const extractors = generator.generateExtractors(dataStructures, classified);

  const codeExtractor = extractors.find(e => e.type === 'code');
  assertTrue(codeExtractor !== undefined, '应该有代码块提取器');
  assertEquals(codeExtractor.field, 'codeBlocks', 'field应该是codeBlocks');
  assertEquals(codeExtractor.selector, 'pre code, pre, textarea[readonly]', 'selector应该正确');
});

// 测试6: generateExtractors() - 生成列表提取器
test('应该生成列表提取器', () => {
  const dataStructures = {
    tables: [],
    codeBlocks: [],
    lists: [{ type: 'ul', count: 3 }]
  };
  const classified = { template: [], unique: [], mixed: [] };

  const extractors = generator.generateExtractors(dataStructures, classified);

  const listExtractor = extractors.find(e => e.type === 'list');
  assertTrue(listExtractor !== undefined, '应该有列表提取器');
  assertEquals(listExtractor.field, 'lists', 'field应该是lists');
  assertEquals(listExtractor.selector, 'ul, ol', 'selector应该正确');
});

// 测试7: generateExtractors() - 生成所有类型的提取器
test('应该生成所有类型的提取器', () => {
  const dataStructures = {
    tables: [{ columns: ['A', 'B'] }],
    codeBlocks: [{ language: 'python' }],
    lists: [{ type: 'ol' }]
  };
  const classified = { template: [], unique: [], mixed: [] };

  const extractors = generator.generateExtractors(dataStructures, classified);

  assertEquals(extractors.length, 4, '应该有4个提取器'); // title + table + code + list
  assertTrue(extractors.some(e => e.type === 'text'), '应该有text类型');
  assertTrue(extractors.some(e => e.type === 'table'), '应该有table类型');
  assertTrue(extractors.some(e => e.type === 'code'), '应该有code类型');
  assertTrue(extractors.some(e => e.type === 'list'), '应该有list类型');
});

// 测试8: generateFilters() - 从清洗规则生成过滤器
test('应该从清洗规则生成过滤器', () => {
  const cleaningRules = {
    removePatterns: [
      { target: 'heading', pattern: 'Navigation', reason: 'Template noise' },
      { target: 'paragraph', pattern: 'Footer', reason: 'Template noise' }
    ]
  };
  const classified = { template: [] };

  const filters = generator.generateFilters(cleaningRules, classified);

  assertGreaterThan(filters.length, 1, '应该至少有2个过滤器');
  assertEquals(filters[0], {
    type: 'remove',
    target: 'heading',
    pattern: 'Navigation',
    reason: 'Template noise'
  }, '第一个过滤器应该匹配');
  assertEquals(filters[1], {
    type: 'remove',
    target: 'paragraph',
    pattern: 'Footer',
    reason: 'Template noise'
  }, '第二个过滤器应该匹配');
});

// 测试9: generateFilters() - 从高频模板内容生成过滤器
test('应该从高频模板内容生成过滤器', () => {
  const cleaningRules = { removePatterns: [] };
  const classified = {
    template: [
      { type: 'heading', content: 'Common Header Text', ratio: 0.98 },
      { type: 'paragraph', content: 'Repeated paragraph content', ratio: 0.96 },
      { type: 'heading', content: 'Low frequency', ratio: 0.80 }
    ]
  };

  const filters = generator.generateFilters(cleaningRules, classified);

  assertGreaterThan(filters.length, 0, '应该有过滤器');
  const highFreqFilters = filters.filter(f => f.reason.includes('High frequency'));
  assertEquals(highFreqFilters.length, 2, '应该有2个高频过滤器'); // Only items with ratio > 0.95
});

// 测试10: generateFilters() - 避免重复过滤器
test('应该避免重复过滤器', () => {
  const cleaningRules = {
    removePatterns: [
      { target: 'heading', pattern: 'Common Header Text', reason: 'Template noise' }
    ]
  };
  const classified = {
    template: [
      { type: 'heading', content: 'Common Header Text', ratio: 0.98 }
    ]
  };

  const filters = generator.generateFilters(cleaningRules, classified);

  // 应该不创建重复的过滤器
  const headerFilters = filters.filter(f => f.pattern.includes('Common Header'));
  assertEquals(headerFilters.length, 1, '不应该有重复的过滤器');
});

// 测试11: generateFilters() - 限制额外过滤器数量
test('应该限制额外过滤器为5个', () => {
  const cleaningRules = { removePatterns: [] };
  const classified = {
    template: Array.from({ length: 10 }, (_, i) => ({
      type: 'paragraph',
      content: `Template content ${i}`,
      ratio: 0.96
    }))
  };

  const filters = generator.generateFilters(cleaningRules, classified);

  assertLessThanOrEqual(filters.length, 5, '过滤器数量应该不超过5个');
});

// 测试12: generateFilters() - 无清洗规则时返回空数组
test('无清洗规则时应该返回空数组', () => {
  const cleaningRules = { removePatterns: [] };
  const classified = { template: [] };

  const filters = generator.generateFilters(cleaningRules, classified);

  assertEquals(filters, [], '应该返回空数组');
});

// 测试13: _escapeRegex() - 转义特殊字符
test('应该转义正则表达式特殊字符', () => {
  const testCases = [
    { input: 'hello.world', expected: 'hello\\.world' },
    { input: 'test*pattern', expected: 'test\\*pattern' },
    { input: 'a+b?c', expected: 'a\\+b\\?c' },
    { input: 'x^y$z', expected: 'x\\^y\\$z' },
    { input: '{a}[b](c)|d', expected: '\\{a\\}\\[b\\]\\(c\\)\\|d' },
    { input: 'back\\slash', expected: 'back\\\\slash' }
  ];

  testCases.forEach(({ input, expected }) => {
    const result = generator._escapeRegex(input);
    assertEquals(result, expected, `转义"${input}"应该得到"${expected}"`);
  });
});

// 测试14: _escapeRegex() - 不修改普通字符串
test('不应该修改没有特殊字符的字符串', () => {
  const input = 'simple text without special chars';
  const result = generator._escapeRegex(input);
  assertEquals(result, input, '应该保持不变');
});

// 异步测试
async function runAsyncTests() {
  console.log('\n--- 异步测试 ---\n');
  
  const tempDir = await fs.mkdtemp(path.join(os.tmpdir(), 'config-gen-test-'));
  
  try {
    // 测试15: saveAsJSONL() - 保存为JSONL格式
    await testAsync('应该保存为JSONL格式', async () => {
      const configs = [
        { name: 'config1', extractors: [], filters: [] },
        { name: 'config2', extractors: [], filters: [] }
      ];
      const outputPath = path.join(tempDir, 'test-output.jsonl');

      await generator.saveAsJSONL(configs, outputPath);

      const content = await fs.readFile(outputPath, 'utf-8');
      const lines = content.trim().split('\n');

      assertEquals(lines.length, 2, '应该有2行');
      assertEquals(JSON.parse(lines[0]).name, 'config1', '第一行应该是config1');
      assertEquals(JSON.parse(lines[1]).name, 'config2', '第二行应该是config2');
    });

    // 测试16: saveAsJSONL() - 创建输出目录
    await testAsync('应该创建输出目录', async () => {
      const configs = [{ name: 'test', extractors: [], filters: [] }];
      const outputPath = path.join(tempDir, 'nested', 'dir', 'output.jsonl');

      await generator.saveAsJSONL(configs, outputPath);

      const exists = await fs.access(outputPath).then(() => true).catch(() => false);
      assertTrue(exists, '文件应该存在');
    });

    // 测试17: saveAsJSONL() - 处理空配置数组
    await testAsync('应该处理空配置数组', async () => {
      const configs = [];
      const outputPath = path.join(tempDir, 'empty.jsonl');

      await generator.saveAsJSONL(configs, outputPath);

      const content = await fs.readFile(outputPath, 'utf-8');
      assertEquals(content, '', '应该是空文件');
    });

    // 测试18: saveAsJSONL() - 保存复杂配置对象
    await testAsync('应该保存复杂配置对象', async () => {
      const configs = [
        {
          name: 'complex-config',
          description: 'Test config',
          priority: 100,
          urlPattern: {
            pattern: '/test/.*',
            pathTemplate: '/test/{id}',
            queryParams: ['id']
          },
          extractors: [
            { field: 'title', type: 'text', selector: 'h1' },
            { field: 'table', type: 'table', selector: 'table', columns: ['A', 'B'] }
          ],
          filters: [
            { type: 'remove', target: 'heading', pattern: 'Nav', reason: 'Noise' }
          ],
          metadata: {
            generatedAt: '2024-01-01T00:00:00.000Z',
            pageCount: 10,
            version: '1.0.0'
          }
        }
      ];
      const outputPath = path.join(tempDir, 'complex.jsonl');

      await generator.saveAsJSONL(configs, outputPath);

      const content = await fs.readFile(outputPath, 'utf-8');
      const parsed = JSON.parse(content);

      assertEquals(parsed, configs[0], '应该完全匹配');
    });

  } finally {
    // 清理临时目录
    await fs.rm(tempDir, { recursive: true, force: true });
  }
}

// 运行异步测试
runAsyncTests().then(() => {
  console.log('\n=== 测试完成 ===\n');
  if (process.exitCode === 1) {
    console.log('部分测试失败！');
  } else {
    console.log('所有测试通过！');
  }
}).catch(error => {
  console.error('\n测试运行失败:', error);
  process.exitCode = 1;
});

// 测试19: generateFilters() - 从清洗规则生成保留过滤器
test('应该从清洗规则生成保留过滤器', () => {
  const cleaningRules = {
    removePatterns: [],
    keepPatterns: [
      { target: 'paragraph', contentType: 'api_description', reason: 'API description' },
      { target: 'table', contentType: 'structured_data', reason: 'Data table' }
    ]
  };
  const classified = { template: [], unique: [] };

  const filters = generator.generateFilters(cleaningRules, classified);

  const keepFilters = filters.filter(f => f.type === 'keep');
  assertEquals(keepFilters.length, 2, '应该有2个保留过滤器');
  assertEquals(keepFilters[0].target, 'paragraph', '第一个应该是paragraph');
  assertEquals(keepFilters[0].contentType, 'api_description', 'contentType应该匹配');
  assertEquals(keepFilters[1].target, 'table', '第二个应该是table');
});

// 测试20: generateFilters() - 从低频内容生成保留过滤器
test('应该从低频独特内容生成保留过滤器', () => {
  const cleaningRules = { removePatterns: [], keepPatterns: [] };
  const classified = {
    template: [],
    unique: [
      { type: 'paragraph', content: '获取用户信息的API接口', ratio: 0.15 },
      { type: 'paragraph', content: '查询订单数据', ratio: 0.10 },
      { type: 'code', content: 'function example() {}', ratio: 0.05 },
      { type: 'paragraph', content: 'Some random text', ratio: 0.08 }
    ]
  };

  const filters = generator.generateFilters(cleaningRules, classified);

  const keepFilters = filters.filter(f => f.type === 'keep');
  assertGreaterThan(keepFilters.length, 0, '应该有保留过滤器');
  assertLessThanOrEqual(keepFilters.length, 3, '保留过滤器不应超过3个');
  
  // 验证保留过滤器包含contentType
  keepFilters.forEach(filter => {
    assertTrue(filter.contentType !== undefined, '应该有contentType字段');
    assertTrue(filter.contentType !== 'unknown', 'contentType不应该是unknown');
  });
});

// 测试21: generateFilters() - 混合生成移除和保留过滤器
test('应该同时生成移除和保留过滤器', () => {
  const cleaningRules = {
    removePatterns: [
      { target: 'heading', pattern: 'Navigation', reason: 'Template noise' }
    ],
    keepPatterns: [
      { target: 'paragraph', contentType: 'api_description', reason: 'API description' }
    ]
  };
  const classified = {
    template: [
      { type: 'heading', content: 'Common Header', ratio: 0.98 }
    ],
    unique: [
      { type: 'paragraph', content: '获取数据接口', ratio: 0.12 }
    ]
  };

  const filters = generator.generateFilters(cleaningRules, classified);

  const removeFilters = filters.filter(f => f.type === 'remove');
  const keepFilters = filters.filter(f => f.type === 'keep');
  
  assertGreaterThan(removeFilters.length, 0, '应该有移除过滤器');
  assertGreaterThan(keepFilters.length, 0, '应该有保留过滤器');
});

// 测试22: _inferContentType() - 推断API描述
test('应该正确推断API描述类型', () => {
  const testCases = [
    { content: '获取用户信息', type: 'paragraph', expected: 'api_description' },
    { content: '查询订单列表', type: 'paragraph', expected: 'api_description' },
    { content: '创建新记录', type: 'paragraph', expected: 'api_description' },
    { content: 'API request example', type: 'paragraph', expected: 'api_description' }
  ];

  testCases.forEach(({ content, type, expected }) => {
    const result = generator._inferContentType(content, type);
    assertEquals(result, expected, `"${content}"应该被识别为${expected}`);
  });
});

// 测试23: _inferContentType() - 推断数据字段类型
test('应该正确推断数据字段类型', () => {
  const testCases = [
    { content: '参数名称：id', type: 'paragraph', expected: 'data_field' },
    { content: '字段说明', type: 'paragraph', expected: 'data_field' },
    { content: '属性类型：string', type: 'paragraph', expected: 'data_field' }
  ];

  testCases.forEach(({ content, type, expected }) => {
    const result = generator._inferContentType(content, type);
    assertEquals(result, expected, `"${content}"应该被识别为${expected}`);
  });
});

// 测试24: _inferContentType() - 推断代码示例类型
test('应该正确推断代码示例类型', () => {
  const testCases = [
    { content: 'function test() {}', type: 'code', expected: 'code_example' },
    { content: '示例代码如下', type: 'paragraph', expected: 'code_example' },
    { content: 'Example usage', type: 'paragraph', expected: 'code_example' }
  ];

  testCases.forEach(({ content, type, expected }) => {
    const result = generator._inferContentType(content, type);
    assertEquals(result, expected, `"${content}"应该被识别为${expected}`);
  });
});

// 测试25: _inferContentType() - 推断结构化数据类型
test('应该正确推断结构化数据类型', () => {
  const result1 = generator._inferContentType('任意内容', 'table');
  assertEquals(result1, 'structured_data', 'table类型应该被识别为structured_data');

  const result2 = generator._inferContentType('任意内容', 'list');
  assertEquals(result2, 'list_data', 'list类型应该被识别为list_data');
});

// 测试26: generateFilters() - 过滤掉unknown类型的保留规则
test('应该过滤掉unknown类型的保留规则', () => {
  const cleaningRules = { removePatterns: [], keepPatterns: [] };
  const classified = {
    template: [],
    unique: [
      { type: 'paragraph', content: 'Random text without keywords', ratio: 0.15 },
      { type: 'paragraph', content: 'Another random paragraph', ratio: 0.10 }
    ]
  };

  const filters = generator.generateFilters(cleaningRules, classified);

  const keepFilters = filters.filter(f => f.type === 'keep');
  
  // 由于内容不包含关键词，应该被识别为unknown并被过滤掉
  keepFilters.forEach(filter => {
    assertTrue(filter.contentType !== 'unknown', '不应该包含unknown类型的保留规则');
  });
});
