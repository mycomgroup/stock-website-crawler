---
id: "url-69f485f0"
type: "api"
title: "Mutual Fund Countries"
url: "https://eulerpool.com/developers/api/mutual/fund/countries"
description: "Returns geographic allocation breakdown"
source: ""
tags: []
crawl_time: "2026-03-18T06:04:42.577Z"
metadata:
  requestMethod: "GET"
  endpoint: "/api/1/mutual-fund/countries/{symbol}"
  responses:
    - {"code":"200","description":"Country breakdown"}
    - {"code":"401","description":"Invalid or missing API key"}
    - {"code":"404","description":"Resource not found"}
  curlExample: "curl -X GET \\\n  'https://api.eulerpool.com/api/1/mutual-fund/countries/VFINX' \\\n  -H 'Accept: application/json'"
  jsonExample: ""
  suggestedFilename: "mutual_fund_countries"
---

# Mutual Fund Countries

## 源URL

https://eulerpool.com/developers/api/mutual/fund/countries

## 描述

Returns geographic allocation breakdown

## API 端点

**Method**: `GET`
**Endpoint**: `/api/1/mutual-fund/countries/{symbol}`

## 响应状态

| 状态码 | 描述 |
|--------|------|
| 200 | Country breakdown |
| 401 | Invalid or missing API key |
| 404 | Resource not found |

## 代码示例

```bash
curl -X GET \
  'https://api.eulerpool.com/api/1/mutual-fund/countries/VFINX' \
  -H 'Accept: application/json'
```

## 文档正文

Returns geographic allocation breakdown

## API 端点

**Method:** `GET`
**Endpoint:** `/api/1/mutual-fund/countries/{symbol}`
