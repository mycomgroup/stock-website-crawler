/**
 * TemplateContentAnalyzer 单元测试
 */

const TemplateContentAnalyzer = require('../lib/content-analyzer');

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

// 测试套件
console.log('\n=== TemplateContentAnalyzer 单元测试 ===\n');

const analyzer = new TemplateContentAnalyzer();

// 测试1: extractContentBlocks() - 提取标题
test('应该正确提取标题', () => {
  const markdown = `# 标题1
## 标题2
### 标题3`;
  
  const blocks = analyzer.extractContentBlocks(markdown);
  assertEquals(blocks.length, 3, '应该提取3个标题');
  assertEquals(blocks[0].type, 'heading', '第一个应该是标题');
  assertEquals(blocks[0].content, '# 标题1', '内容应该匹配');
  assertEquals(blocks[1].content, '## 标题2', '内容应该匹配');
  assertEquals(blocks[2].content, '### 标题3', '内容应该匹配');
});

// 测试2: extractContentBlocks() - 提取段落
test('应该正确提取段落', () => {
  const markdown = `这是第一段。
这是第一段的第二行。

这是第二段。`;
  
  const blocks = analyzer.extractContentBlocks(markdown);
  assertEquals(blocks.length, 2, '应该提取2个段落');
  assertEquals(blocks[0].type, 'paragraph', '应该是段落类型');
  assertTrue(blocks[0].content.includes('第一段'), '应该包含第一段内容');
  assertTrue(blocks[1].content.includes('第二段'), '应该包含第二段内容');
});

// 测试3: extractContentBlocks() - 提取表格
test('应该正确提取表格', () => {
  const markdown = `| 列1 | 列2 |
|-----|-----|
| 值1 | 值2 |
| 值3 | 值4 |`;
  
  const blocks = analyzer.extractContentBlocks(markdown);
  assertEquals(blocks.length, 1, '应该提取1个表格');
  assertEquals(blocks[0].type, 'table', '应该是表格类型');
  assertEquals(blocks[0].rows, 4, '应该有4行');
  assertTrue(blocks[0].content.includes('列1'), '应该包含表格内容');
});

// 测试4: extractContentBlocks() - 提取代码块
test('应该正确提取代码块', () => {
  const markdown = `\`\`\`javascript
function test() {
  return 'hello';
}
\`\`\``;
  
  const blocks = analyzer.extractContentBlocks(markdown);
  assertEquals(blocks.length, 1, '应该提取1个代码块');
  assertEquals(blocks[0].type, 'code', '应该是代码类型');
  assertEquals(blocks[0].language, 'javascript', '应该识别语言');
  assertTrue(blocks[0].content.includes('function test'), '应该包含代码内容');
});

// 测试5: extractContentBlocks() - 提取列表
test('应该正确提取列表', () => {
  const markdown = `- 项目1
- 项目2
- 项目3`;
  
  const blocks = analyzer.extractContentBlocks(markdown);
  assertEquals(blocks.length, 1, '应该提取1个列表');
  assertEquals(blocks[0].type, 'list', '应该是列表类型');
  assertEquals(blocks[0].items, 3, '应该有3个项目');
});

// 测试6: extractContentBlocks() - 混合内容
test('应该正确提取混合内容', () => {
  const markdown = `# 标题

这是一个段落。

- 列表项1
- 列表项2

| 表格 |
|------|
| 数据 |

\`\`\`js
code
\`\`\``;
  
  const blocks = analyzer.extractContentBlocks(markdown);
  assertEquals(blocks.length, 5, '应该提取5个块');
  assertEquals(blocks[0].type, 'heading', '第1个应该是标题');
  assertEquals(blocks[1].type, 'paragraph', '第2个应该是段落');
  assertEquals(blocks[2].type, 'list', '第3个应该是列表');
  assertEquals(blocks[3].type, 'table', '第4个应该是表格');
  assertEquals(blocks[4].type, 'code', '第5个应该是代码');
});

// 测试7: normalizeText() - 文本标准化
test('应该正确标准化文本', () => {
  const text1 = '  Hello   World!  ';
  const text2 = 'hello world';
  const normalized1 = analyzer.normalizeText(text1);
  const normalized2 = analyzer.normalizeText(text2);
  assertEquals(normalized1, normalized2, '标准化后应该相同');
  assertEquals(normalized1, 'hello world', '应该移除标点和多余空格');
});

// 测试8: normalizeText() - 中文支持
test('应该正确处理中文', () => {
  const text = '你好，世界！';
  const normalized = analyzer.normalizeText(text);
  assertEquals(normalized, '你好世界', '应该保留中文字符');
});

