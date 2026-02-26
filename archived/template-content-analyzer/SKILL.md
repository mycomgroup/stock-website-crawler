# Template Content Analyzer Skill

## 📋 技能概述

**名称**: template-content-analyzer  
**版本**: 2.0.0  
**类型**: 内容分析工具  
**作者**: Template Analyzer Team

**功能描述**:  
分析markdown页面内容，识别模板模式和独特数据，自动生成提取器和过滤器配置。通过频率分析区分固定的模板内容和变化的独特内容。

**关键词**: template-analysis, content-analysis, frequency-analysis, markdown-parser, web-crawler

---

## 🎯 使用场景

1. **网页爬虫优化** - 识别页面模板，只保存独特内容
2. **数据提取** - 自动生成内容提取规则
3. **模板识别** - 发现多个页面的共同结构
4. **内容去重** - 过滤重复的模板内容
5. **配置生成** - 自动生成TemplateParser配置

---

## 🚀 快速开始

### 基本使用

```bash
# 分析lixinger-crawler项目的页面模板
node run-skill.js lixinger-crawler
```

### 自定义阈值

```bash
# 使用更严格的模板阈值
node run-skill.js lixinger-crawler --template-threshold 0.9

# 同时调整独特内容阈值
node run-skill.js lixinger-crawler --template-threshold 0.9 --unique-threshold 0.1
```

---

## 📥 输入参数

### 必需参数

#### 1. projectName
- **类型**: string
- **描述**: 项目名称，对应output目录下的子目录
- **示例**: `lixinger-crawler`
- **说明**: 脚本会自动查找 `output/<projectName>/` 目录

### 可选参数

#### 2. --template-threshold
- **类型**: number (0-1)
- **描述**: 模板内容频率阈值
- **默认值**: 0.8
- **说明**: 
  - 出现频率 ≥ 此值的内容被视为模板内容
  - 值越高，识别越严格
  - 建议范围: 0.7 - 0.95

#### 3. --unique-threshold
- **类型**: number (0-1)
- **描述**: 独特内容频率阈值
- **默认值**: 0.2
- **说明**:
  - 出现频率 ≤ 此值的内容被视为独特内容
  - 值越低，识别越严格
  - 建议范围: 0.05 - 0.3

#### 4. --sample-urls
- **类型**: string (逗号分隔)
- **描述**: 可选的样例URL，用于实时验证
- **示例**: `--sample-urls "https://example.com/page1,https://example.com/page2"`

---

## 📤 输出结构

### 目录结构

```
output/<projectName>/
├── url-patterns.json              # 输入：URL模式文件
├── pages/                         # 输入：markdown页面
└── templates/                     # 输出：模板配置目录
    ├── template-summary.json      # 汇总文件
    ├── analytics-chart-maker.json # 单个模板配置
    ├── detail-sz.json
    └── ...                        # 每个URL模式一个文件
```

### 输出文件说明

#### 1. template-summary.json（汇总文件）

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
    }
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

#### 2. 单个模板配置文件

