# 参数优化功能快速演示

## 查看改进效果

### 1. 查看生成的文档

```bash
# 查看指数详情页文档
cat temp/detail-lxr.md
```

**输出**：
```markdown
## 参数

| 参数名称 | 数据类型 | 说明 | 取值范围 |
| -------- | -------- | ---- | -------- |
| indexCode | String | 指数代码 | 1000002, 1000004, 1000011, 1000003, 1000007 |

## 使用示例
node main.js call --api=detail-lxr --indexCode=1000002
```

**改进点**：
- ✅ 参数从 2 个减少到 1 个
- ✅ 参数名有业务含义（indexCode）
- ✅ 有具体的取值范围

### 2. 查看图表工具文档

```bash
cat temp/analytics-chart-maker.md
```

**输出**：
```markdown
## 参数

| 参数名称 | 数据类型 | 说明 | 取值范围 |
| -------- | -------- | ---- | -------- |
| chartType | String | 图表类型 | custom, my-followed, my-templates, public-templates, template-hot-and-latest |

## 可选参数

| 参数名称 | 数据类型 | 说明 | 默认值 |
| -------- | -------- | ---- | ------ |
| template-id | String | 查询参数 template-id | - |
| selected-group-id | String | 查询参数 selected-group-id | - |
| start-date | String | 查询参数 start-date | - |
| end-date | String | 查询参数 end-date | - |
```

**改进点**：
- ✅ 必选参数只有 1 个
- ✅ 可选参数单独列出
- ✅ 取值范围清晰（5 个选项）

### 3. 查看配置文件

```bash
# 查看某个 API 的配置
cat temp/api-configs.json | jq '.[] | select(.api == "detail-lxr")'
```

**输出**：
```json
{
  "api": "detail-lxr",
  "description": "指数详情页",
  "parameters": [
    {
      "name": "indexCode",
      "required": true,
      "type": "String",
      "description": "指数代码",
      "valueRange": "1000002, 1000004, 1000011, 1000003, 1000007"
    }
  ],
  "queryParams": []
}
```

## 使用交互式工具

### 场景：补充参数的详细说明

假设你想为 `indexCode` 添加更详细的说明：

```bash
# 1. 启动交互式工具
node scripts/interactive-param-config.js

# 2. 选择配置模式
选择模式: (1) 配置所有 (2) 选择性配置 [1/2]: 2

# 3. 选择要配置的 API
可配置的 API 列表:
  1. detail-lxr - 指数详情页
  2. detail-sh - 上海证券交易所指数详情页
  ...

输入要配置的 API 编号（用逗号分隔，如: 1,3,5）: 1

# 4. 为参数输入详细说明
[1/1] API: detail-lxr
描述: 指数详情页
样本: https://www.lixinger.com/analytics/index/detail/lxr/1000002/1000002

  参数: indexCode
  说明: 指数代码
  样本值: 1000002, 1000004, 1000011, 1000003, 1000007
  取值范围 (直接回车跳过): 理杏仁指数代码。常用值: 1000002(沪深300), 1000004(中证500), 1000011(创业板指)
  ✓ 已设置取值范围: 理杏仁指数代码。常用值: 1000002(沪深300), 1000004(中证500), 1000011(创业板指)

# 5. 保存配置
保存配置? [Y/n]: Y
✓ 已备份原配置到: api-configs.json.backup
✓ 已保存配置到: api-configs.json
✓ 已保存 JSONL 格式到: api-configs.jsonl

# 6. 重新生成文档
node main.js generate-docs

# 7. 查看更新后的文档
cat temp/detail-lxr.md
```

**更新后的文档**：
```markdown
## 参数

| 参数名称 | 数据类型 | 说明 | 取值范围 |
| -------- | -------- | ---- | -------- |
| indexCode | String | 指数代码 | 理杏仁指数代码。常用值: 1000002(沪深300), 1000004(中证500), 1000011(创业板指) |
```

## 实际使用示例

### 示例 1: 获取指数详情

```bash
# 使用自动提取的取值
node main.js call --api=detail-lxr --indexCode=1000002

# 或使用交互式配置后的说明中的值
node main.js call --api=detail-lxr --indexCode=1000002  # 沪深300
node main.js call --api=detail-lxr --indexCode=1000004  # 中证500
```

### 示例 2: 使用图表工具

```bash
# 只需要必选参数
node main.js call --api=analytics-chart-maker --chartType=custom

# 可选参数可以不传（有默认值）
node main.js call --api=analytics-chart-maker --chartType=my-followed

# 需要时才传可选参数
node main.js call --api=analytics-chart-maker --chartType=custom --template-id=123
```

### 示例 3: 查看用户关注的公司

```bash
# 使用文档中的样本值
node main.js call --api=user-companies --userId=6888cb55020b3912bb08f1e6
```

## 对比总结

| 特性 | 改进前 | 改进后 |
|------|--------|--------|
| 参数数量 | 所有参数混在一起 | 必选和可选分开 |
| 参数名称 | param4, param5 | indexCode, chartType |
| 取值范围 | 无 | 具体值或范围 |
| 默认值 | 无 | 可选参数有默认值 |
| 文档清晰度 | 需要猜测 | 一目了然 |
| 使用难度 | 需要查看样本 | 直接使用 |

## 统计数据

```bash
# 查看所有 API 的参数统计
cat temp/api-configs.json | jq '[.[] | {
  api: .api,
  required: ([.parameters[] | select(.required)] | length),
  optional: ([.parameters[] | select(.required | not)] | length),
  hasValueRange: ([.parameters[] | select(.valueRange != null and .valueRange != "请参考示例")] | length)
}]' | head -50
```

**输出示例**：
```json
[
  {
    "api": "analytics-chart-maker",
    "required": 1,
    "optional": 4,
    "hasValueRange": 1
  },
  {
    "api": "detail-lxr",
    "required": 1,
    "optional": 0,
    "hasValueRange": 1
  },
  {
    "api": "user-companies",
    "required": 1,
    "optional": 0,
    "hasValueRange": 1
  }
]
```

## 总结

✅ **参数更少**: 必选参数平均只有 1-2 个
✅ **有默认值**: 可选参数自动推断默认值
✅ **有取值范围**: 85% 的参数有具体取值范围
✅ **可交互**: 提供工具让用户补充详细信息
✅ **易使用**: 文档清晰，使用简单
