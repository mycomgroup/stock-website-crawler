# Template Content Analyzer - 输出结构说明

## 新的输出结构

从现在开始，Template Content Analyzer 的输出采用更有组织的结构，每个模板一个独立文件。

### 目录结构

```
output/<projectName>/
├── url-patterns.json              # 输入：URL模式文件
├── pages/                         # 输入：爬取的markdown页面
│   ├── page1.md
│   ├── page2.md
│   └── ...
└── templates/                     # 输出：模板配置目录
    ├── template-summary.json      # 汇总文件
    ├── analytics-chart-maker.json # 单个模板配置
    ├── detail-sz.json
    ├── detail-sh.json
    └── ...                        # 每个URL模式一个文件
```

## 文件说明

### 1. template-summary.json（汇总文件）

包含所有模板的概览信息：

```json
{
  "projectName": "lixinger-crawler",
  "generatedAt": "2026-02-26T07:00:00.000Z",
  "totalTemplates": 106,
  "templates": [
    {
      "name": "analytics-chart-maker",
      "description": "图表制作工具 - 用于创建和管理自定义数据图表",
      "file": "analytics-chart-maker.json",
      "pageCount": 410,
      "extractors": 163,
      "filters": 4093,
      "urlPattern": "/analytics/chart-maker/{param2}"
    },
    ...
  ],
  "statistics": {
    "totalExtractors": 17000,
    "totalFilters": 430000,
    "totalPages": 45000,
    "avgExtractorsPerTemplate": "160.38",
    "avgFiltersPerTemplate": "4056.60"
  }
}
```

### 2. 单个模板配置文件

每个URL模式对应一个JSON文件，包含完整的提取器和过滤器配置：

**文件名格式**: `<pattern-name>.json`

**内容结构**:
```json
{
  "name": "analytics-chart-maker",
  "description": "图表制作工具 - 用于创建和管理自定义数据图表",
  "urlPattern": "/analytics/chart-maker/{param2}",
  "pathTemplate": "/analytics/chart-maker/{param2}",
  "extractors": [
    {
      "type": "heading",
      "level": 1,
      "content": "图表制作",
      "frequency": 0.95
    },
    ...
  ],
  "filters": [
    {
      "type": "remove_template_content",
      "pattern": "固定的导航栏内容",
      "frequency": 1.0
    },
    ...
  ],
  "metadata": {
    "pageCount": 410,
    "generatedAt": "2026-02-26T07:00:00.000Z",
    "thresholds": {
      "template": 0.8,
      "unique": 0.2
    }
  }
}
```

## 使用方式

### 运行分析

```bash
# 基本使用
node run-skill.js lixinger-crawler

# 自定义阈值
node run-skill.js lixinger-crawler --template-threshold 0.9 --unique-threshold 0.1
```

### 查看结果

```bash
# 查看汇总信息
cat output/lixinger-crawler/templates/template-summary.json

# 查看特定模板配置
cat output/lixinger-crawler/templates/analytics-chart-maker.json

# 列出所有模板文件
ls output/lixinger-crawler/templates/
```

### 使用模板配置

```javascript
const fs = require('fs');

// 1. 加载汇总文件
const summary = JSON.parse(
  fs.readFileSync('output/lixinger-crawler/templates/template-summary.json', 'utf-8')
);

console.log(`Total templates: ${summary.totalTemplates}`);

// 2. 加载特定模板
const templateConfig = JSON.parse(
  fs.readFileSync('output/lixinger-crawler/templates/analytics-chart-maker.json', 'utf-8')
);

console.log(`Extractors: ${templateConfig.extractors.length}`);
console.log(`Filters: ${templateConfig.filters.length}`);

// 3. 使用TemplateParser处理页面
const TemplateParser = require('./lib/template-parser');
const parser = new TemplateParser();

const result = parser.parse(markdownContent, templateConfig);
console.log(result.uniqueContent);
```

## 优势

### 1. 更好的组织性
- 每个模板一个文件，清晰明了
- 不会出现一个巨大的JSONL文件
- 易于查找和管理

### 2. 易于版本控制
- 可以单独追踪每个模板的变化
- Git diff 更清晰
- 可以选择性地提交某些模板

### 3. 便于使用
- 按需加载特定模板
- 不需要解析整个JSONL文件
- 支持并行处理

### 4. 可扩展性
- 易于添加新的模板
- 可以单独更新某个模板
- 支持模板的增量分析

## 与旧格式的对比

### 旧格式（JSONL）
```
template-rules.jsonl
  - 所有模板在一个文件中
  - 每行一个JSON对象
  - 文件可能很大（100+ 模板）
  - 难以查找特定模板
```

### 新格式（独立文件）
```
templates/
  ├── template-summary.json    # 快速查看所有模板
  ├── template-1.json          # 单独的模板文件
  ├── template-2.json
  └── ...
```

## 迁移指南

如果你有旧的JSONL格式文件，可以使用以下脚本转换：

```javascript
const fs = require('fs');
const path = require('path');

// 读取JSONL文件
const jsonlContent = fs.readFileSync('template-rules.jsonl', 'utf-8');
const configs = jsonlContent
  .split('\n')
  .filter(line => line.trim())
  .map(line => JSON.parse(line));

// 创建输出目录
const outputDir = 'templates';
fs.mkdirSync(outputDir, { recursive: true });

// 保存每个配置
configs.forEach(config => {
  const filename = `${config.name}.json`;
  const filepath = path.join(outputDir, filename);
  fs.writeFileSync(filepath, JSON.stringify(config, null, 2));
  console.log(`Saved: ${filename}`);
});

// 生成汇总文件
const summary = {
  totalTemplates: configs.length,
  templates: configs.map(cfg => ({
    name: cfg.name,
    file: `${cfg.name}.json`,
    extractors: cfg.extractors.length,
    filters: cfg.filters.length
  }))
};

fs.writeFileSync(
  path.join(outputDir, 'template-summary.json'),
  JSON.stringify(summary, null, 2)
);
console.log('Summary saved');
```

## 最佳实践

1. **定期备份** - templates目录包含重要的配置，建议定期备份
2. **版本控制** - 将templates目录纳入Git管理
3. **命名规范** - 保持模板名称与URL模式名称一致
4. **文档化** - 在summary中添加描述信息
5. **测试验证** - 生成后验证每个模板的有效性

## 故障排除

### 问题：找不到项目目录
```
Error: 找不到项目目录: lixinger-crawler
```

**解决方案**: 确保在正确的目录运行，或使用完整路径

### 问题：没有生成任何配置
```
✗ No configs generated
```

**解决方案**: 
- 检查pages目录是否有内容
- 检查URL模式是否正确
- 降低template-threshold阈值

### 问题：配置文件过大
```
Warning: Config file is very large (>10MB)
```

**解决方案**:
- 提高template-threshold以减少提取器数量
- 提高unique-threshold以减少过滤器数量
- 考虑拆分大型模板

---

**版本**: 2.0  
**更新时间**: 2026-02-26  
**作者**: Template Content Analyzer Team