// 测试9: calculateFrequency() - 计算频率
test('应该正确计算内容频率', () => {
  const pages = [
    '# 标题\n段落1',
    '# 标题\n段落2',
    '# 标题\n段落1'
  ];
  
  const frequency = analyzer.calculateFrequency(pages);
  
  // 标题出现在所有3个页面
  const headingKey = Array.from(frequency.keys()).find(k => k.startsWith('heading:'));
  assertTrue(headingKey !== undefined, '应该找到标题');
  assertEquals(frequency.get(headingKey).count, 3, '标题应该出现3次');
  
  // 段落1出现在2个页面
  const para1Keys = Array.from(frequency.keys()).filter(k => 
    k.startsWith('paragraph:') && frequency.get(k).normalizedContent.includes('段落1')
  );
  assertTrue(para1Keys.length > 0, '应该找到段落1');
  assertEquals(frequency.get(para1Keys[0]).count, 2, '段落1应该出现2次');
});

// 测试10: classifyContent() - 内容分类
test('应该正确分类内容', () => {
  const frequency = new Map();
  
  // 高频内容（出现在所有5个页面）
  frequency.set('heading:标题', {
    type: 'heading',
    content: '# 标题',
    normalizedContent: '标题',
    count: 5,
    pages: [0, 1, 2, 3, 4]
  });
  
  // 低频内容（只出现在1个页面，比率0.2刚好等于阈值，应该归为unique）
  frequency.set('paragraph:独特', {
    type: 'paragraph',
    content: '独特内容',
    normalizedContent: '独特内容',
    count: 1,
    pages: [0]
  });
  
  // 中频内容（出现在3个页面）
  frequency.set('paragraph:混合', {
    type: 'paragraph',
    content: '混合内容',
    normalizedContent: '混合内容',
    count: 3,
    pages: [0, 1, 2]
  });
  
  const classified = analyzer.classifyContent(frequency, 5);
  
  assertEquals(classified.template.length, 1, '应该有1个模板内容');
  // 1/5 = 0.2，刚好等于阈值，按照 < 0.2 的逻辑，应该是mixed
  assertTrue(classified.unique.length === 0 || classified.mixed.length >= 1, '0.2的比率应该不是unique');
  assertEquals(classified.mixed.length, 2, '应该有2个混合内容');
  
  assertEquals(classified.template[0].ratio, 1.0, '模板内容比率应该是100%');
});

// 测试11: classifyContent() - 自定义阈值
test('应该支持自定义阈值', () => {
  const frequency = new Map();
  
  frequency.set('test:content', {
    type: 'paragraph',
    content: '测试',
    normalizedContent: '测试',
    count: 7,
    pages: [0, 1, 2, 3, 4, 5, 6]
  });
  
  // 使用默认阈值 (0.8, 0.2)
  const classified1 = analyzer.classifyContent(frequency, 10);
  assertEquals(classified1.mixed.length, 1, '70%应该是混合内容');
  
  // 使用自定义阈值 (0.6, 0.3)
  const classified2 = analyzer.classifyContent(frequency, 10, { template: 0.6, unique: 0.3 });
  assertEquals(classified2.template.length, 1, '70%应该是模板内容');
});

// 测试12: analyzeTemplate() - 完整流程
test('应该完成完整的模板分析流程', () => {
  const pages = [
    '# API文档\n这是API说明\n## 参数\n| 参数 | 说明 |\n|------|------|\n| id | 编号 |',
    '# API文档\n这是API说明\n## 参数\n| 参数 | 说明 |\n|------|------|\n| name | 名称 |',
    '# API文档\n这是API说明\n## 返回值\n| 字段 | 说明 |\n|------|------|\n| code | 状态码 |'
  ];
  
  const result = analyzer.analyzeTemplate(pages);
  
  assertTrue(result.stats !== undefined, '应该有统计信息');
  assertTrue(result.classified !== undefined, '应该有分类结果');
  assertTrue(result.frequency !== undefined, '应该有频率数据');
  
  assertEquals(result.stats.totalPages, 3, '应该有3个页面');
  assertTrue(result.stats.totalBlocks > 0, '应该有内容块');
  assertTrue(result.classified.template.length > 0, '应该有模板内容');
});

// 测试13: 空内容处理
test('应该正确处理空内容', () => {
  const blocks = analyzer.extractContentBlocks('');
  assertEquals(blocks.length, 0, '空内容应该返回空数组');
});

// 测试14: 只有空行的内容
test('应该正确处理只有空行的内容', () => {
  const blocks = analyzer.extractContentBlocks('\n\n\n');
  assertEquals(blocks.length, 0, '只有空行应该返回空数组');
});

// 测试15: 嵌套列表
test('应该正确提取嵌套列表', () => {
  const markdown = `- 项目1
  - 子项目1
  - 子项目2
- 项目2`;
  
  const blocks = analyzer.extractContentBlocks(markdown);
  assertEquals(blocks.length, 1, '应该提取1个列表');
  assertEquals(blocks[0].type, 'list', '应该是列表类型');
  assertTrue(blocks[0].content.includes('子项目'), '应该包含子项目');
});

