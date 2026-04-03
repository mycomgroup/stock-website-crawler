---
id: "url-42828f60"
type: "api"
title: "Options Chain"
url: "https://eulerpool.com/developers/api/market/options"
description: "Returns the full options chain (calls & puts) for a US-listed ticker via CBOE"
source: ""
tags: []
crawl_time: "2026-03-18T05:50:25.611Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/market/options/{ticker}"
  responses:
    - {"code":"200","description":"Options chain grouped by expiration"}
    - {"code":"401","description":"Invalid or missing API key"}
    - {"code":"404","description":"Resource not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/market/options/AAPL' \\\n  -H 'Accept: application/json'"
  jsonExample: "{\n  \"ticker\": \"AAPL\",\n  \"expirations\": {\n    \"expiration_date\": \"2026-03-21T00:00:00.000Z\",\n    \"calls\": [],\n    \"puts\": []\n  }\n}"
  suggestedFilename: "market_options"
---

# Options Chain

## 源URL

https://eulerpool.com/developers/api/market/options

## 描述

Returns the full options chain (calls & puts) for a US-listed ticker via CBOE

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/market/options/{ticker}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Options chain grouped by expiration |
| 401 | Invalid or missing API key |
| 404 | Resource not found |

## 代码示例

### 示例 1 (bash)

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/market/options/AAPL' \
  -H 'Accept: application/json'
```

### 示例 2 (json)

```json
{
  "ticker": "AAPL",
  "expirations": {
    "expiration_date": "2026-03-21T00:00:00.000Z",
    "calls": [],
    "puts": []
  }
}
```

## 文档正文

Returns the full options chain (calls & puts) for a US-listed ticker via CBOE

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/market/options/{ticker}`
