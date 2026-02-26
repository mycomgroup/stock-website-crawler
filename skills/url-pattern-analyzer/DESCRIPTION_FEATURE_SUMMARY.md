# URL模式中文描述功能总结

## 功能概述

为URL Pattern Analyzer添加了自动生成详细中文描述的功能，让每个URL模式都有清晰易懂的说明。

## 主要特性

### 1. 自动描述生成

在生成URL模式时，自动为每个模式生成详细的中文描述，包括：
- 市场信息（上海证券交易所、深圳证券交易所等）
- 资产类型（公司、基金、指数、行业等）
- 页面类型（详情页、数据看板、列表页等）
- 数据类型（基本面数据、估值数据、资金流向等）
- 子类型详情（PEG估值指标、DCF估值、成本分析等）

### 2. JSON结构优化

```json
{
  "name": "fundamental-peg",
  "description": "公司详情页 - 基本面数据(PEG估值指标)",
  "pathTemplate": "/analytics/company/detail/{market}/{code}/fundamental/peg",
  "pattern": "...",
  "queryParams": [...],
  "urlCount": 123,
  "samples": [...]
}
```

description字段紧跟在name后面，方便阅读。

### 3. 报告展示

#### 模式分布表格
```
| 排名 | 模式名称 | 中文描述 | URL数量 | 占比 | 路径模板 |
|------|----------|----------|---------|------|----------|
| 1 | analytics-chart-maker | 图表制作工具 - 用于创建和管理自定义数据图表 | 923 | 10.97% | ... |
| 2 | detail-sz | 深圳证券交易所公司详情页 | 751 | 8.93% | ... |
```

#### 详情展示
```markdown
### 1. analytics-chart-maker

**描述**: 图表制作工具 - 用于创建和管理自定义数据图表

- **URL数量**: 923 (10.97%)
- **路径模板**: `/analytics/chart-maker/{param2}`
...
```

## 描述示例

### 基础模式
- `detail-sz` → "深圳证券交易所公司详情页"
- `detail-sh` → "上海证券交易所公司详情页"
- `detail-nasdaq` → "纳斯达克公司详情页"

### 数据类型模式
- `sh-followed-users` → "上海证券交易所公司详情页 - 关注用户列表"
- `csi-fund-list` → "中证指数指数详情页 - 基金列表"
- `constituents-list` → "申万2021行业行业详情页 - 成分股数据"

### 基本面数据模式
- `fundamental-peg` → "公司详情页 - 基本面数据(PEG估值指标)"
- `fundamental-dcf` → "公司详情页 - 基本面数据(DCF现金流折现估值)"
- `fundamental-profit` → "公司详情页 - 基本面数据(盈利能力分析)"
- `fundamental-growth` → "公司详情页 - 基本面数据(成长性指标)"
- `fundamental-cashflow` → "公司详情页 - 基本面数据(现金流分析)"

### 估值数据模式
- `valuation-primary` → "申万2021行业行业详情页 - 基本面数据(估值分析)"
- `valuation-fitting` → "上海证券交易所基金详情页 - 估值数据(估值拟合分析)"

### 资金流向模式
- `capital-flow-mutual-market` → "上海证券交易所公司详情页 - 财务数据(主要财务指标)"
- `capital-flow-mutual-market` → "公司详情页 - 资金流向数据(沪深港通资金流)"

### 用户相关模式
- `user-companies` → "用户关注的公司列表"
- `user-discussions` → "用户发表的讨论帖子"
- `user-memo` → "用户的个人备忘录"

### 工具类模式
- `analytics-chart-maker` → "图表制作工具 - 用于创建和管理自定义数据图表"
- `api-doc` → "开放API文档 - API接口说明和使用指南"
- `open-api` → "开放API服务 - 提供数据接口访问"

## 技术实现

### 1. 描述生成逻辑

位于 `lib/report-generator.js` 的 `_generateDescription()` 方法：

```javascript
_generateDescription(pattern) {
  // 1. 解析路径段
  const segments = pathTemplate.split('/').filter(s => s && !s.startsWith('{'));
  
  // 2. 识别市场
  if (pathTemplate.includes('/sh/')) market = '上海证券交易所';
  
  // 3. 识别资产类型
  if (segments.includes('company')) assetType = '公司';
  
  // 4. 识别数据类型和子类型
  if (segments.includes('fundamental')) {
    dataType = '基本面数据';
    if (name.includes('peg')) subType = 'PEG估值指标';
  }
  
  // 5. 组合描述
  return `${market}${assetType}${pageType} - ${dataType}(${subType})`;
}
```

### 2. 独立脚本

`scripts/add-descriptions.js` - 可以为已有的JSON文件添加描述：

```bash
node add-descriptions.js url-patterns.json url-patterns-with-desc.json
```

### 3. 自动集成

在主流程中自动调用，无需额外操作：

```bash
node run-skill.js lixinger-crawler
```

生成的JSON和报告都会自动包含中文描述。

## 使用场景

1. **快速理解URL模式** - 通过描述快速了解每个模式的业务含义
2. **文档生成** - 自动生成的报告包含详细说明，无需手动编写
3. **数据分析** - 根据描述筛选和分类URL模式
4. **爬虫配置** - 根据描述设置不同类型页面的爬取策略
5. **团队协作** - 清晰的描述让团队成员快速理解URL结构

## 配置和扩展

### 添加新的翻译规则

在 `_generateDescription()` 方法中添加新的识别逻辑：

```javascript
// 识别新的数据类型
if (segments.includes('new-data-type')) {
  dataType = '新数据类型';
  if (name.includes('sub-type')) subType = '子类型说明';
}
```

### 自定义描述格式

修改描述组合逻辑：

```javascript
// 自定义格式
if (market && assetType && dataType) {
  description = `【${market}】${assetType} | ${dataType}`;
}
```

## 优势

1. **自动化** - 无需手动编写描述，自动生成
2. **一致性** - 所有描述遵循统一的格式和规则
3. **详细性** - 包含完整的业务信息，易于理解
4. **可扩展** - 易于添加新的识别规则和翻译
5. **多语言** - 可以轻松扩展支持其他语言

## 未来改进

1. 支持多语言描述（英文、日文等）
2. 从样本URL中提取更多上下文信息
3. 使用机器学习优化描述生成
4. 支持自定义描述模板
5. 添加描述质量评分

---

**版本**: 1.0  
**更新时间**: 2026-02-26  
**作者**: URL Pattern Analyzer Team
