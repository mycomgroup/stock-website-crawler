---
id: "url-f862917"
type: "api"
title: "Ticker and Trends API"
url: "https://eulerpool.com/developers/api/trends/ticker/trends"
description: "Returns the current values for specific symbols."
source: ""
tags: []
crawl_time: "2026-03-18T05:34:11.374Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/trends/ticker-trends/{symbol}"
  responses:
    - {"code":"200","description":"Returns the trend state representation of the requested values. If symbol=all the return value will be an array of the given model/example."}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/trends/ticker-trends/all' \\\n  -H 'Accept: application/json'"
  jsonExample: "{\n  \"previousDayQuote\": 2.3,\n  \"lastQuote\": 2.5,\n  \"currentQuote\": 3.1,\n  \"rate\": 3.1,\n  \"currency\": \"EUR\",\n  \"name\": \"Bitcoin\",\n  \"isin\": \"DEXXXXXXXXX\",\n  \"symbol\": \"AAPL\",\n  \"type\": \"etf\"\n}"
  suggestedFilename: "trends_ticker_trends"
---

# Ticker and Trends API

## 源URL

https://eulerpool.com/developers/api/trends/ticker/trends

## 描述

Returns the current values for specific symbols.

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/trends/ticker-trends/{symbol}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns the trend state representation of the requested values. If symbol=all the return value will be an array of the given model/example. |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/trends/ticker-trends/all' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
{
  "previousDayQuote": 2.3,
  "lastQuote": 2.5,
  "currentQuote": 3.1,
  "rate": 3.1,
  "currency": "EUR",
  "name": "Bitcoin",
  "isin": "DEXXXXXXXXX",
  "symbol": "AAPL",
  "type": "etf"
}
```

## 文档正文

Returns the current values for specific symbols.

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/trends/ticker-trends/{symbol}`
