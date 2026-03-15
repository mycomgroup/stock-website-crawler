# Web API Generator Skill

## 功能描述

将 URL patterns 转换为 API 文档和配置，提供命令行客户端进行实时网页抓取。支持交互式配置和手动编辑。

## 核心能力

1. **文档生成**: 从 url-patterns.json 生成类似 REST API 的文档
2. **配置生成**: 生成包含数据选择器的配置文件
3. **交互式配置**: 支持用户查看和调整配置
4. **手动编辑**: 用户可以直接编辑配置文件中的 XPath/选择器
5. **API 客户端**: 像调用 API 一样使用网页抓取
6. **结构化输出**: 返回 CSV 或 JSON 格式的数据

## 工作流程

### 1. 生成初始配置

```bash
node main.js generate-docs
```

生成：
- 用户文档（Markdown）
- 基础配置（JSON），包含 API 信息、参数、输出格式
- 数据选择器字段（初始为空）

**参数优化特性**：
- ✅ 自动检测重复参数并合并
- ✅ 根据 URL 路径推断业务含义
- ✅ 从样本中提取参数取值范围
- ✅ 必选参数和可选参数分开显示
- ✅ 可选参数自动推断默认值

**参数命名规则**：
- 自动检测重复参数（所有样本中值相同的参数）并合并
- 根据 URL 路径推断业务含义：
  - `/company/` → `stockCode`
  - `/industry/` → `industryCode`
  - `/index/` → `indexCode`
  - `/fund/` → `fundCode`
  - `/user/` → `userId`
- 无法推断的参数保持原名（如 `param4`）

**取值范围自动提取**：
- 样本值 ≤ 5 个：直接列出所有值
- 样本值 > 5 个且都是数字：显示数字范围
- 样本值 > 5 个且有共同前缀：显示前缀模式
- 其他情况：显示"多个值"

**参数命名示例**：

```
原始: /analytics/index/detail/lxr/{param4}/{param5}
样本: .../lxr/1000002/1000002
结果: indexCode (合并重复参数)
取值: 1000002, 1000004, 1000011, 1000003, 1000007

原始: /analytics/chart-maker/{param2}
样本: .../chart-maker/custom, .../chart-maker/my-followed
结果: chartType
取值: custom, my-followed, my-templates, public-templates, template-hot-and-latest
```

### 1.5 交互式补充参数信息（可选）

如果自动提取的取值范围不够准确，可以使用交互式工具补充：

```bash
# 交互式配置参数取值范围
node scripts/interactive-param-config.js

# 或指定配置文件
node scripts/interactive-param-config.js ./output/web-api-docs/api-configs.json
```

交互式工具功能：
- 显示需要配置的 API 列表
- 显示每个参数的样本值
- 让用户输入准确的取值范围
- 自动备份原配置文件
- 保存更新后的配置

**交互示例**：
```
[1/10] API: detail-lxr
描述: 指数详情页
样本: https://www.lixinger.com/analytics/index/detail/lxr/1000002/1000002

  参数: indexCode
  说明: 指数代码
  样本值: 1000002, 1000004, 1000011, 1000003, 1000007
  取值范围 (直接回车跳过): 理杏仁指数代码，如 1000002(沪深300), 1000004(中证500)
  ✓ 已设置取值范围: 理杏仁指数代码，如 1000002(沪深300), 1000004(中证500)
```

### 2. 分析数据选择器（可选）

```bash
# 自动分析页面结构
node scripts/analyze-data-selectors.js --limit=5

# 或只分析特定 API
node scripts/analyze-data-selectors.js --apis=detail-sh,constituents-list
```

自动访问页面并提取：
- 表格选择器（CSS 和 XPath）
- 主内容区域选择器
- 数据容器选择器

### 3. 查看和调整配置（交互式）

打开生成的配置文件查看：

```bash
# 查看基础配置
cat output/web-api-docs/api-configs.json | jq '.[0]'

# 查看分析的选择器
cat output/data-selectors.json | jq '.[0]'
```

配置示例：
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
    "dataContainers": [".data-container"]
  }
}
```

### 4. 手动编辑配置

如果自动分析的选择器不准确，直接编辑配置文件：

```bash
# 编辑配置
vim output/web-api-docs/api-configs.json
```

修改示例：
```json
{
  "api": "my-api",
  "dataSelectors": {
    "primaryTable": "table.my-custom-class",  // 改为正确的选择器
    "primaryTableXPath": "//*[@id='my-table']",  // 改为正确的 XPath
    "allTables": [
      {
        "selector": "table:nth-of-type(2)",  // 使用第二个表格
        "xpath": "//table[2]"
      }
    ]
  }
}
```

### 5. 测试配置

```bash
# 使用配置调用 API
node main.js call \
  --api=constituents-list \
  --config=./output/web-api-docs/api-configs.json \
  --param4=480301 \
  --param5=480301
