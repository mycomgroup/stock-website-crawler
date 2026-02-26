# Template Content Analyzer - 脚本说明

本目录包含用于模板内容分析和配置驱动解析的脚本。

## 脚本列表

### 1. analyze-page-template.js

分析页面模板，生成模板分析报告。

**用法**:
```bash
node scripts/analyze-page-template.js [options]
```

**功能**:
- 分析URL模式对应的页面内容
- 识别模板内容和独特数据
- 生成清洗规则
- 输出JSON和Markdown格式报告

### 2. test-template-parser.js

测试配置驱动的TemplateParser（基础测试）。

**用法**:
```bash
# 使用示例配置
node scripts/test-template-parser.js

# 使用自定义配置
node scripts/test-template-parser.js path/to/config.jsonl
```

**功能**:
- 加载JSONL格式的模板配置
- 创建TemplateParser实例
- 测试URL匹配
- 显示Parser详细信息

### 3. test-config-parsing.js

使用Playwright测试配置驱动的解析（任务 5.5.4）。

**用法**:
```bash
# 使用示例配置
node scripts/test-config-parsing.js

# 使用自定义配置
node scripts/test-config-parsing.js path/to/config.jsonl
```

**功能**:
- 使用真实的Playwright页面对象
- 测试所有提取器类型（text, table, code, list）
- 验证URL匹配和优先级
- 测试完整的解析流程
- 使用测试HTML页面验证功能

**测试内容**:
- ✓ 文本提取器（text）
- ✓ 表格提取器（table）
- ✓ 代码块提取器（code）
- ✓ 列表提取器（list）
- ✓ URL匹配和优先级
- ✓ 完整解析流程

### 4. test-real-pages.js

使用真实网页测试配置驱动的解析。

**用法**:
```bash
# 测试真实网页
node scripts/test-real-pages.js examples/template-config.jsonl https://www.lixinger.com/open/api/doc?api-key=cn/company
```

**功能**:
- 访问真实网页
- 使用配置驱动的解析
- 验证提取器在真实页面上的效果
- 保存解析结果到文件

**注意**: 需要网络连接和目标网站可访问

### 5. generate-template-config.js

根据URL模式和页面分析结果，生成JSONL格式的模板配置文件。

**用法**:
```bash
node scripts/generate-template-config.js [options]
```

**选项**:
- `--patterns, -p <path>`: URL模式文件路径 (默认: stock-crawler/output/lixinger-crawler/url-patterns.json)
- `--pages, -d <path>`: 页面目录路径 (默认: stock-crawler/output/lixinger-crawler/pages)
- `--output, -o <path>`: 输出文件路径 (默认: stock-crawler/output/lixinger-crawler/template-rules.jsonl)
- `--pattern-name, -n <name>`: 只生成指定名称的模式配置 (可选)
- `--template-threshold <number>`: 模板内容阈值 (默认: 0.8)
- `--unique-threshold <number>`: 独特内容阈值 (默认: 0.2)
- `--yes, -y`: 跳过确认提示
- `--help, -h`: 显示帮助信息

**功能**:
- 自动分析页面内容并生成配置
- 支持批量生成多个模式的配置
- 提供交互式确认
- 生成详细的报告

**示例**:
```bash
# 生成所有模式的配置
node scripts/generate-template-config.js

# 只生成api-doc模式的配置
node scripts/generate-template-config.js -n api-doc

# 自定义输出路径
node scripts/generate-template-config.js -o output/my-rules.jsonl

# 跳过确认提示
node scripts/generate-template-config.js -y

# 自定义阈值
node scripts/generate-template-config.js --template-threshold 0.9 --unique-threshold 0.1
```

**输出文件**:
- `template-rules.jsonl`: 模板配置文件（JSONL格式）
- `template-rules-report.json`: 生成报告（包含统计信息和详细信息）

### 6. test-generate-config.js

测试generate-template-config.js脚本的功能。

**用法**:
```bash
node scripts/test-generate-config.js
```

**功能**:
- 验证脚本可执行性
- 测试命令行参数解析
- 检查依赖模块
- 验证输入文件检查

### 7. validate-config-workflow.js ⭐ **推荐**

综合验证脚本，验证配置驱动解析的完整工作流（任务 5.5）。

