# 模板生成工作流程指南

## 概述

本指南介绍如何使用配置驱动的方式生成HTML提取模板，避免频繁修改代码。

## 核心理念

1. **配置驱动**：所有参数通过配置文件控制
2. **先测试后批量**：先生成少量模板验证效果
3. **页面分类**：根据页面类型使用不同配置
4. **迭代优化**：根据效果调整配置参数

## 完整工作流程

### 阶段1：准备和探索（1-2个模板）

#### 1.1 查看可用配置

```bash
cd skills/html-template-generator

# 查看所有配置文件
ls -la config/

# 可用配置：
# - default.json       默认配置
# - quick-test.json    快速测试（2样本，可见浏览器）
# - production.json    生产环境（5样本，严格）
# - detail-pages.json  详情页优化
# - list-pages.json    列表页优化
# - table-pages.json   表格页优化
```

#### 1.2 生成第一个模板并预览

使用 `quick-test.json` 配置快速测试：

```bash
node scripts/generate-and-test.js api-doc \
  --input ../../stock-crawler/output/lixinger-crawler/url-patterns.json \
  --output-dir ../../stock-crawler/output/lixinger-crawler/templates \
  --preview-dir ../../stock-crawler/output/lixinger-crawler/previews \
  --config config/quick-test.json
```

**输出**：
- `templates/api-doc.json` - 模板文件
- `previews/api-doc.md` - 预览Markdown

#### 1.3 检查预览效果

```bash
# 打开预览文件
cat ../../stock-crawler/output/lixinger-crawler/previews/api-doc.md

# 或使用编辑器
code ../../stock-crawler/output/lixinger-crawler/previews/api-doc.md
```

**检查清单**：
- [ ] 标题是否正确提取？
- [ ] 表格格式是否完整？
- [ ] 列表项是否正确？
- [ ] 是否包含不需要的内容（广告、导航）？
- [ ] 是否缺少重要内容？

### 阶段2：分类和调整（根据页面类型）

根据预览效果，判断页面类型并选择合适的配置。

#### 2.1 识别页面类型

| 页面类型 | 特征 | 推荐配置 |
|---------|------|---------|
| **列表页** | 多个相似项目、搜索结果、产品列表 | `list-pages.json` |
| **详情页** | 单个内容、文章详情、API文档 | `detail-pages.json` |
| **表格页** | 大量表格数据、财务报表、参数说明 | `table-pages.json` |
| **混排页** | 多种内容类型、首页、仪表板 | `default.json` |

#### 2.2 使用对应配置重新生成

**示例：API文档页（详情页）**

```bash
node scripts/generate-and-test.js api-doc \
  --input ../../stock-crawler/output/lixinger-crawler/url-patterns.json \
  --output-dir ../../stock-crawler/output/lixinger-crawler/templates \
  --preview-dir ../../stock-crawler/output/lixinger-crawler/previews \
  --config config/detail-pages.json
```

**示例：公司列表页（列表页）**

```bash
node scripts/generate-and-test.js company-list \
  --input ../../stock-crawler/output/lixinger-crawler/url-patterns.json \
  --output-dir ../../stock-crawler/output/lixinger-crawler/templates \
  --preview-dir ../../stock-crawler/output/lixinger-crawler/previews \
  --config config/list-pages.json
```

**示例：财务数据页（表格页）**

```bash
node scripts/generate-and-test.js financial-data \
  --input ../../stock-crawler/output/lixinger-crawler/url-patterns.json \
  --output-dir ../../stock-crawler/output/lixinger-crawler/templates \
  --preview-dir ../../stock-crawler/output/lixinger-crawler/previews \
  --config config/table-pages.json
```

### 阶段3：参数微调（根据具体问题）

如果预设配置效果不理想，通过命令行参数微调。

#### 3.1 常见问题和解决方案

**问题1：提取内容不完整**

原因：频率阈值太高，某些元素被过滤

解决：降低频率阈值

```bash
node scripts/generate-and-test.js api-doc \
  --input url-patterns.json \
  --output-dir output/templates \
  --preview-dir output/previews \
  --config config/detail-pages.json \
  --frequency-threshold 0.6  # 从0.8降到0.6
```

**问题2：包含太多噪音（广告、导航等）**

原因：过滤规则不够

解决：创建自定义配置文件

```json
// config/my-custom.json
{
  "description": "自定义配置 - 增强过滤",
  "filters": {
    "removeSelectors": [
      "nav", "header", "footer", "aside",
      ".sidebar", ".ad", ".advertisement",
      ".related-articles", ".comments",
      "[class*='banner']", "[id*='promo']"
    ]
  }
}
```

使用自定义配置：

```bash
node scripts/generate-and-test.js api-doc \
  --input url-patterns.json \
  --output-dir output/templates \
  --preview-dir output/previews \
  --config config/my-custom.json
```

