---
id: "url-beb0d67"
type: "api"
title: "Market Holidays"
url: "https://eulerpool.com/developers/api/market/holidays"
description: "Returns the full exchange holiday schedule including early-close days. Currently covers US exchanges (NYSE/NASDAQ). Updated monthly."
source: ""
tags: []
crawl_time: "2026-03-18T05:53:44.316Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/market/holidays"
  responses:
    - {"code":"200","description":"Exchange holiday schedule"}
    - {"code":"401","description":"Invalid or missing API key"}
    - {"code":"404","description":"Resource not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/market/holidays' \\\n  -H 'Accept: application/json'"
  jsonExample: "{\n  \"exchange\": \"US\",\n  \"holidays\": {\n    \"date\": \"2025-07-04T00:00:00.000Z\",\n    \"eventName\": \"Independence Day\",\n    \"tradingHour\": \"\",\n    \"postMarket\": \"\"\n  }\n}"
  suggestedFilename: "market_holidays"
---

# Market Holidays

## 源URL

https://eulerpool.com/developers/api/market/holidays

## 描述

Returns the full exchange holiday schedule including early-close days. Currently covers US exchanges (NYSE/NASDAQ). Updated monthly.

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/market/holidays`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Exchange holiday schedule |
| 401 | Invalid or missing API key |
| 404 | Resource not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/market/holidays' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
{
  "exchange": "US",
  "holidays": {
    "date": "2025-07-04T00:00:00.000Z",
    "eventName": "Independence Day",
    "tradingHour": "",
    "postMarket": ""
  }
}
```

## 文档正文

Returns the full exchange holiday schedule including early-close days. Currently covers US exchanges (NYSE/NASDAQ). Updated monthly.

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/market/holidays`