每个URL模式对应一个JSON文件：

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
    }
  ],
  "filters": [
    {
      "type": "remove_template_content",
      "pattern": "固定的导航栏内容",
      "frequency": 1.0
    }
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

---

## 💡 工作原理

### 分析流程

```
1. 加载URL模式
   ↓
2. 匹配对应的markdown文件
   ↓
3. 解析markdown内容
   ↓
4. 频率分析
   ├─ 统计每个内容块的出现频率
   ├─ 识别模板内容（高频）
   └─ 识别独特内容（低频）
   ↓
5. 生成配置
   ├─ 创建extractors（提取独特内容）
   └─ 创建filters（过滤模板内容）
   ↓
6. 保存配置文件
```

### 频率分析原理

**模板内容**（Template Content）:
- 出现频率 ≥ template-threshold
- 例如：导航栏、页脚、固定标题
- 处理方式：生成filter规则，在解析时移除

**独特内容**（Unique Content）:
- 出现频率 ≤ unique-threshold
- 例如：文章正文、数据表格、特定信息
- 处理方式：生成extractor规则，在解析时提取

**中间内容**（Semi-template）:
- 频率介于两个阈值之间
- 例如：部分固定的标题、可选的章节
- 处理方式：根据具体情况决定

---

## 🎨 使用示例

### 示例1：基本分析

```bash
# 分析lixinger-crawler项目
node run-skill.js lixinger-crawler
```

**输出**:
```
=== Template Content Analyzer - Enhanced Runner ===

Project: lixinger-crawler
Template Threshold: 0.8
Unique Threshold: 0.2

Step 1: Locating project directory...
✓ Found: /path/to/output/lixinger-crawler

Step 2: Checking required files...
✓ URL patterns file: url-patterns.json
✓ Pages directory: pages/

Step 3: Creating output directory...
✓ Templates directory: templates/

Step 4: Loading URL patterns...
✓ Loaded 106 URL patterns

Step 5: Running analysis...
[1/106] Analyzing: analytics-chart-maker
  Found 410 files
  ✓ Generated config: 163 extractors, 4093 filters
[2/106] Analyzing: detail-sz
  Found 416 files
  ✓ Generated config: 165 extractors, 4141 filters
...

=== Analysis Complete ===
Total patterns: 106
Success: 106
Skipped: 0
Failed: 0

Statistics:
  - Total templates: 106
  - Total extractors: 17000
  - Total filters: 430000
  - Avg extractors/template: 160.38

✓ All done!
```

### 示例2：严格模板识别

```bash
# 使用更高的阈值，只识别出现频率很高的内容为模板
node run-skill.js lixinger-crawler --template-threshold 0.95
```

**效果**:
- 更少的内容被识别为模板
- 生成更少的filters
- 保留更多的内容

### 示例3：宽松独特内容识别

```bash
# 降低独特内容阈值，识别更多独特内容
node run-skill.js lixinger-crawler --unique-threshold 0.1
```

**效果**:
- 更多的内容被识别为独特
- 生成更多的extractors
- 提取更详细的信息

### 示例4：平衡配置

```bash
# 平衡的配置，适合大多数场景
node run-skill.js lixinger-crawler \
  --template-threshold 0.85 \
  --unique-threshold 0.15
```

---

## 🔧 参数调优指南

### 阈值选择建议

| 场景 | template-threshold | unique-threshold | 说明 |
|------|-------------------|------------------|------|
| 严格模板识别 | 0.9 - 0.95 | 0.1 - 0.15 | 只过滤非常固定的内容 |
| 平衡配置 | 0.8 - 0.85 | 0.15 - 0.2 | 适合大多数场景 |
| 激进过滤 | 0.7 - 0.8 | 0.2 - 0.3 | 过滤更多模板内容 |
| 保守提取 | 0.85 - 0.9 | 0.05 - 0.1 | 只提取非常独特的内容 |

### 调优步骤

1. **初始分析** - 使用默认参数运行
2. **检查结果** - 查看生成的extractors和filters数量
3. **调整阈值** - 根据需求调整参数
4. **验证效果** - 使用样例URL测试
5. **迭代优化** - 重复2-4步直到满意

### 常见问题调优

#### 问题1：生成的filters太多

**原因**: template-threshold太低，很多内容被识别为模板

**解决方案**:
```bash
# 提高template-threshold
node run-skill.js lixinger-crawler --template-threshold 0.9
```

#### 问题2：提取的内容不够

**原因**: unique-threshold太低，很多独特内容未被识别

**解决方案**:
```bash
# 提高unique-threshold
node run-skill.js lixinger-crawler --unique-threshold 0.3
```

#### 问题3：配置文件过大

**原因**: 页面数量多，内容复杂

**解决方案**:
```bash
# 使用更严格的阈值
node run-skill.js lixinger-crawler \
  --template-threshold 0.9 \
  --unique-threshold 0.1
```

---

## 📊 输出统计说明

### 统计指标

- **totalTemplates**: 成功生成配置的模板数量
- **totalExtractors**: 所有模板的提取器总数
- **totalFilters**: 所有模板的过滤器总数
- **totalPages**: 分析的页面总数
- **avgExtractorsPerTemplate**: 平均每个模板的提取器数量
- **avgFiltersPerTemplate**: 平均每个模板的过滤器数量

### 质量评估

**优秀配置**:
- avgExtractorsPerTemplate: 50-200
- avgFiltersPerTemplate: 1000-5000
- 提取器数量适中，能提取关键信息
- 过滤器数量合理，能有效去除模板

**需要优化**:
- avgExtractorsPerTemplate < 10: 提取内容太少
- avgExtractorsPerTemplate > 500: 提取内容太多
- avgFiltersPerTemplate > 10000: 过滤规则过多

---

## 🔍 使用生成的配置

### 加载配置

```javascript
const fs = require('fs');
const path = require('path');

// 1. 加载汇总文件
const summaryPath = 'output/lixinger-crawler/templates/template-summary.json';
const summary = JSON.parse(fs.readFileSync(summaryPath, 'utf-8'));

console.log(`Total templates: ${summary.totalTemplates}`);

// 2. 加载特定模板
const templateName = 'analytics-chart-maker';
const templatePath = `output/lixinger-crawler/templates/${templateName}.json`;
const templateConfig = JSON.parse(fs.readFileSync(templatePath, 'utf-8'));

console.log(`Extractors: ${templateConfig.extractors.length}`);
console.log(`Filters: ${templateConfig.filters.length}`);
```

### 使用TemplateParser

```javascript
const TemplateParser = require('./lib/template-parser');

// 创建解析器
const parser = new TemplateParser();

// 解析页面
const markdownContent = fs.readFileSync('page.md', 'utf-8');
const result = parser.parse(markdownContent, templateConfig);

// 获取独特内容
console.log('Unique content:', result.uniqueContent);
console.log('Filtered blocks:', result.filteredBlocks);
```

---

## 🎓 最佳实践

### 1. 准备工作

- 确保有足够的样本页面（建议 ≥ 10个）
- 页面应该是同一模板的不同实例
- 页面内容应该已经是markdown格式

### 2. 参数选择

- 首次运行使用默认参数
- 根据结果调整阈值
- 记录最佳参数配置

### 3. 结果验证

- 检查生成的extractors是否合理
- 验证filters是否过滤了正确的内容
- 使用样例URL测试效果

### 4. 配置管理

- 将templates目录纳入版本控制
- 定期更新配置
- 保留历史版本以便回滚

### 5. 性能优化

- 对于大型项目，考虑分批处理
- 使用更严格的阈值减少配置大小
- 定期清理不再使用的配置

---

## 🐛 故障排除

### 问题1：找不到项目目录

**错误信息**:
```
Error: 找不到项目目录: lixinger-crawler
```

**解决方案**:
- 确保在正确的目录运行脚本
- 检查output目录是否存在
- 使用完整路径

### 问题2：没有匹配的文件

**错误信息**:
```
⚠ No matching files, skipped
```

**原因**: URL模式与markdown文件名不匹配

**解决方案**:
- 检查pages目录中的文件名
- 确认URL模式是否正确
- 查看文件名生成规则

### 问题3：内存不足

**错误信息**:
```
JavaScript heap out of memory
```

**解决方案**:
```bash
# 增加Node.js内存限制
NODE_OPTIONS="--max-old-space-size=4096" node run-skill.js lixinger-crawler
```

### 问题4：分析速度慢

**原因**: 页面数量多，内容复杂

**解决方案**:
- 使用更高的阈值减少处理量
- 考虑分批处理
- 使用更快的硬盘（SSD）

---

## 📚 相关文档

- [OUTPUT_STRUCTURE.md](./OUTPUT_STRUCTURE.md) - 输出结构详细说明
- [README.md](./README.md) - 项目概述
- [docs/USAGE_GUIDE.md](./docs/USAGE_GUIDE.md) - 详细使用指南
- [docs/API.md](./docs/API.md) - API文档
- [docs/CONFIG_FORMAT.md](./docs/CONFIG_FORMAT.md) - 配置格式说明

---

## 🤝 贡献

欢迎提交Issue和Pull Request！

---

## 📄 许可证

MIT License

---

**版本**: 2.0.0  
**更新时间**: 2026-02-26  
**维护者**: Template Analyzer Team