**问题3：表格提取不正确**

原因：表格结构复杂（合并单元格、多级表头）

解决：使用表格页配置

```bash
node scripts/generate-and-test.js financial-table \
  --input url-patterns.json \
  --output-dir output/templates \
  --preview-dir output/previews \
  --config config/table-pages.json
```

**问题4：动态加载内容未提取**

原因：页面加载后需要等待JavaScript渲染

解决：增加等待时间

```bash
node scripts/generate-and-test.js dynamic-page \
  --input url-patterns.json \
  --output-dir output/templates \
  --preview-dir output/previews \
  --wait-time 5000  # 等待5秒
```

**问题5：样本页面差异大**

原因：样本数量少或页面结构不一致

解决：增加样本数量

```bash
node scripts/generate-and-test.js varied-pages \
  --input url-patterns.json \
  --output-dir output/templates \
  --preview-dir output/previews \
  --max-samples 10  # 增加到10个样本
```

#### 3.2 创建项目专用配置

根据调试结果，创建项目专用配置文件：

```json
// config/lixinger-api.json
{
  "description": "理杏仁API文档页面专用配置",
  
  "fetching": {
    "maxSamples": 5,
    "waitTime": 3000,
    "waitForSelector": ".api-content"
  },
  
  "analysis": {
    "frequencyThreshold": 0.7,
    "detectPageType": true
  },
  
  "pageTypes": {
    "detail": {
      "extraction": {
        "focusOnMainContent": true,
        "extractFullHierarchy": true
      }
    }
  },
  
  "filters": {
    "removeSelectors": [
      "nav", "aside", ".sidebar",
      ".related-links", "[class*='ad']"
    ]
  },
  
  "patterns": {
    "include": ["api-*", "doc-*"]
  }
}
```

### 阶段4：批量生成（确认效果后）

确认配置效果良好后，批量生成所有模板。

#### 4.1 按页面类型分批生成

**生成所有API文档页**

```bash
node scripts/batch-generate-with-config.js \
  --input ../../stock-crawler/output/lixinger-crawler/url-patterns.json \
  --output-dir ../../stock-crawler/output/lixinger-crawler/templates \
  --config config/detail-pages.json \
  --include-patterns "api-*,doc-*"
```

**生成所有列表页**

```bash
node scripts/batch-generate-with-config.js \
  --input ../../stock-crawler/output/lixinger-crawler/url-patterns.json \
  --output-dir ../../stock-crawler/output/lixinger-crawler/templates \
  --config config/list-pages.json \
  --include-patterns "*-list,*-index,search-*"
```

**生成所有表格页**

```bash
node scripts/batch-generate-with-config.js \
  --input ../../stock-crawler/output/lixinger-crawler/url-patterns.json \
  --output-dir ../../stock-crawler/output/lixinger-crawler/templates \
  --config config/table-pages.json \
  --include-patterns "*-data,*-report,*-stats"
```

#### 4.2 按优先级生成

先生成最重要的模板：

```bash
node scripts/batch-generate-with-config.js \
  --input ../../stock-crawler/output/lixinger-crawler/url-patterns.json \
  --output-dir ../../stock-crawler/output/lixinger-crawler/templates \
  --config config/production.json \
  --priority-patterns "api-doc,detail-sh,detail-sz,company-profile"
```

#### 4.3 分段生成（避免一次性处理太多）

```bash
# 生成前20个
node scripts/batch-generate-with-config.js \
  --input url-patterns.json \
  --output-dir output/templates \
  --config config/production.json \
  --limit 20

# 生成第21-40个
node scripts/batch-generate-with-config.js \
  --input url-patterns.json \
  --output-dir output/templates \
  --config config/production.json \
  --start-from 20 \
  --limit 20

# 生成第41个开始的所有
node scripts/batch-generate-with-config.js \
  --input url-patterns.json \
  --output-dir output/templates \
  --config config/production.json \
  --start-from 40
```

#### 4.4 排除测试和备份模板

```bash
node scripts/batch-generate-with-config.js \
  --input url-patterns.json \
  --output-dir output/templates \
  --config config/production.json \
  --exclude-patterns "*-test,*-backup,*-old"
```

### 阶段5：验证和优化

#### 5.1 批量验证生成的模板

创建验证脚本：

```bash
#!/bin/bash
# validate-templates.sh

TEMPLATES_DIR="../../stock-crawler/output/lixinger-crawler/templates"
PREVIEWS_DIR="../../stock-crawler/output/lixinger-crawler/previews"

for template in $TEMPLATES_DIR/*.json; do
  name=$(basename "$template" .json)
  echo "Validating $name..."
  
  # 检查文件大小
  size=$(wc -c < "$template")
  if [ $size -lt 100 ]; then
    echo "  ⚠️  Warning: Template too small ($size bytes)"
  fi
  
  # 检查JSON格式
  if ! jq empty "$template" 2>/dev/null; then
    echo "  ❌ Error: Invalid JSON"
  else
    echo "  ✅ Valid"
  fi
done
```