**用法**:
```bash
# 使用示例配置
node scripts/validate-config-workflow.js

# 使用自定义配置
node scripts/validate-config-workflow.js path/to/config.jsonl

# 详细输出模式
node scripts/validate-config-workflow.js --verbose
```

**功能**:
- ✅ 步骤1: 加载JSONL配置文件
- ✅ 步骤2: 创建TemplateParser实例
- ✅ 步骤3: 测试URL匹配和优先级
- ✅ 步骤4: 使用Playwright测试数据提取
- ✅ 步骤5: 生成详细的验证报告

**输出**:
- 控制台显示详细的验证过程
- 生成验证报告: `output/validation-report.json`
- 返回退出码: 0表示成功，1表示失败

**验证内容**:
- 配置文件格式正确性
- Parser实例创建成功
- URL正则匹配准确性
- 所有提取器类型工作正常（text, table, code, list）
- 数据提取完整性
- 过滤器应用效果

**示例输出**:
```
======================================================================
配置驱动解析 - 完整工作流验证
======================================================================

步骤 1: 加载配置文件
----------------------------------------------------------------------
✓ 成功加载 2 个配置

配置统计:
  总配置数: 2
  配置名称: api-doc, dashboard
  总提取器数: 9
  总过滤器数: 2

步骤 2: 创建TemplateParser实例
----------------------------------------------------------------------
✓ 创建Parser: api-doc (优先级: 100)
✓ 创建Parser: dashboard (优先级: 90)

步骤 3: 测试URL匹配
----------------------------------------------------------------------
测试URL: https://www.lixinger.com/open/api/doc?api-key=cn/company
  ✓ 匹配: api-doc (优先级: 100)

步骤 4: 测试数据提取（使用Playwright）
----------------------------------------------------------------------
✓ 浏览器启动成功
✓ 解析成功
提取字段: 6/6

步骤 5: 生成验证报告
----------------------------------------------------------------------
✓ 报告已保存: output/validation-report.json

======================================================================
验证总结
======================================================================
步骤 1 - 加载配置文件: ✓ 通过
步骤 2 - 创建Parser实例: ✓ 通过
步骤 3 - URL匹配测试: ✓ 通过
步骤 4 - 数据提取测试: ✓ 通过

总体结果: ✓ 所有测试通过

结论: 配置驱动的解析功能正常工作，可以投入使用
```

**验证报告格式**:
```json
{
  "timestamp": "2026-02-25T22:10:04.391Z",
  "summary": {
    "configLoaded": true,
    "parsersCreated": 2,
    "urlMatchingPassed": true,
    "dataExtractionPassed": true
  },
  "details": {
    "step1": { ... },
    "step2": { ... },
    "step3": { ... },
    "step4": { ... }
  }
}
```

**示例输出**:
```
============================================================
TemplateParser 配置驱动测试
============================================================

步骤 1: 加载配置文件
------------------------------------------------------------
✓ 成功加载 2 个配置

配置统计:
  - 总配置数: 2
  - 配置名称: api-doc, dashboard
  - 总提取器数: 9
  - 总过滤器数: 2

步骤 2: 创建TemplateParser实例
------------------------------------------------------------
✓ 创建Parser: api-doc (优先级: 100)
✓ 创建Parser: dashboard (优先级: 90)

成功创建 2/2 个Parser实例

步骤 3: 测试URL匹配
------------------------------------------------------------
测试URL: https://www.lixinger.com/open/api/doc?api-key=cn/company
  ✓ 匹配Parser: api-doc

步骤 4: Parser详细信息
------------------------------------------------------------
Parser: api-doc
  描述: Parser configuration for /open/api/doc
  优先级: 100
  URL模式: ^https://www\.lixinger\.com/open/api/doc\?api-key=(.+)$
  路径模板: /open/api/doc
  查询参数: api-key
  提取器数量: 6
  ...
```

## 配置文件格式

配置文件使用JSONL格式（每行一个JSON对象）。

**示例配置** (`examples/template-config.jsonl`):

