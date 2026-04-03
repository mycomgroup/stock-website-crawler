---
id: "url-23a76ed5"
type: "api"
title: "AlleAktien Fundamentals"
url: "https://eulerpool.com/developers/api/partner/alleaktien/fundamentals"
description: "Batch fundamental metrics for AlleAktien by ISINs (German field names)"
source: ""
tags: []
crawl_time: "2026-03-18T05:37:02.315Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/partner/alleaktien/fundamentals"
  responses:
    - {"code":"200","description":"Fundamental metrics keyed by ISIN"}
    - {"code":"401","description":"Invalid or missing API key"}
    - {"code":"404","description":"Resource not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/partner/alleaktien/fundamentals?isins=US5949181045%2CDE0007164600' \\\n  -H 'Accept: application/json'"
  jsonExample: ""
  suggestedFilename: "partner_alleaktien_fundamentals"
---

# AlleAktien Fundamentals

## 源URL

https://eulerpool.com/developers/api/partner/alleaktien/fundamentals

## 描述

Batch fundamental metrics for AlleAktien by ISINs (German field names)

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/partner/alleaktien/fundamentals`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Fundamental metrics keyed by ISIN |
| 401 | Invalid or missing API key |
| 404 | Resource not found |

## 代码示例

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/partner/alleaktien/fundamentals?isins=US5949181045%2CDE0007164600' \
  -H 'Accept: application/json'
```

## 文档正文

Batch fundamental metrics for AlleAktien by ISINs (German field names)

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/partner/alleaktien/fundamentals`
