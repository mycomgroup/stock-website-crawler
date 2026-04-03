---
id: "url-554f69ad"
type: "api"
title: "Currency-Adjusted Returns"
url: "https://eulerpool.com/developers/api/market/analytics/fx/returns"
description: "Returns stock performance adjusted for currency fluctuations"
source: ""
tags: []
crawl_time: "2026-03-18T06:13:14.923Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/market/analytics/fx-returns/{identifier}"
  responses:
    - {"code":"200","description":"Currency-adjusted return data"}
    - {"code":"401","description":"Invalid or missing API key"}
    - {"code":"404","description":"Resource not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/market/analytics/fx-returns/{identifier}?range=1y&currency=EUR' \\\n  -H 'Accept: application/json'"
  jsonExample: "{\n  \"isin\": \"US5949181045\",\n  \"stockCurrency\": \"USD\",\n  \"targetCurrency\": \"EUR\",\n  \"range\": \"1y\",\n  \"returnLocal\": 15.3,\n  \"returnTarget\": 12.1,\n  \"fxImpact\": -3.2\n}"
  suggestedFilename: "market_analytics_fx_returns"
---

# Currency-Adjusted Returns

## 源URL

https://eulerpool.com/developers/api/market/analytics/fx/returns

## 描述

Returns stock performance adjusted for currency fluctuations

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/market/analytics/fx-returns/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Currency-adjusted return data |
| 401 | Invalid or missing API key |
| 404 | Resource not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/market/analytics/fx-returns/{identifier}?range=1y&currency=EUR' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
{
  "isin": "US5949181045",
  "stockCurrency": "USD",
  "targetCurrency": "EUR",
  "range": "1y",
  "returnLocal": 15.3,
  "returnTarget": 12.1,
  "fxImpact": -3.2
}
```

## 文档正文

Returns stock performance adjusted for currency fluctuations

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/market/analytics/fx-returns/{identifier}`
