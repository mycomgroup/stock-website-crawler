# URL Pattern Analyzer Skill

## 基本信息

- **名称**: url-pattern-analyzer
- **版本**: 1.0.0
- **类型**: analyzer
- **入口**: main.js
- **描述**: 从links.txt文件中分析URL模式并生成模式报告

## 功能说明

这个skill可以：
- 自动识别URL中的模式（路径结构、参数规律）
- 将相似的URL自动分组（聚类）
- 生成正则表达式匹配规则
- 输出JSON和Markdown格式的分析报告

## 输入参数

### 必需参数

| 参数名 | 类型 | 说明 | 示例 |
|--------|------|------|------|
| `linksFile` | string | links.txt文件路径 | `stock-crawler/output/lixinger-crawler/links.txt` |
| `outputFile` | string | 输出JSON文件路径 | `stock-crawler/output/lixinger-crawler/url-patterns.json` |

### 可选参数

| 参数名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `minGroupSize` | number | 5 | 最小分组大小（过滤掉URL数量少于此值的模式） |
| `sampleCount` | number | 5 | 每个模式的示例URL数量 |
| `markdown` | boolean | false | 是否同时生成Markdown报告 |

## 输出结果

### 返回对象

```json
{
  "success": true,
  "patternsFile": "path/to/url-patterns.json",
  "patternCount": 10,
  "totalUrls": 8403,
  "patterns": [...]
}
```

### 输出文件

1. **JSON报告** (`url-patterns.json`):
   - 包含所有识别的URL模式
   - 每个模式的正则表达式
   - 示例URL列表
   - 统计信息

2. **Markdown报告** (`url-patterns.md`, 可选):
   - 可读性更好的分析报告
   - 包含统计图表
   - 详细的模式说明

## 使用方式

### 方式1: 命令行直接运行

```bash
# 基本使用
node main.js <linksFile> <outputFile>

# 生成Markdown报告
node main.js <linksFile> <outputFile> --markdown

# 自定义参数
node main.js <linksFile> <outputFile> --min-group-size 10 --sample-count 3
```

### 方式2: 通过项目名运行（推荐）

使用 `run-skill.js` 脚本，只需提供项目名：

```bash
# 在skills/url-pattern-analyzer目录下
node run-skill.js lixinger-crawler

# 自定义参数
node run-skill.js lixinger-crawler --min-group-size 10 --max-patterns 20
```

### 方式3: 在Kiro中使用

```
"分析 lixinger-crawler 项目的URL模式"
"使用url-pattern-analyzer分析URL，最小分组10个"
```

## 参数调优建议

### minGroupSize（最小分组大小）

- **默认值**: 5
- **建议值**:
  - 小型网站（<1000个URL）: 3-5
  - 中型网站（1000-5000个URL）: 5-10
  - 大型网站（>5000个URL）: 10-20
- **作用**: 过滤掉URL数量太少的模式，减少噪音

### sampleCount（示例数量）

- **默认值**: 5
- **建议值**: 3-10
- **作用**: 控制每个模式显示多少个示例URL

### maxPatterns（最大模式数）

- **默认值**: 无限制
- **建议值**: 20-50
- **作用**: 只保留URL数量最多的前N个模式

## 输出报告说明

### 统计信息

报告会包含以下统计信息：

1. **总体统计**
   - 总URL数量
   - 识别的模式数量
   - 分析耗时

2. **每个模式的统计**
   - 模式名称
   - 路径模板
   - 正则表达式
   - URL数量和占比
   - 查询参数列表
   - 示例URL

3. **质量指标**
   - 覆盖率（被分类的URL占比）
   - 平均每个模式的URL数量
   - 最大/最小模式的URL数量

## 示例输出

### JSON格式

```json
{
  "summary": {
    "totalUrls": 8403,
    "patternCount": 15,
    "analyzedAt": "2026-02-26T13:00:00.000Z"
  },
  "patterns": [
    {
      "name": "api-doc",
      "pathTemplate": "/open/api/doc",
      "pattern": "^https://www\\.lixinger\\.com/open/api/doc\\?api-key=(.+)$",
      "queryParams": ["api-key"],
      "urlCount": 163,
      "percentage": 1.94,
      "samples": [
        "https://www.lixinger.com/open/api/doc?api-key=cn/company",
        "https://www.lixinger.com/open/api/doc?api-key=hk/index"
      ]
    }
  ]
}
```

### Markdown格式

```markdown
# URL Pattern Analysis Report

## Summary

- Total URLs: 8,403
- Patterns Identified: 15
- Analysis Time: 2026-02-26 13:00:00

## Top Patterns

### 1. api-doc (163 URLs, 1.94%)

- Path Template: `/open/api/doc`
- Pattern: `^https://www\.lixinger\.com/open/api/doc\?api-key=(.+)$`
- Query Params: api-key

**Sample URLs:**
1. https://www.lixinger.com/open/api/doc?api-key=cn/company
2. https://www.lixinger.com/open/api/doc?api-key=hk/index
```

## 依赖项

无外部依赖，使用Node.js内置模块。

## 关键词

- url-analysis
- pattern-recognition
- clustering
- web-crawler

## 版本历史

- **1.0.0** (2026-02-26): 初始版本
  - URL模式识别和聚类
  - JSON和Markdown报告生成
  - 性能优化（支持8000+URL）

## 相关文档

- [README.md](./README.md) - 详细使用说明
- [lib/url-clusterer.js](./lib/url-clusterer.js) - 聚类算法实现
- [lib/report-generator.js](./lib/report-generator.js) - 报告生成器

## 技术特点

1. **智能聚类**: 基于URL结构相似度自动分组
2. **正则生成**: 自动生成匹配规则
3. **高性能**: 支持分析8000+URL，耗时<10秒
4. **灵活配置**: 支持多种参数调整
5. **双格式输出**: JSON（机器可读）+ Markdown（人类可读）
