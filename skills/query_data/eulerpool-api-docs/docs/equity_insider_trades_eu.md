---
id: "url-227b0b1e"
type: "api"
title: "EU Insider Trades (BaFin) API"
url: "https://eulerpool.com/developers/api/equity/insider/trades/eu"
description: "Returns German/EU insider trading disclosures from BaFin (Bundesanstalt fuer Finanzdienstleistungsaufsicht). Unique dataset not available in US-only APIs."
source: ""
tags: []
crawl_time: "2026-03-18T06:11:42.986Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/equity/insider-trades-eu/{identifier}"
  responses:
    - {"code":"200","description":"Returns BaFin insider trades"}
    - {"code":"401","description":"Token not valid"}
    - {"code":"404","description":"Security not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/equity/insider-trades-eu/{identifier}' \\\n  -H 'Accept: application/json'"
  jsonExample: "[\n  {}\n]"
  suggestedFilename: "equity_insider_trades_eu"
---

# EU Insider Trades (BaFin) API

## 源URL

https://eulerpool.com/developers/api/equity/insider/trades/eu

## 描述

Returns German/EU insider trading disclosures from BaFin (Bundesanstalt fuer Finanzdienstleistungsaufsicht). Unique dataset not available in US-only APIs.

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/equity/insider-trades-eu/{identifier}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Returns BaFin insider trades |
| 401 | Token not valid |
| 404 | Security not found |

## 代码示例

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/equity/insider-trades-eu/{identifier}' \
  -H 'Accept: application/json'
```

## 文档正文

Returns German/EU insider trading disclosures from BaFin (Bundesanstalt fuer Finanzdienstleistungsaufsicht). Unique dataset not available in US-only APIs.

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/equity/insider-trades-eu/{identifier}`
