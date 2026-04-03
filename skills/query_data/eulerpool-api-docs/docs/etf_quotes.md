---
id: "url-4c178fc"
type: "api"
title: "ETF Quotes API"
url: "https://eulerpool.com/developers/api/etf/quotes"
description: "Returns historical quotes for the given ETF identifier and timeframe. Dates are in milliseconds since 1970."
source: ""
tags: []
crawl_time: "2026-03-18T05:40:01.042Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/etf/quotes/{identifier}"
  responses:
    - {"code":"200","description":"Returns ETF quotes"}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Security not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/etf/quotes/{identifier}?startdate=1704067200000&enddate=1735689600000' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {}\n]"
  suggestedFilename: "etf_quotes"
---

# ETF Quotes API

## 源URL

https://eulerpool.com/developers/api/etf/quotes

## 描述

Returns historical quotes for the given ETF identifier and timeframe. Dates are in milliseconds since 1970.

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/etf/quotes/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns ETF quotes |
| 401 | Token not valid |
| 404 | Security not found |

## 代码示例

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/etf/quotes/{identifier}?startdate=1704067200000&enddate=1735689600000' \
  -H 'Accept: application/json'
```

## 文档正文

Returns historical quotes for the given ETF identifier and timeframe. Dates are in milliseconds since 1970.

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/etf/quotes/{identifier}`