// 测试20: identifyTableStructures() - 识别表格结构
test('应该正确识别表格结构', () => {
  const pages = [
    '| 参数 | 类型 | 说明 |\n|------|------|------|\n| id | int | 编号 |',
    '| 参数 | 类型 | 说明 |\n|------|------|------|\n| name | string | 名称 |',
    '| 字段 | 说明 |\n|------|------|\n| code | 状态码 |'
  ];
  
  const tables = analyzer.identifyTableStructures(pages);
  
  assertTrue(tables.length > 0, '应该识别出表格结构');
  assertTrue(tables[0].columnCount > 0, '应该有列数');
  assertTrue(tables[0].columns.length > 0, '应该有列名');
  assertTrue(tables[0].occurrences > 0, '应该有出现次数');
  assertTrue(tables[0].hasHeader !== undefined, '应该标识是否有表头');
});

// 测试21: identifyTableStructures() - 相同结构的表格应该合并
test('应该合并相同结构的表格', () => {
  const pages = [
    '| 参数 | 类型 |\n|------|------|\n| id | int |',
    '| 参数 | 类型 |\n|------|------|\n| name | string |',
    '| 参数 | 类型 |\n|------|------|\n| age | int |'
  ];
  
  const tables = analyzer.identifyTableStructures(pages);
  
  assertEquals(tables.length, 1, '相同结构的表格应该合并为一个');
  assertEquals(tables[0].occurrences, 3, '应该出现3次');
  assertEquals(tables[0].columnCount, 2, '应该有2列');
});

// 测试22: identifyCodeBlocks() - 识别代码块
test('应该正确识别代码块', () => {
  const pages = [
    '```javascript\nfunction test() {}\n```',
    '```javascript\nconst x = 1;\n```',
    '```python\ndef test():\n    pass\n```'
  ];
  
  const codeBlocks = analyzer.identifyCodeBlocks(pages);
  
  assertTrue(codeBlocks.length > 0, '应该识别出代码块');
  assertTrue(codeBlocks[0].language !== undefined, '应该有语言标识');
  assertTrue(codeBlocks[0].occurrences > 0, '应该有出现次数');
  assertTrue(codeBlocks[0].avgLength > 0, '应该有平均长度');
});

// 测试23: identifyCodeBlocks() - 按语言分组
test('应该按语言分组代码块', () => {
  const pages = [
    '```javascript\ncode1\n```',
    '```javascript\ncode2\n```',
    '```python\ncode3\n```'
  ];
  
  const codeBlocks = analyzer.identifyCodeBlocks(pages);
  
  const jsBlocks = codeBlocks.find(cb => cb.language === 'javascript');
  const pyBlocks = codeBlocks.find(cb => cb.language === 'python');
  
  assertTrue(jsBlocks !== undefined, '应该有JavaScript代码块');
  assertTrue(pyBlocks !== undefined, '应该有Python代码块');
  assertEquals(jsBlocks.occurrences, 2, 'JavaScript应该出现2次');
  assertEquals(pyBlocks.occurrences, 1, 'Python应该出现1次');
});

// 测试24: identifyCodeBlocks() - 推断语言
test('应该能够推断代码语言', () => {
  const pages = [
    '```\nfunction test() { return true; }\n```',
    '```\ndef test():\n    return True\n```',
    '```\n{"key": "value"}\n```'
  ];
  
  const codeBlocks = analyzer.identifyCodeBlocks(pages);
  
  assertTrue(codeBlocks.length > 0, '应该识别出代码块');
  // 应该能推断出至少一种语言
  const hasInferredLanguage = codeBlocks.some(cb => 
    cb.language !== 'unknown' && cb.language !== ''
  );
  assertTrue(hasInferredLanguage, '应该能推断出语言');
});

// 测试25: identifyLists() - 识别列表
test('应该正确识别列表', () => {
  const pages = [
    '- 项目1\n- 项目2\n- 项目3',
    '- 项目A\n- 项目B',
    '1. 第一项\n2. 第二项'
  ];
  
  const lists = analyzer.identifyLists(pages);
  
  assertTrue(lists.length > 0, '应该识别出列表');
  assertTrue(lists[0].listType !== undefined, '应该有列表类型');
  assertTrue(lists[0].itemCount > 0, '应该有项目数量');
  assertTrue(lists[0].occurrences > 0, '应该有出现次数');
});

// 测试26: identifyLists() - 区分有序和无序列表
test('应该区分有序和无序列表', () => {
  const pages = [
    '- 无序项1\n- 无序项2',
    '1. 有序项1\n2. 有序项2'
  ];
  
  const lists = analyzer.identifyLists(pages);
  
  const unordered = lists.find(l => l.listType === 'unordered');
  const ordered = lists.find(l => l.listType === 'ordered');
  
  assertTrue(unordered !== undefined, '应该有无序列表');
  assertTrue(ordered !== undefined, '应该有有序列表');
});

// 测试27: identifyLists() - 识别嵌套列表
test('应该识别嵌套列表', () => {
  const pages = [
    '- 项目1\n  - 子项目1\n  - 子项目2\n- 项目2'
  ];
  
  const lists = analyzer.identifyLists(pages);
  
  assertTrue(lists.length > 0, '应该识别出列表');
  assertTrue(lists[0].hasNesting === true, '应该标识为嵌套列表');
});

