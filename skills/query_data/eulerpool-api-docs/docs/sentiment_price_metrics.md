---
id: "url-6b791758"
type: "api"
title: "Price Metrics API"
url: "https://eulerpool.com/developers/api/sentiment/price/metrics"
description: "Returns price performance statistics including 52-week high/low, moving averages, beta, and YTD return"
source: ""
tags: []
crawl_time: "2026-03-18T06:10:27.964Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/sentiment/price-metrics/{identifier}"
  responses:
    - {"code":"200","description":"Returns price metrics"}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Security not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/sentiment/price-metrics/{identifier}' \\\n  -H 'Accept: application/json'"
  jsonExample: "{\n  \"symbol\": \"AAPL\",\n  \"52WeekHigh\": 199.62,\n  \"52WeekLow\": 124.17,\n  \"10DayAverageTradingVolume\": 53717320,\n  \"beta\": 1.29\n}"
  suggestedFilename: "sentiment_price_metrics"
---

# Price Metrics API

## 源URL

https://eulerpool.com/developers/api/sentiment/price/metrics

## 描述

Returns price performance statistics including 52-week high/low, moving averages, beta, and YTD return

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/sentiment/price-metrics/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns price metrics |
| 401 | Token not valid |
| 404 | Security not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/sentiment/price-metrics/{identifier}' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
{
  "symbol": "AAPL",
  "52WeekHigh": 199.62,
  "52WeekLow": 124.17,
  "10DayAverageTradingVolume": 53717320,
  "beta": 1.29
}
```

## 文档正文

Returns price performance statistics including 52-week high/low, moving averages, beta, and YTD return

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/sentiment/price-metrics/{identifier}`
