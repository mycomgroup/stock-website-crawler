/**
 * TemplateParser 单元测试
 */

const { test } = require('node:test');
const assert = require('node:assert');
const TemplateParser = require('../lib/template-parser');

// 模拟配置
const validConfig = {
  name: 'test-parser',
  description: 'Test parser configuration',
  priority: 100,
  urlPattern: {
    pattern: '^https://example\\.com/test/(.+)$',
    pathTemplate: '/test/*',
    queryParams: []
  },
  extractors: [
    {
      field: 'title',
      type: 'text',
      selector: 'h1',
      required: true
    },
    {
      field: 'content',
      type: 'text',
      selector: 'p'
    }
  ],
  filters: [],
  metadata: {
    generatedAt: '2024-02-25T10:00:00.000Z',
    pageCount: 10,
    version: '1.0.0'
  }
};

test('TemplateParser', async (t) => {
  await t.test('构造函数 - Parser创建测试', async (t) => {
    await t.test('应该成功创建Parser实例', () => {
      const parser = new TemplateParser(validConfig);
      assert.strictEqual(parser.getName(), 'test-parser');
      assert.strictEqual(parser.getPriority(), 100);
    });

    await t.test('应该正确设置所有Parser属性', () => {
      const parser = new TemplateParser(validConfig);
      
      // 验证基本属性
      assert.strictEqual(parser.name, 'test-parser');
      assert.strictEqual(parser.config.name, 'test-parser');
      assert.strictEqual(parser.config.description, 'Test parser configuration');
      assert.strictEqual(parser.config.priority, 100);
      
      // 验证URL模式
      assert.ok(parser.pattern instanceof RegExp);
      assert.strictEqual(parser.config.urlPattern.pathTemplate, '/test/*');
      
      // 验证提取器配置
      assert.ok(Array.isArray(parser.config.extractors));
      assert.strictEqual(parser.config.extractors.length, 2);
      assert.strictEqual(parser.config.extractors[0].field, 'title');
      assert.strictEqual(parser.config.extractors[0].type, 'text');
      
      // 验证过滤器配置
      assert.ok(Array.isArray(parser.config.filters));
      
      // 验证元数据
      assert.ok(parser.config.metadata);
      assert.strictEqual(parser.config.metadata.version, '1.0.0');
    });

    await t.test('应该成功创建多个Parser实例', () => {
      const config1 = {
        ...validConfig,
        name: 'parser-1',
        priority: 100
      };
      const config2 = {
        ...validConfig,
        name: 'parser-2',
        priority: 200,
        urlPattern: {
          pattern: '^https://example\\.com/api/(.+)$',
          pathTemplate: '/api/*',
          queryParams: []
        }
      };
      const config3 = {
        ...validConfig,
        name: 'parser-3',
        priority: 50
      };
      
      const parser1 = new TemplateParser(config1);
      const parser2 = new TemplateParser(config2);
      const parser3 = new TemplateParser(config3);
      
      // 验证每个Parser都是独立的实例
      assert.strictEqual(parser1.getName(), 'parser-1');
      assert.strictEqual(parser2.getName(), 'parser-2');
      assert.strictEqual(parser3.getName(), 'parser-3');
      
      // 验证优先级
      assert.strictEqual(parser1.getPriority(), 100);
      assert.strictEqual(parser2.getPriority(), 200);
      assert.strictEqual(parser3.getPriority(), 50);
      
      // 验证URL模式不同
      assert.ok(parser1.matches('https://example.com/test/123'));
      assert.ok(parser2.matches('https://example.com/api/users'));
      assert.ok(!parser1.matches('https://example.com/api/users'));
      assert.ok(!parser2.matches('https://example.com/test/123'));
    });

    await t.test('应该正确编译字符串格式的正则表达式', () => {
      const config = {
        ...validConfig,
        urlPattern: {
          ...validConfig.urlPattern,
          pattern: '^https://example\\.com/test/[0-9]+$'
        }
      };
      const parser = new TemplateParser(config);
      
      assert.ok(parser.pattern instanceof RegExp);
      assert.ok(parser.matches('https://example.com/test/123'));
      assert.ok(parser.matches('https://example.com/test/999'));
      assert.ok(!parser.matches('https://example.com/test/abc'));
    });

    await t.test('应该正确编译带标志的正则表达式字符串', () => {
      const config = {
        ...validConfig,
        urlPattern: {
          ...validConfig.urlPattern,
          pattern: '/test\\/(.+)/i'
        }
      };
      const parser = new TemplateParser(config);
      
      // 验证大小写不敏感
      assert.ok(parser.matches('https://example.com/TEST/123'));
      assert.ok(parser.matches('https://example.com/test/123'));
      assert.ok(parser.matches('https://example.com/TeSt/123'));
    });

    await t.test('应该正确处理RegExp对象', () => {
      const config = {
        ...validConfig,
        urlPattern: {
          ...validConfig.urlPattern,
          pattern: /^https:\/\/example\.com\/test\/(.+)$/i
        }
      };
      const parser = new TemplateParser(config);
      
      assert.ok(parser.pattern instanceof RegExp);
      assert.ok(parser.matches('https://example.com/TEST/123'));
    });

    await t.test('应该在缺少config时抛出错误', () => {
      assert.throws(
        () => new TemplateParser(),
        /Config is required/
      );
    });

    await t.test('应该在config为null时抛出错误', () => {
      assert.throws(
        () => new TemplateParser(null),
        /Config is required/
      );
    });

    await t.test('应该在缺少name时抛出错误', () => {
      const config = { ...validConfig };
      delete config.name;
      assert.throws(
        () => new TemplateParser(config),
        /Config\.name is required/
      );
    });

    await t.test('应该在name为空字符串时抛出错误', () => {
      const config = { ...validConfig, name: '' };
      assert.throws(
        () => new TemplateParser(config),
        /Config\.name is required/
      );
    });

    await t.test('应该在缺少urlPattern时抛出错误', () => {
      const config = { ...validConfig };
      delete config.urlPattern;
      assert.throws(
        () => new TemplateParser(config),
        /Config\.urlPattern\.pattern is required/
      );
    });

    await t.test('应该在缺少urlPattern.pattern时抛出错误', () => {
      const config = {
        ...validConfig,
        urlPattern: {
          pathTemplate: '/test/*',
          queryParams: []
        }
      };
      assert.throws(
        () => new TemplateParser(config),
        /Config\.urlPattern\.pattern is required/
      );
    });

    await t.test('应该在urlPattern.pattern无效时抛出错误', () => {
      const config = {
        ...validConfig,
        urlPattern: {
          ...validConfig.urlPattern,
          pattern: '[invalid regex('
        }
      };
      assert.throws(
        () => new TemplateParser(config),
        /Invalid URL pattern/
      );
    });

    await t.test('应该在extractors不是数组时抛出错误', () => {
      const config = { ...validConfig, extractors: 'not-array' };
      assert.throws(
        () => new TemplateParser(config),
        /Config\.extractors must be an array/
      );
    });

    await t.test('应该在extractors为null时抛出错误', () => {
      const config = { ...validConfig, extractors: null };
      assert.throws(
        () => new TemplateParser(config),
        /Config\.extractors must be an array/
      );
    });

    await t.test('应该在extractors缺失时抛出错误', () => {
      const config = { ...validConfig };
      delete config.extractors;
      assert.throws(
        () => new TemplateParser(config),
        /Config\.extractors must be an array/
      );
    });

    await t.test('应该接受空的extractors数组', () => {
      const config = { ...validConfig, extractors: [] };
      const parser = new TemplateParser(config);
      assert.ok(parser);
      assert.strictEqual(parser.config.extractors.length, 0);
    });

    await t.test('应该接受没有priority的配置', () => {
      const config = { ...validConfig };
      delete config.priority;
      const parser = new TemplateParser(config);
      assert.strictEqual(parser.getPriority(), 0);
    });

    await t.test('应该接受没有filters的配置', () => {
      const config = { ...validConfig };
      delete config.filters;
      const parser = new TemplateParser(config);
      assert.ok(parser);
    });

    await t.test('应该接受没有metadata的配置', () => {
      const config = { ...validConfig };
      delete config.metadata;
      const parser = new TemplateParser(config);
      assert.ok(parser);
    });

    await t.test('应该正确初始化复杂配置', () => {
      const complexConfig = {
        name: 'complex-parser',
        description: 'Complex parser with multiple extractors and filters',
        priority: 150,
        urlPattern: {
          pattern: '^https://api\\.example\\.com/v[0-9]+/(.+)$',
          pathTemplate: '/v*/resource',
          queryParams: ['key', 'format']
        },
        extractors: [
          {
            field: 'title',
            type: 'text',
            selector: 'h1',
            required: true
          },
          {
            field: 'description',
            type: 'text',
            selector: '.description',
            pattern: '^Description:'
          },
          {
            field: 'dataTable',
            type: 'table',
            selector: 'table.data',
            columns: ['Name', 'Value', 'Type']
          },
          {
            field: 'examples',
            type: 'code',
            selector: 'pre code'
          },
          {
            field: 'features',
            type: 'list',
            selector: 'ul.features'
          }
        ],
        filters: [
          {
            type: 'remove',
            target: 'text',
            pattern: 'Advertisement',
            reason: 'Remove ads'
          },
          {
            type: 'transform',
            target: 'text',
            pattern: '\\s+',
            replacement: ' ',
            reason: 'Normalize whitespace'
          }
        ],
        metadata: {
          generatedAt: '2024-02-25T10:00:00.000Z',
          pageCount: 50,
          version: '2.0.0',
          author: 'test'
        }
      };
      
      const parser = new TemplateParser(complexConfig);
      
      // 验证所有属性都正确设置
      assert.strictEqual(parser.getName(), 'complex-parser');
      assert.strictEqual(parser.getPriority(), 150);
      assert.strictEqual(parser.config.extractors.length, 5);
      assert.strictEqual(parser.config.filters.length, 2);
      assert.ok(parser.matches('https://api.example.com/v1/users'));
      assert.ok(parser.matches('https://api.example.com/v2/posts'));
      assert.ok(!parser.matches('https://api.example.com/users'));
    });
  });

  await t.test('matches()', async (t) => {
    await t.test('应该正确匹配URL', () => {
      const parser = new TemplateParser(validConfig);
      assert.strictEqual(parser.matches('https://example.com/test/123'), true);
      assert.strictEqual(parser.matches('https://example.com/test/abc'), true);
    });

    await t.test('应该正确拒绝不匹配的URL', () => {
      const parser = new TemplateParser(validConfig);
      assert.strictEqual(parser.matches('https://example.com/other/123'), false);
      assert.strictEqual(parser.matches('https://other.com/test/123'), false);
    });
  });

  await t.test('getPriority()', async (t) => {
    await t.test('应该返回配置的优先级', () => {
      const parser = new TemplateParser(validConfig);
      assert.strictEqual(parser.getPriority(), 100);
    });

    await t.test('应该在未设置时返回默认优先级0', () => {
      const config = { ...validConfig };
      delete config.priority;
      const parser = new TemplateParser(config);
      assert.strictEqual(parser.getPriority(), 0);
    });
  });

  await t.test('getConfig()', async (t) => {
    await t.test('应该返回配置对象', () => {
      const parser = new TemplateParser(validConfig);
      const config = parser.getConfig();
      assert.strictEqual(config.name, 'test-parser');
      assert.strictEqual(config.priority, 100);
    });
  });

  await t.test('getName()', async (t) => {
    await t.test('应该返回Parser名称', () => {
      const parser = new TemplateParser(validConfig);
      assert.strictEqual(parser.getName(), 'test-parser');
    });
  });

  await t.test('parse() - 模拟测试', async (t) => {
    await t.test('应该返回包含type和url的结果', async () => {
      const parser = new TemplateParser(validConfig);
      
      // 创建模拟的page对象
      const mockPage = {
        evaluate: async () => 'Test Title'
      };
      
      const result = await parser.parse(mockPage, 'https://example.com/test/123');
      
      assert.strictEqual(result.type, 'test-parser');
      assert.strictEqual(result.url, 'https://example.com/test/123');
      assert.ok(result.timestamp);
    });

    await t.test('应该在提取失败时返回错误信息', async () => {
      const parser = new TemplateParser(validConfig);
      
      // 创建会抛出错误的模拟page对象
      const mockPage = {
        evaluate: async () => {
          throw new Error('Extraction failed');
        }
      };
      
      const result = await parser.parse(mockPage, 'https://example.com/test/123');
      
      assert.strictEqual(result.type, 'test-parser');
      assert.ok(result.error);
    });
  });

  await t.test('executeExtractor()', async (t) => {
    await t.test('应该在未知类型时抛出错误', async () => {
      const parser = new TemplateParser(validConfig);
      const mockPage = {};
      const invalidExtractor = {
        field: 'test',
        type: 'unknown',
        selector: 'div'
      };
      
      await assert.rejects(
        async () => await parser.executeExtractor(mockPage, invalidExtractor),
        /Unknown extractor type/
      );
    });
  });

  await t.test('extractText() - 模拟测试', async (t) => {
    await t.test('应该提取文本内容', async () => {
      const parser = new TemplateParser(validConfig);
      const mockPage = {
        evaluate: async () => 'Test Content'
      };
      
      const extractor = {
        field: 'content',
        type: 'text',
        selector: 'p'
      };
      
      const result = await parser.extractText(mockPage, extractor);
      assert.strictEqual(result, 'Test Content');
    });

    await t.test('应该在提取失败时抛出错误', async () => {
      const parser = new TemplateParser(validConfig);
      const mockPage = {
        evaluate: async () => {
          throw new Error('Element not found');
        }
      };
      
      const extractor = {
        field: 'content',
        type: 'text',
        selector: 'p'
      };
      
      await assert.rejects(
        async () => await parser.extractText(mockPage, extractor),
        /Text extraction failed/
      );
    });
  });

  await t.test('extractTable() - 模拟测试', async (t) => {
    await t.test('应该提取表格数据', async () => {
      const parser = new TemplateParser(validConfig);
      const mockPage = {
        evaluate: async () => [{
          headers: ['列1', '列2'],
          rows: [['值1', '值2']]
        }]
      };
      
      const extractor = {
        field: 'table',
        type: 'table',
        selector: 'table'
      };
      
      const result = await parser.extractTable(mockPage, extractor);
      assert.ok(result.headers);
      assert.ok(result.rows);
    });
  });

  await t.test('extractCode() - 模拟测试', async (t) => {
    await t.test('应该提取代码块', async () => {
      const parser = new TemplateParser(validConfig);
      const mockPage = {
        evaluate: async () => [{
          language: 'javascript',
          code: 'console.log("test");'
        }]
      };
      
      const extractor = {
        field: 'code',
        type: 'code',
        selector: 'pre code'
      };
      
      const result = await parser.extractCode(mockPage, extractor);
      assert.ok(Array.isArray(result));
      assert.strictEqual(result.length, 1);
    });
  });

  await t.test('extractList() - 模拟测试', async (t) => {
    await t.test('应该提取列表', async () => {
      const parser = new TemplateParser(validConfig);
      const mockPage = {
        evaluate: async () => [{
          type: 'ul',
          items: ['项目1', '项目2']
        }]
      };
      
      const extractor = {
        field: 'list',
        type: 'list',
        selector: 'ul'
      };
      
      const result = await parser.extractList(mockPage, extractor);
      assert.ok(Array.isArray(result));
      assert.strictEqual(result.length, 1);
    });
  });

  await t.test('applyFilters()', async (t) => {
    await t.test('应该返回原始结果（当前实现）', () => {
      const parser = new TemplateParser(validConfig);
      const result = { type: 'test', data: 'test data' };
      const filtered = parser.applyFilters(result);
      assert.deepStrictEqual(filtered, result);
    });

    await t.test('应该在没有过滤器时返回原始结果', () => {
      const parser = new TemplateParser(validConfig);
      const result = { 
        type: 'test', 
        url: 'https://example.com/test',
        title: 'Test Title',
        content: 'Test Content'
      };
      const filtered = parser.applyFilters(result);
      assert.deepStrictEqual(filtered, result);
    });

    await t.test('应该应用remove过滤器', () => {
      const config = {
        ...validConfig,
        filters: [
          {
            type: 'remove',
            target: 'text',
            pattern: 'Noise',
            reason: 'Remove noise'
          }
        ]
      };
      const parser = new TemplateParser(config);
      const result = {
        type: 'test',
        url: 'https://example.com/test',
        title: 'Test Title',
        content: 'This is Noise content'
      };
      const filtered = parser.applyFilters(result);
      assert.strictEqual(filtered.title, 'Test Title');
      assert.strictEqual(filtered.content, '');
    });

    await t.test('应该应用keep过滤器', () => {
      const config = {
        ...validConfig,
        filters: [
          {
            type: 'keep',
            target: 'text',
            pattern: '^Keep',
            reason: 'Keep only matching content'
          }
        ]
      };
      const parser = new TemplateParser(config);
      const result = {
        type: 'test',
        url: 'https://example.com/test',
        title: 'Keep This',
        content: 'Remove This'
      };
      const filtered = parser.applyFilters(result);
      assert.strictEqual(filtered.title, 'Keep This');
      assert.strictEqual(filtered.content, '');
    });

    await t.test('应该应用transform过滤器', () => {
      const config = {
        ...validConfig,
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
      const parser = new TemplateParser(config);
      const result = {
        type: 'test',
        url: 'https://example.com/test',
        title: 'Test   Title',
        content: 'Test\n\nContent'
      };
      const filtered = parser.applyFilters(result);
      assert.strictEqual(filtered.title, 'Test Title');
      assert.strictEqual(filtered.content, 'Test Content');
    });

    await t.test('应该应用多个过滤器', () => {
      const config = {
        ...validConfig,
        filters: [
          {
            type: 'remove',
            target: 'text',
            pattern: 'Noise',
            reason: 'Remove noise'
          },
          {
            type: 'transform',
            target: 'text',
            pattern: '\\s+',
            replacement: ' ',
            reason: 'Normalize whitespace'
          }
        ]
      };
      const parser = new TemplateParser(config);
      const result = {
        type: 'test',
        url: 'https://example.com/test',
        title: 'Test   Title',
        content: 'This is Noise content'
      };
      const filtered = parser.applyFilters(result);
      assert.strictEqual(filtered.title, 'Test Title');
      assert.strictEqual(filtered.content, '');
    });

    await t.test('应该处理数组类型的数据', () => {
      const config = {
        ...validConfig,
        filters: [
          {
            type: 'remove',
            target: 'code',
            pattern: 'debug',
            reason: 'Remove debug code'
          }
        ]
      };
      const parser = new TemplateParser(config);
      const result = {
        type: 'test',
        url: 'https://example.com/test',
        codeBlocks: [
          { language: 'js', code: 'console.log("test");' },
          { language: 'js', code: 'console.debug("debug");' }
        ]
      };
      const filtered = parser.applyFilters(result);
      assert.strictEqual(filtered.codeBlocks.length, 1);
      assert.strictEqual(filtered.codeBlocks[0].code, 'console.log("test");');
    });

    await t.test('应该处理表格数据', () => {
      const config = {
        ...validConfig,
        filters: [
          {
            type: 'remove',
            target: 'table',
            pattern: 'deprecated',
            reason: 'Remove deprecated rows'
          }
        ]
      };
      const parser = new TemplateParser(config);
      const result = {
        type: 'test',
        url: 'https://example.com/test',
        mainTable: {
          headers: ['Name', 'Status'],
          rows: [
            ['Feature A', 'active'],
            ['Feature B', 'deprecated']
          ]
        }
      };
      const filtered = parser.applyFilters(result);
      assert.strictEqual(filtered.mainTable.rows.length, 1);
      assert.deepStrictEqual(filtered.mainTable.rows[0], ['Feature A', 'active']);
    });

    await t.test('应该保留元数据字段', () => {
      const config = {
        ...validConfig,
        filters: [
          {
            type: 'remove',
            target: 'all',
            pattern: '.*',
            reason: 'Remove all'
          }
        ]
      };
      const parser = new TemplateParser(config);
      const result = {
        type: 'test',
        url: 'https://example.com/test',
        timestamp: '2024-01-01T00:00:00.000Z',
        title: 'Test Title'
      };
      const filtered = parser.applyFilters(result);
      assert.strictEqual(filtered.type, 'test');
      assert.strictEqual(filtered.url, 'https://example.com/test');
      assert.strictEqual(filtered.timestamp, '2024-01-01T00:00:00.000Z');
    });

    await t.test('应该处理过滤器错误', () => {
      const config = {
        ...validConfig,
        filters: [
          {
            type: 'unknown',
            target: 'text',
            pattern: 'test'
          }
        ]
      };
      const parser = new TemplateParser(config);
      const result = {
        type: 'test',
        url: 'https://example.com/test',
        title: 'Test Title'
      };
      // 应该不抛出错误，只是记录警告
      const filtered = parser.applyFilters(result);
      assert.strictEqual(filtered.title, 'Test Title');
    });
  });

  await t.test('removeFilter()', async (t) => {
    await t.test('应该移除匹配的文本内容', () => {
      const parser = new TemplateParser(validConfig);
      const filter = {
        type: 'remove',
        target: 'text',
        pattern: 'remove'
      };
      const result = {
        type: 'test',
        url: 'https://example.com/test',
        title: 'Keep this',
        content: 'Please remove this'
      };
      const filtered = parser.removeFilter(result, filter);
      assert.strictEqual(filtered.title, 'Keep this');
      assert.strictEqual(filtered.content, '');
    });

    await t.test('应该移除数组中匹配的项', () => {
      const parser = new TemplateParser(validConfig);
      const filter = {
        type: 'remove',
        target: 'code',
        pattern: 'debug'
      };
      const result = {
        type: 'test',
        url: 'https://example.com/test',
        codeBlocks: [
          { language: 'js', code: 'console.log("test");' },
          { language: 'js', code: 'console.debug("test");' },
          { language: 'js', code: 'console.info("test");' }
        ]
      };
      const filtered = parser.removeFilter(result, filter);
      assert.strictEqual(filtered.codeBlocks.length, 2);
    });

    await t.test('应该移除表格中匹配的行', () => {
      const parser = new TemplateParser(validConfig);
      const filter = {
        type: 'remove',
        target: 'table',
        pattern: 'deprecated'
      };
      const result = {
        type: 'test',
        url: 'https://example.com/test',
        mainTable: {
          headers: ['Name', 'Status'],
          rows: [
            ['Feature A', 'active'],
            ['Feature B', 'deprecated'],
            ['Feature C', 'active']
          ]
        }
      };
      const filtered = parser.removeFilter(result, filter);
      assert.strictEqual(filtered.mainTable.rows.length, 2);
    });
  });

  await t.test('keepFilter()', async (t) => {
    await t.test('应该只保留匹配的文本内容', () => {
      const parser = new TemplateParser(validConfig);
      const filter = {
        type: 'keep',
        target: 'text',
        pattern: '^Keep'
      };
      const result = {
        type: 'test',
        url: 'https://example.com/test',
        title: 'Keep this',
        content: 'Remove this'
      };
      const filtered = parser.keepFilter(result, filter);
      assert.strictEqual(filtered.title, 'Keep this');
      assert.strictEqual(filtered.content, '');
    });

    await t.test('应该只保留数组中匹配的项', () => {
      const parser = new TemplateParser(validConfig);
      const filter = {
        type: 'keep',
        target: 'code',
        pattern: 'log'
      };
      const result = {
        type: 'test',
        url: 'https://example.com/test',
        codeBlocks: [
          { language: 'js', code: 'console.log("test");' },
          { language: 'js', code: 'console.debug("test");' },
          { language: 'js', code: 'console.log("info");' }
        ]
      };
      const filtered = parser.keepFilter(result, filter);
      assert.strictEqual(filtered.codeBlocks.length, 2);
    });

    await t.test('应该只保留表格中匹配的行', () => {
      const parser = new TemplateParser(validConfig);
      const filter = {
        type: 'keep',
        target: 'table',
        pattern: 'active'
      };
      const result = {
        type: 'test',
        url: 'https://example.com/test',
        mainTable: {
          headers: ['Name', 'Status'],
          rows: [
            ['Feature A', 'active'],
            ['Feature B', 'deprecated'],
            ['Feature C', 'active']
          ]
        }
      };
      const filtered = parser.keepFilter(result, filter);
      assert.strictEqual(filtered.mainTable.rows.length, 2);
    });
  });

  await t.test('transformFilter()', async (t) => {
    await t.test('应该转换文本内容', () => {
      const parser = new TemplateParser(validConfig);
      const filter = {
        type: 'transform',
        target: 'text',
        pattern: '\\s+',
        replacement: ' '
      };
      const result = {
        type: 'test',
        url: 'https://example.com/test',
        title: 'Test   Title',
        content: 'Test\n\nContent'
      };
      const filtered = parser.transformFilter(result, filter);
      assert.strictEqual(filtered.title, 'Test Title');
      assert.strictEqual(filtered.content, 'Test Content');
    });

    await t.test('应该转换数组中的内容', () => {
      const parser = new TemplateParser(validConfig);
      const filter = {
        type: 'transform',
        target: 'code',
        pattern: 'console\\.log',
        replacement: 'logger.info'
      };
      const result = {
        type: 'test',
        url: 'https://example.com/test',
        codeBlocks: [
          { language: 'js', code: 'console.log("test");' },
          { language: 'js', code: 'console.log("info");' }
        ]
      };
      const filtered = parser.transformFilter(result, filter);
      assert.strictEqual(filtered.codeBlocks[0].code, 'logger.info("test");');
      assert.strictEqual(filtered.codeBlocks[1].code, 'logger.info("info");');
    });

    await t.test('应该转换表格中的内容', () => {
      const parser = new TemplateParser(validConfig);
      const filter = {
        type: 'transform',
        target: 'table',
        pattern: 'deprecated',
        replacement: 'legacy'
      };
      const result = {
        type: 'test',
        url: 'https://example.com/test',
        mainTable: {
          headers: ['Name', 'Status'],
          rows: [
            ['Feature A', 'active'],
            ['Feature B', 'deprecated']
          ]
        }
      };
      const filtered = parser.transformFilter(result, filter);
      assert.strictEqual(filtered.mainTable.rows[1][1], 'legacy');
    });

    await t.test('应该使用默认替换值', () => {
      const parser = new TemplateParser(validConfig);
      const filter = {
        type: 'transform',
        target: 'text',
        pattern: 'remove'
      };
      const result = {
        type: 'test',
        url: 'https://example.com/test',
        title: 'Please remove this'
      };
      const filtered = parser.transformFilter(result, filter);
      assert.strictEqual(filtered.title, 'Please  this');
    });
  });
});

console.log('\n=== TemplateParser 单元测试完成 ===\n');