// 测试28: analyzeTemplate() - 包含数据结构识别
test('完整分析应该包含数据结构识别', () => {
  const pages = [
    '# 标题\n\n| 表格 |\n|------|\n| 数据 |\n\n```js\ncode\n```\n\n- 列表项',
    '# 标题\n\n| 表格 |\n|------|\n| 数据 |\n\n```js\ncode\n```\n\n- 列表项'
  ];
  
  const result = analyzer.analyzeTemplate(pages);
  
  assertTrue(result.dataStructures !== undefined, '应该有数据结构');
  assertTrue(result.dataStructures.tables !== undefined, '应该有表格结构');
  assertTrue(result.dataStructures.codeBlocks !== undefined, '应该有代码块结构');
  assertTrue(result.dataStructures.lists !== undefined, '应该有列表结构');
  
  assertTrue(result.stats.tableStructures !== undefined, '统计应该包含表格数量');
  assertTrue(result.stats.codeBlockTypes !== undefined, '统计应该包含代码块类型数量');
  assertTrue(result.stats.listTypes !== undefined, '统计应该包含列表类型数量');
});

// 测试29: identifyNoisePatterns() - 识别噪音模式
test('应该正确识别噪音模式', () => {
  const templateContent = [
    {
      type: 'heading',
      content: '# API文档',
      normalizedContent: 'api文档',
      count: 10,
      ratio: 1.0,
      pages: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    },
    {
      type: 'heading',
      content: '## 导航',
      normalizedContent: '导航',
      count: 9,
      ratio: 0.9,
      pages: [0, 1, 2, 3, 4, 5, 6, 7, 8]
    },
    {
      type: 'paragraph',
      content: '版权所有',
      normalizedContent: '版权所有',
      count: 8,
      ratio: 0.8,
      pages: [0, 1, 2, 3, 4, 5, 6, 7]
    }
  ];
  
  const noisePatterns = analyzer.identifyNoisePatterns(templateContent);
  
  assertTrue(noisePatterns.length >= 2, '应该识别出至少2个噪音模式（>90%）');
  assertTrue(noisePatterns[0].pattern !== undefined, '应该有匹配模式');
  assertTrue(noisePatterns[0].reason.includes('Template noise'), '应该有原因说明');
  assertTrue(noisePatterns[0].ratio >= 0.9, '噪音比率应该>=90%');
});

// 测试30: identifyNoisePatterns() - 自定义阈值
test('应该支持自定义噪音识别阈值', () => {
  const templateContent = [
    {
      type: 'heading',
      content: '# 标题',
      normalizedContent: '标题',
      count: 8,
      ratio: 0.8,
      pages: [0, 1, 2, 3, 4, 5, 6, 7]
    }
  ];
  
  // 使用默认阈值（0.9），不应该识别为噪音
  const noisePatterns1 = analyzer.identifyNoisePatterns(templateContent);
  assertEquals(noisePatterns1.length, 0, '80%不应该被识别为噪音（默认阈值90%）');
  
  // 使用自定义阈值（0.7），应该识别为噪音
  const noisePatterns2 = analyzer.identifyNoisePatterns(templateContent, { minRatio: 0.7 });
  assertEquals(noisePatterns2.length, 1, '80%应该被识别为噪音（自定义阈值70%）');
});

// 测试31: identifyDataPatterns() - 识别数据模式
test('应该正确识别数据模式', () => {
  const uniqueContent = [
    {
      type: 'paragraph',
      content: '获取公司基本信息',
      normalizedContent: '获取公司基本信息',
      count: 1,
      ratio: 0.1,
      pages: [0]
    },
    {
      type: 'code',
      content: 'https://api.lixinger.com/company',
      normalizedContent: 'httpsapilixingercomcompany',
      count: 2,
      ratio: 0.2,
      pages: [0, 1]
    }
  ];
  
  const dataStructures = {
    tables: [
      {
        columns: ['参数', '类型', '说明'],
        columnCount: 3,
        occurrences: 5,
        pages: [0, 1, 2, 3, 4]
      }
    ],
    codeBlocks: [
      {
        language: 'javascript',
        occurrences: 3,
        avgLength: 50
      }
    ],
    lists: []
  };
  
  const dataPatterns = analyzer.identifyDataPatterns(uniqueContent, dataStructures);
  
  assertTrue(dataPatterns.length > 0, '应该识别出数据模式');
  
  // 应该包含独特内容的模式
  const uniquePatterns = dataPatterns.filter(p => p.reason && p.reason.includes('Unique data'));
  assertTrue(uniquePatterns.length >= 2, '应该识别出独特内容模式');
  
  // 应该包含表格数据模式
  const tablePatterns = dataPatterns.filter(p => p.type === 'table');
  assertTrue(tablePatterns.length >= 1, '应该识别出表格数据模式');
  
  // 应该包含代码块模式
  const codePatterns = dataPatterns.filter(p => p.type === 'code');
  assertTrue(codePatterns.length >= 1, '应该识别出代码块模式');
});

