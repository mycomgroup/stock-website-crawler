---
id: "url-7c59db01"
type: "api"
title: "Index Constituents"
url: "https://eulerpool.com/developers/api/index/constituents"
description: "Returns companies in a stock market index (S&P 500, DAX, etc.)"
source: ""
tags: []
crawl_time: "2026-03-18T05:31:43.555Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/index/constituents/{id}"
  responses:
    - {"code":"200","description":"Companies in the index"}
    - {"code":"401","description":"Invalid or missing API key"}
    - {"code":"404","description":"Resource not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/index/constituents/sp500?start=0&end=500' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"isin\": \"US0378331005\",\n  \"ticker\": \"AAPL\",\n  \"name\": \"Apple\",\n  \"country\": \"US\",\n  \"sector\": \"Technology\",\n  \"industry\": \"Consumer Electronics\",\n  \"mcap\": 0\n}\n]"
  suggestedFilename: "index_constituents"
---

# Index Constituents

## 源URL

https://eulerpool.com/developers/api/index/constituents

## 描述

Returns companies in a stock market index (S&P 500, DAX, etc.)

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/index/constituents/{id}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Companies in the index |
| 401 | Invalid or missing API key |
| 404 | Resource not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/index/constituents/sp500?start=0&end=500' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "isin": "US0378331005",
  "ticker": "AAPL",
  "name": "Apple",
  "country": "US",
  "sector": "Technology",
  "industry": "Consumer Electronics",
  "mcap": 0
}
]
```

## 文档正文

Returns companies in a stock market index (S&P 500, DAX, etc.)

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/index/constituents/{id}`
