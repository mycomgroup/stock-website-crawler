# 模板分析器 - 需求文档

## 概述

从已抓取的页面数据中自动分析URL模式和页面模板，生成专用的Parser代码，提高数据提取的准确性和效率。

## 用户故事

### 故事1: URL模式聚类分析
**作为** 爬虫开发者  
**我想要** 自动分析links.txt中的URL，识别出不同的URL模式  
**以便** 了解网站有哪些类型的页面，为每种类型创建专用Parser

**验收标准**:
1. 能够读取links.txt文件，解析JSON格式的URL记录
2. 能够识别URL中的模式（路径结构、参数规律）
3. 能够将相似的URL自动分组（聚类）
4. 生成URL模式分析报告，包含：
   - 每种模式的正则表达式
   - 每种模式的URL数量
   - 每种模式的示例URL（3-5个）
5. 输出格式为JSON和Markdown两种

### 故事2: 页面模板内容分析
**作为** 爬虫开发者  
**我想要** 分析同一模板类型的多个页面，识别出模板内容和独特数据  
**以便** 知道哪些内容是噪音（需要过滤），哪些是有用数据（需要保留）

**验收标准**:
1. 能够读取指定URL组对应的markdown文件
2. 能够提取页面中的文本块（段落、标题、表格、代码块等）
3. 能够计算每个文本块在同组页面中的出现频率
4. 能够识别：
   - 高频内容（>80%出现率）= 模板内容/噪音
   - 低频内容（<20%出现率）= 独特数据
   - 中频内容（20-80%）= 需要进一步分析
5. 生成模板分析报告，包含：
   - 识别出的模板元素列表
   - 识别出的数据特征列表
   - 清洗前后的对比示例

### 故事3: 生成模板配置文件
**作为** 爬虫开发者  
**我想要** 根据模板分析结果，生成JSONL格式的模板配置文件  
**以便** 通过配置驱动的方式进行数据提取，安全且易于调整

**验收标准**:
1. 能够基于URL模式生成匹配规则
2. 能够基于模板分析生成提取规则，包含：
   - CSS选择器配置
   - 数据提取字段配置
   - 噪音过滤规则配置
3. 配置文件格式为JSONL（每行一个JSON对象）
4. 配置文件位置：`output/{project}/template-rules.jsonl`
5. 支持大模型自动修改配置（纯数据，无代码）
6. 配置包含完整的注释和说明

### 故事4: Skill集成
**作为** 系统  
**我想要** 将分析和生成功能封装为可复用的skills  
**以便** 可以通过简单的命令完成整个流程

**验收标准**:
1. 创建skill: `analyze-url-patterns`
   - 输入：links.txt路径
   - 输出：URL模式分析报告
2. 创建skill: `analyze-page-template`
   - 输入：URL模式名称、pages目录
   - 输出：模板内容分析报告
3. 创建skill: `generate-parser-code`
   - 输入：模板分析报告
   - 输出：Parser类代码文件
4. 创建skill: `template-analyzer-workflow`
   - 整合上述三个skill
   - 一键完成从分析到代码生成

## 功能需求

### FR1: URL模式识别
- 支持识别路径模式（如 `/open/api/doc`）
- 支持识别查询参数模式（如 `?api-key={value}`）
- 支持识别动态路径段（如 `/analytics/{type}/dashboard`）
- 自动生成正则表达式
- 支持自定义相似度阈值

### FR2: 内容频率分析
- 支持多种内容块类型：标题、段落、表格、列表、代码块
- 支持文本标准化（去除空格、换行等）
- 支持相似度计算（处理轻微变化的文本）
- 支持可配置的频率阈值

### FR3: 配置生成
- 生成符合JSONL格式的配置文件
- 支持自定义配置模板
- 生成完整的提取器配置（text, table, code, list）
- 生成完整的过滤器配置（remove, keep, transform）
- 包含元数据（生成时间、版本、页面数量）
- 包含注释和说明
- 易于大模型理解和修改

### FR4: 报告生成
- 生成详细的分析报告（Markdown格式）
- 包含可视化的统计图表（文本表格）
- 包含清洗前后的对比示例
- 包含建议和注意事项

## 非功能需求

### NFR1: 性能
- 分析1000个URL应在10秒内完成
- 分析100个页面应在30秒内完成
- 生成配置应在1秒内完成
- 配置加载应在100ms内完成

### NFR2: 可维护性
- 代码模块化，每个skill独立
- 配置与代码分离
- 详细的日志输出
- 完整的文档

### NFR3: 可扩展性
- 支持添加新的URL模式识别算法
- 支持添加新的内容分析策略
- 支持自定义配置格式
- 支持其他网站的分析
- 配置易于大模型修改和优化

