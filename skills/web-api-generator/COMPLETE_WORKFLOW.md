# 完整工作流

## 概述

生成完整的 API 配置需要三个步骤：

1. **生成基础配置** - 从 url-patterns.json 生成 API 文档和基础配置
2. **分析数据选择器** - 访问实际页面，分析核心数据块的选择器
3. **合并配置** - 将选择器合并到配置文件中

## 步骤 1: 生成基础配置

```bash
cd skills/web-api-generator

# 生成 API 文档和基础配置
node main.js generate-docs

# 输出文件:
# - output/web-api-docs/README.md
# - output/web-api-docs/api-configs.json (基础配置)
# - output/web-api-docs/*.md (用户文档)
```

生成的基础配置示例：

```json
{
  "api": "constituents-list",
  "description": "成分股列表",
  "outputFormat": "csv",
  "dataSelectors": {
    "primaryTable": null,  // 待填充
    "primaryTableXPath": null,  // 待填充
    "allTables": [],  // 待填充
    "mainContent": "main",
    "dataContainers": []  // 待填充
  }
}
```

## 步骤 2: 分析数据选择器

```bash
# 分析所有 API 的数据选择器（需要登录）
node scripts/analyze-data-selectors.js

# 或者只分析前 5 个（用于测试）
node scripts/analyze-data-selectors.js --limit=5

# 或者只分析特定 API
node scripts/analyze-data-selectors.js --apis=detail-sh,constituents-list

# 输出文件:
# - output/data-selectors.json
```

这个脚本会：
1. 登录理杏仁
2. 访问每个 API 的示例 URL
3. 分析页面结构
4. 提取表格、主内容区域、数据容器的选择器

生成的选择器配置示例：

```json
{
  "api": "constituents-list",
  "url": "https://www.lixinger.com/analytics/industry/detail/sw_2021/480301/480301/constituents/list",
  "dataSelectors": {
    "primaryTable": "table.data-table",
    "primaryTableXPath": "//*[@id='main-table']",
    "allTables": [
      {
        "selector": "table.data-table",
        "xpath": "//*[@id='main-table']",
        "headers": ["股票代码", "股票名称", "权重"]
      }
    ],
    "mainContent": "main",
    "mainContentXPath": "//main",
    "dataContainers": [".data-container", "#table-wrapper"]
  },
  "analysis": {
    "tableCount": 1,
    "hasMainContent": true,
    "dataContainerCount": 2
  }
}
```

## 步骤 3: 合并配置

```bash
# 合并选择器到配置文件
node scripts/merge-selectors.js \
  --configs=./output/web-api-docs/api-configs.json \
  --selectors=./output/data-selectors.json \
  --output=./output/web-api-docs/api-configs-complete.json

# 输出文件:
# - output/web-api-docs/api-configs-complete.json (完整配置)
```

最终的完整配置：

```json
{
  "api": "constituents-list",
  "description": "成分股列表",
  "outputFormat": "csv",
  "dataSelectors": {
    "primaryTable": "table.data-table",
    "primaryTableXPath": "//*[@id='main-table']",
    "allTables": [
      {
        "selector": "table.data-table",
        "xpath": "//*[@id='main-table']",
        "headers": ["股票代码", "股票名称", "权重"]
      }
    ],
    "mainContent": "main",
    "mainContentXPath": "//main",
    "dataContainers": [".data-container", "#table-wrapper"]
  }
}
```

## 步骤 4: 使用完整配置

```bash
# 使用完整配置调用 API
node main.js call \
  --api=constituents-list \
  --config=./output/web-api-docs/api-configs-complete.json \
  --param4=480301 \
  --param5=480301
```

web-api-client.js 会使用配置中的选择器来精确提取数据。

## 一键运行

创建脚本 `generate-complete-config.sh`:

```bash
#!/bin/bash

echo "步骤 1: 生成基础配置..."
node main.js generate-docs

echo ""
echo "步骤 2: 分析数据选择器（前 10 个）..."
node scripts/analyze-data-selectors.js --limit=10

echo ""
echo "步骤 3: 合并配置..."
node scripts/merge-selectors.js

echo ""
echo "✓ 完成！完整配置已生成："
echo "  output/web-api-docs/api-configs-complete.json"
```

运行：
```bash
chmod +x generate-complete-config.sh
./generate-complete-config.sh
```

## 增量更新

如果只想更新特定 API 的选择器：

```bash
# 1. 分析特定 API
node scripts/analyze-data-selectors.js \
  --apis=detail-sh,constituents-list \
  --output=./output/data-selectors-partial.json

# 2. 手动合并或使用脚本
node scripts/merge-selectors.js \
  --configs=./output/web-api-docs/api-configs-complete.json \
  --selectors=./output/data-selectors-partial.json \
  --output=./output/web-api-docs/api-configs-complete.json
```

## 配置文件说明

### 基础配置 (api-configs.json)
- 从 url-patterns.json 自动生成
- 包含 API 基本信息、参数、输出格式
- 选择器字段为空

### 选择器配置 (data-selectors.json)
- 通过访问实际页面分析生成
- 包含 CSS 选择器和 XPath
- 包含分析统计信息

### 完整配置 (api-configs-complete.json)
- 合并了基础配置和选择器
- 可直接用于 web-api-client.js
- 包含所有必要信息

## 注意事项

1. **登录要求**: analyze-data-selectors.js 需要登录，确保 .env 文件配置正确
2. **速率限制**: 分析会访问实际页面，建议使用 --limit 参数测试
3. **选择器稳定性**: 页面结构变化可能导致选择器失效，需要重新分析
4. **增量更新**: 可以只更新部分 API 的选择器

## 故障排除

### 问题 1: 分析失败

```bash
# 检查登录
node scripts/analyze-data-selectors.js --apis=detail-sh --limit=1

# 查看详细错误
node scripts/analyze-data-selectors.js --apis=detail-sh 2>&1 | tee error.log
```

### 问题 2: 选择器不准确

手动编辑 `data-selectors.json`，调整选择器：

```json
{
  "api": "my-api",
  "dataSelectors": {
    "primaryTable": "table.my-custom-class",  // 修改为正确的选择器
    "primaryTableXPath": "//*[@id='my-table']"
  }
}
```

### 问题 3: 合并失败

检查文件路径和格式：

```bash
# 验证 JSON 格式
cat output/web-api-docs/api-configs.json | jq '.'
cat output/data-selectors.json | jq '.'
```

## 下一步

1. 生成完整配置
2. 测试几个 API 调用
3. 根据需要调整选择器
4. 集成到你的项目中
