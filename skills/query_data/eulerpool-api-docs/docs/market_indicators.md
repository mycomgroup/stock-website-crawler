---
id: "url-61e72c42"
type: "api"
title: "Market Indicators"
url: "https://eulerpool.com/developers/api/market/indicators"
description: "Returns market-wide indicators (VIX, Put/Call ratio, etc.) for the last N days"
source: ""
tags: []
crawl_time: "2026-03-18T05:58:01.428Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/market/indicators"
  responses:
    - {"code":"200","description":"Market indicators grouped by name"}
    - {"code":"401","description":"Invalid or missing API key"}
    - {"code":"404","description":"Resource not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/market/indicators?days=30' \\\n  -H 'Accept: application/json'"
  jsonExample: ""
  suggestedFilename: "market_indicators"
---

# Market Indicators

## 源URL

https://eulerpool.com/developers/api/market/indicators

## 描述

Returns market-wide indicators (VIX, Put/Call ratio, etc.) for the last N days

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/market/indicators`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Market indicators grouped by name |
| 401 | Invalid or missing API key |
| 404 | Resource not found |

## 代码示例

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/market/indicators?days=30' \
  -H 'Accept: application/json'
```

## 文档正文

Returns market-wide indicators (VIX, Put/Call ratio, etc.) for the last N days

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/market/indicators`
