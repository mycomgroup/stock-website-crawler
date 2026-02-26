import { describe, it, beforeEach, afterEach } from 'node:test';
import assert from 'node:assert';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import ConfigLoader from '../lib/config-loader.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

describe('ConfigLoader', () => {
  const testDir = path.join(__dirname, 'fixtures', 'config-loader');
  const validConfigPath = path.join(testDir, 'valid-config.jsonl');
  const invalidConfigPath = path.join(testDir, 'invalid-config.jsonl');
  const emptyConfigPath = path.join(testDir, 'empty-config.jsonl');
  const malformedConfigPath = path.join(testDir, 'malformed-config.jsonl');

  beforeEach(() => {
    // 创建测试目录
    if (!fs.existsSync(testDir)) {
      fs.mkdirSync(testDir, { recursive: true });
    }

    // 创建有效的配置文件
    const validConfig1 = {
      name: 'api-doc',
      description: 'API documentation parser',
      priority: 100,
      urlPattern: {
        pattern: '^https://www\\.example\\.com/api/doc\\?id=(.+)$',
        pathTemplate: '/api/doc',
        queryParams: ['id']
      },
      extractors: [
        {
          field: 'title',
          type: 'text',
          selector: 'h1',
          required: true
        },
        {
          field: 'parameters',
          type: 'table',
          selector: 'table.params',
          columns: ['name', 'type', 'description']
        }
      ],
      filters: [
        {
          type: 'remove',
          target: 'heading',
          pattern: 'Navigation',
          reason: 'Template noise'
        }
      ],
      metadata: {
        generatedAt: '2024-01-01T00:00:00.000Z',
        pageCount: 50,
        version: '1.0.0'
      }
    };

    const validConfig2 = {
      name: 'dashboard',
      description: 'Dashboard parser',
      priority: 90,
      urlPattern: {
        pattern: '^https://www\\.example\\.com/dashboard$',
        pathTemplate: '/dashboard',
        queryParams: []
      },
      extractors: [
        {
          field: 'title',
          type: 'text',
          selector: 'h1'
        },
        {
          field: 'codeBlocks',
          type: 'code',
          selector: 'pre code'
        }
      ],
      filters: []
    };

    fs.writeFileSync(
      validConfigPath,
      JSON.stringify(validConfig1) + '\n' + JSON.stringify(validConfig2)
    );

    // 创建空配置文件
    fs.writeFileSync(emptyConfigPath, '');

    // 创建格式错误的配置文件
    fs.writeFileSync(
      malformedConfigPath,
      '{"name": "test", "invalid json\n{"name": "test2"}'
    );

    // 创建缺少必需字段的配置文件
    const invalidConfig = {
      name: 'incomplete',
      // 缺少 urlPattern 和 extractors
    };
    fs.writeFileSync(invalidConfigPath, JSON.stringify(invalidConfig));
  });

  afterEach(() => {
    // 清理测试文件
    if (fs.existsSync(testDir)) {
      fs.rmSync(testDir, { recursive: true, force: true });
    }
  });

  describe('loadConfigs()', () => {
    it('应该成功加载有效的JSONL配置文件', () => {
      const configs = ConfigLoader.loadConfigs(validConfigPath);
      
      assert.strictEqual(configs.length, 2);
      assert.strictEqual(configs[0].name, 'api-doc');
      assert.strictEqual(configs[1].name, 'dashboard');
    });

    it('应该在文件不存在时抛出错误', () => {
      const nonExistentPath = path.join(testDir, 'non-existent.jsonl');
      
      assert.throws(
        () => ConfigLoader.loadConfigs(nonExistentPath),
        /Config file not found/
      );
    });

    it('应该在文件为空时抛出错误', () => {
      assert.throws(
        () => ConfigLoader.loadConfigs(emptyConfigPath),
        /Config file is empty/
      );
    });

    it('应该在JSON格式错误时抛出错误', () => {
      assert.throws(
        () => ConfigLoader.loadConfigs(malformedConfigPath),
        /Invalid JSON/
      );
    });

    it('应该在配置验证失败时抛出错误', () => {
      assert.throws(
        () => ConfigLoader.loadConfigs(invalidConfigPath),
        /Config validation failed/
      );
    });

    it('应该跳过空行', () => {
      const configWithEmptyLines = path.join(testDir, 'with-empty-lines.jsonl');
      const config = {
        name: 'test',
        urlPattern: { pattern: 'test', pathTemplate: '/test' },
        extractors: [{ field: 'title', type: 'text', selector: 'h1' }]
      };
      
      fs.writeFileSync(
        configWithEmptyLines,
        JSON.stringify(config) + '\n\n' + JSON.stringify(config)
      );

      const configs = ConfigLoader.loadConfigs(configWithEmptyLines);
      assert.strictEqual(configs.length, 2);
    });
  });

  describe('validateConfig()', () => {
    it('应该验证通过有效的配置', () => {
      const validConfig = {
        name: 'test',
        urlPattern: {
          pattern: 'test',
          pathTemplate: '/test'
        },
        extractors: [
          {
            field: 'title',
            type: 'text',
            selector: 'h1'
          }
        ]
      };

      const error = ConfigLoader.validateConfig(validConfig, 1);
      assert.strictEqual(error, null);
    });

    it('应该检测缺少必需字段', () => {
      const invalidConfig = {
        name: 'test'
        // 缺少 urlPattern 和 extractors
      };

      const error = ConfigLoader.validateConfig(invalidConfig, 1);
      assert.ok(error);
      assert.ok(error.includes('Missing required field'));
    });

    it('应该检测缺少urlPattern.pattern', () => {
      const invalidConfig = {
        name: 'test',
        urlPattern: {
          pathTemplate: '/test'
          // 缺少 pattern
        },
        extractors: [{ field: 'title', type: 'text', selector: 'h1' }]
      };

      const error = ConfigLoader.validateConfig(invalidConfig, 1);
      assert.ok(error);
      assert.ok(error.includes('urlPattern.pattern is required'));
    });

    it('应该检测缺少urlPattern.pathTemplate', () => {
      const invalidConfig = {
        name: 'test',
        urlPattern: {
          pattern: 'test'
          // 缺少 pathTemplate
        },
        extractors: [{ field: 'title', type: 'text', selector: 'h1' }]
      };

      const error = ConfigLoader.validateConfig(invalidConfig, 1);
      assert.ok(error);
      assert.ok(error.includes('urlPattern.pathTemplate is required'));
    });

    it('应该检测extractors不是数组', () => {
      const invalidConfig = {
        name: 'test',
        urlPattern: { pattern: 'test', pathTemplate: '/test' },
        extractors: 'not an array'
      };

      const error = ConfigLoader.validateConfig(invalidConfig, 1);
      assert.ok(error);
      assert.ok(error.includes('extractors must be an array'));
    });

    it('应该检测extractors为空数组', () => {
      const invalidConfig = {
        name: 'test',
        urlPattern: { pattern: 'test', pathTemplate: '/test' },
        extractors: []
      };

      const error = ConfigLoader.validateConfig(invalidConfig, 1);
      assert.ok(error);
      assert.ok(error.includes('extractors array cannot be empty'));
    });

    it('应该检测extractor缺少field', () => {
      const invalidConfig = {
        name: 'test',
        urlPattern: { pattern: 'test', pathTemplate: '/test' },
        extractors: [
          {
            type: 'text',
            selector: 'h1'
            // 缺少 field
          }
        ]
      };

      const error = ConfigLoader.validateConfig(invalidConfig, 1);
      assert.ok(error);
      assert.ok(error.includes('Missing field name'));
    });

    it('应该检测extractor缺少type', () => {
      const invalidConfig = {
        name: 'test',
        urlPattern: { pattern: 'test', pathTemplate: '/test' },
        extractors: [
          {
            field: 'title',
            selector: 'h1'
            // 缺少 type
          }
        ]
      };

      const error = ConfigLoader.validateConfig(invalidConfig, 1);
      assert.ok(error);
      assert.ok(error.includes('Missing type'));
    });

    it('应该检测extractor缺少selector', () => {
      const invalidConfig = {
        name: 'test',
        urlPattern: { pattern: 'test', pathTemplate: '/test' },
        extractors: [
          {
            field: 'title',
            type: 'text'
            // 缺少 selector
          }
        ]
      };

      const error = ConfigLoader.validateConfig(invalidConfig, 1);
      assert.ok(error);
      assert.ok(error.includes('Missing selector'));
    });

    it('应该检测无效的extractor type', () => {
      const invalidConfig = {
        name: 'test',
        urlPattern: { pattern: 'test', pathTemplate: '/test' },
        extractors: [
          {
            field: 'title',
            type: 'invalid-type',
            selector: 'h1'
          }
        ]
      };

      const error = ConfigLoader.validateConfig(invalidConfig, 1);
      assert.ok(error);
      assert.ok(error.includes('Invalid type'));
    });

    it('应该检测filters不是数组', () => {
      const invalidConfig = {
        name: 'test',
        urlPattern: { pattern: 'test', pathTemplate: '/test' },
        extractors: [{ field: 'title', type: 'text', selector: 'h1' }],
        filters: 'not an array'
      };

      const error = ConfigLoader.validateConfig(invalidConfig, 1);
      assert.ok(error);
      assert.ok(error.includes('filters must be an array'));
    });
  });

  describe('createParsers()', () => {
    it('应该在没有ParserClass时返回配置对象', () => {
      const parsers = ConfigLoader.createParsers(validConfigPath);
      
      assert.strictEqual(parsers.length, 2);
      assert.strictEqual(parsers[0].name, 'api-doc');
      assert.strictEqual(parsers[1].name, 'dashboard');
    });

    it('应该使用提供的ParserClass创建实例', () => {
      class MockParser {
        constructor(config) {
          this.config = config;
          this.type = 'MockParser';
        }
      }

      const parsers = ConfigLoader.createParsers(validConfigPath, MockParser);
      
      assert.strictEqual(parsers.length, 2);
      assert.strictEqual(parsers[0].type, 'MockParser');
      assert.strictEqual(parsers[0].config.name, 'api-doc');
      assert.strictEqual(parsers[1].type, 'MockParser');
      assert.strictEqual(parsers[1].config.name, 'dashboard');
    });

    it('应该在Parser构造失败时抛出错误', () => {
      class FailingParser {
        constructor(config) {
          throw new Error('Parser construction failed');
        }
      }

      assert.throws(
        () => ConfigLoader.createParsers(validConfigPath, FailingParser),
        /Failed to create parser/
      );
    });
  });

  describe('loadConfigByName()', () => {
    it('应该按名称加载配置', () => {
      const config = ConfigLoader.loadConfigByName(validConfigPath, 'api-doc');
      
      assert.ok(config);
      assert.strictEqual(config.name, 'api-doc');
      assert.strictEqual(config.priority, 100);
    });

    it('应该在配置不存在时返回null', () => {
      const config = ConfigLoader.loadConfigByName(validConfigPath, 'non-existent');
      
      assert.strictEqual(config, null);
    });
  });

  describe('getConfigStats()', () => {
    it('应该返回正确的统计信息', () => {
      const stats = ConfigLoader.getConfigStats(validConfigPath);
      
      assert.strictEqual(stats.totalConfigs, 2);
      assert.deepStrictEqual(stats.configNames, ['api-doc', 'dashboard']);
      assert.strictEqual(stats.totalExtractors, 4); // 2 + 2
      assert.strictEqual(stats.totalFilters, 1);
      
      // 检查extractor类型统计
      assert.strictEqual(stats.extractorTypes.text, 2);
      assert.strictEqual(stats.extractorTypes.table, 1);
      assert.strictEqual(stats.extractorTypes.code, 1);
      
      // 检查filter类型统计
      assert.strictEqual(stats.filterTypes.remove, 1);
    });

    it('应该处理没有filters的配置', () => {
      const stats = ConfigLoader.getConfigStats(validConfigPath);
      
      assert.strictEqual(stats.totalFilters, 1); // 只有第一个配置有filter
    });
  });
});
