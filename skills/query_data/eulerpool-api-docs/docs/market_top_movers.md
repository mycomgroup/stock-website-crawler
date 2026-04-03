---
id: "url-698ea7ca"
type: "api"
title: "Top Gainers & Losers"
url: "https://eulerpool.com/developers/api/market/top/movers"
description: "Returns stocks with the largest positive and negative daily price changes"
source: ""
tags: []
crawl_time: "2026-03-18T06:00:00.783Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/market/top-movers"
  responses:
    - {"code":"200","description":"Top gainers and losers"}
    - {"code":"401","description":"Invalid or missing API key"}
    - {"code":"404","description":"Resource not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/market/top-movers?country=US&limit=20' \\\n  -H 'Accept: application/json'"
  jsonExample: "{\n  \"gainers\": {\n    \"isin\": \"string\",\n    \"ticker\": \"string\",\n    \"name\": \"string\",\n    \"price\": 0,\n    \"change\": 0,\n    \"changePct\": 0\n  },\n  \"losers\": {\n    \"isin\": \"string\",\n    \"ticker\": \"string\",\n    \"name\": \"string\",\n    \"price\": 0,\n    \"change\": 0,\n    \"changePct\": 0\n  }\n}"
  suggestedFilename: "market_top_movers"
---

# Top Gainers & Losers

## 源URL

https://eulerpool.com/developers/api/market/top/movers

## 描述

Returns stocks with the largest positive and negative daily price changes

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/market/top-movers`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Top gainers and losers |
| 401 | Invalid or missing API key |
| 404 | Resource not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/market/top-movers?country=US&limit=20' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
{
  "gainers": {
    "isin": "string",
    "ticker": "string",
    "name": "string",
    "price": 0,
    "change": 0,
    "changePct": 0
  },
  "losers": {
    "isin": "string",
    "ticker": "string",
    "name": "string",
    "price": 0,
    "change": 0,
    "changePct": 0
  }
}
```

## 文档正文

Returns stocks with the largest positive and negative daily price changes

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/market/top-movers`
