---
id: "url-52a10a03"
type: "api"
title: "Stock Search API"
url: "https://eulerpool.com/developers/api/equity/search"
description: "Search for stocks, ETFs, and crypto by name, ticker, or ISIN. Uses full-text search with typo tolerance. Comparable to Finnhub /search."
source: ""
tags: []
crawl_time: "2026-03-18T05:46:03.096Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/equity/search"
  responses:
    - {"code":"200","description":"Returns matching securities."}
    - {"code":"400","description":"Missing query parameter"}
    - {"code":"401","description":"Token not valid"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/equity/search?q=Apple' \\\n  -H 'Accept: application/json'"
  jsonExample: "{\n  \"count\": 5,\n  \"results\": {\n    \"name\": \"Apple Inc.\",\n    \"isin\": \"US0378331005\",\n    \"ticker\": \"AAPL\",\n    \"type\": \"stock\",\n    \"currency\": \"USD\"\n  }\n}"
  suggestedFilename: "equity_search"
---

# Stock Search API

## 源URL

https://eulerpool.com/developers/api/equity/search

## 描述

Search for stocks, ETFs, and crypto by name, ticker, or ISIN. Uses full-text search with typo tolerance. Comparable to Finnhub /search.

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/equity/search`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns matching securities. |
| 400 | Missing query parameter |
| 401 | Token not valid |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/equity/search?q=Apple' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
{
  "count": 5,
  "results": {
    "name": "Apple Inc.",
    "isin": "US0378331005",
    "ticker": "AAPL",
    "type": "stock",
    "currency": "USD"
  }
}
```

## 文档正文

Search for stocks, ETFs, and crypto by name, ticker, or ISIN. Uses full-text search with typo tolerance. Comparable to Finnhub /search.

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/equity/search`
