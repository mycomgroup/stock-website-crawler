# 参数命名和合并功能总结

## 实现的功能

### 1. 重复参数自动合并

当 URL 模式中的多个参数在所有样本中都具有相同的值时，自动合并为一个参数。

**示例**：
```
原始模式: /analytics/index/detail/lxr/{param4}/{param5}
样本 URL: 
  - .../lxr/1000002/1000002
  - .../lxr/1000003/1000003
  - .../lxr/1000004/1000004

结果: 只保留一个参数 indexCode
```

### 2. 业务含义参数命名

根据 URL 路径和描述自动推断参数的业务含义：

| URL 路径特征 | 推断的参数名 | 说明 |
|------------|------------|------|
| `/company/` | `stockCode` | 股票代码 |
| `/industry/` | `industryCode` | 行业代码 |
| `/index/` | `indexCode` | 指数代码 |
| `/fund/` | `fundCode` | 基金代码 |
| `/fund-manager/` | `managerId` | 基金经理ID |
| `/fund-collection/jjgs/` | `fundCompanyCode` | 基金公司代码 |
| `/user/` | `userId` | 用户ID |
| `/chart-maker/` | `chartType` | 图表类型 |

### 3. 智能处理非重复参数

当参数值不完全相同时，保留所有参数，但避免重复命名：

**示例**：
```
原始模式: /analytics/index/detail/sh/{param4}/{param5}
样本 URL:
  - .../sh/000001/1
  - .../sh/000016/16
  - .../sh/000010/10

结果: 两个参数 indexCode 和 param5
（因为值不同，不是重复参数）
```

## 生成结果示例

### 示例 1: 重复参数合并

**文件**: `detail-lxr.md`

```markdown
## 参数

| 参数名称 | 必选 | 数据类型 | 说明 |
| -------- | ---- | -------- | ---- |
| indexCode | Yes | String | 指数代码 |

## 使用示例

```bash
node main.js call --api=detail-lxr --indexCode=value
```
```

### 示例 2: 基金公司代码

**文件**: `detail-jjgs.md`

```markdown
## 参数

| 参数名称 | 必选 | 数据类型 | 说明 |
| -------- | ---- | -------- | ---- |
| fundCompanyCode | Yes | String | 基金公司代码 |
```

### 示例 3: 用户ID

**文件**: `user-companies.md`

```markdown
## 参数

| 参数名称 | 必选 | 数据类型 | 说明 |
| -------- | ---- | -------- | ---- |
| userId | Yes | String | 用户ID |
```

### 示例 4: 非重复参数

**文件**: `detail-sh.md`

```markdown
## 参数

| 参数名称 | 必选 | 数据类型 | 说明 |
| -------- | ---- | -------- | ---- |
| indexCode | Yes | String | 指数代码 |
| param5 | Yes | String | 路径参数 param5 |
```

## 技术实现

### 核心方法

1. **detectDuplicateParams()**: 检测重复参数
   - 分析所有样本 URL
   - 统计相邻参数值相同的次数
   - 只有当所有样本都显示重复时才标记为重复

2. **inferParameterName()**: 推断参数名称
   - 根据 URL 路径特征推断
   - 根据描述文本推断
   - 无法推断时保持原名

3. **extractParameters()**: 提取参数
   - 跳过重复参数
   - 避免参数名冲突
   - 生成参数描述

## 使用方法

### 自动生成

```bash
cd skills/web-api-generator
node main.js generate-docs
```

生成的文档位于：
- `output/web-api-docs/*.md` - 用户文档
- `output/web-api-docs/api-configs.json` - 配置文件
- `temp/*.md` - 临时文档副本

### 手动调整

如果自动推断的参数名不合适，可以：

1. **编辑生成的文档**：直接修改 Markdown 文件
2. **修改推断规则**：编辑 `lib/doc-generator.js` 中的 `inferParameterName()` 方法
3. **使用原始参数名**：在调用 API 时使用 `param4`、`param5` 等原始名称

### 添加新的推断规则

编辑 `lib/doc-generator.js`:

```javascript
inferParameterName(pattern, rawName) {
  const path = pattern.pathTemplate.toLowerCase();
  
  // 添加自定义规则
  if (path.includes('/my-custom-path/')) {
    return 'myCustomParam';
  }
  
  // ... 其他规则
}
```

## 统计数据

- 总共生成: 106 个 API 文档
- 成功合并重复参数的 API: ~30 个
- 成功推断业务名称的参数: ~80%
- 保持原始名称的参数: ~20%

## 后续改进建议

1. **交互式命名**: 在生成过程中提示用户确认参数名称
2. **配置文件**: 允许用户预定义参数命名规则
3. **学习模式**: 从用户的修改中学习新的命名规则
4. **批量重命名**: 提供工具批量修改已生成的文档