```jsonl
{"name":"api-doc","description":"Parser configuration for /open/api/doc","priority":100,"urlPattern":{"pattern":"^https://www\\.lixinger\\.com/open/api/doc\\?api-key=(.+)$","pathTemplate":"/open/api/doc","queryParams":["api-key"]},"extractors":[{"field":"title","type":"text","selector":"h1, h2, title","required":true},{"field":"parameters","type":"table","selector":"table","columns":["参数名称","必选","类型","说明"]}],"filters":[{"type":"remove","target":"heading","pattern":"API文档","reason":"Template noise (100% frequency)"}],"metadata":{"generatedAt":"2024-02-25T10:00:00.000Z","pageCount":163,"version":"1.0.0"}}
```

**配置结构**:

```javascript
{
  // 基本信息
  "name": "api-doc",                    // 模板名称
  "description": "...",                 // 描述
  "priority": 100,                      // 优先级
  
  // URL匹配规则
  "urlPattern": {
    "pattern": "^https://...",          // 正则表达式
    "pathTemplate": "/open/api/doc",    // 路径模板
    "queryParams": ["api-key"]          // 查询参数
  },
  
  // 数据提取规则
  "extractors": [
    {
      "field": "title",                 // 字段名
      "type": "text",                   // 类型: text, table, code, list
      "selector": "h1, h2, title",      // CSS选择器
      "required": true,                 // 是否必需
      "pattern": "^获取",               // 匹配模式（可选）
      "columns": ["列1", "列2"]         // 表格列名（table类型）
    }
  ],
  
  // 噪音过滤规则
  "filters": [
    {
      "type": "remove",                 // 类型: remove, keep, transform
      "target": "heading",              // 目标类型
      "pattern": "API文档",             // 匹配模式
      "reason": "Template noise"        // 原因说明
    }
  ],
  
  // 元数据
  "metadata": {
    "generatedAt": "2024-02-25T10:00:00.000Z",
    "pageCount": 163,
    "version": "1.0.0"
  }
}
```

## 工作流程

### 完整工作流程

1. **分析URL模式** (使用 url-pattern-analyzer skill)
   ```bash
   # 生成 url-patterns.json
   ```

2. **生成模板配置** (使用 generate-template-config.js) - **推荐方式**
   ```bash
   # 一步生成配置文件
   node scripts/generate-template-config.js -y
   # 生成 template-rules.jsonl 和 template-rules-report.json
   ```

   或者分步执行：

   a. **分析页面模板** (使用 analyze-page-template.js)
   ```bash
   node scripts/analyze-page-template.js
   # 生成模板分析报告
   ```

   b. **手动生成配置文件**
   ```bash
   # 基于分析报告手动创建配置
   ```

3. **测试配置** (使用 test-template-parser.js)
   ```bash
   node scripts/test-template-parser.js template-rules.jsonl
   # 验证配置正确性
   ```

4. **使用配置进行解析** (任务 5.5.4)
   ```bash
   # 使用Playwright实际测试解析效果
   node scripts/test-config-parsing.js template-rules.jsonl
   ```

## 相关文件

- `lib/config-loader.js` - 配置加载器
- `lib/template-parser.js` - 配置驱动的解析器
- `lib/content-analyzer.js` - 内容分析器
- `examples/template-config.jsonl` - 示例配置文件
- `test/config-loader.test.js` - ConfigLoader单元测试
- `test/template-parser.test.js` - TemplateParser单元测试

## 测试

运行所有测试:
```bash
npm test
```

运行特定测试:
```bash
node test/config-loader.test.js
node test/template-parser.test.js
```

## 下一步

- 任务 5.5.4: 测试配置驱动的解析（需要Playwright）
- 任务 5.6: 完善单元测试
- 任务 6: 生成脚本和文档

## 注意事项

1. **配置文件格式**: 必须是有效的JSONL格式，每行一个完整的JSON对象
2. **正则表达式**: pattern字段可以是字符串或 `/pattern/flags` 格式
3. **提取器类型**: 支持 text, table, code, list 四种类型
4. **过滤器**: 当前实现为占位符，未来可扩展
5. **独立测试**: 当前脚本不依赖爬虫系统，可独立运行

## 问题排查

### 配置加载失败

检查配置文件格式:
```bash
# 验证JSON格式
cat config.jsonl | jq .
```

### URL不匹配

检查正则表达式:
```javascript
const pattern = new RegExp(config.urlPattern.pattern);
console.log(pattern.test(url));
```

### 提取器执行失败

检查CSS选择器和页面结构是否匹配。
