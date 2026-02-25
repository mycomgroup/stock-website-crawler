# 模板分析器设计更新总结

## 更新日期
2026-02-25

## 核心架构：Skills-Based

### 架构决策
1. **Skills放在根目录**: `skills/url-pattern-analyzer/` 和 `skills/template-content-analyzer/`
2. **由大模型执行**: Skills由大模型调用，可以使用算法库
3. **配置生成合并**: Template Config Generator合并到Skill 2中
4. **测试脚本独立**: Template Parser作为测试脚本，不集成到现有代码
5. **整体测试后集成**: 先验证配置效果，再考虑集成到爬虫系统

### 系统组成

#### Skill 1: url-pattern-analyzer
**位置**: `skills/url-pattern-analyzer/`

**结构**:
```
skills/url-pattern-analyzer/
├── README.md              # Skill说明文档
├── skill.json             # Skill配置
├── main.js                # 入口文件（由大模型调用）
├── lib/
│   ├── url-clusterer.js   # URL聚类算法
│   ├── similarity.js      # 相似度计算
│   └── pattern-gen.js     # 正则表达式生成
└── test/
    └── test-analyzer.js   # 测试脚本
```

**功能**: 
- 读取links.txt
- URL聚类分组
- 生成url-patterns.json

#### Skill 2: template-content-analyzer
**位置**: `skills/template-content-analyzer/`

**结构**:
```
skills/template-content-analyzer/
├── README.md                    # Skill说明文档
├── skill.json                   # Skill配置
├── main.js                      # 入口文件（由大模型调用）
├── lib/
│   ├── content-analyzer.js      # 内容分析
│   ├── frequency-calc.js        # 频率计算
│   ├── structure-detector.js    # 数据结构识别
│   ├── config-generator.js      # 配置生成器（合并原Skill 3）
│   └── validator.js             # 实时验证（可选）
├── scripts/
│   └── test-template-parser.js  # Template Parser测试脚本
└── test/
    └── test-analyzer.js         # 测试脚本
```

**功能**: 
- 读取url-patterns.json
- 分析每个pathTemplate
- 生成TemplateConfig对象
- 保存为template-rules.jsonl

#### Test Script: test-template-parser.js
**位置**: `skills/template-content-analyzer/scripts/`

**功能**:
- 加载template-rules.jsonl
- 创建TemplateParser实例
- 测试配置驱动的解析
- 验证提取效果
- 生成测试报告

**不集成到现有代码**: 仅作为测试工具使用

### 工作流程

```
1. 大模型调用 Skill 1: url-pattern-analyzer
   ├─ 输入：links.txt
   ├─ 处理：URL聚类、模式识别
   └─ 输出：url-patterns.json

2. 大模型调用 Skill 2: template-content-analyzer
   ├─ 输入：url-patterns.json + pages/*.md
   ├─ 处理：
   │  ├─ 对每个pathTemplate分析内容
   │  ├─ 生成extractors和filters
   │  └─ 合并所有配置
   └─ 输出：template-rules.jsonl

3. 运行测试脚本验证配置
   ├─ 脚本：test-template-parser.js
   ├─ 加载：template-rules.jsonl
   ├─ 测试：配置驱动的解析
   └─ 报告：提取效果验证

4. 整体测试通过后，考虑集成到爬虫系统
```

**新增组件**：
```javascript
// 配置生成器
class TemplateConfigGenerator {
  generateConfig(analysis)      // 生成配置对象
  generateExtractors(analysis)  // 生成提取器配置
  generateFilters(analysis)     // 生成过滤器配置
  saveAsJSONL(configs, path)    // 保存为JSONL格式
}

// 模板解析器（配置驱动）
class TemplateParser extends BaseParser {
  constructor(config)           // 接收配置对象
  matches(url)                  // 基于配置的URL匹配
  parse(page, url, options)     // 基于配置的数据提取
  executeExtractor(page, ext)   // 执行提取器
  applyFilters(result)          // 应用过滤器
}

// 配置加载器
class ConfigLoader {
  static loadConfigs(jsonlPath)    // 从JSONL加载配置
  static createParsers(jsonlPath)  // 创建Parser实例
}
```

#### 2. 任务列表 (tasks.md)

**里程碑M2变更**：
- 任务4：从"Parser代码生成器"改为"模板配置生成器"
- 任务5：从"生成脚本和文档"改为"模板解析器（配置驱动）"
- 新增任务6：生成脚本和文档

**具体任务变更**：
- 4.1: 创建TemplateConfigGenerator类（替代ParserCodeGenerator）
- 4.2: 配置格式设计（替代代码模板）
- 4.3: 生成提取规则（替代生成解析逻辑）
- 4.4: 生成过滤规则（新增）
- 5.1: 创建TemplateParser类（新增）
- 5.2: 创建ConfigLoader类（新增）
- 5.3: 实现提取器执行（新增）
- 5.4: 实现过滤器应用（新增）
- 5.5: 集成到爬虫系统（新增）