#### 5.2 抽查预览效果

随机抽查几个模板的预览效果：

```bash
# 为随机5个模板生成预览
for template in $(ls templates/*.json | shuf -n 5); do
  name=$(basename "$template" .json)
  node scripts/test-render-template.js "$template" \
    > "previews/${name}.md"
done
```

#### 5.3 记录问题模板

创建问题清单：

```bash
# problem-templates.txt
api-doc-v2: 表格提取不完整，需要调整frequencyThreshold
company-list: 包含太多广告，需要增加过滤规则
financial-data: 复杂表头处理不正确，需要使用table-pages配置
```

#### 5.4 重新生成问题模板

```bash
# 使用调整后的配置重新生成
node scripts/generate-and-test.js api-doc-v2 \
  --input url-patterns.json \
  --output-dir output/templates \
  --preview-dir output/previews \
  --frequency-threshold 0.6
```

## 配置文件速查表

| 配置文件 | 适用场景 | 关键参数 |
|---------|---------|---------|
| `default.json` | 通用场景 | threshold=0.8, samples=5 |
| `quick-test.json` | 快速测试 | threshold=0.5, samples=2, headless=false |
| `production.json` | 生产环境 | threshold=0.8, samples=5, retry=5 |
| `detail-pages.json` | 详情页/文章页 | focusOnMainContent=true |
| `list-pages.json` | 列表页/索引页 | focusOnItems=true, minItemCount=3 |
| `table-pages.json` | 表格页/数据页 | focusOnTables=true, handleComplexHeaders=true |

## 命令速查表

### 单个模板生成和测试

```bash
# 基本用法
node scripts/generate-and-test.js <template-name> \
  --input <patterns-file> \
  --output-dir <templates-dir> \
  --preview-dir <previews-dir>

# 使用配置文件
node scripts/generate-and-test.js <template-name> \
  --input <patterns-file> \
  --output-dir <templates-dir> \
  --preview-dir <previews-dir> \
  --config config/<config-file>

# 覆盖参数
node scripts/generate-and-test.js <template-name> \
  --input <patterns-file> \
  --output-dir <templates-dir> \
  --preview-dir <previews-dir> \
  --config config/<config-file> \
  --frequency-threshold 0.6 \
  --max-samples 3
```

### 批量生成

```bash
# 基本批量生成
node scripts/batch-generate-with-config.js \
  --input <patterns-file> \
  --output-dir <templates-dir>

# 使用配置文件
node scripts/batch-generate-with-config.js \
  --input <patterns-file> \
  --output-dir <templates-dir> \
  --config config/<config-file>

# 过滤模式
node scripts/batch-generate-with-config.js \
  --input <patterns-file> \
  --output-dir <templates-dir> \
  --include-patterns "api-*,detail-*" \
  --exclude-patterns "*-test"

# 分段处理
node scripts/batch-generate-with-config.js \
  --input <patterns-file> \
  --output-dir <templates-dir> \
  --start-from 20 \
  --limit 10
```

## 最佳实践

1. **始终先测试**：使用 `generate-and-test.js` 测试1-2个模板
2. **保存配置**：为不同项目创建专用配置文件
3. **版本控制**：将配置文件纳入Git管理
4. **文档化**：在配置文件中添加 `description` 说明
5. **渐进调整**：每次只调整1-2个参数
6. **分类处理**：按页面类型使用不同配置
7. **批量验证**：生成后抽查验证效果
8. **记录问题**：维护问题模板清单

## 故障排查

### 配置不生效

1. 检查配置文件路径是否正确
2. 验证JSON格式：`jq empty config/my-config.json`
3. 确认命令行参数拼写正确

### 提取效果不理想

1. 降低 `frequencyThreshold`（0.8 → 0.6）
2. 增加 `maxSamples`（5 → 10）
3. 调整 `filters.removeSelectors`
4. 使用对应页面类型的配置

### 生成速度慢

1. 减少 `maxSamples`（5 → 2）
2. 使用 `--limit` 分批处理
3. 使用 `--include-patterns` 限制范围

### 浏览器问题

1. 检查Chrome是否安装
2. 验证 `userDataDir` 路径
3. 尝试 `--headless false` 查看浏览器行为

## 总结

通过配置驱动的方式，你可以：

1. ✅ 无需修改代码，只调整配置参数
2. ✅ 按页面类型使用不同策略
3. ✅ 先测试后批量，确保质量
4. ✅ 灵活过滤和优先级控制
5. ✅ 快速迭代和优化

记住：**先测试1-2个模板，确认效果后再批量生成！**
