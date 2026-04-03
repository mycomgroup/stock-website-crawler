---
id: "url-12774569"
type: "api"
title: "Symbol Search"
url: "https://eulerpool.com/developers/api/screener/search"
description: "Search for stocks, ETFs, and other securities by name, ticker, or ISIN"
source: ""
tags: []
crawl_time: "2026-03-18T05:51:05.412Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/screener/search/{query}"
  responses:
    - {"code":"200","description":"Search results (max 20)"}
    - {"code":"401","description":"Invalid or missing API key"}
    - {"code":"404","description":"Resource not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/screener/search/Apple' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"type\": \"stock\",\n  \"name\": \"Apple\",\n  \"isin\": \"US0378331005\",\n  \"ticker\": \"AAPL\",\n  \"wkn\": \"string\",\n  \"currency\": \"USD\",\n  \"country\": \"US\",\n  \"industry\": \"string\",\n  \"marketcap\": 0\n}\n]"
  suggestedFilename: "screener_search"
---

# Symbol Search

## 源URL

https://eulerpool.com/developers/api/screener/search

## 描述

Search for stocks, ETFs, and other securities by name, ticker, or ISIN

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/screener/search/{query}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Search results (max 20) |
| 401 | Invalid or missing API key |
| 404 | Resource not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/screener/search/Apple' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "type": "stock",
  "name": "Apple",
  "isin": "US0378331005",
  "ticker": "AAPL",
  "wkn": "string",
  "currency": "USD",
  "country": "US",
  "industry": "string",
  "marketcap": 0
}
]
```

## 文档正文

Search for stocks, ETFs, and other securities by name, ticker, or ISIN

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/screener/search/{query}`
