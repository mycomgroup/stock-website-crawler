---
id: "url-22ff9553"
type: "api"
title: "Fair Value"
url: "https://eulerpool.com/developers/api/fair/value/by/isin"
description: "Returns the computed fair value for a stock by identifier"
source: ""
tags: []
crawl_time: "2026-03-18T06:01:00.126Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/fair-value/by-isin/{identifier}"
  responses:
    - {"code":"200","description":"Fair value data"}
    - {"code":"401","description":"Invalid or missing API key"}
    - {"code":"404","description":"Resource not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/fair-value/by-isin/{identifier}' \\\n  -H 'Accept: application/json'"
  jsonExample: "{\n  \"isin\": \"US0378331005\",\n  \"fairValue\": 185.5,\n  \"lastPrice\": 178.72,\n  \"upside\": 3.79\n}"
  suggestedFilename: "fair_value_by_isin"
---

# Fair Value

## 源URL

https://eulerpool.com/developers/api/fair/value/by/isin

## 描述

Returns the computed fair value for a stock by identifier

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/fair-value/by-isin/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Fair value data |
| 401 | Invalid or missing API key |
| 404 | Resource not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/fair-value/by-isin/{identifier}' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
{
  "isin": "US0378331005",
  "fairValue": 185.5,
  "lastPrice": 178.72,
  "upside": 3.79
}
```

## 文档正文

Returns the computed fair value for a stock by identifier

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/fair-value/by-isin/{identifier}`