## 数据模型

### URL模式
```typescript
interface URLPattern {
  name: string;              // 模式名称，如 "api-doc"
  pattern: RegExp;           // 正则表达式
  pathTemplate: string;      // 路径模板，如 "/open/api/doc"
  queryParams: string[];     // 查询参数列表
  urlCount: number;          // 匹配的URL数量
  samples: string[];         // 示例URL
}
```

### 模板分析结果
```typescript
interface TemplateAnalysis {
  templateName: string;
  urlPattern: URLPattern;
  pageCount: number;
  
  // 内容分类
  templateContent: ContentBlock[];  // 高频内容（噪音）
  uniqueContent: ContentBlock[];    // 低频内容（数据）
  mixedContent: ContentBlock[];     // 中频内容
  
  // 数据特征
  dataStructures: {
    tables: TableStructure[];
    codeBlocks: CodeBlockStructure[];
    lists: ListStructure[];
  };
  
  // 清洗规则
  cleaningRules: {
    removePatterns: string[];
    keepPatterns: string[];
    removeElements: string[];
  };
}
```

### 内容块
```typescript
interface ContentBlock {
  type: 'heading' | 'paragraph' | 'table' | 'code' | 'list';
  content: string;
  frequency: number;        // 出现次数
  frequencyRatio: number;   // 出现率 (0-1)
  samples: string[];        // 出现在哪些页面
}
```

### 模板配置
```typescript
interface TemplateConfig {
  // 基本信息
  name: string;              // 模板名称，如 "api-doc"
  description: string;       // 描述
  priority: number;          // 优先级
  
  // URL匹配规则
  urlPattern: {
    pattern: string;         // 正则表达式字符串
    pathTemplate: string;    // 路径模板
    queryParams: string[];   // 查询参数列表
  };
  
  // 数据提取规则
  extractors: Extractor[];
  
  // 噪音过滤规则
  filters: Filter[];
  
  // 元数据
  metadata: {
    generatedAt: string;     // ISO时间戳
    pageCount: number;       // 分析的页面数量
    version: string;         // 配置版本
  };
}

interface Extractor {
  field: string;             // 字段名
  type: 'text' | 'table' | 'code' | 'list';
  selector: string;          // CSS选择器
  required?: boolean;        // 是否必需
  pattern?: string;          // 匹配模式（可选）
  columns?: string[];        // 表格列名（table类型）
}

interface Filter {
  type: 'remove' | 'keep' | 'transform';
  target: string;            // 目标类型
  pattern: string;           // 匹配模式
  reason: string;            // 原因说明
}
```

## 技术约束

1. 使用Node.js和ES6+语法
2. 使用现有的文件系统API
3. 不引入新的重型依赖
4. 与现有Parser架构兼容
5. 输出文件使用UTF-8编码

## 优先级

1. **P0 (必须)**: 故事1 - URL模式聚类分析
2. **P0 (必须)**: 故事2 - 页面模板内容分析
3. **P1 (重要)**: 故事3 - 自动生成Parser代码
4. **P2 (可选)**: 故事4 - Skill集成

## 里程碑

### M1: 基础分析功能（3天）
- 完成URL模式识别
- 完成内容频率分析
- 生成基础分析报告

### M2: 配置生成功能（2天）
- 完成模板配置生成器
- 完成TemplateParser类（配置驱动）
- 完成ConfigLoader类
- 生成JSONL配置文件
- 集成到爬虫系统

### M3: Skill封装（1天）
- 创建独立的skills
- 编写skill文档
- 集成到工作流

## 测试策略

### 单元测试
- URL模式匹配测试
- 内容频率计算测试
- 配置生成测试
- 配置加载测试
- 提取器执行测试

### 集成测试
- 完整流程测试（从links.txt到生成配置）
- 多种URL模式测试
- 边界情况测试
- 配置驱动解析测试

### 验收测试
- 使用理杏仁的实际数据测试
- 验证生成的配置格式正确
- 验证TemplateParser能正常工作
- 验证解析效果与手写Parser相当

## 风险和缓解

### 风险1: URL模式识别不准确
**缓解**: 提供手动调整机制，支持自定义分组

### 风险2: 内容频率阈值难以确定
**缓解**: 提供可配置的阈值，生成多个版本供选择

### 风险3: 配置格式设计不合理
**缓解**: 参考现有Parser实现，提供配置验证工具，支持配置版本升级

## 参考资料

- 现有Parser实现：`src/parsers/api-doc-parser.js`
- Parser架构文档：`doc/PARSER_ARCHITECTURE.md`
- 已抓取数据：`output/lixinger-crawler/`
