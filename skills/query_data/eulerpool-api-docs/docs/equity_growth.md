---
id: "url-665d8de4"
type: "api"
title: "Growth Metrics API"
url: "https://eulerpool.com/developers/api/equity/growth"
description: "Returns compound annual growth rates (3Y, 5Y, 10Y) for revenue, net income, EBIT, dividends, and EPS"
source: ""
tags: []
crawl_time: "2026-03-18T05:46:23.011Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/equity/growth/{identifier}"
  responses:
    - {"code":"200","description":"Returns growth data"}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Security not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/equity/growth/{identifier}' \\\n  -H 'Accept: application/json'"
  jsonExample: "{\n  \"isin\": \"US0378331005\",\n  \"income3Y\": 12.5,\n  \"income5Y\": 0,\n  \"income10Y\": 0,\n  \"revenue3Y\": 0,\n  \"revenue5Y\": 0,\n  \"revenue10Y\": 0,\n  \"ebit3Y\": 0,\n  \"ebit5Y\": 0,\n  \"ebit10Y\": 0\n}"
  suggestedFilename: "equity_growth"
---

# Growth Metrics API

## 源URL

https://eulerpool.com/developers/api/equity/growth

## 描述

Returns compound annual growth rates (3Y, 5Y, 10Y) for revenue, net income, EBIT, dividends, and EPS

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/equity/growth/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns growth data |
| 401 | Token not valid |
| 404 | Security not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/equity/growth/{identifier}' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
{
  "isin": "US0378331005",
  "income3Y": 12.5,
  "income5Y": 0,
  "income10Y": 0,
  "revenue3Y": 0,
  "revenue5Y": 0,
  "revenue10Y": 0,
  "ebit3Y": 0,
  "ebit5Y": 0,
  "ebit10Y": 0
}
```

## 文档正文

Returns compound annual growth rates (3Y, 5Y, 10Y) for revenue, net income, EBIT, dividends, and EPS

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/equity/growth/{identifier}`
