---
id: "url-616e12d0"
type: "api"
title: "FX Rate Series"
url: "https://eulerpool.com/developers/api/market/fx"
description: "Returns historical exchange rates between two currencies"
source: ""
tags: []
crawl_time: "2026-03-18T05:39:41.135Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/market/fx/{from}/{to}"
  responses:
    - {"code":"200","description":"FX rate time series"}
    - {"code":"401","description":"Invalid or missing API key"}
    - {"code":"404","description":"Resource not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/market/fx/EUR/USD?range=1y' \\\n  -H 'Accept: application/json'"
  jsonExample: "{\n  \"from\": \"EUR\",\n  \"to\": \"USD\",\n  \"range\": \"1y\",\n  \"rates\": []\n}"
  suggestedFilename: "market_fx"
---

# FX Rate Series

## 源URL

https://eulerpool.com/developers/api/market/fx

## 描述

Returns historical exchange rates between two currencies

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/market/fx/{from}/{to}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | FX rate time series |
| 401 | Invalid or missing API key |
| 404 | Resource not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/market/fx/EUR/USD?range=1y' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
{
  "from": "EUR",
  "to": "USD",
  "range": "1y",
  "rates": []
}
```

## 文档正文

Returns historical exchange rates between two currencies

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/market/fx/{from}/{to}`