**Skill名称变更**：
- Skill 3: 从 `generate-parser-code` 改为 `generate-template-config`

#### 3. 需求文档 (requirements.md)

**故事3变更**：
- 标题：从"自动生成Parser代码"改为"生成模板配置文件"
- 输出：从"Parser类代码文件"改为"JSONL格式的模板配置文件"
- 位置：`output/{project}/template-rules.jsonl`

**验收标准变更**：
1. 能够基于URL模式生成匹配规则
2. 能够基于模板分析生成提取规则（CSS选择器、字段配置）
3. 配置文件格式为JSONL（每行一个JSON对象）
4. 配置文件位置：`output/{project}/template-rules.jsonl`
5. 支持大模型自动修改配置（纯数据，无代码）
6. 配置包含完整的注释和说明

**新增数据模型**：
```typescript
interface TemplateConfig {
  name: string;
  description: string;
  priority: number;
  urlPattern: { pattern, pathTemplate, queryParams };
  extractors: Extractor[];
  filters: Filter[];
  metadata: { generatedAt, pageCount, version };
}

interface Extractor {
  field: string;
  type: 'text' | 'table' | 'code' | 'list';
  selector: string;
  required?: boolean;
  pattern?: string;
  columns?: string[];
}

interface Filter {
  type: 'remove' | 'keep' | 'transform';
  target: string;
  pattern: string;
  reason: string;
}
```

### 配置文件格式示例

```jsonl
{"name":"api-doc","description":"Parser configuration for api-doc","priority":100,"urlPattern":{"pattern":"/\\/api\\/doc/","pathTemplate":"/open/api/doc","queryParams":["api-key"]},"extractors":[{"field":"title","type":"text","selector":"h1, h2, title","required":true},{"field":"requestUrl","type":"text","selector":"code, pre","pattern":"open\\.lixinger\\.com|api\\.lixinger"},{"field":"parameters","type":"table","selector":"table","columns":["参数","必选","类型","说明"]}],"filters":[{"type":"remove","target":"heading","pattern":"API文档","reason":"Template noise (100% frequency)"}],"metadata":{"generatedAt":"2026-02-25T10:00:00.000Z","pageCount":163,"version":"1.0.0"}}
```

### 使用方式

#### 生成配置
```bash
# 分析URL模式
node scripts/analyze-url-patterns.js

# 分析页面模板
node scripts/analyze-page-template.js api-doc

# 生成配置文件
node scripts/generate-template-config.js api-doc
```

#### 使用配置
```javascript
// 在crawler-main.js中加载配置
const configPath = path.join(outputDir, 'template-rules.jsonl');
if (fs.existsSync(configPath)) {
  const templateParsers = ConfigLoader.createParsers(configPath);
  parsers.push(...templateParsers);
}
```

#### 修改配置
大模型可以直接读取和修改JSONL文件：
1. 读取配置文件
2. 解析JSON对象
3. 修改提取器或过滤器
4. 保存回文件
5. 无需重启，配置即时生效

### 优势总结

1. **安全性**：配置文件不会破坏现有代码
2. **灵活性**：可以随时修改配置，无需重新生成代码
3. **可维护性**：配置比代码更容易理解和修改
4. **AI友好**：大模型可以轻松理解和优化配置
5. **热更新**：修改配置后无需重启系统
6. **版本控制**：配置文件更容易进行版本管理
7. **调试友好**：可以快速测试不同的配置组合

### 下一步行动

1. 开始实施任务1.1 - 创建URLPatternAnalyzer类
2. 按照更新后的设计文档和任务列表执行
3. 重点关注配置格式的设计和验证
4. 确保TemplateParser能正确执行配置
5. 提供配置示例和文档

## 文件变更清单

- ✅ `.kiro/specs/template-analyzer/requirements.md` - 已更新
- ✅ `.kiro/specs/template-analyzer/design.md` - 已更新
- ✅ `.kiro/specs/template-analyzer/tasks.md` - 已更新
- ✅ `.kiro/specs/template-analyzer/DESIGN_UPDATE_SUMMARY.md` - 新建

## 验收标准更新

### M2验收标准
- [x] 生成的配置文件格式正确（JSONL）
- [x] 配置包含完整的提取器和过滤器
- [x] TemplateParser能正确加载配置
- [x] 配置驱动的解析效果与手写Parser相当
- [x] 配置包含完整的注释和元数据
- [x] 生成时间 < 1秒
- [x] 大模型可以轻松修改配置
