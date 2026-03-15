# API 配置文件格式

## 概述

配置文件定义了每个 API 的输入参数和输出格式。

## 格式

### JSON 格式 (api-configs.json)

```json
[
  {
    "api": "constituents-list",
    "description": "申万2021行业行业详情页 - 成分股数据",
    "pathTemplate": "/analytics/industry/detail/sw_2021/{param4}/{param5}/constituents/list",
    "pattern": "^https://www\\.lixinger\\.com/analytics/industry/detail/sw_2021/([^/]+)/([^/]+)/constituents/list$",
    "parameters": [
      {
        "name": "param4",
        "required": true,
        "type": "String",
        "description": "路径参数 param4"
      },
      {
        "name": "param5",
        "required": true,
        "type": "String",
        "description": "路径参数 param5"
      }
    ],
    "queryParams": [],
    "outputFormat": "csv",
    "dataExtraction": {
      "tables": "primary",
      "charts": false,
      "images": false,
      "mainContent": false
    },
    "samples": [
      "https://www.lixinger.com/analytics/industry/detail/sw_2021/480301/480301/constituents/list",
      "https://www.lixinger.com/analytics/industry/detail/sw_2021/480401/480401/constituents/list"
    ]
  },
  {
    "api": "detail-sh",
    "description": "上海证券交易所公司详情页",
    "pathTemplate": "/analytics/company/detail/sh/{param4}/{param5}",
    "pattern": "^https://www\\.lixinger\\.com/analytics/company/detail/sh/([^/]+)/([^/]+)(\\?.*)?$",
    "parameters": [
      {
        "name": "param4",
        "required": true,
        "type": "String",
        "description": "路径参数 param4"
      },
      {
        "name": "param5",
        "required": true,
        "type": "String",
        "description": "路径参数 param5"
      }
    ],
    "queryParams": ["from-my-followed"],
    "outputFormat": "md",
    "dataExtraction": {
      "tables": "all",
      "charts": true,
      "images": true,
      "mainContent": true
    },
    "samples": [
      "https://www.lixinger.com/analytics/company/detail/sh/605056/605056",
      "https://www.lixinger.com/analytics/company/detail/sh/688687/688687"
    ]
  }
]
```

### JSONL 格式 (api-configs.jsonl)

每行一个 JSON 对象：

```jsonl
{"api":"constituents-list","description":"申万2021行业行业详情页 - 成分股数据","outputFormat":"csv",...}
{"api":"detail-sh","description":"上海证券交易所公司详情页","outputFormat":"md",...}
```

## 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| api | String | API 名称（唯一标识） |
| description | String | API 描述 |
| pathTemplate | String | URL 路径模板 |
| pattern | String | URL 正则表达式 |
| parameters | Array | 参数列表 |
| queryParams | Array | 查询参数列表 |
| outputFormat | String | 输出格式：`csv` 或 `md` |
| dataExtraction | Object | 数据提取配置 |
| samples | Array | 示例 URL |

### outputFormat 规则

- **csv**: 纯数据表格，如成分股列表、股东列表、估值数据等
- **md**: 详情页面，包含多种内容类型（表格、图表、文本等）

### dataExtraction 配置

```json
{
  "tables": "primary" | "all",  // primary: 只提取主表格, all: 提取所有表格
  "charts": true | false,        // 是否提取图表
  "images": true | false,        // 是否提取图片
  "mainContent": true | false    // 是否提取主要内容
}
```

## 输出示例

### CSV 格式输出

```json
{
  "success": true,
  "api": "constituents-list",
  "url": "https://www.lixinger.com/...",
  "outputFormat": "csv",
  "data": {
    "type": "csv",
    "title": "成分股列表",
    "tables": [
      {
        "headers": ["股票代码", "股票名称", "权重"],
        "rows": [
          ["600519", "贵州茅台", "10.5%"],
          ["000858", "五粮液", "8.2%"]
        ],
        "csv": "股票代码,股票名称,权重\n600519,贵州茅台,10.5%\n000858,五粮液,8.2%"
      }
    ]
  }
}
```

### MD 格式输出

```json
{
  "success": true,
  "api": "detail-sh",
  "url": "https://www.lixinger.com/...",
  "outputFormat": "md",
  "data": {
    "type": "md",
    "title": "贵州茅台(600519)",
    "description": "公司详情",
    "tables": [...],
    "charts": 5,
    "images": 3,
    "mainContent": [...]
  }
}
```

## 自动判断规则

generate-docs.js 会根据以下规则自动判断输出格式：

### CSV 关键词
- list, 列表
- constituents, 成分股
- shareholders, 股东
- fund-list, 基金列表
- valuation, 估值
- fundamental, 基本面

### MD 关键词
- detail, 详情
- doc, 文档
- profile, 简介
- chart-maker, 图表

## 自定义配置

你可以手动编辑 `api-configs.json` 来调整输出格式：

```json
{
  "api": "my-custom-api",
  "outputFormat": "csv",  // 改为 csv
  "dataExtraction": {
    "tables": "primary",  // 只提取主表格
    "charts": false,
    "images": false,
    "mainContent": false
  }
}
```

## 使用配置

```bash
# 使用默认配置
node main.js call --api=constituents-list --param4=480301 --param5=480301

# 指定配置文件
node main.js call \
  --api=constituents-list \
  --param4=480301 \
  --param5=480301 \
  --config=./custom-configs.json

# 指定输出文件
node main.js call \
  --api=constituents-list \
  --param4=480301 \
  --param5=480301 \
  --output=./data/constituents.csv
```