```

查看输出是否正确，如果不对，返回步骤 4 调整配置。

### 6. 合并和保存最终配置

```bash
# 合并选择器到配置
node scripts/merge-selectors.js \
  --configs=./output/web-api-docs/api-configs.json \
  --selectors=./output/data-selectors.json \
  --output=./output/web-api-docs/api-configs-complete.json
```

## 配置文件说明

### 配置文件位置

- `output/web-api-docs/api-configs.json` - 基础配置
- `output/data-selectors.json` - 自动分析的选择器
- `output/web-api-docs/api-configs-complete.json` - 最终完整配置

### 手动编辑指南

#### 1. 修改输出格式

```json
{
  "api": "my-api",
  "outputFormat": "csv"  // 改为 "md" 或 "csv"
}
```

#### 2. 修改表格选择器

```json
{
  "dataSelectors": {
    "primaryTable": "table.my-class",  // CSS 选择器
    "primaryTableXPath": "//*[@id='my-table']"  // XPath
  }
}
```

#### 3. 指定特定表格

```json
{
  "dataSelectors": {
    "primaryTable": "table:nth-of-type(2)",  // 第二个表格
    "primaryTableXPath": "//table[2]"
  }
}
```

#### 4. 添加多个表格

```json
{
  "dataSelectors": {
    "allTables": [
      {
        "selector": "table.table1",
        "xpath": "//*[@id='table1']"
      },
      {
        "selector": "table.table2",
        "xpath": "//*[@id='table2']"
      }
    ]
  }
}
```

## 使用场景

### 场景 1: 快速生成（自动）

```bash
# 1. 生成配置
node main.js generate-docs

# 2. 自动分析选择器
node scripts/analyze-data-selectors.js --limit=10

# 3. 合并
node scripts/merge-selectors.js

# 4. 使用
node main.js call --api=my-api --param4=value
```

### 场景 2: 手动配置（精确）

```bash
# 1. 生成基础配置
node main.js generate-docs

# 2. 手动编辑配置
vim output/web-api-docs/api-configs.json
# 添加你知道的 XPath 和选择器

# 3. 测试
node main.js call --api=my-api --param4=value

# 4. 如果不对，继续调整配置
```

### 场景 3: 混合模式（推荐）

```bash
# 1. 生成配置
node main.js generate-docs

# 2. 自动分析部分 API
node scripts/analyze-data-selectors.js --apis=api1,api2,api3

# 3. 查看结果
cat output/data-selectors.json | jq '.'

# 4. 手动调整不准确的配置
vim output/web-api-docs/api-configs.json

# 5. 测试每个 API
node main.js call --api=api1 --param4=value

# 6. 满意后合并
node scripts/merge-selectors.js
```

## 输入

- url-patterns.json 文件路径
- 登录凭证（用户名、密码）
- API 调用参数
- 数据选择器（可选，可手动编辑）

## 输出

- API 文档（Markdown 格式）
- 配置文件（JSON 格式）
- 结构化数据（CSV 或 JSON 格式）

## 依赖

- Node.js
- Playwright
- 现有的 stock-crawler 组件

## 常见问题

### Q: 参数名称不准确怎么办？

A: 
1. 查看生成的文档，确认参数名称
2. 如果自动推断的名称不合适，可以：
   - 方案 1: 直接编辑生成的 Markdown 文档
   - 方案 2: 修改 `lib/doc-generator.js` 中的 `inferParameterName()` 方法，添加新的推断规则
   - 方案 3: 在调用 API 时使用原始参数名（如 `param4`）

示例：如果 `param5` 应该是 `shortCode`，可以修改推断逻辑：
```javascript
inferParameterName(pattern, rawName) {
  // 添加自定义规则
  if (pattern.pathTemplate.includes('/detail/sh/') && rawName === 'param5') {
    return 'shortCode';
  }
  // ... 其他规则
}
```

### Q: 如何知道正确的 XPath？

A: 
1. 在浏览器中打开页面
2. 右键点击目标元素 → 检查
3. 在开发者工具中右键元素 → Copy → Copy XPath
4. 粘贴到配置文件中

### Q: 自动分析的选择器不准确怎么办？

A: 直接编辑配置文件，修改 `dataSelectors` 字段。

### Q: 如何测试配置是否正确？

A: 使用 `node main.js call` 命令测试，查看输出是否符合预期。

### Q: 可以只配置部分 API 吗？

A: 可以，使用 `--apis` 参数只分析特定 API，其他的手动配置。
