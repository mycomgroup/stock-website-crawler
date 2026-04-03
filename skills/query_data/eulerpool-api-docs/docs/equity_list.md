---
id: "url-6ab95233"
type: "api"
title: "List All Stocks API"
url: "https://eulerpool.com/developers/api/equity/list"
description: "Returns a paginated list of all stocks sorted by market capitalization descending. Use offset and limit for pagination. Comparable to Finnhub /stock/symbol."
source: ""
tags: []
crawl_time: "2026-03-18T05:42:43.663Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/equity/list"
  responses:
    - {"code":"200","description":"Returns paginated stock list."}
    - {"code":"401","description":"Token not valid"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/equity/list?offset=0&limit=10' \\\n  -H 'Accept: application/json'"
  jsonExample: "{\n  \"offset\": 0,\n  \"limit\": 100,\n  \"total\": 35000,\n  \"results\": {\n    \"isin\": \"US0378331005\",\n    \"ticker\": \"AAPL\",\n    \"name\": \"Apple\",\n    \"sector\": \"Technology\",\n    \"wkn\": \"865985\"\n  }\n}"
  suggestedFilename: "equity_list"
---

# List All Stocks API

## 源URL

https://eulerpool.com/developers/api/equity/list

## 描述

Returns a paginated list of all stocks sorted by market capitalization descending. Use offset and limit for pagination. Comparable to Finnhub /stock/symbol.

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/equity/list`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns paginated stock list. |
| 401 | Token not valid |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/equity/list?offset=0&limit=10' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
{
  "offset": 0,
  "limit": 100,
  "total": 35000,
  "results": {
    "isin": "US0378331005",
    "ticker": "AAPL",
    "name": "Apple",
    "sector": "Technology",
    "wkn": "865985"
  }
}
```

## 文档正文

Returns a paginated list of all stocks sorted by market capitalization descending. Use offset and limit for pagination. Comparable to Finnhub /stock/symbol.

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/equity/list`
