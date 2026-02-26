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
- **1.4.0** (2026-02-26): 质量检查和迭代优化
  - 添加质量检查脚本
  - 支持反复优化工作流
  - 添加智能拆分参数

## 质量检查和迭代优化

### 工作流程

1. **初次分析**: 使用默认参数生成初步结果
2. **质量检查**: 运行验证脚本发现问题
3. **调整参数**: 根据检查结果优化参数
4. **重新分析**: 使用新参数再次分析
5. **重复2-4**: 直到质量满意

### 质量检查规则

运行质量检查脚本：
```bash
node scripts/validate-patterns.js ../../stock-crawler/output/lixinger-crawler/url-patterns.json
```

#### 检查规则列表

1. **过大簇检查** (warning)
   - 检查是否有URL数量 > 500 的模式
   - 可能混合了不同类型的页面
   - 建议: 使用 `--try-refine-top-n` 或 `--strict-top-n` 参数

2. **样本一致性检查** (error)
   - 检查样本URL的路径深度是否一致
   - 不一致说明混合了不同结构
   - 建议: 增加细分参数

3. **重复名称检查** (warning)
   - 检查是否有相同名称的模式
   - 应该进一步细分或合并
   - 建议: 调整细分参数

4. **过度泛化检查** (warning)
   - 检查路径模板参数占比是否过高（>70%）
   - 模板过于泛化可能不准确
   - 建议: 增加路径匹配严格度

5. **不一致段检查** (error)
   - 检查样本中是否有半固定段（2-5个不同值）
   - 应该按这些值细分
   - 建议: 增加 `--refine-max-values` 参数

6. **模式数量检查** (info)
   - 检查模式总数是否在合理范围
   - <1000 URLs: 应该 <50 个模式
   - 1000-5000 URLs: 应该 <100 个模式
   - 5000-10000 URLs: 应该 <150 个模式
   - >10000 URLs: 应该 <200 个模式

7. **覆盖率检查** (warning)
   - 检查分类覆盖率是否 >90%
   - 覆盖率低说明很多URL未分类
   - 建议: 降低 `--min-group-size` 参数

8. **主导簇检查** (warning)
   - 检查最大模式是否占比 >30%
   - 占比过高可能需要细分
   - 建议: 使用 `--try-refine-top-n` 参数

### 迭代优化示例

#### 示例1: 发现大簇问题

```bash
# 第1次分析
node run-skill.js lixinger-crawler

# 质量检查
node scripts/validate-patterns.js ../../stock-crawler/output/lixinger-crawler/url-patterns.json

# 输出: ⚠️ 模式 "analytics-chart-maker" 包含 923 个URL

# 第2次分析 - 尝试拆分大簇
node run-skill.js lixinger-crawler --try-refine-top-n 10

# 再次检查
node scripts/validate-patterns.js ../../stock-crawler/output/lixinger-crawler/url-patterns.json
```

#### 示例2: 发现样本不一致

```bash
# 质量检查发现问题
# 输出: ❌ 模式 "detail-sz" 的样本URL路径深度不一致

# 使用更激进的细分
node run-skill.js lixinger-crawler \
  --refine-max-values 12 \
  --refine-min-count 5 \
  --strict-top-n 10

# 验证结果
node scripts/validate-patterns.js ../../stock-crawler/output/lixinger-crawler/url-patterns.json
```

#### 示例3: 模式数量过多

```bash
# 质量检查
# 输出: ℹ️ 模式数量 150 可能过多

# 增加最小分组大小
node run-skill.js lixinger-crawler --min-group-size 20

# 验证结果
node scripts/validate-patterns.js ../../stock-crawler/output/lixinger-crawler/url-patterns.json
```

### AI 使用建议

作为 AI，你应该：

1. **自动运行质量检查**: 每次分析后自动运行验证脚本
2. **解读检查结果**: 理解每个警告和错误的含义
3. **生成优化方案**: 根据问题提出具体的参数调整
4. **反复迭代**: 最多尝试3-5次，找到最佳配置
5. **记录过程**: 在报告中说明优化过程和最终选择

### 质量标准

**优秀** (可以停止迭代):
- ✅ 无错误
- ✅ 警告 ≤ 2个
- ✅ 覆盖率 > 95%
- ✅ 最大簇 < 500 个URL
- ✅ 模式数量在合理范围

**良好** (可选继续优化):
- ✅ 无错误
- ⚠️ 警告 3-5个
- ✅ 覆盖率 > 90%
- ⚠️ 最大簇 < 1000 个URL

**需要优化** (必须继续):
- ❌ 有错误
- ⚠️ 警告 > 5个
- ❌ 覆盖率 < 90%
- ❌ 最大簇 > 1000 个URL

## 相关文档

- [README.md](./README.md) - 详细使用说明
- [质量检查工作流](./docs/guides/QUALITY_CHECK_WORKFLOW.md) - 反复优化指南 ⭐ 重要
- [实用调优指南](./docs/guides/PRACTICAL_GUIDE.md) - 参数调优技巧
- [价值导向分析](./docs/knowledge/VALUE_FOCUSED_ANALYSIS.md) - 业务价值分析
- [lib/url-clusterer.js](./lib/url-clusterer.js) - 聚类算法实现
- [lib/report-generator.js](./lib/report-generator.js) - 报告生成器
- [scripts/validate-patterns.js](./scripts/validate-patterns.js) - 质量检查脚本

## 技术特点

1. **智能聚类**: 基于URL结构相似度自动分组
2. **正则生成**: 自动生成匹配规则
3. **高性能**: 支持分析8000+URL，耗时<10秒
4. **灵活配置**: 支持多种参数调整
5. **双格式输出**: JSON（机器可读）+ Markdown（人类可读）