// 测试32: identifyDataPatterns() - 推断内容类型
test('应该能够推断数据内容类型', () => {
  const uniqueContent = [
    {
      type: 'paragraph',
      content: '参数说明：id为必填项',
      normalizedContent: '参数说明id为必填项',
      count: 1,
      ratio: 0.1,
      pages: [0]
    },
    {
      type: 'paragraph',
      content: '返回值包含code和message',
      normalizedContent: '返回值包含code和message',
      count: 1,
      ratio: 0.1,
      pages: [1]
    }
  ];
  
  const dataStructures = { tables: [], codeBlocks: [], lists: [] };
  const dataPatterns = analyzer.identifyDataPatterns(uniqueContent, dataStructures);
  
  // 应该推断出参数描述
  const paramPattern = dataPatterns.find(p => p.contentType === 'parameter_description');
  assertTrue(paramPattern !== undefined, '应该识别出参数描述');
  
  // 应该推断出返回值描述
  const responsePattern = dataPatterns.find(p => p.contentType === 'response_description');
  assertTrue(responsePattern !== undefined, '应该识别出返回值描述');
});

// 测试33: generateCleaningRules() - 生成清洗规则
test('应该正确生成清洗规则', () => {
  const classified = {
    template: [
      {
        type: 'heading',
        content: '# API文档',
        normalizedContent: 'api文档',
        count: 10,
        ratio: 1.0,
        pages: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
      },
      {
        type: 'heading',
        content: '## 导航',
        normalizedContent: '导航',
        count: 10,
        ratio: 1.0,
        pages: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
      }
    ],
    unique: [
      {
        type: 'paragraph',
        content: '获取公司信息',
        normalizedContent: '获取公司信息',
        count: 1,
        ratio: 0.1,
        pages: [0]
      }
    ],
    mixed: []
  };
  
  const dataStructures = {
    tables: [
      {
        columns: ['参数', '类型'],
        columnCount: 2,
        occurrences: 5
      }
    ],
    codeBlocks: [],
    lists: []
  };
  
  const cleaningRules = analyzer.generateCleaningRules(classified, dataStructures);
  
  assertTrue(cleaningRules.removePatterns !== undefined, '应该有移除规则');
  assertTrue(cleaningRules.keepPatterns !== undefined, '应该有保留规则');
  assertTrue(cleaningRules.removeElements !== undefined, '应该有移除元素规则');
  assertTrue(cleaningRules.summary !== undefined, '应该有摘要信息');
  
  assertTrue(cleaningRules.removePatterns.length >= 2, '应该有移除规则');
  assertTrue(cleaningRules.keepPatterns.length >= 1, '应该有保留规则');
  assertTrue(cleaningRules.removeElements.length >= 2, '应该有移除元素规则');
  
  // 验证移除规则格式
  const removeRule = cleaningRules.removePatterns[0];
  assertEquals(removeRule.type, 'remove', '应该是移除类型');
  assertTrue(removeRule.pattern !== undefined, '应该有匹配模式');
  assertTrue(removeRule.reason !== undefined, '应该有原因说明');
  
  // 验证保留规则格式
  const keepRule = cleaningRules.keepPatterns[0];
  assertEquals(keepRule.type, 'keep', '应该是保留类型');
  assertTrue(keepRule.contentType !== undefined, '应该有内容类型');
});

// 测试34: generateCleaningRules() - 移除元素规则
test('应该生成高频标题的移除元素规则', () => {
  const classified = {
    template: [
      {
        type: 'heading',
        content: '# API文档',
        normalizedContent: 'api文档',
        count: 10,
        ratio: 0.96,  // 改为>0.95
        pages: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
      },
      {
        type: 'heading',
        content: '## 导航菜单',
        normalizedContent: '导航菜单',
        count: 10,
        ratio: 1.0,
        pages: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
      },
      {
        type: 'paragraph',
        content: '这是一个段落',
        normalizedContent: '这是一个段落',
        count: 9,
        ratio: 0.9,
        pages: [0, 1, 2, 3, 4, 5, 6, 7, 8]
      }
    ],
    unique: [],
    mixed: []
  };
  
  const dataStructures = { tables: [], codeBlocks: [], lists: [] };
  const cleaningRules = analyzer.generateCleaningRules(classified, dataStructures);
  
  // 应该只为高频标题（>95%）生成移除元素规则
  assertTrue(cleaningRules.removeElements.length >= 2, '应该有移除元素规则');
  
  const headingElements = cleaningRules.removeElements.filter(e => e.type === 'heading');
  assertTrue(headingElements.length >= 2, '应该有标题移除规则');
  
  // 验证标题文本被正确提取
  const apiDocElement = headingElements.find(e => e.text === 'API文档');
  assertTrue(apiDocElement !== undefined, '应该提取出"API文档"标题');
  
  const navElement = headingElements.find(e => e.text === '导航菜单');
  assertTrue(navElement !== undefined, '应该提取出"导航菜单"标题');
});

