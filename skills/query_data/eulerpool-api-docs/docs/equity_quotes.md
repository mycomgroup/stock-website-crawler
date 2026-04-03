---
id: "url-5522de34"
type: "api"
title: "Quote API"
url: "https://eulerpool.com/developers/api/equity/quotes"
description: "Returns the quotes for the given Identifier (ISIN or Crypto Symbol) and timeframe. Dates are in milliseconds since 1970."
source: ""
tags: []
crawl_time: "2026-03-18T05:45:23.282Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/equity/quotes/{identifier}"
  responses:
    - {"code":"200","description":"Returns quotes for the given ISIN in the given timeframe (default is 1 year)"}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Security not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/equity/quotes/{identifier}?startdate=1704067200000&enddate=1735689600000' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {\n  \"timestamp\": 1732621245000,\n  \"price\": 123.23\n}\n]"
  suggestedFilename: "equity_quotes"
---

# Quote API

## 源URL

https://eulerpool.com/developers/api/equity/quotes

## 描述

Returns the quotes for the given Identifier (ISIN or Crypto Symbol) and timeframe. Dates are in milliseconds since 1970.

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/equity/quotes/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns quotes for the given ISIN in the given timeframe (default is 1 year) |
| 401 | Token not valid |
| 404 | Security not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/equity/quotes/{identifier}?startdate=1704067200000&enddate=1735689600000' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
[
  {
  "timestamp": 1732621245000,
  "price": 123.23
}
]
```

## 文档正文

Returns the quotes for the given Identifier (ISIN or Crypto Symbol) and timeframe. Dates are in milliseconds since 1970.

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/equity/quotes/{identifier}`
