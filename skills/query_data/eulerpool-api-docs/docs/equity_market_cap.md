---
id: "url-3a2eaeac"
type: "api"
title: "Historical Market Cap API"
url: "https://eulerpool.com/developers/api/equity/market/cap"
description: "Returns daily historical market capitalization computed from share price × shares outstanding. Available for up to 5 years of history."
source: ""
tags: []
crawl_time: "2026-03-18T05:59:01.395Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/equity/market-cap/{identifier}"
  responses:
    - {"code":"200","description":"Returns daily market cap time series."}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Security not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/equity/market-cap/{identifier}' \\\n  -H 'Accept: application/json'"
  jsonExample: "{\n  \"isin\": \"string\",\n  \"currency\": \"string\",\n  \"sharesOutstanding\": 0,\n  \"data\": {\n    \"timestamp\": 0,\n    \"price\": 0,\n    \"marketCap\": 0\n  }\n}"
  suggestedFilename: "equity_market_cap"
---

# Historical Market Cap API

## 源URL

https://eulerpool.com/developers/api/equity/market/cap

## 描述

Returns daily historical market capitalization computed from share price × shares outstanding. Available for up to 5 years of history.

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/equity/market-cap/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns daily market cap time series. |
| 401 | Token not valid |
| 404 | Security not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/equity/market-cap/{identifier}' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
{
  "isin": "string",
  "currency": "string",
  "sharesOutstanding": 0,
  "data": {
    "timestamp": 0,
    "price": 0,
    "marketCap": 0
  }
}
```

## 文档正文

Returns daily historical market capitalization computed from share price × shares outstanding. Available for up to 5 years of history.

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/equity/market-cap/{identifier}`