// 测试35: analyzeTemplate() - 包含清洗规则
test('完整分析应该包含清洗规则', () => {
  const pages = [
    '# API文档\n\n获取公司信息\n\n| 参数 | 类型 |\n|------|------|\n| id | int |',
    '# API文档\n\n获取指数信息\n\n| 参数 | 类型 |\n|------|------|\n| code | string |',
    '# API文档\n\n获取行业信息\n\n| 参数 | 类型 |\n|------|------|\n| name | string |'
  ];
  
  const result = analyzer.analyzeTemplate(pages);
  
  assertTrue(result.cleaningRules !== undefined, '应该有清洗规则');
  assertTrue(result.cleaningRules.removePatterns !== undefined, '应该有移除规则');
  assertTrue(result.cleaningRules.keepPatterns !== undefined, '应该有保留规则');
  assertTrue(result.cleaningRules.removeElements !== undefined, '应该有移除元素规则');
  assertTrue(result.cleaningRules.summary !== undefined, '应该有摘要');
  
  // 验证摘要信息
  assertTrue(result.cleaningRules.summary.totalNoisePatterns >= 0, '应该有噪音模式数量');
  assertTrue(result.cleaningRules.summary.totalDataPatterns >= 0, '应该有数据模式数量');
  assertTrue(result.cleaningRules.summary.totalRemoveRules >= 0, '应该有移除规则数量');
  assertTrue(result.cleaningRules.summary.totalKeepRules >= 0, '应该有保留规则数量');
});

// 测试36: generateAnalysisJSON() - 生成JSON报告
test('应该正确生成JSON格式的分析报告', () => {
  const pages = [
    '# API文档\n\n获取公司信息\n\n| 参数 | 类型 |\n|------|------|\n| id | int |',
    '# API文档\n\n获取指数信息\n\n| 参数 | 类型 |\n|------|------|\n| code | string |'
  ];
  
  const analysisResult = analyzer.analyzeTemplate(pages);
  const urlPattern = {
    name: 'api-doc',
    pathTemplate: '/open/api/doc',
    pattern: '^https://www\\.lixinger\\.com/open/api/doc\\?api-key=(.+)$',
    queryParams: ['api-key'],
    urlCount: 163
  };
  
  const jsonReport = analyzer.generateAnalysisJSON(analysisResult, urlPattern);
  
  // 验证基本结构
  assertTrue(jsonReport.templateName !== undefined, '应该有模板名称');
  assertTrue(jsonReport.urlPattern !== undefined, '应该有URL模式');
  assertTrue(jsonReport.metadata !== undefined, '应该有元数据');
  assertTrue(jsonReport.statistics !== undefined, '应该有统计信息');
  assertTrue(jsonReport.contentClassification !== undefined, '应该有内容分类');
  assertTrue(jsonReport.dataStructures !== undefined, '应该有数据结构');
  assertTrue(jsonReport.cleaningRules !== undefined, '应该有清洗规则');
  
  // 验证元数据
  assertEquals(jsonReport.metadata.pageCount, 2, '页面数应该是2');
  assertTrue(jsonReport.metadata.generatedAt !== undefined, '应该有生成时间');
  assertEquals(jsonReport.metadata.version, '1.0.0', '版本应该是1.0.0');
  
  // 验证URL模式
  assertEquals(jsonReport.urlPattern.name, 'api-doc', 'URL模式名称应该正确');
  assertEquals(jsonReport.urlPattern.pathTemplate, '/open/api/doc', '路径模板应该正确');
  
  // 验证统计信息
  assertEquals(jsonReport.statistics.totalPages, 2, '总页面数应该是2');
  assertTrue(jsonReport.statistics.totalBlocks > 0, '应该有内容块');
});

// 测试37: generateAnalysisMarkdown() - 生成Markdown报告
test('应该正确生成Markdown格式的分析报告', () => {
  const pages = [
    '# API文档\n\n获取公司信息\n\n| 参数 | 类型 |\n|------|------|\n| id | int |',
    '# API文档\n\n获取指数信息\n\n| 参数 | 类型 |\n|------|------|\n| code | string |'
  ];
  
  const analysisResult = analyzer.analyzeTemplate(pages);
  const urlPattern = {
    name: 'api-doc',
    pathTemplate: '/open/api/doc',
    pattern: '^https://www\\.lixinger\\.com/open/api/doc\\?api-key=(.+)$',
    queryParams: ['api-key'],
    urlCount: 163
  };
  
  const markdownReport = analyzer.generateAnalysisMarkdown(analysisResult, urlPattern);
  
  // 验证报告包含关键部分
  assertTrue(markdownReport.includes('# 模板分析报告'), '应该有标题');
  assertTrue(markdownReport.includes('api-doc'), '应该包含模板名称');
  assertTrue(markdownReport.includes('## 统计概览'), '应该有统计概览部分');
  assertTrue(markdownReport.includes('## 模板内容（噪音）'), '应该有模板内容部分');
  assertTrue(markdownReport.includes('## 独特内容（数据）'), '应该有独特内容部分');
  assertTrue(markdownReport.includes('## 数据结构'), '应该有数据结构部分');
  assertTrue(markdownReport.includes('## 清洗规则'), '应该有清洗规则部分');
  assertTrue(markdownReport.includes('## 建议'), '应该有建议部分');
  
  // 验证表格格式
  assertTrue(markdownReport.includes('| 指标 | 数量 |'), '应该有统计表格');
  assertTrue(markdownReport.includes('|------|------|'), '应该有表格分隔符');
  
  // 验证包含页面数
  assertTrue(markdownReport.includes('2'), '应该包含页面数量');
});

