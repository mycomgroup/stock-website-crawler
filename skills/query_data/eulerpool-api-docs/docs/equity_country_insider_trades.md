---
id: "url-1b5bbdb6"
type: "api"
title: "Country Insider Trades API"
url: "https://eulerpool.com/developers/api/equity/country/insider/trades"
description: "Returns insider trading activity across all companies in a given country (e.g. DE for Germany/BaFin, US for SEC)"
source: ""
tags: []
crawl_time: "2026-03-18T06:14:19.597Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/equity/country-insider-trades/{country}"
  responses:
    - {"code":"200","description":"Returns country-level insider trades."}
    - {"code":"401","description":"Token not valid"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/equity/country-insider-trades/US' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {}\n]"
  suggestedFilename: "equity_country_insider_trades"
---

# Country Insider Trades API

## 源URL

https://eulerpool.com/developers/api/equity/country/insider/trades

## 描述

Returns insider trading activity across all companies in a given country (e.g. DE for Germany/BaFin, US for SEC)

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/equity/country-insider-trades/{country}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns country-level insider trades. |
| 401 | Token not valid |

## 代码示例

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/equity/country-insider-trades/US' \
  -H 'Accept: application/json'
```

## 文档正文

Returns insider trading activity across all companies in a given country (e.g. DE for Germany/BaFin, US for SEC)

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/equity/country-insider-trades/{country}`
