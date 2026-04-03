---
id: "url-166dff12"
type: "api"
title: "Commodity Quotes API"
url: "https://eulerpool.com/developers/api/commodity/quotes"
description: "Returns historical price data for a commodity"
source: ""
tags: []
crawl_time: "2026-03-18T05:55:03.084Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/commodity/quotes/{ticker}"
  responses:
    - {"code":"200","description":"Returns commodity price history"}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Commodity not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/commodity/quotes/XAU?startdate=1704067200000&enddate=1735689600000' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"timestamp\": 1705276800000,\n  \"price\": 2045.5\n}\n]"
  suggestedFilename: "commodity_quotes"
---

# Commodity Quotes API

## 源URL

https://eulerpool.com/developers/api/commodity/quotes

## 描述

Returns historical price data for a commodity

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/commodity/quotes/{ticker}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns commodity price history |
| 401 | Token not valid |
| 404 | Commodity not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/commodity/quotes/XAU?startdate=1704067200000&enddate=1735689600000' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "timestamp": 1705276800000,
  "price": 2045.5
}
]
```

## 文档正文

Returns historical price data for a commodity

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/commodity/quotes/{ticker}`