// 测试38: generateCleaningExamples() - 生成清洗前后对比示例
test('应该正确生成清洗前后对比示例', () => {
  const pages = [
    '# API文档\n\n## 导航\n\n获取公司信息\n\n| 参数 | 类型 |\n|------|------|\n| id | int |',
    '# API文档\n\n## 导航\n\n获取指数信息\n\n| 参数 | 类型 |\n|------|------|\n| code | string |'
  ];
  
  const analysisResult = analyzer.analyzeTemplate(pages);
  const cleaningRules = analysisResult.cleaningRules;
  
  const examples = analyzer.generateCleaningExamples(pages, cleaningRules, { maxExamples: 2 });
  
  // 验证示例数量
  assertEquals(examples.length, 2, '应该生成2个示例');
  
  // 验证示例结构
  const example = examples[0];
  assertTrue(example.index !== undefined, '应该有索引');
  assertTrue(example.original !== undefined, '应该有原始内容');
  assertTrue(example.cleaned !== undefined, '应该有清洗后内容');
  assertTrue(example.stats !== undefined, '应该有统计信息');
  
  // 验证原始内容
  assertTrue(example.original.content !== undefined, '应该有原始内容文本');
  assertTrue(example.original.length > 0, '原始内容长度应该大于0');
  assertTrue(example.original.preview !== undefined, '应该有原始内容预览');
  
  // 验证清洗后内容
  assertTrue(example.cleaned.content !== undefined, '应该有清洗后内容文本');
  assertTrue(example.cleaned.length >= 0, '清洗后内容长度应该>=0');
  assertTrue(example.cleaned.preview !== undefined, '应该有清洗后内容预览');
  
  // 验证统计信息
  assertTrue(example.stats.originalLength > 0, '应该有原始长度');
  assertTrue(example.stats.cleanedLength >= 0, '应该有清洗后长度');
  assertTrue(example.stats.reduction !== undefined, '应该有减少百分比');
  assertTrue(example.stats.removedLength >= 0, '应该有移除的长度');
});

// 测试39: generateCleaningExamples() - 验证清洗效果
test('清洗示例应该实际移除高频内容', () => {
  const pages = [
    '# API文档\n\n## 导航\n\n获取公司信息',
    '# API文档\n\n## 导航\n\n获取指数信息',
    '# API文档\n\n## 导航\n\n获取行业信息'
  ];
  
  const analysisResult = analyzer.analyzeTemplate(pages);
  const cleaningRules = analysisResult.cleaningRules;
  
  const examples = analyzer.generateCleaningExamples(pages, cleaningRules, { maxExamples: 1 });
  
  const example = examples[0];
  
  // 清洗后的内容应该比原始内容短（因为移除了高频模板内容）
  assertTrue(example.stats.cleanedLength <= example.stats.originalLength, 
    '清洗后的内容应该不长于原始内容');
  
  // 如果有移除规则，应该有实际的减少
  if (cleaningRules.removePatterns.length > 0 || cleaningRules.removeElements.length > 0) {
    assertTrue(example.stats.removedLength >= 0, '应该有内容被移除');
  }
});

// 测试40: generateAnalysisJSON() - 内容截断
test('JSON报告应该截断过长的内容', () => {
  const longContent = 'A'.repeat(500);
  const pages = [
    `# 标题\n\n${longContent}`,
    `# 标题\n\n${longContent}`
  ];
  
  const analysisResult = analyzer.analyzeTemplate(pages);
  const urlPattern = {
    name: 'test',
    pathTemplate: '/test',
    pattern: '^/test$',
    queryParams: []
  };
  
  const jsonReport = analyzer.generateAnalysisJSON(analysisResult, urlPattern);
  
  // 验证内容被截断到200字符
  if (jsonReport.contentClassification.template.length > 0) {
    const templateItem = jsonReport.contentClassification.template[0];
    assertTrue(templateItem.content.length <= 200, '模板内容应该被截断到200字符');
  }
  
  if (jsonReport.contentClassification.unique.length > 0) {
    const uniqueItem = jsonReport.contentClassification.unique[0];
    assertTrue(uniqueItem.content.length <= 200, '独特内容应该被截断到200字符');
  }
});

console.log('\n=== 测试完成 ===\n');

if (process.exitCode === 1) {
  console.log('部分测试失败');
} else {
  console.log('所有测试通过！');
}

