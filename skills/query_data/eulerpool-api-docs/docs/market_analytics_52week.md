---
id: "url-63952438"
type: "api"
title: "52-Week Analytics"
url: "https://eulerpool.com/developers/api/market/analytics/52week"
description: "Returns price range statistics (high, low, position) for a given ticker and time range"
source: ""
tags: []
crawl_time: "2026-03-18T06:08:44.552Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/market/analytics/52week/{ticker}"
  responses:
    - {"code":"200","description":"Range analytics"}
    - {"code":"401","description":"Invalid or missing API key"}
    - {"code":"404","description":"Resource not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/market/analytics/52week/AAPL?range=1y' \\\n  -H 'Accept: application/json'"
  jsonExample: "{\n  \"range\": \"1y\",\n  \"days\": 365,\n  \"low\": 142.5,\n  \"high\": 198.23,\n  \"currentPrice\": 178.72,\n  \"rangePosition\": 65\n}"
  suggestedFilename: "market_analytics_52week"
---

# 52-Week Analytics

## 源URL

https://eulerpool.com/developers/api/market/analytics/52week

## 描述

Returns price range statistics (high, low, position) for a given ticker and time range

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/market/analytics/52week/{ticker}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Range analytics |
| 401 | Invalid or missing API key |
| 404 | Resource not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/market/analytics/52week/AAPL?range=1y' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
{
  "range": "1y",
  "days": 365,
  "low": 142.5,
  "high": 198.23,
  "currentPrice": 178.72,
  "rangePosition": 65
}
```

## 文档正文

Returns price range statistics (high, low, position) for a given ticker and time range

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/market/analytics/52week/{ticker}`
