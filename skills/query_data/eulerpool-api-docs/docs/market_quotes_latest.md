---
id: "url-2df5759f"
type: "api"
title: "Latest Quotes"
url: "https://eulerpool.com/developers/api/market/quotes/latest"
description: "Returns the most recent price for one or more tickers"
source: ""
tags: []
crawl_time: "2026-03-18T05:33:51.521Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/market/quotes/latest"
  responses:
    - {"code":"200","description":"Latest price per ticker"}
    - {"code":"401","description":"Invalid or missing API key"}
    - {"code":"404","description":"Resource not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/market/quotes/latest?stocks=US0378331005' \\\n  -H 'Accept: application/json'"
  jsonExample: ""
  suggestedFilename: "market_quotes_latest"
---

# Latest Quotes

## 源URL

https://eulerpool.com/developers/api/market/quotes/latest

## 描述

Returns the most recent price for one or more tickers

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/market/quotes/latest`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Latest price per ticker |
| 401 | Invalid or missing API key |
| 404 | Resource not found |

## 代码示例

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/market/quotes/latest?stocks=US0378331005' \
  -H 'Accept: application/json'
```

## 文档正文

Returns the most recent price for one or more tickers

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/market/quotes/latest`