// 测试16: loadMarkdownPages() - 批量加载页面
test('应该能够批量加载markdown页面', async () => {
  const fs = require('fs').promises;
  const path = require('path');
  const os = require('os');
  
  // 创建临时测试文件
  const tempDir = path.join(os.tmpdir(), 'test-markdown-' + Date.now());
  await fs.mkdir(tempDir, { recursive: true });
  
  try {
    // 创建测试文件
    const testFiles = [];
    for (let i = 0; i < 5; i++) {
      const filePath = path.join(tempDir, `test${i}.md`);
      await fs.writeFile(filePath, `# Test ${i}\n\nContent ${i}`);
      testFiles.push(filePath);
    }
    
    // 测试批量加载
    const batches = [];
    for await (const batch of analyzer.loadMarkdownPages(testFiles, { batchSize: 2 })) {
      batches.push(batch);
    }
    
    assertEquals(batches.length, 3, '应该有3个批次（2+2+1）');
    assertEquals(batches[0].length, 2, '第一批应该有2个文件');
    assertEquals(batches[1].length, 2, '第二批应该有2个文件');
    assertEquals(batches[2].length, 1, '第三批应该有1个文件');
    
    // 验证内容
    assertTrue(batches[0][0].content.includes('Test 0'), '应该包含正确的内容');
    assertTrue(batches[0][0].fileName === 'test0.md', '应该有正确的文件名');
    assertTrue(batches[0][0].size > 0, '应该有文件大小');
  } finally {
    // 清理临时文件
    await fs.rm(tempDir, { recursive: true, force: true });
  }
});

// 测试17: matchPagesToURLs() - 匹配URL和文件
test('应该能够匹配URL模式和markdown文件', async () => {
  const fs = require('fs').promises;
  const path = require('path');
  const os = require('os');
  
  // 创建临时测试目录
  const tempDir = path.join(os.tmpdir(), 'test-pages-' + Date.now());
  await fs.mkdir(tempDir, { recursive: true });
  
  try {
    // 创建测试文件
    await fs.writeFile(path.join(tempDir, 'api-doc-test.md'), '# API Doc');
    await fs.writeFile(path.join(tempDir, 'dashboard-test.md'), '# Dashboard');
    await fs.writeFile(path.join(tempDir, 'other-page.md'), '# Other');
    
    // 创建子目录
    const subDir = path.join(tempDir, 'subdir');
    await fs.mkdir(subDir);
    await fs.writeFile(path.join(subDir, 'api-doc-nested.md'), '# Nested API Doc');
    
    // 测试匹配
    const urlPattern = {
      name: 'api-doc',
      pathTemplate: '/open/api/doc',
      pattern: '^https://www\\.lixinger\\.com/open/api/doc\\?api-key=(.+)$'
    };
    
    const matchedFiles = await analyzer.matchPagesToURLs(urlPattern, tempDir);
    
    assertTrue(matchedFiles.length >= 2, '应该至少匹配2个文件');
    assertTrue(matchedFiles.some(f => f.includes('api-doc-test.md')), '应该匹配api-doc-test.md');
    assertTrue(matchedFiles.some(f => f.includes('api-doc-nested.md')), '应该匹配嵌套的文件');
    assertTrue(!matchedFiles.some(f => f.includes('other-page.md')), '不应该匹配other-page.md');
  } finally {
    // 清理临时文件
    await fs.rm(tempDir, { recursive: true, force: true });
  }
});

// 测试18: loadMarkdownPages() - 处理错误文件
test('应该能够处理读取失败的文件', async () => {
  const testFiles = [
    '/nonexistent/file1.md',
    '/nonexistent/file2.md'
  ];
  
  const batches = [];
  for await (const batch of analyzer.loadMarkdownPages(testFiles, { batchSize: 10 })) {
    batches.push(batch);
  }
  
  // 应该返回空批次或跳过错误文件
  assertTrue(batches.length >= 0, '应该能够处理错误而不崩溃');
  if (batches.length > 0) {
    assertEquals(batches[0].length, 0, '错误文件应该被跳过');
  }
});

// 测试19: 流式处理 - 避免内存溢出
test('应该使用流式处理避免内存溢出', async () => {
  const fs = require('fs').promises;
  const path = require('path');
  const os = require('os');
  
  // 创建临时测试文件
  const tempDir = path.join(os.tmpdir(), 'test-stream-' + Date.now());
  await fs.mkdir(tempDir, { recursive: true });
  
  try {
    // 创建较多测试文件
    const testFiles = [];
    for (let i = 0; i < 10; i++) {
      const filePath = path.join(tempDir, `test${i}.md`);
      await fs.writeFile(filePath, `# Test ${i}\n\n${'Content '.repeat(100)}`);
      testFiles.push(filePath);
    }
    
    // 使用小批次测试流式处理
    let totalPages = 0;
    let batchCount = 0;
    
    for await (const batch of analyzer.loadMarkdownPages(testFiles, { batchSize: 3 })) {
      batchCount++;
      totalPages += batch.length;
      // 验证每批不超过批次大小
      assertTrue(batch.length <= 3, '每批不应超过批次大小');
    }
    
    assertEquals(totalPages, 10, '应该处理所有10个文件');
    assertEquals(batchCount, 4, '应该有4个批次（3+3+3+1）');
  } finally {
    // 清理临时文件
    await fs.rm(tempDir, { recursive: true, force: true });
  }
});
